# Additional Resources — cost-accounting

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `measurement-status.md` | Measured, computed, estimated and unknown; the flag in the data; the partial-reporting case; reconciliation as ground truth |
| `attribution.md` | The run → node → phase tree, the three attribution questions, ablation, and the reporting shape |
| `cost-per-success.md` | The arithmetic that shows why per-call cost points the wrong way on a workload that retries |
| `budgets-and-caps.md` | Run caps beside step budgets, halting versus truncating, the unmeasured-cap case, and the increase path |
| `cost-regression-gates.md` | Delta gating, baselines, thresholds from variance, and separating price drift from usage drift |
| `showback-and-chargeback.md` | Tagging, units, shared cost, the showback-first sequence, and the distortion each unit invites |
| `forecasting.md` | Unit × volume, the three inputs and how each lies, scenarios, and the break-even ratio |
| `reconciliation.md` | Window matching, per-model comparison, what variance means, and the reconciliation log |
| `run-level-levers.md` | Node count, iterations, escalation timing, caching, per-node model routing — and the two lever families |
| `proxies-and-drift.md` | When a proxy is legitimate, how it drifts silently, and when to replace it |
| `anti-patterns.md` | Sixteen cost anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Fifteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a cost-accounting programme against a stated scenario, with the
arithmetic shown and every figure provenance-tagged.

## Source material

Model prices, cache-discount rates and billing rules change frequently and differ per account, region
and tier. Confirm the current version before citing a rate.

| Source | What it governs |
|---|---|
| `scripts/workflow-runner.py` (this repository) | The executor `usage` contract, per-node accumulation, and `budget.max_cost_usd` enforcement |
| `scripts/export-traces.py` (this repository) | Per-node and session-level cost attributes in the exported spans |
| `scripts/skill-sli-report.py` (this repository) | Cost per successful run, and the cost regression gate |
| Provider pricing pages and contract terms | Token rates, cache discounts, commitment tiers — per account and region, current version |
| Provider billing APIs | Authoritative spend, for reconciliation |
| `token-efficiency` (this library) | Per-request cost arithmetic and cache economics — the complementary half of the picture |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present
with enforcement columns, that the measured-versus-unmeasured distinction is required rather than
optional, that a proxy must be labelled with its drift condition, that the decision metric is cost per
successful outcome rather than per call, that a budget requires both an enforcement mechanism and an
increase path, and that a security control may never be traded for a saving. Run it before relying on
the skill's output.
