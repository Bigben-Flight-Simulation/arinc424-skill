"""Derive ARINC 424 code tables from the Rust model instead of the PDFs.

The ``arinc424-core`` crate already encodes every enumerated field as a Rust
enum whose ``from_char`` / ``from_str`` arms are the authoritative code table,
and whose variant names carry the meaning (``'A' => AirportAsWaypoint``). That
is both cleaner and more complete than the flattened tables in the PDF, so the
skill takes its code tables from here.

Field numbers come from the ``// 5.NN Name (ABBREV)`` comment at the top of each
module; modules without one are matched by name against the parsed spec, with a
small alias table for the ones whose Rust name differs from the spec name.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
DEFAULT_MODEL_ROOT = Path(r"D:/FlightSimulation/Coding/arinc424-model-rs")

def _model_root() -> Path:
    """Where arinc424-model-rs lives.

    Only ``python rustparse.py <path>`` hands a path on the command line; when
    this module is imported the positional argument belongs to whoever imported
    us (``build.py --force``, for one) and must not be mistaken for a path.
    """
    if __name__ == "__main__" and len(sys.argv) > 1:
        return Path(sys.argv[1])
    return DEFAULT_MODEL_ROOT


MODEL_ROOT = _model_root()
DATA_TYPES = MODEL_ROOT / "crates/arinc424-core/src/data_types"

HEADER = re.compile(r"^//\s*(5\.\d+)\s+(.+?)(?:\s*\(([^)]*)\))?\s*$")
IMPL = re.compile(r"impl\s+Arinc(Code|StrCode)\s+for\s+(\w+)")
CHAR_ARM = re.compile(r"'(\\?.)'\s*=>\s*(?:Self::|(\w+)::)?(\w+)\s*,")
STR_ARM = re.compile(r'"([^"]*)"\s*=>\s*(?:Self::|(\w+)::)?(\w+)\s*,')
POSITION = re.compile(r"col_(\d+)")

#: Rust module name -> spec field name, for modules that carry no 5.NN header.
ALIASES = {
    "cust_area": "Customer/Area Code",
    "record_type": "Record Type",
    "section_code": "Section Code",
    "subs_code": "Subsection Code",
    "navaid_class": "NAVAID Class",
    "navaid_limitation_code": "Navaid Limitation Code",
    "ndb_facility_characteristics": "Facility Characteristics",
    "route_type": "Route Type",
    "waypoint_type": "Waypoint Type",
    "waypoint_usage": "Waypoint Usage",
    "waypoint_description_code": "Waypoint Description Code",
    "turn_direction": "Turn Direction",
    "application_type": "Continuation Record Application Type",
    "duplicate_indicator": "Duplicate Indicator",
    "figure_of_merit": "Figure of Merit",
    "mag_var": "Magnetic Variation",
    "name_format_indicator": "Name Format Indicator",
    "start_end_indicator": "Start/End Indicator",
    "start_end_date_time": "Start/End Date",
    "time_zone": "Time Zone",
    "altitude": "Altitude/Minimum Altitude",
    "combined_sect_code": "Section Code",
}

# Module -> explicit field number, for enums whose name no longer exists.
NUMBER_OVERRIDES = {
    "figure_of_merit": "5.149",  # renamed "Navaid Usable Range" in later editions
}

SKIP = {"mod", "tables"}


def normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def camel_words(name: str) -> str:
    """``VhfNavaidType1`` -> ``Vhf Navaid Type1``."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)
    return re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", spaced)


def unescape(value: str) -> str:
    return value.replace("\\t", "\t").replace("\\ ", " ").replace("\\\\", "\\")


def parse_file(path: Path) -> list[dict]:
    """Every ``ArincCode``/``ArincStrCode`` enum in one module."""
    text = path.read_text(encoding="utf-8", errors="replace")
    match = HEADER.match(text.splitlines()[0].strip()) if text.strip() else None
    header = (match.group(1), match.group(2).strip(), (match.group(3) or "").strip()) if match else None

    tables = []
    for match in IMPL.finditer(text):
        kind, enum_name = match.group(1), match.group(2)
        body = text[match.end() :]
        stop = body.find("\nimpl ")
        chunk = body[: stop if stop > 0 else len(body)]

        entries = []
        if kind == "Code":
            for arm in CHAR_ARM.finditer(chunk):
                raw, _, variant = arm.groups()
                entries.append({"code": unescape(raw), "variant": variant})
        else:
            for arm in STR_ARM.finditer(chunk):
                raw, _, variant = arm.groups()
                entries.append({"code": unescape(raw), "variant": variant})

        entries = [e for e in entries if e["variant"] not in {"Other", "Unknown"}]
        if entries:
            tables.append(
                {
                    "enum": enum_name,
                    "module": path.stem,
                    "header": header,
                    "entries": entries,
                }
            )
    return tables


def collect(model_root: Path) -> list[dict]:
    root = model_root / "crates/arinc424-core/src/data_types"
    if not root.exists():
        raise SystemExit(f"data_types not found under {model_root}")
    tables = []
    for path in sorted(root.rglob("*.rs")):
        if path.stem in SKIP:
            continue
        for table in parse_file(path):
            relative = path.relative_to(root).with_suffix("")
            parts = list(relative.parts)
            position = None
            for part in reversed(parts):
                found = POSITION.fullmatch(part)
                if found:
                    position = int(found.group(1))
                    break
            table["position"] = position
            table["path"] = "::".join(parts)
            # Closest enclosing module first: col_28.rs inside
            # navaid_class/vhf_class/ belongs to navaid_class.
            ancestors = parts[:-1] if POSITION.fullmatch(parts[-1]) else parts
            table["modules"] = list(reversed(ancestors))
            tables.append(table)
    return tables


def resolve_field(table: dict, fields: dict[str, dict]) -> str | None:
    if table["header"]:
        return table["header"][0]

    # A few enums predate the current field name: the spec renamed Figure of
    # Merit to Navaid Usable Range but the Rust module kept the old word.
    override = NUMBER_OVERRIDES.get(table["path"].split("::")[-1])
    if override and override in fields:
        return override

    for module in table.get("modules", []):
        alias = ALIASES.get(module)
        if not alias:
            continue
        key = normalise(alias)
        for number, field in fields.items():
            if normalise(field["name"]) == key:
                return number

    key = normalise(camel_words(table["enum"]))
    best = None
    for number, field in fields.items():
        field_key = normalise(field["name"])
        if not field_key:
            continue
        if field_key in key or key in field_key:
            score = len(field_key)
            if best is None or score > best[1]:
                best = (number, score)
    return best[0] if best else None


def build_codes(fields: dict[str, dict] | None = None) -> dict:
    if fields is None:
        fields_path = SKILL_ROOT / "data/arinc424.json"
        fields = {}
        if fields_path.exists():
            fields = json.loads(fields_path.read_text(encoding="utf-8")).get("fields", {})

    tables = collect(MODEL_ROOT)
    grouped: dict[str, dict] = {}
    unresolved = []

    for table in tables:
        number = resolve_field(table, fields)
        if not number:
            unresolved.append(table["path"])
            continue
        field = fields.get(number) or {}
        entry = grouped.setdefault(
            number,
            {
                # The spec's own wording wins over the Rust file header, which
                # is only a transcription of it.
                "name": field.get("name") or (table["header"][1] if table["header"] else table["module"]),
                "abbreviation": field.get("abbreviation") or "",
                "groups": [],
            },
        )
        if not entry["abbreviation"] and table["header"] and table["header"][2]:
            entry["abbreviation"] = table["header"][2]
        entry["groups"].append(
            {
                "position": table["position"],
                "enum": table["enum"],
                "source": f"arinc424-core::data_types::{table['path']}",
                "entries": table["entries"],
            }
        )

    for entry in grouped.values():
        entry["groups"].sort(key=lambda g: (g["position"] is not None, g["position"] or 0, g["enum"]))

    if unresolved:
        print(f"  unresolved code tables ({len(unresolved)}): {', '.join(sorted(unresolved)[:12])}", file=sys.stderr)
    return grouped


if __name__ == "__main__":
    codes = build_codes()
    print(f"{len(codes)} fields carry code tables, {sum(len(v['groups']) for v in codes.values())} tables")
    for number in list(codes)[:5]:
        print(number, codes[number]["name"], codes[number]["abbreviation"])


# --------------------------------------------------------------------------- #
# Record structs
# --------------------------------------------------------------------------- #

MODEL_RECORD = re.compile(r"#\[arinc_record\(mappings\s*=\s*\[([^\]]*)\]\)\]")
MODEL_CONT = re.compile(r"#\[arinc_record_continuation\((.*?)\)\]", re.DOTALL)
STRUCT = re.compile(r"pub struct (\w+)")
ARINC_FIELD = re.compile(
    r"#\[arinc\(start\s*=\s*(\d+),\s*end\s*=\s*(\d+)[^\]]*\)\]\s*(?:pub\s+)?(\w+)\s*:\s*([\w:<>, ]+)",
    re.DOTALL,
)
MAPPING = re.compile(r"\(\s*'(.|\s)'\s*,\s*'(.|\s)'\s*,\s*(\d+)\s*\)")


def parse_model_records(model_root: Path) -> list[dict]:
    """The record structs declared in ``arinc424-core``, with their column map."""
    root = model_root / "crates/arinc424-core/src/model"
    out = []
    for path in sorted(root.rglob("*.rs")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for block in re.split(r"\n(?=#\[derive)", text):
            struct = STRUCT.search(block)
            if not struct:
                continue
            fields = [
                {
                    "start": int(m.group(1)),
                    "end": int(m.group(2)),
                    "name": m.group(3),
                    "type": m.group(4).strip(),
                }
                for m in ARINC_FIELD.finditer(block)
            ]
            if not fields:
                continue

            entry = {
                "struct": struct.group(1),
                "file": str(path.relative_to(model_root)).replace("\\", "/"),
                "kind": "continuation" if MODEL_CONT.search(block) else "primary",
                "mappings": [],
                "fields": fields,
            }
            record = MODEL_RECORD.search(block)
            if record:
                entry["mappings"] = [
                    {"section": m.group(1), "subsection": m.group(2), "position": int(m.group(3))}
                    for m in MAPPING.finditer(record.group(1))
                ]
            cont = MODEL_CONT.search(block)
            if cont:
                body = cont.group(1)
                entry["continuation_pos"] = _int_attr(body, "continuation_pos")
                entry["base_start"] = _int_attr(body, "base_start")
                entry["base_end"] = _int_attr(body, "base_end")
                type_match = re.search(r"cont_type\s*=\s*'(.)'", body)
                entry["cont_type"] = type_match.group(1) if type_match else None
                entry["primaries"] = re.findall(r"(\w+Record|\w+Primary)\s*,?\s*\n", body)
            out.append(entry)
    return out


def _int_attr(body: str, name: str) -> int | None:
    match = re.search(rf"{name}\s*=\s*(\d+)", body)
    return int(match.group(1)) if match else None
