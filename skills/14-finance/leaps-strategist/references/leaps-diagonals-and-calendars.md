# LEAPS Diagonals & Calendars — Deep Reference

> **Reading time:** 12 min | **Prerequisites:** options-strategist (calendars, diagonals), leaps-strategist (stock replacement, PMCC)

## Overview

LEAPS diagonals and calendars extend the PMCC concept into multi-cycle premium harvesting strategies. The core insight: a single DITM LEAPS call can serve as the "backing" for **multiple cycles** of short-dated premium collection, amortizing the LEAPS' extrinsic cost across many short-leg expirations.

## LEAPS Diagonal (PMCC Extended)

### Multi-Cycle Premium Harvesting

```
Setup: Buy 1 LEAPS Call (DTE 540, K_long, Δ=0.85) for $X

Cycle 1: Sell 1 30-DTE Call (K_short1, Δ=0.25) for premium P1
  → At expiration or 50% profit: close/roll short leg
Cycle 2: Sell 1 30-DTE Call (K_short2, Δ=0.25) for premium P2
  → Repeat...
Cycle N: Sell 1 30-DTE Call (K_shortN, Δ=0.25) for premium PN

After N cycles: Total premium collected = P1 + P2 + ... + PN
```

[COMPUTED] With 12 monthly cycles at 1% monthly ROC (on LEAPS cost), annual premium collected ≈ 12% of LEAPS cost. This offsets the LEAPS extrinsic decay and dividend gap.

### The Amortization Math

```
LEAPS cost: $11,500 (SPY 400 Call, Jan 2027)
LEAPS extrinsic: $1,100 (must be "earned back" through premium)

Monthly premium target: $150-250 (1.3-2.2% monthly ROC on LEAPS cost)
Months to amortize extrinsic: $1,100 / $200 ≈ 5.5 months

After 6 months: Extrinsic fully amortized. Remaining premium = pure profit.
Remaining LEAPS life: 12+ months of premium harvesting.
```

### Strike Progression Across Cycles

```
Cycle 1 (Month 1): Short K = S × 1.03 (3% OTM, Δ=0.25)
  Stock at $500 → sell $515 call

Month 2: Stock at $510
Cycle 2: Short K = S × 1.03 = $525
  Rolled up to maintain 3% OTM distance

Month 3: Stock at $495 (pulled back)
Cycle 3: Short K = S × 1.03 = $510
  Rolled down to capture premium at new price level
```

**Rule:** Every cycle, set the short strike at the same delta (e.g., 0.25) relative to current price. This maintains consistent probability OTM while capturing more premium as the stock rises.

### When the LEAPS Goes Deep ITM

If the stock has rallied significantly and the LEAPS is now at 0.95+ delta:

```
Option 1: Sell the entire position. LEAPS has captured most of the upside.
Option 2: Roll the LEAPS up to a higher strike, taking profits and resetting to 0.80 delta.
Option 3: Continue selling calls at wider OTM strikes (e.g., 0.15 delta instead of 0.25).
```

## Double LEAPS Calendar

### Strategy Definition

A **double LEAPS calendar** combines a LEAPS diagonal on the call side with a LEAPS diagonal on the put side:

```
Long:  1 LEAPS Call (DITM, DTE 540)  +  1 LEAPS Put (OTM, DTE 540)
Short: 1 Near Call (OTM, DTE 30)      +  1 Near Put (OTM, DTE 30)
```

This creates a delta-neutral, theta-positive position that harvests premium from both sides while the LEAPS provide long-dated vega exposure.

### Construction

| Leg | Side | Option | Strike | DTE | Delta |
|-----|------|--------|--------|-----|-------|
| Long 1 | Long | Call | 0.85Δ (DITM) | 540 | +0.85 |
| Short 1 | Short | Call | 0.25Δ (OTM) | 30 | -0.25 |
| Long 2 | Long | Put | 0.85Δ (DITM) | 540 | -0.85 |
| Short 2 | Short | Put | 0.25Δ (OTM) | 30 | +0.25 |
| **Net** | — | — | — | — | **~0.00** |

### Why Double LEAPS Calendars?

1. **Delta-neutral premium harvesting.** Collect theta from both call and put short legs.
2. **Vega-positive.** The long LEAPS have significant vega → position gains from IV expansion.
3. **Wider profit range than iron condor.** The long LEAPS provide protection on large moves that would hurt an iron condor.
4. **Cost:** 2 LEAPS premiums = higher capital requirement. ~$25,000-35,000 for SPY-sized double LEAPS calendar.

### When to Use

| Scenario | Best Structure |
|----------|---------------|
| Sideways market, low IV, expect IV to rise → IV expansion gains on LEAPS | Double LEAPS Calendar |
| Bullish, want income → PMCC (single LEAPS diagonal) | PMCC |
| Sideways, high IV, expect IV to fall → vega-negative | Iron Condor (NOT double LEAPS calendar) |

## LEAPS Ratio Calendar

### Strategy Definition

A leveraged variant where more near-dated shorts are sold than LEAPS held:

```
Long:  1 LEAPS Call (DITM)
Short: 2 Near Calls (OTM, different strikes or same)

Ratio: 1:2 (1 LEAPS backs 2 near-dated shorts)
```

[VERIFIED] This is only appropriate in Portfolio Margin accounts. In Reg T, the "extra" short call is treated as uncovered — margin requirement is punitive.

### P&L Profile

```
Max profit: Stock at or just below the higher short strike at near expiration.
  = LEAPS appreciation + both short calls expire worthless

Risk: Stock rallies above BOTH short strikes. One short is covered by LEAPS.
  The other is NAKED → unlimited risk above the higher short strike.
```

[COMMON-PRACTICE] LEAPS ratio calendars are used by professional traders in PM accounts to juice returns in range-bound markets. The naked short risk makes them inappropriate for most retail accounts.

## Common Pitfalls

| ❌ Pitfall | ✅ Prevention |
|-----------|--------------|
| LEAPS extrinsic cost > total premium collected over remaining life | Before entry: sum of expected premiums must exceed extrinsic. If not, the trade is -EV |
| Short call strike BELOW LEAPS strike (guaranteed loss on assignment) | Always: short_K > long_K. This is the PMCC prime directive |
| LEAPS DTE < 180 at entry → not enough cycles to amortize extrinsic | Minimum 365 DTE for PMCC. 540+ preferred |
| Trading LEAPS on illiquid names → wide spreads on both long and short legs | Only SPY, QQQ, IWM, AAPL, MSFT, and similarly liquid LEAPS |
| Rolling short calls for debits repeatedly → "death by a thousand rolls" | Max 2 debit rolls. If third roll would be a debit, close the position |

## Provenance

[VERIFIED] PMCC/LEAPS diagonal mechanics from CBOE and OIC. Multi-cycle premium harvesting from practitioner literature.
[COMPUTED] Amortization calculations use arithmetic. Actual results depend on IV environment and strike selection.
[COMMON-PRACTICE] 12 cycles/year at 1% monthly ROC is a target, not a guarantee. Realized premium varies with IV.
[ESTIMATED] Double LEAPS calendar capital requirement based on SPY at $500. Scale linearly for other underlyings.
[AS OF 2026-07]
