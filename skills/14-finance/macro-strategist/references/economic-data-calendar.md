# Economic Data Calendar

## Tier 1 Releases (Market-Moving)
| Release | Frequency | Typical Time (ET) | Market Impact |
|---------|-----------|-------------------|---------------|
| Nonfarm Payrolls | Monthly (1st Friday) | 8:30 AM | High (employment, wages) |
| CPI | Monthly (~10th-15th) | 8:30 AM | High (inflation) |
| FOMC Decision | 8x/year | 2:00 PM | Very High (policy rate, dot plot, SEP) |
| GDP (Advance) | Quarterly | 8:30 AM | High (economic growth) |
| ISM Manufacturing PMI | Monthly (1st business day) | 10:00 AM | High (business cycle) |
| Retail Sales | Monthly (~15th) | 8:30 AM | Medium-High (consumer) |
| PCE Price Index | Monthly (last business day) | 8:30 AM | High (Fed's preferred inflation) |

## Tier 2 Releases (Context-Shaping)
| Release | Frequency | Key Component |
|---------|-----------|--------------|
| ISM Services PMI | Monthly (3rd business day) | Services = ~77% of US GDP |
| JOLTS Job Openings | Monthly | Labor market tightness |
| Initial Jobless Claims | Weekly (Thursday) | Highest frequency labor data |
| Consumer Confidence (Conference Board) | Monthly (last Tuesday) | Expectations index = leading indicator |
| Durable Goods Orders | Monthly | Business investment proxy |
| Housing Starts | Monthly | Construction activity |
| Industrial Production | Monthly | Manufacturing + mining + utilities |

## Data Revision Patterns
| Data Type | Typical Revision | Direction Bias |
|-----------|-----------------|----------------|
| GDP (Advance → Final) | ±0.6% | Upward in recessions (preliminary too pessimistic) |
| Nonfarm Payrolls (1st → 3rd) | ±50K | No consistent bias |
| Retail Sales | ±0.3% | Slightly upward |
| CPI | ±0.1% | No consistent bias (annual revision only) |

## Consensus Sources
- **Bloomberg Survey**: Most widely cited; median of economist forecasts
- **Reuters Poll**: Alternative to Bloomberg
- **Econoday**: Calendar + consensus + analysis
- **Trading Economics**: Free alternative, less comprehensive

## Surprise Computation
```
Surprise = Actual - Consensus
Normalized Surprise = (Actual - Consensus) / Historical Surprise Std Dev
```
Normalized surprise > 1.5 = significant surprise (market-moving)

## Provenance
[VERIFIED] Release schedules from BLS, BEA, Census Bureau, Federal Reserve
[AS OF 2026-01]

