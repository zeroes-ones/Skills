---
name: caching-architect
description: >
  Use when designing, reviewing, or debugging a cache layer — choosing what to cache and for
  how long, invalidation strategy, cache-key design, stampede and thundering-herd protection,
  multi-layer coherence, cache warm-up, or when stale or wrong data is being served. Handles
  the invalidation decision (TTL vs. event-driven vs. write-through), stampede defences
  (single-flight, probabilistic early expiry), key design, per-layer coherence rules, and
  staleness budgets. Do NOT use for query-level indexing and schema optimisation
  (database-designer, performance-engineer), CDN edge configuration as delivery infrastructure
  (cloud-architect), capacity and headroom modelling (performance-engineer, site-reliability-engineer), or runtime
  dependency resilience (resilience-pattern-engineer).
author: Sandeep Kumar Penchala
license: MIT
type: architecture
status: stable
version: 1.0.0
updated: 2026-09-11
tags:
  - caching
  - cache-invalidation
  - cache-stampede
  - cache-keys
  - ttl
  - consistency
  - staleness
  - thundering-herd
  - single-flight
  - multi-layer-cache
token_budget: 3500
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
chain:
  examples:
    - skills/04-architecture/caching-architect/examples/backtest
  consumes_from:
    - system-architect
    - database-designer
    - api-designer
    - performance-engineer
    - observability-engineer
    - codebase-design
  feeds_into:
    - performance-engineer
    - system-architect
    - backend-developer
    - resilience-pattern-engineer
    - site-reliability-engineer
workflow:
  artifacts:
    inputs: [data-access-patterns, consistency-requirements]
    outputs: [cache-design]
  completion:
    criteria:
      - Every cached item declares its invalidation strategy, never a TTL alone without justification
      - Every cache key is derived from an explicit key schema and names its versioning approach
      - Every cache has a stampede defence whose activation is observable
      - Every cached path declares a staleness budget tied to a business requirement
    evidence: required
  escalate_to: [human-gate]
---

# Caching Architect

> **Portability target:** Spec-level. This skill encodes domain expertise, not tool-specific commands.

Treat a cache as a correctness-critical subsystem with a performance benefit, not an optimisation.

## Route the Request **(QUICK)**

### Auto-Route (No User Input Required)

| ID | Signal | Route to |
|----|--------|----------|
| A1 | `file_contains("*.yaml", "redis\|memcached\|cacheStore\|cacheTTL")` | **Cache Audit** — read the existing keys and TTLs, then Decision Tree 1 |
| A2 | Cache client present (redis/elasticache/ioredis/pymemcache) with no invalidation path | **Invalidation Gap** — Decision Tree 1 |
| A3 | Incident or bug referencing stale data, wrong data after update, or "cache not cleared" | **Coherence Analysis** — Decision Tree 3 |
| A4 | Cache hit-rate dashboards or `X-Cache` headers present | **Stampede & Hit-Rate Review** — Decision Tree 2 |
| A5 | Cache read path present but no single-flight / lock / dedup mechanism | **Stampede Risk** — Decision Tree 2 |

### Intent Route (Ask the User)

```
├── "we serve stale data after an update"        → Invalidation (Decision Tree 1) then Coherence (3)
├── "what should we cache and for how long?"     → Decision Tree 1
├── "our cache dies under load spikes"           → Stampede defence (Decision Tree 2)
├── "how do we design the cache key?"            → Key Design section
├── "we have Redis + CDN + browser, they disagree" → Coherence (Decision Tree 3)
└── "review whether our caching is safe"         → Full workflow, all three trees
```

## Anti-Rationalization **(QUICK)**

| Rationalization | Why it is wrong | Required response |
|-----------------|-----------------|-------------------|
| "It's only a performance optimisation." | A cache changes what data users see. That is a correctness change, not a speed change. | Assign a staleness budget and a coherence rule (R1, R4). |
| "We'll set a short TTL, that's the invalidation." | A TTL is a *staleness acceptance*, not an invalidation strategy. It bounds how wrong you can be, it does not make you right. | Declare the invalidation event as well as the TTL, or accept TTL-only in writing (R1). |
| "Cache misses just fall through to the database." | Under a cold start or a hot key, every miss falls through *simultaneously* — that is the stampede that takes down the database. | Every cache needs a stampede defence (R3). |
| "The key is just the ID." | Keys that ignore tenant, locale, auth scope, or version serve one user's data to another, or serve stale data after a schema change. | Derive keys from an explicit key schema (R2). |
| "Cache invalidation is one of the two hard problems." | Repeating the joke is not a design. The problem is well-characterised: name the event, the scope, and the coherence rule. | Produce the invalidation plan, not the aphorism. |
| "We'll add caching later if it's slow." | Retrofitting a cache means retrofitting coherence into code that assumed a single source of truth. | Design the coherence model with the data model. |

## Ground Rules — Read Before Anything Else **(QUICK)**

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| **R1** | **REFUSE to accept a TTL as the only invalidation strategy without a written staleness acceptance.** A TTL bounds error; it does not eliminate it. | Cached item has a TTL and no invalidation event, and no recorded staleness budget | STOP. Respond: "A TTL alone means you are accepting that users see data up to [N] old. State the business staleness budget, or name the invalidation event (write-through, event-driven, versioned key). I will not ship TTL-only caching without that acceptance in writing." |
| **R2** | **REFUSE to cache under a key that is not derived from an explicit key schema.** Keys that omit tenant, locale, auth scope, or version leak data across boundaries or serve stale data after a schema change. | Cache key built inline from a string, with no declared components or version namespace | STOP. Respond: "What are the components of this key? Show me the key schema — every dimension that must separate two cached values. An ad-hoc key serving one tenant's data to another is a security incident, not a cache miss." |
| **R3** | **REFUSE to ship a cache with no stampede defence.** A cold cache or a hot key causes simultaneous misses that hit the origin together. | Cache read path with no single-flight, lock, probabilistic-expiry, or request-coalescing mechanism | STOP. Respond: "What happens on a cold start or when a hot key expires? Without a stampede defence, every caller misses at once and hits the origin together. Name the mechanism — single-flight, coalescing, or probabilistic early expiry." |
| **R4** | **REFUSE to cache without a declared staleness budget.** 'Eventually consistent' is not a budget; a number and a business owner are. | No staleness budget recorded for the cached path | STOP. Respond: "How stale may this data be, and who owns that decision? 'Eventually' is not a budget. Give me a number — seconds, minutes — and the business owner who accepts it." |
| **R5** | **REFUSE to add a second cache layer without a coherence rule between layers.** Layered caches that disagree produce data that is impossible to reason about. | Additional cache layer (CDN, client, service-local) with no stated precedence or propagation rule | STOP. Respond: "With two layers, which wins on conflict, and how does an invalidation propagate between them? Undefined layer precedence produces a system where no observation matches reality." |
| **R6** | **REFUSE to tune cache size or TTL without a measured hit rate.** Resizing from intuition either wastes memory or increases origin load, and nobody can tell which. | Cache parameters changed with no before/after hit-rate measurement | STOP. Respond: "What is the current hit rate, by key class? Without it, a size or TTL change is a guess that may increase origin load. Measure first, then change." |

## Anti-Hallucination

- **Admit uncertainty.** If you do not have the measured hit rate, the origin load, or the observed write rate for a key class, say so and mark derived figures ESTIMATED. Never present an assumed hit rate as measured.
- **Flag your knowledge cutoff.** Cache client semantics change between versions — Redis eviction policies, client-side cache libraries, and CDN invalidation APIs all differ. State that specific behaviours must be confirmed against the installed version rather than recalled.
- **Never guess security.** A cache key that omits a tenant or authorization scope is a data-leak vector, not a performance detail. Refuse to approve it and escalate to `appsec-engineer`.
- **[VERIFIED] provenance.** Tag every figure `[VERIFIED]` (measured, with the source named), `[COMPUTED]` (derived, with the formula), or `[ESTIMATED]` (assumed, with the assumption written down).

## The Expert's Mindset **(QUICK)**

A cache is a **copy of the truth held somewhere else**, and every copy can be wrong. That framing changes the discipline: the cache is not a performance feature bolted on afterwards, it is a **second source of data** that must be kept coherent with the first. Teams that adopt this framing design coherence with the data model; teams that do not, retrofit it into code that assumed a single source of truth.

The second shift is that **a TTL is not invalidation, it is accepted error.** A TTL says "I will serve wrong data for at most N seconds". That is a legitimate engineering decision — but it is a *decision*, and someone must own the number. The most common cache bug in production is not a crash; it is a value that was correct when written and wrong when read, with nobody having decided how long that was acceptable.

Third: **caches fail at the worst moment — when they are empty.** A cold start, a node eviction, or a hot key expiring all cause simultaneous misses that arrive at the origin together. The origin was sized for the *cached* traffic pattern, not for the miss pattern, so the stampede is what actually takes systems down. Every cache needs a defence for the moment it holds nothing.

Fourth: **keys are a security boundary.** A cache key that omits the tenant, the authorization scope, or the locale does not merely cause misses — it serves one caller's data to another. This is the failure mode that turns a performance optimisation into a breach.

## What Cache Masters Know **(STANDARD)**

- **Invalidation is an event, not a duration.** Write-through, event-driven invalidation, or a versioned key namespace are strategies; a TTL is the fallback when none of them is affordable.
- **Stale-while-revalidate beats synchronous refresh** for read-heavy paths: serve the stale value, refresh in the background, and never make a user wait for a refresh they did not request.
- **Probabilistic early expiry** (sometimes called "XFetch") prevents stampedes without a lock: recompute early with a probability that rises as the entry approaches expiry, so entries expire at different times.
- **Negative caching is a decision with its own TTL.** Caching "not found" protects the origin from repeated lookups of absent data — but it also caches transient failures as if they were facts.
- **The hit rate is not the goal; the origin load is.** A 99% hit rate with a hot key that misses in bursts is worse than a 90% hit rate that misses evenly.
- **Multi-layer caches need a precedence rule and a propagation rule.** Without both, no observation of the system matches its actual state.

### When to Break Your Own Rules **(DEEP)**

- **A genuinely immutable value may use an infinite TTL** — a content-addressed asset, a historical record. State the immutability argument explicitly; do not let "it never changes" become an assumption for mutable data.
- **A cache serving non-user-specific, non-sensitive public data may share one key across tenants** — that is correct, not a leak. Name the reason the data is safe to share.
- **A short TTL may be the *right* invalidation strategy** when the write rate is low and the staleness budget is generous (a metrics dashboard). Say so, with the number.
- **A cache may be deliberately disabled on the write path** to keep writes simple and correct, accepting higher read latency. That is a valid trade — record it rather than leaving it implicit.

## Deliberate Practice **(STANDARD)**

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | List five cached items and write down what invalidation event makes each correct | 30 min | Every item has an event or a recorded staleness acceptance |
| Intermediate | Design a cache key schema for a multi-tenant resource, then prove two tenants cannot collide | 45 min | A collision test showing tenant isolation |
| Advanced | Simulate a cold start on a hot key and design the defence that keeps origin load flat | 2 h | Origin QPS unchanged during a full-cache flush |
| Expert | Take a three-layer cache (browser → CDN → service) and define precedence plus propagation for each invalidation event | 1 day | An update propagates to all layers within the staleness budget, verified |

## Operating at Different Levels **(STANDARD)**

### L1: Apprentice
- **Scope:** TTL-only caching with ad-hoc keys
- **Autonomy:** Adds caching where instructed
- **Impact:** Reduces load; serves stale data unpredictably
- **Craft:** Knows a cache can be wrong

### L2: Practitioner
- **Scope:** Explicit keys, invalidation on write, measured hit rate
- **Autonomy:** Designs a cache for a feature
- **Impact:** Staleness is bounded and known
- **Craft:** Writes a key schema; invalidates on the write path

### L3: Senior
- **Scope:** Stampede defences, staleness budgets, negative caching policy
- **Autonomy:** Owns cache design for a service
- **Impact:** Caches survive cold starts and hot keys without origin damage
- **Craft:** Measures hit rate by key class; chooses the defence per pattern

### L4: Staff / Principal
- **Scope:** Multi-layer coherence, cache as a data-consistency concern
- **Autonomy:** Sets cache standards across services
- **Impact:** Layered caches have defined precedence and propagation
- **Craft:** Designs coherence before the data model ships

### L5: Transformative
- **Scope:** Caching and consistency co-designed; staleness is a product-visible contract
- **Autonomy:** Owns the organisation's data-freshness posture
- **Impact:** Users see a defined freshness guarantee, not an accident of TTLs
- **Craft:** Turns staleness from an implementation detail into a stated guarantee

## When to Use **(QUICK)**

| Use this skill | Use a neighbour instead |
|----------------|------------------------|
| Designing what to cache, keys, TTLs, invalidation | `database-designer` — indexing, schema, query planning |
| Fixing stale or wrong data served from a cache | `performance-engineer` — origin latency and throughput optimisation |
| Adding stampede / cold-start protection | `performance-engineer` — capacity headroom and autoscaling |
| Coherence across browser, CDN, and service caches | `cloud-architect` — CDN topology and edge delivery |
| Cache as a failure domain (cache down = ?) | `resilience-pattern-engineer` — timeouts, breakers, degradation |
| Cache memory sizing and eviction pressure | `site-reliability-engineer` — SLOs and error budgets for the origin |

## When NOT to Use **(QUICK)**

1. **The problem is slow queries with no repeat access pattern** — that is indexing and query design (`database-designer`), not caching. A cache on non-repeated access is pure cost.
2. **The task is CDN configuration for delivery, not data coherence** — use `cloud-architect`; this skill governs what data may be stale, not how bytes reach the edge.
3. **The cache is being sized for capacity** — use `performance-engineer`; headroom modelling is a different discipline from coherence.
4. **A dependency is failing and you need runtime defence** — use `resilience-pattern-engineer`; a cache can mask a failure, but the defence belongs there.
5. **The data is security-scoped and the key cannot include the scope** — stop. Escalate to `appsec-engineer`; caching beyond an authorization boundary is out of scope here.

## Decision Trees **(STANDARD)**

### Decision Tree 1: What invalidation strategy does this cached item need?

```
Is the value immutable (content-addressed, historical, never rewritten)?
├── Yes → IMMUTABLE KEY: infinite TTL, version/hash in the key. State the immutability argument.
└── No ↓
    On write, does the writer know the cache key (or can it derive it)?
    ├── Yes → WRITE-THROUGH / EXPLICIT INVALIDATION on the write path
    │         └── Is there more than one writer (another service, a batch job, a DBA)?
    │             ├── Yes → EVENT-DRIVEN invalidation (write path cannot know all readers)
    │             └── No  → explicit invalidation is sufficient. Add a TTL as a safety net.
    └── No (writer cannot identify readers) ↓
        Is the staleness budget generous (minutes to hours)?
        ├── Yes → TTL + STALE-WHILE-REVALIDATE (serve stale, refresh in background)
        └── No (budget is seconds) ↓
            Use a VERSIONED KEY: derive the key from a version that changes on write
            └── REQUIRED: state who bumps the version and how, with a test that proves it
```

### Decision Tree 2: Which stampede defence for this cache?

```
Can concurrent misses for the same key be coalesced in-process?
├── Yes → SINGLE-FLIGHT / REQUEST COALESCING (one origin call per key per process)
└── No (multi-process or multi-node) ↓
    Is a distributed lock affordable (latency, complexity, failure handling)?
    ├── Yes → DISTRIBUTED LOCK + single-flight inside the lock holder
    │         └── REQUIRED: what happens if the lock holder dies? (lock TTL, not a lock forever)
    └── No ↓
        Use PROBABILISTIC EARLY EXPIRY (recompute early with rising probability near expiry)
        └── Spreads expiry across time, no lock, no coordination
    Finally: is the origin able to shed load when the stampede happens anyway?
    └── Every cache ALSO needs an origin-side defence (see resilience-pattern-engineer)
```

### Decision Tree 3: Layers disagree — which wins?

```
Which layer is authoritative for this datum?
├── The origin of truth is the database → databases's value is correct; caches are copies
└── Define, per layer, from the consumer's perspective:
    ├── Browser / client cache: shortest precedence, most likely to be stale
    ├── CDN / edge cache: shared across users — only for non-user-specific data
    └── Service / application cache: closest to truth, invalidated on write
    On a write event, propagation order is REQUIRED:
    ├── Invalidate service cache → publish event → purge CDN → (client TTL/versioned URL)
    └── Each step has a latency, and the sum must fit inside the staleness budget (R4)
```

## Core Workflow **(STANDARD)**

| Phase | Time | What you do | Complete when |
|-------|------|-------------|---------------|
| **1. Access patterns** | 20 min | Identify read/write ratio, key cardinality, and access skew per data class | Complete when each candidate has a measured read:write ratio and a hot-key assessment |
| **2. Staleness budget** | 15 min | Determine the acceptable staleness per data class, with a business owner | Complete when every cached path has a numeric budget and a named owner (R4) |
| **3. Invalidation** | 25 min | Run Decision Tree 1 per data class | Complete when every item has a named invalidation event or a recorded TTL-only acceptance (R1) |
| **4. Key schema** | 20 min | Define key components, order, and version namespace | Complete when the key schema is written and a collision test proves isolation (R2) |
| **5. Stampede defence** | 20 min | Run Decision Tree 2 per hot key | Complete when every cache has a defence with observable activation (R3) |
| **6. Coherence** | 25 min | Run Decision Tree 3 across all layers | Complete when precedence and propagation are defined per layer (R5) |
| **7. Origin protection** | 15 min | Confirm the origin can survive the miss pattern | Complete when origin-side shedding exists for the worst-case miss burst |
| **8. Observability** | 20 min | Define hit rate by key class, miss bursts, and revalidation counts | Complete when a hit-rate metric exists per key class, not just globally |
| **9. Verify** | 30 min | Run the verification sequence | Complete when all six checks pass |
| **10. Record** | 10 min | Log the design and its rationale in the State Log | Complete when each TTL and rule has a recorded *why* |

## Best Practices **(STANDARD)**

1. **State the staleness budget before choosing a mechanism.** The mechanism follows from the number and the owner, never the reverse.
2. **Prefer invalidation on write over TTL wherever the writer can identify readers.** TTL is the fallback, not the default.
3. **Use versioned keys for schema changes.** Bumping a key namespace version invalidates everything old without a purge, and it is atomic.
4. **Include every separator dimension in the key** — tenant, locale, auth scope, entity id, and version. Then write the collision test.
5. **Add `stale-while-revalidate` semantics** so a refresh never blocks a user who did not ask for it.
6. **Use probabilistic early expiry when a lock is unaffordable.** It spreads expiry without coordination.
7. **Give negative results their own short TTL** — but never cache transient failures as if they were "not found".
8. **Measure hit rate by key class, not globally.** A hot key's miss pattern is invisible in an aggregate number.
9. **Define layer precedence explicitly, then test propagation end to end.** "It'll expire eventually" is not a coherence rule.
10. **Record the *why* for every TTL.** The next engineer will otherwise "tune" it, and the number is a business decision.

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Users see old data after an update | TTL-only caching with no write invalidation | Add explicit or event-driven invalidation; keep the TTL as a safety net | A TTL is accepted error, not invalidation |
| One customer sees another customer's data | Key omits tenant or authorization scope | Add every separator dimension to the key schema; add a collision test. A leak of this class typically costs **$100,000–$1,000,000+** in incident response and regulatory exposure | Keys are a security boundary |
| Origin database falls over during a deploy or cache flush | Stampede — every caller misses simultaneously | Add single-flight or coalescing; add probabilistic early expiry; shed at the origin. Origin overload commonly costs **$50,000–$500,000** per event | Caches fail when empty |
| Hit rate looks high but origin load is volatile | Aggregate hit rate hides a hot key that misses in bursts | Measure hit rate by key class; add a stampede defence for the hot key | The goal is origin load, not hit rate |
| Old and new data appear together | Two cache layers disagree; no precedence rule | Define precedence and propagation order; test end to end | Layered caches need a coherence rule |
| Cache appears correct in staging, wrong in production | Different eviction pressure, cardinality, or TTL rounding | Reproduce with production cardinality and eviction limits. Diagnosis typically **$10,000–$75,000** | Cache behaviour is a function of scale |
| A schema change silently serves stale records | Key version not bumped | Version the key namespace; bump on shape change | Versioning makes invalidation atomic |
| "Not found" results persist after the record is created | Negative result cached with too long a TTL | Short negative TTL; never cache transient failures as not-found | Negative caching is a separate decision |

## Error Recovery **(QUICK)**

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|--------------|------------|
| Wrong data served in production | Determine the key class and whether the key is correct (R2) | Purge the affected key class and confirm the origin value | Escalate to `incident-responder` if the data is security-scoped |
| Origin overloaded by misses | Enable or tighten single-flight; if absent, throttle at the origin | Flush to a known-good state and warm from the origin deliberately | Escalate to `resilience-pattern-engineer` for origin-side shedding |
| Update not visible within the budget | Trace propagation across layers (Decision Tree 3) | Purge upstream layers manually and record the gap | Revisit the budget or the propagation design — do not extend the TTL silently |
| Hit rate collapsed after a change | Check key version — a bump invalidates everything by design | Warm the cache deliberately rather than letting it warm under load | Revert the version bump if it was unintended |
| Cache memory exhausted, evictions climbing | Measure hit rate by key class; identify low-value classes | Reduce TTL or exclude the low-value class | Escalate to `performance-engineer` for sizing |
| Two layers oscillate (each repopulating from the other) | Precedence rule is undefined or inverted | Define precedence explicitly and enforce it in code | Disable the outer layer until coherence is provable |

**Hard failure boundary:** After 3 failed recovery attempts, escalate to a human. Do not loop.

## Cross-Skill Coordination **(STANDARD)**

### Upstream (What This Skill Needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|---------------|----------------|----------------------|
| `system-architect` | Service topology, read/write paths | Identify where caching is possible and what coherence is required |
| `database-designer` | Schema, access patterns, write paths | Determine what invalidation the write path can emit |
| `api-designer` | Endpoint semantics, cache headers | Decide what may be cached at the edge and by clients |
| `performance-engineer` | Measured latency and origin load | Size the benefit and validate the hit-rate target |
| `observability-engineer` | Existing metrics and dashboards | Place hit-rate-by-class and miss-burst instrumentation |
| `codebase-design` | Data access layer structure | Put the cache in one place rather than scattered through callers |

### Downstream (What This Skill Produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|-----------------|------------|------------------------|
| `performance-engineer` | Hit-rate targets and origin-load model | Validate that the cache achieves the intended reduction |
| `system-architect` | Coherence requirements per data class | Keep the topology consistent with the freshness contract |
| `backend-developer` | Key schema and invalidation events | Implement the cache correctly on the read and write paths |
| `resilience-pattern-engineer` | Origin miss-burst profile | Design the origin-side shedding and breakers for the worst-case miss |
| `site-reliability-engineer` | Staleness budget and hit-rate SLIs | Wire alerts for freshness violations and origin load |

## Proactive Triggers **(STANDARD)**

- **A new cached item is proposed** → Require an invalidation event or a written staleness acceptance before it ships (R1). 🔴
- **A cache key is built inline from a string** → Require the key schema and a collision test (R2). 🔴
- **A cache read path has no single-flight or coalescing** → Flag the stampede risk before the first cold start (R3). 🔴
- **A second cache layer is introduced** → Require precedence and propagation rules (R5). 🟡
- **A TTL or cache size is changed** → Require before/after hit rate by key class (R6). 🟡
- **A schema change alters a cached shape** → Require a key version bump so invalidation is atomic. 🟠

## Anti-Patterns **(STANDARD)**

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ **TTL-only caching** — "it'll expire in 5 minutes" as the whole strategy | ✅ Name the invalidation event; keep TTL as a safety net (R1) |
| ❌ **Ad-hoc keys** — `"user:" + id` built inline at each call site | ✅ A declared key schema with tenant, scope, and version (R2) |
| ❌ **No stampede defence** — assuming misses are cheap | ✅ Single-flight, coalescing, or probabilistic early expiry (R3) |
| ❌ **Global hit-rate monitoring** — one number for all keys | ✅ Hit rate by key class, exposing hot-key burst patterns |
| ❌ **Cache-aside everywhere** — no single owner of the cache logic | ✅ One data-access layer owns caching, so coherence has one place to live |
| ❌ **Caching transient failures** — a timeout stored as "not found" | ✅ Cache only definitive negatives, with a short TTL |
| ❌ **Layered caches with no precedence** — each layer guessing | ✅ Explicit precedence and propagation order, tested (R5) |
| ❌ **Tuning TTL by feel** — changing the number to fix a symptom | ✅ Measure hit rate by class first (R6); the TTL is a business decision |

## State Log **(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Invalidation chosen | Write-through + event-driven for multi-writer keys; TTL 300s as safety net | Up to 300s staleness if the event is lost | Event delivery monitored; TTL bounds the worst case |
| 2 | Stampede defence chosen | Single-flight per process; probabilistic early expiry across nodes | Slightly earlier recompute (extra origin calls) | Recompute probability tuned by measured origin headroom |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still within scope?
3. Has any new information invalidated prior decisions?
4. Has a TTL or key schema changed without a new State Log row? If so, the design has drifted from its rationale.

## Production Checklist **(STANDARD)**

- [ ] **CR1: Staleness budget declared** — Verification: every cached path has a numeric budget and a named business owner
- [ ] **CR2: Invalidation event named** — Verification: each item has an invalidation event, or a recorded TTL-only acceptance
- [ ] **CR3: Key schema written** — Verification: key components, order, and version namespace are documented
- [ ] **CR4: Collision test present** — Verification: a test proves two tenants (or scopes) cannot collide on a key
- [ ] **CR5: Stampede defence present** — Verification: single-flight, coalescing, or probabilistic expiry exists per hot key
- [ ] **CR6: Defence activation observable** — Verification: the stampede defence emits a metric when it engages
- [ ] **CR7: Layer precedence defined** — Verification: each cache layer has a stated precedence and propagation order
- [ ] **CR8: Propagation tested** — Verification: an update is observed to propagate to every layer within the budget
- [ ] **CR9: Hit rate by key class** — Verification: hit rate is measured per key class, not only globally
- [ ] **CR10: Origin protected** — Verification: the origin can shed load during a worst-case miss burst
- [ ] **CR11: Negative TTL bounded** — Verification: negative results have a short, explicit TTL and transient failures are never cached as negatives
- [ ] **CR12: Rationale recorded** — Verification: the State Log explains each TTL and rule, not just its value

## What Good Looks Like **(QUICK)**

A cache design where every cached item declares an invalidation event (or a written TTL-only acceptance with a numeric staleness budget and a named owner); keys come from an explicit schema that includes every separator dimension and a version namespace, with a collision test proving isolation; every hot key has a stampede defence whose activation is observable; layered caches have defined precedence and a tested propagation order; and hit rate is measured per key class. The team can answer "how stale can this be, and who decided?" for any cached value.

**Signs of Excellence:**
- Every TTL traces to a business staleness budget with a named owner
- A collision test proves tenants and scopes cannot share a key
- Cold-start origin load is flat, because the stampede defence works
- An update is observed propagating to every layer within the budget

**Signs of Dysfunction:**
- "It expires in 5 minutes" offered as the invalidation strategy
- Keys built inline at each call site
- One global hit-rate number
- No one knows what happens on a full cache flush

## Verification

Run this sequence. Do not proceed past a failure.

1. **Invalidation check.** Does every cached item have a named invalidation event, or a recorded TTL-only acceptance with a numeric budget? If any is TTL-only by accident, stop and fix R1.
2. **Key check.** Is every key derived from a declared key schema, including tenant, scope, and version? Does a collision test prove isolation? If not, stop and fix R2.
3. **Stampede check.** Does every cache have a defence (single-flight, coalescing, or probabilistic expiry) with observable activation? If not, stop and fix R3.
4. **Budget check.** Does every cached path have a numeric staleness budget and a named owner? If not, stop and fix R4.
5. **Coherence check.** Do all layers have defined precedence and a tested propagation order? If undefined, stop and fix R5.
6. **Hit-rate check.** Is hit rate measured by key class, and is the origin able to shed a worst-case miss burst? If only a global number exists, stop and fix R6.

**Pass criteria:** All six checks pass before the cache ships.

## Verification Guardrails **(STANDARD)**

### Pre-Generation
- [ ] Access patterns measured: read:write ratio and cardinality per candidate data class
- [ ] A business owner is available to accept the staleness budget
- [ ] The write paths are known, including writers outside this service

### Post-Generation
- [ ] No cached item lacks an invalidation event or a written acceptance
- [ ] No key is built outside the declared key schema
- [ ] No cache lacks a stampede defence
- [ ] Layer precedence and propagation are defined and tested

## References **(QUICK)**

- `references/invalidation-catalogue.md` — every refresh strategy with its cost and the case it fails in
- `references/staleness-and-ttl.md` — the TTL-to-acceptable-error arithmetic and the owned staleness budget
- `references/stampede-defences.md` — the miss-multiplier, single-flight savings, and the XFetch formulation
- `references/key-schema-and-cardinality.md` — separator dimensions, cardinality as capacity, keys as a security boundary
- `references/coherence-models.md` — the five inter-layer models and the precedence + propagation rule each needs
- `references/measurement.md` — hit rate by key class, the skew it reveals, and the reversibility check
- `references/failure-narratives.md` — five production failures and the rule each justifies
- `references/verification-recipes.md` — the six verification checks as runnable procedures
- `references/sources.md` — every claim traced to a source, tagged by strength
- `references/related-reading.md` — where this skill plugs into the library
- `scripts/verify-skill.sh` — runnable verification harness for this skill
- Related: `performance-engineer`, `system-architect`, `database-designer`, `resilience-pattern-engineer`, `site-reliability-engineer`

## Gotchas **(STANDARD)**

| Gotcha | Cost if missed | Fix |
|--------|----------------|-----|
| Key omits tenant or auth scope | Cross-tenant leak; incident response and regulatory exposure commonly **$100,000–$1,000,000+** | Key schema with every separator dimension + collision test (R2) |
| No stampede defence | Origin falls over on cold start or cache flush; **$50,000–$500,000** per event | Single-flight, coalescing, or probabilistic early expiry (R3) |
| TTL-only caching on mutating data | Users see stale data after an update; diagnosis typically **$10,000–$75,000** | Name the invalidation event; TTL as safety net (R1) |
| Aggregate hit rate only | A hot key's miss bursts are invisible; origin load becomes volatile | Hit rate by key class (R6) |
| Layered caches with no precedence | Old and new data appear together; no observation matches reality | Precedence + propagation rules, tested (R5) |
| Schema change without a key version bump | Stale records served indefinitely after a shape change | Version the key namespace; bump on shape change |
| Transient failure cached as "not found" | An outage becomes sticky wrong data with a long TTL | Never cache transient failures as negatives |
| Negative TTL too long | New records invisible for the TTL duration | Short negative TTL with its own budget |
| Tuning TTL by feel | Wasted memory or hidden origin load increase | Measure first (R6); TTL is a business decision |
