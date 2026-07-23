# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
Founder running experiments manually with a Google Sheet + Google Optimize free tier. Feature flags via environment variables or simple config toggles. Funnel analysis: Mixpanel/Amplitude free tier. No formal experimentation framework — ship and measure. Growth model: spreadsheet projections. Cost: $0-200/month. Overkill: server-side A/B framework, experiment platform (Eppo/Optimizely), full CDP, feature flag SaaS.

### Small (2-10 people, 100-10K users)
Dedicated growth engineer. A/B testing: LaunchDarkly/Flagsmith + custom or lightweight platform (GrowthBook open-source). Funnel analysis: Mixpanel/Amplitude with SQL access. Experimentation framework with hypothesis template and pre-registration. Feature flags for progressive rollouts. Growth model: Python/spreadsheet with weekly updates. Cost: $500-3K/month. Overkill: CDP (Segment), multivariate testing, multi-armed bandits.

### Medium (10-50 people, 10K-1M users)
Growth team (2-3 engineers). Experiment platform: Eppo, Statsig, or Optimizely with server-side + client-side. Feature flag platform with targeting rules, gradual rollouts, kill switches. CDP for unified user profiles. Multi-armed bandits for ongoing optimization. Statistical rigor: CUPED, sequential testing, stratified sampling. Growth model in Python with data warehouse integration. Cost: $5K-25K/month.

### Enterprise (50+ people, 1M+ users)
Growth engineering pod (5-10). Experiment platform with custom integrations, holdout groups, long-term effect measurement. Shadow deployments for ML models. Experiment interaction detection. Global feature flag management with change management. Dedicated experimentation data pipeline. Causal inference: diff-in-diff, IV, synthetic control. Growth model: real-time, ML-driven forecast. Cost: $50K-300K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | >2 experiments/month, need feature flags for production safety | Add LaunchDarkly/Flagsmith; implement hypothesis template; move beyond Google Optimize |
| Small → Medium | >10 experiments/month, need interaction detection, or >3 growth engineers | Adopt experiment platform (Eppo/Statsig); add CDP; implement advanced statistical methods |
| Medium → Enterprise | >50 experiments/month, ML-driven personalization, regulatory experimentation requirements | Build dedicated experimentation pipeline; add causal inference; implement holdout groups |
