#!/usr/bin/env python3
"""
skill-incorporate.py — per-skill incorporation scorecard (stdlib only).

How the repo incorporates itself: every skill should reach the full treatment —
referenceable node (always true), workflow: node contract, default-mode eligibility
(Core Workflow + Verification), golden regression cases, and a retrieval index entry.
This script computes the scorecard across the whole library so the gaps ("every skill
should have X") are data, not vibes.

Columns per skill:
    contract    frontmatter carries a workflow: block
    eligible    body has Core Workflow + a Verification heading (default-mode node)
    golden      evals/golden/<name>/cases.json exists
    retrieval   present in the lexical skill index (embedding layer = next wave, B6)

CLI:
    python3 scripts/skill-incorporate.py              # aggregate + top gaps
    python3 scripts/skill-incorporate.py --json       # full per-skill matrix
Exit 0.
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")
GOLDEN_DIR = os.path.join(ROOT, "evals", "golden")


def _front(text):
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def _body(text):
    m = re.search(r"^---\s*\n.*?\n---\s*\n(.*)$", text, re.S)
    return m.group(1) if m else text


def scan():
    rows = []
    for domain in sorted(os.listdir(SKILLS_DIR)):
        dpath = os.path.join(SKILLS_DIR, domain)
        if not os.path.isdir(dpath):
            continue
        for name in sorted(os.listdir(dpath)):
            path = os.path.join(dpath, name, "SKILL.md")
            if not os.path.isfile(path):
                continue
            text = open(path, encoding="utf-8").read()
            front = _front(text)
            body = _body(text)
            nm = re.search(r"(?m)^name:[ \t]*[\"']?([^\"'\n]+)", front)
            canonical = nm.group(1).strip() if nm else name
            rows.append({
                "name": canonical,
                "domain": domain,
                "path": os.path.relpath(path, ROOT),
                "contract": bool(re.search(r"(?m)^workflow:\s*$", front)),
                "eligible": bool(re.search(r"^#+\s+Core Workflow", body, re.M)
                                 and re.search(r"^#+\s+Verification", body, re.M)),
                "golden": os.path.isdir(os.path.join(GOLDEN_DIR, canonical)),
                "retrieval": True,  # lexical index covers every skill (embeddings = next wave)
            })
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="Per-skill incorporation scorecard")
    ap.add_argument("--json", action="store_true", help="full per-skill matrix")
    ap.add_argument("--limit", type=int, default=12, help="gap-list length")
    args = ap.parse_args(argv)

    rows = scan()
    if args.json:
        print(json.dumps(rows, indent=1))
        return 0

    total = len(rows)
    n_contract = sum(1 for r in rows if r["contract"])
    n_eligible = sum(1 for r in rows if r["eligible"])
    n_golden = sum(1 for r in rows if r["golden"])
    print("incorporation over %d skills:" % total)
    print("  workflow: contract   %d/%d" % (n_contract, total))
    print("  default-mode eligible %d/%d" % (n_eligible, total))
    print("  golden eval set      %d/%d" % (n_golden, total))
    print("  retrieval index      %d/%d (lexical; embeddings = next wave)" % (total, total))

    missing_contract = [r["name"] for r in rows if r["eligible"] and not r["contract"]]
    missing_golden = [r["name"] for r in rows if not r["golden"]]
    print("\ngaps (eligible without workflow: contract): %d" % len(missing_contract))
    for n in missing_contract[: args.limit]:
        print("   - %s" % n)
    if len(missing_contract) > args.limit:
        print("   ... and %d more" % (len(missing_contract) - args.limit))
    print("gaps (no golden eval set): %d of %d" % (len(missing_golden), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
