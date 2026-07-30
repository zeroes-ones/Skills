# Hedging with Options

## Protective Puts: Cost and Construction

A protective put is long stock + long OTM put. It caps downside at the put strike while preserving upside participation (minus premium cost).

### Cost Quantification
5% OTM put on a stock position costs approximately 1-2% of position value per year, depending on volatility [ESTIMATED ±0.3%].

| Underlying | 5% OTM Put (30 DTE) | Annualized Cost (% of position) | Notes |
|------------|---------------------|--------------------------------|-------|
| SPY | ~0.12% per month | ~1.4% | Low IV reduces cost |
| QQQ | ~0.18% per month | ~2.2% | Higher IV = costlier protection |
| AAPL | ~0.15% per month | ~1.8% | Moderate IV |
| TSLA | ~0.40% per month | ~4.8% | High IV makes puts expensive |

[ESTIMATED at typical IV levels, actual premium depends on current IV]

### Rolling Mechanics
Before expiration, sell the expiring put and buy the next-month put [COMMON-PRACTICE]:
```
Roll cost = new_put_premium - expiring_put_market_value
```
If SPY rallied, the expiring put is nearly worthless and the roll costs nearly full premium. If SPY dropped, the expiring put has gained value, reducing the roll cost. Rolling at 7-10 DTE captures remaining time value before final decay.

### Put Spread Alternative
Instead of buying a single protective put, buy a 5% OTM put and sell a 10-15% OTM put [COMMON-PRACTICE]:
```
Net cost = long_put_premium - short_put_premium
```
Example: SPY at $500. Buy 475 put for $2.50. Sell 450 put for $1.00. Net cost: $1.50 vs $2.50 for single put — 40% cost reduction [COMPUTED].

Trade-off: Protection ends at the short strike (450). Below 450, the position loses $1 for every $1 drop, same as unhedged. Above 475, you lose only the net premium. Between 450 and 475, the short put partially offsets gains from the long put.

## Collar: Zero-Cost Construction

Collar = long stock + buy OTM put + sell OTM call [COMMON-PRACTICE]:
```
net_cost = put_premium - call_premium
target: net_cost ≈ 0  (zero-cost collar)
```

Construction algorithm:
1. Select put strike for desired floor (e.g., 5% OTM)
2. Find call strike whose premium exactly offsets the put premium
3. If no exact match, accept small debit or credit

Example: XYZ at $100. 95-strike put costs $2.00. Find call strike where premium = $2.00. If 108-strike call = $2.00, collar bounds: floor at $95, cap at $108. Zero net cost [COMPUTED].

### Collar Drawbacks
- Upside is capped at the call strike. A stock that rallies 30% only delivers 8% gains (to the cap)
- Put-call parity: zero-cost collars are mathematically equivalent to a box spread. The risk-free rate is embedded in the pricing [INFERRED]
- Early exercise risk on the short call near dividends (see pin-risk-detection reference)

## Tail Hedge Sizing

Tail hedging allocates a small portion of portfolio to deeply OTM options that pay off massively in crashes [COMMON-PRACTICE]:

### Allocation and Construction
- **Allocation**: 1-2% of portfolio value per year to OTM put premiums
- **Strike selection**: 30-40 delta below current price (typically 25-35% OTM on SPX)
- **Expiration**: 3-6 months out, rolled quarterly
- **Sizing rule**: Position should pay off 100%+ of portfolio drawdown at the strike

### Real-World Reference: Universa Investments
Universa's tail hedge strategy returned +4,144% in March 2020. SPX fell 34%, Universa's tail hedge fund returned +4,144%, offsetting equity losses in client portfolios [VERIFIED]. Key insight: the fund did NOT produce returns in calm markets. It was a persistent 1-2% annual drag that paid off in a single month.

### DIY Tail Hedge Cost
Portfolio: $1,000,000. Annual tail hedge budget: $10,000-$20,000 (1-2%). Buy 30-delta SPX puts quarterly. At $10,000/quarter, you can buy approximately 2-3 SPX 30-delta put spreads per quarter (depending on current VIX). In March 2020, a $10,000 quarterly allocation in Jan 2020 SPX puts would have been worth $150,000-$200,000 at the trough [ESTIMATED, ±25%].

## Delta Hedging Mechanics

To neutralize directional risk on an option position:
```
shares_to_sell = delta × position_size × 100
```
A long 10-contract 0.45-delta call = +450 delta. Sell 450 shares to hedge. Portfolio is now delta-neutral [COMPUTED].

### Rebalancing Frequency
Gamma causes delta to change as price moves, requiring rebalancing:
- **Continuous**: Infinitely frequent rebalancing = perfect hedge but infinite transaction costs. Theoretical ideal only.
- **Intraday**: Rebalance when delta shifts > 0.10 per contract. Balances hedge accuracy with costs.
- **Daily**: Rebalance at close. Enough for positions with gamma ≤ 0.02 per contract.
- **Weekly**: Only for very low-gamma positions (≤ 0.005 gamma, deep OTM or far-dated).

### Cost of Delta Hedging
```
cost_per_year = trades_per_day × days_per_year × shares_per_trade × slippage_per_share
```
Example: 2 rebalances/day × 252 days × 500 shares × $0.01 slippage = $2,520/year drag on a $100,000 position = 2.52% annual slippage cost [COMPUTED]. This is the hidden cost of delta-hedging actively managed option positions.

## Correlation Breakdown During Crashes

Hedges that rely on correlation fail during crashes when correlation breaks [VERIFIED]:

| Hedge | Calm Correlation | Crash Correlation | Effective Protection |
|-------|-----------------|-------------------|---------------------|
| VIX calls vs SPX | -0.95 | -0.60 | 63% of expected in crash |
| Long treasuries (TLT) vs SPX | -0.40 | -0.55 | 138% of expected (positive surprise) |
| Gold (GLD) vs SPX | -0.15 | +0.20 | Negative — gold sells off with stocks in liquidity crises |
| Yen (FXY) vs SPX | -0.20 | -0.40 | 200% of expected — yen is the classic risk-off currency |

Example: You expect your VIX call hedge to pay $10,000 when SPX drops 10%. In the crash, correlation weakens and you only get $6,300. Your portfolio is $3,700 under-hedged [COMPUTED].

## Diversified Hedge Portfolio

The only reliable multi-crash hedge allocation [COMMON-PRACTICE]:
- **40% VIX calls / VIX futures**: Directly hedges volatility spike
- **30% SPX puts**: Directly hedges price decline, regardless of correlation
- **20% Long treasury calls (TLT/IEF)**: Rate-cut beneficiary during crashes
- **10% Cash**: Dry powder for opportunistic deployment during dislocations

This 3-pronged hedge covers the three crisis drivers: vol spikes (VIX), price declines (SPX puts), and rate responses (treasuries). No single hedge is sufficient because no single driver is guaranteed [INFERRED from historical crisis analysis].

## Hedge Monitoring Cadence

- **Daily**: Check net delta. Has the hedge coverage ratio changed?
- **Weekly**: Recalculate hedge cost vs portfolio value. Has the drag increased?
- **Monthly**: Evaluate hedge performance on backtested scenarios. Adjust allocation if regime changed.
- **Quarterly**: Full hedge review. Roll expiring hedges. Rebalance across hedge instruments.
