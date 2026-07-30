# ETF Classification and Parameter Adjustments

## ETF Type Matrix

| Type | Examples | BB Std Dev | RSI Period | Volume Indicators | Signal Direction |
|------|----------|-----------|------------|-------------------|-----------------|
| Standard 1x | SPY, QQQ, IWM, DIA | 2.0σ | 14 | Standard | Standard |
| Leveraged 2x Long | SSO, UDOW, QLD | 2.3σ | 18 | Standard | Standard |
| Leveraged 3x Long | TQQQ, UPRO, UDOW | 2.5σ | 21 | Standard | Standard |
| Leveraged 2x Inverse | SDS, DXD, QID | 2.3σ | 18 | Standard | REVERSE |
| Leveraged 3x Inverse | SQQQ, SPXU, SDOW | 2.5σ | 21 | Standard | REVERSE |
| Sector | XLF, XLE, XLV, XLK, XLY | 2.0σ | 14 | Standard + RS | Standard |
| Commodity | GLD, SLV, USO | 2.0σ | 14 | SKIP | Standard |
| Volatility | VXX, UVXY, VIXY | 3.0σ | 21 | SKIP | Do NOT trade mean-reversion |

## Leveraged ETF Decay Mechanics

Daily reset leveraged ETFs suffer volatility decay:

```

Annual decay ≈ (leverage_factor^2 - leverage_factor) * σ^2 / 2
For TQQQ (3x) with σ = 25%: decay ≈ (9-3) * 0.0625 / 2 = 18.75% annually in sideways markets

```

Holding period > 5 days: decay exceeds signal edge for most technical strategies.
- Reduce position size by 25% for holds 5-20 days
- Do not hold leveraged ETFs through weekends without a stop

## Inverse ETF Signal Reversal

For inverse ETFs (SQQQ, SPXU, etc.):
- Golden cross on SQQQ = QQQ making new lows = BEARISH for SQQQ holders
- RSI oversold on SQQQ = QQQ overbought = SELL SQQQ signal
- BB lower band touch on SQQQ = QQQ upper band = RESISTANCE on QQQ

**Rule: Reverse ALL signal directions for inverse ETFs. A buy signal on SQQQ means the underlying (QQQ) is breaking down.**

## Sector ETF Relative Strength

```

RS(ticker) = ticker_close / SPY_close
RS_sma50 = SMA(50, RS)
RS_trend = RS_sma50[-1] - RS_sma50[-20]

RS_trend > 0.02: sector outperforming → amplify buy signals (+15 confidence)
RS_trend < -0.02: sector underperforming → dampen buy signals (-15 confidence)

```

Sector rotation detected when 3+ sectors shift RS trend direction simultaneously.

## Commodity ETF Adjustments

- Volume indicators (OBV, volume ratio) are RELIABLE for equity ETFs but UNRELIABLE for commodity ETFs
- Commodity volume represents speculative flow, not accumulation/distribution
- Check contango/backwardation for oil (USO) and VIX futures curve for VXX
