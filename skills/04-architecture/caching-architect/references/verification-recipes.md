# Verification Recipes — runnable checks for this skill

> The checks in SKILL.md's Verification section, made runnable.

---

## Verification recipes

The six checks in SKILL.md's Verification section, made runnable.

### 4.1 Key-isolation collision test

Prove two tenants (or scopes) cannot map to the same key. This is a property test, not an example:

```
for tenant_a, tenant_b in sample where tenant_a != tenant_b:
    for every other dimension combination D:
        assert key(tenant_a, D) != key(tenant_b, D)
```

The test fails the moment a dimension is dropped from the schema — which is the only way this bug
can be introduced.

### 4.2 Stampede-under-flush test

```
1. Warm the cache; record origin QPS.                      # baseline
2. Flush the cache entirely, under full traffic.
3. Measure peak origin QPS.
   PASS: peak <= origin's shed threshold (CR10), because the defence engaged.
   FAIL: peak approaches total request rate → the defence is absent or not firing.
4. Assert the defence emitted its activation metric (CR6).
```

Without step 4 you cannot distinguish "the defence worked" from "the load happened to be low".

### 4.3 Propagation test

```
1. Write a value through the app.
2. Poll every layer (browser → CDN → service) in order.
3. Assert all layers return the new value within the declared staleness budget (CR8).
   Record the observed propagation time per layer — it is the input to the budget, not a guess.
```

### 4.4 Hit-rate-by-class check

```
For each key class with an owner:
  assert a hit-rate metric exists that is scoped to that class.
  assert no alert is defined on global hit rate alone.      # CR9
```

### 4.5 Reversibility check (did the last change make it worse?)

```
Before changing a TTL or size (R6):
  record hit rate by class, origin QPS, and p99 origin latency.   # baseline
After:
  re-record the same three.
  FAIL if origin QPS rose or p99 rose without a recorded reason.
```

This is the recipe behind R6: a TTL change that raises origin load is a *regression* that a
hit-rate-only view can miss.
