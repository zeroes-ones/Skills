#!/usr/bin/env python3
"""regression-scope.py — dependency-graph regression scope calculator (stdlib only, P9).

When a skill changes, its dependents may regress. This tool turns the frontmatter
chain graph into a concrete re-test scope:

    direct dependents   = skills whose chain.consumes_from includes the changed skill
    transitive          = closure over consumes_from edges (--transitive)

It also lists each dependent's per-skill eval file (skills/<domain>/<name>/evals/)
so a regression runner knows exactly which evals to re-run, plus the shared
suites (evals/evals.json, tier2/tier3) when --shared is passed.

Usage:
    python3 scripts/regression-scope.py backend-developer
    python3 scripts/regression-scope.py backend-developer --transitive --json
    python3 scripts/regression-scope.py backend-developer frontend-developer

Exit codes: 0 always (scope computation is not a pass/fail gate; the caller decides).
"""

import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS = os.path.join(REPO, "skills")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yaml_shim import safe_load  # noqa: E402


def _load_graph():
    """Return {skill_name: {"consumes_from": [...], "feeds_into": [...], "path": ...}}."""
    graph = {}
    for domain_dir in sorted(os.listdir(SKILLS)):
        domain_path = os.path.join(SKILLS, domain_dir)
        if not os.path.isdir(domain_path):
            continue
        for name_dir in sorted(os.listdir(domain_path)):
            skill_md = os.path.join(domain_path, name_dir, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            content = open(skill_md, encoding="utf-8").read()
            parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
            fm = safe_load(parts[1]) if len(parts) >= 3 else {}
            chain = fm.get("chain", {}) if isinstance(fm.get("chain"), dict) else {}
            name = fm.get("name") or name_dir
            graph[name] = {
                "name": name,
                "path": f"skills/{domain_dir}/{name_dir}/SKILL.md",
                "evals_dir": f"skills/{domain_dir}/{name_dir}/evals",
                "consumes_from": chain.get("consumes_from", []),
                "feeds_into": chain.get("feeds_into", []),
            }
    return graph


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("skills", nargs="+", help="changed skill name(s)")
    ap.add_argument("--transitive", action="store_true", help="include transitive dependents")
    ap.add_argument("--shared", action="store_true", help="list shared suites to re-run")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    graph = _load_graph()
    unknown = [s for s in args.skills if s not in graph]
    if unknown:
        print(f"unknown skill(s): {unknown}", file=sys.stderr)
        return 2

    dependents = set()
    for changed in args.skills:
        direct = {name for name, g in graph.items() if changed in g["consumes_from"]}
        dependents |= direct
        if args.transitive:
            frontier = set(direct)
            while frontier:
                nxt = set()
                for d in frontier:
                    nxt |= {name for name, g in graph.items() if d in g["consumes_from"]}
                new = nxt - dependents
                dependents |= new
                frontier = new

    result = {
        "changed": sorted(args.skills),
        "transitive": args.transitive,
        "direct_dependents": sorted({n for n in dependents if n not in args.skills}),
        "dependents": sorted(dependents),
    }
    if args.transitive:
        # keep all transitive members; direct subset is included above
        pass

    detail = [{"name": g["name"], "path": g["path"], "evals_dir": g["evals_dir"]}
              for n in sorted(dependents) for g in [graph[n]]]

    if args.json:
        out = dict(result)
        out["dependent_details"] = detail
        if args.shared:
            out["shared_suites"] = [
                "evals/evals.json",
                "evals/tier2-routing-evals.json",
                "evals/tier3-behavioral/seed-scenarios.json",
                "evals/tier3-behavioral/adversarial-scenarios.json",
            ]
        print(json.dumps(out, indent=2))
    else:
        print(f"changed skills        : {', '.join(sorted(args.skills))}")
        print(f"mode                  : {'transitive' if args.transitive else 'direct'}")
        print(f"dependent skills      : {len(dependents)}")
        for g in detail:
            has_evals = os.path.isdir(os.path.join(REPO, g["evals_dir"]))
            print(f"  {g['name']:<36} {g['path']}  evals:{'yes' if has_evals else 'no'}")
        if args.shared:
            print("shared suites to re-run: evals/evals.json, tier2, tier3 seeds+adversarial")
    return 0


if __name__ == "__main__":
    sys.exit(main())
