#!/usr/bin/env python3
"""
Professor Fan Critique Pipeline — nine-dimension academic review automation.

Usage:
    python3 critique_pipeline.py --input thesis_chapter.md --output report.md
    python3 critique_pipeline.py --input slides.pptx --json
    python3 critique_pipeline.py --checklist                          # Print checklist and exit
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Optional


# ──────────────────────────────────────────────
# Core principles (from first group meeting)
# ──────────────────────────────────────────────

CORE_PRINCIPLES = [
    {
        "id": "P1",
        "name": "problem_driven",
        "label": "问题驱动（非技术驱动）",
        "question": "你解决了什么问题？不是用了什么技术？",
        "checks": [
            "开篇第一段在讲问题而非技术栈",
            "去掉所有技术名词后研究框架仍然成立",
            "技术方案被放在问题陈述之后",
        ],
    },
    {
        "id": "P2",
        "name": "quantity_to_quality",
        "label": "量→质叙事转换",
        "question": "你带来了什么知识转变？",
        "checks": [
            "创新点落脚在知识形态的转变而非数据规模",
            "不是用'我处理了多少数据'来论证价值",
            "能清晰回答'数据变成了什么知识'",
        ],
    },
    {
        "id": "P3",
        "name": "closed_loop",
        "label": "抽取→质检→应用闭环",
        "question": "你的流程完整吗？",
        "checks": [
            "覆盖抽取、质检、应用三个环节",
            "每个环节之间有明确的接口和验证",
            "没有缺少任何一个环节",
        ],
    },
    {
        "id": "P4",
        "name": "problem_data_match",
        "label": "问题→数据对应",
        "question": "你说的问题在你的数据里能找到吗？",
        "checks": [
            "每个研究问题都有对应的数据源",
            "数据源的局限性与问题的重要性匹配",
            "没有'问题很好但数据支撑不了'的情况",
        ],
    },
    {
        "id": "P5",
        "name": "explainability",
        "label": "可解释性与专家判断",
        "question": "你的方法专家看得懂吗？",
        "checks": [
            "方法每一步都能追溯到输入",
            "有专家介入/人机协同的接口",
            "不是端到端黑箱",
        ],
    },
]

# ──────────────────────────────────────────────
# Nine evaluation dimensions
# ──────────────────────────────────────────────

DIMENSIONS = [
    {
        "id": 1,
        "name": "scope_focus",
        "label": "题目聚焦度",
        "question": "你题目写这么大，做不完怎么办？",
        "checks": [
            "题目范围是否过于宽泛（如'面向分子育种'→ 应聚焦到具体抗性）",
            "领域专家能否一眼看出具体解决了什么问题",
            "题目承诺的内容与实际产出是否匹配",
            "是否存在'题目写战略报告，实际做系统'的落差",
        ],
        "red_flag": "题目包含'面向XX领域'而非聚焦具体问题",
    },
    {
        "id": 2,
        "name": "literature_baseline",
        "label": "文献基础对比",
        "question": "国内外都在做，你凭什么说你是新的？",
        "checks": [
            "是否系统梳理了同类工作（RiceScientist, CDLM, 龙虾助手等）",
            "是否有对比表格（方法/数据规模/技术路线/评估方式）",
            "是否说明别人做了什么、做到了什么程度、还有什么没做好",
            "核心claim是否有顶刊文献背书",
            "是否讨论了与神经符号方法（neuro-symbolic）的关系",
            "是否明确了学科圈定（覆盖了哪些社区、排除了哪些）",
        ],
        "red_flag": "综述不提已有系统，或只说'现有方法存在不足'但不具体",
    },
    {
        "id": 3,
        "name": "innovation_authenticity",
        "label": "创新点真实性",
        "question": "你说'首次'，你敢确定吗？",
        "checks": [
            "每个创新点是否经过了'有没有人做过'的严格检索",
            "'首次'、'首个'等绝对化表述是否有充分证据",
            "如果已有类似工作，差异点是否足够显著（而非多一个维度）",
            "创新是问题层面的突破还是技术层面的组装",
        ],
        "red_flag": "声称'首次将XX用于XX'但已有大量类似研究",
    },
    {
        "id": 4,
        "name": "data_depth",
        "label": "数据深度分析",
        "question": "你报了20万篇，然后呢？",
        "checks": [
            "数据量之外是否有分类分析（品种分布、年代分布、质量分布）",
            "是否对初始数据做了基本统计和可视化",
            "数据质量评估是否到位（预印本占比、来源可信度）",
            "数据的局限性是否明确说明",
            "是否承认了真值标定困难（私有材料不可获取）",
            "是否完成了从'量'到'质'的叙事转换",
        ],
        "red_flag": "只说'我采集了XX篇'但不分析数据长什么样",
    },
    {
        "id": 5,
        "name": "domain_knowledge",
        "label": "领域知识深度",
        "question": "你懂水稻育种吗？",
        "checks": [
            "是否展示了基本领域理解（品种分类、系谱关系、育种目标）",
            "是否考虑了品种差异对知识迁移的影响",
            "系谱信息（父本/母本/传代）是否在知识体系中体现",
            "基因→表型核心链条是否清晰（每个基因可追溯到可测量表型）",
            "是否存在'一个基因通用所有品种'的外行假设",
            "是否考虑了时空对齐问题（同一基因在不同环境/阶段的表现差异）",
        ],
        "red_flag": "把不同品种的文献知识混为一谈，不考虑品种背景",
    },
    {
        "id": 6,
        "name": "authority_integration",
        "label": "权威知识库整合",
        "question": "光有文献够吗？权威数据库呢？",
        "checks": [
            "是否整合了权威数据库（NCBI, IRRI, UniProt, KEGG, RiceVarMap）",
            "是否区分了'文献中的知识'和'数据库中的金标准'",
            "推理和决策是否以权威库作为ground truth锚点",
            "本体的定位是否正确——约束术语，不是推理引擎",
        ],
        "red_flag": "只依赖文献抽取的知识做推理，无权威数据库校验基准",
    },
    {
        "id": 7,
        "name": "naming_alignment",
        "label": "命名体系与对齐",
        "question": "同一个东西不同数据库叫法不一样，你怎么办？",
        "checks": [
            "是否意识到不同数据库使用不同的ID体系",
            "是否有明确的ID对齐/实体对齐方案",
            "是否评估了对齐工作的难度和工作量",
            "品种名/基因名的异名（synonym）是否已考虑",
            "是否考虑了时空对齐问题（同一实体在不同时间/地点的标注差异）",
            "是否识别了多源语义冲突（不同社区对同一概念的不同定义）",
        ],
        "red_flag": "假设所有数据库使用统一命名体系，或完全忽略对齐问题",
    },
    {
        "id": 8,
        "name": "feasibility_verification",
        "label": "可行性验证",
        "question": "你说能辅助决策，怎么证明？",
        "checks": [
            "是否有端到端验证方案（如复现已发表论文的结果）",
            "不请领域专家能否独立验证系统有效性",
            "是否有明确的验证指标和成功标准",
            "是否有'先小规模验证再大规模推进'的节奏",
            "干实验vs湿实验的鸿沟是否已考虑",
        ],
        "red_flag": "只有系统设计，没有任何验证计划或预实验",
    },
    {
        "id": 9,
        "name": "review_risk",
        "label": "送审风险预判",
        "question": "审稿专家会怎么怼你？",
        "checks": [
            "最可能被攻击的三个薄弱点是什么",
            "这些薄弱点是否有预先准备好的回应",
            "是否存在'题目过大、落地不足、名实不符'的结构性风险",
            "方法的局限性是否坦诚说明而非藏着掖着",
            "是否有'给自己挖坑'的表述",
            "学科圈定是否明确（in scope vs out of scope）",
            "每个研究问题是否都有对应的数据源支撑",
            "干实验vs湿实验的鸿沟是否被承认",
            "系统定位是否现实（'文献知识挖掘' vs '分子育种平台'）",
        ],
        "red_flag": "全文无局限性讨论，所有表述都过于自信",
    },
]


@dataclass
class CritiqueResult:
    """Result of critiquing one dimension."""
    dimension_id: int
    dimension_name: str
    dimension_label: str
    risk: str  # RED / YELLOW / GREEN
    findings: list[str] = field(default_factory=list)
    suggestion: Optional[str] = None


def run_critique() -> list[CritiqueResult]:
    """
    Interactive critique: the user answers yes/no for each check,
    then receives a structured report.

    In agent mode, this is called with pre-analyzed input.
    For CLI usage, it prompts interactively.
    """
    results = []
    print("=" * 60)
    print("  樊老师锐评 — 核心原则 + 九维评审扫描")
    print("=" * 60)

    # Core principles check (from first group meeting)
    print(f"\n{'#' * 60}")
    print("  【核心原则检查】— 来自第一次组会")
    print(f"{'#' * 60}")
    principle_failures = 0
    for p in CORE_PRINCIPLES:
        print(f"\n  [{p['id']}] {p['label']}")
        print(f"  追问：{p['question']}")
        for check in p["checks"]:
            answer = input(f"  ✔ 是否满足？({check}) [y/n]: ").strip().lower()
            if answer == "n":
                principle_failures += 1
                print(f"    ⚠️ 未满足: {check}")

    if principle_failures >= 3:
        print(f"\n  ⚠️  ⚠️  {principle_failures}项核心原则未满足——建议重新审视研究框架")

    print(f"\n{'#' * 60}")
    print("  【九维评审扫描】")
    print(f"{'#' * 60}")

    for dim in DIMENSIONS:
        print(f"\n{'─' * 60}")
        print(f"  [{dim['id']}] {dim['label']}")
        print(f"  核心追问：{dim['question']}")
        print(f"{'─' * 60}")

        findings = []
        red_count = 0
        yellow_count = 0

        for check in dim["checks"]:
            answer = input(f"  ✔ 是否满足？({check}) [y/n]: ").strip().lower()
            if answer == "n":
                findings.append(f"未满足: {check}")
                yellow_count += 1

        # Determine risk level
        if dim["red_flag"] and any(
            rf in str(findings) for rf in [dim["red_flag"]]
        ):
            risk = "RED"
        elif yellow_count >= 2:
            risk = "RED" if yellow_count >= 3 else "YELLOW"
        elif yellow_count >= 1:
            risk = "YELLOW"
        else:
            risk = "GREEN"

        results.append(
            CritiqueResult(
                dimension_id=dim["id"],
                dimension_name=dim["name"],
                dimension_label=dim["label"],
                risk=risk,
                findings=findings,
            )
        )

    return results


def generate_report(results: list[CritiqueResult]) -> str:
    """Generate a markdown report from critique results."""
    reds = [r for r in results if r.risk == "RED"]
    yellows = [r for r in results if r.risk == "YELLOW"]

    if reds:
        overall = "REJECT — 存在致命缺陷，建议修改后重新送审"
    elif len(yellows) >= 3:
        overall = "CONDITIONAL — 存在明显不足，需要重大修改"
    elif yellows:
        overall = "CONDITIONAL — 存在若干问题，建议修改"
    else:
        overall = "PASS — 无明显问题"

    lines = [
        "## 樊老师锐评报告",
        "",
        f"### 总体风险: {overall}",
        "",
        "### 九维扫描结果",
        "| 维度 | 风险 | 关键发现 |",
        "|------|------|---------|",
    ]

    for r in results:
        findings_str = "; ".join(r.findings[:2]) if r.findings else "无明显问题"
        emoji = {"RED": "🔴", "YELLOW": "🟡", "GREEN": "🟢"}
        lines.append(f"| {r.dimension_id}. {r.dimension_label} | {emoji[r.risk]} {r.risk} | {findings_str} |")

    if reds:
        lines.extend([
            "",
            "### 三大致命问题 (RED)",
        ])
        for i, r in enumerate(reds[:3], 1):
            lines.append(f"{i}. **{r.dimension_label}**: {'; '.join(r.findings)}")

    lines.extend([
        "",
        "---",
        "*Generated by professor-fan-critique-skill*",
    ])

    return "\n".join(lines)


def print_checklist():
    """Print the evaluation checklist for manual use."""
    print("# 樊老师九维评审自检清单\n")
    for dim in DIMENSIONS:
        print(f"## {dim['id']}. {dim['label']}")
        print(f"**核心追问**: {dim['question']}\n")
        for check in dim["checks"]:
            print(f"- [ ] {check}")
        print(f"\n*典型红线: {dim['red_flag']}*\n")


def main():
    parser = argparse.ArgumentParser(
        description="Professor Fan's nine-dimension academic critique"
    )
    parser.add_argument("--input", help="Input file (thesis/proposal/slides)")
    parser.add_argument("--output", help="Output report file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--checklist", action="store_true", help="Print checklist and exit"
    )
    args = parser.parse_args()

    if args.checklist:
        print_checklist()
        sys.exit(0)

    # Interactive mode
    results = run_critique()
    report = generate_report(results)

    if args.json:
        print(json.dumps([r.__dict__ for r in results], ensure_ascii=False, indent=2))
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
