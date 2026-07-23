# Core Workflow — Full Implementation

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
