# Momentum & ORB with Options — Intraday Options Reference

> **Reading time:** 10 min | **Prerequisites:** technical-signals-engineer (ORB, momentum), options-strategist, intraday-options-trader

## Using Options Instead of Shares for Intraday Setups

[COMMON-PRACTICE] Options offer defined risk (for buyers), leverage, and capital efficiency for intraday trades — but come with spread costs and theta decay that shares don't have. For setups lasting < 4 hours, options can be superior IF spreads are tight and DTE is right.

## Opening Range Breakout (ORB) with Options

### Classic ORB Setup

```
Opening Range: 9:30-9:35 (5 min) or 9:30-10:00 (30 min)
Breakout: Price breaks above OR high (long) or below OR low (short)
Target: OR width projected from breakout point
Stop: Other side of OR
```

### Options vs. Shares for ORB

| Factor | Shares | Options (ATM, 7+ DTE) |
|--------|--------|----------------------|
| Leverage | 1:1 | 5-20:1 (depending on strike/DTE) |
| Defined risk | No (stop-loss needed) | Yes (premium paid) |
| Spread cost | 1 tick ($0.01) | 2-5% of option price |
| Theta decay | None | -$0.50 to $2.00 per hour (for ATM near-dated) |
| Gap risk | Full | Capped at premium |
| Best when | Tight spreads on shares, overnight gap risk is acceptable | Want defined risk, need leverage, options liquid |

### ORB Options Strategy Selection

| ORB Signal Strength | Best Options Structure | Rationale |
|--------------------|-----------------------|------------|
| Strong (volume confirmation, broad market aligned) | ATM Debit Spread (5-wide, 60-70 DTE) | Higher probability, lower theta decay than single leg |
| Moderate (volume OK, broad market neutral) | ATM Long Call/Put (7-14 DTE) | Simpler, no short leg to manage, but theta is higher |
| Weak (low volume, broad market against) | Skip trade or ATM Butterfly (0DTE) | Butterfly if SPX pin-seeking; otherwise no trade |

[BACKTEST-EVIDENCE] From Trading project: ORB setups on individual stocks with options underperform ORB with shares due to spread costs on the options side. ORB with SPX/SPY options is viable due to tight spreads.

## Momentum Entry with Options

### Momentum Confirmation

```
Must confirm ALL 3:
1. Volume: Current bar volume > previous 5 bars average × 1.5
2. Price: Price making new 5-minute high/low in direction of momentum
3. Delta: T&S shows more prints at ask than bid (2:1+ ratio for longs, reversed for shorts)
```

### Momentum Options Strategy

```
Setup: Strong momentum candle confirmed (all 3 conditions met)
Entry: ATM or slightly OTM Call (for long) or Put (for short)
Strike: 1 strike OTM (Δ=0.40-0.50)
DTE: 7-14 DTE (enough theta buffer for intraday hold)
Exit: 50% of options profit OR momentum reversal (confirmed by T&S flip)
Stop: 30% of premium paid (tight — momentum fades fast)
```

[COMPUTED] With 50% profit target and 30% stop:
- Win rate needed for breakeven: 37.5%
- With 45% win rate: EV = (0.45 × 50%) + (0.55 × -30%) = +6% per trade
- After spread costs (~3-5%): net +1-3% per trade

This is thin. Momentum with options needs >50% win rate or tighter stops.

### FalseStopGuard for Momentum Options

[BACKTEST-EVIDENCE] From the Trading project: FalseStopGuard is a 4-layer exit confirmation that prevents premature exits on noise:

```
Layer 1 (Liquidity): Is the pullback on above-average volume? If no → likely noise
Layer 2 (Wick): Is there a long wick in the opposite direction? If no → continuation pattern, not reversal
Layer 3 (Volume): Did the pullback bar have >120% of trailing 5-bar average volume? If no → not a reversal
Layer 4 (Thin Window): Is the pullback confined to <3 consecutive bars? If yes → noise, not reversal

Exit only if: Layer 1 OR (Layer 2 AND Layer 3) confirms. Otherwise: hold.
```

## News/Event Intraday Options Trading

### FOMC Minutes / Rate Decision (2:00 PM)

```
Pre-FOMC: IV elevated. Strategy = sell premium (iron condor, short strangle)
  BUT: do NOT hold through the announcement unless you want to bet on vol crush magnitude
Post-FOMC (2:00-2:30 PM first reaction): Huge vol. NO new entries. Let the market digest
Post-FOMC (2:30-4:00 PM): IV crushed, but realized vol still elevated.
  Strategy = buy ATM straddle (vol already crushed, scalp if the trend continues)
```

### CPI / NFP / Economic Data (8:30 AM)

```
Pre-release: Position flat. Do not hold options through 8:30 AM data
Post-release (9:30 AM open): Gap open. Assess gap size vs. expected move
  Gap < expected move → gap fade trade (contrarian)
  Gap > expected move → gap continuation trade (momentum)
Best structure: ATM debit spread (defined risk, defined reward, lower theta than single leg)
```

### Unexpected News (Mid-Session)

```
1. Determine if news is structural (earnings revision, M&A, regulatory) or noise (analyst note, rumor)
2. Structural news → trade the direction with ATM options (momentum). Size: 25% of normal
3. Noise → fade the move with OTM credit spreads. Size: 50% of normal
4. If unsure → skip. Unexpected news creates wide spreads and unpredictable reversals
```

## The Gamma Tightening Rule

[BACKTEST-EVIDENCE] From the Trading project data:

```
For DTE ≤ 7 (including intraday holdings):
  Add +5% to stop buffer (e.g., 30% stop → 35% stop)
  Reason: Gamma acceleration near expiration causes exaggerated moves
  A noise wick can breach a tight stop on a near-dated option

For DTE ≤ 3:
  Add +10% to stop buffer
  Reason: Extreme gamma. Standard stops will be triggered by noise
```

## Position Sizing for Intraday Options

```
Intraday max position = (account_value × daily_risk_pct) / (option_premium × 100)

Example:
  $50,000 account, 1% daily risk max = $500 max loss
  ATM SPY call, $3.00 premium = $300/contract
  Max contracts = $500 / $300 = 1 contract

Intraday-specific adjustments:
- First trade of day: 100% of max size (fresh mental capital)
- After a win: 75% of max size (counter overconfidence bias)
- After a loss: 50% of max size (counter revenge trading bias)
- After 2 consecutive losses: STOP for the day. No exceptions
- After 3 wins: Reduce to 50% (reversion to mean in win rate incoming)
```

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Using shares-style stop-losses on options | Options moves are non-linear. A 1% stock move ≠ 1% option move. Use option price stops or delta-adjusted stops |
| Trading momentum with 0DTE options | 0DTE moves too fast for momentum confirmation. Use 7+ DTE for momentum trades |
| Ignoring spread cost in win-rate math | Factor 2-5% spread cost into every trade. At 5 trades/day, spread costs = 10-25% of daily P&L |
| ORB with options on individual stocks | SPX/SPY only for ORB with options. Individual stock options have spreads too wide for ORB entries |
| Adding to losers intraday | Never double down on an intraday options trade. Gamma and theta are both working against you |

## Provenance

[VERIFIED] ORB methodology from Tony Crabel's "Day Trading with Short Term Price Patterns" and modern adaptations.
[COMPUTED] Options EV calculations for momentum trades. Assumes 30% stop, 50% target, 45% win rate. Actual results vary.
[BACKTEST-EVIDENCE] FalseStopGuard 4-layer exit, gamma tightening rule from Trading project backtest analysis.
[COMMON-PRACTICE] Post-FOMC vol crush scalp from professional day trading desks.
[AS OF 2026-07]
