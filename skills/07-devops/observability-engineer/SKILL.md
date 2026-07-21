---
name: observability-engineer
description: Metrics, logs, traces integration, SLO/SLI/error budget framework, Prometheus/Grafana/Loki/Tempo, OpenTelemetry, dashboard design (USE/RED/golden signals), alert design, and incident response. Triggered by observability, monitoring, prometheus, grafana, SLO, alert, dashboard, golden signals, tracing, opentelemetry.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - observability-engineer
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Observability Engineer

Design, implement, and operate observability systems that deliver actionable insight into system
health, performance, and user experience. This skill unifies the three pillars — metrics, logs,
traces — through SLO-based alerting, meaningful dashboards, and incident-ready runbooks. Deep
coverage of OpenTelemetry instrumentation, Prometheus recording/alerting rules, Grafana dashboard
provisioning, Loki log aggregation, and Tempo distributed tracing.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Instrument a service with metrics → Jump to "Core Workflow > Phase 1" (Instrumentation) and "Sub-Skills > metrics-instrumentation"
├── Set up a logging pipeline → Go to "Core Workflow > Phase 2" (Logging) and "Sub-Skills > log-aggregation"
├── Implement distributed tracing → Jump to "Core Workflow > Phase 3" (Tracing) and "Sub-Skills > distributed-tracing"
├── Design a dashboard (RED/USE/Golden Signals) → Go to "Core Workflow > Phase 4" (Dashboards) and "Best Practices > Dashboard Design"
├── Configure alerts (SLO-based, multi-window burn rate) → Jump to "Core Workflow > Phase 5" (Alerting) and "Best Practices > Alert Design"
├── Define SLOs and error budgets → Go to "Decision Trees > SLO Definition" and "Core Workflow > Phase 5"
└── Not sure where to start? → "Core Workflow > Phase 1" — instrumentation comes first; you can't observe what you don't measure
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never alert on symptoms without a runbook.** If the alert fires and the on-call engineer has no documented steps to diagnose and mitigate, it's not an alert — it's noise that wakes someone up.
- **Dashboards must tell a story, not just show numbers.** Every dashboard should answer a specific question: "Is the service healthy?", "Where is latency coming from?", "Are we within SLO?" A grid of random graphs helps no one.
- **Logs need structure (JSON).** Free-form text logs are impossible to query at scale. Every log line must be structured (JSON) with consistent field names and types across services.
- **Cardinality kills metrics — watch label values.** A metric label with user IDs, request IDs, or full URLs creates a new time series for every unique value. Use high-cardinality data in logs/traces, not metrics.
- **Always define what "normal" looks like before alerting.** Threshold-based alerts without understanding baseline patterns generate false positives. Use anomaly detection or multi-window burn rates where possible.
- **Admit what you don't know.** If you're unfamiliar with a specific observability backend (Datadog, New Relic, Honeycomb), say so and stick to the principles — the tools change, the concepts don't.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Instrumenting services with OpenTelemetry SDKs for unified metrics, traces, and structured logs
- Designing SLOs, SLIs, and error budgets for critical user journeys with multi-window burn rate alerting
- Building tiered Grafana dashboards from RED (Rate-Errors-Duration) and USE (Utilization-Saturation-Errors) methods
- Setting up log aggregation pipelines with Grafana Loki or Elasticsearch, including retention policies and PII redaction
- Deploying distributed tracing with Grafana Tempo or Jaeger, including sampling strategies and span design
- Defining alerting rules with Alertmanager → PagerDuty routing, on-call escalation, and alert fatigue prevention
- Correlating metrics → traces → logs via exemplars and trace_id injection
- Establishing observability as code: dashboards, alerts, recording rules in Git

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Metrics Backend: Prometheus vs SaaS
```
                     ┌──────────────────────────┐
                     │ START: Metrics collection  │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Team <5 AND monthly budget  │
                    │ <$500 for observability?    │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Self-hosted │   │ >500 nodes /    │
                    │ Prometheus  │   │ 10M active      │
                    │ + Grafana   │   │ series?         │
                    │ (free, ops  │   └────┬────────┬───┘
                    │  overhead)  │        │ YES    │ NO
                    └─────────────┘   ┌────▼────┐ ┌▼──────────┐
                                      │ SaaS    │ │ Prometheus │
                                      │ (Datadog│ │ + Thanos/  │
                                      │ /Grafana│ │ Mimir for  │
                                      │ Cloud)  │ │ scale      │
                                      └─────────┘ └────────────┘
```
**When to choose Self-Hosted Prometheus:** Budget <$500/month, <500 nodes, <10M active series, team has ops capacity (2-4 hrs/week). **When to choose SaaS:** >500 nodes, >10M series, no ops capacity, need integrated APM + logs + traces, budget >$2K/month. **When to choose Prometheus+Thanos:** Scale beyond single Prometheus but budget-constrained, 10M-100M series, team can manage distributed TSDB.

### Log Aggregation: Loki vs Elasticsearch
```
                     ┌──────────────────────────┐
                     │ START: Log aggregation     │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Need full-text search AND   │
                    │ complex aggregations?       │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Elasticsearch│  │ Grafana Loki    │
                    │ (powerful    │   │ (label-based,   │
                    │  search,     │   │  S3-backed,     │
                    │  higher ops) │   │  lower ops)     │
                    └─────────────┘   └────────────────┘
```
**When to choose Loki:** K8s-native, label-based indexing sufficient, want S3-backed storage, budget <$1K/month, already using Grafana. **When to choose Elasticsearch:** Full-text log search required, complex aggregations (e.g., business analytics on logs), team has ES expertise, budget >$2K/month.

### Alert Severity Classification
```
                     ┌──────────────────────────┐
                     │ START: New alert condition │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ User-facing functionality   │
                    │ is broken or degraded?      │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ CRITICAL    │   │ Will cause user  │
                    │ (page on-   │   │ impact in <2hr   │
                    │ call, <5min │   │ if unaddressed?  │
                    │ ack)        │   └────┬────────┬───┘
                    └─────────────┘        │ YES    │ NO
                                      ┌────▼────┐ ┌▼──────────┐
                                      │ WARNING │ │ INFO       │
                                      │ (page   │ │ (dashboard │
                                      │ business│ │ or ticket,  │
                                      │ hours)  │ │ no page)    │
                                      └─────────┘ └────────────┘
```
**When to set CRITICAL:** User-facing broken, error budget burning >10% in 1hr, revenue impact, page on-call with <5min ack SLA. **When to set WARNING:** Error budget burning >5% in 6hr, approaching threshold, page during business hours only. **When to set INFO:** Trend anomaly, no immediate user impact, dashboard-only, auto-generate ticket.

### Dashboard Design: RED vs USE vs Golden Signals
```
                     ┌──────────────────────────┐
                     │ START: Dashboard for a     │
                     │ service or resource        │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Monitoring a service (API,  │
                    │ worker, consumer)?          │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ RED Method  │   │ USE Method      │
                    │ (Rate,      │   │ (Utilization,   │
                    │  Errors,    │   │  Saturation,    │
                    │  Duration)  │   │  Errors) for    │
                    │ + Golden    │   │ infra resources │
                    │ Signals     │   │ (CPU, mem, disk)│
                    └─────────────┘   └────────────────┘
```
**When to use RED:** Every service endpoint — Rate (req/sec), Errors (5xx %), Duration (p50/p95/p99 latency). Add Golden Signals: traffic, latency, errors, saturation. **When to use USE:** Infrastructure — CPU utilization, memory saturation (OOM risk), disk I/O errors, network packet drops.

### Tracing Sampling Strategy
```
                     ┌──────────────────────────┐
                     │ START: Sampling strategy   │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ >10K spans/sec AND budget   │
                    │ <$1K/month for tracing?     │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Tail-based  │   │ Head-based      │
                    │ sampling    │   │ sampling (10-   │
                    │ (keep 100%  │   │ 50% rate, keep  │
                    │  of errors  │   │ all at lower    │
                    │  + slow     │   │ throughput)     │
                    │  traces)    │   └────────────────┘
                    └─────────────┘
```
**When to choose Tail-Based:** >10K spans/sec, need 100% error/slow traces, budget-constrained, can deploy OpenTelemetry Collector with tail sampling processor. **When to choose Head-Based:** <10K spans/sec, simpler to implement, 10-50% sampling rate sufficient, no Collector deployment desired.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Observability Strategy & SLO Framework

1. **Critical User Journey Identification** — Not every endpoint. Identify the 3-5 journeys that directly deliver user value (login, search, checkout, content feed, API). Each journey gets its own SLI + SLO.

2. **SLI Definition Patterns**:

   | SLI Type | Definition | PromQL Example |
   |---|---|---|
   | **Availability** | Proportion of successful requests | `sum(rate(http_requests{status!~"5.."}[28d])) / sum(rate(http_requests[28d]))` |
   | **Latency** | Proportion faster than threshold | `sum(rate(duration_bucket{le="0.3"}[28d])) / sum(rate(duration_count[28d]))` |
   | **Throughput** | Successful requests per second | `rate(http_requests{status!~"5.."}[5m])` |
   | **Freshness** | Data age vs expected | `time() - max(updated_at)` |
   | **Durability** | Write persistence rate | `writes_acknowledged / writes_attempted` |

3. **SLO Target Selection**:

   | SLO | Allowed Downtime (30 days) | Use Case |
   |---|---|---|
   | 99.9% | 43.2 min | Internal tools, batch processing |
   | 99.95% | 21.6 min | Customer-facing, non-critical |
   | 99.99% | 4.3 min | Payment, auth, critical API |
   | 99.999% | 26 sec | Financial settlement, life-safety |

   **Anti-patterns**: 100% SLO (impossible), SLO = current performance (no improvement), one SLO per service (undifferentiated), no error budget policy (wish, not commitment).

4. **Error Budget Policy** — Define what happens when budget depletes:
   ```
   Budget ≥ 50%: Normal operations, feature deploys allowed
   Budget 20-50%: Riskier deploys blocked, prioritize reliability
   Budget 5-20%: All feature deploys blocked, reliability-only
   Budget < 5%: Full freeze, notify VP Engineering
   ```


**What good looks like:** Every service emits structured logs, metrics, and traces. Grafana dashboard shows RED metrics (Rate/Errors/Duration) per service. Alert fires within 60 seconds of SLO violation. p99 latency tracked and trended weekly.

5. **Stack Selection Decision**:
   ```
   Self-managed?
   ├─ YES → Prometheus + Grafana + Loki + Tempo (OSS Grafana stack)
   │   ├─ HA Prometheus: Thanos or Grafana Mimir
   │   └─ Best for: Control, cost predictability, Kubernetes-native
   └─ NO → Managed/SaaS
       ├─ Grafana Cloud, Datadog, Honeycomb, New Relic
       └─ Best for: Small team, rapid onboarding, reduced ops burden
   ```

### Phase 2 (~30 min): Metrics & Dashboard Design

1. **USE Method — Infrastructure Resources**

   For every resource (CPU, memory, disk, network):

   | Resource | Utilization | Saturation | Errors |
   |---|---|---|---|
   | CPU | `100 - (avg(rate(cpu_idle[5m])) * 100)` | `node_load1 / count(cpu_cores)` at load > cores×2 | CPU throttling count > 0 |
   | Memory | `(1 - mem_available/mem_total) * 100` | Swap usage > 0 | OOM kills `increase(oom_kill[5m]) > 0` |
   | Disk | `(1 - disk_free/disk_total) * 100` | I/O wait > 30% | Read/write errors > 0 |
   | Network | `rate(bytes_transmitted[5m]) * 8 / link_speed` | Dropped packets > 0 | Interface errors > 0 |

2. **RED Method — Service Endpoints**

   For every service endpoint:

   ```promql
   # Rate — anomaly detection: request rate drops >50% from 1h ago
   rate(http_requests_total[5m]) / rate(http_requests_total[5m] offset 1h) < 0.5

   # Errors — error rate > 1% for 5 min
   sum(rate(http_requests{status=~"5.."}[5m])) / sum(rate(http_requests[5m])) > 0.01

   # Duration — P99 latency > 500ms for 5 min
   histogram_quantile(0.99, sum(rate(duration_bucket[5m])) by (le)) > 0.5
   ```

3. **Four Golden Signals** — Monitor at edge AND per service:
   - **Latency**: Time to service a request. Distinguish successful vs error latency.
   - **Traffic**: Demand on the system (requests/sec, concurrent sessions).
   - **Errors**: Failed requests — explicit (500), implicit (200 with wrong content), policy (over-quota).
   - **Saturation**: How "full" the service is. CPU, memory, I/O, queue depth, connection pool utilization.

4. **Tiered Dashboard Design**:
   ```
   Level 1: SLO Compliance Dashboard (executive) — Are we meeting commitments?
   Level 2: Service Dashboard (per-team) — RED metrics per endpoint, error budget burn-down
   Level 3: Infrastructure Dashboard (platform) — USE metrics per node/cluster
   Level 4: Drill-Down Dashboard (on-call) — Detailed request traces, log correlation
   ```

5. **Recording Rules** — Pre-compute expensive PromQL for dashboards:
   ```yaml
   groups:
     - name: service-recording-rules
       rules:
         - record: job:http_requests:rate5m
           expr: rate(http_requests_total[5m])
         - record: job:http_errors:rate5m
           expr: rate(http_requests_total{status=~"5.."}[5m])
         - record: job:http_error_rate:ratio5m
           expr: |
             sum(job:http_errors:rate5m) / sum(job:http_requests:rate5m)
         - record: job:http_latency:p99_5m
           expr: |
             histogram_quantile(0.99,
               sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job))
   ```

6. **Dashboard as Code** — Grafana provisioning via Terraform or Grafonnet:
   ```hcl
   resource "grafana_dashboard" "service_overview" {
     config_json = jsonencode({
       title = "Service Overview — ${var.service_name}"
       panels = [ ... ]
     })
   }
   ```

### Phase 3 (~20 min): Log Aggregation & Analysis

1. **Structured Logging Standard** — Every log line MUST include:
   ```json
   {
     "timestamp": "2026-07-21T14:32:00.123Z",
     "level": "INFO",
     "service": "checkout-service",
     "trace_id": "0af7651916cd43dd8448eb211c80319c",
     "span_id": "b7ad6b7169203331",
     "message": "Order processed",
     "context": {
       "order_id": "ord_abc123",
       "amount": 99.99,
       "duration_ms": 245
     }
   }
   ```

2. **Log Agent Selection**:
   | Agent | Strengths | Best For |
   |---|---|---|
   | **Promtail** | Native Loki integration, Kubernetes discovery, pipeline stages | Loki deployments |
   | **Fluent Bit** | Lightweight (~450KB), high throughput, 30+ plugins | High-volume, resource-constrained |
   | **Vector** | Ultra-fast (Rust), unified logs+metrics, programmable transforms | Performance-critical, unified pipeline |

3. **Loki Architecture** — Index-free design: labels for metadata, log content is full-text searchable:
   ```
   Write path: Promtail → Distributor → Ingester → Object Storage (S3/GCS)
   Read path:  Querier ← Ingester + Object Storage → Grafana
   ```
   Key config: `chunk_block_size`, `chunk_target_size`, `max_chunk_age`, retention via `table_manager.retention_period`.

4. **Retention Tiers & Cost Control**:
   | Tier | Retention | Storage | Query Speed |
   |---|---|---|---|
   | Hot | 7 days | SSD/Provisioned IOPS | < 1 second |
   | Warm | 30-90 days | Object storage | < 5 seconds |
   | Cold/Archive | 1-7 years | Glacier/Archive tier | Minutes to hours |
   | Compliance | 7+ years | WORM (Write Once Read Many) | Hours |

5. **PII Redaction in Logs** — Process at collection time:
   ```yaml
   # Promtail pipeline stage — redact email patterns
   - stages:
       - replace:
           expression: '([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
           replace: '[REDACTED_EMAIL]'
       - replace:
           expression: '(\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b)'
           replace: '[REDACTED_CC]'
   ```

6. **Log-Based Metrics** — Derive metrics from log streams:
   ```logql
   # Error rate by endpoint from logs
   sum by (endpoint) (rate({service="api"} | json | level = "ERROR" [5m]))

   # P95 response duration from access logs
   histogram_quantile(0.95,
     sum by (le) (rate({service="nginx"} | json | unwrap duration_ms [5m])))
   ```

### Phase 4 (~15 min): Distributed Tracing

1. **OpenTelemetry Architecture**:
   ```
   Application (OTel SDK) → OTLP → Collector Agent (DaemonSet) → Collector Gateway → Tempo
   ```

2. **Sampling Strategy** — The most critical tracing decision:
   | Strategy | When | Config |
   |---|---|---|
   | **Head, Probabilistic 10%** | Always enabled, SDK-level | `TraceIdRatioBased(0.1)` |
   | **Tail, 100% errors** | Gateway-level | `tail_sampling: status_code: [ERROR]` |
   | **Tail, latency > 500ms** | Gateway-level | `tail_sampling: latency: {threshold_ms: 500}` |
   | **Combined** | Production standard | Head 10% + Tail 100% errors/slow → ~12-15% capture |

3. **Span Design Principles**:
   - One span per logical operation (DB query, HTTP call, cache lookup)
   - Set `status` to ERROR on exceptions; record exception details
   - Use semantic conventions: `http.method`, `db.system`, `messaging.destination`
   - Custom attributes sparingly: domain-specific, no PII, no unbounded cardinality

4. **Trace-Log Correlation**:
   ```
   User: "Why did my order fail?"
   → Search logs for order_id → find trace_id → Tempo: full waterfall
   → Identify: CheckoutService → PaymentService timeout (3000ms exceeded)
   → Drill into PaymentService logs by trace_id → DB connection pool exhausted
   → <!-- DEEP: 10+min -->
Root cause: connection pool leak in PaymentService v2.3.0
   ```

5. **Baggage Propagation** — Pass business context across service boundaries:
   ```python
   from opentelemetry import baggage

   baggage.set_baggage("customer.id", "cust_789")
   baggage.set_baggage("experiment.variant", "treatment_b")
   # Available in every downstream span
   ```

### Phase 5 (~25 min): Alerting & Incident Response

1. **Alert Philosophy**:
   > Page on symptoms (user impact), not causes (infrastructure anomaly). Every page must require immediate human action.

2. **Multi-Window Burn Rate Alerting** — The standard for SLO-based alerting:

   | Burn Rate | Budget Exhausted In | Short Window | Long Window | Action |
   |---|---|---|---|---|
   | 5x | 6 days | 1h | 6h | Create ticket (P3) |
   | 10x | 3 days | 30m | 6h | Page on-call (P2) |
   | 14.4x | 2 days | 5m | 1h | Page on-call (P1) |
   | 36x | 20 hours | 5m | 30m | Emergency page (P0) |

   Short window detects fast burns; long window confirms sustained issue (filters blips). Both must fire.

3. **Prometheus Alerting Rule**:
   ```yaml
   - alert: SLOBurnRate14x
     expr: |
       (  # Short: 5m at 14.4x
         sum(rate(http_errors[5m])) / sum(rate(http_requests[5m])) > 0.00072 * 14.4
       )
       and
       (  # Long: 1h at 14.4x
         sum(rate(http_errors[1h])) / sum(rate(http_requests[1h])) > 0.00072 * 14.4 * (1/12)
       )
     for: 5m
     labels:
       severity: P1
     annotations:
       summary: "SLO burn rate 14.4x — error budget critical"
       runbook_url: "https://wiki/runbooks/slo-burn-14x"
   ```

4. **Alert Severity Levels**:

   | Level | Response Time | Notification | Example |
   |---|---|---|---|
   | **P0 — Emergency** | 5 min (24/7) | Phone call + PagerDuty | Prod down, security breach, data loss |
   | **P1 — Critical** | 15 min (24/7) | PagerDuty push | SLO burn rate 14.4x, major feature broken |
   | **P2 — High** | 30 min (24/7) | PagerDuty push | SLO burn rate 10x, performance degraded |
   | **P3 — Medium** | 1 hour (business) | Slack/email | Elevated errors, capacity warning |
   | **P4 — Low** | 4 hours (business) | Ticket | Disk > 70%, cert expiring in 14 days |

5. **Alertmanager Routing & Deduplication**:
   ```yaml
   route:
     group_by: ['alertname', 'severity', 'service']
     group_wait: 30s        # Collect alerts in group before sending
     group_interval: 5m     # Interval for follow-ups within same group
     repeat_interval: 4h    # Resend if still firing after 4h

     routes:
       - match: {severity: P0}
         receiver: pagerduty-critical
         group_wait: 10s
       - match: {severity: P1}
         receiver: pagerduty-high
       - match: {severity: P2}
         receiver: pagerduty-high

   inhibit_rules:
     - source_match: {severity: 'P0'}
       target_match: {severity: 'P1'}
       equal: ['service']  # P0 suppresses P1 for same service
   ```

6. **Alert Fatigue Prevention Checklist**:
   - [ ] Every alert has a documented runbook with specific, actionable steps
   - [ ] Alerts are symptoms, not causes (page on SLO burn, not high CPU)
   - [ ] False positive rate < 10% (validate with 30-day historical data)
   - [ ] Silenced during maintenance windows
   - [ ] Low-severity alerts inhibited when higher-severity fires for same service
   - [ ] Monthly fire-drill: inject synthetic failure, verify full notification chain
   - [ ] Alert count per on-call shift < 5 (if > 5, reduce sensitivity or fix root causes)

### Phase 6 (~25 min): Observability as Code

1. **Git-Based Observability** — All dashboards, alerts, recording rules in version control:
   ```
   observability/
   ├── dashboards/
   │   ├── service-overview.json
   │   └── slo-compliance.json
   ├── alerts/
   │   ├── slo-alerts.yaml
   │   └── service-alerts.yaml
   ├── rules/
   │   └── recording-rules.yaml
   └── terraform/
       ├── grafana.tf
       ├── prometheus.tf
       └── alertmanager.tf
   ```

2. **Change Review for Alerts** — Every alert change requires PR review. Changes include:
   - Threshold adjustments → review historical data to verify sensitivity
   - New alerts → confirm runbook exists before merge
   - Removed alerts → verify no gap in coverage

3. **Dashboard Review Process** — Quarterly: which dashboards have zero views in 90 days? Archive or consolidate. Which dashboards have high view counts but low utility? Redesign.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | devops-engineer | Deployed infrastructure and services |
| **This** | observability-engineer | Instrumentation, dashboards, alerts, SLO definitions |
| **After** | site-reliability-engineer | Error budgets and reliability decisions based on observability data |

Common chains:
- **Chain**: devops-engineer → observability-engineer → site-reliability-engineer — Services are deployed and instrumented; SRE uses observability data for reliability management
- **Chain**: platform-engineer → observability-engineer → incident-responder — Platform provides standard instrumentation; incident response uses dashboards and alerts during outages

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `slo-design` | Defining SLIs, SLO targets, error budgets, and burn-rate alerting for service reliability |
| `dashboard-design` | Building USE (infrastructure), RED (services), and golden-signal dashboards in Grafana |
| `alerting-strategy` | Designing alert philosophy, severity levels, fatigue prevention, and on-call routing |
| `distributed-tracing` | Instrumenting microservices with OpenTelemetry, span design, and sampling strategies |
| `logging-strategy` | Implementing structured logging with PII redaction, retention policies, and trace correlation |
| `metrics-collection` | Prometheus metrics design, cardinality management, recording rules, and long-term storage |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Observability engineers make systems understandable. They instrument services, build dashboards, configure alerts, and define SLOs — coordinating with every service owner, SRE, and incident responder in the organization.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | Service instrumentation, metric design | RED metrics implementation, structured logging format, trace context propagation, custom business metrics |
| **Frontend Developer** | RUM setup, Core Web Vitals tracking | Web Vitals instrumentation, error boundary telemetry, user journey tracing, session replay config |
| **DevOps Engineer** | Monitoring infrastructure deployment, alert routing | Prometheus/Thanos deployment, Grafana provisioning, Alertmanager config, PagerDuty integration |
| **SRE / Incident Responder** | Alert design, SLO enforcement, incident response | Alert severity calibration, burn rate thresholds, error budget policy, on-call runbook links in alerts |
| **Security Engineer** | Audit logging, anomaly detection | Audit log collection, SIEM integration, anomaly detection rules, PII redaction in logs |
| **Data Engineer** | Data pipeline observability, cost monitoring | Pipeline metrics (lag, freshness, row counts), warehouse query performance, Spark cluster metrics |
| **Cloud Architect** | Cloud-native observability (CloudWatch, Cloud Monitoring) | AWS/GCP/Azure native monitoring integration, cost allocation for observability data, log storage tiering |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Error budget burn rate exceeds threshold (fast burn) | Service owner, Incident Responder | Potential SEV2/SEV1; may need immediate mitigation |
| New service deployed without instrumentation | Service owner, DevOps | Add RED metrics, structured logging, and tracing before production traffic |
| Alert storm (>5 alerts in 5 minutes) | Incident Responder, DevOps | Investigate root cause; may need alert correlation/suppression |
| Observability cost spike (log volume 2x, metric cardinality explosion) | Service owner, Cloud Architect | Identify source; add sampling, cardinality limits, or log filtering |
| Dashboard showing stale data (>1 hour) | DevOps | Data pipeline health check; Prometheus/Thanos/Loki storage investigation |

### Escalation Path

```
SLO breach (error budget exhausted)? → Service owner → Incident Responder → CTO Advisor
Observability infrastructure down? → DevOps Engineer → Cloud Architect
Alerting not firing during incident? → Incident Responder (immediate fix)
Cardinality explosion degrading Prometheus? → DevOps Engineer → Cloud Architect (infra scale)
```

## Best Practices
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

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Observability = PaaS built-in logs + metrics. No custom dashboards. No alerts (check manually). No tracing. No structured logging. Debug via `console.log` + PaaS log viewer.
- **What to skip**: Prometheus. Grafana. OpenTelemetry. Structured logging. SLOs. Alerting. Dashboards. Log aggregation. Distributed tracing.
- **Coordination**: You check logs when something breaks. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Structured logging (JSON). Log aggregation (Papertrail/Logtail or cloud-native). Uptime monitoring (Pingdom/Checkly). Basic alerting (uptime + error rate via email/Slack). RED metrics hand-rolled or framework built-in. One dashboard with key metrics.
- **What to skip**: Prometheus + Grafana (use managed). Distributed tracing. SLOs. Error budgets. On-call rotation tooling beyond PagerDuty basics.
- **Coordination**: Alerts go to shared Slack channel. Weekly check on error trends. On-call rotation via calendar.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full observability stack (Prometheus + Grafana + Loki + Tempo). OpenTelemetry for distributed tracing. Structured logging with trace correlation IDs. SLOs defined for critical journeys. Alertmanager with severity routing. Dashboards as code (Grafana in Terraform/Grafonnet). RED + USE metrics. On-call with PagerDuty + runbooks. RUM for frontend (if applicable).
- **What to skip**: AIOps/Anomaly detection. Full data warehouse for observability. Dedicated observability team (embed in platform team).
- **Coordination**: Observability weekly review with platform team. Monthly SLO review. Quarterly alert tuning. Incident post-mortems.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Observability platform team. Centralized observability with multi-tenancy. Error budget policies enforced. Chaos engineering with observability validation. AIOps for anomaly detection. Cost attribution for observability data. Log sampling and retention policies. Compliance audit trails. Observability as a product (self-service dashboards, alert configuration). Synthetic monitoring. Business KPI dashboards.
- **What's full production**: Observability center of excellence. Self-service observability platform. Automated runbook linking. Incident analysis automation. Observability data lifecycle management.
- **Coordination**: Observability platform team weekly. Monthly SLO + error budget review with service owners. Quarterly observability strategy review.

### Transition Triggers
- **Solo → Small**: First time you can't debug a production issue because logs are missing.
- **Small → Medium**: >3 services with inter-service calls. First incident where you couldn't trace root cause without distributed tracing.
- **Medium → Enterprise**: 10+ services with SLO commitments. Multi-team on-call. Compliance requires audit trails.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
### Instrumentation
- [ ] **[S1]**  All services instrumented with OpenTelemetry SDKs (auto-instrumentation minimum)
- [ ] **[S2]**  Manual instrumentation for critical business logic spans with domain attributes
- [ ] **[S3]**  `trace_id` and `span_id` in all structured log lines
- [ ] **[S4]**  Resource attributes set: `service.name`, `service.version`, `deployment.environment`
- [ ] **[S5]**  Sampling strategy documented and tuned: head 10% + tail 100% errors/slow

### SLOs & Alerting
- [ ] **[S6]**  SLIs defined for all critical user journeys (3-5 journeys)
- [ ] **[S7]**  SLO targets set with error budget policy per journey
- [ ] **[S8]**  Multi-window burn-rate alerts configured for each SLO (5x, 14.4x, 36x)
- [ ] **[S9]**  Alertmanager routing: severity-based → PagerDuty/Slack with inhibition rules
- [ ] **[S10]**  Runbook URLs on every alert annotation
- [ ] **[S11]**  Dead man's switch (Watchdog alert) monitoring pipeline health
- [ ] **[S12]**  Monthly alerting fire-drill verifies end-to-end notification chain

### Dashboards
- [ ] **[S13]**  SLO compliance dashboard with burn-down charts per critical journey
- [ ] **[S14]**  RED dashboards for every production service (Rate, Errors, Duration)
- [ ] **[S15]**  USE dashboards for infrastructure: CPU, memory, disk, network per node
- [ ] **[S16]**  Dashboards provisioned as code (Terraform/Grafonnet/Git)
- [ ] **[S17]**  Recording rules for expensive PromQL queries

### Logging
- [ ] **[S18]**  Structured JSON logging with consistent schema across all services
- [ ] **[S19]**  Log aggregation pipeline: Promtail/Fluent Bit → Loki or Elasticsearch
- [ ] **[S20]**  Retention tiers configured (hot 7d, warm 30d, cold 1yr+)
- [ ] **[S21]**  PII redaction pipeline at collection time (emails, credit cards, SSNs)
- [ ] **[S22]**  Log-based metrics derived for error rates, latency distributions

### Tracing
- [ ] **[S23]**  Distributed tracing with head + tail sampling strategy
- [ ] **[S24]**  OpenTelemetry Collector Agent (DaemonSet) on every node
- [ ] **[S25]**  Gateway (≥ 3 replicas) for tail sampling and multi-backend routing
- [ ] **[S26]**  Trace-log correlation working end-to-end: log → trace_id → full waterfall
- [ ] **[S27]**  Semantic conventions followed for HTTP, DB, messaging spans

### Operations
- [ ] **[S28]**  On-call rotations, escalation policies, silence/maintenance windows configured
- [ ] **[S29]**  Synthetic monitoring (black-box probes) validates critical paths from outside
- [ ] **[S30]**  Runbooks exist for all P0/P1/P2 alerts with specific, actionable steps
- [ ] **[S31]**  Blameless postmortem process established; action items tracked to completion
- [ ] **[S32]**  Capacity planning: metrics retention ≥ 13 months for year-over-year trends

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [SLO Cookbook — Production Field Manual](references/slo-cookbook.md) — SLI patterns, SLO formulation, error budget mechanics, burn rate alerting, dashboard design
- [Alert Design Patterns](references/alert-design-patterns.md) — USE/RED methods, multi-window burn rate alerts, severity definitions, runbook integration, deduplication
- [OpenTelemetry Guide — Production Field Manual](references/opentelemetry-guide.md) — SDK configuration, collector deployment, sampling strategies, attribute conventions, trace-log correlation
- Google SRE Workbook — Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/
- Prometheus Alerting Rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
- Grafana Dashboard Best Practices: https://grafana.com/docs/grafana/latest/best-practices/
- OpenTelemetry Documentation: https://opentelemetry.io/docs/
- Thanos — Highly Available Prometheus: https://thanos.io/
