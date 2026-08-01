# Volatility Arbitrage Backtesting Methodology

> **Portability target:** Spec-level. Backtesting concepts are universal — adapt to any backtesting framework.

## Why Vol Arb Backtesting Is Different

Standard backtesting methodology fails for volatility arbitrage. Three problems:

1. **Path dependency:** A short strangle might profit $500 in 90% of paths and lose $5,000 in 10% of paths. The average outcome ($50 profit) hides catastrophic tail risk.

2. **Sampling bias:** Daily sampling misses intraday vol spikes. A VIX spike from 15 to 45 and back to 18 within one day looks like a "quiet day" in daily data but was a -90% event for short vol.

3. **Non-stationarity:** The VRP (variance risk premium) has structural breaks. Backtesting 2010-2020 (declining rates, low vol regime) and trading 2025+ is regime extrapolation.

## Required Methodology

### 1. Path-by-Path, Not Average

Never report an average outcome. Report the distribution:

```
Percentile:  1st   5th   25th   50th   75th   95th   99th
P&L:        -$28K  -$8K   +$1K   +$3K   +$5K   +$7K  +$9K
```

If the 1st percentile is -$28K and max position risk is $30K, you need $30K per unit — not the "average" risk.

### 2. Intraday Sampling for Spike Detection

| Data Frequency | Missed Spike Detection Rate | Recommendation |
|---------------|---------------------------|----------------|
| Daily close | 60-80% of intraday vol spikes | Unacceptable for vol arb backtesting |
| Hourly | 30-40% | Minimum for long-vol strategies |
| 15-minute | 10-20% | Minimum for short-vol strategies |
| 5-minute | 5-10% | Recommended for all vol arb |
| 1-minute | < 2% | Required for gamma scalping and intraday vol arb |

### 3. Regime-Segmented Testing

| Regime Period | Characteristics | Vol Arb Behavior |
|--------------|----------------|-----------------|
| 2004-2007 | Low vol, pre-crisis | Short vol: profitable. Long vol: bleed. |
| 2008-2009 | Crisis, extreme vol | Short vol: catastrophic. Long vol: windfall. |
| 2010-2019 | Low vol, QE, low rates | Short vol: golden era. Long vol: slow bleed. |
| Mar 2020 | COVID crash | Short vol: -50% to -90%. Long vol: +100% to +500%. |
| 2020-2021 | Recovery, high retail flow | Short vol: profitable but volatile. Long vol: fade. |
| 2022-2023 | Rate hiking, elevated VIX | Short vol: okay. Long vol: choppy. |

**Test across ALL regimes, not just the current one.** If your strategy only works in one regime, it's not a strategy — it's a regime bet.

### 4. Transaction Cost Modeling

Vol arb involves frequent rebalancing. Transaction costs compound:

| Cost Component | Estimate | Vol Arb Impact |
|---------------|---------|---------------|
| Option commissions | $0.15-1.00/contract | 5-20 trades/month = significant |
| Bid-ask spread | 1-5% for equity options, 0.5-2% for SPX | The #1 hidden cost |
| Slippage on delta hedges | $0.01-0.05/share | Daily hedging = adds up |
| Exchange fees | $0.02-0.05/contract | Minor but not zero |
| Market impact | Varies by size | Relevant above 50 contracts |

**Model total transaction cost as 2-5% of gross return for vol arb strategies.**

### 5. Walk-Forward Validation

Static parameters overfit. Walk-forward methodology:

1. Optimize on 2018-2020 → Test on 2021
2. Optimize on 2019-2021 → Test on 2022
3. Optimize on 2020-2022 → Test on 2023
4. Optimize on 2021-2023 → Test on 2024

If performance degrades > 30% out-of-sample vs in-sample, the strategy is overfit.

## Red Flags in Vol Arb Backtests

- Sharpe > 2.0 → Almost certainly overfit or missing tail risk
- Max drawdown < 10% of annual return → Tail risk not captured
- Daily-sampled data only → Missing 60-80% of vol spike events
- Single-regime testing (e.g., only 2010-2019) → Overfit to declining vol regime
- No transaction cost modeling → Returns inflated by 20-50%
- Static parameters (no walk-forward) → Strategy will degrade in production

## Minimum Viable Backtest Checklist

- [ ] Intraday data (minimum 15-minute bars) for spike detection
- [ ] Full distribution reported (1st/5th/25th/50th/75th/95th/99th percentiles)
- [ ] Regime-segmented results across at least 3 distinct regimes
- [ ] Transaction costs modeled at realistic rates
- [ ] Walk-forward validation: 4+ rolling windows
- [ ] Out-of-sample performance within 30% of in-sample
- [ ] Max drawdown consistent with tail event frequency
- [ ] Correlation analysis: does the strategy add alpha or just beta to vol?
