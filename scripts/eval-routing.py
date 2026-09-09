#!/usr/bin/env python3
"""eval-routing.py — canonical routing evaluator (stdlib only, Tier 2).

Routing baseline over each skill's indexable profile. Algorithm:
light suffix normalization -> augmented TF -> IDF log(1+N/df) -> cosine.
Indexed fields per skill:
  - head field: skill name + description + tags (weight 1.0)
  - auxiliary field: the body's "When to Use" section (weight 0.15), its own IDF
The auxiliary field reuses vocabulary the skill already publishes, so the router
sees the same trigger language an agent reads — no external data.

Faithful stdlib port of scripts/run-routing-evals.js scoring semantics so the
routing baseline is measurable in any environment (no node required).

Scores every scenario in evals/tier2-routing-evals.json (core 49) plus
evals/tier2-routing-adversarial.json (semantic, keyword-poor prompts), with
per-case allow_top_n, reporting per-suite and overall:

    rank-1 hit rate, top-N hit rate, MRR,
    must-not violations (false activations), expected-missing rate

This is the single canonical routing number the repo publishes; the node
runner and this tool implement the same algorithm, so results are comparable.

Usage:
    python3 scripts/eval-routing.py                 # text report
    python3 scripts/eval-routing.py --json          # machine-readable
    python3 scripts/eval-routing.py --suite <id>    # single suite

Exit: 0 (reporting tool; gating is a separate step once targets are set).
"""

import argparse
import glob
import json
import math
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS_DIR = os.path.join(REPO, "skills")
EVALS_DIR = os.path.join(REPO, "evals")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yaml_shim import safe_load  # noqa: E402

STOP_WORDS = {
    "the", "and", "for", "not", "use", "when", "with", "that", "this", "are",
    "from", "can", "has", "was", "all", "but", "its", "may", "than", "into",
    "also", "does", "some", "each", "over", "such", "will", "just", "only",
    "been", "more", "new", "any", "very", "our", "about", "should", "used",
    "which", "other", "being", "using", "don", "because", "there", "their",
}


def stem(word):
    """Light suffix normalization (stdlib-only). Keeps routing vocabulary aligned
    across inflected forms: 'minimizing'/'minimize'/'minimized' -> 'minimiz',
    'scaling'/'scales' -> 'scal'. Conservative: only transforms words of len > 4
    and never strips to a token shorter than 3 chars."""
    w = word
    if len(w) <= 4:
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("ing"):
        s = w[:-3]
        if len(s) >= 3:
            if s.endswith("e") and not s.endswith(("ee", "oe", "ye")):
                s = s[:-1]
            if len(s) > 3 and s[-1] == s[-2] and s[-1] not in "aeiou":
                s = s[:-1]
            return s
    if w.endswith("ed") and len(w) > 4:
        s = w[:-2]
        if s.endswith("e") and not s.endswith(("ee", "oe", "ye")):
            s = s[:-1]
        if len(s) > 3 and s[-1] == s[-2] and s[-1] not in "aeiou":
            s = s[:-1]
        return s
    if w.endswith("s") and not w.endswith(("ss", "us", "is")) and len(w) > 4:
        return w[:-1]
    return w


def tokenize(text):
    toks = re.sub(r"[^a-z0-9\s-]", " ", text.lower()).split()
    out = []
    for t in toks:
        for part in re.split(r"[\s-]+", t):
            if len(part) > 1 and part not in STOP_WORDS:
                out.append(stem(part))
    return out


def compute_tf(doc_tokens):
    tf = {}
    for t in doc_tokens:
        tf[t] = tf.get(t, 0) + 1
    max_freq = max(tf.values()) if tf else 0
    for t in tf:
        tf[t] = 0.5 + 0.5 * (tf[t] / max_freq) if max_freq else 0.0
    return tf


def compute_idf(docs, total):
    df = {}
    for doc in docs:
        for t in set(doc):
            df[t] = df.get(t, 0) + 1
    return {t: math.log(1 + total / v) for t, v in df.items()}


def cosine(query_vec, doc_vec):
    dot = qmag = dmag = 0.0
    for t, qv in query_vec.items():
        qmag += qv * qv
        dot += qv * doc_vec.get(t, 0.0)
    for v in doc_vec.values():
        dmag += v * v
    if qmag == 0 or dmag == 0:
        return 0.0
    return dot / (math.sqrt(qmag) * math.sqrt(dmag))


def collect_skills():
    skills = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            p = os.path.join(root, "SKILL.md")
            content = open(p, encoding="utf-8").read()
            parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            fm = safe_load(parts[1])
            desc = fm.get("description", "")
            if not desc:
                continue
            tags = fm.get("tags", [])
            tags = tags if isinstance(tags, list) else []
            skills.append({
                "name": fm.get("name") or os.path.basename(os.path.dirname(p)),
                "desc": desc,
                "tags": tags,
                "body": parts[2],
            })
    return skills


# Section headings the router harvests as a light, field-weighted signal.
_HEADING_RE = re.compile(r"^#{1,4}\s+(.*)$", re.MULTILINE)


def section_text(body, wanted):
    """Return text under body headings whose lowercase name contains a wanted phrase."""
    chunks = _HEADING_RE.split(body)  # [pre, head1, text1, head2, text2, ...]
    out = []
    for i in range(1, len(chunks), 2):
        head = chunks[i].lower()
        if any(w in head for w in wanted):
            text = chunks[i + 1] if i + 1 < len(chunks) else ""
            out.append(text)
    return " ".join(out)


def load_cases(target_suite):
    cases = []
    files = [
        os.path.join(EVALS_DIR, "tier2-routing-evals.json"),
        os.path.join(EVALS_DIR, "tier2-routing-adversarial.json"),
    ]
    for f in files:
        if not os.path.isfile(f):
            continue
        data = json.load(open(f, encoding="utf-8"))
        for suite in data.get("suites", []):
            if target_suite and suite["id"] != target_suite:
                continue
            for sc in suite.get("scenarios", []):
                cases.append({
                    "suite": suite["id"],
                    "id": sc["id"],
                    "prompt": sc["input"],
                    "expected": sc["expected"],
                    "must_not_route": sc.get("must_not_route", []),
                    "allow_top_n": sc.get("allow_top_n", 1),
                })
    return cases


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--suite", default=None)
    args = ap.parse_args()

    skills = collect_skills()
    names = {s["name"] for s in skills}

    # Head field: skill name + description + tags. Auxiliary field: the body's
    # "When to Use" section, harvested per skill and weighted at WHEN_WEIGHT.
    # Each field gets its own IDF so field vocabulary is compared on equal terms.
    head_docs = [tokenize(s["name"]) + tokenize(s["desc"]) + tokenize(" ".join(s["tags"]))
                 for s in skills]
    when_docs = [list(set(tokenize(section_text(s["body"], ["when to use"])))) for s in skills]
    idf_head = compute_idf(head_docs, len(skills))
    idf_when = compute_idf(when_docs, len(skills)) if any(when_docs) else {}
    WHEN_WEIGHT = 0.15
    doc_vectors = []
    for s, hd, wt in zip(skills, head_docs, when_docs):
        tf = compute_tf(hd)
        vec = {t: v * idf_head.get(t, 0.0) for t, v in tf.items()}
        if idf_when:
            tf_w = compute_tf(wt)
            for t, v in tf_w.items():
                vec[t] = vec.get(t, 0.0) + WHEN_WEIGHT * v * idf_when.get(t, 0.0)
        doc_vectors.append({"name": s["name"], "vec": vec})

    cases = load_cases(args.suite)
    if not cases:
        print("no scenarios found", file=sys.stderr)
        return 2

    unknown = sorted({c["expected"] for c in cases} - names)
    if unknown:
        print(f"FATAL: expected skill(s) not on disk: {unknown}", file=sys.stderr)
        return 2

    by_suite = {}
    for c in cases:
        qtf = compute_tf(tokenize(c["prompt"]))
        qvec = {t: v * idf_head.get(t, 0.0) for t, v in qtf.items()}
        ranked = sorted(
            (cosine(qvec, d["vec"]), d["name"]) for d in doc_vectors)
        ranked = [(n, s) for s, n in ranked]
        ranked.reverse()
        top_n = ranked[:c["allow_top_n"]]
        top_names = [n for n, _ in top_n]
        rank1 = top_names[0] if top_names else None
        expected_rank = next((i for i, (n, _) in enumerate(ranked) if n == c["expected"]), -1)
        res = {
            "suite": c["suite"],
            "id": c["id"],
            "rank1_hit": rank1 == c["expected"],
            "topN_hit": c["expected"] in top_names,
            "mrr": 1.0 / (expected_rank + 1) if expected_rank >= 0 else 0.0,
            "expected_rank": expected_rank + 1 if expected_rank >= 0 else None,
            "must_not_violations": [n for n in c["must_not_route"] if n in top_names],
            "top5": [n for n, _ in ranked[:5]],
        }
        by_suite.setdefault(c["suite"], []).append(res)

    def agg(items):
        n = len(items)
        rank1 = sum(1 for r in items if r["rank1_hit"])
        topn = sum(1 for r in items if r["topN_hit"])
        mrr = sum(r["mrr"] for r in items) / n if n else 0
        viol = sum(len(r["must_not_violations"]) for r in items)
        return {
            "n": n,
            "rank1": round(100.0 * rank1 / n, 1),
            "topN": round(100.0 * topn / n, 1),
            "mrr": round(mrr, 3),
            "must_not_violations": viol,
        }

    overall = agg([r for items in by_suite.values() for r in items])
    suites = {sid: agg(items) for sid, items in sorted(by_suite.items())}

    if args.json:
        print(json.dumps({
            "corpus_skills": len(skills),
            "overall": overall,
            "suites": suites,
            "details": {sid: items for sid, items in sorted(by_suite.items())},
        }, indent=2))
    else:
        print(f"corpus skills indexed : {len(skills)}")
        print(f"scenarios scored      : {overall['n']}")
        print(f"rank-1 hit rate       : {overall['rank1']}%")
        print(f"top-N hit rate        : {overall['topN']}%")
        print(f"MRR                   : {overall['mrr']}")
        print(f"must-not violations   : {overall['must_not_violations']}")
        for sid, a in suites.items():
            print(f"  {sid}: n={a['n']} rank1={a['rank1']}% topN={a['topN']}% "
                  f"mrr={a['mrr']} viol={a['must_not_violations']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
