# Pullback & Reversal Patterns — Swing Options Reference

> **Reading time:** 10 min | **Prerequisites:** technical-signals-engineer (chart patterns), options-strategist, swing-options-trader

## Pullback vs. Reversal: The Critical Distinction

[VERIFIED] A pullback is a counter-trend move within an existing trend. A reversal is a trend change. Pullbacks are entry opportunities. Reversals require a complete strategy change.

## Pullback Identification

### The Healthy Pullback Checklist

```
All must be true for a HEALTHY pullback (entry opportunity):

1. Price stays above/below the 50SMA (uptrend/downtrend)
   - Uptrend pullback: price > 50SMA ✓
   - Downtrend pullback: price < 50SMA ✓

2. Pullback volume < average daily volume
   - Weak selling in uptrend pullback ✓
   - Weak buying in downtrend pullback ✓

3. RSI resets to 40-50 (from overbought in uptrend) OR 50-60 (from oversold in downtrend)

4. Pullback retraces 38.2-61.8% of the prior trend leg (Fibonacci)
   - <38.2%: too shallow (trend still extended)
   - 38.2-61.8%: optimal entry zone
   - >61.8%: too deep (potential reversal, not pullback)

5. Support/resistance from prior structure holds:
   - Prior swing high (now support in uptrend) ✓
   - Prior swing low (now resistance in downtrend) ✓
```

### Pullback Entry with Options

| Pullback Depth | Options Structure | Strike Placement | Risk |
|---------------|-------------------|-----------------|------|
| Shallow (<38.2%) | ATM Debit Spread | ATM, tight spread (3-5 wide) | Moderate — trend still extended |
| Optimal (38.2-61.8%) | Bull Put / Bear Call Spread | Short at support/resistance level | **Best risk/reward** |
| Deep (>61.8%, still above MA) | Wider credit spread OR wait | Short further OTM | Higher — potential reversal |
| Deep (broke MA) | Do not enter. This is a trend break | N/A | Reversal risk |

## Reversal Identification

### Reversal Confirmation (MUST have 3+ signals)

```
1. Structure break: Price breaks a significant swing high/low
   - Uptrend reversal: lower low formed ✓
   - Downtrend reversal: higher high formed ✓

2. Moving average crossover: 20SMA crosses 50SMA in reversal direction

3. Volume confirmation: Reversal candle on above-average volume

4. RSI divergence:
   - Bearish divergence: price makes higher high, RSI makes lower high
   - Bullish divergence: price makes lower low, RSI makes higher low

5. ADX rollover: ADX > 25 starts declining

6. Multiple timeframe: Reversal visible on both daily and weekly charts
```

### Reversal Entry with Options

[COMMON-PRACTICE] Never enter a reversal trade on the FIRST signal. Wait for confirmation (3+ signals). False reversals are common and costlier with options due to theta.

| Reversal Phase | Action | Options Structure |
|---------------|--------|-------------------|
| First signal (divergence, trend line break) | WATCH. Do not enter | None — too early |
| Confirmation (3+ signals above) | Enter at 25% size | ATM Debit Spread in new direction |
| First pullback in new trend | Add to 100% size | Bull Put (new uptrend) / Bear Call (new downtrend) at pullback |
| New trend established (price > 20 + 50SMA) | Full trend-following mode | See trend-following-with-options.md |

## Fibonacci Retracement with Options Entry

[COMPUTED] Fibonacci levels for options strike placement:

| Fibonacci Level | Uptrend Pullback Entry | Downtrend Rally Entry | Strike Placement |
|----------------|----------------------|---------------------|-----------------|
| 23.6% | Too shallow. Wait or skip | Too shallow. Wait or skip | — |
| 38.2% | Bull Put Spread. Short at this level | Bear Call Spread. Short at this level | Slightly OTM from level |
| 50.0% | Strong entry. Short at 50% level | Strong entry. Short at 50% level | ATM or slightly ITM for credit |
| 61.8% | Cautious entry. Wider strikes. Closer stop | Cautious entry. Wider strikes. Closer stop | Further OTM (lower delta) |
| 78.6% | Do not enter. Reversal risk too high | Do not enter. Reversal risk too high | — |

## Support/Resistance with Options Strikes

### Strike Placement Around Key Levels

```
Support zone in uptrend:
- Short put strike: AT or slightly BELOW support
  (If support at $100, short $99 or $100 put)
- Stop loss: Daily close below support - 1 ATR
  (If support at $100 and ATR = $2, stop at daily close < $98)

Resistance zone in downtrend:
- Short call strike: AT or slightly ABOVE resistance
  (If resistance at $110, short $110 or $111 call)
- Stop loss: Daily close above resistance + 1 ATR
```

### The False Breakout Trap

[BACKTEST-EVIDENCE] False breakouts are common at support/resistance levels:

```
Strategy: Enter AFTER the level is tested and HOLDS, not in anticipation.

WRONG: "SPY approaching $500 support — I'll sell a $500 put spread now at $498"
  → If support breaks, the short put is ITM immediately

RIGHT: Wait for SPY to touch $500, bounce, and confirm with a green daily candle.
  → THEN sell the $500 put spread (or $498 for margin of safety)
```

## Gap Strategies with Options

### Gap Fill Probability

[VERIFIED] Gaps fill ~60-70% of the time (varies by gap type):

| Gap Type | Fill Rate | Options Strategy | DTE |
|----------|----------|-----------------|-----|
| Common gap (no news) | ~70% | Debit spread toward the gap | 14-21 DTE |
| Breakaway gap (trend start, high vol) | ~30% | Do not fade. Trade in gap direction | 30-45 DTE |
| Runaway gap (mid-trend, continuation) | ~40% | Trade in gap direction, tighter stop | 21-30 DTE |
| Exhaustion gap (trend end, reversal) | ~80% | Fade the gap. Debit spread opposite direction | 14-21 DTE |

### Gap Fade with Options

```
Setup: SPY gaps down 1.5% from $500 to $492.50 (common gap on no news)
Strategy: Gap fill expected within 3-7 days

Entry: Bull Put Spread
  Short put: $490 (below gap low for margin of safety)
  Long put: $485 (5-wide)
  DTE: 21 days
  Target: 50% of credit OR gap filled (SPY back to $498+)
  Stop: SPY makes a new low below gap low
```

## The "Score Doesn't Matter" Rule for Pullbacks

[BACKTEST-EVIDENCE] **Repeating the #1 Trading project lesson:** Higher trend/entry scores do NOT correlate with better pullback trade outcomes. When entering pullbacks:

1. **Ignore the absolute score.** Use it only for direction (is the trend up or down?)
2. **Focus on pullback depth** (38.2-61.8% is the sweet spot regardless of score)
3. **Volume on pullback matters more than entry score** (low volume pullback = healthy)
4. **RSI reset matters more than entry score** (oversold/overbought condition reset = better entry)

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Entering a "pullback" that broke the 50SMA | A pullback that breaks the 50SMA is a potential reversal. Wait for confirmation before entering |
| Fading a breakaway gap | Breakaway gaps (high vol, trend start) fill only 30% of the time. Trade WITH the gap, not against it |
| Entering at first divergence signal | Divergences can persist for weeks. Wait for price confirmation (structure break) before entering |
| Using the same option structure for pullbacks and breakouts | Pullbacks = credit spreads (sell premium at support). Breakouts = debit spreads (buy momentum) |
| "The score is 92 — this pullback entry is a sure thing" | Score calibration is inverted. High scores predict mean reversion. Trust pullback depth and volume, not score |

## Provenance

[VERIFIED] Fibonacci retracement levels and gap types from technical analysis canon (Murphy, Edwards & Magee).
[COMPUTED] Gap fill rates from published research on gap behavior. Rates vary by market regime.
[BACKTEST-EVIDENCE] Score calibration inversion and false breakout observations from Trading project backtest.
[COMMON-PRACTICE] "Wait for confirmation before reversal entry" from professional swing trading methodology (Minervini, O'Neil).
[AS OF 2026-07]
