# arinc424-model-rs 集成与扩展

`arinc424-model-rs`（v0.14.x）是 ARINC 424-18 的 Rust 实现。本页说明怎么用它解析数据、
怎么给它加记录类型和字段，以及哪些地方容易踩坑。

> **列位基准**：模型实现的是 **424-18**。改代码时所有 `start`/`end` 只能查 424-18 的布局
> （`arinc424.py record <编号> --version 18`）。424-19 以后新增的字段在模型里没有位置。

## 仓库分层

| 层 | 位置 | 职责 |
|---|---|---|
| `arinc424-core` | `crates/arinc424-core` | 记录结构体、字段编解码、代码表枚举 |
| `arinc424-macro-rules` | `crates/arinc424-macro-rules` | `define_business_typed_builders!` 之类的声明宏 |
| `arinc424-proc-macros` | `crates/arinc424-proc-macros` | `ArincSpec` / `arinc_record` / `arinc_record_continuation` |
| `arinc424-model` | `src/` | 产物级模型 + 单遍解析器 + AIRAC 周期 |

公开入口（`src/lib.rs`）：

```rust
pub use metadata::AiracCycle;
pub use navdata::{parse_file, sort_procedures, NavData};
pub use record::Coordinate;
```

## 一、用它解析数据

```rust
use arinc424_model::{parse_file, sort_procedures};

let mut data = parse_file(std::path::Path::new("FAACIFP18.dat"))?;
sort_procedures(&mut data);          // 把 SID/STAR/进近的公共段与过渡段排好序
println!("{} airports, {} navaids", data.airports.len(), data.navaids.len());
```

- `parse_file(path)`：单文件。
- `parse_files(paths)`：多文件按序合并（主记录与其续记录可能跨文件）。
- `parse_bytes(&[u8])`：内存输入。**记录按字节处理**，源文件不保证是合法 UTF-8。
- `NavData` 的字段都是 `Vec`：`airports`、`runways`、`navaids`、`waypoints`、`airways`、
  `procedures`、`localizers`、`fir_points`。

解析完的辅助查询：

```rust
arinc424_model::resolve_fix(&data, "KJFK", &leg);            // Option<Coordinate>
arinc424_model::lookup_fix(&data, 'E', 'A', "K6", "DCT");    // section, subsection, icao, ident
arinc424_model::count_unresolved(&data);                     // 有多少航段没解析出坐标
arinc424_model::unresolved_fix_summary(&data);               // Vec<(String, usize)>
```

`NavData` 的主要字段：`airports`、`runways`、`runway_records`、`navaids`、`waypoints`、
`localizers`、`communications`、`minimum_safe_altitudes`、`fir_points` 都是 `Vec`；
`airways` 与 `procedures` 是 `BTreeMap`（航路按标识符索引，程序按机场索引，
另有 `airway_order` 保留源文件顺序）；`fix_index` / `ident_index` / `airport_index`
是定位点的坐标索引。

`record` 模块是底层工具，直接按列取值：

```rust
use arinc424_model::record::{field, ch, trimmed, parse_coordinate, section, subsection_of};

let lat = field(line, 32, 41);                 // &[u8]，1-based、闭区间
let c   = ch(line, 5);                         // 第 5 列的字符
let s   = section(line);                       // 'D'、'P'…
let sub = subsection_of(line);                 // 机场程序读第 13 列，其余读第 6 列
let xy  = parse_coordinate(field(line,32,41), field(line,42,51));
```

## 二、加一个记录类型

以新增 VHF 导航台为例，实际文件是
`crates/arinc424-core/src/model/business/navaid/vhf.rs`。

**1. 声明结构体。** `#[arinc(start, end)]` 用的是规范里的 1-based 闭区间列位：

```rust
use arinc424_proc_macros::ArincSpec;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default, ArincSpec)]
#[arinc_record(mappings = [('D', ' ', 6)])]
pub struct VhfPrimaryRecord {
    #[arinc(start = 1, end = 1)]
    pub recd_type: RecordType,
    #[arinc(start = 2, end = 4)]
    pub cust_area: CustAreaItem,
    #[arinc(start = 5, end = 5)]
    pub sect_code: SectionCode,
    #[arinc(start = 14, end = 17)]
    pub vor_ident: String,
    #[arinc(start = 22, end = 22, continuation = true)]
    pub cont_nr: char,
    #[arinc(start = 23, end = 27,
            builder_ty = crate::field_types::spec_builders::VorFrequencyBuilder)]
    pub vor_freq: FrequencyType,
    #[arinc(start = 33, end = 41,
            builder_ty = crate::field_types::spec_builders::LatitudeOptBuilder)]
    pub vor_lat: LatLonType,
    // …
}
```

要点：

- `mappings = [('D', ' ', 6)]` 里的 `6` 是 **Subsection 所在列**。VHF 在第 6 列；
  机场程序（PD/PE/PF）在第 13 列，写成 `('P', 'D', 13)`。
- `continuation = true` 标记续记录号那一列（第 22 列，程序记录是第 39 列）。
- 空白列**不用声明**，但相邻字段之间不能留空隙以外的重叠——列位必须能被
  `start/end` 唯一确定。
- 需要特殊编解码的字段挂 `builder_ty = ...::XxxBuilder`，其余走自动推断。

**2. 把结构体挂进 `model/mod.rs` 的模块树**，并在 `navdata.rs` 的
`parse_reader_into` 里按 Section/Subsection 派发。

**3. 加测试。** 每个记录类型都有对应的测试模块，用真实数据行做往返断言：
`编码 → 132 列 → 解码 → 与原文逐字段相等`。

## 三、加一个续记录

续记录复用主记录的前若干列，用 `arinc_record_continuation` 声明：

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default, ArincSpec)]
#[arinc_record_continuation(
    primary = crate::model::navaid::VhfPrimaryRecord,
    base_start = 1,
    base_end = 21,
    continuation_pos = 22,
    cont_type = 'L'
)]
pub struct VhfLimitationContinuationRecord {
    #[arinc(start = 22, end = 22, continuation = true)]
    pub cont_nr: char,
    #[arinc(start = 23, end = 23)]
    pub application_type: ContinuationApplicationType,
    #[arinc(start = 28, end = 107)]
    pub limitations: [VhfLimitationBlock; 5],   // 5 个 20 列的块
    #[arinc(start = 124, end = 128)]
    pub file_recd_no: FileRecdNoType,
    #[arinc(start = 129, end = 132)]
    pub cycle: CycleType,
}
```

- `base_start`/`base_end` 是从主记录继承的列区间（1–21）：续记录的前 21 列
  与主记录逐字相同，不用重复声明。
- `cont_type = 'L'` 是第 23 列的应用类型字母。同一个主记录可以有多个续记录类型，
  每个字母一个。
- 重复块写成 `[Block; N]`，`Block` 自身也是 `#[derive(ArincSpec)]` 的结构体，
  但它的 `start`/`end` 是**块内相对列位**（`VhfLimitationBlock` 从 1 开始，宽 20 列）。

## 四、加一个字段类型

`crates/arinc424-core/src/field_types/definitions.rs` 里是类型别名，文件头注释写规范编号：

```rust
/// 5.36 Latitude (LATITUDE)
///
/// 5.37 Longitude (LONGITUDE)
pub type LatLonType = Option<f64>;
```

需要自定义编解码时，在 `field_types/business/` 写 `deserialize`/`serialize`，
再用宏注册 builder：

```rust
// field_types/spec_builders/business.rs
arinc424_macro_rules::define_business_typed_builders!(
    LatitudeOptBuilder => Option<f64> => (latitude::deserialize_opt, latitude::serialize_opt),
);
```

然后在 `spec_builders.rs` 里 `pub use business::LatitudeOptBuilder;`。

**规则**：可空字段一律 `Option<T>`；全空白列反解为 `None`，不要反解成 `0`。

## 五、加一个代码表

`crates/arinc424-core/src/data_types/` 下每个文件一个枚举，文件第一行写规范编号：

```rust
// 5.21 Path and Termination (PATH TERM)
```

枚举实现 `ArincCode`，并且**必须保留兜底变体**，让未知码值不至于让整条记录解析失败：

```rust
impl ArincCode for RecordType {
    fn from_char(value: char) -> Self {
        match value {
            ' ' => Self::Blank,
            'S' => Self::Standard,
            'T' => Self::Tailored,
            other => Self::Other(other),      // 兜底
        }
    }
    fn as_char(&self) -> char { /* 反查 */ }
}
```

多列联合的代码表（如 Waypoint Description Code 的第 40/41/42 列）放在以枚举命名的
子目录里，每列一个文件：`waypoint_description_code/col_40.rs`。

本 skill 的码表就是从这个目录的枚举生成的，所以**加了枚举后重新跑
`python tools/build.py`**，码表会自动出现在 `references/05-code-tables.md` 和
`arinc424.py codes` 里。

## 六、坑

- **列位是 424-18 的。** 用 `arinc424.py record 4.1.2.1 --version 18` 取，别用默认版本。
- **`start`/`end` 是闭区间且从 1 开始。** `start = 33, end = 41` 表示 9 列。
- **经纬度是压缩的度分秒串**，不是十进制。`N33591899` = 北纬 33°59′18.99″，
  用 `parse_coordinate` 或对应 builder，不要自己切字符串。
- **记录按字节读。** 字段取值返回 `&[u8]`；转文本用 `text()`/`trimmed()`，
  不要假设是 UTF-8。
- **续记录号列不固定。** 大多数是第 22 列，机场程序是第 39 列，判断前先看布局。
- **数据的版本比模型新。** 拿到 424-23 的数据时，424-19 之后新增的列在模型里没有字段，
  解析会静默忽略——核对时以 `diff` 命令的「added」列表为准。

## 七、核对清单

改完模型后确认：

1. `cargo test` 全绿。
2. 新结构体的列位与 `arinc424.py record <编号> --version 18` 一致。
3. 用一条真实数据行做 `decode → encode` 往返，输出与原文逐字节相同。
4. 若新增/修改了 `data_types` 枚举，重跑 `python tools/build.py && python tools/render.py`。

`references/08-model-mapping.md` 里有全部结构体与 424-18 布局的逐列核对结果，
可以直接用来检查有没有漏列。
