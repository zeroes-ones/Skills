# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->
<!-- Run: `bash scripts/checklist-backend.sh` for automated pass/fail on all items. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | API documented with OpenAPI 3.1 spec — shared with consumers, validated in CI | `npx @redocly/cli lint openapi.yaml --format=stylish` → must return 0 | CI: `redocly lint` in `.github/workflows/api-lint.yml` |
| **[S2]** | Authentication and authorization implemented — JWT validated, RBAC enforced, secrets managed | `grep -rn "auth\|jwt\|rbac\|passport" src/ --include="*.ts" --include="*.js"`  → must match > 0 files | — |
| **[S3]** | Input validation on all endpoints — server-side, not client-side only | `grep -rn "validate\|zod\|joi\|yup\|class-validator" src/ --include="*.ts" --include="*.js"`  → must find validation at every POST/PUT handler | ESLint: `no-restricted-imports` — forbid `req.body` direct access outside validation middleware |
| **[S4]** | Error responses consistent format with request IDs for tracing | `grep -rn "request_id\|requestId\|correlationId" src/ --include="*.ts" --include="*.js"`  → must match in error handler | Template: copy `templates/error-response.ts` into `src/middleware/error-handler.ts` |
| **[S5]** | Database migrations versioned and backward-compatible with rollback plan | `npx prisma migrate status` OR `npx knex migrate:list` → must show all applied, no pending | CI check: `prisma migrate deploy --preview-feature` in dry-run mode |
| **[S6]** | Health checks: liveness (`/health`) and readiness (`/health/ready`) endpoints | `curl -s http://localhost:${PORT}/health \| jq .status` → must return `"ok"` | Copy `templates/health-check.ts` into `src/routes/health.ts` |
| **[S7]** | Structured logging with correlation IDs propagated across services | `grep -rn "pino\|winston\|bunyan\|structuredClone\|JSON.stringify" src/ --include="*.ts" --include="*.js"`  → must match logger initialization | — |
| **[S8]** | Graceful shutdown handling SIGTERM with connection draining | `grep -rn "SIGTERM\|SIGINT\|graceful\|server.close" src/ --include="*.ts" --include="*.js"`  → must match signal handler | Copy `templates/graceful-shutdown.ts` into `src/server.ts` |
| **[S9]** | Rate limiting and throttling on public endpoints | `grep -rn "rate.limit\|rateLimit\|express-rate-limit\|throttle" src/ --include="*.ts" --include="*.js"`  → must match middleware setup | `npm install express-rate-limit` + copy `templates/rate-limit.ts` |
| **[S10]** | Integration tests on database, cache, and external service interactions | `npx jest --testPathPattern="integration\|\.integration\." --passWithNoTests` (or vitest equivalent) → must find and pass integration tests | CI: `jest --testPathPattern=integration` in pipeline |
| **[S11]** | Load tested at 2× expected peak QPS before production launch | `npx autocannon -c 100 -d 30 http://localhost:${PORT}/api/health` → P99 latency must be < 100ms at 2× peak QPS | `npm install --save-dev autocannon` + script: `scripts/load-test.sh` |
| **[S12]** | Monitoring: error rate, P95 latency, throughput, DB connection pool, queue depth | `grep -rn "prometheus\|datadog\|newrelic\|opentelemetry\|metrics" package.json`  → must find monitoring SDK | `npm install prom-client` + copy `templates/metrics.ts` |
