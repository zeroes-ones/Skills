# Risk Metrics Guide

## Value at Risk (VaR)
**Definition**: Maximum expected loss over a given time horizon at a given confidence level.

```
VaR(α) = Portfolio_Value * σ * Z(α) * sqrt(T)
```
Where:
- σ = daily volatility (standard deviation of returns)
- Z(α) = Z-score for confidence α (1.65 for 95%, 2.33 for 99%)
- T = time horizon in days

### VaR Methodologies
| Method | Pros | Cons |
|--------|------|------|
| Parametric | Fast, simple | Assumes normality — underestimates tail risk |
| Historical | No distribution assumption, captures real tails | Limited by history, slow to adapt |
| Monte Carlo | Flexible, handles complex portfolios | Computationally expensive, GIGO |
| Cornish-Fisher | Adjusts for skewness/kurtosis | Still parametric at core |

## Conditional VaR (CVaR / Expected Shortfall)
**Definition**: Expected loss GIVEN that loss exceeds VaR threshold.

```
CVaR(α) = E[Loss | Loss > VaR(α)]
```

**Why CVaR matters**: VaR says "99% of days you lose less than $X." CVaR says "On the 1% worst days, you lose $Y on average." CVaR is always ≥ VaR and tells you what the tail actually costs.

## Maximum Drawdown (MDD)
```
MDD = (Peak - Trough) / Peak
```
Measured over the entire equity curve.

## Calmar Ratio
```
Calmar = CAGR / MDD
```
Above 1.0 is good. Below 0.5 is concerning.

## Sortino Ratio
```
Sortino = (Return - MAR) / Downside_Deviation
```
Where Downside_Deviation = std_dev of returns BELOW MAR (minimum acceptable return)

## Omega Ratio
```
Omega = ∫[MAR,∞] (1 - F(x)) dx / ∫[-∞, MAR] F(x) dx
```
Measures ratio of probability-weighted gains to probability-weighted losses. Should be > 1.

## Stress Testing
### Historical Scenarios
| Scenario | Equities | Bonds | Gold | VIX |
|----------|---------|-------|------|-----|
| 2008 GFC | -55% | +5% | +5% | +130% |
| 2020 COVID | -34% | +1% | +5% | +340% |
| 2022 Rate Hike | -19% | -13% | -0.3% | +50% |
| 1987 Crash | -22% (single day) | +8% | +40% | +315% |

### Forward-Looking Scenarios
- Rates +200bps shock
- Credit spread widening +3σ
- Currency devaluation 20%
- Commodity supply shock

## Tail Risk and Extreme Value Theory
### Hill Estimator
Fits a generalized Pareto distribution (GPD) to tail observations for extrapolating beyond historical max.

### Key Metrics
| Metric | Formula | Interpretation |
|--------|---------|---------------|
| Skewness | E[(R - μ)³] / σ³ | Negative = left-tail risk |
| Excess Kurtosis | E[(R - μ)⁴] / σ⁴ - 3 | >0 = fat tails |
| Tail Index (ξ) | From GPD fit | <0.5 = very fat tails, 0.5-1 = moderate, >1 = thin |

## Provenance
[VERIFIED] VaR, CVaR, Sortino, Calmar, Omega from financial mathematics literature
[COMPUTED] Stress test scenarios from historical market data — exact returns vary by index and measurement window
[AS OF 2026-01]

