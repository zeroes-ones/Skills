# Volume Analysis — Indicator Interpretation

## Volume as Confirmation

Volume confirms price. Price moving on low volume = low conviction. Price moving on high volume = institutional participation.

| Price Move | Volume | Interpretation |
|-----------|--------|----------------|
| Up strongly | > 2x avg | Institutional accumulation — bullish |
| Up strongly | < 0.5x avg | Low-conviction drift — likely to reverse |
| Down strongly | > 2x avg | Institutional distribution — bearish |
| Down strongly | < 0.5x avg | Low-conviction drift — likely to reverse |

## OBV — On-Balance Volume
Granville (1963). Cumulative running total of signed volume.

**Standard formula (gap-distorted):**
OBV[t] = OBV[t-1] + vol[t] * sign(close[t] - close[t-1])

**Corrected formula (intraday direction):**
OBV[t] = OBV[t-1] + vol[t] * sign(close[t] - open[t])

Use corrected formula. The standard formula accumulates volume on gap-up opens even when the day is intraday distribution.

## OBV Divergence Signals
- Price ↑, OBV ↓ or flat: Distribution under strength. Smart money selling into rally. Bearish.
- Price ↓, OBV ↑ or flat: Accumulation under weakness. Smart money buying the dip. Bullish.
- OBV making new highs before price: Leading indicator. Bullish.
- OBV making new lows before price: Leading indicator. Bearish.

## Volume Ratio

```

vol_ratio = volume / SMA(volume, 20)

< 0.5: Very low activity — signals on low volume are unreliable
0.5-1.5: Normal range
1.5-2.0: Elevated — meaningful participation
> 2.0: Volume surge — institutional activity, high conviction

```

## VWAP — Volume-Weighted Average Price
- Resets daily at market open
- Price > VWAP: intraday bullish, buyers in control
- Price < VWAP: intraday bearish, sellers in control
- VWAP is the institutional execution benchmark — reversion to VWAP is mean reversion to where most volume traded
- Best use: intraday entry refinement (buy pullbacks to VWAP in uptrends)

