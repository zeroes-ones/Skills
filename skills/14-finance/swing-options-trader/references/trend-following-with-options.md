# Trend Following with Options — Swing Options Reference

> **Reading time:** 10 min | **Prerequisites:** technical-signals-engineer (trend systems), options-strategist, swing-options-trader

## Translating Trends to Options

[VERIFIED] Trend following with shares is straightforward: buy and hold until the trend breaks. With options, you must manage theta, structure selection, and entry timing. The wrong options structure can lose money even when you're right about the trend direction.

## The Trend-Options Matrix

### Trend Phase → Options Structure

| Trend Phase | Characteristics | Best Options Structures | Why |
|------------|----------------|------------------------|-----|
| **Early Trend** (breakout, <2 weeks old) | Strong momentum, low retracement, ADX rising from <20 | ATM Debit Spread (Call for up, Put for down) | Captures initial momentum. Capped profit is fine — the move may be short |
| **Established Trend** (2-8 weeks old) | Higher highs/lows, ADX 25-40, price above 20/50 SMA | Diagonal (long DITM, short OTM) or PMCC for uptrends | Collects premium while participating. LEAPS diagonal for longer trends |
| **Mature Trend** (8+ weeks) | ADX > 40, price extended from SMAs, momentum slowing | Bull Put Spread (for uptrend) or Bear Call Spread (for downtrend) | Selling premium into elevated IV. Trend may stall but reversal unlikely |
| **Trend Exhaustion** (ADX > 50, divergences) | RSI divergence, volume declining, wide-range reversal candles | Iron Condor or Short Strangle | Trend losing steam. Range-bound expected. Collect sideways premium |
| **Trend Reversal** (new trend forming) | Broken structure, moving average crossovers | Wait for confirmation. Then ATM Debit Spread in new direction | Reversal trading without confirmation is trend-following's kryptonite |

## Technical Indicators for Options Entry

### Moving Average Systems

```
Trend filter: Price > 20SMA AND 20SMA > 50SMA = uptrend. Reverse for downtrend.

Pullback entry in uptrend:
1. Price pulls back to 20SMA or 50SMA
2. RSI(14) on daily < 50 (reset from overbought)
3. Volume on pullback < average (low conviction selling)
4. Entry: Bull Put Spread at the moving average support level
5. Strike: Short put at or just below the MA support (0.25-0.30Δ)
```

### ADX (Average Directional Index)

```
ADX < 20: No trend. Options: Credit spreads, iron condors. No directional debit spreads.
ADX 20-25: Trend forming. Options: ATM debit spreads. Smaller size while trend confirms.
ADX 25-40: Strong trend. Options: Debit spreads OR diagonals for leveraged participation.
ADX > 40: Very strong trend. Options: Bull put / bear call spreads. Sell premium. Trend is mature.
ADX > 50: Extreme trend. Options: Reduce size 50%. Trend exhaustion likely. Tighten stops.
```

[BACKTEST-EVIDENCE] In the Trading project backtest, entries when ADX was between 20-30 significantly outperformed entries at ADX > 40 across 8 of 11 tickers. Entering mature trends underperforms.

### RSI for Options Entry Timing

```
For uptrends (bull put spreads, call debit spreads):
  Entry: RSI(14) < 50 on daily (pullback intra-trend)
  Avoid: RSI > 70 (extended, high probability of mean reversion)

For downtrends (bear call spreads, put debit spreads):
  Entry: RSI(14) > 50 on daily (bounce intra-trend)
  Avoid: RSI < 30 (oversold, snap-back risk)

For neutral strategies (iron condors, short strangles):
  Entry: RSI 40-60 on daily (equilibrium)
  Avoid: RSI trending strongly to extremes (breakout risk)
```

## The Pullback Entry Playbook

### Bull Put Spread on Support (Uptrend Pullback)

```
Conditions:
1. Weekly: Uptrend confirmed (price > 20SMA, 20SMA > 50SMA)
2. Daily: Price pulled back to 20SMA or identified support
3. Daily RSI: 40-50 (reset from overbought)
4. Volume: Below 20-day average (selling pressure is weak)

Entry: Sell put spread with short strike AT or just BELOW the support level
Short strike: 0.25-0.30Δ, at the support zone
Width: 5-wide for most stocks (adjust for price level)
DTE: 30-45 days
Profit target: 50% of credit received
Stop: 2× credit received OR support broken on daily close
```

### Bear Call Spread on Resistance (Downtrend Rally)

```
Conditions:
1. Weekly: Downtrend confirmed (price < 20SMA, 20SMA < 50SMA)
2. Daily: Price rallied to 20SMA or identified resistance
3. Daily RSI: 50-60 (relief rally, not reversal)
4. Volume: Below 20-day average (buying pressure is weak)

Entry: Sell call spread with short strike AT or just ABOVE the resistance
Short strike: 0.25-0.30Δ, at the resistance zone
Width: 5-wide
DTE: 30-45 days
Profit target: 50% of credit received
Stop: 2× credit received OR resistance broken on daily close
```

## The Score Calibration Trap

[BACKTEST-EVIDENCE] **Critical finding from the Trading project:** Higher scores do NOT predict better outcomes across 9 of 11 test tickers. The relationship is often inverted — high momentum scores predict mean reversion, not continuation.

```
What this means for swing options:
- A "strong" trend score (>80) is NOT a reason to size up
- A "moderate" score (50-70) often produced better outcomes
- Score should be used directionally (up/down) not for conviction sizing
- Trend duration (how long the trend has been running) is a better predictor than trend "strength"
```

**The correct filter:** Use scores for direction. Use trend DURATION for sizing. New trends (< 3 weeks) → larger size. Mature trends (> 8 weeks) → smaller size.

## Earnings Blackout Gate

[VERIFIED] Swing trades that span an earnings date carry binary event risk:

```
If earnings date falls within the swing holding period:
  1. Close the position BEFORE earnings (at market close on earnings day - 1)
  2. OR: Size to 25% of normal (accept the binary risk)
  3. OR: Replace with a structure that benefits from IV crush (iron condor, short strangle IF conviction is neutral)

Never hold a directional options swing trade through earnings at full size.
Post-earnings gaps of 5-15% are common and can wipe out months of swing profits.
```

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| "The trend is strong, I'll buy OTM calls for maximum leverage" | ATM debit spreads or DITM calls. OTM calls on established trends have lower delta and higher theta — the trend has to accelerate to profit |
| Using trend scores for position sizing | Scores are directional, not conviction metrics. Size based on trend duration, vol regime, and Kelly-adjusted risk |
| Entering pullbacks that broke the moving average | A pullback TO the MA is an entry. A pullback THROUGH the MA is a trend break. Differentiate |
| Trend following with credit spreads in the first 2 weeks of a new trend | Credit spreads cap upside. In the early trend phase, use debit spreads to capture the initial momentum surge |

## Provenance

[VERIFIED] ADX interpretation from J. Welles Wilder's "New Concepts in Technical Trading Systems" (1978), adapted for options.
[COMMON-PRACTICE] Pullback entries on moving averages from Linda Raschke and professional swing trading methodology.
[BACKTEST-EVIDENCE] Score calibration inversion and trend duration outperformance from Trading project backtest across 11 tickers.
[COMPUTED] RSI, ADX thresholds are standard interpretations adapted for options entry timing.
[AS OF 2026-07]
