#!/usr/bin/env python3
"""arinc424 -- look things up in the ARINC 424 specification database.

Zero dependencies, Python 3.8+.

    arinc424.py decode "SBBBBAAAD..."          # 132-column line -> fields
    arinc424.py encode 4.1.2.1 col7=EGLL col14=VOR
    arinc424.py record 4.1.9.1                 # layout, all editions
    arinc424.py field 5.17                     # definition + code table
    arinc424.py codes 5.17
    arinc424.py diff 4.1.2.1 --from 18 --to 23
    arinc424.py search "waypoint description"
    arinc424.py list records|fields|codes
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "arinc424.json"
DB: dict | None = None

LINE_WIDTH = 132


def load() -> dict:
    global DB
    if DB is None:
        if not DATA.exists():
            sys.exit(f"specification database missing: {DATA}\nrun tools/build.py first")
        DB = json.loads(DATA.read_text(encoding="utf-8"))
    return DB


def editions() -> list[str]:
    return load()["meta"]["editions"]


def latest() -> str:
    return load()["meta"]["latest"]


# --------------------------------------------------------------------------- #
# Record layout lookup
# --------------------------------------------------------------------------- #


def all_records() -> dict[str, dict]:
    return load()["records"]


def resolve_record(query: str, version: str | None = None) -> tuple[str, dict]:
    """Accept ``4.1.2.1``, ``4.1.2`` or a record code such as ``PD``."""
    records = all_records()
    version = version or latest()

    if query in records:
        group = records[query]
        layouts = group["editions"].get(version) or group["editions"][latest()]
        return query, layouts

    for number, group in records.items():
        layouts = group["editions"].get(version) or {}
        if query in layouts:
            return number, {query: layouts[query]}

    code = query.upper()
    matches = [n for n, g in records.items() if code in [c.upper() for c in g["record_codes"]]]
    if len(matches) == 1:
        group = records[matches[0]]
        return matches[0], group["editions"].get(version) or group["editions"][latest()]

    needle = query.lower()
    fuzzy = [n for n, g in records.items() if needle in g["title"].lower()]
    if len(fuzzy) == 1:
        group = records[fuzzy[0]]
        return fuzzy[0], group["editions"].get(version) or group["editions"][latest()]

    sys.exit(f"unknown record {query!r}; try `arinc424.py list records`")


def layout_code_columns(layout: dict) -> tuple[int, int | None, int | None, int | None]:
    """(section col, subsection col, continuation col, application col).

    The subsection does not live at column 6 everywhere: procedure records
    carry it at column 13, and continuation records add an application-type
    letter of their own. Reading the columns from the layout keeps `decode`
    correct for every family without special cases.
    """
    section = subsection = continuation = application = None
    for field in layout["fields"]:
        name = field["name"].lower()
        # Some tables print a bare "Section"/"Subsection" instead of
        # "Section Code"; both spellings have to be recognised or the layout
        # filter silently lets a neighbouring record family through.
        if section is None and (name == "section" or name.startswith("section code")):
            section = field["start"]
        elif subsection is None and name.startswith("subsection"):
            subsection = field["start"]
        elif continuation is None and name.startswith("continuation record"):
            continuation = field["start"]
        elif application is None and name.startswith("application type"):
            application = field["start"]
    return section or 5, subsection, continuation, application


def cell(line: str, column: int | None) -> str:
    return line[column - 1 : column] if column else ""


APPLICATION_SPEC = "5.91"
# Words that appear in nearly every layout title and carry no signal.
TITLE_NOISE = {
    "airport",
    "airports",
    "record",
    "records",
    "continuation",
    "primary",
    "and",
    "heliport",
    "heliports",
    "data",
}


def application_letter(layout: dict, column: int | None = None) -> str | None:
    """The application-type letter a continuation record answers to.

    Some layout rows spell it out (``Application Type (1)
    L-Vhf Navaid Limitation Continuation 5.91``). When they do not, the letter
    is recovered from field 5.91's own code table by matching the layout title
    against the meaning of each letter -- "Flight Planning Continuation" is the
    layout that answers to `P`.
    """
    for field in layout["fields"]:
        if not field["name"].lower().startswith("application type"):
            continue
        if column is not None and field["start"] != column:
            continue
        match = re.match(r"\s*([A-Z])\s*[-:]", field.get("reference") or "")
        if match:
            return match.group(1)

    table = code_table(APPLICATION_SPEC)
    if not table:
        return None
    title = re.sub(r"[^a-z ]", " ", layout["title"].lower()).split()
    wanted = {word for word in title if word not in TITLE_NOISE}
    if not wanted:
        return None

    best: tuple[float, str] | None = None
    runner_up = 0.0
    for group in table["groups"]:
        for entry in group["entries"]:
            # Variants come from Rust identifiers ("FlightPlanningContinuation").
            spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", entry["variant"])
            meaning = re.sub(r"[^a-z ]", " ", spaced.lower()).split()
            useful = {word for word in meaning if word not in TITLE_NOISE}
            if not useful:
                continue
            matches = len(wanted & useful)
            # Share of the letter's meaning that the title covers, with the
            # generic words counted at half weight so that
            # "Flight Planning Continuation" beats "Flight Planning Primary
            # Data Continuation" for a title that only says "Flight Planning".
            ratio = matches / (len(useful) + 0.5 * (len(meaning) - len(useful)))
            if ratio < 0.5:
                continue
            if best is None or ratio > best[0]:
                runner_up = best[0] if best else 0.0
                best = (ratio, entry["code"])
            elif ratio > runner_up:
                runner_up = ratio
    if best is None or runner_up >= best[0]:
        return None
    return best[1]


def sort_key(number: str) -> tuple:
    """Compare section numbers numerically: 4.1.9.1 before 4.1.20.2."""
    return tuple(int(part) if part.isdigit() else part for part in number.split("."))


def is_primary_layout(layout: dict) -> bool:
    """A layout that declares the record from column 1.

    Continuations and extensions open with "Fields as on Primary Records", so
    the title alone is not enough -- 4.1.20.2 is an extension that never says
    so in its name.
    """
    title = layout["title"].lower()
    if "continuation" in title or "extension" in title:
        return False
    first = layout["fields"][0] if layout["fields"] else None
    if first and "as on primary" in first["name"].lower():
        return False
    return True


def detect_layout(line: str, version: str) -> tuple[str, dict]:
    """Pick the layout that actually matches this record's own code columns."""
    records = all_records()
    section_char = line[4:5]

    candidates: list[tuple[int, str, dict]] = []
    # Groups that answer to this section letter but not to the subsection
    # actually present in the line -- kept so the failure message can name the
    # offending column instead of only the section.
    subsection_seen: dict[int, tuple[str, set[str]]] = {}
    for group_number, group in records.items():
        layouts = group["editions"].get(version) or {}
        codes = [code for code in (group["record_codes"] or []) if code]
        if not any(code[0] == section_char for code in codes):
            continue
        # Subsections the group answers to. A group recorded only by its
        # section letter ("D") accepts nothing but a blank subsection -- that
        # single rule keeps an NDB record ('DB') from decoding as a VHF one.
        named = {code[1:] for code in codes if len(code) >= 2}
        subsections = named or {" "}
        specificity = 2 if named else 1
        # Continuation layouts open with "Fields as on Primary Records" and so
        # carry no code columns of their own; they inherit them from the
        # group's primary layout.
        inherited = None
        for layout in layouts.values():
            if is_primary_layout(layout):
                inherited = layout_code_columns(layout)
                break
        if inherited is None:
            inherited = (5, None, None, None)

        for layout_number, layout in layouts.items():
            own = layout_code_columns(layout)
            # "Fields as on Primary Records" marks a layout that inherits its
            # code columns; any Section Code further along the record belongs
            # to a referenced navaid, not to the record itself.
            inherits = any(
                "as on primary" in field["name"].lower() for field in layout["fields"]
            )
            sec_col, sub_col = (inherited[0], inherited[1]) if inherits else (own[0], own[1])
            if cell(line, sec_col) != section_char:
                continue
            if sub_col and cell(line, sub_col) not in subsections:
                seen = subsection_seen.setdefault(sub_col, (cell(line, sub_col), set()))
                seen[1].update(subsections)
                continue
            candidates.append((specificity, layout_number, layout))

    if not candidates:
        known = sorted(
            {code[0] for group in records.values() for code in group["record_codes"] or [] if code}
        )
        # The section letter may well be valid -- it is the subsection beside it
        # that no group answers to. Say which, or the message contradicts the
        # list of known sections printed right after it.
        if subsection_seen:
            detail = "; ".join(
                f"column {col} holds {value!r} but section {section_char!r} accepts "
                f"{', '.join(repr(s) for s in sorted(accepted))}"
                for col, (value, accepted) in sorted(subsection_seen.items())
            )
            sys.exit(
                f"no layout matches section {section_char!r} with that subsection "
                f"in 424-{version} -- {detail}"
            )
        sys.exit(
            f"no layout matches section {section_char!r} in 424-{version}; "
            f"known sections: {known}"
        )

    # The most specific record code wins; ties fall back to layout order.
    candidates.sort(key=lambda item: (-item[0], sort_key(item[1])))
    ordered = [(number, layout) for _, number, layout in candidates]

    # Every candidate is judged by its own columns: a primary layout expects a
    # blank or zero continuation number, a continuation layout expects a number
    # and the application-type letter that names it.
    alternatives: list[tuple[str, dict]] = []
    for layout_number, layout in ordered:
        if not is_primary_layout(layout):
            continue
        _, _, cont_col, _ = layout_code_columns(layout)
        if not cont_col or cell(line, cont_col).strip() in ("", "0"):
            return layout_number, layout

    for layout_number, layout in ordered:
        if is_primary_layout(layout):
            continue
        _, _, cont_col, app_col = layout_code_columns(layout)
        if not cont_col or cell(line, cont_col).strip() in ("", "0"):
            continue
        if app_col and application_letter(layout, app_col):
            if cell(line, app_col) == application_letter(layout, app_col):
                return layout_number, layout
        # Without a letter this layout cannot claim the record; keep looking
        # for one that can, and fall back with a warning if none can.
        alternatives.append((layout_number, layout))

    if len(alternatives) > 1:
        # No letter pinned it down, so say which layouts were in the running
        # rather than silently picking one.
        print(
            "continuation application type does not name a unique layout; "
            "candidates: "
            + ", ".join(f"{number} {layout['title']}" for number, layout in alternatives),
            file=sys.stderr,
        )
    if alternatives:
        return alternatives[0]
    return ordered[0]


# --------------------------------------------------------------------------- #
# Field values
# --------------------------------------------------------------------------- #


def code_table(number: str) -> dict | None:
    return load()["codes"].get(number)


def decode_value(raw: str, spec: str | None, position: int | None = None) -> str | None:
    """Translate a raw field value through the code table, when there is one."""
    if not spec:
        return None
    table = code_table(spec)
    if not table:
        return None

    groups = table["groups"]
    chosen = None
    if position is not None:
        for group in groups:
            if group["position"] == position:
                chosen = group
                break
    if chosen is None:
        chosen = next((g for g in groups if g["position"] is None), None)
    if chosen is None:
        return None

    for entry in chosen["entries"]:
        if entry["code"] == raw:
            return entry["variant"]
    return None


def humanise(variant: str) -> str:
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", variant).strip()


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #


def cmd_decode(args) -> None:
    line = args.line.rstrip("\n")
    if len(line) < LINE_WIDTH and args.pad:
        line = line.ljust(LINE_WIDTH)
    if len(line) != LINE_WIDTH:
        sys.exit(f"expected a {LINE_WIDTH}-character record, got {len(line)}")

    version = args.version or latest()
    number, layout = detect_layout(line, version)

    rows = []
    for field in layout["fields"]:
        raw = line[field["start"] - 1 : field["end"]]
        meaning = decode_value(raw.strip(), field.get("spec"), position=field["start"])
        rows.append(
            {
                "start": field["start"],
                "end": field["end"],
                "columns": f"{field['start']}-{field['end']}",
                "name": field["name"],
                "raw": raw,
                "value": raw.strip(),
                "spec": field.get("spec"),
                "meaning": humanise(meaning) if meaning else None,
            }
        )

    if args.json:
        print(
            json.dumps(
                {"record": number, "layout": layout["title"], "edition": version, "fields": rows},
                ensure_ascii=False,
                indent=1,
            )
        )
        return

    print(f"{number}  {layout['title']}   [ARINC 424-{version}]")
    print("-" * 78)
    for row in rows:
        if args.blank is False and not row["value"] and not row["name"].startswith(("Blank", "Reserved")):
            continue
        meaning = f"  <- {row['meaning']}" if row["meaning"] else ""
        print(f"{row['columns']:>8}  {row['name'][:34]:34}  {row['raw']!r:12}{meaning}")
    if layout.get("notes"):
        print()
        for note in layout["notes"]:
            print(f"  {note}")


def cmd_encode(args) -> None:
    version = args.version or latest()
    number, layout = resolve_record(args.record, version)
    layout_number = next(iter(layout))
    layout = layout[layout_number]

    assignments: dict[str, str] = {}
    for item in args.assign:
        if "=" not in item:
            sys.exit(f"expected col=value, got {item!r}")
        key, value = item.split("=", 1)
        assignments[key.strip()] = value

    line = [" "] * LINE_WIDTH
    used: set[str] = set()
    for field in layout["fields"]:
        if field["name"].lower().startswith(("blank", "reserved")):
            continue
        width = field["end"] - field["start"] + 1
        # An exact column start or an exact field name always wins over a
        # "some column inside this field" match, so that ``30=`` and ``31=``
        # stay distinguishable when 30 names a five-column field.
        key = next(
            (
                candidate
                for predicate in (
                    lambda k: k == str(field["start"]),
                    lambda k: k == field["name"],
                    lambda k: k.isdigit() and field["start"] <= int(k) <= field["end"],
                )
                for candidate in sorted(assignments)
                if candidate not in used and predicate(candidate)
            ),
            None,
        )
        if key is None:
            continue
        used.add(key)
        value = assignments[key]
        if len(value) > width:
            sys.exit(f"{field['name']}: {value!r} is longer than {width} columns")
        line[field["start"] - 1 : field["end"]] = list(value.ljust(width))

    leftover = [k for k in assignments if k not in used]
    if leftover:
        print(f"unknown columns: {', '.join(sorted(leftover))}", file=sys.stderr)
        print("columns for this layout:", file=sys.stderr)
        for field in layout["fields"]:
            print(f"  {field['start']:>3}-{field['end']:<3} {field['name']}", file=sys.stderr)
        sys.exit(1)

    print("".join(line))


def cmd_record(args) -> None:
    version = args.version or latest()
    number, layouts = resolve_record(args.record, version)

    for layout_number, layout in layouts.items():
        print(f"{layout_number}  {layout['title']}   [ARINC 424-{version}]")
        print(f"page {layout['page']}   {len(layout['fields'])} fields")
        if layout.get("deleted_by"):
            print(f"  DELETED by supplement {layout['deleted_by']}")
        print("-" * 78)
        for field in layout["fields"]:
            spec = f"  ({field['spec']})" if field.get("spec") else ""
            print(
                f"{field['start']:>4}-{field['end']:<4} {field['name'][:44]:44} "
                f"{field['length']:>3}{spec}"
            )
        if layout.get("prose"):
            print()
            print(f"  {layout['prose'][:600]}")
        if layout.get("notes"):
            print()
            for note in layout["notes"]:
                print(f"  {note}")
        if not args.quiet:
            others = []
            for edition in editions():
                group = all_records()[number]["editions"].get(edition) or {}
                others.append(f"{edition}:{'y' if layout_number in group else '-'}")
            print()
            print("  editions " + "  ".join(others))
        print()


def cmd_field(args) -> None:
    fields = load()["fields"]
    query = args.query

    entry = fields.get(query)
    if entry is None:
        match = re.fullmatch(r"5\.(\d+)", query)
        if match:
            entry = fields.get(f"5.{match.group(1)}")
    if entry is None:
        needle = query.lower()
        hits = [f for f in fields.values() if needle in f["name"].lower()]
        if len(hits) == 1:
            entry = hits[0]
        elif len(hits) > 1:
            print(f"{len(hits)} fields match {query!r}:")
            for hit in sorted(hits, key=lambda f: int(f["number"].split(".")[1]))[:20]:
                print(f"  {hit['number']:>6}  {hit['name']}")
            return
    if entry is None:
        sys.exit(f"unknown field {query!r}")

    print(f"{entry['number']}  {entry['name']}")
    if entry["abbreviation"]:
        print(f"abbreviation: {entry['abbreviation']}")
    present = [v for v in editions() if v in entry["editions"]]
    missing = [v for v in editions() if v not in entry["editions"]]
    print(f"defined in: {', '.join(present)}" + (f"   absent in: {', '.join(missing)}" if missing else ""))
    print("-" * 78)
    if entry["prose"]:
        print(wrap(entry["prose"]))
    for table in entry.get("tables", []):
        print(f"\n  table, page {table['page']}:")
        for row in table["rows"]:
            print("   " + " | ".join(cell for cell in row if cell))

    codes = code_table(entry["number"])
    if codes:
        print()
        print("  code table (from the Rust model):")
        for group in codes["groups"]:
            label = f"column {group['position']}" if group["position"] else "value"
            print(f"\n    {label}  [{group['enum']}]")
            for item in group["entries"]:
                print(f"      {item['code']!r:6} {humanise(item['variant'])}")

    used = []
    for number, group in all_records().items():
        for layout_number, layout in (group["editions"].get(latest()) or {}).items():
            for field in layout["fields"]:
                if field.get("spec") == entry["number"]:
                    used.append(f"{layout_number} col {field['start']}")
    if used:
        print()
        print("  used by: " + ", ".join(sorted(set(used))[:12]))


def wrap(text: str, width: int = 78) -> str:
    import textwrap

    return textwrap.fill(re.sub(r"\s+", " ", text), width=width)


def cmd_codes(args) -> None:
    codes = code_table(args.query)
    if codes is None:
        sys.exit(f"no code table for {args.query!r}; try `list codes`")
    print(f"{args.query}  {codes['name']}  ({codes['abbreviation']})")
    for group in codes["groups"]:
        label = f"column {group['position']}" if group["position"] else "value"
        print(f"\n{label}   {group['enum']}")
        for item in group["entries"]:
            print(f"  {item['code']!r:6} {humanise(item['variant'])}")


def cmd_diff(args) -> None:
    source, target = args.source, args.target
    fields_db = load()["fields"]

    if args.what.startswith("5."):
        entry = fields_db.get(args.what)
        if entry is None:
            sys.exit(f"unknown field {args.what!r}")
        print(f"{args.what}  {entry['name']}")
        for edition in editions():
            info = entry["editions"].get(edition)
            if info:
                print(f"  424-{edition}: {info['name']}  ({info['abbreviation'] or '-'})  page {info['page']}")
            else:
                print(f"  424-{edition}: -")
        return

    number = args.what if args.what in all_records() else resolve_record(args.what)[0]
    group = all_records()[number]
    print(f"{number}  {group['title']}")
    print()
    for layout_number, changes in compare_layouts(number, source, target).items():
        print(f"{layout_number}")
        if not changes:
            print("   no column changes")
            continue
        for change in changes:
            print(f"   {change}")


def compare_layouts(number: str, source: str, target: str) -> dict[str, list[str]]:
    editions_map = all_records()[number]["editions"]
    left = editions_map.get(source) or {}
    right = editions_map.get(target) or {}
    out: dict[str, list[str]] = {}

    for layout_number in sorted(set(left) | set(right)):
        changes = []
        a, b = left.get(layout_number), right.get(layout_number)
        if a and not b:
            changes.append(f"removed after 424-{source}")
        elif b and not a:
            changes.append(f"added in 424-{target}")
        else:
            left_fields = {f["start"]: f for f in a["fields"]}
            right_fields = {f["start"]: f for f in b["fields"]}
            for start in sorted(set(left_fields) | set(right_fields)):
                fa, fb = left_fields.get(start), right_fields.get(start)
                if fa and not fb:
                    changes.append(f"col {start}: removed {fa['name']!r}")
                elif fb and not fa:
                    changes.append(f"col {start}: added {fb['name']!r} ({fb['length']})")
                elif fa["name"] != fb["name"]:
                    changes.append(f"col {start}: {fa['name']!r} -> {fb['name']!r}")
                elif fa["end"] != fb["end"]:
                    changes.append(f"col {start}: width {fa['length']} -> {fb['length']} ({fb['name']})")
                elif (fa.get("spec") or "") != (fb.get("spec") or ""):
                    changes.append(f"col {start}: reference {fa.get('spec')} -> {fb.get('spec')} ({fb['name']})")
        out[layout_number] = changes
    return out


def stem(word: str) -> str:
    """Crude suffix stripping, enough for ARINC's spelling habits.

    ``terminator``/``termination`` both reduce to ``terminat``, so a search for
    "path terminator" still finds the field named "Path and Termination".
    """
    word = word.lower().strip("()[]{}.,")
    for suffix, replacement in (("ation", "at"), ("ator", "at"), ("ies", "y")):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[: -len(suffix)] + replacement
    if word.endswith("s") and len(word) > 3 and not word.endswith("ss"):
        word = word[:-1]
    return word


def cmd_search(args) -> None:
    """Search record titles, layout columns, field definitions and code tables.

    Words are ANDed, so `path terminator` finds "Path and Termination" even
    though no single line contains the phrase.
    """
    words = [stem(word) for word in args.text.split() if word.strip()]
    data = load()
    hits = 0

    def matches(*parts: str) -> bool:
        haystack = [stem(token) for token in " ".join(p for p in parts if p).split()]
        joined = " ".join(haystack)
        return all(word in joined for word in words)

    for number, group in all_records().items():
        for layout_number, layout in (group["editions"].get(latest()) or {}).items():
            if matches(layout["title"]):
                print(f"layout  {layout_number:10} {layout['title']}")
                hits += 1
            for field in layout["fields"]:
                if matches(field["name"], field.get("reference") or ""):
                    print(
                        f"column  {layout_number:10} "
                        f"{field['start']}-{field['end']} {field['name']}"
                    )
                    hits += 1
                    break
        if matches(group["title"], ",".join(group["record_codes"]), number):
            print(f"record  {number:10} {group['title']}")
            hits += 1

    for number, field in data["fields"].items():
        if matches(field["name"], field.get("abbreviation") or ""):
            print(f"field   {number:10} {field['name']}")
            hits += 1
        elif args.deep and matches(field.get("prose") or ""):
            print(f"field   {number:10} {field['name']}   (in definition)")
            hits += 1

    for number, table in data["codes"].items():
        body = " ".join(
            f"{item['variant']} {item['code']}" for group in table["groups"] for item in group["entries"]
        )
        if matches(table["name"], number, body):
            print(f"codes   {number:10} {table['name']}")
            hits += 1

    if not hits:
        print(f"nothing found for {args.text!r}; try --deep to search definitions")


def cmd_list(args) -> None:
    if args.what == "records":
        for number, group in all_records().items():
            codes = ",".join(group["record_codes"]) or "-"
            print(f"{number:10} {codes:12} {group['title']}")
    elif args.what == "fields":
        for number, field in sorted(load()["fields"].items(), key=lambda kv: int(kv[0].split(".")[1])):
            print(f"{number:8} {(field['abbreviation'] or '-'):18} {field['name']}")
    elif args.what == "codes":
        for number, codes in sorted(load()["codes"].items(), key=lambda kv: int(kv[0].split(".")[1])):
            print(f"{number:8} {codes['name']}")
    else:
        sys.exit("list what? records | fields | codes")


def main() -> None:
    parser = argparse.ArgumentParser(prog="arinc424", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("decode", help="split a 132-column record into fields")
    p.add_argument("line")
    p.add_argument("--version")
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-blank", dest="blank", action="store_false", default=True)
    p.add_argument("--pad", action="store_true", help="pad short lines with blanks")
    p.set_defaults(func=cmd_decode)

    p = sub.add_parser("encode", help="assemble a record from field values")
    p.add_argument("record")
    p.add_argument("assign", nargs="*", metavar="col=value")
    p.add_argument("--version")
    p.set_defaults(func=cmd_encode)

    p = sub.add_parser("record", help="show a record layout")
    p.add_argument("record")
    p.add_argument("--version")
    p.add_argument("--quiet", action="store_true")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("field", help="show a field definition and its codes")
    p.add_argument("query")
    p.set_defaults(func=cmd_field)

    p = sub.add_parser("codes", help="show a code table")
    p.add_argument("query")
    p.set_defaults(func=cmd_codes)

    p = sub.add_parser("diff", help="compare a record or field across editions")
    p.add_argument("what")
    p.add_argument("--from", dest="source", default=editions()[0])
    p.add_argument("--to", dest="target", default=latest())
    p.set_defaults(func=cmd_diff)

    p = sub.add_parser("search", help="find records and fields by name")
    p.add_argument("text")
    p.add_argument("--deep", action="store_true", help="also search definition text")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("list", help="list records, fields or code tables")
    p.add_argument("what", nargs="?", default="records")
    p.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
