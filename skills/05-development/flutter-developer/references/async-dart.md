# Async Dart — Future, Stream, Isolates

## The Three Tools

| Tool | For | Pitfall |
|------|-----|---------|
| `Future` / `async`-`await` | One-shot async work (network, IO) | Forgetting error handling; unawaited futures |
| `Stream` | Repeated events (updates, progress, sockets) | Never disposing the subscription → leaks |
| `Isolate` / `Isolate.run` | CPU-heavy work off the UI isolate | Data is copied across isolates — keep payloads small |

## Rules

1. **Never block the UI isolate.** IO and CPU work are async (`await`) or offloaded (`Isolate.run`).
2. **Always handle errors.** `try/catch` around awaited calls; `onError` on streams; never a silent unhandled future.
3. **Dispose subscriptions.** Every `StreamSubscription`, `StreamController`, and timer gets disposed in `dispose()` (or managed lifecycle).
4. **Prefer `Isolate.run` for one-shot CPU work.** It spawns a short-lived isolate and returns the result — simpler than managing a long-lived isolate.
5. **Keep isolate payloads small.** Passing a 50MB list copies it; pass a path/ID and load inside the isolate.

## Common Async Bugs

| Bug | Fix |
|-----|-----|
| `setState()` after dispose | Guard with `mounted` before calling setState after an await |
| Streams accumulate / duplicate events | Single-subscription streams; cancel before re-subscribing |
| Unhandled async error crashes release | `FlutterError.onError` / zone error handlers; test error paths |
| UI jank from a big `jsonDecode` | `Isolate.run(() => jsonDecode(raw))`; show a loading state |
| Race: two concurrent fetches overwrite state | Cancellation tokens / query keys (see data-layer.md) |

## Testing Async

- `fakeAsync`/`tester.runAsync` in widget tests for timers and async work.
- `async` matchers (`expectLater(stream, emitsInOrder(...))`) for stream tests.
- Inject a fake clock/network for deterministic tests — never real timers or live APIs in tests.
