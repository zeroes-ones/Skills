# Orchestra Platform — Chaos Engineering

**Owner:** Reliability Engineering | **Date:** 2026-07-21 | **Tool:** Chaos Mesh + Litmus

## Experiment Catalog

All 5 experiments passed GameDay validation in staging before production execution.

| # | Experiment | Result | Recovery | Errors |
|---|---|---|---|---|
| 1 | **Pod kill (random)** — kill 1 template-engine pod every 60s for 10 min | ✅ Pass | 0.3s (Istio retry) | 0 |
| 2 | **AZ failure (us-east-1a)** — simulate full availability zone outage | ✅ Pass | 45s traffic shift to 1b/1c | 2 (0.001%) |
| 3 | **Redis primary failover** — force primary node restart | ✅ Pass | 8s failover; 12 queued requests replayed via RabbitMQ | 0 data loss |
| 4 | **DB replica failure** — terminate 1 of 2 read replicas | ✅ Pass | read traffic to remaining replica; p95 120ms → 180ms | 0 (within SLO) |
| 5 | **Network latency injection** — 200ms latency on template-engine | ✅ Pass | circuit breaker opened after 5 failures; cache fallback active | 3-min degraded |

## GameDay Q4 2026 — Findings

**Finding 1:** Circuit breaker was missing on the `plugin-registry` service. Rediscovered during the AZ failure simulation when plugin-registry was in the blast radius without protection. **Action:** Circuit breaker added. Completed within 3 days.

**Finding 2:** Redis reconnection timeout defaulted to 60 seconds — too long for a service that handles real-time requests. **Action:** Reduced to 15 seconds with exponential backoff. Completed within 7 days.

Both action items resolved and verified in follow-up GameDay.

## Resilience Score

| Dimension | Pre-GameDay | Post-GameDay |
|---|---|---|
| Circuit breakers | 70% coverage | 100% coverage |
| Retry + backoff | 85% | 90% |
| Timeouts configured | 80% | 95% |
| Fallback paths | 75% | 85% |
| Health checks | 90% | 95% |
| Graceful degradation | 90% | 95% |
| **Overall** | **82%** | **94%** |

## Engineering Principle

> **Never experiment in production without a verified kill switch.** Blast radius must be measured before, during, and after every experiment. Every chaos experiment starts with the question: "How do we stop this if it goes wrong?"
