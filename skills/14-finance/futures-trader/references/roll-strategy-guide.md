# Roll Strategy Guide

> Roll execution: calendar spread orders, timing windows, cost analysis, broker-specific roll mechanics.

## Why Rolls Matter

Futures expire. To maintain continuous exposure, positions must be "rolled" — close the expiring contract and open the next expiration. The roll IS the recurring cost (or benefit) of futures exposure. Done poorly, roll costs destroy returns. Done well, roll yield can be a structural edge.

## Roll Timing Windows

Optimal roll timing: **7-10 calendar days before Last Trading Day (LTD)**

| DTE | Front-Month Liquidity | Next-Month Liquidity | Recommendation |
|-----|----------------------|---------------------|----------------|
| 14+ | HIGH | LOW | Monitor. Plan roll date. |
| 10-14 | HIGH | GROWING | Acceptable roll window. Begin execution. |
| 7-10 | MEDIUM | HIGH | OPTIMAL. Next-month volume > front-month. |
| 3-7 | LOW | HIGH | Acceptable but spreads widening. |
| 0-3 | VERY LOW | HIGH | URGENT. Illiquidity risk. Execute immediately. |

## Calendar Spread Mechanics

The calendar spread = Front Month Price - Next Month Price

```
Spread > 0 → BACKWARDATION (front-month premium)
Spread < 0 → CONTANGO (front-month discount)
```

### Roll Cost/Benefit Computation

```
Annualized Roll Impact = (Calendar Spread / Front-Month Price) × (365 / Days Between Expirations)
```

**Examples:**

```
Crude Oil (CL): Front $75.00, Next $75.80, 30 days between expirations
Calendar Spread: -$0.80 (contango)
Annualized Cost: (0.80/75.00) × (365/30) = 13.0% → LONG positions pay 13%/year in roll

S&P 500 (ES): Front 5525.50, Next 5550.25, 90 days between expirations
Calendar Spread: -$24.75 (contango)
Annualized Cost: (24.75/5525.50) × (365/90) = 1.82% → Modest roll cost for ES longs

Natural Gas (NG): Front $3.50, Next $4.20, 30 days
Calendar Spread: -$0.70 (heavy contango)
Annualized Cost: (0.70/3.50) × (365/30) = 243% → LONG NG is a disaster in contango
```

## Calendar Spread Orders (vs Two Outright Orders)

### CORRECT: Calendar Spread Order

```
Order: "Sell 1 ESU6 / Buy 1 ESZ6 at +3.75 limit"
Type: Calendar Spread
Execution: Both legs fill simultaneously at the spread price
Cost: ONE bid-ask spread
Slippage: 0.5-1 tick in liquid spreads
```

### WRONG: Two Outright Orders

```
Step 1: "Sell 1 ESU6 at market" → Filled at bid
Step 2: "Buy 1 ESZ6 at market" → Filled at ask
Cost: TWO bid-ask spreads (double)
Slippage: 2-4 ticks from market movement between orders
Leg Risk: Market moves while one leg is open
```

**Always use calendar spread orders.** Every major broker supports them:
- IBKR: Combo order with spread type = "Calendar"
- Schwab (thinkorswim): Spread order → Calendar tab
- Multiplier: Exchange-native spread order type = guaranteed simultaneous fill

## Roll Yield as a Strategy

Roll yield can be harvested as a strategy (not just a cost to manage):

- **Long backwardated markets** → Earn positive roll yield as front-month converges to spot
- **Short contango markets** → Earn positive roll yield as front-month converges to spot
- **Calendar spread trading** → Trade the shape change, not the outright direction

Example: A trader who is ALWAYS long the S&P 500 via ES futures pays ~1.8% annual roll cost. A trader who is long ES when backwardated (rare) and flat when in contango captures roll yield selectively.

## Broker Roll-Specific Notes

### Interactive Brokers (IBKR)
- IBKR auto-liquidates physical-delivery long futures 2-3 days before FND
- Use "Rollover" button in TWS or API: close front-month + open next-month as spread
- API: Use `whatIf=True` to verify margin impact before executing roll

### Schwab (thinkorswim)
- thinkorswim "Roll" feature: right-click position → Create Closing Order → With Opening Order
- Manual spread construction: Analyze tab → Spread Book
- Auto-liquidation at FND-3 for physical delivery contracts

### Alpaca
- Futures not supported as of 2026-07-28 [VERIFIED]

## Roll Cost Tracking

Track every roll to quantify the strategy's structural cost:

| Roll Date | Contract | Front Close | Next Close | Calendar Spread | Annualized Cost | Slippage |
|-----------|----------|------------|------------|----------------|-----------------|----------|
| 2026-09-08 | ES | 5525.50 | 5550.25 | -24.75 | 1.82% | 0.50 ticks |
| 2026-08-12 | CL | 72.40 | 73.15 | -0.75 | 12.3% | 2.00 ticks |

Track cumulative roll costs per year per product. If roll costs exceed strategy edge, the strategy is negative carry.

