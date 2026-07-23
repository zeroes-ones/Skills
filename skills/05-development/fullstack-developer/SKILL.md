---
name: fullstack-developer
description: 'End-to-end feature delivery across frontend and backend, API consumption
  and design, database queries, authentication flows, monorepo patterns, deployment
  pipelines, and full-stack testing. Trigger: fullstack, full-stack, end-to-end, frontend-backend
  integration, monorepo, fullstack feature.'
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- fullstack-developer
token_budget: 4000
output:
  type: code
  path_hint: ./
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

| ❌ Anti-Pattern | ✅ Do This Instead |
|-----------------|---------------------|
| Duplicating Zod/validation schemas in frontend and backend — type drift inevitable, backend validation diverges from frontend within 3 sprints | Share schemas in a monorepo package (`packages/validators`). Import the same Zod schema in both frontend form validation AND backend API route. Run `tsc --noEmit` in CI to catch drift. If not using monorepo, publish as a versioned npm package |
| Using `useEffect` for data fetching — causes client-server waterfalls, flash-of-loading on every navigation, and doubled render cycles | Fetch data on the server: Next.js RSC, Remix loaders, tRPC server-side calls. For client-side mutations, use `useMutation` (TanStack Query), Server Actions, or `useFormState`. `useEffect` fetching is the #1 cause of poor LCP and unnecessary loading spinners |
| Building a separate REST API that the frontend calls over `fetch()` — no type safety, no contract enforcement, "works on my machine" API drift | Use tRPC (TypeScript end-to-end) or GraphQL with codegen for type-safe APIs. If REST is required, generate types from the OpenAPI spec using `openapi-typescript`. Never hand-write `fetch()` calls with string URLs and `as` casts — that's how 60% of production API bugs originate |
| Running database migrations as part of `npm run dev` or in the application startup — causes production outages when 5 pods start simultaneously and all try to run the same migration | Database migrations are a deployment concern, not an application concern: (1) Run migrations as a separate CI/CD step BEFORE the application deploys, (2) Use advisory locks (PostgreSQL `pg_advisory_lock`) so concurrent migration runs are safe, (3) Every migration must have a tested rollback script. The application should start with existing schema ASSERTIONS, not schema modifications |
| Mocking `fetch` or axios in unit tests instead of testing the real API integration — tests pass but production calls fail on auth headers, CORS, or response shape mismatch | Test the real integration: (1) unit tests for pure logic with Zod schemas, (2) integration tests that spin up the actual API (Vitest + Supertest or Playwright API testing), (3) E2E tests for the full browser→API→DB flow. Mocking the HTTP layer hides the 80% of bugs that live in the boundary between client and server |
| Shipping without correlation IDs or structured logging — "it works locally" becomes "nobody knows what happened in production" when 5 services are involved | Every request gets a `x-correlation-id` header at the entry point (API gateway or middleware). Pass it through every service and log it with every message. Structured logging: `logger.info({ correlationId, userId, action: 'order.created', orderId })`. Without this, debugging a distributed fullstack bug is archaeology, not engineering |
| Using the same database connection pool size for dev laptop (1 user) and production (10K concurrent) — production exhausts pool under load, requests queue, users see timeouts | Size connection pools per environment: dev=5, staging=10, production=(2 × CPU cores) + 1 for each service. Use PgBouncer for connection pooling in production if you have >10 backend instances. Monitor pool utilization: if >70%, add capacity before customers notice. The pool is a queue — when it's full, users wait |

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

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Frontend showed "Order placed" but backend never created the order — orders silently lost | Frontend validated the form, sent the POST, got a 200 and showed success. The backend API actually returned 202 Accepted, but the frontend treated any 2xx as success — the background job processing the order failed silently | Fix frontend to distinguish 200 from 202/201. Add end-to-end tracing with correlation IDs so the full flow (browser click → API → DB → background job) can be observed in a single trace. Implement webhook/status polling for async operations | **Every 2xx status code is not the same.** 200 = completed, 201 = created, 202 = accepted (async). Frontend must handle each differently. Async operations need a status endpoint or webhook — don't assume 202 means "done". An acknowledgment is not a confirmation |
| Browser reported CORS error on every API call — cross-origin request blocked | Fullstack app had frontend on `app.example.com` and API on `api.example.com`. Backend CORS config set `Access-Control-Allow-Origin` to `*` but also sent `Access-Control-Allow-Credentials: true` — browsers reject wildcard origin with credentials | Set explicit origin: `Access-Control-Allow-Origin: https://app.example.com`. Use an environment-specific origin list in backend config. Handle preflight (OPTIONS) requests correctly. Add CORS configuration to the deployment checklist | **CORS with credentials requires explicit origins, not wildcards.** `Access-Control-Allow-Origin: *` + `credentials: include` is rejected by all modern browsers. Configure CORS explicitly per environment. Test CORS in CI with a headless browser making cross-origin requests |
| Deploy passed CI but the staging site showed a 502 error for 30 minutes | Monorepo migration script ran before the database migration was complete — the new code expected a column that didn't exist yet | Sequence the deploy: run DB migration first, then deploy code that depends on the new schema. Use expand-contract pattern for schema changes (add nullable, deploy code, backfill, set NOT NULL, drop old). Add pre-deploy health checks | **Database and code deploys must be sequenced, not simultaneous.** Separating schema changes from code changes is the #1 zero-downtime deployment pattern. Run migrations before deploying the code that depends on them. Always have a rollback plan for migrations |
| User session expired every 10 minutes on iOS Safari, but worked fine on Chrome | Safari's ITP (Intelligent Tracking Prevention) blocks third-party cookies. The app used cookie-based auth from `api.example.com` for the SPA running on `app.example.com` | Switch to same-site cookie deployment: frontend and API on the same domain (`app.example.com` + `api.app.example.com`). Or use JWT stored in memory/localStorage and sent via `Authorization: Bearer` header instead of cookies | **Same-site cookies don't work across different domains on Safari.** Apple's ITP aggressively blocks cross-domain cookies. Deploy frontend and API on the same registered domain. If you must use separate domains, use token-based auth (Authorization header) instead of cookies |
| PR merged to main, CI passed, but production broke 24 hours later when a new user signed up | Only tested the feature with existing test data. The new user signup flow hit an unhandled edge case in the backend when `name` field was null (new user hadn't set a name yet) | Add null/undefined handling for every field the new user flow touches. Write integration tests using fresh (empty) state, not just pre-seeded data. Add fuzz testing for form inputs | **Test with fresh state, not just seeded data.** Integration tests that only run against pre-seeded data miss null-pointer and undefined-field edge cases. Every feature that creates new entities needs tests with empty initial state |


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
