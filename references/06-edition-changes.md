# 版本变更总览

ARINC 424 每次改版都会增删记录类型、调整列位、扩充字段。这一页按版本顺序汇总变更，方便回答「这个字段是哪一版才有的」「这条记录的列位在 20 到 21 之间动过吗」。

单条记录的细节用 `arinc424.py diff 4.1.2.1 --from 18 --to 23` 查。

## 424-18 新增记录类型（36）

- 4.1.2 VHF NAVAID Record (D)
- 4.1.3 NDB NAVAID Record (DB or PN)
- 4.1.4 Waypoint Record (EA) or (PC)
- 4.1.5 Holding Pattern Records (EP)
- 4.1.6 Enroute Airways Records (ER)
- 4.1.7 Airport Records (PA)
- 4.1.8 Airport Gate Records (PB)
- 4.1.9 Airport SID/STAR/Approach (PD, PE, and PF)
- 4.1.10 Runway Records (PG)
- 4.1.11 Airport and Heliport Localizer and Glideslope Records (PI)
- 4.1.12 Company Route Records (R)
- 4.1.13 Airport and Heliport Localizer Marker Records (PM)
- 4.1.14 Airport Communications Records (PV)
- 4.1.15 Airways Marker Records (EM)
- 4.1.16 Cruising Tables Records (TC)
- 4.1.17 FIR/UIR Records (UF)
- 4.1.18 Restrictive Airspace Records (UR)
- 4.1.19 Grid MORA Records (AS)
- 4.1.20 Airport MSA (Minimum Sector Altitude) Records (PS)
- 4.1.21 Enroute Airways Restriction Records (EU)
- 4.1.22 Airport and Heliport MLS (Azimuth, Elevation and Back Azimuth) Records (PL)
- 4.1.23 Enroute Communications Records (EV)
- 4.1.24 Preferred Routes Records (ET)
- 4.1.25 Controlled Airspace Records (UC)
- 4.1.26 Geographical Reference Table Records (TG)
- 4.1.27 Flight Planning Arrival/Departure Data Records (PR)
- 4.1.28 Airport SBAS Path Point Records (PP)
- 4.1.29 GLS Record (PT)
- 4.1.31 Airport TAA (PK)
- 4.1.30 Alternate Record (RA)
- 4.2.1 Heliport Records (HA)
- 4.2.2 Heliport Terminal Waypoint Records (HC)
- 4.2.3 Heliport SID/STAR/Approach (HD/HE/HF)
- 4.2.4 Heliport MSA (HS)
- 4.2.5 Heliport Communications Records (HV)
- 4.2.6 Heliport (TAA) (HK)

## 424-19 新增记录类型（4）

- 4.1.32 TACAN-Only NAVAID Record (DT)
- 4.1.33 Special Activity Area (ES)
- 4.1.34 Communication Type Translation (TV)
- 4.2.7 Helicopter Operations Company Route Records (RH)

## 424-20 新增记录类型（2）

- 4.1.35 GBAS Path Point Record (PQ)
- 4.2.8 Helicopter Operations SBAS Path Point Records (HP)

## 424-21 新增记录类型（2）

- 4.1.36 Airport Helipad Record (PH)
- 4.2.9 Heliport Helipad Record (HH)

## 424-23 新增记录类型（1）

- 4.1.37 ATN Data (ATN NSAP) Record (TL)

## 各版记录数量

| 版本 | 记录组 | 布局 | 字段定义 | 页数 |
|---|---|---|---|---|
| 424-18 | 36 | 99 | 247 | 402 |
| 424-19 | 40 | 102 | 271 | 450 |
| 424-20 | 42 | 105 | 301 | 635 |
| 424-21 | 44 | 110 | 312 | 487 |
| 424-22 | 44 | 111 | 320 | 487 |
| 424-23 | 45 | 125 | 343 | 535 |

## 各版新增的字段定义

**18 → 19**（43 个）

- 5.15 Inbound Course Theta
- 5.16 Continuation Record Number
- 5.23 Recommended NAVAID
- 5.32 Cycle Date
- 5.50 Glideslope Position (GS FR RW THRES) Elevation Position
- 5.87 TERMINAL/ALTERNATE Airport
- 5.93 Facility Characteristics
- 5.106 Service Indicator
- 5.121 Lower/Upper Limit
- 5.125 FIR/UIR Name
- 5.141 Starting Latitude
- 5.169 Elevation Angle Span
- 5.170 Decision Height
- 5.182 Guard/Transmit
- 5.187 Distance Description
- 5.188 Communications Distance
- 5.213 Controlled Airspace Type
- 5.222 GNSS/FMS Indicator
- 5.231 Along Track Distance
- 5.256 Reference Path Data Selector
- 5.270 TCH Value Indicator
- 5.277 DME Operational Service Volume
- 5.278 Activity Type
- 5.279 Activity Identifier
- 5.280 Special Activity Area Size
- 5.281 Special Activity Area Volume
- 5.282 Special Activity Area Operating Times
- 5.283 Communications Class
- 5.284 Assigned Sector Name
- 5.285 Time Narrative
- 5.286 Multi-Sector Indicator
- 5.287 Type Recognized By
- 5.288 Translation
- 5.289 Used On
- 5.290 Procedure Design Mag Var
- 5.291 Procedure Design Mag Var Indicator
- 5.292 Category Distance
- 5.293 Vertical Scale Factor
- 5.294 RVSM Minimum Level
- 5.295 RVSM Maximum Level
- 5.296 RNP Level of Service
- 5.297 Route Inappropriate Navaid Indicator
- 5.298 Holding Pattern/Race Track Course Reversal Leg Inbound/Outbound Indicator

**19 → 20**（30 个）

- 5.5 Subsection Code
- 5.6 Airport/Heliport Identifier
- 5.14 ICAO Code
- 5.27 Route Distance From, Holding Distance/Time
- 5.31 File Record Number
- 5.37 Longitude
- 5.45 Localizer Frequency
- 5.47 Localizer Bearing
- 5.51 Localizer Width
- 5.52 Glideslope Angle (GS ANGLE) Minimum Elevation Angle
- 5.53 Transition Altitude/Level
- 5.74 Component Elevation
- 5.75 From/To - Airport/Heliport/Fix
- 5.85 ENRT TRANS
- 5.86 Cruise Altitude
- 5.99 Marker Type
- 5.108 IFR Capability
- 5.122 FIR/UIR ATC Reporting Units Speed
- 5.155 BARO-VNAV Not Authorized
- 5.162 Step Climb Indicator
- 5.165 Magnetic/True Indicator
- 5.189 Position Narrative
- 5.198 Datum Code
- 5.200 Remote Facility
- 5.212 Runway Gradient
- 5.215 Controlled Airspace Classification
- 5.220 Preferred Route Use Indicator
- 5.299 Procedure Referenced Fix Identifier
- 5.300 Final Approach Course as Runway
- 5.301 Procedure Design Aircraft Category or Type

**20 → 21**（11 个）

- 5.302 Surface Type
- 5.303 Helipad Shape
- 5.304 Sector Bearing Reference Waypoint
- 5.305 Heliport Type
- 5.306 Preferred Multiple Approach Indicator
- 5.307 Special Indicator
- 5.308 Remote Altimeter Flag
- 5.309 Maximum Allowable Helicopter Weight
- 5.310 Helicopter Performance Requirement
- 5.311 FIR/FRA Transition
- 5.312 Starter Extension

**21 → 22**（8 个）

- 5.313 TORA
- 5.314 TODA
- 5.315 ASDA
- 5.316 LDA
- 5.317 Runway Usage Indicator
- 5.318 Runway Accuracy Compliance Flag
- 5.319 Landing Threshold Elevation Accuracy Compliance Flag
- 5.320 SBAS Final Approach Course

**22 → 23**（23 个）

- 5.321 Helipad Maximum Rotor Diameter
- 5.322 Helipad Type
- 5.323 Helipad Orientation
- 5.324 Helipad Identifier Orientation
- 5.325 Preferred Approach Bearing
- 5.326 Ground Facility Indentifier
- 5.327 Authority Format Identifier
- 5.328 Initial Domain Identifier
- 5.329 Version
- 5.330 Administration
- 5.331 Routing Domain Format
- 5.332 Administrative Region Selector
- 5.333 Location
- 5.334 System Identifier
- 5.335 Network Service Access Point Selector
- 5.336 Context Management Transport Selector
- 5.337 Use Indicator
- 5.338 VOR Range/Power
- 5.339 DME Expanded Service Volume
- 5.340 Unmanned Aerial Vhicle (UAV) Only
- 5.341 Military Indicator
- 5.342 Source of LAL/VAL
- 5.343 Holding Pattern Magnetic Variation

