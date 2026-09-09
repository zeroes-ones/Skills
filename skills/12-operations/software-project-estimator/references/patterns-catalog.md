# Patterns Catalog — Effort Sizing (backing reference for software-project-estimator)

Dense reference tables the skill pulls when producing an estimate. All figures are
**anchors, not facts**: calibrate to your own actuals (see the backtest in
`examples/backtest/`).

## Size class → base effort anchors

| Class | Base effort | Band | Typical scope |
|---|---|---|---|
| XS | ≤ 3 engineer-days | ±15% | one change, landing page |
| S | 3–10 engineer-days | ±20–25% | one feature |
| M | 2–6 engineer-weeks | ±30% | MVP slice, 1–2 integrations |
| L | 1.5–3 engineer-months | ±40% | product v1 |
| XL | 3–9 engineer-months | ±50% | platform, multi-area |
| XXL | > 9 engineer-months | probabilistic | program (require decomposition) |

## Method by planning altitude

| Altitude | Method | Output |
|---|---|---|
| Roadmap budget | t-shirt XS–XXL (XS=1 … XXL=13) | coarse totals |
| Sprint | story points + velocity | points only |
| Quote / SOW | three-point (O+4M+P)/6 days | low/base/high |
| Repeat project | reference-class vs 3+ actuals | anchored band |

## Contingency by risk profile

Greenfield+clear spec +15–20% · integrations-heavy +25–30% · vague spec +30–40% ·
regulated/high-SLA +25–35% · new stack +20–30%.

## Accuracy context

Cone of Uncertainty ±4× early; typical overruns 30–40%; 60–80% of projects overrun in some
dimension; missing integration/test/deploy work is the classic silent miss (budget 20–35%).

## Cost-of-estimate example (dollar context)

Under-estimating an M-class MVP by one band (±30%) on a $30,000 build costs ≈ **$9,000** in
absorbed overrun; a disputed SOW re-quote cycle typically runs **$2,000–$10,000** in friction.
