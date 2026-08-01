# Regime Adaptation for Swing Options

> **Portability target:** Spec-level. Regime definitions are universal — adapt entry/exit rules to any market data source.

## The Single Biggest Swing Edge

Most swing traders use one strategy in all market conditions. Winners adapt. The biggest edge in swing options is regime detection + strategy adaptation — not strategy selection.

## Regime Classifier

| Regime | SPY vs 50SMA | VIX Range | Best Strategies | Avoid |
|--------|-------------|-----------|----------------|-------|
| Bull Trend | Above, SMA rising | 10-18 | Bull put spreads, call diagonals, covered strangles | Bear call spreads (fade the trend = death) |
| Bull Quiet | Above, SMA flat | 10-15 | Iron condors, short strangles, calendars | Directional debit — no trend to pay for premium |
| Bear Trend | Below, SMA falling | 18-30 | Bear call spreads, put diagonals, put calendars | Bull put spreads (catching knives = account blow-up) |
| Bear Volatile | Below, SMA falling | 25-40 | Long puts, put debit spreads, VIX calls | ANY credit spread — vol crushes short premium |
| Chop/Range | Oscillating around SMA | 15-22 | Iron condors, butterflies, short strangles | Directional — chop stops out both sides |
| Crash/Correction | Well below, steep drop | 30-60+ | Cash, long VIX, OTM puts as lottery tickets | EVERYTHING except tail hedges and cash |

## September & October: The Tightening

[BACKTEST-EVIDENCE] From the Trading project's 1,068-trade backtest: September average return was -7.2% vs. +3.1% for other months. Volatility seasonality is real.

| Month | Adjustment |
|-------|-----------|
| Jan-Aug | Standard regime settings |
| September | Reduce credit spread width by 15%, reduce size by 25%, avoid earnings plays |
| October | Reduce delta by 10%, favor debit over credit on directional |
| Nov-Dec | Year-end rally bias — favor calls, reduce put sizing |

## VIX-Based Sizing Table

| VIX Level | Max Size (per trade) | Max Portfolio Exposure | Notes |
|-----------|---------------------|----------------------|-------|
| < 15 | 5% | 40% | Low vol = mean reversion to higher vol. Don't max out. |
| 15-20 | 4% | 35% | Sweet spot for premium selling |
| 20-25 | 3% | 25% | Normal-size spread trades |
| 25-30 | 2% | 15% | Reduce. VIX > 25 = elevated risk |
| 30-35 | 1% | 10% | Mostly cash. If trading, only debit spreads |
| > 35 | 0% | 0% | Cash only. No position is a position |

## Broad Market Gate

From the Trading project backtest: **Do not enter longs when:**
- SPY < 50-day SMA AND RSI(14) < 35 → Skip all bullish positions
- VIX > 30 → Halve all sizes regardless of strategy

These two rules filtered 40% of losing trades while eliminating only 15% of winners.

## Regime Transition Detection

The most dangerous periods are regime transitions:

| Transition Signal | Action |
|------------------|--------|
| SPY crosses 50SMA (either direction) | Reduce size 50% for 3 days. Let the new regime establish. |
| VIX > 20 for 3 consecutive days | Shift from credit to debit strategies. Vol regime is changing. |
| 10-day realized vol > 30-day implied vol | Underlying is moving faster than options price. Go delta-1 (shares) or use debit spreads. |
| Correlations spike (SPX sector corr > 0.7) | Reduce net exposure. Diversification is failing. |

## Dollar Impact

A swing account that trades one regime 100% of the time loses 15-30% annually vs. a regime-adapting account trading the same underlying selection. The difference is NOT strategy — it's environment awareness.

| Regime Approach | Annual Return | Max Drawdown | Sharpe |
|---------------|-------------|-------------|--------|
| Single strategy, all regimes | -5% to +8% | -30% to -40% | 0.2-0.4 |
| Regime-adapted strategies | +12% to +25% | -15% to -25% | 0.7-1.2 |

The regime classifier takes 30 seconds to run. It's the highest-ROI edge in swing options.
