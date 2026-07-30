# Indicator Formulas — Exact Mathematical Definitions

## SMA (Simple Moving Average)

```

SMA(n) = (P[t] + P[t-1] + ... + P[t-n+1]) / n

```

Source: Statistical standard. Requires n valid closing prices.

## EMA (Exponential Moving Average)

```

EMA(n)[t] = P[t] * α + EMA(n)[t-1] * (1 - α)
where α = 2 / (n + 1)
Seed: EMA(n)[n-1] = SMA(n) over first n periods

```

Source: Welles Wilder adaptation of standard exponential smoothing.

## RSI — Wilder's Relative Strength Index

```

RSI(14) = 100 - (100 / (1 + RS))
RS = avg_gain_14 / avg_loss_14

avg_gain_14[0] = sum(gains over first 14 periods) / 14
avg_gain_14[t] = (avg_gain_14[t-1] * 13 + gain[t]) / 14
avg_loss_14[0] = sum(losses over first 14 periods) / 14
avg_loss_14[t] = (avg_loss_14[t-1] * 13 + loss[t]) / 14

gain[t] = max(P[t] - P[t-1], 0)
loss[t] = max(P[t-1] - P[t], 0)

```

Source: Welles Wilder, _New Concepts in Technical Trading Systems_ (1978), pp. 63-70.
CRITICAL: Use Wilder smoothing (recursive), NOT simple average. Simple average produces incorrect values.

## MACD — Moving Average Convergence Divergence

```

MACD Line = EMA(12, close) - EMA(26, close)
Signal Line = EMA(9, MACD Line)
Histogram = MACD Line - Signal Line

```

Source: Gerald Appel, _Technical Analysis: Power Tools for Active Investors_ (2005).
All EMAs use standard exponential smoothing with α = 2/(n+1).

## Bollinger Bands

```

Middle Band = SMA(20, close)
Upper Band = SMA(20) + k * σ(20)
Lower Band = SMA(20) - k * σ(20)
σ(20) = population standard deviation of close over 20 periods
k = 2.0 (standard), k = 2.5 (leveraged ETFs)

%B = (close - Lower) / (Upper - Lower)
Bandwidth = (Upper - Lower) / Middle

```

Source: John Bollinger, _Bollinger on Bollinger Bands_ (2002).
σ is population std dev (dividing by n), not sample std dev (dividing by n-1) — Bollinger's specification.

## ATR — Average True Range (Wilder)

```

TR = max(high - low, |high - prev_close|, |low - prev_close|)

ATR(14)[0] = sum(TR over first 14 periods) / 14
ATR(14)[t] = (ATR(14)[t-1] * 13 + TR[t]) / 14

```

Source: Welles Wilder, _New Concepts in Technical Trading Systems_ (1978), pp. 22-25.
Uses same Wilder smoothing as RSI.

## OBV — On-Balance Volume (Corrected for Gaps)

```

Standard (has gap distortion): OBV[t] = OBV[t-1] + volume[t] * sign(close[t] - close[t-1])

Corrected (intraday direction): OBV[t] = OBV[t-1] + volume[t] * sign(close[t] - open[t])

```

Source: Joseph Granville, _Granville's New Key to Stock Market Profits_ (1963).
The corrected formula using `close > open` captures intraday buying/selling pressure regardless of overnight gaps.

## VWAP — Volume-Weighted Average Price

```

VWAP = Σ(price[i] * volume[i]) / Σ(volume[i])
for all trades in current session. Reset daily.

```

Source: Institutional trading standard. Used by algorithms for execution quality measurement.

## Stochastic RSI

```

StochRSI = (RSI - min(RSI, n)) / (max(RSI, n) - min(RSI, n))
where n = 14, RSI = Wilder RSI(14)

```

Source: Tushar Chande and Stanley Kroll, _The New Technical Trader_ (1994).

## ADX — Average Directional Index

```

+DM = max(high - prev_high, 0) if high - prev_high > prev_low - low, else 0
-DM = max(prev_low - low, 0) if prev_low - low > high - prev_high, else 0
+DI = EMA(14, +DM) / ATR(14) * 100
-DI = EMA(14, -DM) / ATR(14) * 100
DX = |+DI - -DI| / (+DI + -DI) * 100
ADX = EMA(14, DX)

```

Source: Welles Wilder, _New Concepts in Technical Trading Systems_ (1978), pp. 35-50.
All EMAs use Wilder smoothing (same as RSI/ATR).

