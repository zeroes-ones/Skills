# Statistical Evaluation Methodology

<!-- QUICK: 30s -- Statistical evals replace binary pass/fail with SPRT sequential testing (α=0.05, β=0.20), bootstrapped confidence intervals for small samples, and AgentAssay's statistical detection framework (86% true defect detection vs 0% for binary pass/fail). -->

## Why Statistical Eval?

Binary pass/fail evaluation has a 0% true defect detection rate for AI agents. An agent that passes 18/20 tests is indistinguishable from one that passes 20/20 due to stochastic noise. Statistical methods detect real behavioral changes with quantified confidence.

## SPRT: Sequential Probability Ratio Test

SPRT stops evaluation as soon as statistical significance is reached, saving 40-60% of eval cost compared to fixed-sample testing.

### Theory

```
H₀: agent_pass_rate ≥ p₀ (null hypothesis: agent is "good enough")
H₁: agent_pass_rate ≤ p₁ (alternative: agent is degraded)

Boundaries:
  A = log((1-β)/α)        # Upper boundary: accept H₀
  B = log(β/(1-α))        # Lower boundary: reject H₀ (accept H₁)

After each test result r ∈ {pass, fail}:
  LLR += log(P(r|H₁) / P(r|H₀))

Decision:
  LLR ≥ A → Stop: accept H₀ (agent passes)
  LLR ≤ B → Stop: accept H₁ (agent fails)
  B < LLR < A → Continue testing
```

### Implementation

```python
from dataclasses import dataclass
from typing import Optional
import math

@dataclass
class SPRTConfig:
    """SPRT configuration with standard α=0.05, β=0.20 bounds."""
    p0: float = 0.90   # Null hypothesis: agent passes ≥ 90%
    p1: float = 0.80   # Alternative: agent passes ≤ 80%
    alpha: float = 0.05  # Type I error: false positive
    beta: float = 0.20   # Type II error: false negative
    max_tests: int = 200  # Safety limit to prevent infinite runs

class SPRTRunner:
    def __init__(self, config: SPRTConfig):
        self.config = config
        self.A = math.log((1 - config.beta) / config.alpha)
        self.B = math.log(config.beta / (1 - config.alpha))
        self.llr = 0.0
        self.passes = 0
        self.fails = 0
    
    def update(self, passed: bool) -> Optional[str]:
        """Update SPRT with a test result. Returns decision or None."""
        if passed:
            lr = self.config.p1 / self.config.p0  # Likelihood ratio for pass
            self.passes += 1
        else:
            lr = (1 - self.config.p1) / (1 - self.config.p0)  # LR for fail
            self.fails += 1
        
        self.llr += math.log(lr)
        
        if self.llr >= self.A:
            return "accept_null"  # Agent is good enough
        elif self.llr <= self.B:
            return "reject_null"  # Agent is degraded
        elif (self.passes + self.fails) >= self.config.max_tests:
            return "max_tests_reached"
        return None  # Continue testing

# Usage
sprt = SPRTRunner(SPRTConfig(p0=0.90, p1=0.80))
for result in run_eval_tests():
    decision = sprt.update(result.passed)
    if decision:
        print(f"SPRT stopped after {sprt.passes + sprt.fails} tests: {decision}")
        break
```

### Cost Savings

| Method | Tests to Decision (avg) | Cost @ $2/test | Savings |
|--------|------------------------|----------------|---------|
| Fixed sample (n=100) | 100 | $200 | Baseline |
| SPRT (agent clearly good) | 20-30 | $40-60 | 70-80% |
| SPRT (agent clearly bad) | 10-15 | $20-30 | 85-90% |
| SPRT (borderline) | 80-200 | $160-400 | -100% to 20% |

## Bootstrap Confidence Intervals

When sample sizes are small (< 50), bootstrap CIs provide reliable uncertainty quantification:

```python
import numpy as np

def bootstrap_ci(scores: List[float], n_bootstrap: int = 10000, 
                 ci_level: float = 0.95) -> Tuple[float, float]:
    """
    Compute bootstrap confidence interval for mean score.
    
    For n=20 samples, a 95% CI might be [0.62, 0.88] —
    very different from the point estimate of 0.75.
    """
    n = len(scores)
    boot_means = []
    
    for _ in range(n_bootstrap):
        sample = np.random.choice(scores, size=n, replace=True)
        boot_means.append(np.mean(sample))
    
    alpha = (1 - ci_level) / 2
    lower = np.percentile(boot_means, alpha * 100)
    upper = np.percentile(boot_means, (1 - alpha) * 100)
    
    return lower, upper

# Always report CI alongside point estimate:
# "Agent pass rate: 0.75 (95% CI: [0.62, 0.88], n=20)"
```

## AgentAssay Framework

AgentAssay is a statistical detection framework that achieves **86% true defect detection** versus **0%** for binary pass/fail. Based on the methodology from the AgentAssay paper.

### Core Insight

Binary pass/fail can't distinguish:
- A broken agent that got lucky (10% of runs) → false negative
- A working agent that got unlucky (10% of runs) → false positive

AgentAssay uses effect size detection: even if individual test outcomes overlap, the **distribution** of outcomes reveals the defect.

### Implementation

```python
from scipy import stats

def agent_assay_test(
    baseline_scores: List[float],  # Scores from known-good agent
    candidate_scores: List[float],  # Scores from agent under test
    effect_size_threshold: float = 0.3,  # Cohen's d threshold
    p_value_threshold: float = 0.05
) -> dict:
    """
    AgentAssay: detect behavioral defects using effect size analysis.
    
    Returns:
      - defect_detected: bool
      - effect_size: Cohen's d
      - p_value: Mann-Whitney U test
      - confidence: "low" | "medium" | "high"
    """
    # Non-parametric test (no normality assumption)
    statistic, p_value = stats.mannwhitneyu(
        candidate_scores, baseline_scores, alternative='two-sided'
    )
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.std(baseline_scores)**2 + np.std(candidate_scores)**2) / 2)
    effect_size = abs(np.mean(candidate_scores) - np.mean(baseline_scores)) / pooled_std
    
    defect_detected = (p_value < p_value_threshold) and (effect_size > effect_size_threshold)
    
    # Confidence based on both statistical significance and practical significance
    if p_value < 0.01 and effect_size > 0.5:
        confidence = "high"
    elif p_value < 0.05 and effect_size > 0.3:
        confidence = "medium"
    else:
        confidence = "low"
    
    return {
        "defect_detected": defect_detected,
        "effect_size": round(effect_size, 3),
        "p_value": round(p_value, 4),
        "confidence": confidence,
        "baseline_mean": round(np.mean(baseline_scores), 3),
        "candidate_mean": round(np.mean(candidate_scores), 3),
        "n_baseline": len(baseline_scores),
        "n_candidate": len(candidate_scores)
    }

# Binary pass/fail: 0% detection rate
# AgentAssay: 86% detection rate (from paper)
```

## When to Use Each Method

| Method | Sample Size | Use When | Avoid When |
|--------|-------------|----------|------------|
| SPRT | 10-200 | Continuous eval with cost constraints | Fixed budget already allocated |
| Bootstrap CI | 20-50 | Reporting uncertainty on small samples | n > 1000 (use normal approximation) |
| AgentAssay | 30+ per group | Comparing agent versions; detecting subtle regressions | n < 20 per group (insufficient power) |
| Fixed sample | n ≥ 100 | Budget is fixed; no early stopping needed | Cost-sensitive; early decisions possible |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| "Agent passed 19/20, ship it" | 95% pass rate could be 85-100% (95% CI); no way to know if degradation is real | Always report CI: "0.95 (95% CI: [0.75, 1.00], n=20)" |
| Comparing point estimates without CIs | "0.92 vs 0.88" might be noise (CI overlap) or signal (CI separation) | Compare CI overlap: overlapping CI → not significant; non-overlapping CI → significant |
| Running fixed n=10 for all decisions | n=10 CI is too wide to detect anything smaller than a 30% degradation | Use SPRT: stop early when clearly good/bad, continue when borderline |
| Ignoring effect size | p < 0.05 with d = 0.05 is statistically significant but practically meaningless | Require both p < 0.05 AND d > 0.3 (meaningful effect size) |
