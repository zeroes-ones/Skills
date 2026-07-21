---
name: qa-engineer
description: Test pyramid strategy, unit/integration/e2e testing with Playwright and Cypress, API testing, performance testing with k6, test automation frameworks, coverage goals, and quality metrics. Trigger: QA, quality assurance, testing, test strategy, Playwright, Cypress, k6, test automation, coverage.
author: Sandeep Kumar Penchala
type: quality
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - qa-engineer
token_budget: 2179
output:
  type: "code"
  path_hint: "./"
---
# QA Engineer

Design and implement comprehensive test strategies following the test pyramid model. This skill covers the full testing lifecycle: unit testing with Vitest/Jest/pytest, integration testing with real databases and services, end-to-end testing with Playwright and Cypress, API contract testing, performance and load testing with k6, test data management, coverage enforcement, and CI integration for continuous quality.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing a test strategy for a new or existing project
- Implementing the test pyramid (unit → integration → E2E) with appropriate tools
- Writing Playwright or Cypress E2E tests for critical user flows
- Setting up API contract testing (Pact, schemas, snapshots)
- Performing load/stress testing with k6 or Artillery
- Establishing code coverage thresholds and quality gates in CI
- Building test data factories and fixtures for reproducible tests
- Debugging flaky tests and improving test stability

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Test Type Selection
```
                     ┌──────────────────────────┐
                     │ START: What kind of test? │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Does the behavior involve multiple  │
              │ systems (DB + API + UI)?            │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Is it a critical │  │ Does it involve      │
        │ revenue path?    │  │ external dependencies│
        └──┬───────────┬───┘  │ (DB, API, file I/O)? │
           │ YES       │ NO   └──┬───────────────┬───┘
           ▼           ▼        │ YES           │ NO
      ┌────────┐ ┌──────────┐   ▼               ▼
      │ E2E    │ │Integration│ ┌──────────┐ ┌──────────┐
      │(Play-  │ │test       │ │Integration│ │Unit test │
      │wright) │ │(Supertest)│ │test       │ │(Vitest/  │
      └────────┘ └──────────┘ └──────────┘ │Jest)     │
                                           └──────────┘
```
**When to choose E2E:** Covers signup → purchase → fulfillment. Revenue-impacting. Used by > 80% of users. Run on every merge to main.  
**When to choose Unit test:** Pure logic, data transformation, validation rules. No I/O. Must run in < 5ms. Covers all edge cases and error paths.

### Performance Test Depth
```
                     ┌──────────────────────────────┐
                     │ START: What perf test level? │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Are you deploying to production?        │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Is this a major  │    │ Smoke test only:     │
        │ release (breaking│    │ 5 VUs, 2 min. Verify │
        │ changes, infra   │    │ endpoints respond.   │
        │ migration)?      │    └──────────────────────┘
        └──┬───────────┬───┘
           │ YES       │ NO
           ▼           ▼
    ┌────────────┐ ┌──────────────┐
    │ Load +     │ │ Smoke +      │
    │ Stress +   │ │ Load test    │
    │ Soak test  │ │ (p95 < 500ms)│
    └────────────┘ └──────────────┘
```
**When to run full suite:** Major version release, infrastructure migration, expected traffic surge (Black Friday, launch event).  
**When smoke test suffices:** Routine deploy. No infrastructure changes. Response time trend is stable over past 7 days.

### Coverage Strategy
```
                     ┌─────────────────────────────┐
                     │ START: Coverage targets?    │
                     └─────────────┬───────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Code handles auth, payments, or PII?    │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ ≥ 90% line cov.  │    │ ≥ 80% line coverage. │
        │ Branch coverage  │    │ Block merge on drop  │
        │ required. Block  │    │ below threshold.     │
        │ merge on < 90%.  │    └──────────────────────┘
        └──────────────────┘
```
**When 90%+ is required:** Auth, billing, data export, permission systems. Any code where a bug = money lost or data breached.  
**When 80% is acceptable:** Internal tools, admin dashboards, non-critical UI components. Cost of 100% coverage exceeds risk of bug.

### Flaky Test Response
```
                     ┌───────────────────────────┐
                     │ START: Test is flaky      │
                     └───────────┬───────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Failed > 3 times in last 10 runs?   │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Quarantine now.  │  │ Investigate root     │
        │ Move to @flaky   │  │ cause: race cond,    │
        │ suite. Create    │  │ time dependency, or  │
        │ fix ticket (P1). │  │ shared state leak?   │
        └──────────────────┘  └──────────────────────┘
```
**When to quarantine immediately:** CI reliability dropping below 90%. Flaky test blocking > 3 PRs in a week. Root cause unknown and fix estimate > 1 day.  
**When to fix in place:** Root cause obvious (missing await, unseeded random). Fix takes < 30 minutes. Test provides unique coverage no other test provides.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Test Strategy & Pyramid Design
1. **Test pyramid distribution**:
   - **Unit tests (60-70%)**: Individual functions, hooks, components in isolation. Fast (< 5ms each), no I/O, run on every commit.
   - **Integration tests (20-25%)**: Modules working together, database queries, API endpoints, auth flows. Real dependencies (test DB, test Redis), < 200ms each.
   - **E2E tests (5-10%)**: Critical user journeys through the full stack. Real browser/device, real API, real database. < 30s per flow.
   - **Other**: Contract tests, visual regression tests, performance tests, accessibility tests, smoke tests.
2. **Tool selection matrix**:
   | Layer | Frontend | Backend (Node) | Backend (Python) | Backend (Go) |
   |-------|----------|----------------|------------------|--------------|
   | Unit | Vitest + Testing Library | Vitest/Jest | pytest | `go test` |
   | Integration | MSW + Vitest | Supertest | httpx + pytest | `httptest` |
   | E2E | Playwright | — | — | — |
   | API | — | Supertest/Pact | pytest + schemas | testify |
   | Performance | — | k6 / autocannon | k6 | k6 / vegeta |
3. **Coverage targets**: 80% line coverage minimum, 90% for critical paths (auth, payments, data integrity). Enforce via CI quality gate.

### Phase 2 (~30 min): Unit Testing
1. **Structure**: AAA pattern — Arrange, Act, Assert. One assertion per test (behavioral, not implementation detail). Descriptive names: `it('returns 401 when token is expired')`.
2. **Mocking strategy**: Mock at module boundaries — external APIs, databases, file system, clock. Don't mock internals of the module under test. Use `vi.mock` (Vitest), `jest.mock`, `unittest.mock` (Python), `gomock`/`testify`.
3. **Edge cases**: Null/undefined, empty inputs, boundary values (0, -1, MAX_SAFE_INTEGER), invalid types, concurrent calls, error states.
4. **Test data**: Use factories (Fishery, factory_boy, custom builders) for realistic test data. Avoid magic strings/numbers without semantic meaning.
5. **Snapshots**: Use sparingly. Only for stable outputs (serialized data, error messages). Never snapshot large component trees — use specific assertions instead.

### Phase 3 (~20 min): Integration Testing
1. **Database integration**: Test against real PostgreSQL/MongoDB instance (testcontainers, Docker Compose, or dedicated test DB). Each test runs in a transaction that rolls back.
2. **API integration**: Supertest (Express), FastAPI `TestClient`, `httptest` (Go). Test full request → handler → response cycle including middleware, validation, error handling.
3. **Auth integration**: Test login, token refresh, protected endpoint access, role-based access.
4. **External service mocking**: Mock Stripe, SendGrid, AWS SDKs at the HTTP level (nock, MSW, wiremock) or use sandbox/test modes provided by the service.
5. **Test fixtures**: Seed database before test suite with known data. Use migration-based seeding, not ad-hoc inserts.

### Phase 4 (~15 min): End-to-End Testing with Playwright
1. **Setup**: `playwright.config.ts` with multiple projects (Chromium, Firefox, WebKit, Mobile Chrome, Mobile Safari). Configure `baseURL`, `viewport`, `storageState` for authenticated state.
2. **Test structure**: Use Page Object Model (POM) or screen-based fixtures for maintainable selectors. Prefer `getByRole`, `getByLabel`, `getByTestId` over CSS/XPath selectors.
3. **Critical flows to automate**:
   - Signup and onboarding
   - Login/logout and session persistence
   - Core CRUD operations (create, read, update, delete primary entities)
   - Checkout/payment flow (with Stripe test mode)
   - Permission and role boundary testing
   - Error states: network failure, server error, validation errors
4. **Visual regression**: `toHaveScreenshot()` for critical pages. Run on Chromium only. Handle anti-aliasing and OS differences with `maxDiffPixelRatio`.
5. **Authentication state**: `storageState` to reuse authenticated sessions across tests. Avoid re-logging-in for every test.
6. **Data seeding**: Seed via API or database before tests. Each test should create its own data or use isolated test data. Never depend on execution order.

### Phase 5 (~25 min): API & Contract Testing
1. **Schema validation**: Validate API responses against OpenAPI schema or JSON Schema. Use `ajv` (Node), `jsonschema` (Python), `gojsonschema` (Go).
2. **Contract testing with Pact**: Consumer-driven contracts. Consumer defines expectations; provider verifies. Publish pacts to Pact Broker.
3. **Snapshot testing**: Record API responses as snapshots. Diff on change. Useful for ensuring backward compatibility.
4. **Property-based testing**: fast-check (JS), Hypothesis (Python), rapid (Go). Generate random inputs to find edge cases automatically.

### Phase 6 (~25 min): Performance Testing with k6
1. **Test types**:
   - **Smoke test**: Verify system works under minimal load (1-5 VUs). Run on every deploy.
   - **Load test**: Expected production load. Verify response times and error rates at normal traffic.
   - **Stress test**: Find breaking point. Ramp VUs until system degrades.
   - **Soak test**: Sustained load over hours. Find memory leaks, connection pool exhaustion.
   - **Spike test**: Sudden traffic surge. Test auto-scaling response.
2. **k6 script structure**: `export const options = { stages: [...] }`, `export default function() { ... }`. Use `check()` for assertions, `trend()` for custom metrics, `group()` for scenario organization.
3. **Metrics to track**: `http_req_duration` (p50, p95, p99), `http_req_failed`, `http_reqs` (throughput), `vus`, `iterations`. Set thresholds: `http_req_duration: ['p(95)<500']`.
4. **CI integration**: Run smoke tests in CI. Load/stress tests in dedicated environment, not production.

### Phase 7 (~25 min): Quality Gates & CI Integration
1. **CI pipeline testing stages**:
   - **Lint & type-check**: Fast (< 2 min). Block merge on failure.
   - **Unit tests**: Fast (< 5 min). Block merge on failure or coverage drop.
   - **Integration tests**: Medium (< 10 min). Block merge on failure.
   - **E2E smoke tests**: Medium (< 15 min). Non-blocking initially; block once stable.
   - **Performance smoke**: Fast (< 5 min, k6 minimal VUs). Warning threshold only.
2. **Coverage reporting**: Generate coverage in CI. Upload to Codecov/Coveralls. Enforce per-patch coverage (coverage on changed lines).
3. **Flaky test management**: Tag flaky tests with `@flaky` or `.skip`. Quarantine flaky tests in separate suite. Track flaky test rate — investigate if > 2%.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Tests as documentation**: A good test suite explains what the system does. Test names should read like specifications.
- **Deterministic tests**: No `Date.now()`, `Math.random()`, or network calls in unit tests. Use seeded faker/falso for test data.
- **Test isolation**: Tests must not share state. Each test sets up and tears down its own context.
- **Fast feedback**: Unit tests < 5s for the full suite. Integration < 60s. E2E smoke < 5 min. Optimize aggressively.
- **Shift-left testing**: Catch bugs as early as possible. Test at the lowest pyramid level that can verify the behavior.
- **Tagging**: Tag tests by type (`@smoke`, `@regression`, `@slow`, `@flaky`) for selective execution in CI.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
QA engineers bridge development, operations, and product — ensuring quality is built in, not inspected after. Coordination with developers, security, DevOps, and product is essential for shift-left quality.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | API testing, integration test design | API contract (OpenAPI spec), test data requirements, mock service endpoints, error response scenarios |
| **Frontend Developer** | E2E test authoring, visual regression | Test IDs (data-testid), critical user flows, loading/error/empty states, accessibility requirements |
| **Mobile Developer** | Device matrix, platform-specific testing | Device coverage plan, Maestro/Detox configuration, offline scenarios, platform permission test cases |
| **Security Reviewer** | Security test cases, penetration testing | Share auth test scenarios, input validation edge cases; receive security findings for test case creation |
| **DevOps Engineer** | CI test integration, test environments | Test environment provisioning, test database seeding, CI pipeline test stage configuration |
| **CI/CD Builder** | Quality gates, test stage design | Coverage thresholds, flaky test quarantine, test parallelization, artifact management for test reports |
| **Observability Engineer** | Performance testing, SLI validation | k6/Artillery script review, response time thresholds, error rate validation against SLOs |
| **Product Strategist** | Acceptance criteria, user scenarios | Clarify expected behavior, edge cases, and user impact; report quality trends for roadmap input |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Test coverage drops below threshold | Development team lead | Root cause investigation; coverage must be restored before next deploy |
| Flaky test rate exceeds 2% | Development team, DevOps | Quarantine flaky tests; investigate root cause; CI reliability at risk |
| Critical bug found in staging | Product Strategist, Development lead | Go/no-go decision for release; risk assessment |
| Performance threshold breached | Observability Engineer, DevOps | Joint investigation — code regression or infrastructure degradation? |
| Security test failure (auth bypass, data leak) | Security Reviewer, Security Engineer | Immediate remediation; may block release |
| Test environment unavailable or unstable | DevOps Engineer | Blocked testing; escalate for infrastructure fix |

### Escalation Path

```
Release-blocking bug found? → Product Strategist → CTO Advisor
Security vulnerability in testing? → Security Reviewer → Security Engineer
Infrastructure blocking testing? → DevOps Engineer → Cloud Architect
Flaky CI pipeline? → CI/CD Builder → DevOps Engineer
Quality trend degradation (3+ sprints)? → Engineering Manager → CTO Advisor
```

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: QA = you testing manually before launch. No test automation. No test pyramid. No CI/CD tests. No performance testing. Testing = "does it work on my machine?"
- **What to skip**: Test automation. CI/CD test stage. Test pyramid. Coverage metrics. Performance testing. Visual regression. Contract testing. Flaky test management.
- **Coordination**: You test your own code. Manual smoke test before deploy.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Unit tests for critical paths. CI runs tests on PR. Manual QA for releases. Test cases documented (spreadsheet or test management tool). Bug tracking in issue tracker. Basic API testing (manual via Postman).
- **What to skip**: E2E tests. Performance testing. Visual regression. Contract testing. Dedicated QA engineer (devs do testing). Coverage gates. Flaky test management.
- **Coordination**: Test cases reviewed in PR. Release checklist with manual test steps. Weekly bug triage.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated QA engineer. Full test pyramid (unit + integration + E2E). CI with quality gates (coverage ≥80%, no failing tests). Playwright/Cypress E2E for critical flows. Performance smoke tests (k6). API contract tests (Pact). Visual regression on critical pages. Coverage tracking (Codecov). Flaky test management (<2% rate). Test data management.
- **What to skip**: Full-time performance testing team. Multiple QA environments. Dedicated test infrastructure team. AI-driven test generation.
- **Coordination**: QA embedded in product teams. Weekly QA sync. Release go/no-go with QA sign-off. Bi-weekly test case review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: QA team with specialization (automation, performance, security, accessibility). Full test pyramid enforced. Performance testing with production-like load. Chaos engineering. Accessibility testing automated in CI. Security testing in pipeline. Test environment as code. Test data obfuscation. Contract testing across all services. Release management with quality gates. QA metrics and dashboards.
- **What's full production**: Quality engineering center of excellence. Test platform team. Automated test generation. Quality gates pipeline. Release readiness review board.
- **Coordination**: QA leadership weekly. Cross-team test strategy quarterly. Release readiness review per release. Quality metrics review monthly.

### Transition Triggers
- **Solo → Small**: First production bug that testing could have caught. Second developer joining.
- **Small → Medium**: Manual QA cannot keep up with release cadence. First major regression in production. >10K users.
- **Medium → Enterprise**: Multiple products with independent release cycles. Compliance requires test evidence. >100K users.

## Sub-Skills
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


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Test timed out` | Async test not resolving | Add `await` to async assertions; increase `testTimeout` |
| `Element not found` | Selector doesn't match rendered DOM | Use `page.waitForSelector()` before interaction; check render timing |
| `flaky test` | Race condition between test and app state | Add `waitFor`/`toBeVisible` instead of fixed timeouts |
| `Snapshot mismatch` | Component output changed | Run `--updateSnapshot` after intentional UI changes |
| `Network Error` | Mock not set up for endpoint | Add `page.route()` or `server.use()` for all API calls |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Test pyramid distribution documented with coverage targets per layer
- [ ] **[S2]**  Unit test coverage ≥ 80% overall, ≥ 90% for critical paths (auth, payments)
- [ ] **[S3]**  Integration tests covering all API endpoints with real database interactions
- [ ] **[S4]**  Playwright/Cypress E2E tests covering top 5 critical user journeys
- [ ] **[S5]**  API contract tests (schema validation or Pact) for all public-facing endpoints
- [ ] **[S6]**  k6 performance smoke tests running in CI with response time thresholds
- [ ] **[S7]**  Visual regression tests on critical pages with baseline images in repository
- [ ] **[S8]**  Flaky test rate < 2% with quarantine process and investigation backlog
- [ ] **[S9]**  Coverage trends tracked (Codecov/Coveralls) and review required on drops
- [ ] **[S10]**  QA environment with dedicated test database and seeded data refreshed daily

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Playwright Documentation](https://playwright.dev/docs/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [k6 Documentation](https://k6.io/docs/)
- [Pact — Contract Testing](https://docs.pact.io/)
- [Testcontainers](https://testcontainers.com/)
- [Testing Trophy — Kent C. Dodds](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Martin Fowler — TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Google Testing Blog](https://testing.googleblog.com/)
