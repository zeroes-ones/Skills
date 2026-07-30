# Carry & Roll-Down Strategies

## Total Expected Return Decomposition

```
Total Return = Income Return + Roll-Down Return + Price Return
```

- **Income Return:** Coupon / Bond Price. The "carry" component — cash you receive.
- **Roll-Down Return:** Price appreciation as the bond ages down the yield curve, assuming an unchanged yield curve.
- **Price Return:** Residual — yield changes, spread changes, curve shape changes.

## Roll-Down Mechanics

### How Roll-Down Works
On an upward-sloping yield curve, a 10-year bond yields more than a 9.5-year bond.
After 6 months, your 10-year bond has 9.5 years remaining. If the yield curve hasn't changed, it now trades at the 9.5-year point's (lower) yield → price appreciation.

### Roll-Down Computation
```
Roll-Down (bp) = Yield(Current Maturity) - Yield(Forward Maturity)
Roll-Down Return (%) = Modified_Duration × Roll-Down (bp) / 100
Roll-Down Return ($) = Roll-Down Return (%) × Notional
```

### Example
```
10yr Treasury: 4.00%
9.5yr Treasury (interpolated): 3.92%
Roll-Down (6mo) = 4.00% - 3.92% = 8bp
Modified Duration = 8.2
Roll-Down Return = 8.2 × 0.08 / 100 = 0.656% over 6 months = 1.31% annualized
```

### Where Roll-Down Is Largest

| Curve Segment | Typical Slope | Roll-Down Potential | Best For |
|--------------|---------------|-------------------|----------|
| 2yr-5yr | Steepest segment | Highest roll-down per unit of duration | Short-duration carry |
| 5yr-10yr | Moderate | Moderate roll-down, more liquid | Core carry |
| 10yr-30yr | Flattest | Lowest roll-down, highest duration risk | Only if term premium is attractive |
| TIPS curve | Flatter than nominals | Lower roll-down | Inflation protection + carry |

## Net Carry Computation

### For Cash Bonds
```
Gross Carry = Yield
Financing = Repo_Rate × (Days / 360)
Net Carry = Gross_Carry - Financing

Daily Net Carry ($) = Net_Carry × Notional / 365
```

### For Futures
```
Implied Carry = Yield_CTD - Implied_Repo_Rate
Net Carry = Implied Carry (no separate financing — already in futures price)
```

Futures net carry is typically close to 0 — the basis (cash-futures spread) converges to zero at delivery, and the carry is priced into the futures level.

### For Receive-Fixed Swaps
```
Gross Carry = Swap_Rate
Financing = SOFR/OIS rate (floating leg cost)
Net Carry = Swap_Rate - SOFR - Swap_Spread
```

## Carry-Volatility Ratio

The key metric for carry trades: how many days of positive carry to offset a 1σ adverse move?

```
Daily Carry (bp) = Net Carry (%) / 365
Daily Vol (bp) = Yield Volatility × Duration

Days to Offset 1σ = Daily Vol / Daily Carry
```

| Strategy | Daily Carry | Daily 1σ Move | Days to Offset | Viable? |
|----------|------------|---------------|----------------|---------|
| Long 5yr Treasury | 0.6bp | 4bp | 7 days | ✓ Stable income |
| Long 30yr Treasury | 0.3bp | 12bp | 40 days | ⚠️ One bad week wipes out 2 months carry |
| 2s10s Steepener | 0.1bp | 3bp | 30 days | ⚠️ Slow bleed if curve keeps flattening |
| IG Credit carry | 1.2bp | 5bp | 4 days | ✓ Best carry/vol ratio (but tail risk!) |
| HY Credit carry | 2.5bp | 12bp | 5 days | ⚠️ Good ratio, catastrophic tails |

**Key Insight:** HY credit has the best carry/vol ratio in normal times, but the distribution is negatively skewed. When spreads blow out, they blow out 500-1000bp — 50-100 days of carry wiped out in a week.

## Carry Trade Execution

### Cash Bond Carry
```
1. Identify bond with attractive carry (yield - repo > 0)
2. Check: bond NOT on special (repo rate ≤ GC)
3. Buy bond, finance in repo
4. Monitor: repo rate daily. If bond goes special, financing cost drops → EXTRA profit
5. Exit: when carry turns negative or yield has moved enough to achieve target
```

### Curve Carry (Steepener)
```
1. Long short-maturity bond (lower yield), Short long-maturity bond (higher yield)
2. Net Carry = Yield(long - carry_earned) - Yield(short - carry_paid) - Repo_differential
3. Typically: net carry NEGATIVE (you pay more on the short than you earn on the long)
4. Carry bleed sets a time limit — if the curve doesn't steepen, you lose every day
5. Duration-neutral sizing: Notional_long / Notional_short = DV01_short / DV01_long
```

### Roll-Down Capture (Riding the Curve)
```
1. Buy bond at steepest part of upward-sloping curve (typically 2yr-5yr)
2. Hold for 3-6 months
3. Bond ages down the curve, yield drops → price appreciates
4. Sell before maturity gets too short (liquidity drops below 1yr)
5. Repeat with a new bond at the longer maturity point
```

## Break-Even Analysis

```
Breakeven Yield Move = Annual Net Carry (%) / Duration
Breakeven Spread Move = Annual Net Carry (%) / Spread Duration
Breakeven Curve Move = Daily Net Carry (bp) × Days_Held
```

**At breakeven:** the carry earned exactly offsets the adverse price move.
**Beyond breakeven:** the trade loses money net of carry.

