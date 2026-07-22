---
name: fullstack-developer
description: "End-to-end feature delivery across frontend and backend, API consumption and design, database queries, authentication flows, monorepo patterns, deployment pipelines, and full-stack testing. Trigger: fullstack, full-stack, end-to-end, frontend-backend integration, monorepo, fullstack feature."
author: Sandeep Kumar Penchala
type: development
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - fullstack-developer
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Fullstack Developer

Deliver complete features across the entire stack — from database to UI. This skill covers end-to-end feature development: TypeScript monorepos with shared types, full-stack frameworks (Next.js, Remix, SvelteKit), API integration patterns, database access from server-side code, authentication flows spanning frontend and backend, deployment orchestration, and comprehensive testing across all layers.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Build a full-stack feature end-to-end → Start at "Core Workflow" — follow all phases
├── Frontend-heavy task (UI, state, routing) → Invoke frontend-developer skill for deep patterns
├── Backend-heavy task (API, database, auth) → Invoke backend-developer skill for deep patterns
├── Integrate a REST/GraphQL API → Jump to "Core Workflow > Phase 2 (API Integration)"
├── Set up database access (Prisma/Drizzle/SQL) → Go to "Decision Trees > Database Access Pattern"
├── Implement authentication (NextAuth/Clerk/Lucia) → Go to "references/auth-patterns.md"
├── Set up a monorepo → Jump to "Decision Trees > Monorepo vs Polyrepo"
├── Deploy a full-stack app → Go to "Core Workflow > Phase 5 (Deployment)"
└── Don't know where to start? → Describe the feature in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never start without defining the API contract first.** Frontend and backend must agree on the shape of data before either side writes code. Do not build UI and API in parallel without a shared contract.
- **Always consider which side owns the logic.** Validation on both sides (defense in depth), but business logic lives on the backend. Do not put pricing calculations or auth decisions in the frontend.
- **Don't optimize prematurely.** Build the simplest end-to-end path first, then profile. Do not split into microservices or add Redis caching before you have a working feature and measured bottlenecks.
- **Always test across the full stack.** A passing frontend test + passing backend test ≠ a working feature. Integration tests that cross the boundary are non-negotiable.
- **Admit what you don't know.** If a task is purely frontend or purely backend, say so and invoke the specialized skill rather than giving shallow advice.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Delivering a feature that spans database, API, and UI layers
- Building full-stack applications with Next.js, Remix, SvelteKit, or Nuxt
- Setting up monorepos (Turborepo, Nx, pnpm workspaces) with shared packages
- Integrating frontend with REST/GraphQL APIs and implementing data fetching patterns
- Implementing authentication flows that span client and server (NextAuth, Lucia, Clerk)
- Querying databases from server-side code (Prisma, Drizzle, SQLAlchemy)
- Setting up CI/CD pipelines for full-stack deployments (Vercel, Railway, Docker)
- <!-- DEEP: 10+min -->
Debugging issues that cross the frontend-backend boundary

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Monorepo vs Polyrepo
```
                     ┌──────────────────────────┐
                     │ START: One repo or many? │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Do frontend and backend share       │
              │ types, validation, or configs?      │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Monorepo with    │  │ Teams fully           │
        │ shared packages. │  │ independent with      │
        │ Turborepo/Nx for │  │ separate release      │
        │ task orchestration│  │ cycles?               │
        └──────────────────┘  └──┬───────────────┬───┘
                                 │ YES           │ NO
                                 ▼               ▼
                          ┌────────────┐  ┌──────────────┐
                          │ Polyrepo   │  │ Monorepo     │
                          │ with       │  │ still        │
                          │ published  │  │ simplifies   │
                          │ packages   │  │ coordination │
                          └────────────┘  └──────────────┘
```
**When Monorepo:** Shared types/Zod schemas between frontend and backend. Single CI triggering. Atomic cross-cutting changes. Team < 30 engineers.  
**When Polyrepo:** Fully independent services with separate deploy cadences. Teams don't need each other's code. Published API contracts are sufficient.

### API Architecture Decision
```
                     ┌──────────────────────────────┐
                     │ START: REST, GraphQL, tRPC?  │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Is the frontend and backend the same    │
              │ team (monolith/monorepo)?               │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ tRPC: end-to-end │    │ Does client need     │
        │ type safety from │    │ flexible/partial     │
        │ DB to UI. No code│    │ data fetching?       │
        │ generation.      │    └──┬───────────────┬───┘
        └──────────────────┘       │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ GraphQL    │  │ REST with    │
                            │ with       │  │ OpenAPI code │
                            │ Relay/     │  │ generation   │
                            │ Apollo     │  └──────────────┘
                            └────────────┘
```
**When tRPC:** TypeScript monorepo. Same team owns frontend + backend. No third-party API consumers. Prototype speed matters.  
**When REST:** Public API consumed by third parties. Caching via CDN/HTTP important. Simple CRUD with predictable resource patterns.

### Auth Strategy
```
                     ┌──────────────────────────────┐
                     │ START: Auth approach?        │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Using Next.js?                          │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ NextAuth/Auth.js │    │ Need enterprise SSO  │
        │ for built-in     │    │ (SAML/OIDC) or       │
        │ provider support.│    │ multi-tenant?        │
        │ Server Components│    └──┬───────────────┬───┘
        │ + middleware.    │       │ YES           │ NO
        └──────────────────┘       ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ Clerk /    │  │ Lucia +      │
                            │ WorkOS /   │  │ custom DB.   │
                            │ Auth0      │  │ Session-based│
                            │ (managed)  │  │ or JWT.      │
                            └────────────┘  └──────────────┘
```
**When NextAuth:** Next.js app. OAuth providers (Google, GitHub) needed. JWT sessions adequate. Team wants fast setup with configuration over code.  
**When Clerk/WorkOS:** Enterprise SSO (SAML). Multi-tenant with org management. Need pre-built UI components. Don't want to store passwords.

### Deployment Platform
```
                     ┌──────────────────────────────┐
                     │ START: Where to deploy?      │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Using Next.js or SvelteKit?             │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Vercel. Zero-    │    │ Need full container  │
        │ config edge +    │    │ control, multi-      │
        │ serverless. Best │    │ process, or specific │
        │ DX for frameworks│    │ networking?          │
        └──────────────────┘    └──┬───────────────┬───┘
                                   │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ Railway /  │  │ PaaS: Render,│
                            │ Fly.io /   │  │ Heroku,      │
                            │ Docker on  │  │ or managed   │
                            │ ECS        │  │ container    │
                            └────────────┘  └──────────────┘
```
**When Vercel:** Next.js/SvelteKit app. Edge functions useful. Preview deployments needed. Team < 10. Don't want to manage infrastructure.  
**When Docker/ECS:** Background workers, cron jobs, WebSocket servers. Specific networking requirements (VPC, service mesh). Compliance requires specific base images.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Monorepo Setup & Shared Contracts
1. **Package manager**: pnpm workspaces for efficient disk usage and strict dependency resolution.
2. **Monorepo structure**:
   ```
   /apps
     /web        — Next.js frontend
     /api        — Express/Fastify/Hono backend (if separate)
   /packages
     /shared     — TypeScript types, Zod schemas, constants
     /ui         — Shared React/Vue component library
     /config     — ESLint, TypeScript, Tailwind configs
     /database   — Prisma/Drizzle schema, migrations
   ```
3. **Shared types**: Single source of truth for API contracts. `packages/shared` exports DTOs, Zod validation schemas, TypeScript interfaces. Imported by both frontend and backend.
4. **Turborepo pipeline**: Define `turbo.json` with dependency-aware tasks: `build`, `lint`, `typecheck`, `test`, `dev`. Caching for unchanged packages.

### Phase 2 (~30 min): Full-Stack Feature Development
1. **Start from the database**: Design schema changes with Prisma/Drizzle migrations. Write seed data for the feature. Create repository functions with proper types.
2. **API layer**: Implement endpoint in server code (Next.js API routes, tRPC router, Express controller, or Server Actions). Apply validation with shared Zod schemas. Return typed responses.
3. **Frontend integration**: Call API with TanStack Query (client components) or direct fetch (server components). Handle loading, error, empty, and success states. Implement optimistic updates for mutations.
4. **End-to-end type safety**: tRPC for full type safety from DB to UI without code generation. Or use OpenAPI-generated client from shared spec.
5. **Authentication awareness**: Protected routes on both server (middleware) and client (redirect unauthenticated). Access session/user in API, pass to frontend via server components or API response.

### Phase 3 (~20 min): Data Flow Patterns
1. **Server Components (Next.js App Router)**: Fetch data directly in Server Components — `async` components calling DB or internal APIs. No client-side waterfall.
2. **tRPC**: Define procedures (queries, mutations, subscriptions) in backend; import types directly in frontend. Auto-completion for inputs and outputs.
3. **REST with generated client**: OpenAPI spec → `openapi-typescript` + `openapi-fetch` for type-safe fetch wrapper. Share spec as workspace package.
4. **GraphQL**: Codegen from schema to generate typed hooks (`useQuery`, `useMutation`). Fragment colocation for component-level data requirements.
5. **Server Actions** (Next.js): Form mutations handled on server. Use `useFormState` + Zod validation. Revalidate affected paths with `revalidatePath`/`revalidateTag`.

### Phase 4 (~15 min): Authentication Flows
1. **Credentials**: Email/password with bcrypt hashing. Session-based (Iron Session, express-session) or JWT. CSRF protection for cookie-based auth.
2. **OAuth/OIDC**: NextAuth.js/Auth.js for Next.js; Lucia for framework-agnostic. Configure multiple providers (Google, GitHub, enterprise SSO). Handle account linking.
3. **Session management**: HttpOnly, Secure, SameSite=Lax cookies. Session expiry with sliding expiration. Refresh token rotation with reuse detection (family-based).
4. **Authorization**: Role-based access control (RBAC) checked in middleware and API layer. Column-level or row-level security in database (PostgreSQL RLS) for multi-tenant apps.
5. **Protected page patterns**: Middleware redirect for unauthenticated requests. Loading state while session resolves. Graceful handling of expired sessions.

### Phase 5 (~25 min): Testing Across the Stack
1. **Database tests**: Integration tests with real PostgreSQL (testcontainers or Docker Compose). Apply migrations, seed data, run tests, rollback. Each test in its own transaction.
2. **API tests**: Supertest (Express) or `testClient` (Hono) or `request` (Next.js). Test status codes, response shape, error handling, auth checks.
3. **Frontend tests**: Vitest + Testing Library for components. Mock API responses with MSW (Mock Service Worker) for realistic network simulation.
4. **E2E tests**: Playwright with real backend (no mocking). Test critical flows: signup, login, core CRUD, checkout. Run against staging environment.
5. **Contract tests**: Verify frontend expectations match backend responses. Use shared Zod schemas as contract. Consider Pact for cross-team scenarios.

### Phase 6 (~25 min): Deployment & Observability
1. **Platform**: Vercel (Next.js, SvelteKit), Railway/Render (Docker), Fly.io (edge), AWS ECS/EKS (enterprise). Use Infrastructure as Code (Terraform/Pulumi).
2. **Environment parity**: Dev, Staging, Production environments identical except for scale. Use same Docker image promoted through environments.
3. **Database migrations in CI/CD**: Run migrations as part of deploy pipeline. Transactional migrations with rollback capability. Backup before migration.
4. **Observability**: OpenTelemetry for distributed tracing across frontend and backend. Structured logging with correlation IDs propagated through all layers. Frontend RUM (Real User Monitoring) with web-vitals.
5. **Feature flags**: LaunchDarkly, GrowthBook, or homegrown. Wrap new features; toggle per environment, user segment, or percentage rollout.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Type safety end-to-end**: Use Zod schemas shared between frontend and backend. tRPC or typed fetch for compile-time guarantees.
- **Server-first data fetching**: Fetch on server when possible (RSC, SSR loaders). Eliminates client-server waterfalls and improves LCP.
- **Progressive enhancement**: Core functionality works without JavaScript. Forms submit natively; JavaScript enhances with client-side validation and optimistic UI.
- **Single source of truth**: Shared validation, shared types, shared constants. DRY across the stack.
- **Graceful degradation**: External service failures shouldn't crash the app. Show cached/stale data, fallback UI, retry buttons.
- **Security mindset**: Validate on both client (UX) and server (security). Never trust client input. Sanitize user-generated content. CSP headers, CSRF tokens.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Fullstack developers own features end-to-end — database to UI. This breadth means they coordinate with nearly every role: backend for API design, frontend for UX patterns, DevOps for deployment, and security for auth hardening.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | Shared API ownership, separate backend services | API contract boundaries, service ownership, middleware compatibility |
| **Frontend Developer** | UI patterns, component library usage | Shared component API, design token alignment, state management conventions |
| **Database Designer** | Schema changes, migration strategy | Migration scripts, index recommendations, query performance expectations |
| **Security Engineer** | Auth flows spanning client-server | Session management approach (JWT vs cookies), CSRF protection, input validation strategy |
| **DevOps Engineer** | Deployment pipeline, environment config | Full-stack build steps, environment variables, database migration in CI/CD |
| **QA Engineer** | E2E test scenarios, integration testing | Critical user paths, test data seeding, API mocking strategy for error states |
| **Observability Engineer** | Distributed tracing, error tracking | Correlation ID propagation (frontend → API → DB), structured log format, RUM integration |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Database schema change requiring migration | Backend, DevOps, QA | Deployment sequencing, test environment reset, rollback plan |
| Auth flow redesign (new provider, session change) | Security Engineer, Frontend | Security review, cross-client impact assessment |
| Monorepo structure change | All developers in repo | Build pipeline impact, import path changes, local dev setup |
| Shared package breaking change | Backend, Frontend, Mobile (if consumers) | Version bump coordination, migration guide |
| Deployment blocking issue | DevOps | Rollback decision, hotfix path |

### Escalation Path

```
Database migration failure? → Database Designer → DevOps Engineer
Auth vulnerability discovered? → Security Engineer → CTO Advisor
Cross-service integration broken? → Backend Developer → System Architect
Deploy blocked (infra)? → DevOps Engineer → Cloud Architect
```


**What good looks like:** Feature works end-to-end: user clicks button → API call → database write → UI updates. TypeScript types shared between frontend and backend with zero contract drift. CI pipeline runs full-stack tests in under 10 minutes.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Fullstack = Next.js (pages or app router) or Remix. One codebase. Database via ORM (Prisma/Drizzle). Auth = NextAuth/Clerk. Deploy to Vercel. No monorepo. No CI/CD. Manual testing.
- **What to skip**: Monorepo. Docker. Separate frontend/backend. Message queues. Redis. Microservices. E2E tests. Feature flags. Structured logging. Type sharing packages.
- **Coordination**: You own everything. Ship fast.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Monorepo (Turborepo) with shared types/validation. Fullstack framework (Next.js/Remix). CI/CD with lint + type-check + test + deploy. Database migrations in CI. Basic error handling. Structured logging. E2E test for critical flow. Feature flags for risky changes.
- **What to skip**: Separate frontend/backend services. Message queues (inline async is fine). Redis (unless caching needed). Multiple deployment targets.
- **Coordination**: PR review. API contract in shared types package. Weekly fullstack sync.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Monorepo with multiple apps/packages. Separate services for compute-heavy work. Message queues for async processing. Redis for caching. Full E2E test suite. Feature flags with gradual rollout. Error monitoring (Sentry). Observability with correlation IDs. Database migration rollback plans.
- **What to skip**: Microservices (>3 services). Kubernetes (Vercel/ECS is enough). Multi-region.
- **Coordination**: Weekly fullstack guild. Architecture RFC for new services. Cross-team type contract review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Platform team owning shared infra. Microservices for domain boundaries. Full observability (traces + metrics + logs). SLOs with error budgets. Canary deployments. A/B testing infrastructure. Feature flag platform (LaunchDarkly). Multi-region deployment. Compliance audit trails. Database sharding as needed.
- **What's full production**: Internal developer platform. Service catalog. Automated dependency updates. Contract testing. Developer experience metrics.
- **Coordination**: Platform team weekly. Architecture review board. Cross-team service contract sync. Quarterly capacity planning.

### Transition Triggers
- **Solo → Small**: Second fullstack developer. Monolith becomes hard to reason about for one person.
- **Small → Medium**: Need to separate concerns (compute-heavy work blocking request lifecycle). >1K req/s.
- **Medium → Enterprise**: 5+ teams in monorepo. Multi-region or compliance requirements. >10K req/s.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | idea-to-spec | Feature specification, user stories, acceptance criteria |
| **This** | fullstack-developer | End-to-end implementation: database schema, API routes, UI components, deployment config |
| **After** | code-reviewer | Reviews full-stack PR for correctness, security, and integration quality |

Common chains:
- **Idea to production**: idea-to-spec → fullstack-developer → code-reviewer — Spec defines the feature, fullstack builds it across all layers, reviewer validates
- **Architecture-driven feature**: system-architect → fullstack-developer → devops-engineer — Architecture defines system boundaries, fullstack implements within them, DevOps deploys

## Sub-Skills
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


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Module not found: Can't resolve '...'` | Missing dependency or incorrect import path | `npm install <package>` or fix import path |
| `TypeError: Cannot read properties of undefined` | Accessing property on null/undefined value | Add optional chaining (`?.`) or null check before access |
| `Connection refused` | Target service not running or wrong host/port | Check service status: `docker ps`; verify environment variables |
| `ECONNREFUSED` | Database server not running | `docker compose up -d db`; check connection string |
| `413 Payload Too Large` | Request body exceeds server limit | Increase `body-parser` limit or paginate the request |
| `port 3000 already in use` | Previous process still bound to port | `lsof -ti:3000 \| xargs kill` or use `PORT=3001` |
| `ETIMEDOUT` | Network connectivity issue or firewall | Check network: `ping <host>`; verify firewall rules |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Monorepo with shared types/validation package consumed by frontend and backend
- [ ] **[S2]**  All API responses typed end-to-end (tRPC, typed fetch, or generated client)
- [ ] **[S3]**  Authentication flow working across all layers (signup, login, session refresh, logout)
- [ ] **[S4]**  Authorization enforced on server for all protected operations
- [ ] **[S5]**  Form submissions validated on server with shared Zod schemas
- [ ] **[S6]**  Error states, loading states, and empty states handled on every data-dependent view
- [ ] **[S7]**  E2E test covering at least one critical flow (end-to-end: UI → API → DB → back)
- [ ] **[S8]**  Database migrations run automatically in CI/CD pipeline with backup step
- [ ] **[S9]**  Structured logging with correlation IDs spanning frontend requests through backend
- [ ] **[S10]**  Feature flags in place for gradual rollout of major features

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Turborepo Documentation](https://turbo.build/repo/docs)
- [tRPC Documentation](https://trpc.io/docs)
- [Next.js Full-Stack Patterns](https://nextjs.org/docs/app/building-your-application)
- [Prisma Documentation](https://www.prisma.io/docs)
- [TanStack Query](https://tanstack.com/query/latest)
- [Mock Service Worker](https://mswjs.io/)
- [Playwright Documentation](https://playwright.dev/)
- [Auth.js / NextAuth.js](https://authjs.dev/)
