# Swap/Rollover Mechanics

## The 5:00 PM ET Cutoff

FX spot trades settle T+2. At 5:00 PM ET New York, ALL open positions are "rolled" — the broker closes your position at the day's value date and reopens it for the next value date. The interest rate differential between the two currencies is credited/debited at this time.

**Critical:** This is NOT prorated. A position held for 1 minute past 5:00 PM ET pays/receives the full day's swap. Close at 4:59 PM = no swap. Close at 5:01 PM = full day swap.

## Triple Swap Wednesday

FX spot settlement is T+2. On Wednesday at 5 PM ET, the settlement date becomes Monday (T+2 from Wednesday = Friday, but +2 from settlement perspective). The position must be rolled to Tuesday's value date, requiring 3 days of swap (Saturday, Sunday, Monday).

**Result:** Wednesday rollover = 3× normal swap. This also applies on the last trading day before any multi-day holiday (Christmas, New Year, etc.).

## Swap Rate Determination

```
Swap = (Long Currency Overnight Rate - Short Currency Overnight Rate) × Notional / 365
     + Broker Markup (typically 0.25-1.00% of the rate differential)
```

Brokers set their own swap rates based on:
1. Interbank tom-next rates
2. Their funding costs in each currency
3. Their desired markup (varies wildly by broker)

## Broker Swap Comparison (Example Rates)

| Broker | Long AUD/JPY (1 lot) | Long EUR/USD (1 lot) | Long USD/TRY (1 lot) | Notes |
|--------|---------------------|---------------------|---------------------|-------|
| OANDA | +$8.20/day | -$7.50/day | -$55/day | Transparent rate calculation |
| IG | +$6.80/day | -$8.00/day | -$60/day | Wider markup on exotics |
| FXCM | +$4.50/day | -$9.00/day | -$70/day | Known for poor swap rates |
| IBKR | ~benchmark + 0.5% | ~benchmark + 0.5% | ~benchmark + 0.5% | Most competitive, transparent |
| Pepperstone | +$7.50/day | -$8.00/day | Swap-free only | Offers swap-free accounts |

**Variance:** Up to $3.70/day difference on the same trade between cheapest and most expensive broker. Over 3 months = $333 difference per standard lot.

## Islamic/Swap-Free Accounts

Available at most brokers. How they work:
- No swap credited or debited
- Instead, the broker charges a fixed "admin fee" per lot per night (typically $5-10)
- Or widens the spread on entry/exit
- Good for: multi-week holds, avoiding triple swap, avoiding negative carry on shorts
- Bad for: positive carry trades (you lose the swap income), scalping (wider spreads)

## Rollover Timing by Broker (ET)

| Broker | Rollover Time (ET) | Cutoff to Avoid Swap | Triple Day |
|--------|-------------------|---------------------|------------|
| OANDA | 5:00 PM | 4:59 PM | Wednesday |
| IG | 5:00 PM | 4:45 PM (15 min early!) | Wednesday |
| FXCM | 5:00 PM | 5:00 PM (no grace) | Wednesday |
| IBKR | 5:00 PM | 4:59 PM | Wednesday |
| Pepperstone | 5:00 PM | 4:59 PM | Wednesday |
| FOREX.com | 5:00 PM | 4:55 PM (5 min early) | Wednesday |

Some brokers close rollover at 4:45 PM to process. Check your specific broker.

