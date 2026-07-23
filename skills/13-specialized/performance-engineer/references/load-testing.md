# Load Testing

### k6 Scripts

Use `k6 run script.js` with the `--out json` flag for detailed results.

**Ramp-up (Baseline)**:
```javascript
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '5m', target: 100 },   // ramp up to 100 users
    { duration: '10m', target: 100 },  // hold
    { duration: '5m', target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<2000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/endpoint');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```


**What good looks like:** Performance profile identifies the top 3 bottlenecks ranked by impact. Each optimization includes measured before/after with p50/p95/p99 latency. Load test at 2x peak QPS shows p95 < 500ms. Flame graph available for CPU profiling.

**Soak (Endurance)** — detect memory leaks, connection leaks:
```javascript
export const options = {
  stages: [
    { duration: '10m', target: 50 },   // ramp to moderate load
    { duration: '8h', target: 50 },    // hold for 8 hours
    { duration: '5m', target: 0 },     // ramp down
  ],
};
```

**Spike (Burst)** — test auto-scaling and queue buffering:
```javascript
export const options = {
  stages: [
    { duration: '1m', target: 10 },    // baseline
    { duration: '10s', target: 500 },  // sudden spike to 500
    { duration: '5m', target: 500 },   // hold spike
    { duration: '5m', target: 10 },    // recover
  ],
};
```

**Stress (Breaking point)** — find where the system breaks:
```javascript
export const options = {
  stages: [
    { duration: '5m', target: 200 },
    { duration: '5m', target: 400 },
    { duration: '5m', target: 600 },
    { duration: '5m', target: 800 },
    { duration: '5m', target: 1000 },
  ],
};
```

### wrk2 — Constant-Throughput Latency Testing

wrk2 maintains a fixed request rate (unlike wrk's open-loop), making it ideal for correct latency-at-load measurements:

```bash
# 10,000 requests/sec for 60 seconds, 4 threads, 100 connections
wrk2 -t4 -c100 -d60s -R10000 --latency https://api.example.com/endpoint
```

Key difference from k6: wrk2 is L7 HTTP only, no scripting. Best for micro-benchmarks of a single endpoint.

### Artillery — YAML-Based Scenario Testing

```yaml
config:
  target: 'https://api.example.com'
  phases:
    - duration: 60
      arrivalRate: 5
      rampTo: 50
      name: 'Warm up'
    - duration: 600
      arrivalRate: 50
      name: 'Sustained load'
  defaults:
    headers:
      Authorization: 'Bearer {{ token }}'

scenarios:
  - name: 'User browsing flow'
    flow:
      - get:
          url: '/api/products'
          capture:
            - json: '$.products[0].id'
              as: 'productId'
      - think: 3
      - get:
          url: '/api/products/{{ productId }}'
      - post:
          url: '/api/cart'
          json:
            productId: '{{ productId }}'
            quantity: 1
```

Artillery excels at multi-step user flows and WebSocket testing.

### Infrastructure Sizing from Load Test Results

- **Correlating load to resources**: If 200 VUs produce 500 req/s at 60% CPU, then 400 VUs (1000 req/s) will need ~2x the instances or ~83% CPU.
- **Cost prediction**: (peak_req_per_sec / capacity_per_instance) × instance_cost × replica_for_redundancy = monthly compute cost at scale.
- **Headroom**: Design for 60-70% utilization at peak. Above 80%, response times degrade exponentially (queueing theory).
- **Bottleneck identification**: Instrument every hop. If CPU is at 30% but latency is high — it's not CPU, it's the DB/network/lock contention.

### Statistical Analysis of Results

- **Interpreting percentiles**: Flat curve up to P95 then a "knee" means a specific bottleneck activates at that load (e.g., GC kicks in, connection pool exhausts).
- **Identifying bottlenecks from data**: High P50 + low P50 = fast median but rare events are terrible (GC/lock contention). Low P50 + high P95 = queueing delay or resource saturation at peak. Growing P50 over time in soak = memory leak.
- **Comparing before/after**: Run exactly the same test (same tool, same parameters, same environment), compare percentiles at the same request rate.
