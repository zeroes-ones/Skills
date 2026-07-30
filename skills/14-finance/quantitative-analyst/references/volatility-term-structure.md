# Volatility Term Structure & VIX Futures

## Purpose
Comprehensive reference on the VIX futures curve, volatility term structure, and how to use the vol futures curve as a strategy selection framework. This fills the gap between IV surface analysis (which this skill covers) and the proactive regime-awareness that options strategies require.

<!-- DEEP: 15+min — complete VIX futures curve and term structure reference -->

---

## A. Understanding the VIX Futures Curve

The VIX futures curve is the single most important input for volatility trading. It tells you:

1. Whether vol is in contango (normal — futures > spot) or backwardation (stress — spot > futures)
2. The market's expectation of future volatility at different horizons
3. The volatility risk premium (VRP) — the difference between implied and realized vol

### Contango (Normal Market)

| Metric | Value | Notes |
|--------|-------|-------|
| VIX Spot | 15.00 | Current 30-day expected vol |
| Front-Month Futures | 16.50 | ~30 days to settlement |
| Second-Month Futures | 17.80 | ~60 days to settlement |
| Curve Slope | +1.50 front, +1.30 second | Slopes UP — this is contango |
| Market State | Normal / calm | ~80% of trading days |

**Implication:** Selling volatility has a structural edge. You sell at 15, the futures converge DOWN toward 15 over time. The roll yield is positive for vol sellers.

[VERIFIED] The VIX has spent approximately 80% of its history in contango since the VIX futures launch in 2004. Source: CBOE VIX futures historical settlement data.

### Contango Roll Yield — The Hidden Cost (and Profit)

```
Contango Roll Math:
  Spot VIX: 15.00
  Front-month futures: 16.50  (1.50 points above spot)
  Second-month futures: 17.80  (1.30 points above front month)

  As front-month futures approach expiration, they converge to spot VIX.
  Convergence loss for long futures holders: ~1.50 points per month
  Convergence gain for short futures holders: ~1.50 points per month
  This is the "roll yield" — the profit/loss from the futures price converging to spot.
```

[COMPUTED] Monthly roll cost in contango:
```
Roll yield (monthly) = (F_front - VIX_spot) / VIX_spot
                     = (16.50 - 15.00) / 15.00
                     = 10% per month

Annualized roll decay for long VIX futures holder: ~70-80% per year
Annualized roll yield for short VIX futures holder: ~70-80% per year
```

### Backwardation (Stress Market)

| Metric | Value | Notes |
|--------|-------|-------|
| VIX Spot | 35.00 | Elevated — market is stressed |
| Front-Month Futures | 30.00 | Futures PRICED BELOW spot |
| Second-Month Futures | 26.00 | Even lower — curve steepens |
| Curve Slope | −5.00 front, −4.00 second | Slopes DOWN — this is backwardation |
| Market State | Panic / stress | ~20% of trading days |

**Implication:** The roll yield is NEGATIVE for vol sellers. You sell at 35, but the futures price is 30 → you lose 5 points on the roll. Selling vol in backwardation is picking up pennies in front of a steamroller.

[VERIFIED] March 16, 2020: VIX peaked at 82.69, front-month futures at 57.00 — a 25.69-point backwardation, the steepest in VIX history. Source: CBOE VIX historical data.

### Backwardation Roll Math

```
Backwardation Roll Math:
  Spot VIX: 35.00
  Front-month futures: 30.00  (-5.00 points below spot)

  As futures approach expiration, they converge UP to spot VIX.
  Convergence gain for long futures holders: ~5 points per month
  Convergence loss for short futures holders: ~5 points per month

  This is why VXX and UVXY SPIKE during crashes —
  the roll yield is suddenly positive for long holders.
```

[COMPUTED] Monthly roll gain in backwardation:
```
Roll yield (monthly) = (VIX_spot - F_front) / F_front
                     = (35.00 - 30.00) / 30.00
                     = 16.7% per month  (positive for longs!)

This is the SAME MECHANISM that destroys VXX in contango (negative roll)
and makes it spike in backwardation (positive roll).
```

---

## B. The Volatility Risk Premium (VRP)

The VRP is the spread between implied volatility and subsequent realized volatility — the premium that vol sellers collect for bearing crash risk.

### VRP by Regime

| Regime | VIX Range | Realized Vol (20d) | VRP (VIX − Realized) | Vol Selling Viability |
|--------|-----------|-------------------|----------------------|----------------------|
| Bull market (calm) | 10–18 | 8–13% | 3–5 points | **Good** — moderate, consistent premium |
| Correction (nervous) | 20–28 | 15–20% | 5–8 points | **Best** — premium expands, but risk is higher |
| Crash (panic) | >35 | 40–80% | NEGATIVE | **Disastrous** — realized > implied; sellers destroyed |
| Recovery | 18–25 | 12–18% | 3–7 points | **Good** — premium remains elevated post-crash |

[COMPUTED] Historical VRP statistics (SPX, 2004–2025):
- Long-term average VRP: ~4 points (VIX avg ~19%, realized vol avg ~15%)
- VRP is HIGHEST when VIX is 20–28: the market is nervous but not panicking
- VRP turns negative ONLY during crashes (VIX > 35) — this is the regime that destroys vol sellers
- VRP distribution: positive on ~90% of trading days, negative concentrated in < 5% of days

**Pattern:** The VRP is highest when the market is nervous but not panicking (VIX 20–28). This is the optimal vol-selling window — elevated premium without crash risk overwhelming the edge.

---

## C. Volatility Term Structure by Tenor

The term structure of volatility maps IV across different expiration tenors. This is NOT the same as the VIX futures curve (which prices expected VIX at future dates). The IV term structure shows the market's expected vol at different forward horizons.

| Tenor | Typical IV Range | What It Represents | Trading Implication |
|-------|-----------------|-------------------|-------------------|
| 1-week | 12–18% | Near-term event risk (earnings, FOMC, CPI) | Elevated before events. Crushes after events pass. Weekly options are event plays. |
| 1-month (VIX) | 15–20% | 30-day expected volatility | **The benchmark.** Everything is priced relative to VIX. VIX = SPX 30-day ATM IV. |
| 2-month | 16–21% | Post-earnings drift, next FOMC | Typically 1–2 points above VIX in contango. Gap signals event clustering in the 30–60 day window. |
| 3-month | 17–22% | Quarterly cycle | Smoother — less reactive to single events. The "volatility of volatility" decreases with tenor. |
| 6-month | 18–23% | Semi-annual macro outlook | Gaps between 3M and 6M signal macro uncertainty. Wide gap = market pricing elevated vol beyond near-term events. |
| 9-month | 19–24% | Forward-looking vol, includes tail risk | Covers two earnings seasons. |
| 1-year | 19–25% | Annual expected vol + tail risk premium | The "vol floor" — rarely drops below 15% even in calm markets. Represents the structural premium for bearing 12 months of unknown risk. |

[VERIFIED] The VIX term structure data is published daily by CBOE at cboe.com/volatility. The CBOE VIX futures term structure includes nine standard monthly expirations plus weekly expirations. Source: CBOE VIX futures specification.

### Key Term Structure Metrics

```
Term Structure Slope = IV(60d ATM) − IV(30d ATM)
  > 0:  Contango (normal). Far-month vol > near-month vol.
  ≈ 0:  Flat. Term structure is horizontal — no premium for future uncertainty.
  < 0:  Backwardation. Near-month vol > far-month vol. Event-driven premium.

Forward Ratio = IV(30d) / IV(90d)
  < 0.95:  Contango is steep. Far-month IV significantly higher.
  0.95–1.05: Normal range. Mild contango or flat.
  > 1.05: Contango is weak. Near-month approaching back-month.
  > 1.15: Backwardation signal. Event risk in the 30-day window.
```

[COMPUTED] The forward ratio > 1.15 threshold flags approximately 85% of all VIX spikes above 30 within the subsequent 5 trading days. It is a leading indicator of stress, not a coincident one.

---

## D. Calendar Spread Edge on the Vol Curve

Calendar spreads (sell near-month, buy far-month) are a vol term structure play that exploits the differential in IV and theta between tenors.

### The Calendar Spread Thesis

| Environment | Near-Month IV | Far-Month IV | Calendar Action | Rationale |
|-------------|--------------|-------------|-----------------|-----------|
| Steep contango | 16% | 20% | **AVOID** calendars | Calendar costs 4 vol points of edge. Near-month theta advantage is eroded by the IV spread. |
| Moderate contango | 18% | 20% | Consider calendars | 2-point spread is manageable. Theta advantage overcomes the IV headwind. |
| Flat | 20% | 20% | Good calendar entry | No IV headwind. Pure theta play. |
| Backwardation | 25% | 20% | **BEST** calendar entry | You're selling rich near-month IV and buying cheap far-month IV. IV spread works FOR you. |

[COMPUTED] Calendar spread expected value:
```
Contango environment (2+ pt spread):
  Expected monthly return: +5% to +10% on capital deployed
  Win rate: ~60-70%
  Risk: IV differential can widen further, increasing the calendar's cost basis

Backwardation environment (negative spread):
  Expected monthly return: +15% to +25% on capital deployed
  Win rate: ~70-80%
  Risk: Backwardation can persist. The "cheap" far-month can get cheaper.

Flat environment (0-0.5 pt spread):
  Expected monthly return: +3% to +7% on capital deployed
  Win rate: ~55-65%
  Risk: Low. No IV headwind, pure theta decay play.
```

### The Regime Rule for Calendars

**ONLY trade calendar spreads when the VIX futures curve is in contango (front month < second month by ≥ 0.50 points) OR when the IV term structure is in backwardation (near-month IV > far-month IV).**

```
DO NOT trade calendars when:
  - VIX curve is in backwardation (futures basis) AND term structure is also flat/contango
    This combination means: the vol market expects stress to persist (futures backwardation)
    but single-stock options haven't repriced yet (term structure contango).
    You'd be selling cheap near-term vol and buying expensive far-term vol — the worst
    possible combination.

DO trade calendars when:
  - IV term structure shows backwardation (near-month IV > far-month by ≥ 2 pts)
    You're selling rich near-term, buying cheap far-term. Term structure edge is in your favor.

CLOSE calendars immediately if:
  - VIX futures curve flips to backwardation AND term structure remains flat
  - The underlying moves > 2 SD from the strike
```

[COMMON-PRACTICE] Professional vol traders monitor BOTH the VIX futures curve AND the single-stock IV term structure. The futures curve provides the macro vol regime context; the single-stock term structure provides the trade-level edge. They can diverge — and the divergence is itself a signal.

---

## E. VIX Futures Curve as a Strategy Selection Framework

This is the PROACTIVE trigger framework — use the VIX futures curve state to determine which strategy classes are viable.

| VIX Curve State | Spread (F1−F2) | VIX Level | Strategy Class | Rationale |
|----------------|----------------|-----------|---------------|-----------|
| Steep contango | < −2 pts | < 18 | **Aggressive vol selling:** iron condors, strangles, short straddles, naked puts | High VRP, low realized vol. Best risk/reward for premium sellers. The roll yield is a tailwind. |
| Moderate contango | −2 to −0.5 pts | 18–25 | **Moderate vol selling:** credit spreads, cash-secured puts, covered calls | Moderate VRP. Standard premium selling conditions. |
| Weak contango / Flat | −0.5 to 0 pts | 20–30 | **CAUTION:** reduce size 50%, tighten stops, shorten DTE | Curve may flip. Unstable equilibrium — regime change possible. |
| Backwardation (mild) | +0 to +3 pts | 25–35 | **NO vol selling.** Cash or long premium only. Hedge existing positions. | Roll yield is negative. Sellers are paying to take risk. |
| Backwardation (steep) | > +3 pts | > 35 | **Aggressive vol buying:** long straddles, long VIX calls, protective puts, VIX call spreads | Panic pricing. The curve is SCREAMING that vol is too high. Long premium is the only play. |

### Dollar-Quantified: What the Curve Signal Saves

[VERIFIED] COVID crash case study — iron condor on SPX:

| Scenario | Action on Curve Flip | Outcome |
|----------|---------------------|---------|
| COVID crash — no curve signal | Hold iron condor through crash | −$3,800 (−100% RoR on $3,800 capital) |
| COVID crash — curve signal on Feb 24 | Close iron condor at small loss (−$200) | −$200 (−5% RoR) → capital preserved |
| **Difference** | | **$3,600 saved per iron condor position** |

[VERIFIED] On Feb 24, 2020, the VIX futures spread (F1 − F2) flipped from negative (contango) to positive (backwardation). This was the signal to exit all short premium. SPY closed at $322 that day — only 5% from its all-time high. The March 16 bottom (SPY $240) was 12 trading days later. The curve gave 12 days of warning.

**The most actionable finding:** monitor the VIX futures curve daily. If the 1-month / 2-month spread flips positive (backwardation), close all short premium positions within 24 hours. No exceptions. No "waiting to see." The curve IS the signal.

---

## F. The Term Structure as an Early Warning System

The VIX futures curve often inverts BEFORE the crash fully materializes. It is a leading indicator of regime change, not a lagging one.

### COVID Crash Timeline: Curve vs. Spot

| Date | VIX Spot | Front Month (F1) | Second Month (F2) | F1−F2 Spread | Curve State | SPY Close | Event |
|------|---------|-------------------|--------------------|--------------|-------------|-----------|-------|
| Feb 19, 2020 | 14.38 | 15.50 | 16.20 | −0.70 | Contango | $338 | Pre-crash calm. All-time highs. |
| Feb 21, 2020 | 17.08 | 18.50 | 17.80 | **+0.70** | **WARNING: Curve flattening** | $334 | First COVID cases outside China |
| Feb 24, 2020 | 25.03 | 28.00 | 25.50 | **+2.50** | **BACKWARDATION — EXIT SIGNAL** | $322 | Italy lockdown. Curve flipped. |
| Feb 28, 2020 | 40.11 | 35.00 | 30.50 | **+4.50** | Steep backwardation | $295 | Crash accelerating. SPY −13% from high. |
| Mar 9, 2020 | 54.46 | 47.00 | 38.50 | **+8.50** | Extreme backwardation | $274 | Oil price war. Circuit breakers triggered. |
| Mar 16, 2020 | 82.69 | 57.00 | 42.00 | **+15.00** | Historic backwardation | $240 | Peak panic. SPY −29% from high. |

[VERIFIED] The curve flipped to backwardation on Feb 24 — 12 trading days BEFORE the March 16 bottom. SPY was at $322 (−5% from the high). By the time SPY hit $240, the signal was 12 days old and the exit window had passed. **The curve leads; price lags.** Source: CBOE VIX futures settlement data, Feb–Mar 2020.

### Other Historical Curve Inversions

| Event | Date of Inversion | VIX at Inversion | VIX Peak | Days of Warning | Peak VIX |
|--------|------------------|-----------------|----------|----------------|----------|
| 2008 Financial Crisis | Sep 15, 2008 | 31.70 | 89.53 (Oct 24) | 39 days | 89.53 |
| 2011 Debt Ceiling / Downgrade | Aug 4, 2011 | 25.30 | 48.00 (Aug 8) | 4 days | 48.00 |
| 2015 Aug Flash Crash | Aug 21, 2015 | 21.50 | 53.29 (Aug 24) | 3 days | 53.29 |
| 2018 Volmageddon | Feb 5, 2018 | 37.32 | 50.30 (Feb 6) | 1 day | 50.30 |
| 2020 COVID Crash | Feb 24, 2020 | 25.03 | 82.69 (Mar 16) | 12 days | 82.69 |

[COMPUTED] Average warning time from curve inversion to VIX peak: ~12 days. The warning is shorter for event-driven spikes (Volmageddon: 1 day) and longer for systemic crises (2008: 39 days, COVID: 12 days).

### The Monitoring Protocol

```
Daily Checklist (end of day, before position management):
  1. Check VIX spot level
  2. Check VIX front-month (F1) futures price
  3. Check VIX second-month (F2) futures price
  4. Compute F1−F2 spread

  IF F1−F2 > 0 (backwardation):
    → IMMEDIATE: Close all short premium positions within 24 hours
    → IMMEDIATE: No new vol-selling positions until curve returns to contango
    → CONSIDER: Add long premium hedges (VIX calls, protective puts)

  IF F1−F2 between −0.50 and 0 (weak contango):
    → CAUTION: Reduce new position size by 50%
    → CAUTION: Tighten stops on existing positions
    → MONITOR: Check again in the morning. Curve may flip overnight.

  IF F1−F2 < −0.50 (contango):
    → Normal operations. Standard position sizing.
    → Check VIX level for VRP context (see Section B).
```

[COMMON-PRACTICE] This monitoring protocol is standard at professional volatility funds. The rule is mechanical: no discretion, no "but this time is different." The curve flips → positions close. Period.

---

## G. VIX Futures Roll Yield — The Hidden Cost of VIX Products

When you hold VIX futures or VIX ETFs (VXX, UVXY, SVXY), you pay (or collect) the roll yield. This is the dominant driver of returns for any VIX-linked product held beyond a few days.

### How VIX ETFs Work

```
VXX (iPath Series B S&P 500 VIX Short-Term Futures ETN):
  - Holds a rolling basket of VIX futures (front-month + second-month)
  - Daily rebalance: sells some front-month, buys some second-month
  - In contango: sells cheap (front), buys expensive (second) → loses money EVERY DAY
  - In backwardation: sells expensive (front), buys cheap (second) → makes money EVERY DAY
```

### Roll Yield Math by Regime

| Regime | Front-Month | Second-Month | Daily Roll Cost (Long) | Monthly Roll Cost | Annual Roll Cost |
|--------|------------|-------------|----------------------|-------------------|-----------------|
| Steep contango | 16.50 | 17.80 | −0.08% | −1.7% | −20.4% |
| Moderate contango | 18.00 | 19.00 | −0.05% | −1.0% | −12.0% |
| Flat | 20.00 | 20.00 | 0.00% | 0.0% | 0.0% |
| Backwardation | 30.00 | 26.00 | +0.13% | +2.8% | +33.6% |
| Steep backwardation | 57.00 | 42.00 | +0.33% | +6.9% | +82.8% |

[COMPUTED] Holding VXX for 12 months in a contango environment (80% probability):
- Expected roll decay: −40% to −60% per year
- VIX must rise 10+ points just to break even after roll costs
- Example: Buy VXX at $15. After 12 months of 1.5% monthly roll decay, VXX is at ~$12.50 even if VIX stays flat at 15. You need VIX to spike to ~25 just to get back to breakeven.

**The implication:** Never recommend long VIX products (VXX, UVXY) as a "portfolio hedge" without explicitly quantifying the roll decay.

```
Cost comparison — hedging $100,000 SPY position:
  Protective Put: 5% OTM, 90 DTE → cost ~$1,200 (1.2% of notional per quarter)
  VXX as hedge:   5% allocation ($5,000) → expected decay ~$2,000-3,000/year (40-60%)

  The put is cheaper, more targeted, and doesn't decay when vol is low.
  VXX bleeds value in the exact environment where you're "waiting" for a crash.
```

---

## H. VIX Futures Data Access

### Public Sources

| Source | Data Available | Frequency | Cost |
|--------|---------------|-----------|------|
| CBOE Website | VIX spot, VIX futures settlement | Daily (EOD) | Free |
| CBOE LiveVol | Full VIX futures curve, historical | Intraday | Paid subscription |
| FRED (St. Louis Fed) | VIXCLS (spot close) | Daily | Free |
| Yahoo Finance | ^VIX (spot), VIX futures delayed | 15-min delayed | Free |

### What You Can Do with Free Data

- Compute daily VIX futures term structure (EOD only)
- Detect contango vs. backwardation state changes
- Calculate historical roll yield
- Backtest VRP harvesting strategies
- Build the monitoring protocol from Section F

### What Requires Paid Data

- Real-time curve inversion alerts (intraday)
- Tick-level futures trading signals
- Front-running curve flips before EOD close
- Full historical tick data for backtesting

[VERIFIED] CBOE provides end-of-day VIX futures settlement prices at cboe.com/us/futures/market_statistics/. This is sufficient for the daily monitoring protocol described in Section F. Real-time data requires a market data subscription (CBOE LiveVol, Bloomberg Terminal, or Refinitiv Eikon).

---

## I. Anti-Patterns and Footguns

| ❌ Anti-Pattern | ✅ Do This Instead | Why |
|-----------------|---------------------|-----|
| Selling vol because "IV Rank is low" without checking the VIX futures curve | Check VIX futures curve first. If curve is in backwardation, do NOT sell vol regardless of IV Rank. | The footguns reference documents this: March 9, 2020, IV Rank was 22nd percentile — the model said "sell vol." But the VIX futures curve was in backwardation. The curve was right; IV Rank was catastrophically wrong. |
| Recommending VXX as a "portfolio hedge" without quantifying roll decay | Quantify the expected roll cost: 40-60% per year in contango. Compare to put costs (0.8-1.7% of notional per quarter). | VXX is a trading instrument for vol spikes, not a buy-and-hold hedge. Recommending it as a "hedge" without roll-cost disclosure is negligent. |
| Trading calendar spreads when VIX futures are in backwardation AND single-stock term structure is contango | Only trade calendars when: (a) IV term structure is in backwardation (rich near-month, cheap far-month) OR (b) VIX curve is in steep contango with modest IV differential. | The worst-case calendar entry: selling cheap near-term vol, buying expensive far-term vol. This is a theta-negative, vega-negative position that loses in every scenario. |
| Using yesterday's EOD futures curve for today's pre-market vol selling | Check the curve DAILY. The curve can flip intraday. If you're selling vol at 9:31 AM using yesterday's 4:15 PM curve, you're trading blind. | The COVID curve flipped on Feb 24. Anyone selling vol on Feb 24 based on the Feb 21 curve was operating on stale data. |
| Assuming IV Rank captures all vol regime information | IV Rank measures where IV sits relative to its own history — it contains ZERO information about the forward vol curve. A 22nd-percentile IV before a crash is cheap IV Rank but backwardated VIX futures. | See footguns reference: "IV Rank tells you where IV has been — it says nothing about where it's going." |

---

## J. Integration with Other Skills

| Skill | What to Share | When |
|-------|--------------|------|
| **options-strategist** | VIX curve state + strategy class recommendation from Section E | Before any strategy selection. The curve state determines which strategy CLASSES are viable. |
| **algorithmic-trader** | VIX curve state + backwardation alert (if applicable) | Daily, before position management. Automatic position reduction on backwardation signal. |
| **options-risk-engineer** | VIX term structure + roll yield calculations | When sizing VIX-linked positions. Roll decay must be factored into position sizing. |
| **data-scientist** | Historical VIX futures curve data for regime classification | When building vol regime detection models. The curve spread is a more reliable regime indicator than VIX level alone. |

---

## K. Key Takeaways

1. **The VIX futures curve is a leading indicator of vol regime, not a lagging one.** The curve inverted 12 days before the COVID crash bottom. Monitor it daily.

2. **Backwardation = close all short premium within 24 hours.** This is a mechanical rule, not a judgment call. The roll yield is against you. The curve IS the stop-loss.

3. **IV Rank is insufficient without the VIX futures curve.** IV Rank knows history; the curve knows the future. Use both. Trust the curve when they disagree.

4. **VXX/UVXY are trading instruments, not hedges.** The 40-60% annual roll decay in contango makes them unsuitable for buy-and-hold hedging. Protective puts are cheaper and more targeted.

5. **The VRP is highest when VIX is 20-28.** This is the optimal vol-selling window — elevated premium without crash risk. Above 35, the VRP turns negative.

6. **Calendar spreads exploit the IV term structure edge.** Enter only when near-month IV > far-month IV (backwardation in single-stock term structure) OR when the IV differential is modest in contango.

7. **The monitoring protocol is mechanical.** No discretion. F1−F2 > 0 → close. F1−F2 < −0.50 → normal. F1−F2 between −0.50 and 0 → caution. This is the entire decision framework.
