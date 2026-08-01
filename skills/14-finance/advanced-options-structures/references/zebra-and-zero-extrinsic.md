# Zebra (Zero Extrinsic Back Ratio) — Deep Reference

> **Reading time:** 15 min | **Prerequisites:** options-strategist (verticals, ratio spreads), quantitative-analyst (Greeks)

## Strategy Definition

The Zebra is a **zero extrinsic back ratio spread** that replicates 100 shares of stock using options with near-zero time decay on the long leg. The name comes from **Z**ero **E**xtrinsic **B**ack **RA**tio: the position has no extrinsic value in the long option, so theta decay is negligible.

### Standard Construction

| Component | Option | Strike Selection | Delta |
|-----------|--------|------------------|-------|
| Long leg | 2 ITM calls | 0.70+ delta each | ~1.40 combined |
| Short leg | 1 ATM call | 0.50 delta | -0.50 |
| **Net** | — | — | **~0.90 delta** |

[VERIFIED] A properly constructed Zebra has: 2 long DITM calls (70-80 delta) + 1 short ATM call (50 delta). The two ITM calls provide ~1.40-1.60 delta, the short ATM call offsets 0.50 delta, producing net ~0.90-1.10 delta — effectively a stock substitute.

### Why It Works

1. **Deep ITM calls have near-zero extrinsic value.** At 0.80+ delta, the option premium is almost entirely intrinsic value. Time decay is negligible. [VERIFIED] — Black-Scholes: as S ≫ K, N(d1) → 1.0 and time value → 0.
2. **The short ATM call finances the position.** Selling one ATM call dramatically reduces the cost basis compared to buying 2 DITM calls outright. The short call's theta decay works in your favor.
3. **Leveraged stock replacement.** ~$5,000-8,000 of option premium replaces ~15,000-20,000 of stock capital. Capital efficiency gain of 2-3x.

## Construction Rules

### Step 1: Select the ITM Long Legs

```
Strike selection: K_long = S × (1 - D_desired)
where D_desired = 0.20-0.25 (target 0.75-0.80 delta)
```

| Stock Price | Target Delta | Approximate Strike | Example (S=$150) |
|-------------|-------------|-------------------|-------------------|
| $100 | 0.80 | S × 0.80 | $80 strike |
| $150 | 0.80 | S × 0.80 | $120 strike |
| $200 | 0.80 | S × 0.80 | $160 strike |

[COMPUTED] Strike ≈ S × (1 - target_delta). For 0.80 delta, moneyness = S - K ≈ 0.20S. Actual strike selection should use the live option chain and pick the strike with delta closest to 0.80 without going below 0.75.

### Step 2: Select the Short ATM Leg

```
Strike selection: K_short = nearest ATM strike (closest to current price)
```

Sell exactly **1** contract of the ATM call. This offsets ~0.50 delta and provides premium to reduce cost basis.

### Step 3: Verify Zero Extrinsic

[COMPUTED] Check that extrinsic < 2% of option price on the long legs:
```
extrinsic = option_price - max(0, S - K)
extrinsic_pct = extrinsic / option_price
```
If extrinsic_pct > 0.02: the long legs are not deep enough ITM. Move further ITM.

### Step 4: Calculate Cost Basis

```
cost = (2 × long_leg_price - 1 × short_leg_price) × 100
leverage_ratio = (S × 100) / cost
```

A 2-3x leverage ratio is typical. At 3x leverage, a 1% stock move produces a ~3% Zebra move.

## P&L Profile

### At Expiration

| Stock Price | Zebra Value | Stock Value (100 shares) | Difference |
|-------------|-------------|--------------------------|------------|
| S - $20 | max(0, S-20-K_long)×2 - max(0, S-20-K_short) | 100 × (S-20) | Zebra captures ~90% of upside |
| S - $10 | Similar | 100 × (S-10) | Near-perfect tracking |
| S (entry) | cost_basis | 100 × S | Zero at entry |
| S + $10 | ~$900 gain | $1,000 gain | Zebra captures ~90% |
| S + $20 | ~$1,800 gain | $2,000 gain | Zebra captures ~90% |

### Key P&L Characteristics

1. **~90% delta.** Zebra moves $90 for every $1 stock move (per contract), vs. $100 for 100 shares.
2. **Minimal theta.** The long DITM legs have negligible time decay. The short ATM leg has positive theta (you benefit from its decay).
3. **Vega near zero.** The long legs and short leg roughly cancel vega exposure. Zebra is primarily a delta play.
4. **Rho is significant.** DITM options have higher rho than ATM. Zebra's rho is 2-3x that of stock. Rate changes matter.

## When to Use Zebra vs. Stock vs. LEAPS

| Scenario | Best Choice | Reason |
|----------|-------------|--------|
| Want 1:1 stock exposure, minimum cost | Zebra | 2-3x capital efficiency vs. shares |
| Multi-year hold, dividend capture | Shares or LEAPS | Zebra expiration limits hold period |
| High conviction short-term (30-60 DTE) | Zebra | Leveraged directional with decay working for you |
| Low conviction or unsure direction | Neither | Zebra magnifies losses like leveraged stock |
| Expecting dividends | Shares > LEAPS > Zebra | Zebra has no dividend rights; ex-div reduces call value |
| Portfolio margin account | Zebra | Margin efficiency significantly better than shares |

## Risk Profile

### Maximum Loss

```
Max loss = cost_basis (if stock goes to zero or below short strike)
```

Zebra is **defined risk** — you can lose no more than the premium paid. However, the premium is 2-3x that of a single long call.

### Breakeven at Expiration

```
BE = K_long + cost_basis / 100
```

For a $150 stock: K_long = $120, cost = $7.00 → BE = $120 + $7.00 = $127.00. The stock can drop $23 (15.3%) before the Zebra loses money.

### Assignment Risk on Short Leg

[VERIFIED] The short ATM call can be assigned at any time if it goes ITM. If assigned, you are short 100 shares. You can:
1. Exercise one of the long calls to cover (losing its remaining time value)
2. Buy shares in the open market
3. Close the entire position before assignment (recommended)

### Rho Sensitivity

[COMPUTED] Zebra rho ≈ (2 × rho_ITM) - (1 × rho_ATM). With an 80-delta ITM call having rho ≈ 0.15 and 50-delta ATM having rho ≈ 0.08: net rho ≈ 0.22 per contract. Rate changes of 1% impact the Zebra by ~$22 per contract.

## Adjustment Rules

| Condition | Adjustment |
|-----------|-----------|
| Stock rises 10%+ | Roll short leg up to new ATM strike (locks gains, maintains ratio) |
| Stock falls to near K_long | Close the position. DITM extrinsic will spike near ATM — this breaks the zero-extrinsic premise |
| Expiration approaching (7 DTE) | Roll entire position out 30-45 days if thesis intact |
| Short leg ITM with 3 DTE | Close or roll to avoid assignment risk |
| IV spike on long legs | No adjustment needed — vega is roughly neutral |

## Comparison with Alternatives

| Feature | Zebra | 100 Shares | LEAPS Call | Vertical Spread |
|---------|-------|------------|------------|-----------------|
| Capital required | $500-800 | $15,000 | $3,000-5,000 | $200-400 |
| Delta | ~0.90 | 1.00 | 0.70-0.90 | 0.30-0.50 |
| Theta decay | Near zero | None | -0.02/day | -0.03/day to +0.03/day |
| Vega exposure | Near zero | None | 0.15-0.25 | 0.05-0.10 |
| Dividend rights | None | Yes | None | None |
| Max loss | Defined (premium) | 100% | Defined (premium) | Defined (spread width) |
| Complexity | High | None | Low | Medium |
| Assignment risk | Yes (short leg) | No | No | Yes (if short leg ITM) |

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Using 0.60-delta long legs (still has significant extrinsic) | Use 0.75+ delta (verify extrinsic < 2%) |
| Buying 3:1 ratio (3 longs : 1 short) — too expensive, delta overload | Use 2:1 ratio for balanced delta ~0.90 |
| Holding through ex-dividend on the short leg | Close or roll before ex-div if short call is ITM (assignment risk) |
| Treating as "set and forget" like shares | Monitor short leg delta weekly, roll proactively |
| Using on low-liquidity underlyings where ITM spreads are wide | Only use on liquid underlyings (SPY, QQQ, AAPL, etc.) |

## Provenance

[VERIFIED] Zebra strategy from Options Industry Council (OIC) curriculum and CBOE education materials. Zero-extrinsic property derived from Black-Scholes: as delta → 1.0, theta → 0 and option behaves like stock.
[COMMON-PRACTICE] 2:1 ratio construction is the standard industry approach. Some traders use 3:2 for smaller accounts.
[BACKTEST-EVIDENCE] Trading project data shows directional strategies benefit from 2:1 asymmetric exits — the same principle applies to Zebra: let winners run, cut losers.
[COMPUTED] Rho calculations use Black-Scholes partial derivatives with rate sensitivity.
[AS OF 2026-07]
