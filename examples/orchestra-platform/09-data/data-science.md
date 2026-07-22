# Orchestra Platform — A/B Test Analysis

**Experiment ID:** EXP-2026-042 | **Date:** July 7–20, 2026 | **Owner:** Data Science

## Experiment Overview

**Goal:** Improve template wizard completion rate.

**Hypothesis:** Adding a progress indicator and estimated completion time to the template creation wizard increases the completion rate from 68% (current baseline) to 75%.

## Experimental Design

| Parameter | Value |
|---|---|
| Randomization unit | User ID (hashed) |
| Split ratio | 50/50 (control/variant) |
| Sample size | n = 1,200 (600 per arm) |
| Duration | 14 days |
| Primary metric | Template completion rate |
| Guardrail metrics | Time-to-create, error rate, NPS survey response |

## Results

| Metric | Control | Variant | Δ | p-value | Sig? |
|---|---|---|---|---|---|
| Completion rate | 68.3% (410/600) | 74.2% (445/600) | +5.9pp (+8.7%) | 0.031 | ✅ |
| Time-to-create (mean) | 14.2 min | 14.5 min | +0.3 min | 0.42 | ❌ |
| Error rate | 3.1% | 2.9% | −0.2pp | 0.61 | ❌ |
| NPS | 42 | 43 | +1 | 0.38 | ❌ |

- **95% confidence interval for lift:** [+0.5pp, +11.2pp]
- **Statistical power:** 83% (target: 80%) — experiment sufficiently powered

## Guardrail Assessment

All guardrail metrics show no statistically significant degradation. Time-to-create, error rate, and NPS remain functionally unchanged. No negative user experience signals detected.

## Recommendation

**Ship to 100% of users.** Monitor completion rate daily for 2 weeks post-launch with an automatic alert if it drops below 65%.

## Important Caveat

> **Correlation is not causation.** The variant changed both the progress indicator AND the button color (gray → blue). We cannot isolate which change drove the improvement. Recommend a follow-up experiment: keep the progress indicator, A/B test button color independently.

## Supplementary Analysis

- Churn prediction model (notebook: `notebooks/churn-prediction-v2.ipynb`)
- Time-to-value analysis segmented by template type (notebook: `notebooks/time-to-value-v3.ipynb`)

---

*Analysis performed in Jupyter; raw data available in `s3://orchestra-experiments/exp-2026-042/`.*
