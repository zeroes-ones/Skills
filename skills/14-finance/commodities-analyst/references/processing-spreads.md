# Processing Spreads Reference

## Crack Spreads (Refining)
Reflect the margin from refining crude oil into petroleum products.

### 3-2-1 Crack Spread
```
Crack = (2 * Gasoline + 1 * Heating Oil - 3 * Crude) / 3
```
- Most common refining margin proxy
- Traded on NYMEX as a combined order
- Seasonal: Gasoline crack peaks spring (driving season), heating oil crack peaks fall

### Key Crack Relationships
| Spread | Formula | Seasonality |
|--------|---------|-------------|
| 3-2-1 Crack | (2*RBOB + 1*HO - 3*WTI)/3 | Gasoline-driven in Q2, distillate in Q4 |
| 5-3-2 Crack | (3*RBOB + 2*HO - 5*WTI)/5 | Asian refining economics |
| Gasoline Crack | RBOB - WTI | Peak March-May |
| Heating Oil Crack | HO - WTI | Peak October-December |

## Crush Spread (Soybean Processing)
Reflects margin from crushing soybeans into meal and oil.

### Board Crush
```
Crush = (Soybean Meal * 48/2000 + Soybean Oil * 11 - Soybeans)
```
- 48 lbs meal per bushel, 11 lbs oil per bushel
- Meal = ~60% of crush value, Oil = ~40%

### Key Driver: China Demand
- China = ~60% of global soybean imports
- African swine fever, tariffs, stockpiling → major volatility drivers

## Spark Spread (Natural Gas → Electricity)
Reflects margin from generating electricity from natural gas.

```
Spark Spread = Electricity Price - (Natural Gas Price * Heat Rate)
```
- Heat rate: BTU needed per MWh (~7,000-10,000 depending on plant efficiency)
- Traded per power market: PJM, ERCOT, CAISO, etc.

## Livestock Processing Spreads
| Spread | Composition | Signal |
|--------|-------------|--------|
| Cattle Crush | Live Cattle - (Corn * Feed Ratio + Feeder Cattle) | Feedlot margin |
| Hog Crush | Lean Hogs - (Corn * Feed Ratio + Soybean Meal * Ratio) | Finishing margin |

## Execution
- Most processing spreads trade as pre-defined strategies on CME/ICE
- Crack spreads: NYMEX crack spread options available
- Crush: CBOT Board Crush futures
- Margin requirements typically LOWER than outright positions (offsetting risk)

## Provenance
[VERIFIED] Formula and relationships from CME Group product documentation
[AS OF 2026-01]

