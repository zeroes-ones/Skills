# Small-Context 100% Runbook — Run Efficiently With Tiny Windows, Zero Memory Loss

The practical, deep answer to two questions asked together: (1) do we have context saving and
memory to run efficiently in small context windows *without memory loss* (context engineering),
and (2) how do we make skills world-class fast/efficient/100%-effective across single-agent,
multi-agent, handoffs, and iterative-until-done. All numbers below are measured on this repo;
every mechanism is a shipped tool.

## 1. The budget math: tiny windows are enough

A workflow never loads the whole library — it loads **one active skill at a time**, plus tiny
boundary prompts. Measured context budget for real flows:

| Item | Size (measured) |
|---|---|
| One skill, compiled (`.skills-compiled/`) | ~4,150 – 6,514 tokens (idea-to-spec 4,650 · system-architect 4,153 · code-reviewer 4,618 · backend-developer 5,209 · qa-engineer 6,514) |
| A whole 3-node serial chain, loaded one node at a time | 13,421 tokens *total across the run*, but only ~5k in window at any moment |
| A quality-fix loop (2 skills) | 11,723 total; ~5-6k in window at any moment |
| Boundary templates (verify/handoff/escalate) | ~256 – 303 words each |
| Run memory entry | ~883 bytes (~230 words) |

Conclusion: **any 16k window runs these flows comfortably; 32k is headroom**. The design rule is
per-hop, not per-run: keep the active skill + current payload + last memory entry in window;
everything else lives in state/memory on disk.

## 2. Context saving — the four levers

1. **Load compiled, not raw.** Skills compile to 65-90% fewer tokens (avg effective load 3,545
   vs ~8,976 raw body words; 63.4% measured saving). Compiled copies are what agents should read.
2. **Progressive disclosure.** Read Route the Request + Ground Rules (QUICK) first; drill into
   DEEP sections only when the task needs them — routing decisions cost a fraction of the body.
3. **Compact each hop.** `context-compaction-strategies` between nodes keeps handoff context
   shrinking instead of growing (context-rot defense); `context-optimizer` minimizes an existing
   prompt while holding quality (≥90% retention); `token-efficiency` prices it.
4. **Payloads, never transcripts.** Handoffs carry the 9-key registry (summary, evidence refs,
   decisions, open questions, budget…) — summaries and artifact pointers, not conversation logs.

## 3. Memory without loss — the write–manage–read model

| Mechanism | What it does | Loss-prevention |
|---|---|---|
| Run memory (`--memory`, B1) | one structured entry per run (~883 B): workflow/outcome/iterations/verdicts/handoff/counts, tagged `trust: context_only` | durable across sessions; anti-poisoning (context, never instructions) |
| Hash-checked checkpoints | run-state saved per step with hashes; resume from the last verified checkpoint | a crash can't lose work; corruption aborts instead of propagating |
| Decision ledger + open questions | every decision logged; open questions travel in payloads | nothing silently vanishes (a resolved question becomes a decision) |
| Structured handoffs | downstream never re-derives upstream context | no re-read = no re-derivation drift |

Measured: memory entry is **~6× smaller than the full checkpoint** (883 B vs 3.8 KB), so
"remember the last run" costs ~56 words of context, not a replay. Consolidation/forgetting
(the *manage* half) and retrieval are the documented next wave (self-incorporation doc), not the
write side.

## 4. Context engineering — which skill, when

| Situation | Skill |
|---|---|
| Design what to keep across a session | `context-engineering` |
| Minimize an existing prompt/context, hold quality | `context-optimizer` |
| Implement compaction/pruning/dual-representation | `context-compaction-strategies` |
| Budget, cache, price tokens | `token-efficiency` |

(Each has clean "Do NOT use" routing; compiled saving measured 80-90% for these four.)

## 5. The 100%-effective protocol (per mode, scored)

Effectiveness = `scripts/run-effectiveness.py` (0-100): completion 25 · clean 20 · exit-by-design
15 · handoffs 15 · questions 10 · budget 10 · memory 5. Measured: happy run **100/100** with
memory; exhaustion run **45/100** (escalation, no exit-by-design, no final payload) — gated with
`--threshold`.

- **Single-agent:** compiled load → QUICK-first → one evidence-backed verify → budget = history+1
  → guardrails fail cheapest. Iterate only on the gatekeeper's verdict.
- **Multi-agent:** parallelize independent nodes (`parallel:` + `join: all`, disjoint writers) so
  cost ≈ max latency; supervisors route to worker sub-agents (each worker = an agent node via
  `agent_executor.py`); share typed state, not chats.
- **Handoffs:** payload-only, hash-verified, compacted each hop, open questions travel.
- **Iterative-until-done:** exit on one gatekeeper + three code brakes (max_iterations,
  stagnation, step budget) + escalation-with-context + verifier-gated self-improvement
  (`skill-evolve-promote`) so future runs converge faster. Full doctrine:
  `docs/world-class-execution.md`.

## 6. The exact command set (small window, zero loss, 100%)

```bash
# one flow, small window, no loss
python3 scripts/workflow-runner.py \
  --manifest workflow/manifests/quality-fix-loop.yaml \
  --executor scripts/executors/agent_executor.py \   # your LLM backend (AGENT_CMD=...)
  --guardrail scripts/lib/guardrails.py \
  --memory ./agent-memory \
  --state ./run-state.json

# prove effectiveness after the run
python3 scripts/run-effectiveness.py --state run-state.json --memory --threshold 90

# inspect what you spent
python3 scripts/export-traces.py --state run-state.json     # spans w/ token/cost slots
python3 scripts/skill-sli-report.py --dir . --gate-escalation 0.5
python3 scripts/benchmark-skills.py --root skills --markdown  # effective-load baseline

# level-up the flow itself when it fails
python3 scripts/skill-evolve-prep.py --dir .            # failure -> draft inbox
python3 scripts/skill-evolve-promote.py --state run-state.json --manifest ... --executor ...
```

## 7. The one-sentence doctrine

**Small windows are fine**: one compiled skill (~5k tokens) + a ~300-word template + an ~230-word
memory entry per hop; **memory loss is prevented by construction** (hash-checked checkpoints,
structured payloads, context-only run memory); and **100% effective is a measured score**, gated
at 90+ per run, enforced per push by the repo-self-check dogfood gate. Full details live in
`docs/world-class-execution.md`, `examples/efficiency-in-action.md`, and
`docs/self-incorporation.md`.
