# Multi-Timeframe Analysis

## Timeframe Hierarchy

| Timeframe | Function | Weight |
|-----------|----------|--------|
| Monthly | Secular trend (multi-year) | Background context |
| Weekly | Primary trend (months) | HIGH — defines trade direction |
| Daily | Signal generation | PRIMARY — all signals generated here |
| 4-Hour | Entry refinement | Optional — for active traders |
| 60-Min | Entry timing | Optional — for day traders |

## The Unbreakable Rule

**Only trade signals in the direction of the weekly trend.**

- Weekly uptrend + daily buy signal = TRADE
- Weekly uptrend + daily sell signal = IGNORE (counter-trend)
- Weekly downtrend + daily sell signal = TRADE
- Weekly downtrend + daily buy signal = IGNORE (counter-trend)
- Weekly sideways + any daily signal = FILTER through regime check

## Weekly Trend Determination

```

weekly_sma_slope = (SMA(50, weekly_close)[-1] - SMA(50, weekly_close)[-4]) / SMA(50, weekly_close)[-4]

slope > 0.02 (2% over 4 weeks): UPTREND
slope < -0.02: DOWNTREND
|slope| <= 0.02: SIDEWAYS

```

## Entry Refinement (4-Hour)

When daily signal fires, use 4-hour chart for entry timing:
- Buy signal: enter on 4-hour pullback to VWAP or EMA(21) — not at the high of the signal day
- Sell signal: enter on 4-hour bounce to VWAP or EMA(21) — not at the low of the signal day

This improves average entry by 0.5-1.5% vs. entering at signal bar close.

## Timeframe Alignment Table

| Weekly | Daily Signal | Action |
|--------|-------------|--------|
| Bullish | Bullish | ACT — aligned, full size |
| Bullish | Bearish | IGNORE — counter-trend fade risk |
| Bearish | Bearish | ACT — aligned, full size |
| Bearish | Bullish | IGNORE — counter-trend bounce trap |
| Sideways | Bullish | FILTER — regime check, 50% size |
| Sideways | Bearish | FILTER — regime check, 50% size |

