# Execution Quality

## Slippage Measurement
```
Slippage = (Executed_Price - Signal_Price) / Signal_Price * Direction
```
Where Direction = 1 for buys (slippage = paid more than signal), -1 for sells
Negative slippage = worse than signal price

### Components of Execution Cost
| Component | Typical Range | Notes |
|-----------|--------------|-------|
| Commission | $0-5 per trade (retail), $0.001-0.01/share (inst) | Fixed cost |
| Half-Spread | 0.01-0.50% | Crossing the bid-ask |
| Market Impact | 0.05-2.0% depending on size/volume | Temporary + permanent |
| Delay Cost | 0.05-0.50% | Price movement between decision and execution |
| Opportunity Cost | 0-∞ | Cost of NOT executing (for limit orders) |

## VWAP Comparison
```
VWAP = Σ (Price_i * Volume_i) / Σ Volume_i
Execution_Quality = (Executed_VWAP / Market_VWAP - 1) * Direction
```
- Negative = executed worse than VWAP
- Positive = executed better than VWAP

## Arrival Price / Implementation Shortfall
```
IS = (Executed_Price - Arrival_Price) / Arrival_Price * Direction + Opportunity_Cost
```
Where Arrival_Price = mid-price when order was submitted

## Market Impact Models (Almgren-Chriss)
```
Impact = σ * sqrt(Q / V) * (permanent_coeff + temporary_coeff)
```
Where:
- σ = volatility
- Q = order size
- V = average daily volume
- Coefficients calibrated to market microstructure

## Execution Quality Benchmarks by Asset Class
| Asset | Good Slippage | Acceptable | Poor |
|-------|-------------|-----------|------|
| US Large Cap Equities | <5 bps | 5-15 bps | >15 bps |
| US Small Cap Equities | <15 bps | 15-50 bps | >50 bps |
| US Treasuries | <2 bps | 2-10 bps | >10 bps |
| FX Majors | <3 bps | 3-10 bps | >10 bps |
| Crypto (BTC/ETH) | <10 bps | 10-50 bps | >50 bps |
| Crypto (Altcoins) | <50 bps | 50-200 bps | >200 bps |

## Provenance
[VERIFIED] Market impact from Almgren-Chriss framework; benchmark ranges from industry TCA data
[COMPUTED] Execution cost estimates are illustrative — actual costs vary by venue, time, and conditions
[AS OF 2026-01]

