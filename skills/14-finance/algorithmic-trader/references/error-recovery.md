# Algorithmic Trader — Error Recovery

## Symptom → Root Cause → Fix

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Backtest Sharpe > 3 but live P&L is negative | Overfitting to noise. Too many parameters relative to trade count. Look-ahead bias in feature engineering. | Walk-forward validation: train on 70%, validate on 15%, test on 15%. Time-series split, not random. If walk-forward Sharpe drops >40%, strategy is overfit. | **Backtests lie when you let them.** Every parameter you tune is a degree of freedom that can fit noise. Keep parameter count < sqrt(n_trades). |
| Live fills consistently worse than backtest assumptions | Slippage model too optimistic. Mid-price backtest vs. actual bid-ask execution. Market impact not modeled. | Pull real fill data from broker. Compute actual slippage distribution. Use worst-quartile slippage in simulations. Model market impact using Almgren-Chriss for position sizes >1% ADV. | **The execution gap is real and quantifiable.** A strategy that returns +18% in simulation returns +9% in production. Always budget 50% of backtest alpha for execution friction. |
| Duplicate orders / double fills in production | Missing idempotency. Network retry causes broker to receive order twice. | Implement UUID-based idempotency keys on every order. Store keys in persistent store. Broker deduplicates by key within 24h window. | **Network retries without idempotency = double fills.** This is a $10K-$500K mistake. One line of code prevents it. |
| Strategy stops placing orders silently | Broker API rate limit exceeded. Authentication token expired. Position limit hit. | Implement heartbeat monitoring. Alert if no orders placed in expected window. Log every API response status. Circuit breaker: stop if error rate >5% in rolling 5min window. | **Silent failure is the most expensive failure.** You don't know you're not trading until you check. Automate the checking. |
| Position size drifts from target over time | Corporate actions (splits, dividends) not reflected. Cash drag from uninvested dividends. Drift from market moves. | Rebalance schedule: time-based (monthly) or threshold-based (5% drift). Account for corporate actions in position calculation. Reinvest dividends automatically. | **Unmanaged drift compounds.** A 5% monthly drift unrebalanced for a year = portfolio that no longer matches your strategy. |
| Strategy works in bull market, fails in bear | Regime-specific alpha. Factor timing rather than true edge. | Test across regimes: bull (2009-2020), bear (2008, 2020 Q1, 2022), sideways (2015-2016). Strategy should work in at least 2 of 3 regimes. | **Bull market genius is common. All-weather edge is rare.** If your alpha only appears in uptrends, you're long beta, not generating alpha. |

## Provenance
[VERIFIED] Error patterns from production algorithmic trading experience
[COMPUTED] Cost estimates based on typical retail/institutional account sizes
[AS OF 2026-01]

