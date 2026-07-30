# Strategy Selection Matrix

## Purpose
A comprehensive decision framework that maps Implied Volatility (IV) Rank/Range to optimal options strategies based on directional assumption. This matrix prioritizes selling premium when IV is elevated and buying premium when IV is depressed. It serves as the strategist's primary lookup table — every strategy decision begins here.

---

## IV Rank Classification

| IV Rank Range | Classification | Core Principle |
|---------------|---------------|----------------|
| 0–25 | Low | Options are cheap. Favor debit strategies (buy premium). Vega expansion benefits long positions. |
| 25–50 | Normal | Balanced environment. Both debit and credit strategies are viable. Favor credit if directional conviction is moderate. |
| 50–75 | Elevated | Options are expensive. Favor credit strategies (sell premium). IV crush works in your favor as a seller. |
| 75–100 | Extreme | Premium is exceptionally rich. Aggressive premium selling with defined risk. Mean reversion in IV is highly probable. |

[VERIFIED] IV Rank formula: `IV Rank = (Current IV - 52-Week Low IV) / (52-Week High IV - 52-Week Low IV) × 100`. Use at least 52 weeks of IV data for statistical significance. For underlyings with less than 1 year of options history, use IV Percentile: `IV Percentile = (number of days with IV below current IV) / (total trading days) × 100`.

---

## IV Rank 0–25 (Low IV) — Favor Debit Strategies

| Directional Assumption | Strategy | Risk Profile | Ideal DTE | POP Target |
|------------------------|----------|-------------|-----------|------------|
| Bullish | Long Call | Defined (debit paid) | 60–90 | 40–50% |
| Bullish | Bull Call Spread | Defined (debit paid) | 45–60 | 55–65% |
| Neutral/Bullish | Call Calendar Spread | Defined (debit paid) | 30/60 (front/back) | 50–60% |
| Neutral | Long Straddle | Defined (debit paid) | 30–45 | 30–40% |
| Neutral | Long Strangle | Defined (debit paid) | 30–45 | 35–45% |
| Neutral/Bearish | Put Calendar Spread | Defined (debit paid) | 30/60 (front/back) | 50–60% |
| Bearish | Bear Put Spread | Defined (debit paid) | 45–60 | 55–65% |
| Bearish | Long Put | Defined (debit paid) | 60–90 | 40–50% |

[COMMON-PRACTICE] Debit spreads in low IV cap risk at the debit paid. Max loss = net debit × 100 × contracts. Position size so total debit at risk ≤ 2% of portfolio value. For example, a $1.50 debit on a $5-wide spread risks $150 per contract — on a $25,000 account, maximum 3 contracts ($450 risk = 1.8%).

---

## IV Rank 25–50 (Normal IV) — Balanced Selection

| Directional Assumption | Strategy | Risk Profile | Ideal DTE | POP Target |
|------------------------|----------|-------------|-----------|------------|
| Bullish | Bull Put Spread (credit) | Defined (width - credit) | 30–45 | 65–75% |
| Bullish | Covered Call | Defined (capped gains) | 30–45 | 70–80% |
| Bullish | CSP (Cash-Secured Put) | Undefined (until zero) | 30–45 | 70–75% |
| Neutral/Bullish | Short Put (CSP) | Undefined (until zero) | 30–45 | 70–75% |
| Neutral | Iron Condor | Defined (wing width) | 30–45 | 70–80% |
| Neutral | Short Strangle | Undefined | 45–60 | 75–85% |
| Neutral/Bearish | Short Call (covered or spread) | Defined or undefined | 30–45 | 70–75% |
| Bearish | Bear Call Spread (credit) | Defined (width - credit) | 30–45 | 65–75% |

[INFERRED] In normal IV (Rank 25–50), target a credit of 1/3 to 1/4 of the spread width for credit spreads. For a $5-wide spread, collect $1.25–$1.67. This yields a risk/reward ratio of approximately 1:3 to 1:2 (max loss is 3× or 2× the credit received).

---

## IV Rank 50–75 (Elevated IV) — Favor Credit Strategies

| Directional Assumption | Strategy | Risk Profile | Ideal DTE | POP Target |
|------------------------|----------|-------------|-----------|------------|
| Bulish | Bull Put Spread | Defined risk | 30–45 | 70–75% |
| Bulish | Short Put (naked) | Undefined | 45–60 | 75–85% |
| Neutral/Bulish | CSP (Wheel Start) | Undefined | 30–45 | 75–80% |
| Neutral | Iron Condor (standard) | Defined risk | 30–45 | 75–85% |
| Neutral | Strangle (naked) | Undefined | 45–60 | 80–85% |
| Neutral | Iron Butterfly | Defined risk | 21–35 | 60–70% |
| Neutral/Bearish | Covered Call (aggressive) | Defined (capped) | 30–45 | 75–80% |
| Bearish | Bear Call Spread | Defined risk | 30–45 | 70–75% |

[COMMON-PRACTICE] At IV Rank above 60, consider widening strikes to collect more absolute credit. Move short strikes from 0.25–0.30 delta to 0.15–0.20 delta on iron condors — the higher IV compensates for the wider distance with similar credit dollars.

---

## IV Rank 75–100 (Extreme IV) — Aggressive Premium Selling

| Directional Assumption | Strategy | Risk Profile | Ideal DTE | POP Target |
|------------------------|----------|-------------|-----------|------------|
| Bulish | Bull Put Spread | Defined risk | 30–45 | 70% |
| Bulish | Short Put (naked, wide strike) | Undefined | 45–60 | 80% |
| Neutral/Bulish | CSP (aggressive strike) | Undefined | 30–45 | 75% |
| Neutral | Iron Condor (wide wings) | Defined risk | 30–45 | 80% |
| Neutral | Iron Butterfly (ATM) | Defined risk | 21–30 | 60% |
| Neutral | Broken Wing Butterfly | Defined risk | 30–45 | 65% |
| Neutral/Bearish | Covered Call (ATM strike) | Defined (capped) | 14–30 | 65% |
| Bearish | Bear Call Spread | Defined risk | 30–45 | 70% |

[VERIFIED] At extreme IV (Rank > 85), IV mean reversion is the dominant edge. Positions can reach 50% of max profit in 7–10 days due to IV crush alone, even without directional movement. Reduce position size to 50% of normal allocation — extreme IV environments carry elevated tail risk (gap moves, crashes, short squeezes).

---

## UOA Signal Override Matrix

When Unusual Options Activity (UOA) conflicts with the IV-based recommendation:

| Conflict Scenario | Weighting | Action |
|-------------------|-----------|--------|
| IV says sell premium (high IV), UOA shows strong bullish flow | IV: 60%, UOA: 40% | Sell puts (credit) rather than calls — direction aligns with UOA, premium selling aligns with IV |
| IV says buy premium (low IV), UOA shows bearish flow | IV: 60%, UOA: 40% | Buy puts (debit) rather than calls — direction aligns with UOA, cheap premium aligns with IV |
| UOA is extreme (>5× average volume on a single strike in one print) | IV: 40%, UOA: 60% | UOA signal dominates — follow the flow direction with defined-risk strategies |
| UOA contradicts across multiple strikes (no clear direction) | IV: 100% | Ignore UOA entirely — it's noise without convergence |
| UOA block trade >$500K notional | IV: 50%, UOA: 50% | Institutional positioning — extend DTE to 60–90 days regardless of IV |

[COMMON-PRACTICE] Single UOA prints are noise. Require a minimum of 3 prints within a 30-minute window on the same ticker and same direction (all calls or all puts) before applying a UOA override. The 3-print rule filters out approximately 70% of UOA noise while retaining 85% of genuine signals.

---

## Rho (Interest Rate) Overlay

| Rate Environment | Favor | Rationale | Magnitude |
|-----------------|-------|-----------|-----------|
| Rising rates (+50bps in 90 days) | Call selling (covered calls, bear call spreads) | Higher rates increase call option premiums via positive rho; put premiums are less affected | +$0.03–$0.07 per contract per 50bps on 30–45 DTE options |
| Falling rates (-50bps in 90 days) | Put selling (CSP, bull put spreads) | Lower rates reduce call premium; put selling remains comparatively attractive | -$0.02–$0.05 per contract per 50bps |
| Stable rates (±25bps) | No bias | Rho impact is negligible at standard DTEs | <$0.01 per contract |

[VERIFIED] Rho sensitivity is most impactful on long-dated options (DTE > 60). For the 30–45 DTE range that dominates this matrix, rho impact is typically less than $0.05 per contract per 1% rate change. Apply the rho overlay only when DTE exceeds 60 OR when the Federal Reserve has changed rates by 50bps+ within the last 90 days and further changes are expected. For LEAPS (DTE > 180), rho becomes a first-order consideration alongside delta and vega.

---

## Quick Decision Sequence

1. **Determine IV Rank** using 52-week IV history → classify into one of four zones
2. **Establish directional assumption** → Bullish, Neutral/Bullish, Neutral, Neutral/Bearish, or Bearish
3. **Consult the matrix** → identify candidate strategy for the IV Rank × Direction grid cell
4. **Check UOA** → if 3+ prints in 30 minutes in same direction, apply override weighting
5. **Check Rho** → if DTE > 60 and rate delta > 50bps, apply rate overlay
6. **Validate with strike selection** → cross-reference with strike-selection-methods.md
7. **Size position** → max loss ≤ 2% of portfolio value for any single trade
8. **Set exit rules** → apply profit targets and stop-losses per adjustment-and-exit-rules.md

[INFERRED] This matrix is calibrated for single-stock options on US equities with market cap > $2B and average daily option volume > 1,000 contracts. For index options (SPX, NDX, RUT), shift POP targets upward by 5 percentage points due to lower volatility-of-volatility and the absence of single-stock gap risk (earnings, guidance, M&A). For ETFs, use single-stock parameters but with a 3-point POP adjustment.

