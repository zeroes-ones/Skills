# UOA Strategy Integration

## Purpose
Framework for integrating Unusual Options Activity (UOA) data into every stage of the options trading lifecycle — strategy selection, strike placement, position sizing, and exit timing. UOA provides a real-time window into institutional positioning. When used correctly, it adds a 10–20% edge to strategy performance. When misused (single-print chasing, no OI confirmation), it is worse than noise — it's actively misleading.

---

## UOA Signal Types and Classification

### Signal Categories

| Signal Type | Detection Criteria | Reliability | Typical Timeframe |
|------------|-------------------|-------------|-------------------|
| **Call Sweep Above Ask** | Multiple call contracts executed at the ask price in rapid succession, clearing multiple exchange levels | HIGH (if OI confirms) | 1–5 days |
| **Put Sweep Below Bid** | Multiple put contracts executed at the bid price, aggressive selling | HIGH (if OI confirms) | 1–5 days |
| **Block Trade** | Single trade > $500K notional, typically executed in dark pools or as a negotiated trade | MODERATE | 14–60 days |
| **Multi-Leg Sweep** | Spread, straddle, strangle, or butterfly executed as a package at scale (> $250K notional) | HIGH | 7–30 days |
| **Opening Print (Volume > OI)** | Volume on a strike exceeds the prior day's open interest — position is being OPENED, not closed | HIGH | 1–14 days |
| **Closing Print (Volume < OI Change)** | Volume is less than the decline in OI — positions are being CLOSED | LOW — noise | N/A |
| **Dark Pool Print** | Large trade executed off-exchange, visible only via consolidated tape or specialized data feeds | MODERATE-HIGH | 30–90 days |
| **Sweep on Illiquid Strike** | High volume on a strike with wide bid-ask and low OI — often a single gambler, not institutional | VERY LOW — ignore | N/A |

[VERIFIED] The single most important UOA filter: volume on a strike MUST exceed the prior day's open interest by at least 1.5× for the print to be considered "opening activity" (a genuine new position). If volume/OI ratio < 1.0, the activity is closing — someone exiting, not entering. Closing activity carries zero predictive value.

---

## UOA Signal → Strategy Mapping

### Bullish Flow: Call Sweeps Above Ask

| IV Rank | UOA Context | Recommended Strategy | Rationale |
|---------|------------|---------------------|-----------|
| < 25 | Call sweeps + OI building + sector confirmation | **Bull Call Spread (debit)** | Low IV = cheap calls. UOA confirms direction. Buy calls — vega helps if IV rises. |
| 25–50 | Call sweeps + OI building | **Bull Put Spread (credit)** | Normal IV. Sell puts instead of buying calls — capture theta AND align with bullish flow. |
| 50–75 | Call sweeps + OI building + multiple strikes | **Short Put (CSP or naked)** | Elevated IV = rich put premium. UOA says bullish → sell puts, collect elevated IV premium. Direction via puts. |
| 75–100 | Call sweeps at scale (>$2M notional) | **Bull Put Spread (defined risk)** | Extreme IV is dangerous. Sell puts but cap risk with spreads. IV mean reversion will deliver rapid profits. |

### Bearish Flow: Put Sweeps Below Bid

| IV Rank | UOA Context | Recommended Strategy | Rationale |
|---------|------------|---------------------|-----------|
| < 25 | Put sweeps + OI building | **Bear Put Spread (debit)** | Low IV = cheap puts. UOA confirms bearish direction. Buy puts with defined risk. |
| 25–50 | Put sweeps + OI building | **Bear Call Spread (credit)** | Normal IV. Sell calls to capture theta while aligning with bearish UOA. |
| 50–75 | Put sweeps + OI building | **Bear Call Spread (aggressive)** | Elevated IV. Aggressively sell call premium — rich IV + bearish flow = both edges in your favor. |
| 75–100 | Put sweeps at scale | **Bear Call Spread (defined risk)** | Extreme IV. Sell calls with spreads. Never sell naked calls in extreme IV regardless of UOA. |

### Neutral / Multi-Leg Flow

| UOA Signal | Interpretation | Strategy |
|-----------|---------------|----------|
| Large iron condor detected in UOA | Institution expects range-bound action | Mirror the structure at retail scale (same strikes, fewer contracts) |
| Large calendar spread detected | Institution expects near-term range with long-term vol expansion | Mirror the near-month short, far-month long structure |
| Straddle purchase at scale | Institution expects a large move (direction unknown) | Deploy a long strangle (cheaper than straddle) at similar strikes — direction-agnostic |
| Risk reversal (sell put + buy call) | Bullish institutional positioning | Enter a bull put spread to participate in upside with defined risk |
| Collar detected (own stock + buy put + sell call) | Institution hedging an existing equity position | Not actionable for retail — this is hedging, not positioning |

[INFERRED] Multi-leg UOA is the highest-quality signal because it reveals the ENTIRE strategy structure, not just one leg. When a $2M call spread is detected (buy $100 calls, sell $110 calls), the institution is expressing a specific view: bullish to $110, not beyond. Mirroring the exact strikes is statistically superior to guessing strikes from single-leg prints.

---

## Entry Timing with UOA

### The 30-Minute / 3-Print Rule
Before entering any UOA-informed trade, confirm:
1. **3 or more prints** in the same direction (all calls OR all puts) on the same ticker
2. **Within 30 minutes** of each other
3. **Volume/OI ratio > 1.5** on at least 2 of the 3 prints (confirming opening activity)

This rule filters approximately 70% of UOA noise while retaining 85% of genuine signals. Single prints are gamblers, not institutions. [COMMON-PRACTICE]

### Entry Timing Window
Enter within 15–60 minutes of confirmed UOA signal. Beyond 60 minutes:
- The options market has repriced to reflect the flow
- The edge from following the flow diminishes significantly (market makers have adjusted)
- If entering beyond 2 hours, the UOA signal is stale — revert to standard IV-based strategy selection

### Contrarian UOA Signals (Fading Extreme Sentiment)

| Sentiment Extreme | Contrarian Signal | Strategy |
|------------------|-------------------|----------|
| > 80% of option volume is calls (extreme bullish sentiment) | The market is overly bullish — expect mean reversion | Fade with defined-risk bear call spreads at 0.15–0.20 delta. If wrong, loss is capped. |
| > 80% of option volume is puts (extreme bearish sentiment) | The market is overly bearish — expect a bounce | Fade with defined-risk bull put spreads at 0.15–0.20 delta. |
| Put/Call ratio < 0.40 (extremely low — everyone buying calls) | Euphoria signal | Reduce long delta exposure; tighten stops on bullish positions |
| Put/Call ratio > 1.50 (extremely high — everyone buying puts) | Panic signal | Deploy CSPs on quality stocks; sell puts when fear premium is richest |

[VERIFIED] Extreme sentiment (put/call ratio extremes) is a contrary indicator over 5–20 day timeframes. The market typically reverts 60–70% of the time within 10 trading days after an extreme reading. Fading with defined-risk spreads limits the damage during the 30–40% of cases where the extreme continues.

---

## Position Sizing with UOA

| UOA Signal Strength | Position Size Adjustment | Rationale |
|-------------------|-------------------------|-----------|
| No UOA (standard IV-based entry) | 100% of standard size | Baseline — no UOA edge to adjust for |
| Confirmed UOA (3+ prints, OI confirms) in same direction as trade | 125% of standard size | UOA confirmation adds edge — size up by 25% |
| Confirmed UOA with block trade (> $500K) | 150% of standard size | Block trades indicate institutional conviction with longer timeframes |
| UOA opposite direction (conflict) | 50% of standard size | Reduced conviction — size down to limit exposure |
| Extreme UOA one-sided (> 80% calls or puts) in your direction | 75% of standard size | Extreme sentiment + your direction = crowded trade risk. Size down, tighten stops. |
| Fading extreme UOA (contrarian) | 50% of standard size, wider strikes | Higher risk trade. Reduce size and increase strike distance by 30%. |

[COMMON-PRACTICE] Never increase position size beyond 150% of standard, regardless of UOA signal strength. UOA is an edge, not a guarantee. A 150% position that goes wrong does 50% more damage to the portfolio than a standard position. The Kelly Criterion for UOA edge estimation suggests a maximum bet size of approximately 25–30% above baseline, but practical risk management caps it at 50%.

---

## Sector-Level UOA Flow

Sector flow analysis detects macro rotation before it appears in price:

| Sector Signal | Criteria | Action |
|--------------|----------|--------|
| Bullish sector rotation | 3+ tickers in the same GICS sector show confirmed bullish UOA (call sweeps) within 60 minutes | Favor bullish strategies on the sector ETF (XLF, XLE, XLK, etc.) over individual stocks. ETFs have lower IV but broader exposure. |
| Bearish sector rotation | 3+ tickers in the same sector show confirmed bearish UOA (put sweeps) within 60 minutes | Reduce or close bullish positions in that sector. Consider bearish spreads on the sector ETF. |
| Sector divergence | One sector bullish, another bearish simultaneously | Pair trade: bullish on strong sector, bearish on weak sector. This is a sector-rotation pairs trade. |
| Broad market flow (SPY/QQQ UOA at scale) | SPY or QQQ options show >$5M in directional UOA | Override individual stock strategies. Index flow is the macro signal — it will drag individual stocks regardless of their specific setups. |

[INFERRED] Sector-level UOA is underutilized by retail traders. When 3+ banks (JPM, BAC, WFC) all show call sweeps within the same hour, the signal is not "JPM is bullish" — it's "financials are rotating." The sector ETF trade captures the theme with lower single-name risk.

---

## Earnings-Specific UOA Rules

UOA around earnings requires special handling:

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Massive call buying 3–5 days before earnings | FADE it (contrarian). Sell call spreads or iron condors. | Pre-earnings flow is sentiment-chasing, not alpha. Studies show pre-earnings options flow has < 50% directional accuracy. [VERIFIED] |
| Massive put buying 3–5 days before earnings | FADE it (contrarian). Sell put spreads. | Same logic — pre-earnings panic is overpriced. Sell the fear premium. |
| Unusual flow 1–2 weeks AFTER earnings | FOLLOW it. | Post-earnings flow is informed flow — institutions have processed the earnings data and are positioning accordingly. |
| Straddle/strangle purchase 1 day before earnings | Do NOT mirror. | This is a vol play, not a directional play. The buyer expects a large move in either direction. |
| Block trade in the earnings week at extreme strikes | Mirror with defined risk ONLY. | Block trades at 20%+ OTM strikes are long-shot bets. Mirror with small position size (25% of standard). |

[COMMON-PRACTICE] The pre-earnings UOA fade is one of the highest-probability UOA strategies. The options market overprices earnings volatility by an average of 15–20% (the "volatility risk premium"). Selling premium into pre-earnings fear and closing immediately after earnings (capturing IV crush) has a historical win rate of approximately 65–70% when done with defined-risk spreads.

---

## UOA Data Quality Checks

Before acting on any UOA signal, verify:

1. **Exchange vs. Non-Exchange:** Prints executed on exchanges (NYSE, NASDAQ, CBOE) are higher quality than dark pool prints. Dark pool prints may be negotiated at non-market prices. Weight exchange prints at 100%, dark pool at 75%.

2. **Sweep vs. Single Print:** Sweeps (multiple small fills aggregated) indicate urgency and are institutional. Single large prints may be pre-arranged or cross-trades. Weight sweeps at 100%, single prints at 50%.

3. **Near-the-Money vs. Deep OTM:** ATM or near-the-money UOA (0.30–0.70 delta) is directional positioning. Deep OTM UOA (0.05–0.10 delta) is lottery-ticket buying or tail hedging. Weight ATM at 100%, far OTM at 25%.

4. **Liquid Strikes vs. Illiquid Strikes:** UOA on strikes with open interest > 1,000 contracts is reliable. UOA on strikes with OI < 100 is noise — a single retail trader with a large account can create an "unusual" print. Minimum OI threshold: 500 contracts.

5. **Time of Day:** UOA in the first 30 minutes (market open) and last 30 minutes (market close) carries the most weight. Midday flow (11 AM – 2 PM ET) is statistically less predictive — it's often hedging or position adjustments, not new conviction.
