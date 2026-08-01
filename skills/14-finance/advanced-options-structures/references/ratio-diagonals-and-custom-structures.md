# Ratio Diagonals & Custom Structure Design — Deep Reference

> **Reading time:** 15 min | **Prerequisites:** options-strategist (diagonals, calendars, ratio spreads, backspreads), quantitative-analyst (Greeks, vol surface)

## Overview

When off-the-shelf strategies don't fit, traders build custom structures by combining primitives. Ratio diagonals are the most versatile custom hybrid — they combine the **time-spread mechanics of diagonals** with the **leverage of ratio spreads** to create strategies with specific Greek profiles tailored to a market view.

This reference covers:
1. Ratio diagonal construction and optimization
2. The strategy composition framework (how to build custom structures)
3. Gamma-neutral and delta-gamma-theta target construction
4. When to build custom vs. use standard strategies

---

## Part 1: Ratio Diagonals

### Strategy Definition

A **ratio diagonal** is a diagonal spread where the number of short contracts exceeds the number of long contracts — creating leveraged theta harvesting with directional or volatility exposure.

### Standard Construction

```
Long:  N contracts at DTE_far, strike K_long
Short: M contracts at DTE_near, strike K_short

where M > N (ratio > 1:1)

Common ratios:
- 1:2 (conservative — 2 shorts per 1 long)
- 1:3 (aggressive — 3 shorts per 1 long)
- 2:3 (balanced — 3 shorts per 2 longs)
```

### Types of Ratio Diagonals

| Type | Construction | Greek Profile | Best For |
|------|-------------|---------------|----------|
| **Call Ratio Diagonal** | Long far OTM calls, short more near ATM calls | Theta++, Delta+, Vega- | Mildly bullish with high IV |
| **Put Ratio Diagonal** | Long far OTM puts, short more near ATM puts | Theta++, Delta-, Vega- | Mildly bearish with high IV |
| **Call Ratio Backspread Diagonal** | Long far ATM calls, fewer short near OTM calls | Theta~, Delta++, Vega+ | Strongly bullish, low IV |
| **Put Ratio Backspread Diagonal** | Long far ATM puts, fewer short near OTM puts | Theta~, Delta--, Vega+ | Strongly bearish, low IV |

### Call Ratio Diagonal — Detailed Example

**Market view:** Mildly bullish on SPY. Expect 2-3% up move over 45 days. IV rank = 55% (elevated).

```
Long:  1 SPY 500 Call, DTE 75 (far-dated, ATM, delta 0.50)
Short: 2 SPY 510 Call, DTE 21 (near-dated, 2% OTM, delta 0.35 each)

Net Greeks at entry:
- Delta: +0.50 - 2×0.35 = -0.20 (slightly bearish at entry → stock must rise)
- Gamma: +0.02 - 2×0.04 = -0.06 (short gamma — position hurts on large moves)
- Theta: -0.03 + 2×0.06 = +0.09 (positive theta — time decay works for you)
- Vega:  +0.15 - 2×0.08 = -0.01 (roughly vega-neutral)
```

[COMPUTED] The negative delta at entry is intentional: the stock must rise to reach the profit zone. Once the stock moves up, delta becomes positive as the OTM shorts go further OTM.

### P&L Zones (Call Ratio Diagonal 1:2)

```
Zone 1 (Stock flat or down): Small loss. Theta collection offsets some of the negative delta loss.
Zone 2 (Stock slowly rising to K_short): MAX PROFIT. Short legs decay, long leg appreciates.
Zone 3 (Stock above K_short): Profit declines as additional short legs go ITM.
Zone 4 (Stock well above K_short): Loss. The extra short leg dominates.
```

[COMPUTED] Max profit at near-expiration with stock at K_short:
```
Max profit ≈ (K_short - K_long) × 100 × N_long + remaining_time_value_on_long - cost_basis
```

### Risk: The Naked Short Problem

The ratio means you have more short contracts than long. If the short strike is breached, the excess shorts (M - N) are **uncovered**. This is the primary risk:

```
At 1:2 ratio with stock above K_short:
- 1 short call is covered by the long call (diagonal spread)
- 1 short call is NAKED → unlimited risk on this leg
```

**Risk mitigation:**
1. Set a stop at K_short + 25% of the credit received
2. Buy a far OTM wing call to cap the naked short (converts to a flyagonal)
3. Close the entire position if stock closes above K_short for 2 consecutive days

---

## Part 2: Strategy Composition Framework

### The Primitive Catalog

Every options strategy is a combination of these primitives:

| Primitive | Greek Profile | P&L Characteristic |
|-----------|--------------|-------------------|
| **Long Call** | Δ+, Γ+, Θ-, V+ | Unlimited upside, defined risk |
| **Short Call** | Δ-, Γ-, Θ+, V- | Defined profit, unlimited risk |
| **Long Put** | Δ-, Γ+, Θ-, V+ | Unlimited upside (on downside), defined risk |
| **Short Put** | Δ+, Γ-, Θ+, V- | Defined profit, large defined risk |
| **Long Stock** | Δ=1, Γ=0, Θ=0, V=0 | Linear P&L, unlimited both ways |
| **Short Stock** | Δ=-1, Γ=0, Θ=0, V=0 | Linear P&L, unlimited both ways |

### Composition Rules

To build a custom structure with target Greeks:

```
Target Delta = Σ(delta_i × quantity_i × sign_i)
Target Gamma = Σ(gamma_i × quantity_i × sign_i)
Target Theta = Σ(theta_i × quantity_i × sign_i)
Target Vega  = Σ(vega_i × quantity_i × sign_i)

where sign_i = +1 for long, -1 for short
```

### Common Custom Structures

| Desired Profile | Construction Approach | Example |
|----------------|----------------------|---------|
| Delta-positive, theta-positive, gamma-neutral | Ratio diagonal (call) | 1 long far ITM call + 2 short near OTM calls |
| Delta-neutral, vega-long, theta-neutral | Double calendar | Long far ATM straddle + short near ATM straddle |
| Delta-positive, vega-short, gamma-flat | Ratio vertical | 1 long ATM call + 2 short OTM calls (same expiration) |
| Delta-short, theta-long, gamma-long | Put ratio backspread | 1 short ATM put + 2 long OTM puts |

### Composition Constraints

| Constraint | Rule | Why |
|-----------|------|-----|
| Max legs | ≤ 6 for liquid underlyings, ≤ 4 for moderate | Each leg adds execution complexity and slippage |
| Min credit/debit | Net premium ≥ $0.50/contract | Transaction costs eat smaller premiums |
| Liquidity | Each leg volume > 50, OI > 500 | Must be able to enter and exit each leg |
| Single order | Always enter as one spread order | Legging risk is catastrophic for custom structures |
| Defined risk preferred | Cap any naked shorts with wings | Unlimited risk + custom structure = unpredictable outcomes |

---

## Part 3: Delta-Gamma-Theta Target Construction

### Solving for Leg Quantities

Given target Greeks (Δ_target, Γ_target, Θ_target, V_target) and a set of candidate options with known Greeks, solve for quantities:

```
This is an underdetermined system (4 constraints, many variables).
Use iterative approach:

1. Select the primary leg based on Δ_target
2. Add a hedge leg to neutralize unwanted Γ
3. Add a time-spread leg to adjust Θ
4. Add a vega leg if needed
5. Verify all constraints
6. Check P&L diagram for unexpected behavior
```

### Example: Build a Structure That Is...

**Target:** Δ=+0.30 (moderate bullish), Γ=0 (gamma-neutral), Θ=+0.05 (positive theta), V≈0 (vega-neutral)

**Solution approach:**
```
Step 1 (Δ): Long 1 ATM call (Δ=+0.50) → need to reduce to +0.30
Step 2 (hedge): Short 1 call at higher strike (Δ=-0.20) → net Δ=+0.30
Step 3 (Θ): The short leg has Θ=-0.03, long has Θ=-0.04 → net Θ=-0.07 (negative — bad)
             → Change to diagonal: short near-dated call (Θ=-0.06) → net Θ=-0.10 → worse
             → Add 1 more short near-dated call: net Θ=-0.03+0.06=+0.03 → still not enough
             → Use 2 short near-dated + 1 long far-dated call
             → Net: Θ = -0.03 + 2×0.06 = +0.09 ✓
Step 4 (Γ): Check gamma: long Γ=+0.04, 2 shorts Γ=-0.06 each → net Γ=-0.08 (negative)
             → Increase long to 2 contracts: net Γ = 2×0.04 - 2×0.06 = -0.04 → closer
             → Widen strikes: shorts at further OTM (Γ=-0.03) → net Γ = 2×0.04 - 2×0.03 = +0.02 ✓
Step 5 (V): Verify vega. Adjust short DTE if needed.
```

**Result:** 2 long far ATM calls + 2 short near OTM calls. This is a 2:2 ratio diagonal (or 1:1 ratio diagonal × 2).

---

## Part 4: When to Build Custom vs. Use Standard

| Decision Factor | Use Standard Strategy | Build Custom |
|----------------|----------------------|-------------|
| Greek precision needed | Approximate is fine | Specific delta/theta/vega targets |
| Time to expiration | Single DTE works | Need differential time decay |
| Vol view per strike | Uniform vol view | Different IV views at different strikes/DTEs |
| Account restrictions | Reg T, no PM | Portfolio margin (efficiency matters) |
| Monitoring capability | Set-and-forget OK | Need active Greek monitoring |
| Exit strategy | Standard exit rules | Custom exit logic needed |

[COMMON-PRACTICE] 90% of options trades should use standard strategies. Custom structures add complexity without adding edge unless you have a specific, quantifiable reason for the customization.

## Common Failure Modes

| ❌ Failure Mode | Root Cause | ✅ Prevention |
|---------------|------------|--------------|
| Naked shorts in ratio diagonals blow up | Underestimated tail risk | Always cap with a far OTM wing. The small debit saves the trade |
| Custom structure Greeks shift dramatically | Did not model Greeks over time/price path | Run a 3-scenario Greek simulation: stock +1σ, flat, -1σ at 50% of DTE |
| Illiquid leg can't be closed | Built structure on moderate-liquidity name | Verify OI > 500 on every leg. Simulate exit cost before entry |
| Structure becomes something unintended | Legs were entered separately (legging) → market moved → one leg filled, others didn't | ALWAYS enter as a single spread order. If partial fill, cancel the rest immediately |
| P&L doesn't match model | Used mid-price for modeling, filled at bid/ask | Model using bid (sell legs) and ask (buy legs), not mid. If P&L disappears, skip |

## Provenance

[VERIFIED] Greek composition mathematics from Black-Scholes partial derivatives. Leg neutrality constraints from option market-making literature.
[COMMON-PRACTICE] Strategy composition framework used by options market makers and institutional volatility desks to construct bespoke hedges.
[COMPUTED] All Greek calculations use Black-Scholes with standard partial derivatives.
[ESTIMATED] "90% of trades should use standard strategies" is a practitioner heuristic. There is no academic study on this specific ratio.
[BACKTEST-EVIDENCE] Trading project data confirms that simpler strategies (long calls/puts) with proper exits outperform complex multi-leg structures for directional trades in small accounts.
[AS OF 2026-07]
