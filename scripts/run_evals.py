#!/usr/bin/env python3
"""
Eval runner for professor-fan-critique-skill.

Usage:
    python3 run_evals.py              # Run all evals
    python3 run_evals.py --validate   # Validate eval spec
    python3 run_evals.py --rollout    # Execute skill on golden inputs
"""

import argparse
import json
import sys
from pathlib import Path


EVALS = [
    {
        "id": "check-dimension-count",
        "description": "SKILL.md defines exactly 9 evaluation dimensions",
        "command": 'grep -c "^### [0-9]\." SKILL.md',
        "expect": "9",
    },
    {
        "id": "check-red-flags",
        "description": "SKILL.md includes Red Flags section with at least 8 items",
        "command": 'grep -c "^\- ❌" SKILL.md',
        "expect_min": "8",
    },
    {
        "id": "check-risk-levels",
        "description": "SKILL.md defines RED/YELLOW/GREEN risk levels",
        "command": 'grep -c "RED\|YELLOW\|GREEN" SKILL.md',
        "expect_min": "3",
    },
    {
        "id": "check-frontmatter",
        "description": "SKILL.md has valid YAML frontmatter with name and description",
        "command": 'grep -c "^name:\|^description:" SKILL.md',
        "expect": "2",
    },
    {
        "id": "check-output-format",
        "description": "SKILL.md specifies structured output format (markdown report)",
        "command": 'grep -c "樊老师锐评报告" SKILL.md',
        "expect": "1",
    },
    {
        "id": "check-trigger-section",
        "description": "SKILL.md has Trigger section with invocation examples",
        "command": 'grep -c "## Trigger" SKILL.md',
        "expect": "1",
    },
]


def validate():
    """Validate eval spec structure."""
    print("Validating eval spec...")
    for ev in EVALS:
        required = ["id", "description", "command", "expect"]
        missing = [k for k in required if k not in ev]
        if missing:
            print(f"  FAIL: {ev.get('id', 'unknown')} missing: {missing}")
            return False
        print(f"  OK: {ev['id']}")
    print("VALID")
    return True


def run_evals(skill_dir: str = "."):
    """Run all binary checks."""
    import subprocess

    print("Running evals...\n")
    passed = 0
    failed = 0
    results = []

    for ev in EVALS:
        result = subprocess.run(
            ev["command"],
            shell=True,
            capture_output=True,
            text=True,
            cwd=skill_dir,
        )
        output = result.stdout.strip()

        if "expect" in ev:
            ok = output == ev["expect"]
        elif "expect_min" in ev:
            try:
                ok = int(output) >= int(ev["expect_min"])
            except ValueError:
                ok = False
        else:
            ok = result.returncode == 0

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        print(f"  [{status}] {ev['id']}: {ev['description']}")
        if not ok:
            print(f"          Expected: {ev.get('expect', ev.get('expect_min', 'truthy'))}, Got: {output}")
        results.append({"id": ev["id"], "status": status, "output": output})

    print(f"\nResults: {passed} passed, {failed} failed out of {len(EVALS)}")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="professor-fan-critique evals")
    parser.add_argument("--validate", action="store_true", help="Validate eval spec")
    parser.add_argument("--rollout", action="store_true", help="Run skill on golden inputs")
    parser.add_argument("--promote", action="store_true", help="Promote baseline (placeholder)")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Skill directory")
    args = parser.parse_args()

    if args.validate:
        success = validate()
    elif args.rollout:
        print("Rollout mode: executing skill on golden cases...")
        success = run_evals(args.skill_dir)
    else:
        success = run_evals(args.skill_dir)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
