# 字段定义索引

共 343 个字段定义（第 5 章）。编号与 ARINC 424 正文一致，记录布局的「引用」列指向这些编号。

「码表」列有 ✓ 的字段，其取值含义已结构化，可用 `arinc424.py codes 5.xx` 查询，也可直接看 [码表总表](05-code-tables.md)。

| 编号 | 字段名 | 缩写 | 定义于 | 码表 |
|---|---|---|---|---|
| [5.1](04-fields/5.1.md) | General |  | 全部 |  |
| [5.2](04-fields/5.2.md) | Record Type | S/T | 全部 | ✓ |
| [5.3](04-fields/5.3.md) | Customer/Area Code | CUST/AREA | 全部 | ✓ |
| [5.4](04-fields/5.4.md) | Section Code | SEC CODE | 全部 | ✓ |
| [5.5](04-fields/5.5.md) | Subsection Code | SUB CODE | 20 21 22 23 | ✓ |
| [5.6](04-fields/5.6.md) | Airport/Heliport Identifier | ARPT/HELI IDENT | 18 20 21 22 23 |  |
| [5.7](04-fields/5.7.md) | Route Type | RT TYPE | 全部 | ✓ |
| [5.8](04-fields/5.8.md) | Route Identifier | ROUTE IDENT | 全部 |  |
| [5.9](04-fields/5.9.md) | SID/STAR Route Identifier | SID/STAR IDENT | 全部 |  |
| [5.10](04-fields/5.10.md) | Approach Route Identifier | APPROACH IDENT | 全部 |  |
| [5.11](04-fields/5.11.md) | Transition Identifier | TRANS IDENT | 全部 |  |
| [5.12](04-fields/5.12.md) | Sequence Number | SEQ NR | 全部 |  |
| [5.13](04-fields/5.13.md) | Fix Identifier | FIX IDENT | 全部 |  |
| [5.14](04-fields/5.14.md) | ICAO Code | ICAO CODE | 20 21 22 23 |  |
| [5.15](04-fields/5.15.md) | Inbound Course Theta |  | 19 20 21 22 23 |  |
| [5.16](04-fields/5.16.md) | Continuation Record Number | CONT NR | 19 20 21 22 23 |  |
| [5.17](04-fields/5.17.md) | Waypoint Description Code | DESC CODE | 全部 | ✓ |
| [5.18](04-fields/5.18.md) | Boundary Code | BDY CODE | 全部 | ✓ |
| [5.19](04-fields/5.19.md) | Level | LEVEL | 全部 | ✓ |
| [5.20](04-fields/5.20.md) | Turn Direction | TURN DIR | 全部 | ✓ |
| [5.21](04-fields/5.21.md) | Path and Termination | PATH TERM | 全部 | ✓ |
| [5.22](04-fields/5.22.md) | Turn Direction Valid | TDV | 全部 |  |
| [5.23](04-fields/5.23.md) | Recommended NAVAID | RECD NAV | 19 20 21 22 23 |  |
| [5.24](04-fields/5.24.md) | Theta | THETA | 全部 |  |
| [5.25](04-fields/5.25.md) | Rho | RHO | 全部 |  |
| [5.26](04-fields/5.26.md) | Outbound Course | OB CRS | 全部 |  |
| [5.27](04-fields/5.27.md) | Route Distance From, Holding Distance/Time | RTE DIST FROM, HOLD DIST/TIME | 20 21 22 23 |  |
| [5.28](04-fields/5.28.md) | Inbound Course | IB CRS | 全部 |  |
| [5.29](04-fields/5.29.md) | Altitude Description | ALT DESC | 全部 | ✓ |
| [5.30](04-fields/5.30.md) | Altitude/Minimum Altitude |  | 全部 |  |
| [5.31](04-fields/5.31.md) | File Record Number | FRN | 18 20 21 22 23 |  |
| [5.32](04-fields/5.32.md) | Cycle Date | CYCLE | 19 20 21 22 23 |  |
| [5.33](04-fields/5.33.md) | VOR/NDB Identifier | VOR IDENT/NDB IDENT | 全部 |  |
| [5.34](04-fields/5.34.md) | VOR/NDB Frequency | VOR/NDB FREQ | 全部 |  |
| [5.35](04-fields/5.35.md) | NAVAID Class | CLASS | 全部 | ✓ |
| [5.36](04-fields/5.36.md) | Latitude | LATITUDE | 全部 |  |
| [5.37](04-fields/5.37.md) | Longitude | LONGITUDE | 20 21 22 23 |  |
| [5.38](04-fields/5.38.md) | DME Identifier | DME IDENT | 全部 |  |
| [5.39](04-fields/5.39.md) | Magnetic Variation | MAG VAR, D MAG VAR | 全部 |  |
| [5.40](04-fields/5.40.md) | DME Elevation | DME ELEV | 全部 |  |
| [5.41](04-fields/5.41.md) | Region Code | REGN CODE | 全部 |  |
| [5.42](04-fields/5.42.md) | Waypoint Type | TYPE | 全部 | ✓ |
| [5.43](04-fields/5.43.md) | Waypoint Name/Description | NAME/DESC | 全部 |  |
| [5.44](04-fields/5.44.md) | Localizer/MLS/GLS Identifier | LOC, MLS, GLS IDENT | 全部 |  |
| [5.45](04-fields/5.45.md) | Localizer Frequency | FREQ | 18 20 21 22 23 |  |
| [5.46](04-fields/5.46.md) | Runway Identifier | RUNWAY ID | 全部 |  |
| [5.47](04-fields/5.47.md) | Localizer Bearing | LOC BRG | 18 20 21 22 23 |  |
| [5.48](04-fields/5.48.md) | Localizer Position (LOC FR RW END) Azimuth/Back Azimuth Position (AZ/BAZ FR |  | 全部 |  |
| [5.49](04-fields/5.49.md) | Localizer/Azimuth Position Reference | @, +, - | 全部 | ✓ |
| [5.50](04-fields/5.50.md) | Glideslope Position (GS FR RW THRES) Elevation Position | EL FR RW THRES | 19 20 21 22 23 |  |
| [5.51](04-fields/5.51.md) | Localizer Width | LOC WIDTH | 20 21 22 23 |  |
| [5.52](04-fields/5.52.md) | Glideslope Angle (GS ANGLE) Minimum Elevation Angle | MIN ELEV ANGLE | 18 20 21 22 23 |  |
| [5.53](04-fields/5.53.md) | Transition Altitude/Level | TRANS ALTITUDE/LEVEL | 18 20 21 22 23 |  |
| [5.54](04-fields/5.54.md) | Longest Runway | LONGEST RWY | 全部 |  |
| [5.55](04-fields/5.55.md) | Airport/Heliport Elevation | ELEV | 全部 |  |
| [5.56](04-fields/5.56.md) | Gate Identifier | GATE IDENT | 全部 |  |
| [5.57](04-fields/5.57.md) | Runway Length | RUNWAY LENGTH | 全部 |  |
| [5.58](04-fields/5.58.md) | Runway Bearing | RWY BRG | 全部 |  |
| [5.59](04-fields/5.59.md) | Runway Description | RUNWAY DESCRIPTION | 全部 |  |
| [5.60](04-fields/5.60.md) | Name | NAME | 全部 |  |
| [5.61](04-fields/5.61.md) | Notes (Continuation Records) | NOTES | 全部 |  |
| [5.62](04-fields/5.62.md) | Inbound Holding Course | IB HOLD CRS | 全部 |  |
| [5.63](04-fields/5.63.md) | Turn | TURN | 全部 |  |
| [5.64](04-fields/5.64.md) | Leg Length | LEG LENGTH | 全部 |  |
| [5.65](04-fields/5.65.md) | Leg Time | LEG TIME | 全部 |  |
| [5.66](04-fields/5.66.md) | Station Declination | STN DEC | 全部 |  |
| [5.67](04-fields/5.67.md) | Threshold Crossing Height | TCH | 全部 |  |
| [5.68](04-fields/5.68.md) | Landing Threshold Elevation | LANDING THRES ELEV | 全部 |  |
| [5.69](04-fields/5.69.md) | Threshold Displacement Distance | DSPLCD THR | 全部 |  |
| [5.70](04-fields/5.70.md) | Vertical Angle | VERT ANGLE | 全部 |  |
| [5.71](04-fields/5.71.md) | Name Field |  | 全部 |  |
| [5.72](04-fields/5.72.md) | Speed Limit | SPEED LIMIT | 全部 |  |
| [5.73](04-fields/5.73.md) | Speed Limit Altitude |  | 全部 |  |
| [5.74](04-fields/5.74.md) | Component Elevation | GS ELEV, EL ELEV, AZ ELEV, BAZ ELEV | 18 20 21 22 23 |  |
| [5.75](04-fields/5.75.md) | From/To - Airport/Heliport/Fix |  | 18 20 21 22 23 |  |
| [5.76](04-fields/5.76.md) | Company Route Ident |  | 全部 |  |
| [5.77](04-fields/5.77.md) | VIA Code |  | 全部 |  |
| [5.78](04-fields/5.78.md) | SID/STAR/APP/AWY (S/S/A/AWY) SID/STAR/AWY | S/S/AWY | 全部 |  |
| [5.79](04-fields/5.79.md) | Stopway |  | 全部 |  |
| [5.80](04-fields/5.80.md) | ILS/MLS/GLS Category | CAT | 全部 | ✓ |
| [5.81](04-fields/5.81.md) | ATC Indicator | ATC | 全部 | ✓ |
| [5.82](04-fields/5.82.md) | Waypoint Usage |  | 全部 | ✓ |
| [5.83](04-fields/5.83.md) | To FIX |  | 全部 |  |
| [5.84](04-fields/5.84.md) | RUNWAY TRANS |  | 全部 |  |
| [5.85](04-fields/5.85.md) | ENRT TRANS |  | 18 20 21 22 23 |  |
| [5.86](04-fields/5.86.md) | Cruise Altitude |  | 18 20 21 22 23 |  |
| [5.87](04-fields/5.87.md) | TERMINAL/ALTERNATE Airport | TERM/ALT ARPT | 19 20 21 22 23 |  |
| [5.88](04-fields/5.88.md) | Alternate Distance | ALT DIST | 全部 |  |
| [5.89](04-fields/5.89.md) | Cost Index |  | 全部 |  |
| [5.90](04-fields/5.90.md) | ILS/DME Bias |  | 全部 |  |
| [5.91](04-fields/5.91.md) | Continuation Record Application Type | APPL | 全部 | ✓ |
| [5.92](04-fields/5.92.md) | Facility Elevation | FAC ELEV | 全部 |  |
| [5.93](04-fields/5.93.md) | Facility Characteristics | FAC CHAR | 19 20 21 22 23 | ✓ |
| [5.94](04-fields/5.94.md) | True Bearing | TRUE BRG | 全部 |  |
| [5.95](04-fields/5.95.md) | Government Source | SOURCE | 全部 |  |
| [5.96](04-fields/5.96.md) | Glideslope Beam Width | GS BEAM WIDTH | 全部 |  |
| [5.97](04-fields/5.97.md) | Touchdown Zone Elevation | TDZE | 全部 |  |
| [5.98](04-fields/5.98.md) | Elevation Type |  | 全部 |  |
| [5.99](04-fields/5.99.md) | Marker Type | MKR TYPE | 20 21 22 23 |  |
| [5.100](04-fields/5.100.md) | Minor Axis Bearing | MINOR AXIS TRUE BRG | 全部 |  |
| [5.101](04-fields/5.101.md) | Communications Type | COMM TYPE | 全部 |  |
| [5.102](04-fields/5.102.md) | Radar | RADAR | 全部 |  |
| [5.103](04-fields/5.103.md) | Communications Frequency | COMM FREQ | 全部 |  |
| [5.104](04-fields/5.104.md) | Frequency Units | FREQ UNIT | 全部 |  |
| [5.105](04-fields/5.105.md) | Call Sign | CALL SIGN | 全部 |  |
| [5.106](04-fields/5.106.md) | Service Indicator | SERV IND | 19 20 21 22 23 |  |
| [5.107](04-fields/5.107.md) | ATA/IATA Designator | ATA/IATA | 全部 |  |
| [5.108](04-fields/5.108.md) | IFR Capability | IFR | 18 20 21 22 23 |  |
| [5.109](04-fields/5.109.md) | Runway Width | WIDTH | 全部 |  |
| [5.110](04-fields/5.110.md) | Marker Ident | MARKER IDENT | 全部 |  |
| [5.111](04-fields/5.111.md) | Marker Code | MARKER CODE | 全部 |  |
| [5.112](04-fields/5.112.md) | Marker Shape | SHAPE | 全部 |  |
| [5.113](04-fields/5.113.md) | High/Low | HIGH/LOW | 全部 |  |
| [5.114](04-fields/5.114.md) | Duplicate Indicator | DUP IND | 全部 | ✓ |
| [5.115](04-fields/5.115.md) | Directional Restriction |  | 全部 | ✓ |
| [5.116](04-fields/5.116.md) | FIR/UIR Identifier | FIR/UIR IDENT | 全部 |  |
| [5.117](04-fields/5.117.md) | FIR/UIR Indicator | IND | 全部 |  |
| [5.118](04-fields/5.118.md) | Boundary Via | BDRY VIA | 全部 |  |
| [5.119](04-fields/5.119.md) | Arc Distance | ARC DIST | 全部 |  |
| [5.120](04-fields/5.120.md) | Arc Bearing | ARC BRG | 全部 |  |
| [5.121](04-fields/5.121.md) | Lower/Upper Limit |  | 19 20 21 22 23 |  |
| [5.122](04-fields/5.122.md) | FIR/UIR ATC Reporting Units Speed | RUS | 18 20 21 22 23 |  |
| [5.123](04-fields/5.123.md) | FIR/UIR ATC Reporting Units Altitude | RUA | 全部 |  |
| [5.124](04-fields/5.124.md) | FIR/UIR Entry Report | ENTRY | 全部 |  |
| [5.125](04-fields/5.125.md) | FIR/UIR Name |  | 19 20 21 22 23 |  |
| [5.126](04-fields/5.126.md) | Restrictive Airspace Name |  | 全部 |  |
| [5.127](04-fields/5.127.md) | Maximum Altitude | MAX ALT | 全部 |  |
| [5.128](04-fields/5.128.md) | Restrictive Airspace Type | REST TYPE | 全部 |  |
| [5.129](04-fields/5.129.md) | Restrictive Airspace Designation |  | 全部 |  |
| [5.130](04-fields/5.130.md) | Multiple Code | MULTI CD | 全部 |  |
| [5.131](04-fields/5.131.md) | Time Code | TIME CD | 全部 |  |
| [5.132](04-fields/5.132.md) | NOTAM |  | 全部 |  |
| [5.133](04-fields/5.133.md) | Unit Indicator | UNIT IND | 全部 |  |
| [5.134](04-fields/5.134.md) | Cruise Table Identifier | CRSE TBL IDENT | 全部 |  |
| [5.135](04-fields/5.135.md) | Course FROM/TO |  | 全部 |  |
| [5.136](04-fields/5.136.md) | Cruise Level From/To |  | 全部 |  |
| [5.137](04-fields/5.137.md) | Vertical Separation |  | 全部 |  |
| [5.138](04-fields/5.138.md) | Time Indicator | TIME IND | 全部 |  |
| [5.139](04-fields/5.139.md) | Procedure Name |  | 全部 |  |
| [5.140](04-fields/5.140.md) | Controlling Agency |  | 全部 |  |
| [5.141](04-fields/5.141.md) | Starting Latitude |  | 19 20 21 22 23 |  |
| [5.142](04-fields/5.142.md) | Starting Longitude |  | 全部 |  |
| [5.143](04-fields/5.143.md) | Grid MORA |  | 全部 |  |
| [5.144](04-fields/5.144.md) | Center Fix | CENTER FIX | 全部 |  |
| [5.145](04-fields/5.145.md) | Radius Limit |  | 全部 |  |
| [5.146](04-fields/5.146.md) | Sector Bearing | SEC BRG | 全部 |  |
| [5.147](04-fields/5.147.md) | Sector Altitude | SEC ALT | 全部 |  |
| [5.148](04-fields/5.148.md) | Enroute Alternate Airport/Heliport | EAA | 全部 |  |
| [5.149](04-fields/5.149.md) | Navaid Usable Range |  | 全部 | ✓ |
| [5.150](04-fields/5.150.md) | Frequency Protection Distance | FREQ PRD | 全部 |  |
| [5.151](04-fields/5.151.md) | FIR/UIR Address | ADDRESS | 全部 |  |
| [5.152](04-fields/5.152.md) | Start/End Indicator | S/E IND | 全部 | ✓ |
| [5.153](04-fields/5.153.md) | Start/End Date |  | 全部 |  |
| [5.154](04-fields/5.154.md) | Restriction Identifier | REST IDENT | 全部 |  |
| [5.155](04-fields/5.155.md) | BARO-VNAV Not Authorized |  | 18 20 21 22 23 |  |
| [5.156](04-fields/5.156.md) | Intentionally Left Blank |  | 全部 |  |
| [5.157](04-fields/5.157.md) | Airway Restriction Start/End Date | START/END DATE | 全部 |  |
| [5.158](04-fields/5.158.md) | VFR Checkpoint Flag |  | 全部 |  |
| [5.159](04-fields/5.159.md) | ATC Assigned Only |  | 全部 |  |
| [5.160](04-fields/5.160.md) | Units of Altitude | UNIT IND | 全部 |  |
| [5.161](04-fields/5.161.md) | Restriction Altitude | RSTR ALT | 全部 |  |
| [5.162](04-fields/5.162.md) | Step Climb Indicator | STEP | 18 20 21 22 23 |  |
| [5.163](04-fields/5.163.md) | Restriction Notes |  | 全部 |  |
| [5.164](04-fields/5.164.md) | EU Indicator | EU IND | 全部 |  |
| [5.165](04-fields/5.165.md) | Magnetic/True Indicator | M/T IND | 20 21 22 23 | ✓ |
| [5.166](04-fields/5.166.md) | Channel |  | 全部 |  |
| [5.167](04-fields/5.167.md) | MLS Azimuth Bearing (MLS AZ BRG) MLS Back Azimuth Bearing | MLS BAZ BRG | 全部 |  |
| [5.168](04-fields/5.168.md) | Azimuth Proportional Angle Right/Left (AZ PRO RIGHT/LEFT) Back Azimuth |  | 全部 |  |
| [5.169](04-fields/5.169.md) | Elevation Angle Span | EL ANGLE SPAN | 19 20 21 22 23 |  |
| [5.170](04-fields/5.170.md) | Decision Height | DH | 19 20 21 22 23 |  |
| [5.171](04-fields/5.171.md) | Minimum Descent Height | MDH | 全部 |  |
| [5.172](04-fields/5.172.md) | Azimuth Coverage Sector Right/Left | AZ COV RIGHT/LEFT | 全部 |  |
| [5.173](04-fields/5.173.md) | Nominal Elevation Angle | NOM ELEV ANGLE | 全部 |  |
| [5.174](04-fields/5.174.md) | Restrictive Airspace Link Continuation | LC | 全部 |  |
| [5.175](04-fields/5.175.md) | Holding Speed | HOLD SPEED | 全部 |  |
| [5.176](04-fields/5.176.md) | Pad Dimensions |  | 全部 |  |
| [5.177](04-fields/5.177.md) | Public/Military Indicator | PUB/MIL | 全部 | ✓ |
| [5.178](04-fields/5.178.md) | Time Zone |  | 全部 | ✓ |
| [5.179](04-fields/5.179.md) | Daylight Time Indicator | DAY TIME | 全部 |  |
| [5.180](04-fields/5.180.md) | Pad Identifier | PAD IDENT | 全部 |  |
| [5.181](04-fields/5.181.md) | H24 Indicator | H24 | 全部 |  |
| [5.182](04-fields/5.182.md) | Guard/Transmit | G/T | 19 20 21 22 23 |  |
| [5.183](04-fields/5.183.md) | Sectorization | SECTOR | 全部 |  |
| [5.184](04-fields/5.184.md) | Communication Altitude | COMM ALTITUDE | 全部 |  |
| [5.185](04-fields/5.185.md) | Sector Facility | SEC FAC | 全部 |  |
| [5.186](04-fields/5.186.md) | Sectorization Narrative |  | 全部 |  |
| [5.187](04-fields/5.187.md) | Distance Description | DIST DESC | 19 20 21 22 23 | ✓ |
| [5.188](04-fields/5.188.md) | Communications Distance | COMM DIST | 19 20 21 22 23 |  |
| [5.189](04-fields/5.189.md) | Position Narrative |  | 18 20 21 22 23 |  |
| [5.190](04-fields/5.190.md) | FIR/RDO Identifier | FIR/RDO | 全部 |  |
| [5.191](04-fields/5.191.md) | Triad Stations | TRIAD STA | 全部 |  |
| [5.192](04-fields/5.192.md) | Group Repetition Interval | GRI | 全部 |  |
| [5.193](04-fields/5.193.md) | Additional Secondary Phase Factor | ASF | 全部 |  |
| [5.194](04-fields/5.194.md) | Initial/Terminus Airport/Fix |  | 全部 |  |
| [5.195](04-fields/5.195.md) | Time of Operation |  | 全部 |  |
| [5.196](04-fields/5.196.md) | Name Format Indicator | NAME IND | 全部 | ✓ |
| [5.197](04-fields/5.197.md) | Modulation | MODULN | 全部 |  |
| [5.198](04-fields/5.198.md) | Datum Code | DATUM | 20 21 22 23 |  |
| [5.199](04-fields/5.199.md) | Signal Emission | SIG EM | 全部 |  |
| [5.200](04-fields/5.200.md) | Remote Facility | REM FAC | 18 20 21 22 23 |  |
| [5.201](04-fields/5.201.md) | Restriction Record Type | REST TYPE | 全部 |  |
| [5.202](04-fields/5.202.md) | Exclusion Indicator | EXC IND | 全部 |  |
| [5.203](04-fields/5.203.md) | Block Indicator | BLOCK IND | 全部 |  |
| [5.204](04-fields/5.204.md) | ARC Radius | ARC RAD | 全部 |  |
| [5.205](04-fields/5.205.md) | Navaid Limitation Code | NLC | 全部 | ✓ |
| [5.206](04-fields/5.206.md) | Component Affected Indicator | COMP AFFTD IND | 全部 | ✓ |
| [5.207](04-fields/5.207.md) | Sector From/Sector To | SECTR | 全部 | ✓ |
| [5.208](04-fields/5.208.md) | Distance Limitation | DIST LIMIT | 全部 |  |
| [5.209](04-fields/5.209.md) | Altitude Limitation | ALT LIMIT | 全部 |  |
| [5.210](04-fields/5.210.md) | Sequence End Indicator | SEQ END | 全部 | ✓ |
| [5.211](04-fields/5.211.md) | Required Navigation Performance | RNP | 全部 |  |
| [5.212](04-fields/5.212.md) | Runway Gradient | RWY GRAD | 18 20 21 22 23 |  |
| [5.213](04-fields/5.213.md) | Controlled Airspace Type | ARSP TYPE | 19 20 21 22 23 |  |
| [5.214](04-fields/5.214.md) | Controlled Airspace Center | ARSP CNTR | 全部 |  |
| [5.215](04-fields/5.215.md) | Controlled Airspace Classification | ARSP CLASS | 18 20 21 22 23 |  |
| [5.216](04-fields/5.216.md) | Controlled Airspace Name | ARSP NAME | 全部 |  |
| [5.217](04-fields/5.217.md) | Controlled Airspace Indicator | CTLD ARSP IND | 全部 |  |
| [5.218](04-fields/5.218.md) | Geographical Reference Table Identifier | GEO REF TBL ID | 全部 |  |
| [5.219](04-fields/5.219.md) | Geographical Entity | GEO ENT | 全部 |  |
| [5.220](04-fields/5.220.md) | Preferred Route Use Indicator | ET IND | 18 20 21 22 23 |  |
| [5.221](04-fields/5.221.md) | Aircraft Use Group | ACFT USE GP | 全部 |  |
| [5.222](04-fields/5.222.md) | GNSS/FMS Indicator | GNSS/FMS IND | 19 20 21 22 23 | ✓ |
| [5.223](04-fields/5.223.md) | Operation Type | OPS TYPE | 全部 |  |
| [5.224](04-fields/5.224.md) | Route Indicator | RTE IND | 全部 |  |
| [5.225](04-fields/5.225.md) | Ellipsoidal Height |  | 全部 |  |
| [5.226](04-fields/5.226.md) | Glide Path Angle | GPA | 全部 |  |
| [5.227](04-fields/5.227.md) | Orthometric Height | ORTH HGT | 全部 |  |
| [5.228](04-fields/5.228.md) | Course Width At Threshold | CRS WDTH | 全部 |  |
| [5.229](04-fields/5.229.md) | Final Approach Segment Data CRC Remainder | FAS CRC | 全部 |  |
| [5.230](04-fields/5.230.md) | Procedure Type | PROC TYPE | 全部 |  |
| [5.231](04-fields/5.231.md) | Along Track Distance | ATD | 19 20 21 22 23 |  |
| [5.232](04-fields/5.232.md) | Number of Engines Restriction | NOE | 全部 |  |
| [5.233](04-fields/5.233.md) | Turboprop/Jet Indicator | TURBO | 全部 |  |
| [5.234](04-fields/5.234.md) | RNAV Flag | RNAV | 全部 |  |
| [5.235](04-fields/5.235.md) | ATC Weight Category | ATC WC | 全部 |  |
| [5.236](04-fields/5.236.md) | ATC Identifier | ATC ID | 全部 |  |
| [5.237](04-fields/5.237.md) | Procedure Description | PROC DESC | 全部 |  |
| [5.238](04-fields/5.238.md) | Leg Type Code | LTC | 全部 |  |
| [5.239](04-fields/5.239.md) | Reporting Code | RPT | 全部 |  |
| [5.240](04-fields/5.240.md) | Altitude | ALT | 全部 |  |
| [5.241](04-fields/5.241.md) | Fix Related Transition Code | FRT Code | 全部 |  |
| [5.242](04-fields/5.242.md) | Procedure Category | PROC CAT | 全部 |  |
| [5.243](04-fields/5.243.md) | GLS Station Identifier |  | 全部 |  |
| [5.244](04-fields/5.244.md) | SBAS/GBAS Channel |  | 全部 |  |
| [5.245](04-fields/5.245.md) | Service Volume Radius |  | 全部 |  |
| [5.246](04-fields/5.246.md) | TDMA Slots |  | 全部 |  |
| [5.247](04-fields/5.247.md) | Station Type |  | 全部 |  |
| [5.248](04-fields/5.248.md) | Station Elevation WGS84 |  | 全部 |  |
| [5.249](04-fields/5.249.md) | Surface Code | SC | 全部 | ✓ |
| [5.250](04-fields/5.250.md) | Alternate Record Type | ART | 全部 |  |
| [5.251](04-fields/5.251.md) | Distance To Alternate | DTA | 全部 |  |
| [5.252](04-fields/5.252.md) | Alternate Type | ALT TYPE | 全部 |  |
| [5.253](04-fields/5.253.md) | Primary and Additional Alternate Identifier | ALT IDENT | 全部 |  |
| [5.254](04-fields/5.254.md) | Fixed Radius Transition Indicator | FIXED RAD IND | 全部 |  |
| [5.255](04-fields/5.255.md) | SBAS Service Provider Identifier | SBAS ID | 全部 |  |
| [5.256](04-fields/5.256.md) | Reference Path Data Selector | REF PDS | 19 20 21 22 23 |  |
| [5.257](04-fields/5.257.md) | Reference Path Identifier | REF ID | 全部 |  |
| [5.258](04-fields/5.258.md) | Approach Performance Designator | APD | 全部 |  |
| [5.259](04-fields/5.259.md) | Length Offset | OFFSET | 全部 |  |
| [5.260](04-fields/5.260.md) | Terminal Procedure Flight Planning Leg Distance | LEG DIST | 全部 |  |
| [5.261](04-fields/5.261.md) | Speed Limit Description | SLD | 全部 | ✓ |
| [5.262](04-fields/5.262.md) | Approach Type Identifier | ATI | 全部 |  |
| [5.263](04-fields/5.263.md) | Horizontal Alert Limit (HAL)/Lateral Alert Limit | LAL | 全部 |  |
| [5.264](04-fields/5.264.md) | Vertical Alert limit | VAL | 全部 |  |
| [5.265](04-fields/5.265.md) | Path Point TCH |  | 全部 |  |
| [5.266](04-fields/5.266.md) | TCH Units Indicator |  | 全部 |  |
| [5.267](04-fields/5.267.md) | High Precision Latitude | HPLAT | 全部 |  |
| [5.268](04-fields/5.268.md) | High Precision Longitude | HPLONG | 全部 |  |
| [5.269](04-fields/5.269.md) | Helicopter Procedure Course | HPC | 全部 |  |
| [5.270](04-fields/5.270.md) | TCH Value Indicator | TCHVI | 19 20 21 22 23 | ✓ |
| [5.271](04-fields/5.271.md) | Procedure Turn | PROC TURN | 全部 |  |
| [5.272](04-fields/5.272.md) | TAA Sector Identifier |  | 全部 |  |
| [5.273](04-fields/5.273.md) | TAA Waypoint |  | 全部 |  |
| [5.274](04-fields/5.274.md) | TAA Sector Radius |  | 全部 |  |
| [5.275](04-fields/5.275.md) | Level of Service Name | LSN | 全部 |  |
| [5.276](04-fields/5.276.md) | Level of Service Authorized |  | 全部 |  |
| [5.277](04-fields/5.277.md) | DME Operational Service Volume | D-OSV | 19 20 21 22 23 |  |
| [5.278](04-fields/5.278.md) | Activity Type |  | 19 20 21 22 23 |  |
| [5.279](04-fields/5.279.md) | Activity Identifier |  | 19 20 21 22 23 |  |
| [5.280](04-fields/5.280.md) | Special Activity Area Size |  | 19 20 21 22 23 |  |
| [5.281](04-fields/5.281.md) | Special Activity Area Volume |  | 19 20 21 22 23 |  |
| [5.282](04-fields/5.282.md) | Special Activity Area Operating Times |  | 19 20 21 22 23 |  |
| [5.283](04-fields/5.283.md) | Communications Class | Comm Class | 19 20 21 22 23 |  |
| [5.284](04-fields/5.284.md) | Assigned Sector Name | ASN | 19 20 21 22 23 |  |
| [5.285](04-fields/5.285.md) | Time Narrative |  | 19 20 21 22 23 |  |
| [5.286](04-fields/5.286.md) | Multi-Sector Indicator | MSEC IND | 19 20 21 22 23 |  |
| [5.287](04-fields/5.287.md) | Type Recognized By | TRB | 19 20 21 22 23 |  |
| [5.288](04-fields/5.288.md) | Translation |  | 19 20 21 22 23 |  |
| [5.289](04-fields/5.289.md) | Used On |  | 19 20 21 22 23 |  |
| [5.290](04-fields/5.290.md) | Procedure Design Mag Var | PDMV | 19 20 21 22 23 |  |
| [5.291](04-fields/5.291.md) | Procedure Design Mag Var Indicator | PDMVI | 19 20 21 22 23 |  |
| [5.292](04-fields/5.292.md) | Category Distance |  | 19 20 21 22 23 |  |
| [5.293](04-fields/5.293.md) | Vertical Scale Factor | VSF | 19 20 21 22 23 |  |
| [5.294](04-fields/5.294.md) | RVSM Minimum Level |  | 19 20 21 22 23 |  |
| [5.295](04-fields/5.295.md) | RVSM Maximum Level |  | 19 20 21 22 23 |  |
| [5.296](04-fields/5.296.md) | RNP Level of Service | LSN | 19 20 21 22 23 |  |
| [5.297](04-fields/5.297.md) | Route Inappropriate Navaid Indicator |  | 19 20 21 22 23 |  |
| [5.298](04-fields/5.298.md) | Holding Pattern/Race Track Course Reversal Leg Inbound/Outbound Indicator |  | 19 20 21 22 23 |  |
| [5.299](04-fields/5.299.md) | Procedure Referenced Fix Identifier |  | 20 21 22 23 |  |
| [5.300](04-fields/5.300.md) | Final Approach Course as Runway |  | 20 21 22 23 |  |
| [5.301](04-fields/5.301.md) | Procedure Design Aircraft Category or Type |  | 20 21 22 23 |  |
| [5.302](04-fields/5.302.md) | Surface Type |  | 21 22 23 |  |
| [5.303](04-fields/5.303.md) | Helipad Shape |  | 21 22 23 |  |
| [5.304](04-fields/5.304.md) | Sector Bearing Reference Waypoint |  | 21 22 23 |  |
| [5.305](04-fields/5.305.md) | Heliport Type |  | 21 22 23 |  |
| [5.306](04-fields/5.306.md) | Preferred Multiple Approach Indicator |  | 21 22 23 |  |
| [5.307](04-fields/5.307.md) | Special Indicator |  | 21 22 23 |  |
| [5.308](04-fields/5.308.md) | Remote Altimeter Flag |  | 21 22 23 |  |
| [5.309](04-fields/5.309.md) | Maximum Allowable Helicopter Weight |  | 21 22 23 |  |
| [5.310](04-fields/5.310.md) | Helicopter Performance Requirement |  | 21 22 23 |  |
| [5.311](04-fields/5.311.md) | FIR/FRA Transition |  | 21 22 23 |  |
| [5.312](04-fields/5.312.md) | Starter Extension |  | 21 22 23 |  |
| [5.313](04-fields/5.313.md) | TORA |  | 22 23 |  |
| [5.314](04-fields/5.314.md) | TODA |  | 22 23 |  |
| [5.315](04-fields/5.315.md) | ASDA |  | 22 23 |  |
| [5.316](04-fields/5.316.md) | LDA |  | 22 23 |  |
| [5.317](04-fields/5.317.md) | Runway Usage Indicator |  | 22 23 |  |
| [5.318](04-fields/5.318.md) | Runway Accuracy Compliance Flag |  | 22 23 |  |
| [5.319](04-fields/5.319.md) | Landing Threshold Elevation Accuracy Compliance Flag |  | 22 23 |  |
| [5.320](04-fields/5.320.md) | SBAS Final Approach Course |  | 22 23 |  |
| [5.321](04-fields/5.321.md) | Helipad Maximum Rotor Diameter |  | 23 |  |
| [5.322](04-fields/5.322.md) | Helipad Type |  | 23 |  |
| [5.323](04-fields/5.323.md) | Helipad Orientation |  | 23 |  |
| [5.324](04-fields/5.324.md) | Helipad Identifier Orientation |  | 23 |  |
| [5.325](04-fields/5.325.md) | Preferred Approach Bearing |  | 23 |  |
| [5.326](04-fields/5.326.md) | Ground Facility Indentifier |  | 23 |  |
| [5.327](04-fields/5.327.md) | Authority Format Identifier | AFI | 23 |  |
| [5.328](04-fields/5.328.md) | Initial Domain Identifier |  | 23 |  |
| [5.329](04-fields/5.329.md) | Version | VER | 23 |  |
| [5.330](04-fields/5.330.md) | Administration | ADM | 23 |  |
| [5.331](04-fields/5.331.md) | Routing Domain Format | RDF | 23 |  |
| [5.332](04-fields/5.332.md) | Administrative Region Selector | ARS | 23 |  |
| [5.333](04-fields/5.333.md) | Location | LOC | 23 |  |
| [5.334](04-fields/5.334.md) | System Identifier | SYS | 23 |  |
| [5.335](04-fields/5.335.md) | Network Service Access Point Selector | NSEL | 23 |  |
| [5.336](04-fields/5.336.md) | Context Management Transport Selector | CM TSEL | 23 |  |
| [5.337](04-fields/5.337.md) | Use Indicator |  | 23 |  |
| [5.338](04-fields/5.338.md) | VOR Range/Power | VORPWR | 23 |  |
| [5.339](04-fields/5.339.md) | DME Expanded Service Volume | DESV | 23 |  |
| [5.340](04-fields/5.340.md) | Unmanned Aerial Vhicle (UAV) Only |  | 23 |  |
| [5.341](04-fields/5.341.md) | Military Indicator |  | 23 |  |
| [5.342](04-fields/5.342.md) | Source of LAL/VAL |  | 23 |  |
| [5.343](04-fields/5.343.md) | Holding Pattern Magnetic Variation | HPMV | 23 |  |
