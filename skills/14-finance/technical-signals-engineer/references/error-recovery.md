# Technical Signals Engineer — Error Recovery

## Symptom → Root Cause → Fix

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Indicator generates signal that looks perfect in hindsight | Repainting: indicator uses future data to compute "current" value. Common in zigzag, fractals, some ML indicators. | Lock each bar's indicator value once the next bar opens. Never recompute historical indicator values. Test: does indicator value at bar N change when bar N+1 arrives? If yes = repainting. | **Repainting indicators are the cocaine of backtesting — they make everything look amazing but destroy you in live trading.** Every bar's indicator value must be immutable once computed. |
| Multi-timeframe signals conflict: daily bullish, hourly bearish | No timeframe hierarchy. Each timeframe given equal weight. | Higher timeframe always dominates: monthly > weekly > daily > 4h > 1h > 15m. Lower timeframe refines entry within higher timeframe direction. | **The trend is your friend until the higher timeframe says otherwise.** Trade in the direction of the timeframe one level above your execution timeframe. |
| Volume analysis misleading on ETFs | ETF volume reflects basket creation/redemption, not conviction in underlying. High ETF volume ≠ high conviction in component stocks. | Separate ETF volume from single-stock volume analysis. For ETFs, use underlying aggregate volume, not ETF volume. | **ETF volume is noise for technical signals.** An ETF can trade billions in volume because of arbitrage, not because anyone has a directional view on the components. |
| Regime detection overfits to historical classifications | Training regime classifier on full dataset including future data. Regime labels assigned with hindsight bias. | Walk-forward regime classification: classify each month using only data available at that time. Retrain classifier annually on expanding window. | **Hindsight regime labels are useless for live trading.** If you need to know the future to classify the present, your regime detector is a history book, not a trading tool. |
| Signal confidence score doesn't predict outcome | Confidence scoring based on in-sample fit. No out-of-sample validation of confidence bins. | Bucket signals by confidence decile. Track win rate per decile out-of-sample for 100+ signals. If win rate doesn't monotonically increase with confidence, scoring is broken. | **Confidence is a prediction, not a feeling.** Your confidence score should predict win rate. If high-confidence signals don't win more than low-confidence ones, your scoring function is random. |

## Provenance
[VERIFIED] Technical signal failure modes from systematic trading experience
[COMPUTED] Indicator repainting detection from backtesting best practices
[AS OF 2026-01]

