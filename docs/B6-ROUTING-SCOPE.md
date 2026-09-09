# B6 — Semantic Skill Retrieval & Routing: Build Scope

Status: **scoped, not executed** — execution requires an embedding/model-API environment
(no node, no API keys in the offline sandbox). Per project rules, any behavioral-lift claim
from this build is an **architectural hypothesis until measured** against the canonical
baseline below.

Source: Frontier B6 of `BEYOND-LOOPS-GRAPHS.md`.

## 1. Why

- Canonical routing baseline (63 scenarios, `scripts/eval-routing.py`, committed):
  **rank-1 55.6%** (core-49: 71.4%), top-N 66.7%, MRR 0.624, 6 must-not violations.
  Raised from 42.9% / 60.3% / 0.531 / 7 by the 2026 routing pass (index profile upgrade
  + YAML parser fix); full attribution and reproduction in
  `docs/benchmarks-vs-agent-skills.md`.
- Semantic-adversarial suite (keyword-poor prompts): **rank-1 0.0%** — lexical matching
  fails on meaning. Any retrieval upgrade must be gated on beating these numbers, not on
  vibes.
- Static routers stop scaling: 298 skills today, thousands tomorrow.

## 2. Design

```
query
  → embed(query)
  → top-K over skill index (K=25)
  → rerank (cross-encoder or light transformer over {query, name, description, tags})
  → chain-aware bundle expansion (add prerequisite skills via chain.consumes_from)
  → select smallest sufficient set
  → routing eval
```

Index corpus: skill **bodies** + descriptions + tags (research: body > metadata; the
frontmatter description alone under-specifies scope). Optional embedder: stdlib TF-IDF
baseline stays the floor; a real embedder is an environment-provided model API
(`scripts/build-skill-index.py` is the current lexical baseline).

## 3. Evaluation protocol (unchanged test sets — no cherry-picking)

- `evals/tier2-routing-evals.json` (49 core scenarios, incl. negative triggers)
- `evals/tier2-routing-adversarial.json` (14 semantic, keyword-poor)
- Metrics: rank-1 / top-N / MRR / must-not violations (false activation) / missing-skill
  rate; plus **tokens-per-task vs full-load** (the "effective context" story).
- Run via `scripts/eval-routing.py --json` with a pluggable scorer interface behind
  `route(query) -> [(skill, score)]`.

## 4. Acceptance (block merge on failure)

| Metric | Current (lexical) | Target |
|---|---|---|
| Rank-1 (63 scenarios) | 55.6% | ≥ 75% (and strictly > lexical) |
| Rank-1 (adversarial) | 0.0% | ≥ 50% |
| MRR | 0.624 | ≥ 0.80 |
| Must-not violations | 6 | ≤ 2% of scenarios |
| Tokens/task vs full load | n/a (router unmeasured) | ≤ 25% of full-load tokens at ≥ baseline quality |

Thresholds are starting points; the hard gate is **monotone improvement over the lexical
floor on the same scenarios** — a fancier router that loses to TF-IDF is reverted.

## 5. Build order

1. Add a `Router` interface (`route(query, k) -> ranked`) with the current TF-IDF as the
   reference implementation; wire `eval-routing.py` to score any router.
2. Implement rerank on the existing TF-IDF top-K (deterministic, stdlib) — measure; keep
   only if it beats the floor.
3. Embedding + rerank behind the same interface (requires model API env).
4. Chain-bundle expansion using `chain.consumes_from`; measure precision/recall of the
   returned bundle vs the expected single skill.

## 6. Dependencies & honest caveats

- Needs: an embedder/API (or an offline model) — not available in the current sandbox.
- Skills 1–3 of the build order are executable without an API and are the first increment.
- No new skill content is required; this is retrieval + measurement only.
