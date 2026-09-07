# Self-Incorporation — How the Library Upgrades Itself with Loops, Graphs & Vectors

> The deep answer to: *how can the Skills repo incorporate itself — automatically — so that
> every skill, over time, has the full treatment?* Mechanism + current measured state +
> the every-skill checklist + cadence. The governing idea: incorporation is a **loop**, driven
> by a **graph**, informed by **vectors**, and gated by **verification** — the same stack this
> repo runs on projects, pointed back at itself.

## 1. What "every skill should have" means (the checklist)

| # | Capability | Tool / artifact | Current (measured) |
|---|-----------|-----------------|--------------------|
| 1 | Referenceable as a graph node | any manifest can name it | **297/297** |
| 2 | Default-mode eligibility (Core Workflow + Verification) | audit/coverage | **281/297** |
| 3 | `workflow:` node contract (typed artifacts, criteria, escalation) | frontmatter | **30/297** |
| 4 | Golden regression cases | `evals/golden/<skill>/cases.json` | **3/297** |
| 5 | Retrieval index entry (lexical now, embeddings next) | `build-skill-index.py` | **297/297** |
| 6 | Boundary templates / verify discipline | `workflow/templates/` | by protocol |
| 7 | Run memory + traces + SLIs when executed | `--memory`, `export-traces`, `skill-sli-report` | per run |
| 8 | Verifier-gated self-improvement when it fails | `skill-evolve-prep/promote` | pipeline ready |
| 9 | Portability + lint cleanliness | gates, `lint-workflow` | 100% portable |
| 10 | Cross-OS/any-LLM attach for projects | `project-init.sh` + `agent_executor.py` | ready |

Gap report: run `python3 scripts/skill-incorporate.py` — it prints exactly which of #1-5 each
skill has and the two live gaps: **252 eligible skills still lack a `workflow:` contract**, and
**294 skills lack a golden set**.

## 2. The loop: incorporate → verify → promote (never unverified)

Incorporation is the same audited loop as self-improvement (B3/M1), applied to the checklist:

```
for each skill S (driven by a workflow graph over the library):
   1. INDEX     ensure S is in the retrieval index (rebuild if body changed)
   2. CONTRACT  ensure S carries workflow: (or is default-mode eligible)
   3. EVAL      ensure S has >=1 golden case; run it; record baseline
   4. VERIFY    run S's gates (lint-workflow, golden, engine self-tests)
   5. PROMOTE   only pass-verified states update the published baseline
                (each promotion is audit-ledgered with its source run)
```

Because promotion is verifier-gated, "incorporation" cannot silently degrade a skill: a proposed
contract, golden case, or content fix must survive replay + evals before it counts. Failure runs
feed the same loop — a skill that escalates in production becomes a candidate (B3) whose fix must
pass before promotion.

## 3. The graph: incorporate by running the library on itself

`workflow/manifests/repo-self-check.yaml` already runs the repo's quality gates as a parallel
graph (validate → lints → golden evals → human gate). The full incorporation drive is the same
shape scaled per skill:

- **One manifest per incorporation pass** with nodes like `incorporate:<skill>` (bound to
  `scripts/skill-incorporate.py` and the per-skill lints) — parallel blocks over batches of
  skills, join-all, escalate to a human gate when the pass cannot converge.
- **Loops at the right granularity**: iterate a failing skill's fix-loop until its gates pass or
  the budget escalates; never loop the whole library on one skill's problem.

## 4. The vectors: retrieval that scales to "every skill"

Indexing every skill is table stakes; finding the right skill at runtime is the vector problem
(B6 / next wave):

- **Index every skill body, not just metadata** — research (SkillRouter) shows the body is the
  decisive routing signal (metadata-only drops retrieval 29-44 points). `build-skill-index.py`
  already indexes 297 names + descriptions lexically (Top-1 30% / Top-5 60%); the embedding +
  rerank layer must beat that baseline.
- **Top-K + rerank**, then **dependency-aware bundles**: when a skill is selected, pull its
  prerequisites from the chain graph so a worker gets the whole path, not one node.
- **Auto-re-index on change**: any `SKILL.md` edit re-indexes that skill (hook) so the vector
  store never drifts from the repo.

## 5. Cadence — when incorporation runs

| Trigger | What runs | Cost |
|---------|-----------|------|
| Every commit touching a skill | re-index that skill + lint-workflow + per-skill golden (fast) | seconds |
| Every push / PR | `workflow-graphs` CI job: engine self-tests, golden evals, repo-self-check dogfood | minutes (path-filtered; docs-only pushes skip) |
| Nightly (cron) | full `skill-incorporate.py` + benchmark + SLI over committed checkpoints | cheap, informational |
| On failure anywhere | failure trace → draft inbox → verifier-gated promote (B3/M1) | per incident |

This is also the resource-efficiency answer (see `docs/git-ci-efficiency.md`): run the cheap,
local incorporation steps per commit; spend CI credits once per push; cancel superseded runs;
never let generated indexes/contracts drift from their sources.

## 6. Honest state and next wave

- **Now:** 297/297 referenceable + indexed; 281 default-eligible; 30 contracts; 3 golden sets;
  dogfood + self-improvement loops running; gaps are measured and actionable per skill
  (`skill-incorporate.py` lists them).
- **Next wave:** (a) auto-propose `workflow:` contracts for the 252 eligible skills by
  chain-degree priority (G1 phases 3+), (b) auto-scaffold golden cases for the 294 without them
  (draft from expected_behavior + verify against replay), (c) the embedding + rerank layer over
  bodies to beat the 30% lexical baseline, (d) nightly cron wiring for the incorporate report.

Every item above is a loop, graph, vector, or verification primitive this repo already runs —
pointed at itself.
