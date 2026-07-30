# Strike Selection Methods

## Purpose
Four quantitative and technical methods for selecting option strike prices. Each serves different market conditions and strategy types. Cross-validate with at least two methods before entering any position to eliminate emotional strike placement.

---

## Method 1: Delta-Based Strike Selection

### Core Principle
Delta approximates the market-implied probability of an option expiring ITM. A 0.30 delta put has ~30% chance of ITM, implying ~70% POP when sold short.

### Strike Price Formula
```
K = S × exp( (r - q + σ²/2) × T - σ × √T × N⁻¹(delta) )
```
Where: `S` = spot price, `r` = risk-free rate (0.0525), `q` = dividend yield, `σ` = IV (decimal), `T` = DTE/365, `N⁻¹` = inverse standard normal CDF.

### Delta-to-Strategy Mapping

| Target Delta | POP (if short) | Use Case |
|-------------|----------------|----------|
| 0.10 | 90% | Long protective wings, ultra-conservative short strikes |
| 0.15–0.20 | 80–85% | Conservative short strikes (iron condors, strangles) |
| 0.20–0.30 | 70–80% | Standard short strikes (credit spreads, CSP, covered calls) |
| 0.30–0.40 | 60–70% | Aggressive short strikes (high IV environments) |
| 0.50 | 50% | ATM — straddle centers, butterfly apex |

[VERIFIED] Delta overstates actual POP by 2–5% due to volatility smile and fat tails. Subtract 2–3% from naive delta-based POP estimates for realistic probability. [INFERRED] For index options (SPX, NDX), delta is a more accurate probability proxy — the fat-tail adjustment is only 1–2% due to diversification reducing extreme tail events.

### When to Use: All probability-based risk management. Liquid underlyings with bid-ask < $0.05 at target strikes. Normal IV (Rank 25–75).
### When NOT to Use: Illiquid options (spreads > $0.10). Within 3 days of binary events. Extreme skew (put IV > call IV by 15+ vol points).
### Validation: Delta strike should be beyond 1.5× expected move. If within 0.5× EM, event vol is distorting delta — switch to Method 2.

---

## Method 2: Standard Deviation / Expected Move

### Core Principle
Price options at distances measured in standard deviations from current price, using the market-implied expected move.

### Expected Move Formula
```
Expected Move (1 SD) = S × σ × √(DTE / 365)
```
Example: SPY at $500, IV = 20%, 30 DTE → EM = $500 × 0.20 × 0.287 = $28.67. Price stays within $471.33–$528.67 with ~68% confidence.

### Strike Placement by SD Level

| SD Level | Confidence | Short Strike Use | Long Wing Use |
|----------|-----------|-----------------|---------------|
| 0.8 SD | ~58% inside | Aggressive (IV Rank > 60) | Not recommended |
| 1.0 SD | ~68% inside | Standard for neutral strategies | Minimum for credit spread longs |
| 1.2 SD | ~77% inside | Conservative neutral | Standard for iron condor wings |
| 1.5 SD | ~87% inside | Very conservative, naked options | Conservative wings |
| 2.0 SD | ~95% inside | "Set and forget" strangles | Ultra-conservative |

### Iron Condor Formula
```
Short Put  = S - (1.0 × EM)    Long Put  = S - (1.5 to 2.0 × EM)
Short Call = S + (1.0 × EM)    Long Call = S + (1.5 to 2.0 × EM)
```

### When to Use: Iron condors, strangles, all neutral premium-selling. When delta is unreliable. For visualizing profit zones in price terms.
### When NOT to Use: Strong trending markets. IV Rank < 20 (EM too small, premium insufficient). Directional debit strategies.
### Validation: EM should be > 3× ATM bid-ask spread. Target > 5× for iron condors. If EM = $2.00 and straddle spread is $0.80, edge is too small after friction.

---

## Method 3: Support/Resistance-Based Strike Selection

### Core Principle
Place short strikes at technical levels where price has historically reversed, aligning option positions with observable chart structure.

### Technical Level Hierarchy

| Priority | Level | Reliability | Application |
|----------|-------|-------------|-------------|
| 1 | 200-Day SMA | Very High | Never short puts below or short calls above on trending stocks |
| 2 | Monthly Pivots: (H+L+C)/3 | High | Preferred for 30–45 DTE; R1/R2 resistance, S1/S2 support |
| 3 | 50-Day SMA | High | Intermediate trend boundary |
| 4 | Volume Profile POC | High | Avoid placing short strikes AT the POC (congestion zone) |
| 5 | Weekly Pivots | Moderate | Supplemental for 7–21 DTE only |
| 6 | Prior Month High/Low | Moderate | Memory-based resistance/support |

### Placement Rules
- **Short put:** At or just below support. Cushion = 0.5–1.0% of stock price below the level.
- **Short call:** At or just above resistance. Cushion = 0.5–1.0% above.
- **CSP/Wheel:** AT support where assignment is acceptable — no cushion needed.
- **Covered call:** AT or above resistance depending on intent to keep shares.

### When to Use: Stocks in well-defined ranges. When chart structure is stronger than IV signal. As cross-check against delta/SD methods.
### When NOT to Use: Breakouts/breakdowns. Post-earnings (5–10 day reset period). Low-float stocks where levels are noise.
### Validation: Strike must be ≥ 2× ATR(14) from current price for DTE < 21. If ATR = $3.00 and strike is $96 on $100 stock (1.33× ATR), the level is too close.

---

## Method 4: IV Skew-Based Strike Selection

### Core Principle
OTM puts typically carry higher IV than equidistant OTM calls (volatility smirk). Exploit this by selling the richer side and underweighting the cheaper side.

### Skew Classification
```
Skew = IV(OTM Put at -5%) - IV(OTM Call at +5%)
```
- **Normal:** +3 to +8 vol points → no adjustment needed
- **Elevated:** +8 to +15 vol points → overweight put selling by 30%
- **Extreme:** >+15 vol points → sell puts aggressively (defined risk); consider buying cheap calls as hedge
- **Reverse (call skew):** Calls > puts by >3 vol points → rare; reduce call selling size by 50%
- **Flat:** ±3 vol points → symmetrical pricing, fair condors

### Strategy Adjustments by Skew

| Skew | Action |
|------|--------|
| Elevated put skew | Favor put credit spreads, CSPs; reduce call spread allocation by 30% |
| Extreme put skew | Sell puts via defined-risk spreads; risk reversal (sell put + buy call) |
| Reverse call skew | Favor call credit spreads but at 50% size — reverse skew precedes explosive moves |
| Flat | Iron condors and strangles are fairly priced |

### When to Use: All credit spread and iron condor selection. Unbalanced condors. Pre-earnings to identify overpriced direction.
### When NOT to Use: DTE < 7 (unstable skew). Illiquid chains. Event-driven skew that will collapse instantly.
### Validation: Recalculate skew after removing 2 highest and 2 lowest IV strikes. If pattern persists → genuine. If disappears → artifact of wide markets.

---

## Multi-Method Validation

Before entry, validate with ≥ 2 of 4 methods:

| Methods Agreeing | Action |
|-----------------|--------|
| 3 of 4 agree | Full-size entry at consensus strikes |
| 2 agree, 2 disagree | Use more conservative strikes at 75% position size |
| All 4 disagree | Pass — underlying not suitable for options currently |

[COMMON-PRACTICE] Professional traders validate every trade with delta + expected move at minimum. Technical and skew methods fine-tune, not override, the quantitative foundation. [VERIFIED] The minimum 2-method validation rule is standard at proprietary trading firms — single-method strike selection is explicitly prohibited in most firm risk manuals.
