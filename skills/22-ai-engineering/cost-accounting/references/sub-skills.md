# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `measurement-status` | Is this number measured, computed, estimated or unknown? | `references/measurement-status.md` — R1 |
| `attribution` | Which node and which phase consumed the cost | `references/attribution.md` — R5 |
| `cost-per-success` | The decision metric, and the arithmetic that shows why | `references/cost-per-success.md` — R3 |
| `budgets-caps` | Run-level caps, halting, and the increase path | `references/budgets-and-caps.md` — R4 |
| `cost-gates` | Delta gating, baselines, price versus usage drift | `references/cost-regression-gates.md` |
| `showback` | Attribution per team, and when chargeback is safe | `references/showback-and-chargeback.md` |
| `forecasting` | Unit economics to volume, scenarios and bands | `references/forecasting.md` — R6 |
| `reconciliation` | Comparing the accounting to the invoice | `references/reconciliation.md` |
| `levers` | Node count, iterations, escalation, caching, routing | `references/run-level-levers.md` |
| `proxies` | When a proxy is acceptable and how it drifts | `references/proxies-and-drift.md` — R2 |

## Split when

- **The question is one number.** "What did this run cost?" is `measurement-status` plus `attribution`, and it is bounded.
- **A budget is being set** — `budgets-caps` alone, with the measured baseline it needs.
- **A saving is being claimed** — `cost-per-success` plus `cost-gates`.
- **The accounting is being reconciled** — that is `reconciliation`, a self-contained session.
- **The task is reducing what one call costs** — hand to `token-efficiency`; that is the other family of lever.

## Stay whole when

- **Cost accounting is being introduced to a workload for the first time.** Plumbing, baseline,
  attribution, budget and gate are one piece of work; doing them separately produces a number nobody
  trusts and a cap nobody enforces.
- **A runaway spend is being investigated.** Attribution, the loop lever and the cap interact — a
  cap without attribution will be set at the wrong place.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `token-efficiency` | per-request token minimisation, caching, output control, per-request cost | the run's measured total, its attribution, and its bounds |
| `context-optimizer` | minimising a context payload at held quality | the price of the payload, and whether the reduction paid |
| `agent-eval-pipeline` | the quality score and the success rate | pairing that outcome with the spend |
| `agentic-complexity-ladder` | which architecture a task needs | the measured cost of the rung chosen |
| `workflow-graph-authoring` | the manifest's structure | the budget fields, and their enforcement |
| `observability-engineer` | the telemetry pipeline carrying the spans | what the spans must carry for attribution |
| `finops-engineer` | cloud and infrastructure spend, contracts | agent spend, folded into that picture |
| `site-reliability-engineer` | error budgets and SLIs | spend as an SLI with a budget |

The pattern: `token-efficiency` reduces the cost of a call; this skill measures what the run cost,
attributes it, bounds it, and decides whether the reduction was real once the outcome is counted.
