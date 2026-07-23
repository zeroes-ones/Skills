# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person) → Small (2-10) → Medium (10-50) → Enterprise (50+)

| Dimension | Solo | Small | Medium | Enterprise |
|-----------|------|-------|--------|------------|
| **Monitoring** | Server logs + `htop` | Datadog free tier / Signoz | Full APM + RUM + distributed tracing | SLO dashboards + burn-rate alerts + anomaly detection |
| **Profiling** | None (fix if slow) | Ad-hoc pprof/py-spy for top 3 endpoints | Always-on profiler (Datadog CP) | Continuous profiling across all hosts |
| **Load Testing** | curl in a loop | k6 manual run before launch | k6 in CI on PRs | Geo-distributed load generation + regression gating |
| **Caching** | None | Redis on app server for hot queries | Redis HA + CDN + multi-layer | Redis cluster + edge caching + cache warming |
| **Database** | Single instance | Index tuning + EXPLAIN ANALYZE | Read replicas + PgBouncer + pganalyze | Sharded DB + automated index recommendations |
| **Frontend** | No optimization | Lighthouse check before deploy | Lighthouse CI + bundle budgets | RUM + per-page monitoring + trend alerts |
| **SLOs** | "It works" | Latency targets on critical paths | Formal SLOs with error budgets | Multi-tier SLOs with business-level objectives |
| **Team** | Devs fix if slow | 1 backend specialist | Performance/infra team (2-3) | Dedicated performance team (4+) |

### Transition Triggers

| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | P95 >1s on user-facing endpoint | Add APM, start manual profiling, add Redis for hot queries |
| Small → Medium | >10 services, P95 regression caught late | APM on all services, k6 in CI, SLOs with alerts, formal perf budget |
| Medium → Enterprise | >50 services, perf issues cause revenue loss | Geo-distributed load testing, continuous profiling, business-level SLOs |
