# arinc424-skill

ARINC 424 导航数据规范的全量参考与工具集，覆盖 **424-18 到 424-23 六个版本**。
给 AI agent（WorkBuddy / Claude Code 等）使用：agent 读到本目录的 `SKILL.md` 后，
就能查规范、解码/编码 132 列记录、对比版本差异、指导修改 `arinc424-model-rs`。

## 怎么让 AI 用上它

skill 目前不在全局技能目录里，需要在对话里指给 agent 看。**任一方式**：

```
读一下 D:/FlightSimulation/Coding/arinc424-skill/SKILL.md，然后……
```

```
@"D:/FlightSimulation/Coding/arinc424-skill" 帮我……
```

（`@` 引用目录，或直接把 SKILL.md 拖进对话。）

之后同一轮对话里的所有 ARINC 424 问题都会走这个 skill：它会自己调
`scripts/arinc424.py` 查数据库、翻 `references/` 里的文档，不需要你每次都引用。

## Prompt 怎么写（示例）

### 解读一条记录

直接把整行数据贴进来（132 个字符，别截断）：

```
读一下 D:/FlightSimulation/Coding/arinc424-skill/SKILL.md，然后解码这条记录，
逐字段解释是什么意思：
SUSAD   KJFKK1JFK  0 11350V      N40381900W073464600……
```

### 查规范 / 问概念

```
ARINC 424-23 里跑道记录的 Runway Gradient 占哪几列？5.x 章节号是多少？
```

```
PATH TERM 的 TF 和 RF 有什么区别？给出代码表定义。
```

### 构造记录

```
帮我按 424-23 写一条 VOR 主记录：JFK 台，频率 113.50，坐标 N40°38'19" W73°46'46"，
其余字段按规范补默认值，输出 132 列定宽行。
```

### 对比版本

```
VHF NAVAID 记录在 424-18 和 424-23 之间列位有什么变化？我要迁移解析器。
```

### 改 Rust 模型

```
我想在 arinc424-model-rs 里加一个 Holding Pattern 记录类型，
参考 arinc424-skill 的 09-rust-guide，告诉我步骤和列位定义。
```

## 写好 prompt 的三个要点

1. **尽量指明版本号**。六个版本列位不同（例：VOR Name 在 424-18 占 94–123 列，
   424-23 占 94–118 列）。不写版本时 agent 默认按 424-23 处理。
2. **贴数据要贴整行**。132 列定宽格式，列位即语义；少一个字符整条记录错位。
   如果不确定是主记录还是续记录也没关系，工具会自动判定。
3. **问"什么/哪几列/什么意思"直接问就行**；数据库自包含，不依赖 PDF，
   agent 能脱离规范原文回答。

## 目录结构（给想了解原理的人）

```
SKILL.md            agent 入口：决策树、命令速查、工作流
scripts/arinc424.py 零依赖 CLI：decode/encode/record/field/codes/diff/search/list
data/arinc424.json  单一数据源：六版布局 + 字段定义 + 代码表 + Rust 模型映射
references/         396 篇由数据源生成的文档（记录分册/字段页/码表/版本变更/Rust 指南）
tools/              构建管线：PDF 提取 → rustparse → build → render
tests/acceptance.py 验收：652 条布局列位完整性、45 组编解码往返、文档一致性
docs/               六版规范 PDF（仅构建期使用）
```

### 重建（仅维护者需要）

```bash
python tests/acceptance.py          # 验收
python tools/build.py --force       # 从 PDF 重建数据源（venv 需装 pdfplumber + pypdf）
python tools/render.py              # 由数据源重新生成 references/
```

`tools/rustparse.py` 中模型仓库路径默认 `D:/FlightSimulation/Coding/arinc424-model-rs`，
单独运行 `python tools/rustparse.py <模型仓库路径>` 可覆盖。
