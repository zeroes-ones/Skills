# Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Feature flags | Environment variables or JSON config in DB | LaunchDarkly ($75/mo starter) or Flagsmith (self-hosted free) | >5 flags, need non-engineer toggling, or need % rollouts |
| A/B testing | Custom: hash(user_id) % 2 → variant, log to analytics | LaunchDarkly experiments, GrowthBook (self-hosted free, cloud $99/mo) | >1 experiment/month, need statistical engine, or non-engineers run tests |
| Analytics | PostHog (self-hosted free, cloud $0.00031/event) or Plausible ($9/mo) | Amplitude ($800+/mo) or Mixpanel Growth ($20/mo startup) | Need behavioral cohorts, funnel analysis beyond basic funnels, or >1M events/mo |
| Event pipeline | Manual Segment/RudderStack setup | Segment Team ($120/mo) or RudderStack Cloud (free up to 1M events) | >5 event destinations or need warehouse sync |
| Experiment analysis | Google Sheets + manual t-test | GrowthBook (open source), Statsig (free up to 10K MTUs) | >2 experiments/month, need CUPED/bootstrap/pre-registration |
| Growth model | Google Sheets with cohort tables | Python/Jupyter notebook with automated data pull | Model has >20 inputs or updated monthly (worth automation) |
| Referral/viral | Custom: invite codes, reward via DB flag + API call | ReferralRock ($200/mo) or FriendBuy ($299/mo) | Need fraud detection, multi-language, or A/B testing referral mechanics |

**Annual growth tool budget:** MVP: $0-240. Growth: $1K-15K. Scale: $30K-200K+.
