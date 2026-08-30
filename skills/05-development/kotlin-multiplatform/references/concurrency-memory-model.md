# Concurrency Under the New Memory Model

> `[VERIFIED 2026-08]` — the new Kotlin memory model removed freezing; `freeze()`/`isFrozen` semantics are gone. Code that relied on freezing must be re-verified.

## What Changed

| Old model | New model |
|-----------|-----------|
| Objects frozen to share across threads | No freezing; objects are shared, thread-safety is the developer's job |
| `freeze()` / `isFrozen` available | Removed (Kotlin 1.7.20+ with the new memory model default) |
| Copy-on-freeze semantics | Explicit synchronization or confinement required |

## The Rules

1. **Mutable shared state must be synchronized or confined.** Choose one:
   - **Confine** — all access on a single dispatcher/thread (the simplest and most common).
   - **Synchronize** — `Mutex`, `kotlinx.atomicfu`, or a lock for cross-thread access.
2. **Immutable data is safe to share** — a value published once needs no locking.
3. **Document the concurrency model** per shared object; a reviewer should see "confined to X" or "guarded by Mutex Y".
4. **Test concurrency** — a commonTest that exercises concurrent access catches violations deterministically (use `runTest` with controlled dispatchers).

## Patterns

```kotlin
// Confined: all mutation on a single dispatcher
private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
private val state = MutableStateFlow(...)
// only mutated within this scope

// Synchronized: Mutex for cross-thread access
private val mutex = Mutex()
private var cache: Cache? = null
suspend fun getCache(): Cache = mutex.withLock { cache ?: load().also { cache = it } }
```

## What to Audit

- `@ThreadLocal` usages (still valid, but verify intent).
- Any place that previously called `freeze()` — now a no-op or compile error; replace with real thread-safety.
- Singletons in the shared module mutated from multiple threads (repository caches, token holders).

## Failure Mode

Symptom: intermittent crashes or data races in production, only on one platform (usually iOS where threads differ). Detection: crash logs with concurrent access; a stress test. Fix: confine or synchronize; add a regression test.
