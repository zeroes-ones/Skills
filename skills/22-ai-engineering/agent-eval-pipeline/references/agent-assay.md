# AgentAssay — Defect Detection Methodology for AI Agents

AgentAssay is a statistical framework for detecting behavioral defects in AI agents through controlled experimentation.
It replaces binary pass/fail evaluation with effect-size detection, achieving 86% true defect detection vs 0% for
binary comparison.

## Core Principle

Binary pass/fail (e.g., 19/20 vs 20/20) has zero statistical power for detecting meaningful behavioral changes in
stochastic systems. AgentAssay uses effect-size measurement with configurable sensitivity thresholds.

## Defect Taxonomy

| Category | Definition | Example |
|----------|-----------|---------|
| Hallucination | Agent produces factually incorrect output | "The file is at /src/main.py" when file does not exist |
| Omission | Agent fails to perform a required step | Skips error handling when creating files with invalid paths |
| Wrong-Tool | Agent selects incorrect tool for the task | Uses `bash` instead of `edit` for file modifications |
| Loop | Agent repeats the same action without progress | Re-reads the same file 5+ times without acting |
| Timeout | Agent exceeds step budget without completion | 50+ turns on a task that should take 10 |

## Statistical Framework

### Effect Size Detection

For each defect category, compute Cohen's d between baseline and candidate:

```
d = (mean_candidate - mean_baseline) / pooled_std
```

Thresholds:
- d < 0.2: Negligible (no action)
- 0.2 ≤ d < 0.5: Small effect (investigate)
- 0.5 ≤ d < 0.8: Medium effect (block if negative direction)
- d ≥ 0.8: Large effect (block unconditionally)

### Required Sample Size

Minimum samples per condition for 80% power at α=0.05:

| Effect Size (d) | Required N |
|----------------|------------|
| 0.2 (small) | 394 |
| 0.5 (medium) | 64 |
| 0.8 (large) | 26 |

### SPRT Integration

AgentAssay can run as SPRT with categorical outcomes:

1. Define H₀: defect rates are equal across categories
2. Define H₁: any category has increased defect rate beyond δ
3. Run iteratively, compute log-likelihood ratio
4. Stop when crossing α or β boundary

## References

- AgentAssay: Defect Detection for AI Agents (2025), Evaluation Systems Conference
- Statistical Power Analysis for Behavioral Sciences, Cohen (1988)
