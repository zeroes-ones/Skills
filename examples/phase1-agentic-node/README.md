# Phase 1 — Proof That a Node Is an Agentic Skill, Not an API Call

> **Status: measured, passing.** This directory is the archived evidence for Phase 1 of
> [`docs/skill-automation-platform.md`](../../docs/skill-automation-platform.md): one library
> workflow manifest executed end-to-end with a **real agent CLI as the node executor**, so every
> node's content was model reasoning grounded in that node's `SKILL.md` — not a fixed request.

## The run

```bash
cd <repo root>
AGENT_CMD='claude -p' AGENT_FALLBACK=0 \
  python3 scripts/workflow-runner.py \
    --manifest workflow/manifests/senior-dev-loop.yaml \
    --executor scripts/executors/agent_executor.py \
    --guardrail scripts/lib/guardrails.py \
    --memory examples/phase1-agentic-node/memory \
    --state examples/phase1-agentic-node/run-state.json
```

`AGENT_FALLBACK=0` is **mandatory** for any claim made from this run. The executor's default
(`AGENT_FALLBACK=1`) returns a stub `pass` when an agent call fails or times out — a run that
"succeeded" under the default proves nothing about node content. With `0`, a failed call is
surfaced instead of masked.

## Measured result — 3 agent turns, all real

Every turn below is a genuine model call (`fallback=false` in the transcript), each one grounded in
the referenced skill's compiled excerpt injected into its prompt:

| Turn | Node | Skill injected | Skill words | Verdict | Seconds |
|------|------|----------------|-------------|---------|---------|
| 1 | `implement` | `incremental-implementation` | 405 | `changes_requested` | 331.2 |
| 2 | `review` | `code-reviewer` | 1,200 | `pass` | 60.5 |
| 3 | `ship-gate` | — (gate node) | 0 | `pass` | 115.4 |

Run outcome: **`complete`** — the loop exited on its declared `exit_when`
(`review.verdict == pass`) after **1 iteration**, 3 steps used against a budget of 40, and a
registered handoff (`handoff-v1`, sha `176099b50f3b`) crossing the final boundary.

The nodes did not summarise a handoff payload. They read the actual working tree:
`implement` statically verified the in-flight D1/D2 changes and the regenerated
`.sha256manifest`; `review` produced a line-level code review of ~110 changed lines (confirming
`_crash_checkpoint` soundness, that the exception re-raises after checkpointing, and that
`save_state` no-ops on a `None` path). That is the "node is not an API call" claim demonstrating
itself.

## Archived evidence

| File | What it is |
|------|------------|
| `run-state.json` | The checkpoint: per-node status/verdict/iterations, budget, handoff, log |
| `agent-transcript.jsonl` | One JSON line per agent turn (node, verdict, seconds, fallback flag, prompt words, reply excerpt) |
| `run-traces.jsonl` | OTel-shaped spans from `scripts/export-traces.py` (4 spans: session + 3 nodes) |
| `sli-report.txt` | Per-workflow SLIs from `scripts/skill-sli-report.py` — 1 run, 1 complete, **escalation rate 0.00**, avg 3.0 steps |
| `effectiveness.txt` | `scripts/run-effectiveness.py` score: **100/100** (completion 25, clean 20, exit-by-design 15, handoffs 15, no open questions 10, budget 10, memory 5) |
| `memory/senior-dev-loop.jsonl` | Durable run-memory entry (`trust: context_only`) |

Reproduce the observability artifacts:

```bash
python3 scripts/export-traces.py --state examples/phase1-agentic-node/run-state.json
python3 scripts/skill-sli-report.py --dir examples/phase1-agentic-node
python3 scripts/run-effectiveness.py --state examples/phase1-agentic-node/run-state.json --memory
```

## Two defects this run found

The first attempt at this run **failed**, and that failure is why the platform doc carries two
defects. Both are now fixed; the second is guarded by the engine's own test suite.

| ID | Defect | Fix |
|----|--------|-----|
| **D1** | `AGENT_TIMEOUT` defaulted to 90s — a real node took 149.6s, then exceeded 180s, so the default guaranteed spurious timeouts | Default raised to 600s in `scripts/executors/agent_executor.py`, with the measurement recorded in its docstring |
| **D2** | A node raising inside a loop pass propagated out of `run()` and **no run-state was written at all** — two completed nodes were discarded and `--state` resume was impossible for exactly the runs that need it | `Runner._crash_checkpoint()` logs an `action: error` entry and checkpoints *before* re-raising; both execution sites wrapped; regression fixture `t-crash-checkpoint` added to `--selftest` (12 checks, 0 failed) |

D2 is the reason this proof is trustworthy at all: had the second run crashed like the first, the
checkpoint and these artifacts would still exist and the run would resume from the failed node
rather than restarting.

## Known limitation this run exposes

The `ship-gate` node is declared `kind: human`, yet it was **executed as an agent turn** (turn 3
above) because the headless runner has no wait/approval queue. That is gap **A4** in the platform
doc, not a bug in this run — it is why A4 ("human-in-the-loop wait/resume") is a build item rather
than a done item. Until A4 ships, a `kind: human` gate is a *routing* decision point, not a real
pause for a human.

## What this does not prove

- **Not** that the workflow's *output* was correct — that requires the golden-set eval gates
  (frontier B2), not this run.
- **Not** cost/latency accounting: `run-effectiveness.py` and `export-traces.py` carry cost fields
  that a real executor does not yet report (spans record 0 placeholders).
- **Not** unattended reliability at scale — one run, one agent backend (`claude -p`).

## The L2 → L3 delta on one skill

Phase 1 item 3 asks for the difference between a default-mode node and a declared-contract node on
the *same* skill. The run above used `incremental-implementation` as its `implement` node, so it is
the natural specimen: it executed at **L2** (no contract) and now carries an **L3** contract.

| | L2 — default mode (as run) | L3 — declared contract (now) |
|---|---|---|
| Declaration | No `workflow:` block in `SKILL.md` | 12-line block appended to frontmatter |
| Artifacts | Unnamed; inferred from the manifest's `outputs: [change]` | Typed: `inputs: [spec]` → `outputs: [change]` |
| Definition of done | The skill's Verification table, consulted at execution time | Three explicit criteria — flag defaults to false, tests pass in both flag states, ADD-only schema |
| Evidence | Required only by convention | `evidence: required`, declared |
| Exhaustion | The loop's own `escalate_to` was the only routing | Node declares `escalate_to: [human-gate]` |
| Lint | n/a — nothing to lint | `scripts/lib/lint-workflow.py` validates the block |
| Counted by | — | `validate-workflows.py --coverage` readiness |

What the run-state actually recorded for that node:

| | `implement` record in `run-state.json` |
|---|---|
| Fields | `status=done`, `verdict=changes_requested`, `iterations=1`, `evidence=["agent-turn:implement"]`, `summary` (400 chars) |

The evidence is a real agent turn — but it is **undifferentiated**: nothing in the checkpoint says
*which* criterion the verdict was judged against. That is the gap the contract closes: it turns "the
executor returned a verdict" into "the node claims these three named things, and evidence is required
for each".

**The limit was real, and has since been closed — opt-in.** At the time of the run, the engine read
only the manifest's `nodes[].skill` name and never parsed the `workflow:` block, so declared criteria
did not gate anything. That is no longer true: `--enforce-contracts` now asserts `evidence: required`
and requires every declared criterion to be covered by the node's `criteria_met` report, refusing to
mark an unsubstantiated node done. It is **off by default**, because most executors (including the
stub used in tests) do not report per-criterion coverage — so a contract is still reviewability,
lintability, a named escalation target and a readiness metric *unless* you switch enforcement on. See
§6 of [`docs/skill-automation-platform-build-log.md`](../../docs/skill-automation-platform-build-log.md)
for the demonstration.

**Measured effect:** declared contracts went **30 → 43** skills, by adding blocks to 13 of the 14
skills that library manifests and examples exercise but that declared nothing (the fourteenth,
`using-agent-skills`, was reverted — it has no Core Workflow section, so it is not a default-mode node):

```bash
python3 scripts/validate-workflows.py --coverage
# readiness: 301 eligible (default-mode nodes), 43 declared workflow: blocks
```
