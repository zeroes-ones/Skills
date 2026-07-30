# Trade Performance Analyst — Error Recovery

## Symptom → Root Cause → Fix

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Reported Sharpe is absurdly high (>5) on simple strategy | Using daily returns in annualization but normalizing incorrectly. Or cherry-picked sample with only winning months. | Verify: annualized_sharpe = daily_sharpe * sqrt(252). If daily returns show serial correlation, use Newey-West adjustment: sqrt(252 / (1 + 2 * Σ ρ(k))) | **Sharpe > 3 is suspicious.** Investigate measurement error before celebrating. True Sharpe > 3 is extremely rare — Renaissance Technologies Medallion Fund is estimated at ~2-4. |
| Performance metrics computed but strategy still loses money | Only positive performance shown because drawdowns and losses are in a different reporting period. Time-average vs dollar-average mismatch. | Always report: CAGR (geometric, not arithmetic), MDD, % of time underwater. These three together are triangulation — if any two look good and the third is terrible, investigate. | **Arithmetic mean returns overstate actual wealth growth.** A strategy that loses 50% then gains 50% has arithmetic mean return = 0% but geometric = -25%. Always use geometric (CAGR). |
| Attribution shows factor contributions that sum to more than total return | Factor specification error (multicollinearity between factors) or omitted factors | Check VIF (variance inflation factor) for each factor. Remove factors with VIF > 10. Use stepwise regression or LASSO. Ensure all factor returns are synchronized to portfolio return dates. | **Multicollinear factors inflate attribution.** Value and low-volatility are often correlated — including both over-attributes to whichever loads first in the regression. |
| Drawdown analysis shows impossible values (negative drawdowns, >100%) | Data errors: missing prices (zero or NaN), split/corporate action not adjusted, or timestamp mismatch | Validate: all prices > 0, all timestamps monotonically increasing, no gaps > 5 trading days without flagging. Re-run with split-adjusted data. | **Garbage in, garbage out.** Performance analysis is only as good as the input data. Always validate data before computing metrics. |
| Behavioral bias detector flags disposition effect but trader uses mechanical stops | Confounding: stops auto-close trades at fixed levels, making discretionary trades appear biased by comparison | Filter behavioral analysis to DISCRETIONARY exit trades only. Report separately: systematic exits vs discretionary exits. Only apply bias detection to discretionary subset. | **Mechanical rules mask real behavioral patterns.** Always separate systematic from discretionary decisions before bias analysis. |
| Small sample Sharpe looks great but forward test is random | Overfitting to noise in small sample. With 10 trades, Sharpe = 2.0 has 95% CI [-0.9, 4.9] — could easily be zero or negative | Report confidence intervals for all metrics. Flag any metric with n < 30 as "low confidence." Use Bayesian shrinkage: posterior = (n / (n + k)) * sample + (k / (n + k)) * prior | **Small sample performance is noise.** Never make allocation decisions from <30 independent trades. The confidence intervals are wider than most traders realize. |
| Different calculation methods give materially different performance | Methodology choices (annualization factor, geometric vs arithmetic, gross vs net of fees, time-weighted vs money-weighted) | Standardize: always document methodology (252 vs 365 days, simple vs log returns, gross vs net). Report BOTH gross and net of fees. For IRRs, use Modified Dietz for multi-period. | **Methodology differences can flip a strategy from "great" to "terrible."** Always disclose methodology and compute at least two methods for robustness. |

## Verification Workflow
1. **Data integrity check**: All prices > 0, timestamps monotonically increasing, no NaN/Inf
2. **Return computation**: Verify compound returns match terminal equity (within 1bp tolerance)
3. **Metric cross-validation**: Sharpe, Sortino, and Calmar should be directionally consistent
4. **Attribution sum check**: Factor contributions must sum to total return within ±5bp
5. **Sample size flagging**: Any metric from <30 observations must carry a confidence warning
6. **Methodology disclosure**: Annualization factor, geometric/arithmetic, gross/net documented

## Provenance
[VERIFIED] Methodology from CFA Institute Performance Presentation Standards (GIPS)
[AS OF 2026-01]

