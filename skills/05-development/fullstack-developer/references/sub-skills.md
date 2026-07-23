# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `monorepo-architecture` | Setting up Turborepo/Nx with shared packages, dependency graphs, and CI caching | Package boundaries, build pipeline design, shared config strategy, import constraints |
| `api-design` | Designing REST, GraphQL, or tRPC APIs consumed by your own frontend | End-to-end type safety, contract sharing, error response standardization, pagination patterns |
| `database-integration` | Prisma/Drizzle schema design, migrations, query optimization from server-side code | Migration safety (locking, backfill), N+1 prevention, connection pooling, read replicas |
| `auth-fullstack` | Implementing auth flows spanning client and server (NextAuth, Lucia, Clerk) | Session management (HttpOnly cookies vs JWT), CSRF, refresh token rotation, RBAC enforcement |
| `server-actions` | Next.js Server Actions for form mutations with progressive enhancement | `useFormState` + Zod, `revalidatePath`/`revalidateTag`, optimistic updates, error handling |
| `e2e-testing` | Playwright tests covering full stack: UI → API → DB → back | Test data seeding, auth state reuse, API mocking strategy, visual regression, CI parallelization |
| `deployment-orchestration` | CI/CD pipelines deploying frontend + backend + database migrations atomically | Environment parity, migration rollback, preview deployments, feature flag rollout |
| `observability-fullstack` | Distributed tracing with correlation IDs across frontend, API, and database | OpenTelemetry setup, structured logging, RUM integration, SLO dashboard for full-stack features |
