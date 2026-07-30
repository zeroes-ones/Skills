# Duration & Convexity Formulas

## Duration Types — When to Use Each

| Type | Formula | Unit | Use Case | Pitfall |
|------|---------|------|----------|---------|
| Macaulay | Σ(t × PV(CF_t)) / Price | Years | Time-to-repayment. Intuitive. | Not directly useful for hedging |
| Modified | Macaulay / (1 + y/n) | % per 100bp | Parallel shift price sensitivity for option-free bonds | Assumes parallel shift. Wrong for non-parallel |
| Effective | (P_down - P_up) / (2 × P_0 × Δy) | % per 100bp | Bonds with embedded options (callable, puttable, MBS) | Requires OAS model — model-dependent |
| DV01 | Modified_Duration × Price × Notional × 0.0001 | Dollars | Hedging. What you actually use | Not comparable across different notionals without normalization |
| Key Rate | ΔP at each Treasury maturity point | % per 100bp at key tenor | Non-parallel curve shift analysis | Requires key rate shift model (e.g., 2yr, 5yr, 10yr, 30yr) |
| Spread Duration | ΔP per 100bp change in OAS/Z-spread | % per 100bp | Credit risk measurement | Often confused with rate duration. Separate risk factor |

## Modified Duration Example

```
Bond: 5% coupon, 10yr, semi-annual, price = 100, YTM = 5%
Macaulay Duration = Σ(t × CF_t / 1.025^t) / 100 = 7.79 years
Modified Duration = 7.79 / (1 + 0.05/2) = 7.79 / 1.025 = 7.60
→ 1% (100bp) rate increase → price drops 7.60%
→ DV01 per $1M = 7.60 × 1.00 × $1,000,000 × 0.0001 = $760
```

## Convexity Formula

```
Convexity = Σ(t × (t+1) × PV(CF_t)) / (Price × (1+y/n)²)

Price Change = -Modified_Duration × Δy + 0.5 × Convexity × (Δy)²

Example: MD = 7.60, Convexity = 0.65, Δy = +1.00% (100bp)
  Duration effect: -7.60 × 0.01 = -7.60%
  Convexity correction: 0.5 × 0.65 × (0.01)² = +0.00325% = +0.33bp
  Total: -7.597%  (negligible convexity for small moves)

  At Δy = +2.00% (200bp):
  Duration: -7.60 × 0.02 = -15.20%
  Convexity: 0.5 × 0.65 × (0.02)² = +0.013% = +1.3bp
  Total: -15.187%
```

## Convexity Cross-Over Point

The move size at which convexity correction exceeds X% of the duration effect:

```
Δy where |0.5 × C × (Δy)²| > X% × |MD × Δy|
  → |Δy| > 2 × X% × MD / C
```

For MD = 7.60, C = 0.65, X% = 10%:
  |Δy| > 2 × 0.10 × 7.60 / 0.65 = 2.34% = 234bp
→ Convexity matters >10% of duration only beyond ±234bp. Safe to ignore for most daily moves.

## DV01 vs Duration for Hedging

**WRONG:**
"Portfolio has duration 6.0. Hedge with 6.0 duration of futures."
Problem: $10M of 2yr bonds with duration 2.0 has DV01 = $2,000. $10M of 30yr bonds with duration 18.0 has DV01 = $18,000. Same "duration × notional" doesn't mean same dollar risk.

**RIGHT:**
Portfolio DV01 = $45,000. Futures DV01 = $78/contract. Hedge = 45,000 / 78 = 577 contracts.

Always match DV01 (dollars), not duration (percentages).

