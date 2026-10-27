"""End-to-end checks for the ARINC 424 skill.

Run after ``tools/build.py`` and ``tools/render.py``:

    python tests/acceptance.py

Every check exits non-zero on the first failure. The point is that the JSON
database, the CLI and the rendered markdown never drift apart.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "arinc424.json"
CLI = ROOT / "scripts" / "arinc424.py"
REFERENCES = ROOT / "references"
LINE_WIDTH = 132

failures: list[str] = []
checks = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(f"{name}: {detail}")
        print(f"  FAIL  {name}  {detail}")
    else:
        print(f"  ok    {name}")


def run(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=ROOT,
    )
    if result.returncode != 0:
        raise AssertionError(f"{' '.join(args)} failed: {result.stderr.strip()[:300]}")
    return result.stdout


def main() -> int:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    records = payload["records"]
    fields = payload["fields"]
    codes = payload["codes"]
    editions = payload["meta"]["editions"]

    print("== database ==")
    check("editions", editions == ["18", "19", "20", "21", "22", "23"], str(editions))
    check("record groups", len(records) >= 40, str(len(records)))
    check("fields", len(fields) >= 300, str(len(fields)))
    check("code tables", len(codes) >= 30, str(len(codes)))

    # Every layout must tile columns 1..132 with no gap and no overlap.
    gaps: list[str] = []
    overlaps: list[str] = []
    empty: list[str] = []
    unnamed: list[str] = []
    total_layouts = 0
    for number, group in records.items():
        for edition, layouts in group["editions"].items():
            for layout_number, layout in layouts.items():
                total_layouts += 1
                where = f"{layout_number}@424-{edition}"
                cols = layout["fields"]
                if not cols:
                    empty.append(where)
                    continue
                if cols[0]["start"] != 1 or cols[-1]["end"] != LINE_WIDTH:
                    gaps.append(f"{where} ends at {cols[-1]['end']}")
                for previous, current in zip(cols, cols[1:]):
                    if current["start"] != previous["end"] + 1:
                        gaps.append(f"{where} hole before column {current['start']}")
                    if current["start"] <= previous["end"]:
                        overlaps.append(f"{where} column {current['start']}")
                for field in cols:
                    if not field["name"] or len(field["name"]) < 3:
                        unnamed.append(f"{where} column {field['start']}")

    check("layouts are non-empty", not empty, ", ".join(empty[:5]))
    check("columns 1..132 covered", not gaps, f"{len(gaps)}: {'; '.join(gaps[:4])}")
    check("no overlapping columns", not overlaps, f"{len(overlaps)}: {'; '.join(overlaps[:4])}")
    check("field names parsed", not unnamed, f"{len(unnamed)}: {'; '.join(unnamed[:4])}")
    print(f"        ({total_layouts} layouts checked)")

    print("== cli: round trip ==")
    # Encode a deterministic value into every non-blank column, decode it back
    # and require the same characters out.
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    round_trip_failures: list[str] = []
    skipped: list[str] = []
    for number, group in records.items():
        layouts = group["editions"].get("23") or {}
        primary = next(
            (
                n
                for n in sorted(layouts)
                if not any(
                    word in layouts[n]["title"].lower()
                    for word in ("continuation", "extension")
                )
                and layouts[n]["fields"]
            ),
            None,
        )
        if primary is None:
            skipped.append(number)
            continue
        layout = layouts[primary]

        def column(name: str) -> int | None:
            for field in layout["fields"]:
                lowered = field["name"].lower()
                if lowered.startswith(name) and field["end"] - field["start"] <= 4:
                    return field["start"]
            return None

        section_col = column("section")
        subsection_col = column("subsection")
        code = group["record_codes"][0] if group["record_codes"] else ""
        if not section_col or not code:
            skipped.append(f"{number} (no section column)")
            continue

        assignments = []
        expected: dict[int, str] = {}
        for index, field in enumerate(layout["fields"]):
            name = field["name"].lower()
            if name.startswith(("blank", "reserved")):
                continue
            width = field["end"] - field["start"] + 1
            # Section/Subsection must stay truthful or `decode` picks another
            # layout; every other column takes a rotating filler.
            if field["start"] == section_col:
                value = code[0]
            elif subsection_col and field["start"] == subsection_col:
                value = code[1] if len(code) > 1 else " "
            elif name.startswith("continuation record"):
                value = "0"
            else:
                value = (alphabet[index % len(alphabet)] * width)[:width]
            assignments.append(f"{field['start']}={value}")
            expected[field["start"]] = value.ljust(width)

        line = run("encode", primary, "--version", "23", *assignments).rstrip("\n")
        if len(line) != LINE_WIDTH:
            round_trip_failures.append(f"{primary} produced {len(line)} columns")
            continue
        decoded = run("decode", line, "--json", "--version", "23")
        try:
            parsed = json.loads(decoded)
        except json.JSONDecodeError as error:
            round_trip_failures.append(f"{primary} bad json: {error}")
            continue
        for item in parsed.get("fields", []):
            want = expected.get(item["start"])
            if want is None:
                continue
            # `decode` reports values trimmed of their padding, so a column
            # filled with blanks round-trips to the empty string.
            if item["value"] != want.strip():
                round_trip_failures.append(
                    f"{primary} column {item['start']}: {item['value']!r} != {want.strip()!r}"
                )
                break

    check("encode/decode round trip", not round_trip_failures, "; ".join(round_trip_failures[:4]))
    print(
        f"        ({len(records) - len(skipped)} record groups round-tripped"
        + (f", skipped {', '.join(skipped)}" if skipped else "")
        + ")"
    )

    print("== cli: queries ==")
    check("record", "Section Code" in run("record", "4.1.2.1", "--quiet"))
    check("field", "Waypoint Description Code" in run("field", "5.17"))
    check("codes", "Waypoint" in run("codes", "5.17"))
    check("diff", "4.1.2" in run("diff", "4.1.2.1"))
    check("search", "Path and Termination" in run("search", "path terminator"))
    check("list records", "VHF NAVAID" in run("list", "records"))
    check("list fields", "Record Type" in run("list", "fields"))
    check("list codes", len(run("list", "codes").splitlines()) >= 30)

    print("== references ==")
    expected_pages = [
        "00-orientation.md",
        "01-record-index.md",
        "03-field-index.md",
        "05-code-tables.md",
        "06-edition-changes.md",
        "07-glossary.md",
        "08-model-mapping.md",
        "09-rust-guide.md",
    ]
    for page in expected_pages:
        path = REFERENCES / page
        check(f"{page} exists", path.exists() and path.stat().st_size > 200)

    missing_records = [
        n for n in records if not (REFERENCES / "02-records" / f"{n}.md").exists()
    ]
    check("one page per record group", not missing_records, ", ".join(missing_records[:5]))
    missing_fields = [
        n for n in fields if not (REFERENCES / "04-fields" / f"{n}.md").exists()
    ]
    check("one page per field", not missing_fields, ", ".join(missing_fields[:5]))

    # Every internal link in SKILL.md and the index pages must resolve.
    broken: list[str] = []
    for page in list(REFERENCES.rglob("*.md")) + [ROOT / "SKILL.md"]:
        text = page.read_text(encoding="utf-8")
        for target in re.findall(r"references/([\w./-]+\.md)", text):
            if not (REFERENCES / target).exists():
                broken.append(f"{page.name} -> {target}")
    check("internal links resolve", not broken, "; ".join(broken[:4]))

    print("== model mapping ==")
    model = payload.get("model") or []
    check("rust structs parsed", len(model) >= 15, str(len(model)))
    mapped = [s for s in model if s["mappings"]]
    check("structs carry record codes", len(mapped) >= 10, str(len(mapped)))

    print()
    if failures:
        print(f"{len(failures)} of {checks} checks FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"all {checks} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
