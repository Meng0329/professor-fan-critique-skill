# professor-fan-critique-skill — Eval Spec

## Binary Checks

| ID | Description | Check |
|----|------------|-------|
| check-dimension-count | SKILL.md defines exactly 9 evaluation dimensions | `grep -c "^### [0-9]\." SKILL.md` = 9 |
| check-red-flags | SKILL.md includes Red Flags section with 8+ items | `grep -c "^\- ❌" SKILL.md` >= 8 |
| check-risk-levels | SKILL.md defines RED/YELLOW/GREEN risk levels | `grep -c "RED\|YELLOW\|GREEN" SKILL.md` >= 3 |
| check-frontmatter | SKILL.md has valid YAML frontmatter | `grep -c "^name:\|^description:" SKILL.md` = 2 |
| check-output-format | SKILL.md specifies structured output format | `grep -c "樊老师锐评报告" SKILL.md` >= 1 |
| check-trigger-section | SKILL.md has Trigger section | `grep -c "## Trigger" SKILL.md` >= 1 |

## Golden Cases

### Case 1: Thesis Chapter Review

**Input**: A thesis chapter with overly broad title, missing literature comparison, and inflated innovation claims.

**Expected behavior**: The skill should flag at minimum:
- Scope focus as RED (title too broad)
- Literature baseline as RED (missing comparable systems)
- Innovation authenticity as RED (unsubstantiated "first-ever" claims)
- Review risk as YELLOW or RED (no limitations section)

### Case 2: PPT Slide Deck Review

**Input**: A defense presentation with no data analysis, no authoritative database mention, and no validation plan.

**Expected behavior**: The skill should flag at minimum:
- Data depth as RED (no analysis beyond counts)
- Authority integration as RED (no database grounding)
- Feasibility verification as RED (no validation plan)

### Case 3: Innovation Paragraph Review

**Input**: A paragraph claiming "first-ever conditional knowledge graph for rice molecular breeding" without prior art comparison.

**Expected behavior**: The skill should flag at minimum:
- Innovation authenticity as RED or YELLOW (unsubstantiated "first-ever")
- Literature baseline as YELLOW (missing prior art discussion)
