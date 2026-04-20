# 数据流接口规范

> 定义 Analyst → Synthesizer 的 JSON schema，确保端到端数据无损传递。

## 总览

```
小说文本
  ↓
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Structure        │  │ Character        │  │ Style            │
│ Analyst          │  │ Analyst          │  │ Analyst          │
│ → structure.json │  │ → characters.json│  │ → style.json     │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ↓
                     ┌─────────────────┐
                     │ Synthesizer      │
                     │ 读取3个JSON      │
                     │ → 3个 .md 文件   │
                     └─────────────────┘
                              ↓
              {type}-structure.md    (→ plot-design.md 格式)
              {type}-characters.md   (→ character-design.md 格式)
              {type}-techniques.md   (→ writing-techniques.md 格式)
```

---

## Analyst 1: Structure Analyst → `structure.json`

```jsonc
{
  "meta": {
    "novel_name": "小说名",
    "genre": "题材类型",
    "total_chapters": 10,
    "total_words": 5000,
    "structure_type": "重生复仇五幕式"  // 归类后的结构名
  },

  // 剧情模板 — 直接映射到 {type}-structure.md 的"核心剧情模板"
  "templates": [
    {
      "name": "订婚修罗场复仇",
      "one_liner": "重生到订婚宴，当场撕破渣男假面",
      "applicable_scenarios": "重生复仇、先婚后爱",
      "beats": [
        {
          "step": 1,
          "description": "重生回关键节点（订婚宴/婚礼/签约现场）",
          "tension": 6,
          "emotion": "震惊+暗涌的恨意"
        },
        {
          "step": 2,
          "description": "假装顺从，暗中收集证据",
          "tension": 5,
          "emotion": "憋屈+隐忍"
        }
        // ... 更多步骤
      ]
    }
  ],

  // 冲突升级链 — 直接映射到"冲突升级链"章节
  "conflict_chain": [
    {"level": "表层", "description": "订婚宴上的公开羞辱", "example": "原文摘录"},
    {"level": "利益", "description": "家族企业控制权之争", "example": "原文摘录"},
    {"level": "价值观", "description": "忠诚vs利益的价值碰撞", "example": "原文摘录"},
    {"level": "情感", "description": "我算什么——被最亲的人背叛", "example": "原文摘录"}
  ],

  // 爽点分布 — 映射到"爽点节奏公式"
  "pleasure_points": [
    {
      "chapter": 3,
      "type": "小",           // 小/中/大
      "subtype": "打脸",      // 打脸/反转/胜利/揭露/碾压/众人震惊
      "description": "当场揭穿渣男的假面",
      "intensity": 7,
      "technique": "压-亮-弹",
      "example": "原文摘录"
    }
  ],

  // 反转技法 — 映射到"反转技法库"
  "reversals": [
    {
      "chapter": 5,
      "type": "身份反转",      // 身份反转/动机反转/立场反转
      "setup_chapter": 1,
      "description": "女主实际是真正的继承人",
      "formula": "表面弱势 → 身份揭露 → 权力反转"
    }
  ],

  // 情绪弧线 — 用于 Synthesizer 生成节奏公式
  "emotional_arc": [
    {"chapter": 1, "emotion": "憋屈", "intensity": 8, "trend": "压"},
    {"chapter": 2, "emotion": "隐忍", "intensity": 5, "trend": "积累"},
    {"chapter": 3, "emotion": "爽", "intensity": 7, "trend": "弹"}
  ],

  // 章末钩子 — 映射到"章末钩子"章节
  "chapter_hooks": [
    {
      "chapter": 1,
      "hook_type": "悬念钩",   // 悬念钩/反转钩/危机钩/情感钩/选择钩
      "description": "她看到了监控——三年前那场火，不是意外"
    }
  ]
}
```

---

## Analyst 2: Character Analyst → `characters.json`

```jsonc
{
  "meta": {
    "novel_name": "小说名",
    "genre": "题材类型"
  },

  // 角色配置 — 映射到"标准角色配置"
  "cast_config": {
    "protagonist_count": 1,
    "protagonist_gender": "女",
    "required_archetypes": [
      {
        "archetype": "重生女主",
        "function": "承载读者代入，执行复仇计划",
        "frequency": "10/10篇重生文"
      },
      {
        "archetype": "渣男未婚夫",
        "function": "制造冲突，提供打脸对象",
        "frequency": "9/10篇"
      }
    ],
    "optional_archetypes": [
      {
        "archetype": "忠犬男二",
        "function": "提供情感替代选项，对比渣男",
        "frequency": "7/10篇"
      }
    ],
    "total_range": "5-8人"
  },

  // 角色原型 — 映射到"角色原型"和"角色语言特征模板"
  "character_archetypes": [
    {
      "archetype_name": "重生复仇女主",
      "traits": ["隐忍", "果决", "擅长伪装"],
      "typical_arc": "前世被背叛致死 → 重生觉醒 → 隐忍布局 → 逐个击破 → 终极复仇",
      "motivation": "讨回公道 + 保护真正关心的人",
      "weakness": "对真情的渴望可能被利用",
      "language_profile": {
        "sentence_pattern": "短句为主，陈述句多，偶用反问",
        "vocabulary": "冷静克制，关键时刻用狠话",
        "catchphrase_patterns": ["你以为呢？", "等着瞧"],
        "example_lines": [
          "上辈子我信了你。这辈子，我一个字都不会信。",
          "林晚，你想要的，我都会亲手毁掉。"
        ]
      }
    },
    {
      "archetype_name": "渣男未婚夫",
      "traits": ["虚伪", "贪婪", "表面深情"],
      "typical_arc": "假意深情 → 逐渐暴露 → 真相揭露 → 身败名裂",
      "language_profile": {
        "sentence_pattern": "温柔长句（假面时期）→ 恼羞成短句（暴露后）",
        "vocabulary": "前期甜言蜜语，后期推卸责任",
        "example_lines": [
          "念念，我会一辈子对你好的。",
          "你疯了！你知道你在说什么吗？"
        ]
      }
    }
    // ... 更多原型
  ],

  // 关系模式 — 映射到"关系模式库"
  "relationship_patterns": [
    {
      "pattern_name": "渣男+女主+白莲花三角",
      "characters": ["重生女主", "渣男未婚夫", "白莲花女配"],
      "typical_arc": "女主信任渣男 → 发现白莲花插足 → 揭露真相 → 两人身败名裂",
      "trigger_event": "女主重生/发现证据",
      "frequency": "8/10篇重生文"
    },
    {
      "pattern_name": "女主+忠犬守护",
      "characters": ["重生女主", "忠犬男二/暗恋者"],
      "typical_arc": "默默守护 → 女主注意到 → 逐步靠近 → 终成眷属",
      "frequency": "7/10篇"
    }
  ],

  // 角色弧光模板 — 映射到"角色弧光模板"
  "arc_templates": [
    {
      "arc_type": "复仇觉醒型",
      "start": "天真/被蒙蔽/牺牲型人格",
      "trigger": "死亡/背叛/真相揭露",
      "transition": "觉醒→冷酷→找到底线",
      "end": "强大但不失去人性"
    }
  ]
}
```

---

## Analyst 3: Style Analyst → `style.json`

```jsonc
{
  "meta": {
    "novel_name": "小说名",
    "genre": "题材类型"
  },

  // 开篇钩子 — 映射到"开篇钩子"
  "opening_hook": {
    "type": "死亡回溯",         // 匹配 writing-techniques.md A-J
    "structure": "先写死亡场景（被烧死）→ 重生回三年前（订婚宴）→ 形成强烈对比",
    "effect": "读者立刻知道前世结局，带着上帝视角看女主复仇",
    "example": "火光吞噬一切的那一刻..."
  },

  // 对话技法 — 映射到"对话模式库"
  "dialogue_techniques": [
    {
      "name": "表面温柔实际狠",
      "formula": "温柔语气 + 狠毒内容",
      "example": "林晚，你想要的，我都会亲手毁掉。——笑着说",
      "usage": "女主反击白莲花、反派式威胁",
      "frequency": "5次"
    },
    {
      "name": "信息差质问",
      "formula": "主角明知答案，故意问对方 → 对方撒谎 → 读者看戏",
      "example": "\"子墨，你昨晚去哪了？\"（实际已跟踪）",
      "usage": "审讯/试探/当众揭穿前的铺垫",
      "frequency": "3次"
    }
  ],

  // 爽点技法 — 映射到"爽点实现技法"
  "pleasure_techniques": [
    {
      "name": "当众打脸三连击",
      "structure": {
        "press": "反派当众羞辱女主（'你配不上子墨'）",
        "show": "女主亮出证据/身份/实力",
        "pop": "全场震惊 + 反派面如死灰 + 渣男求饶"
      },
      "example_chapter": 3,
      "intensity": 8
    },
    {
      "name": "递进式身份揭露",
      "structure": {
        "press": "众人以为女主是废物/弃子",
        "show": "第一层揭露（商业能力）→ 第二层（真实身份）→ 第三层（幕后大佬）",
        "pop": "层层递进，每层震惊一波人"
      },
      "example_chapter": 7,
      "intensity": 9
    }
  ],

  // 节奏数据 — 映射到"节奏控制参考"
  "rhythm_profile": {
    "avg_dialogue_ratio": "35%",
    "avg_sentence_length": 14,
    "tension_pattern": "开篇高压→中段积累→后段爆发",
    "chapter_transition_style": "悬念留白为主，偶用时间跳跃",
    "chapter_rhythm": [
      {"phase": "开篇（1-3章）", "dialogue_ratio": "25%", "sentence_length": 12, "density": "高", "mood": "憋屈+悬念"},
      {"phase": "中段（4-7章）", "dialogue_ratio": "35%", "sentence_length": 15, "density": "中", "mood": "积累+小爽"},
      {"phase": "高潮（8-10章）", "dialogue_ratio": "40%", "sentence_length": 10, "density": "高", "mood": "爆发+爽"}
    ]
  },

  // 金句 — 映射到"金句公式"
  "golden_lines": [
    {
      "formula": "对比式",
      "structure": "上辈子X → 这辈子Y",
      "example": "上辈子我为你挡刀。这辈子，你挡在我面前，我也不会眨眼。",
      "usage": "女主态度转变的关键时刻"
    }
  ],

  // 章末钩子统计
  "hook_statistics": {
    "most_used_type": "悬念钩",
    "types_used": {
      "悬念钩": 5,
      "反转钩": 3,
      "危机钩": 2
    }
  }
}
```

---

## Synthesizer 输入模板

编排器拼装 Synthesizer 的 task 时，使用以下模板：

```
## 输入数据

### Structure Analyst 输出
{structure.json 完整内容}

### Character Analyst 输出
{characters.json 完整内容}

### Style Analyst 输出
{style.json 完整内容}

## 任务

根据以上三个 JSON，生成 3 个 Writer-ready reference 文件：
1. `{genre}-structure.md` — 从 structure.json 的 templates/conflict_chain/pleasure_points/reversals/emotional_arc/chapter_hooks 生成
2. `{genre}-characters.md` — 从 characters.json 的 cast_config/character_archetypes/relationship_patterns/arc_templates 生成
3. `{genre}-techniques.md` — 从 style.json 的 opening_hook/dialogue_techniques/pleasure_techniques/rhythm_profile/golden_lines 生成

严格按 SKILL.md 中定义的 Writer-ready 格式输出。每个技法必须附原文例句。
```

---

## 字段映射速查表

| Analyst JSON 字段 | Synthesizer 输出文件 | Writer-ready 章节 |
|-------------------|---------------------|-------------------|
| `structure.templates` | `{genre}-structure.md` | 核心剧情模板 |
| `structure.conflict_chain` | `{genre}-structure.md` | 冲突升级链 |
| `structure.pleasure_points` | `{genre}-structure.md` | 爽点节奏公式 |
| `structure.reversals` | `{genre}-structure.md` | 反转技法库 |
| `structure.chapter_hooks` | `{genre}-structure.md` | 章末钩子技法 |
| `characters.cast_config` | `{genre}-characters.md` | 标准角色配置 |
| `characters.character_archetypes` | `{genre}-characters.md` | 角色原型 + 语言特征 |
| `characters.relationship_patterns` | `{genre}-characters.md` | 关系模式库 |
| `characters.arc_templates` | `{genre}-characters.md` | 角色弧光模板 |
| `style.opening_hook` | `{genre}-techniques.md` | 开篇钩子 |
| `style.dialogue_techniques` | `{genre}-techniques.md` | 对话模式库 |
| `style.pleasure_techniques` | `{genre}-techniques.md` | 爽点实现技法 |
| `style.rhythm_profile` | `{genre}-techniques.md` | 节奏控制参考 |
| `style.golden_lines` | `{genre}-techniques.md` | 金句公式 |
