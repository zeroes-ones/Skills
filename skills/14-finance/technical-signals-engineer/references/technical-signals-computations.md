# Technical Signals — Full Computation Reference

Extracted from Core Workflow for progressive disclosure. Loaded on demand when the model needs implementation-level detail.

---

## Core Workflow

<!-- STANDARD: 3min -->

### Phase 1: Compute Indicators Correctly

```

1. VERIFY DATA QUALITY
   ├── OHLCV completeness: check for NaN, zero-volume bars, pre/post-market artifacts
   ├── Sufficient history: len(close) >= max(lookback_periods) + 50 warmup bars
   └── Corporate actions adjusted: splits and dividends must be back-adjusted

   Complete when: data passes quality checks. Minimum bars verified.

2. COMPUTE TREND INDICATORS
   ├── SMA(20, 50, 200): simple moving average — sum(close[-n:]) / n
   ├── EMA(9, 21, 50): exponential — price * (2/(n+1)) + prev_EMA * (1 - 2/(n+1))
   ├── SMA slope check: (SMA[-1] - SMA[-5]) / SMA[-5] > 0.001 → uptrend
   └── Golden Cross: SMA(50) crosses above SMA(200) with volume confirmation

   Complete when: all MAs computed. Trend direction determined (up/down/sideways).

3. COMPUTE MOMENTUM INDICATORS
   ├── RSI(14): 100 - (100 / (1 + avg_gain_14 / avg_loss_14)) — Wilder smoothing
   ├── MACD(12, 26, 9): EMA(12) - EMA(26) → MACD line; EMA(9) of MACD line → signal
   ├── MACD Histogram: MACD line - signal line
   ├── Stochastic RSI(14): (RSI - min_RSI_14) / (max_RSI_14 - min_RSI_14)
   └── RSI Divergence: price makes higher high, RSI makes lower high → bearish divergence

   Complete when: all momentum indicators computed with correct formulas.

4. COMPUTE VOLATILITY INDICATORS
   ├── Bollinger Bands(20, 2): middle= SMA(20), upper= SMA(20)+2*σ, lower= SMA(20)-2*σ
   ├── %B: (close - lower) / (upper - lower)
   ├── Bandwidth: (upper - lower) / middle → squeeze when bandwidth < 10th percentile of 125-day
   ├── ATR(14): Wilder smoothed true range — for stop-loss placement, not signal generation
   └── Keltner Channels(20, 2*ATR): for breakout confirmation against Bollinger squeezes

   Complete when: volatility indicators computed. Squeeze/expansion regime identified.

5. COMPUTE VOLUME INDICATORS
   ├── OBV: cumulative volume * sign(close - prev_close)
   ├── Volume SMA(20): baseline for volume confirmation checks
   ├── Volume Ratio: current_volume / SMA(volume, 20) → >1.5 = elevated, >2.0 = surge
   └── OBV divergence: price up, OBV flat/down → distribution under strength → bearish

   Complete when: volume indicators computed. Volume confirmation ready for signal validation.

6. COMPUTE COMPOSITE INDICATORS
   ├── VWAP: cumulative(price * volume) / cumulative(volume) — reset daily
   └── VWAP position: price > VWAP = bullish, price < VWAP = bearish (intraday only)

```

### Phase 2: Generate Calibrated Buy/Sell Signals

```

1. PRIMARY SIGNAL PATTERNS (any single pattern = candidate, needs Phase 3 confirmation)
   ├── SMA Crossover Family
   │   ├── Golden Cross BULLISH: SMA(50) crosses above SMA(200)
   │   │   └── Requires: volume > SMA(vol, 20), price above SMA(200) for 3+ sessions
   │   ├── Death Cross BEARISH: SMA(50) crosses below SMA(200)
   │   │   └── Requires: volume > SMA(vol, 20), price below SMA(200) for 3+ sessions
   │   ├── EMA Bull Cross BULLISH: EMA(9) crosses above EMA(21)
   │   │   └── Short-term signal. Requires RSI > 40 (not oversold bounce trap)
   │   └── EMA Bear Cross BEARISH: EMA(9) crosses below EMA(21)
   │       └── Short-term signal. Requires RSI < 60 (not overbought pullback)
   │
   ├── RSI Signal Family
   │   ├── RSI Oversold BULLISH: RSI(14) crosses above 30 from below
   │   │   └── Requires: SMA(50) slope positive (trend context) — oversold in uptrend
   │   ├── RSI Overbought BEARISH: RSI(14) crosses below 70 from above
   │   │   └── Requires: SMA(50) slope negative (trend context) — overbought in downtrend
   │   ├── Bullish Divergence BULLISH: price makes lower low, RSI makes higher low
   │   │   └── High-conviction reversal signal. Requires volume confirmation.
   │   └── Bearish Divergence BEARISH: price makes higher high, RSI makes lower high
   │       └── High-conviction reversal signal. Requires volume confirmation.
   │
   ├── MACD Signal Family
   │   ├── MACD Bull Cross BULLISH: MACD line crosses above signal line
   │   │   └── Requires: both lines below zero (early trend) OR above zero (trend continuation)
   │   ├── MACD Bear Cross BEARISH: MACD line crosses below signal line
   │   │   └── Requires: both lines above zero (exhaustion) OR below zero (trend acceleration)
   │   ├── MACD Zero Cross BULLISH: MACD line crosses above zero
   │   │   └── Stronger than signal line cross. Wait for confirmation bar close above zero.
   │   └── MACD Zero Cross BEARISH: MACD line crosses below zero
   │       └── Stronger than signal line cross. Trend shift confirmation.
   │
   ├── Bollinger Band Signal Family
   │   ├── Band Walk (Riding the Bands) BULLISH: price walks upper band with %B near 1.0
   │   │   └── Strong trend continuation. Do NOT fade — this is NOT "overbought."
   │   ├── Band Walk BEARISH: price walks lower band with %B near 0.0
   │   │   └── Strong trend continuation. Do NOT fade — this is NOT "oversold."
   │   ├── Bollinger Squeeze: bandwidth < 10th percentile of 125-day → breakout imminent
   │   │   └── Requires ADX > 25 for direction OR wait for close outside band + volume surge
   │   ├── W-Bottom BULLISH: price makes low below lower band, rebounds, retests above lower band
   │   │   └── Requires: second low above lower band, volume higher on rebound than first low
   │   └── M-Top BEARISH: inverse of W-Bottom. Second high below upper band, lower volume.
   │
   └── Volume Confirmation Family
       ├── Volume Surge BULLISH: price up 2%+, volume > 2x SMA(vol, 20)
       │   └── Institutional accumulation signal. Strong when near support.
       ├── Volume Surge BEARISH: price down 2%+, volume > 2x SMA(vol, 20)
       │   └── Institutional distribution signal. Strong when near resistance.
       ├── OBV Confirmation BULLISH: OBV making new highs with price
       └── OBV Divergence BEARISH: price up, OBV flat/declining → distribution

2. SIGNAL SCORING (0-100 confidence)
   Score = Σ(indicator_scores) / max_possible * 100

   Individual indicator scores:
   ├── Golden/Death Cross: 40 points (high weight — rare, meaningful)
   ├── MACD signal cross: 25 points
   ├── RSI divergence: 35 points
   ├── Bollinger squeeze breakout: 30 points
   ├── EMA crossover: 15 points (lower weight — frequent, noisy)
   ├── OBV divergence: 20 points
   ├── Volume surge: 25 points — but ONLY as confirmation, not standalone
   └── Trend alignment bonus: +10 if signal direction = SMA(50) slope direction

   Confidence thresholds:
   ├── 70+: HIGH conviction — strong multi-indicator alignment, act
   ├── 50-69: MEDIUM conviction — needs additional filter (regime check)
   ├── 30-49: LOW conviction — watchlist only, do not act
   └── <30: NOISE — ignore

   Complete when: all active patterns identified with confidence scores. Signals ranked by score.

```

### Phase 3: Multi-Indicator Confirmation

```

1. TWO-CLUSTER RULE (minimum for actionable signal)
   Signals must come from at least TWO different indicator clusters:
   ├── Cluster A — TREND: SMA crossovers, EMA alignment, ADX, Supertrend
   ├── Cluster B — MOMENTUM: RSI, MACD, Stochastic, CCI
   ├── Cluster C — VOLATILITY: Bollinger Bands, Keltner Channels, ATR-based
   └── Cluster D — VOLUME: OBV, Volume SMA cross, MFI, accumulation/distribution

   Valid combinations: A+B, A+C, B+C, A+B+D, B+C+D
   Invalid (reject): A-only, B-only, D-only, A+A (two trend — redundant, not confirming)

2. REGIME FILTER (market context adjustment)
   ├── TRENDING (ADX > 25, SMA(50) slope > 0.1%/day):
   │   ├── Favor: trend-following signals (MA crossovers, MACD trend, band walks)
   │   ├── Penalize: mean-reversion signals (RSI overbought/oversold fades)
   │   └── RSI adjustment: in strong uptrend, RSI 70-80 is NOT overbought — it's trend strength
   │
   ├── RANGING (ADX < 20, SMA(50) flat ±0.05%/day):
   │   ├── Favor: mean-reversion signals (Bollinger Band touches, RSI extremes)
   │   ├── Penalize: trend-following signals (MA crossovers whipsaw)
   │   └── MACD adjustment: ignore MACD crossovers in ranges — they're noise
   │
   └── VOLATILE (ATR/close > 3%, VIX > 30 for SPX):
       ├── Widen all bands: Bollinger at 2.5σ, Keltner at 2.5 ATR
       ├── Increase RSI thresholds: oversold < 25, overbought > 75
       └── Reduce position size by 50% — signal accuracy degrades in chaos

3. TIME-FRAME ALIGNMENT (higher time frame = regime, lower = entry)
   ├── Weekly chart: defines PRIMARY trend (bull/bear/range)
   ├── Daily chart: generates SIGNALS (Phase 2 patterns)
   ├── 4-hour/60-min: refines ENTRY timing (optional for active traders)
   └── Rule: only trade signals ALIGNED with weekly trend direction

   Complete when: signal confirmed by ≥2 clusters, regime-appropriate, time-frame aligned.

```

### Phase 4: ETF-Specific and Stock-Specific Adjustments

```

1. ETF CLASSIFICATION (before computing any indicator)
   ├── STANDARD (SPY, QQQ, IWM, DIA): default parameters, default signal logic
   ├── LEVERAGED LONG (TQQQ, UPRO, SSO, UDOW):
   │   ├── Bollinger: ±2.5σ (not 2.0σ) — volatility amplified by leverage factor
   │   ├── RSI: 21-period (not 14) — need longer lookback to smooth amplified swings
   │   ├── Decay-aware: leveraged ETFs lose 3-8%/year to volatility decay in sideways markets
   │   │   └── Holding period >5 days: decay drag exceeds signal edge → reduce position 25%
   │   └── Signal direction: same as underlying but with amplified magnitude
   │
   ├── LEVERAGED SHORT/INVERSE (SQQQ, SPXU, SDOW, TZA):
   │   ├── Same parameter adjustments as leveraged long
   │   └── REVERSE ALL SIGNAL DIRECTIONS: golden cross → bearish, death cross → bullish
   │       └── RSI oversold on inverse ETF = underlying overbought → SELL inverse
   │
   ├── SECTOR ETFs (XLF, XLE, XLV, XLK, XLY, etc.):
   │   ├── Compute relative strength: sector_ETF / SPY ratio → SMA(50) of ratio
   │   ├── RS ratio rising AND absolute signal bullish → amplified conviction (+15 score)
   │   ├── RS ratio falling AND absolute signal bullish → reduced conviction (-15 score)
   │   └── Sector rotation detection: 3+ sector RS trends shifting simultaneously → macro regime change
   │
   └── COMMODITY/VOLATILITY ETFs (GLD, USO, VXX, UVXY):
       ├── VXX/UVXY: DO NOT APPLY MEAN-REVERSION SIGNALS — these decay structurally
       ├── GLD/USO: use SMA(50, 200) but ignore volume indicators (commodity volume ≠ equity volume)
       └── Contango/backwardation: check futures curve before signals on commodity ETFs

2. STOCK-SPECIFIC ADJUSTMENTS
   ├── EARNINGS WINDOW: suppress ALL signals [-2, +2] trading days around earnings
   │   └── After earnings: wait for 5 full sessions of post-earnings price discovery before resuming
   │
   ├── DIVIDEND DATES: ex-dividend date = price drops by dividend amount
   │   └── Suppress signals on ex-div date — price drop is mechanical, not a sell signal
   │
   ├── STOCK SPLITS: recalculate ALL indicators post-split with adjusted history
   │   └── Never compute indicators across a split boundary without split-adjusted data
   │
   ├── LOW FLOAT / LOW VOLUME (<$5M avg daily volume):
   │   ├── Bollinger Bands unreliable — low liquidity distorts σ calculation
   │   ├── RSI prone to manipulation — ignore or require 2x normal divergence confirmation
   │   └── OBV meaningless — single institution trade can flip cumulative volume
   │
   └── GAP-ADJUSTED ENTRIES:
       ├── Gap up >2% from previous close → adjust buy entry to VWAP or gap-fill level
       ├── Gap down >2% → adjust sell entry to VWAP or gap-fill level
       └── Gap >5% → suppress signal entirely (event-driven move, not technical)

   Complete when: all asset-class adjustments applied. Parameters differ by ETF type. Earnings/dividend windows suppressed.

```

### Phase 5: Portfolio Scanning and Signal Output

```

1. BATCH SCAN INPUT
   ├── Ticker list: ["SPY", "QQQ", "AAPL", "MSFT", ...]
   ├── Scan type: ALL (all indicators), CROSSOVER_ONLY, RSI_ONLY, SQUEEZE_ONLY
   ├── Min confidence: default 50 (medium+), adjustable
   └── Asset-class aware: ETF vs stock parameters auto-selected per ticker

2. SIGNAL OUTPUT STRUCTURE (every signal must include ALL fields)
   {
     "ticker": "AAPL",
     "asset_type": "stock",
     "signal_date": "2026-07-30",
     "signal_type": "BULLISH",
     "confidence": 72,
     "patterns": [
       {"name": "Golden Cross", "cluster": "trend", "score": 40},
       {"name": "Volume Surge", "cluster": "volume", "score": 25},
       {"name": "Trend Alignment", "score": 10}
     ],
     "confirming_clusters": ["trend", "volume"],
     "regime": "trending",
     "regime_aligns": true,
     "timeframe_alignment": {"weekly": "bullish", "signal_direction": "bullish", "aligned": true},
     "entry_price": 195.50,
     "stop_loss": 189.80,
     "take_profit_1": 205.00,
     "take_profit_2": 215.00,
     "invalidated_by": null,
     "warnings": [],
     "earnings_window": false,
     "data_quality": {"bars": 252, "gaps": 0, "adjusted": true}
   }

3. SIGNAL PRIORITIZATION (when multiple tickers fire)
   ├── Sort by: confidence DESC, volume_ratio DESC
   ├── Top 5 by confidence get detailed signal cards
   └── Remaining above threshold: summary table only

   Complete when: All tickers scanned. Signals output in structured JSON with all required fields.

```

## Decision Trees


