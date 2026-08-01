# LEAPS Hedging & Portfolio Insurance — Deep Reference

> **Reading time:** 12 min | **Prerequisites:** options-strategist (protective puts, collars), options-risk-engineer (portfolio hedging), leaps-strategist (stock replacement)

## Overview

LEAPS puts provide long-dated portfolio insurance. Unlike short-dated hedges that must be constantly rolled (incurring transaction costs and timing risk), a LEAPS put provides a **multi-year downside floor** with a single premium payment. This reference covers the mathematics of LEAPS-based hedging, cost amortization, and strategy selection.

## LEAPS Protective Puts

### Strategy Definition

```
+100 Shares (or LEAPS call as stock replacement)
+1 LEAPS Put (DITM or ATM, DTE 365+)

Net position: Long stock + long put = synthetic call at the put strike.
Downside: Capped at (entry_price - put_strike + put_premium).
Upside: Unlimited (less put premium).
```

### Why LEAPS Puts Instead of Rolling Monthly Puts?

| Feature | Monthly Puts (30 DTE) | LEAPS Puts (365+ DTE) |
|---------|----------------------|----------------------|
| Annual cost | 12 × monthly premium (typically 8-12% of notional) | 1× LEAPS premium (typically 5-8% of notional per year) |
| Management | Must roll 12 times/year — timing risk, gap risk between rolls | Set once. No roll risk |
| Vega exposure | Low (30 DTE vega is small) | High (LEAPS vega is 3-5x short-dated) |
| IV sensitivity | Buy when IV is low to minimize cost | Critical: must buy when IV rank < 30% |
| Strike flexibility | Can adjust strike every month | Fixed strike for the term |
| Gap protection | Only protects for the current 30-day window | Protects continuously for 1-3 years |

[COMPUTED] LEAPS puts are typically cheaper on an annualized basis than rolling monthly puts (5-8% vs. 8-12% of notional), but the upfront cash outlay is larger.

### Strike Selection for LEAPS Protective Puts

| Put Strike (% of Spot) | Delta | Annualized Cost (% of notional) | Protection Level |
|------------------------|-------|-------------------------------|-----------------|
| 95% (5% OTM) | -0.35 | 5-7% | Catastrophic only |
| 90% (10% OTM) | -0.25 | 3-5% | Bear market floor |
| 80% (20% OTM) | -0.12 | 1.5-2.5% | Tail risk only |
| 100% (ATM) | -0.50 | 8-12% | Full notional protection |

[COMMON-PRACTICE] 10-15% OTM LEAPS puts offer the best cost/protection balance for most portfolios. ATM puts are too expensive for continuous protection.

### The Cost Amortization Framework

```
Annual protection cost = LEAPS_put_premium / years_to_expiration
Protection cost as % of portfolio = annual_cost / portfolio_value
"Is it worth it?" → Compare to expected drawdown probability × drawdown magnitude

Example: SPY @ $500, Jan 2027 450 Put (10% OTM, ~550 DTE)
Premium: $18.00  →  Annual cost: $18 / 1.5 years = $12/year
% of portfolio: $12 / $500 = 2.4% per year

If you expect a 20%+ drawdown every 3-5 years:
Expected annual drawdown cost: 20% / 4 = 5% per year
LEAPS put cost: 2.4% per year
Net: Protection costs less than expected drawdown → justified.
```

[ESTIMATED] The expected drawdown probability is the key assumption. Historical SPY drawdowns > 20% occur roughly every 3-5 years. For individual stocks, drawdowns are more frequent and deeper.

## LEAPS Collars

### Strategy Definition

```
+100 Shares
+1 LEAPS Put (floor)
-1 LEAPS Call (cap — finances the put)

Net: Zero-cost or near-zero-cost multi-year collar.
```

### Zero-Cost LEAPS Collar Construction

```
Step 1: Select LEAPS put strike for desired floor (e.g., 10% OTM)
Step 2: Calculate put premium
Step 3: Find LEAPS call strike whose premium ≥ put premium
Step 4: If call premium > put premium → net credit (ideal)
        If call premium < put premium → net debit (widen call strike or tighten put strike)
```

[COMPUTED] For SPY @ $500, Jan 2027 (550 DTE), IV=18%:
- Put at $450 (10% OTM): ~$18.00
- Call at $575 (15% OTM): ~$18.00
- Result: Zero-cost collar with +15% upside, -10% downside for 18 months.

### When LEAPS Collars Beat Standard Collars

| Scenario | Monthly Collar (30 DTE) | LEAPS Collar (365+ DTE) | Winner |
|----------|------------------------|------------------------|--------|
| Want continuous protection, minimal management | 12 rolls/year, gap risk at each roll | Set once, continuous protection | **LEAPS** |
| Want to adjust strikes based on market conditions | Can adjust monthly | Fixed for term | **Monthly** |
| High IV environment | Both legs expensive (buy put, sell call) | Both legs expensive | **Neither** — wait for lower IV |
| Low IV environment | Cheap to buy put, but sold call is also cheap | Both legs cheap. Lock in rates for years | **LEAPS** |
| Taxable account, want to defer gains | Short-term gains on monthly call sales | LTCG if held > 1 year | **LEAPS** |

## LEAPS for Tail Risk Hedging

### The "Dragon Portfolio" Approach

[COMMON-PRACTICE] Allocate 2-5% of portfolio annually to deep OTM LEAPS puts as tail risk insurance. These expire worthless 90%+ of the time but pay 10-50x in a crash.

```
Portfolio: $500,000
Tail hedge allocation: 3% = $15,000/year
Purchase: SPY LEAPS puts at 20-30% OTM, 18-24 month DTE

Normal year: Lose $15,000 (3% drag on portfolio)
Crash year (-30%): Puts gain 10-20x → $150,000-$300,000 gain
Net: Hedge partially or fully offsets portfolio loss.
```

### LEAPS Put Ladder

Instead of one big LEAPS put position, build a ladder across strikes:

```
Put 1: 5% OTM  — 50% of hedge allocation (catastrophic)
Put 2: 15% OTM — 30% of hedge allocation (bear market)
Put 3: 25% OTM — 20% of hedge allocation (tail risk)

Total annual cost: ~3% of portfolio.
```

[COMPUTED] The ladder approach provides graduated protection: the 5% OTM puts kick in early, the 25% OTM puts provide convexity in a crash.

## Rho Sensitivity in LEAPS Hedges

[VERIFIED] LEAPS have significantly higher rho than short-dated options. For 18-month LEAPS:
- ATM put rho: ~-0.25 (per 1% rate change, per contract)
- ATM call rho: ~+0.25

A 1% Fed rate cut increases LEAPS put values by ~$25/contract and decreases LEAPS call values by ~$25/contract. For a 10-contract hedge, that's ±$250 per 1% rate move.

**Rate sensitivity implications:**
- **Rising rate environment:** LEAPS calls benefit (higher rho on calls), LEAPS puts are cheaper
- **Falling rate environment:** LEAPS puts benefit, LEAPS calls lose value
- **Hedge timing:** Buy LEAPS puts when rates are high (puts cheaper, rho works in your favor if rates fall)

## Common Pitfalls

| ❌ Pitfall | ✅ Prevention |
|-----------|--------------|
| Buying LEAPS puts when IV rank > 50% (overpaying for insurance) | Only buy LEAPS puts when IV rank < 30%. Wait for vol compression |
| LEAPS put strike too close to spot → expensive, decays faster | Minimum 10% OTM for protective puts. Wider for tail hedges |
| Forgetting to factor rho into LEAPS hedge decisions | In a rate-cutting cycle, LEAPS puts appreciate from rho alone. In a hiking cycle, they lose value |
| Selling LEAPS calls in a collar and the stock doubles → massive opportunity cost | Accept the cap. The protection was free. If FOMO > protection value, don't collar |
| Using LEAPS puts on individual stocks → single-stock gap risk not hedged | LEAPS puts on individual stocks protect against gradual declines, not overnight gaps (the option market prices this in). For gap protection, use index LEAPS |

## Provenance

[VERIFIED] Protective put and collar mechanics from CBOE and OIC.
[VERIFIED] LEAPS rho sensitivity: Black-Scholes rho = K × T × e^(-rT) × N(d2). Longer T = larger rho.
[COMMON-PRACTICE] Dragon Portfolio tail hedging concept from Artemis Capital Management and Universa Investments research.
[COMPUTED] Annualized cost calculations. Actual LEAPS premiums vary with IV, rates, and dividends.
[ESTIMATED] 2-5% tail hedge allocation is a practitioner range. Universa advocates higher allocations for institutional portfolios.
[AS OF 2026-07]
