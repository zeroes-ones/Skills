# Observability Engineer - Alert Design Patterns

Alert design methodology: signal vs noise, USE/RED methods, multi-window burn rate alerting, and runbook integration.

---

## Signal vs. Noise — Avoiding Alert Fatigue

### The Problem
Alert fatigue kills incident response. If >30% of alerts are false positives or non-actionable, engineers stop paying attention.

### Principles
1. **Every alert must require human action.** If no human action is needed, it's a dashboard metric, not an alert.
2. **Alerts should be symptoms, not causes.** Alert on "service is slow" not "CPU is high" (CPU high is a cause, slow is the symptom).
3. **Page on SLO breach, warn on everything else.** PagerDuty/PagerTree for P1-P2; Slack/email for P3-P5.
4. **Alert on what users experience.** If users aren't affected, it's probably not page-worthy.

### Elimination Checklist (Before Adding an Alert)
- [ ] What specific human action does this alert require?
- [ ] Could this be solved by automation (auto-scaling, restart, failover)?
- [ ] Is there already an alert that covers this failure mode?
- [ ] What's the false positive rate? Test with historical data.
- [ ] What's the runbook URL for this alert?

---

## USE Method — Resource-Level Alerts

USE = **U**tilization, **S**aturation, **E**rrors. Applied to every resource (CPU, memory, disk, network).

### CPU
| Metric | Alert | Threshold | PromQL |
|--------|-------|-----------|--------|
| Utilization | CPU usage high | >90% for 5m | `100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90` |
| Saturation | Run queue length | load > cores * 2 for 5m | `node_load1 / count by(instance)(node_cpu_seconds_total{mode="idle"}) > 2` |
| Errors | CPU throttling | any throttling | `rate(node_cpu_throttled_seconds_total[5m]) > 0` |

### Memory
| Metric | Alert | Threshold | PromQL |
|--------|-------|-----------|--------|
| Utilization | Memory usage high | >90% for 5m | `(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 90` |
| Saturation | Swapping | swap used > 0 | `node_memory_SwapFree_bytes < node_memory_SwapTotal_bytes` |
| Errors | OOM kills | any OOM | `increase(node_vmstat_oom_kill[5m]) > 0` |

### Disk
| Metric | Alert | Threshold | PromQL |
|--------|-------|-----------|--------|
| Utilization | Disk space low | >85% (warn), >95% (crit) | `(node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 15` |
| Saturation | I/O wait | >30% for 10m | `rate(node_disk_io_time_seconds_total[5m]) * 100 > 30` |
| Errors | Disk errors | any read/write errors | `increase(node_disk_read_errors_total[5m]) > 0` |

### Network
| Metric | Alert | Threshold | PromQL |
|--------|-------|-----------|--------|
| Utilization | Bandwidth saturation | >80% of link speed | `rate(node_network_transmit_bytes_total[5m]) * 8 / link_speed > 0.8` |
| Saturation | Dropped packets | any drops | `rate(node_network_drop_total[5m]) > 0` |
| Errors | Interface errors | any errors | `rate(node_network_transmit_errs_total[5m]) > 0` |

---

## RED Method — Service-Level Alerts

RED = **R**ate, **E**rrors, **D**uration. Applied to every service endpoint.

### Rate (Requests per second)
Monitor for anomalies, not absolutes:
```promql
# Warn if request rate drops >50% from 1h ago (possible outage upstream)
rate(http_requests_total[5m]) / rate(http_requests_total[5m] offset 1h) < 0.5
```

### Errors (Failed requests)
```promql
# Error rate > 1% for 5 minutes
sum(rate(http_requests_total{status=~"5.."}[5m])) 
/ 
sum(rate(http_requests_total[5m])) > 0.01

# Error rate > 5% for 1 minute (fast-burning)
sum(rate(http_requests_total{status=~"5.."}[1m])) 
/ 
sum(rate(http_requests_total[1m])) > 0.05
```

### Duration (Latency)
```promql
# P99 latency > 500ms for 5 minutes
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 0.5

# P50 latency > target (sign of broad slowdown)
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 0.1
```

---

## Multi-Window Burn Rate Alerting for SLOs

### Concept
An SLO of 99.9% availability means 0.1% error budget. Burn rate = how fast you're consuming it.

| Burn Rate | Error Budget Consumed In | Page? |
|-----------|-------------------------|-------|
| 1x | 30 days (entire window) | No — expected |
| 2x | 15 days | Warn on 1h |
| 5x | 6 days | Page on 1h |
| 10x | 3 days | Page on 30m |
| 36x | 20 hours | Page on 5m (critical) |

### Multi-Window Alerts
Use two windows to avoid false positives on brief spikes:
- **Short window:** 5 minutes — detects fast, high-severity issues
- **Long window:** 1 hour — confirms sustained issue, filters transient blips

```promql
# SLO: 99.9% availability (0.1% error budget)
# Alert at 10x burn rate over 1h short window AND 5x over 6h long window
# Short window: 1h at 10x = 10% error budget consumed
# Long window: 6h at 5x = 3% error budget consumed

# Short window check
(
  sum(rate(http_errors_total[1h]))
  /
  sum(rate(http_requests_total[1h]))
) > 0.01  # 10x * 0.1% * 1h = 1% threshold

# AND long window check
(
  sum(rate(http_errors_total[6h]))
  /
  sum(rate(http_requests_total[6h]))
) > 0.003  # 5x * 0.1% * 6h = 3% threshold
```

### Burn Rate Formula
```
threshold = burn_rate * error_budget * alert_window / SLO_period
```

Example: 99.9% SLO, 5x burn rate, 1h alert window, 30-day SLO period:
```
threshold = 5 * 0.001 * (1h/720h) = 5 * 0.001 * 0.00139 ≈ 0.0007%
```

---

## Alert Severity Definitions

| Level | Response Time | Notification | Example |
|-------|-------------|-------------|---------|
| **P1 - Critical** | 5 min (24/7) | Phone call + PagerDuty | Production down, data loss, security breach |
| **P2 - High** | 15 min (24/7) | PagerDuty push | Degraded service, partial outage, SLO at risk |
| **P3 - Medium** | 1 hour (business hours) | Slack/email | Elevated error rates, performance degradation |
| **P4 - Low** | 4 hours (business hours) | Slack channel | Non-critical warnings, capacity approaching threshold |
| **P5 - Info** | Next business day | Dashboard/ticket | Disk >70%, cert expiring in 30 days |

---

## Runbook-Linked Alerting

Every alert definition MUST include a `runbook_url` annotation.

```yaml
groups:
- name: service_alerts
  rules:
  - alert: HighErrorRate
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m])) 
      / 
      sum(rate(http_requests_total[5m])) > 0.05
    for: 5m
    labels:
      severity: P2
      service: my-service
    annotations:
      summary: "High error rate on {{ $labels.service }}"
      description: "Error rate is {{ $value | humanizePercentage }} over the last 5 minutes."
      runbook_url: "https://wiki.company.com/runbooks/high-error-rate"
      dashboard_url: "https://grafana.company.com/d/service-overview"
```

---

## Alert Grouping & Deduplication

### Grouping Strategies
```yaml
# Group by alert name + severity — separate notification per service
route:
  group_by: ['alertname', 'severity']
  group_wait: 30s       # Wait to collect more alerts in group
  group_interval: 5m    # Subsequent notifications for same group
  repeat_interval: 4h   # Re-send if still firing after 4h

  routes:
  - match:
      severity: P1
    receiver: 'pagerduty-critical'
    group_wait: 10s      # Faster for P1

  - match:
      severity: P2
    receiver: 'pagerduty-high'

  - match:
      severity: P3
    receiver: 'slack-warnings'
```

### Deduplication Techniques
1. **Alertmanager dedup:** Alerts with identical labels deduplicated automatically
2. **Inhibition rules:** Suppress low-severity alerts when higher-severity fires
   ```yaml
   inhibit_rules:
   - source_match:
       severity: 'P1'
     target_match:
       severity: 'P2'
     equal: ['service']  # P1 suppresses P2 for same service
   ```
3. **Maintenance windows:** Silence alerts during planned maintenance
4. **Flapping detection:** Don't re-alert if alert resolved and re-fired within 5 minutes

---

## Prometheus Alert Rules — Complete Examples

### Service Availability
```yaml
- alert: ServiceDown
  expr: up == 0
  for: 2m
  labels:
    severity: P1
  annotations:
    summary: "Service {{ $labels.job }} is down"
    description: "{{ $labels.instance }} has been unreachable for 2 minutes."
    runbook_url: "https://wiki.company.com/runbooks/service-down"
```

### API Latency
```yaml
- alert: HighLatency
  expr: |
    histogram_quantile(0.99, 
      sum(rate(http_request_duration_seconds_bucket{service="api"}[5m])) by (le, endpoint)
    ) > 1.0
  for: 10m
  labels:
    severity: P2
  annotations:
    summary: "High P99 latency on {{ $labels.endpoint }}"
    description: "P99 latency is {{ $value }}s for endpoint {{ $labels.endpoint }}"
    runbook_url: "https://wiki.company.com/runbooks/high-latency"
```

### Certificate Expiry
```yaml
- alert: CertificateExpiring
  expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7  # 7 days
  for: 1h
  labels:
    severity: P3
  annotations:
    summary: "TLS certificate for {{ $labels.instance }} expires in < 7 days"
    description: "Certificate expires at {{ $value | humanizeTimestamp }}"
    runbook_url: "https://wiki.company.com/runbooks/cert-expiry"
```

### Dead Man's Switch (Alerting Pipeline Health)
```yaml
- alert: Watchdog
  expr: vector(1)
  labels:
    severity: P1
  annotations:
    summary: "Watchdog — alerts if Alertmanager stops firing"
    description: "This is a dead man's switch. If this stops alerting, your monitoring pipeline is broken."
    runbook_url: "https://wiki.company.com/runbooks/watchdog"
```
