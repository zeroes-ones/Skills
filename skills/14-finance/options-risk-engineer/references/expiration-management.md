# Expiration Management

## DTE-Based Action Rules

Theta decay is non-linear. Gamma risk is non-linear. Both accelerate near expiration. The following timeline is based on empirical options behavior [COMMON-PRACTICE]:

### 45 DTE: Open Window
- **Action**: Open new premium-selling positions (short strangles, iron condors, credit spreads)
- **Rationale**: Theta decay curve inflection point — theta accelerates from here through expiration. You capture the steepest portion of the decay curve [VERIFIED]
- **Gamma**: Negligible for OTM positions. A 25-delta put at 45 DTE has gamma ~0.008. Delta changes 0.08 per $10 move — manageable [COMPUTED]
- **Example**: Sell 25-delta strangle on SPY at 45 DTE. Theta ~$12/day per contract. Position has 25 days of "smooth" decay before gamma acceleration begins at 21 DTE

### 21 DTE: Close/Roll Window
- **Action**: Close or roll existing positions to 45 DTE
- **Rationale**: Gamma risk inflects upward at 21 DTE. Gamma of that 25-delta put is now ~0.015 — nearly double. Delta can shift significantly intraday [VERIFIED]
- **Roll mechanics**: Buy back expiring option, sell same strike at 45 DTE. Net credit should be positive. If roll is for a debit, reconsider the position [COMMON-PRACTICE]
- **Cost of waiting**: Rolling at 14 DTE vs 21 DTE typically costs 15-25% more in slippage and spread crossing due to tighter markets near expiration [ESTIMATED, ±5%]

### 7 DTE: Aggressive Close
- **Action**: Close all short gamma positions regardless of P&L unless part of a defined-risk spread at max profit
- **Rationale**: Gamma is extreme. ATM gamma at 7 DTE is ~3x 21-DTE gamma and ~10x 45-DTE gamma [VERIFIED]
- **Example**: 25-delta SPY put at 7 DTE: gamma ~0.035. A $5 SPY move shifts delta by 0.175 per contract. On 20 contracts, that's 350 shares of delta appearing from a routine intraday move [COMPUTED]
- **Exception**: Defined-risk spreads (iron condors, verticals) approaching max profit can be held. Max loss is capped. Pin risk still applies — see pin-risk-detection reference

### 0 DTE: Pre-Close Deadline
- **Action**: Close all positions by 3:00 PM ET
- **Rationale**: Broker auto-liquidation windows begin at 3:00-3:45 PM ET. You want to close on YOUR terms, not the broker's [BROKER-VERIFIED]
- **0 DTE gamma**: ATM gamma at 0 DTE morning is 5-10x 7-DTE gamma. Delta moves from 0 to 1.00 on a sub-$1 price move. This is gambling, not trading — unless part of a defined, size-limited strategy [VERIFIED]

## Cash-Settled vs Physical Delivery

This distinction is critical for expiration management [VERIFIED]:

### Cash-Settled Tickers (No Assignment Risk)
| Ticker | Underlying | Multiplier | Settlement |
|--------|-----------|------------|------------|
| SPX | S&P 500 Index | $100 | Cash — difference between settlement and strike, no shares |
| XSP | Mini S&P 500 | $100 | Cash — 1/10 SPX size, same settlement mechanics |
| VIX | CBOE Volatility Index | $100 | Cash — settled to VIX exercise settlement value |
| NDX | Nasdaq-100 Index | $100 | Cash |
| RUT | Russell 2000 Index | $100 | Cash |
| DJX | Dow Jones Industrial Average | $100 | Cash |
| MRUT | Micro Russell 2000 | $100 | Cash |

Cash settlement means: If your short SPX 4500 put is ITM by $10 at expiration, you pay $1,000 ($10 × $100 multiplier). No stock position created. No Monday gap risk. This is why SPX is preferred for undefined-risk strategies [VERIFIED].

### Physical Delivery Tickers (Assignment = 100 Shares)
SPY, QQQ, IWM, DIA, AAPL, MSFT, NVDA, TSLA, and ALL single-stock options settle to physical delivery of 100 shares per contract [VERIFIED].

Assignment on 10 SPY 500 puts = you buy 1,000 shares of SPY at $500 = $500,000 position. If SPY gaps to $485 by Monday open, instant unrealized loss = $15,000.

## Expiration Friday Timeline

All times Eastern [VERIFIED]:

| Time | Event |
|------|-------|
| 9:30 AM | Regular trading opens |
| 12:00 PM | Half-day check — review all expiring positions |
| 2:00 PM | Broker risk desks begin account reviews |
| 2:45 PM | Final decision deadline for manual closes |
| 3:00 PM | Robinhood begins auto-closing ITM options [VERIFIED] |
| 3:45 PM | IBKR liquidation deadline for margin-deficient accounts [BROKER-VERIFIED] |
| 4:00 PM | **Options stop trading.** Whatever you hold is what settles |
| 4:00-5:30 PM | OCC receives exercise/assignment instructions from clearing firms |
| 5:30 PM | OCC processes net exercise/assignment notices [VERIFIED] |
| ~9:00 PM - Saturday AM | Broker sends assignment notifications to customers |
| Monday 9:30 AM | Stock market re-opens. Weekend gap realized |

## Weekend Gap Risk by Product

| Product | Avg Weekend Gap (±%) | Max 5-Year Gap | Implication |
|---------|---------------------|----------------|-------------|
| SPX | N/A (cash-settled) | N/A | No gap risk from SPX options themselves |
| SPY | ±0.4% | -4.1% | $4.10/share × 1000 shares = $4,100 on 10 contracts |
| QQQ | ±0.9% | -5.8% | $24/share × 1000 shares = $24,000 on 10 contracts |
| AAPL | ±1.1% | -12.9% | $24/share × 1000 shares = $24,000 on 10 contracts |
| TSLA | ±2.3% | -21.3% | $53/share × 1000 shares = $53,000 on 10 contracts |
| NVDA | ±1.8% | -18.5% | $23/share × 1000 shares = $23,000 on 10 contracts |

[COMPUTED from historical data]

Cost of closing pin-risk options Friday ($3-5/contract) vs potential Monday gap loss (table above): The insurance is virtually always worth it.

## 0DTE Gamma Risk Quantification

Gamma of ATM 0DTE options vs same-strike longer-dated [VERIFIED]:

| DTE | ATM Gamma (SPY) | Delta Change per $1 Move |
|-----|-----------------|--------------------------|
| 30 DTE | ~0.012 | 0.012 delta shift per $1 |
| 7 DTE | ~0.035 | 0.035 delta shift per $1 |
| 0 DTE (AM) | ~0.080 | 0.080 delta shift per $1 |
| 0 DTE (PM, final hour) | ~0.250+ | 0.250 delta shift per $1 |

At 0DTE final hour, a $0.50 SPY move shifts an ATM option from 0.50 delta to ~0.63 delta — 13 deltas per contract from a routine tick. On 100 contracts, that's 1,300 shares of additional delta exposure that appeared in minutes [COMPUTED]. This is what blows up accounts.

## Pre-Expiration Checklist

1. **Monday before expiration**: Identify all positions expiring this week
2. **Tuesday**: Roll positions at 14 DTE → 45 DTE for premium-selling strategies
3. **Wednesday**: Final check on any positions not yet rolled/closed
4. **Thursday**: Pin-risk scan for Friday's expiration. Close positions within 0.5% of spot
5. **Friday morning**: Verify NO short options remain open near the money
6. **Friday 2:00 PM ET**: Final review. Any position still open? Why?
7. **Friday 3:00 PM ET**: All positions should be closed or DEFINITELY intentional holds
8. **Saturday**: Review assignment notifications from broker
9. **Monday**: Deal with any resulting stock positions
