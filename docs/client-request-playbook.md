# Client Request Playbook — From "Can You Build…?" to Delivered + Maintained

A one-page decision map for freelancers, agencies, and delivery orgs: whatever the client asks
for, this doc says **which skills to load, which runnable example to copy, how to estimate and
price it, and where YOU sit (the human gates).**

> New to the repo? Start with `examples/payments-api-ship/TUTORIAL.md`, then come back here.

---

## How to use this playbook

1. Find the client request below (or combine rows for a bigger ask).
2. Open the named skills (they load as playbooks with decision trees + verification).
3. Copy the named example manifest as your skeleton and swap skill nodes for the client's stack.
4. Run the estimate → price → support pipeline before you promise a number.
5. Mark your human-gate points so the automation knows exactly where to stop and ask you.

---

## Request → route map

| If the client asks… | Skills (chain order) | Copy this manifest | Estimate path | Your gates |
|---|---|---|---|---|
| **Build a new app** | idea-to-spec → system-architect → database-designer → api-designer → backend-developer → frontend-developer → qa-engineer → code-reviewer | `examples/payments-api-ship` | estimator: size class → L/B/H → pricing | spec sign-off, release approval |
| **Add a feature** | idea-to-spec / product-manager → backend-developer + frontend-developer → code-reviewer → qa-engineer | `examples/add-feature/add-feature.yaml` | same pipeline on the delta | feature acceptance |
| **Change the UI** | frontend-developer → (accessibility-auditor if public) → qa-engineer → code-reviewer | `examples/ui-change/ui-change.yaml` | small: S class band | UI sign-off |
| **Change / create an API** | database-designer (if schema moves) → api-designer → backend-developer → secure-api-design → code-reviewer → qa-engineer | `examples/api-change/api-change.yaml` | estimator on contract + implementation | contract review |
| **Create a database / schema** | idea-to-spec → system-architect → database-designer → backend-developer | `examples/db-create/db-create.yaml` | schema-first: M class + migration allowance | schema review |
| **Migrate a DB or system** | migration-architect → plan-gate → api-designer → backend-developer → qa-engineer (parity suite) → cutover-gate → documentation-engineer + deprecation-engineer | `examples/strangler-migration` | per-slice estimate + cutover risk buffer | **plan gate** and **cutover gate** (two humans) |
| **Fix an incident / prod issue** | incident-responder → debugging-and-error-recovery → backend-developer → observability-engineer → commander-gate | `examples/production-incident` | T&M / emergency terms, not fixed | declare / rollback call |
| **Support & maintain after launch** | software-maintenance-support-estimator → customer-support-engineer → release-manager (+ incident-responder for firefights) | `examples/support-maintain/support-maintain.yaml` for the monthly loop; `examples/production-incident` for ops | maintenance: 15–25% of build/yr, risk-adjusted | SLA/bucket scope, renewals |

Combine rows as the real ask dictates — "build me an app that also migrates my legacy DB" =
`payments-api-ship` (build) + `strangler-migration` (migration slice), sequenced with the
estimator sizing each part.

---

## The money pipeline (every row above ends here)

```
software-project-estimator           effort: XS–XXL class -> low/base/high + assumptions
      ▼                              (altitude decides method: t-shirt vs points vs 3-point)
services-engagement-pricing          price: model + rate card + category multiplier
      ▼                              (fixed buffer 15–25% | T&M caps | retainer premium)
software-maintenance-support-estimator   annual % of build + SLA tiers + enhancement lane
      ▼
statement-of-work-authoring              full SOW draft (scope/deliverables/acceptance/
                                         milestones/change control/terms) → legal review
```

Numbers you can start from (details + sources in `docs/estimation-research.md`):

| Figure | Default |
|---|---|
| Typical project overrun to plan for | 30–40% (60–80% of projects overrun in some way) |
| Re-estimation trigger | scope change ≥ 15–20% |
| Solo billable load | 1,200–1,400 h/yr (~60–70% utilization) |
| Overhead | 25–40% of labor; firm multipliers 2.0–3.7× |
| B2B vs B2C pricing | ~2–4× |
| Maintenance | 15–25% of build/yr (30–40% regulated/legacy/high-SLA) |

---

## Where you sit (human gates) by who you are

| Practitioner | Activation | You approve | Automation does |
|---|---|---|---|
| Freelancer (new) | `--solo` (8 skills) | every release/golive — loop escalates straight to you | single-lane build-verify loop |
| Freelancer (experienced) | `--grow` (18 skills) | acceptance + fixed-price scope changes | agent gate tries fixer/verify first, bounded reroutes |
| Agency / small team | mid | prod gate (team lead) | parallel tracks (backend+frontend, reviewer+security+QA, join: all) |
| Delivery org | `--full` | compliance gate + release board | parallel readiness, canary, observability, retainers |

In every case the human gate fires with an evidence trail
(`workflow/templates/escalate.md`): what was tried per pass, the blocker, the recommended next
decision — never an empty "help."

---

## Start in five commands

```bash
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
cd client-project && skills-init --solo        # or --grow / --full
# open the playbook for the ask, e.g. migration:
python3 scripts/workflow-runner.py \
    --manifest examples/strangler-migration/strangler-migration.yaml \
    --executor examples/strangler-migration/executor_demo.py --state /tmp/migrate.json
# then price it: read skills/12-operations/software-project-estimator,
#   skills/15-sales/services-engagement-pricing,
#   skills/15-sales/software-maintenance-support-estimator
```

## Honest limits (read once)

- Skills raise your floor (process, quality gates, defensible numbers) — they don't remove the
  need for scope clarity, your own project actuals, and a capable agent/you to execute.
- "Zero errors" is bounded self-correction (`exit_when` + budgets + gates), not a guarantee.
- Benchmarks are anchors: calibrate every % and rate to your own delivery history and widen
  bands until you have it.

## See it working

All six runnable examples + detailed annotated diagrams:
`examples/DETAILED-DIAGRAMS.md` (legend, budgets, loops, gates, escalation arcs).
