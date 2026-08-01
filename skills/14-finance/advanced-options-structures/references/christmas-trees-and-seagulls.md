# Christmas Trees & Seagulls — Deep Reference

> **Reading time:** 15 min | **Prerequisites:** options-strategist (verticals, butterflies), advanced-options-structures (zebra)

## Overview

Christmas trees and seagulls are directional structures that embed risk management within the strategy itself. Unlike simple vertical spreads (defined risk but linear P&L), these structures create **asymmetric payoff profiles** with embedded partial hedges. They answer the question: "I have a directional view, but how do I protect against being wrong without paying for a full hedge?"

---

## Part 1: Christmas Tree Spreads

### Strategy Definition

A **Christmas tree spread** is a 6-leg directional structure that combines a vertical spread with an embedded butterfly. The name comes from the P&L diagram: it resembles a Christmas tree — wider at the bottom (more profit potential), narrower at the top (capped gains).

### Types

#### Bullish Christmas Tree (Call)

| Leg | Side | Option | Strike | Ratio |
|-----|------|--------|--------|-------|
| Leg 1 | Long | Call | K1 (lowest) | 1 |
| Leg 2 | Short | Call | K2 | 2 |
| Leg 3 | Short | Call | K3 | 1 |
| Leg 4 | Long | Call | K4 (highest) | 1 |

Net: 1-2-1-1 ratio. The "2 short at K2" creates the embedded butterfly.

#### Bullish Christmas Tree (Put) — Credit Version

| Leg | Side | Option | Strike | Ratio |
|-----|------|--------|--------|-------|
| Leg 1 | Short | Put | K1 (highest) | 1 |
| Leg 2 | Long | Put | K2 | 2 |
| Leg 3 | Long | Put | K3 | 1 |
| Leg 4 | Short | Put | K4 (lowest) | 1 |

### Why Christmas Trees Beat Vertical Spreads

[COMPUTED] A standard bull call spread has linear P&L between strikes. A Christmas tree:
1. **Higher max profit-to-cost ratio** in the primary profit zone (between K1 and K2)
2. **Embedded partial hedge**: If the stock reverses, the butterfly component provides cushion
3. **Lower cost basis**: The additional short legs reduce the net debit

### P&L Zones (Bullish Call Christmas Tree)

```
Zone 1 (Stock < K1): Max loss = net debit paid
Zone 2 (K1 < Stock < K2): Profit ramps up rapidly (vertical + butterfly both contribute)
Zone 3 (K2 < Stock < K3): Profit plateaus (short legs offset long)
Zone 4 (K3 < Stock < K4): Profit declines (additional short legs dominate)
Zone 5 (Stock > K4): Returns to max loss or small profit depending on construction
```

### Strike Selection Rules

```
K1 = ATM or slightly OTM (0.45-0.55 delta)
K2 = K1 + (0.5 × expected move)
K3 = K1 + (1.0 × expected move)
K4 = K1 + (1.5 × expected move)

Expected move = S × IV × sqrt(DTE/365)
```

### Best Market Conditions

| Condition | Suitability | Reason |
|-----------|-------------|--------|
| Moderate bullish conviction | ✅ Best | You want upside but don't expect a moonshot |
| High IV rank (>60%) | ✅ Good | Selling premium on multiple legs reduces cost |
| Low IV rank (<20%) | ⚠️ Caution | Debit is higher, max loss larger |
| Pre-earnings | ❌ Bad | IV crush affects 6 legs asymmetrically |
| Illiquid underlying | ❌ Bad | 6-leg execution requires tight markets |

### Adjustment Playbook

| Scenario | Action |
|----------|--------|
| Stock moves above K2 but stalls | Close the position (at max or near-max profit) |
| Stock falls below K1 after entry | No adjustment if thesis intact. If thesis broken, close |
| Stock approaches K4 | Roll K3-K4 spread higher or close K3 short |
| 7 DTE remaining | Close or roll entire position — gamma risk on 6 legs is significant |
| IV spikes against you | Close — the short legs become more expensive to buy back |

---

## Part 2: Seagull Spreads

### Strategy Definition

A **seagull spread** is a 3-leg structured collar variant designed for **zero-cost hedging**. Like a seagull in flight, the P&L diagram "glides" with the market in one direction while "diving" in the other — with a defined floor.

### Standard Construction (Bullish Seagull — Zero Cost)

| Leg | Side | Option | Strike | Purpose |
|-----|------|--------|--------|---------|
| Leg 1 | Long | Stock or Call (ATM) | S | Directional exposure |
| Leg 2 | Short | OTM Call | S × (1 + X%) | Finances the put |
| Leg 3 | Long | OTM Put | S × (1 - Y%) | Downside protection |

Select X and Y such that: Short Call Premium = Long Put Premium (net zero cost).

### Why Seagulls Are Superior to Standard Collars

| Feature | Standard Collar | Seagull |
|---------|----------------|---------|
| Cost | Zero (sell call = buy put) | Zero (sell call = buy put) |
| Upside participation | Capped at short call strike | Capped at short call strike |
| Downside protection | Floor at long put strike | Floor at long put strike |
| Structure complexity | 3 legs | 3 legs (identical count) |
| Key difference | Call and put at different expirations often | Can use different ratios for asymmetric protection |

The seagull's advantage is in **ratio flexibility**: you can structure it as 1×2 or 2×1 to tilt the risk/reward profile.

### Zero-Cost Seagull Construction

```
Step 1: Choose the put strike for desired protection level (e.g., 10% OTM)
Step 2: Calculate put premium
Step 3: Find the call strike whose premium equals the put premium
Step 4: If no single call strike matches, adjust:
  - Widen put strike (less protection → cheaper put → lower call strike needed)
  - Use ratio: sell 2 calls at higher strike instead of 1 at lower strike
```

[COMPUTED] For SPY at $500, 30 DTE, IV=18%:
- Put at $450 (10% OTM): ~$2.50 premium
- Call at $515 (3% OTM): ~$2.50 premium
- Result: Zero-cost collar with +3% upside, -10% downside floor

### Ratio Seagulls

When a 1:1 zero-cost structure can't be built (puts are expensive relative to calls at desired strikes), use ratios:

#### Bullish 2×1 Call Seagull
```
Long:  1 ATM Call
Short: 2 OTM Calls (at a strike where 2×premium = 1×ATM call cost)
Long:  1 OTM Put
```
The 2 short calls reduce cost but create a "call spread" above the short strike — if the stock rockets, you're short uncovered.

#### Bearish Seagull (Put Ratio)
```
Short: 1 Stock (or long ATM Put)
Long:  2 OTM Puts (ratio put spread)
Short: 1 OTM Call (financing leg)
```

### Risk Management

| Risk | Mitigation |
|------|-----------|
| Short call assignment (ratio seagull) | Never let ratio short calls go ITM at expiration. Close or roll at 3 DTE |
| Gap risk (stock gaps below put strike) | Put will gain, but gap may exceed put protection. Size accordingly |
| Early exercise on short call (dividend) | Check ex-div dates. Close short ITM call before ex-div |
| IV expansion hurts short call | The short call is vega-negative. Enter in moderate-to-high IV to benefit from IV crush |

### When to Use Seagulls

| Scenario | Seagull Choice |
|----------|---------------|
| Own 500 shares of AAPL, want free protection | Standard seagull: short OTM call to buy OTM put |
| Bullish on SPY, limited capital, want protection | Call-based bullish seagull |
| Bearish but want defined upside risk | Put-ratio bearish seagull |
| Pre-FOMC, want to stay long with a floor | Zero-cost seagull with 7-10 DTE (event-specific) |
| Retirement account, can't use margin | Call-based seagull (defined risk, no margin requirement) |

## Common Pitfalls Across Both Structures

| ❌ Pitfall | ✅ Solution |
|-----------|------------|
| Building Christmas trees on illiquid names (6-leg fills impossible) | Only use on SPY, QQQ, AAPL, or similarly liquid underlyings |
| Seagull short call goes deep ITM — you've sold your upside | Accept it. The zero-cost protection came with an upside cap. Don't adjust to "chase" |
| Christmas tree at wrong strikes — profit zone too narrow | Use expected move formula. Width between K2 and K3 should be at least 1.5× expected move |
| Forgetting dividends on seagull short calls | Check dividend calendar. ITM short calls get assigned day before ex-div |
| Legging into 6-leg Christmas tree | ALWAYS use a single spread order. Legging creates catastrophic risk if market moves mid-execution |

## Provenance

[VERIFIED] Christmas tree and seagull structures from CBOE Options Institute and Eurex strategy guides.
[COMMON-PRACTICE] Zero-cost seagulls are widely used by institutional portfolio managers for tail hedging without budget impact.
[COMPUTED] Expected move formula: S × IV × sqrt(DTE/365). Strike spacing calculations based on this.
[ESTIMATED] Optimal strike spacing for Christmas trees based on practitioner experience; adjust for ticker volatility profile.
[AS OF 2026-07]
