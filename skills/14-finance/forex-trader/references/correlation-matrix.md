# Correlation Matrix & Net Exposure

## 20-Day Rolling Correlations (Typical Regime)

| | EUR/USD | USD/JPY | GBP/USD | USD/CHF | AUD/USD | NZD/USD | USD/CAD |
|-|---------|---------|---------|---------|---------|---------|---------|
| EUR/USD | 1.00 | -0.40 | +0.85 | -0.95 | +0.70 | +0.65 | -0.60 |
| USD/JPY | | 1.00 | -0.30 | +0.50 | -0.20 | -0.15 | +0.25 |
| GBP/USD | | | 1.00 | -0.80 | +0.65 | +0.60 | -0.55 |
| USD/CHF | | | | 1.00 | -0.68 | -0.63 | +0.62 |
| AUD/USD | | | | | 1.00 | +0.90 | -0.75 |
| NZD/USD | | | | | | 1.00 | -0.70 |
| USD/CAD | | | | | | | 1.00 |

### Key Relationships

1. **EUR/USD ↔ USD/CHF: -0.95.** Near-perfect inverse. Long EUR/USD + short USD/CHF = essentially the same trade, 2× size. DO NOT combine.

2. **AUD/USD ↔ NZD/USD: +0.90.** Both commodity currencies, both anti-USD, both Asia-Pacific. Being long both = 2× the same bet.

3. **EUR/USD ↔ GBP/USD: +0.85.** Both European, both anti-USD. Significant overlap.

4. **USD/CAD ↔ AUD/USD: -0.75.** Oil correlation: CAD and AUD both commodity currencies, but CAD is quoted as USD/CAD (inverted). So they move inversely.

## Net USD Exposure Computation

```
usd_exposure = 0

For each position:
  if pair is XXX/USD:  # EUR/USD, GBP/USD, AUD/USD, NZD/USD
    usd_exposure += -notional_usd * direction  # long = short USD
  elif pair is USD/XXX:  # USD/JPY, USD/CAD, USD/CHF
    usd_exposure += notional_usd * direction  # long = long USD
  elif pair is cross (XXX/YYY):
    # Decompose: long XXX, short YYY
    if XXX is USD-related:
      usd_exposure += exchange_exposure * XXX_USD_delta
    # ... recursively decompose
```

### Worked Example

Account: $50,000. Positions:
1. Long 0.5 lots EUR/USD: -$55,250 USD exposure (short USD)
2. Long 0.3 lots GBP/USD: -$37,950 USD exposure (short USD)
3. Short 0.2 lots USD/JPY: -$20,000 USD exposure (short USD)
4. Long 0.1 lots USD/CAD: +$10,000 USD exposure (long USD)

Net USD exposure: -$55,250 - $37,950 - $20,000 + $10,000 = -$103,200
Ratio to equity: $103,200 / $50,000 = 2.06× → [ALERT: Exceeds 2× limit]

If USD rallies 1%: Loss ≈ $1,032. If USD rallies 2%: Loss ≈ $2,064 (4.1% of account).

This trader thought they had 4 diversified positions. They have 3.75 positions short USD and 0.25 long USD.

## Concentration Rules

| Single Currency Exposure | Action |
|---|---|
| Net exposure < 1× equity | ✓ Acceptable |
| Net exposure 1-2× equity | ⚠️ Elevated. Monitor daily |
| Net exposure > 2× equity | ❌ Reduce or hedge |
| Any pair > 40% of total risk | Reduce size |
| Three pairs in same direction vs same currency | Consolidate to 1-2 |

