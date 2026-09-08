#!/usr/bin/env python3
"""workflow-eligibility.py — workflow-contract eligibility report (stdlib only).

Every skill is an executable node in default mode when its SKILL.md carries both
a Core Workflow section and a Verification section (its completion source).
Adding an explicit frontmatter `workflow:` contract upgrades it to a first-class
workflow node. This report answers critique #2's backlog question:

    declared   = skills with an explicit `workflow:` frontmatter contract
    eligible   = skills with Core Workflow + Verification (can adopt a contract)
    backlog    = eligible but undeclared (the Tier-2/Tier-3 adoption candidates)

Output: per-domain table + full backlog list, text or --json.

Usage:
    python3 scripts/workflow-eligibility.py              # text report
    python3 scripts/workflow-eligibility.py --json       # machine-readable
    python3 scripts/workflow-eligibility.py --domain finance
"""

import argparse
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS_DIR = os.path.join(REPO, "skills")


def _frontmatter(content):
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--domain", default=None, help="filter to one domain dir")
    args = ap.parse_args()

    rows = []
    for domain in sorted(os.listdir(SKILLS_DIR)):
        if args.domain and domain != args.domain:
            continue
        dpath = os.path.join(SKILLS_DIR, domain)
        if not os.path.isdir(dpath):
            continue
        for name in sorted(os.listdir(dpath)):
            p = os.path.join(dpath, name, "SKILL.md")
            if not os.path.isfile(p):
                continue
            content = open(p, encoding="utf-8").read()
            front = _frontmatter(content)
            canonical = None
            m = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)", front)
            canonical = m.group(1).strip() if m else name
            rows.append({
                "name": canonical,
                "path": f"skills/{domain}/{name}/SKILL.md",
                "domain": domain,
                "declared": bool(re.search(r"(?m)^workflow:\s*$", front)),
                "eligible": bool(re.search(r"^#+\s+Core Workflow", content, re.M)
                                 and re.search(r"^#+\s+Verification", content, re.M)),
            })

    declared = [r for r in rows if r["declared"]]
    eligible = [r for r in rows if r["eligible"]]
    backlog = [r for r in rows if r["eligible"] and not r["declared"]]

    if args.json:
        print(json.dumps({
            "total": len(rows),
            "declared_contracts": len(declared),
            "eligible": len(eligible),
            "backlog_eligible_undeclared": len(backlog),
            "backlog": [{"name": r["name"], "domain": r["domain"], "path": r["path"]} for r in backlog],
        }, indent=2))
        return 0

    print(f"skills total                       : {len(rows)}")
    print(f"explicit workflow: contracts       : {len(declared)}")
    print(f"eligible (Core Workflow+Verify)    : {len(eligible)}")
    print(f"backlog (eligible, undeclared)     : {len(backlog)}")
    print("")
    print("per-domain (declared / eligible / backlog):")
    domains = sorted({r["domain"] for r in rows})
    for d in domains:
        dr = [r for r in rows if r["domain"] == d]
        dd = len([r for r in dr if r["declared"]])
        de = len([r for r in dr if r["eligible"]])
        db = len([r for r in dr if r["eligible"] and not r["declared"]])
        bar = "#" * min(40, db)
        print(f"  {d:<22} declared={dd:<3} eligible={de:<3} backlog={db:<3} {bar}")
    print("")
    print("backlog sample (first 20, alphabetical):")
    for r in backlog[:20]:
        print(f"  {r['name']:<40} {r['path']}")
    print("")
    print(f"tip: adopt contracts in usage-frequency order per domain "
          f"(Tier 1 = the {len(declared)} declared today, Tier 2 = next {min(100 - len(declared), len(backlog))} of this backlog).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
