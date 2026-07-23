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

## What Good Looks Like

> Types flow end-to-end from database schema through API contracts to UI props — the compiler catches mismatches before they reach production.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | idea-to-spec | Feature specification, user stories, acceptance criteria |
| **This** | fullstack-developer | End-to-end implementation: database schema, API routes, UI components, deployment config |
| **After** | code-reviewer | Reviews full-stack PR for correctness, security, and integration quality |

Common chains:
- **Idea to production**: idea-to-spec → fullstack-developer → code-reviewer — Spec defines the feature, fullstack builds it across all layers, reviewer validates
- **Architecture-driven feature**: system-architect → fullstack-developer → devops-engineer — Architecture defines system boundaries, fullstack implements within them, DevOps deploys

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

## Gotchas

- **Time zones across stack**: The browser sends local time in forms. Node.js `new Date()` parses as UTC. PostgreSQL `timestamp` stores without timezone, `timestamptz` normalizes to UTC. Always store UTC, convert only at display layer.
- **CSRF tokens** are validated by comparing the cookie value to the request header. If your cookie `SameSite` is `Lax` but your frontend is on a different subdomain, the cookie won't send on POST — silent 403s with no console error.
- **API response size**: Next.js `getServerSideProps` passes all returned data to the client as `__NEXT_DATA__`. If you return full database rows with 50 columns, every one ships to the browser — even unused columns.
- **Prisma/Drizzle relation queries** in a loop produce N+1 queries. `include` or `with` clauses batch the relation but only one level deep. Nested relations need explicit `.findMany()` with `where: { id: { in: [...] } }`.
- **Session store** (Redis, DB, memory): if you use in-memory sessions during development, every server restart logs everyone out. Tests that depend on session state fail intermittently when the session store is not shared across parallel test workers.
- **File uploads via `multipart/form-data`** bypass JSON body parsers. If your validation middleware assumes `req.body` is JSON, file upload endpoints will silently receive `{}` and pass validation on empty.

## Verification

- [ ] Run `npm test` / `pytest` across frontend AND backend — both pass independently
- [ ] Run `npm run build` for frontend — zero build errors
- [ ] Start full stack: `docker-compose up` or `npm run dev` — app starts, login works, CRUD flow works
- [ ] Run integration test that touches frontend → API → database → back: `npm run test:e2e`
- [ ] Check network tab: no 4xx or 5xx responses in normal flows
- [ ] Verify CORS configuration: frontend origin exactly matches API's `Access-Control-Allow-Origin`

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Negative Constraints**: See [negative-constraints.md](references/negative-constraints.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

