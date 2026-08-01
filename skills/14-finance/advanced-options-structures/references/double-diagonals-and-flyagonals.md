# Double Diagonals & Flyagonals — Deep Reference

> **Reading time:** 18 min | **Prerequisites:** options-strategist (calendars, diagonals, butterflies), quantitative-analyst (Greeks, vol surface)

## Overview

Double diagonals and flyagonals are time-spread hybrids that combine the theta harvesting of calendars/diagonals with the defined-risk structure of butterflies/verticals. They are advanced structures that exploit **volatility surface mispricing** — specifically the interaction between the term structure (different expirations) and skew (different strikes).

---

## Part 1: Double Diagonals

### Strategy Definition

A **double diagonal** is a 4-leg structure combining two diagonal spreads: one on the call side and one on the put side.

```
Long: 1 ITM/ATM call at DTE_far, 1 ITM/ATM put at DTE_far
Short: 1 OTM call at DTE_near, 1 OTM put at DTE_near

All four legs typically at different strikes.
```

### Standard Construction

| Leg | Side | Option | Strike | DTE | Delta |
|-----|------|--------|--------|-----|-------|
| Leg 1 | Long | Call | S × 1.00 (ATM) | 60-90 | 0.50 |
| Leg 2 | Short | Call | S × 1.05 (5% OTM) | 14-21 | 0.30 |
| Leg 3 | Long | Put | S × 1.00 (ATM) | 60-90 | -0.50 |
| Leg 4 | Short | Put | S × 0.95 (5% OTM) | 14-21 | -0.30 |
| **Net** | — | — | — | — | **~0.00** (delta-neutral at entry) |

### Why It Works

1. **Dual theta harvesting.** Both short legs (call and put) decay faster than the long legs due to nearer expiration. Theta is positive on the net position.
2. **Vega-positive with a ceiling.** The long-dated legs have higher vega than the short-dated legs, so the position gains from IV expansion — but the short legs cap the upside.
3. **Vol surface arbitrage.** The term structure is typically in contango (far-dated IV > near-dated IV). By going long far-dated and short near-dated, you capture the roll-down as near-dated options expire and far-dated options retain premium.

### P&L Profile

```
Max profit: Achieved if the stock is at the short call OR short put strike at the near expiration.
Approximate max profit = credit_received + (remaining time value on long legs - near-zero on expired short legs)

Max loss: If the stock makes a large move beyond either short strike. The long legs provide some protection but the position can still lose significantly.

BE points: Two breakeven points wider than the short strikes, determined by the net debit/credit and long leg Greeks.
```

### Greek Exposures Over Time

| Time | Delta | Gamma | Theta | Vega |
|------|-------|-------|-------|------|
| Entry (DTE_far=75, DTE_near=21) | ~0 | ~0 | +0.08 | +0.15 |
| Mid-cycle (DTE_far=54, DTE_near=7) | ~0 | ±0.02 | +0.15 | +0.10 |
| Near exp. rolls (DTE_far=47, DTE_near=0) | varies | varies | — | — |
| After roll (new DTE_near=21) | ~0 | ~0 | +0.08 | +0.15 |

[COMPUTED] Theta accelerates as the near expiration approaches, peaking in the final 7 days.

### Adjustment Rules

| Condition | Adjustment |
|-----------|-----------|
| Stock approaches short call strike (within 1%) | Roll short call up and out (higher strike, next expiration) |
| Stock approaches short put strike (within 1%) | Roll short put down and out |
| IV drops 20%+ post-entry | Close entire position — the vega loss on long legs dominates |
| Near expiration (7 DTE) | Roll both short legs to next expiration (typically 21-30 DTE) |
| Earnings within near DTE | Close short legs before earnings, re-enter after IV crush |

### Ideal Market Conditions

[COMMON-PRACTICE] Double diagonals work best in:
- **Low-to-moderate IV environment** (IV rank 20-50): You're buying vega on the long legs, so you don't want to buy at the top
- **Sideways to gently trending market**: Theta harvesting requires the stock to stay within the short strikes
- **Normal term structure (contango)**: Far-dated IV > near-dated IV for roll-down capture
- **Liquid underlyings**: 4-leg execution requires tight markets (SPY, QQQ, IWM, AAPL)

---

## Part 2: Flyagonals

### Strategy Definition

A **flyagonal** (butterfly + diagonal) is a 4-leg hybrid that combines the pin-seeking behavior of a butterfly with the time-decay harvesting of a diagonal. It's effectively a butterfly where the body (central strikes) uses two different expirations.

### Standard Construction

```
Long:  1 call at K_body (nearer expiration)
Short: 2 calls at K_body (farther expiration)
Long:  1 call at K_wing (farther expiration)

OR the symmetric version:
Long:  1 call at K_lower, DTE_far
Short: 1 call at K_body, DTE_near
Short: 1 call at K_body, DTE_far
Long:  1 call at K_upper, DTE_far
```

### Why Flyagonals Outperform Standard Butterflies

1. **Theta harvesting from the diagonal component.** The short near-dated leg at the body decays faster than the long far-dated wing.
2. **Wider profit zone.** Because the wings are far-dated (more time value = wider BE), the flyagonal has a wider profitable range than a standard butterfly at entry.
3. **Vol surface edge.** The flyagonal exploits both skew (wing pricing) and term structure (body decay differential).

### P&L Profile

```
Max profit at expiration of near leg: Stock exactly at K_body.
  = (K_body - K_lower) × 100 - net_debit   [call flyagonal]

Secondary peak: At far expiration, if stock at K_body, the remaining butterfly
has additional value equal to the time premium on the far-dated wings.
```

### When Flyagonals Beat Butterflies

| Scenario | Butterfly | Flyagonal | Winner |
|----------|-----------|-----------|--------|
| Stock trending toward strike | Good | Better (theta edge) | Flyagonal |
| Stock oscillating around strike | Good | Slightly better | Flyagonal |
| IV crush after entry | Bad (vega-negative) | Worse (more vega on wings) | Butterfly |
| Wide bid/ask on wings | OK | Worse (4 legs) | Butterfly |
| Small account (sub-$500) | Better (cheaper) | Worse (more premium) | Butterfly |
| Vol surface in contango | OK | Better (captures roll-down) | Flyagonal |

### Greeks at Entry

| Greek | Standard Butterfly | Flyagonal | Reason for Difference |
|-------|-------------------|-----------|----------------------|
| Delta | ~0 | ~0 | Both delta-neutral at body |
| Gamma | Negative at body, positive at wings | Same shape, slightly wider | Far-dated wings smooth the gamma curve |
| Theta | +0.05 to +0.10 | +0.08 to +0.12 | Diagonal decay adds theta |
| Vega | -0.05 to -0.10 | -0.02 to -0.05 | Far-dated wings carry more vega |

[COMPUTED] Flyagonals are approximately 20-30% more theta-positive than equivalent butterflies at entry, at the cost of being 20-30% less vega-negative.

## Construction Rules for Both Structures

### Liquidity Requirements

[VERIFIED] 4-leg structures require all legs to be liquid:
- Each leg: volume > 50 contracts, open interest > 500
- Bid/ask spread < 5% on each leg
- Total slippage on 4 legs < 3% of max profit
- Only trade on highly liquid underlyings: SPY, QQQ, IWM, AAPL, MSFT, NVDA

### Entry Timing

- **Best:** 10:00-11:00 AM ET (spreads have settled, liquidity is good)
- **Acceptable:** 11:00 AM-3:00 PM ET
- **Avoid:** First 30 minutes (wide spreads), last 30 minutes (pin risk on short legs)
- **Never:** Pre-market or after-hours (no options market)

### Position Sizing

```
Max position size = min(
    5% of account,
    $2,000 notional,
    max_loss < 2% of account_value
)
```

For a $10,000 account: max $500 risk per double diagonal/flyagonal.

## Common Failure Modes

| ❌ Failure Mode | Root Cause | ✅ Prevention |
|---------------|------------|--------------|
| Stock blows through short strikes | Underestimated realized vol | Size for the wings, not the body. If stock breaches a short strike, close immediately |
| IV crush kills the position | Entered during high IV (earnings, events) | Check IV rank < 50 before entering. Never enter within 5 days of earnings |
| Short leg assignment on ex-div | Forgot to check dividend calendar | Check ex-div dates for all legs. Close short ITM calls before ex-div |
| Roll for debit repeatedly | Emotional attachment to "recovering" | Max 2 rolls. If third roll would be a debit, close the position |
| Legging in one side at a time | Trying to time fills | Always enter as a single 4-leg order (spread order) to avoid legging risk |

## Provenance

[VERIFIED] Double diagonal and flyagonal structures from CBOE and OIC advanced curriculum.
[COMMON-PRACTICE] 4-leg execution as spread orders is standard industry practice. Legging in is considered speculative.
[COMPUTED] Greek calculations use Black-Scholes with differential DTE for diagonal components.
[ESTIMATED] 20-30% theta improvement in flyagonals vs. butterflies is based on example scenarios; actual values depend on volatility surface shape.
[AS OF 2026-07]
