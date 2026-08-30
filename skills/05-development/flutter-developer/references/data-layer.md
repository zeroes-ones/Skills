# Data Layer — Repository Pattern, Models, Offline Cache

## The Pattern

```
Widgets → Providers/Blocs → Repositories → Data Sources (API, DB, platform)
```

- **Repositories** are the single source of truth for a domain: they own caching, offline sync, and error mapping.
- **Data sources** are dumb: one per transport (API client, SQLite, platform channel).
- **Models** are immutable (`freezed` or manual), with `fromJson`/`toJson` and explicit null handling.

## Offline-First

1. **Cache-first reads** — show cached data instantly, refresh in background (Riverpod/Bloc handles the state).
2. **Write queue** — offline mutations queue locally (SQLite/drift) and sync when connectivity returns.
3. **Conflict resolution** — last-write-wins for simple fields; explicit merge for complex entities; never silent overwrite of user edits.
4. **Storage** — `drift`/SQLite for structured data; `shared_preferences` for small settings; files for large blobs.

## Async State Model

Use the QueryKey/caching approach: a request is identified by a key (e.g., `product/{id}`); concurrent fetches for the same key dedupe; stale responses don't overwrite fresh ones (check a monotonic request id or `ref.invalidate`).

## Error Mapping

| Layer | Error handling |
|-------|----------------|
| Transport | Timeouts, retries with backoff, typed API errors |
| Repository | Maps transport errors to domain errors; decides cache-vs-error |
| UI | Shows cached data + non-blocking error toast; retry affordance |

## Testing

- Repository tests: fake data sources + in-memory cache.
- Widget tests: inject fake repositories/providers — never hit the network.
- Integration tests: real API against a test environment or mock server.
