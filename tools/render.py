"""Render the reference library from ``data/arinc424.json``.

    python tools/render.py

Everything under ``references/`` is generated; edit the templates here, not the
markdown. Hand-written pages (orientation, glossary, model guide) live in
``tools/templates/`` and are copied over verbatim.
"""

from __future__ import annotations

import json
import re
import shutil
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
DATA = SKILL_ROOT / "data/arinc424.json"
OUT = SKILL_ROOT / "references"
TEMPLATES = HERE / "templates"

DB = json.loads(DATA.read_text(encoding="utf-8"))
EDITIONS: list[str] = DB["meta"]["editions"]
LATEST: str = DB["meta"]["latest"]
RECORDS: dict = DB["records"]
FIELDS: dict = DB["fields"]
CODES: dict = DB["codes"]
MODEL: list = DB["model"]


def slug(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:48]


def code(word: str) -> str:
    """``AirportAsWaypoint`` -> ``Airport as waypoint``."""
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", word)
    text = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
    return text.strip()


def wrap(text: str, width: int = 96) -> str:
    return textwrap.fill(re.sub(r"\s+", " ", text).strip(), width=width)


PARAGRAPH = re.compile(
    r"(?=(?:Definition/Description:|Source/Content:|Notes?\s*\d+\s*:|Length:|"
    r"Character Type:|Table\s+\d+-\d+|Figure\s+\d+-\d+))"
)


def prose_blocks(text: str) -> str:
    """Break the spec's definition text at its own section markers."""
    if not text:
        return ""
    parts = [part.strip() for part in PARAGRAPH.split(text) if part.strip()]
    return "\n\n".join(wrap(part) for part in parts)


def table(headers: list[str], rows: list[list[str]], align: str | None = None) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        cells = ["" if cell is None else str(cell) for cell in row]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Diffing
# --------------------------------------------------------------------------- #


def match_fields(left: list[dict], right: list[dict]) -> list[tuple]:
    """Pair fields by name, then by column, so a move is reported as a move."""
    pairs: list[tuple] = []
    right_pool = list(right)

    for field in left:
        hit = next(
            (f for f in right_pool if f["name"].lower() == field["name"].lower()), None
        )
        if hit:
            right_pool.remove(hit)
            pairs.append((field, hit))

    for field in left:
        if any(field is pair[0] for pair in pairs):
            continue
        hit = next((f for f in right_pool if f["start"] == field["start"]), None)
        if hit:
            right_pool.remove(hit)
            pairs.append((field, hit))
        else:
            pairs.append((field, None))

    for field in right_pool:
        pairs.append((None, field))
    return pairs


def describe_change(left: dict | None, right: dict | None) -> str:
    if left and not right:
        return f"删除 {left['name']}（列 {left['start']}-{left['end']}）"
    if right and not left:
        return f"新增 {right['name']}（列 {right['start']}-{right['end']}，长 {right['length']}）"
    parts = []
    if left["name"] != right["name"]:
        parts.append(f"名称 {left['name']} → {right['name']}")
    if left["start"] != right["start"] or left["end"] != right["end"]:
        parts.append(f"列位 {left['start']}-{left['end']} → {right['start']}-{right['end']}")
    if left["length"] != right["length"]:
        parts.append(f"长度 {left['length']} → {right['length']}")
    if (left.get("spec") or "") != (right.get("spec") or ""):
        parts.append(f"引用 {left.get('spec') or '-'} → {right.get('spec') or '-'}")
    if not parts:
        return ""
    return f"{right['name']}：" + "，".join(parts)


def layout_changes(left: dict, right: dict) -> list[str]:
    changes = []
    for old, new in match_fields(left["fields"], right["fields"]):
        text = describe_change(old, new)
        if text:
            changes.append(text)
    return changes


# --------------------------------------------------------------------------- #
# Model mapping
# --------------------------------------------------------------------------- #


def model_for(group_number: str) -> list[tuple[dict, dict]]:
    """Rust structs that declare one of this group's record codes.

    A group recorded only by its section letter ("D") must not claim every
    struct whose section is `D` -- the NDB struct is `DB`, not `D`. The
    subsection has to agree, blank included.
    """
    group = RECORDS[group_number]
    # A one letter code ("D") means "D with a blank subsection".
    codes = {code.ljust(2) for code in group["record_codes"] if code}
    hits = []
    seen: set[int] = set()
    for index, struct in enumerate(MODEL):
        if not struct["mappings"] or struct["kind"] != "primary":
            continue
        for mapping in struct["mappings"]:
            combo = (mapping["section"] + mapping["subsection"]).ljust(2)
            if combo not in codes:
                continue
            if index not in seen:
                seen.add(index)
                hits.append((struct, mapping))
            break
    return hits


def primary_layout(layouts: dict) -> tuple[str, dict] | None:
    for number, layout in layouts.items():
        title = layout["title"].lower()
        if "continuation" in title or "extension" in title:
            continue
        if not layout["fields"]:
            continue
        return number, layout
    return None


def model_comparison(struct: dict, layout: dict) -> tuple[list[str], list[str]]:
    """Columns the spec defines but the struct does not cover, plus packed ones.

    The model sometimes types two adjacent spec columns as one field (the
    section and subsection codes become ``CombinedSectCode``); that is a
    representation choice, not a gap, so it is reported separately.
    """
    spec = {
        f["start"]: f
        for f in layout["fields"]
        if not f["name"].lower().startswith(("blank", "reserved"))
    }
    model = struct["fields"]

    covered = {}
    for start, field in spec.items():
        for candidate in model:
            if candidate["start"] <= start and candidate["end"] >= field["end"]:
                covered[start] = candidate
                break

    missing = [
        f"列 {start} {spec[start]['name']}（{spec[start]['length']}）"
        for start in sorted(spec)
        if start not in covered
    ]
    packed = [
        f"列 {m['start']}-{m['end']} `{m['name']}`"
        for m in model
        if sum(1 for start in spec if m["start"] <= start <= m["end"]) > 1
    ]
    return missing, packed


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #


def render_record_index() -> str:
    rows = []
    for number, group in RECORDS.items():
        present = [v for v in EDITIONS if group["editions"].get(v)]
        rows.append(
            [
                f"[{number}](02-records/{number}.md)",
                f"`{','.join(group['record_codes']) or '-'}`",
                group["title"],
                f"{len(group['editions'].get(LATEST, {}))}",
                " ".join(present),
            ]
        )
    return (
        "# 记录类型索引\n\n"
        f"共 {len(RECORDS)} 个记录组。每组一个参考页，列出全部子记录的列位表、"
        "版本差异与模型实现情况。\n\n"
        "记录代码即 `Section + Subsection`：`D` 表示 D 节、子节为空白；`PD` 表示 P 节 D 子节。\n\n"
        + table(["编号", "代码", "名称", "布局数", "出现于"], rows)
        + "\n\n> 布局数取 424-" + LATEST + "。早期版本记录的字段更少。\n"
    )


def render_record(number: str) -> str:
    group = RECORDS[number]
    present = [v for v in EDITIONS if group["editions"].get(v)]
    lines = [f"# {number} {group['title']}", ""]

    meta = [f"记录代码 `{','.join(group['record_codes']) or '-'}`"]
    meta.append(f"出现于 {' '.join('424-' + v for v in present)}")
    if not group["editions"].get(LATEST):
        meta.append(f"424-{LATEST} 已删除")
    lines.append("> " + " ｜ ".join(meta))
    lines.append("")

    layouts = group["editions"].get(LATEST) or group["editions"][present[-1]]
    edition = LATEST if group["editions"].get(LATEST) else present[-1]

    by_edition = {v: group["editions"].get(v) or {} for v in EDITIONS}

    for layout_number, layout in layouts.items():
        lines.append(f"## {layout_number} {layout['title']}")
        lines.append("")
        if layout.get("deleted_by"):
            lines.append(f"> 该记录在 424-{edition} 中标注：被 Supplement {layout['deleted_by']} 删除。")
            lines.append("")
        if layout.get("prose"):
            lines.append(prose_blocks(layout["prose"]))
            lines.append("")

        rows = []
        for field in layout["fields"]:
            rows.append(
                [
                    f"{field['start']}",
                    f"{field['end']}",
                    f"{field['length']}",
                    field["name"],
                    field.get("spec") or "",
                ]
            )
        lines.append(table(["列", "止", "长", "字段名", "引用"], rows))
        lines.append("")

        if layout.get("notes"):
            for note in layout["notes"]:
                lines.append(f"> {note}")
            lines.append("")

        # edition comparison
        variants = {}
        for edition_key, layouts_in_edition in by_edition.items():
            if layout_number in layouts_in_edition:
                variants[edition_key] = layouts_in_edition[layout_number]

        if len(variants) > 1:
            lines.append("### 版本差异")
            lines.append("")
            transitions = []
            keys = [v for v in EDITIONS if v in variants]
            for index in range(len(keys) - 1):
                before, after = keys[index], keys[index + 1]
                changes = layout_changes(variants[before], variants[after])
                if changes:
                    transitions.append((f"{before} → {after}", changes))
            # against the first edition that has it
            if len(keys) > 1:
                overall = layout_changes(variants[keys[0]], variants[keys[-1]])
                if transitions or overall:
                    lines.append(
                        f"下表比较 424-{keys[0]} 与 424-{keys[-1]}。"
                        "列位移动通常意味着整段字段重新排布，改代码时要同步调整。"
                    )
                    lines.append("")
                    if overall:
                        for change in overall:
                            lines.append(f"- {change}")
                        lines.append("")
                    if transitions:
                        lines.append("<details><summary>逐版过渡</summary>")
                        lines.append("")
                        for label, changes in transitions:
                            lines.append(f"**{label}**")
                            lines.append("")
                            for change in changes:
                                lines.append(f"- {change}")
                            lines.append("")
                        lines.append("</details>")
                        lines.append("")
        else:
            lines.append(
                f"> 该记录只在 424-{next(iter(variants))} 中定义。"
            )
            lines.append("")

        for struct, mapping in model_for(number):
            eighteen = group["editions"].get("18") or {}
            candidate = primary_layout(eighteen)
            if not candidate:
                continue
            layout_number, layout18 = candidate
            missing, packed = model_comparison(struct, layout18)
            lines.append("### 模型实现")
            lines.append("")
            lines.append(
                f"`{struct['struct']}`（`{struct['file']}`）实现 424-18 版 "
                f"{layout_number}，共 {len(struct['fields'])} 个字段。"
            )
            if missing:
                lines.append("")
                lines.append("规范中有、结构体未声明的列：" + "；".join(missing))
            if packed:
                lines.append("")
                lines.append("结构体把相邻两列合成一个类型：" + "；".join(packed))
            if not missing:
                lines.append("")
                lines.append("规范中的每一个非空白列都有对应字段。")
            lines.append("")

    return "\n".join(lines) + "\n"


def render_field_index() -> str:
    rows = []
    for number in sorted(FIELDS, key=lambda n: int(n.split(".")[1])):
        field = FIELDS[number]
        present = [v for v in EDITIONS if v in field["editions"]]
        rows.append(
            [
                f"[{number}](04-fields/{number}.md)",
                field["name"],
                field["abbreviation"] or "",
                " ".join(present) if len(present) < len(EDITIONS) else "全部",
                "✓" if number in CODES else "",
            ]
        )
    return (
        "# 字段定义索引\n\n"
        f"共 {len(FIELDS)} 个字段定义（第 5 章）。编号与 ARINC 424 正文一致，"
        "记录布局的「引用」列指向这些编号。\n\n"
        "「码表」列有 ✓ 的字段，其取值含义已结构化，可用 `arinc424.py codes 5.xx` 查询，"
        "也可直接看 [码表总表](05-code-tables.md)。\n\n"
        + table(["编号", "字段名", "缩写", "定义于", "码表"], rows)
        + "\n"
    )


def render_field(number: str) -> str:
    field = FIELDS[number]
    lines = [f"# {number} {field['name']}", ""]

    info = []
    if field["abbreviation"]:
        info.append(f"缩写 `{field['abbreviation']}`")
    present = [v for v in EDITIONS if v in field["editions"]]
    absent = [v for v in EDITIONS if v not in field["editions"]]
    info.append("定义于 " + " ".join("424-" + v for v in present))
    if absent:
        info.append("缺失于 " + " ".join("424-" + v for v in absent))
    lines.append("> " + " ｜ ".join(info))
    lines.append("")

    used = []
    for group_number, group in RECORDS.items():
        for layout_number, layout in (group["editions"].get(LATEST) or {}).items():
            for field_in_layout in layout["fields"]:
                if field_in_layout.get("spec") == number:
                    used.append(
                        f"{layout_number} 列 {field_in_layout['start']}"
                        f"（{field_in_layout['name']}）"
                    )
    if used:
        lines.append("**用于：** " + "；".join(sorted(set(used))[:14]))
        if len(used) > 14:
            lines[-1] += f" 等 {len(set(used))} 处"
        lines.append("")

    if field["prose"]:
        lines.append("## 定义")
        lines.append("")
        lines.append(prose_blocks(field["prose"]))
        lines.append("")

    codes = CODES.get(number)
    if codes:
        lines.append("## 码表")
        lines.append("")
        lines.append("> 取自 `arinc424-core` 的枚举，比正文表格更完整；变体名即语义。")
        lines.append("")
        for group in codes["groups"]:
            label = f"第 {group['position']} 列" if group["position"] else "取值"
            lines.append(f"**{label}** — `{group['enum']}`")
            lines.append("")
            rows = [[f"`{item['code']}`", code(item["variant"])] for item in group["entries"]]
            lines.append(table(["代码", "含义"], rows))
            lines.append("")

    spec_tables = field.get("tables") or []
    if spec_tables:
        lines.append("## 正文表格")
        lines.append("")
        for entry in spec_tables[:2]:
            lines.append(f"（424-{LATEST} 第 {entry['page']} 页）")
            lines.append("")
            rows = entry["rows"]
            if rows:
                lines.append(table(rows[0], rows[1:]))
                lines.append("")

    if len(present) > 1:
        lines.append("## 版本")
        lines.append("")
        rows = []
        for edition in EDITIONS:
            detail = field["editions"].get(edition)
            if detail:
                rows.append(
                    [f"424-{edition}", detail["name"], detail["abbreviation"] or "", f"{detail['page']}"]
                )
            else:
                rows.append([f"424-{edition}", "—", "", ""])
        lines.append(table(["版本", "字段名", "缩写", "页码"], rows))
        lines.append("")

    return "\n".join(lines) + "\n"


def render_code_tables() -> str:
    lines = [
        "# 码表总表",
        "",
        "ARINC 424 里的枚举字段，代码与其含义的对照。**这里的码表来自 "
        "`arinc424-core` 的 Rust 枚举**：每个 `'X' => Variant` 分支都是一个合法取值，"
        "变体名就是规范对该取值的描述。正文里的表格常有排版错乱，代码是更可靠的来源。",
        "",
        "用法：`arinc424.py codes 5.17`，或直接看下面的分节。",
        "",
        "## 目录",
        "",
    ]
    ordered = sorted(CODES, key=lambda n: int(n.split(".")[1]))
    for number in ordered:
        lines.append(f"- [{number} {CODES[number]['name']}](#{number.replace('.', '')}-{slug(CODES[number]['name'])})")
    lines.append("")

    for number in ordered:
        entry = CODES[number]
        anchor = f"{number.replace('.', '')}-{slug(entry['name'])}"
        lines.append(f'<a id="{anchor}"></a>')
        lines.append("")
        lines.append(f"## {number} {entry['name']}")
        lines.append("")
        if entry["abbreviation"]:
            lines.append(f"缩写 `{entry['abbreviation']}`")
            lines.append("")
        for group in entry["groups"]:
            label = f"第 {group['position']} 列" if group["position"] else "取值"
            lines.append(f"**{label}** — `{group['enum']}`（`{group['source']}`）")
            lines.append("")
            rows = [[f"`{item['code']}`", code(item["variant"])] for item in group["entries"]]
            lines.append(table(["代码", "含义"], rows))
            lines.append("")
    return "\n".join(lines) + "\n"


def render_edition_changes() -> str:
    lines = [
        "# 版本变更总览",
        "",
        "ARINC 424 每次改版都会增删记录类型、调整列位、扩充字段。这一页按版本顺序"
        "汇总变更，方便回答「这个字段是哪一版才有的」「这条记录的列位在 20 到 21 之间动过吗」。",
        "",
        "单条记录的细节用 `arinc424.py diff 4.1.2.1 --from 18 --to 23` 查。",
        "",
    ]

    # record groups by first edition
    first_seen = {}
    for edition in EDITIONS:
        new = []
        for number, group in RECORDS.items():
            if not group["editions"].get(edition):
                continue
            if number not in first_seen:
                first_seen[number] = edition
                new.append(f"{number} {group['title']}")
        if new:
            lines.append(f"## 424-{edition} 新增记录类型（{len(new)}）")
            lines.append("")
            for item in new:
                lines.append(f"- {item}")
            lines.append("")

    # layout counts per edition
    lines.append("## 各版记录数量")
    lines.append("")
    rows = []
    for edition in EDITIONS:
        groups = sum(1 for g in RECORDS.values() if g["editions"].get(edition))
        layouts = sum(len(g["editions"].get(edition) or {}) for g in RECORDS.values())
        fields = sum(1 for f in FIELDS.values() if edition in f["editions"])
        rows.append([f"424-{edition}", str(groups), str(layouts), str(fields), str(DB["meta"]["pages"][edition])])
    lines.append(table(["版本", "记录组", "布局", "字段定义", "页数"], rows))
    lines.append("")

    # per-transition field additions
    lines.append("## 各版新增的字段定义")
    lines.append("")
    for index in range(len(EDITIONS) - 1):
        before, after = EDITIONS[index], EDITIONS[index + 1]
        added = [
            f"{n} {f['name']}"
            for n, f in FIELDS.items()
            if after in f["editions"] and before not in f["editions"]
        ]
        if added:
            lines.append(f"**{before} → {after}**（{len(added)} 个）")
            lines.append("")
            for item in added:
                lines.append(f"- {item}")
            lines.append("")
    return "\n".join(lines) + "\n"


def render_model_mapping() -> str:
    lines = [
        "# 模型与规范对照",
        "",
        "`arinc424-model-rs` 实现的是 **ARINC 424-18**。后来的版本调整过列位，"
        "照 424-23 的表格改代码会写坏数据。这一页给出每个记录结构体与 424-18 布局的核对结果。",
        "",
    ]
    rows = []
    for struct in MODEL:
        target = "、".join(f"{m['section']}/{m['subsection'].strip() or '空白'}" for m in struct["mappings"])
        if struct["kind"] == "continuation":
            target = f"续记录（{struct.get('cont_type')}）"
        rows.append([f"`{struct['struct']}`", struct["kind"], target, str(len(struct["fields"]))])
    lines.append(table(["结构体", "类型", "记录代码", "字段数"], rows))
    lines.append("")

    lines.append("## 逐记录核对")
    lines.append("")
    lines.append(
        "只比较主记录：结构体是否覆盖 424-18 布局中的每一个非空白列。"
        "结构体把 Section/Subsection 两列合成一个类型的地方不算缺口，单独标为「合并表示」。"
    )
    lines.append("")
    for struct in MODEL:
        if struct["kind"] != "primary" or not struct["mappings"]:
            continue
        target = None
        for mapping in struct["mappings"]:
            combo = (mapping["section"] + mapping["subsection"]).ljust(2)
            for number, group in RECORDS.items():
                if combo not in {code.ljust(2) for code in group["record_codes"] if code}:
                    continue
                candidate = primary_layout(group["editions"].get("18") or {})
                if candidate:
                    target = (number, *candidate)
                    break
            if target:
                break
        if not target:
            lines.append(f"### `{struct['struct']}`")
            lines.append("")
            lines.append("未找到对应的 424-18 主记录布局。")
            lines.append("")
            continue

        _, layout_number, layout = target
        missing, packed = model_comparison(struct, layout)
        status = "一致" if not missing else "有缺口"
        lines.append(f"### `{struct['struct']}` ↔ {layout_number} {layout['title']}（{status}）")
        lines.append("")
        if missing:
            lines.append("规范有、结构体缺：" + "；".join(missing))
            lines.append("")
        if packed:
            lines.append("合并表示：" + "；".join(packed))
            lines.append("")
        if not missing:
            lines.append("规范中的每一个非空白列都有对应字段。")
            lines.append("")
    return "\n".join(lines) + "\n"


ORIENTATION = """# 从这里开始

ARINC 424 是航空导航数据的**文本交换标准**。它规定了一条记录怎么用 132 个定宽字符
表示一个机场、一个导航台、一段航路或一条进离场程序。几乎所有航电数据库（FMS、
机模、飞行计划软件）的上游都是它。

这一页讲结构。具体某个字段怎么编码，看 [字段索引](03-field-index.md)；某条记录有哪些列，
看 [记录类型索引](01-record-index.md)。

## 一条记录的形状

每行固定 132 列，没有分隔符，**一切靠列位**。所有版本的记录都共享同一副骨架：

| 列 | 字段 | 说明 |
|---|---|---|
| 1 | Record Type | `S` 标准记录，`T` 定制记录 |
| 2–4 | Customer/Area Code | 数据提供方代码，常见 `USA`、`EUR` |
| 5 | Section Code | 大类：`D` 导航台、`E` 航路、`P` 机场 |
| 6 或 13 | Subsection Code | 小类，与 Section 组成两字母记录码 |
| 22 或 39 | Continuation Record No. | `0` 或空白是主记录，`1`–`9` 是第几条续记录 |
| 23 或 40 | Application Type | **只在续记录里有**，决定这条续记录装什么 |
| 124–128 | File Record Number | 文件内序号 |
| 129–132 | Cycle Date | `YYNN`，如 `2607` 是 2026 年第 7 个 AIRAC 周期 |

Subsection 的列位不固定：机场类记录把它挪到第 13 列，因为第 7–12 列要放
机场 ICAO 代码。SID/STAR/进近记录更特殊——它们的续记录号在第 39 列、应用类型在第 40 列。
**不要假设它总在第 22 列，要看具体记录的列位表。**

## 主记录与续记录

一条主记录的 132 列装不下所有信息时，会跟若干条**续记录**。续记录的前 21 列（或前 38 列）
通常照抄主记录，从第 22 列（或第 39 列）开始才是自己的内容：

- **续记录号**：`0` 或空白 = 主记录；`1`、`2`… 是续记录在序列中的位置。
- **应用类型**：一个字母，说明这条续记录装的是注释、飞行计划信息、仿真参数、还是
  导航台覆盖限制。同一个 Section 下可能有五六种续记录，靠这个字母区分。

解码时如果看到第 22 列不是 `0`，就要去找对应的续记录布局，否则会把注释当成字段读。

## Section 与 Subsection

记录码是 Section + Subsection 两字母拼接，例如 `PD` 是 Section `P`（机场）的
Subsection `D`（SID）。只有 Section 没有 Subsection 的（如 `D` 导航台），第二字母是空白。

下面是从规格库里汇总出来的记录码一览：

"""

RECORD_CODES_TAIL = """
## 数值怎么编

ARINC 424 里的数字大多是**定长定标的字符串**，不是自由格式的数：

- **经纬度**：度分秒压缩，纬度 9 位、经度 10 位，首字符 `N`/`S`、`E`/`W`。
  `N33591899` 读作北纬 33°59′18.99″。
- **频率**：VOR 5 位是 `11390`（113.90 MHz）；NDB 5 位是千赫。
- **磁差**：5 位，首位是 `E`/`W`，后四位是十分之一度。
- **高度**：5 位，单位英尺；`FL` 前缀表示飞行高度层。
- **周期日期**：4 位 `YYNN`。

精确规则以字段页为准，不要凭印象凑位数——宽度错了整条记录就错位。

## 六个版本

工作区里的 PDF 覆盖 424-18 到 424-23。结构随版本演进：

- 424-18 是 `arinc424-model-rs` 实现的那一版，也是很多数据供应商的输出格式。
- 中间几版陆续加了 PBN、FRA、TAA、GBAS 等概念，续记录种类变多。
- 424-23 是当前最新，字段最全。

**版本之间列位会动。** 典型例子：VHF 导航台的 VOR Name 在 424-18 占 94–123 列（30 位），
到 424-23 缩到 94–118（25 位），腾出的 5 列塞进了 VFR 检查点等新字段。
拿 424-23 的表格去改按 424-18 写的代码，会让后面所有字段错位。

每个记录页的「版本差异」一节列出了这些变化；跨版本的完整变更见
[版本变更总览](06-edition-changes.md)。

## 怎么用这个 skill

先判断你要做什么，再决定看哪里：

| 你要做的事 | 用什么 |
|---|---|
| 把一条 132 列记录拆成字段 | `arinc424.py decode "<记录>"` |
| 按字段值拼出一条记录 | `arinc424.py encode 4.1.2.1 1=S 5=D 14=LAX …` |
| 查某条记录有哪些列 | [记录类型索引](01-record-index.md) → `02-records/` |
| 查某个字段的含义和取值 | [字段索引](03-field-index.md) → `04-fields/` |
| 查代码对应什么意思（PATH TERM、航路类型…） | [码表总表](05-code-tables.md) |
| 比较两个版本的差异 | `arinc424.py diff 4.1.2.1 --from 18 --to 23` |
| 改 Rust 模型 | [模型与规范对照](08-model-mapping.md) |

工具都在 `scripts/arinc424.py`，零依赖，直接跑 Python 即可：

```bash
python scripts/arinc424.py record 4.1.9.1          # 看布局
python scripts/arinc424.py decode "$(cat line.txt)" # 解码
python scripts/arinc424.py field 5.21               # 看字段定义
python scripts/arinc424.py list records             # 列出全部记录
```

**默认版本是最新的 424-23。** 如果你手上的数据或代码是 424-18，加 `--version 18`，
否则列位会对不上。
"""


GLOSSARY_TERMS = [
    ("ACF", "机场/设施", "Aerodrome/Company/Facility 相关数据，泛指机场、导航台等地面设施。"),
    ("AIRAC", "定期生效的航行资料周期", "28 天一个周期，导航数据按它发布。记录末尾的 Cycle Date 就是这个周期的编号。"),
    ("Application Type", "应用类型", "续记录第 23 列（机场程序是第 40 列）的字母，说明这条续记录装什么内容。"),
    ("Continuation Record", "续记录", "一条主记录装不下时的后续记录，靠 Continuation Record No. 排序。"),
    ("Customer/Area Code", "客户/区域代码", "第 2–4 列，标识数据提供方，如 USA、EUR。"),
    ("Cycle Date", "周期日期", "第 129–132 列，`YYNN` 格式，记录所属的 AIRAC 周期。"),
    ("DME", "测距仪", "Distance Measuring Equipment，给出到台的斜距。常与 VOR 并置成 VOR/DME。"),
    ("Duplicate Indicator", "重复指示符", "同名导航台/航路点出现多次时，用第二个字母区分（如 `LAX` 与 `LAXA`）。"),
    ("Enroute Airway", "航路", "航路航线，由一串航路点与航段组成，记录码 `ER`。"),
    ("File Record Number", "文件记录号", "第 124–128 列，文件内序号，用于定位与增量更新。"),
    ("FIR / UIR", "飞行情报区 / 高空情报区", "Flight Information Region / Upper FIR，空域管理的基本单元。"),
    ("Fix", "定位点", "可用于定位的地理点，包括航路点、导航台、机场基准点。"),
    ("FRA", "自由航路空域", "Free Route Airspace，允许航路点之间直飞，不依赖固定航路。"),
    ("GLS", "GNSS 着陆系统", "GBAS Landing System，基于 GBAS 的精密进近。"),
    ("ILS", "仪表着陆系统", "由航向台（LOC）、下滑台（GS）与指点标组成。"),
    ("Localizer", "航向台", "ILS 的水平引导分量，给出跑道中心线方向。"),
    ("Magnetic Variation", "磁差", "磁北与真北的夹角，东偏为正。记录里 5 位，首位 E/W。"),
    ("MORA", "最低偏航高度", "Minimum Off-Route Altitude，网格化的安全高度。"),
    ("MSA", "最低扇区高度", "Minimum Sector Altitude，以某点为中心、按扇区给出的最低安全高度。"),
    ("NAVAID", "导航台", "VOR、NDB、TACAN 等地面导航设施的统称。"),
    ("NDB", "无方向性信标", "Non-Directional Beacon，靠 ADF 测向。频率单位 kHz。"),
    ("PBN", "基于性能的导航", "Performance Based Navigation，涵盖 RNAV 与 RNP 规范。"),
    ("Preferred Route", "优选航路", "预先定义的常用航路组合，记录码 `ET`。"),
    ("Primary Record", "主记录", "续记录号为 0 的那条记录，定义一个实体的主体信息。"),
    ("Procedure", "程序", "SID、STAR、进近的统称，由一串航段（leg）组成。"),
    ("RNAV", "区域导航", "Area Navigation，允许航空器沿任意期望航径飞行。"),
    ("RNP", "所需导航性能", "Required Navigation Performance，带机载性能监视与告警的 RNAV。"),
    ("SID", "标准仪表离场程序", "Standard Instrument Departure，记录码 `PD`。"),
    ("STAR", "标准终端进场程序", "Standard Terminal Arrival Route，记录码 `PE`。"),
    ("TAA", "终端进场高度", "Terminal Arrival Altitude，进近程序周边的扇区高度。"),
    ("TACAN", "战术空中导航", "军用 VOR/DME 组合，记录码 `DT`。"),
    ("TCH", "跑道入口高", "Threshold Crossing Height，航空器过跑道入口时的轮高。"),
    ("Transition", "过渡", "连接航路与程序、或程序与进近的过渡航段，用 Transition Identifier 标识。"),
    ("VOR", "甚高频全向信标", "VHF Omnidirectional Range，给出相对台的磁方位。频率 108–118 MHz。"),
    ("Waypoint", "航路点", "程序或航路上用于定义航径的点，不一定是实体设施。"),
    ("Waypoint Description Code", "航路点描述码", "第 40–43 列的四字符标记，说明这个点是什么（机场、导航台、飞越点等）。"),
]

PATH_TERM = [
    ("IF", "Initial Fix", "起始点：只定义位置，本身不构成航段。"),
    ("TF", "Track to Fix", "从当前点直飞下一个定位点，航径是大圆航线。"),
    ("CF", "Course to Fix", "按指定航向飞到定位点，航径是固定方位线。"),
    ("DF", "Direct to Fix", "从当前位置直飞定位点，不约束进入方位。"),
    ("FA", "Fix to Altitude", "从定位点沿航径飞至指定高度。"),
    ("FC", "Track from Fix to Distance", "从定位点沿航道飞指定距离。"),
    ("FD", "Track from Fix to DME Distance", "从定位点沿航道飞到某个 DME 距离。"),
    ("FM", "Fix to Manual Termination", "从定位点开始，航径由飞行员手动终止。"),
    ("CA", "Course to Altitude", "沿指定航向爬升到某个高度。"),
    ("CD", "Course to DME Distance", "沿指定航向飞到某个 DME 距离。"),
    ("CI", "Course to Intercept", "沿指定航向飞到切入下一个航径。"),
    ("CR", "Course to Radial", "沿指定航向飞到某条径向线。"),
    ("RF", "Constant Radius Arc", "定半径圆弧，圆心与半径由相邻航段确定。"),
    ("AF", "Arc to Fix", "沿圆弧飞到定位点。"),
    ("VA", "Heading to Altitude", "按指定航向飞到某个高度。"),
    ("VD", "Heading to DME Distance", "按指定航向飞到某个 DME 距离。"),
    ("VI", "Heading to Intercept", "按指定航向飞到切入下一个航径。"),
    ("VM", "Heading to Manual Termination", "按指定航向飞，由飞行员手动终止。"),
    ("VR", "Heading to Radial", "按指定航向飞到某条径向线。"),
    ("FI", "Fix to Intercept", "从定位点飞到切入下一个航径。"),
    ("HA", "Hold to Altitude", "等待航线，到达指定高度后退出。"),
    ("HF", "Hold to Fix", "等待航线，到达定位点后退出。"),
    ("HM", "Hold to Manual Termination", "等待航线，由飞行员手动退出。"),
]


def render_orientation() -> str:
    rows = []
    for number, group in RECORDS.items():
        latest_layouts = group["editions"].get(LATEST) or {}
        if not latest_layouts:
            continue
        layouts = "、".join(sorted(latest_layouts))
        rows.append(
            [
                f"`{','.join(group['record_codes']) or '-'}`",
                group["title"],
                f"{len(latest_layouts)}",
                f"[{number}](02-records/{number}.md)",
            ]
        )
    body = ORIENTATION + table(["记录码", "名称", "布局数", "详情"], rows) + "\n" + RECORD_CODES_TAIL
    return body


def render_glossary() -> str:
    lines = [
        "# 术语与约定",
        "",
        "ARINC 424 的正文用大量缩写。这一页收常用术语，以及航径终止码的完整含义。",
        "",
        "## 常用术语",
        "",
    ]
    rows = [[f"**{term}**", zh, definition] for term, zh, definition in GLOSSARY_TERMS]
    lines.append(table(["术语", "中文", "含义"], rows))
    lines.append("")
    lines.append("## 航径终止码（PATH TERM）")
    lines.append("")
    lines.append(
        "程序记录的每个航段都带一个两字母的航径终止码，决定这一段怎么飞。"
        "它定义在字段 5.21，完整取值见 [码表](05-code-tables.md#521-path-and-termination)。"
    )
    lines.append("")
    rows = [[f"`{code_}`", name, definition] for code_, name, definition in PATH_TERM]
    lines.append(table(["代码", "全称", "含义"], rows))
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for stale in (OUT / "02-records", OUT / "04-fields"):
        if stale.exists():
            shutil.rmtree(stale)
    (OUT / "02-records").mkdir()
    (OUT / "04-fields").mkdir()

    (OUT / "00-orientation.md").write_text(render_orientation(), encoding="utf-8")
    (OUT / "01-record-index.md").write_text(render_record_index(), encoding="utf-8")
    for number in RECORDS:
        (OUT / "02-records" / f"{number}.md").write_text(render_record(number), encoding="utf-8")

    (OUT / "03-field-index.md").write_text(render_field_index(), encoding="utf-8")
    for number in FIELDS:
        (OUT / "04-fields" / f"{number}.md").write_text(render_field(number), encoding="utf-8")

    (OUT / "05-code-tables.md").write_text(render_code_tables(), encoding="utf-8")
    (OUT / "06-edition-changes.md").write_text(render_edition_changes(), encoding="utf-8")
    (OUT / "07-glossary.md").write_text(render_glossary(), encoding="utf-8")
    (OUT / "08-model-mapping.md").write_text(render_model_mapping(), encoding="utf-8")

    if TEMPLATES.exists():
        for template in TEMPLATES.glob("*.md"):
            shutil.copy(template, OUT / template.name)

    total = sum(1 for _ in OUT.rglob("*.md"))
    print(f"rendered {total} markdown files into references/")


if __name__ == "__main__":
    main()
