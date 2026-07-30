# Market Regime Detection

## Regime Classification

| Regime | ADX | SMA(50) Slope | ATR/Close | Signal Strategy |
|--------|-----|---------------|-----------|-----------------|
| Strong Uptrend | > 25 | > +0.1%/day | Any | Trend-following, band walks |
| Weak Uptrend | 20-25 | +0.05 to +0.1%/day | Any | Trend-following with tighter stops |
| Ranging | < 20 | Flat (±0.05%/day) | < 2% | Mean-reversion, BB reversals |
| Volatile Uptrend | > 25 | > +0.1%/day | > 3% | Trend-following, 50% position size |
| Volatile Downtrend | > 25 | < -0.1%/day | > 3% | Trend-following shorts, 50% size |
| Volatile Range | < 20 | Flat | > 3% | Stay out — no edge in chaotic ranges |

## ADX Computation
ADX measures trend strength, NOT direction. ADX > 25 = trending. ADX < 20 = ranging.
Computed from +DI and -DI (Directional Indicators) per Wilder (1978). See indicator-formulas.md.

## SMA Slope

```

slope = (SMA(50)[-1] - SMA(50)[-5]) / SMA(50)[-5]
slope > 0.001 (0.1%/day): meaningful uptrend
slope < -0.001: meaningful downtrend
|slope| < 0.0005 (0.05%/day): flat/sideways

```

## Regime Transition Detection
- ADX crossing above 20 from below: range → trend transition
- ADX crossing below 25 from above: trend → range transition
- ATR/close ratio doubling in < 5 days: volatility regime change
- Transition periods (3-5 days after regime change): reduce position size 50%, tighten stops

## Indicator Suitability by Regime

| Indicator | Trending | Ranging | Volatile |
|-----------|----------|---------|----------|
| SMA Crossovers | Excellent | Poor (whipsaw) | Fair (wider filter) |
| MACD | Excellent | Poor (noise) | Fair |
| RSI Divergence | Fair | Excellent | Poor |
| BB Mean Reversion | Poor (fade trends) | Excellent | Fair (wider bands) |
| Volume Surge | Good | Good | Good |
