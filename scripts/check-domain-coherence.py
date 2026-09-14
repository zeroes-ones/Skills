#!/usr/bin/env python3
"""check-domain-coherence.py — detect vocabulary that belongs to a different domain.

Motivation: the 2026-08-02 batch applied a finance/trading research block to 39
lifestyle skills. `gardener`, `sleep-optimizer`, `relationship-architect` and
`stoic-practitioner` all contain "bull-market", "shift to defensive posture", and
"close the position and cut the loss" — sentences that are nonsense in those
domains and were never noticed, because `deep-research-gate.sh` checks that
*market* skills cover regimes and explicitly SKIPS non-market domains. Nothing
ever checked the inverse.

This gate checks the inverse: vocabulary from one domain appearing in another.

Usage:
    python3 scripts/check-domain-coherence.py               # report, exit 0
    python3 scripts/check-domain-coherence.py --strict      # exit 1 on any violation
    python3 scripts/check-domain-coherence.py --json

Exit codes: 0 = clean or report-only, 1 = cross-domain vocabulary found.
"""

import argparse
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS = os.path.join(REPO, "skills")

# Domains where the vocabulary below is legitimate.
MARKET_DOMAINS = {
    "14-finance",
    "18-corporate-finance",
    "26-web3",
    "27-creator-finance",
}

# Phrases that only make sense in a market context. Matched case-insensitively on a
# whole-phrase basis so ordinary English ("position", "exposure") does not trip them.
MARKET_PHRASES = [
    r"bull[- ]market",
    r"bear[- ]market",
    r"stop[- ]loss",
    r"close the position",
    r"cut the loss",
    r"shift to defensive posture",
    r"drawdown",
    r"max(?:imum)? drawdown",
]

# Phrases that only make sense in a domain that handles money at all. These fire on
# non-financial domains only when they appear as *advice*, not as a cost example.
# Deliberately narrow: "portfolio allocation" describes a fintech UI's subject matter
# legitimately (fintech-ui-designer) and is not advice, so it is NOT listed here.
FINANCE_ADVICE_PHRASES = [
    r"risk[- ]adjusted return",
    r"sharpe ratio",
    r"kelly criterion",
]

# Domains whose *subject matter* is money or markets, so naming those concepts is
# legitimate even though the skill is not itself a trading skill.
MONEY_ADJACENT_DOMAINS = {
    "01-strategy",     # business strategy legitimately discusses markets
    "03-design",       # fintech/health UI design describes its subject matter
    "11-legal",
    "19-governance",
}

COMPILED = [(p, re.compile(p, re.I)) for p in MARKET_PHRASES]
FIN_COMPILED = [(p, re.compile(p, re.I)) for p in FINANCE_ADVICE_PHRASES]

# Cost-of-failure language is fine anywhere; these headers imply a finance template
# was poured into a non-finance skill.
TEMPLATE_HEADERS = [
    r"CRITICAL: Must have\s*≥?\s*\d+\s*dollar-quantified gotchas",
]


def domain_of(path):
    rel = os.path.relpath(path, SKILLS)
    return rel.split(os.sep)[0]


def scan():
    hits = []
    for root, _dirs, files in os.walk(SKILLS):
        if "SKILL.md" not in files:
            continue
        path = os.path.join(root, "SKILL.md")
        dom = domain_of(path)
        name = os.path.basename(root)
        text = open(path, encoding="utf-8", errors="replace").read()
        if dom in MARKET_DOMAINS:
            continue
        # Market *vocabulary* is judged everywhere; but an advisory section written for a
        # trading audience inside a business/design skill is a different defect than a
        # lifestyle skill that acquired trading boilerplate. Report the latter as errors
        # and the former as a separate, softer class.
        soft = dom in MONEY_ADJACENT_DOMAINS
        for pat, rx in COMPILED:
            for m in rx.finditer(text):
                line = text[: m.start()].count("\n") + 1
                hits.append({"skill": name, "domain": dom, "line": line,
                             "phrase": m.group(0), "kind": "market-vocabulary",
                             "class": pat,
                             "severity": "soft" if soft else "error"})
        for pat, rx in FIN_COMPILED:
            for m in rx.finditer(text):
                line = text[: m.start()].count("\n") + 1
                hits.append({"skill": name, "domain": dom, "line": line,
                             "phrase": m.group(0), "kind": "finance-advice",
                             "class": pat, "severity": "error"})
        for pat in TEMPLATE_HEADERS:
            for m in re.finditer(pat, text, re.I):
                line = text[: m.start()].count("\n") + 1
                hits.append({"skill": name, "domain": dom, "line": line,
                             "phrase": m.group(0), "kind": "misfiled-template",
                             "class": pat, "severity": "error"})
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true", help="exit 1 on any violation")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    hits = scan()
    by_skill = {}
    for h in hits:
        by_skill.setdefault((h["skill"], h["domain"]), []).append(h)
    by_domain = {}
    for h in hits:
        by_domain[h["domain"]] = by_domain.get(h["domain"], 0) + 1

    if args.json:
        print(json.dumps({
            "violations": len(hits),
            "skills_affected": len(by_skill),
            "by_domain": by_domain,
            "by_kind": {k: sum(1 for h in hits if h["kind"] == k)
                        for k in {h["kind"] for h in hits}},
            "examples": sorted(hits, key=lambda h: (h["skill"], h["line"]))[:args.top],
        }, indent=2))
    else:
        print("=== Domain coherence (cross-domain vocabulary) ===")
        print(f"violations: {len(hits)}  across {len(by_skill)} skills")
        print()
        if by_domain:
            print("by domain:")
            for d, n in sorted(by_domain.items(), key=lambda x: -x[1]):
                print(f"  {n:>4}  {d}")
            print()
            print(f"top {min(args.top, len(by_skill))} skills:")
            for (name, dom), hs in sorted(by_skill.items(), key=lambda x: -len(x[1]))[:args.top]:
                sample = ", ".join(sorted({h["phrase"] for h in hs})[:3])
                print(f"  {len(hs):>3}  {name:34s} {dom:22s} {sample}")

    errors = [h for h in hits if h.get("severity") != "soft"]
    if args.strict and errors:
        print(f"\nFAIL: {len(errors)} cross-domain phrase(s). Content must match its domain; "
              f"market/regime language belongs only in market domains.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
