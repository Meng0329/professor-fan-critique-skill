# professor-fan-critique-skill — 樊老师锐评

A rigorous academic review skill that evaluates research proposals, thesis chapters, presentation slides, and manuscripts against nine evaluation dimensions: scope focus, literature baseline, innovation authenticity, data depth, domain knowledge, authority integration, naming & alignment, feasibility verification, and review risk anticipation.

## When This Activates

The user invokes `/professor-fan-critique-skill` or asks for:
- Academic review / critique of a proposal or paper
- Checking thesis or dissertation chapters before submission
- Verifying innovation claims or novelty statements
- Preparing for thesis defense or proposal defense
- Reviewing presentation slides for expert audience
- "樊老师帮我看看" / "锐评一下" / "帮我审审"

## How to Use

1. Read SKILL.md for the full nine-dimension evaluation framework
2. Apply the scanning workflow to provided material
3. Produce a structured report with risk levels per dimension
4. Identify the three most critical issues

## Files

- `SKILL.md` — Full evaluation framework and workflow
- `scripts/critique_pipeline.py` — Automated critique runner
- `references/nine-dimensions.md` — Detailed dimension reference with examples
- `assets/checklist_template.md` — Reusable checklist template
- `evals/professor-fan-critique.eval.md` — Eval spec
