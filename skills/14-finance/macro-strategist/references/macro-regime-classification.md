# Macro Regime Classification

## The 2x2 Growth-Inflation Matrix
```
                    INFLATION
              ABOVE TREND    BELOW TREND
           ┌──────────────┬──────────────┐
ABOVE      │ OVERHEATING  │ GOLDILOCKS   │
TREND      │ Risk: Fed    │ Risk:        │
           │ tightening   │ complacency  │
G  ────────┼──────────────┼──────────────┤
R          │ STAGFLATION  │ RECESSION    │
O BELOW    │ Risk: margin │ Risk: credit │
W TREND    │ compression  │ defaults     │
T          │              │              │
H          └──────────────┴──────────────┘
```

## Indicator Taxonomy
| Type | Examples | Lead Time | Reliability |
|------|----------|-----------|-------------|
| Leading | ISM New Orders, Building Permits, Consumer Expectations, Yield Curve | 6-12 months | Moderate (false positives) |
| Coincident | Industrial Production, Personal Income, Retail Sales, Payrolls | 0 months | High (current state) |
| Lagging | Unemployment Rate, CPI, Commercial Loans, Unit Labor Costs | -3 to -12 months | High (confirms trend) |

## Key Indicators for Regime Detection
| Indicator | Growth Signal | Inflation Signal | Frequency |
|-----------|--------------|-----------------|-----------|
| ISM Manufacturing PMI | >50 expanding | Prices Paid sub-index | Monthly |
| Nonfarm Payrolls | >150K healthy | Avg Hourly Earnings YoY | Monthly |
| Core PCE YoY | N/A (growth proxy via consumption) | vs 2% target | Monthly |
| 10Y-2Y Spread | Inversion = recession signal (12-24mo lag) | N/A | Daily |
| Initial Jobless Claims | >300K = softening | N/A | Weekly |

## Regime Transition Triggers
| From → To | Typical Trigger |
|-----------|----------------|
| Goldilocks → Overheating | Commodity price shock, wage spiral, fiscal stimulus |
| Goldilocks → Recession | Fed overtightening, credit crunch, external shock |
| Overheating → Stagflation | Supply shock (energy, food), productivity decline |
| Recession → Goldilocks | Fed easing + fiscal stimulus + inventory restocking |

## Provenance
[VERIFIED] NBER business cycle dating methodology; indicator definitions from BEA, BLS, Fed
[AS OF 2026-01]

