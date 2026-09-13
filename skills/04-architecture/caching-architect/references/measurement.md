# Measurement — hit rate by key class, not in aggregate

> An aggregate hit rate hides the distribution. This file shows the failure the aggregate cannot
> see, and why every tuning change must be judged on origin load rather than on the hit rate alone
> (R6).

---

## Where the hit rate actually goes

An aggregate hit rate hides the distribution. The failure that matters is the hot-key skew:

```
key class A: 1,000,000 keys, 90% hit rate, evenly spread   → origin load stable
key class B: 1 key, 99.9% hit rate, but expires every 60 s → 1,000 req/s burst at each expiry
```

Global hit rate ≈ 97% and looks healthy; the origin still sees a periodic 33× spike. **Measure by
key class** (R6, CR9) — the aggregate number is not able to see class B.

---

## The hit-rate-by-class check

```
For each key class with an owner:
  assert a hit-rate metric exists that is scoped to that class.
  assert no alert is defined on global hit rate alone.      # CR9
```

---

## The reversibility check (did the last change make it worse?)

```
Before changing a TTL or size (R6):
  record hit rate by class, origin QPS, and p99 origin latency.   # baseline
After:
  re-record the same three.
  FAIL if origin QPS rose or p99 rose without a recorded reason.
```

This is the recipe behind R6: a TTL change that raises origin load is a *regression* that a
hit-rate-only view can miss.
