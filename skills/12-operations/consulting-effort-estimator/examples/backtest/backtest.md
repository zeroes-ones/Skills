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

Dollar P&L: discovery day-box at $1,200/day → 1-day miss ≈ **$1,200**; fractional ramp
under-modeled by 3 days/mo ≈ **$3,600/mo** of unbilled ramp; review-cycle miss on a design
deliverable ≈ **$2,400–$3,600**.

**Complete when:** the calibration log shows ≥3 engagements and the anchors + utilization
defaults trace to the deltas above, not to an industry guess.

## Scenario analysis

Best case: scope frozen at kickoff and integration clean — actuals land at or under base.
Worst case: scope creeps past the 15–20% trigger and integration surfaces late — overrun
reaches the top of the band. Lesson learned: publish the assumption register before work and
re-quote at the trigger; every overrun in the table above traces to a missed trigger or a
missing workstream.
