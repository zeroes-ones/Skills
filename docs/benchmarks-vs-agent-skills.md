# Routing Benchmark — Reproducible

How this library's skill routing is measured, the numbers it publishes, and how to
reproduce or re-score any peer corpus with the same harness.

> Scope: this is the **lexical floor** — the deterministic, stdlib-only router. It is
> *not* the semantic router. The two live in different layers: an agent using the
> library routes through `using-agent-skills` + skill descriptions (the model is the
> semantic router); this benchmark measures how far a zero-cost lexical index can get on
> the same task set, so "routing improved" is data, not prose.

## 1. Measured results

### 1a. Held-out lexical baseline (`scripts/benchmark-skills.py`)

10 unambiguous held-out tasks, query → expected skill, scored by lexical overlap over
each skill's indexed profile (name + description + tags).

| Metric | Before | After | Δ |
|---|---|---|---|
| Top-1 | 3/10 (30%) | **5/10 (50%)** | +2 |
| Top-5 | 6/10 (60%) | 6/10 (60%) | 0 |

`scripts/build-skill-index.py --eval` runs the identical baseline and prints the same
numbers (50% / 60%).

What changed: hyphen-split tokenization (so `fullstack` now matches
`fullstack-developer`) and the skill's `tags` were added to the indexed profile. The
remaining five misses are cases where the expected skill's own name + description +
tags share no distinctive vocabulary with the prompt (e.g. *"respond to a production
outage and write an incident report"* → `incident-responder`, whose profile lacks
`outage` / `production` / `report`; *"define the REST endpoints and error model for a
new domain"* → `api-designer`, whose profile lacks `endpoint`). Those are
description/tag under-specification, fixable by enriching the profile or by the
semantic router (see §4).

### 1b. Canonical evaluator (`scripts/eval-routing.py`)

63 scenarios = 49 core (`evals/tier2-routing-evals.json`) + 14 semantic-adversarial
(`evals/tier2-routing-adversarial.json`), unchanged test sets. TF-IDF over each skill's
indexed fields with per-field IDF; metrics rank-1 / top-N / MRR / must-not violations.

| Config | rank-1 | top-N | MRR | must-not |
|---|---|---|---|---|
| A. Historical baseline (desc+tags, pre-fix parser) | 42.9% | 60.3% | 0.531 | 7 |
| B. Parser fix only (tags now load) | 47.6% | 65.1% | 0.576 | 8 |
| C. **Parser fix + index upgrade (published)** | **55.6%** | **66.7%** | **0.624** | **6** |

Final suite-level (config C):

| Suite | n | rank-1 | top-N | MRR | viol |
|---|---|---|---|---|---|
| routing-core-development | 8 | 100.0% | 100.0% | 1.000 | 0 |
| routing-quality-security | 6 | 100.0% | 100.0% | 1.000 | 1 |
| routing-design-ux | 6 | 83.3% | 100.0% | 0.917 | 0 |
| routing-devops-infra | 6 | 83.3% | 100.0% | 0.889 | 0 |
| routing-trading-finance | 6 | 83.3% | 100.0% | 0.889 | 3 |
| routing-negative-triggers | 4 | 50.0% | 50.0% | 0.543 | 1 |
| routing-product-strategy | 7 | 42.9% | 57.1% | 0.546 | 1 |
| routing-meta-disambiguation | 6 | 16.7% | 50.0% | 0.296 | 0 |
| routing-semantic-adversarial | 14 | 0.0% | 7.1% | 0.096 | 0 |
| **Overall** | **63** | **55.6%** | **66.7%** | **0.624** | **6** |

### 1c. What changed, and why it is not cherry-picking

Three independent, general changes, each measured separately on the same test sets:

1. **YAML parser correctness (`scripts/yaml_shim.py`, `scripts/_compile_skill.py`).**
   Flush-left block bullets (`tags:\n- api`) were silently dropped by both stdlib
   parsers, so tag vocabulary was missing from routing profiles in any environment
   without PyYAML — including this one. The parsers now accept indented and flush-left
   bullets, matching PyYAML (CI). Row A → B: +4.7 pp rank-1 from loading existing data.
2. **Index profile upgrade (`scripts/eval-routing.py`, mirrored in
   `scripts/run-routing-evals.js`).** Indexed fields per skill: name (anchor) +
   description + tags at weight 1.0, plus the body's own "When to Use" section at
   weight 0.15 (own IDF). Light suffix normalization (`minimizing`/`minimize` →
   `minimiz`). Row B → C: +8.0 pp rank-1, −2 violations.
3. **Lexical baseline tokenization (`scripts/benchmark-skills.py`,
   `scripts/build-skill-index.py`).** Hyphen splitting on both sides + tags in the
   profile: Top-1 30% → 50%.

### 1d. The adversarial ceiling (honest)

`routing-semantic-adversarial` deliberately paraphrases away every distinctive term
(*"A third of our CI runs fail on tests that pass locally, and the failing test moves
around run to run"* → `qa-engineer`; *"the user asks us to delete everything we hold"* →
`gdpr-privacy`). After normalization only high-frequency words survive (`fail`, `run`,
`test`), which no lexical index can discriminate: rank-1 stays 0.0%. This suite exists
to prove that point and to gate the semantic build (`docs/B6-ROUTING-SCOPE.md` targets
≥ 50% there with an embedder). Treat 55.6% / 0.0% as the lexical floor, not a product
ceiling.

## 2. Reproduce

```bash
# Held-out lexical baseline (10 tasks) — also refreshes COMPARISON.md's measured block
python3 scripts/benchmark-skills.py --root skills --markdown
python3 scripts/benchmark-skills.py --root skills --update COMPARISON.md
python3 scripts/build-skill-index.py --eval

# Canonical evaluator (63 scenarios incl. adversarial)
python3 scripts/eval-routing.py            # text report
python3 scripts/eval-routing.py --json     # machine-readable (per-suite + per-case)

# Node runner (same algorithm; used by scripts/run-evals.sh tier 2)
node scripts/run-routing-evals.js
```

Environment note: `scripts/eval-routing.py` imports `yaml_shim` (stdlib YAML subset)
rather than PyYAML so it runs anywhere; after the parser fix its tag parsing matches
PyYAML on this corpus. The JS runner mirrors the same index profile for parity.

## 3. Scoring a peer corpus with the same harness

Corpus-level metrics (count, load cost, structure, portability) score any peer layout:

```bash
python3 scripts/benchmark-skills.py --root skills --markdown            # this library
python3 scripts/benchmark-skills.py --root <peer>/skills --shallow      # addyosmani-style layout
python3 scripts/benchmark-skills.py --root <peer-dir> --flat            # flat prompt dir
```

Routing rows are omitted for peers: their skill names do not match this library's
held-out task set, so a cross-corpus routing comparison would not be apples-to-apples.
The honest cross-repo comparison stays corpus-level (see `COMPARISON.md` measured
table); the routing benchmark above is this library's own regression floor, run
informational in CI (`validate.yml` → "Routing baseline (informational)").

## 4. Relationship to the semantic build (B6)

`docs/B6-ROUTING-SCOPE.md` scopes the embedding-based router and its acceptance gates.
Its "Current (lexical)" column now reads the numbers in §1b; the hard gate there is
**monotone improvement over this lexical floor on the same scenarios** — any future
router must beat 55.6% rank-1 / 0.624 MRR and keep must-not violations ≤ 2% before it
may replace the floor. These results raise the floor; they do not retire the semantic
target (≥ 75% rank-1, ≥ 50% adversarial).

## 5. Data-quality note

9 of 303 skills carry no `tags` (finance cluster: `commodities-analyst`,
`crypto-trader`, `fixed-income-analyst`, `macro-strategist`, `trade-performance-analyst`,
plus `mock-data-sync`, `nonprofit-fundraising-engineer`, `pricing-purchase-optimizer`,
`source-driven-development`). Their routing profiles rely on name + description only;
adding tags is a cheap future lift.
