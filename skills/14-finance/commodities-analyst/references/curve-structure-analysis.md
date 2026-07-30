# Curve Structure Analysis

## Contango vs Backwardation

### Contango: Futures > Spot
```
Price
  │    ╱
  │   ╱  Futures curve slopes upward
  │  ╱
  │ ╱
  │╱  Spot price below futures
  └─────────────────► Time
```
**Causes**: Storage costs, financing costs, ample supply
**Strategy**: Short futures, long spot (if storage available) — earns the roll yield
**Risk**: Contango represents a cost to long-only positions — negative roll yield

### Backwardation: Futures < Spot
```
Price
  │╲
  │ ╲  Futures curve slopes downward
  │  ╲
  │   ╲
  │    ╲  Spot price above futures
  └─────────────────► Time
```
**Causes**: Supply shortage, convenience yield, immediate demand premium
**Strategy**: Long futures, capture positive roll yield as futures converge to spot
**Risk**: Backwardation represents a return to long-only positions — positive roll yield

## Roll Yield Calculation
```
Roll Yield = (Price_Near - Price_Far) / Price_Near * (365 / Days_Between)
```
- Contango: Negative roll yield (front month more expensive than deferred)
- Backwardation: Positive roll yield (front month cheaper than deferred)

## Inventory-Curve Relationship
| Inventory Level | Curve Shape | Signal |
|----------------|-------------|--------|
| Low inventory | Backwardation | Supply tight, immediate delivery premium |
| Normal inventory | Flat | Balanced market |
| High inventory | Contango | Supply ample, storage economics dominate |
| Extreme inventory | Super-contango | Storage approaching capacity — oil 2020 scenario |

## Curve Trade Constructions
- **Calendar spread**: Long front month, short deferred (bullish)
- **Reverse calendar**: Short front month, long deferred (bearish/storage play)
- **Butterfly**: Long near, short middle, long far
- **Roll optimization**: Roll front-month positions to maximize/minimize roll yield

## Provenance
[VERIFIED] Theory from commodity finance literature (Working, Kaldor, Brennan)
[AS OF 2026-01]

