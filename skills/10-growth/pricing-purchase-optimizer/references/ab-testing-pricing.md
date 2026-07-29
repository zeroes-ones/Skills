# A/B Testing for Pricing Pages

## Statistical Framework

### Required Parameters

| Parameter | Minimum | Recommended | Why |
|-----------|---------|-------------|-----|
| Sample size | 2,500/ variant | 10,000+/ variant | Small samples = high variance = unreliable results |
| Duration | 1 week | 2+ weeks | Capture weekday/weekend, pay cycle, and novelty decay |
| p-value | < 0.05 | < 0.01 | Standard statistical significance threshold |
| MDE (Minimum Detectable Effect) | 5% relative | 3% relative | Below 3% requires very large samples (50K+) |
| Power | 80% | 90% | Probability of detecting real effect if it exists |

### Sample Size Calculator

```
For conversion rate test (baseline: 3%, MDE: 15% relative):
  n = (Z_α/2 + Z_β)² × (p₁(1-p₁) + p₂(1-p₂)) / (p₂ - p₁)²

  Where:
  Z_α/2 = 1.96 (for α = 0.05)
  Z_β = 1.28 (for power = 0.90)
  p₁ = 0.03 (baseline conversion)
  p₂ = 0.0345 (3% + 15% = 3.45%)

  Result: ~ 50,000 per variant
```

### RAMP Plan

```
Stage 1: 5% traffic → Monitor 24hr. Guardrail: no CR drop >10%.
Stage 2: 25% traffic → Monitor 48hr. Guardrail: RPV stable.
Stage 3: 50% traffic → Monitor 72hr. Check statistical significance.
Stage 4: 100% traffic → Winner declared only if p < 0.05.
```

## Test Variables (Single Variable Per Test)

| Test | Variable | Control | Variant | Primary Metric |
|------|----------|---------|---------|---------------|
| Tier count | 4 tiers | 3 tiers | Conversion rate | |
| Tier highlighting | No highlight | "Most Popular" on middle | Middle tier selection % | |
| Annual toggle default | Monthly default | Annual default | Annual plan selection % | |
| CTA copy | "Get Started" | "Start Free Trial" | Click-through rate | |
| Price endpoints | $99 (charm) | $100 (round) | Conversion rate | |
| Social proof | No testimonials | Customer logos + quote | Conversion rate | |

## CUPED (Controlled Experiment Using Pre-Experiment Data)

Reduce variance by accounting for pre-experiment behavior:

```
CUPED-adjusted metric = Y - θ × (X - X̄)

Where:
Y = metric during experiment
X = same metric before experiment
θ = cov(Y, X) / var(X)
X̄ = mean of pre-experiment metric

Variance reduction: typically 10-50%
Sample size reduction: same percentage as variance reduction
```

## Multi-Armed Bandit (Thompson Sampling)

Allocate traffic dynamically to winning variant:

```
For each variant:
  Sample from Beta(α + conversions, β + non-conversions)
  Allocate next visitor to variant with highest sample

Advantage: converges faster than fixed A/B.
Disadvantage: harder to interpret, risk of early false convergence.
Use when: testing many variants (5+) and want faster convergence.
```

## Guardrail Metrics

Must not degrade below thresholds:

| Guardrail | Threshold | Action if Breached |
|-----------|-----------|-------------------|
| Revenue Per Visitor (RPV) | -5% vs control | Pause test, investigate |
| Signup → Paid conversion | -10% vs control | Pause test |
| Support ticket rate | +20% vs control | Review for confusion/bugs |
| Page load time | +500ms vs control | Performance regression |
| Refund/chargeback rate | +50% vs control | Dark pattern suspicion |
