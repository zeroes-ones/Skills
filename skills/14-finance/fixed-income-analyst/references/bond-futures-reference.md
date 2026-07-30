# Bond Futures Reference

## US Treasury Futures Contracts

| Contract | Underlying | Notional | Min Tick | Tick Value | Deliverable Basket |
|----------|-----------|----------|----------|-----------|-------------------|
| ZT (2yr) | 2yr Treasury | $200,000 | 1/4 of 1/32 = $15.625 | $15.625 | Original maturity ≤5.25yr, remaining ≥1.75yr |
| Z3N (3yr) | 3yr Treasury | $200,000 | 1/4 of 1/32 = $15.625 | $15.625 | Original maturity ≤5.25yr, remaining ≥2.75yr |
| ZF (5yr) | 5yr Treasury | $100,000 | 1/4 of 1/32 = $7.8125 | $7.8125 | Original maturity ≤5.25yr, remaining ≥4.17yr |
| ZN (10yr) | 10yr Treasury | $100,000 | 1/2 of 1/32 = $15.625 | $15.625 | Original maturity ≤10yr, remaining ≥6.5yr |
| TN (Ultra 10yr) | 10yr Treasury | $100,000 | 1/2 of 1/32 = $15.625 | $15.625 | Original maturity ≤10yr, remaining ≥9.5yr |
| TWE (20yr) | 20yr Treasury | $100,000 | 1/2 of 1/32 = $15.625 | $15.625 | Original maturity >6yr, remaining ≥19.83yr |
| ZB (30yr) | 30yr Treasury | $100,000 | 1/32 = $31.25 | $31.25 | Remaining ≥15yr, ≤25yr (if callable, first call date) |
| UB (Ultra 30yr) | 30yr Treasury | $100,000 | 1/32 = $31.25 | $31.25 | Remaining ≥25yr |

## Conversion Factor (CF)

The conversion factor adjusts for coupon differences. The futures contract assumes delivery of a 6% coupon bond.

```
CF = PV(Bond Cash Flows @ 6% yield) / Face Value

CF > 1.0 → bond has coupon > 6%. Long pays MORE on delivery.
CF < 1.0 → bond has coupon < 6%. Long pays LESS on delivery.
```

Invoice Price on Delivery: `Futures_Price × CF + Accrued_Interest`

## Cheapest-to-Deliver (CTD)

The bond from the deliverable basket that minimizes: `Futures_Price × CF - Bond_Price`

**CTD Rules of Thumb:**
- Yields < 6%: Low-coupon, long-duration bonds are CTD
- Yields > 6%: High-coupon, short-duration bonds are CTD
- The CTD changes when yields cross the 6% threshold
- Modified duration of the futures ≈ duration of the CTD / CF

## Futures DV01 Computation

```
CTD_DV01 = Modified_Duration_CTD × Price_CTD × $100,000 × 0.0001
Futures_DV01 = CTD_DV01 / CTD_CF

Note: The futures contract tracks the CTD bond's price / CF.
```

### Example: ZN (10yr) Hedge Ratio
```
Portfolio DV01: $45,000
CTD: 4.25% 11/15/2032, price 99.50, MD = 6.8, CF = 0.85
CTD_DV01 = 6.8 × 0.9950 × $100,000 × 0.0001 = $67.66
Futures_DV01 = $67.66 / 0.85 = $79.60

Hedge ratio = $45,000 / $79.60 = 565.3 → 565 contracts
```

## CTD Switch Impact

When the CTD switches:
1. **Futures DV01 changes immediately** — the contract now tracks a different bond
2. **Hedge ratio must be recalculated** — typical change: 5-15%
3. **Switch trigger:** yield crosses 6% threshold, or relative richness of deliverable bonds changes

**Monitoring:** CME publishes daily CTD and conversion factor data. Check before every hedge adjustment.

## Roll Mechanics

Treasury futures expire quarterly: March (H), June (M), September (U), December (Z).
Roll period: typically 1-2 weeks before first notice day (FND).

Roll cost: `New_Contract_Price - Old_Contract_Price + Calendar_Spread`
The calendar spread = difference between front-month and next-month contracts.
Typical roll cost: 1-3bp per quarter.

## Euro / UK Bond Futures

| Contract | Exchange | Notional | Underlying | CTD Maturity Range |
|----------|---------|----------|-----------|-------------------|
| Bund (FGBL) | Eurex | €100,000 | German govt 10yr | 8.5-10.5yr remaining |
| Bobl (FGBM) | Eurex | €100,000 | German govt 5yr | 4.5-5.5yr remaining |
| Schatz (FGBS) | Eurex | €100,000 | German govt 2yr | 1.75-2.25yr remaining |
| Buxl (FGBX) | Eurex | €100,000 | German govt 30yr | 24-35yr remaining |
| Long Gilt (FLG) | ICE | £100,000 | UK govt 10yr+ | 8.75-13yr remaining |

