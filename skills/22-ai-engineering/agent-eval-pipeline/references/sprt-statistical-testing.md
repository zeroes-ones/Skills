# SPRT Statistical Testing for Agent Evals

## Sequential Probability Ratio Test (SPRT)

Tests hypothesis H0 (A = B) vs H1 (A ≠ B) with sequential sampling.

```
Parameters:
- α = 0.05 (false positive rate — claim improvement when none exists)
- β  = 0.20 (false negative rate — miss real improvement)
- δ  = 0.05 (minimum detectable effect size — 5% change)

Stop when:
- LLR ≥ log((1-β)/α)  → Reject H0: Significant difference detected
- LLR ≤ log(β/(1-α))  → Accept H0: No significant difference
- Otherwise: Collect more data
```

## Python Implementation
```python
import numpy as np
from scipy.stats import norm

def sprt_test(runs_a, runs_b, alpha=0.05, beta=0.2, delta=0.05):
    n = len(runs_a)
    mean_a, mean_b = np.mean(runs_a), np.mean(runs_b)
    std_a, std_b = np.std(runs_a, ddof=1), np.std(runs_b, ddof=1)

    # Log-likelihood ratio for normal distribution
    se = np.sqrt(std_a**2/n + std_b**2/n)
    z = (mean_b - mean_a) / se if se > 0 else 0
    llr = n * np.log(std_a/std_b) + 0.5 * sum(
        ((r - mean_a)/std_a)**2 - ((r - mean_b)/std_b)**2
        for r in runs_a + runs_b
    )

    A = np.log((1 - beta) / alpha)
    B = np.log(beta / (1 - alpha))

    if llr >= A: return "SIGNIFICANT"
    elif llr <= B: return "NOT_SIGNIFICANT"
    else: return "COLLECT_MORE"
```

## Minimum Sample Sizes
- Detecting 5% effect: ~30 runs minimum
- Detecting 2% effect: ~100 runs
- Detecting 10% effect: ~15 runs
