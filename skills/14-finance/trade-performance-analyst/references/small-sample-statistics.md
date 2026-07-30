# Small Sample Statistics

## The Problem
Most performance metrics are computed from finite trade samples. With <30 trades, estimates are noisy. With <10 trades, estimates are nearly meaningless.

## Confidence Intervals

### Sharpe Ratio Standard Error (Lo, 2002)
```
SE(Sharpe) ≈ sqrt((1 + 0.5 * SR²) / n)
```
Where:
- SR = sample Sharpe ratio (annualized)
- n = number of observations (years or trades depending on unit)

**95% CI**: SR ± 1.96 * SE

### Example: Why Sample Size Matters
| Trades | Sharpe | SE | 95% CI |
|--------|--------|----|--------|
| 10 | 1.5 | 0.50 | [0.52, 2.48] — no conclusion possible |
| 30 | 1.5 | 0.29 | [0.93, 2.07] — likely positive |
| 100 | 1.5 | 0.16 | [1.19, 1.81] — statistically significant |
| 300 | 1.5 | 0.09 | [1.32, 1.68] — precise estimate |

**Rule of thumb**: Need 30+ independent trades before Sharpe is meaningful. Need 100+ before it's precise.

## Minimum Sample Size by Metric
| Metric | Minimum Trades | Minimum Months | Notes |
|--------|----------------|----------------|-------|
| Win Rate | 30 | — | Narrow CI at 30, but regime dependence means need 100+ |
| Average Win/Loss | 30 | — | Sensitive to outliers — need larger samples |
| Sharpe Ratio | 30 | 36 | Monthly data needs 3 years minimum |
| Sortino Ratio | 50 | 36 | Needs more data because downside deviation uses subset |
| Maximum Drawdown | 100 | 60 | MDD is path-dependent and highly sample-sensitive |
| Calmar Ratio | 100 | 60 | MDD denominator amplifies sample noise |
| Profit Factor | 30 | — | Wins + losses aggregated — decent convergence at 30 |
| Expectancy | 50 | — | Product of win_rate * avg_win — compound noise |

## Common Statistical Traps

### Look-Ahead Bias
Using information in backtesting that wouldn't have been available at the time of the trade.
**Detect**: Check if any input data has timestamps after the trade entry date.
**Example**: Using full-year earnings to trade in January = look-ahead. Using previous quarter's reported earnings only = correct.

### Survivorship Bias
Backtesting only on assets that still exist, ignoring those that went bankrupt or were delisted.
**Detect**: Compare universe composition at each historical date.
**Fix**: Use point-in-time index constituents, not current constituents.

### Data Snooping
Testing many strategies and reporting the one that worked best — without adjusting for multiple comparisons.
```
Adjusted_Threshold = 1 - (1 - α)^(1 / k)
```
Where k = number of strategies tested. Bonferroni correction: divide α by k.

### Overfitting
Adding parameters until backtest looks perfect but out-of-sample fails.
**Detect**: In-sample Sharpe >> out-of-sample Sharpe
**Prevent**: Always hold out data. Walk-forward analysis. Minimum 30% of dataset reserved for OOS.

## Provenance
[VERIFIED] Confidence intervals from Lo (2002), Bonferroni from statistical literature
[COMPUTED] Minimum sample sizes are guidelines — actual requirements depend on strategy Sharpe/turnover/correlation
[AS OF 2026-01]

