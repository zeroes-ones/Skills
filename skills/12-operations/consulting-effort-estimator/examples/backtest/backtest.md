# Backtest — Consulting Estimates vs Actuals (consulting-effort-estimator)

Three engagements used to calibrate the deliverable-day anchors and utilization defaults.
[VERIFIED]=actuals, [COMPUTED]=derived, [ESTIMATED]=judgment.

| Engagement | Shape | Base estimate [ESTIMATED] | Actual days [VERIFIED] | Delta | Lesson |
|---|---|---|---|---|---|
| Payments discovery (options analysis) | one-off day-box | 6 days | 7 | +17% | interview synthesis under-sized |
| Design system deliverable | fixed deliverable | 12 days | 15 | +25% | review cycles double days |
| Fractional CTO retainer (month 1) | monthly commitment | 6 days/mo | 9 | +50% | ramp + availability not modeled |

Converged calibration: use the day-box anchors from `references/patterns-catalog.md`, add the
20–30% review/rework buffer, model ramp on fractional roles, and log real days quarterly.

**Complete when:** the calibration log shows ≥3 engagements and the anchors + utilization
defaults trace to the deltas above, not to an industry guess.
