# Performance Measurement

### Establishing Baselines

Instrument every layer of the stack. Without baselines, you cannot tell if an optimization helped or hurt.

| Layer | What to Measure | Tools |
|-------|----------------|-------|
| Application | Latency (P50/P95/P99), throughput, error rate per endpoint | OpenTelemetry, APM (Datadog, New Relic, Honeycomb) |
| Infrastructure | CPU, memory, disk I/O, network I/O | Prometheus + Node Exporter, Grafana |
| Database | Query latency, connections, cache hit ratio, replication lag, deadlocks | pg_stat_statements, EXPLAIN ANALYZE, slow query log |
| Frontend | LCP, INP, CLS, TTFB, FCP, JS parse time | RUM (CrUX, Web Vitals JS), Lighthouse |

### Percentile Metrics Deep Dive

- **P50 (median)**: Tells you what the "typical" user experiences — but it's misleading because it hides the tail. A service can have a 50ms P50 and a 10s P99 and still look good.
- **P95**: 95% of users are faster than this. Best single number for "most users experience acceptable performance."
- **P99**: Catches the outliers — GC pauses, cold starts, network contention. Critical for SLOs: "99% of requests complete within 500ms."
- **Histogram vs Summary**: Histograms let you compute arbitrary percentiles client-side (Prometheus `histogram_quantile`). Summaries precompute percentiles server-side but cannot be aggregated across dimensions. Prefer histograms.

### Latency Distribution & Long-Tail Latency

Long-tail latency — the few requests that take 10x longer than the median — is the most damaging to user experience. Common causes:
- **Coordinated omission**: Load tools that pause between requests (ignoring queued latency) report artificially low latency. wrk2 and k6 solve this with open-loop or constant-throughput modes.
- **Head-of-line blocking**: One slow request blocks subsequent requests in a single-threaded model.
- **Garbage collection pauses**: Stop-the-world GC in Java/C#/Go causes all threads to pause briefly — visible only at P99+.
- **Cold starts**: Serverless functions, connection pool warm-up, JVM warm-up — first request after idle is disproportionately slow.

### RED vs USE Methodologies

- **RED** (Rate, Errors, Duration): Application-focused. For every service: What is the request rate? How many are failing? How long do successful ones take?
- **USE** (Utilization, Saturation, Errors): Infrastructure-focused. For every resource: What is the utilization? Is it saturated (queue depth > 0)? Are there errors?

Use both in tandem — RED tells you _what_ is slow, USE tells you _which resource_ is the bottleneck.
