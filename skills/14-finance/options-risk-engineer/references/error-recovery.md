# Options Risk Engineer — Error Recovery

## Symptom → Root Cause → Fix

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Portfolio Greeks show delta-neutral but P&L is highly directional | Greeks computed at different times. Stale option prices. Missing dividend adjustments skewing delta. | Synchronize: all Greek calculations must use same timestamp. Validate: sum of deltas × underlying move should explain >90% of P&L. Flag if unexplained P&L >10%. | **Greek calculations are garbage-in, garbage-out.** If your inputs are stale, your Greeks are fiction. Synchronize all prices before computing. |
| Pin risk disaster: assigned on ITM options you thought would expire worthless | Didn't monitor on expiration day. Short option went from OTM to ITM in final hour. Didn't close before 4:00 PM ET. | Close all short options <0.05 delta by 3:00 PM ET on expiration day. Never hold short options into expiration without explicit intent and adequate capital for assignment. | **Pin risk costs real money.** A $0.05 option that goes ITM at 3:55 PM can create a $50K stock position you didn't want. Close early or accept the assignment. |
| Margin call on portfolio that looked fine yesterday | Portfolio margin recalculated after hours. Correlation assumptions broke during tail event. Reg T margin triggered by day trade count. | Monitor margin utilization in real-time with buffer: target <50% of available. Stress test margin under correlation=1 scenario. Know both Reg T and portfolio margin rules. | **Margin requirements change when you least expect it.** During volatility, margin expands while portfolio value contracts — a double squeeze that can liquidate positions. |
| Vega P&L attribution doesn't match actual change | Using constant IV assumption. IV surface shift not parallel — skew moves differently from ATM. Term structure twist. | Decompose vega: ATM vega, skew vega, term-structure vega. Track each separately. Use sticky-strike for short-dated, sticky-delta for long-dated. | **"Vega" is not one number.** The volatility surface has at least 3 dimensions of movement. Treating vega as scalar = wrong attribution. |
| Correlation hedging fails during crisis | Diversification benefit disappears when you need it most. All correlations → 1 during tail events. | Stress test portfolio at corr=1 across all assets. Know your portfolio's correlation-1 P&L. Size positions so even corr=1 scenario doesn't breach risk limits. | **Diversification works until it doesn't.** The moment you really need your hedges, correlations collapse to 1. Size for the worst case, not the average. |

## Provenance
[VERIFIED] Options risk failure modes from market-making and portfolio management experience
[COMPUTED] Assignment and margin scenarios based on standard contract sizes
[AS OF 2026-01]

