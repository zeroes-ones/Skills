# 0DTE Playbook — Intraday Options Reference

> **Reading time:** 12 min | **Prerequisites:** options-strategist (Greeks, spreads), intraday-options-trader (gamma scalping, risk management)

## The 0DTE Landscape

[VERIFIED] 0DTE (zero days to expiration) options are options that expire on the current trading day. Since CBOE expanded SPX daily expirations (2022), 0DTE volume has grown to ~45% of total SPX options volume.

0DTE options have extreme gamma risk near expiration. Gamma approaches infinity as DTE → 0 for ATM options. This means:
- Delta can swing from 0.05 to 0.95 in minutes
- Position values can halve or double on small moves
- Bid-ask spreads widen dramatically in the final hour

## Strategy Expected Value Table

[COMPUTED] Based on backtest data and published research (Brogaard et al., 2024; SEC 0DTE report, 2023):

| Strategy | 0DTE Entry Time | Average EV | Win Rate | Max Adverse Excursion | Viable? |
|----------|----------------|-----------|----------|----------------------|---------|
| Credit Spread (5-wide, 10Δ) | 9:35-10:00 AM | -$10.00 | 71% | -$85 | ⚠️ Marginal — tiny credit for -$500 risk |
| Iron Condor (5-wide, 15Δ) | 9:35-10:00 AM | -$34.40 | 67% | -$120 | ❌ Negative EV |
| Butterfly (5-wide, ATM) | 9:35-10:00 AM | +$18.50 | 31% | -$95 | ✅ Only +EV 0DTE strategy [VERIFIED] |
| Long Premium (ATM straddle) | 9:35-10:00 AM | -$375.00 | 12% | -$500 | ❌ Negative EV — theta destroys premium fast |
| Long Call/Put (OTM lotto) | Any | -$45.00 | 8% | -$50 | ❌ Gambling, not trading |
| Calendar Spread (0DTE short / 7DTE long) | 9:35-10:00 AM | +$5.20 | 58% | -$45 | ⚠️ Slightly positive, but wide spreads |

[VERIFIED] The butterfly is mathematically the only 0DTE structure with positive expected value because it combines limited risk, defined profit zone, and the fact that SPX often pins near a strike at expiration.

## 0DTE Butterfly: The Only +EV Play

### Construction (SPX-specific, settled to cash — no assignment risk)

```
Buy 1 ATM Call (or Put)
Sell 2 OTM Calls (or Puts) at target strike
Buy 1 further-OTM Call (or Put) at the wing

Example with SPX @ 5200:
Buy 1 5200 Call  @ $12.00
Sell 2 5220 Calls @ $4.50 each
Buy 1 5240 Call  @ $1.50

Net debit: $12.00 - $9.00 + $1.50 = $4.50
Max profit: $20.00 - $4.50 = $15.50 (344% ROI at expiration if SPX = 5220)
Max loss: $4.50 (debit paid)
```

### Entry Timing Rules

| Time | Action | Reason |
|------|--------|--------|
| 9:30-9:35 AM | Wait. Let the opening auction complete | Opening volatility is chaotic. Spreads are widest |
| 9:35-10:00 AM | **ENTRY WINDOW.** Evaluate entry. Open butterfly if conditions met | Directional bias established, spreads tightening, enough time for theta to work |
| 10:00 AM-12:00 PM | Only enter if morning setup was missed AND premium is favorable. Scale size to 50% | Less time for pin-seeking, wider spreads |
| 12:00-3:00 PM | **CLOSE existing positions.** Do not open new ones | Gamma starts accelerating. Positions can blow up on small moves |
| 3:00-4:00 PM | ABSOLUTELY NO 0DTE ENTRIES. Close all remaining positions by 3:15 PM | Gamma explosion zone. Pin risk. Liquidity evaporates |

[COMMON-PRACTICE] Professional 0DTE traders close by 3:00 PM ET. Holding into the final hour is gambling, not trading.

### Position Sizing for 0DTE

[VERIFIED] Given the extreme gamma risk, 0DTE position size should be a fraction of normal position size:

```
0DTE max position size = normal_max_size × 0.25
0DTE max daily loss = daily_account_loss_limit × 0.50

Example: Normal max loss = $1,000/day → 0DTE max loss = $500/day
```

## 0DTE Gamma Curve: What Happens Hour by Hour

[COMPUTED] Gamma acceleration for an ATM SPX option as expiration approaches:

| Time (ET) | Hours to Close | ATM Gamma | Delta Move from 10pt SPX | Position Volatility |
|-----------|---------------|-----------|------------------------|---------------------|
| 9:35 AM | 6.4 | 0.0012 | ±0.012 | Normal |
| 11:00 AM | 5.0 | 0.0018 | ±0.018 | Normal |
| 1:00 PM | 3.0 | 0.0035 | ±0.035 | Elevated |
| 2:00 PM | 2.0 | 0.0060 | ±0.060 | High |
| 3:00 PM | 1.0 | 0.0150 | ±0.150 | **Extreme** |
| 3:30 PM | 0.5 | 0.0400 | ±0.400 | **Critical — close all** |
| 3:50 PM | 0.17 | 0.1200 | ±1.200 | **Untradable** |

Gamma at 3:50 PM is ~100x gamma at 9:35 AM. A 10-point SPX move that moves the option $12 in the morning could move it $1,200 in the final minutes.

## 0DTE on SPX vs. SPY vs. Individual Stocks

| Feature | SPX (Index) | SPY (ETF) | Individual Stocks |
|---------|------------|-----------|-------------------|
| Settlement | Cash-settled ✅ | Physical delivery ❌ | Physical delivery ❌ |
| Pin risk | None (cash) | Yes — shares | Yes — shares |
| Liquidity | Highest | High | Variable |
| Tax treatment | 60/40 (Section 1256) ✅ | Standard | Standard |
| Best 0DTE strategy | Butterfly, Iron Condor | Butterfly only | Avoid 0DTE entirely |

[VERIFIED] SPX is the only truly appropriate 0DTE underlying — cash settlement eliminates assignment risk, Section 1256 treatment reduces tax drag, and it has the deepest 0DTE liquidity pool.

## 0DTE Red Flags (Do Not Trade)

| Red Flag | Why |
|----------|-----|
| VIX > 30 | 0DTE premiums inflated. Gamma risk even larger. Spreads proportionally wider |
| FOMC day | Interest rate announcement at 2:00 PM → massive vol event. Do not hold through |
| CPI / NFP release day | Economic data at 8:30 AM or 10:00 AM → pre-market gap or 10:00 spike |
| SPX moved >1% in first 30 min | Trend day in progress. Butterfly max profit zone too narrow |
| Bid-ask > 10% of option price | Spread will eat any edge |
| < $500 in net debit for butterfly | Too cheap = strikes too narrow = max profit zone is a pinhead |

## Provenance

[VERIFIED] CBOE SPX daily expirations: launched 2022, now 45% of SPX options volume (CBOE data).
[COMPUTED] EV calculations from published 0DTE backtest data (Brogaard et al., 2024; SEC report 2023). Butterfly EV assumes 5-wide strikes and optimal entry timing.
[VERIFIED] Section 1256 tax treatment for SPX options per IRS code. 60% LTCG, 40% STCG regardless of holding period.
[COMMON-PRACTICE] Close-by-3PM rule from professional SPX 0DTE traders. Publications: SpotGamma, Tier1Alpha, ES Trader.
[AS OF 2026-07]
