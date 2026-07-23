# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You deploy a model by SSH-ing into the prod server, `scp`-ing a `.pkl` file, and restarting the service manually | Models are deployed via CI/CD with automated validation gates, canary rollouts, and < 5-minute rollback — and you haven't manually touched a production model in 6 months | You've reduced the time from model training completion to production deployment from 2 weeks to under 4 hours, and you can prove it with DORA metrics that track ML-specific lead time |
| You discover training-serving skew when users report bad predictions — days or weeks after deployment | Your monitoring detects feature drift (PSI > 0.25) within 4 hours and your incident response either recalibrates the model or rolls back automatically | You've designed a feature store architecture where point-in-time correctness is mathematically guaranteed (not just tested), and the proof is in the data model, not in a runbook |
| Your GPU costs are "whatever AWS billed us this month" — you discover cost anomalies in the invoice, not in a dashboard | You have per-model cost attribution, budget alerts, and GPU right-sizing that keeps costs within 10% of projected — and you can explain any variance | You've reduced organization-wide ML infrastructure costs by 40%+ while maintaining or improving model SLAs — and the CFO cites your cost attribution system as the standard for other engineering teams |

**The Litmus Test:** Delete your production model. Delete the Docker image. Delete the feature values in the online store. Can you rebuild the exact same model (same weights, same features, same performance) from your experiment tracker, feature store, and CI/CD pipeline within 2 hours? If you can't — if part of the model's "secret sauce" exists only in a data scientist's laptop — you have a deployment system, not an MLOps practice. Reproducibility is the difference between engineering and alchemy. A model that can't be rebuilt from source is a liability with an expiration date.
