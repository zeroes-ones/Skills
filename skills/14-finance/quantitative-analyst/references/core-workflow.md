# Core Workflow — Full Implementation

<!-- STANDARD: 5min overview — skim the phases, read your target phase in detail -->

<!-- DEEP: 10+min -->
### Phase 1: Data Validation (5-10 min)
<!-- DEEP: Full validation protocol — read before processing any options data -->
**Goal**: Reject bad data before it contaminates signal generation.

**Steps:**
1. **Stale quote check**: Reject any quote where (now − quote_timestamp) > 60 seconds. Options markets move fast; stale quotes produce phantom signals.
2. **Bad print filter**: Reject trades with condition codes indicating: cancelled (C), corrected (CT), late (L), out-of-sequence (O). Accept only: regular (blank/@), ISO, sweep-eligible.
3. **Dividend-adjusted chain validation**: Cross-reference ex-dividend dates within option expiration. Calls on stocks going ex-div within DTE will have adjusted strikes. Flag and exclude from UOA unless dividend adjustment is explicitly modeled.
4. **Earnings blackout**: Flag all trades within 2 calendar days of the underlying's next earnings date. Pre-earnings options activity is predominantly hedging, not directional bets.
5. **Bid-ask spread sanity**: Reject options where (ask − bid) / mid > 25% (illiquid strikes produce noise). For mid-caps, threshold may relax to 35%.
6. **Volume-to-OI sanity**: If volume > 5× open interest AND premium < $100K, possible data error — flag for manual review.

**Output**: Cleaned options trade log with `is_valid`, `rejection_reason` columns.

<!-- DEEP: 10+min -->
### Phase 2: UOA Detection (10-20 min)
<!-- DEEP: Full UOA pipeline — this is the core differentiator -->
**Goal**: Identify unusual options activity meeting premium, volume, and condition thresholds.

**Steps:**
1. **Premium threshold filter**: Single trade premium ≥ $1,000,000 OR cumulative premium in strike/expiry within 5-min window ≥ $1,000,000.
2. **OI comparison**: Compute `volume / open_interest` ratio at the trade's strike+expiry. Ratio > 1.0 = new position opening (high conviction). Ratio < 0.3 = likely closing (fade signal). Ratio 0.3-1.0 = indeterminate.
3. **Average volume comparison**: Compute 20-day rolling average volume at this strike. Flag if today's volume > 10× average.
4. **Condition code classification** (see Decision Tree 1 above): ISO → SWEEP; exchange single large print → BLOCK; floor execution → FLOOR; multi-exchange same-second fills → SWEEP.
5. **Side determination**: Compare trade price to contemporaneous bid/ask midpoint. Price ≥ ask → ASK-side (bought, aggressive). Price ≤ bid → BID-side (sold, aggressive). Bid < price < ask → mid (passive/negotiated, ambiguous).
6. **Multi-leg detection**: Within a 60-second window for the same underlying, detect: same strike, opposite type → straddle; adjacent strikes, same type → vertical spread; non-adjacent strikes, same type, same side → strangle; three strikes with ratio → butterfly/condor.
7. **Sector/ETF context**: Cross-reference the underlying with its sector ETF performance. Sector tailwind (+2% on week) amplifies bullish call signals; sector headwind dampens them.

**Python pseudocode for UOA detection:**
```python
def detect_uoa(trades: pd.DataFrame, quotes: pd.DataFrame,
               oi: pd.DataFrame, min_premium: float = 1_000_000,
               oi_ratio_threshold: float = 1.0,
               avg_vol_multiple: float = 10.0) -> pd.DataFrame:
    """
    Detect unusual options activity from cleaned trade data.
    Returns DataFrame with UOA flags and signal metadata.
    """
    signals = []

    for (ticker, strike, expiry), group in trades.groupby(['ticker','strike','expiry']):
        # Premium aggregation within 5-min rolling window
        group = group.sort_values('timestamp')
        group['premium_5min'] = (group['premium']
            .rolling('5min', on='timestamp').sum())

        # Filter: $1M+ premium
        uoa = group[group['premium_5min'] >= min_premium]

        for _, trade in uoa.iterrows():
            # OI comparison
            current_oi = oi.loc[
                (oi.ticker == ticker) &
                (oi.strike == strike) &
                (oi.expiry == expiry), 'open_interest'
            ].values
            oi_ratio = trade['volume'] / current_oi[0] if len(current_oi) > 0 and current_oi[0] > 0 else float('inf')

            # Side determination
            bid, ask = get_contemporaneous_quote(quotes, trade)
            mid = (bid + ask) / 2
            if trade['price'] >= ask * 0.995:        # near or at ask
                side = 'ASK'
                intent = 'BULLISH' if trade['option_type'] == 'CALL' else 'BEARISH'
            elif trade['price'] <= bid * 1.005:       # near or at bid
                side = 'BID'
                intent = 'BEARISH' if trade['option_type'] == 'CALL' else 'BULLISH'
            else:
                side = 'MID'
                intent = 'NEUTRAL'

            # OI-based position assessment
            if oi_ratio > 1.0:
                position_type = 'OPENING'  # new position
            elif oi_ratio < 0.3:
                position_type = 'CLOSING'  # likely closing
            else:
                position_type = 'INDETERMINATE'

            # Build signal record
            signals.append({
                'ticker': ticker,
                'timestamp': trade['timestamp'],
                'strike': strike,
                'expiry': expiry,
                'dte': (expiry - trade['timestamp'].date()).days,
                'option_type': trade['option_type'],
                'premium': trade['premium_5min'],
                'volume': trade['volume'],
                'oi_ratio': round(oi_ratio, 2),
                'side': side,
                'intent': intent,
                'position_type': position_type,
                'condition_code': trade['condition_code'],
                'trade_classification': classify_trade_type(trade)
            })

    return pd.DataFrame(signals)
```

**Output**: `uoa_signals` DataFrame with one row per detected unusual trade.

<!-- DEEP: 10+min -->
### Phase 3: Greeks Analysis (10-15 min)
<!-- DEEP: Full Greeks computation and interpretation -->
**Goal**: Compute and validate Greeks for UOA-flagged strikes; assess IV context.

**Steps:**
1. **IV computation**: For each flagged strike, invert Black-Scholes to solve for implied volatility using the trade price. Use Newton-Raphson with initial guess σ₀ = 0.30, tolerance 1e-6, max 100 iterations. If NR fails to converge, fall back to bisection method on [0.001, 5.0].
2. **Greeks computation** (standard Black-Scholes partial derivatives):
   - **Delta (Δ)**: Δ_call = N(d₁), Δ_put = N(d₁) − 1. Interpretation: probability of expiring ITM (roughly). ATM ≈ 0.50; deep ITM → ±1.0; deep OTM → 0.
   - **Gamma (Γ)**: Γ = N'(d₁) / (S₀·σ·√T). Interpretation: rate of Delta change per $1 move in underlying. Highest ATM near expiry — explosive gamma squeezes possible. Normalize as dollar gamma: Γ_$ = Γ × S₀² × 0.01 for position sizing.
   - **Theta (Θ)**: Θ_call = −[S₀·N'(d₁)·σ] / (2√T) − r·K·e^(−rT)·N(d₂). Interpretation: daily time decay. Accelerates dramatically in final 30 days. A 7-DTE ATM option loses ~2-3% per day to Theta.
   - **Vega (ν)**: ν = S₀·√T·N'(d₁) / 100. Interpretation: dollar change per 1% IV change. High Vega = vulnerable to IV crush (post-earnings). Vega peaks ATM at ~60 DTE.
   - **Rho (ρ)**: ρ_call = K·T·e^(−rT)·N(d₂) / 100. Interpretation: sensitivity to risk-free rate. Least important Greek for short-dated options; matters for LEAPS.
3. **IV Rank & Percentile**: Compute 52-week IV range for the underlying. IV Rank = (current IV − 52wk min IV) / (52wk max IV − 52wk min IV). IV Percentile = percentile rank of current IV in 52-week distribution. IV Rank > 70 = options expensive (sell premium, fade buy signals). IV Rank < 30 = options cheap (buy premium, amplify buy signals).
4. **IV Skew analysis**: Compute 25-delta risk reversal (25Δ call IV − 25Δ put IV). Widening negative skew = growing downside fear. Compare current skew to 20-day average.
5. **Term structure**: Compare 30-day ATM IV to 90-day ATM IV. Normal contango (back-month IV > front-month IV) = no event premium. Backwardation (front-month IV > back-month IV) = event-driven premium (earnings, binary event, FOMC). Forward ratio = IV(30d) / IV(90d) > 1.15 flags event risk.
6. **Greeks validation**: Cross-check computed Greeks against data provider values (if available). Flag discrepancies > 5% for Delta, > 10% for Gamma/Theta/Vega — indicates different pricing model assumptions (rates, dividends, or wrong underlying price).

**Output**: `greeks_analysis` DataFrame with IV, all five Greeks, IV rank/percentile, skew metrics, and term structure for every UOA-flagged strike.

<!-- DEEP: 10+min -->
### Phase 4: Signal Generation (5-10 min)
<!-- DEEP: Full signal classification logic -->
**Goal**: Classify each UOA detection into a trade signal with confidence level.

**Signal Classification Matrix:**

| Signal | Premium | Side | Option | DTE Range | Moneyness | IV Rank | Position | Sector | Confidence |
|--------|---------|------|--------|-----------|-----------|---------|----------|--------|------------|
| **STRONG BUY** | ≥$5M | ASK | CALL | 30-90 | ATM/OTM | >70 | OPENING | Tailwind | HIGH |
| **BUY** | $1M-$5M | ASK | CALL | 14-90 | ATM/OTM | >50 | OPENING | Neutral+ | MEDIUM |
| **WEAK BUY** | ≥$1M | ASK | CALL | 7-14 | ATM | Any | OPENING | Any | LOW |
| **NEUTRAL** | ≥$1M | MID | Any | Any | Any | Any | INDETERMINATE | Any | NONE |
| **SELL/PUT BUY** | ≥$1M | ASK | PUT | 14-90 | ATM/OTM | >50 | OPENING | Headwind | MEDIUM |
| **FADE** | ≥$1M | BID | CALL | Any | ATM | <30 | CLOSING | Any | LOW |
| **IGNORE** | Any | Any | Any | <7 | Deep OTM | Any | Any | Any | NONE |

**Entry strategy logic:**
1. **Confirmation stacking**: UOA signal + technical breakout (price > 20-day high) + sector tailwind = upgrade confidence one level.
2. **Fade rules**: Deep OTM (<0.20 delta) options with <7 DTE and premium > $1M = lottery flow, NOT smart money. Flag as IGNORE regardless of premium.
3. **Earnings filter**: Any signal with DTE < 5 trading days before earnings = downgrade one confidence level. Pre-earnings flow is hedging, not directional.
4. **OI confirmation gate**: OPENING positions = full signal strength. CLOSING positions = invert signal (closing calls = bearish). INDETERMINATE = downgrade one level.
5. **Size-to-float check**: Premium / market_cap > 0.1% on mid-caps ($2B-$10B) = extraordinary. For mega-caps (>$200B), threshold relaxes to premium > $10M.

**Entry trigger output format:**
```json
{
  "signal_id": "UOA-2026-07-21-XYZ",
  "ticker": "XYZ",
  "timestamp": "2026-07-21T14:32:00Z",
  "signal": "STRONG_BUY",
  "confidence": "HIGH",
  "entry_trigger": {
    "type": "BREAKOUT_CONFIRMATION",
    "condition": "price > 20-day high AND volume > 1.5x avg",
    "entry_price": "market_on_breakout",
    "stop_loss": "strike * 0.85 OR -15% from entry",
    "take_profit": "strike * 1.30 OR +25% from entry"
  },
  "greeks_snapshot": {
    "delta": 0.62, "gamma": 0.041, "theta": -0.085,
    "vega": 0.23, "iv_rank": 78, "dte": 45
  },
  "evidence": [
    "$5.2M ask-side OTM calls, 45 DTE, IV rank 78",
    "OI ratio 2.3 → new positions opening",
    "Sweep execution across 3 exchanges",
    "Sector ETF +2.8% this week (tailwind)",
    "No earnings within 10 days"
  ],
  "risks": [
    "Mid-cap liquidity: wide spreads on exit",
    "IV rank 78 → options expensive, IV crush possible on sector rotation",
    "Position size: $5.2M on $4B market cap = 0.13% (significant)"
  ]
}
```

**Output**: `trade_signals.json` — one structured signal per UOA detection, ready for algorithmic-trader consumption.

<!-- DEEP: 10+min -->
### Phase 5: Signal Delivery (2-5 min)
**Goal**: Package signals for downstream consumption by algorithmic-trader skill.

**Steps:**
1. **Deduplication**: Merge signals within same ticker/strike/expiry within 15-minute window. Keep highest-premium instance.
2. **Ranking**: Sort by `confidence` (HIGH > MEDIUM > LOW) then by `premium` descending.
3. **Delivery format**: Output as structured JSON (schema above) — the algorithmic-trader skill consumes this exact format.
4. **Summary statistics**: Report total signals, STRONG BUY count, BUY count, aggregate premium, top-5 tickers by premium, sector distribution.
5. **Risk warnings**: Attach global risk context — VIX level, macro event calendar (FOMC, CPI), sector rotation signals.

**Output**: `signal_batch_YYYY-MM-DD.json` ready for handoff.
