"""Parse the ARINC 424 specification PDFs into a structured specification database.

The six editions are laid out differently but share one grammar:

* Chapter 4 (record layouts) is a table of ``column | field name (length) |
  reference``. Editions 18-21 print it in a second column *beside* the running
  prose, so the extracted text stream is column-major and useless as-is.
* Chapter 5 (field definitions) interleaves prose with ruled code tables.

Both are therefore read through page geometry: tables are located with
pdfplumber, their rows are rebuilt by clustering words on the y axis, and prose
is read from the words outside those table boxes. A table is kept as one atomic
block so that interleaved prose can never break a row sequence.

Every layout is validated afterwards: the extracted rows must tile columns
1..132 without holes, which doubles as a check that nothing was dropped.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber
import pypdf

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
DOCS = SKILL_ROOT / "docs"
CACHE = HERE / ".cache"

VERSIONS = ["18", "19", "20", "21", "22", "23"]

DASHES = "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"

PAGE_HEADER = re.compile(
    r"^(ARINC SPECIFICATION 424|\d+\.\d+\s+NAVIGATION\s+DATA\s*[-\u2013\u2014]\s*"
    r"(RECORD LAYOUT|FIELD DEFINITIONS))",
    re.IGNORECASE,
)
FOOTER = re.compile(r"^(-?\s*\d+\s*-?|ARINC SPECIFICATION 424.*)$", re.IGNORECASE)
HEADING = re.compile(r"^(\d+(?:\.\d+){1,3})\s+(\S.*)$")
TITLE_SUFFIX = re.compile(r"^(Records?|Continuation Records?|Record|Data|Table)$", re.IGNORECASE)
COLUMN_HEADER = re.compile(
    r"^Columns?\s+F[a-z]*\s+Name\s*\(Length\)\s*(Reference)?\s*$", re.IGNORECASE
)
ROW_RANGE = re.compile(r"^(\d{1,3})\s+thru\s+(\d{1,3})\s*(.*)$", re.IGNORECASE)
ROW_HYPHEN = re.compile(r"^(\d{1,3})\s*-\s*(\d{1,3})\s+(\S.*)$")
ROW_SINGLE = re.compile(r"^(\d{1,3})\s+(\S.*)$")
BARE_NUMBER = re.compile(r"^(\d{1,3})$")
DANGLING_RANGE = re.compile(r"^(\d{1,3})\s+thru\s*(\d{1,3})?\s*$", re.IGNORECASE)
# The other half of a broken range: "thru 84 Reserved (Expansion) (4)" lands on
# one line while its start number ("81") is emitted separately, sometimes after
# it. Left alone, columns 81-84 vanish and the whole layout is discarded.
ORPHAN_RANGE = re.compile(r"^thru\s+(\d{1,3})\b\s*(\S.*)?$", re.IGNORECASE)
LENGTH_TOKEN = re.compile(r"\((\d{1,3})\)?")
NOTE = re.compile(r"^(Note\s*\d+\s*:|Notes?\s*:)", re.IGNORECASE)
SUSPECT_NAME = re.compile(r"^(\(\d{1,3}\)?)?$")
DELETED = re.compile(r"deleted by supplement\s*(\d+)", re.IGNORECASE)


# Bullets and Wingdings glyphs the layout tables use as footnote markers.
BULLETS = "\uf0b7\uf0a7\uf0fc\u2022\u00b7\u25cf\u25aa\u25a0*>"

BULLET = re.compile(rf"^[\s{BULLETS}]+|[\s{BULLETS}]+$")


def normalise(text: str) -> str:
    for dash in DASHES:
        text = text.replace(dash, "-")
    return (
        text.replace("\u00a0", " ")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def reflow(text: str) -> str:
    """Collapse whitespace and drop the bullet markers some cells carry."""
    return BULLET.sub("", re.sub(r"\s+", " ", text)).strip()


@dataclass
class Element:
    """A visual block on a page: either one prose line or one whole table."""

    top: float
    kind: str  # "prose" | "table"
    page: int
    lines: list[str] = field(default_factory=list)
    center: float = 0.0
    height: float = 0.0


GUTTER_GAP = 20.0
SECTION_NUMBER = re.compile(r"^\d+(\.\d+)*$")
SUBSECTION_NUMBER = re.compile(r"^\d+\.\d+\.\d+\.\d+$")


def flatten(cell) -> str:
    """One cell of a table row as a single line of text.

    pdfplumber hands back either None, a string, or -- for a cell it could not
    decide about -- a list of fragments.
    """
    if cell is None:
        return ""
    if isinstance(cell, str):
        return " ".join(cell.split())
    if isinstance(cell, (list, tuple)):
        return " ".join(part for part in (flatten(item) for item in cell) if part)
    return str(cell)


def split_segments(words: list[dict]) -> list[list[dict]]:
    """Split a visual line wherever the horizontal gap looks like a column gutter.

    Two-column editions put unrelated text at the same height; without this the
    left column's heading and the right column's heading would be welded into
    one line.

    A second cut is needed wherever the gutter is too narrow to see: the same
    editions can place two headings on one baseline, welding
    ``4.1.21.2 Enroute Airways Restriction Altitude Exclusion`` to
    ``4.1.22.1 Airport and Heliport MLS Primary Records``. A four-part section
    number appearing mid-line is always the start of the next column's heading,
    never part of a sentence.
    """
    segments: list[list[dict]] = []
    current: list[dict] = []
    previous_right = None
    for word in words:
        gap = None if previous_right is None else word["x0"] - previous_right
        # A heading number sits well clear of its title; never split there.
        keep = current and SECTION_NUMBER.fullmatch(current[-1]["text"]) is not None
        if current and SUBSECTION_NUMBER.fullmatch(word["text"]) and not keep:
            segments.append(current)
            current = []
        elif gap is not None and gap > GUTTER_GAP and not keep:
            if current:
                segments.append(current)
            current = []
        current.append(word)
        previous_right = word["x1"]
    if current:
        segments.append(current)
    return segments


class Book:
    """A single ARINC 424 edition."""

    def __init__(self, version: str):
        self.version = version
        self.path = DOCS / f"ARINC 424-{version}.pdf"
        self._reader = pypdf.PdfReader(str(self.path))
        self._plumber = pdfplumber.open(str(self.path))
        self._elements: dict[int, list[Element]] = {}
        self._word_cache: dict[int, list[dict]] = {}
        self._gutters: dict[int, float | None] = {}
        self._body_cache: dict[int, list[dict]] = {}
        self.outline = self._read_outline()

    @property
    def page_count(self) -> int:
        return len(self._reader.pages)

    def close(self) -> None:
        self._plumber.close()

    def _read_outline(self) -> list[dict]:
        entries: list[dict] = []

        def walk(items, level):
            for item in items:
                if isinstance(item, list):
                    walk(item, level + 1)
                else:
                    try:
                        page = self._reader.get_destination_page_number(item) + 1
                    except Exception:
                        page = -1
                    entries.append(
                        {"level": level, "title": normalise(str(item.title)).strip(), "page": page}
                    )

        walk(self._reader.outline, 0)
        return entries

    # -- page geometry ----------------------------------------------------- #

    def _cell_lines(self, table) -> list[str]:
        """One line per table row, straight from pdfplumber's cell grid.

        A cell stays whole, which is the whole point: a row whose text sits on
        two baselines ("52 thru" / "57" / "Runway Gradient (6)") is one row to
        pdfplumber and two to any word-by-word re-flow.
        """
        lines = [
            reflow(normalise(" ".join(cell for cell in (flatten(cell) for cell in row) if cell)))
            for row in table.extract()
        ]
        return [line for line in lines if line]

    def _word_lines(self, page: int, table, inside) -> list[str]:
        """One line per visual baseline inside the table box."""
        rows: dict[float, list] = {}
        for word in self._words(page):
            if inside(word, table.bbox):
                rows.setdefault(round(word["top"], 0), []).append(word)
        lines = []
        for top in sorted(rows):
            line = " ".join(w["text"] for w in sorted(rows[top], key=lambda w: w["x0"]))
            line = reflow(normalise(line))
            if line:
                lines.append(line)
        return lines

    def _table_lines(self, page: int, table, inside) -> list[str]:
        """Row text for a table, preferring the cell grid.

        The cell grid is far better when pdfplumber actually resolves the grid,
        but some editions give it a table it collapses into a single row --
        there it would throw away every row but the first. Fall back to
        baselines whenever the grid looks collapsed, which is whenever it
        yields far fewer lines than the words visibly occupy.
        """
        cells = self._cell_lines(table)
        words = self._word_lines(page, table, inside)
        if len(cells) >= 2 and len(cells) * 2 >= len(words):
            return cells
        return words

    def elements(self, page: int) -> list[Element]:
        if page in self._elements:
            return self._elements[page]

        plumber_page = self._plumber.pages[page - 1]
        tables = plumber_page.find_tables()
        boxes = [table.bbox for table in tables]

        inside = lambda word, box: (  # noqa: E731
            word["x0"] >= box[0] - 2
            and word["x1"] <= box[2] + 2
            and word["top"] >= box[1] - 2
            and word["bottom"] <= box[3] + 2
        )

        elements: list[Element] = []
        for table in tables:
            lines = self._table_lines(page, table, inside)
            if lines:
                box = table.bbox
                elements.append(
                    Element(box[1], "table", page, lines, (box[0] + box[2]) / 2, box[3] - box[1])
                )

        prose: dict[float, list] = {}
        for word in self._words(page):
            if any(inside(word, box) for box in boxes):
                continue
            prose.setdefault(round(word["top"], 0), []).append(word)
        for top in sorted(prose):
            for segment in split_segments(sorted(prose[top], key=lambda w: w["x0"])):
                line = " ".join(w["text"] for w in segment)
                line = reflow(normalise(line))
                if not line or PAGE_HEADER.match(line) or FOOTER.match(line):
                    continue
                center = (segment[0]["x0"] + segment[-1]["x1"]) / 2
                elements.append(Element(top, "prose", page, [line], center, 0.0))

        elements.sort(key=lambda e: (e.top, e.kind == "table"))
        self._elements[page] = elements
        return elements

    def _words(self, page: int) -> list[dict]:
        if page not in self._word_cache:
            self._word_cache[page] = self._plumber.pages[page - 1].extract_words()
        return self._word_cache[page]

    def body_words(self, page: int) -> list[dict]:
        """Words minus the running header and footer.

        The running header spans both columns, so leaving it in would hide the
        very gutter the two-column editions are read along.
        """
        if page in self._body_cache:
            return self._body_cache[page]

        lines: dict[float, list[dict]] = {}
        for word in self._words(page):
            lines.setdefault(round(word["top"], 0), []).append(word)

        kept: list[dict] = []
        for top in sorted(lines):
            text = " ".join(w["text"] for w in sorted(lines[top], key=lambda w: w["x0"]))
            text = reflow(normalise(text))
            if PAGE_HEADER.match(text) or FOOTER.match(text):
                continue
            kept.extend(lines[top])
        self._body_cache[page] = kept
        return kept

    def gutter(self, page: int) -> float | None:
        """Centre of the widest full-height whitespace channel, if any.

        Editions 18-21 print the running prose and the layout tables side by
        side, and the reading order is column by column -- not line by line.
        A channel counts only when it runs clear of *every* word on the page,
        which a table's own column gap does not.
        """
        if page in self._gutters:
            return self._gutters[page]
        words = self.body_words(page)
        self._gutters[page] = None
        if not words:
            return None

        low = min(w["x0"] for w in words)
        high = max(w["x1"] for w in words)
        if high - low < 120:
            return None

        bins = [0] * (int(high - low) + 2)
        for word in words:
            for x in range(int(word["x0"] - low), int(word["x1"] - low) + 1):
                if 0 <= x < len(bins):
                    bins[x] += 1

        runs: list[tuple[int, int]] = []
        start = None
        for index, count in enumerate(bins):
            if count == 0:
                start = index if start is None else start
            else:
                if start is not None and index - start >= 12:
                    runs.append((low + start, low + index))
                start = None
        if start is not None and len(bins) - start >= 12:
            runs.append((low + start, low + len(bins)))

        best = None
        for left, right in runs:
            left_count = sum(1 for w in words if w["x1"] <= left + 2)
            right_count = sum(1 for w in words if w["x0"] >= right - 2)
            if left_count >= 15 and right_count >= 15:
                if best is None or (right - left) > (best[1] - best[0]):
                    best = (left, right)
        if best:
            self._gutters[page] = (best[0] + best[1]) / 2
        return self._gutters[page]

    def blocks(self, start: int, end: int, column_major: bool = True) -> list[Element]:
        """Elements of a page range in reading order."""
        out: list[Element] = []
        for page in range(start, end):
            elements = list(self.elements(page))
            split = self.gutter(page) if column_major else None
            if split is not None:
                elements.sort(key=lambda e: (0 if e.center < split else 1, e.top))
            out.extend(elements)
        return out

    def flow(self, start: int, end: int, column_major: bool = True) -> list[tuple[int, str]]:
        """Reading-order lines for a page range.

        With ``column_major`` the page is read column by column, which is how
        the two-column editions are meant to be read. Tables stay contiguous.
        """
        out: list[tuple[int, str]] = []
        for element in self.blocks(start, end, column_major):
            for line in element.lines:
                out.append((element.page, line))
        return out


# --------------------------------------------------------------------------- #
# Chapter boundaries
# --------------------------------------------------------------------------- #


def chapter_range(book: Book, number: str) -> tuple[int, int]:
    """Page span of a top-level chapter such as ``4.0``, bookmarks or not."""
    pattern = re.compile(rf"^{re.escape(number)}\s", re.IGNORECASE)
    for index, entry in enumerate(book.outline):
        if pattern.match(entry["title"]):
            start = entry["page"]
            for other in book.outline[index + 1 :]:
                if other["page"] > start and re.match(r"^\d+\.0\s", other["title"], re.IGNORECASE):
                    return start, other["page"]
            return start, book.page_count + 1
    for page in range(1, book.page_count + 1):
        for element in book.elements(page)[:3]:
            if element.lines and pattern.match(element.lines[0]):
                return page, book.page_count + 1
    raise LookupError(f"chapter {number} not found in 424-{book.version}")


# --------------------------------------------------------------------------- #
# Chapter 4 -- record layouts
# --------------------------------------------------------------------------- #


def join_wrapped(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Re-assemble rows whose cells wrapped over several lines.

    ``23`` / ``Application Type (1)`` / ``F-Additional Sectorization`` /
    ``Continuation`` / ``5.91`` is one row, not five.
    """
    merged: list[tuple[int, str]] = []
    index = 0
    while index < len(lines):
        page, line = lines[index]
        if BARE_NUMBER.match(line):
            parts = [line]
            cursor = index + 1
            while cursor < len(lines):
                nxt = lines[cursor][1]
                if re.match(r"^\d{1,3}\b", nxt) or HEADING.match(nxt) or COLUMN_HEADER.match(nxt):
                    break
                parts.append(nxt)
                cursor += 1
                if re.search(r"\b5\.\d+\b", nxt):
                    break
            merged.append((page, " ".join(parts)))
            index = cursor
            continue
        merged.append((page, line))
        index += 1
    return merged


def join_dangling(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Re-attach column ranges that the PDF broke across lines.

    ``124 thru`` / ``128`` / ``File Record No. (5) 5.31`` becomes one row.
    So does the reversed break ``thru 84 Reserved (Expansion) (4)`` / ``81``.
    """
    merged: list[tuple[int, str]] = []
    carry = ""
    orphan: tuple[int, str, int] | None = None
    for page, line in lines:
        text = (carry + " " + line).strip() if carry else line
        carry = ""
        if orphan is not None:
            end, rest, orphan_page = orphan
            orphan = None
            start = BARE_NUMBER.match(text)
            if start:
                merged.append((page, f"{start.group(1)} thru {end} {rest}".strip()))
                continue
            # Its start number never arrived. Keep the fragment anyway: the
            # declared length is often enough to place it.
            merged.append((orphan_page, f"thru {end} {rest}".strip()))
        orphan_match = ORPHAN_RANGE.match(text)
        if orphan_match:
            orphan = (int(orphan_match.group(1)), orphan_match.group(2) or "", page)
            continue
        if DANGLING_RANGE.match(text):
            carry = text
            continue
        if orphan is None:
            merged.append((page, text))
    if carry:
        merged.append((lines[-1][0] if lines else 0, carry))
    if orphan is not None:
        end, rest, orphan_page = orphan
        merged.append((orphan_page, f"thru {end} {rest}".strip()))
    return merged


def dropped_digit(start: int, end: int, expected: int) -> int | None:
    """The column number the PDF printed short by its first character.

    One table in 424-19 lost the leading character of every column number --
    ``22`` reads ``2``, ``124`` reads ``24`` -- and 424-18 printed ``28 Time
    Code`` as ``8 Time Code``. The printed number is therefore the expected one
    minus a whole power of ten, and must still be its suffix.
    """
    if expected <= start:
        return None
    shift = expected - start
    if shift % (10 ** len(str(start))) != 0:
        return None
    if not str(expected).endswith(str(start)):
        return None
    return expected if end + shift <= 132 else None


NUMBERLESS_ROW = re.compile(
    r"^([A-Za-z(][^0-9]*?)\s*\((\d{1,3})\)\s*(\S.*)?$"
)


def parse_numberless_row(line: str, expected_start: int) -> dict | None:
    """A row whose column number never made it into the text layer at all.

    ``Continuation Record Number (1) 5.16`` belongs at column 22; only the
    declared length can say so. Kept deliberately narrow -- the row must carry
    a length and either a field reference or one of the filler names -- so that
    prose wrapped under a table is not mistaken for a row.
    """
    if COLUMN_HEADER.match(line) or NOTE.match(line):
        return None
    match = NUMBERLESS_ROW.match(line.strip())
    if not match:
        return None
    name, length, reference = match.group(1).strip(), int(match.group(2)), match.group(3) or ""
    if not (1 <= length <= 132) or expected_start + length - 1 > 132:
        return None
    filler = name.lower().startswith(("blank", "reserved", "fields as on"))
    if not filler and not re.search(r"\b5\.\d+\b", reference + " " + name):
        return None
    return {
        "start": expected_start,
        "end": expected_start + length - 1,
        "length": length,
        "declared_length": length,
        "repaired": True,
        "name": reflow(name).rstrip(" -"),
        "reference": reference.strip(),
        "spec": (re.findall(r"\b5\.\d+\b", reference) or [None])[0],
        "specs": re.findall(r"\b5\.\d+\b", reference),
        "note": None,
    }


def parse_row(line: str, expected_start: int) -> dict | None:
    """Parse one layout row, placing it at ``expected_start``.

    The printed column range wins when it lines up with the previous row. When
    it does not, the declared length is used to re-derive the range (the volume
    misprints ranges such as ``19 thru 132`` for 129..132). A range that fits
    neither way is rejected, which is how stray text gets filtered out. A length
    that merely disagrees with a correctly placed range is corrected and the
    printed value kept in ``declared_length``.
    """
    line = re.sub(r"(\d)\s*thru\s*(\d)", r"\1 thru \2", line)
    line = re.sub(r"(\d)\s*thru\s*$", r"\1 thru", line)

    match = ROW_RANGE.match(line)
    if match:
        raw_start, raw_end, rest = int(match.group(1)), int(match.group(2)), match.group(3)
    else:
        match = ROW_HYPHEN.match(line)
        if match:
            raw_start, raw_end, rest = int(match.group(1)), int(match.group(2)), match.group(3)
        else:
            match = ORPHAN_RANGE.match(line)
            if match:
                # "thru 92 Notes (69) 5.61": the end survived, the start did
                # not (see ``dropped_digit``). Place it from its length.
                raw_start, raw_end, rest = None, int(match.group(1)), match.group(2) or ""
            else:
                match = ROW_SINGLE.match(line)
                if not match:
                    return None
                raw_start = raw_end = int(match.group(1))
                rest = match.group(2)

    if raw_end > 132:
        return None
    if raw_start is None:
        pass
    elif raw_start < 1 or raw_end < raw_start:
        return None
    else:
        repaired_start = dropped_digit(raw_start, raw_end, expected_start)
        if repaired_start is not None:
            raw_end += repaired_start - raw_start
            raw_start = repaired_start
            if raw_end > 132:
                return None

    rest = rest.strip()
    length_match = None
    for length_match in LENGTH_TOKEN.finditer(rest):
        pass

    if length_match and length_match.start() > 0:
        name = reflow(rest[: length_match.start()]).rstrip(" -")
        declared = int(length_match.group(1))
        reference = rest[length_match.end() :].strip()
    elif raw_start is None:
        # No printed start and no printed length either -- "Fields as on
        # Primary Records" carries neither. The printed end is still good, so
        # take the start from wherever the previous row left off.
        if raw_end < expected_start:
            return None
        name = reflow(rest).rstrip(" -")
        declared = raw_end - expected_start + 1
        reference = ""
        trailing = re.match(r"^(.*?)\s+(\d\.\d+)\s*$", name)
        if trailing:
            name, reference = trailing.group(1).strip(), trailing.group(2)
    else:
        name = reflow(rest).rstrip(" -")
        declared = raw_end - raw_start + 1
        reference = ""
        trailing = re.match(r"^(.*?)\s+(\d\.\d+)\s*$", name)
        if trailing:
            name, reference = trailing.group(1).strip(), trailing.group(2)

    if not name:
        return None

    if raw_start is None:
        # The end is printed, the start is not; the gap the previous row left
        # is the only thing that can name it.
        start, end = expected_start, raw_end
        repaired = True
    elif raw_start == expected_start:
        start, end = raw_start, raw_end
        repaired = declared != end - start + 1
    elif declared and raw_end - declared + 1 == expected_start:
        start, end = expected_start, raw_end
        repaired = True
    else:
        return None

    codes = re.findall(r"\b5\.\d+\b", reference)
    note_ref = re.findall(r"Note\s*(\d+)", reference, re.IGNORECASE)
    return {
        "start": start,
        "end": end,
        "length": end - start + 1,
        "declared_length": declared,
        "repaired": repaired,
        "name": name,
        "reference": reference,
        "spec": codes[0] if codes else None,
        "specs": codes,
        "note": note_ref[0] if note_ref else None,
    }


BARE_RANGE = re.compile(r"^(\d{1,3})\s+thru\s+(\d{1,3})$", re.IGNORECASE)


def join_strayed_ranges(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Re-unite a column range with the field name printed above it.

    ``File Record No. (5) 5.31`` followed by ``124 thru 128`` is one row whose
    cells came out in the wrong order.
    """
    merged: list[tuple[int, str]] = []
    for page, line in lines:
        if (
            merged
            and BARE_RANGE.match(line)
            and not merged[-1][1][:1].isdigit()
            and LENGTH_TOKEN.search(merged[-1][1])
            and not COLUMN_HEADER.match(merged[-1][1])
        ):
            merged[-1] = (merged[-1][0], f"{line} {merged[-1][1]}")
            continue
        merged.append((page, line))
    return merged


def split_rows(lines: list[tuple[int, str]]) -> tuple[list[dict], list[str], bool]:
    """Rows of one layout table plus the lines that could not be attributed."""
    fields: list[dict] = []
    leftovers: list[str] = []
    in_table = False
    broken = False
    index = 0

    while index < len(lines):
        page, line = lines[index]
        if COLUMN_HEADER.match(line):
            in_table = True
            index += 1
            continue
        if NOTE.match(line):
            leftovers.append(line)
            index += 1
            continue
        if not in_table:
            leftovers.append(line)
            index += 1
            continue

        expected = fields[-1]["end"] + 1 if fields else 1
        row = parse_row(line, expected)
        if row is None:
            row = parse_numberless_row(line, expected)
        if row is None:
            leftovers.append(line)
            if not fields:
                broken = True
            index += 1
            continue
        row["page"] = page

        # Some cells wrap so that only the length lands on the row's own line and
        # the field name is emitted afterwards: ``85 (1) 5.149`` followed by
        # ``Navaid Useable Range``.
        if SUSPECT_NAME.match(row["name"]):
            look = index + 1
            while look < len(lines) and look <= index + 4:
                candidate = lines[look][1]
                if parse_row(candidate, row["end"] + 1) is not None:
                    break
                if is_name_fragment(candidate):
                    row["name"] = candidate
                    index = look
                    break
                look += 1

        fields.append(row)
        index += 1

    return fields, leftovers, broken


def is_name_fragment(line: str) -> bool:
    """A wrapped field name: words only, no leading column number, no reference."""
    if not line or line[0].isdigit() or NOTE.match(line):
        return False
    if re.search(r"\b5\.\d+\b", line):
        return False
    return 1 <= len(line.split()) <= 6 and line[0].isalpha()


def leftover_notes(lines: list[str]) -> tuple[list[str], str]:
    """Split table leftovers into footnotes and free prose."""
    notes: list[str] = []
    prose: list[str] = []
    for line in lines:
        if NOTE.match(line):
            notes.append(line)
        elif notes:
            notes[-1] = notes[-1] + " " + line
        else:
            prose.append(line)
    return [reflow(n) for n in notes], reflow(" ".join(prose))


def split_title(title: str) -> tuple[str, str]:
    match = HEADING.match(title)
    if not match:
        return "", title
    return match.group(1), match.group(2).strip()


def extract_record_codes(title: str) -> list[str]:
    """Record codes such as ``(D)``, ``(PD, PE, and PF)``, ``(DB or PN)``."""
    codes: list[str] = []
    for group in re.findall(r"\(([^)]*)\)", title):
        for token in re.findall(r"\b[A-Z]{1,2}\b", group):
            if token not in {"OR", "AND"} and token not in codes:
                codes.append(token)
    return codes


LETTER_SPACED = re.compile(r"\b[A-Za-z]\b")


def looks_like_title(title: str) -> bool:
    """Reject the record-layout diagrams, whose labels are letter-spaced."""
    words = title.split()
    if not words or len(words) < 2:
        return False
    if sum(1 for word in words if LETTER_SPACED.fullmatch(word)) >= 2:
        return False
    return any(len(word) >= 3 for word in words)


def heading_positions(flow: list[tuple[int, str]]) -> list[tuple[int, str, int]]:
    """(line index, section number, page) for every chapter 4 heading."""
    positions = []
    for index, (page, line) in enumerate(flow):
        match = HEADING.match(line)
        if not match:
            continue
        number = match.group(1)
        if not number.startswith("4.") or number.count(".") not in (2, 3):
            continue
        if not looks_like_title(match.group(2)):
            continue
        positions.append((index, number, page))
    return positions


def parse_layout(buffer: list[tuple[int, str]]) -> tuple[list[dict], list[str], str, bool]:
    fields, leftovers, broken = split_rows(join_dangling(join_wrapped(join_strayed_ranges(buffer))))
    notes, prose = leftover_notes(leftovers)
    tiles = not broken and fields and fields[0]["start"] == 1 and fields[-1]["end"] == 132
    return fields, notes, prose, bool(tiles)


def extract_records(book: Book) -> list[dict]:
    """Chapter 4, resolved per subsection against both reading orders.

    The two-column editions put a section's prose and its table in different
    columns, and which one comes first varies by page. Rather than guessing,
    each subsection is parsed from the column-major reading and, when the rows
    do not tile columns 1..132, re-parsed from the top-down reading.
    """
    start, end = chapter_range(book, "4.0")
    primary = book.flow(start, end, column_major=True)
    fallback = book.flow(start, end, column_major=False)

    primary_positions = heading_positions(primary)
    fallback_positions = heading_positions(fallback)
    fallback_index = {(number, page): index for index, number, page in fallback_positions}

    groups: dict[str, dict] = {}
    order: list[str] = []
    retried = 0

    for position, (index, number, page) in enumerate(primary_positions):
        next_index = (
            primary_positions[position + 1][0]
            if position + 1 < len(primary_positions)
            else len(primary)
        )
        heading_line = primary[index][1]
        buffer = primary[index + 1 : next_index]
        fields, notes, prose, ok = parse_layout(buffer)

        number_parts = number.split(".")
        group_number = ".".join(number_parts[:3])
        _, heading_text = split_title(heading_line)
        heading_text = absorb_title_suffix(primary, index, heading_text)

        # Register the group before looking at the layout: a group heading whose
        # own page carries no table still names the section the sub-layouts
        # belong to.
        if group_number not in groups:
            groups[group_number] = {
                "number": group_number,
                "title": "",
                "record_codes": [],
                "page_start": page,
                "description": "",
                "subsections": [],
            }
            order.append(group_number)
        group = groups[group_number]

        if len(number_parts) == 3:
            group["title"] = heading_text
            group["record_codes"] = extract_record_codes(heading_text)
            group["page_start"] = page
            if prose:
                group["description"] = prose

        if not ok:
            fallback_start = fallback_index.get((number, page))
            if fallback_start is not None:
                later = [i for i, _, _ in fallback_positions if i > fallback_start]
                fallback_end = later[0] if later else len(fallback)
                retry = fallback[fallback_start + 1 : fallback_end]
                retry_fields, retry_notes, retry_prose, retry_ok = parse_layout(retry)
                if retry_ok:
                    fields, notes, prose, ok = retry_fields, retry_notes, retry_prose, True
                    retried += 1

        if not ok:
            continue

        if len(number_parts) == 3:
            # Some sections (4.1.34 Communication Type Translation) carry the
            # layout directly under the group heading, with no sub-number of
            # their own. Only treat it as an implicit subsection when the table
            # really starts here -- otherwise the rows belong to a neighbouring
            # section that happens to share the page.
            if not any(COLUMN_HEADER.match(text) for _, text in buffer[:4]):
                continue

        text = " ".join(line for _, line in primary[index:next_index])
        deleted = DELETED.search(text)
        group["subsections"].append(
            {
                "number": number,
                "title": heading_text,
                "page_start": page,
                "page_end": buffer[-1][0] if buffer else page,
                "fields": fields,
                "notes": notes,
                "prose": prose,
                "deleted_by": int(deleted.group(1)) if deleted else None,
            }
        )

    result = [groups[key] for key in order if groups[key]["subsections"]]
    book.retried = retried
    return result


def absorb_title_suffix(lines: list[tuple[int, str]], index: int, title: str) -> str:
    """Re-attach a heading that wrapped onto the next line (``Records``)."""
    for offset in (1, 2, 3):
        if index + offset >= len(lines):
            break
        nxt = lines[index + offset][1]
        if HEADING.match(nxt):
            break
        if TITLE_SUFFIX.match(nxt):
            return f"{title} {nxt}"
        if len(nxt.split()) > 3:
            break
    return title


# --------------------------------------------------------------------------- #
# Chapter 5 -- field definitions
# --------------------------------------------------------------------------- #


def parse_field_title(title: str) -> tuple[str, str, str]:
    """``5.21 Path and Termination (PATH TERM)`` -> number, name, abbreviation."""
    number, rest = split_title(title)
    match = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", rest)
    if match:
        return number, match.group(1).strip(), match.group(2).strip()
    return number, rest.strip(), ""


def extract_fields(book: Book) -> list[dict]:
    start, end = chapter_range(book, "5.0")

    fields: list[dict] = []
    current: dict | None = None
    for page in range(start, end):
        for element in book.elements(page):
            first = element.lines[0] if element.lines else ""
            heading = HEADING.match(first)
            is_heading = (
                element.kind == "prose" and heading is not None and re.fullmatch(r"5\.\d+", heading.group(1))
            )
            if is_heading:
                if current:
                    fields.append(current)
                number, name, abbrev = parse_field_title(first)
                current = {
                    "number": number,
                    "name": name,
                    "abbreviation": abbrev,
                    "page_start": page,
                    "page_end": page,
                    "prose_parts": [],
                    "tables": [],
                }
                rest = first[heading.end() :].strip()
                if rest:
                    current["prose_parts"].append(rest)
                continue
            if current is None:
                continue
            current["page_end"] = page
            if element.kind == "prose":
                current["prose_parts"].append(" ".join(element.lines))
            else:
                rows = [split_table_row(line) for line in element.lines]
                rows = [r for r in rows if any(cell for cell in r)]
                if rows:
                    current["tables"].append({"page": page, "rows": rows})

    if current:
        fields.append(current)

    for item in fields:
        item["prose"] = reflow(" ".join(item.pop("prose_parts")))
    return fields


def split_table_row(line: str) -> list[str]:
    """Split a rebuilt table row into cells on runs of two or more spaces.

    Row rebuilding joins words with single spaces, so the only wide gaps left
    are the original column gutters -- except that a cell may itself contain a
    single space. Two-space runs are therefore the reliable separator.
    """
    cells = re.split(r"\s{2,}", line)
    if len(cells) == 1:
        match = re.match(r"^(.*?)\s{1,}(\S{1,8})$", line)
        if match:
            cells = [match.group(1), match.group(2)]
    return [cell.strip() for cell in cells]


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def summarise(version: str, force: bool = False) -> dict:
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"spec-{version}.json"
    if path.exists() and not force:
        return json.loads(path.read_text(encoding="utf-8"))

    book = Book(version)
    try:
        data = {
            "version": version,
            "pages": book.page_count,
            "chapters": {
                "3": chapter_range(book, "3.0"),
                "4": chapter_range(book, "4.0"),
                "5": chapter_range(book, "5.0"),
            },
            "groups": extract_records(book),
            "fields": extract_fields(book),
        }
    finally:
        book.close()

    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def main() -> None:
    version = sys.argv[1] if len(sys.argv) > 1 else "23"
    force = "--force" in sys.argv
    data = summarise(version, force)
    layouts = sum(len(g["subsections"]) for g in data["groups"])
    print(
        f"[{version}] pages={data['pages']} groups={len(data['groups'])} "
        f"layouts={layouts} fields={len(data['fields'])}"
    )
    for group in data["groups"]:
        for sub in group["subsections"]:
            holes = sorted(
                set(range(1, 133))
                - {c for f in sub["fields"] for c in range(f["start"], f["end"] + 1)}
            )
            if holes:
                print(f"  ! {sub['number']} holes={holes[:8]}")


if __name__ == "__main__":
    main()
