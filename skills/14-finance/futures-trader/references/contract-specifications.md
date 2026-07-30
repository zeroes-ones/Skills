# Contract Specifications

> Reference for all major futures contracts: multiplier, tick size, tick value, delivery type, FND/LTD, trading hours, exchange.

## Equity Index Futures (CME)

| Contract | Symbol | Multiplier | Tick Size | Tick Value | Point Value | Delivery | Primary Session (CT) |
|----------|--------|-----------|-----------|------------|-------------|----------|----------------------|
| E-mini S&P 500 | ES | $50 × index | 0.25 | $12.50 | $50 | Cash | 8:30 AM-3:15 PM |
| Micro E-mini S&P | MES | $5 × index | 0.25 | $1.25 | $5 | Cash | 8:30 AM-3:15 PM |
| E-mini Nasdaq-100 | NQ | $20 × index | 0.25 | $5.00 | $20 | Cash | 8:30 AM-3:15 PM |
| Micro E-mini Nasdaq | MNQ | $2 × index | 0.25 | $0.50 | $2 | Cash | 8:30 AM-3:15 PM |
| E-mini Dow | YM | $5 × index | 1.00 | $5.00 | $5 | Cash | 8:30 AM-3:15 PM |
| E-mini Russell 2000 | RTY | $50 × index | 0.10 | $5.00 | $50 | Cash | 8:30 AM-3:15 PM |

## Commodity Futures

| Contract | Symbol | Exchange | Contract Size | Tick Size | Tick Value | Point Value | Delivery | Primary Session (CT) |
|----------|--------|----------|--------------|-----------|------------|-------------|----------|----------------------|
| Crude Oil | CL | NYMEX | 1,000 barrels | $0.01 | $10.00 | $1,000 | Physical | 8:00 AM-1:30 PM |
| Natural Gas | NG | NYMEX | 10,000 MMBtu | $0.001 | $10.00 | $10,000 | Physical | 8:00 AM-1:30 PM |
| Gold | GC | COMEX | 100 troy oz | $0.10 | $10.00 | $100 | Physical | 7:20 AM-12:30 PM |
| Silver | SI | COMEX | 5,000 troy oz | $0.005 | $25.00 | $5,000 | Physical | 7:25 AM-12:25 PM |
| Copper | HG | COMEX | 25,000 lbs | $0.0005 | $12.50 | $25,000 | Physical | 8:10 AM-1:00 PM |
| Corn | ZC | CBOT | 5,000 bushels | $0.0025 | $12.50 | $5,000 | Physical | 8:30 AM-1:20 PM |
| Soybeans | ZS | CBOT | 5,000 bushels | $0.0025 | $12.50 | $5,000 | Physical | 8:30 AM-1:20 PM |
| Wheat | ZW | CBOT | 5,000 bushels | $0.0025 | $12.50 | $5,000 | Physical | 8:30 AM-1:20 PM |
| Cotton | CT | ICE | 50,000 lbs | $0.01 | $5.00 | $500 | Physical | 8:00 AM-1:20 PM |
| Coffee | KC | ICE | 37,500 lbs | $0.0005 | $18.75 | $37,500 | Physical | 8:30 AM-1:00 PM |

## Interest Rate Futures (CBOT/CME)

| Contract | Symbol | Underlying | Point Value | Tick Value | Delivery |
|----------|--------|-----------|-------------|------------|----------|
| 30-Year T-Bond | ZB | $100,000 face | $1,000 | $15.625 | Physical |
| 10-Year T-Note | ZN | $100,000 face | $1,000 | $15.625 | Physical |
| 5-Year T-Note | ZF | $100,000 face | $1,000 | $7.8125 | Physical |
| 2-Year T-Note | ZT | $200,000 face | $2,000 | $7.8125 | Physical |
| Eurodollar | GE | $1,000,000 | $2,500/bp | $6.25 | Cash |
| Fed Funds | ZQ | $5,000,000 | $4,166.70/bp | $10.4175 | Cash |

## Currency Futures (CME)

| Contract | Symbol | Contract Size | Tick Value | Delivery |
|----------|--------|--------------|------------|----------|
| Euro FX | 6E | €125,000 | $12.50 | Physical |
| Japanese Yen | 6J | ¥12,500,000 | $12.50 | Physical |
| British Pound | 6B | £62,500 | $6.25 | Physical |
| Australian Dollar | 6A | A$100,000 | $10.00 | Physical |

## Globex Trading Hours

All CME Group products trade on Globex:
- **Sunday 5:00 PM CT – Friday 4:00 PM CT** (23 hours/day, 5 days/week)
- **Daily maintenance break:** 4:00 PM – 5:00 PM CT (60 minutes)
- **Note:** Equity index futures have a 3:15 PM – 3:30 PM CT trading halt
- **Grains:** Overnight session 7:00 PM – 7:45 AM CT; Day session 8:30 AM – 1:20 PM CT

## Expiration Cycles

- **Equity Index:** Quarterly (Mar/Jun/Sep/Dec) — H, M, U, Z
- **Grains:** Varies — Corn: Mar/May/Jul/Sep/Dec (H, K, N, U, Z)
- **Energy:** Monthly — all 12 months
- **Metals:** Even months + nearest odd — Gold: Feb/Apr/Jun/Aug/Dec + nearest 3 from (Jan/Mar/May/Jul/Sep/Nov)
- **Interest Rates:** Quarterly
- **Currencies:** Quarterly + serial months

## Key Sources

- CME Group Product Slate: cmegroup.com/markets
- ICE Futures: theice.com/products
- Contract multipliers and ticks verified against exchange specifications

