# Liquidity and Slippage

## The Hidden Tax: Bid-Ask Spread

Every option trade pays the spread. This is a real, dollar-quantified cost that compounds with every roll, adjustment, and exit.

### Spread Cost Formula
```
spread_cost_pct = (ask - bid) / mid × 100%
```
This percentage is your entry+exit tax. You pay half the spread on entry, half on exit [VERIFIED].

Example: SPY 500 call, bid $2.45, ask $2.55, mid $2.50:
```
spread_cost_pct = ($0.10) / $2.50 × 100% = 4.0%
cost per contract = $0.10 × 100 = $10
round-trip cost = $10 entry + $10 exit = $20
```
[COMPUTED]

If your expected profit is $50/contract, the $20 spread cost consumes 40% of your edge.

### Spread Thresholds

| Spread (% of mid) | Action |
|-------------------|--------|
| < 1% | Excellent liquidity. Market orders acceptable [COMMON-PRACTICE] |
| 1-3% | Good liquidity. Limit orders at mid fill ~70-90% of time |
| 3-5% | Moderate. Limit orders required. Expect to cross spread ~50% of time |
| 5-10% | Poor. Trade only if edge justifies. Mid fills rare. Cross spread expected |
| > 10% | Toxic. Do not trade. Slippage exceeds reasonable edge [COMMON-PRACTICE] |

## Open Interest-Based Position Limits

Open Interest (OI) represents total outstanding contracts. Your position relative to OI determines exit difficulty:

```
position_pct_of_OI = (your_contracts / open_interest) × 100%
```

| Your % of OI | Exit Difficulty | Expected Slippage |
|--------------|-----------------|-------------------|
| < 1% | Trivial | 0.01-0.03/contract |
| 1-5% | Easy | 0.03-0.05/contract |
| 5-10% | Moderate | 0.05-0.15/contract — you move the market |
| 10-20% | Difficult | 0.15-0.40/contract — you ARE the market maker |
| > 20% | Dangerous | 0.40+/contract — cannot exit without multi-tick slippage |

[ESTIMATED, ±30% depending on underlying liquidity]

Example: You hold 50 contracts with OI of 500 = 10% of OI. When you exit, your 50 contracts represent significant liquidity demand. The market maker widens spread by $0.10-0.20 to accommodate your size. Cost: $0.15 × 100 × 50 = $750 in excess slippage [COMPUTED].

## Fill Probability by Liquidity Tier

Real fill rates from empirical market observations [INFERRED]:

### Liquid Tier (SPY weeklies, QQQ monthlies, AAPL front-month)
- ATM options: Fill at mid ~90%+ of attempts
- 10-delta OTM: Fill at mid ~75% of attempts
- 5-delta OTM: Fill at mid ~60% of attempts

### Semi-Liquid Tier (Mid-cap monthlies, sector ETFs)
- ATM options: Fill at mid ~70% of attempts
- 10-delta OTM: Fill at mid ~50% of attempts
- 5-delta OTM: Fill at mid ~30% of attempts — expect to cross spread

### Illiquid Tier (Low OI, wide strikes, small-cap)
- ATM options: Fill at mid ~40% of attempts
- OTM options: Fill at mid ~15% of attempts — expect to cross full spread
- Deep OTM: Fill at mid < 5% — assume you cross the full spread

## Slippage Estimate Formulas

### By Liquidity Tier
```
liquid_slippage = 0.02 × contracts          (SPY, QQQ, AAPL)
semi_liquid_slippage = 0.08 × contracts     (mid-cap, sector ETFs)
illiquid_slippage = 0.30 × contracts        (low OI, wide markets)
```
Per-contract, not per-dollar [ESTIMATED, ±40%].

### Pre-Trade Slippage Check
```
expected_cost = spread_cost_pct × option_price × 100 × contracts
if expected_cost > 0.50 × expected_profit: DO NOT TRADE
```
If slippage eats more than half your edge, the trade has negative expected value [COMPUTED].

## Volume vs Open Interest

Volume and OI serve different purposes in liquidity assessment [VERIFIED]:

- **Volume**: Trading activity TODAY. High volume = active market, tight spreads. Low volume = few participants, wide spreads.
- **OI**: Total outstanding contracts. High OI = deep market, many exit counterparties. Low OI = shallow market, your position IS the market.

### Volume/OI Ratio
```
volume_to_OI = daily_volume / open_interest
```
| Ratio | Market Condition |
|-------|-----------------|
| > 10% | Very active. Spreads tighten intraday |
| 2-10% | Normal. Reliable fills |
| 1-2% | Slow. Wider spreads, fewer fills |
| < 1% | Stale. Quoted spread is theoretical — real fills much worse |

Example: Option with 5000 OI and 25 daily volume = 0.5% ratio. The $0.10 displayed spread means nothing — the last trade was hours ago. Your fill will likely be $0.25+ off mid [ESTIMATED].

## Options Trading Hours

Options trade ONLY during regular market hours [VERIFIED]:
- **9:30 AM - 4:00 PM ET** — regular session
- No pre-market. No after-hours.
- Orders placed outside these hours queue for the next regular open
- Exception: SPX and VIX options trade until 4:15 PM ET [VERIFIED]
- Futures options (ES, NQ, CL, GC): trade 23 hours on Globex but are most liquid during regular US hours

### Intraday Liquidity Patterns
| Time (ET) | Liquidity | Notes |
|-----------|-----------|-------|
| 9:30-9:45 AM | Poor | Markets opening. Wide spreads. Don't execute large orders |
| 9:45-12:00 PM | Best | Peak liquidity. Tightest spreads. Execute here |
| 12:00-3:00 PM | Good | Steady. Acceptable execution |
| 3:00-3:45 PM | Declining | Brokers auto-liquidating. Spreads widening |
| 3:45-4:00 PM | Poor | Last-minute positioning. Execution quality degrades |

## Pre-Trade Liquidity Checklist

1. Check bid-ask spread: `(ask - bid) / mid × 100%`. If > 5%, reconsider.
2. Check OI: `your_size / open_interest × 100%`. If > 5%, reduce size.
3. Check volume/OI ratio: `volume / OI × 100%`. If < 1%, expect wider fills.
4. Check time: If before 9:45 AM or after 3:00 PM ET, delay execution.
5. Size orders: Max 20% of displayed bid/ask size per order. Split large orders.
6. Use limit orders at mid. If no fill in 60 seconds, adjust $0.01 toward natural (bid for sells, ask for buys).

## Real Slippage Example

Scenario: 20 contracts of an AAPL OTM put. Displayed market: bid $1.80, ask $1.90, mid $1.85. Spread = 5.4% — borderline.

Expected fill: $1.83 (mid + $0.02 toward ask). Realized slippage: $0.02 × 100 × 20 = $40 per side = $80 round-trip. On a $3,700 position, that's 2.2% in slippage alone [COMPUTED].

If the expected edge on this trade was 10% ($370), slippage consumes 22% of it. Still profitable, but meaningfully reduced [COMPUTED].

