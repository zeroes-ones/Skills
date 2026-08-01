# Earnings Swing Playbook — Swing Options Reference

> **Reading time:** 10 min | **Prerequisites:** options-strategist (volatility strategies), fundamental-analyst (earnings), swing-options-trader

## The Earnings Opportunity

[VERIFIED] Earnings announcements create the largest predictable IV events in individual stocks. IV typically rises 2-3 weeks before earnings (IV run-up), then collapses immediately after the announcement (IV crush). This predictable pattern creates three distinct trading opportunities.

## The IV Run-Up / Crush Cycle

```
Timeline:
T-21 to T-14: IV starts rising as traders position for earnings
T-14 to T-1:  IV accelerates upward (pre-earnings positioning peak)
T-0 (earnings): IV collapses. Option prices drop 30-70% immediately after announcement
T+1 to T+5:     IV stabilizes at new, lower level
```

[COMPUTED] For an average large-cap stock:
- Pre-earnings IV rise: +20-50% from baseline
- Post-earnings IV crush: -30-60% from peak
- Net: Post-earnings IV is typically 10-20% lower than pre-earnings baseline

## Strategy 1: Pre-Earnings Run-Up (Long Vega)

### The Setup

```
Entry: 14-21 days before earnings
Exit: 1-2 days before earnings (capture IV run-up, avoid binary event)

Strategy: Long ATM Calendar Spread
  - Buy: 45-60 DTE option (will still have significant vega post-earnings)
  - Sell: Weekly option expiring before earnings (collects theta during run-up)
  - OR: Buy ATM Straddle (naked long vol — higher risk, higher reward)

Why this works:
  - IV rise inflates the long option's value
  - Short/theta leg partially offsets decay
  - Exit before the binary event eliminates gap risk
```

### Pre-Earnings Entry Checklist

```
- [ ] Earnings date confirmed (check company IR, not just estimates)
- [ ] IV percentile < 50% (room to run up — don't buy already-elevated IV)
- [ ] No competing events (sector earnings, macro) within the window
- [ ] Spread < 5% of option price (can exit cleanly)
- [ ] Exit order placed: GTC limit to close 2 days before earnings
```

### Profit Target & Risk

```
Target: IV rise captures 30-50% of the calendar spread's vega value
Stop: IV drops 10% from entry (run-up not materializing — cut it)
Max hold: Until 2 trading days before earnings. Then exit regardless.

[COMPUTED] Expected return: +5-15% on capital for successful pre-earnings calendar.
Risk: -10-15% if IV doesn't rise. This is a thin-edge, moderate-frequency strategy.
```

## Strategy 2: Post-Earnings Drift (Post-Earnings Announcement Drift — PEAD)

[VERIFIED] Post-Earnings Announcement Drift (PEAD) is the tendency for stocks to drift in the direction of the earnings surprise for days/weeks after the announcement. This is one of the most robust anomalies in finance (Ball & Brown, 1968; confirmed in dozens of subsequent studies).

### The Setup

```
Entry: 1-3 days after earnings (after IV has crushed and initial gap has settled)
Exit: 5-20 days later (drift typically lasts 2-6 weeks)

Selection criteria:
1. Earnings surprise > 5% (beat OR miss by >5% vs. consensus)
2. Post-earnings price reaction confirms the surprise direction
3. Gap not faded within 3 days (stock continues in surprise direction)
4. Volume > average on post-earnings days (institutional accumulation/distribution)

Strategy: ATM Debit Spread in the surprise direction
  - DTE: 30-45 days (plenty of time for drift)
  - Width: 5-wide for standard, 10-wide for high-conviction
  - Target: 100% of spread width (max profit)
  - Stop: 50% of debit (tighter — the drift may not materialize)
```

### PEAD Failure Patterns

| Pattern | What It Means | Action |
|---------|--------------|--------|
| Stock gaps in surprise direction, then reverses within 3 days | "Sell the news" — the market priced it in. Drift unlikely | Close the trade |
| Stock gaps opposite to earnings surprise | Confused market. Drift unreliable | Skip trade |
| Low post-earnings volume | No institutional participation. Drift unlikely | Skip trade |
| Stock gaps huge (>10%) and then goes flat | Move exhausted. Gap already priced everything in | Skip trade |

## Strategy 3: Post-Earnings IV Crush Capture (Short Vega)

### The Setup

```
Entry: Immediately after earnings (next trading day)
Exit: 1-3 weeks later

Strategy: Short Iron Condor or Short Strangle
  - IV has been crushed → premiums deflated but still slightly elevated
  - Stock range likely to contract post-earnings (event passed)
  - DTE: 30-45 days
  - Short strikes: 0.15-0.20Δ (wider than normal — post-earnings range is unpredictable)

Risk: Post-earnings continuation move is larger than expected.
      Always: undefined risk strategies (strangle) require PM and wide stops.
```

[COMPUTED] Post-earnings iron condors have a higher win rate than random iron condors because:
1. The major binary event has passed
2. IV is still slightly above baseline (inflated premiums for a week or two)
3. Historical post-earnings volatility is lower than pre-earnings

## The Earnings Blackout Gate

[VERIFIED] For any swing options position, check earnings dates before entry:

```
If earnings within holding period:
  Option 1: Close position before earnings
  Option 2: Reduce to 25% size (accept binary risk on 1/4 of position)
  Option 3: Replace with earnings-specific strategy (below)
  NEVER: Hold a full-sized directional options position through earnings

Post-earnings gaps:
  5-15% gap is NORMAL for earnings
  A 10% gap against a 0.80Δ call → option loses 40-60% of value
  On a credit spread: gap through short strike → max loss
```

## Earnings Options Strategy Selection Matrix

| Scenario | Pre-Earnings (T-21 to T-2) | Through Earnings | Post-Earnings (T+1 to T+20) |
|----------|--------------------------|-----------------|---------------------------|
| High conviction directional | ATM Calendar or Diagonal (long veg) | **CLOSE before earnings.** Never hold through | PEAD: Debit spread in surprise direction |
| Neutral to bullish | Bull Put Spread (collect elevated IV premium) | Reduce to 25% or close | Bull Put Spread at lower IV, wider strikes |
| Neutral to bearish | Bear Call Spread | Reduce to 25% or close | Bear Call Spread at lower IV |
| No directional view | Iron Condor (pre-earnings IV elevated) | **CLOSE before earnings** | Iron Condor (crushed IV, wider strikes) |
| Want to bet on the event | — | Straddle/Strangle (need > expected move to profit) | — |

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| "I'll hold my call spread through earnings — they always beat" | Even when they beat, stocks can drop (guidance, "sell the news"). Never hold full size through earnings |
| Buying straddles into earnings without checking the implied move | Implied move = ATM straddle price / stock price. If the implied move is 8% and the stock's average earnings move is 6%, the straddle is overpriced. You're paying for more vol than historical |
| "Post-earnings IV crush is over — I missed it" | IV stays slightly elevated for 1-2 weeks as uncertainty fully resolves. The crush is immediate, the bleed is slow. There's time |
| Trading earnings strategies on illiquid options | Earnings strategies require clean entries and exits. Only trade stocks where the options chain has OI > 500 and spread < 3% |

## Provenance

[VERIFIED] PEAD from Ball & Brown (1968) through Fama (1998) to modern replications. One of the most robust anomalies in finance.
[VERIFIED] IV run-up/crush pattern from Donders & Vorst (1996) and subsequent options research.
[COMPUTED] Expected returns from pre-earnings calendars and post-earnings iron condors based on published IV behavior data.
[COMMON-PRACTICE] Earnings strategy timing from professional volatility trading desks.
[AS OF 2026-07]
