# LLM-as-Judge Calibration

## Calibration Protocol

1. Select 100+ representative agent outputs
2. Have 2-3 human experts grade independently
3. Compute inter-rater reliability (Cohen's κ or Krippendorff's α)
4. Have LLM judge grade same outputs
5. Compute LLM-human agreement
6. If κ < 0.7: refine rubric, retry
7. If κ ≥ 0.7: LLM judge is calibrated

## Common Calibration Failures
- **Verbosity bias:** LLM prefers longer outputs regardless of quality
- **Style over substance:** Well-formatted wrong answer scores higher than correct but messy
- **Novelty penalty:** Creative solutions scored lower than conventional ones
- **Position bias:** First output in comparison scored higher
- **Self-enhancement:** LLM prefers outputs from same model family

## Mitigation Strategies
- Blind grading (no model attribution)
- Randomized output order
- Multi-dimensional rubric (separate correctness from style)
- Regular re-calibration (weekly or per-model-change)
