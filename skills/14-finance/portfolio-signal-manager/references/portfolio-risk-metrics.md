# Portfolio Risk Metrics — Computation Methods

## VaR (Value at Risk) — 95% Confidence, 1-Day

**Historical Simulation (preferred):**

```

Sort daily returns (trailing 252 days) ascending.
VaR(95%) = return at 5th percentile × Portfolio_Value

```

**Parametric (fallback):**

```

VaR(95%) = Portfolio_Value × (μ - 1.645σ)
Assumes normal distribution — breaks during fat-tail events.

```

## CVaR (Conditional VaR)

```

CVaR(95%) = average of all returns below VaR(95%) threshold
Always > VaR. During crises, CVaR can be 2-3x VaR.

```

## Effective N (Diversification Measure)

```

From correlation matrix eigenvalues λᵢ:
N_effective = (Σ λᵢ)² / Σ(λᵢ²)

Interpretation:
├── N_effective ≈ actual position count → Well diversified
├── N_effective ≈ 1-2 with 10+ positions → Closet index fund
└── N_effective < 3 with any portfolio → Diversification failure

```

## Stress Test Scenarios

| Scenario | SPY Move | Correlation | VIX | Bonds |
|----------|---------|-------------|-----|-------|
| 2008 GFC | -38% | → 1.0 | 80 | +5% |
| 2020 COVID | -34% | → 1.0 | 82 | +5% |
| 2022 Rate Hike | -19% | Growth -30%, Value -7% | 35 | -13% |
| Tech Crash | QQQ -33% | Tech → 1.0 | 45 | +2% |
| Flash Crash | -9% in 30min | Normal | 40 | +1% |
