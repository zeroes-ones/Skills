# Backtest — Estimation vs Actuals (software-project-estimator)

Three completed projects used to calibrate the anchors in `references/patterns-catalog.md`.
Figures tagged [VERIFIED]=actuals, [COMPUTED]=derived, [ESTIMATED]=judgment.

| Project | Class | Base estimate [ESTIMATED] | Actual effort [VERIFIED] | Delta | Lesson |
|---|---|---|---|---|---|
| Invoice export feature | S | 6 engineer-days | 7.5 | +25% | PDF edge cases under-estimated |
| Booking MVP (auth+payments) | M | 5 engineer-weeks | 6.5 | +30% | payment integration = classic silent miss |
| Legacy DB → new schema | L | 8 engineer-weeks | 11 | +38% | parity testing dominated |

Converged calibration: add integration/test allowance (20–35%) and the risk contingency from
the decision tree; S-class bands ±25% held within ±10% when decomposition was done.

Dollar P&L: M-class base $30,000; band miss (±30%) cost ≈ **$9,000** absorbed; S-class
under-estimate by one band ≈ **$1,800** on a $6,000 quote.

**Complete when:** the calibration log shows ≥3 actuals and the default bands are the result of
the deltas above, not an industry guess.

## Scenario analysis

Best case: scope frozen at kickoff and integration clean — actuals land at or under base.
Worst case: scope creeps past the 15–20% trigger and integration surfaces late — overrun
reaches the top of the band. Lesson learned: publish the assumption register before work and
re-quote at the trigger; every overrun in the table above traces to a missed trigger or a
missing workstream.
