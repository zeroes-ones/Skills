#!/usr/bin/env python3
"""
eval-golden.py — deterministic golden-case checks for a skill (stdlib only).

Frontier B2 (BEYOND-LOOPS-GRAPHS.md): per-skill golden datasets with pattern checks, runnable in
CI. Cases live in evals/golden/<skill>/cases.json:

    {"skill": "<name>",
     "cases": [
       {"id": "...", "input": "...", "expected_behavior": "...",
        "checks": [{"label": "...", "patterns": ["...", ...]}],
        "reference_output": "text that must satisfy the checks"} ]}

The harness validates the schema, then for every case applies each check's regex patterns to the
candidate text (reference_output by default, or --output for a live transcript). A case passes
when every label has at least one matching pattern. Exit 0 iff all cases pass — golden sets must
not rot. LLM-generated outputs and judge-based scoring plug in behind the same contract later.

Usage:
    python3 scripts/lib/eval-golden.py --cases evals/golden/qa-engineer/cases.json
    python3 scripts/lib/eval-golden.py --cases ... --output transcript.txt   # live output
    python3 scripts/lib/eval-golden.py --cases ... --json
"""

import argparse
import json
import os
import re
import sys

_SKIP_KEYS = ("input", "expected_behavior", "reference_output")


def _load_cases(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as exc:
        raise SystemExit("cannot read cases: %s" % exc)
    except ValueError as exc:
        raise SystemExit("cases file is not valid JSON: %s" % exc)
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("skill"), str):
        errors.append("top level must be {'skill': str, 'cases': [...]}")
    for case in data.get("cases") or []:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            errors.append("every case needs a string 'id'")
        if not isinstance(case.get("checks"), list):
            errors.append("case %r needs a checks list" % case.get("id"))
    if errors:
        raise SystemExit("schema errors:\n  " + "\n  ".join(errors))
    return data


def evaluate_case(case, text):
    """Return (passed_labels, failed_labels, skipped) for one case against candidate text.
    Patterns are treated as case-insensitive LITERAL substrings (matching the seed-scenarios.json
    convention), not raw regex."""
    passed, failed = [], []
    for check in case.get("checks") or []:
        patterns = check.get("patterns") or []
        hit = any(re.search(re.escape(p), text, re.IGNORECASE | re.MULTILINE) for p in patterns)
        (passed if hit else failed).append(check.get("label", "?"))
    return passed, failed


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic golden-case checks for a skill")
    ap.add_argument("--cases", required=True, help="evals/golden/<skill>/cases.json")
    ap.add_argument("--output", help="candidate transcript file (default: reference_output)")
    ap.add_argument("--json", action="store_true", help="machine-readable summary")
    args = ap.parse_args(argv)

    data = _load_cases(args.cases)
    skill = data["skill"]
    results = []
    missing = 0
    for case in data.get("cases") or []:
        cid = case["id"]
        text = None
        if args.output:
            if not os.path.isfile(args.output):
                missing += 1
                results.append({"id": cid, "ok": False,
                                "reason": "output file missing: %s" % args.output})
                continue
            text = open(args.output, encoding="utf-8").read()
        elif case.get("reference_output"):
            text = case["reference_output"]
        else:
            missing += 1
            results.append({"id": cid, "ok": False,
                            "reason": "no reference_output and no --output provided"})
            continue
        passed, failed = evaluate_case(case, text)
        ok = not failed
        results.append({"id": cid, "ok": ok, "passed": passed, "failed": failed})
    total = len(data.get("cases") or [])
    ok_n = sum(1 for r in results if r["ok"])

    if args.json:
        print(json.dumps({"skill": skill, "total": total, "passed": ok_n,
                          "missing": missing, "cases": results}, indent=2))
    else:
        print("golden: %s | %d/%d cases pass%s" %
              (skill, ok_n, total, "" if missing == 0 else " (%d unexecutable)" % missing))
        for r in results:
            if r["ok"]:
                print("  PASS %s" % r["id"])
            else:
                print("  FAIL %s (%s)" % (r["id"], ", ".join(r.get("failed") or [r.get("reason", "?")])))
    return 1 if (missing or ok_n < total) else 0


if __name__ == "__main__":
    sys.exit(main())
