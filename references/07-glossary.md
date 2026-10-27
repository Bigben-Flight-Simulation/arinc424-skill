# 术语与约定

ARINC 424 的正文用大量缩写。这一页收常用术语，以及航径终止码的完整含义。

## 常用术语

| 术语 | 中文 | 含义 |
|---|---|---|
| **ACF** | 机场/设施 | Aerodrome/Company/Facility 相关数据，泛指机场、导航台等地面设施。 |
| **AIRAC** | 定期生效的航行资料周期 | 28 天一个周期，导航数据按它发布。记录末尾的 Cycle Date 就是这个周期的编号。 |
| **Application Type** | 应用类型 | 续记录第 23 列（机场程序是第 40 列）的字母，说明这条续记录装什么内容。 |
| **Continuation Record** | 续记录 | 一条主记录装不下时的后续记录，靠 Continuation Record No. 排序。 |
| **Customer/Area Code** | 客户/区域代码 | 第 2–4 列，标识数据提供方，如 USA、EUR。 |
| **Cycle Date** | 周期日期 | 第 129–132 列，`YYNN` 格式，记录所属的 AIRAC 周期。 |
| **DME** | 测距仪 | Distance Measuring Equipment，给出到台的斜距。常与 VOR 并置成 VOR/DME。 |
| **Duplicate Indicator** | 重复指示符 | 同名导航台/航路点出现多次时，用第二个字母区分（如 `LAX` 与 `LAXA`）。 |
| **Enroute Airway** | 航路 | 航路航线，由一串航路点与航段组成，记录码 `ER`。 |
| **File Record Number** | 文件记录号 | 第 124–128 列，文件内序号，用于定位与增量更新。 |
| **FIR / UIR** | 飞行情报区 / 高空情报区 | Flight Information Region / Upper FIR，空域管理的基本单元。 |
| **Fix** | 定位点 | 可用于定位的地理点，包括航路点、导航台、机场基准点。 |
| **FRA** | 自由航路空域 | Free Route Airspace，允许航路点之间直飞，不依赖固定航路。 |
| **GLS** | GNSS 着陆系统 | GBAS Landing System，基于 GBAS 的精密进近。 |
| **ILS** | 仪表着陆系统 | 由航向台（LOC）、下滑台（GS）与指点标组成。 |
| **Localizer** | 航向台 | ILS 的水平引导分量，给出跑道中心线方向。 |
| **Magnetic Variation** | 磁差 | 磁北与真北的夹角，东偏为正。记录里 5 位，首位 E/W。 |
| **MORA** | 最低偏航高度 | Minimum Off-Route Altitude，网格化的安全高度。 |
| **MSA** | 最低扇区高度 | Minimum Sector Altitude，以某点为中心、按扇区给出的最低安全高度。 |
| **NAVAID** | 导航台 | VOR、NDB、TACAN 等地面导航设施的统称。 |
| **NDB** | 无方向性信标 | Non-Directional Beacon，靠 ADF 测向。频率单位 kHz。 |
| **PBN** | 基于性能的导航 | Performance Based Navigation，涵盖 RNAV 与 RNP 规范。 |
| **Preferred Route** | 优选航路 | 预先定义的常用航路组合，记录码 `ET`。 |
| **Primary Record** | 主记录 | 续记录号为 0 的那条记录，定义一个实体的主体信息。 |
| **Procedure** | 程序 | SID、STAR、进近的统称，由一串航段（leg）组成。 |
| **RNAV** | 区域导航 | Area Navigation，允许航空器沿任意期望航径飞行。 |
| **RNP** | 所需导航性能 | Required Navigation Performance，带机载性能监视与告警的 RNAV。 |
| **SID** | 标准仪表离场程序 | Standard Instrument Departure，记录码 `PD`。 |
| **STAR** | 标准终端进场程序 | Standard Terminal Arrival Route，记录码 `PE`。 |
| **TAA** | 终端进场高度 | Terminal Arrival Altitude，进近程序周边的扇区高度。 |
| **TACAN** | 战术空中导航 | 军用 VOR/DME 组合，记录码 `DT`。 |
| **TCH** | 跑道入口高 | Threshold Crossing Height，航空器过跑道入口时的轮高。 |
| **Transition** | 过渡 | 连接航路与程序、或程序与进近的过渡航段，用 Transition Identifier 标识。 |
| **VOR** | 甚高频全向信标 | VHF Omnidirectional Range，给出相对台的磁方位。频率 108–118 MHz。 |
| **Waypoint** | 航路点 | 程序或航路上用于定义航径的点，不一定是实体设施。 |
| **Waypoint Description Code** | 航路点描述码 | 第 40–43 列的四字符标记，说明这个点是什么（机场、导航台、飞越点等）。 |

## 航径终止码（PATH TERM）

程序记录的每个航段都带一个两字母的航径终止码，决定这一段怎么飞。它定义在字段 5.21，完整取值见 [码表](05-code-tables.md#521-path-and-termination)。

| 代码 | 全称 | 含义 |
|---|---|---|
| `IF` | Initial Fix | 起始点：只定义位置，本身不构成航段。 |
| `TF` | Track to Fix | 从当前点直飞下一个定位点，航径是大圆航线。 |
| `CF` | Course to Fix | 按指定航向飞到定位点，航径是固定方位线。 |
| `DF` | Direct to Fix | 从当前位置直飞定位点，不约束进入方位。 |
| `FA` | Fix to Altitude | 从定位点沿航径飞至指定高度。 |
| `FC` | Track from Fix to Distance | 从定位点沿航道飞指定距离。 |
| `FD` | Track from Fix to DME Distance | 从定位点沿航道飞到某个 DME 距离。 |
| `FM` | Fix to Manual Termination | 从定位点开始，航径由飞行员手动终止。 |
| `CA` | Course to Altitude | 沿指定航向爬升到某个高度。 |
| `CD` | Course to DME Distance | 沿指定航向飞到某个 DME 距离。 |
| `CI` | Course to Intercept | 沿指定航向飞到切入下一个航径。 |
| `CR` | Course to Radial | 沿指定航向飞到某条径向线。 |
| `RF` | Constant Radius Arc | 定半径圆弧，圆心与半径由相邻航段确定。 |
| `AF` | Arc to Fix | 沿圆弧飞到定位点。 |
| `VA` | Heading to Altitude | 按指定航向飞到某个高度。 |
| `VD` | Heading to DME Distance | 按指定航向飞到某个 DME 距离。 |
| `VI` | Heading to Intercept | 按指定航向飞到切入下一个航径。 |
| `VM` | Heading to Manual Termination | 按指定航向飞，由飞行员手动终止。 |
| `VR` | Heading to Radial | 按指定航向飞到某条径向线。 |
| `FI` | Fix to Intercept | 从定位点飞到切入下一个航径。 |
| `HA` | Hold to Altitude | 等待航线，到达指定高度后退出。 |
| `HF` | Hold to Fix | 等待航线，到达定位点后退出。 |
| `HM` | Hold to Manual Termination | 等待航线，由飞行员手动退出。 |

