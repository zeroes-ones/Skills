# OpenTelemetry Guide — Production Field Manual

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Instrumentation Patterns](#instrumentation-patterns)
3. [Collector Deployment](#collector-deployment)
4. [Sampling Strategies](#sampling-strategies)
5. [Attribute Conventions](#attribute-conventions)
6. [Trace-Log-Metric Correlation](#trace-log-metric-correlation)
7. [Production Configurations](#production-configurations)

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    APPLICATION                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  OpenTelemetry SDK                                     │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │    │
│  │  │  Traces   │  │ Metrics  │  │  Logs (Bridge)   │    │    │
│  │  │  Provider │  │ Provider │  │  Provider        │    │    │
│  │  └────┬─────┘  └────┬─────┘  └────────┬─────────┘    │    │
│  │       │             │                 │               │    │
│  │  ┌────┴─────────────┴─────────────────┴──────────┐    │    │
│  │  │  OTLP Exporter (gRPC/HTTP)                    │    │    │
│  │  └──────────────────────┬────────────────────────┘    │    │
│  └─────────────────────────┼─────────────────────────────┘    │
└────────────────────────────┼──────────────────────────────────┘
                             │ OTLP
              ┌──────────────┴──────────────┐
              ▼                             ▼
   ┌──────────────────────┐    ┌──────────────────────┐
   │  Collector (Agent)   │    │  Collector (Gateway) │
   │  Per-node DaemonSet  │───▶│  Cluster-level       │
   │  - Receivers         │    │  - Batch processor    │
   │  - Processors        │    │  - Tail sampling      │
   │  - Exporters          │    │  - Exporters          │
   └──────────────────────┘    └──────────┬───────────┘
                                          │
                          ┌───────────────┼───────────────┐
                          ▼               ▼               ▼
                   ┌──────────┐   ┌──────────┐   ┌──────────┐
                   │  Tempo   │   │ Prometheus│   │  Loki    │
                   │  (Traces)│   │ (Metrics) │   │  (Logs)  │
                   └──────────┘   └──────────┘   └──────────┘
```

---

## Instrumentation Patterns

### Auto-Instrumentation — Zero-Code

```bash
# Node.js — auto-instrument with zero code changes
node --require @opentelemetry/auto-instrumentations-node/register app.js

# Python — auto-instrument via agent
opentelemetry-instrument \
  --traces_exporter otlp \
  --metrics_exporter otlp \
  --service_name my-service \
  python app.py

# Java — auto-instrument via Java agent
java -javaagent:opentelemetry-javaagent.jar \
  -Dotel.service.name=my-service \
  -Dotel.traces.exporter=otlp \
  -jar myapp.jar

# Kubernetes — inject via init container or sidecar
# Or use OpenTelemetry Operator for auto-instrumentation injection
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: java-instrumentation
spec:
  exporter:
    endpoint: http://otel-collector:4317
  propagators:
    - tracecontext
    - baggage
  java:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-java:latest
```

### Manual Instrumentation — When You Need Control

```python
# Python — manual span creation
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.amount", 99.99)

        # Child span for database call
        with tracer.start_as_current_span("db.lookup_customer") as db_span:
            db_span.set_attribute("db.system", "postgresql")
            db_span.set_attribute("db.operation", "SELECT")
            customer = db.query(order_id)

        # Child span for payment processing
        with tracer.start_as_current_span("payment.charge") as pay_span:
            pay_span.set_attribute("payment.provider", "stripe")
            charge_payment(customer, order_id)

        span.set_attribute("order.status", "completed")
```

```javascript
// Node.js — manual instrumentation
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('checkout-service');

async function processCheckout(cartId) {
  const span = tracer.startSpan('process_checkout', {
    attributes: { 'cart.id': cartId, 'cart.items': 5 }
  });

  try {
    await validateInventory(cartId);
    await chargePayment(cartId);
    span.setAttribute('checkout.status', 'success');
  } catch (error) {
    span.setAttribute('checkout.status', 'failed');
    span.recordException(error);
    span.setStatus({ code: trace.StatusCode.ERROR, message: error.message });
    throw error;
  } finally {
    span.end();
  }
}
```

### When to Use Auto vs Manual

| Auto-Instrumentation | Manual Instrumentation |
|---|---|
| Standard HTTP/gRPC/DB libraries | Custom business logic |
| Zero-code, fast onboarding | Domain-specific attributes |
| Covers ~80% of telemetry needs | Covers the remaining 20% — the most critical spans |
| Limited semantic context | Rich: `order.amount`, `search.query`, `experiment.variant` |
| **Start here.** Then add manual for gaps. | **Focus on critical user journeys.** |

---

## Collector Deployment

### Agent Mode — Per-Node DaemonSet

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-agent
spec:
  mode: daemonset
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      hostmetrics:
        collection_interval: 30s
        scrapers:
          cpu:
          memory:
          disk:
          network:
      kubeletstats:
        collection_interval: 30s

    processors:
      batch:
        send_batch_size: 8192
        timeout: 5s
      memory_limiter:
        check_interval: 1s
        limit_mib: 500
        spike_limit_mib: 150

    exporters:
      otlp:
        endpoint: otel-gateway-collector:4317
        tls:
          insecure: true
      logging:  # Debug only; remove in production
        loglevel: info

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [otlp]
        metrics:
          receivers: [otlp, hostmetrics, kubeletstats]
          processors: [memory_limiter, batch]
          exporters: [otlp]
```

### Gateway Mode — Cluster-Level Aggregation

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-gateway
spec:
  mode: deployment
  replicas: 3
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317

    processors:
      batch:
        send_batch_size: 8192
        timeout: 10s
      memory_limiter:
        check_interval: 1s
        limit_mib: 2000
      tail_sampling:
        policies:
          - name: error-policy
            type: status_code
            status_code: {status_codes: [ERROR]}
          - name: latency-policy
            type: latency
            latency: {threshold_ms: 500}
          - name: probabilistic-policy
            type: probabilistic
            probabilistic: {sampling_percentage: 10}

    exporters:
      otlp/tempo:
        endpoint: tempo:4317
        tls:
          insecure: true
      prometheus:
        endpoint: 0.0.0.0:8889

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, tail_sampling, batch]
          exporters: [otlp/tempo]
        metrics:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [prometheus]
```

### Agent vs Gateway Decision

| Agent | Gateway |
|---|---|
| Per-node, handles SDK export locally | Cluster-level, central aggregation |
| Light processing: memory limiter, batch | Heavy processing: tail sampling, filtering, routing |
| Avoids single point of failure | Single point of failure (mitigated by replicas) |
| Lower latency (same node) | Extra hop (acceptable with batching) |
| **Always deploy agent.** | **Add gateway when you need tail sampling or multi-backend routing.** |

---

## Sampling Strategies

### Head Sampling (at SDK/Agent)

```python
# Probabilistic: 10% of traces sampled
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

sampler = TraceIdRatioBased(1/10)  # 10%

# Parent-based: respect upstream sampling decision
from opentelemetry.sdk.trace.sampling import ParentBased

sampler = ParentBased(root=TraceIdRatioBased(1/10))
```

### Tail Sampling (at Collector Gateway)

```yaml
processors:
  tail_sampling:
    decision_wait: 30s  # Wait for all spans in trace
    num_traces: 50000   # In-memory cache size
    policies:
      # Always sample errors
      - name: errors
        type: status_code
        status_code:
          status_codes: [ERROR]

      # Always sample slow requests
      - name: high-latency
        type: latency
        latency:
          threshold_ms: 1000

      # Sample 10% of normal traffic
      - name: default
        type: probabilistic
        probabilistic:
          sampling_percentage: 10
```

### Sampling Decision Matrix

| Strategy | When | Pros | Cons |
|---|---|---|---|
| **Always-on (100%)** | Low-traffic, debugging, cost is no issue | Complete visibility | High cost, storage |
| **Head, Probabilistic** | High-traffic services | Predictable rate, simple | May miss rare errors |
| **Head, Rate-Limiting** | Bursty traffic | Bounds traces/second | Uneven distribution |
| **Tail** | Need all errors + slow traces | Catches anomalies | Adds latency, requires gateway |
| **Hybrid** | Production standard: head 10% + tail sample errors/slow | Best of both worlds | Operational complexity |

### Recommended Production Sampling

```
1. Head sample: 10% probabilistic via SDK (ParentBased)
2. Tail sample: 100% errors, 100% latency > 500ms, 10% remaining
3. Total capture: ~12-15% of trace volume
4. Cost: ~12-15% of full capture cost
5. Visibility: 100% of errors and performance anomalies + representative sample
```

---

## Attribute Conventions

### Required Span Attributes — Every Span

```yaml
# HTTP spans
http.method: GET
http.url: https://api.example.com/orders/12345
http.status_code: 200
http.route: /orders/:id
net.peer.name: api.example.com

# Database spans
db.system: postgresql
db.operation: SELECT
db.name: orders_db
db.statement: SELECT * FROM orders WHERE id = $1

# Messaging spans
messaging.system: kafka
messaging.destination: orders-topic
messaging.operation: receive

# RPC spans
rpc.system: grpc
rpc.service: OrderService
rpc.method: GetOrder
```

### Custom Attributes — Domain-Specific

```python
# ✅ Good: domain-specific, high-cardinality-but-filterable
span.set_attribute("order.id", "ord_abc123")
span.set_attribute("order.amount", 99.99)
span.set_attribute("order.currency", "USD")
span.set_attribute("customer.tier", "premium")
span.set_attribute("payment.provider", "stripe")
span.set_attribute("experiment.variant", "control")
span.set_attribute("feature_flag.new_checkout", True)

# ❌ Bad: unbounded cardinality (creates metric explosion)
span.set_attribute("user.email", user_email)  # Never — PII + cardinality bomb
span.set_attribute("search.query_raw", raw_query)  # High cardinality, potentially PII
span.set_attribute("request.body", full_body)  # Huge + potentially sensitive
```

### Attribute Cardinality Limits

| Cardinality | Examples | Safe for Metrics? | Safe for Traces? |
|---|---|---|---|
| Low (< 100) | `http.method`, `db.system`, `service.name` | ✅ | ✅ |
| Medium (100-1000) | `http.route`, `customer.tier`, `region` | ✅ With care | ✅ |
| High (1000-100000) | `order.id`, `user.id`, `session.id` | ❌ Never | ✅ With sampling |
| Unbounded | `user.email`, `request.body`, timestamps | ❌❌❌ | ❌ PII + massive |

---

## Trace-Log-Metric Correlation

### Trace ID in Structured Logs

```json
{
  "timestamp": "2026-07-21T14:32:00.123Z",
  "level": "INFO",
  "service": "checkout-service",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "message": "Order processed successfully",
  "order_id": "ord_abc123",
  "duration_ms": 245
}
```

```python
# Python — inject trace context into logs
from opentelemetry import trace

def log_with_trace(message, **kwargs):
    span = trace.get_current_span()
    ctx = span.get_span_context()
    log_data = {
        "trace_id": format(ctx.trace_id, '032x') if ctx.is_valid else None,
        "span_id": format(ctx.span_id, '016x') if ctx.is_valid else None,
        "message": message,
        **kwargs
    }
    logger.info(json.dumps(log_data))
```

### Exemplars — Metric-to-Trace Link

```promql
# Prometheus exemplar links a histogram bucket to a specific trace
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m])
)

# In Grafana: click on a histogram bucket → "View exemplars" → jump to trace
```

### Correlation Flow

```
1. User request arrives → trace_id generated
2. Middleware injects trace_id into logging context
3. Every log line includes trace_id + span_id
4. Metrics export exemplars (trace_id, value) alongside histogram buckets
5. Grafana links: Metric → Exemplar → Trace → Logs (by trace_id)
```

---

## Production Configurations

### SDK Configuration — TypeScript/Node.js

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { ParentBasedSampler, TraceIdRatioBasedSampler } from '@opentelemetry/sdk-trace-sampling';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'checkout-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: 'v2.3.1',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
    'k8s.namespace.name': 'prod',
    'k8s.pod.name': process.env.HOSTNAME,
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector.observability:4317',
  }),
  metricExporter: new OTLPMetricExporter({
    url: 'http://otel-collector.observability:4317',
  }),
  sampler: new ParentBasedSampler({
    root: new TraceIdRatioBasedSampler(0.1),  // 10%
  }),
  instrumentations: [
    // Auto-instrumentation for common libraries
  ],
});

sdk.start();

// Graceful shutdown
process.on('SIGTERM', () => {
  sdk.shutdown().then(() => console.log('OTel SDK shut down'));
});
```

### Collector — Production Hardened Config

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        max_recv_msg_size_mib: 32
        max_concurrent_streams: 100
      http:
        endpoint: 0.0.0.0:4318

processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 2000  # Based on pod memory limits
    spike_limit_mib: 500

  batch:
    send_batch_size: 8192
    timeout: 5s
    send_batch_max_size: 16384

  attributes:
    actions:
      - key: k8s.pod.name
        action: upsert
        from_attribute: k8s.pod.name  # Enrich from k8s metadata

  filter:
    traces:
      span:
        - 'attributes["http.url"] contains "/health"'  # Drop health checks
        - 'attributes["http.url"] contains "/metrics"'  # Drop metrics scrapes

  tail_sampling:
    decision_wait: 30s
    policies:
      - name: errors
        type: status_code
        status_code: {status_codes: [ERROR]}
      - name: slow-requests
        type: latency
        latency: {threshold_ms: 500}
      - name: default
        type: probabilistic
        probabilistic: {sampling_percentage: 10}

exporters:
  otlp/tempo:
    endpoint: tempo.monitoring:4317
    tls:
      insecure: true
    sending_queue:
      enabled: true
      num_consumers: 10
      queue_size: 10000
    retry_on_failure:
      enabled: true
      initial_interval: 5s
      max_interval: 30s
      max_elapsed_time: 300s

  prometheus:
    endpoint: 0.0.0.0:8889
    resource_to_telemetry_conversion:
      enabled: true

  logging:
    loglevel: warn  # Only warn/error in production

extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777

service:
  extensions: [health_check, pprof]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, filter, tail_sampling, batch]
      exporters: [otlp/tempo, logging]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, attributes, batch]
      exporters: [prometheus]
```

---

## Production Hardening Checklist

- [ ] All services have `service.name`, `service.version`, and `deployment.environment` resource attributes
- [ ] SDK exporters point to collector, not directly to backend (collector provides buffering, retry, sampling)
- [ ] Agent (DaemonSet) deployed on every node for low-latency local collection
- [ ] Gateway (Deployment ≥ 3 replicas) deployed for tail sampling and multi-backend routing
- [ ] Sampling strategy documented: head 10% probabilistic + tail 100% errors/latency
- [ ] Collector `memory_limiter` configured (≤ 80% of pod memory limit)
- [ ] Collector batch processor enabled with `send_batch_size` 8192+ and 5-10s timeout
- [ ] Health check endpoint (13133) configured for liveness/readiness probes
- [ ] Collector metrics exported (Prometheus) for self-monitoring
- [ ] `trace_id` injected into structured logs for trace-log correlation
- [ ] HTTP semantic conventions followed for all inbound/outbound HTTP spans
- [ ] PII/gdpr-sensitive data never stored in span attributes
- [ ] Graceful shutdown configured: SDK `shutdown()` + collector terminationGracePeriodSeconds
- [ ] Collector retry_on_failure configured with exponential backoff
- [ ] Filter processor drops health check and metrics scrape traces to reduce noise
