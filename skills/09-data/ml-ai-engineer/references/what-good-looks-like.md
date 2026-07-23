# What Good Looks Like — Full Quality Standard

Every training run is reproducible: pinned dependencies, versioned datasets, seeded randomness, and a logged git hash. The evaluation harness catches regressions across every slice before deployment, and the model registry gates promotion from staging to production with automated A/B validation. Drift monitoring fires a retrain pipeline before prediction quality degrades below threshold, and model cards document intended use, limitations, and fairness evaluations for every production model. A new ML engineer can reproduce a six-month-old experiment in under an hour.

> This is the full aspirational quality standard. The compressed version in SKILL.md is optimized for model token budgets.
