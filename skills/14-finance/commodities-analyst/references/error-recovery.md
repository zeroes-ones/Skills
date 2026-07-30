# Commodities Error Recovery

## Additional Error Patterns

### 1. Weather Premium Overestimation
**Symptom**: Bought on weather forecast that didn't materialize
**Root Cause**: Long-range weather forecasts have ~50% skill at 10 days, near-zero at 20+ days
**Fix**: Scale weather-driven positions to forecast confidence. 7-day forecast: 0.7 skill; 14-day: 0.3 skill. Position size proportional to forecast skill.
**Lesson**: Weather is only tradeable inside the high-skill forecast window (5-7 days). Beyond that, it's gambling on model runs.

### 2. Global Balance vs Local Balance Confusion
**Symptom**: Shorted wheat based on global surplus, but local supply was tight → price surged
**Root Cause**: Commodities are physical, not statistical. Wheat in Russia does NOT equal wheat in Kansas. Transportation costs, quality differences, and trade barriers segment markets.
**Fix**: Analyze supply/demand at the DELIVERY POINT, not globally. CME wheat = deliverable at specific locations. Global surplus with local deficit = backwardation, not contango.
**Lesson**: The only supply that matters for futures price is deliverable supply at exchange-approved warehouses.

### 3. Processing Spread Execution Failure
**Symptom**: Crack spread analysis correct but lost money on execution
**Root Cause**: Processing spreads are multi-leg orders with wide bid-ask and leg ratio mismatches
**Fix**: Use exchange-listed spread orders (not legging in). Check spread liquidity separately from leg liquidity. Size for spread execution, not leg execution.
**Lesson**: Processing spreads trade as their own instruments. The spread market can be wider/thinner than the leg markets.

### 4. Gold/Silver Ratio Mean Reversion Trap
**Symptom**: Bought gold/silver ratio expecting reversion to "normal" 60, ratio kept climbing to 90+ (2020) or 120+ (2024)
**Root Cause**: The "long-term average" of the gold/silver ratio reflects a monetary system (bimetallism) that ended in 1971. Since 1971, the ratio has been 15-125, with no stable mean.
**Fix**: Don't trade this mean reversion without a catalyst. The ratio can stay extreme for years. Trade the catalyst, not the ratio level.
**Lesson**: Historical ratios from different monetary regimes are not comparable. Post-1971, gold/silver is a sentiment indicator, not a mean-reverting spread.

## Provenance
[VERIFIED] Error patterns from commodity trading literature and market analysis
[AS OF 2026-01]

