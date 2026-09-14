# Verification Recipes

Runnable checks for a memory design.

## 1. Read path exercised

```python
entries = read_memory(store, workflow="my-flow", limit=5)
assert entries, "read path returns nothing — memory is a log, not memory"
```

## 2. Trust label enforced

```python
ctx = memory_context(store, "my-flow")
assert "NOT instructions" in ctx, "recall is unlabelled — poisoning path"
assert ctx.strip().startswith("PRIOR RUN MEMORY"), "wrapper missing"
```

## 3. Poisoning guard

```python
# an entry whose trust marker was stripped must be flagged, not trusted
entry = {"workflow": "x", "outcome": "complete"}   # no trust field
assert read_memory(store, "x")[0].get("trust_unverified") is True
```

## 4. Consolidation bounds the store

```python
before = count_entries(store, "my-flow")
rep = consolidate_memory(store, "my-flow", keep=3)
after = count_entries(store, "my-flow")
assert after < before and rep["consolidated"] > 0
assert read_memory(store, "my-flow", 99)[-1].get("consolidated") is True
```

## 5. Idempotent manage job

```python
consolidate_memory(store, "my-flow", keep=3)
a = read_entries(store, "my-flow")
consolidate_memory(store, "my-flow", keep=3)
assert a == read_entries(store, "my-flow"), "manage job is not idempotent"
```

## 6. Corruption tolerated

```python
open(store + "/my-flow.jsonl", "a").write("{ not json\n")
entries = read_memory(store, "my-flow")   # must not raise
assert isinstance(entries, list)
```

## 7. Cost measured, both ways

Run the same task with `--recall` and without; compare outcome and injected tokens. Record the delta — including when it is zero.
