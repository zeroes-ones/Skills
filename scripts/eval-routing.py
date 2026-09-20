#!/usr/bin/env python3
"""eval-routing.py — canonical routing evaluator (stdlib only, Tier 2).

Routing over each skill's indexable profile. Algorithm: light suffix
normalization -> field-weighted BM25 (BM25F) -> negative-trigger discount.
Indexed fields per skill and their weights:

  - name + description + tags  (3.0 / 1.0 / 1.0)  — the head field
  - the body's "When to Use" section (1.5)
  - the FULL skill body (0.02)  — the long tail the cosine router never saw

Why the body field: the previous cosine-TF router indexed only name, description,
tags and the "When to Use" section, so ~95% of body vocabulary was unreachable.
Measured on this corpus (327 skills): descriptions average 77.6 tokens while
bodies average 1538.9 UNIQUE tokens. Everything a skill actually teaches —
the error decoder, the anti-patterns, the gotchas — was invisible to the router.

Honest measured result (2026-09-19, 63 unchanged scenarios): overall rank-1
55.6% -> 58.7%, top-N 63.5% -> 71.4%, MRR 0.618 -> 0.672, must-not 5 -> 6,
adversarial rank-1 0.0% -> 14.3%. On the 49-scenario core suite rank-1 is
UNCHANGED at 71.4% and top-N unchanged at 81.6%: the whole overall gain is the
body field reaching 2 of 14 paraphrased adversarial prompts. Two suites regress
(routing-product-strategy 42.9% -> 14.3%, routing-quality-security 100% -> 83.3%).
See the RANK1_FLOOR block below and docs/benchmarks-vs-agent-skills.md for the
full per-suite table — this is a thin improvement, not a solved problem.

Negative routing: each skill's own `Do NOT use` clause (326/327 skills declare
one, mean 19 tokens) is tokenized into a negative set and the score is discounted
by NEG_WEIGHT x the share of the query's IDF mass that lands in it:

    final = max(0, bm25 * (1 - NEG_WEIGHT * share))

Query expansion is deliberately NOT implemented. A free PPMI co-occurrence
expansion was prototyped and measured on this same scorer and set: rank-1 falls
58.7% -> 36.5%, adversarial 14.3% -> 7.1%, MRR 0.672 -> 0.506. High-PPMI pairs
are corpus idioms ("skill", "agent") that pull every prompt toward the same hub
skills, so the expansion costs ~22 pp and buys nothing.

Scores every scenario in evals/tier2-routing-evals.json (core 49) plus
evals/tier2-routing-adversarial.json (semantic, keyword-poor prompts), with
per-case allow_top_n, reporting per-suite and overall:

    rank-1 hit rate, top-N hit rate, MRR,
    must-not violations (false activations), expected-missing rate

This is the single canonical routing number the repo publishes. It is a lexical
router: the adversarial suite is a lexical-unlearnable paraphrase set, and no
configuration here clears it (12 of 14 remain wrong). That needs an embedder.

Usage:
    python3 scripts/eval-routing.py                 # text report
    python3 scripts/eval-routing.py --json          # machine-readable
    python3 scripts/eval-routing.py --suite <id>    # single suite
    python3 scripts/eval-routing.py --check         # gate on RANK1_FLOOR
    python3 scripts/eval-routing.py --grid          # re-run the tuning grid

Exit: 0 for the reporting modes. With --check, 1 when overall rank-1 falls
below RANK1_FLOOR (documented at its definition below).
"""

import argparse
import glob
import itertools
import json
import math
import os
import random
import re
import statistics
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


# Each skill declares what it is NOT for in its description; that clause is the
# skill's own negative routing signal. Mirrors scripts/run-routing-evals.js:235.
_DO_NOT_USE_RE = re.compile(r"Do NOT use[^.]*(?:\.[^.]*){0,3}", re.I)


def do_not_use_text(desc):
    m = _DO_NOT_USE_RE.search(desc or "")
    return m.group(0) if m else ""


# --- BM25F ----------------------------------------------------------------
# Field weights. Tuned by grid search over the committed scenarios; see the
# tuning note on RANK1_FLOOR. The body weight is deliberately small: BM25
# length-normalizes fields inside the doc, but a long field still accumulates
# mass across the document, so 'bodies matter' is not the same as 'bodies at
# parity' — measured, body_w 1.0 costs ~8 pp rank-1 versus body_w 0.02.
FIELD_WEIGHTS = {"name": 3.0, "desc": 1.0, "tags": 1.0, "wtu": 1.5, "body": 0.02}
FIELDS = ("name", "desc", "tags", "wtu", "body")
K1 = 1.4
B = 0.6
NEG_WEIGHT = 0.5


def build_index(tokens_by_field, neg_sets):
    """Return the BM25F lookup structures for a corpus.

    df is the UNION document frequency: a token counts once per document no
    matter how many fields it appears in, which is what `df(t)` means in the
    IDF term. `post` maps a token to {doc_key: {field: count}} so scoring only
    visits documents that actually contain the term.
    """
    keys = list(tokens_by_field[FIELDS[0]].keys())
    n = len(keys)
    counts = {f: {} for f in FIELDS}
    for f in FIELDS:
        for k in keys:
            c = {}
            for t in tokens_by_field[f][k]:
                c[t] = c.get(t, 0) + 1
            counts[f][k] = c
    post = {}
    df = {}
    for k in keys:
        seen = set()
        for f in FIELDS:
            for t in counts[f][k]:
                post.setdefault(t, {}).setdefault(k, {})[f] = counts[f][k][t]
                seen.add(t)
        for t in seen:
            df[t] = df.get(t, 0) + 1
    idf = {t: math.log(1 + (n - v + 0.5) / (v + 0.5)) for t, v in df.items()}
    lens = {f: {k: len(tokens_by_field[f][k]) for k in keys} for f in FIELDS}
    avg = {f: (sum(lens[f].values()) / n if n else 0.0) for f in FIELDS}
    norm = {k: sum(FIELD_WEIGHTS[f] * lens[f][k] / avg[f]
                   for f in FIELDS if FIELD_WEIGHTS[f] and avg[f]) for k in keys}
    return {"keys": keys, "post": post, "idf": idf, "norm": norm,
            "neg": {k: neg_sets[k] for k in keys}}


def bm25f(query_tokens, index):
    """BM25F score per doc key: sum_t IDF(t) * f_d(t) * (k1+1) / (f_d(t) + k1*K)."""
    scores = {k: 0.0 for k in index["keys"]}
    for t in set(query_tokens):
        idf = index["idf"].get(t, 0.0)
        if idf <= 0.0:
            continue
        for k, field_counts in index["post"].get(t, {}).items():
            f = sum(FIELD_WEIGHTS[fl] * field_counts.get(fl, 0)
                    for fl in FIELDS if FIELD_WEIGHTS[fl])
            scores[k] += idf * f * (K1 + 1) / (f + K1 * (1 - B + B * index["norm"][k]))
    return scores


def negative_share(query_tokens, index, key):
    """IDF-weighted share of the query's mass that lands in this skill's neg set."""
    neg = index["neg"].get(key, frozenset())
    num = den = 0.0
    for t in set(query_tokens):
        idf = index["idf"].get(t, 0.0)
        if idf <= 0.0:
            continue
        den += idf
        if t in neg:
            num += idf
    return num / den if den else 0.0


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


RANK1_FLOOR = 55.0
"""Overall rank-1 floor asserted by --check, plus the 2026-09-19 tuning record.

Chosen configuration (grid-searched over the 63 committed scenarios via
`--grid`): FIELD_WEIGHTS name=3.0 desc=1.0 tags=1.0 wtu=1.5 body=0.02,
K1=1.4, B=0.6, NEG_WEIGHT=0.5.

Measured against the previous cosine-TF router on the same unchanged scenarios:

    metric                  cosine-TF   BM25F
    overall rank-1 (63)         55.6%   58.7%
    overall top-N (63)          63.5%   71.4%
    overall MRR                0.618   0.672
    must-not violations            5       6
    adversarial rank-1          0.0%   14.3%

Read that table carefully: on the 49-scenario core suite (the view the node
runner gates on) rank-1 is UNCHANGED at 71.4% and top-N unchanged at 81.6%;
the whole overall delta comes from the 14 adversarial scenarios going 0/14 to
2/14. The body field earns its place by reaching paraphrased prompts whose
content words appear in a skill's body but not its description — a real
retrieval improvement, but a thin one. Do not read this file as a claim that
BM25F solved routing.

The one regression is a must-not violation: `route-release-planning` now
returns `release-manager` at rank 1, where the cosine router did not. Six
distinct scenarios violate across the corpus; four are the trading-finance
futures/options adjacency that was already violating before.

Also regressed, and not hidden: routing-product-strategy (42.9% -> 14.3%) and
routing-quality-security (100% -> 83.3%). The product-strategy loss is BM25's
IDF punishing common-but-needed words: `cto-advisor` loses "build-vs-buy for
our authentication system" partly to `home-buying` on the token `buy`. No grid
configuration recovered that suite above 14.3% while keeping BM25 IDF.

Why the floor is 55.0%: the previous router measured 55.6%, so a floor at or
below that would be vacuous. 55.0% was chosen only after checking that every
BM25F variant in the grid lands at 55.6% or above, so the floor still admits
the worst honest configuration while tolerating corpus drift. It is a
regression gate, not an aspirational target — the targets in
docs/B6-ROUTING-SCOPE.md (75% rank-1, 50% adversarial) remain unmet.

Anti-overfit note: rank-1 gaps of one or two scenarios inside this grid are
noise, not signal. Bootstrap over 63 scenarios gives a standard deviation of
~6 pp. The best point estimate the grid produces (60.3%) collapses back to
55.6% when body_w moves from 0.03 to 0.04, so it was not shipped. The chosen
configuration sits on a plateau: at body_w 0.02 with wtu 1.5, every measured
{k1, b} pair returns 58.7%, and its leave-one-suite-out minimum is 52.7%.

Rejected: free PPMI query expansion. Prototyped and measured on this scorer and
set, PPMI over head-field co-occurrence drops rank-1 58.7% -> 36.5%, adversarial
14.3% -> 7.1%, MRR 0.672 -> 0.506, because the highest-PPMI pairs are corpus
idioms shared by every hub skill. Net cost ~22 pp with no gain, so it is not
implemented.

Also measured and NOT shipped: keeping the old IDF `log(1 + N/df)` instead of
BM25's `log(1 + (N - df + 0.5)/(df + 0.5))` lifts rank-1 to 68.3% / MRR 0.752
and recovers product-strategy to 42.9%, but doubles must-not violations to 10.
It is documented here as an alternative for whoever is willing to trade false
activations for rank-1.

Not achievable under stdlib-only: routing-semantic-adversarial. Those prompts
are paraphrased so that no distinctive term survives; 12 of 14 remain wrong
under every lexical configuration measured. Clearing that suite needs an
embedding model, not a better lexical formula.
"""


def score_corpus(skills, cases, weights=None, k1=None, b=None, neg_weight=None):
    """Rank every case under an explicit configuration. Used by --grid tuning.

    `weights` overrides FIELD_WEIGHTS for the term-saturation term only; the
    length normalizer always uses FIELD_WEIGHTS, so the grid moves the body's
    vote without also moving every document's length penalty.
    """
    weights = weights or FIELD_WEIGHTS
    k1 = K1 if k1 is None else k1
    b = B if b is None else b
    neg_weight = NEG_WEIGHT if neg_weight is None else neg_weight
    by_field = {f: {} for f in FIELDS}
    neg_sets = {}
    for s in skills:
        k = s["name"]
        by_field["name"][k] = tokenize(k)
        by_field["desc"][k] = tokenize(s["desc"])
        by_field["tags"][k] = tokenize(" ".join(s["tags"]))
        by_field["wtu"][k] = tokenize(section_text(s["body"], ["when to use"]))
        by_field["body"][k] = tokenize(s["body"])
        neg_sets[k] = frozenset(tokenize(do_not_use_text(s["desc"])))
    index = build_index(by_field, neg_sets)
    saved = dict(FIELD_WEIGHTS)
    FIELD_WEIGHTS.update(weights)
    try:
        out = []
        for c in cases:
            qtokens = tokenize(c["prompt"])
            scored = []
            for k in index["keys"]:
                raw = 0.0
                for t in set(qtokens):
                    idf = index["idf"].get(t, 0.0)
                    if idf <= 0.0:
                        continue
                    fc = index["post"].get(t, {}).get(k)
                    if not fc:
                        continue
                    f = sum(FIELD_WEIGHTS[fl] * fc.get(fl, 0)
                            for fl in FIELDS if FIELD_WEIGHTS[fl])
                    raw += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * index["norm"][k]))
                share = negative_share(qtokens, index, k)
                scored.append((max(0.0, raw * (1.0 - neg_weight * share)), k))
            ranked = sorted(scored, reverse=True)
            ranked = [(n, sc) for sc, n in ranked]
            top_names = [n for n, _ in ranked[:c["allow_top_n"]]]
            rank = next((i for i, (n, _) in enumerate(ranked) if n == c["expected"]), -1)
            out.append({
                "suite": c["suite"],
                "rank1_hit": bool(top_names) and top_names[0] == c["expected"],
                "topN_hit": c["expected"] in top_names,
                "mrr": 1.0 / (rank + 1) if rank >= 0 else 0.0,
                "must_not_violations": [n for n in c["must_not_route"] if n in top_names],
            })
        return out
    finally:
        FIELD_WEIGHTS.clear()
        FIELD_WEIGHTS.update(saved)


def run_grid(skills, cases):
    """Report the tuning grid so the chosen config can be re-derived, not trusted.

    Includes the anti-overfit columns: leave-one-suite-out minimum rank-1 and a
    bootstrap standard deviation over scenario resamples, both of which show
    that single-scenario gaps inside this grid are noise.
    """
    suites = sorted({c["suite"] for c in cases})
    grid = {"k1": (1.0, 1.4, 2.0), "b": (0.3, 0.6, 0.9),
            "body": (0.0, 0.02, 0.05, 0.1, 1.0), "wtu": (0.0, 1.5)}
    rows = []
    for k1, b, body, wtu in itertools.product(grid["k1"], grid["b"], grid["body"], grid["wtu"]):
        w = dict(FIELD_WEIGHTS, body=body, wtu=wtu)
        res = score_corpus(skills, cases, weights=w, k1=k1, b=b)
        n = len(res)
        r1 = 100.0 * sum(1 for r in res if r["rank1_hit"]) / n
        loso = min(100.0 * sum(1 for r in res if r["suite"] != h and r["rank1_hit"])
                   / len([r for r in res if r["suite"] != h]) for h in suites)
        rng = random.Random(11)
        boot = statistics.stdev([100.0 * sum(1 for r in (res[rng.randrange(n)]
                                                         for _ in range(n)) if r["rank1_hit"]) / n
                                 for _ in range(200)])
        rows.append((r1, loso, -boot, k1, b, body, wtu))
    rows.sort(reverse=True)
    print(f"{'k1':>4} {'b':>4} {'body_w':>7} {'wtu_w':>6} {'rank1':>7} {'LOSO_min':>9} {'boot_sd':>8}")
    for r1, loso, nb, k1, b, body, wtu in rows[:12]:
        print(f"{k1:>4} {b:>4} {body:>7} {wtu:>6} {r1:>6.1f}% {loso:>8.1f}% {-nb:>8.1f}")
    print(f"\nchosen: k1={K1} b={B} body_w={FIELD_WEIGHTS['body']} "
          f"wtu_w={FIELD_WEIGHTS['wtu']} (see RANK1_FLOOR for why)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--suite", default=None)
    ap.add_argument("--check", action="store_true",
                    help=f"exit 1 if overall rank-1 < {RANK1_FLOOR}%%")
    ap.add_argument("--grid", action="store_true", help="re-run the tuning grid")
    args = ap.parse_args()

    skills = collect_skills()
    names = {s["name"] for s in skills}

    if args.grid:
        cases = load_cases(args.suite)
        if not cases:
            print("no scenarios found", file=sys.stderr)
            return 2
        return run_grid(skills, cases)

    # Five tokenized fields per skill. The body is indexed in full; FIELD_WEIGHTS
    # decides how much of a vote each field gets. Document keys are skill names.
    by_field = {f: {} for f in FIELDS}
    neg_sets = {}
    for s in skills:
        k = s["name"]
        by_field["name"][k] = tokenize(k)
        by_field["desc"][k] = tokenize(s["desc"])
        by_field["tags"][k] = tokenize(" ".join(s["tags"]))
        by_field["wtu"][k] = tokenize(section_text(s["body"], ["when to use"]))
        by_field["body"][k] = tokenize(s["body"])
        neg_sets[k] = frozenset(tokenize(do_not_use_text(s["desc"])))
    index = build_index(by_field, neg_sets)

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
        qtokens = tokenize(c["prompt"])
        raw = bm25f(qtokens, index)
        scored = []
        for k in sorted(names):
            share = negative_share(qtokens, index, k)
            scored.append((max(0.0, raw[k] * (1.0 - NEG_WEIGHT * share)), k))
        # Sort by (score, name) descending: score first, ties by name descending —
        # the historical tie-break, kept so per-case rankings stay comparable with
        # the published baseline. Converted to (name, score) for the report below.
        ranked = sorted(scored, reverse=True)
        ranked = [(n, s) for s, n in ranked]
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

    if args.check:
        ok = overall["rank1"] >= RANK1_FLOOR
        # stderr so `--json --check` keeps stdout parseable.
        print(f"{'PASS' if ok else 'FAIL'}: overall rank-1 {overall['rank1']}% "
              f"{'>=' if ok else '<'} floor {RANK1_FLOOR}%", file=sys.stderr)
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
