# Stampede Defences — the arithmetic behind single-flight and early expiry

> A cold start or a mass expiry removes the cache for a hot key. This file shows why that is a
> load-multiplier problem, and what each defence actually saves (R3).

---

## Stampede load, and what a single-flight actually saves

A cold start or a mass expiry removes the cache for a hot key. The origin then sees the *miss*
pattern, sized for the *cached* pattern:

```
cached steady state:   2,000 req/s, 97% hit rate  →  60 req/s to the origin
mass expiry (no defence): 2,000 req/s, 0% hit    →  2,000 req/s to the origin
                                                        = 33× the origin's designed load
```

A single-flight (request coalescing) per key collapses that burst to **one** origin call per key
being recomputed:

```
single-flight, 1 hot key, 2,000 concurrent callers
  without: 2,000 origin queries
  with:        1 origin query, 1,999 callers wait on the same future
  → origin load during the flush = 1 query, not 2,000
```

That is the entire justification for R3. Note the trade the table in SKILL.md flags: **waiters now
share the leader's latency**, so the single-flight timeout must be shorter than the caller's own
deadline, or a slow leader becomes everyone's outage.

---

## Probabilistic early expiry (XFetch)

When a lock or a leader election is unaffordable, entries can be recomputed *early* with a
probability that rises as expiry approaches. The standard formulation:

```
now            = current time
expiry         = the entry's expiry timestamp
delta          = time to recompute the value
beta           = 1.0 (tunable; > 1 biases toward earlier recompute)

recompute if:  now - delta * beta * ln(random()) >= expiry
```

| Situation | Probability of early recompute | Effect |
|-----------|-------------------------------|--------|
| Just written (`now << expiry`) | ≈ 0 | No extra load |
| Half-way to expiry | Low, rising | Load spread begins |
| At expiry | ≈ 1 | Certain recompute |

**Why it beats a lock here.** There is no coordination, so it cannot deadlock and adds no round
trip; the cost is a small number of redundant recomputes, which is exactly what "spread the expiry"
means. It is the right default for a hot key shared across many processes where a distributed lock
would itself become the bottleneck.

---

## The cold start is the load the origin must survive

The *warm* steady state is not the load the origin must survive — the cold state is. This is why the
origin-shed threshold (CR10) is separate from the stampede defence (CR5): the defence reduces the
burst, and the origin must still shed the remainder.
