# Production Guardrail Metrics

## Metric Targets

| Metric | Target | Alert Threshold | Rationale |
|--------|--------|----------------|-----------|
| **FPR per layer** | < 0.1% | > 0.5% | At 0.5% FPR on 1M req/day = 5,000 false blocks daily |
| **FNR per layer** | < 5% | > 10% | FNR > 10% means 1 in 10 harmful inputs passes undetected |
| **Block rate** | 0.1-2% | > 5% | Sudden spike indicates attack, new bypass vector, or classifier degradation |
| **Latency p50** | < 15ms | > 30ms | Per-layer latency budget; aggregate must stay < 100ms |
| **Latency p99** | < 50ms | > 100ms | Tail latency kills user experience; parallelize where possible |
| **Challenge rate** | 0.5-3% | > 10% | High challenge rate suggests threshold too aggressive |
| **Retry success rate** | > 80% | < 50% | Users rephrasing after challenge should succeed > 80% of the time |
| **Guard collapse score** | > 0.85 | < 0.70 | Cosine similarity below 0.7 = safety alignment degraded |

## OpenTelemetry Instrumentation

```python
from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider

meter = metrics.get_meter("guardrails")
tracer = trace.get_tracer("guardrails")

# Counters
fpr_counter = meter.create_counter(
    "guardrail.false_positives",
    description="False positive decisions per layer"
)
fnr_counter = meter.create_counter(
    "guardrail.false_negatives",
    description="False negative decisions (detected post-hoc)"
)
block_counter = meter.create_counter(
    "guardrail.blocks",
    description="Block decisions by layer and reason"
)

# Histograms
latency_histogram = meter.create_histogram(
    "guardrail.latency_ms",
    description="Per-layer guardrail latency",
    unit="ms"
)

# Gauges
safety_similarity = meter.create_observable_gauge(
    "guardrail.collapse_score",
    description="Safety embedding cosine similarity (FW-SSR)"
)

# Instrumented guardrail call
@tracer.start_as_current_span("guardrail.input_layer")
def instrumented_input_guardrail(user_input: str) -> dict:
    start = time.time()
    result = input_guardrail(user_input)
    elapsed = (time.time() - start) * 1000

    span = trace.get_current_span()
    span.set_attribute("guardrail.layer", "input")
    span.set_attribute("guardrail.jailbreak_score", result.get("confidence", {}).get("jailbreak", 0))
    span.set_attribute("guardrail.decision", "block" if not result["allow"] else "allow")

    latency_histogram.record(elapsed, {"layer": "input"})

    if not result["allow"]:
        block_counter.add(1, {"layer": "input", "reason": result["flags"][0]})

    return result
```

## Prometheus Recording Rules

```yaml
groups:
  - name: guardrail_alerts
    rules:
      - alert: HighFPR
        expr: rate(guardrail_false_positives[5m]) / rate(guardrail_total_checks[5m]) > 0.005
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Guardrail FPR exceeding 0.5%"

      - alert: HighBlockRate
        expr: rate(guardrail_blocks[5m]) / rate(guardrail_total_checks[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Block rate anomaly — possible attack in progress"

      - alert: GuardCollapse
        expr: guardrail_collapse_score < 0.7
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Safety embedding similarity dropped below threshold"

      - alert: HighLatency
        expr: histogram_quantile(0.99, guardrail_latency_ms) > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Guardrail p99 latency exceeding 100ms budget"
```

## Audit Logging Schema

```json
{
  "timestamp": "2026-07-24T12:09:00Z",
  "session_id": "sess_abc123",
  "layer": "input",
  "classifier": "prompt_guard",
  "decision": "block",
  "score": 0.92,
  "reason": "jailbreak_attempt",
  "input_hash": "sha256:b4f8...",
  "output_hash": null,
  "model": "gpt-4o",
  "latency_ms": 12.4,
  "operator": "auto"
}
```

## Dashboard Layout

```
┌─────────────────────┐  ┌─────────────────────┐
│    Block Rate (1h)    │  │    FPR by Layer       │
│    ┌─────────────┐   │  │  Input:   0.08%      │
│    │ ▁▂▃▅▃▂▁▂▃▅  │   │  │  Prompt:  0.05%      │
│    │ Current: 1.2%│   │  │  Runtime: 0.12%      │
│    └─────────────┘   │  │  Output:  0.03%      │
├─────────────────────┤  ├─────────────────────┤
│   Latency p99 (ms)   │  │   Collapse Score      │
│   Input:   8.2       │  │   Current: 0.91       │
│   Prompt:  12.1      │  │   Threshold: 0.70     │
│   Runtime: 15.3      │  │   Trend:    →         │
│   Output:  22.7      │  │                       │
│   Total:   58.3      │  │                       │
└─────────────────────┘  └─────────────────────┘
```
