#!/usr/bin/env python3
"""grade-golden.py — deterministic golden-case grader (stdlib only).

RED->GREEN eval, deterministic half. Grades a recorded agent output against the
pattern checks in evals/golden/<skill>/cases.json (artifact checks + rubric
patterns — no LLM-as-judge). This is the grading stage the full RED->GREEN
loop feeds: RED output (no-skill baseline) should FAIL the checks; GREEN output
(with-skill, e.g. the case's reference_output) should PASS.

Usage:
    python3 scripts/grade-golden.py                    # grade reference_output (GREEN demo)
    python3 scripts/grade-golden.py --red              # degraded-output demo (RED detection)
    python3 scripts/grade-golden.py --json             # machine-readable
    python3 scripts/grade-golden.py --output-dir DIR   # grade real recorded outputs:
                                                       #   DIR/<skill>/<case-id>.txt overrides reference

Exit codes: 0 = all graded outputs pass their checks, 1 = violations (use to gate).

Honesty note: this validates the *grading* stage only. Real agent A/B runs
(no-skill vs with-skill transcripts) require an agent runtime + model API and
are executed separately; until then any behavioral-lift claim is a hypothesis.
"""

import argparse
import glob
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
GOLDEN = os.path.join(REPO, "evals", "golden")


def _matches(patterns, text):
    lowered = text.lower()
    return any(p.lower() in lowered for p in patterns)


def grade_case(skill, case, recorded_output, output_dir=None):
    """Grade one case. Returns (case_id, ok, details)."""
    checks = case.get("checks", [])
    results = []
    for chk in checks:
        ok = _matches(chk.get("patterns", []), recorded_output)
        results.append({"label": chk["label"], "patterns": chk.get("patterns", []), "pass": ok})
    ok = all(r["pass"] for r in results)
    return {"skill": skill, "case": case["id"], "ok": ok, "checks": results}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--red", action="store_true",
                    help="demo RED detection: grade an empty/no-skill output (expect FAILs)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--output-dir", default=None,
                    help="dir with real recorded outputs: <dir>/<skill>/<case-id>.txt")
    args = ap.parse_args()

    results = []
    for cases_path in sorted(glob.glob(os.path.join(GOLDEN, "*", "cases.json"))):
        skill = os.path.basename(os.path.dirname(cases_path))
        data = json.load(open(cases_path, encoding="utf-8"))
        for case in data.get("cases", []):
            recorded = None
            if args.output_dir:
                cand = os.path.join(args.output_dir, skill, case["id"] + ".txt")
                if os.path.exists(cand):
                    recorded = open(cand, encoding="utf-8").read()
            if recorded is None:
                recorded = "" if args.red else case.get("reference_output", "")
            results.append(grade_case(skill, case, recorded))

    passed = [r for r in results if r["ok"]]
    failed = [r for r in results if not r["ok"]]

    if args.json:
        print(json.dumps({
            "mode": "red_demo" if args.red else ("recorded" if args.output_dir else "green_reference"),
            "graded": len(results),
            "pass": len(passed),
            "fail": len(failed),
            "results": results,
        }, indent=2))
    else:
        mode = "RED demo (empty output)" if args.red else (
            "recorded outputs" if args.output_dir else "GREEN (reference_output)")
        print(f"golden grader — {mode}")
        for r in results:
            status = "PASS" if r["ok"] else "FAIL"
            print(f"  [{status}] {r['skill']}/{r['case']}")
            if not r["ok"]:
                for c in r["checks"]:
                    if not c["pass"]:
                        print(f"      unmet check '{c['label']}' (patterns: {c['patterns']})")
        print(f"graded: {len(results)}  pass: {len(passed)}  fail: {len(failed)}")

    if args.red or args.output_dir:
        return 0  # demo / recorded modes are informational
    return 0 if not failed else 1  # GREEN-reference mode is the gate


if __name__ == "__main__":
    sys.exit(main())
