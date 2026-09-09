#!/usr/bin/env python3
"""
benchmark-skills.py — measurable library metrics for a skills corpus (stdlib only).

Frontier L1 / M2 (COMPARISON.md -> living benchmark): score ANY skills corpus with the same
deterministic metrics so 'best in class' is data, not prose. Layout expected:
<root>/<domain>/<skill>/SKILL.md (this library's convention); peer corpora in other layouts can
be passed as a flat dir of prompt files via --flat.

Metrics:
  skills            total SKILL.md prompts
  eligible          prompts with Core Workflow + a Verification heading (default-mode nodes)
  declared_contracts prompts whose frontmatter carries a `workflow:` block
  avg_body_words    mean body size (proxy for load cost; the token story)
  portability       % declaring a portability target
  golden_coverage   of the library's evals/golden/<name> sets, how many exist in this corpus
  routing_top1/top5 accuracy of lexical routing over the corpus against the held-out task set
                    (meaningful only when the corpus shares this library's skill names)

Usage:
    python3 scripts/benchmark-skills.py --root skills                 # this library
    python3 scripts/benchmark-skills.py --root skills --markdown      # markdown table
    python3 scripts/benchmark-skills.py --root <peer> --flat          # flat peer prompt dir
    python3 scripts/benchmark-skills.py --root skills --update COMPARISON.md
Exit 0.
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLDEN_DIR = os.path.join(ROOT, "evals", "golden")

# Held-out task -> expected skill (shared with build-skill-index.py ROUTING_EVAL).
ROUTING_TASKS = [
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


def _body(text):
    m = re.search(r"^---\s*\n.*?\n---\s*\n(.*)$", text, re.S)
    return m.group(1) if m else text


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


def _tags(front):
    out = []
    collecting = False
    for ln in front.splitlines():
        if re.match(r"^tags:[ \t]*$", ln):
            collecting = True
            continue
        if collecting:
            if re.match(r"^[A-Za-z_]+:", ln):
                break
            m = re.match(r"^[ \t]*-[ \t]*([a-z0-9][a-z0-9-]*)", ln)
            if m:
                out.append(m.group(1))
    return out


def collect(root, flat=False, shallow=False):
    """Return list of {name, path, text, front, body_words, eligible, declared, portable}."""
    items = []
    if flat:
        for f in sorted(os.listdir(root)):
            if f.endswith((".md", ".txt")):
                path = os.path.join(root, f)
                text = open(path, encoding="utf-8").read()
                name = os.path.splitext(f)[0]
                items.append((name, path, text))
    elif shallow:
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name, "SKILL.md")
            if not os.path.isfile(path):
                continue
            text = open(path, encoding="utf-8").read()
            items.append((name, path, text))
    else:
        for domain in sorted(os.listdir(root)):
            dpath = os.path.join(root, domain)
            if not os.path.isdir(dpath):
                continue
            for name in sorted(os.listdir(dpath)):
                path = os.path.join(dpath, name, "SKILL.md")
                if not os.path.isfile(path):
                    continue
                text = open(path, encoding="utf-8").read()
                items.append((name, path, text))
    rows = []
    for name, path, text in items:
        front = _frontmatter(text)
        nm = re.search(r"(?m)^name:[ \t]*[\"']?([^\"'\n]+)", front)
        canonical = nm.group(1).strip() if nm else name
        body = _body(text)
        rows.append({
            "name": canonical,
            "path": path,
            "body_words": len(body.split()),
            "desc": _description(front),
            "tags": _tags(front),
            "eligible": bool(re.search(r"^#+\s+Core Workflow", body, re.M)
                             and re.search(r"^#+\s+Verification", body, re.M)),
            "declared": bool(re.search(r"(?m)^workflow:\s*$", front)),
            "portable": "Portability target" in text,
        })
    return rows


def lexical_topk(query, rows, k):
    # Tokenize on letter/digit runs only so hyphenated skill names ("fullstack-developer")
    # and query compounds ("fullstack") match; index name + description + tags.
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored = []
    for r in rows:
        toks = re.findall(r"[a-z0-9]+",
                          (r["name"] + " " + r["desc"] + " " + " ".join(r["tags"])).lower())
        scored.append((sum(1 for t in q if t in toks), r["name"]))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [n for s, n in scored[:k] if s > 0]


def measure(rows):
    total = len(rows)
    eligible = sum(1 for r in rows if r["eligible"])
    declared = sum(1 for r in rows if r["declared"])
    portable = sum(1 for r in rows if r["portable"])
    avg_body = int(sum(r["body_words"] for r in rows) / total) if total else 0
    names = {r["name"] for r in rows}
    golden_sets = [n for n in os.listdir(GOLDEN_DIR) if os.path.isdir(os.path.join(GOLDEN_DIR, n))] \
        if os.path.isdir(GOLDEN_DIR) else []
    golden_hits = [n for n in golden_sets if n in names]
    top1 = sum(1 for q, exp in ROUTING_TASKS if lexical_topk(q, rows, 1) == [exp])
    top5 = sum(1 for q, exp in ROUTING_TASKS if exp in lexical_topk(q, rows, 5))
    n_tasks = len(ROUTING_TASKS)
    # effective load: compiled tokens from .skills-compiled metadata where present
    compiled = os.path.join(ROOT, ".skills-compiled")
    eff_total = eff_hits = eff_body = 0
    if os.path.isdir(compiled):
        for r in rows:
            meta = os.path.join(compiled, r["name"], "metadata.json")
            if os.path.isfile(meta):
                eff_hits += 1
                eff_total += json.load(open(meta, encoding="utf-8")).get("compiled_tokens", 0)
                eff_body += r["body_words"]
    avg_eff = int(eff_total / eff_hits) if eff_hits else 0
    avg_eff_body = int(eff_body / eff_hits) if eff_hits else 0
    return {
        "skills": total,
        "eligible": eligible,
        "declared_contracts": declared,
        "avg_body_words": avg_body,
        "portability_pct": round(100.0 * portable / total, 1) if total else 0.0,
        "golden_sets": len(golden_sets),
        "golden_coverage": "%d/%d" % (len(golden_hits), len(golden_sets)),
        "routing_top1": "%d/%d (%.0f%%)" % (top1, n_tasks, 100.0 * top1 / n_tasks),
        "routing_top5": "%d/%d (%.0f%%)" % (top5, n_tasks, 100.0 * top5 / n_tasks),
        "compiled_coverage": "%d/%d" % (eff_hits, total),
        "avg_compiled_tokens": avg_eff,
        "effective_saving_pct": round(100.0 * (1 - avg_eff / max(1, avg_eff_body)), 1)
        if avg_eff_body else 0.0,
    }


def _markdown(m):
    rows = [
        ("Skills (prompts)", m["skills"]),
        ("Executable-node eligible (Core Workflow + Verification)", m["eligible"]),
        ("Declared `workflow:` contracts", m["declared_contracts"]),
        ("Avg body words (load cost)", m["avg_body_words"]),
        ("Compiled coverage", m["compiled_coverage"]),
        ("Avg effective load (compiled tokens)", m["avg_compiled_tokens"]),
        ("Effective load saving vs raw body", "%.1f%%" % m["effective_saving_pct"]),
        ("Portability target declared", "%.1f%%" % m["portability_pct"]),
        ("Golden eval sets covered", m["golden_coverage"]),
        ("Routing Top-1 / Top-5 (lexical baseline)", "%s / %s" % (m["routing_top1"], m["routing_top5"])),
    ]
    return "\n".join("| %s | %s |" % (k, v) for k, v in rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic metrics for any skills corpus")
    ap.add_argument("--root", required=True, help="corpus root (domain/name/SKILL.md layout)")
    ap.add_argument("--flat", action="store_true", help="root holds flat prompt files")
    ap.add_argument("--shallow", action="store_true",
                    help="root holds <skill>/SKILL.md (single-level, peer layout)")
    ap.add_argument("--markdown", action="store_true", help="emit a markdown table")
    ap.add_argument("--update", help="replace the measured-baseline block in a markdown doc")
    args = ap.parse_args(argv)

    rows = collect(args.root, flat=args.flat, shallow=args.shallow)
    m = measure(rows)

    if args.markdown:
        print(_markdown(m))
    else:
        for k, v in m.items():
            print("%-22s %s" % (k, v))

    if args.update:
        doc = args.update
        text = open(doc, encoding="utf-8").read()
        marker = "<!-- MEASURED-BASELINE:START -->"
        endmark = "<!-- MEASURED-BASELINE:END -->"
        block = ("%s\n\n" % marker) + _markdown(m) + ("\n\n%s" % endmark)
        if marker in text:
            text = re.sub(re.escape(marker) + r".*?" + re.escape(endmark),
                          lambda _m: block, text, flags=re.S)
        else:
            text += "\n\n%s\n" % block
        open(doc, "w", encoding="utf-8").write(text)
        print("updated %s" % doc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
