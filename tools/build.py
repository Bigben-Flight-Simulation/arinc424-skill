"""Build the machine-readable specification database used by the skill.

    python tools/build.py [--force]

Writes ``data/arinc424.json``:

    {
      "meta":    {...},                  # editions, page counts, provenance
      "records": {...},                  # record groups, per-edition layouts
      "fields":  {...},                  # field definitions, per-edition index
      "codes":   {...}                   # code tables derived from the Rust model
    }
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
DATA = SKILL_ROOT / "data"

sys.path.insert(0, str(HERE))

from pdfparse import VERSIONS, summarise  # noqa: E402
import rustparse  # noqa: E402


def build_records(specs: dict[str, dict]) -> dict:
    """Record groups keyed by section number, with one layout set per edition."""
    groups: dict[str, dict] = {}
    for version in VERSIONS:
        for group in specs[version]["groups"]:
            entry = groups.setdefault(
                group["number"],
                {"number": group["number"], "title": "", "record_codes": [], "editions": {}},
            )
            if group["title"]:
                entry["title"] = group["title"]
            if group["record_codes"]:
                entry["record_codes"] = group["record_codes"]
            layouts = {}
            for sub in group["subsections"]:
                layouts[sub["number"]] = {
                    "title": sub["title"],
                    "page": sub["page_start"],
                    "deleted_by": sub["deleted_by"],
                    "prose": sub["prose"],
                    "notes": sub["notes"],
                    "fields": [
                        {
                            "start": f["start"],
                            "end": f["end"],
                            "length": f["length"],
                            "name": f["name"],
                            "reference": f["reference"],
                            "spec": f["spec"],
                            "note": f["note"],
                            "declared_length": f["declared_length"],
                        }
                        for f in sub["fields"]
                    ],
                }
            entry["editions"][version] = layouts
    return groups


def build_fields(specs: dict[str, dict]) -> dict:
    """Field definitions: prose and tables from the newest edition, an index for all."""
    latest = VERSIONS[-1]
    fields: dict[str, dict] = {}
    for field in specs[latest]["fields"]:
        fields[field["number"]] = {
            "number": field["number"],
            "name": field["name"],
            "abbreviation": field["abbreviation"],
            "prose": field["prose"],
            "tables": field["tables"],
            "editions": {latest: {"name": field["name"], "abbreviation": field["abbreviation"], "page": field["page_start"]}},
        }
    for version in VERSIONS:
        for field in specs[version]["fields"]:
            entry = fields.setdefault(
                field["number"],
                {
                    "number": field["number"],
                    "name": field["name"],
                    "abbreviation": field["abbreviation"],
                    "prose": "",
                    "tables": [],
                    "editions": {},
                },
            )
            entry["editions"][version] = {
                "name": field["name"],
                "abbreviation": field["abbreviation"],
                "page": field["page_start"],
            }
    return fields


SUSPECT = re.compile(r"^[\(\)\d\s]*$")


def repair_names(groups: dict[str, dict]) -> int:
    """Borrow a field name from another edition when this one lost it.

    A handful of cells wrap so badly that nothing on the row survives but the
    length ("(100)"). The same column in a neighbouring edition almost always
    still carries the name.
    """
    repaired = 0
    by_number: dict[str, list[dict]] = {}
    for group in groups.values():
        for layouts in group["editions"].values():
            for layout_number, layout in layouts.items():
                by_number.setdefault(layout_number, []).append(layout)

    for layout_number, layouts in by_number.items():
        for layout in layouts:
            for field in layout["fields"]:
                if not SUSPECT.match(field["name"]):
                    continue
                for other in layouts:
                    if other is layout:
                        continue
                    for candidate in other["fields"]:
                        if SUSPECT.match(candidate["name"]):
                            continue
                        if candidate["start"] == field["start"] and candidate["end"] == field["end"]:
                            field["name"] = candidate["name"]
                            field["reference"] = field["reference"] or candidate["reference"]
                            field["spec"] = field["spec"] or candidate["spec"]
                            repaired += 1
                            break
                    if not SUSPECT.match(field["name"]):
                        break
                if SUSPECT.match(field["name"]):
                    field["name"] = "Unnamed"
                    field["unnamed"] = True
    return repaired


def main() -> None:
    force = "--force" in sys.argv
    specs = {}
    for version in VERSIONS:
        print(f"reading ARINC 424-{version} ...", flush=True)
        specs[version] = summarise(version, force)

    records = build_records(specs)
    repaired = repair_names(records)

    payload = {
        "meta": {
            "editions": VERSIONS,
            "latest": VERSIONS[-1],
            "pages": {v: specs[v]["pages"] for v in VERSIONS},
            "source": "ARINC 424-18 ... 424-23 (docs/)",
        },
        "records": records,
        "fields": build_fields(specs),
        "model": rustparse.parse_model_records(rustparse.MODEL_ROOT),
    }
    # Code tables are matched against the field names, so they come last.
    payload["codes"] = rustparse.build_codes(payload["fields"])

    DATA.mkdir(exist_ok=True)
    out = DATA / "arinc424.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    size = out.stat().st_size / 1024
    print(
        f"wrote {out.relative_to(SKILL_ROOT)} "
        f"({size:.0f} KB, {len(payload['records'])} record groups, "
        f"{len(payload['fields'])} fields, {len(payload['codes'])} code tables, "
        f"{repaired} names recovered)"
    )


if __name__ == "__main__":
    main()
