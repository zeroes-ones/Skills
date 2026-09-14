#!/usr/bin/env python3
"""check-content-duplication.py — detect verbatim blocks shared across skills.

Motivation: the 2026-08-02 cohort of 39 skills was batch-generated and shares
whole sections verbatim (4-6 unique sections out of ~26). No existing gate can
see this: the template linter checks that a heading exists, not that its content
is about this skill.

Two legitimate exceptions exist and are allowlisted below:
  * a small set of sections the template defines as deliberately generic
    (Error Recovery is documented as "the ONLY generic section");
  * boilerplate wrappers that carry no routing or domain meaning.

Usage:
    python3 scripts/check-content-duplication.py                 # report, exit 0
    python3 scripts/check-content-duplication.py --strict        # exit 1 on new offenders
    python3 scripts/check-content-duplication.py --json
    python3 scripts/check-content-duplication.py --baseline F    # compare against a baseline list

Exit codes: 0 = within baseline/report-only, 1 = new duplicated block introduced.
"""

import argparse
import hashlib
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS = os.path.join(REPO, "skills")

# Sections the template defines as generic, plus pure-structure wrappers. Content in
# these is expected to repeat and is not a duplication defect.
GENERIC_SECTIONS = {
    "error recovery",
    "research_prerequisite — execute before any output",
    "state log",
    "state log schema",
    "anti-drift check",
    "anti-hallucination",
    "verification guardrails",
    "verification",
    "references",
    "deliberate practice",
}

MIN_WORDS = 20          # below this it is a heading, not a section
SHARED_THRESHOLD = 3    # appearing in >= N skills makes it a shared block


def normalise(text):
    """Collapse whitespace and strip depth markers so formatting does not mask identity."""
    t = re.sub(r"<!--\s*(?:QUICK|STANDARD|DEEP)[^>]*-->", " ", text)
    t = re.sub(r"\*\*\((?:QUICK|STANDARD|DEEP)(?::[^)]*)?\)\*\*", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def sections_of(path):
    """Yield (title, normalised_body) for each ## section in a SKILL.md body."""
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return
    parts = re.split(r"^##\s+", text, flags=re.M)[1:]
    for part in parts:
        lines = part.split("\n")
        title = re.sub(r"^<!--\s*(?:QUICK|STANDARD|DEEP)[^>]*-->\s*", "", lines[0])
        title = re.sub(r"\s*\*\*\((?:QUICK|STANDARD|DEEP)[^)]*\)\*\*\s*", "", title).strip()
        body = normalise("\n".join(lines[1:]))
        if len(body.split()) >= MIN_WORDS:
            yield title, body


def collect():
    """map normalised-block-hash -> {title, words, skills[]}"""
    blocks = {}
    for root, _dirs, files in os.walk(SKILLS):
        if "SKILL.md" not in files:
            continue
        path = os.path.join(root, "SKILL.md")
        name = os.path.basename(root)
        for title, body in sections_of(path):
            key = hashlib.sha1(body.encode("utf-8")).hexdigest()
            entry = blocks.setdefault(key, {"title": title, "body": body,
                                            "words": len(body.split()), "skills": []})
            entry["skills"].append(name)
    return blocks


def is_generic(title):
    return title.strip().lower() in GENERIC_SECTIONS


def offenders(blocks):
    """Shared blocks that are NOT allowlisted, sorted by reach."""
    out = []
    for _key, e in blocks.items():
        if len(e["skills"]) < SHARED_THRESHOLD:
            continue
        if is_generic(e["title"]):
            continue
        out.append(e)
    out.sort(key=lambda e: -len(e["skills"]))
    return out


def skill_duplication_ratio(blocks):
    """name -> (shared_sections, total_sections) excluding generic sections."""
    totals, shared = {}, {}
    for e in blocks.values():
        generic = is_generic(e["title"])
        is_shared = len(e["skills"]) >= SHARED_THRESHOLD and not generic
        for n in e["skills"]:
            totals[n] = totals.get(n, 0) + 1
            if is_shared:
                shared[n] = shared.get(n, 0) + 1
    return {n: (shared.get(n, 0), totals[n]) for n in totals}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any non-allowlisted shared block exists")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--baseline", help="file of known-shared block hashes to ignore")
    ap.add_argument("--top", type=int, default=15, help="how many offenders to print")
    args = ap.parse_args()

    blocks = collect()
    bad = offenders(blocks)

    known = set()
    if args.baseline and os.path.exists(args.baseline):
        known = {l.strip() for l in open(args.baseline, encoding="utf-8") if l.strip()}
        bad = [e for e in bad if hashlib.sha1(e["body"].encode()).hexdigest() not in known]

    ratio = skill_duplication_ratio(blocks)
    worst = sorted(((n, s, t) for n, (s, t) in ratio.items() if t),
                   key=lambda x: -(x[1] / x[2]))[:10]

    if args.json:
        print(json.dumps({
            "non_generic_shared_blocks": len(bad),
            "skills_affected": len({s for e in bad for s in e["skills"]}),
            "worst_ratios": [{"skill": n, "shared": s, "total": t} for n, s, t in worst],
            "top_blocks": [{"title": e["title"], "skills": len(e["skills"]),
                            "words": e["words"], "examples": e["skills"][:5]} for e in bad[:args.top]],
        }, indent=2))
    else:
        print("=== Content duplication (non-allowlisted shared blocks) ===")
        print(f"shared blocks (>= {SHARED_THRESHOLD} skills, excluding {len(GENERIC_SECTIONS)} generic sections): {len(bad)}")
        print(f"skills affected: {len({s for e in bad for s in e['skills']})}")
        print()
        if bad:
            print(f"top {min(args.top, len(bad))} by reach:")
            for e in bad[:args.top]:
                print(f"  {len(e['skills']):>4}x [{e['title'][:38]:38s}] {e['words']:>4}w  "
                      f"e.g. {', '.join(e['skills'][:3])}")
        print()
        print("worst per-skill ratios (shared/total, generic excluded):")
        for n, s, t in worst:
            print(f"  {n:38s} {s:>2}/{t:<3} ({s / t * 100:.0f}%)")

    if args.strict and bad:
        print(f"\nFAIL: {len(bad)} non-allowlisted shared block(s). "
              f"Repeated content belongs in a reference, or must be rewritten for this skill.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
