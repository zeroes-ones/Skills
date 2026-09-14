# Backtest Example — implementation-planner

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario is a fixed, hypothetical cross-service feature: "saved payment methods at checkout."
- Two services (checkout, billing) and one shared schema, mirroring the worked example in
  `references/worked-example.md`.
- Team size and rates are illustrative inputs, not measured from any organisation.
- Outputs are scenario illustrations validating the planning workflow, not observed outcomes.

| Parameter | Value | Tag |
|---|---|---|
| Engineering day rate (blended) | $900 | [ESTIMATED] |
| Team size available | 3 engineers | [ESTIMATED] |
| Naive plan (horizontal slicing) duration | 20 days | [ESTIMATED] |
| Planned implementation (vertical slices) duration | 14 days | [ESTIMATED] |
| Days lost to one late integration surprise | 5 days | [ESTIMATED] |
| Days lost to one unplanned backfill sprint | 8 days | [ESTIMATED] |
| Days lost to one merge collision on a shared file | 2 days | [ESTIMATED] |

## Computed scenario ([COMPUTED])

**Without this skill — horizontal slicing.** Layers built in sequence: all models, then all
services, then all endpoints. Nothing is demoable until the final week, and every integration
risk lands at once.

- Duration: 20 days × 3 engineers × $900 = **$54,000** of effort
- One late integration surprise: +5 days = 5 × 3 × $900 = **$13,500**
- One discovered-late backfill sprint: +8 days = 8 × 3 × $900 = **$21,600**
- Total: 33 days, **$89,100**

**With this skill — vertical slices + explicit DAG.**

- Slice 1 is a walking skeleton, so integration risk is retired on day 3 rather than day 25.
- Collision surfaces are checked per wave: the two tasks that would have touched
  `checkout/src/Checkout.tsx` are serialised, avoiding one merge incident.
- Backfill, rollout flag, rollback, and flag-removal are emitted as first-class tasks
  (Decision Tree 4), so the "unplanned sprint" is planned.
- Duration: 14 days × 3 × $900 = **$37,800**
- Remaining exposure: zero late-integration surprise, zero unplanned backfill,
  one avoided merge collision (2 days × 1 engineer × $900 = $1,800 avoided)
- Total: 14 days, **$37,800**

**Delta:** 19 days and **$51,300** avoided on this single feature (≈58% of the naive cost).

## Best case

The first vertical slice surfaces an unexpected dependency in day 3 rather than week 4. The plan
is invalidated cheaply, re-sliced against real information, and the critical path is recomputed
before any significant effort is committed. Front-loading the highest-uncertainty task (Phase 6 of
the Core Workflow) is what makes this cheap: the plan can only be wrong at a point where being
wrong costs hours.

## Worst case

The plan is produced against a spec that has not actually been decided — an unknown remains that
`wayfinder` was supposed to resolve. Every slice inherits the wrong assumption, and the DAG is
structurally correct but aimed at the wrong target. This is the failure mode Ground Rule R1 and
Anti-Rationalization AR-02 exist to prevent; the mitigation is the Phase 1 gate: confirm the
approach is decided before slicing, and route back to `wayfinder` if it is not.

## Learnings / key takeaways

1. The dominant saving is **not** writing a plan faster — it is retiring integration risk early.
   Horizontal slicing hides the largest cost until it is most expensive.
2. The forgotten work (backfill, rollout, rollback, cleanup) is 30% of a real plan and 0% of a
   naive one. Emitting it as tasks converts an unplanned sprint into a scheduled one.
3. Collision surfaces are cheap to check and expensive to skip: 2 days of merge rework per
   incident, and the incident is fully predictable from the file list.
4. A plan's value is partly measurable as avoided cost, but the more reliable signal is
   **plan-vs-reality delta** — the number of tasks that ballooned or blocked unexpectedly.

## What this does not show

- No real team, velocity, or historical incident data underlies these rates; they are stated
  assumptions for arithmetic, not benchmarks.
- The 58% figure depends entirely on how bad the horizontal baseline is. A team that already
  slices vertically and checks collisions would see a much smaller delta — the structure of the
  saving transfers, the percentage does not.
- Estimation of duration or cost is explicitly **not** this skill's job; those numbers exist here
  only to make the planning difference legible. See `software-project-estimator`.
