# Credit Analysis Framework

## Credit Spread Hierarchy

| Rating | Category | Typical Spread Range | 5yr CDS Range | Loss Given Default | Recovery Rate |
|--------|----------|---------------------|--------------|-------------------|---------------|
| AAA/AA | Highest quality | 20-50bp | 10-30bp | 10-15% | 85-90% |
| A | Upper medium | 50-80bp | 30-50bp | 20-30% | 70-80% |
| BBB | Lower medium (IG) | 80-200bp | 50-150bp | 35-50% | 50-65% |
| BB | Highest HY | 200-400bp | 150-350bp | 50-60% | 40-50% |
| B | High yield | 400-700bp | 350-600bp | 60-75% | 25-40% |
| CCC/CC | Very high risk | 700-2000bp | 600-2000bp | 75-90% | 10-25% |
| C/D | In/near default | 2000bp+ | 2000bp+ | 90-100% | 0-25% |

## Rating Cliff Risk

BBB- (lowest IG) → BB+ (highest HY) = "fallen angel"
- IG-only mandates forced to sell on downgrade → 50-150bp spread widening
- HY market is ~1/3 size of IG → more price impact per dollar of forced selling
- Check: near-term maturities, refinancing risk, leverage trajectory, covenant headroom

## Credit Metrics

### Leverage
```
Debt / EBITDA — most common. <2× = very low leverage. 2-4× = moderate. 4-6× = high. >6× = very high.
Net Debt / EBITDA — subtracts cash. Better for companies with large cash balances.
```

### Coverage
```
EBIT / Interest Expense — interest coverage. <2× = danger. >5× = comfortable.
EBITDA / Interest — less conservative (adds back D&A). >3× minimum for IG.
```

### Liquidity
```
(Cash + Revolver Availability) / Debt Maturities Next 12 Months
<1.0× = liquidity gap. Must refinance or draw revolvers.
>2.0× = comfortable liquidity buffer.
```

## CDS-Bond Basis

```
Basis = CDS Spread - Bond Z-Spread

Positive basis (>0): CDS wider than bond spread. Bond is RICH to CDS.
Negative basis (<0): CDS tighter than bond spread. Bond is CHEAP to CDS.
```

**Causes of Basis:**
1. **Funding cost:** Bonds require financing; CDS doesn't → positive basis (bond price reflects funding cost)
2. **Delivery option:** CDS has cheapest-to-deliver option in default → CDS wider (positive basis, 5-15bp typical)
3. **Bond-specific risk:** Covenant issues, event risk not in CDS → negative basis
4. **Liquidity:** Illiquid bond → bond spread wider than CDS → negative basis (bond cheapness premium)
5. **Short-sale constraints:** Hard to short bonds, easy to buy CDS protection → can drive positive basis

**Trading Rule:** Basis <-30bp AND no bond-specific risk → potential long bond/short CDS basis trade. Basis >50bp → investigate funding dislocation or delivery option richness.

## Credit Spread Regimes

| Regime | IG Spread Range | HY Spread Range | Macro Context | Action |
|--------|----------------|----------------|---------------|--------|
| Extreme tight | <80bp | <300bp | Peak cycle, low default expectations | Underweight credit. Asymmetric risk |
| Tight | 80-110bp | 300-450bp | Late cycle, benign | Neutral to underweight |
| Normal | 110-160bp | 450-650bp | Mid-cycle | Neutral. Pick spots |
| Wide | 160-250bp | 650-1000bp | Recession fear, elevated defaults | Overweight (contrarian if fundamentals OK) |
| Crisis | >250bp | >1000bp | Recession/crisis, forced selling | Maximum overweight. Capital required to withstand further widening |

## Sector Relative Value

| Sector | Typical Spread vs Industrials | Key Risk |
|--------|------------------------------|----------|
| Financials (senior) | +10 to +30bp | Regulatory, systemic risk |
| Financials (subordinated) | +80 to +200bp | Bail-in risk, TLAC |
| Energy (IG) | +20 to +50bp | Oil price, energy transition |
| Utilities | -10 to +20bp | Rate sensitivity (high duration) |
| REITs | +30 to +80bp | Property cycle, rates |
| Consumer (IG) | -10 to +20bp | Consumer cycle, disruption |
| Technology (IG) | -20 to +10bp | Disruption, but strong balance sheets |

