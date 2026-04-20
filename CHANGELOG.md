# 更新日志

## [1.0.0] - 2026-04-21

### 初始版本

#### 核心架构
- 多 Agent 协作设计：Structure Analyst / Character Analyst / Style Analyst / Synthesizer
- 三种工作模式：
  - **Mode A**：单篇深度拆解（分析报告，人读）
  - **Mode B**：单篇套路提取（从分析中抽象 Writer-ready 模式）
  - **Mode C**：批量套路库（同类型多篇合并，生成类型参考库）

#### 数据流接口
- `references/data-flow-spec.md` — Analyst → Synthesizer 的 JSON schema 规范
  - Structure Analyst → `structure.json`（模板/冲突链/爽点/反转/情绪弧线/钩子）
  - Character Analyst → `characters.json`（角色配置/原型/关系模式/弧光模板）
  - Style Analyst → `style.json`（开篇钩子/对话技法/爽点技法/节奏/金句）
  - Synthesizer → 3 个 Writer-ready `.md` 文件
- 字段映射速查表：15 个 JSON 字段 → 3 个 Writer-ready 章节的精确对应

#### Agent 定义
- `agents/structure-analyst.md` — 剧情结构分析（模板/冲突/爽点/反转）
- `agents/character-analyst.md` — 角色关系分析（原型/配置/关系模式）
- `agents/style-analyst.md` — 文风技法分析（钩子/对话/节奏/金句）
- `agents/synthesizer.md` — 合成器（JSON → novel-writer 格式 Markdown）

#### 工具
- `scripts/chunk_novel.py` — 长文本分块脚本（按章节/字数自动拆分）
- `references/analysis-framework.md` — 分析框架参考（三幕/英雄之旅/网文结构）
- `references/mermaid-templates.md` — 关系图/时间线模板

#### 测试数据
- `test-data/novel_01-02` — 自写测试篇（重生文 + 悬疑文）
- `test-data/novel_03-04` — 用户提供篇（重生复仇 37KB + 甜宠 50KB）

#### 首批分析产出
- 🏷️ 重生复仇套路库 — 从 2 篇重生复仇小说提取
  - 剧情模板：订婚宴修罗场复仇（7步节拍表）
  - 角色原型：重生女主/渣男/白莲花/忠犬/恶毒继母
  - 写作技法：当众打脸/信息差碾压/递进真相揭露
- 🏷️ 甜宠套路库 — 从 1 篇甜宠小说提取
  - 剧情模板：合约恋爱变真爱（6步节拍表）
  - 角色原型：甜宠女主/暗恋型男主
  - 写作技法：反差萌暴击/暗恋暴击/细节撒糖
- 产出已同步至 novel-writer-skill 的 references/ 目录

#### 与 novel-writer 的协作关系
```
novel-analyzer（读）               novel-writer（写）
分析小说 → 提取套路 → Writer-ready .md → 合并进 references/
```
