# Scale Depth: Solo → Small → Medium → Enterprise — Marketplace Platform Builder

### Solo (1 person, 0-100 users)
- **Stack**: What you know best. Speed matters more than optimal tech. Managed services to avoid ops burden.
- **Database**: SQLite dev, managed Postgres prod (Render/Railway/Supabase free tier).
- **Deployment**: Single server or serverless. Vercel/Render/Railway web, App Store mobile.
- **Monitoring**: Uptime (Better Uptime), errors (Sentry free), analytics (Plausible/PostHog).
- **Key constraint**: Your time. Automate everything. Sleep is important.

### Small Team (2-5 people, 100-1,000 users)
- **Stack**: Standardize language/framework. CI/CD pipeline. Code review mandatory.
- **Database**: Managed with automated backups. Connection pooling. Read replicas if needed.
- **Deployment**: Staging mirrors production. Feature flags for gradual rollouts.
- **Monitoring**: APM added. Alerts for error rate spikes and latency degradation.
- **Key constraint**: Coordination. Clear ownership. Document in ADRs.

### Growing (5-20 people, 1,000-50,000 users)
- **Stack**: Microservices for independent deployables. Default to modular monolith.
- **Database**: Per-service or per-domain DB. Read/write splitting. Redis caching.
- **Deployment**: Blue-green/canary. Automated rollback. Load testing before releases.
- **Monitoring**: Full observability. SLOs with error budgets. On-call with runbooks.
- **Key constraint**: Complexity. "You build it, you run it."

### Enterprise (20+ people, 50,000+ users)
- **Stack**: Platform team paved roads. Service mesh. Multi-region.
- **Database**: Sharded. Event sourcing for audit. Data warehouse for analytics.
- **Deployment**: Multi-region geographic routing. Chaos engineering. SOC 2/ISO 27001.
- **Monitoring**: Dedicated observability team. Anomaly detection. 12-month capacity planning.
- **Key constraint**: Organizational complexity. API contracts between teams.
