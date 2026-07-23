---
name: fullstack-developer
description: >
  Use when delivering end-to-end features spanning frontend and backend, integrating
  APIs with UI layers, implementing full-stack authentication flows, working in TypeScript
  monorepos, or orchestrating deployment across all tiers. Handles database-to-UI
  feature delivery, shared type systems, API consumption patterns, and full-stack
  testing strategies. Do NOT use for pure frontend UI work, pure backend API development,
  infrastructure provisioning, or mobile app development.
author: Sandeep Kumar Penchala
license: MIT
type: development
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- fullstack
- typescript
- nextjs
- monorepo
- api-integration
- authentication
- postgresql
token_budget: 4000
chain:
  consumes_from:
  - api-designer
  - backend-developer
  - database-designer
  - frontend-developer
  - tdd-guide
  feeds_into:
  - api-test-suite-builder
  - devops-engineer
  - qa-engineer
  - security-reviewer
  - tdd-guide
---
# Fullstack Developer

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Deliver complete features across the entire stack — from database to UI. This skill covers end-to-end feature development: TypeScript monorepos with shared types, full-stack frameworks (Next.js, Remix, SvelteKit), API integration patterns, database access from server-side code, authentication flows spanning frontend and backend, deployment orchestration, and comprehensive testing across all layers.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("package.json", "\"next\"\|\"react\"\|\"vue\"")` AND `file_contains("package.json", "\"prisma\"\|\"drizzle\"\|\"@neondatabase\"")` OR `file_exists("src/app/api/\|src/pages/api/")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("package.json", "\"react\"\|\"vue\"\|\"next\"")` AND NOT `file_exists("src/app/api/\|src/pages/api/")` | Invoke **frontend-developer** instead. Pure frontend, no API layer present. |
| A3 | `file_contains("package.json", "\"express\"\|\"fastify\"")` AND NOT `file_exists("src/components/\|pages/")` | Invoke **backend-developer** instead. Pure backend, no UI layer present. |
| A4 | `file_exists("openapi.yaml\|openapi.json")` AND `file_contains("*.yaml", "paths:\|/api/")` | Invoke **api-designer** instead. This is API contract design work. |
| A5 | `file_contains("prisma/schema.prisma", "model\|datasource")` AND NOT `file_exists("src/app/\|src/pages/")` | Invoke **database-designer** instead. Schema design without fullstack context. |
| A6 | `file_contains("docker-compose.yml\|Dockerfile", "nginx\|deploy")` OR `file_exists(".github/workflows/deploy*")` | Invoke **devops-engineer** instead. This is infrastructure/deployment work. |
| A7 | `file_contains("*", "NEXTAUTH_SECRET\|@clerk\|lucia-auth\|@auth")` OR `file_contains("*", "JWT\|OAuth\|session")` | Jump to **Decision Trees** — Authentication Strategy. |
| A8 | `file_contains("*", "tRPC\|@trpc\|GraphQL\|@apollo\|typegraphql")` OR `file_contains("*.ts", "z.object\|zod")` | Jump to **Decision Trees** — API Integration Pattern. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

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
├── Need deep frontend patterns → Invoke frontend-developer skill instead
├── Need deep backend patterns → Invoke backend-developer skill instead
├── Need API contract design → Invoke api-designer skill instead
├── Need database schema design → Invoke database-designer skill instead
├── Need security review → Invoke security-reviewer skill instead
├── Need DevOps/deploy pipeline → Invoke devops-engineer skill instead
├── Need QA test strategy → Invoke qa-engineer skill instead
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

## The Expert's Mindset
<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent fullstack developers make the frontend work and the backend work. Masters understand that **the boundary between them is the product.** Every decision about where data lives, where validation runs, and where computation happens shapes user experience, performance, and maintainability. The fullstack advantage isn't doing both sides — it's knowing which side should own each responsibility.

### Cognitive Biases That Kill Fullstack Systems
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Frontend favoritism** | Putting business logic in the client "because it's faster" — until you need to reuse it in mobile, API, or batch jobs | Business logic belongs on the backend. The frontend is a presentation layer. If logic lives in the client, you will reimplement it for every new surface. |
| **Backend favoritism** | Designing the API around database tables instead of UI needs — forcing 5 round trips to render a single page | APIs serve use cases, not data models. A BFF (Backend-for-Frontend) that returns exactly what one screen needs beats a "pure" REST API that requires N+1 client fetches. |
| **Stack-blind optimization** | Optimizing the API to 12ms while the frontend takes 3 seconds to paint because nobody measured end-to-end | Measure user-visible latency: click-to-render, not just server response time. A 12ms API is meaningless if the client spends 2 seconds parsing the response. |

### What Fullstack Masters Know That Others Don't
- **Data ownership is not about the database — it's about the API contract.** Frontend owns UI state. Backend owns domain state. The API is the contract. Type generation from OpenAPI (frontend types from backend schema) eliminates an entire class of bugs.
- **Validation lives in three places for different reasons.** Database constraints (integrity), backend validation (security/business rules), frontend validation (UX). None replaces the others. Backend validation without database constraints means a bug in the API can corrupt data. Database constraints without backend validation means cryptic errors reach users.
- **The cost of crossing the network boundary is 1000× higher than crossing a function call.** Batch requests. Use GraphQL or BFF to fetch exactly what the screen needs in one round trip. Every additional API call adds 50-200ms of latency the user feels.
- **Every refactor must remove dead code across the whole stack.** When you refactor, hunt for unused API endpoints, stale database columns, dead frontend components, and abandoned feature flags. Fullstack refactoring means cleaning both sides — a cleaner backend and a zombie frontend component creates confusion for the next developer.

### When to Break Your Own Rules
- **Skip the API for internal tools.** An admin panel that queries the database directly (via a secure internal service) is faster to build and perfectly adequate for 5 internal users. Not every screen needs a REST API.
- **Put computation in the client when it's truly presentation-only.** Sorting a 200-row table, formatting dates, local search — the user's device can handle this faster than a round trip. Server-side rendering is not always the answer.

## Operating at Different Levels

Fullstack spans two disciplines, so level manifests in the sophistication of integration decisions — where to put logic, how to design the boundary, and how to optimize the whole.

| Level | Fullstack Output Characteristics |
|---|---|
| **L1 — Apprentice** | Implements features following established patterns. Learns the stack boundaries. "Here's the endpoint and the component that consumes it." |
| **L2 — Practitioner** | Delivers full features independently — database through UI. Handles errors at both layers. Solid integration quality. |
| **L3 — Senior** | Makes boundary decisions with explicit rationale: "This logic belongs in the API because..." Designs the data flow end-to-end. Trade-off analysis across the stack. |
| **L4 — Staff** | Defines fullstack patterns for the org: monorepo strategy, shared package architecture, API contract standards. "This is how all our features should connect frontend to backend." |
| **L5 — Principal** | Creates fullstack frameworks or methodologies adopted across the industry. "Here's a new way to think about the frontend-backend boundary." |

**Usage**: Say "as an L3 fullstack developer, design the data flow for..." Default: **L2** (production-ready, independent execution).

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
<!-- DEEP: 10+min -->
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

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Duplicating Zod/validation schemas in frontend and backend — type drift inevitable within 3 sprints | Share schemas in a monorepo package (`packages/validators`). Import the same Zod schema in both frontend form validation AND backend API route. | `grep -rn "z\.object\|z\.string\|z\.number" packages/ -l \| sort \| uniq -c \| awk '$1 > 1'` → finds duplicate schema definitions across packages | Pre-commit hook: `scripts/check-duplicate-schemas.sh` — fails if same schema name exists in both `apps/web` and `apps/api` |
| Using `useEffect` for data fetching — causes client-server waterfalls, flash-of-loading, doubled render cycles | Fetch data on the server: Next.js RSC, Remix loaders, tRPC server-side calls. For client-side mutations, use `useMutation`. | `grep -rn "useEffect.*fetch\|useEffect.*axios" --include="*.tsx" --include="*.jsx"` → finds fetch-in-effect patterns | eslint `no-restricted-syntax: [{selector: "CallExpression[callee.name='useEffect'][arguments.0.body.body]:has(CallExpression[callee.name='fetch'])", message: "Server-fetch in RSC/loader, not useEffect."}]` |
| Building a separate REST API with hand-written `fetch()` — no type safety, API drift, "works on my machine" | Use tRPC (TypeScript end-to-end) or GraphQL with codegen. If REST required, generate types from OpenAPI spec using `openapi-typescript`. | `grep -rn "as \w+\|as any" --include="*.tsx" src/ -l` → finds `as` casts on API responses (type-unsafe) | eslint `@typescript-eslint/no-unsafe-assignment: error` + `@typescript-eslint/no-unsafe-member-access: error` |
| Running database migrations in application startup — 5 pods start simultaneously, all run same migration | Run migrations as a separate CI/CD step BEFORE deploy. Use advisory locks. Every migration must have a tested rollback. | `grep -rn "migrate\|prisma migrate\|knex migrate" --include="*.ts" --include="*.js" src/` → finds migrations in app code | CI: run migrations as a dedicated job before deploy. `prisma migrate deploy --preview-feature` in pre-deploy step |
| Mocking `fetch` or axios in unit tests instead of testing real API integration — production fails on auth headers, CORS, response shape | Test the real integration: unit tests for pure logic, integration tests with real API (Vitest + Supertest), E2E for browser→API→DB. | `grep -rn "jest\.mock\|vi\.mock\|mock.*axios\|mock.*fetch" --include="*.test.*" --include="*.spec.*"` → finds HTTP mocking | eslint `jest/no-mocks-import: error` + CI: require at least 1 integration test per API route |
| Shipping without correlation IDs or structured logging — debugging distributed bugs is archaeology | Every request gets `x-correlation-id` at entry point. Pass through every service. Structured logging with `correlationId, userId, action`. | `grep -rn "correlationId\|x-correlation-id\|x-request-id" src/ --include="*.ts" -l \| wc -l` → 0 = no correlation ID | Template: copy `templates/correlation-middleware.ts` into every service. CI check: fail if no correlation middleware detected |
| Using same DB connection pool size for dev (1 user) and production (10K concurrent) — production exhausts pool, users see timeouts | Size pools per env: dev=5, staging=10, production=(2×CPU)+1. Use PgBouncer for >10 instances. Monitor pool utilization at >70%. | `grep -rn "connection_limit\|pool_size\|max_connections" --include="*.env*" --include="*.ts" \| wc -l` → 0 = no pool config | CI: `grep -rn "DATABASE_URL" --include="*.env*" -A 1 \| grep "pool"` — fail if pool settings not found |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `backend-developer` | API implementation, type definitions, validation schemas, middleware behavior | Before wiring frontend to backend; ensures data contract alignment |
| `frontend-developer` | Component APIs, design token alignment, state management conventions, UI patterns | Before building UI that consumes the full-stack; avoids duplication |
| `api-designer` | OpenAPI 3.1 spec, auth scheme, error codes, pagination conventions | Before integrating any API; contract-first approach |
| `database-designer` | ERD, schema DDL, indexing strategy, migration scripts, query performance baselines | Before implementing data access layer; schema must exist first |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `devops-engineer` | Full-stack build steps, environment variables, database migration in CI/CD, deploy configuration | DevOps can't build CI/CD pipeline without understanding the full stack |
| `qa-engineer` | Critical user paths end-to-end, test data seeding, API mocking strategy for error states | QA can't design integration tests without full-stack context |
| `security-reviewer` | Auth flows spanning client-server, session management approach, CSRF protection, input validation strategy | Security can't review auth without understanding client-to-server flow |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Database schema change requiring migration | Backend, DevOps, QA | Deployment sequencing, test environment reset, rollback plan |
| Auth flow redesign (new provider, session change) | Security Engineer, Frontend | Security review, cross-client impact assessment |
| Monorepo structure change | All developers in repo | Build pipeline impact, import path changes, local dev setup |
| Shared package breaking change | Backend, Frontend, Mobile | Version bump coordination, migration guide |
| Deployment blocking issue | DevOps | Rollback decision, hotfix path |

### Escalation Path

```
Database migration failure? → Database Designer → DevOps Engineer
Auth vulnerability discovered? → Security Engineer → CTO Advisor
Cross-service integration broken? → Backend Developer → System Architect
Deploy blocked (infra)? → DevOps Engineer → Cloud Architect
```

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| User describes "we'll share types between frontend and backend by just keeping them in sync manually" | Intervene: "Manual type sync is guaranteed to drift. Set up a monorepo with `packages/types` or use tRPC for automatic type inference from backend to frontend. Without this, every API change will silently break the frontend and you'll find out from Sentry, not TypeScript" | Manual type sync between frontend and backend is the #1 source of production TypeScript errors. One developer changes the API response shape, another's frontend breaks 3 days later in production. tRPC or shared Zod schemas eliminate this entire class of bugs at compile time |
| New fullstack feature being built without discussing the database migration first | Flag: "Database schema changes must be designed BEFORE the API and frontend: (1) What columns/tables are needed? (2) Is the migration reversible? (3) Does it require backfill? (4) Will it lock the table? Design the migration and review it with the database-designer before any frontend code is written" | Schema-first development prevents the "frontend built, API built, migration impossible" deadlock. Adding a NOT NULL column to a 10M-row table without a default and backfill strategy locks the table and causes a production outage. Schema design is the foundation — build it first |
| Developer writing inline `fetch('/api/users')` with no error handling, no loading state, no retry logic | Warn: "Every API call needs: (1) type-safe client (tRPC/TanStack Query), (2) loading state (skeleton, not spinner), (3) error state with retry button, (4) empty state, (5) success state. Raw fetch() with no states handles exactly 1 of 4 possible UI states. TanStack Query gives you all 4 for free" | Every network call has 4 states: loading, error, empty, success. Hand-writing fetch() means you'll forget one. TanStack Query enforces all 4 states are handled. A missing error state means the user sees a broken page — a missing empty state means "no results" shows as a loading spinner forever |
| Team building mobile and web clients that will consume the same backend but designing APIs optimized for web only | Alert: "Mobile clients have different constraints: (1) slower/less reliable networks — need smaller payloads and offline support, (2) battery concerns — minimize polling, (3) background state — push notifications for data changes. Design a BFF (Backend for Frontend) layer: one API for web (full responses, SSR-friendly), one for mobile (minimal payloads, delta sync). One-size API fits nobody" | Web and mobile have fundamentally different network, battery, and interaction patterns. A single API optimized for web (large payloads, polling, cookie auth) breaks on mobile (metered data, battery drain, no cookies in WebView). BFF pattern: each client gets its own optimized API gateway |
| Monorepo PR showing a new API endpoint but no corresponding OpenAPI spec update or type export | Block: "Every new or changed API endpoint must include: (1) OpenAPI spec update, (2) type export in shared package, (3) at least one integration test exercising the endpoint with real auth. Without this, the frontend team can't consume the endpoint and QA can't test it. The spec is the contract — update it before merge" | API endpoints without published contracts create an integration tax that compounds with every new feature. The frontend team discovers new endpoints by reading backend PRs. QA writes API tests from curl commands. The OpenAPI spec is the source of truth — if it's not updated, the endpoint effectively doesn't exist for consumers |
| Feature deployed but production error rate spikes because the frontend deployed before the backend API was ready | Flag: "Deploy order matters: (1) Database migrations (backward-compatible), (2) Backend (new endpoints, old endpoints unchanged), (3) Frontend (can now safely call new endpoints). Never deploy frontend first if it depends on a new API. Use feature flags: backend deploys new endpoint behind a flag, frontend deploys with the flag off, QA verifies end-to-end, then enable the flag" | Deployment ordering bugs are the most embarrassing production incidents — the button is there but clicking it returns 404. Feature flags decouple deployment from release: deploy code at any time, release features when ready. Without them, you're coordinating deployment timing across teams, which is a coordination failure, not a technical solution |
| No end-to-end test covering the critical user path (signup→create→purchase) — unit tests pass but the full flow is broken | Alert: "Unit tests can't catch: CORS misconfiguration, cookie SameSite issues, redirect chain breakage, CSRF token mismatch, database migration missing column, environment variable typo. One Playwright test covering signup→create→purchase catches all of these simultaneously. If you have zero E2E tests, write this one today" | The most expensive production bugs live in the gaps between layers — the exact gaps that unit tests don't cover. A single E2E test of the critical path catches bugs that would require 50+ unit tests across 5 services to surface. E2E tests are not optional for fullstack development; they are the only tests that verify the system works end-to-end |

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

## What Good Looks Like

> Types flow end-to-end from database schema through API contracts to UI props — the compiler catches mismatches before they reach production. Server Actions handle mutations with progressive enhancement, Zod validation at every boundary, and optimistic updates that reconcile seamlessly with server state. The monorepo builds predictably with Turborepo caching; shared packages stay in sync and a single `git push` deploys the full stack behind a preview URL. Playwright tests exercise real user flows across UI, API, and database, and distributed traces carry correlation IDs from browser click to database query. Features ship behind feature flags, roll out gradually, and roll back instantly — no downtime, no drama.

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


## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `CORS.*blocked\|Access-Control-Allow-Origin\|cross-origin.*blocked` + `grep -rn "origin.*\*\|credentials.*true" src/ --include="*.ts"` finds wildcard CORS with credentials | Browser blocked every API call — cross-origin request silently failed | `Access-Control-Allow-Origin: *` + `credentials: true` — browsers reject wildcard origin with credentials per Fetch Standard §3.2.5 | Set explicit origin: `origin: req.headers.origin`, validate against allowlist. Test CORS with `fetch` from actual frontend domain, not Postman | 1. Find wildcard origins: `grep -rn "origin.*['\"]\*['\"]" src/ -A 2 \| grep "credentials"` 2. Replace with `origin: ['https://app.example.com']` 3. Test: `curl -H "Origin: https://app.example.com" -I https://api.example.com/health` → must return `Access-Control-Allow-Origin: https://app.example.com` |
| `GET /api/.*502\|502 Bad Gateway` + `grep -rn "\.include\|\.select\|eager\|relations" src/ --include="*.ts" -c` returns 0 (no eager loading) | Deploy passed CI but staging showed 502 for 30 min — new code expected column that didn't exist | Monorepo migration ran before DB migration — code expected column that wasn't created yet | Sequence deploy: DB migration first, then code deploy. Use expand-contract pattern. Add pre-deploy health check that verifies schema | 1. Grep migration dependency: `grep -rn "ALTER TABLE\|ADD COLUMN" prisma/migrations/` 2. Verify CI runs migrations before deploy step 3. Add: `prisma migrate deploy` as pre-deploy job 4. Test: deploy migration-only first, verify app starts |
| `202 Accepted\|status.*202` + `grep -rn "res\.status(200)\|\.json.*success" src/ --include="*.ts"` finds frontend treating all 2xx as success | "Order placed" shown but order never created — orders silently lost | Frontend treated 202 Accepted as success; background job processing the order failed silently | Distinguish 200 vs 201 vs 202 in frontend. Add polling/webhook for async operations. Implement correlation-ID tracing end-to-end | 1. Find async endpoints: `grep -rn "202\|Accepted\|background\|queue" src/` 2. Add status polling: `useQuery(['order', id], () => fetch(...), { refetchInterval: 2000 })` 3. Add correlation ID to every request 4. Test: simulate background job failure, verify frontend shows error |
| `session.*expired\|401.*silent\|Safari.*logged.*out` + `grep -rn "domain.*example\|cookie.*domain" src/ --include="*.ts"` finds cross-domain cookie config | User session expired every 10 min on iOS Safari but worked on Chrome | Safari ITP blocks third-party cookies — app used cookie auth from `api.example.com` for SPA on `app.example.com` | Deploy on same registered domain (`app.example.com` + `api.app.example.com`) or use JWT via `Authorization: Bearer` header instead of cookies | 1. Check domain config: `grep -rn "cookie\|session" src/ -A 3 \| grep "domain"` 2. If cross-domain, migrate to same-site or token-based 3. Test: Playwright test on WebKit (Safari) verifying session persistence |
| `TypeError.*null\|undefined.*property` + `grep -rn "new.*user\|signup\|register" src/ --include="*.ts"` finds user creation without field handling | Production broke 24h later — new user signup crashed on null `name` field | Only tested with existing seeded data. New user flow had unhandled null edge case | Add null/undefined handling for every field. Write integration tests with fresh state, not just pre-seeded data | 1. Find signup handlers: `grep -rn "createUser\|signup\|register" src/ -A 10` 2. Verify every field handles null: `grep -rn "\.name\b" src/ \| grep -v "?"` 3. Test: create user with minimal fields → must succeed 4. Add fuzz testing for form inputs |
| `Error: ORM.*N\+1\|query took.*\d{4,}ms` + `grep -rn "\.findMany\|\.findAll" src/ --include="*.ts" -A 5 \| grep -v "include\|select"` | 2,400 queries for single page load — endpoint timed out at 30s | ORM lazy loading: `order.customer.name` triggered separate query per order. No `include` on Prisma query | Use `include` for all relations accessed in response. Enable query logging in dev. Add CI test: assert ≤ 5 queries per endpoint | 1. Enable logging: `log: ['query']` in Prisma client 2. Add `include: { customer: true, items: true }` 3. Test: `assert(prismaQueryCount <= 5)` 4. CI gate: fail if any endpoint issues > 10 queries |


## Production Checklist
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

## Negative Constraints
<!-- DEEP: 5min -- hard-gate rules. Violating any of these is a production incident waiting to happen. -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|--------------------|--------------------|--------------------|
| NC1 | **REFUSE to prefix server-side secrets with `NEXT_PUBLIC_`** — Next.js inlines all `NEXT_PUBLIC_*` env vars into the client JS bundle. This is how $47K in fraudulent charges happened. | `grep -rn "NEXT_PUBLIC_.*SECRET\|NEXT_PUBLIC_.*KEY\|NEXT_PUBLIC_.*TOKEN" --include="*.env*" --include="*.ts" --include="*.js" \| grep -c` → > 0 | BLOCK build. Rename to `*_SECRET_KEY` (no prefix). Run `trufflehog filesystem . --json --fail` in pre-commit. |
| NC2 | **REFUSE CORS `origin: '*'` with `credentials: true`** — all browsers silently reject this per Fetch Standard §3.2.5. The response is a network error with no console message. | `grep -rn "origin.*['\"]\*['\"]" src/ -A 2 \| grep "credentials.*true" \| grep -c` → > 0 | BLOCK merge. Replace with explicit origin allowlist and `credentials: true`. Test with actual cross-origin fetch, not Postman. |
| NC3 | **STOP running DB migrations in application startup** — when 5 pods start simultaneously, all run the same migration, causing race conditions and outages. | `grep -rn "migrate\|prisma migrate\|knex migrate" --include="*.ts" --include="*.js" src/ \| grep -v "scripts\|CI\|ci" \| grep -c` → > 0 | BLOCK merge. Move migrations to a dedicated CI pre-deploy job. Use advisory locks. Every migration must have a tested rollback. |
| NC4 | **DETECT and BLOCK ORM queries without `include`** — accessing relations without eager loading triggers N+1 queries. 200 orders × 3 relations = 600 extra queries, timing out at 30s. | `grep -rn "\.findMany\|\.findAll\|\.find(" src/ -A 5 \| grep -v "include\|select\|relations\|eager" \| grep -c` → > 0 | BLOCK PR. Add `include` for all relations accessed in the response. Enable query logging in dev. Add CI test: `assert(queryCount <= 5)`. |
| NC5 | **REFUSE to ship without correlation IDs** — debugging a distributed fullstack bug without correlation IDs is archaeology. Every request must carry `x-correlation-id` from browser through API to DB. | `grep -rn "x-correlation-id\|correlationId" src/ --include="*.ts" --include="*.tsx" -l \| wc -l` → 0 | BLOCK merge. Copy `templates/correlation-middleware.ts` into API middleware. Add `x-correlation-id` generation on the frontend. |
| NC6 | **STOP deploying code before running DB migrations** — new code expecting columns that don't exist causes 502 errors. DB and code must be sequenced. | CI YAML: verify `migrate` step runs BEFORE `deploy` step. `grep -rn "needs:\|depends_on" .github/workflows/deploy* \| grep -v "migrate" \| grep -c` → > 0 (deploy doesn't wait for migrate) | BLOCK deploy. Reorder CI pipeline: migration job → deploy job. Use expand-contract pattern for schema changes. |
| NC7 | **DETECT Zod schemas only in one layer** — schema drift between frontend and backend causes production validation bugs within 3 sprints. | `find apps/ -name "*.ts" -exec grep -l "z\.object" {} \; \| sort \| uniq -c \| awk '$1 < 2 {print $2}' \| wc -l` → > 0 (schemas in only one layer) | BLOCK PR. Extract schemas to shared `packages/validators/`. Import from both frontend and backend. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can build a CRUD app but don't know what happens when the database connection pool is empty — you assume "the cloud handles that" | You can open Chrome DevTools, trigger a user flow, trace the request through the Network tab → API route → database query log → back, and identify which layer adds the most latency — then fix it | Your fullstack app handles 1,000 concurrent users on a $20/month single VPS without error rates exceeding 0.1% — and you can explain exactly which bottlenecks you'd hit at 10,000 users |
| You store secrets in `.env.local` and copy them manually between environments — you've accidentally committed a `.env` file at least twice | You have a secrets management pipeline: secrets never touch developer machines, they're injected at runtime via Vault/Infisical/Doppler, and a pre-commit hook blocks any file containing `SECRET\|KEY\|TOKEN` | You define the secrets management standard for your org — developers push code, and secrets are automatically provisioned per-environment with automatic rotation every 90 days |
| You test your app by clicking through the happy path in Chrome and calling it done — "the error states will be handled later" | Your E2E tests cover the happy path, error path (API down), empty state (no data), and edge cases (long strings, special characters, concurrent requests) for every critical flow | You ship a feature on Friday at 5 PM and go camping for the weekend with no cell service — and no one pages you because the monitoring, alerts, and graceful degradation you built handle every failure mode |

**The Litmus Test:** Build an auth system from scratch — signup, login, session refresh, password reset, email verification — with NO frameworks (no NextAuth, no Auth0, no Clerk). You must handle: token storage (httpOnly cookie vs localStorage tradeoffs), CSRF protection, refresh token rotation with replay detection, and rate limiting. Deploy it on a $6/month VPS. If you reach for Auth0 because "it's too complicated," you don't understand what Auth0 is doing — and that's fine, but you're not L3.

## Deliberate Practice
<!-- DEEP: 10+min — how to improve, not just what you do -->

### The Fullstack Improvement Loop
1. **Trace one user flow end-to-end** — Click in browser → network request → API handler → database query → response → render. Measure each segment.
2. **Find the slowest link** — Is it the database query? Network waterfall? Client-side render? Bundle parse time?
3. **Optimize the bottleneck and re-measure end-to-end** — The only metric that matters is user-perceived latency: time from interaction to fully painted result.
4. **Repeat across different flows** — Login, search, checkout, dashboard. Each flow stresses different parts of the stack.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Build the same todo app with 3 different stacks (Next.js+Prisma, Remix+Drizzle, SvelteKit+SQLite). Compare DX, performance, bundle size | Monthly | Can articulate stack tradeoffs from actual data, not blog posts |
| Competent → Expert | Add a feature that requires changing the database schema, API contract, AND UI. Time yourself end-to-end. The goal: < 4 hours from idea to deployed | Monthly | Reduces friction — the fullstack advantage is speed of shipping a complete feature |
| Expert → Master | Delete your API and rebuild it with a different paradigm: REST → GraphQL, or REST → tRPC. Compare client code complexity, type safety, and latency | Quarterly | Understands that API paradigms are UX decisions, not architectural preferences |

### The One Thing
**Ship a complete feature — database schema change through UI — in under 2 hours every month.** Speed reveals bottlenecks in your tooling, your understanding, and your stack. If you can't ship a complete feature in 2 hours, something in your stack is too complex. Find it. Simplify it. Repeat.

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
