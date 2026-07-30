# Margin Requirements for Options Portfolios

## Regulation T (Reg T) Margin

Reg T is the Federal Reserve baseline for retail margin accounts. It applies to all non-Portfolio Margin accounts [VERIFIED].

### Stock Margin
- **Initial margin**: 50% of purchase price
- **Maintenance margin**: 25% of current market value
- **Pattern day trader (PDT)**: $25,000 minimum equity. 4+ day trades in 5 business days triggers PDT designation. Below $25K = account restricted to closing only [VERIFIED]

### Long Options (Reg T)
- Long calls and puts: **100% of premium**. Must be paid in full. No margin lending on long options.
- No maintenance requirement after purchase — maximum loss is premium paid.
- Cash-secured puts: 100% of (strike × 100 × contracts) minus premium received. Cash must be in account.

### Naked Calls (Reg T)
```
Margin = 100% of premium + 20% of underlying price - OTM amount
```
Minimum: premium + 10% of underlying price [VERIFIED].

Example: AAPL at $185, sell 190 strike call for $0.50 credit, 1 contract:
```
Margin = $50 premium + (20% × $18,500) - $500 OTM = $50 + $3,700 - $500 = $3,250
```
[COMPUTED]

### Naked Puts (Reg T)
```
Margin = 100% of premium + 20% of underlying price - OTM amount
```
Minimum: premium + 10% of strike price [VERIFIED].

Example: SPY at $500, sell 480 strike put for $1.50 credit, 1 contract:
```
Margin = $150 premium + (20% × $50,000) - $2,000 OTM = $150 + $10,000 - $2,000 = $8,150
```
[COMPUTED]

### Spreads (Reg T)
```
Margin = Maximum loss = (strike_width × 100 × contracts) - net_credit_received
```
Debit spreads: margin = debit paid (max loss is what you paid). Credit spreads: margin = width - credit received [VERIFIED].

Example: 10-lot SPX 4500/4510 call credit spread, $0.60 credit:
```
Margin = ($10 width × 100 × 10) - $600 credit = $10,000 - $600 = $9,400
```
[COMPUTED]

## Portfolio Margin (PM)

Portfolio Margin uses theoretical pricing models (not fixed percentages) to compute max loss under standardized stress scenarios. It is available to qualifying accounts with regulatory minimum $100,000 equity [VERIFIED].

### PM Calculation Method
Positions are stressed under ±15% price moves (varies by underlying — index ±15%, large-cap ±20%, small-cap ±30%). Theoretical losses are computed using options pricing models. Total PM requirement = sum of worst-case theoretical losses across scenarios [BROKER-VERIFIED].

### PM vs Reg T: Real Comparison

| Position | Reg T Margin | PM Margin | Savings |
|----------|--------------|-----------|---------|
| 10-lot SPX iron condor (50-wide wings) | ~$50,000 | ~$12,000 | 76% [BROKER-VERIFIED] |
| 100 SPY shares + collar | ~$25,000 | ~$3,500 | 86% |
| 5-lot TSLA strangle (50-wide) | ~$35,000 | ~$18,000 | 49% |
| Diversified 20-position theta portfolio | ~$200,000 | ~$65,000 | 68% [ESTIMATED] |

PM recognizes that hedged positions offset each other. Reg T treats each leg independently, significantly overstating actual risk [VERIFIED].

### PM Minimums and Qualifications
- **TD Ameritrade / Schwab**: $110,000 minimum equity [BROKER-VERIFIED]
- **Interactive Brokers**: $100,000 minimum equity (US residents), $500,000 (non-US) [BROKER-VERIFIED]
- **TastyTrade**: $125,000 minimum [BROKER-VERIFIED]
- Must pass broker's options knowledge assessment
- Pattern Day Trader rules still apply unless portfolio > $25,000

## SPAN Margin (Futures Options)

SPAN (Standard Portfolio Analysis of Risk) uses 16 standardized risk scenarios for futures and futures options [VERIFIED]:

- 6 scenarios from underlying price changes (±1/3, ±2/3, ±3/3 of price scan range)
- 6 scenarios from price changes + volatility changes (same price moves, ±vol shifts)
- 4 scenarios from extreme price moves (±extreme move, ±extreme move × 0.35)
- SPAN risk arrays available daily from CME: cmegroup.com/clearing/span
- ES (S&P 500 futures) options scan range: ~$6,000-12,000 depending on volatility [VERIFIED]

## Margin Call Triggers and Timelines

### Reg T Margin Calls
- **Trigger**: Maintenance excess < $0 (equity falls below maintenance requirement)
- **Timeline**: T+5 business days to meet call [VERIFIED]
- **Broker action on T+5**: Sell positions at broker's discretion to restore compliance. They choose which positions to liquidate, not you.

### Portfolio Margin Calls
- **Trigger**: PM deficit > $1,000 [BROKER-VERIFIED]
- **Timeline**: Same day or next business day. PM calls are treated as urgent.
- **Broker action**: Immediate liquidation of positions to reduce margin requirement. No grace period. IBKR begins auto-liquidation sequence within minutes of deficit detection [BROKER-VERIFIED].

### Real Margin Call Scenario
Portfolio: $120K equity, $110K PM requirement → $10K excess.
Market moves 2% against positions → PM recalculated at $128K.
Deficit: -$8K. Over $1,000 threshold. IBKR begins liquidation.
Result: Positions closed at unfavorable prices. Additional losses from forced selling compound the move [COMPUTED].

## Margin Computation Cheat Sheet

```
# Always compute from broker API — never guess [BROKER-VERIFIED]
margin = broker.get_margin_requirement(positions)

# Key ratios to monitor daily:
margin_utilization = total_margin_requirement / net_liquidation_value
excess_liquidity = net_liquidation_value - total_margin_requirement

# Safety thresholds:
if margin_utilization > 0.70: WARNING — room to maneuver shrinking
if margin_utilization > 0.85: DANGER — small move triggers call
if margin_utilization > 0.95: IMMINENT — reduce positions NOW
```

### BP (Buying Power) Effect
Options Buying Power = (Net Liq - Margin Requirement) × 2 for Reg T accounts [VERIFIED].
Options BP drops non-linearly: a 10% portfolio drawdown reduces BP by more than 10% because margin requirements rise as positions move against you. Double-whammy effect must be modeled [INFERRED].

## Common Margin Traps

1. **Weekend margin expansion**: Brokers may increase margin requirements before weekends or major events. IBKR raised maintenance requirements to 50%+ during March 2020 [VERIFIED].
2. **Earnings volatility expansion**: Margin requirements spike through earnings. A position manageable pre-earnings becomes a margin call post-earnings due to IV expansion, not price movement [BROKER-VERIFIED].
3. **Concentration penalty**: PM accounts with >50% in single underlying may face additional margin add-ons. TDA applies concentration charges; IBKR may restrict PM benefits [BROKER-VERIFIED].
4. **Portfolio Margin recalc**: PM recalculates continuously intraday. A midday spike in volatility increases theoretical losses, increasing margin requirements in real time. You may be fine at 10:00 AM and in a deficit at 2:00 PM [BROKER-VERIFIED].
