# Backtest — Quotes vs Outcomes (services-engagement-pricing)

Three real quotes compared to what actually happened, for rate/multiplier/buffer calibration.
[VERIFIED]=actual outcome, [COMPUTED]=derived, [ESTIMATED]=judgment.

| Deal | Category | Model | Quoted [VERIFIED] | Outcome | Lesson |
|---|---|---|---|---|---|
| Local cafe site | C2C | fixed | $1,800 | delivered 1.9× hours | no buffer → rebuild with 20% |
| SaaS checkout rebuild | B2B | T&M | $120/h, cap $24K | $22K | caps + burn reports kept trust |
| Compliance portal | B2G | fixed | $96K (2.4× base) | +18% scope → re-quote | 15–20% trigger worked |

Calibration: fixed quotes carry 15–25% buffer; B2B multiplier 2–4× holds; never skip the
assumptions register (the B2G deal survived because scope boundary was written down).

**Complete when:** the quote log shows ≥3 outcomes and the buffer/multiplier defaults trace to
the deltas above.
