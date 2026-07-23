# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- Run AA tests on every new experiment configuration before launching real tests — ensure no systemic bias in randomization.
- Never stop an experiment early based on "significance trending" — pre-commit to runtime based on sample size calculations.
- Segment experiment results by platform, geography, and user type — aggregate lift can hide heterogeneous treatment effects.
- Maintain a single source of truth for metrics definitions (metrics layer like dbt or Looker explores).
- Ship "losing" variants when they teach something fundamental about user behavior — the goal is learning, not just winning.
- Use holdout groups (control groups that never see the treatment for extended periods) to measure long-term effects invisible in short experiments.
- Implement circuit breakers on all external growth loops: rate limiting, fraud thresholds, automated kill on anomaly detection.
- Growth model should be a living document — update monthly with actuals and reforecast.
