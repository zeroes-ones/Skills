# Carry Trade Framework

## The Core Question

"Given interest rate differential X and daily volatility Y, how many days of positive carry does it take to offset a 1-standard-deviation adverse move?"

If carry can't offset a 1σ move in a reasonable holding period, the trade is negative expected value.

## Carry Return Computation

```
Annual Carry Return = Long Currency Rate - Short Currency Rate
Daily Carry Return = Annual Carry Return / 365
Daily Swap (pips) = (Notional × Daily Carry Return) / Pip Value
```

### Example: Long AUD/JPY
```
AUD rate: 4.35%
JPY rate: 0.25%
Annual carry: +4.10%
Daily carry: 4.10% / 365 = 0.01123%

On 1 standard lot ($100K equivalent): $100,000 × 0.0001123 = $11.23/day carry earned
```

## Break-Even Analysis

### Formula
```
Days to Offset 1σ = (1σ Daily Move %) / (Daily Carry %)
```

| Pair | Long Currency Rate | Short Currency Rate | Annual Carry | Daily Vol (1σ) | Days to Offset 1σ | Viable? |
|------|-------------------|--------------------|-------------|----------------|-------------------|---------|
| AUD/JPY | 4.35% | 0.25% | +4.10% | 0.55% | 49 days | ⚠️ Marginal — needs 7+ weeks |
| NZD/JPY | 4.25% | 0.25% | +4.00% | 0.60% | 55 days | ❌ Too slow |
| USD/MXN | 5.25% | 9.50% | -4.25% | 1.40% | Short: 120 days | ❌ Negative carry + high vol |
| USD/TRY | 5.25% | 50.00% | -44.75% | 2.50% | Short: 2 days! | ⚠️ Carry attractive but crash risk extreme |
| USD/ZAR | 5.25% | 8.25% | -3.00% | 1.20% | Short: 146 days | ❌ Carry too small vs vol |
| EUR/TRY | 3.75% | 50.00% | -46.25% | 2.50% | Short: 2 days | ⚠️ Same as USD/TRY — political risk |
| GBP/JPY | 5.00% | 0.25% | +4.75% | 0.65% | 50 days | ⚠️ Marginal |

## Negative Carry Trade Rules

When shorting a high-yield currency (short TRY, short ZAR):
1. **The carry is AGAINST you.** Every day you hold, you pay swap.
2. **The trade MUST have a catalyst.** You're not collecting carry — you're betting on a currency collapse.
3. **Time decay is real.** At -44.75% annual carry, holding 1 month costs -3.7% of notional.
4. **Maximum hold: 90 days.** If the collapse hasn't happened by then, the trade thesis is wrong.
5. **Size at 25% of normal.** The carry cost plus gap risk is double the risk of a positive-carry trade.

## Swap Rate Comparison Checklist

Before entering any carry trade held >1 week:
- [ ] Check swap rates at 3+ brokers
- [ ] Confirm swap direction (long = earn? or long = pay?)
- [ ] Verify Islamic/swap-free account availability
- [ ] Compute total swap cost over expected holding period
- [ ] Confirm swap < 20% of expected profit

