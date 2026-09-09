# Backtest — Support Contracts vs Actuals (software-maintenance-support-estimator)

Three support contracts compared to actuals for anchor calibration.
[VERIFIED]=actual, [COMPUTED]=derived, [ESTIMATED]=judgment.

| System | Build cost [VERIFIED] | Annual % quoted | Actual hours | Lesson |
|---|---|---|---|---|
| Internal tool (stable) | $60K | 15% ($9K) | 8.4K/yr-equivalent | near anchor, true-up 0 |
| Fintech checkout | $210K | 22% ($46K) | 49K/yr-equivalent | regulated uplift justified |
| Legacy CRM, high debt | $180K | 30% ($54K) | 63K/yr-equivalent | debt priced, or it bleeds |

Calibration: stable internal ≈ 12–15%, typical SaaS ≈ 15–20%, regulated/legacy ≈ 25–40%;
always add the enhancement T&M lane (corrective/perfective split held in practice).

**Complete when:** the contract log shows ≥3 actuals and the % drivers are adjusted from the
deltas above, not taken verbatim from the 15–25% anchor.

## Scenario analysis

Best case: scope frozen at kickoff and integration clean — actuals land at or under base.
Worst case: scope creeps past the 15–20% trigger and integration surfaces late — overrun
reaches the top of the band. Lesson learned: publish the assumption register before work and
re-quote at the trigger; every overrun in the table above traces to a missed trigger or a
missing workstream.
