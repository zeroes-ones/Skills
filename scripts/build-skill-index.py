#!/usr/bin/env python3
"""
build-skill-index.py — skill index + baseline lexical routing eval (stdlib only).

Frontier B6 (BEYOND-LOOPS-GRAPHS.md): semantic retrieval over the skill library. This builds a
plain JSON index of every skills/**/SKILL.md (name, domain, path, description, body word count,
chain-degree via frontmatter) and provides a deterministic LEXICAL search baseline over
name+description tokens. No embeddings here — the point is the measurable baseline that an
embedding + rerank layer (SkillRouter-style, body-weighted) must beat, plus routing evals.

CLI:
    python3 scripts/build-skill-index.py --build            # index over all skills; prints summary
    python3 scripts/build-skill-index.py --build --out index.json
    python3 scripts/build-skill-index.py --search "database schema design"
    python3 scripts/build-skill-index.py --eval             # held-out task->skill accuracy
Exit 0.
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")

# Held-out task -> expected skill (unambiguous subset used for the routing baseline).
ROUTING_EVAL = [
    ("define the REST endpoints and error model for a new domain", "api-designer"),
    ("design the relational schema and migrations for an ecommerce domain", "database-designer"),
    ("set up a CI/CD pipeline with quality gates and approvals", "ci-cd-builder"),
    ("implement mobile screens with offline, push, and permissions", "mobile-developer"),
    ("build analytics models and lineage for metric definitions", "analytics-engineer"),
    ("plan a product roadmap with prioritized scope and acceptance criteria", "product-manager"),
    ("respond to a production outage and write an incident report", "incident-responder"),
    ("minimize tokens of an existing prompt while holding answer quality", "context-optimizer"),
    ("engineer prompts at scale with versioning and system-prompt governance", "llm-engineer"),
    ("secure an API surface with auth flows, data classification and network controls",
     "security-engineer"),
]


def _frontmatter(text):
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def _description(front):
    out, collecting = [], False
    for ln in front.splitlines():
        if re.match(r"^description:[ \t]*(>|$)", ln):
            collecting = True
            continue
        if collecting:
            if re.match(r"^[A-Za-z_]+:", ln):
                break
            if ln.strip():
                out.append(ln.strip())
    return " ".join(out)


def _chain_degree(front):
    cnt = 0
    for ln in front.splitlines():
        if re.match(r"^[ \t]*-[ \t]*[a-z0-9][a-z0-9-]*$", ln):
            cnt += 1
    return cnt


def build_index():
    index = []
    for domain in sorted(os.listdir(SKILLS_DIR)):
        dpath = os.path.join(SKILLS_DIR, domain)
        if not os.path.isdir(dpath):
            continue
        for name_dir in sorted(os.listdir(dpath)):
            path = os.path.join(dpath, name_dir, "SKILL.md")
            if not os.path.isfile(path):
                continue
            text = open(path, encoding="utf-8").read()
            front = _frontmatter(text)
            nm = re.search(r"(?m)^name:[ \t]*[\"']?([^\"'\n]+)", front)
            name = nm.group(1).strip() if nm else name_dir
            body = text[len("---"):]
            m2 = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
            body = m2.group(2) if m2 else body
            index.append({
                "name": name,
                "domain": domain,
                "path": os.path.relpath(path, ROOT),
                "description": _description(front)[:600],
                "body_words": len(body.split()),
                "chain_degree": _chain_degree(front),
            })
    return sorted(index, key=lambda s: s["name"])


def _tokens(skill):
    return re.findall(r"[a-z0-9][a-z0-9-]*",
                      (skill["name"] + " " + skill["description"]).lower())


def lexical_search(query, index, topk=5):
    q = set(re.findall(r"[a-z0-9][a-z0-9-]*", query.lower()))
    scored = []
    for skill in index:
        toks = _tokens(skill)
        score = sum(1 for t in q if t in toks)
        scored.append((score, skill["name"]))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [name for _s, name in scored[:topk] if _s > 0]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Skill index + baseline lexical routing eval")
    ap.add_argument("--build", action="store_true", help="build the index over all skills")
    ap.add_argument("--out", help="write the index JSON to this file")
    ap.add_argument("--search", help="lexical top-k search over the index")
    ap.add_argument("--eval", action="store_true", help="held-out routing accuracy baseline")
    args = ap.parse_args(argv)

    if args.build or args.search or args.eval:
        index = build_index()
    else:
        ap.print_help()
        return 0

    if args.build:
        print("index: %d skills across %d domains"
              % (len(index), len({s["domain"] for s in index})))
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(index, fh, indent=1)

    if args.search:
        hits = lexical_search(args.search, index)
        print("search: %r -> %s" % (args.search, ", ".join(hits) if hits else "(no hits)"))

    if args.eval:
        n = len(ROUTING_EVAL)
        top1 = sum(1 for q, exp in ROUTING_EVAL if lexical_search(q, index, 1) == [exp])
        top5 = 0
        for q, exp in ROUTING_EVAL:
            hits = lexical_search(q, index, 5)
            if exp in hits:
                top5 += 1
        print("routing eval (lexical baseline): %d tasks | Top-1 %d/%d (%.0f%%) | Top-5 %d/%d (%.0f%%)"
              % (n, top1, n, 100.0 * top1 / n, top5, n, 100.0 * top5 / n))
        print("note: lexical name+description baseline; embedding+rerank over bodies must beat it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
