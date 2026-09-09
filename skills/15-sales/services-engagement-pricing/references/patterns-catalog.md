# Patterns Catalog — Pricing & Quoting (backing reference for services-engagement-pricing)

Dense reference tables for building rate cards and quotes. All figures are anchors; calibrate
to your own actuals and market (see `examples/backtest/`).

## Rate math

- Billable load: 1,200–1,400 hrs/yr solo (~60–70% utilization), not 2,080.
- Rate = (salary + overhead 25–40% + profit 15–25%) ÷ billable hours.
- Firm multiplier: direct pay × 2.0–3.7 overhead factor × 1.10–1.25 profit markup.
- Effective rate trap: add 15–40% for unbilled time before judging a rate.

## Model choice

| Situation | Model | Guardrail |
|---|---|---|
| Clear scope, known work | fixed-bid | buffer 15–25% + assumptions |
| Evolving scope | T&M | not-to-exceed cap + burn report |
| Ongoing availability | retainer | premium over project rate |
| Measurable outcome | value-based | metric + floor agreed first |
| New relationship | hourly/day | track actuals |

## Category multipliers (applied to base)

C2C 1× (lowest) · B2C ~1× · B2B ~2–4× · B2G ~3–5× (compliance, slow pay).

## Quote example (dollar context)

M-class build, base $48,000: +20% buffer → $57,600 fixed; range $52,000–$64,000. B2B
presentation at 2× base-equivalent; typical SOW re-negotiation on scope creep costs
**$3,000–$15,000** of absorbed work when the 15–20% trigger is ignored.
