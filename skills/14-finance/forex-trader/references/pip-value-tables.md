# Pip Value Tables

## Pip Value Formula by Pair Type

### USD-Quote Pairs (EUR/USD, GBP/USD, AUD/USD, NZD/USD)
```
Pip Value (USD) = (Lot Size in units × 0.0001) / 1.0
```
Since quote = USD, pip value is constant regardless of price:
- 1 standard lot (100K): $10.00/pip
- 1 mini lot (10K): $1.00/pip
- 1 micro lot (1K): $0.10/pip

### USD-Base Pairs (USD/JPY, USD/CAD, USD/CHF, USD/MXN, USD/ZAR, USD/TRY)
```
Pip Value (USD) = (Lot Size × pip_size) / Current Price
```
Pip value CHANGES with price. Must recompute at entry.
- USD/JPY pip = 0.01 (not 0.0001)
- All others: pip = 0.0001

| Pair | Price | 1 Standard Lot Pip Value | Formula |
|------|-------|-------------------------|---------|
| USD/JPY | 100 | $10.00 | (100K × 0.01) / 100 |
| USD/JPY | 150 | $6.67 | (100K × 0.01) / 150 |
| USD/JPY | 200 | $5.00 | (100K × 0.01) / 200 |
| USD/CAD | 1.30 | $7.69 | (100K × 0.0001) / 1.30 |
| USD/CAD | 1.40 | $7.14 | (100K × 0.0001) / 1.40 |
| USD/CHF | 0.90 | $11.11 | (100K × 0.0001) / 0.90 |
| USD/CHF | 1.00 | $10.00 | (100K × 0.0001) / 1.00 |

### Cross Pairs (EUR/JPY, GBP/JPY, EUR/GBP, EUR/CHF, etc.)
```
Pip Value (USD) = (Lot Size × pip_size × BASE/USD rate) / Cross Price
```
OR: Pip Value in Quote Currency × (Quote/USD rate)

| Pair | Price | Base/USD | 1 Lot Pip (USD) | Formula |
|------|-------|----------|----------------|---------|
| EUR/JPY | 165 | EUR/USD=1.10 | $6.67 | (100K × 0.01 × 1.10) / 165 |
| GBP/JPY | 200 | GBP/USD=1.27 | $6.35 | (100K × 0.01 × 1.27) / 200 |
| EUR/GBP | 0.86 | EUR/USD=1.10 | $12.79 | (100K × 0.0001 × 1.10) / 0.86 |
| EUR/CHF | 0.98 | EUR/USD=1.10 | $11.22 | (100K × 0.0001 × 1.10) / 0.98 |

### Exotic/EM Pairs
| Pair | Typical Price | Pip Size | 1 Lot Pip (USD) | Notes |
|------|--------------|----------|----------------|-------|
| USD/MXN | 17.00 | 0.0001 | $0.59 | Very small pip value; size by ATR, not pips |
| USD/ZAR | 18.50 | 0.0001 | $0.54 | 3000+ pip ATR = $1,620 daily risk per lot |
| USD/TRY | 32.00 | 0.0001 | $0.31 | Capital controls risk; gaps common |
| USD/BRL | 5.50 | 0.0001 | $1.82 | Onshore vs offshore pricing divergence |
| USD/SGD | 1.34 | 0.0001 | $7.46 | Managed float; sudden intervention risk |
| USD/HKD | 7.83 | 0.0001 | $1.28 | Pegged within band; intervention near 7.85 |

## Key Insight: Pips ≠ Risk

A 20-pip stop on EUR/USD = $200 risk per standard lot.
A 500-pip stop on USD/ZAR = $270 risk per standard lot.

Always compute dollar risk: `risk_usd = stop_distance_pips × pip_value_usd`
Never compare pip stop distances across pairs — compare dollar risk.

