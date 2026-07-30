# Perpetual Futures Mechanics

## Funding Rate Formula
```
Funding Rate = Premium Index + clamp(Interest Rate - Premium Index, -0.05%, 0.05%)
```
Where Premium Index = (Mark Price - Index Price) / Index Price

## Major Exchange Funding Intervals
| Exchange | Default Interval | Rate Cap | Notes |
|----------|-----------------|----------|-------|
| Binance | 8 hours (00:00, 08:00, 16:00 UTC) | ±0.375% | Some pairs use 4-hour or 2-hour |
| Bybit | 8 hours | ±0.375% | USDC-margined may differ |
| OKX | 8 hours | ±0.375% | Same as Binance standard |
| dYdX | 1 hour | ±0.05% | Decentralized, Governance-set |

## Annualizing Funding Rate
```
Annualized = Funding_Rate * (365 * 24 / Interval_Hours)
```
Example: 0.01% per 8h = 0.01% * (365*24/8) = 10.95% annualized

## Mark vs Index Price
- **Index Price**: Volume-weighted spot price across major exchanges
- **Mark Price**: Price used for liquidation — computed from index + decaying funding basis
- **Divergence risk**: Mark-index spread widens during volatility → liquidation before index moves

## Liquidation Mechanics
| Feature | Cross Margin | Isolated Margin |
|---------|-------------|-----------------|
| Collateral | Entire account | Position-specific allocation |
| Liquidation threshold | Maintenance margin % of total | Maintenance margin % of position |
| Partial liquidation | Common on major exchanges | Rare |

## Insurance Fund
- Covers bankruptcy losses when liquidated position < 0
- Fund size per exchange: Binance ~$500M+, Bybit ~$300M+, OKX ~$200M+
- Depletion risk during cascading liquidations

## Provenance
[VERIFIED] Formula from Binance, Bybit, OKX documentation
[AS OF 2026-01 — VERIFY LIVE RATES]

