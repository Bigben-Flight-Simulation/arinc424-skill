# 从这里开始

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

| 记录码 | 名称 | 布局数 | 详情 |
|---|---|---|---|
| `D` | VHF NAVAID Record (D) | 5 | [4.1.2](02-records/4.1.2.md) |
| `DB,PN` | NDB NAVAID Record (DB or PN) | 4 | [4.1.3](02-records/4.1.3.md) |
| `EA,PC` | Waypoint Record (EA) or (PC) | 3 | [4.1.4](02-records/4.1.4.md) |
| `EP` | Holding Pattern Records (EP) | 3 | [4.1.5](02-records/4.1.5.md) |
| `ER` | Enroute Airways Records (ER) | 3 | [4.1.6](02-records/4.1.6.md) |
| `PA` | Airport Records (PA) | 3 | [4.1.7](02-records/4.1.7.md) |
| `PB` | Airport Gate Records (PB) | 2 | [4.1.8](02-records/4.1.8.md) |
| `PD,PE,PF` | Airport SID/STAR/Approach (PD, PE, and PF) | 5 | [4.1.9](02-records/4.1.9.md) |
| `PG` | Runway Records (PG) | 3 | [4.1.10](02-records/4.1.10.md) |
| `PI` | Airport and Heliport Localizer and Glideslope Records (PI) | 3 | [4.1.11](02-records/4.1.11.md) |
| `R` | Company Route Records (R) | 1 | [4.1.12](02-records/4.1.12.md) |
| `PM` | Airport and Heliport Localizer Marker Records (PM) | 2 | [4.1.13](02-records/4.1.13.md) |
| `PV` | Airport Communications Records (PV) | 6 | [4.1.14](02-records/4.1.14.md) |
| `EM` | Airways Marker Records (EM) | 2 | [4.1.15](02-records/4.1.15.md) |
| `TC` | Cruising Tables Records (TC) | 1 | [4.1.16](02-records/4.1.16.md) |
| `UF` | FIR/UIR Records (UF) | 2 | [4.1.17](02-records/4.1.17.md) |
| `UR` | Restrictive Airspace Records (UR) | 4 | [4.1.18](02-records/4.1.18.md) |
| `AS` | Grid MORA Records (AS) | 1 | [4.1.19](02-records/4.1.19.md) |
| `PS` | Airport MSA (Minimum Sector Altitude) Records (PS) | 3 | [4.1.20](02-records/4.1.20.md) |
| `EU` | Enroute Airways Restriction Records (EU) | 4 | [4.1.21](02-records/4.1.21.md) |
| `PL` | Airport and Heliport MLS (Azimuth, Elevation and Back Azimuth) Records (PL) | 2 | [4.1.22](02-records/4.1.22.md) |
| `EV` | Enroute Communications Records (EV) | 4 | [4.1.23](02-records/4.1.23.md) |
| `ET` | Preferred Routes Records (ET) | 4 | [4.1.24](02-records/4.1.24.md) |
| `UC` | Controlled Airspace Records (UC) | 5 | [4.1.25](02-records/4.1.25.md) |
| `TG` | Geographical Reference Table Records (TG) | 2 | [4.1.26](02-records/4.1.26.md) |
| `PR` | Flight Planning Arrival/Departure Data Records (PR) | 4 | [4.1.27](02-records/4.1.27.md) |
| `PP` | Airport SBAS Path Point Records (PP) | 2 | [4.1.28](02-records/4.1.28.md) |
| `PT` | GLS Record (PT) | 2 | [4.1.29](02-records/4.1.29.md) |
| `PK` | Airport TAA (PK) | 2 | [4.1.31](02-records/4.1.31.md) |
| `RA` | Alternate Record (RA) | 1 | [4.1.30](02-records/4.1.30.md) |
| `HA` | Heliport Records (HA) | 3 | [4.2.1](02-records/4.2.1.md) |
| `HC` | Heliport Terminal Waypoint Records (HC) | 3 | [4.2.2](02-records/4.2.2.md) |
| `HD,HE,HF` | Heliport SID/STAR/Approach (HD/HE/HF) | 5 | [4.2.3](02-records/4.2.3.md) |
| `HS` | Heliport MSA (HS) | 3 | [4.2.4](02-records/4.2.4.md) |
| `HV` | Heliport Communications Records (HV) | 6 | [4.2.5](02-records/4.2.5.md) |
| `HK` | Heliport (TAA) (HK) | 2 | [4.2.6](02-records/4.2.6.md) |
| `DT` | TACAN-Only NAVAID Record (DT) | 5 | [4.1.32](02-records/4.1.32.md) |
| `ES` | Special Activity Area (ES) | 1 | [4.1.33](02-records/4.1.33.md) |
| `TV` | Communication Type Translation (TV) | 1 | [4.1.34](02-records/4.1.34.md) |
| `RH` | Helicopter Operations Company Route Records (RH) | 1 | [4.2.7](02-records/4.2.7.md) |
| `PQ` | GBAS Path Point Record (PQ) | 2 | [4.1.35](02-records/4.1.35.md) |
| `HP` | Helicopter Operations SBAS Path Point Records (HP) | 2 | [4.2.8](02-records/4.2.8.md) |
| `PH` | Airport Helipad Record (PH) | 1 | [4.1.36](02-records/4.1.36.md) |
| `HH` | Heliport Helipad Record (HH) | 1 | [4.2.9](02-records/4.2.9.md) |
| `TL` | ATN Data (ATN NSAP) Record (TL) | 1 | [4.1.37](02-records/4.1.37.md) |

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
