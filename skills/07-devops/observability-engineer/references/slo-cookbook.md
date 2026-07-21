# SLO Cookbook — Production Field Manual

## Table of Contents
1. [SLI Definition Patterns](#sli-definition-patterns)
2. [SLO Formulation](#slo-formulation)
3. [Error Budget Mechanics](#error-budget-mechanics)
4. [Burn Rate Alerting](#burn-rate-alerting)
5. [Multi-Window Alert Design](#multi-window-alert-design)
6. [SLO Dashboard Design](#slo-dashboard-design)
7. [SLO Lifecycle Management](#slo-lifecycle-management)

---

## SLI Definition Patterns

### The SLI Equation
```
SLI = Good Events / Total Valid Events × 100
```

### Core SLI Types

| SLI Type | Definition | Metric Example | Good If |
|---|---|---|---|
| **Availability** | Proportion of requests that succeed | `http_requests_total{status!~"5.."}` / `http_requests_total` | Status ≠ 5xx |
| **Latency** | Proportion of requests faster than threshold | `histogram_quantile(0.99, ...)` < 300ms | Duration < SLO threshold |
| **Error Rate** | Proportion of requests that fail | `http_errors_total` / `http_requests_total` | Errors < budget |
| **Throughput** | Successful requests per second | `rate(http_requests_total{status!~"5.."}[5m])` | Above minimum threshold |
| **Freshness** | Data age in seconds | `now() - max(updated_at)` | Age < SLA |
| **Durability** | Proportion of writes that persist | Successful writes / Total writes | > 99.9999999% (11 nines) |
| **Correctness** | Proportion of responses matching expected | `correct_responses / total_responses` | As high as possible |

### Latency SLI — Histogram Design

```promql
# Define good events: requests completing in < 300ms
sum(rate(http_request_duration_seconds_bucket{le="0.3"}[28d]))
/
sum(rate(http_request_duration_seconds_count[28d]))

# Multi-threshold SLI: 90% < 100ms AND 99% < 300ms AND 99.9% < 1000ms
# Each is a separate SLI; the SLO is the composite
```

### Availability SLI — Distinguish Client vs Server Errors

```promql
# Good SLI: only 5xx errors are "bad" (client 4xx errors are user errors)
sum(rate(http_requests_total{status!~"5.."}[28d]))
/
sum(rate(http_requests_total[28d]))

# Strict SLI (transactional systems): 4xx AND 5xx are "bad"
sum(rate(http_requests_total{status=~"2.."}[28d]))
/
sum(rate(http_requests_total[28d]))
```

### Critical User Journey SLIs

Don't measure every endpoint equally. Identify the 3-5 journeys that represent user value:

| User Journey | Primary SLI | Secondary SLI | SLO Window |
|---|---|---|---|
| Login | Availability: % of successful logins | Latency: p99 < 1s | 28 days |
| Search | Latency: p95 < 300ms | Availability: % non-error | 28 days |
| Checkout | Availability: % successful payments | Durability: payment record written | 7 days (stricter) |
| Content Feed | Freshness: < 5 min stale | Latency: p95 < 200ms | 7 days |
| API (B2B) | Availability: % 200 responses | Latency: p99 < 500ms | 30 days |

---

## SLO Formulation

### The SLO Formula
```
SLO = Target Percentage for SLI over a Compliance Window
```

### Choosing Your SLO Target

| SLO | Nines | Allowed Downtime (30 days) | Typical Use Case |
|---|---|---|---|
| 99.9% | Three nines | 43.2 minutes | Internal tools, batch processing |
| 99.95% | Three-and-a-half | 21.6 minutes | Customer-facing, non-critical |
| 99.99% | Four nines | 4.32 minutes | Payment, auth, critical API |
| 99.999% | Five nines | 26 seconds | Telco, life-safety, financial settlement |

### SLO Anti-Patterns

1. **100% SLO** — Impossible to achieve; guarantees alert fatigue. Even five nines (99.999%) is extreme.
2. **SLO = Current Performance** — If you're at 99.5%, setting 99.5% means zero improvement budget. Set slightly above current performance.
3. **One SLO per service** — A service might need 99.99% availability for critical endpoints and 99% for admin endpoints. Differentiate.
4. **SLO without error budget policy** — An SLO without a decision framework for what happens when the budget runs out is a dashboard metric, not an SLO.
5. **Annual SLO** — Too long to be actionable. 28-30 day rolling windows are standard; 7-day windows for fast-moving consumer products.

### SLO Formulation Process

```
1. Identify critical user journey
2. Define SLI (what to measure)
3. Measure current performance over 4 weeks
4. Set SLO slightly above current (stretch, not impossible)
5. Define error budget policy:
   - Budget > 50%: normal operations
   - Budget 20-50%: freeze risky deploys, prioritize reliability
   - Budget < 20%: halt feature deploys, all eng on reliability
   - Budget exhausted: page on-call, SEV-level response
6. Review quarterly: has performance improved? Raise SLO.
```

---

## Error Budget Mechanics

### Error Budget Calculation
```
Error Budget = (1 - SLO) × Total Valid Events

For 99.9% SLO, 28-day window, 10M requests/month:
Error Budget = (1 - 0.999) × 10,000,000 = 10,000 allowed errors
```

### Error Budget Burn Rate
```
Burn Rate = (Error Budget Consumed) / (Error Budget Expected Over Period)

Linear burn: 1x = consuming budget at expected rate (will exhaust in 28d)
Critical burn: 10x = will exhaust budget in 2.8 days
Emergency burn: 100x = will exhaust budget in 6.7 hours
```

### Error Budget Policy — Decision Framework

```yaml
error_budget_policy:
  green:  # Budget ≥ 50%
    deploy: allowed
    change_freeze: none
    priority: feature_work

  yellow: # Budget 20-50%
    deploy: allowed_with_extra_review
    change_freeze: risky_changes_blocked
    priority: balance

  orange: # Budget 5-20%
    deploy: blocked (except reliability fixes)
    change_freeze: all_non_reliability
    priority: reliability_only

  red:    # Budget < 5%
    deploy: blocked_completely
    change_freeze: full
    priority: incident_response
    escalation: notify_vp_engineering
```

### Error Budget Enforcement in CI/CD

```yaml
# Pre-deploy check: query error budget status
- name: Check error budget
  run: |
    BUDGET=$(curl -s "https://prometheus.example.com/api/v1/query?query=error_budget_remaining" | jq '.data.result[0].value[1]')
    if (( $(echo "$BUDGET < 20" | bc -l) )); then
      echo "Error budget below 20%. Deploy blocked."
      exit 1
    fi
```

---

## Burn Rate Alerting

### The Burn Rate Formula

```
Alert Threshold = Burn Rate × (1 - SLO) × (Alert Window / SLO Window)

Example: 99.9% SLO, 10x burn rate, 1h alert window, 30d SLO window
  = 10 × 0.001 × (1h / 720h)
  = 10 × 0.001 × 0.00139
  = 0.0000139
  = 0.00139% error rate threshold for 1h window
```

### Standard Burn Rate Alert Table

| Burn Rate | Time to Exhaust | Short Window | Long Window | Action |
|---|---|---|---|---|
| 1x | 30 days | — | — | No alert (expected) |
| 5x | 6 days | 1h | 6h | Create ticket |
| 10x | 3 days | 30m | 6h | Page on-call (P2) |
| 14.4x | 2 days | 5m | 1h | Page on-call (P1) |
| 36x | 20 hours | 5m | 30m | Critical page (P0) |

### PromQL — Multi-Window Burn Rate Alert

```promql
# 99.9% SLO, error-based SLI
# Alert at 14.4x burn rate (will exhaust budget in ~2 days)

# Short window: 5 minutes at 14.4x = error rate > 0.072%
(
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
) > 0.00072 * 14.4

# AND long window: 1 hour at 14.4x = error rate > 0.014%
and
(
  sum(rate(http_requests_total{status=~"5.."}[1h]))
  /
  sum(rate(http_requests_total[1h]))
) > 0.00072 * 14.4 * (1/12)
```

### Why Multi-Window?

Single-window alerts on short windows produce false positives from transient blips. Single-window alerts on long windows detect issues too slowly.

```
Short window: Detects fast burns (high severity, short duration)
Long window: Confirms sustained issue (filters blips)
Both must fire → alert is real and urgent
```

---

## Multi-Window Alert Design

### Alert Severity Stack

```yaml
groups:
  - name: slo-alerts

    # P2: Sustained 5x burn
    - alert: SLOBurnRate5x
      expr: |
        (short_window_5x) and (long_window_5x)
      for: 15m
      labels:
        severity: P2
        slo: "99.9%-availability"
      annotations:
        summary: "SLO burn rate 5x — error budget depleting"
        description: "At current rate, error budget exhausts in ~6 days."
        runbook_url: "https://wiki/runbooks/slo-burn-5x"

    # P1: Critical 14.4x burn
    - alert: SLOBurnRate14x
      expr: |
        (short_window_14x) and (long_window_14x)
      for: 5m
      labels:
        severity: P1
        slo: "99.9%-availability"
      annotations:
        summary: "SLO burn rate 14.4x — critical budget consumption"
        description: "At current rate, error budget exhausts in ~2 days."
        runbook_url: "https://wiki/runbooks/slo-burn-14x"

    # P0: Emergency 36x burn
    - alert: SLOBurnRate36x
      expr: |
        (short_window_36x) and (long_window_36x)
      for: 2m
      labels:
        severity: P0
        slo: "99.9%-availability"
      annotations:
        summary: "SLO burn rate 36x — immediate action required"
        description: "At current rate, error budget exhausts in ~20 hours."
        runbook_url: "https://wiki/runbooks/slo-burn-36x"
```

### Alertmanager Routing by Severity

```yaml
route:
  group_by: ['alertname', 'severity', 'slo']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    - match:
        severity: P0
      receiver: pagerduty-critical
      group_wait: 10s

    - match:
        severity: P1
      receiver: pagerduty-high

    - match:
        severity: P2
      receiver: slack-sre-channel
```

---

## SLO Dashboard Design

### SLO Dashboard Layout

```
┌─────────────────────────────────────────────────┐
│  SLO Compliance — Checkout Service               │
│  ┌────────────┬────────────┬──────────────────┐  │
│  │  SLO Gauge │ Error      │ Burn Rate        │  │
│  │  99.95% ✓  │ Budget     │ Multiplier       │  │
│  │            │ 78% rem.   │ 0.8x (normal)    │  │
│  └────────────┴────────────┴──────────────────┘  │
├─────────────────────────────────────────────────┤
│  Error Budget Burn-Down (28-day)                 │
│  ┌──────────────────────────────────┐            │
│  │ ████████████░░░░░░░░░░░░░░░░░░░░ │ 22% used   │
│  └──────────────────────────────────┘            │
├─────────────────────────────────────────────────┤
│  SLI Trend (P99 Latency, 7-day)                  │
│  ┌──────────────────────────────────┐            │
│  │    ╱╲   ╱╲                       │            │
│  │   ╱  ╲_╱  ╲___  ─── SLO (300ms) │            │
│  │               ╲                  │            │
│  └──────────────────────────────────┘            │
├─────────────────────────────────────────────────┤
│  Alert Firing?  │  Recent Deploys   │  Incidents │
│  None           │  v2.3.1 (8h ago)  │  0 active  │
└─────────────────────────────────────────────────┘
```

### Grafana Dashboard JSON Skeleton

```json
{
  "title": "SLO Compliance — Checkout Service",
  "panels": [
    {
      "title": "SLO Status",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(http_requests_good[28d])) / sum(rate(http_requests_total[28d])) * 100",
        "legendFormat": "SLI"
      }],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              { "value": null, "color": "red" },
              { "value": 99.9, "color": "green" }
            ]
          }
        }
      }
    },
    {
      "title": "Error Budget Remaining",
      "type": "gauge",
      "targets": [{
        "expr": "100 - (sum(rate(http_errors_total[28d])) / (0.001 * sum(rate(http_requests_total[28d])))) * 100"
      }]
    }
  ]
}
```

---

## SLO Lifecycle Management

### SLO Review Cadence

| Activity | Frequency | Owner | Output |
|---|---|---|---|
| SLO compliance review | Weekly | Service owners | Compliance %, budget remaining |
| SLO definition review | Quarterly | SRE + Product | Adjust targets, add/remove SLIs |
| Error budget policy review | Quarterly | SRE + Eng leadership | Update escalation paths |
| SLO tooling audit | Annually | Platform/SRE | Verify alert accuracy, dashboard freshness |

### SLO Change Management

```yaml
slo_change_process:
  proposal:
    - Document current SLO and performance
    - Propose new target with justification (customer impact, competitive, reliability goal)
    - Estimate cost to achieve (engineering time, infrastructure)
  review:
    - SRE team review for technical feasibility
    - Product review for customer impact alignment
    - VP Engineering approval
  implementation:
    - Update monitoring (dashboards, alerts, runbooks)
    - Communication: service owners, on-call rotations, support team
    - 2-week grace period before enforcement
```

### SLO Retirement Criteria

- The user journey is deprecated or replaced
- The SLI metric is no longer collected reliably
- The SLO has been at 100% for 6+ months (no signal value)
- The service is decommissioned

---

## Common SLO Anti-Patterns

1. **Alerting on SLO violation directly** — SLO is a 28-day rolling metric. By the time it drops, the error budget is fully depleted. Alert on *burn rate*, not *SLO compliance*.
2. **Single-window alerts** — Even with burn rate, single short windows cause false positives. Always use short + long window AND logic.
3. **No error budget policy** — An SLO without consequences is a wish, not a commitment. Define what happens at each budget level.
4. **SLO = 100%** — Impossible. Sets the team up for alert fatigue and cynicism. Use five nines only when genuinely justified.
5. **Composite SLOs that mask issues** — "99.9% across all endpoints" hides the endpoint at 95%. Track SLOs per endpoint or per critical journey.
6. **Ignoring SLO during incident response** — If the incident is caused by a known risk (e.g., risky deploy), that deploy should have been blocked by the error budget policy.
