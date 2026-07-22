# SRE Practices

> **Author:** Sandeep Kumar Penchala

Comprehensive Site Reliability Engineering patterns covering SLO/SLI frameworks, error budgets, incident management, monitoring architecture, alerting design, capacity planning, chaos engineering, and runbook automation. These practices operationalize the site-reliability-engineer skill's reliability engineering discipline.

## SLO/SLI/SLA Framework

### Defining SLIs (Service Level Indicators)

| Category | SLI | Measurement | Good Target |
|----------|-----|-------------|-------------|
| Latency | P95/P99 request latency | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` | P95 < 200ms |
| Error Rate | Proportion of failed requests | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` | < 0.1% |
| Throughput | Requests per second | `rate(http_requests_total[1m])` | > N req/s (capacity-based) |
| Saturation | CPU/memory/queue depth | `cpu_utilization` / `queue_depth` | CPU < 70%, queue < 100 |
| Availability | Uptime (error rate < threshold) | `1 - error_rate` or probe success rate | 99.9% – 99.99% |

### SLO Targets by Criticality

| Service Tier | Availability | Latency P95 | Error Budget (30d) |
|-------------|-------------|-------------|-------------------|
| Tier 0 (Critical — revenue) | 99.99% | < 100ms | 4.3 min downtime |
| Tier 1 (Important — user-facing) | 99.9% | < 300ms | 43 min downtime |
| Tier 2 (Background — async) | 99% | < 1s | 7.2 hours downtime |
| Tier 3 (Internal — tools) | 99% | < 2s | 7.2 hours downtime |

### Prometheus SLO Recording Rules

```yaml
groups:
  - name: slo
    rules:
      - record: job:http_requests:availability_ratio
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[30d]))
          / sum(rate(http_requests_total[30d]))
      - record: job:http_requests:error_budget_remaining
        expr: |
          (1 - (1 - job:http_requests:availability_ratio) / 0.001) * 100
        # 0.001 = allowed error rate for 99.9% SLO
```

## Error Budget Policy

### Burn Rate Alerts

```yaml
# Alert when burning error budget too fast
groups:
  - name: slo-alerts
    rules:
      # Fast burn: 2% budget consumed in 1 hour → page on-call
      - alert: SLOBurnRateHigh
        expr: |
          (1 - sum(rate(http_requests_total{status=~"5.."}[1h])) / sum(rate(http_requests_total[1h])))
          < 0.998                 # 0.2% error rate over 1h = 2% budget burn
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "SLO burn rate critical — 2% budget consumed in 1h"
          description: "{{ $labels.job }} error budget projected to exhaust in 2 days"
          runbook: "https://wiki.internal/slo-burn-runbook"

      # Slow burn: 10% budget consumed in 3 days → ticket
      - alert: SLOBurnRateWarning
        expr: |
          (1 - sum(rate(http_requests_total{status=~"5.."}[3d])) / sum(rate(http_requests_total[3d])))
          < 0.9997
        for: 10m
        labels:
          severity: warning
```

### Error Budget Exhaustion Response

```
Error budget remaining > 50%  → Business as usual; deploy freely
Error budget remaining 20-50%  → Monitor closely; consider reducing deploy velocity
Error budget remaining < 20%   → Freeze non-critical deploys; focus on reliability
Error budget EXHAUSTED         → HALT all deploys; all engineering → reliability work
                                 until budget recovers (next window or 30-day reset)
```

## Incident Management

### Severity Levels

| Level | Name | Response Time | Example |
|-------|------|--------------|---------|
| SEV-0 | Critical — revenue/security | < 5 min (page) | Site down, data breach, payment failures |
| SEV-1 | Major — core feature broken | < 15 min (page) | Login broken, checkout unavailable |
| SEV-2 | Minor — feature degraded | < 1 hour | Search slow, partial feature broken |
| SEV-3 | Trivial — cosmetic | < 1 business day | UI glitch, non-blocking issue |

### Incident Commander Role

```
Incident Commander (IC) responsibilities:
  1. Declare incident; set severity
  2. Assign roles: Communications Lead, Operations Lead
  3. Start incident timer; create Slack channel (#inc-YYYY-MM-DD-title)
  4. Maintain shared state (Google Doc / incident.io)
  5. Timebox investigations — escalate if no progress in 30 min
  6. Decide to rollback / failover / scale — take action
  7. Declare resolution; trigger postmortem

IC is NOT debugging — IC orchestrates. Debuggers are separate.
```

### Postmortem Template

```markdown
# Postmortem: [Title]
- Date: 2026-07-21
- Severity: SEV-1
- Duration: 47 minutes (14:03 - 14:50 UTC)
- IC: @jane
- Authors: @jane, @bob

## Summary
Two-sentence summary of what happened and impact.

## Timeline (UTC)
- 14:03: Deploy v2.3.0 to production
- 14:05: PagerDuty alert — 5xx rate 8%
- 14:07: @jane declares SEV-1; rollback initiated
- 14:10: Rollback complete; error rate normalizing
- 14:15: Root cause identified — config key mismatch
- 14:50: All metrics back to baseline

## Root Cause
The `DATABASE_URL` config key was renamed to `DB_URL` in v2.3.0
but migration script still referenced the old key, causing connection failures.

## Impact
- 3,200 users affected (12% of active users)
- $4,200 estimated revenue impact (42 min downtime)

## Action Items
- [ ] Add integration test for config key consistency (P0, @bob)
- [ ] Add pre-deploy config validation script (P1, @alice)
- [ ] Update runbook with config change checklist (P2, @jane)
```

## Monitoring Architecture

### Unified Observability Stack

```
┌──────────────────────────────────────────────────────────┐
│                    Grafana (Dashboards)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐   │
│  │ Metrics  │  │  Logs    │  │  Traces              │   │
│  │Prometheus│  │  Loki    │  │  Tempo/Jaeger        │   │
│  │          │  │          │  │                      │   │
│  │Exemplars─┼──┼──────────┤  │  (trace-id in logs)  │   │
│  └──────────┘  └──────────┘  └──────────────────────┘   │
└──────────────────────────────────────────────────────────┘

Exemplar: links a metric data point to a trace
  → "P99 latency spike at 14:05 → click to see the exact slow trace"
```

### RED Metrics (Every Service)

```
Rate      — Requests per second
Errors    — Failed requests per second
Duration  — Latency distribution (P50, P95, P99)

USE Metrics (Every Resource):
  Utilization  — % of resource used
  Saturation   — Queue depth, concurrency
  Errors       — Hardware/software errors
```

## Alerting Design

### Alert Threshold Selection

```yaml
# DO: alert on SLO burn rate, not raw thresholds
# DON'T: alert on "CPU > 80% for 5min" (noisy; may be expected batch job)

# Good: alert on sustained saturation
- alert: HighCPU
  expr: avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) > 0.8
  for: 30m                                  # Sustained, not transient
  annotations:
    runbook: "https://wiki.internal/high-cpu-runbook"
```

### Anti-Fatigue Principles

```
1. Every alert MUST have a runbook link
2. Alerts MUST be actionable — if no human action needed, it's a dashboard metric
3. No alerts on symptoms that self-heal within 5 minutes
4. Group related alerts — one notification, not 15
5. Set different notification channels by severity:
   - Critical → PagerDuty (wakes someone up)
   - Warning → Slack channel (#alerts-warning)
   - Info → Dashboard only (no notification)
```

## Capacity Planning

### Load Testing with k6

```javascript
// k6 load test script
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },     // Ramp up to 100 VUs
    { duration: '5m', target: 100 },     // Stay at 100
    { duration: '2m', target: 500 },     // Ramp to 500
    { duration: '5m', target: 500 },     // Stay at 500
    { duration: '2m', target: 0 },       // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],    // 95th percentile < 200ms
    http_req_failed: ['rate<0.01'],      // Error rate < 1%
  },
};

export default function () {
  const res = http.get('http://myapp/health');
  check(res, { 'status 200': r => r.status === 200 });
  sleep(1);
}
```

### Traffic Forecasting

```
Capacity formula:
  Required capacity = peak_rps * p99_latency * concurrency_per_instance
  Instance count = ceil(required_capacity / capacity_per_instance)
  Add 30% headroom for failover + traffic spikes
```

## Chaos Engineering

### Steady State Hypothesis

```yaml
# Chaos Mesh experiment — kill 1 pod, verify service stays healthy
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: kill-order-service-pod
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces: [prod]
    labelSelectors:
      app: order-service
  duration: "60s"
  scheduler:
    cron: "@every 30m"     # Run every 30 min during GameDay
```

### Tool Comparison

| Tool | Complexity | Best For |
|------|-----------|----------|
| Chaos Mesh | Medium | Kubernetes-native; pod/network/stress |
| Litmus | Medium | Kubernetes; rich experiment catalog |
| Gremlin | Low | SaaS; easy onboarding; multi-infra |
| AWS FIS | Medium | AWS-native; integrated with CloudWatch |

### GameDay Structure

```
1. Hypothesis: "If 1 order-service pod dies, users see no errors"
2. Scope (blast radius): single pod in 3-replica deployment
3. Run experiment during business hours (observability is strongest)
4. Monitor: error rate, latency, throughput
5. Abort condition: error rate > 0.5% or P95 > 500ms
6. Retrospective: what did we learn? What needs hardening?
```

## Runbook Automation

### Common Runbook Template

```markdown
# Runbook: High 5xx Error Rate
**Owner:** SRE Team
**Severity:** SEV-1

## Triage (5 min)
1. Check dashboard: [5xx Dashboard](grafana-link)
2. Recent deploys? `argocd app list | grep -v Synced`
3. Upstream dependencies healthy? Check [Service Map](link)

## Mitigation (10 min)
1. **ROLLBACK** (fastest fix, low risk):
   `argocd app rollback order-service --to <last-known-good>`
2. **SCALE** (if backend overloaded):
   `kubectl scale deployment order-service --replicas=10`
3. **FAILOVER** (if zone/region issue):
   Route53: update weighted record → failover region

## Verify
1. Error rate returns to < 0.1% → `rate(http_requests_total{status=~"5.."}[1m])`
2. Latency P95 < 200ms → `histogram_quantile(0.95, ...)`
3. Announce resolution in #inc-* channel
```

### Automated Runbook Execution

```python
# runbook-automation.py — run a runbook by name
import subprocess, sys, json

runbooks = {
    "rollback": lambda svc: subprocess.run(["argocd", "app", "rollback", svc]),
    "scale-up": lambda svc, count: subprocess.run(["kubectl", "scale", f"deployment/{svc}", f"--replicas={count}"]),
    "restart": lambda svc: subprocess.run(["kubectl", "rollout", "restart", f"deployment/{svc}"]),
}

if __name__ == "__main__":
    action, service = sys.argv[1], sys.argv[2]
    if action in runbooks:
        print(f"Executing {action} on {service}...")
        result = runbooks[action](service)
        print(f"Completed: {result.returncode}")
```

These SRE practices implement the site-reliability-engineer skill's reliability framework — SLOs drive decisions, error budgets gate releases, incidents follow structured response, and runbooks make recovery repeatable and fast.
