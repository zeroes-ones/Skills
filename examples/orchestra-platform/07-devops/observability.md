# Observability — Orchestra Platform

## Metrics

Orchestra uses a **federated Prometheus** architecture:

- **Cluster-level Prometheus** scrapes each EKS cluster independently (dev, staging, prod). Retention: 2 hours, no long-term storage.
- **Global Prometheus** federates from all cluster instances, aggregating cross-environment metrics. Retention: 13 months in Thanos-backed object storage.
- **Grafana** provides dashboards across two families:
  - **RED dashboards** (per service) — Rate of requests, Error rate, Duration (p50/p95/p99). Enables quick identification of which service is degraded.
  - **USE dashboards** (per node) — Utilization, Saturation, Errors for CPU, memory, disk I/O, and network throughput.

## Logs

All services emit **structured JSON logs** to stdout, collected by Promtail and stored in **Loki** with a 30-day retention policy. Log levels are environment-enforced at the sidecar level:

| Environment | Minimum Level | Rationale |
|---|---|---|
| dev | DEBUG | Full visibility for development |
| staging | INFO | Production-like behavior without noise |
| prod | WARN | Only actionable signals in production |

Structured fields include `trace_id`, `service`, `environment`, and `user_id` (hashed). PII never appears in log messages — it is redacted by the logging middleware before emission.

## Traces

Distributed tracing via **Tempo**, with **OpenTelemetry auto-instrumentation** across the stack:

- Go services — `otelgrpc` and `otelhttp` middleware
- Node.js services — `@opentelemetry/auto-instrumentations-node`
- React frontend — `@opentelemetry/sdk-trace-web` with W3C trace context propagation

**Sampling strategy**: 100% of error traces, 10% of successful traces. This captures every failure for debugging while controlling storage cost.

## Service Level Objectives (SLOs)

Orchestra maintains **12 SLOs** across its services. Key ones:

| SLO | Target | Error Budget (monthly) |
|---|---|---|
| API availability | 99.9% | 43.8 minutes |
| Template execution success rate | 99.5% | 219 minutes |
| API read latency (p95) | < 200ms | — |
| API write latency (p95) | < 500ms | — |
| Service catalog search latency (p95) | < 100ms | — |

## Alerts

Three-tier alert routing via Alertmanager → PagerDuty:

| Priority | Response | Example |
|---|---|---|
| **P1** | Page on-call engineer, 5-min ack SLA | API error rate > 5% for 5 min |
| **P2** | Page during business hours only | p95 latency exceeds SLO for 15 min |
| **P3** | Auto-create Jira ticket | Disk usage > 80% predicted in 7 days |

Every alert **must link to a runbook**. Alerts without runbooks are rejected at code review. The alert description includes a direct link to the relevant Grafana dashboard with the time range pre-selected.

## Dashboards

Three primary dashboards serve different audiences:

1. **Orchestra Overview** — golden signals (latency, traffic, errors, saturation) across all services. First screen on-call engineers check.
2. **Per Service RED** — one dashboard per microservice, drilled into request rate, error breakdown, and latency percentiles.
3. **Business Metrics** — template activations, executions per day, daily active users, and conversion funnel. Primarily for product and leadership.

> **Principle: Never alert on symptoms without a runbook. Dashboard must tell a story.**
