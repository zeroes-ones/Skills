# Additional Resources — agentic-complexity-ladder

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `the-ladder.md` | The six rungs side by side: what each buys, costs, breaks, and how it debugs |
| `workflow-vs-agent.md` | Predictability as the deciding axis, the four settling questions, and the bounded-agent form |
| `entry-criteria.md` | The measured failure each rung entry requires, and the failure taxonomy that maps to rungs |
| `exit-criteria.md` | Writing falsifiable return conditions at climb time, the re-evaluation cadence, and the removal audit |
| `de-escalation.md` | Auditing by removal, simplifying without a regression, and reporting a simplification as a win |
| `routing-decisions.md` | The clustering test, separability, the traffic question, and when routing is the wrong rung |
| `parallelism-thresholds.md` | Sectioning versus voting, the slowest-branch arithmetic, and the aggregation policy |
| `orchestrator-costs.md` | Planning tokens, the cost tail, the debugging penalty, and the 20-input test |
| `graph-justification.md` | The five justifications, the governance case, and the tells of an unjustified graph |
| `over-build-audit.md` | Reading a design for removal candidates, the graph tells, and the two-list comparison |
| `anti-patterns.md` | Fifteen complexity anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Fifteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a complexity decision against a stated scenario, with the arithmetic
shown and every figure provenance-tagged.

## Source material

Framework and model capabilities change quickly, so a rung that was necessary last year may be
unnecessary now. Confirm a current capability before relying on it.

| Source | What it governs |
|---|---|
| Anthropic, "Building Effective Agents" | The simplicity default; the workflows-versus-agents distinction; the pattern taxonomy (prompt chaining, routing, parallelisation, orchestrator-workers, evaluator-optimizer) and when each applies |
| `WORKFLOW-SYSTEM.md` (this repository) | Graph workflows with typed nodes, loops, gates and budgets, and what the engine enforces |
| `workflow-graph-authoring` (this library) | Manifest authoring once the shape is decided |
| `cost-accounting` (this library) | The measured cost and latency of each rung |
| `multi-agent-orchestration` (this library) | Topology detail once multi-agent is warranted |
| Framework and model documentation | Current capability, per installed version — the input that moves the ladder |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present
with enforcement columns, that the burden of proof sits on the complexity rather than the simplicity,
that each rung must name a measured failure, that agency is refused where the steps are knowable, that
every rung has a falsifiable exit condition, and that an open action space is treated as a security
decision rather than an architecture one. Run it before relying on the skill's output.
