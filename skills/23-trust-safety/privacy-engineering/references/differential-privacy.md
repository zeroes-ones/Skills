# Differential Privacy

Epsilon selection, Laplace/Gaussian mechanisms, privacy budget
accounting, and composition theorems for practical DP implementation.

## Query Sensitivity (Delta-f)

The maximum change in query output from adding or removing one
individual from the dataset.

| Query Type | Sensitivity Formula | Example |
|-----------|-------------------|---------|
| Count | Delta-f = 1 | "How many users clicked?" — each person contributes 1 |
| Sum | Delta-f = max(value) | "Total revenue" — max individual purchase is cap |
| Average | Delta-f = (max - min) / n | "Average age" — range/narrower with more people |
| Histogram | Delta-f = 1 (disjoint) or 2 (overlapping) | "Users by age bucket" — each in exactly one bucket |
| Median | Delta-f = unbounded (use alternative) | Median requires exponential mechanism or smooth sensitivity |

## Epsilon Privacy Budget

| Epsilon | Privacy Level | Noise Level | Use Case |
|---------|--------------|-------------|----------|
| 0.01 | Extremely strong | Very noisy | Census Bureau, highly sensitive data |
| 0.1 | Strong | Moderate noise | Apple emoji/QuickType suggestions, health data queries |
| 0.5 | Good | Low-moderate noise | Research datasets with strong privacy guarantees |
| 1.0 | Moderate | Low noise | Typical analytics, aggregate dashboards |
| 2.0-5.0 | Weak-moderate | Minimal noise | Internal business intelligence with known users |
| 10+ | Very weak | Negligible | May as well release raw data |

## Laplace Mechanism

Adds Laplace noise scaled by sensitivity/epsilon. Optimal for L1
sensitivity (counts, sums, histograms).

```
laplace_noise = Lap(scale = sensitivity / epsilon)
private_result = true_result + laplace_noise
```

Standard deviation of noise = sqrt(2) * sensitivity / epsilon.
At epsilon=1.0, sensitivity=1: SD ≈ 1.41 counts.

## Gaussian Mechanism

Adds Gaussian noise scaled by L2 sensitivity. Used when composition
requires tighter bounds via advanced composition theorems.

## Composition Theorems

**Basic Composition**: epsilon_total = epsilon_1 + epsilon_2 + ... + epsilon_k
Running k queries each with epsilon consumes k*epsilon of the budget.

**Advanced Composition** (Dwork-Roth-Vadhan): For k queries with
epsilon, delta each, total privacy loss is approximately
sqrt(2k*ln(1/delta')) * epsilon + k*epsilon*(e^epsilon - 1).

**Parallel Composition**: Queries on DISJOINT data subsets do not
sum — epsilon_total = max(epsilon_i) across partitions.

## Local vs Global Differential Privacy

| Property | Global DP (Centralized) | Local DP |
|----------|------------------------|----------|
| Trust model | Trusted curator has raw data | Users don't trust server |
| Utility | High (noise added once) | Lower (noise per user) |
| Implementation | Add noise to query results | Users randomize before sending |
| Example | US Census Bureau | Apple iOS, Google RAPPOR |
| Epsilon per query | 0.1-1.0 usable | 2-10 per user (accumulates fast) |

## Privacy Budget Accounting

Track a privacy ledger for production DP systems:
- Total epsilon budget per dataset (e.g., 10.0/month)
- Per-query epsilon consumption logged
- Budget exhaustion triggers query rejection or noise increase
- Budget resets on schedule (daily, weekly, monthly)
- Alerting when approaching budget limit
