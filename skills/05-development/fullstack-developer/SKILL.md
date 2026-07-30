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
    - qa-engineer
    - security-reviewer
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
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "We'll define the API contract as we build — frontend and backend can evolve together." | Without a shared contract, integration fails at the boundary every time. Mismatched field names, missing properties, and type drift don't surface until runtime — and then both teams blame each other. Define the contract once (OpenAPI, typed DTOs, or GraphQL schema) and both sides build against truth. Skipping this step costs 40%+ of integration time in rework. |
| "This discount logic is simple — putting it on the frontend avoids an API call and feels faster." | Business logic on the client is a security hole, not an optimization. Anyone can modify your pricing in devtools before checkout. When you need that logic in mobile, admin panel, and batch jobs, you'll reimplement it 3 times — each with different bugs. Server-side is the single source of truth. |
| "Let's set this up as microservices from day one — we'll need to scale eventually." | Premature microservices create distributed system problems (network failures, data inconsistency, deployment complexity) before you have a working product. A monolith with clean boundaries ships in weeks. Microservices with 3-person team ship in months — if they ship at all. Scale when you have measured bottlenecks, not hypothetical ones. |
| "Unit tests on the frontend AND backend cover everything — integration tests are redundant." | The boundary is where 80% of fullstack bugs live: serialization mismatches, auth token handling, error response parsing. Isolated tests pass while the feature is broken. One cross-boundary integration test catches more real bugs than 50 unit tests on either side. |
| "Server-side validation can wait — the frontend already validates all inputs before sending." | Client-side validation is bypassable with a single `curl` command. Every form field that's only validated in the browser is an open door to your database. One malicious POST with crafted JSON can corrupt your data, bypass your business rules, or inject garbage that crashes your backend. Frontend validation is a UX convenience — backend validation is the lock on the door. |

Deliver complete features across the entire stack — from database to UI. This skill covers end-to-end feature development: TypeScript monorepos with shared types, full-stack frameworks (Next.js, Remix, SvelteKit), API integration patterns, database access from server-side code, authentication flows spanning frontend and backend, deployment orchestration, and comprehensive testing across all layers.

## Route the Request
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

These rules are non-negotiable constraints that detect fullstack mistakes before they are given. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE building both sides without a shared API contract | Trigger: User requests frontend AND backend work without providing or agreeing to an API contract — OpenAPI spec, GraphQL schema, typed DTOs, or shared TypeScript interfaces that both sides reference | STOP. Respond: "Frontend and backend must agree on the data shape before either writes code. Without a shared contract, integration will fail at the boundary. Define the API contract first: OpenAPI spec, GraphQL schema, or typed shared DTOs. Provide this and I'll build both sides against it." |
| R2 | REFUSE business logic or auth decisions on the frontend | Trigger: User proposes or generated code implements pricing calculations, discount rules, permission/role checks, or data validation as the sole enforcement point in client-side code | STOP. Respond: "Business rules must execute server-side: [specific logic]. The frontend is attacker-controlled territory — any logic there is a UX convenience, not a security boundary. Move pricing, auth decisions, and authoritative validation to the backend. Client-side checks are for user experience only." |
| R3 | DETECT premature infrastructure complexity | Trigger: User proposes microservices, message queues, Redis caching, event sourcing, or service mesh before a monolithic end-to-end feature exists with measured performance bottlenecks | STOP. Respond: "This adds infrastructure complexity before a working feature exists. Build the simplest end-to-end path first — monolithic deployment, single database, direct API calls. Profile to find the actual bottleneck, then add complexity exactly where the data shows it's needed." |
| R4 | REFUSE shipping without cross-boundary integration tests | Trigger: User claims a feature is complete with only isolated frontend unit tests AND isolated backend unit tests — no contract tests, API integration tests, or end-to-end tests across the boundary | STOP. Respond: "Isolated frontend tests + isolated backend tests ≠ a working feature. The boundary is where most bugs live: serialization mismatches, auth token handling, error response parsing. Add at minimum: contract tests against the API schema, and one end-to-end test exercising the full request flow." |
| R5 | DETECT secrets or credentials exposed to the client | Trigger: Generated frontend code contains API keys, database connection strings, JWT signing secrets, private tokens, or `NEXT_PUBLIC_`-prefixed variables that should remain server-only | STOP. Respond: "This code exposes a secret to the client: [specific value/variable]. Everything in client-side JavaScript is readable by every user via browser devtools. Move this to a server-side environment variable, API route handler, or backend-only config. The client gets only short-lived session tokens, never secrets." |
| R6 | DETECT validation gap — frontend-only with no server-side counterpart | Trigger: Generated code validates input (required fields, format, length) only on the frontend with no corresponding server-side validation for the same endpoint | STOP. Respond: "Validation exists on the frontend but not on the backend for: [specific field/endpoint]. Client-side validation is bypassable with a single `curl` command. Add server-side validation as the authoritative check — frontend validation is a UX convenience, not a security measure." |
| R7 | **ANCHOR to runtime versions before generating full-stack code.** Never generate Next.js/Remix/SvelteKit/Prisma/Drizzle API calls from training data alone — full-stack frameworks have tightly coupled frontend+backend APIs that both change between major versions. | Trigger: skill receives code-generation task involving full-stack framework APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect framework and ORM versions → anchor all API calls (both frontend and backend) to detected versions → if versions are newer than training cutoff, add // VERIFY: comments on framework-specific calls | STOP. Respond: "Detected: {framework}@{version}, {orm}@{version}. Anchoring all full-stack API calls to these versions. Frontend and backend must use the same version's APIs — version mismatch at the boundary is a common source of bugs. See `scripts/references/source-of-truth-anchoring.md`." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

Fullstack spans two disciplines, so level manifests in the sophistication of integration decisions — where to put logic, how to design the boundary, and how to optimize the whole.

| Level | Fullstack Output Characteristics |
|---|---|
| **L1 — Apprentice** | Implements features following established patterns. Learns the stack boundaries. "Here's the endpoint and the component that consumes it." |
| **L2 — Practitioner** | Delivers full features independently — database through UI. Handles errors at both layers. Solid integration quality. |
| **L3 — Senior** | Makes boundary decisions with explicit rationale: "This logic belongs in the API because..." Designs the data flow end-to-end. Trade-off analysis across the stack. |
| **L4 — Staff** | Defines fullstack patterns for the org: monorepo strategy, shared package architecture, API contract standards. "This is how all our features should connect frontend to backend." |
| **L5 — Principal** | Creates fullstack frameworks or methodologies adopted across the industry. "Here's a new way to think about the frontend-backend boundary." |

**Usage**: Say "as an L3 fullstack developer, design the data flow for..." Default: **L2** (production-ready, independent execution).

### Solo Developer
- Next.js with SQLite or PostgreSQL via Docker Compose — single codebase, single deploy
- tRPC for end-to-end type safety without code generation overhead
- Prisma or Drizzle for schema management with auto-generated migrations
- NextAuth.js for authentication with OAuth providers
- Vercel + Supabase/Neon for hosting — no infrastructure management
- Feature flags via environment variables, manual rollout

### Small Team (2-5)
- Monorepo with Turborepo: `/apps/web`, `/apps/api` (if separate), `/packages/shared`
- Shared Zod schemas in `packages/shared` — single source of truth for validation
- CI/CD with preview deployments, E2E tests on staging, automated migrations
- Redis for session store and cache, shared across all environments
- Structured logging with correlation IDs from browser to database
- Contract tests between frontend and API using shared schemas

### Medium Team (5-20)
- Multi-app monorepo with Nx or Turborepo, shared packages for UI, types, config, database
- API gateway for auth, rate limiting, routing across services
- Feature flags with LaunchDarkly or GrowthBook for phased rollout and A/B testing
- Distributed tracing with OpenTelemetry across frontend and all backend services
- Database read replicas with automated read/write split at repository layer
- Saga pattern for multi-service workflows with compensating transactions

### Enterprise (20+)
- Platform team maintaining internal fullstack framework, shared packages, and CI templates
- Micro-frontend architecture with module federation for independent team deployment
- SLO-driven reliability: error budget burn rate alerts, p95 latency tracked per endpoint
- Automated canary deployments with health-based rollback across all services
- Compliance automation (SOC2, GDPR) with audit trail from UI action to database write
- Chaos engineering: regular cross-stack failure injection (DB failover, API degradation, CDN outage)

## When to Use
<!-- STANDARD: 3min -->

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

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

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

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->

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
  Complete when: `pnpm dev` starts all apps without import errors, shared types resolve correctly in both frontend and backend IDEs.

### Phase 2 (~30 min): Full-Stack Feature Development
<!-- DEEP: 10+min -->
1. **Start from the database**: Design schema changes with Prisma/Drizzle migrations. Write seed data for the feature. Create repository functions with proper types.
2. **API layer**: Implement endpoint in server code (Next.js API routes, tRPC router, Express controller, or Server Actions). Apply validation with shared Zod schemas. Return typed responses.
3. **Frontend integration**: Call API with TanStack Query (client components) or direct fetch (server components). Handle loading, error, empty, and success states. Implement optimistic updates for mutations.
4. **End-to-end type safety**: tRPC for full type safety from DB to UI without code generation. Or use OpenAPI-generated client from shared spec.
5. **Authentication awareness**: Protected routes on both server (middleware) and client (redirect unauthenticated). Access session/user in API, pass to frontend via server components or API response.
  Complete when: A full CRUD flow works end-to-end — database write → API response → frontend render — with typed responses across the stack.

### Phase 3 (~20 min): Data Flow Patterns
1. **Server Components (Next.js App Router)**: Fetch data directly in Server Components — `async` components calling DB or internal APIs. No client-side waterfall.
2. **tRPC**: Define procedures (queries, mutations, subscriptions) in backend; import types directly in frontend. Auto-completion for inputs and outputs.
3. **REST with generated client**: OpenAPI spec → `openapi-typescript` + `openapi-fetch` for type-safe fetch wrapper. Share spec as workspace package.
4. **GraphQL**: Codegen from schema to generate typed hooks (`useQuery`, `useMutation`). Fragment colocation for component-level data requirements.
5. **Server Actions** (Next.js): Form mutations handled on server. Use `useFormState` + Zod validation. Revalidate affected paths with `revalidatePath`/`revalidateTag`.
  Complete when: At least one data flow pattern is wired end-to-end with type safety — no `any` types cross the frontend/backend boundary.

### Phase 4 (~15 min): Authentication Flows
1. **Credentials**: Email/password with bcrypt hashing. Session-based (Iron Session, express-session) or JWT. CSRF protection for cookie-based auth.
2. **OAuth/OIDC**: NextAuth.js/Auth.js for Next.js; Lucia for framework-agnostic. Configure multiple providers (Google, GitHub, enterprise SSO). Handle account linking.
3. **Session management**: HttpOnly, Secure, SameSite=Lax cookies. Session expiry with sliding expiration. Refresh token rotation with reuse detection (family-based).
4. **Authorization**: Role-based access control (RBAC) checked in middleware and API layer. Column-level or row-level security in database (PostgreSQL RLS) for multi-tenant apps.
5. **Protected page patterns**: Middleware redirect for unauthenticated requests. Loading state while session resolves. Graceful handling of expired sessions.
  Complete when: Login, session persistence, protected route redirect, and logout all work across frontend and backend. CSRF protection is active.

### Phase 5 (~25 min): Testing Across the Stack
1. **Database tests**: Integration tests with real PostgreSQL (testcontainers or Docker Compose). Apply migrations, seed data, run tests, rollback. Each test in its own transaction.
2. **API tests**: Supertest (Express) or `testClient` (Hono) or `request` (Next.js). Test status codes, response shape, error handling, auth checks.
3. **Frontend tests**: Vitest + Testing Library for components. Mock API responses with MSW (Mock Service Worker) for realistic network simulation.
4. **E2E tests**: Playwright with real backend (no mocking). Test critical flows: signup, login, core CRUD, checkout. Run against staging environment.
5. **Contract tests**: Verify frontend expectations match backend responses. Use shared Zod schemas as contract. Consider Pact for cross-team scenarios.
  Complete when: `npm test` passes across all layers (unit, integration, E2E) with real database and no mocked network in integration tests.

### Phase 6 (~25 min): Deployment & Observability
1. **Platform**: Vercel (Next.js, SvelteKit), Railway/Render (Docker), Fly.io (edge), AWS ECS/EKS (enterprise). Use Infrastructure as Code (Terraform/Pulumi).
2. **Environment parity**: Dev, Staging, Production environments identical except for scale. Use same Docker image promoted through environments.
3. **Database migrations in CI/CD**: Run migrations as part of deploy pipeline. Transactional migrations with rollback capability. Backup before migration.
4. **Observability**: OpenTelemetry for distributed tracing across frontend and backend. Structured logging with correlation IDs propagated through all layers. Frontend RUM (Real User Monitoring) with web-vitals.
5. **Feature flags**: LaunchDarkly, GrowthBook, or homegrown. Wrap new features; toggle per environment, user segment, or percentage rollout.
  Complete when: Staging deploy succeeds, database migrations run in pipeline, OpenTelemetry traces span from browser to database, and a feature flag gates the new feature.
  Complete when: All tests pass — unit, integration, and E2E with > 80% coverage on new code.
  Complete when: Accessibility audit passes — WCAG 2.1 AA compliance with automated and manual checks.

## Best Practices
<!-- STANDARD: 3min -->

1. **Share validation schemas as the single source of truth across the stack.** Define Zod/Yup schemas in a shared `packages/shared` monorepo package. Both the API layer and the frontend form import from the same schema file. If tRPC, the procedure input IS the validation. Never duplicate validation logic or regex patterns between client and server — the divergence creates bugs where client says "valid" but server rejects.

2. **Standardize on a consistent API response envelope.** Every endpoint returns `{ data: T, error?: { code: string, message: string }, meta?: { page, total } }`. Enforce with a shared response builder or middleware. Frontend error handling becomes a single `if (response.error)` check instead of per-endpoint conditional shape inspection. Type the envelope in shared types and import into both client and server.

3. **Design the database schema first, then the API contract, then the UI.** Fullstack means you own the data model. Start migrations in `packages/database`, write the repository layer, define the API surface, then build the UI that consumes it. Bottom-up design prevents the UI from dictating a suboptimal data model and ensures the database schema supports all required queries without N+1 workarounds.

4. **Use tRPC or end-to-end types for full-stack type safety without code generation.** tRPC propagates types from database queries through API procedures to the frontend — renaming a column in the schema produces a TypeScript error at every usage site. For REST, use OpenAPI-generated clients (`openapi-typescript` + `openapi-fetch`) from a shared spec. Type safety across the boundary catches mismatches at compile time, not in production.

5. **Hydration is a contract, not an afterthought.** Server-rendered HTML must match the client's first render exactly. Mismatches (dates formatted differently, `typeof window` checks in render, random values) cause React hydration errors that degrade to full client re-renders. Test hydration by building for production (Strict Mode doesn't catch all mismatches) and checking the browser console for "did not match" warnings.

6. **Keep the monorepo dependency graph strictly acyclic.** Apps depend on packages, never the reverse. A shared package importing from an app creates circular dependencies, breaks Turborepo caching, and makes CI pipelines non-deterministic. Enforce with ESLint rules (`import/no-restricted-paths`) that ban cross-boundary imports. Visualize the graph with `nx graph` or `turbo run build --graph`.

7. **Propagate correlation IDs from the browser to the database.** Generate a `x-request-id` in the browser on page load (or the server on SSR). Pass it through every API call, background job, and database query. Structured logging at every layer includes the correlation ID — tracing a user action from button click to database write becomes a single log query, not a cross-service forensic investigation.

8. **Authenticate at the edge, authorize at the data layer.** Middleware validates the session/JWT and rejects unauthenticated requests at the boundary. But authorization (can this user access this resource?) lives at the repository/service layer, not in middleware. Row-Level Security (RLS) in PostgreSQL for multi-tenant apps pushes authorization to the database where it can't be bypassed by a forgotten middleware check.

9. **Environment parity is a productivity multiplier.** Every developer runs the same Docker Compose stack as CI and staging. Database version, Node.js version, package manager version, OS-level dependencies — all pinned. "Works on my machine" is a configuration divergence bug, not an acceptable state. Validate config on startup with strict schema checking (Zod, convict) that fails fast on missing or malformed variables.

10. **Treat API response size as a client performance concern.** Next.js `getServerSideProps` serializes ALL returned data into `__NEXT_DATA__` in the HTML. Returning full database rows with 50 columns ships every unused column to the browser. Select only the fields the UI needs. Use `superjson` or sparse field sets (`?fields=id,name`) to keep the HTML payload lean — it affects First Contentful Paint directly.

## Error Recovery **(STANDARD)**
<!-- STANDARD: 3min -->

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---------|--------|-----|
| User describes "we'll share types between frontend and backend by just keeping them in sync manually" | Intervene: "Manual type sync is guaranteed to drift. Set up a monorepo with `packages/types` or use tRPC for automatic type inference from backend to frontend. Without this, every API change will silently break the frontend and you'll find out from Sentry, not TypeScript" | Manual type sync between frontend and backend is the #1 source of production TypeScript errors. One developer changes the API response shape, another's frontend breaks 3 days later in production. tRPC or shared Zod schemas eliminate this entire class of bugs at compile time |
| New fullstack feature being built without discussing the database migration first | Flag: "Database schema changes must be designed BEFORE the API and frontend: (1) What columns/tables are needed? (2) Is the migration reversible? (3) Does it require backfill? (4) Will it lock the table? Design the migration and review it with the database-designer before any frontend code is written" | Schema-first development prevents the "frontend built, API built, migration impossible" deadlock. Adding a NOT NULL column to a 10M-row table without a default and backfill strategy locks the table and causes a production outage. Schema design is the foundation — build it first |
| Developer writing inline `fetch('/api/users')` with no error handling, no loading state, no retry logic | Warn: "Every API call needs: (1) type-safe client (tRPC/TanStack Query), (2) loading state (skeleton, not spinner), (3) error state with retry button, (4) empty state, (5) success state. Raw fetch() with no states handles exactly 1 of 4 possible UI states. TanStack Query gives you all 4 for free" | Every network call has 4 states: loading, error, empty, success. Hand-writing fetch() means you'll forget one. TanStack Query enforces all 4 states are handled. A missing error state means the user sees a broken page — a missing empty state means "no results" shows as a loading spinner forever |
| Team building mobile and web clients that will consume the same backend but designing APIs optimized for web only | Alert: "Mobile clients have different constraints: (1) slower/less reliable networks — need smaller payloads and offline support, (2) battery concerns — minimize polling, (3) background state — push notifications for data changes. Design a BFF (Backend for Frontend) layer: one API for web (full responses, SSR-friendly), one for mobile (minimal payloads, delta sync). One-size API fits nobody" | Web and mobile have fundamentally different network, battery, and interaction patterns. A single API optimized for web (large payloads, polling, cookie auth) breaks on mobile (metered data, battery drain, no cookies in WebView). BFF pattern: each client gets its own optimized API gateway |
| Monorepo PR showing a new API endpoint but no corresponding OpenAPI spec update or type export | Block: "Every new or changed API endpoint must include: (1) OpenAPI spec update, (2) type export in shared package, (3) at least one integration test exercising the endpoint with real auth. Without this, the frontend team can't consume the endpoint and QA can't test it. The spec is the contract — update it before merge" | API endpoints without published contracts create an integration tax that compounds with every new feature. The frontend team discovers new endpoints by reading backend PRs. QA writes API tests from curl commands. The OpenAPI spec is the source of truth — if it's not updated, the endpoint effectively doesn't exist for consumers |
| Feature deployed but production error rate spikes because the frontend deployed before the backend API was ready | Flag: "Deploy order matters: (1) Database migrations (backward-compatible), (2) Backend (new endpoints, old endpoints unchanged), (3) Frontend (can now safely call new endpoints). Never deploy frontend first if it depends on a new API. Use feature flags: backend deploys new endpoint behind a flag, frontend deploys with the flag off, QA verifies end-to-end, then enable the flag" | Deployment ordering bugs are the most embarrassing production incidents — the button is there but clicking it returns 404. Feature flags decouple deployment from release: deploy code at any time, release features when ready. Without them, you're coordinating deployment timing across teams, which is a coordination failure, not a technical solution |
| No end-to-end test covering the critical user path (signup→create→purchase) — unit tests pass but the full flow is broken | Alert: "Unit tests can't catch: CORS misconfiguration, cookie SameSite issues, redirect chain breakage, CSRF token mismatch, database migration missing column, environment variable typo. One Playwright test covering signup→create→purchase catches all of these simultaneously. If you have zero E2E tests, write this one today" | The most expensive production bugs live in the gaps between layers — the exact gaps that unit tests don't cover. A single E2E test of the critical path catches bugs that would require 50+ unit tests across 5 services to surface. E2E tests are not optional for fullstack development; they are the only tests that verify the system works end-to-end |

## State Log
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist **(STANDARD)**
<!-- STANDARD: 3min -->

Before any production deployment, verify ALL of:

1. `npm test` / `pytest` — frontend and backend tests pass independently, E2E tests pass
2. `npm run build` — frontend builds with zero errors, backend compiles, migrations are valid
3. `npm run typecheck` — zero TypeScript errors across `apps/` and `packages/`
4. `npm run lint` — zero ESLint errors, no `server-only` violations in client code, no `NEXT_PUBLIC_` secrets
5. Shared validation schemas: all Zod/Yup schemas in `packages/shared`, imported by both client and server
6. API response envelope: every endpoint returns `{ data, error?, meta? }` — verified by contract test
7. Database migration tested against a clone of production: backward-compatible, rollback tested
8. Secrets audit: `grep -r 'NEXT_PUBLIC_' --include='*.ts*' | grep -v 'NEXT_PUBLIC_APP_URL\|NEXT_PUBLIC_API_URL'` returns only intentional public values
9. Environment config validated on startup: missing or malformed variables cause fast-fail, not runtime errors
10. Docker Compose parity: `docker-compose up` locally matches staging/production — same images, same versions
11. CORS configured: `Access-Control-Allow-Origin` matches frontend origin exactly, credentials enabled if using cookies
12. Correlation ID propagation verified: client → API → database trace shows unified `x-request-id`
13. Hydration tested: production build, zero "did not match" warnings in browser console on first load
14. Client bundle audited: `source-map-explorer` shows no server-only code, no duplicate dependencies, no accidental large imports
15. Runbook exists for top 3 cross-stack failure modes (DB unreachable, API down, auth provider outage)

## What Good Looks Like
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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

## Anti-Patterns
<!-- STANDARD: 3min -->

### 1. Duplicated Validation Logic
**What it looks like:** Zod schemas on the frontend, different Yup/Joi schemas on the backend, regex patterns that differ by one character. A field passes client validation, gets rejected by the server with an opaque error. Users see a green checkmark, submit, get "Invalid email," retype the same email three times, and abandon.
**Cost:** $15,000-$50,000/year in inconsistent validation bugs and abandoned forms.
**Fix:** Share validation schemas in `packages/shared`. Both client and server import from ONE source schema. tRPC makes this automatic — the procedure input IS the validation.

### 2. No API Response Envelope
**What it looks like:** Endpoints return `{ user: {...} }`, `{ data: {...} }`, `{ result: {...} }`, or `null` on error. Frontend error handling grows a maze of `if (res.user)`, `if (res.data)`, `if (!res.error)`. A new endpoint returning `{ item: {...} }` causes silent data loss.
**Cost:** $10,000-$30,000 in error handling complexity and silent bugs.
**Fix:** Standardize on `{ data: T, error?: { code, message }, meta?: { ... } }`. Enforce with shared response builder. Type the envelope in shared types.

### 3. Time Zone Confusion Across the Stack
**What it looks like:** The browser sends local time. Node.js `new Date()` parses as UTC. PostgreSQL `timestamp` stores without timezone, `timestamptz` normalizes to UTC. Dates drift by hours depending on which layer interprets them.
**Fix:** Store everything as UTC. Use `timestamptz` in PostgreSQL. Convert to local time only at the display layer. Use `date-fns-tz` or `Intl.DateTimeFormat` for formatting.

### 4. CSRF Token Subdomain Mismatch
**What it looks like:** Cookie `SameSite=Lax` but frontend is on a different subdomain from the API. The cookie doesn't send on POST — silent 403s with no console error.
**Fix:** Deploy frontend and API on the same domain (reverse proxy). Or use `SameSite=None; Secure` with explicit CORS configuration. Test cross-origin POST from the actual frontend origin.

### 5. Oversized API Responses in SSR
**What it looks like:** `getServerSideProps` returns full database rows with 50 columns. All of it serializes into `__NEXT_DATA__` in the HTML — every unused column ships to every browser. First Contentful Paint regresses proportionally.
**Fix:** Select only the fields the UI needs. Use sparse field sets (`?fields=id,name`). Return DTOs, not raw database rows. Audit with `curl | wc -c` on production page HTML.

### 6. N+1 Queries in ORM Relations
**What it looks like:** `include` or `with` clauses batch relations one level deep. Nested relations (user → posts → comments → author) hit the database once per parent row per level. A page showing 20 posts with comments generates 20 × 20 = 400 queries.
**Fix:** Use explicit `.findMany()` with `where: { id: { in: ids } }` for nested relations. Use DataLoader pattern for batching. Monitor query count with `pg_stat_statements` or Prisma query logging.

### 7. In-Memory Sessions in Development
**What it looks like:** Dev uses in-memory session store. Every server restart logs everyone out. Tests fail intermittently when parallel workers don't share session state.
**Fix:** Use Redis or database-backed sessions even in development (Docker Compose makes this trivial). Configure test session store to be shared across parallel workers.

### 8. multipart/form-data Bypasses JSON Validation
**What it looks like:** File upload endpoints use `multipart/form-data`. JSON body parsers skip these requests — `req.body` is `{}`. Validation middleware passes on empty body, and the handler receives no data.
**Fix:** Use dedicated multipart parsing middleware (multer, formidable, Busboy). Validate file fields separately from JSON fields. Test file upload endpoints with actual `FormData`.

### 9. Environment Configuration Divergence
**What it looks like:** `.env` in development, different connection strings in staging, different parameter names in production. "Works on my machine" debugging consumes days of team time.
**Cost:** $10,000-$40,000/year in environment-specific debugging and delayed deployments.
**Fix:** Single configuration library with strict schema validation (Zod + dotenv-safe). Fail fast on startup with clear error messages. Docker Compose locally mirrors staging/production configurations.

### 10. Partial Failures in Multi-Step Workflows
**What it looks like:** A checkout flow creates order → deducts inventory → charges payment → sends email. Email service is down, entire request returns 500, but payment was captured and inventory deducted. No compensating transaction.
**Cost:** $50,000-$500,000 in financial reconciliation, refunds, and lost trust.
**Fix:** Saga pattern — each step has a compensating action. Outbox pattern for at-least-once delivery of side effects. Idempotency keys on every state-changing operation. Monitor and alert on stuck sagas.

### 11. Server Secrets Leaked to Client Bundle
**What it looks like:** `NEXT_PUBLIC_` prefix or importing `@/lib/db` in a client component ships API keys and database credentials into the browser bundle. Anyone inspecting the page has database access bypassing all authorization.
**Cost:** $20,000-$200,000 in security breach response and credential rotation.
**Fix:** ESLint rules banning server imports in client code. `server-only` npm package for modules that must never resolve in the browser. `source-map-explorer` audit on production bundles. `NEXT_PUBLIC_` prefix only for intentional public values like app URL.

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When full-stack apps go wrong, they go wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| API works in development, returns CORS errors in production — frontend can't reach the backend | Development uses `localhost:3000` hitting `localhost:8080` — same origin. Production deploys frontend to `app.example.com` and API to `api.example.com` — different origins. Browser blocks cross-origin requests | Configure CORS on the backend: `Access-Control-Allow-Origin: https://app.example.com` (not `*`). Use `credentials: 'include'` on the frontend with `Access-Control-Allow-Credentials: true`. Test with the actual production domains, not localhost | CORS is a browser-enforced security boundary. It doesn't exist in `curl`, Postman, or server-to-server calls. The only way to catch CORS bugs is testing with a real browser pointed at production URLs |
| Authentication works on `example.com` but fails on `app.example.com` — session cookie not sent cross-subdomain | Session cookie set with default `SameSite=Lax` and no `Domain` attribute. The browser sends the cookie to `example.com` but not to `api.example.com`. Login succeeds, but every subsequent API call is unauthenticated | Set cookie with `Domain=.example.com` (leading dot) for cross-subdomain sharing. Set `SameSite=Lax` with `Secure=true` in production. For different domains entirely, use token-based auth (JWT in `Authorization` header) instead of cookies | Subdomains are different origins to the browser. Cookies don't flow between them unless you explicitly configure the Domain attribute. One missing `.` breaks authentication for every subdomain |
| Form submits twice — database has duplicate records, payment charged twice | Optimistic UI updates the state immediately AND the form submit handler fires on button click. User clicks Submit → state updates → re-render → button re-mounts → click event fires again on the new button | Disable the submit button after first click: `disabled={isSubmitting}`. Use `useTransition` or `useOptimistic` for server actions. Add idempotency keys to every mutation endpoint: send `X-Idempotency-Key` header, server deduplicates by key | Every submit button click can fire multiple times — double-click, keyboard + mouse, re-render re-trigger. Server-side idempotency is the only guarantee. Client-side disabling is a UX nicety, not a data integrity solution |
| SSR page renders, then disappears and re-renders — flash of unstyled content, layout shift, poor Core Web Vitals | The server renders the page, sends HTML, the client hydrates and immediately triggers a data fetch because the server didn't pass the data. The fetch updates state → re-render. The user sees: rendered → blank → rendered | Pass all page data via `getServerSideProps`/`loader` functions. Don't fetch the same data on the client that the server already fetched. Use React Query with `initialData` from server props. Use `dehydrate`/`hydrate` for cache transfer | SSR is wasted if the client immediately fetches the same data. The user pays the SSR cost (server time) AND the CSR cost (client fetch + render). Data must flow from server to client through the initial HTML payload |
| Frontend sends POST with `Content-Type: application/json`, backend receives empty body — `req.body` is `{}` | Express `express.json()` middleware is declared AFTER the route handler. Or body parser is configured with a size limit smaller than the payload. The middleware never processes the body before the handler runs | Declare `app.use(express.json({ limit: '1mb' }))` BEFORE all route definitions. Add request logging middleware that logs `req.body` to catch empty bodies. Use Zod/Yup validation that fails fast on missing fields with clear error messages | Middleware order is execution order. Express processes middleware sequentially — a body parser declared after routes will never run for those routes. This bug survives code review because the middleware is "in the file" |
| API version mismatch — frontend deployed with v2 schema, backend still serves v1. Production breaks, staging works | Frontend and backend deployments are not atomic. The CDN caches the new frontend bundle while the backend rollout is still in progress. For 2-3 minutes, users get v2 frontend talking to v1 backend | Version your API in the URL: `/api/v1/users` and `/api/v2/users`. Never deploy breaking changes without a new version. Backend must support N-1 version for the duration of the rollout. Use feature flags to decouple deploy from release | Deployments are not instantaneous. During a rolling deploy, some instances run old code and some run new code. Your API must handle both old and new clients for at least one deploy cycle |

## Gotchas
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Duplicating validation logic between frontend and backend — client says "valid" but server rejects | $20K-$60K in bug fixes and data integrity repairs | Share Zod/Yup schemas in a monorepo `packages/shared` package. Both API and forms import from the same schema. With tRPC, the procedure input IS the validation. |
| Hydration mismatch from `Date.now()` or `typeof window` checks in render — React re-renders entire page on client | $10K-$30K in performance debugging and Core Web Vitals regressions | Guard browser-only code with `useEffect` (client-only). Pass server data via `getServerSideProps`/`loader`. Build for production and check console for "did not match" warnings. |
| API version mismatch during rolling deploy — v2 frontend talks to v1 backend for 2-3 minutes | $25K-$75K in production incidents and rollback costs | Version API in URL: `/api/v1/` and `/api/v2/`. Backend must support N-1 version during rollout. Use feature flags to decouple deploy from release. |
| Mixing server state into client state management (Redux/Zustand) — cache synchronization bugs multiply | $15K-$50K in debugging stale-data bugs | Server state → TanStack Query/SWR. Form state → React Hook Form. Client ephemeral state → Zustand/Context. Never duplicate server data in client stores. |
| Deploying with `nodeIntegration: true` in Electron or missing CSP headers — XSS turns into RCE on user machines | $50K-$200K in security incident response and reputational damage | Set `contextIsolation: true`, `nodeIntegration: false`. Use Content-Security-Policy headers. Expose only needed APIs via `contextBridge`. Audit with `grep -rn 'nodeIntegration.*true'`. |

## Verification
<!-- STANDARD: 3min -->

- [ ] Run `npm test` / `pytest` across frontend AND backend — both pass independently
- [ ] Run `npm run build` for frontend — zero build errors
- [ ] Start full stack: `docker-compose up` or `npm run dev` — app starts, login works, CRUD flow works
- [ ] Run integration test that touches frontend → API → database → back: `npm run test:e2e`
- [ ] Check network tab: no 4xx or 5xx responses in normal flows
- [ ] Verify CORS configuration: frontend origin exactly matches API's `Access-Control-Allow-Origin`

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Negative Constraints**: See [negative-constraints.md](references/negative-constraints.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
