# Shared Data Layer — Ktor, kotlinx.serialization, SQLDelight

## The Stack

| Concern | Library | Why |
|---------|---------|-----|
| Networking | **Ktor client** | Multiplatform, engine per platform, interceptors, typed |
| Serialization | **kotlinx.serialization** | Multiplatform, compile-safe, no reflection |
| Persistence | **SQLDelight** | Type-safe SQL, generates Kotlin, multiplatform drivers |
| Async | **kotlinx-coroutines** | Flow/structured concurrency in commonMain |

## Repository Pattern (Shared)

```
commonMain:
  DataSource (Ktor client) → Repository → UseCases → ViewModels (shared or platform)
androidMain/iosMain:
  Http engines, SQL drivers, platform caches
```

## Ktor Client Setup

```kotlin
// commonMain
val client = HttpClient {
    install(ContentNegotiation) { json(Json { ignoreUnknownKeys = true }) }
    install(HttpTimeout) { requestTimeoutMillis = 15_000 }
}
```

- Engine chosen per platform (`HttpClient(Android)` / `HttpClient(Darwin)`).
- Add interceptors for auth tokens, logging, and retries in commonMain.

## SQLDelight

- `.sq` files define typed queries; schema migrations versioned in the shared module.
- Drivers: Android (AndroidSqliteDriver), iOS (NativeSqliteDriver).
- Keep the schema in commonMain; platform drivers injected.

## Serialization Rules

- `@Serializable` data classes as DTOs; map to domain models explicitly.
- `ignoreUnknownKeys = true` for forward-compat with the API.
- Never serialize platform types; keep DTOs pure Kotlin.

## Offline-First (Shared)

- Cache-first reads via SQLDelight; refresh in background.
- Write queue for offline mutations; sync on connectivity (expect: network-status).
- Conflict resolution: last-write-wins for simple fields; explicit merge for complex entities.

## Testing

- commonTest: repository with a MockEngine (Ktor) + in-memory SQLDelight driver.
- Never hit live APIs in tests.
