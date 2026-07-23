# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: Data scientist = you also do data engineering, analytics, and ML. Focus on fast, directional analyses. Jupyter notebooks are fine. Statistical rigor: report p-values but don't obsess over power analysis. Models are proof-of-concept.
- **What to skip**: Power analysis for every test. Formal experiment documentation. Separate training/serving infrastructure. Model monitoring and drift detection. Multiple comparison corrections for exploratory analyses.
- **Coordination**: Self-contained. Share results as notebook exports or 2-pager memos.
- **Cost**: Free — use Python (scipy, statsmodels, scikit-learn), Jupyter, and Google Colab.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Basic experiment platform (growth tool, feature flag service). Statistical rigor: power analysis before all experiments, SRM checks, CUPED. Peer review of experiment designs before launch. Model versioning with Git. Result documentation in shared knowledge base.
- **What to skip**: Full MLOps pipeline. Experimentation platform (use feature flags + SQL). Causal inference for every question (A/B test when possible).
- **Coordination**: Weekly experiment review. Coordinate with data engineer for pipeline reliability. Share experiment calendar to avoid interaction effects.
- **Cost**: $0-500/month for BI tools. Time: 1-2 days per experiment from design to decision.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated experimentation platform with automated SRM, sequential testing, CUPED. Full MLOps for production models. Experimentation culture: quarterly planning, experiment review board. Model governance: fairness audits, documentation for compliance. Advanced causal inference for non-randomizable questions.
- **What to skip**: Real-time model serving (batch is fine for most). Custom experimentation platform (use off-the-shelf). Bayesian methods everywhere (frequentist is adequate for most).
- **Coordination**: Bi-weekly experiment review board. Data science guild for methodology standards. Coordinate with compliance for model risk management.
- **Cost**: $2K-10K/month (experimentation platform, compute). Dedicated experimentation PM.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Tiered experimentation (exploratory → canary → holdout → full launch). Model risk management framework. Centralized feature store connecting experiments to production models. Data science platform with shared compute, versioned environments, and reproducibility guarantees. Cross-team experiment interference detection. Federated learning for privacy-sensitive use cases.
- **What's full production**: Experimentation center of excellence. Model cards for all production models. Ethical AI review board. Counterfactual evaluation framework. Data science on-call rotation for critical models.
- **Coordination**: Monthly experiment governance board. Cross-functional model review (legal, compliance, product, engineering). Quarterly methodology audit.
- **Cost**: $50K-200K+/month (platform, compute, dedicated experimentation team, governance).

### Transition Triggers
- **Solo → Small**: Second analyst joins. >100 users making predictive models valuable. First revenue-impacting experiment.
- **Small → Medium**: 5+ parallel experiments. First production model serving customers. Compliance requirements appear.
- **Medium → Enterprise**: 20+ data scientists. Model risk management required by regulation. Cross-team experiment interference observed.
