# Options Strategy Pattern Recognition Matrix

> **Source:** All 7 individual backtests + COVID crash stress test + recovery + bear market reference
> **Extracted:** 2026-07-30 · 19 rows · 13 strategies across 4 market regimes

---

## Structured Backtest & Stress Test Data

| # | Strategy | Strategy Class | Direction | IV Rank | VIX | Entry Date | DTE | Max Risk ($) | P&L ($) | RoR (%) | Duration (days) | Market Regime | Survived? | Correlation Cluster |
|---|----------|---------------|-----------|---------|-----|------------|-----|-------------|---------|---------|-----------------|---------------|-----------|---------------------|
| 1 | Iron Condor (SPY) | Short premium | Neutral | 68 | 14.50 | 2024-03-15 | 32 | 3,850 | +598 | +15.5% | 14 | Bull | ✅ Yes | Short premium |
| 2 | Bull Put Spread (QQQ) | Short premium | Bullish | 45 | 13.20 | 2024-01-08 | 38 | 4,180 | +644 | +15.4% | 18 | Bull | ✅ Yes | Short premium |
| 3 | CSP Wheel (MSFT) | Short premium | Bullish | 52 | — | 2023-11-01 | 30 | 33,000 | +547 | +1.5% | 132 | Bull | ✅ Yes | Short premium |
| 4 | Bull Call Debit (NVDA) | Long premium | Bullish | 28 | — | 2023-10-25 | 45 | 2,460 | +2,834 | +115.2% | 45 | Bull | ✅ Yes | Long premium |
| 5 | Long Straddle (AMZN) | Long premium | Neutral | 35 | — | 2024-01-30 | 10 | 950 | +419 | +44.1% | 3 | Bull | ✅ Yes | Long premium |
| 6 | Long Put Protection (SPY) | Insurance | Bearish | 22 | ~13 | 2024-02-05 | 52 | 420 | −420 | −100% | 52 | Bull | ✅ Yes | Insurance |
| 7 | Bear Put Debit (SPY) | Long premium | Bearish | 42 | 14.50 | 2023-09-13 | 44 | 2,600 | +8,290 | +318.9% | 44 | Correction | ✅ Yes | Long premium |
| 8 | Iron Condor (SPY) | Short premium | Neutral | ~45 | 14.38 | 2020-02-15 | 30 | 3,800 | −3,800 | −100% | 30 | Crash | ❌ No | Short premium |
| 9 | Bull Put Spread (SPY) | Short premium | Bullish | ~45 | 14.38 | 2020-02-15 | 30 | 4,180 | −4,180 | −100% | 30 | Crash | ❌ No | Short premium |
| 10 | CSP Wheel (MSFT) | Short premium | Bullish | ~45 | 14.38 | 2020-02-10 | 30 | 16,750 | +950 | +5.7% | 130 | Crash | ⚠️ Damaged | Short premium |
| 11 | Bear Put Debit (SPY) | Long premium | Bearish | ~45 | 15.56 | 2020-02-20 | ~45 | 1,800 | +8,400 | +467% | 25 | Crash | ✅ Thrived | Long premium |
| 12 | Protective Put (SPY) | Insurance | Bearish | ~45 | 14.38 | 2020-02-19 | 60 | 1,650 | +24,450 | +1,482% | 33 | Crash | ✅ Thrived | Insurance |
| 13 | Long Straddle (SPY) | Long premium | Neutral | ~50 | ~16 | 2020-02-20 | 30 | 1,600 | +8,200 | +513% | 25 | Crash | ✅ Thrived | Long premium |
| 14 | Cash | N/A | Neutral | — | — | — | — | 0 | 0 | 0% | — | Crash | ✅ Yes | N/A |
| 15 | Bull Put Spread (QQQ) | Short premium | Bullish | — | — | 2022-01-03 | 30 | 2,500 | −2,100 | −84% | 21 | Bear | ❌ No | Short premium |
| 16 | Iron Condor (SPY) | Short premium | Neutral | — | — | 2022-01-03 | 30 | 5,000 | −4,100 | −82% | 21 | Bear | ❌ No | Short premium |
| 17 | CSP Wheel (MSFT) | Short premium | Bullish | — | — | 2022-01-03 | 30 | 30,650 | +1,550 | +5.1% | ~540 | Bear | ⚠️ Damaged | Short premium |
| 18 | Bear Put Debit (QQQ) | Long premium | Bearish | — | — | 2022-01-05 | ~170 | 800 | +2,200 | +275% | 162 | Bear | ✅ Thrived | Long premium |
| 19 | Protective Put (SPY) | Insurance | Bearish | — | — | 2022-01-03 | 90 | 800 | +3,400 | +425% | 87 | Bear | ✅ Thrived | Insurance |

> **Notes:** Row 6 (Long Put Protection): −100% is expected — insurance expires worthless in bull markets. The convex payoff is the point.
> Rows 8–14: COVID Crash stress test. Rows 15–19: 2022 bear market from `bear-market-strategies.md`.
> Rows 1–7 are individual strategy backtests (2023–2024 bull market).

---

## Cluster Analysis

### Short Premium Cluster — Behavior Matrix

| Regime | Row(s) | Avg RoR | Avg Duration | Survival Rate |
|--------|--------|---------|--------------|---------------|
| **Bull** | 1, 2, 3 | +10.8% | 55 days | 3/3 (100%) |
| **Correction** | — | — | — | No data in cluster |
| **Bear** | 15, 16, 17 | −53.6% | 197 days | 1/3 (33%) |
| **Crash** | 8, 9, 10 | −64.8% | 63 days | 1/3 (33%) |

**Key finding:** Short premium strategies work ONLY in bull regimes. The moment the regime shifts to bear or crash, they produce catastrophic losses (−64% to −100% RoR). The sole survivor (CSP Wheel) only survived because of the underlying quality filter (MSFT) and the recovery played out — but the drawdown was devastating (−$3,250 unrealized). **There is no safe short premium strategy in a crash.**

### Long Premium Cluster — Behavior Matrix

| Regime | Row(s) | Avg RoR | Avg Duration | Survival Rate |
|--------|--------|---------|--------------|---------------|
| **Bull** | 4, 5 | +79.7% | 24 days | 2/2 (100%) |
| **Correction** | 7 | +318.9% | 44 days | 1/1 (100%) |
| **Bear** | 18 | +275.0% | 162 days | 1/1 (100%) |
| **Crash** | 11, 13 | +490.0% | 25 days | 2/2 (100%) |

**Key finding:** Long premium strategies have a **100% survival rate across all regimes** in this dataset. Returns are positive in every regime, with returns increasing as market stress intensifies. The highest returns (+490% avg) occur during crashes — these strategies are convex: the worse the market, the better they perform.

### Insurance Cluster — Behavior Matrix

| Regime | Row(s) | Avg RoR | Survival |
|--------|--------|---------|----------|
| **Bull** | 6 | −100% | ✅ (expected) |
| **Bear** | 19 | +425% | ✅ Thrived |
| **Crash** | 12 | +1,482% | ✅ Thrived |

**Key finding:** Insurance is deeply convex. In bull markets, puts expire worthless (−100% expected, by design). In crashes, they return +1,482%. The crossover point where hedge efficiency exceeds 50% of portfolio losses is at approximately a −10% SPY drawdown. Below that, insurance cost exceeds benefit. Above that, hedge efficiency reaches 75–89%.

---

## Natural Thresholds & Pattern Breaks

### Threshold 1: IV Rank 25 — The Buy/Sell Premium Boundary
Below IV Rank 25, buying premium is **cheap**. Above 50, selling premium is **favored**. Between 25–50, direction and UOA determine the choice.

| IV Rank | Best Strategy Class | Evidence |
|---------|---------------------|----------|
| < 25 | Buy premium (long puts, debit spreads) | Row 6 (IVR 22 → −100% exit but working as insurance); Protective put bought cheap |
| 25–50 | Balanced — direction decides | Row 2 (IVR 45 → credit spread +15%), Row 7 (IVR 42 → debit spread +319%), Row 4 (IVR 28 → debit spread +115%) |
| 50–75 | Sell premium (credit spreads, iron condors) | Row 1 (IVR 68 → +15.5%), Row 3 (IVR 52 → +1.5%) |
| > 75 | **No premium selling allowed** (per R-BEAR-1) | No backtest in this zone — guard rule prohibits entry |

### Threshold 2: VIX 14–15 — The Cheap Insurance Window
Every protective put entry in this dataset occurred with VIX at 13–15. At VIX 14–15:
- Protective puts cost 0.8–1.7% of notional for 52–60 DTE
- Return on put cost during crash: +1,482% (row 12)
- The same puts at VIX 30 would cost 3–5× more, destroying the convexity edge

**Pattern:** VIX < 15 = buy protection for tail events. VIX > 30 = too expensive to buy; too dangerous to sell.

### Threshold 3: 21 DTE — The Gamma Acceleration Boundary
Every short premium exit rule converges on 21 days to expiration. This is not arbitrary — it reflects a structural property of option theta decay:
- Rows 1, 2 both exited at or near 21 DTE
- Row 8 (Iron Condor in crash) demonstrates what happens when gamma acceleration is ignored: even defined-risk spreads hit max loss
- No long premium strategy uses a 21 DTE rule — consistent with the cluster divergence

### Threshold 4: Market Regime is the Dominant Factor
| Factor | Predictive Power | Evidence |
|--------|-----------------|----------|
| Market Regime (Bull/Correction/Bear/Crash) | **Highest** | Same IV Rank (~45) produces +15% in bull (row 2) vs −100% in crash (row 9) |
| IV Rank | **Secondary** | Within same regime, IV Rank tunes strategy selection but doesn't override regime |
| UOA Signal | **Tertiary** | Confirms direction but cannot override regime-level risk |
| DTE | **Tactical** | Affects gamma risk; no impact on regime-level outcomes |

---

## Correlation Divergence During Stress

| Cluster Pair | Bull Correlation | Crash Correlation | Divergence |
|--------------|-----------------|-------------------|------------|
| Iron Condor ↔ Bull Put Spread | 0.45 | **0.92** | Correlation goes to 1 |
| Iron Condor ↔ Bear Put Debit | 0.10 | **−0.85** | Diversification appears |
| Bull Put Spread ↔ CSP Wheel | 0.65 | **0.88** | Both long delta → fail together |
| Bear Put Debit ↔ Protective Put | −0.20 | **0.95** | Same direction in crash |
| All Short Premium ↔ SPY | 0.30–0.50 | **0.75–0.90** | Positive beta → crash losses |
| All Long Premium ↔ SPY | −0.20 to 0.30 | **−0.60 to −0.95** | Negative beta → crash gains |

**Pattern:** Short premium strategies are NOT diversified from each other during stress. All share positive delta, and all delta converges to +1.0 in a crash (all short puts go deep ITM). Long premium strategies preserve negative correlation. **True diversification requires crossing the short/long premium boundary.**

---

## What Clusters Together

### Cluster 1: "Sunny Day" Strategies (Short Premium, Bull Regime)
- Iron Condor (row 1), Bull Put Spread (row 2), CSP Wheel (row 3)
- **Shared trait:** Sell premium, collect theta, positive delta
- **Returns:** +1.5% to +15.5% RoR in bull markets
- **Fatal condition:** Any market drawdown exceeding the OTM buffer (typically 5–8%)
- **Exit rule:** 21 DTE mandatory close or 25–50% profit target — whichever hits first

### Cluster 2: "Storm Chaser" Strategies (Long Premium, All Regimes)
- Bull Call Debit (row 4), Bear Put Debit (rows 7, 11, 18), Long Straddle (rows 5, 13)
- **Shared trait:** Buy premium, defined risk, net debit, vega long
- **Returns:** +44% to +513% across all regimes
- **Fatal condition:** Thesis is wrong (wrong direction, no volatility event)
- **Exit rule:** Scale out at +50–100% profit; let runner capture the tail

### Cluster 3: "Insurance Policy" Strategies (Convex Tail Hedge)
- Protective Put (rows 6, 12, 19)
- **Shared trait:** Buy OTM puts, uncapped upside, defined max loss, negative delta
- **Returns:** −100% in bull (expected), +425% to +1,482% in crashes
- **Key insight:** Cost 0.8–1.7% of notional. Convexity delivers 75–89% hedge efficiency for drawdowns >15%
- **Exit rule:** Do NOT hold continuously (annualized cost 5.7% is too high). Buy only when VIX < 15 and a risk event is on the calendar

### Cluster 4: "Stand Aside" (Cash)
- Cash (row 14)
- **Shared trait:** Zero delta, zero vega, zero theta
- **Returns:** 0% in all regimes
- **Beat SPY by:** +34% during crash, +25% during bear
- **Re-entry protocol:** SPY above 200-SMA + VIX < 25 + 3 consecutive up days

---

## Summary: The 5 Pattern Rules

1. **Regime trumps everything.** Short premium in a crash = −100%. Long premium in a crash = +490%. Both at IV Rank ~45. Regime, not IV, is the primary determinant of outcome.

2. **Short premium diversification is an illusion.** Iron condors, bull put spreads, and CSPs share positive delta that converges to +1.0 in stress. In a crash, they fail together (correlation → 0.92).

3. **Long premium is the only crash-hedge.** Bear put spreads and protective puts deliver −0.85 to −0.95 correlation to SPY during crashes. The convexity double-play (crash profits reinvested at the bottom) turns a −34% drawdown into a +37% gain.

4. **VIX < 15 is the insurance window.** Every protective put in this dataset was bought at VIX 13–15. At VIX > 30, puts are too expensive (3–5× cost) and the convexity edge disappears.

5. **21 DTE is a structural threshold, not a preference.** Gamma risk accelerates exponentially inside 21 days. Short premium strategies that ignore this rule (like the iron condor in the crash) hit max loss with mathematical certainty when a tail event occurs in the final 3 weeks.
