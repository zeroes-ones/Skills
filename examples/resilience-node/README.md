# Resilience Design — The Second Real Agentic Run

> **What this is.** The first skill built from
> [`docs/missing-skills-research.md`](../../docs/missing-skills-research.md) — `resilience-pattern-engineer`
> — run as a **real agentic node** with `AGENT_FALLBACK=0`, exactly as Phase 1 proved
> `senior-dev-loop`. Archived here because the run produced a genuinely interesting result:
> **the agent refused to fabricate, and the default engine still reported success.**

## The run

```bash
python3 scripts/workflow-runner.py \
  --manifest examples/resilience-node/resilience-design.yaml \
  --executor scripts/executors/agent_executor.py \
  --guardrail scripts/lib/guardrails.py \
  --memory examples/resilience-node/memory \
  --state examples/resilience-node/run-state.json
# with: AGENT_CMD='claude -p' AGENT_FALLBACK=0
```

Graph: `design` (resilience-pattern-engineer) → `verify` (chaos-engineer) → `human-gate`.

Result: **runner exit=0**, outcome `complete`, 3 steps, effectiveness **85/100**, SLI escalation rate **0.00**.

## What the agent actually did

All three turns are real model calls (`fallback=false`). Verdicts:

| Node | Skill | Verdict | What it did |
|------|-------|---------|-------------|
| `design` | `resilience-pattern-engineer` | **`changes_requested`** | **Refused to produce a design**, invoking the skill's own pre-generation guardrails: the contract declares `inputs: [architecture, dependency-inventory]` and neither was provided |
| `verify` | `chaos-engineer` | `changes_requested` | Verified there was nothing to verify: handoff payload `null`, `artifacts` empty |
| `human-gate` | — | `changes_requested` | Reviewed the run and reported the same |

**This is the skill working as designed.** Its `## Verification Guardrails` section says pre-generation
requires a dependency inventory and a stated deadline; the agent checked, found them absent, and
declined. A skill that produced a plausible-looking resilience plan from no inputs would be worse
than useless — it would be confidently wrong.

## The finding: refusal is not failure

With the **default** engine, the run reported `outcome: complete` — despite **every node returning
`changes_requested`** and no plan being produced.

Why: `design` was marked `status=done` (the executor returned a well-formed result; the *verdict*
was negative), and the loop-less graph advanced to the gate. The gate auto-approved (gap A4), so the
terminal state was reached and `complete` was reported.

**A run where nothing was produced looked identical to a run where everything succeeded.** That is
the exact failure class the enforcement work was built for — and here it is, caught on a real run
rather than a synthetic one.

## The same manifest with enforcement on

```bash
python3 scripts/workflow-runner.py \
  --manifest examples/resilience-node/resilience-design.yaml --enforce-contracts
```

```
[contract-warning] design: declared artifacts.outputs not produced: resilience-plan
[contract]         design: completion.evidence is 'required' but the node reported no evidence;
                           completion.criteria declares 4 criteria (c1, c2, c3, c4) but the node
                           reported no criteria_met coverage

design   status=needs_review   verdict=contract-violation
verify   status=pending        verdict=None      ← never advanced
```

Now the graph **stops**. `design` is not marked done, the downstream node never runs, and the reason
is named. The refusal that was previously invisible is now the run's headline.

| | Default | `--enforce-contracts` |
|---|---|---|
| `design` | `done` / `changes_requested` | **`needs_review` / `contract-violation`** |
| `verify` | ran anyway | **never ran** |
| Run outcome | `complete` | stops at the violation |
| Reason named? | no | yes — missing evidence + 4 uncovered criteria + missing declared output |

## Why this matters for the remaining fifteen skills

This run is the strongest argument yet for the plan's sequencing (§8 of the research doc): **build one,
run it for real, then scale.** Two things surfaced here that no amount of authoring would have
revealed:

1. **The skill's guardrails fire correctly** — it refuses on missing inputs. That is a *good* outcome
   and it only became visible by running it.
2. **The platform's default still papers over refusals.** Enforcement is the difference between a
   refusal being recorded and a refusal being *acted on*. Any workflow that runs these skills
   unattended should run with `--enforce-contracts`.

## Archived evidence

| File | What it is |
|------|------------|
| `resilience-design.yaml` | The manifest (also validated by `validate-workflows.py`) |
| `run-state.json` | Default-mode run: all three nodes `done`, verdicts `changes_requested` |
| `run-state-enforced.json` | Same manifest with `--enforce-contracts`: `contract-violation`, `verify` never ran |
| `agent-transcript.jsonl` | One JSON line per real agent turn (all `fallback=false`) |
| `run-traces.jsonl` | OTel-shaped spans |
| `effectiveness.txt` | **85/100** for the default run |
| `sli-report.txt` | 2 runs, 0 escalated, escalation rate 0.00 |
| `memory/` | Durable run-memory entries |

## Reproduce

```bash
cd <repo root>
AGENT_CMD='claude -p' AGENT_FALLBACK=0 \
  python3 scripts/workflow-runner.py \
    --manifest examples/resilience-node/resilience-design.yaml \
    --executor scripts/executors/agent_executor.py \
    --guardrail scripts/lib/guardrails.py \
    --state examples/resilience-node/run-state.json

# and the enforcement comparison
python3 scripts/workflow-runner.py \
  --manifest examples/resilience-node/resilience-design.yaml --enforce-contracts
```

## Honest limits

- **This does not prove the skill produces a *good* resilience plan** — the agent declined before
  producing one, because the run supplied no architecture or dependency inventory. That is correct
  behaviour, but it means the skill's *output quality* remains unverified by this run.
- To verify output quality, re-run with real inputs: a dependency inventory and a stated deadline in
  the run context. That is the next experiment.
- The `85/100` score is for a run that produced nothing. **The score is not a quality measure** — it
  measures process hygiene (reached terminal state, clean log, exit by design, handoff present). This
  run is the clearest evidence yet that the score needs to be read alongside node verdicts, not
  instead of them.
