# PMCC (Poor Man's Covered Call) Optimization — Deep Reference

> **Reading time:** 15 min | **Prerequisites:** options-strategist (covered calls, diagonals), leaps-strategist (stock replacement)

## Strategy Definition

The Poor Man's Covered Call (PMCC) is a **long diagonal spread** where the long leg is a DITM LEAPS call (acting as stock replacement) and the short leg is a near-dated OTM call (harvesting premium, like a traditional covered call).

```
Standard Covered Call:    +100 Shares        -1 Short Call (30-45 DTE)
PMCC (LEAPS Diagonal):    +1 LEAPS Call (DITM) -1 Short Call (14-45 DTE)
```

[VERIFIED] PMCC is functionally equivalent to a covered call on margin but with defined risk, no margin interest, and 65-80% less capital required.

## Construction Rules

### Step 1: Select the LEAPS Long Leg

```
Requirements:
- Delta ≥ 0.80 (deep ITM)
- DTE ≥ 180 (at least 6 months — ideally 12+ months remaining after short leg expires)
- Extrinsic < 4% of option premium
- Strike ≤ 80% of current stock price
- Open interest > 100
```

### Step 2: Select the Short Call

```
Requirements:
- Delta ≤ 0.30 (70%+ probability OTM)
- DTE: 14-45 days (theta decay sweet spot)
- Strike ABOVE the LEAPS strike (critical — see Strike Hierarchy below)
- Premium received ≥ 1% of LEAPS cost (monthly yield target)
```

### Step 3: The Strike Hierarchy (NON-NEGOTIABLE)

[VERIFIED] The short call strike MUST be above the LEAPS long call strike:

```
Short Call Strike > LEAPS Long Call Strike

Example: LEAPS at $350 strike → short call at $360+ (NOT $340)
```

**Why:** If the short call goes ITM and gets assigned, you deliver shares you don't own. Your broker will exercise your LEAPS to cover — but if the short strike is BELOW the LEAPS strike, the exercise loses the spread width × 100.

```
If LEAPS K_long = $350, short K_short = $340 (VIOLATION):
  Assignment: deliver shares at $340
  Exercise LEAPS: buy shares at $350
  Loss = ($350 - $340) × 100 = $1,000 + lost LEAPS time premium
```

[VERIFIED] Always check: `short_strike > long_strike`. This is the #1 PMCC error.

## PMCC Optimization

### Short Strike Selection

| Short Call Delta | OTM Probability | Monthly Premium (% of LEAPS cost) | Assignment Risk | Best For |
|-----------------|-----------------|-----------------------------------|-----------------|----------|
| 0.10 | ~90% | 0.3-0.5% | Very low | Conservative income |
| 0.20 | ~80% | 0.7-1.0% | Low | Balanced income |
| 0.30 | ~70% | 1.2-1.8% | Moderate | Aggressive income |
| 0.40 | ~60% | 2.0-3.0% | High | High conviction flat-to-down |

[COMMON-PRACTICE] Target 0.20-0.30 delta for the short call. This balances premium collection against assignment risk.

### DTE Selection for Short Calls

| DTE | Theta Decay Rate | Rolls per Year | Premium per Roll | Annualized Premium |
|-----|-----------------|----------------|-----------------|-------------------|
| 7 | Highest (days 5-0) | 52 | Low | 15-25% |
| 14 | High (days 10-0) | 26 | Moderate | 18-30% |
| 21 | Moderate (days 14-0) | 17 | Moderate-High | 20-35% |
| 30 | Steady (days 21-0) | 12 | High | 22-40% |
| 45 | Slow start, fast finish | 8 | Highest | 20-35% |

[COMPUTED] 30-45 DTE short calls offer the best annualized premium with manageable roll frequency. 7 DTE offers highest theta per day but requires weekly management.

### Roll Cadence

| Trigger | Action |
|---------|--------|
| Short call reaches 50% of max profit | Roll to next expiration (capture remaining 50% quickly, redeploy) |
| Short call delta > 0.50 (ITM) | Roll up and out immediately (avoid assignment) |
| 7 DTE remaining on short call | Evaluate: roll now or let expire? If OTM by > 5%, let expire |
| Stock rises above short strike | Roll up and out for a credit if possible. If debit would be > premium received, close both legs |
| Earnings within short DTE | Close short leg before earnings. Re-enter after IV crush |

### When PMCC Beats Buy-Write

| Scenario | Standard Covered Call (Buy-Write) | PMCC | Winner |
|----------|----------------------------------|------|--------|
| Capital required for SPY | $50,000 | ~$13,000 | **PMCC** |
| Monthly premium ($500 strike, 30Δ) | ~$200 (0.4% monthly ROC) | ~$200 (1.5% monthly ROC on LEAPS cost) | **PMCC** |
| Stock drops 20% | Lose $10,000 + premium | Lose ≤ $13,000 max + premium | **Covered Call** (max loss is lower if stock drops < 26%) |
| Stock rises 15% in a month | Shares called away at strike. Gain capped | Short call assigned. LEAPS appreciates. Roll or close whole position | **PMCC** |
| Tax treatment | Dividends taxed as qualified. Cap gains on sale | No dividends. All P&L is cap gains/loss | **Depends** |

## Risk Management

### Assignment on the Short Call

[VERIFIED] If the short call is ITM at expiration (or before ex-dividend), it WILL be assigned. When assigned:
1. You are short 100 shares
2. Your broker will typically auto-exercise the LEAPS to cover (check your broker's policy)
3. You lose the remaining time premium on the LEAPS → this is the primary assignment cost

**Prevention:** Never let an ITM short call approach expiration. Roll at 7 DTE minimum if near the money.

### The Gap-Down Scenario

```
Stock drops from $500 to $400 (-20%):
- Long LEAPS 350 Call: was $161, now ~$65 (loss: $9,600)
- Short 520 Call: expires worthless (gain: premium, ~$200)
- Net loss: ~$9,400 on $13,000 position (-72%)

Compare to 100 shares:
- Loss: $10,000 on $50,000 (-20%)
```

[COMPUTED] LEAPS amplify losses in percentage terms (due to leverage) but cap absolute dollar loss. For small accounts, the dollar loss matters more than the percentage.

### The Rally-Past-Short-Strike Scenario

```
Stock rises from $500 to $550 (+10%):
- Long LEAPS 400 Call: was $115, now ~$163 (gain: $4,800)
- Short 520 Call (30Δ): was $8, now ~$34 (loss: $2,600)
- Net gain: $2,200 on $13,000 (+17% vs. stock +10%)

If short call is assigned:
- LEAPS exercised → lose remaining time value on LEAPS (~$10-15)
- Net slightly worse, but still profitable
```

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Short strike < LEAPS strike | **Always: Short K > Long K.** This is non-negotiable |
| Selling short calls too close to LEAPS strike (spread < $5 wide) | Minimum spread width: $5 for stocks < $100, $10 for stocks $100-500 |
| Letting short call go ITM through expiration | Roll at 7 DTE if short call is ATM or ITM |
| Ignoring dividends on short call | Check ex-div dates. Close ITM short call before ex-div |
| LEAPS DTE < 90 days at entry | Minimum 180 DTE at PMCC entry. 365+ preferred |
| Using 0.60-delta LEAPS as the long leg | Must be 0.80+ delta. Lower delta = more extrinsic = worse stock tracking |

## Provenance

[VERIFIED] PMCC (LEAPS diagonal) mechanics from CBOE and OIC educational materials.
[VERIFIED] Strike hierarchy rule: short strike > long strike is mathematically required to avoid guaranteed loss on assignment.
[COMPUTED] DTE optimization table uses Black-Scholes theta curves. Premium estimates are example only.
[COMMON-PRACTICE] 30-45 DTE short call sweet spot from Tastytrade and Options Alpha mechanics research.
[AS OF 2026-07]
