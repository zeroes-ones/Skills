# Eval Metrics Dashboard

<!-- QUICK: 30s -- Real-time dashboard tracking agent evaluation metrics: pass rates, quality scores, latency distributions, token costs, drift indicators, and safety scores across all evaluation tiers. -->

## Dashboard Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Eval Metrics Dashboard                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Summary    │  │  Quality    │  │  Safety     │              │
│  │  KPIs       │  │  Trends     │  │  Monitor    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Cost       │  │  Drift      │  │  Pipeline   │              │
│  │  Analysis   │  │  Detection  │  │  Health     │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Historical Trends (30/90/365 days)            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Key Metrics

### Tier 1: Summary KPIs (Executive View)

```python
SUMMARY_KPIS = {
    "overall_pass_rate": {
        "description": "Weighted pass rate across all evaluation tiers",
        "target": "≥ 0.90",
        "alert_threshold": "< 0.85",
        "calculation": "(L1_pass_rate * 0.3 + L2_pass_rate * 0.4 + L3_pass_rate * 0.3)"
    },
    "weekly_eval_runs": {
        "description": "Total evaluation runs in the past 7 days",
        "target": "≥ 50 (maintain statistical power)",
        "alert_threshold": "< 30"
    },
    "cost_per_eval": {
        "description": "Average cost per full evaluation run",
        "target": "≤ $25.00",
        "alert_threshold": "> $35.00"
    },
    "time_to_decision": {
        "description": "Average time from PR to eval gate decision",
        "target": "≤ 15 minutes",
        "alert_threshold": "> 25 minutes"
    },
    "false_positive_rate": {
        "description": "Rate at which gates block good changes",
        "target": "≤ 0.05 (α)",
        "alert_threshold": "> 0.08"
    },
    "false_negative_rate": {
        "description": "Rate at which gates pass bad changes",
        "target": "≤ 0.20 (β)",
        "alert_threshold": "> 0.30"
    }
}
```

### Tier 2: Quality Trends

```python
QUALITY_TRENDS = {
    "dimension_scores": {
        "description": "Time series of LLM-as-judge scores per dimension",
        "dimensions": ["completeness", "correctness", "tool_usage", "efficiency", "safety"],
        "visualization": "sparkline with CI bands",
        "alert": "any dimension drops > 0.3 points in 7-day rolling average"
    },
    "scenario_pass_rates": {
        "description": "Per-scenario pass rates over time",
        "visualization": "heatmap (scenario × date)",
        "alert": "any scenario drops below 0.80 for 3 consecutive days"
    },
    "hallucination_rate": {
        "description": "Fraction of outputs containing unsupported claims",
        "target": "≤ 0.05",
        "alert_threshold": "> 0.08",
        "calculation": "unsupported_claims / total_factual_claims"
    },
    "inter_rater_kappa": {
        "description": "Cohen's kappa between LLM judge and human raters",
        "target": "≥ 0.70",
        "alert_threshold": "< 0.60",
        "cadence": "monthly calibration check"
    }
}
```

### Tier 3: Safety Monitor

```python
SAFETY_METRICS = {
    "prompt_injection_resistance": {
        "description": "Pass rate on prompt injection test suite",
        "target": "≥ 0.98",
        "alert_threshold": "< 0.95",
        "sub_metrics": {
            "system_prompt_extraction": "target: 1.00",
            "safety_bypass": "target: 1.00",
            "data_exfiltration": "target: 1.00",
            "tool_manipulation": "target: 0.98",
            "indirect_injection": "target: 0.95"
        }
    },
    "harmful_output_rate": {
        "description": "Fraction of outputs flagged by safety classifier",
        "target": "≤ 0.001 (0.1%)",
        "alert_threshold": "> 0.005 (0.5%)"
    },
    "refusal_accuracy": {
        "description": "Correct refusal rate (refuse when should, comply when should)",
        "target": "≥ 0.95",
        "sub_metrics": {
            "correct_refusal": "refused harmful request",
            "false_refusal": "refused benign request (over-caution)",
            "false_compliance": "complied with harmful request (under-caution)"
        }
    },
    "pii_exposure": {
        "description": "Instances of PII in agent output",
        "target": "0",
        "alert_threshold": "> 0 (immediate alert)"
    }
}
```

### Tier 4: Cost Analysis

```python
COST_METRICS = {
    "total_monthly_spend": {
        "description": "Total evaluation cost this month",
        "budget": "$500/month",
        "alert_threshold": "> $400 (80% of budget)",
        "breakdown": "per_gate, per_agent_version, per_team"
    },
    "cost_per_decision": {
        "description": "Average cost per merge/no-merge decision",
        "target": "≤ $20",
        "calculation": "total_spend / total_decisions"
    },
    "token_efficiency": {
        "description": "Useful evaluation tokens / total tokens",
        "target": "≥ 0.70",
        "alert_threshold": "< 0.60"
    },
    "sprt_savings": {
        "description": "Cost saved by SPRT early stopping vs fixed-sample",
        "target": "≥ 40% vs fixed n=100",
        "calculation": "1 - (sprt_cost / fixed_sample_cost)"
    }
}
```

### Tier 5: Drift Detection

```python
DRIFT_METRICS = {
    "embedding_drift": {
        "description": "Cosine distance between current and baseline output embeddings",
        "target": "< 0.05",
        "alert_threshold": "> 0.15",
        "trend": "7-day rolling average"
    },
    "token_budget_drift": {
        "description": "Percent change in mean tokens per request",
        "target": "within ±10%",
        "alert_threshold": "> ±20%",
        "sub_metrics": ["prompt_tokens", "completion_tokens", "total_tokens"]
    },
    "tool_usage_drift": {
        "description": "Significant changes in tool call frequency",
        "alert_threshold": "> 10 percentage point change for any tool"
    },
    "quality_score_drift": {
        "description": "Statistically significant changes in judge scores",
        "method": "Mann-Whitney U, p < 0.05, Cohen's d > 0.3"
    }
}
```

### Tier 6: Pipeline Health

```python
PIPELINE_HEALTH = {
    "gate_pass_rates": {
        "description": "Pass rate per evaluation gate",
        "gates": ["l1_tool", "l2_scenario", "l3_e2e", "canary"],
        "alert": "any gate pass rate drops below 90% of 30-day average"
    },
    "gate_latency": {
        "description": "P50/P95/P99 latency per gate",
        "l1_target": "P95 < 120s",
        "l2_target": "P95 < 600s",
        "l3_target": "P95 < 1800s"
    },
    "eval_success_rate": {
        "description": "Fraction of eval runs that complete without infra errors",
        "target": "≥ 0.98",
        "alert_threshold": "< 0.95",
        "failure_reasons": ["timeout", "OOM", "network_error", "container_failure"]
    },
    "concurrency_utilization": {
        "description": "Fraction of available eval workers in use",
        "target": "60-80%",
        "alert_threshold": "> 90% (add workers) or < 30% (reduce cost)"
    }
}
```

## Dashboard Implementation

### Prometheus Metrics

```python
from prometheus_client import Counter, Gauge, Histogram, Summary

# L1 Tool Tests
l1_tests_total = Counter('eval_l1_tests_total', 'Total L1 tests run', ['result'])
l1_test_duration = Histogram('eval_l1_test_duration_seconds', 'L1 test duration')

# L2 Scenario Tests
l2_pass_rate = Gauge('eval_l2_pass_rate', 'L2 scenario pass rate')
l2_sprt_decision = Gauge('eval_l2_sprt_decision', 'SPRT decision', ['decision'])

# L3 E2E Tests
l3_completion_rate = Gauge('eval_l3_completion_rate', 'E2E completion rate')
l3_phase_success = Gauge('eval_l3_phase_success', 'Per-phase success rate', ['phase'])

# Quality
judge_score = Gauge('eval_judge_score', 'LLM-as-judge dimension score', ['dimension'])
hallucination_rate = Gauge('eval_hallucination_rate', 'Hallucination rate')
judge_kappa = Gauge('eval_judge_kappa', 'Cohen kappa vs human raters')

# Safety
injection_pass_rate = Gauge('eval_injection_pass_rate', 'Injection test pass rate', ['category'])
harmful_output_rate = Gauge('eval_harmful_output_rate', 'Harmful output rate')

# Cost
eval_cost_total = Counter('eval_cost_total_dollars', 'Total eval cost', ['gate'])
token_usage = Counter('eval_token_usage_total', 'Total tokens used', ['type'])

# Drift
embedding_drift = Gauge('eval_embedding_drift', 'Output embedding drift score')
token_drift_pct = Gauge('eval_token_drift_percent', 'Token budget drift percentage', ['type'])

# Decision
merge_blocked = Counter('eval_merge_blocked_total', 'Merges blocked by eval gates', ['gate'])
false_positive = Counter('eval_false_positive_total', 'False positive gate blocks')
false_negative = Counter('eval_false_negative_total', 'False negative gate passes')
```

### Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "Agent Evaluation Pipeline",
    "panels": [
      {
        "title": "Overall Pass Rate (7-day)",
        "targets": [
          {
            "expr": "avg(eval_l2_pass_rate[7d]) * 0.4 + avg(eval_l1_pass_rate[7d]) * 0.3 + avg(eval_l3_completion_rate[7d]) * 0.3"
          }
        ],
        "thresholds": [
          {"value": 0.85, "color": "red"},
          {"value": 0.90, "color": "yellow"},
          {"value": 0.95, "color": "green"}
        ]
      },
      {
        "title": "Quality Dimensions (Heatmap)",
        "targets": [
          {
            "expr": "eval_judge_score",
            "legendFormat": "{{dimension}}"
          }
        ]
      },
      {
        "title": "Cost per Decision ($)",
        "targets": [
          {
            "expr": "rate(eval_cost_total_dollars[1h]) / rate(eval_merge_blocked_total[1h])"
          }
        ]
      },
      {
        "title": "Embedding Drift",
        "targets": [
          {
            "expr": "eval_embedding_drift",
            "legendFormat": "Drift Score"
          }
        ],
        "thresholds": [
          {"value": 0.05, "color": "green"},
          {"value": 0.15, "color": "yellow"},
          {"value": 0.25, "color": "red"}
        ]
      },
      {
        "title": "Prompt Injection Resistance",
        "targets": [
          {
            "expr": "eval_injection_pass_rate",
            "legendFormat": "{{category}}"
          }
        ]
      }
    ]
  }
}
```

## Alert Rules

```yaml
# prometheus-alerts.yml
groups:
  - name: eval_pipeline_alerts
    rules:
      - alert: EvalQualityDegradation
        expr: avg(eval_l2_pass_rate[1h]) < 0.85
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "L2 scenario pass rate dropped below 85%"

      - alert: EvalCostOverrun
        expr: sum(increase(eval_cost_total_dollars[30d])) > 500
        labels:
          severity: warning
        annotations:
          summary: "Monthly eval cost exceeded $500 budget"

      - alert: SafetyRegression
        expr: eval_injection_pass_rate{category="system_prompt_extraction"} < 1.0
        labels:
          severity: critical
        annotations:
          summary: "Prompt injection resistance degraded — system prompt extractable"

      - alert: BehavioralDriftDetected
        expr: eval_embedding_drift > 0.15
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Agent behavior drift detected (embedding similarity < 0.85)"

      - alert: JudgeDecalibration
        expr: eval_judge_kappa < 0.60
        labels:
          severity: warning
        annotations:
          summary: "LLM judge kappa dropped below 0.60 — recalibration needed"
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Dashboard shows only pass/fail | Cannot diagnose root cause of degradation | Show dimension-level scores, per-scenario breakdowns, and trend lines |
| No alert thresholds defined | Team discovers degradation days later from user complaints | Define alert thresholds for every metric; automate alerting |
| Only showing point estimates | "0.92" without CI is misleading; could be 0.85-0.99 range | Always show confidence intervals alongside point estimates |
| Dashboard not visible to product team | Product decisions about agent quality made without data | Share dashboard with product; add executive summary panel for non-technical stakeholders |
