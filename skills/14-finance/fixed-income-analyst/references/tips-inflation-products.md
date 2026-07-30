# TIPS & Inflation Products

## TIPS Mechanics

### Principal Adjustment
TIPS principal adjusts daily with CPI-U (Consumer Price Index, non-seasonally adjusted).
- Index Ratio = Reference CPI_Today / Reference CPI_IssueDate
- Principal = Face × Index Ratio. This is what you receive at maturity.
- Coupon = Coupon Rate × Adjusted Principal / 2 (semi-annual)
- Deflation protection: at maturity, receive MAX(Face, Adjusted Principal)

### Index Ratio Lag
CPI is reported with ~2-week lag. TIPS use a 3-month lag for the index ratio:
- April 1: uses January CPI (released mid-February)
- The index ratio for any date is interpolated between the first of the month and first of next month
- This lag means you know the inflation accrual for the next 2-2.5 months

## Breakeven Inflation

```
Breakeven = Nominal Yield - TIPS Real Yield

Example: 10yr Nominal = 4.00%, 10yr TIPS = 1.80%
BE = 4.00% - 1.80% = 2.20%
```

IF actual CPI averages 2.20% over 10 years → TIPS and nominal have the same return.
IF CPI > 2.20% → TIPS outperform. IF CPI < 2.20% → nominals outperform.

### Breakeven Decomposition

```
BE = Expected Inflation + Inflation Risk Premium - TIPS Liquidity Premium
```

| Component | Typical Range | Description |
|-----------|--------------|-------------|
| Expected Inflation | 2.0-2.5% (US LT average) | Market's inflation forecast |
| Inflation Risk Premium | +20 to +50bp | Compensation for inflation uncertainty |
| TIPS Liquidity Premium | -10 to -30bp | TIPS are less liquid than nominals → discount |

### Decomposition Example
```
BE = 2.20%
Expected Inflation (SPF 10yr): 2.30%
Inflation Risk Premium (model estimated): +30bp
TIPS Liquidity Premium (implied): 2.30% + 0.30% - 2.20% = +40bp

Interpretation: Market expects 2.30% inflation. TIPS have a 40bp liquidity discount.
TIPS are slightly CHEAP relative to fair value (liquidity premium is higher than typical 10-30bp).
```

## Real Yield Curve

Real yields are driven by:
1. **Real growth expectations** — higher growth = higher real yields
2. **Term premium** — compensation for real rate uncertainty
3. **Fed policy** — real Fed funds rate (nominal - inflation) anchors the short end
4. **Supply/demand** — Treasury TIPS issuance volume, pension/insurance demand for real duration

| Real Yield Level | Historical Context | Signal |
|-----------------|-------------------|--------|
| Negative (< 0%) | Post-GFC, post-COVID — extreme Fed accommodation | Financial repression. Bonds return less than inflation |
| 0-1% | Loose policy, moderate growth | Low real returns. TIPS provide inflation protection cheaply |
| 1-2% | Normalization | "Fair" real returns. TIPS fairly priced |
| >2% | Tight policy, high real growth, or crisis premium | Attractive real yields. Long-duration TIPS compelling |

## TIPS vs Nominal Decision Matrix

| Scenario | Favor TIPS | Favor Nominals |
|----------|-----------|---------------|
| Inflation expectations RISING | TIPS outperform | Nominals underperform |
| Inflation expectations FALLING | TIPS underperform | Nominals outperform |
| Real rates RISING | Both lose, nominals lose more (higher duration) | — |
| Real rates FALLING | Both gain, TIPS gain less (lower duration) | — |
| Flight to quality | TIPS underperform (liquidity premium spikes) | Nominals outperform |
| Inflation SURPRISE to upside | TIPS strongly outperform | — |
| Deflation scare | TIPS underperform (deflation floor is real yield floor) | Nominals strongly outperform |

## TIPS Duration Notes

- TIPS duration is LOWER than same-maturity nominal (real cash flows are smaller for the same coupon rate)
- TIPS DV01 computed with REAL yield, not nominal → typical beta to nominal yields = 0.6-0.8
- When hedging TIPS with nominal futures: scale by `beta = regression(Δtips_real_yield ~ Δnominal_yield)`

