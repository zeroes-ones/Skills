# Efficiency in Action — Tokens, Memory, and Prompts Across Loops & Graphs

A worked, **measured** example of how the workflow layer (and the builds beyond it) spend fewer
tokens, smaller memory, and sharper prompts — without losing correctness. Every number below was
measured live on this repository; every command reproduces it.

## The scenario

A project runs `serial-feature-delivery` (spec → architecture → review) or the
`multi-agent-review-graph` (3 reviewers fan out, aggregate verdict, fix loop, human gate). Each
node loads a skill prompt, carries run context, and hands a payload to the next node. Tokens get
spent in exactly four places — and each layer below cuts one of them.

## 1. Prompts — load less, load the right part

**Progressive disclosure:** a full skill body is heavy — `llm-engineer` alone is ~11,100 words.
Agents are told to read Route the Request + Ground Rules first and drill down only when needed, so
a typical routing decision loads a small fraction of the body.

**Compiled artifacts (`.skills-compiled/`)** — measured on this repo:

| Skill | Full (tokens) | Compiled (tokens) | Saving |
|---|---|---|---|
| iterative-task-execution | 5,211 | 1,025 | **80%** |
| workflow-graph-authoring | 5,239 | 1,236 | **76%** |
| agent-handoff-protocol | 12,376 | 2,506 | **80%** |
| llm-engineer | 16,888 | 5,921 | **65%** |

So each node that loads a skill prompt from `.skills-compiled/` instead of the raw body spends
roughly **1/4 to 1/5 the tokens** — with the same working content.

**Short boundary prompts:** the templates in `workflow/templates/` (`verify-node`, `handoff-out`,
…) are 30-50 lines each, not pages — the discipline lives in the runner (code) and the templates
prompt only the judgment call, so every verify/handoff boundary costs a few hundred tokens, not a
re-read of the whole skill.

## 2. Memory — keep the summary, not the transcript

Run memory entries (B1, `--memory`) measured on this repo:

- A completed `quality-fix-loop` run-state checkpoint: **3,843 bytes** (full transcript + log).
- Its structured memory entry: **634 bytes / ~56 words** — a **~6× smaller** durable summary
  carrying workflow, outcome, iterations, per-node verdicts, handoff, counts — tagged
  `trust: context_only`.

Meaning: when the next run asks "did we do this before?", retrieving the memory entry costs ~1/6
the tokens of replaying the run, and it cannot poison the agent (context-only, never instructions).
Handoffs follow the same rule: payloads carry structured summaries + evidence refs, never raw
conversations.

## 3. Loops & graphs — spend a bounded budget, stop early, block cheap

Measured on the flagship graph (all runs 16 steps because budgets bound them):

- **Bounded loops:** `max_iterations: 3` caps spend — the "exhaust" run proves the loop escalates
  at the budget instead of burning tokens forever (no pass 4, 5, …).
- **Stagnation detector:** two identical passes stop the loop early by construction.
- **Parallel join:** reviewers fan out and the gate fires only after the last member — the engine
  guarantees ordering, so no wasted re-review rounds.
- **Edge guardrails (B5):** a poisoned payload is **blocked mid-graph** (`guardrail-block`) —
  the downstream nodes never run, which is the cheapest possible failure (saves the whole
  remaining pipeline's tokens).
- **Prompt-engineering chain:** `agent-efficiency-pass` (using-agent-skills → llm-engineer →
  context-compaction-strategies → token-efficiency) runs headless in **4 steps**, showing the
  context/token skills themselves operate as graph nodes you can compose into any flow.

## 4. Beyond — telemetry keeps the savings honest

- **SLI gate** (`skill-sli-report.py --gate-escalation 0.5`) fails CI when escalation rates climb —
  cost-per-done stays a tracked number, not a hope.
- **Trace spans** (`export-traces.py`) carry `tokens` / `cost` / `latency_ms` slots per node, ready
  for a span backend to turn into per-skill spend dashboards.
- **Self-improvement (M1)** promotes only verifier-passed calibration changes, so budgets
  converge to *history + 1* and future runs stop one-or-two passes early — measured in the
  accept/reject demo (budget 3→6 vs 4).
- **Benchmark** (`benchmark-skills.py`) publishes avg-body load cost and compiled-vs-raw savings
  per corpus (ours vs. measured peers) — the efficiency story is data.

## The efficiency checklist (what to cut, with the measured tool)

| Cost center | Lever | Measured effect |
|---|---|---|
| Skill prompt loading | `.skills-compiled/` + progressive disclosure | 65-80% token reduction |
| Context carried forward | memory entries + handoff payloads (no transcripts) | ~6× smaller than full state |
| Runaway loops | max_iterations + stagnation + step budget | capped by construction (16/16 steps) |
| Bad output propagation | edge guardrails | downstream nodes never run |
| Re-deriving past work | run memory retrieval | ~56 words instead of a re-run |
| Prompt tuning cycles | prompt/context/token skills as nodes | efficiency chain runs in 4 steps |

## Reproduce it

```bash
# compiled savings
python3 - <<'PY'
import json, os
for n in ["iterative-task-execution", "workflow-graph-authoring", "agent-handoff-protocol"]:
    m = json.load(open(".skills-compiled/%s/metadata.json" % n))
    print(n, m["original_tokens"], "->", m["compiled_tokens"], "tokens (%d%%)" % m["reduction_pct"])
PY

# memory entry vs checkpoint size
python3 scripts/workflow-runner.py --manifest workflow/manifests/quality-fix-loop.yaml \
  --memory /tmp/mem > /dev/null && wc -c /tmp/mem/quality-fix-loop.jsonl

# the efficiency chain as graph nodes
python3 scripts/workflow-runner.py --manifest workflow/manifests/agent-efficiency-pass.yaml

# a poisoned payload stopped before the rest of the graph spends tokens
python3 scripts/workflow-runner.py --manifest workflow/manifests/serial-feature-delivery.yaml \
  --executor <poisoned-executor> --guardrail scripts/lib/guardrails.py
```

## The rule of thumb

Tokens are spent by **content loading, context replay, unbounded retries, and propagated
failures**. This stack attacks all four: compiled + progressive prompts (load less), memory and
structured handoffs (carry less), budgets/stagnation/joins (retry less), and edge guardrails
(fail cheapest) — with SLIs and benchmarks keeping every claim measured.
