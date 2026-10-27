---
name: arinc424
description: ARINC 424 导航数据规范的全量参考与工具集，覆盖 424-18 到 424-23 六个版本。用于解释 132 列定宽记录的每一个字段、解析或构造 .dat/.txt 导航数据行、查询 PATH TERM、Waypoint Description Code、Route Type、NAVAID Class 等代码表、比较版本间的列位变化，以及在 arinc424-model-rs 中扩展记录类型。当用户提到 ARINC 424、导航数据库、navdata、132 列记录、SID/STAR/进近编码、航路点、导航台记录，或需要解读一段固定宽度的航空数据时使用。
---

# ARINC 424 导航数据

ARINC 424 用 132 个定宽字符描述一个机场、导航台、航路或程序。字段位置固定、无分隔符，
所以**列位就是语义**：一个字符的偏移会让整条记录错位。

这个 skill 把六个版本的规范、`arinc424-model-rs` 的列位定义和代码表整理成可查的数据，
并提供命令行工具做解码、编码和版本对比。

## 先做判断

| 用户想要 | 怎么做 |
|---|---|
| 看懂一条记录 | `python scripts/arinc424.py decode "<132列>"` |
| 造一条记录 | `python scripts/arinc424.py encode 4.1.2.1 1=S 5=D …` |
| 知道某记录有哪些列 | `record 4.1.9.1`，或读 `references/02-records/4.1.9.md` |
| 知道某字段什么意思 | `field 5.21`，或读 `references/04-fields/5.21.md` |
| 知道代码含义 | `codes 5.17`，或读 `references/05-code-tables.md` |
| 比较版本差异 | `diff 4.1.2.1 --from 18 --to 23` |
| 改 Rust 模型 | 读 `references/09-rust-guide.md`（加记录/字段/码表的步骤）；`references/08-model-mapping.md` 是逐列核对表 |

工具在 `scripts/arinc424.py`，只用标准库。数据在 `data/arinc424.json`。

## 三条必须先确认的事

**一、这是哪一版的数据？** 六个版本的列位不一样。VHF 导航台的 VOR Name 在 424-18 占
94–123 列，在 424-23 只占 94–118 列，后面挤进了新字段。默认按 424-23 解析，处理
424-18 的数据要显式 `--version 18`。

**二、这是主记录还是续记录？** 第 22 列（机场程序是第 39 列）不是 `0` 或空白，就是续记录。
续记录第 23 列（机场程序第 40 列）的字母说明它装的是什么。按主记录的布局去读续记录，
会把注释、飞行计划信息当成字段。

**三、`arinc424-model-rs` 实现的是 424-18。** 改那个仓库的代码时，列位只能以 424-18 为准。
每个记录页的「模型实现」一节已经核对过结构体与 424-18 布局的对应关系。

## 工作流

### 解析一条记录

```bash
python scripts/arinc424.py decode "SUSAD   KJFK ... "
```

输出逐字段的列区间、原名、原值和代码含义。记录类型由第 5、6 列（或第 13 列）的
Section/Subsection 自动判定，续记录再按第 23 列的应用类型选布局。

需要机器可读就用 `--json`。

### 构造一条记录

```bash
python scripts/arinc424.py encode 4.1.2.1 1=S 2=USA 5=D 14=LAX 23=11390 …
```

键可以是列号，也可以是字段名。输出定长 132 字符，空白补齐。**构造前先确认版本的列位**，
尤其长度变化过的字段（如 VOR Name）。

### 查字段与代码

```bash
python scripts/arinc424.py field 5.17     # 定义、码表、被哪些列引用
python scripts/arinc424.py codes 5.21     # 只列码表
python scripts/arinc424.py search "waypoint description"
```

码表来自 `arinc424-core` 的 Rust 枚举，比 PDF 正文的表格更完整——正文排版经常把
相邻列挤在一起。

### 比较版本

```bash
python scripts/arinc424.py diff 4.1.2.1 --from 18 --to 23
python scripts/arinc424.py diff 5.17                  # 字段在各版的存在情况
```

字段按名称配对，列位移动、长度变化、引用变化都会列出来。

## 参考库导航

```
references/
  00-orientation.md      记录结构、Section/Subsection、数值编码约定、怎么用本 skill
  01-record-index.md     45 个记录组索引
  02-records/<编号>.md   每组一页：列位表 + 版本差异 + 模型实现核对
  03-field-index.md      343 个字段索引（含码表标记）
  04-fields/<5.xx>.md    每字段一页：定义原文 + 码表 + 引用的列
  05-code-tables.md      全部码表（PATH TERM、Route Type、NAVAID Class…）
  06-edition-changes.md  六版变更总览
  07-glossary.md         术语与航径终止码释义
  08-model-mapping.md    Rust 结构体与 424-18 布局的逐列核对
  09-rust-guide.md       怎么调用 arinc424-model-rs、怎么扩展记录类型
```

字段页按规范编号命名，直接读：`references/04-fields/5.21.md`。

## 回答时的注意

- 引用列位时**必须带版本号**，例如「424-18 的第 94–123 列」。脱离版本的列位是错的。
- 记录布局的「引用」列指向第 5 章字段编号，`5.61` 这类编号在各版之间稳定，可以跨版引用。
- 经纬度是度分秒压缩的定长串，不是浮点数。`N33591899` 是北纬 33°59′18.99″。
  不要把它当十进制数四舍五入。
- 空白（Blank）和保留（Reserved）列不是「没有字段」，它们是布局的一部分，
  解析时要保留原位。
- 拿不准某个字段能否为空、长度多少时，去读它的字段页，不要凭常见格式推断。

## 数据来源

- `docs/` 下 424-18 至 424-23 六份 PDF，记录布局与字段定义从中提取，
  每条布局都用「列 1–132 无空洞」校验过。
- 码表与记录结构体来自 `arinc424-model-rs`（v0.14.x）。
- 重建：`python tools/build.py` 后 `python tools/render.py`。
- 自检：`python tests/acceptance.py`（652 条布局的列位完整性、45 组记录编解码往返、
  文档与数据库一致）。
- 排查 PDF 提取：`python tools/debug_layout.py 23`，打印该版里「有布局表却没能铺满
  1–132 列」的小节。
