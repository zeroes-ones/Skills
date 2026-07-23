# Core Workflow — Full Implementation

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
