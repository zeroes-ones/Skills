#!/usr/bin/env python3
"""reconcile-artifacts.py — reconcile declared chain edges against declared artifacts.

A skill states its handoff relationships twice, independently:

    chain.consumes_from / chain.feeds_into     the dependency graph (validate_chains.py)
    workflow.artifacts.inputs / .outputs       the typed node contract (lint-workflow.py)

Nothing currently checks that the two agree. This tool judges each `consumes_from` edge by
whether the named upstream actually *produces* something the consumer declares needing:

    CONFIRMED   upstream.artifacts.outputs contains one of this skill's artifacts.inputs
    PLAUSIBLE   it does not by name, but the conservative normaliser or the explicit synonym
                table maps an upstream output name onto one of this skill's input names
    ORPHAN      the upstream produces none of the declared inputs, by any of those rules
    UNJUDGED    one of the two ends declares no artifacts, so no claim can be made either way

It also reports the reverse direction: for every declared input, which skills' outputs
satisfy it by exact name, and which of those producers are missing from `consumes_from`.

Resolution is deliberately narrow. Name resolution is (1) exact, (2) normalised by
lowercasing and dropping hyphens/underscores and a trailing plural `s`, (3) looked up in the
explicit SYNONYMS table below, where every pairing is traceable to a declared edge already
present in the corpus. There is no edit distance, no token overlap and no stemming beyond
the trailing `s`: token overlap in particular invents producers. Measured on this corpus, the
single input name `design-system` has 10 distinct declared outputs sharing one token with it
(`cache-design`, `prompt-design`, `schema-design`, `interop-design`, `security-design`,
`orchestration-design`, `extension-platform-design`, `verifier-design-evidence`,
`design-system-assets`, `type-system`) — every one of them an unrelated artefact. A synonym is
therefore only listed when the output name is a *more specific form of the same concept* as
the input name and an existing declared edge already pairs the two skills. SYNONYMS and
REJECTED_SYNONYMS are both hand-reviewed; the rejected entries are kept so the next reader
does not re-derive and re-add them.

Advisory by default: the report is printed, the exit code stays 0. --strict turns ORPHAN
edges into exit 1 for callers that have adopted the reconciliation as a gate.

The frontmatter and artifact extraction is delegated to check-chain-coherence.py, which parses
the artifact block with scripts/lib/safe_yaml.py and the chain lists with its own line scan.
Reusing it keeps this report about exactly the contract the rest of the toolchain sees.

Usage:
    python3 scripts/reconcile-artifacts.py                 # advisory report, exit 0
    python3 scripts/reconcile-artifacts.py --json          # machine-readable report
    python3 scripts/reconcile-artifacts.py --strict        # exit 1 if any ORPHAN edge
    python3 scripts/reconcile-artifacts.py --name <skill>  # one consumer
    python3 scripts/reconcile-artifacts.py --top 30        # rows per section
    python3 scripts/reconcile-artifacts.py --synonyms      # dump the synonym table and exit
"""

import argparse
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _load_module(path, modname):
    """Load a hyphenated sibling script as a module (the idiom used by workflow-runner.py)."""
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_COHERENCE = _load_module(os.path.join(ROOT, "scripts", "check-chain-coherence.py"),
                          "check_chain_coherence")

# output name -> input names it satisfies. Each entry is evidenced by a declared
# consumes_from edge already in the corpus, named in the comment.
SYNONYMS = {
    # ui-ux-designer -> website-builder / accessibility-auditor / frontend-developer
    "design-system-assets": {"brand-assets", "design-assets", "design-system"},
    # api-designer -> frontend-developer / secure-api-design
    "api-spec": {"api-contract", "api-design"},
    # ci-cd-builder -> code-formatting-and-linting
    "ci-config": {"existing-config"},
    # platform-hig-architect -> design-system-architect
    "platform-convention-matrix": {"platform-conventions"},
    # typography-designer -> design-system-architect
    "type-system": {"type-scale"},
    "type-tokens": {"type-scale"},
    # ux-researcher -> ui-ux-designer
    "research-brief": {"user-research"},
    # accessibility-auditor -> inclusive-design-engineer
    "accessibility-audit": {"accessibility-findings"},
    # multi-agent-orchestration / verifier-design -> verification-independence-engineer
    "orchestration-design": {"agent-system-design"},
    "verifier-design-evidence": {"agent-system-design"},
    # product-manager -> ux-researcher
    "product-spec": {"product-context"},
}

# Pairings an existing declared edge would also support, rejected on review. Kept here so the
# next reader does not re-derive them and re-add them. Same shape as SYNONYMS.
REJECTED_SYNONYMS = {
    "schema-design": {"design-system", "service-design"},
    "cache-design": {"service-design"},
    "interop-design": {"design-system"},
    "prompt-design": {"design-system"},
    "performance-plan": {"performance-requirements"},
    "review-report": {"review-policy"},
    "api-surface-list": {"api-contract"},
    "type-system": {"design-system"},
}

EXACT, NORMALISED, SYNONYM, NONE = "exact", "normalised", "synonym", "none"
CONFIRMED, PLAUSIBLE, ORPHAN, UNJUDGED = "CONFIRMED", "PLAUSIBLE", "ORPHAN", "UNJUDGED"


def normalise(name):
    """Lowercase, drop separators, drop one trailing plural `s` (never from `ss`).

    No stemming, no synonyms, no fuzzy matching: only the two mechanical collapses the
    corpus actually needs. `api-contract` / `api_contract` / `api-contracts` collapse onto
    one another; `design-system` and `schema-design` stay distinct.
    """
    flat = _SLUG_RE.sub("", name.lower())
    if flat.endswith("s") and not flat.endswith("ss"):
        flat = flat[:-1]
    return flat


def match_tier(output_name, input_name):
    """How the strongest rule rates `output_name` as a producer of `input_name`."""
    if output_name == input_name:
        return EXACT
    if normalise(output_name) == normalise(input_name):
        return NORMALISED
    if input_name in SYNONYMS.get(output_name, ()):
        return SYNONYM
    return NONE


def best_tier(outputs, inputs):
    """Strongest tier across every (output, input) pair, or NONE."""
    rank = {EXACT: 3, NORMALISED: 2, SYNONYM: 1, NONE: 0}
    best = NONE
    for out in outputs:
        for ins in inputs:
            tier = match_tier(out, ins)
            if rank[tier] > rank[best]:
                best = tier
    return best


def classify(tier):
    if tier == EXACT:
        return CONFIRMED
    if tier in (NORMALISED, SYNONYM):
        return PLAUSIBLE
    return ORPHAN


def producer_index(skills):
    """{output name: [skill names that declare producing it]} — exact names only."""
    index = {}
    for name, rec in skills.items():
        art = rec["artifacts"]
        if not art:
            continue
        for out in art["outputs"] or []:
            index.setdefault(out, []).append(name)
    return {k: sorted(v) for k, v in index.items()}


def distinct_inputs(rows):
    """The set of input names declared across the reconciled rows."""
    names = set()
    for row in rows:
        names.update(row["inputs"])
    return names


def reconcile(skills, index):
    """Per-consumer judgement of every consumes_from edge, plus each input's real producers."""
    rows = []
    for name, rec in sorted(skills.items()):
        art = rec["artifacts"]
        if not art or not art["inputs"]:
            continue
        inputs = art["inputs"]
        edges = []
        for up in rec["consumes_from"]:
            upstream = skills.get(up)
            if upstream is None:
                # Dangling references are validate_chains.py's report, not this one's.
                edges.append({"upstream": up, "class": UNJUDGED,
                              "reason": "upstream skill does not resolve"})
                continue
            up_art = upstream["artifacts"]
            if not art or not up_art or not up_art["outputs"]:
                edges.append({"upstream": up, "class": UNJUDGED,
                              "reason": "no artifact claim at one end"})
                continue
            tier = best_tier(up_art["outputs"], inputs)
            verdict = classify(tier)
            entry = {"upstream": up, "class": verdict, "match": tier,
                     "upstream_outputs": up_art["outputs"]}
            if verdict == ORPHAN:
                entry["reason"] = "upstream declares none of this skill's inputs"
            edges.append(entry)

        producers = {}
        for ins in inputs:
            producers[ins] = [p for p in index.get(ins, []) if p != name]
        true_producers = sorted({p for ps in producers.values() for p in ps})
        rows.append({
            "skill": name,
            "file": rec["path"],
            "inputs": inputs,
            "outputs": art["outputs"] or [],
            "consumes_from": list(rec["consumes_from"]),
            "edges": edges,
            "producers": producers,
            "true_producers": true_producers,
            "undeclared_producers": [p for p in true_producers
                                     if p not in rec["consumes_from"]],
            "unproduced_inputs": [i for i in inputs if not producers[i]],
        })
    return rows


def totals(rows):
    counts = {"consumers": len(rows), "inputs": 0, "edges": 0,
              CONFIRMED: 0, PLAUSIBLE: 0, ORPHAN: 0, UNJUDGED: 0,
              "unproduced_inputs": 0, "undeclared_producers": 0}
    for row in rows:
        counts["inputs"] += len(row["inputs"])
        for edge in row["edges"]:
            counts["edges"] += 1
            counts[edge["class"]] += 1
        counts["unproduced_inputs"] += len(row["unproduced_inputs"])
        counts["undeclared_producers"] += len(row["undeclared_producers"])
    return counts


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Reconcile declared chain edges against declared artifacts")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any ORPHAN edge")
    ap.add_argument("--name", help="reconcile only a specific consumer skill")
    ap.add_argument("--top", type=int, default=15, help="rows per section in text output")
    ap.add_argument("--synonyms", action="store_true",
                    help="print the synonym table (and the rejected pairings) and exit")
    args = ap.parse_args(argv)

    if args.synonyms:
        print("=== Artifact Synonym Table ===")
        print()
        print("output name -> input names it satisfies (each evidenced by a declared edge)")
        for out in sorted(SYNONYMS):
            print("  %-30s -> %s" % (out, ", ".join(sorted(SYNONYMS[out]))))
        print()
        print("rejected candidates (an edge supports them, review does not):")
        for out in sorted(REJECTED_SYNONYMS):
            print("  %-30s -> %s" % (out, ", ".join(sorted(REJECTED_SYNONYMS[out]))))
        return 0

    skills = _COHERENCE.load_skills()
    # The producer index is always corpus-wide: a producer the narrow view cannot see is
    # still a producer, so narrowing it would invent "no producer in the corpus" findings.
    index = producer_index(skills)
    if args.name:
        if args.name not in skills:
            print("ERROR: Skill '%s' not found" % args.name, file=sys.stderr)
            return 1
        skills = {args.name: skills[args.name]}

    rows = reconcile(skills, index)
    counts = totals(rows)

    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    GREEN = "\033[0;32m"
    NC = "\033[0m"

    if args.json:
        print(json.dumps({
            "skills_scanned": len(skills),
            "consumers_reconciled": counts["consumers"],
            "inputs_reconciled": counts["inputs"],
            "edges": counts["edges"],
            "confirmed": counts[CONFIRMED],
            "plausible": counts[PLAUSIBLE],
            "orphan": counts[ORPHAN],
            "unjudged": counts[UNJUDGED],
            "unproduced_inputs": counts["unproduced_inputs"],
            "undeclared_producers": counts["undeclared_producers"],
            "synonyms": {k: sorted(v) for k, v in sorted(SYNONYMS.items())},
            "details": rows,
            "strict": args.strict,
            "strict_failures": counts[ORPHAN],
        }, indent=2))
        return 1 if (args.strict and counts[ORPHAN]) else 0

    print("=== Artifact Vocabulary Reconciliation ===")
    print("Skills scanned: %d" % len(skills))
    print("Consumers reconciled (declare artifacts.inputs): %d" % counts["consumers"])
    print()

    print("Judged consumes_from edges (both ends declare artifacts):")
    print("  %s%d CONFIRMED%s  the upstream produces one of my inputs by name"
          % (GREEN, counts[CONFIRMED], NC))
    print("  %s%d PLAUSIBLE%s  only the normaliser or synonym table connects them"
          % (YELLOW, counts[PLAUSIBLE], NC))
    print("  %s%d ORPHAN%s     the upstream produces nothing I declare needing"
          % (RED, counts[ORPHAN], NC))
    print("  %d UNJUDGED   no artifact claim at one end, or a dangling reference"
          % counts[UNJUDGED])
    judged = counts[CONFIRMED] + counts[PLAUSIBLE] + counts[ORPHAN]
    if judged:
        disjoint = counts[PLAUSIBLE] + counts[ORPHAN]
        print("  %d of %d judged edges are name-disjoint (%.1f%%); "
              "%d of those remain ORPHAN after every rule"
              % (disjoint, judged, 100.0 * disjoint / judged, counts[ORPHAN]))
    print()

    print("Declared inputs with no exact producer anywhere in the corpus:")
    print("  %d of %d input declarations across %d distinct names"
          % (counts["unproduced_inputs"], counts["inputs"], len(distinct_inputs(rows))))
    print()

    by_skill = {r["skill"]: r for r in rows}
    orphans = [(r, e) for r in rows for e in r["edges"] if e["class"] == ORPHAN]
    plausible = [(r, e) for r in rows for e in r["edges"] if e["class"] == PLAUSIBLE]

    if orphans:
        consumers = {row["skill"] for row, _ in orphans}
        print("%sORPHAN edges by consumer (%d consumers):%s" % (RED, len(consumers), NC))
        worst = {}
        for row, edge in orphans:
            worst.setdefault(row["skill"], []).append(edge)
        for name, edges in sorted(worst.items(), key=lambda x: -len(x[1]))[:args.top]:
            print("  %3d  %-34s %s" % (len(edges), name, by_skill[name]["file"]))
        print()
        print("ORPHAN edges (first %d of %d):" % (min(args.top, len(orphans)), len(orphans)))
        for row, edge in orphans[:args.top]:
            print("  %s consumes_from %s" % (row["skill"], edge["upstream"]))
            print("      upstream outputs %s" % edge.get("upstream_outputs"))
            print("      my inputs        %s" % row["inputs"])
        print()

    if plausible:
        print("PLAUSIBLE edges (non-identical name, mapped by a rule):")
        for row, edge in plausible[:args.top]:
            print("  %-30s consumes_from %-28s via %s"
                  % (row["skill"], edge["upstream"], edge["match"]))
        print()

    missing = [(r, p) for r in rows for p in r["undeclared_producers"]]
    if missing:
        print("Producers of a declared input that are NOT in consumes_from (%d):" % len(missing))
        for row, prod in missing[:args.top]:
            print("  %-30s produces an input of %-24s but is not declared upstream"
                  % (prod, row["skill"]))
        print()

    no_producer = [(r, i) for r in rows for i in r["unproduced_inputs"]]
    if no_producer:
        print("Declared inputs no skill produces (%d declaration%s):"
              % (len(no_producer), "" if len(no_producer) == 1 else "s"))
        for row, ins in no_producer[:args.top]:
            print("  %-30s declares input %-28s — no producer in the corpus"
                  % (row["skill"], ins))
        print()

    if not orphans and not plausible and not missing and not no_producer:
        print("%s\u2713 every declared edge and input reconciles exactly%s" % (GREEN, NC))
        print()
    print("%sArtifact reconciliation PASSED (advisory)%s" % (GREEN, NC)
          if not orphans else
          "%sArtifact reconciliation: %d ORPHAN edge(s), reported advisory%s"
          % (YELLOW, counts[ORPHAN], NC))
    return 1 if (args.strict and counts[ORPHAN]) else 0


if __name__ == "__main__":
    sys.exit(main())
