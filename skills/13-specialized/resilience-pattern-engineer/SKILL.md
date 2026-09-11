---
name: resilience-pattern-engineer
description: >
  Use when designing or auditing how a system behaves when a dependency degrades — adding
  timeouts, retries, circuit breakers, bulkheads, load shedding, graceful degradation or
  fallback chains, or when a cascading failure has already happened. Handles per-dependency
  pattern selection, retry-storm and jitter mathematics, bulkhead sizing, degradation
  ladders, blast-radius containment, and per-pattern verification including the chaos test
  that proves each defence actually fires. Do NOT use for load testing and capacity sizing
  (performance-engineer, capacity-planning-engineer), chaos experiment design as an ongoing
  programme (chaos-engineer), SLO and error-budget policy (site-reliability-engineer), or
  live incident command (incident-responder).
author: Sandeep Kumar Penchala
license: MIT
type: specialized
status: stable
version: 1.0.0
updated: 2026-09-11
tags:
  - resilience
  - circuit-breaker
  - bulkhead
  - timeout
  - retry
  - backoff
  - jitter
  - load-shedding
  - graceful-degradation
  - cascading-failure
  - fault-tolerance
token_budget: 3500
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
chain:
  examples:
    - skills/13-specialized/resilience-pattern-engineer/examples/backtest
  consumes_from:
    - system-architect
    - cloud-architect
    - api-designer
    - event-driven-architect
    - observability-engineer
    - site-reliability-engineer
    - configuration-change-safety
  feeds_into:
    - chaos-engineer
    - incident-responder
    - performance-engineer
    - observability-engineer
    - release-manager
workflow:
  artifacts:
    inputs: [architecture, dependency-inventory]
    outputs: [resilience-plan]
  completion:
    criteria:
      - Every remote dependency has an explicit timeout budget, never an inherited default
      - Every retry policy uses jittered backoff and declares a total attempt budget
      - Every degradation path names the user-visible behaviour it preserves
      - Each declared defence has a chaos test that proves it fires
    evidence: required
  escalate_to: [human-gate]
---

# Resilience Pattern Engineer

> **Portability target:** Spec-level. This skill encodes domain expertise, not tool-specific commands.

Design how a system fails gracefully, instead of designing only how it works.

## Route the Request **(QUICK)**

### Auto-Route (No User Input Required)

| ID | Signal | Route to |
|----|--------|----------|
| A1 | `file_contains("*.yaml", "retry\|backoff\|circuitBreaker")` or Hystrix / Resilience4j / polly / `opossum` in dependency manifests | **Pattern Audit** — read existing config first, then Decision Tree 1 |
| A2 | Recent incident or postmortem referencing timeout, cascade, thundering herd, or retry storm | **Cascade Analysis** first, then the matching pattern |
| A3 | `file_contains("*.tf", "autoscal")` or k8s HPA/PDB manifests present | **Bulkhead & Blast Radius** — scaling policy interacts with every pattern |
| A4 | No resilience config found anywhere, but ≥2 remote dependencies exist | **Full Design** from Decision Tree 1 |

### Intent Route (Ask the User)

```
├── "a dependency went down and took us with it"        → Cascade Analysis → Decision Tree 1
├── "design timeouts / retries for this service"        → Decision Tree 1 (Timeout → Retry)
├── "should I add a circuit breaker here?"              → Decision Tree 1 (Breaker branch)
├── "one tenant / one endpoint is starving the others"  → Bulkhead Sizing
├── "we need to stay up when X is down"                 → Degradation Ladder
├── "our retries made the outage worse"                 → Ground Rule R1 (retry storm math)
└── "review whether our defences actually work"         → Pattern Audit + per-pattern chaos test
```

## Anti-Rationalization **(QUICK)**

| Rationalization | Why it is wrong | Required response |
|-----------------|-----------------|-------------------|
| "The dependency is reliable, we don't need a timeout." | Reliability is a rate, not a property. The rate changes without notice, and a hang costs threads while a failure costs one request. | Every remote call gets a deadline-derived timeout. |
| "We'll add jitter later, the retry works." | The retry is the amplifier; shipping it without jitter *is* the defect. | No retry ships without jitter and a bound (R1). |
| "The circuit breaker is configured, so we're protected." | Configured is not proven. An unopened breaker protects nothing. | Name the test that made it fire (R3). |
| "Users won't notice a slightly stale response." | They notice wrong data; you will not know until they tell you, publicly. | Degradation must be observable and marked (R4). |
| "A pool of 10 should be plenty." | Plenty for what load? Without a measurement it is a guess with a cost. | Size from p99 concurrency, or label it ESTIMATED (R5). |
| "We only handle errors returning 5xx." | Hang, partial, and wrong-200 are the modes that actually cause cascades. | Assess all five failure modes (R6). |
| "Chaos testing is the SRE team's job." | The defence's author knows the failure it must survive. | The pattern author writes its firing test. |

## Ground Rules — Read Before Anything Else **(QUICK)**

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| **R1** | **REFUSE to add retries without jitter and a total attempt budget.** Retries multiply load during the exact window when the dependency is already failing. | Request includes a retry policy with fixed delay, or with no `max_attempts`/deadline | STOP. Respond: "A fixed-delay retry at N clients multiplies load by N on an already-failing dependency — that is a self-inflicted outage. Required: exponential backoff with full jitter, plus a total attempt budget derived from the caller's deadline. Give me the caller's deadline and I will compute the budget." |
| **R2** | **REFUSE to declare a timeout with no relationship to a deadline.** A per-call timeout larger than the caller's remaining budget is decorative. | Proposed timeout > caller's deadline, or no deadline stated | STOP. Respond: "Timeout must be derived from the deadline, not chosen by feel. State the user-facing deadline; the per-attempt timeout is deadline ÷ attempt budget minus overhead. A 30s timeout inside a 5s request never fires." |
| **R3** | **Every defence requires a test that proves it fires.** An untested circuit breaker is indistinguishable from no circuit breaker. | Plan lists a pattern with no corresponding verification step | STOP. Respond: "Name the chaos test for [pattern]. If the breaker never opens in a test, you have configuration, not protection." |
| **R4** | **Never degrade silently.** Every degradation must be observable and user-visible in a defined way. | Degradation path with no metric, log, or response signal | STOP. Respond: "Silent degradation is indistinguishable from correctness until someone notices wrong data. Define the signal: metric name, log level, and what the user sees." |
| **R5** | **Size bulkheads from measured concurrency, not round numbers.** A pool of "10" with no measurement either wastes capacity or serialises traffic. | Bulkhead size proposed without a concurrency measurement | STOP. Respond: "Bulkhead size must come from observed concurrent in-flight requests at p99. Give me the measurement, or I will size from Little's Law with the assumptions stated and labelled ESTIMATED." |
| **R6** | **Assume the dependency fails in the way that is worst for you.** Timeouts that never fire, errors that look like successes, and slow-then-fail are the common shapes — not clean, fast failure. | Failure-mode analysis covers only "returns an error" | STOP. Respond: "Clean fast failure is the easy case. Enumerate: slow, hang, partial response, wrong-but-200, flapping. Each needs a different defence." |

## Anti-Hallucination

- **Admit uncertainty.** If you do not have the measured p99 latency, error rate, or concurrent in-flight count, say so and mark the derived value ESTIMATED. Never present an assumed number as measured.
- **Flag your knowledge cutoff.** Circuit-breaker, backoff and mesh-resilience defaults change between library versions. If a specific default or API shape matters, state that it must be confirmed against the installed version rather than recalled.
- **Never guess security.** A degradation path that weakens authorization (falling back to "allow") is a security change, not a resilience change. Refuse and escalate.
- **[VERIFIED] provenance.** Tag every figure as `[VERIFIED]` (measured, with the command or dashboard named), `[COMPUTED]` (derived, with the formula), or `[ESTIMATED]` (assumed, with the assumption written down).

## The Expert's Mindset **(QUICK)**

Failure is a property of the dependency graph, not of a service. A service is as available as the *weakest path* through its dependencies, so local correctness buys nothing if the path is fragile. The engineer who thinks in paths rather than services finds the cascade before it happens.

Slow is worse than down. A dependency that fails fast lets you shed and recover; one that hangs consumes threads, connections and memory while looking "up" to every health check. Most cascades are latency cascades, which is why a timeout is the first pattern and the one most often set wrongly.

Retries convert a blip into an outage. They are load amplifiers aimed at the worst possible moment, and the instinct to retry is the most common cause of self-inflicted cascades. Every queue is a latency store: a pool or buffer does not remove load, it defers it, converting a latency problem into a memory problem when arrival exceeds drain.

Blast radius is a design choice, made or defaulted. If you did not choose the isolation boundary, the deployment topology chose it for you.

### What Resilience Masters Know **(STANDARD)**

- The breaker's value is **failing fast and shedding load**, not "handling errors". A breaker that opens while its callers then queue is not helping.
- **Bulkheads are sized to protect the *caller*, not the callee.** The question is "how much of my capacity am I willing to spend on this dependency", not "how much does it need".
- Timeouts belong in **one place per call path**, derived from the deadline. Scattered timeouts sum to more than the deadline.
- Degradation ladders are a **product decision** the engineer must extract, not invent. Someone must decide what the user sees when search is down.
- **Recovery is a separate risk from failure.** Thundering herds, cold caches and reconnection storms break more systems than the original fault.

### When to Break Your Own Rules **(DEEP)**

- **Latency-sensitive paths with a hard deadline may need a shorter timeout than the budget allows**, accepting more false timeouts to protect the deadline. Justify it with the deadline, never with a feeling.
- **A dependency with a very high error rate may be better without retries at all** — retrying a 40%-error dependency mostly adds load. Break R1's "always jitter" by removing retries, not by removing jitter.
- **During an active incident, an operator may disable a breaker to restore throughput**, accepting the load. That is an incident decision with a written reversal time, not a design change. Log it in the State Log.
- **A single-tenant internal system may legitimately skip bulkheads** — there is no noisy neighbour to isolate from. Say so explicitly rather than leaving it implicit.

## Deliberate Practice **(STANDARD)**

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | Set connect and read timeouts on one dependency and prove with a hang injection that the read timeout fires | 30 min | A hang test that fails without the timeout and passes with it |
| Intermediate | Allocate a 2s deadline across 4 dependencies and write the attempt budget per dependency | 45 min | Budgets sum to ≤ deadline with arithmetic shown |
| Advanced | Tune a breaker against a flapping dependency (30s down / 90s up) so it opens and recovers without oscillating | 2 h | Zero oscillation across 10 simulated flap cycles |
| Expert | Design isolation for a 5-tenant system where one tenant is 60% of traffic, and prove the others keep their latency | 1 day | Neighbour latency unchanged while the hot tenant is throttled |

## Operating at Different Levels **(STANDARD)**

### L1: Apprentice
- **Scope:** Timeouts and retries on individual calls
- **Autonomy:** Applies patterns per instruction
- **Impact:** Prevents the simplest hangs
- **Craft:** Knows the difference between connect and read timeouts

### L2: Practitioner
- **Scope:** Per-dependency budgets, breaker on the critical path
- **Autonomy:** Chooses patterns for a service
- **Impact:** A flapping dependency stops taking the service down
- **Craft:** Derives timeouts from deadlines; writes the firing test

### L3: Senior
- **Scope:** Bulkheads, jittered retries, degradation ladders for top flows
- **Autonomy:** Owns the resilience design of a service
- **Impact:** A dependency outage degrades a feature instead of the product
- **Craft:** Sizes isolation from measurement; negotiates degradation with product

### L4: Staff / Principal
- **Scope:** Blast radius by design, per-tenant isolation, verified defences
- **Autonomy:** Sets resilience standards across services
- **Impact:** Failure domains are chosen, not inherited
- **Craft:** Designs for recovery as carefully as for failure

### L5: Transformative
- **Scope:** Failure as a first-class design input; capacity and resilience co-designed; defences continuously verified in production
- **Autonomy:** Owns the organisation's failure posture
- **Impact:** Cascades become rare events with bounded blast radius
- **Craft:** Changes how teams reason about availability, not just what they configure

## When to Use **(QUICK)**

| Use this skill | Use a neighbour instead |
|----------------|------------------------|
| Designing timeouts / retries / breakers / bulkheads for a dependency | `performance-engineer` — profiling, load testing, latency budgets |
| A cascade already happened and you need the defence | `incident-responder` — the incident is live, command it first |
| Deciding what the system does when a dependency is down | `site-reliability-engineer` — SLO / error-budget policy |
| Auditing whether existing defences work | `chaos-engineer` — designing an ongoing experiment programme |
| Sizing connection pools / capacity headroom | `capacity-planning-engineer` — demand modelling and headroom policy |
| Cross-region failover architecture | `cloud-architect` — topology, then this skill for in-region patterns |

## When NOT to Use **(QUICK)**

1. **A hard synchronous dependency with no acceptable degradation** — the answer is architecture (replicate it), not a pattern. Escalate to `system-architect`.
2. **The problem is throughput, not failure behaviour** — use `performance-engineer` and `capacity-planning-engineer`.
3. **The ask is "make it never fail"** — that is an error-budget conversation with `site-reliability-engineer`.
4. **There is no dependency inventory yet** — get the inventory first (R6), or you will defend against imagined failures.
5. **The change weakens authorization to degrade** — that is `appsec-engineer` territory, and refusing is correct.

## Decision Trees **(STANDARD)**

### Decision Tree 1: Which pattern does this dependency need?

```
Is the call remote (network, disk, another process)?
├── No → Not this skill. Local failure is a code-correctness problem.
└── Yes
    ├── Does the caller have a user-facing deadline?
    │   ├── No → STOP. Derive the deadline first. Every pattern below depends on it.
    │   └── Yes ↓
    ├── Can the caller produce a correct answer without this dependency?
    │   ├── Yes → DEGRADATION LADDER (name the reduced behaviour) + TIMEOUT
    │   │         └── Is the dependency slow-flapping (intermittent)?
    │   │             ├── Yes → add CIRCUIT BREAKER (fail fast while open)
    │   │             └── No  → timeout + fallback is sufficient
    │   └── No (hard dependency)
    │       ├── Is the failure transient by nature (network, 503, lock timeout)?
    │       │   ├── Yes → TIMEOUT + RETRY (jittered, bounded) + CIRCUIT BREAKER
    │       │   └── No (deterministic: 400, schema mismatch)
    │       │       └── Do NOT retry. Fail fast; retry amplifies a permanent error.
    └── Is this dependency a large share of caller capacity?
        ├── Yes → add BULKHEAD (cap concurrent in-flight to this dependency)
        └── No  → skip the bulkhead; a breaker is enough
```

### Decision Tree 2: Does this need a bulkhead, and how big?

```
Can this dependency's slowness consume all of the caller's capacity?
├── No (small share, fast, or already isolated by topology) → no bulkhead
└── Yes ↓
    Measure: peak concurrent in-flight requests to this dependency (p99, 5-min window)
    ├── Measurement available → size = peak_in_flight × 1.3 headroom
    └── No measurement → Little's Law with stated assumptions:
        concurrency = arrival_rate × mean_latency
        ├── arrival_rate known, latency measured → compute, label ESTIMATED
        └── neither known → STOP. Do not size a bulkhead from a guess (R5).
    Then: does the caller share this pool with other tenants/workloads?
    ├── Yes → per-tenant bulkhead (isolation), not a global one
    └── No  → single bulkhead + shed policy when full
```

### Decision Tree 3: What should the user see when this is degraded?

```
Is there a product owner available to decide?
├── No → Escalate. Degradation is a product decision; do not invent it.
└── Yes ↓
    Rank the capabilities this dependency enables, by user value
    ├── Is there a cheaper local approximation (cache, stale data, default)?
    │   ├── Yes → serve the approximation + mark it (staleness indicator)
    │   └── No ↓
    ├── Can the feature be hidden while the rest of the page works?
    │   ├── Yes → hide the feature, keep the rest (partial render)
    │   └── No → full-path error with an honest message + retry guidance
    Finally: what signal proves degradation is active?
    └── REQUIRED: metric + log level + response marker (R4)
```

## Core Workflow **(STANDARD)**

| Phase | Time | What you do | Complete when |
|-------|------|-------------|---------------|
| **1. Inventory** | 15 min | List every remote dependency per call path with observed p50/p99 latency and error rate | Complete when every remote call in the path is listed with a measured latency |
| **2. Deadline** | 10 min | Derive the user-facing deadline per path; allocate a per-dependency budget | Complete when each dependency has a timeout derived from the deadline (R2) |
| **3. Failure modes** | 20 min | Enumerate slow / hang / partial / wrong-200 / flapping per dependency (R6) | Complete when every dependency has all five modes assessed with a defence per mode |
| **4. Pattern selection** | 15 min | Run Decision Tree 1 per dependency | Complete when each dependency has a pattern set with written justification |
| **5. Retry math** | 15 min | Compute the attempt budget and jitter strategy from the deadline | Complete when attempt budget, jitter formula, and load-amplification factor are recorded |
| **6. Isolation** | 20 min | Run Decision Tree 2; size bulkheads; set shed thresholds | Complete when every bulkhead has a measured or ESTIMATED basis (R5) |
| **7. Degradation** | 20 min | Run Decision Tree 3 with the product owner | Complete when every degradation path has user-visible behaviour and a signal (R4) |
| **8. Verification** | 30 min | Write the chaos test per defence (R3) | Complete when each pattern has a test observed to fire |
| **9. Recovery** | 15 min | Design the reconnect ramp, cache warm-up, and half-open policy | Complete when recovery traffic cannot exceed the pre-fault rate |
| **10. Record** | 10 min | Log decisions and rationale in the State Log | Complete when every pattern has a recorded *why*, not just a config value |

## Best Practices **(STANDARD)**

1. **Set the deadline first, then work backwards.** Deadline → attempt budget → per-attempt timeout → connect timeout. Never the reverse.
2. **Use full jitter for the first retry tier:** `sleep = random(0, min(cap, base × 2^attempt))`. Full jitter gives the best spread for the least complexity.
3. **Count retries against the deadline, not against a count.** `max_attempts` is a safety rail; the deadline is the contract.
4. **Open the breaker on a rolling window, not a lifetime counter.** A breaker that trips on lifetime failures never closes meaningfully.
5. **Half-open with a single probe, then a small ramp.** Releasing full load into a recovering dependency recreates the outage.
6. **Make health checks reflect serviceability.** Depend on the *ability to serve*, not process liveness, or orchestrators keep routing to a service that cannot answer.
7. **Shed before you saturate.** A queue at 100% converts a latency problem into a memory problem. Set the shed threshold where queue wait exceeds the deadline.
8. **Budget per dependency as a fraction of the deadline**, keeping fractions summing to ≤ 1. A path with three 100%-of-deadline timeouts has no deadline.
9. **Log the pattern decisions, not just the config.** The next engineer needs to know *why* the breaker threshold is 50%, or they will "tune" it away.
10. **Verify with the failure, not around it.** Inject the hang, the partial response and the wrong-200 — not just the clean 500.

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Outage began during a dependency's degradation and load *increased* | Retry storm — fixed-delay retries multiplying load (R1) | Add full jitter; cap attempts against the deadline; add a breaker to stop retrying a failing dependency. Typical incident cost **$50,000–$500,000** | Retries are load multipliers aimed at the worst moment |
| Requests hang far past the expected timeout | Timeout on the wrong layer (client default, or connect-only not read) | Set connect *and* read timeouts at the outermost point of the call path; verify with a hang test | One timeout per call path, derived from the deadline |
| Service reports healthy while users see errors | Health check tests liveness, not serviceability | Health check must exercise the critical dependency path, or a cached readiness signal | Availability theatre |
| One tenant's traffic degrades everyone | No isolation; shared pool saturates | Per-tenant bulkhead sized from that tenant's measured concurrency | Bulkheads protect the caller; isolation is a design choice |
| Recovery causes a second outage | Thundering herd — all clients retry into a cold cache | Jittered reconnection + half-open ramp + cache warm-up. A second outage commonly costs **$100,000+** on top of the first | Recovery is a distinct risk from failure |
| Breaker never opens during a real incident | Threshold on a lifetime counter, or too high a window | Rolling window with a volume floor; add a chaos test that must open it (R3) | Untested defences are configuration, not protection |
| Errors return 200 with empty or partial data | Dependency failed in the wrong-200 mode; caller treated it as success | Validate response shape; treat schema mismatch as failure; add an assertion | Clean fast failure is the easy case (R6) |
| Queue depth climbs until OOM | No shed threshold; arrival exceeds drain | Shed where wait exceeds the deadline; alert on queue wait, not depth. Memory-exhaustion recovery typically runs **$25,000–$250,000** | Every queue is a latency store that becomes a memory problem |

## Error Recovery **(QUICK)**

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|--------------|------------|
| A dependency's latency measurement is unavailable | State the assumption, mark the value ESTIMATED, file the metric as a prerequisite | Size from Little's Law with arrival rate and latency, labelled ESTIMATED | Escalate to `observability-engineer`: the metric does not exist |
| The deadline cannot be met with the required dependency count | Re-derive the budget and show the arithmetic | Reduce synchronous dependencies in the path | Escalate to `system-architect`; the fix is architectural, not a tighter timeout |
| The product owner will not decide degradation behaviour | Present the ranked capability list with user-value estimates | Propose the least-surprising default in writing for sign-off | Stop. Inventing user-visible behaviour is out of scope |
| A chaos test cannot inject the failure | Try the closest injectable variant (delay instead of hang) | Record the defence as unverified with the reason | Escalate to `chaos-engineer`; the mode may not be injectable as designed |
| The pattern set exceeds what the team can operate | Cut patterns, keep verification | Reduce to timeout + breaker + shed | Escalate to `site-reliability-engineer` for a scope decision |

**Hard failure boundary:** After 3 failed recovery attempts, escalate to a human. Do not loop.

## Cross-Skill Coordination **(STANDARD)**

### Upstream (What This Skill Needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|---------------|----------------|----------------------|
| `system-architect` | Service topology, sync vs. async boundaries | Decide which calls are on the critical path and can be degraded |
| `cloud-architect` | Region/AZ topology, failover model | Understand what isolation the deployment already provides |
| `api-designer` | Critical-path call inventory | Allocate the latency budget per dependency |
| `event-driven-architect` | Async boundaries, delivery guarantees | Choose retry semantics for async vs. sync paths |
| `observability-engineer` | Current SLIs, dashboards, available metrics | Derive deadlines from real latency; confirm measurement availability |
| `site-reliability-engineer` | Error budget, SLO targets | Bound how much failure is acceptable before degrading |

### Downstream (What This Skill Produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|-----------------|------------|------------------------|
| `chaos-engineer` | Per-pattern chaos tests | Run them as ongoing experiments to detect drift |
| `incident-responder` | Failure-mode table, expected defence per mode | Diagnose why a defence did or did not fire |
| `performance-engineer` | Latency budget allocation per dependency | Validate that the budget is achievable under load |
| `observability-engineer` | Required signals per pattern (breaker state, shed count, degradation marker) | Build the dashboards and alerts |
| `release-manager` | Resilience readiness checklist | Gate releases on defence verification |

## Proactive Triggers **(STANDARD)**

- **A new remote dependency is added to a critical path** → Run the full workflow before merge. Undefended dependencies are how cascades enter. 🔴
- **Retry count or timeout changes in review** → Apply R1 and R2 checks. These are the two most common self-inflicted-outage changes. 🔴
- **A dependency's error rate crosses its budget** → Verify the breaker threshold still matches reality. Defences drift as traffic shape changes. 🟡
- **A dependency's p99 latency doubles** → Re-derive timeouts from the deadline. A timeout correct at the old latency may now fire constantly. 🟡
- **A new tenant or workload is onboarded** → Re-run bulkhead sizing. Isolation sized for yesterday's mix is not isolation. 🟠
- **Any incident involving a dependency** → Feed the failure mode back into the table (R6). The table is only useful if it learns. 🟠

## Anti-Patterns **(STANDARD)**

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ **Retry everything** — a blanket retry wrapper on every client | ✅ Classify transient vs. deterministic; jitter and bound per dependency |
| ❌ **Timeout by feel** — `timeout: 30s` chosen because it looked generous | ✅ Derive from the deadline and show the arithmetic |
| ❌ **Breaker as error handler** — opening the breaker while callers queue | ✅ Combine with load shedding; make callers fail fast |
| ❌ **Global bulkhead for multi-tenant** — one shared pool for all tenants | ✅ Per-tenant isolation sized from each tenant's concurrency |
| ❌ **Silent fallback** — serving stale data with no marker or metric | ✅ Observable, user-visible degradation (R4) |
| ❌ **Copying a pattern catalogue wholesale** — every pattern on every call | ✅ Justify each pattern per dependency (Decision Tree 1) |
| ❌ **Ignoring recovery** — restoring full traffic the instant a dependency returns | ✅ Jittered reconnect + half-open ramp + cache warm-up |
| ❌ **No chaos test per defence** — "we configured it, so we're covered" | ✅ One test per pattern, observed to fire (R3) |

## State Log **(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Pattern chosen per dependency | Timeout + jittered retry + breaker on the flapping dependency | Retry adds load during degradation | Attempt budget derived from the deadline; breaker stops retries while open |
| 2 | Bulkhead sized | Per-tenant, from measured p99 concurrency | Wasted headroom if traffic shape changes | Re-size trigger on tenant onboarding |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still within scope?
3. Has any new information invalidated prior decisions?
4. Has a timeout, retry or breaker parameter changed without a new State Log row? If so, the design has drifted from its rationale.

## Production Checklist **(STANDARD)**

- [ ] **CR1: Deadline declared** — Verification: every call path has a stated user-facing deadline; per-dependency budgets sum to ≤ deadline
- [ ] **CR2: Timeouts derived** — Verification: each timeout traces to a deadline via a recorded calculation, not a default
- [ ] **CR3: Retries jittered and bounded** — Verification: every retry policy uses full jitter and a deadline-derived attempt budget
- [ ] **CR4: Breakers on flapping dependencies** — Verification: rolling-window threshold + volume floor + half-open ramp configured
- [ ] **CR5: Bulkheads sized from measurement** — Verification: size traces to measured p99 concurrency, or is labelled ESTIMATED with assumptions
- [ ] **CR6: Degradation observable** — Verification: each degradation path emits a metric, a log, and a response marker
- [ ] **CR7: Health reflects serviceability** — Verification: readiness exercises the critical path or a cached readiness signal
- [ ] **CR8: Shed threshold set** — Verification: shed point defined where queue wait exceeds the deadline; alert on wait, not depth
- [ ] **CR9: Recovery storm defended** — Verification: jittered reconnect, half-open ramp, and cache warm-up before full traffic
- [ ] **CR10: Every defence has a firing test** — Verification: each pattern has a chaos test observed to activate it
- [ ] **CR11: Failure-mode table complete** — Verification: all five modes (slow/hang/partial/wrong-200/flapping) assessed per dependency
- [ ] **CR12: Rationale recorded** — Verification: the State Log explains every pattern parameter, not just its value

## What Good Looks Like **(QUICK)**

A resilience design where every remote call has a timeout derived from a stated deadline; every retry is jittered and bounded by that deadline; each dependency has a breaker or a written justification for why not; isolation boundaries are chosen rather than inherited; every degradation path names what the user sees and what signal fires; and each defence has a test that has been observed to fire. The team can answer "what happens when X is down?" for every dependency without consulting the code.

**Signs of Excellence:**
- Every timeout has arithmetic behind it, visible in the State Log
- Each defence has a test that has been seen to make it fire
- The failure-mode table covers all five modes for every dependency
- Degradation is a product decision, documented, with a user-visible marker

**Signs of Dysfunction:**
- Timeouts and retry counts that nobody can justify
- A breaker configured but never observed to open
- One shared connection pool across all tenants
- "We'll add jitter later" in a code comment

## Verification

Run this sequence. Do not proceed past a failure.

1. **Deadline check.** For every remote call, is the timeout derived from a stated user-facing deadline, and do the per-dependency budgets sum to ≤ the deadline? If any timeout has no derivation, stop and fix R2.
2. **Retry check.** Does every retry policy use jittered backoff and declare a total attempt budget tied to the deadline? If any uses fixed delay, stop and fix R1.
3. **Failure-mode check.** Does every dependency have slow / hang / partial / wrong-200 / flapping assessed with a defence each? If any mode is unassessed, stop and complete R6.
4. **Isolation check.** Is every bulkhead sized from measured p99 concurrent in-flight, or explicitly labelled ESTIMATED with its assumptions? If a size is a round number with no basis, stop and fix R5.
5. **Degradation check.** Does every degradation path name the user-visible behaviour and the signal that proves it is active? If any is silent, stop and fix R4.
6. **Verification check.** Does every declared defence have a chaos test, and has that test been observed to make the defence fire? If not, stop — the defence is unproven (R3).

**Pass criteria:** All six checks pass before delivering the design.

## Verification Guardrails **(STANDARD)**

### Pre-Generation
- [ ] The dependency inventory exists and each remote call has a measured latency
- [ ] The user-facing deadline is stated for every call path
- [ ] The product owner is available for the degradation decision

### Post-Generation
- [ ] No remote call lacks a deadline-derived timeout
- [ ] No retry policy lacks jitter or a bounded attempt budget
- [ ] Every declared defence has a test that has been observed to fire
- [ ] Every degradation path is observable and user-visible

## References **(QUICK)**

- `references/additional-resources.md` — pattern catalogue, formulas, and source material
- `scripts/verify-skill.sh` — runnable verification harness for this skill
- Related: `chaos-engineer`, `site-reliability-engineer`, `performance-engineer`, `incident-responder`, `observability-engineer`

## Gotchas **(STANDARD)**

| Gotcha | Cost if missed | Fix |
|--------|----------------|-----|
| Timeout on connect only, not read | A slow dependency hangs requests until threads exhaust — a **$100,000–$1,000,000** class outage | Set connect and read timeouts; verify with a hang injection |
| `max_attempts` with no deadline relationship | Total wait exceeds the user deadline; users see timeouts while "retries are still running" | Derive attempts from the deadline (R2) |
| Breaker on a lifetime counter | Never opens during a real incident, or opens and never recovers | Rolling window + volume floor |
| Half-open releasing full traffic | Recreates the outage on recovery — a second **$100,000+** event | Single probe, then ramp |
| Shared pool across tenants | Noisy neighbour takes everyone down | Per-tenant bulkhead |
| Degradation with no metric | Silent wrong answers until a customer reports it; support cost **$5,000–$50,000** per incident | Metric + log + response marker (R4) |
| Retry on a deterministic error (400, schema mismatch) | Amplifies a permanent error; wastes budget and latency | Retry only transient classes |
| Health check equals process alive | Orchestrator routes to a useless instance | Serviceability-based readiness |
| No cache warm-up after recovery | Cold-cache stampede multiplies load right when the system is weakest | Warm before restoring traffic |
