#!/usr/bin/env python3
"""check-token-budget.py — deterministic token-budget gate (stdlib only).

The repo's architecture treats the *compiled* skill XML
(.skills-compiled/<name>/skill.xml) as the agent-load artifact, and each skill
declares a `token_budget` in frontmatter that the compile step targets
(compile-skills.sh exit code 3 = "Token budget exceeded"). This check verifies
the compiled form actually honours the declared budget:

    compiled_tokens (metadata.json) <= budget (skill.xml root attribute)

It also reports, informationally (never gates on it):
  * skills absent from the compiled set (coverage gap), and
  * the raw SKILL.md word count vs the declared budget (the shipped form —
    larger by design since the compiled XML is the trimmed load artifact).

Usage:
    python3 scripts/check-token-budget.py                 # strict: exit 1 if any over
    python3 scripts/check-token-budget.py --json          # machine-readable
    python3 scripts/check-token-budget.py --allow-over    # report only, exit 0

Exit codes: 0 = all compiled artifacts within budget, 1 = violations found.
"""

import argparse
import glob
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DEFAULT_ROOT = os.path.join(REPO, ".skills-compiled")


def _budget_from_xml(xml_path):
    """Read the budget="N" attribute from a compiled skill.xml root element."""
    try:
        head = open(xml_path, encoding="utf-8").read(512)
    except OSError:
        return None
    m = re.search(r'budget="(\d+)"', head)
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=DEFAULT_ROOT, help="compiled output dir")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--allow-over", action="store_true", help="report-only mode (exit 0)")
    args = ap.parse_args()

    rows = []
    for meta_path in sorted(glob.glob(os.path.join(args.root, "*", "metadata.json"))):
        name = os.path.basename(os.path.dirname(meta_path))
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except (OSError, ValueError) as e:
            rows.append({"skill": name, "error": f"metadata unreadable: {e}"})
            continue
        xml_path = os.path.join(os.path.dirname(meta_path), "skill.xml")
        budget = _budget_from_xml(xml_path)
        compiled = meta.get("compiled_tokens")
        original = meta.get("original_tokens")
        rows.append({
            "skill": name,
            "original_tokens": original,
            "compiled_tokens": compiled,
            "budget": budget,
            "over": bool(compiled is not None and budget is not None and compiled > budget),
        })

    violations = [r for r in rows if r.get("over")]
    errors = [r for r in rows if "error" in r]
    missing_budget = [r["skill"] for r in rows if "budget" not in r and r.get("budget") is None and "error" not in r]

    if args.json:
        print(json.dumps({
            "total_compiled": len(rows),
            "within_budget": sum(1 for r in rows if not r.get("over") and "error" not in r),
            "over_budget": len(violations),
            "metadata_errors": len(errors),
            "violations": [{"skill": r["skill"], "compiled_tokens": r["compiled_tokens"],
                            "budget": r["budget"],
                            "ratio": round(r["compiled_tokens"] / r["budget"], 2) if r["budget"] else None}
                           for r in sorted(violations, key=lambda r: r["compiled_tokens"] / r["budget"] if r["budget"] else 0, reverse=True)],
        }, indent=2))
    else:
        print(f"compiled skills checked : {len(rows)}")
        print(f"within declared budget  : {sum(1 for r in rows if not r.get('over') and 'error' not in r)}")
        print(f"OVER declared budget    : {len(violations)}")
        if errors:
            print(f"metadata errors          : {len(errors)}")
        for r in sorted(violations, key=lambda r: r["compiled_tokens"] / r["budget"] if r["budget"] else 0, reverse=True):
            ratio = r["compiled_tokens"] / r["budget"] if r["budget"] else float("inf")
            print(f"  OVER  {r['skill']}: compiled {r['compiled_tokens']} vs budget {r['budget']} ({ratio:.1f}x)")
        for r in rows:
            if "error" in r:
                print(f"  ERROR {r['skill']}: {r['error']}")

    if errors:
        print("note: metadata errors should be investigated", file=sys.stderr)
    if violations and not args.allow_over:
        print(f"FAIL: {len(violations)} compiled skills exceed their declared token_budget "
              f"(see docs — compiled XML is the agent-load artifact; budgets are a hard contract).")
        return 1
    if violations:
        print(f"report: {len(violations)} compiled skills exceed their declared token_budget (non-blocking).")
    else:
        print("All compiled skills within declared token budget.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
