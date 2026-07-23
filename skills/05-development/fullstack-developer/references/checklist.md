# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Monorepo with shared types/validation package consumed by frontend and backend | `grep -rn "\"@repo/validators\"\|\"@app/validators\"" package.json apps/*/package.json` → must match in both frontend and backend | Template: copy `packages/validators/` monorepo starter |
| **[S2]** | All API responses typed end-to-end (tRPC, typed fetch, or generated client) | `grep -rn "as \w+\|as any" src/ --include="*.tsx" --include="*.ts" -c` → must return 0 | eslint `@typescript-eslint/no-unsafe-assignment: error` |
| **[S3]** | Authentication flow working across all layers (signup, login, session refresh, logout) | `curl -s -X POST http://localhost:${PORT}/api/auth/signup -d '{"email":"test@test.com","password":"Test123!"}' \| jq .token` → must return JWT | Copy `templates/auth-flow.ts` test suite |
| **[S4]** | Authorization enforced on server for all protected operations | `curl -s http://localhost:${PORT}/api/admin/users \| jq .status` → must return 401 (without token) | `npm install @casl/ability` + copy `templates/rbac-middleware.ts` |
| **[S5]** | Form submissions validated on server with shared Zod schemas | `grep -rn "z\.object\|zodResolver" apps/*/src/ -l \| sort \| uniq -c \| awk '$1 < 2'` → every schema must appear in both web and api | Template: copy `packages/validators/src/schemas/` |
| **[S6]** | Error, loading, and empty states handled on every data-dependent view | `grep -rn "\.status\|isLoading\|isError\|isEmpty" src/ --include="*.tsx" -l \| wc -l` → must match all data views | — |
| **[S7]** | E2E test covering at least one critical flow (UI → API → DB → back) | `npx playwright test --project=chromium --grep "@critical"` → must pass | `npx create-playwright` + copy `e2e/critical-flow.spec.ts` |
| **[S8]** | Database migrations run automatically in CI/CD with backup step | `npx prisma migrate status` → must show all applied, no pending | CI: `prisma migrate deploy` as pre-deploy job |
| **[S9]** | Structured logging with correlation IDs spanning frontend through backend | `grep -rn "x-correlation-id\|correlationId" src/ --include="*.ts" --include="*.tsx" -l \| wc -l` → must match ≥ 2 (frontend + backend) | Copy `templates/correlation-middleware.ts` into each service |
| **[S10]** | Feature flags in place for gradual rollout of major features | `grep -rn "useFeatureFlag\|featureFlag\|launchdarkly\|flagsmith\|unleash" src/ --include="*.ts" --include="*.tsx"` → must match | `npm install @vercel/flags` |
