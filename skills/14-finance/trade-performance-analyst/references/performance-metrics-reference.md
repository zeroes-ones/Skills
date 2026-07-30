# Performance Metrics Reference

## Absolute Return Metrics
| Metric | Formula | Notes |
|--------|---------|-------|
| Total Return | (Ending_Value / Starting_Value) - 1 | Gross or net depending on fee inclusion |
| CAGR | (Ending/Starting)^(1/years) - 1 | Annualized geometric return |
| Rolling Returns | CAGR over rolling N-month windows | Shows consistency through time |

## Risk Metrics
| Metric | Formula | Notes |
|--------|---------|-------|
| Volatility (σ) | StdDev(returns) * sqrt(periods/year) | Daily σ * √252 = annualized; Monthly σ * √12 |
| Downside Deviation | StdDev(min(returns, 0)) * sqrt(periods/year) | Only negative returns |
| Max Drawdown | min(P_t/P_peak - 1) | Peak-to-trough, NOT peak-to-current |
| VaR (95%) | 5th percentile of return distribution | Parametric (normal) or historical |
| CVaR (95%) | Mean of returns below VaR threshold | Expected loss WHEN VaR is breached |

## Risk-Adjusted Return Metrics
| Metric | Formula | Confidence Interval |
|--------|---------|---------------------|
| Sharpe Ratio | (R - Rf) / σ | SE ≈ 1/sqrt(N); 90% CI: Sharpe ± 1.645*SE |
| Sortino Ratio | (R - Rf) / σ_downside | Similar to Sharpe but narrower (less data) |
| Calmar Ratio | CAGR / |Max Drawdown| | No standard CI; use bootstrap |
| MAR Ratio | CAGR / |Max Drawdown| | Same formula, different convention |
| Information Ratio | (R - R_benchmark) / σ_tracking_error | Measures consistency of outperformance |
| Omega Ratio | ∫(1-F(x))dx / ∫F(x)dx (above/below threshold) | Considers full distribution shape |

## Win/Loss Metrics
| Metric | Formula | Notes |
|--------|---------|-------|
| Win Rate | Wins / Total Trades | Info-free without expectancy |
| Expectancy | (Win_Rate * Avg_Win) - (Loss_Rate * |Avg_Loss|) | THE key metric — per-trade expected return |
| Profit Factor | Gross_Profit / Gross_Loss | >1.5 is good; >2.0 is excellent |
| Risk/Reward Ratio | Avg_Win / |Avg_Loss| | Must be > (1-Win_Rate)/Win_Rate to be profitable |

## Annualization Caveat
- All annualized metrics assume returns are IID (independent and identically distributed)
- Trading returns are NOT IID (vol clustering, serial correlation)
- Annualized Sharpe from daily data can be upward-biased if returns are autocorrelated

## Provenance
[VERIFIED] Formulas from academic finance (Sharpe 1966, Sortino 1994, Calmar 1991)
[AS OF 2026-01]

