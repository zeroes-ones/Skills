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
- **Rationale**: Gamma is extreme, and its scaling is fixed: ATM gamma obeys **Γ ∝ 1/√T**, so at 7 DTE it is √(21/7) = **1.73×** its 21-DTE value and √(45/7) = **2.54×** its 45-DTE value [COMPUTED]. (The "~3× vs 21-DTE and ~10× vs 45-DTE" figures printed in earlier editions were wrong; they imply ∝ 1/T, which contradicts the Black–Scholes identity `Θ ≈ −½·Γ·S²σ²` stated in `portfolio-greeks-aggregation.md`.)
- **Example**: a 25-delta SPY put at 7 DTE carries gamma ≈ 0.023 per share (Γ = φ(d1)/(Sσ√T) with S = $500, σ = 20%, K ≈ $549): a $5 SPY move shifts delta by 2.30 Δshares per $1 per contract, i.e. 11.5 shares on one contract. On 20 contracts that is ~230 shares of delta appearing from a routine intraday move [COMPUTED]
- **Exception**: Defined-risk spreads (iron condors, verticals) approaching max profit can be held. Max loss is capped. Pin risk still applies — see pin-risk-detection reference

### 0 DTE: Pre-Close Deadline
- **Action**: Close all positions by **2:45 PM ET (14:45)**, with a **3:00 PM ET (15:00) hard stop** — the same clock `intraday-options-trader` publishes for 0DTE
- **Rationale**: Broker auto-liquidation windows begin at 3:00-3:45 PM ET, and a 0DTE position cannot be worked after its close. You want to close on YOUR terms, not the broker's [BROKER-VERIFIED — broker-specific and subject to change; re-read your own broker's rule]
- **0 DTE gamma**: Γ ∝ 1/√T, and the reduced form diverges as T → 0, so the multiple depends entirely on how much of the *session* is left rather than on a fixed number of days: with half a session remaining it is √(7/0.5) ≈ **3.7×** the 7-DTE value, and it keeps rising as the session shortens. That is exactly why the 0DTE bucket is managed by the **clock** (14:45 close / 15:00 hard stop) and not by a gamma multiple. Delta moves from 0 to 1.00 on a sub-$1 price move. This is gambling, not trading — unless part of a defined, size-limited strategy [COMPUTED]

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

| Product (reference price) | Avg weekend gap (±1σ) | Max 5-year weekend gap | Exposure on 10 contracts (1,000 shares) |
|---------|---------------------|----------------|-------------|
| SPX | N/A (cash-settled) | N/A | No gap risk from SPX options themselves |
| SPY ($500) | ±0.5% | −4.1% (Mar 2020) | 4.1% × $500 = $20.50/share × 1,000 = **$20,500** |
| QQQ ($415) | ±1.0% | −5.8% (Mar 2020) | $24.07/share × 1,000 = $24,070 |
| AAPL ($186) | ±1.2% | −12.9% (Mar 2020) | $24.00/share × 1,000 = $24,000 |
| TSLA ($249) | ±2.5% | −21.3% (Mar 2020) | $53.04/share × 1,000 = $53,040 |
| NVDA ($124) | ±1.8% | −18.5% (Mar 2020) | $22.94/share × 1,000 = $22,940 |

[ESTIMATED ±30% — the ±1σ column is a desk estimate of the *typical* weekend gap, not a fitted
distribution; the max-gap column names the episode it is drawn from. The two tables that state this
band (`pin-risk-detection.md` and here) are the same numbers by construction: change one, change
both. Re-measure from your own venue's data before sizing off either.]

Cost of closing pin-risk options Friday ($3-5/contract [ESTIMATED ±40%]) vs potential Monday gap loss (table above): The insurance is virtually always worth it.

## 0DTE Gamma Risk Quantification

ATM gamma scales as **Γ ∝ 1/√T**; the tabulated levels below are illustrative desk values
[ESTIMATED ±30%] for a ~$500 underlying at ~20% IV, anchored at 0.012 at 30 DTE, with the *scaling*
between rows computed from that rule:

| DTE | ATM Γ (per share, per $1) | Δdelta-shares per $1, per contract |
|-----|-----------------|--------------------------|
| 30 DTE | 0.012 | 1.2 |
| 7 DTE | 0.025 | 2.5 |
| 0 DTE (AM, ~half a session left) | 0.093 | 9.3 |
| 0 DTE (PM, final hour) | 0.237 | 23.7 |

At 0DTE final hour, a $0.50 SPY move shifts an ATM option from 0.50 delta to ~0.62 delta — ~12 delta
shares per contract from a routine tick. On 100 contracts, that's ~1,200 shares of additional delta
exposure that appeared in minutes [COMPUTED]. This is what blows up accounts. (The earlier edition's
rows — 0.035 at 7 DTE and 0.080 at 0DTE — were inconsistent with Γ ∝ 1/√T; the ratios there implied
Γ ∝ 1/T. If you re-anchor the table, re-scale every row by √(old anchor / new anchor).)

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

