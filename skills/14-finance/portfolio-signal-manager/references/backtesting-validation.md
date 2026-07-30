# Backtesting & Validation

## Minimum Requirements

| Metric | Minimum | Ideal |
|--------|---------|-------|
| Historical period | 5 years | 10+ years (includes 2008 and 2020) |
| Trade count | >100 | >500 |
| Out-of-sample period | 1 year | 2 years |
| Walk-forward windows | 3 | 10+ |

## Overfitting Detection

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Sharpe > 3.0 | Overfitting or look-ahead bias | Check for data leakage |
| In-sample Sharpe >> Out-of-sample | Overfitting | Reduce parameter count |
| Performance decays over time | Regime-specific overfit | Walk-forward validation |
| All trades same size/direction | Missing transaction costs | Add slippage + commissions |

## What to Backtest

1. Signal accuracy: did BUY signals precede price increases?
2. Conflict resolution: did the weighted matrix pick right?
3. Position sizing: did sizing method improve risk-adjusted returns?
4. Circuit breakers: did they fire at the right times?
5. Tax impact: after-tax returns vs pre-tax
