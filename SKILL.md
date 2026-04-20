---
name: novel-analyzer
description: >
  多Agent协作小说拆解工具。从已有小说中提取剧情模板、角色原型、写作技法，
  输出可直接喂给 novel-writer skill 的 reference 文件。支持单篇深度拆解和批量套路提取。
  触发词：分析小说、拆解小说、提取套路、分析爆款、novel-analyze、拆分小说。
  搭配 novel-writer skill 使用：分析 → 提取套路 → 生成 reference → Writer 按套路创作。
---

# Novel Analyzer — 多Agent协作小说拆解工具

## 架构总览

```
用户输入小说文本
    ↓
[编排器/你]
    ├─ 模式 A：单篇深度拆解
    │   spawn → Structure Analyst（剧情结构）
    │   spawn → Character Analyst（角色与关系）
    │   spawn → Style Analyst（文风与技法）
    │   → 合并 → 生成分析报告
    │
    ├─ 模式 B：套路提取（单篇）
    │   运行模式 A → 从分析报告中抽象套路
    │   → 生成 Writer-ready reference 文件
    │
    └─ 模式 C：批量套路库（多篇）
        对同类型多篇小说运行模式 B
        → 合并去重 → 生成该类型的套路参考库
```

## Agent 角色

| Agent | 职责 | 角色定义文件 |
|-------|------|-------------|
| 📐 **Structure Analyst** | 提取剧情模板、节拍表、冲突升级链、爽点分布 | `agents/structure-analyst.md` |
| 👥 **Character Analyst** | 提取角色原型、关系模式、语言特征、弧光类型 | `agents/character-analyst.md` |
| ✍️ **Style Analyst** | 提取开篇钩子、对话模式、爽点技法、节奏公式 | `agents/style-analyst.md` |
| 🔗 **Synthesizer** | 汇总输出，生成 Writer-ready reference 文件 | `agents/synthesizer.md` |

## 数据流接口

Analyst → Synthesizer 的 JSON schema 定义在 `references/data-flow-spec.md` 中。
所有 Analyst 必须严格按此 schema 输出，Synthesizer 按此 schema 解析输入。

| 文件 | 用途 |
|------|------|
| `references/data-flow-spec.md` | Analyst-Synthesizer JSON 接口定义 + 字段映射表 |
| `references/analysis-framework.md` | 分析框架参考（三幕/英雄之旅等） |
| `references/mermaid-templates.md` | 图表模板 |


## 核心原则：输出必须对齐 Writer 输入

**novel-analyzer 的最终产物不是给人看的分析报告，而是给 Writer 用的写作素材。**

输出内容以 `## 🏷️ {类型}` 标签格式追加到 novel-writer 的现有 reference 文件中（plot-design.md / character-design.md / writing-techniques.md / emotion-curve.md），而非生成独立文件。每个类型的内容在文件内以标签分区，互不干扰。

| 输出内容 | 追加到 novel-writer 文件 | Writer 使用阶段 |
|----------|------------------------|----------------|
| `## 🏷️ {类型}` 剧情模板 | `references/plot-design.md` | Planner 大纲阶段 |
| `## 🏷️ {类型}` 角色原型 | `references/character-design.md` | Planner 大纲阶段 |
| `## 🏷️ {类型}` 写作技法 | `references/writing-techniques.md` | Writer 写作阶段 |
| `## 🏷️ {类型}` 情绪曲线 | `references/emotion-curve.md` | Planner 大纲阶段 |
| `## 🏷️ {类型}` 世界观 | `references/worldbuilding.md` | Planner 大纲阶段（如适用） |

### Writer-ready 格式规范（标签追加模式）

所有输出内容以 `## 🏷️ {类型}` 标签格式**追加**到 novel-writer 的对应 reference 文件中。每个类型在文件内独立成段，通过标签定位。

```markdown
## 🏷️ 重生复仇

> 来源：2篇重生复仇小说分析。大纲阶段使用。

### 核心剧情模板（2种）

#### 模板1：订婚宴修罗场复仇
**一句话：** ...
**适用场景：** ...
**节拍表：**
1. ... — 张力 X/10
2. ... — 张力 X/10

### 冲突升级链
...

### 反转技法库
...

### 爽点节奏公式
...
```

**追加规则：**
- 同一类型的内容只输出一次，以 `## 🏷️ {类型}` 开头
- 如果目标文件中已有该类型的标签段落，应先检查是否需要更新而非重复追加
- 每个标签段落自成一体，包含该类型在该维度的全部内容

**同时输出 slim 精简版：**
- 每个完整段落同时生成一个 `## 🏷️ {类型}` 的 slim 版（追加到 novel-writer 的 `references/slim/` 下对应文件）
- slim 版只保留核心规则和模板名称（~500-800字），不含详细例句和解释

**禁止输出**：纯叙述性的分析段落（"这部小说的主题是..."）。  
**必须输出**：可复用的模板、公式、检查清单（"复仇文五幕式：① ② ③ ④ ⑤"）。

## 工作流程

### 模式 A：单篇深度拆解

#### Step 1：输入处理

**短篇（<5000字）**：直接分析。

**中长篇（>5000字）**：
1. 用 `scripts/chunk_novel.py` 分块
2. 逐块提取结构化数据
3. 跨块合并

#### Step 2：并行启动三个分析师

编排器读取 `agents/` 下三个分析师定义，同时 spawn：

**Structure Analyst** 负责：
- 识别剧情结构类型（三幕/五幕/英雄之旅/网文特殊结构）
- 提取每章节拍（场景、角色、核心动作、张力等级）
- 梳理冲突升级链
- 标注爽点分布和节奏

**Character Analyst** 负责：
- 提取所有角色的原型归类
- 绘制关系矩阵（关系类型 + 变化轨迹）
- 分析角色语言特征（句式、用词、口头禅）
- 记录角色弧光类型

**Style Analyst** 负责：
- 识别开篇钩子模式
- 提取对话技法和张力手段
- 分析爽点实现方式（压-亮-弹等）
- 统计节奏数据（对话比、句长、事件密度）

#### Step 3：合并生成分析报告

三个分析师的结构化输出合并为完整的分析报告。

---

### 模式 B：套路提取（单篇）

#### Step 1：先运行模式 A

获取单篇小说的完整分析。

#### Step 2：启动 Synthesizer

编排器将三个分析师的结构化输出传给 Synthesizer，要求：
- 从具体分析中抽象出可复用模式
- 生成符合 Writer-ready 格式的 reference 文件

Synthesizer 输出 3-4 个文件：
1. `{novel-name}-structure.md` — 剧情模板
2. `{novel-name}-characters.md` — 角色原型
3. `{novel-name}-techniques.md` — 写作技法
4. `{novel-name}-worldbuilding.md` — 世界观规则（如适用）

#### Step 3：保存

写入项目目录：
```
novel-analyzer/output/{novel-name}/
├── analysis-report.md          ← 完整分析报告（人读）
├── plot-design-append.md       ← 🏷️ 段落，追加到 novel-writer/references/plot-design.md
├── character-design-append.md  ← 🏷️ 段落，追加到 novel-writer/references/character-design.md
├── writing-techniques-append.md← 🏷️ 段落，追加到 novel-writer/references/writing-techniques.md
├── emotion-curve-append.md     ← 🏷️ 段落，追加到 novel-writer/references/emotion-curve.md（如适用）
└── slim/                       ← 精简版（每文件~500-800字）
    ├── plot-design-slim.md
    ├── character-design-slim.md
    └── writing-techniques-slim.md
```

---

### 模式 C：批量套路库（多篇同类型）

#### Step 1：对每篇运行模式 B

获取多篇同类型小说各自的套路提取结果。

#### Step 2：启动 Synthesizer 做合并去重

编排器将所有单篇的 Writer-ready 文件传给 Synthesizer，要求：
- 合并相同模式（如多篇都有"打脸"模板 → 合并为通用版）
- 去重相似技法
- 统计频率（哪些模式出现最多 = 最核心套路）
- 生成最终的类型套路库

输出：
```
novel-analyzer/output/{genre}-tropes/
├── plot-design-append.md       ← 合并去重后的 🏷️ 段落
├── character-design-append.md  ← 合并去重后的 🏷️ 段落
├── writing-techniques-append.md← 合并去重后的 🏷️ 段落
├── emotion-curve-append.md     ← 合并去重后的 🏷️ 段落（如适用）
├── batch-analysis.md           ← 批量分析摘要（人读）
└── slim/                       ← 精简版
    ├── plot-design-slim.md
    ├── character-design-slim.md
    └── writing-techniques-slim.md
```

#### Step 3：安装到 novel-writer

将 🏷️ 段落**追加**（非覆盖）到 novel-writer 的对应 reference 文件末尾：
- `plot-design-append.md` 内容 → 追加到 `~/.openclaw/skills/novel-writer/references/plot-design.md` 末尾
- `character-design-append.md` 内容 → 追加到 `~/.openclaw/skills/novel-writer/references/character-design.md` 末尾
- `writing-techniques-append.md` 内容 → 追加到 `~/.openclaw/skills/novel-writer/references/writing-techniques.md` 末尾
- `emotion-curve-append.md` 内容 → 追加到 `~/.openclaw/skills/novel-writer/references/emotion-curve.md` 末尾

同时更新 `genre-tropes.md` 的索引，添加该类型的条目。

slim 文件追加到 `~/.openclaw/skills/novel-writer/references/slim/` 下对应文件。

---

## 输出格式详细规范

### `{type}-structure.md` 剧情模板格式

```markdown
# {类型} 剧情模板参考

> 来源：{N}篇{类型}小说分析。大纲阶段使用。

## 核心剧情模板（N种）

### 模板1：{模板名}
**一句话：** {描述}
**适用场景：** {什么情况下用这个模板}
**节拍表：**
1. {节拍1} — 张力 {X}/10
2. {节拍2} — 张力 {X}/10
3. ...

### 模板2：{模板名}
（同上格式）

## 冲突升级链

**{类型}标准冲突链：**
```
表层冲突 → 利益冲突 → 价值观冲突 → 情感归属冲突
  {示例}     {示例}       {示例}         {示例}
```

## 反转技法库

| 反转类型 | 公式 | 出现频率 |
|----------|------|----------|
| {类型1} | {公式} | X/Y篇 |
| {类型2} | {公式} | X/Y篇 |

## 爽点节奏公式

**{类型}标准节奏：**
- 开篇（1-3章）：{爽点类型}，{频率}
- 前期（4-X章）：{爽点类型}，{频率}
- 中期（X-Y章）：{爽点类型}，{频率}
- 后期（Y-Z章）：{爽点类型}，{频率}
```

### `{type}-characters.md` 角色原型格式

```markdown
# {类型} 角色原型参考

> 来源：{N}篇{类型}小说分析。大纲阶段使用。

## 标准角色配置

**{类型}必备角色（N个）：**
1. **{原型名}** — {功能描述}
   - 典型特征：{列表}
   - 常见关系：与其他角色的典型关系模式
   - 语言特征：{句式/用词/口头禅模式}
   - 出现率：X/Y篇

## 关系模式库

| 模式 | 角色A原型 | 角色B原型 | 关系类型 | 弧光 |
|------|----------|----------|----------|------|
| {模式名} | {原型} | {原型} | {类型} | {变化} |

## 角色弧光模板

**{弧光类型}：**
- 起点状态 → 关键转折 → 终点状态
- 典型触发事件：{列表}
```

### `{type}-techniques.md` 写作技法格式

```markdown
# {类型} 写作技法参考

> 来源：{N}篇{类型}小说分析。写作阶段使用。

## 开篇钩子（N种）

**A. {模式名}** — {描述}
- 适用场景：{什么类型的故事}
- 结构：{具体写法}
- 示例效果：{读者感受}

## 对话模式

**{模式名}：** {公式}
- 例："{真实例句}"
- 用法：{什么时候用}

## 爽点实现技法

**{技法名}（压-亮-弹变体）：**
- 压：{怎么压}
- 亮：{怎么亮}
- 弹：{怎么弹}
- 典型场景：{举例}

## 节奏控制

| 阶段 | 对话占比 | 句长 | 事件密度 | 情绪 |
|------|----------|------|----------|------|
| 开篇 | X% | 短/中/长 | 高/中/低 | {情绪} |
| 中段 | X% | ... | ... | ... |
| 高潮 | X% | ... | ... | ... |

## 金句公式

**{公式名}：** {结构} — 例："{例句}"
```

---

## 子 Agent 调用规范

### 嵌入内容

每次 spawn 时，必须将对应 `agents/*.md` 的完整内容嵌入 task 开头。

传入内容包括：
- Agent 角色定义（`agents/xxx.md` 完整内容）
- 小说文本（分块或完整）
- 分析维度要求
- 输出格式规范（references/data-flow-spec.md 中的 JSON schema）

### 上下文精简

- 单篇分析：传完整文本（短篇）或分块文本（长篇）
- 套路提取：传三个分析师的结构化输出，不传原始文本
- 批量合并：传所有单篇的套路提取结果

---

## Tips

- 角色名多个变体时归一化处理
- 区分文本明确陈述 vs 可推断内容
- 网文特有元素（系统/重生/穿越）单独标记
- 分析结果中标注"出现频率"（N/Y篇），频率高的才是真正的套路
