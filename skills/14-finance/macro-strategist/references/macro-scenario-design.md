# Macro Scenario Design

## Scenario Probability Calibration

### Base-Bull-Bear Framework
```
Scenario Probabilities:
- Baseline: 60% (±10%)
- Upside: 20% (±10%)
- Downside: 20% (±10%)
```
Probabilities must sum to 100%. Never use 100% for any scenario.

## Scenario Construction Template
For each scenario, define:

### 1. Narrative (the "why")
A 2-3 sentence story explaining the economic logic. This must be internally consistent.

### 2. Key Variables
| Variable | Baseline | Upside | Downside |
|----------|----------|--------|----------|
| Real GDP Growth | X% | X+Y% | X-Z% |
| Inflation (CPI/Core PCE) | X% | X+Y% | X-Z% |
| Policy Rate (end of period) | X% | X+Y% | X-Z% |
| 10Y Treasury Yield | X% | X+Y% | X-Z% |
| S&P 500 Price Target | X | X+Y% | X-Z% |
| Credit Spreads (HY OAS) | X bps | X-Y bps | X+Z bps |

### 3. Asset Class Impact
| Asset Class | Baseline Δ | Upside Δ | Downside Δ |
|------------|-----------|----------|------------|
| US Equities | +X% | +Y% | -Z% |
| EM Equities | +X% | +Y% | -Z% |
| US Treasuries (10Y) | ±X bps | ±Y bps | ±Z bps |
| IG Credit | ±X bps | ±Y bps | ±Z bps |
| Gold | ±X% | ±Y% | ±Z% |
| Oil | ±X% | ±Y% | ±Z% |
| Dollar (DXY) | ±X% | ±Y% | ±Z% |

### 4. Scenario Triggers
What data points or events would CONFIRM this scenario is playing out?
What data points would REFUTE it?

## Stress Testing Methodology
- **Historical scenario**: What happened to our portfolio in 2008, 2020, 2022?
- **Hypothetical scenario**: What if China GDP growth falls to 2%? Oil to $120? Fed to 8%?
- **Reverse stress test**: What scenario would cause a 30% drawdown? Then work backward to assess probability.

## Provenance
[VERIFIED] Scenario design methodology from risk management best practices
[AS OF 2026-01]

