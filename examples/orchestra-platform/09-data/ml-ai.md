# Orchestra Platform — ML/AI Feature Design

**Owner:** ML Engineering | **Date:** 2026-07-21 | **Status:** Prototype → Beta

## Feature 1: Template Recommendations

**Approach:** Collaborative filtering using a user-item matrix with features: team size, primary tech stack, industry vertical → template ID.

**Training data:** 5,000 template executions collected over 6 months, filtered for completions only (excludes abandoned wizards).

**Deployment:** FastAPI microservice (`template-recommender`), deployed behind the `ai-recommendations` LaunchDarkly flag.

**Performance:**

| Metric | Score | Threshold |
|---|---|---|
| Precision@5 | 0.72 | > 0.65 |
| Recall@5 | 0.68 | > 0.60 |
| Mean Reciprocal Rank (MRR) | 0.81 | > 0.75 |

**Cold start mitigation:** New users (< 5 interactions) receive popularity-based fallback recommendations from the most-executed templates in their organization's industry segment.

## Feature 2: Service Description Generator

**Model:** Fine-tuned Llama 3 (8B parameters) on 2,000 human-written service descriptions from the Orchestra catalog. Prompt template:

> *"Write a 2-sentence description for a service called {name} of type {template_type} used by {team_name}."*

**Guardrails:** Output validated against max length (200 characters), profanity/toxicity filter, and prohibited term list. Any guardrail violation triggers a generic fallback description.

**Deployment:** Internal API endpoint — not directly exposed to end users. Called by the template wizard on the final confirmation step.

## Monitoring & Maintenance

- **Drift detection:** Recommendation click-through rate monitored daily. Alert triggers if 7-day rolling average drops >20% below baseline.
- **Retraining cadence:** Model retrained every 2 weeks on accumulated interaction data.
- **Shadow deployment:** New model versions run in shadow mode for 3 days; predictions logged but not served until validated against prior version.

## Bias Documentation

> Template recommendations may over-represent popular tech stacks (Node.js, React, PostgreSQL) due to training data class imbalance. Niche stacks (Elixir, Svelte, CockroachDB) appear in fewer training examples and may receive lower recommendation scores. Fairness is monitored across 10 tech stack categories — we track recommendation distribution parity monthly.

## Engineering Principle

> **Never deploy a model without drift monitoring.** Training data bias propagates to predictions. Without monitoring, you will not know when your model starts failing.

---

*Model cards and training run logs in `ml/training-runs/`. Deployment configs in `infra/k8s/template-recommender/`.*
