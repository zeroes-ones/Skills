# Orchestra Platform — Performance Optimization Report

**Date:** 2026-07-18 | **Owner:** Performance Engineering | **Cycle:** Q3 2026 Sprint 3

## Profiling Results

Flame graph analysis of the template engine service under 500 RPS load revealed the following CPU distribution:

| Component | CPU Share (Before) | CPU Share (After) |
|---|---|---|
| Go template parsing/execution | 38% | 12% |
| JSON serialization (std lib) | 22% | 19% |
| Database queries | 18% | 6% |
| Auth middleware (JWT verification) | 12% | 12% |

## Load Test Results (k6)

**Before optimization — baseline at 500 RPS:**
- p95 latency: 180ms — acceptable
- Error rate: 0%

**Before optimization — stress test at 800 RPS:**
- p95 latency: 450ms — breach (SLO: <200ms)
- Error rate: 1.2% — Redis connection pool exhaustion (50 connections maxed out)

## Fixes Applied

1. **Template pre-compilation + LRU cache:** Templates now compiled once at service startup and cached. CPU share dropped from 38% to 12%. p95 improved by 45ms.
2. **Redis connection pool resize:** Increased from 50 → 200 connections. Error rate eliminated at 800 RPS.
3. **Database composite index:** Added `(org_id, service_type)` index on the catalog query path. The `GET /catalog` list endpoint fell from 2.1s → 45ms.
4. **Frontend bundle optimization:** Catalog page bundle reduced 420KB → 180KB via code splitting, route-based lazy loading, and tree shaking unused dependencies.

## Results After Optimization

| Load | p95 Latency | Error Rate |
|---|---|---|
| 500 RPS | 140ms | 0% |
| 800 RPS | 185ms | 0% |
| 1,000 RPS | 220ms | 0% |

**Lighthouse scores:** Mobile 94, Desktop 99.

## Performance Budgets (CI-enforced)

| Budget | Target | Alert |
|---|---|---|
| JS bundle (gzipped) | < 250KB | Build fails if exceeded |
| p95 API latency | < 200ms | Grafana alert, on-call paged |
| Time to Interactive | < 3 seconds | Lighthouse CI check |
| Largest Contentful Paint | < 2.5 seconds | Lighthouse CI check |

## Engineering Principle

> **Never optimize without a baseline measurement.** Load test results that report only averages are misleading — always benchmark p95 and p99. Averages hide tail latency; tails are what users experience.
