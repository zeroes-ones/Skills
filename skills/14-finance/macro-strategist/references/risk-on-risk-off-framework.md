# Risk-On/Risk-Off Framework

## RO/RF Composite Scoring

### Dimensions and Scoring
| Dimension | Risk-On (+1) | Neutral (0) | Risk-Off (-2) |
|-----------|-------------|-------------|---------------|
| G4 Liquidity | Expanding | Flat | Contracting |
| Real Rates | Falling | Flat | Rising sharply |
| Credit Spreads | Tightening | Stable | Widening |
| Econ Surprise | CESI > +20 | CESI -20 to +20 | CESI < -20 |
| Vol Regime | VIX < 20 | VIX 20-30 | VIX > 30 |
| Dollar (DXY) | Weakening | Flat | Strengthening |

### Composite Translation
| Score Range | Regime | Allocation Signal |
|------------|--------|-------------------|
| +7 to +12 | MAX RISK-ON | Full risk allocation, lever if appropriate |
| +3 to +6 | RISK-ON | Overweight risk assets, reduce hedges |
| -1 to +2 | NEUTRAL | Benchmark weights, standard hedges |
| -5 to -2 | RISK-OFF | Underweight risk, increase hedges |
| -12 to -6 | MAX RISK-OFF | Capital preservation mode, full hedge |

## Regime Transition Signals
| Signal | Interpretation | Lead Time |
|--------|---------------|-----------|
| Yield curve steepening (bear steepener) | Inflation expectations rising; late-cycle | 6-12 months |
| Yield curve steepening (bull steepener) | Fed cutting front end; recession pricing | 1-3 months |
| Yield curve flattening (bull flattener) | Fed hiking; risk-off | 1-6 months |
| Defensive sector leadership | Risk-off rotation within equities | 1-3 months |
| VIX futures backwardation | Stress in vol market; risk-off | Days to weeks |
| TED spread widening | Funding market stress | Days |

## Cross-Asset Volatility Monitoring
| Vol Index | Underlying | Normal Range | Stress Level |
|-----------|-----------|-------------|-------------|
| VIX | S&P 500 | 12-20 | >30 (fear), >40 (panic) |
| MOVE | US Treasuries | 60-90 | >120 (rate vol stress) |
| CVIX | FX (DXY) | 5-10 | >12 (currency stress) |
| OVX | Crude Oil | 25-40 | >60 (energy stress) |
| VIX/MOVE ratio | Equity/Rate vol | 0.15-0.25 | >0.30 (equity vol dominating) |

## Provenance
[COMPUTED] Scoring framework from macro strategy research; vol levels from historical data
[AS OF 2026-01]

