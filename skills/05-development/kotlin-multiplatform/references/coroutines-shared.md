# Coroutines in Shared Code — Flow, Scopes, Concurrency

## What Works in commonMain

- `kotlinx-coroutines-core` — `launch`, `async`, `Flow`, `Channel`, `Dispatchers` (default, IO, Main via the main dispatcher library).
- Suspending functions and `Flow` are the idiomatic shared-API surface.

## Scope Discipline

- **Never create a global scope** in the shared module — scope leak = work that outlives the caller.
- ViewModels own a scope (`viewModelScope` on Android; a lifecycle-scoped scope on iOS); the shared layer exposes suspending functions, not scopes.
- For shared state that must survive config changes, inject a scope owned by the platform layer.

## Flow Patterns

- Expose `Flow` from repositories for reactive data; collect in the platform UI.
- Use `stateIn`/`shareIn` with an explicit scope for UI state.
- Handle cancellation: cooperative cancellation (`ensureActive`, `withContext`) — a cancelled collector must stop work.

## Concurrency Under the New Memory Model

- No `freeze()` — the old model's freezing is gone.
- Mutable shared state accessed from multiple threads must be **synchronized or confined**:
  - Confine to a single dispatcher (e.g., all mutations on `Dispatchers.Main` or a dedicated dispatcher).
  - Or use `Mutex`/atomics for cross-thread shared state.
- Document the concurrency model per shared object; add a concurrency test where state is shared.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Global scope in shared code | Inject a scope; never launch from a top-level singleton |
| Blocking call in a suspend fun | `withContext(Dispatchers.IO/Default)` around blocking work |
| Flow collected with no cancellation | `collect` inside a scope; honor cancellation |
| Shared state mutated from two threads | Confine or synchronize; test with concurrent access |
| `Dispatchers.Main` missing on iOS | Include `kotlinx-coroutines-core`'s main-dispatcher artifact per platform |
