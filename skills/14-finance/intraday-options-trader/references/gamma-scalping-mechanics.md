# Gamma Scalping Mechanics — Intraday Options Reference

> **Reading time:** 12 min | **Prerequisites:** quantitative-analyst (Greeks, especially gamma), options-strategist (ATM strategies), intraday-options-trader

## What Is Gamma Scalping?

[VERIFIED] Gamma scalping is the practice of dynamically delta-hedging a long gamma position to capture the difference between realized volatility and implied volatility. When you own an ATM option (long gamma), every favorable move in the underlying increases your delta. By re-hedging (selling deltas after a rally, buying deltas after a drop), you scalp profits from the underlying's movement.

```
Core equation: Gamma scalping P&L ≈ (realized_vol² - implied_vol²) × gamma × S² × t

If realized vol > implied vol: gamma scalping profits exceed theta decay → net profit
If realized vol < implied vol: theta decay exceeds scalping profits → net loss
```

## The Gamma Scalping Setup

### Required Position

```
Long 1 ATM option (call or put — gamma is identical for ATM)
+ Delta hedge (short stock to neutralize delta at entry)

Or equivalently: Long 1 ATM straddle (long call + long put at same strike)
Both legs have positive gamma. No initial delta hedge needed if strikes are balanced.
```

### Entry Criteria

| Criterion | Requirement | Why |
|-----------|------------|-----|
| IV percentile | < 30% | Cheap vol = more likely realized > implied |
| Implied move | Must be LESS than average true range (ATR) × 2 | Market is underpricing potential movement |
| Spread as % of option price | < 5% | Scalping requires frequent trading — spread must be tight |
| DTE | 0-7 DTE (0DTE through weekly) | Highest gamma/theta ratio. Intraday: 0DTE. Multi-day: 3-7 DTE |
| Underlying | SPX, SPY, QQQ only | Liquidity for rapid re-hedging. No single-stock gap risk |

### Sizing

```
Gamma scalp position size = normal_size × 0.30

The 30% multiplier accounts for:
1. Frequent rebalancing costs (commissions, spread)
2. Higher monitoring intensity
3. Model risk (gamma scalping P&L is path-dependent, not point-in-time)
```

## The Hedging Mechanics

### Hedge Band Method

Instead of continuously delta-hedging (impossible), use a hedge band:

```
1. Calculate gamma exposure: GEX = gamma × S² × 100 per 1% move
2. Set hedge band = GEX × 0.50 (hedge when delta moves by half the gamma exposure)
3. When delta exceeds band → re-hedge to delta-neutral

Example:
SPX 5200 Call, gamma = 0.002
GEX = 0.002 × 5200² × 0.01 = $540.80 per 1% move
Hedge band = $540.80 × 0.50 = ~$270
Delta neutral at entry: Δ = 0.50, short 50 deltas of SPX (via futures or shares)
When Δ moves to 0.50 ± 0.05 (i.e., 0.45 or 0.55): re-hedge
```

### Hedging Frequency

| Market Condition | Hedge Frequency | Band Width |
|-----------------|----------------|------------|
| Normal (VIX 15-20) | Every 15-30 min | GEX × 0.50 |
| Active (VIX 20-30) | Every 5-15 min | GEX × 0.75 (wider — more noise) |
| Extreme (VIX > 30) | Every 1-5 min | GEX × 1.00 (wider — spreads widen, re-hedging cost rises) |
| FOMC / Data Release | Do NOT scalp through events. Close before, reopen after | N/A — flat through events |

### Hedging Instrument Selection

| Instrument | Best For | Pros | Cons |
|-----------|----------|------|------|
| /ES futures | SPX options | No borrow cost, tight spread, 24h (almost) | Contract size ($50 × index) may be too large for small positions |
| /MES futures | SPX options (small) | 1/10 size of /ES, accessible for smaller accounts | Slightly wider spreads than /ES |
| SPY shares | SPY options | Easy, fractional shares possible | Borrow cost for shorts, settlement time |
| SPX box spreads | Synthetic short/long stock | No borrow cost, cash-settled | Complex to execute and manage |

## Gamma Scalping P&L Accounting

Track these components separately:

```
1. Option P&L: Change in option price (mark-to-market)
2. Hedge P&L: Profit/loss from delta hedge trades
3. Theta cost: Time decay on the option position
4. Transaction costs: Commissions + spread crossing on hedges

Net gamma scalp P&L = Option P&L + Hedge P&L
Net strategy P&L = Net gamma scalp P&L - Theta cost - Transaction costs
```

[COMMON-PRACTICE] Many traders mistakenly attribute hedge profits to "skill" when they're really just delta-neutralizing a winning directional bet. True gamma scalping requires the hedge P&L to EXCEED theta decay AFTER transaction costs.

## Breakeven Math

[COMPUTED] For an ATM straddle to break even via gamma scalping:

```
Required daily realized move > daily implied move × 1.05 (5% buffer for transaction costs)

SPX 1-Day ATM Straddle, IV=15%:
Daily implied move ≈ 15% / √252 = 0.94%
Daily realized move needed for breakeven: 0.99%+

Historical SPX daily moves:
Average: 0.75% (below breakeven — gamma scalping loses in normal markets)
> 1%: occurs ~30% of trading days
> 2%: occurs ~5% of trading days
```

**Key insight:** Gamma scalping at-the-money options in normal markets is a losing strategy. The theta cost exceeds realized volatility capture. It ONLY works when realized volatility significantly exceeds implied.

## The Real Edge in Gamma Scalping

[BACKTEST-EVIDENCE] From the Trading project data and published research:

1. **Post-event vol crush scalp:** After FOMC/CPI, implied vol drops but realized vol stays elevated for 30-60 minutes. Buy straddles AFTER the event when IV has already fallen, scalp the post-event realized vol.
2. **Opening range gamma scalp:** First 30 minutes after the open have the highest realized/implied vol ratio. Enter at 9:35, close by 10:30.
3. **Fade-the-gap scalp:** After a large opening gap (>1%), IV typically overshoots. Sell the straddle (short gamma — the reverse scalp) as IV mean-reverts.
4. **Volatility clustering:** High-vol days cluster. If yesterday's realized vol > implied, today is more likely to have elevated realized vol. Yesterday's vol ratio predicts today's scalp-ability.

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Gamma scalping with too-small gamma → costs exceed profits | Minimum gamma: 0.0005 (50 SPX points per 1% move). Below this, transaction costs dominate |
| Hedging every tick → paying spread 50+ times/day | Use hedge bands. Each cross costs ~0.5-1 tick. Limit to 5-15 hedges per day |
| Scalping when IV > HV → negative expected value | Only scalp when IV < HV. This is the fundamental edge condition |
| Ignoring gamma asymmetry (OTM vs ITM vs ATM) | ATM gamma is highest. At 1% OTM, gamma is ~70% of ATM. At 2% OTM, ~40% |
| Holding gamma through 3:00 PM → gamma explosion | Close all gamma scalps by 2:30 PM minimum. 3:00 PM+ gamma is unhedgeable |
| Not accounting for vega P&L in "gamma scalp" attribution | If IV also changes, option P&L contains both gamma AND vega components. Decompose before claiming scalp success |

## Provenance

[VERIFIED] Gamma scalping P&L approximation from Carr & Madan (1998) and standard options theory. Realized vol > implied vol is the necessary condition for positive scalp P&L.
[COMPUTED] GEX formula and hedge band calculations. Daily implied move = IV / √252.
[BACKTEST-EVIDENCE] Post-event vol crush pattern and opening range realized/implied ratio from Trading project data and published research.
[COMMON-PRACTICE] Hedge band method from professional options market making desks.
[AS OF 2026-07]
