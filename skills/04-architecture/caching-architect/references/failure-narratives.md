# Failure Narratives — five ways a cache broke correctness in production

> Anonymised narratives of caching decisions that looked right and were wrong. Each ends with the
> rule it justifies.

---

## 3.1 The TTL that was the whole strategy

A team cached a feature-flag evaluation with a 5-minute TTL and no invalidation on write. A customer
disabled a dangerous flag during an incident; the flag kept evaluating as *on* for up to five
minutes across the fleet. Diagnosis took longer than the TTL, so the first reproduction appeared to
"fix itself" — the TTL had aged out the evidence. **Lesson:** a TTL does not merely bound staleness;
it also bounds how long a *correct* fix takes to take effect. R1 exists because "it expires
eventually" and "the wrong answer persists" are the same sentence said differently.

## 3.2 The key that omitted the tenant

A cache key was built inline as `"config:" + configId`. `configId` was globally unique, so no
collision existed — but the *values* differed per tenant by an override, and the override lived in
the value, not the key. One tenant's override was served to every other tenant sharing the config.
**Lesson:** the key must separate on every dimension the *value* depends on, not every dimension the
*identifier* happens to be unique on. This is the class of bug R2 refuses to ship, and the reason the
collision test is written against tenants and scopes, not against entity ids.

## 3.3 The deploy that took down the database

Every deploy flushed a service-local cache. On restart, ~50,000 concurrent requests all missed the
same top-10 keys simultaneously. The origin had been sized for the 3% miss rate of a warm cache, not
for a 100% miss rate. The database saturated, which made the misses slower, which held more
connections, which saturated it further. **Lesson:** the cache's *warm* steady state is not the load
the origin must survive — the cold state is. This is why CR10 (origin protected) is separate from CR5
(stampede defence): the defence reduces the burst, and the origin must still shed the remainder.

## 3.4 Two layers that repopulated each other

A service cache read through to a CDN; the CDN, on miss, read through to the service. Both had TTLs,
neither had a precedence rule. After an invalidation they ping-ponged: each served the other's stale
copy long enough that the "fresh" fetch landed on an entry already being overwritten. New and old
data appeared in the same response. **Lesson:** multi-layer caches need *both* a precedence rule
(which layer wins) and a propagation rule (how invalidation moves between them). R5 requires both,
because either one alone leaves an observable state that matches nothing in the system.

## 3.5 The negative that turned an outage sticky

A lookup wrapped its database call so that a timeout returned "not found", and "not found" was
cached with the standard 1-hour TTL. A brief database failover therefore wrote ~1 hour of *definitive*
absence into the cache for records that existed. **Lesson:** "not found" and "could not determine"
are different facts. Caching the first is a legitimate optimisation (CR11); caching the second
converts a transient failure into persistent wrong data. Never let the error path write a negative.
