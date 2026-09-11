# Additional Resources — Resilience Pattern Engineer

> Deep knowledge loaded on demand. The SKILL.md holds the decisions and rules; this file holds the
> extended material: the pattern catalogue, the formulas worked through, the failure narratives, and
> the sources behind the claims.

---

## 1. Pattern catalogue

Each pattern below lists what it protects against, what it costs, and the failure it introduces if
misapplied. The cost column matters: **every pattern adds latency and a new failure surface**, which
is why Decision Tree 1 in SKILL.md requires justification per dependency rather than blanket
adoption.

| Pattern | Protects against | Cost | Fails when |
|---------|-----------------|------|-----------|
| **Timeout** (connect + read) | Hang; thread/pool exhaustion | Bounded latency; may cut off legitimately slow calls | Set without a deadline relationship — never fires, or fires constantly |
| **Retry with backoff** | Transient failures (network blip, 503, lock timeout) | Amplifies load during degradation | Applied to deterministic errors, or without jitter |
| **Jitter** | Retry synchronisation (thundering herd) | None — it is a free improvement | Absent. Fixed-delay retry is the defect |
| **Circuit breaker** | Repeated calls to a failing dependency; slow-flapping | Fails fast during open; requires recovery logic | Lifetime counter (never opens), or full-load half-open (recreates the outage) |
| **Bulkhead** | One dependency consuming all caller capacity | Wastes headroom; adds a queue | Sized from a round number rather than measurement |
| **Load shedding** | Saturation; queue-driven memory exhaustion | Rejects work that might have succeeded | No threshold, or threshold above the deadline |
| **Graceful degradation** | Full-path failure when a dependency is down | Reduced functionality; product decision required | Silent — wrong data indistinguishable from right |
| **Fallback / hedging** | Latency tails (hedge) or hard failure (fallback) | Duplicate work; cost | Fallback weakens authorization or returns unvalidated data |
| **Rate limiting / quotas** | Abuse; one caller starving others | Rejects legitimate bursts | Global rather than per-caller in a multi-tenant system |
| **Health / readiness gating** | Routing traffic to an instance that cannot serve | Slower rollout | Liveness-only checks (availability theatre) |

---

## 2. The formulas, worked

### 2.1 Deadline allocation

A user-facing deadline is a budget. Split it across the dependencies on the path:

```
deadline            = 2000 ms   (user-facing)
overhead (serialise, render, auth) = 200 ms
available for dependencies         = 1800 ms
dependencies on path               = 4
per-dependency budget              = 1800 / 4 = 450 ms
attempt budget                     = 2 attempts  → per-attempt timeout = 450 / 2 = 225 ms
connect timeout                    = 50 ms  (a fraction of the attempt)
```

Rule: the per-dependency budgets must **sum to ≤ the deadline**. Three timeouts each equal to the
full deadline means the path has no deadline at all.

### 2.2 Full jitter

```
sleep = random(0, min(cap, base * 2^attempt))
```

| attempt | `base*2^n` (base 100ms, cap 2s) | full jitter range |
|---------|-------------------------------|-------------------|
| 0 | 100 ms | 0–100 ms |
| 1 | 200 ms | 0–200 ms |
| 2 | 400 ms | 0–400 ms |
| 3 | 800 ms | 0–800 ms |
| 4 | 1600 ms | 0–1600 ms |
| 5+ | 2000 ms (cap) | 0–2000 ms |

**Why full jitter.** With fixed delay, N clients retry simultaneously and the dependency sees load
multiply by N in that instant. Full jitter spreads the same retries across the whole interval, so
the instantaneous rate stays near the original. "Equal jitter" (`base/2 + random(0, base/2)`) also
works but keeps a floor, so it spreads less for the same complexity.

### 2.3 Retry amplification (why this matters)

10,000 clients, 3 retries each, fixed 1s delay, a dependency that has just started failing:

```
t=0s     10,000 requests   (original load)
t=1s     10,000 requests   (all clients retry #1 at once)
t=2s     10,000 requests   (all clients retry #2 at once)
t=3s     10,000 requests   (all clients retry #3 at once)
→ the dependency sees 4× load during the exact window it is failing
```

With full jitter the same retries arrive spread over 0–1s, 0–2s, 0–4s — the instantaneous rate
rises far less. This is the single most common self-inflicted outage.

### 2.4 Bulkhead sizing

Measured (preferred):

```
size = peak_concurrent_in_flight(p99, 5-min window) * 1.3 headroom
```

Unmeasured (Little's Law, label ESTIMATED):

```
concurrency = arrival_rate * mean_latency
e.g. 200 req/s * 0.25 s = 50 concurrent  → size = 50 * 1.3 = 65
```

Note what the measurement is: **concurrent in-flight to that dependency**, not requests per second.
RPS without latency gives no concurrency figure.

### 2.5 Shed threshold

Shed where queue wait exceeds the deadline, not at queue capacity:

```
shed_when: queue_wait_p99 > deadline
```

Alerting on **queue wait** rather than depth is what distinguishes an early warning from a
post-mortem.

---

## 3. Failure narratives

### 3.1 The retry storm that doubled the outage

A payments service called a card processor with a 3-attempt fixed-delay retry at 1s. The processor
degraded during a regional network event, returning 503s slowly. Every one of the service's ~4,000
in-flight callers retried in lockstep, so the processor — already struggling — saw 4× its normal
load in each 1-second window. Its recovery took far longer than the original fault, and the
merchant-facing outage lasted 40 minutes instead of the ~5 minutes the network event warranted.

**Fix:** full jitter plus a deadline-derived attempt budget, plus a circuit breaker that stopped
retrying once the failure rate crossed a rolling-window threshold.

**Lesson:** the retries *were* the outage. The dependency's fault was the trigger.

### 3.2 The timeout that never fired

A service set a generous 30-second timeout on a dependency whose caller had a 5-second user-facing
deadline. Under load, the dependency slowed to 20 seconds. Every request hit the *caller's* deadline
first, so users saw timeouts, the service logged "upstream slow", and the 30-second timeout never
appeared in any log. The team spent a day investigating a timeout that could not fire.

**Fix:** derive the timeout from the deadline (`deadline ÷ attempts − overhead`) and assert the
relationship in review.

**Lesson:** a timeout larger than the caller's budget is documentation, not protection.

### 3.3 The breaker that protected nothing

A team configured a circuit breaker on a dependency and considered the risk handled. It was
threshold-based on a **lifetime** error counter with a high limit. During a real incident the
counter never crossed the threshold, so the breaker stayed closed and every request paid the full
latency. Separately, no one had ever observed the breaker open — there was no test that made it fire.

**Fix:** rolling-window threshold with a volume floor, plus a chaos test that must open it.

**Lesson:** an unopened breaker is indistinguishable from no breaker. Configured ≠ proven.

### 3.4 The noisy neighbour

A multi-tenant SaaS used one shared database connection pool for all tenants. One tenant ran a bulk
export, saturated the pool, and every other tenant's requests queued behind it. The service was
"up" — health checks passed, the process was alive — while most customers saw timeouts.

**Fix:** per-tenant bulkheads sized from each tenant's measured concurrency, plus a shed policy when
a tenant exceeds its share.

**Lesson:** bulkheads protect the caller from a *sibling*, not just from the callee.

### 3.5 The recovery storm

After a 15-minute dependency outage, the dependency came back healthy. All clients reconnected at
once into cold caches, and the resulting load spike took it down again within two minutes. The
second outage was longer than the first.

**Fix:** jittered reconnection, a half-open breaker ramp (single probe, then gradual), and cache
warm-up before full traffic.

**Lesson:** recovery is a distinct failure mode. Design for it as carefully as for the fault.

### 3.6 The silent degradation

A search dependency went down. The service fell back to an empty result set and returned HTTP 200
with no marker. Users saw "no results" for six hours; support logged it as a search-quality
complaint, and engineering learned of it from a customer escalation the next day.

**Fix:** every degradation path emits a metric, a log, and a response marker (a staleness flag or a
`degraded: true` field).

**Lesson:** silent degradation is indistinguishable from correctness until someone notices wrong
data — and they will notice publicly.

---

## 4. Verification recipes

### 4.1 Proving a read timeout fires

```bash
# Inject a hang (no response) and assert the client gives up at the configured timeout.
# Any HTTP stub that sleeps works; the point is that the call MUST fail at ~timeout.
time curl -sS --max-time 5 http://stub/hang   # expect failure at the read timeout, not at 5s
```

If the call returns after the *caller's* deadline rather than the configured read timeout, the
timeout is on the wrong layer.

### 4.2 Proving a breaker opens

```
1. Point the client at a stub that always fails.
2. Drive traffic past the failure-rate threshold within the rolling window.
3. Assert: the breaker state transitions to OPEN (metric or log).
4. Assert: subsequent calls fail fast (< a few ms) without reaching the dependency.
5. Restore the stub; assert the breaker moves to HALF_OPEN and then CLOSED via the ramp.
```

A breaker with no step 3 observed has never been proven.

### 4.3 Proving a bulkhead isolates

```
1. Give tenant A traffic far above its share.
2. Measure tenant B's p99 latency.
3. Assert: B's latency is unchanged while A is throttled.
```

If B degrades with A, the isolation does not exist.

### 4.4 Proving degradation is observable

```
1. Make the dependency fail.
2. Assert: the degradation metric increments, the log line appears, and the response carries
   the degradation marker.
```

All three, not just one — a metric without a response marker still returns wrong data silently to
the client.

---

## 5. Failure-mode checklist (the five shapes from R6)

For every dependency, walk this table. Clean fast failure is the easy case and the only one most
teams plan for.

| Mode | What it looks like | Defence | Test that proves it |
|------|-------------------|---------|---------------------|
| **Slow** | Latency climbs; requests succeed but late | Deadline-derived timeout; hedge for tails | Latency injection above the timeout |
| **Hang** | No response at all; connection open | Read timeout (not just connect); pool cap | Hang injection; assert timeout fires |
| **Partial** | Response truncated or missing fields | Response validation; treat as failure | Stub returning truncated payload |
| **Wrong-200** | HTTP 200 with empty/wrong data | Schema assertion; sentinel checks | Stub returning valid-shape-but-wrong data |
| **Flapping** | Intermittent errors over minutes | Circuit breaker on a rolling window | Repeated fail/healthy cycles; assert open/close without oscillation |

---

## 6. Sources

The claims in SKILL.md and this file trace to the following. Where a source is weaker (preprint,
thesis, vendor survey), it is marked — the incident-cost ranges and pattern guidance are directional,
not audited.

| Claim | Source | Strength |
|-------|--------|----------|
| Over half of incidents stem from software changes; config updates link to high severity | TU Delft analysis of 348 VOID incident reports (2025) | Thesis — directionally strong |
| ~Half of incidents are non-code; >90% mitigated without a code change | Microsoft Teams study, ACM | Peer-reviewed / industrial |
| Top secondary contributors: communication 48.2%, monitoring 46.5%, documentation 41.1% | TU Delft, 1,500 postmortems | Thesis |
| Cascading failure is the characteristic modern mode | AWS (Oct 2025, DNS automation race condition), Azure (Oct 2025, config change), CrowdStrike (2024, config artifact) | Public incident reports |
| Capacity and code defects are leading root causes | TU Delft VOID analysis | Thesis |
| Retry storms / thundering herds | Standard reliability practice; documented in AWS and Google SRE material | Established practice |
| Jitter strategy (full vs. equal) | AWS Architecture Blog, "Exponential Backoff and Jitter" | Vendor engineering — widely reproduced |
| Bulkhead / isolation patterns | Release It! (Nygard) and successor pattern literature | Established practice |
| Little's Law for concurrency | Queueing theory; standard capacity practice | Foundational |

**Explicitly not claimed:** that any pattern set makes a system failure-proof. The patterns reduce
blast radius and recovery time; they do not remove the need for the layers in the wider research
(`docs/missing-skills-research.md` §4).

---

## 7. Related reading in this library

- `chaos-engineer` — running these defences as ongoing experiments, blast-radius control, GameDays
- `site-reliability-engineer` — SLOs and error budgets, which bound how much failure is acceptable
- `performance-engineer` — latency budgets and load testing, which validate the numbers used here
- `incident-responder` — what to do when a defence fails anyway
- `observability-engineer` — the metrics these patterns depend on (breaker state, shed count, degradation marker)
