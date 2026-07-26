# testing-matrix

Reference documentation for the automation-engineer skill — the complete 12-layer testing pyramid with platform-specific tooling, CI integration patterns, and quality gates.

## Layer 1: Static Analysis

**Purpose:** Catch bugs, style violations, and type errors before tests run. Zero runtime overhead.

| Platform | Tools | Config File |
|----------|-------|-------------|
| iOS/Android (Swift/Kotlin) | SwiftLint, SwiftFormat, detekt, ktlint | `.swiftlint.yml`, `detekt-config.yml` |
| Web/JS | ESLint, Prettier, TypeScript | `.eslintrc.js`, `tsconfig.json` |
| Python/Backend | ruff, mypy, black, pylint | `pyproject.toml`, `mypy.ini` |

**SwiftLint + SwiftFormat (iOS):**
```yaml
# .swiftlint.yml
opt_in_rules:
  - force_unwrapping
  - unavailable_function
line_length: 120
type_body_length: 400
```
```bash
swiftlint lint --strict --reporter github-actions-logging
swiftformat --lint --swiftversion 5.9 Sources/
```

**ESLint + Prettier (Web):**
```json
// package.json scripts
{
  "lint": "eslint src/ --ext .ts,.tsx --max-warnings 0",
  "format:check": "prettier --check 'src/**/*.{ts,tsx,css}'",
  "typecheck": "tsc --noEmit"
}
```

**ruff + mypy (Python):**
```toml
# pyproject.toml
[tool.ruff]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM"]
line-length = 120

[tool.mypy]
strict = true
ignore_missing_imports = false
```

**CI integration (GitHub Actions snippet):**
```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: npm ci && npm run lint && npm run format:check && npm run typecheck
```

## Layer 2: Unit Tests

**Purpose:** Validate individual functions/methods in isolation. Fast, deterministic, no I/O.

| Platform | Framework | Runner | Mocking |
|----------|-----------|--------|---------|
| iOS | XCTest | xcodebuild test | Cuckoo, SwiftyMocky |
| Android | JUnit 5, kotest | Gradle test task | MockK, Mockito |
| Web/JS | Vitest, Jest | vitest, jest | vi.fn(), msw |
| Python | pytest | pytest | unittest.mock, pytest-mock |

**XCTest (iOS):**
```bash
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.0' \
  -resultBundlePath TestResults.xcresult \
  -enableCodeCoverage YES \
  | xcbeautify
```

**Vitest (Web/JS):**
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: { provider: 'v8', reporter: ['text', 'lcov'], thresholds: { branches: 80, functions: 80, lines: 80, statements: 80 } },
  },
});
```

**pytest (Python/Backend):**
```ini
# pyproject.toml
[tool.pytest.ini_options]
addopts = "-v --tb=short --strict-markers --maxfail=5"
testpaths = ["tests"]
markers = ["slow: marks tests as slow", "integration: marks tests as integration"]
```

## Layer 3: Integration Tests

**Purpose:** Verify multiple components work together correctly — database, APIs, message brokers.

| Platform | Approach | Tools |
|----------|----------|-------|
| iOS/Android | CoreData/Room with in-memory store, test doubles | OHHTTPStubs, WireMock (embedded) |
| Web/JS | Test HTTP layer with msw, test DB with Docker | msw, vitest, supertest |
| Python/Backend | TestClient against real DB in test container | pytest, httpx, testcontainers-python |

**Testcontainers (Python backend + Postgres):**
```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg.get_connection_url()

def test_create_user(postgres, client):
    res = client.post("/users", json={"email": "a@b.com"})
    assert res.status_code == 201
```

**Gradle integration tests (Android):**
```kotlin
// app/build.gradle.kts
android {
    sourceSets {
        create("integrationTest") {
            java.srcDir("src/integrationTest/java")
        }
    }
}
tasks.register<Test>("integrationTest") {
    testClassesDirs = files(tasks.named("compileIntegrationTestKotlin"))
    classpath = files(tasks.named("compileIntegrationTestKotlin"))
    useJUnitPlatform()
}
```

## Layer 4: Component Tests

**Purpose:** Test a component's behavior through its public interface (API endpoint, UI widget in isolation).

| Platform | Framework | Scope |
|----------|-----------|-------|
| iOS | SwiftUI preview tests, ViewInspector | Single view/view model |
| Android | Compose testing, Robolectric | Single composable |
| Web/JS | React Testing Library, Cypress Component Testing | Single component |
| Python | httpx TestClient | Single endpoint + service layer |

**React Testing Library (Web component):**
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

test('shows validation error on empty submit', async () => {
  render(<LoginForm onSubmit={vi.fn()} />);
  fireEvent.click(screen.getByRole('button', { name: /sign in/i }));
  expect(await screen.findByText(/email is required/i)).toBeVisible();
});
```

**Compose testing (Android):**
```kotlin
@Test
fun searchField_showsResults_onInput() {
    composeTestRule.setContent { SearchScreen(viewModel) }
    composeTestRule.onNodeWithTag("search_field").performTextInput("kotlin")
    composeTestRule.onAllNodesWithTag("result_item").assertCountEquals(3)
}
```

## Layer 5: End-to-End (E2E) Tests

**Purpose:** Exercise complete user flows through the real application against real (or containerized) backends.

| Platform | Tool | Key Config |
|----------|------|------------|
| iOS | XCUITest | `XCUIApplication().launch()` |
| Android | Espresso, UI Automator | `ActivityScenario.launch()` |
| Web | Playwright, Cypress | `playwright.config.ts` |
| Mobile (cross) | Detox, Maestro | `.detoxrc.js` |

**Playwright (Web E2E):**
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 7'] } },
  ],
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 3 : undefined,
});
```

**Detox (React Native E2E):**
```javascript
// .detoxrc.js
module.exports = {
  apps: {
    'ios.debug': { type: 'ios.app', binaryPath: 'ios/build/Build/Products/Debug-iphonesimulator/App.app', build: 'xcodebuild ...' },
    'android.debug': { type: 'android.apk', binaryPath: 'android/app/build/outputs/apk/debug/app-debug.apk', build: 'cd android && ./gradlew assembleDebug' },
  },
  devices: {
    simulator: { type: 'ios.simulator', device: { type: 'iPhone 16' } },
    emulator: { type: 'android.emulator', device: { avdName: 'Pixel_7_API_34' } },
  },
  configurations: { 'ios.sim.debug': { device: 'simulator', app: 'ios.debug' }, 'android.emu.debug': { device: 'emulator', app: 'android.debug' } },
};
```

## Layer 6: Visual Regression Tests

**Purpose:** Detect unintended visual changes by comparing screenshots against baselines.

| Platform | Tool | Approach |
|----------|------|----------|
| iOS | swift-snapshot-testing | Compare UIView/CALayer snapshots |
| Android | Paparazzi, Roborazzi | Render composables/layouts without emulator |
| Web | Percy, Chromatic, Playwright screenshots | DOM snapshot diffing |

**Paparazzi (Android — no emulator needed):**
```kotlin
@Test
fun homeScreen_snapshot() {
    paparazzi.snapshot { HomeScreen() }
}
```

**Playwright visual (Web):**
```typescript
test('landing page visual', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('landing.png', { maxDiffPixelRatio: 0.01 });
});
```

## Layer 7: Performance Tests

**Purpose:** Establish and enforce latency, throughput, and resource budgets.

| Platform | Tool | Metric |
|----------|------|--------|
| iOS | MetricKit, XCTest performance tests | CPU, memory, launch time |
| Android | Macrobenchmark, Systrace | Frame timing, startup |
| Backend | k6, Locust, Artillery | RPS, p95 latency |

**k6 (backend load test):**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 0 },
  ],
  thresholds: { http_req_duration: ['p(95)<500'], http_req_failed: ['rate<0.01'] },
};
export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Layer 8: Security Tests (SAST + DAST + SCA)

**Purpose:** Detect vulnerabilities in dependencies, code, and running applications.

| Category | Tools | CI Integration |
|----------|-------|---------------|
| SAST (code) | Semgrep, CodeQL, Bandit | Pull request checks |
| SCA (deps) | Dependabot, Snyk, npm audit, OWASP Dependency-Check | Scheduled + PR checks |
| DAST (runtime) | OWASP ZAP, Burp Suite | Staging-only, nightly |
| Secrets | truffleHog, gitleaks, GitGuardian | Pre-commit + CI |

```yaml
# GitHub Actions: security matrix
security:
  strategy:
    matrix:
      scan: [semgrep, trivy, gitleaks]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - if: matrix.scan == 'semgrep'
      uses: semgrep/semgrep-action@v1
      with: { config: 'p/default' }
    - if: matrix.scan == 'trivy'
      uses: aquasecurity/trivy-action@master
      with: { scan-type: 'fs', scanners: 'vuln,secret,misconfig', severity: 'CRITICAL,HIGH' }
    - if: matrix.scan == 'gitleaks'
      uses: gitleaks/gitleaks-action@v2
```

## Layer 9: Accessibility Tests

**Purpose:** Enforce WCAG compliance automatically in CI.

| Platform | Tool | Standard |
|----------|------|----------|
| iOS | Accessibility Inspector, XCTest `accessibility` queries | VoiceOver labels |
| Android | Accessibility Scanner, Espresso `AccessibilityChecks` | Content descriptions |
| Web | axe-core, pa11y, Lighthouse CI | WCAG 2.2 AA |

```typescript
// Playwright + axe-core
import { injectAxe, checkA11y } from 'axe-playwright';
test('a11y audit', async ({ page }) => {
  await page.goto('/settings');
  await injectAxe(page);
  const results = await checkA11y(page, null, {
    detailedReport: true,
    detailedReportOptions: { html: true },
  });
  expect(results.violations).toEqual([]);
});
```

**CI Lighthouse audit (Web):**
```yaml
lighthouse:
  runs-on: ubuntu-latest
  steps:
    - uses: treosh/lighthouse-ci-action@v12
      with:
        urls: 'https://staging.example.com/'
        budgetPath: .github/lighthouse/budget.json
        uploadArtifacts: true
```

## Layer 10: Contract Tests

**Purpose:** Verify API providers and consumers agree on schema and behavior.

| Pattern | Tool | Format |
|---------|------|--------|
| HTTP API | Pact, Spring Cloud Contract | Pact JSON |
| GraphQL | GraphQL Inspector | Schema diff |
| Async/Events | Pact (message), AsyncAPI | AsyncAPI spec |

```bash
# Pact broker + CI
pact-broker can-i-deploy --pacticipant OrderService --version $(git rev-parse HEAD) --to-environment production
```

```typescript
// Consumer pact test
import { Pact } from '@pact-foundation/pact';
const provider = new Pact({ consumer: 'WebApp', provider: 'UserService', port: 1234 });
provider.addInteraction({
  uponReceiving: 'a request for user',
  withRequest: { method: 'GET', path: '/users/1' },
  willRespondWith: { status: 200, body: { id: 1, name: 'Alice' } },
});
```

## Layer 11: Smoke Tests

**Purpose:** Quick sanity check after deploy — is the system fundamentally alive?

```yaml
# GitHub Actions: post-deploy smoke
smoke:
  needs: deploy-staging
  runs-on: ubuntu-latest
  steps:
    - run: |
        curl -fsS -o /dev/null https://staging.example.com/health
        curl -fsS https://staging.example.com/api/v1/status | jq -e '.database == "connected"'
    - name: Playwright smoke
      run: npx playwright test --grep '@smoke' --project=chromium
```

**Key principles:** Run against production or staging, fail fast (<30s), test critical paths only (login, checkout, API health).

## Layer 12: Chaos Tests

**Purpose:** Validate system resilience by intentionally injecting failures.

| Tool | Use Case | Target |
|------|----------|--------|
| Chaos Mesh | K8s chaos | Pod kill, network delay, CPU stress |
| Gremlin | Managed chaos | Multi-cloud |
| toxiproxy | Network chaos | TCP connection disruption |

```bash
# Chaos Mesh: inject pod kill in CI
kubectl apply -f - <<EOF
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: ci-pod-kill
spec:
  action: pod-kill
  mode: one
  selector: { namespaces: [staging], labelSelectors: { app: api } }
  scheduler: { cron: "@every 30s" }
EOF
sleep 60 && ./run-smoke-tests.sh && kubectl delete podchaos ci-pod-kill
```

## Flaky Test Quarantine Pattern

Quarantine flaky tests automatically: move them out of the critical path to a separate suite that runs but does not block merge.

```typescript
// jest-flaky.config.ts — quarantined suite
export default {
  testMatch: ['**/__quarantine__/**/*.test.ts'],
  maxRetries: 3, // flaky suite gets higher retries
};
```

```yaml
# CI: quarantine job — runs in parallel, never blocks merge
quarantine:
  runs-on: ubuntu-latest
  continue-on-error: true  # <-- critical: never blocks
  steps:
    - run: npx jest --config jest-flaky.config.ts --json --outputFile=quarantine.json
    - uses: actions/upload-artifact@v4
      if: failure()
      with: { name: quarantine-report, path: quarantine.json }
```

**Quarantine workflow:** Detect flaky tests → auto-move to `__quarantine__/` directory → create ticket → run in quarantine suite → if passes 5× consecutively, promote back.

## Test Impact Analysis Pattern

Only run tests affected by code changes. Uses dependency graphs and coverage data.

```bash
# Jest --onlyChanged (git-aware)
npx jest --onlyChanged --coverage

# pytest-testmon (smart test selection)
pytest --testmon --testmon-noselect
```

```yaml
# CI: TIA matrix
test-impact:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/cache@v4
      with:
        path: .testmondata
        key: testmon-${{ runner.os }}-${{ github.ref_name }}
        restore-keys: testmon-${{ runner.os }}-
    - run: pytest --testmon --testmon-noselect --junitxml=results.xml
    - run: pytest --testmon --junitxml=full-results.xml  # fallback: full suite if no selection
```

**Knapsack Pro / Buildkite Test Splitter** for parallelizing by test execution time history.

## Coverage Threshold Enforcement

Fail the build when coverage drops below minimum thresholds — enforced in CI, not advisory.

```yaml
# nyc / Istanbul
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 1%  # allow 1% drop on a single PR
    patch:
      default:
        target: 90%  # new code must be well-covered
```

```typescript
// vitest coverage thresholds
coverage: {
  thresholds: {
    lines: 80,
    functions: 80,
    branches: 75,
    statements: 80,
  },
}
```

```toml
# pyproject.toml
[tool.coverage.report]
fail_under = 80
exclude_lines = ["pragma: no cover", "raise NotImplementedError", "if TYPE_CHECKING:"]
```

**Enforcement CI step:**
```yaml
- name: Coverage gate
  run: |
    COV=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
    if (( $(echo "$COV < 80" | bc -l) )); then
      echo "Coverage $COV% below 80% threshold" >&2 && exit 1
    fi
```
