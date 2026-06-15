# professor-fan-critique-skill — 樊老师锐评

**九维学术评审 Skill** — 基于樊老师两次组会锐评提炼的九维评审框架，用于自检开题报告、学位论文、PPT 和学术提案。

## 关于樊老师

樊老师是来自中国农业科学院的研究员/教授，长期从事农业信息与育种领域的研究与评审工作。本 Skill 的九维评审框架源自樊老师在两次组会（第一次组会 + 开题答辩）中对开题报告和 PPT 的锐评。

樊老师的评审风格以 **问题驱动、证据主义、底线思维** 著称：

- **问题驱动**：始终追问"你解决了什么问题？"，而非"你用了什么技术？"
- **证据主义**：每个 claim 都必须有出处，每个创新都必须查证 prior art
- **底线思维**：预判审稿人会从哪里攻击，提前堵漏
- **领域嵌入**：不具备领域常识就无法做有效评审，不能外行评内行
- **名实相符**：题目和内容必须匹配，不能"题大实小"
- **量→质叙事转换**：不是做了多少工作，而是带来了什么知识转变

核心追问可概括为九句话：

> 你题目写这么大，做不完怎么办？国内外都在做，你凭什么说你是新的？你说"首次"，你敢确定吗？你报了 20 万篇，然后呢？你懂水稻育种吗？光有文献够吗？权威数据库呢？同一个东西不同数据库叫法不一样，你怎么办？你说能辅助决策，怎么证明？审稿专家会怎么怼你？

## 安装

### OpenCode (project-level)

```bash
# 项目已包含此 skill，直接使用
# 在对话中输入 /professor-fan-critique-skill 激活
```

### Claude Code

```bash
cp -R professor-fan-critique-skill ~/.claude/skills/professor-fan-critique-skill
```

### GitHub Copilot

```bash
cp -R professor-fan-critique-skill ~/.copilot/skills/professor-fan-critique-skill
```

### Cursor (project-level)

```bash
cp -R professor-fan-critique-skill .cursor/skills/professor-fan-critique-skill
```

### 一键安装

```bash
cd professor-fan-critique-skill
./install.sh              # 自动检测并安装
./install.sh --all        # 安装到所有检测到的平台
```

## 使用

在你的 AI 工具中：

```
/professor-fan-critique-skill [粘贴论文章节]
/professor-fan-critique-skill 樊老师帮我看看这份开题报告的创新点
/professor-fan-critique-skill Critique my defense slides — what will experts attack?
```

## 九维评审框架

| # | 维度 | 核心追问 |
|---|------|---------|
| 1 | 题目聚焦度 | 你题目写这么大，做不完怎么办？ |
| 2 | 文献基础对比 | 国内外都在做，你凭什么说你是新的？ |
| 3 | 创新点真实性 | 你说"首次"，你敢确定吗？ |
| 4 | 数据深度分析 | 你报了20万篇，然后呢？ |
| 5 | 领域知识深度 | 你懂水稻育种吗？ |
| 6 | 权威知识库整合 | 光有文献够吗？权威数据库呢？ |
| 7 | 命名体系与对齐 | 同一个东西不同数据库叫法不一样，你怎么办？ |
| 8 | 可行性验证 | 你说能辅助决策，怎么证明？ |
| 9 | 送审风险预判 | 审稿专家会怎么怼你？ |

## 目录结构

```
professor-fan-critique-skill/
├── SKILL.md                          # 主 skill 定义
├── AGENTS.md                         # 跨工具兼容文件
├── scripts/
│   ├── critique_pipeline.py          # 评审流水线
│   └── run_evals.py                  # Eval runner
├── references/
│   └── nine-dimensions.md            # 九维详细参考
├── assets/
│   └── checklist_template.md         # 自检清单模板
├── evals/
│   └── professor-fan-critique.eval.md # Eval spec
├── install.sh                        # 跨平台安装器
└── README.md                         # 本文件
```

## License

MIT
