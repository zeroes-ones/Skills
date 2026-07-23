# Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| APM / monitoring | Datadog free tier (1-day retention) or Signoz (self-hosted OSS) | Datadog APM ($31/host/mo) or New Relic ($0.30/GB) | Need >1-day retention, custom dashboards, or alerting |
| Profiling | `pprof` (Go), `py-spy` (Python), Chrome DevTools (JS) — all free | Datadog Continuous Profiler ($12/host/mo) | Need always-on profiling across all hosts, not ad-hoc |
| Load testing | k6 (free OSS) or Artillery (free OSS) | k6 Cloud ($50/mo) or Gatling Enterprise | Need managed test execution, geo-distributed load generation, or >100K VUs |
| Caching | Redis (self-hosted on app server, free) | Redis Cloud ($25/mo) or Elasticache | Need HA, managed failover, or >1GB datasets |
| CDN | CloudFlare free / Fastly free tier (up to $50 credit) | CloudFlare Pro ($20/mo) or Fastly | Need WAF, image optimization, or custom edge logic |
| Database optimization | EXPLAIN ANALYZE (free) + manual tuning | pganalyze ($99/mo) or SolarWinds DPA ($2K+) | >10 database instances or need automated index recommendations |
| Frontend performance | Lighthouse (free) + webpack-bundle-analyzer (free) | Calibre ($80/mo) or DebugBear ($49/mo) | Need per-page monitoring, CI integration, or trend alerts |

**Annual performance tool budget by phase:** MVP: $0. Growth: $0-5K. Scale: $10K-100K.
