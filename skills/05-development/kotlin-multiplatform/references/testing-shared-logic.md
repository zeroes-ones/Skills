# Testing Shared Logic — commonTest and Platform Tests

## The Test Structure

```
shared/src/commonTest/    # runs on EVERY target — shared logic
shared/src/androidUnitTest/  # Android-specific tests (actuals)
shared/src/iosTest/          # iOS-specific tests (actuals)
```

## What Goes in commonTest

- Domain logic, validation, use cases.
- Repositories with a Ktor `MockEngine` + in-memory SQLDelight driver.
- Serialization round-trips.
- Concurrency tests (shared state access).

## What Goes in Platform Tests

- expect/actual halves: each platform's actual behaves correctly (Keychain, network status, device info).
- Platform integrations (Android WorkManager, iOS Keychain) that can't run in commonTest.

## Rules

1. **commonTest runs on every target** — "tested on Android only" is not tested (Ground Rule R6).
2. **Fake the boundaries, not the logic** — MockEngine, in-memory DB, fake clocks; never live APIs.
3. **Deterministic** — controlled dispatchers (`runTest`, `StandardTestDispatcher`), no real sleeps.
4. **Concurrency tested** — a test that exercises shared state from multiple coroutines.

## Commands

```bash
./gradlew :shared:testDebugUnitTest          # Android unit tests
./gradlew :shared:iosSimulatorArm64Test      # iOS simulator tests
./gradlew :shared:allTests                   # all configured targets
```

## Release Gate

- [ ] commonTest green on both targets
- [ ] Platform tests green (actuals)
- [ ] iOS consumer build + smoke call green in CI
- [ ] Zero skipped tests
