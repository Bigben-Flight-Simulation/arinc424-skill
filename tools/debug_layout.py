"""Diagnose which chapter-4 subsections fail to tile columns 1..132.

Mirrors ``extract_records``: each subsection is parsed from the column-major
reading and, when the rows do not tile 1..132, re-parsed from the top-down
reading. Only subsections that fail both are reported -- a subsection that
legitimately has no table ("Deleted by Supplement 19", or a cross reference
printed in chapter 5) is skipped.
"""

import sys

sys.path.insert(0, ".")
import pdfparse as pp  # noqa: E402


def gaps_of(fields) -> list[int]:
    covered = set()
    for field in fields:
        covered |= set(range(field["start"], field["end"] + 1))
    return [c for c in range(1, 133) if c not in covered]


def diagnose(version: str) -> None:
    book = pp.Book(version)
    start, end = pp.chapter_range(book, "4.0")
    primary = book.flow(start, end, column_major=True)
    fallback = book.flow(start, end, column_major=False)

    primary_positions = pp.heading_positions(primary)
    fallback_positions = pp.heading_positions(fallback)
    fallback_index = {(n, p): i for i, n, p in fallback_positions}
    fallback_indices = [i for i, _, _ in fallback_positions]
    primary_indices = [i for i, _, _ in primary_positions]

    bad = []
    for slot, (i, number, page) in enumerate(primary_positions):
        if number.count(".") != 3:
            continue
        nxt = primary_indices[slot + 1] if slot + 1 < len(primary_indices) else len(primary)
        buffer = primary[i + 1 : nxt]
        if not any(pp.COLUMN_HEADER.match(text) for _, text in buffer[:4]):
            continue  # no table here at all: prose, deleted section or cross ref

        fields, _, _, ok = pp.parse_layout(buffer)
        if not ok:
            f_start = fallback_index.get((number, page))
            if f_start is not None:
                later = [x for x in fallback_indices if x > f_start]
                f_end = later[0] if later else len(fallback)
                retry, _, _, ok = pp.parse_layout(fallback[f_start + 1 : f_end])
                if ok:
                    fields = retry
        if ok:
            continue
        gaps = gaps_of(fields)
        bad.append(
            (
                number,
                page,
                f"rows={len(fields)}",
                f"first={fields[0]['start'] if fields else None}",
                f"last={fields[-1]['end'] if fields else None}",
                f"gaps={gaps[:14]}",
            )
        )
    print(f"=== 424-{version}: {len(bad)} subsections with a table that failed to tile")
    for item in bad:
        print("   ", item)
    book.close()


if __name__ == "__main__":
    for version in sys.argv[1:] or ["23"]:
        diagnose(version)
