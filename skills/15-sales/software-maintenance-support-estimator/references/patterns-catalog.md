# Patterns Catalog — Maintenance & Support (backing reference for software-maintenance-support-estimator)

Dense reference tables for pricing post-launch services. Anchors, not facts — calibrate to
your own incidents and contracts (see `examples/backtest/`).

## Annual maintenance anchor (15–25% of build, risk-adjusted)

| Profile | Annual % of build |
|---|---|
| Stable, low change | 12–15% |
| Typical SaaS | 15–20% |
| Integrations-heavy | 20–25% |
| Regulated / legacy / high-SLA | 25–40% |
| High debt, no tests/docs | 30–40% |

## Maintenance mix

Corrective 20–25% · adaptive 15–20% · perfective 25–30% · preventive 10–15%.

## SLA tier pricing logic

Bronze: business-hours, next-day P1, base bucket. Silver: +weekend watch, 4h P1, ~1.5×.
Gold: 24×7 on-call, 30–60 min P1, ~2–3× (availability premium).

## Dollar context

A $200,000 build at 18%/yr ≈ **$36,000/yr** (~$3,000/mo retainer + true-up). Under-pricing by
5 points ≈ **$10,000/yr** of hidden cost; a boundary dispute over enhancements typically costs
**$2,000–$8,000** in rework + legal friction when "maintenance vs enhancement" is unwritten.
