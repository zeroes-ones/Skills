# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `test-strategy-design` | New project, major refactor, or test pyramid not delivering ROI | Pyramid distribution, tool selection matrix, coverage targets per layer, CI quality gate design |
| `unit-testing` | Component/hook/function testing: Vitest, Jest, pytest, go test | AAA pattern, mocking strategy (module boundaries only), edge case checklists, factory-based test data |
| `integration-testing` | API endpoint testing, database integration, auth flow verification | Real dependencies (testcontainers), transactional rollback, fixture seeding, external service mocking at HTTP level |
| `e2e-playwright` | Critical user journeys: signup → onboarding → core action → logout | Page Object Model, `getByRole`/`getByLabel` selectors, `storageState` for auth reuse, visual regression |
| `api-contract-testing` | Cross-team API consumers, public APIs, microservice boundaries | OpenAPI schema validation, Pact consumer-driven contracts, snapshot testing for backward compatibility |
| `performance-k6` | Load/stress/soak/spike testing before major releases or infra changes | k6 script structure (`options`, `default`, `check`, `trend`), p95/p99 thresholds, CI smoke test integration |
| `ci-quality-gates` | Automating test stages in CI: lint → unit → integration → E2E → perf smoke | Stage ordering, coverage reporting (Codecov), flaky test quarantine (< 2% rate), merge blocking rules |
| `test-data-management` | Reproducible test data, GDPR-compliant test databases, seed data freshness | Factory libraries (Fishery, factory_boy), migration-based seeding, data obfuscation for production-like data |
