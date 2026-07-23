# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Tag everything**: `team`, `service`, `environment`, `region` on all metrics for consistent drill-down and cost attribution.
- **RED over USE for alerts** — User-facing symptoms (error rate, latency) trump infrastructure causes (high CPU, low disk).
- **One dashboard per service, ≤ 12 panels** — Focused, scannable. Use drill-down links for detail, not infinite scrolling.
- **Recording rules for expensive PromQL** — Pre-compute percentiles, aggregations, and joins. Reduce dashboard load time from 30s to < 1s.
- **Trace all async boundaries** — Span links for Kafka messages, background jobs, cron tasks. Without this, traces break at async boundaries.
- **Dashboard as code** — Terraform Grafana provider, Grafonnet, or JSON in Git. No click-ops dashboard creation.
- **Log with context, not just messages** — Every log line should enable <!-- DEEP: 10+min -->
debugging without additional queries. Include `trace_id`, `user_id` (hashed), `order_id`, `error.stack`.
- **Alert on burn rate, not SLO compliance** — SLO is a 28-day window; by the time it drops, budget is exhausted. Burn rate gives early warning.
- **Monthly fire-drills** — Test the full alerting chain: synthetic failure → Prometheus alert → Alertmanager → PagerDuty → on-call acknowledges → runbook followed.
