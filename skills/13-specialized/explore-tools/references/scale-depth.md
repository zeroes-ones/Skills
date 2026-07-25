## Operating at Different Levels

How tool selection criteria evolve as your organization and system grow.

| Dimension | Solo Developer | Small Team (2-10) | Medium (10-100) | Enterprise (100+) |
|-----------|---------------|-------------------|-----------------|-------------------|
| **Budget** | <$100/month total tools | $100-$1,000/month | $1,000-$10,000/month | $10,000-$100,000+/month |
| **Primary Concern** | Time-to-first-feature, learning curve | Team productivity, onboarding speed | Scalability, reliability, cost predictability | Compliance, SLA, security, vendor management |
| **Tool Complexity** | Simple, batteries-included, minimal config | Balance of power and simplicity | Specialized tools per domain, managed services | Enterprise-grade, SSO, audit logging, RBAC |
| **Hosting** | Vercel/Railway/Render free tiers | Managed PaaS (Railway, Fly.io, Render) | AWS/GCP managed services | Multi-cloud, private cloud, dedicated infrastructure |
| **Database** | SQLite, Supabase free, Neon free | Supabase, PlanetScale, Railway Postgres | AWS RDS Multi-AZ, Aurora | CockroachDB, Spanner, Oracle, enterprise contracts |
| **Auth** | NextAuth.js, Lucia Auth | Clerk free/startup, Supabase Auth | Auth0, WorkOS | Okta, Azure AD, Ping Identity, custom IdP |
| **Monitoring** | Console.log, Sentry free | Sentry, Grafana Cloud free | Datadog, New Relic, Grafana Cloud | Splunk, Datadog Enterprise, AppDynamics |
| **CI/CD** | GitHub Actions free tier | GitHub Actions, Vercel/GitHub integration | GitHub Actions + self-hosted runners, Buildkite | Jenkins, GitLab CI Enterprise, Harness, CircleCI Enterprise |
| **Support Need** | Self-support (docs, issues) | Community support (Discord, forums) | Vendor support (email/Slack) | Dedicated support, TAM, SLA-backed 24/7 |
| **Migration Cost** | Low (days) | Medium (weeks) | High (months) | Extreme (quarters to years) |
| **Decision Process** | Individual, instant | Team discussion, days | Cross-team review, weeks | RFP, legal review, security review, months |
| **Lock-in Tolerance** | High — easy to change | Medium — manageable with planning | Low — changes affect many teams | Very low — multi-year contracts, deep integration |

### Key Insight: The Tool-Cost Inversion Point

At small scale, free/OSS tools are cheap and engineering time is abundant. At enterprise scale, engineering time is expensive ($150-300/hr fully loaded) and tool costs are a rounding error. The inflection point is around 20-50 engineers.

**Solo/Small Team Rule:** Default to free/OSS. Engineering time is "free" (you're building anyway). A $50/month tool that saves 2 hours = $25/hour — likely worth it.
**Medium Team Rule:** Evaluate cost per engineer. A $500/month tool across a 50-person team = $10/person/month. If it saves 30 min/person/month, it pays for itself at $150/hr rates.
**Enterprise Rule:** Compliance, security, and reliability dominate. The cost of a breach ($4M+ average) or compliance failure ($20M GDPR fine) dwarfs any tool cost. Pay for enterprise-grade tools with SLAs, audits, and dedicated support.
