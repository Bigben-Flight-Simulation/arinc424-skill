# 模型与规范对照

`arinc424-model-rs` 实现的是 **ARINC 424-18**。后来的版本调整过列位，照 424-23 的表格改代码会写坏数据。这一页给出每个记录结构体与 424-18 布局的核对结果。

| 结构体 | 类型 | 记录代码 | 字段数 |
|---|---|---|---|
| `AirportPrimary` | primary | P/A | 29 |
| `AirportLocalizerAndGlideSlopePrimary` | primary | P/I | 29 |
| `AirportSidPrimary` | primary | P/D | 43 |
| `AirportStarPrimary` | primary | P/E | 43 |
| `AirportApproachPrimary` | primary | P/F | 43 |
| `AirportRunwayPrimary` | primary | P/G | 27 |
| `FlightPlanningContinuationRecord` | continuation | 续记录（P） | 9 |
| `SimulationContinuationRecord` | continuation | 续记录（S） | 7 |
| `StandardContinuationRecord` | continuation | 续记录（A） | 6 |
| `EnrouteAirwayPrimaryRecord` | primary | E/R | 31 |
| `HoldingPatternPrimaryRecord` | primary | E/P | 23 |
| `NdbPrimaryRecord` | primary | D/B、P/N | 18 |
| `VhfPrimaryRecord` | primary | D/空白 | 25 |
| `VhfLimitationBlock` | primary |  | 5 |
| `VhfLimitationContinuationRecord` | continuation | 续记录（L） | 9 |
| `EnrouteWaypointPrimaryRecord` | primary | E/A | 19 |
| `TerminalWaypointPrimaryRecord` | primary | P/C | 19 |

## 逐记录核对

只比较主记录：结构体是否覆盖 424-18 布局中的每一个非空白列。结构体把 Section/Subsection 两列合成一个类型的地方不算缺口，单独标为「合并表示」。

### `AirportPrimary` ↔ 4.1.7.1 Airport Primary Records（一致）

规范中的每一个非空白列都有对应字段。

### `AirportLocalizerAndGlideSlopePrimary` ↔ 4.1.11.1 Airport and Heliport Localizer and Glide Slope（一致）

合并表示：列 109-110 `supporting_facility_sect_subs_code`

规范中的每一个非空白列都有对应字段。

### `AirportSidPrimary` ↔ 4.1.9.1 Airport SID/STAR/Approach Primary Records（有缺口）

规范有、结构体缺：列 112 Indicator（5）

合并表示：列 37-38 `fix_sect_subs_code`；列 79-80 `recd_nav_sect_subs_code`；列 119-120 `apch_route_qualifier`

### `AirportStarPrimary` ↔ 4.1.9.1 Airport SID/STAR/Approach Primary Records（有缺口）

规范有、结构体缺：列 112 Indicator（5）

合并表示：列 37-38 `fix_sect_subs_code`；列 79-80 `recd_nav_sect_subs_code`；列 119-120 `apch_route_qualifier`

### `AirportApproachPrimary` ↔ 4.1.9.1 Airport SID/STAR/Approach Primary Records（有缺口）

规范有、结构体缺：列 112 Indicator（5）

合并表示：列 37-38 `fix_sect_subs_code`；列 79-80 `recd_nav_sect_subs_code`；列 119-120 `apch_route_qualifier`

### `AirportRunwayPrimary` ↔ 4.1.10.1 Runway Primary Records（一致）

规范中的每一个非空白列都有对应字段。

### `EnrouteAirwayPrimaryRecord` ↔ 4.1.6.1 Enroute Airways Primary Records（一致）

合并表示：列 37-38 `fix_sect_subs_code`

规范中的每一个非空白列都有对应字段。

### `HoldingPatternPrimaryRecord` ↔ 4.1.5.1 Holding Pattern Primary Records（一致）

合并表示：列 37-38 `fix_sect_subs_code`

规范中的每一个非空白列都有对应字段。

### `NdbPrimaryRecord` ↔ 4.1.3.1 NDB NAVAID Primary Records（一致）

规范中的每一个非空白列都有对应字段。

### `VhfPrimaryRecord` ↔ 4.1.2.1 VHF NAVAID Primary Records（一致）

规范中的每一个非空白列都有对应字段。

### `EnrouteWaypointPrimaryRecord` ↔ 4.1.4.1 Waypoint Primary Records（有缺口）

规范有、结构体缺：列 13 Subsection（1）

### `TerminalWaypointPrimaryRecord` ↔ 4.1.4.1 Waypoint Primary Records（有缺口）

规范有、结构体缺：列 6 Subsection Code（1）

