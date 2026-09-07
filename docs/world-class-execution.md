# World-Class Execution Doctrine — Fast, Efficient, 100% Effective, Every Angle

How single-agent, multi-agent, handoffs, and iterative-until-done runs are made as fast and
effective as measured skill systems can be — and how "100% effective" is defined, scored, and
gated. Companion to `examples/efficiency-in-action.md` (token/memory/prompt economics) and
`docs/git-ci-efficiency.md` (resource economy). The differentiator: this doctrine is **measured**,
with `scripts/run-effectiveness.py` turning "effective" into a number.

## 1. What "100% effective" means (and how it is scored)

A run is 100% effective when all seven are true — `scripts/run-effectiveness.py --memory` scores
it out of 100:

| Criterion | Weight | Meaning |
|---|---|---|
| Completion | 25 | Run reached a terminal `complete` state |
| Clean | 20 | No escalation or guardrail block in the log |
| Exit-by-design | 15 | Loop exited on its exit condition, not exhaustion |
| Handoffs | 15 | Final boundary carried a payload (no silent handoff) |
| Questions | 10 | No dangling open questions |
| Budget | 10 | `steps_used <= max_steps` |
| Memory | 5 | Run memory entry written (`--memory`) |

Measured on this repo: the flagship **happy run = 100/100** (with memory), the **exhaustion run =
45/100** (escalation, no exit-by-design, no final payload) and fails a `--threshold 90` gate.
"Done at 100% effectiveness" is therefore: **evidence-backed, escalation-free, budgeted, payload
complete, and memory-written** — not a feeling.

## 2. Speed doctrine, per mode

### Single-agent (fastest path)
1. **Load compiled, not raw.** `.skills-compiled/` skills load at ~3,500 tokens vs ~8,976 raw
   body words (63.4% effective-load saving measured). QUICK-first: read Route + Ground Rules,
   drill down only when needed.
2. **One verify per exit.** Run the verify-node template once with artifact evidence — never
   loop on a claim, never re-read the skill per pass.
3. **Budget = history + 1.** Calibrate `max_iterations` from real passes; a budget that always
   fires is a prediction, not a limit.
4. **Fail cheapest.** A guardrail-block mid-graph stops the rest of the pipeline spending.

### Multi-agent (minimize serial cost)
1. **Parallelize independent nodes with disjoint writers** — `parallel:` + `join: all`; cost
   ≈ max(latency), not sum.
2. **Supervisors route; workers work.** A supervisor node fans out to worker nodes (each worker =
   a sub-agent via `agent_executor.py`) and owns escalation.
3. **Share typed state, not chats.** Every field has one writer; the join merges.
4. **Measure wall-clock:** the engine adds ~100 ms per run; real multi-agent cost is the agent
   LLM leg — spend optimization there (model choice, prompt caching, compaction between hops).

### Handoffs (zero-loss, low-cost)
1. **Payloads, never transcripts.** Nine-key registry (summary/artifacts/decisions/open
   questions/evidence/context/budget…); hash-verified at the boundary; mismatch aborts.
2. **Compact each hop.** Run context compaction between nodes so handoff cost shrinks each hop,
   not grows (context-rot defense).
3. **Open questions travel.** Nothing silently vanishes; a resolved question becomes a decision.

### Iterative-until-done (bounded convergence)
1. **Exit condition on one gatekeeper.** `exit_when: <gatekeeper>.verdict == pass`.
2. **Three brakes, all in code:** `max_iterations`, stagnation detection (identical passes),
   global step budget — the run cannot spin.
3. **Exhaustion escalates with context**, never silent-stops; the escalation itself is the
   handoff to the human gate.
4. **Self-improve the loop:** a run that exhausts becomes a candidate → verifier-gated
   replay → promote or reject (skill-evolve-promote), so future runs converge faster.

## 3. Measured baselines (this repo, 2026-09-07)

| Quantity | Value |
|---|---|
| Engine wall-clock per run (stub) | ~96-100 ms |
| Tool self-tests | validator 177 ms / engine 99 ms / lint 9 checks |
| Effective skill load | 3,545 compiled tokens avg (63.4% saving, 233/297 compiled) |
| Run memory vs full state | ~883 B vs ~3.8 KB (~6× smaller) |
| Flagship effectiveness | happy 100/100 (w/ memory) · exhaust 45/100 |
| Parallel join | gate fires only after all members (guaranteed) |
| Guardrail block | poisoned output never reaches downstream nodes |

## 4. Enforcement "everywhere"

- **Per run:** budgets/stagnation/join/handoff hashes are engine-enforced; effectiveness is
  scored by `scripts/run-effectiveness.py`.
- **Per push:** `repo-self-check.yaml` (workflow-graphs CI job) runs the repo's own gates as a
  graph; golden evals + engine self-tests gate merges.
- **Per project:** `project-init.sh` attaches the same doctrine; `run-ci-locally.sh` mirrors CI
  locally so credits are only spent on final confirmation (docs/git-ci-efficiency.md).
- **Per skill:** incorporation scorecard (`scripts/skill-incorporate.py`) tracks the
  every-skill checklist; new capabilities are generated on demand (`skill-factory.py`) and used
  as nodes/sub-agents.

## 5. The next speed levers (documented, not yet built)

1. **Distribution & registry publishing (best-in-class gap):** publish a flat
   `skills-sh/<name>/SKILL.md` index for skills.sh auto-discovery, add marketplace/plugin
   manifests, and emit `skills-lock.json` from project-init — full plan in
   `docs/distribution-best-in-class.md`.
2. **Span-backend ingest** for live per-project cost/latency dashboards (export-traces is
   import-ready JSONL).
3. **Embedding + rerank routing** over skill bodies — cut load further and beat the 30% lexical
   Top-1 baseline (SkillRouter: bodies, not metadata).
4. **Prompt caching + model tiering** in `agent_executor.py` (fast model for easy nodes, strong
   model for gatekeepers) to shrink the dominant agent-leg cost.
5. **LLM-judge CI** executing the loop-graph behavioral suite as a merge gate.

## 6. The 100% rule

Fast means measured milliseconds; efficient means measured tokens, memory, and retries;
effective means scored 100/100 by `run-effectiveness.py`. If a run cannot show its score, the
definition of done is missing — this doctrine exists so no run in this repo (or a project it
attaches to) ever ships unmeasured.
