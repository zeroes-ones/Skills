# Repo & Financing

## Repo Mechanics

A repurchase agreement (repo) = sell a security with agreement to buy it back at a higher price tomorrow (or at a future date). Economically: collateralized loan.

```
Repo Rate = (Repurchase_Price - Sale_Price) / Sale_Price × (360 / Days)

Example: Sell $10M bond at 100, buy back at 100.0013 tomorrow
  Rate = (0.0013 / 100) × (360 / 1) = 0.00468 = 4.68%
```

## GC vs Special Repo

### General Collateral (GC)
- Rate at which a basket of similar securities can be financed
- Not tied to a specific CUSIP
- Typically close to Fed funds / SOFR
- SOFR itself is a secured (repo) rate

### Special Repo
- A SPECIFIC security trades below GC because it's in high demand
- On-the-run Treasuries frequently go special (50-400bp below GC)
- The special spread = GC rate - special rate
- Caused by: short covering, delivery needs, benchmark status, index inclusion

**Trading Implication:** If you're SHORT a bond that goes on special, your borrow cost = GC - special_spread = much higher. The bond is "hard to borrow."

## Implied Repo Rate (Futures)

The repo rate implied by Treasury futures pricing:

```
Implied Repo = ((Futures_Price × CF + Accrued_at_Delivery) / (Bond_Price + Accrued_Today) - 1) × (360 / Days_to_Delivery)
```

If implied repo > actual repo → the bond is RICH to futures (sell bond, buy futures).
If implied repo < actual repo → the bond is CHEAP to futures (buy bond, sell futures).

CTD is typically the bond with the highest implied repo rate.

## Financing Cost for Bond Positions

### Long Bond
```
Financing Cost = Bond_Price × Notional × Repo_Rate × (Days / 360)
Net Carry = Coupon_Income - Financing_Cost
```

### Short Bond (Reverse Repo)
```
Borrow Cost = Bond_Price × Notional × (GC_Rate - Special_Spread) × (Days / 360)
Net Carry = Financing_Received - Coupon_Owed
```

If the bond is on special, the special spread increases borrow cost. For deeply special bonds (>200bp below GC), the borrow cost can make short positions prohibitively expensive.

## Repo Market Stress Signals

| Signal | Indication |
|--------|-----------|
| SOFR spikes >20bp above Fed funds | Secured funding stress. Collateral scarcity |
| Repo fails increasing | Settlement failures. Specific bond scarcity |
| Tri-party repo rates above GC | Counterparty concerns. Dealer balance sheet constraints |
| Sponsored repo volumes dropping | Dealer intermediation capacity shrinking |
| GCF repo spreads widening | Dealer-to-dealer market stress |

## Carry and Financing Checklist

Before entering any bond position held >1 day:
- [ ] Identify repo rate for the SPECIFIC bond (CUSIP-level), not GC
- [ ] Check if bond is on special: repo rate < GC - 25bp
- [ ] Compute: daily net carry = (coupon/365) - (repo_rate/360 × price)
- [ ] For shorts: check borrow availability. Some bonds are not borrowable
- [ ] For futures: implied repo rate is embedded. No separate financing needed

