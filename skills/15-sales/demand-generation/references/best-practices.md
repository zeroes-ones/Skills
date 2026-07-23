# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -- these rules encode years of wasted ad spend, broken attribution, and nurture sequences that annoyed everyone -->

- UTM hygiene is the foundation of all measurement. Enforce UTM parameters on every outbound link. Use `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` consistently. One missing parameter corrupts attribution for an entire campaign.
- Test ad creative in batches of 5 — kill anything with CTR <0.5% after $500 spend per platform. The best creative often isn't your first guess. Budget 20% of spend for testing.
- Never send identical nurture to everyone who downloads the same asset. Segment by persona, industry, and behavior. A CTO and a marketing manager downloading the same ebook need different follow-up.
- Lead scoring decays over time: a pricing page visit 6 months ago is not the same signal as one yesterday. Apply a 30-day recency decay: score reduces by 50% every 30 days of inactivity.
- MQL→SQL conversion rate <10% means either your scoring model is too generous or sales isn't following up. Audit 50 MQLs: why weren't they accepted or rejected? The answer tells you what to fix.
- Attribution windows matter enormously. A 30-day lookback credits very different channels than a 90-day. Pick one, document it, and don't change it quarter-to-quarter — consistency matters more than precision.
- Email nurture open rates are inflated by Apple Mail Privacy Protection. Look at click rate and conversion rate as primary metrics, not open rate. Open rate is directional at best.
- Holdout groups (10%) on every nurture sequence are non-negotiable. If the nurture doesn't produce statistically significant lift vs. doing nothing, kill it and redirect the effort.
- Use incrementality testing for paid channels: geo-holdout tests (ads in Region A, no ads in comparable Region B) tell you whether paid is creating demand or capturing demand that would have converted organically.
- Marketing automation migrations are more expensive than they appear. Budget 3x the platform cost for implementation, data migration, and training. A rushed migration corrupts data and breaks attribution for months.
