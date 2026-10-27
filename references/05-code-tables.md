# 码表总表

ARINC 424 里的枚举字段，代码与其含义的对照。**这里的码表来自 `arinc424-core` 的 Rust 枚举**：每个 `'X' => Variant` 分支都是一个合法取值，变体名就是规范对该取值的描述。正文里的表格常有排版错乱，代码是更可靠的来源。

用法：`arinc424.py codes 5.17`，或直接看下面的分节。

## 目录

- [5.2 Record Type](#52-record-type)
- [5.3 Customer/Area Code](#53-customer-area-code)
- [5.4 Section Code](#54-section-code)
- [5.5 Subsection Code](#55-subsection-code)
- [5.7 Route Type](#57-route-type)
- [5.17 Waypoint Description Code](#517-waypoint-description-code)
- [5.18 Boundary Code](#518-boundary-code)
- [5.19 Level](#519-level)
- [5.20 Turn Direction](#520-turn-direction)
- [5.21 Path and Termination](#521-path-and-termination)
- [5.29 Altitude Description](#529-altitude-description)
- [5.35 NAVAID Class](#535-navaid-class)
- [5.42 Waypoint Type](#542-waypoint-type)
- [5.49 Localizer/Azimuth Position Reference](#549-localizer-azimuth-position-reference)
- [5.80 ILS/MLS/GLS Category](#580-ils-mls-gls-category)
- [5.81 ATC Indicator](#581-atc-indicator)
- [5.82 Waypoint Usage](#582-waypoint-usage)
- [5.91 Continuation Record Application Type](#591-continuation-record-application-type)
- [5.93 Facility Characteristics](#593-facility-characteristics)
- [5.114 Duplicate Indicator](#5114-duplicate-indicator)
- [5.115 Directional Restriction](#5115-directional-restriction)
- [5.149 Navaid Usable Range](#5149-navaid-usable-range)
- [5.152 Start/End Indicator](#5152-start-end-indicator)
- [5.165 Magnetic/True Indicator](#5165-magnetic-true-indicator)
- [5.177 Public/Military Indicator](#5177-public-military-indicator)
- [5.178 Time Zone](#5178-time-zone)
- [5.187 Distance Description](#5187-distance-description)
- [5.196 Name Format Indicator](#5196-name-format-indicator)
- [5.205 Navaid Limitation Code](#5205-navaid-limitation-code)
- [5.206 Component Affected Indicator](#5206-component-affected-indicator)
- [5.207 Sector From/Sector To](#5207-sector-from-sector-to)
- [5.210 Sequence End Indicator](#5210-sequence-end-indicator)
- [5.222 GNSS/FMS Indicator](#5222-gnss-fms-indicator)
- [5.249 Surface Code](#5249-surface-code)
- [5.261 Speed Limit Description](#5261-speed-limit-description)
- [5.270 TCH Value Indicator](#5270-tch-value-indicator)

<a id="52-record-type"></a>

## 5.2 Record Type

缩写 `S/T`

**取值** — `RecordType`（`arinc424-core::data_types::record_type`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `S` | Standard |
| `T` | Tailored |

<a id="53-customer-area-code"></a>

## 5.3 Customer/Area Code

缩写 `CUST/AREA`

**取值** — `CustAreaItem`（`arinc424-core::data_types::cust_area`）

| 代码 | 含义 |
|---|---|
| `AFR` | Africa |
| `CAN` | Canada And Alaska |
| `EEU` | Eastern Europe |
| `EUR` | Europe |
| `LAM` | Latin America |
| `MES` | Middle East South Asia |
| `PAC` | Pacific |
| `SAM` | South America |
| `SPA` | South Pacific |
| `USA` | USA |

<a id="54-section-code"></a>

## 5.4 Section Code

缩写 `SEC CODE`

**取值** — `SectionCode`（`arinc424-core::data_types::section_code`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Mora |
| `D` | Navaid |
| `E` | Enroute |
| `H` | Heliport |
| `P` | Airport |
| `R` | Company Routes |
| `T` | Tables |
| `U` | Airspace |

<a id="55-subsection-code"></a>

## 5.5 Subsection Code

缩写 `SUB CODE`

**取值** — `AirportSubsCode`（`arinc424-core::data_types::subs_code::airport`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Reference Points |
| `B` | Gates |
| `C` | Terminal Waypoints |
| `D` | Sids |
| `E` | Stars |
| `F` | Approach Procedures |
| `G` | Runways |
| `I` | Localizer Or Glide Slope |
| `K` | Taa |
| `L` | Mls |
| `M` | Localizer Marker |
| `N` | Terminal Ndb |
| `P` | Path Point |
| `R` | Flt Planning Arr Dep |
| `S` | Msa |
| `T` | Gls Station |
| `V` | Communications |

**取值** — `AirspaceSubsCode`（`arinc424-core::data_types::subs_code::airspace`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `C` | Controlled Airspace |
| `F` | Fir Or Uir |
| `R` | Restrictive Airspace |

**取值** — `CompanyRoutesSubsCode`（`arinc424-core::data_types::subs_code::company_routes`）

| 代码 | 含义 |
|---|---|
| ` ` | Company Routes |
| `A` | Alternate Records |

**取值** — `EnrouteSubsCode`（`arinc424-core::data_types::subs_code::enroute`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Waypoints |
| `M` | Airway Markers |
| `P` | Holding Patterns |
| `R` | Airways And Routes |
| `T` | Preferred Routes |
| `U` | Airway Restrictions |
| `V` | Communications |

**取值** — `HeliportSubsCode`（`arinc424-core::data_types::subs_code::heliport`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Pads |
| `C` | Terminal Waypoints |
| `D` | Sids |
| `E` | Stars |
| `F` | Approach Procedures |
| `K` | Taa |
| `S` | Msa |
| `V` | Communication |

**取值** — `MoraSubsCode`（`arinc424-core::data_types::subs_code::mora`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `S` | Grid Mora |

**取值** — `NavaidSubsCode`（`arinc424-core::data_types::subs_code::navaid`）

| 代码 | 含义 |
|---|---|
| ` ` | Vhf Navaid |
| `B` | Ndb Navaid |
| `N` | Terminal Ndb |

<a id="57-route-type"></a>

## 5.7 Route Type

缩写 `RT TYPE`

**取值** — `AirportApproachAndHeliportApproachRouteTypes`（`arinc424-core::data_types::route_type::approach`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Approach Transition |
| `B` | Localizer Or Backcourse Approach |
| `D` | Vor Dme |
| `F` | Fms |
| `G` | Igs |
| `I` | Ils |
| `J` | Gls |
| `L` | Loc |
| `M` | Mls |
| `N` | Ndb |
| `P` | Gps |
| `Q` | Ndb Dme |
| `R` | Rnav |
| `S` | Vor Approach Using Vor Dme Or Vor Tac |
| `T` | Tacan |
| `U` | Sdf |
| `V` | Vor |
| `W` | Mls Type A |
| `X` | Lda |
| `Y` | Mls Type BC |
| `Z` | Missed Approach |

**取值** — `AirportSidAndHeliportSidRouteTypes`（`arinc424-core::data_types::route_type::sid`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `0` | Engine Out Sid |
| `1` | Sid Runway Transition |
| `2` | Sid Or Sid Common Route |
| `3` | Sid Enroute Transition |
| `4` | Rnav Sid Runway Transition |
| `5` | Rnav Sid Or Sid Common Route |
| `6` | Rnav Sid Enroute Transition |
| `F` | Fms Sid Runway Transition |
| `M` | Fms Sid Or Sid Common Route |
| `S` | Fms Sid Enroute Transition |
| `T` | Vector Sid Runway Transition |
| `V` | Vector Sid Enroute Transition |

**取值** — `AirportStarAndHeliportStarRouteTypes`（`arinc424-core::data_types::route_type::star`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `1` | Star Enroute Transition |
| `2` | Star Or Star Common Route |
| `3` | Star Runway Transition |
| `4` | Rnav Star Enroute Transition |
| `5` | Rnav Star Or Star Common Route |
| `6` | Rnav Star Runway Transition |
| `7` | Profile Descent Enroute Transition |
| `8` | Profile Descent Common Route |
| `9` | Profile Descent Runway Transition |
| `F` | Fms Star Enroute Transition |
| `M` | Fms Star Or Star Common Route |
| `S` | Fms Star Runway Transition |

**取值** — `EnrouteAirwayRouteTypes`（`arinc424-core::data_types::route_type::enroute_airway`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Airline Airway |
| `C` | Control |
| `D` | Direct Route |
| `H` | Helicopter Airways |
| `O` | Officially Designated Airways Or Except Rnav Or Helicopter Airways |
| `R` | Rnav Airways |
| `U` | Undesignated Ats Route |

**取值** — `PreferredRouteType`（`arinc424-core::data_types::route_type::preferred_route`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `C` | North American Routes For North Atlantic Traffic Common Portion |
| `D` | Preferential Routes |
| `J` | Pacific Oceanic Transition Routes |
| `M` | Tacan Routes Australia |
| `N` | North American Routes For North Atlantic Traffic Non Common Portion |
| `0` | Preferred Or Preferential Overflight Routes |
| `P` | Preferred Routes |
| `S` | Traffic Orientation System Routes |
| `T` | Tower Enroute Control Routes |

<a id="517-waypoint-description-code"></a>

## 5.17 Waypoint Description Code

缩写 `DESC CODE`

**第 40 列** — `WaypointDescCodeCol40`（`arinc424-core::data_types::waypoint_description_code::col_40`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Airport As Waypoint |
| `E` | Essential Waypoint |
| `F` | Off Airway Waypoint |
| `G` | Runway As Waypoint Or Helipad As Waypoint |
| `H` | Heliport As Waypoint |
| `N` | Ndb Navaid As Waypoint |
| `P` | Phantom Waypoint |
| `R` | Non Essential Waypoint |
| `T` | Transition Essential Waypoint |
| `V` | Vhf Navaid As Waypoint |

**第 41 列** — `WaypointDescCodeCol41`（`arinc424-core::data_types::waypoint_description_code::col_41`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `B` | Flyover Waypoint And End Of SID And STAR Route Type And Apch Transition Or Final Approach |
| `E` | End Of Enroute Airway Or Terminal Procedure Route Type |
| `U` | Uncharted Airway Intersection |
| `Y` | Fly Over Waypoint |

**第 42 列** — `WaypointDescCodeCol42`（`arinc424-core::data_types::waypoint_description_code::col_42`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Unnamed Stepdown Fix After Final Approach Fix |
| `B` | Unnamed Stepdown Fix Before Final Approach Fix |
| `C` | Atc Compulsory Waypoint |
| `G` | Oceanic Gateway Waypoint |
| `M` | First Leg Of Missed Approach Procedure |
| `P` | Path Point Fix |
| `S` | Named Stepdown Fix |

**第 43 列** — `WaypointDescCodeCol43`（`arinc424-core::data_types::waypoint_description_code::col_43`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Initial Approach Fix |
| `B` | Intermediate Approach Fix |
| `C` | Initial Approach Fix With Holding |
| `D` | Initial Approach Fix With Final Approach Course Fix |
| `E` | Final End Point Fix |
| `F` | Published Final Approach Fix Or Database Final Approach Fix |
| `H` | Holding Fix |
| `I` | Final Approach Course Fix |
| `M` | Published Missed Approach Point Fix |

<a id="518-boundary-code"></a>

## 5.18 Boundary Code

缩写 `BDY CODE`

**取值** — `BoundaryCodeItem`（`arinc424-core::data_types::boundary_code`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Africa |
| `C` | Canada And Alaska |
| `2` | Eastern Europe |
| `E` | Europe |
| `L` | Latin America |
| `M` | Middle East South Asia |
| `P` | Pacific |
| `S` | South America |
| `1` | South Pacific |
| `U` | USA |

<a id="519-level"></a>

## 5.19 Level

缩写 `LEVEL`

**取值** — `LevelItem`（`arinc424-core::data_types::level`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `B` | All Altitudes |
| `H` | High Level Airways |
| `L` | Low Level Airways |

<a id="520-turn-direction"></a>

## 5.20 Turn Direction

缩写 `TURN DIR`

**取值** — `TurnDirectionItem`（`arinc424-core::data_types::turn_direction`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `L` | Left |
| `R` | Right |
| `E` | Either |

<a id="521-path-and-termination"></a>

## 5.21 Path and Termination

缩写 `PATH TERM`

**取值** — `PathAndTerminatorItem`（`arinc424-core::data_types::path_and_terminator`）

| 代码 | 含义 |
|---|---|
| `IF` | IF |
| `TF` | TF |
| `CF` | CF |
| `DF` | DF |
| `FA` | FA |
| `FC` | FC |
| `FD` | FD |
| `FM` | FM |
| `CA` | CA |
| `CD` | CD |
| `CI` | CI |
| `CR` | CR |
| `RF` | RF |
| `AF` | AF |
| `VA` | VA |
| `VD` | VD |
| `VI` | VI |
| `VM` | VM |
| `VR` | VR |
| `FI` | FI |
| `HA` | HA |
| `HF` | HF |
| `HM` | HM |

<a id="529-altitude-description"></a>

## 5.29 Altitude Description

缩写 `ALT DESC`

**取值** — `AltitudeDescription`（`arinc424-core::data_types::altitude_description`）

| 代码 | 含义 |
|---|---|
| `+` | Plus |
| `-` | Minus |
| ` ` | Blank |
| `B` | B |
| `C` | C |
| `G` | G |
| `H` | H |
| `I` | I |
| `J` | J |
| `V` | V |
| `X` | X |
| `Y` | Y |

<a id="535-navaid-class"></a>

## 5.35 NAVAID Class

缩写 `CLASS`

**第 28 列** — `NdbNavaidType1`（`arinc424-core::data_types::navaid_class::ndb_class::col_28`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `H` | Ndb |
| `S` | Sabh |
| `M` | Marine Beacon |

**第 28 列** — `VhfNavaidType1`（`arinc424-core::data_types::navaid_class::vhf_class::col_28`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `V` | Vor |

**第 29 列** — `NdbNavaidType2`（`arinc424-core::data_types::navaid_class::ndb_class::col_29`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `I` | Inner Marker |
| `M` | Middle Marker |
| `O` | Outer Marker |
| `C` | Back Marker |

**第 29 列** — `VhfNavaidType2`（`arinc424-core::data_types::navaid_class::vhf_class::col_29`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `D` | Dme |
| `T` | Tacan |
| `M` | Mil Tacan |
| `I` | Ils Dme Or Ils Tacan |
| `N` | Mls Dme N |
| `P` | Mls Dme P |

**第 30 列** — `NdbRangePower`（`arinc424-core::data_types::navaid_class::ndb_class::col_30`）

| 代码 | 含义 |
|---|---|
| `H` | H |
| ` ` | Blank |
| `M` | M |
| `L` | L |

**第 30 列** — `VhfRangePower`（`arinc424-core::data_types::navaid_class::vhf_class::col_30`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `T` | Terminal |
| `L` | Low Altitude |
| `H` | High Altitude |
| `U` | Undefined |
| `C` | Ils Or Tacan |

**第 31 列** — `AddInfo`（`arinc424-core::data_types::navaid_class::col_31`）

| 代码 | 含义 |
|---|---|
| `D` | Biased Ils Dme Or Ils Tacan |
| `A` | Automatic Transcribed Weather Broadcast |
| `B` | Scheduled Weather Broadcast |
| `W` | No Voice On Frequency |
| ` ` | Voice On Frequency |

**第 32 列** — `Collocation`（`arinc424-core::data_types::navaid_class::col_32`）

| 代码 | 含义 |
|---|---|
| ` ` | Collocated Navaids |
| `N` | Non Collocated Navaids |
| `B` | Bfo Operation |
| `A` | Locator Or Marker Collocated |

<a id="542-waypoint-type"></a>

## 5.42 Waypoint Type

缩写 `TYPE`

**第 27 列** — `WaypointTypeCol27`（`arinc424-core::data_types::waypoint_type::col_27`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Arc Center Fix Waypoint |
| `C` | Combined Named Intersection And RNAV |
| `I` | Unnamed Charted Intersection |
| `M` | Middle Marker As Waypoint |
| `N` | Ndb Navaid As Waypoint |
| `O` | Outer Marker As Waypoint |
| `R` | Named Intersection |
| `U` | Uncharted Airway Intersection |
| `V` | Vfr Waypoint |
| `W` | Rnav Waypoint |

**第 28 列** — `EnrouteWaypointTypeCol28`（`arinc424-core::data_types::waypoint_type::enroute_waypoint::col_28`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Initial Approach Fix |
| `B` | Initial And Final Approach Fix |
| `C` | Final Approach Course Fix |
| `D` | Intermediate Approach Fix |
| `E` | Off Route Intersection In The Faa National Reference System |
| `F` | Off Route Intersection |
| `I` | Initial Approach Fix |
| `K` | Final Approach Course Fix At Initial Approach Fix |
| `L` | Final Approach Course Fix At Intermediate Approach Fix |
| `M` | Missed Approach Fix |
| `N` | Initial Approach Fix And Missed Approach Fix |
| `O` | Oceanic Entry Exit Waypoint |
| `P` | Pitch And Catch Point In The Faa High Altitude Redesign |
| `S` | Aacaa And Sua Waypoints In The Faa High Altitude Redesign |
| `U` | Fir Uir Or Controlled Airspace Intersection |
| `V` | Latitude Longitude Intersection Full Degree Of Latitude |
| `W` | Latitude Longitude Intersection Half Degree Of Latitude |

**第 28 列** — `TerminalWaypointTypeCol28`（`arinc424-core::data_types::waypoint_type::terminal_waypoint::col_28`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Final Approach Fix |
| `B` | Initial Approach Fix And Final Approach Fix |
| `C` | Final Approach Course Fix |
| `D` | Intermediate Approach Fix |
| `I` | Initial Approach Fix |
| `K` | Final Approach Course Fix At Initial Approach Fix |
| `L` | Final Approach Course Fix At Intermediate Approach Fix |
| `M` | Missed Approach Fix |
| `N` | Initial Approach Fix And Missed Approach Fix |
| `P` | Unnamed Stepdown Fix |
| `S` | Named Stepdown Fix |
| `U` | Fir Uir Or Controlled Airspace Intersection |

**第 29 列** — `WaypointTypeCol29`（`arinc424-core::data_types::waypoint_type::col_29`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `D` | Sid |
| `E` | Star |
| `F` | Approach |
| `Z` | Multiple |

<a id="549-localizer-azimuth-position-reference"></a>

## 5.49 Localizer/Azimuth Position Reference

缩写 `@, +, -`

**取值** — `LocalizerPositionReferenceItem`（`arinc424-core::data_types::localizer_position_reference`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `+` | Ahead Or Beyond |
| `-` | Offset Side |

<a id="580-ils-mls-gls-category"></a>

## 5.80 ILS/MLS/GLS Category

缩写 `CAT`

**取值** — `LocalizerMlsGlsCategoryClassItem`（`arinc424-core::data_types::localizer_mls_gls_category_class`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `0` | Ils Localizer Only |
| `1` | Category1 |
| `2` | Category2 |
| `3` | Category3 |
| `I` | Igs Facility |
| `L` | Lda With Glideslope |
| `A` | Lda No Glideslope |
| `S` | Sdf With Glideslope |
| `F` | Sdf No Glideslope |

<a id="581-atc-indicator"></a>

## 5.81 ATC Indicator

缩写 `ATC`

**取值** — `AtcIndicatorItem`（`arinc424-core::data_types::atc_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Atc Modify Or Assign |
| `S` | Atc Assign Or Missing |

<a id="582-waypoint-usage"></a>

## 5.82 Waypoint Usage

**取值** — `WaypointUsageCol31`（`arinc424-core::data_types::waypoint_usage`）

| 代码 | 含义 |
|---|---|
| `B` | High And Low Altitude |
| `H` | High Altitude |
| `L` | Low Altitude |
| ` ` | Terminal Use Only |

**取值** — `WaypointUsageRnav`（`arinc424-core::data_types::waypoint_usage`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `R` | Rnav |

<a id="591-continuation-record-application-type"></a>

## 5.91 Continuation Record Application Type

缩写 `APPL`

**取值** — `ContinuationApplicationType`（`arinc424-core::data_types::application_type`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Standard Arinc Continuation |
| `B` | Combined Agency Call Sign And Formatted Time |
| `C` | Call Sign Or Controlling Agency Continuation |
| `E` | Primary Record Extension |
| `L` | Vhf Navaid Limitation Continuation |
| `N` | Sector Narrative Continuation |
| `T` | Time Of Operations Formatted |
| `U` | Time Of Operations Narrative |
| `V` | Time Of Operations Date Range |
| `P` | Flight Planning Continuation |
| `Q` | Flight Planning Primary Data Continuation |
| `S` | Simulation Application Continuation |
| `W` | Airport Procedure Sbas Authorization |

<a id="593-facility-characteristics"></a>

## 5.93 Facility Characteristics

缩写 `FAC CHAR`

**取值** — `EmissionDesignator`（`arinc424-core::data_types::ndb_facility_characteristics`）

| 代码 | 含义 |
|---|---|
| `NON` | Non |
| `A1A` | A1 A |
| `A1B` | A1 B |
| `A2A` | A2 A |
| `A0 ` | Legacy A0 |
| `A1 ` | Legacy A1 |
| `A2 ` | Legacy A2 |

**取值** — `FacCharCol28`（`arinc424-core::data_types::ndb_facility_characteristics`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `S` | Synchronous |
| `A` | Asynchronous |

**取值** — `FacCharCol29`（`arinc424-core::data_types::ndb_facility_characteristics`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `Y` | Voice Ident |
| `N` | No Voice Ident |
| `U` | Undefined |

<a id="5114-duplicate-indicator"></a>

## 5.114 Duplicate Indicator

缩写 `DUP IND`

**取值** — `PositionOneAirspace`（`arinc424-core::data_types::duplicate_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `0` | Undefined |
| `1` | High Altitude |
| `2` | Low Altitude |
| `3` | Sid |
| `4` | Star |
| `5` | Approach |
| `6` | Missed Approach |
| `7` | Undefined With Other Defined |
| `8` | All Altitude |

<a id="5115-directional-restriction"></a>

## 5.115 Directional Restriction

**取值** — `DirectionRestrictionItem`（`arinc424-core::data_types::direction_restriction`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `F` | Forward |
| `B` | Backward |

<a id="5149-navaid-usable-range"></a>

## 5.149 Navaid Usable Range

**取值** — `FigureOfMerit`（`arinc424-core::data_types::figure_of_merit`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `0` | Terminal Use |
| `1` | Low Altitude Use |
| `2` | High Altitude Use |
| `3` | Extended High Altitude Use |
| `7` | Navaid Not Included In A Civil International Notam System |
| `9` | Navaid Out Of Service |

<a id="5152-start-end-indicator"></a>

## 5.152 Start/End Indicator

缩写 `S/E IND`

**取值** — `StartEndIndicatorItem`（`arinc424-core::data_types::start_end_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `C` | Change Date |
| `E` | End Date |
| `S` | Start Date |

<a id="5165-magnetic-true-indicator"></a>

## 5.165 Magnetic/True Indicator

缩写 `M/T IND`

**取值** — `MagneticTrueIndicator`（`arinc424-core::data_types::magnetic_true_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `M` | Magnetic |
| `T` | True |

<a id="5177-public-military-indicator"></a>

## 5.177 Public/Military Indicator

缩写 `PUB/MIL`

**取值** — `PublicMilitaryIndicatorItem`（`arinc424-core::data_types::public_military_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `C` | Civil |
| `M` | Military |
| `P` | Private |

<a id="5178-time-zone"></a>

## 5.178 Time Zone

**取值** — `TimeZoneDesignator`（`arinc424-core::data_types::time_zone`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `Z` | Utc Plus0 |
| `A` | Utc Plus1 |
| `B` | Utc Plus2 |
| `C` | Utc Plus3 |
| `D` | Utc Plus4 |
| `E` | Utc Plus5 |
| `F` | Utc Plus6 |
| `G` | Utc Plus7 |
| `H` | Utc Plus8 |
| `I` | Utc Plus9 |
| `K` | Utc Plus10 |
| `L` | Utc Plus11 |
| `M` | Utc Plus12 |
| `N` | Utc Minus1 |
| `O` | Utc Minus2 |
| `P` | Utc Minus3 |
| `Q` | Utc Minus4 |
| `R` | Utc Minus5 |
| `S` | Utc Minus6 |
| `T` | Utc Minus7 |
| `U` | Utc Minus8 |
| `V` | Utc Minus9 |
| `W` | Utc Minus10 |
| `X` | Utc Minus11 |
| `Y` | Utc Minus12 |

<a id="5187-distance-description"></a>

## 5.187 Distance Description

缩写 `DIST DESC`

**取值** — `DistanceDescription`（`arinc424-core::data_types::distance_description`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `-` | Out To Specified Distance |
| `+` | Beyond Specified Distance |
| `B` | Between Specified Distances |

<a id="5196-name-format-indicator"></a>

## 5.196 Name Format Indicator

缩写 `NAME IND`

**取值** — `NameFormatIndicatorCol96`（`arinc424-core::data_types::name_format_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Abeam Fix |
| `B` | Bearing And Distance Fix |
| `D` | Airport Name As Fix |
| `F` | Fir Fix |
| `H` | Phonetic Letter Name Fix |
| `I` | Airport Ident As Fix |
| `L` | Latitude Longitude Fix |
| `M` | Multiple Word Name Fix |
| `N` | Navaid Ident As Fix |
| `P` | Published Five Letter Name Fix |
| `Q` | Published Name Fix Less Than Five Letters |
| `R` | Published Name Fix More Than Five Letters |
| `T` | Airport Runway Related Fix |
| `U` | Uir Fix |

**取值** — `NameFormatIndicatorCol97`（`arinc424-core::data_types::name_format_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `O` | Localizer Marker With Published Five Letter Identifier |
| `M` | Localizer Marker Without Published Five Letter Identifier |

<a id="5205-navaid-limitation-code"></a>

## 5.205 Navaid Limitation Code

缩写 `NLC`

**取值** — `NavaidLimitationCode`（`arinc424-core::data_types::navaid_limitation_code`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `C` | Coverage |
| `F` | Fluctuations |
| `G` | Roughness |
| `N` | Unreliable |
| `R` | Restricted |
| `T` | Unusable |
| `U` | Out Of Tolerance |

<a id="5206-component-affected-indicator"></a>

## 5.206 Component Affected Indicator

缩写 `COMP AFFTD IND`

**取值** — `ComponentAffectedIndicator`（`arinc424-core::data_types::component_affected_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | Azimuth Component Only Affected |
| `B` | Both Azimuth And Distance Components Affected |
| `D` | Distance Component Only Affected |
| `M` | Azimuth And Distance Components Affected |
| `T` | Distance Component Affected |
| `V` | Vor Azimuth Component Affected |
| `Z` | Vor And Tacan Azimuth And Distance Components Affected |

<a id="5207-sector-from-sector-to"></a>

## 5.207 Sector From/Sector To

缩写 `SECTR`

**取值** — `SectorCharacter`（`arinc424-core::data_types::sector_from_sector_to`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `A` | From000 To015 |
| `B` | From015 To030 |
| `C` | From030 To045 |
| `D` | From045 To060 |
| `E` | From060 To075 |
| `F` | From075 To090 |
| `G` | From090 To105 |
| `H` | From105 To120 |
| `I` | From120 To135 |
| `J` | From135 To150 |
| `K` | From150 To165 |
| `L` | From165 To180 |
| `M` | From180 To195 |
| `N` | From195 To210 |
| `O` | From210 To225 |
| `P` | From225 To240 |
| `Q` | From240 To255 |
| `R` | From255 To270 |
| `S` | From270 To285 |
| `T` | From285 To300 |
| `U` | From300 To315 |
| `V` | From315 To330 |
| `W` | From330 To345 |
| `X` | From345 To000 |

<a id="5210-sequence-end-indicator"></a>

## 5.210 Sequence End Indicator

缩写 `SEQ END`

**取值** — `SequenceEndIndicator`（`arinc424-core::data_types::sequence_end_indicator`）

| 代码 | 含义 |
|---|---|
| `E` | End |
| ` ` | Blank |

<a id="5222-gnss-fms-indicator"></a>

## 5.222 GNSS/FMS Indicator

缩写 `GNSS/FMS IND`

**取值** — `GnssFmsIndicatorItem`（`arinc424-core::data_types::gnss_fms_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `0` | Not Authorized |
| `1` | Gnss Overlay Primary Navaids Monitored |
| `2` | Gnss Overlay Primary Navaids Installed Not Monitored |
| `3` | Gnss Overlay Procedure Title Gps Or Gnss |
| `4` | Fms Overlay |
| `5` | Fms Or Gnss Overlay |
| `A` | Rnav Sbas Authorized |
| `B` | Rnav Sbas Not Authorized |
| `C` | Rnav Sbas Use Not Specified |
| `P` | Stand Alone Gps Gnss |
| `U` | Overlay Authorization Not Specified |

<a id="5249-surface-code"></a>

## 5.249 Surface Code

缩写 `SC`

**取值** — `LongestRunwaySurfaceCodeItem`（`arinc424-core::data_types::longest_runway_surface_code`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `H` | Hard Surface |
| `S` | Soft Surface |
| `W` | Water Runway |
| `U` | Undefined |

<a id="5261-speed-limit-description"></a>

## 5.261 Speed Limit Description

缩写 `SLD`

**取值** — `SpeedLimitDescriptionItem`（`arinc424-core::data_types::speed_limit_description`）

| 代码 | 含义 |
|---|---|
| ` ` | At |
| `+` | Minimum |
| `-` | Maximum |

<a id="5270-tch-value-indicator"></a>

## 5.270 TCH Value Indicator

缩写 `TCHVI`

**取值** — `TchValueIndicatorItem`（`arinc424-core::data_types::tch_value_indicator`）

| 代码 | 含义 |
|---|---|
| ` ` | Blank |
| `I` | Ils Or Mls Glide Slope |
| `R` | Rnav Procedure |
| `V` | Vgsi |
| `D` | Default Fifty Feet |

