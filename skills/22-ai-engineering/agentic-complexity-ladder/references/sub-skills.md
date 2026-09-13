# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `ladder` | Which rung a task needs, and what each buys | `references/the-ladder.md` — Decision Tree 3 |
| `workflow-vs-agent` | Predictability, and the bounded-agent form | `references/workflow-vs-agent.md` — R2 |
| `entry-criteria` | The measured failure each rung entry requires | `references/entry-criteria.md` — R1, R6 |
| `exit-criteria` | Writing the return path, and re-evaluating | `references/exit-criteria.md` — R4 |
| `de-escalation` | Simplifying a working system without a regression | `references/de-escalation.md` |
| `routing` | When a classifier earns its maintenance cost | `references/routing-decisions.md` |
| `parallelism` | Sectioning versus voting, and the aggregation cost | `references/parallelism-thresholds.md` |
| `orchestrator` | Planning cost, the tail, and the debugging penalty | `references/orchestrator-costs.md` |
| `graph` | When an auditable graph is warranted, including for governance | `references/graph-justification.md` |
| `over-build-audit` | The removal audit and the graph tells | `references/over-build-audit.md` |

## Split when

- **One decision dominates.** "Do we need an agent for this?" is `workflow-vs-agent`, and it is bounded.
- **A single rung is being evaluated** — `routing`, `parallelism` or `orchestrator` alone.
- **An over-built system is being audited** — `over-build-audit` plus `de-escalation`.
- **A graph's justification is the question** — `graph`, and its answer may be "not warranted".
- **The task is measuring what a run costs** — hand to `cost-accounting`; that is a separate skill.

## Stay whole when

- **A new agentic system is being designed.** The rung choice, its entry evidence, its own failure mode
  and its exit condition are one decision; splitting them produces a rung with no justification and no
  way to remove it.
- **A system is being simplified.** The audit, the removal test and the de-escalation reporting are one
  piece of work; a partial version leaves complexity that nobody can justify.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `workflow-graph-authoring` | Authoring the manifest, node/edge/loop syntax | Whether the graph rung is warranted at all |
| `cost-accounting` | Measuring and bounding what a run costs | Pricing the *choice* between rungs |
| `multi-agent-orchestration` | Topology selection once multi-agent is warranted | Whether multi-agent is warranted |
| `ai-engineer` | Building the components and prompts | The architecture those components sit in |
| `agent-eval-pipeline` | The task set, the harness and the quality score | The failing case that justifies a climb |
| `context-optimizer` | Reducing a context payload at held quality | Whether a smaller context removes the need for a rung |
| `system-architect` | Service decomposition outside agents | The rungs *inside* an agentic system |
| `agent-handoff-protocol` | The payload contract between nodes | Which nodes exist to hand off between |

The pattern: the neighbours own *the manifest*, *the cost*, *the topology* and *the components*. This
skill owns the single question none of them asks — **did this task need this much machinery at all, and
if so, which failure justified it?**
