# MVP vs Growth vs Scale

| Phase | Team Size | Users | Priority | Growth Approach |
|-------|-----------|-------|----------|----------------|
| **MVP (0→1)** | 1-3 devs, no growth hire | 0-1K | Find first 100 passionate users | Manual outreach + analytics (Plausible/PostHog free) + basic email. No A/B tests — just ship and watch retention. Feature flags: env vars or a JSON config. |
| **Growth (1→10)** | 3-10 devs, 1 growth engineer | 1K-100K | Systematic experimentation | Server-side feature flags (LaunchDarkly free tier or Flagr), A/B testing framework, event taxonomy, growth model spreadsheet. Weekly experiment review. |
| **Scale (10→N)** | 10+ devs, growth team (3-5) | 100K+ | Experimentation culture + automation | Full experimentation platform, ML-powered personalization, automated experiment analysis, dedicated data engineering, holdout groups, multi-arm bandits. |

**MVP rule:** Ship a feature flag in 2 hours (env var + if statement), not 2 weeks (platform evaluation + integration). Upgrade tooling when you've run 10+ manual experiments and the overhead is visible.
