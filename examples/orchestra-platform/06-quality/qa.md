# QA Report — Release v0.9.0

**Test Period**: July 10–18, 2026  
**Release Candidate**: v0.9.0-rc3 → v0.9.0  
**QA Lead**: Maria Santos

## Test Pyramid

| Layer | Count | Framework | Runtime |
|-------|-------|-----------|---------|
| Unit | 247 | Vitest (frontend), Go testing (backend) | 32s (parallel) |
| Integration | 82 | Supertest (API), Testing Library (components) | 4m 12s |
| E2E | 15 | Playwright 1.45 | 8m 47s (3 workers) |

## E2E Test Scenarios — Playwright

Tests run against a full-stack staging environment on every PR. Scenarios: catalog CRUD (create service, edit metadata, verify in list, delete with confirmation), template execution (select "Go API", configure ports, deploy, verify service appears with health status), plugin install (browse marketplace, install Prometheus Exporter plugin, verify config page renders), and auth flow (login, session persistence across page reloads, logout clears session, protected routes redirect to login). All 15 tests pass consistently with zero flakes over 50 CI runs.

## Performance Baseline

Load testing via k6 against staging: p50 62ms, p95 178ms, p99 310ms. Target: p95 < 200ms — met on all endpoints except template execution (p95 420ms due to container build time, excluded from target as it's an async operation). Stress test: 1,000 concurrent virtual users ramping over 5 minutes — 0 errors, p95 degraded to 890ms but recovered within 2 minutes of ramp-down.

## Manual Exploratory Testing

12 test charters executed by 2 QA engineers over 3 days. Focus areas: error recovery (kill mid-deployment, verify retry), concurrent operations (two template executions simultaneously), browser compatibility (Chrome 126, Firefox 128, Safari 17, Edge 126), and responsive layout (1920px, 1440px, 1024px, 375px viewports).

## Bugs Found

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| BUG-412 | Medium | Plugin config save fails silently if JSON has trailing comma | Fixed in rc4 |
| BUG-415 | Medium | Template wizard back button loses environment variable entries | Fixed in rc4 |
| BUG-418 | Low | Admin dashboard date picker resets to UTC midnight instead of local | Deferred to v0.9.1 |

All bugs verified fixed in v0.9.0-rc4. Release approved for production deployment on July 21, 2026.
