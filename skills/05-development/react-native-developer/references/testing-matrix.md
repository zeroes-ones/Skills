# Testing Matrix — Jest, RNTL, Detox, Maestro

## The Pyramid for React Native

| Layer | Tool | Scope | Run where |
|-------|------|-------|-----------|
| Unit | Jest | Pure logic, reducers, utils, API mocks | CI, fast |
| Component | React Native Testing Library (RNTL) | Component render/interaction in isolation | CI, fast |
| Integration | RNTL + React Query/Redux | Screen behavior with data | CI |
| E2E | **Detox** (iOS/Android) or **Maestro** (cross-platform) | Full flows on real devices/simulators | CI device farm + pre-release |

## Rules

1. **E2E on both platforms** — a release that only passed on one platform is not tested (Ground Rule R6).
2. **Oldest supported OS** — test the lowest OS you support; crashes concentrate there.
3. **Real device at least once** — simulators miss push, biometrics, and permission flows.
4. **No skipped tests in the release path** — a skipped E2E test counts as a failure.
5. **Mock boundaries, not behavior** — mock the network (MSW) and native modules (jest mocks), not your own logic.

## Detox vs Maestro

| | Detox | Maestro |
|---|-------|---------|
| Strength | Deep RN integration, sync with app state | Simple YAML flows, cross-platform, low setup |
| Best for | Complex multi-screen flows, sync-sensitive tests | Quick smoke flows, CI simplicity |
| iOS | Simulator/device | Simulator/device |
| Android | Emulator/device | Emulator/device |

Use Detox for the critical-path suite and Maestro for smoke/onboarding; run both in CI.

## Release Gate

- [ ] Jest + RNTL green
- [ ] E2E (Detox or Maestro) green on both platforms
- [ ] Oldest supported OS E2E green
- [ ] Zero skipped tests
- [ ] Crash-free sessions ≥ 99% on the previous release (baseline)

## Test Data

Use deterministic fixtures; never depend on live APIs in E2E. MSW or a mock server keeps tests hermetic and fast.
