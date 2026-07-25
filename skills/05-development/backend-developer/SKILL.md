---
name: backend-developer
description: >
  Use when building REST APIs, implementing authentication, designing database schemas,
  writing server-side business logic, or debugging backend performance issues. Handles
  multi-language backend development (Python/FastAPI, Node.js/Express, Go) with JWT/OAuth
  authentication, database integration, caching strategies, async task processing, push
  notifications (APNs/FCM), WebSocket/SSE streaming, and structured logging. Do NOT use
  for frontend UI work, DevOps infrastructure provisioning, mobile development,
  or LLM pipeline engineering.
license: MIT
compatibility: requires-python-3.10-or-node-18-or-go-1.21
tags:
- backend
- api
- fastapi
- express
- go
- authentication
- database
- caching
- async
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 5000
chain:
  consumes_from:
  - algorithmic-trader
  - api-designer
  - code-reviewer
  - chaos-engineer
  - database-designer
  - documentation-engineer
  - engineering-manager
  - hipaa-technical-implementation
  - idea-to-spec
  - migration-architect
  - monorepo-manager
  - performance-engineer
  - platform-engineer
  - privacy-engineer
  - security-engineer
  - security-reviewer
  - staff-engineer
  - system-architect
  - tdd-guide
  feeds_into:
  - algorithmic-trader
  - api-designer
  - api-test-suite-builder
  - chaos-engineer
  - ci-cd-builder
  - clinical-informatics-specialist
  - code-reviewer
  - customer-support-engineer
  - data-engineer
  - database-designer
  - devops-engineer
  - devrel-advocate
  - docker-kubernetes
  - embedded-engineer
  - frontend-developer
  - fullstack-developer
  - hipaa-technical-implementation
  - llm-engineer
  - market-data-engineer
  - mobile-developer
  - monorepo-manager
  - observability-engineer
  - performance-engineer
  - privacy-engineer
  - qa-engineer
  - sales-engineer
  - security-reviewer
  - staff-engineer
  - tdd-guide
  - technical-writer
---
# Backend Developer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "I'll add error handling and validation after the happy path works — let's not slow down for edge cases." | Raw 500s and unsanitized request bodies are how you get paged at 2 AM. Every `req.body` that hits your database without validation is a data corruption incident waiting to happen. Error handling isn't polish — it's what separates a service from a time bomb. |
| "Idempotency keys and timeouts are enterprise overhead — our API gets maybe 100 requests a day." | Low traffic doesn't protect you from retries. A double-charged customer doesn't care about your QPS. One missing timeout on a database call can cascade into a full outage when the DB hiccups. These aren't scale problems — they're correctness problems that bite at any traffic level. |
| "I know the data model — let's just start writing endpoints and figure out the schema as we go." | Code written against an unknown schema is code you will rewrite. Every endpoint you build before defining relationships, constraints, and query patterns accumulates tech debt at $200+/hour of rework. The schema is the foundation — build on sand, and the walls collapse on first deploy. |
| "Breaking API changes are fine — we'll just update all the clients simultaneously." | Client updates are never simultaneous. Mobile apps update over days. Third-party integrations update never. One breaking change ships, and suddenly your support queue is full of "the app is broken" tickets. A deprecation window costs you a header — skipping it costs you trust. |
| "Kafka/Redis/Kubernetes would future-proof this — better to over-engineer now than migrate later." | Every infrastructure dependency you add is a production incident surface you now own. Resume-driven architecture — choosing tools for their names, not their necessity — is the #1 cause of 6-month rewrites. If you can't point to a measured bottleneck, you don't need the tool. |

Build production-grade backend services with polyglot expertise across Python (FastAPI), Node.js (Express/Fastify), and Go. This is the internal playbook for FAANG-level backend engineering — every section contains concrete, actionable implementation patterns, not generic advice. Covers the full lifecycle: language selection with tradeoff matrices, API design with framework-specific patterns, authentication and authorization (JWT, OAuth 2.0, RBAC), database integration with ORMs and raw SQL, multi-level caching architecture, asynchronous task processing with idempotency guarantees, structured logging with OpenTelemetry tracing, resilience patterns (circuit breakers, retries, graceful degradation), and comprehensive testing.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("package.json", "\"express\"")` OR `file_contains("requirements.txt", "fastapi\|flask\|django")` OR `file_exists("go.mod")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.sql", "CREATE TABLE\|ALTER TABLE")` OR `file_contains("prisma/schema.prisma", "model ")` | Invoke **database-designer** instead. You need schema design, not backend code. |
| A3 | `file_contains("docker-compose.yml\|Dockerfile", "nginx\|proxy\|load")` OR `file_exists("terraform/\|.github/workflows/deploy")` | Invoke **devops-engineer** instead. This is infrastructure work. |
| A4 | `file_exists("openapi.yaml\|openapi.json\|swagger.json")` AND `file_contains("*.yaml", "paths:\|/api/")` | Invoke **api-designer** instead. This is API contract work. |
| A5 | `file_exists("jest.config.*\|vitest.config.*\|cypress.config.*")` AND `file_contains("*.test.*", "describe\|it\(")` | Invoke **qa-engineer** instead. This is test strategy work. |
| A6 | `file_contains("package.json", "\"next\"\|\"react\"\|\"vue\"")` AND `file_contains("*.tsx\|*.jsx", "useState\|useEffect\|<template>")` | Invoke **frontend-developer** or **fullstack-developer** instead. |
| A7 | `file_contains("*", "JWT\|OAuth\|passport\|bcrypt\|@nestjs/passport")` | Jump to **Decision Trees** — Authentication Strategy. |
| A8 | `file_contains("*", "redis\|memcached\|cache\|CacheManager")` | Jump to **Decision Trees** — Caching Strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a new REST API or GraphQL service → Jump to "Core Workflow" — Phase 1 (API Design)
├── Implement authentication (JWT, OAuth) or RBAC → Go to "Decision Trees" — then Phase 2
├── Optimize database queries or set up caching → Jump to "Decision Trees" — Caching Strategy
├── Handle errors, retries, and resilience patterns → Jump to "Best Practices" — idempotency & resilience
├── Set up a project from scratch → Jump to "Scale Depth" — pick your team size, follow the stack
├── Need system architecture decisions → Invoke system-architect skill instead
├── Need security review of backend → Invoke security-reviewer skill instead
└── Not sure? → Describe the problem in plain language and I'll route you

```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to write code without the data model.** Do not produce a single line of endpoint code until you know the schema, relationships, and query patterns. | Trigger: user asks for API endpoint code AND `grep -rn "schema\|migration\|\.sql" --include="*.ts"` returns 0 results in the repo | STOP. Respond: "I need the data model first. Share your schema (Prisma, SQL, ORM models) or describe the entities and relationships. I won't write API code against an unknown database." |
| **R2** | **REFUSE to let exceptions propagate as raw 500s.** Every external call (database, API, queue, file system) MUST have explicit error handling with status codes, logging, and fallback behavior. | Trigger: generated code contains `fetch(` or `axios(` or `pool.query(` without `try/catch` or `.catch()` in the same function scope | STOP. Insert error boundary before proceeding. Add: `try { ... } catch (err) { logger.error({ err, requestId }, 'External call failed'); return res.status(502).json({ error: 'SERVICE_UNAVAILABLE', requestId }); }` |
| **R3** | **REFUSE to pass request bodies directly to database queries or external services.** Validate types, ranges, formats, sizes, and business rules at the boundary. | Trigger: generated code contains `db.query(req.body.` OR `db.insert(req.body)` OR `sql` with `${req.body` without prior Zod/Joi validation | STOP. Insert validation layer: `const schema = z.object({ ... }); const parsed = schema.safeParse(req.body); if (!parsed.success) return res.status(400).json(...)` |
| **R4** | **REFUSE to make breaking API changes without a deprecation window.** New major version OR migration path required. | Trigger: generated code removes a field from response type OR changes a route signature OR renames a query parameter | STOP. Add deprecation header (`Sunset`, `Deprecation`), keep old behavior for 1 version, document migration path. Breaking changes without deprecation are forbidden. |
| **R5** | **STOP and ASK when critical context is missing.** Do not assume database schema, expected QPS, deployment environment, or auth provider. | Trigger: generating code that references database queries, external services, auth, or deployment configs without explicit confirmation of those details in the conversation | STOP. Ask targeted questions: "What's your database? (Postgres/MySQL/Mongo). What's the expected QPS? What auth provider? (Auth0/Clerk/Proprietary). What's the deployment environment?" |
| **R6** | **DETECT and WARN about missing idempotency on write endpoints.** Every POST/PUT/PATCH/DELETE endpoint that changes state MUST have idempotency protection. | Trigger: generated code creates `router.post(` or `router.put(` or `router.delete(` handler without `Idempotency-Key` header check or `idempotency_key` field | WARN: Add comment `// TODO: Add idempotency key check before processing` and insert skeleton: `const idempotencyKey = req.headers['idempotency-key']; if (!idempotencyKey) return res.status(400).json({ error: 'MISSING_IDEMPOTENCY_KEY' });` |
| **R7** | **DETECT and WARN about external calls without timeouts.** Every HTTP call, database query, or gRPC request MUST have an explicit timeout < 10s. | Trigger: generated code contains `fetch(url)` or `axios(url)` or `grpc.Client()` without `timeout` parameter or `AbortSignal` | WARN: Add `timeout: 5000` or `AbortSignal.timeout(5000)`. External calls without timeouts become cascading failures under load. |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff. See `scripts/references/source-of-truth-anchoring.md` for the full anti-hallucination pattern." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent developers make things work. Masters make things **unbreakable under load.** The shift: stop thinking about code paths and start thinking about failure modes. For every endpoint, ask "what happens when 10,000 requests hit this simultaneously?" The database connection pool, the memory allocator, the garbage collector — these are your real constraints. Code you haven't load-tested is code you haven't finished.

### Cognitive Biases That Kill Backend Systems
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Premature optimization** | Adding Redis before measuring if Postgres is the bottleneck | Profile first. Optimization without a flame graph is superstition. |
| **Resume-driven development** | Choosing Kafka for a 100 msg/day queue or Kubernetes for a single service | Every infrastructure choice must solve a measured problem. If you can't point to the bottleneck, you don't need the tool. |
| **Abstraction addiction** | Wrapping every database query in a repository pattern "in case we switch databases" | You won't switch databases. Build abstractions around behavior, not storage. One good abstraction beats five premature ones. |

### What Backend Masters Know That Others Don't
- **Connection pool math is deterministic.** `pool_size = (expected_qps × avg_query_ms) / 1000`. If this exceeds your database's max_connections, you have a scaling problem before you write a line of code.
- **Idempotency is not a feature — it's insurance.** Every payment, order, and write endpoint needs an idempotency key. Retries without idempotency = duplicates. Every retry mechanism without idempotency is a bug.
- **Backpressure propagates.** A slow database makes slow APIs makes slow clients makes angry users. Every layer in the stack needs a timeout shorter than the layer above it. The database timeout must be shorter than the API timeout must be shorter than the client timeout.
- **Every refactor must remove dead code — not just reorganize it.** When you touch a module to refactor, actively hunt for unused routes, dead code paths, commented-out blocks, deprecated wrappers, and legacy compatibility shims. A refactor's diff should be net-negative in lines. Dead code left behind is a tax on every future reader.

### When to Break Your Own Rules
- **Skip the abstraction for one-off scripts.** A 50-line migration script doesn't need repository pattern, dependency injection, or a service layer. It needs to run once and be correct.
- **Use raw SQL when the ORM creates N+1 queries.** ORMs optimize for developer convenience, not query efficiency. When you see 500 queries in your logs for a single endpoint, drop to raw SQL. The ORM is a tool, not a religion.

## Operating at Different Levels

The same backend task produces fundamentally different output depending on the practitioner's level. Invoke this skill with your target level (or the level you want to grow toward) to calibrate depth and scope.

| Level | Backend Output Characteristics |
|---|---|
| **L1 — Apprentice** | Step-by-step implementation with explanations. Safe defaults. "Here's the route handler, here's why we use this pattern." |
| **L2 — Practitioner** | Production-ready implementation with tests, error handling, and edge cases covered. Independent execution. |
| **L3 — Senior** | API design with trade-off analysis, data model design, architectural decisions. Decision rationale included. System-level thinking. |
| **L4 — Staff** | API design standards for the org, cross-service patterns, architectural RFCs. "This is how all our services should handle auth/caching/errors." |
| **L5 — Principal** | Novel patterns that change how the industry thinks about backend design. Framework-level contributions. "Here's a new approach to this class of problem." |

**Usage**: Say "as an L3 backend developer, design the API for..." or "give me an L2 implementation of this endpoint" to calibrate the response. If no level is specified, defaults to **L2** (production-ready, independent execution).

### Solo Developer
- FastAPI or Express with SQLite/PostgreSQL — keep the stack simple
- Auto-generated OpenAPI docs at `/docs` for frontend handoff
- Environment variables in `.env`, validated on startup with Pydantic/Zod
- Background tasks via simple in-process queue (FastAPI `BackgroundTasks`, Bull)
- Health check endpoint only — no distributed tracing yet
- Migrations run manually before deploy: `alembic upgrade head`

### Small Team (2-5)
- Shared OpenAPI spec as source of truth, code-generated types for client/server
- Redis for caching and session storage, connection pooling with PgBouncer
- Structured logging with correlation IDs propagated via `X-Request-ID`
- Async task queue (Celery, BullMQ) with dead-letter queue and retry policies
- CI runs tests, linters, and OpenAPI validation on every PR
- Circuit breakers on all external service calls

### Medium Team (5-20)
- API gateway (Kong, Envoy) for auth, rate limiting, and routing
- Database read replicas with read/write split at the repository layer
- Distributed tracing with OpenTelemetry across all services
- Contract testing between services (Pact or schema-based)
- Feature flags for phased rollout and dark launches
- Automated canary deployments with health-based rollback

### Enterprise (20+)
- Multi-service architecture with dedicated service mesh (Istio, Linkerd)
- Centralized secrets management (Vault, AWS Secrets Manager) with rotation
- SLO-driven alerting: error budget burn rate alerts, p95 latency SLOs
- Chaos engineering: regular GameDays injecting latency, packet loss, node failure
- Compliance automation: PCI/HIPAA/SOC2 evidence collected in CI pipeline
- On-call rotation with runbooks, incident command, and blameless postmortems

## When to Use

- You are building a new REST API or GraphQL service and need to choose the right language and framework
- You need to implement authentication (JWT, OAuth 2.0) and role-based access control (RBAC)
- You are designing a database schema, writing migrations, or optimizing queries for a relational database
- You need to add caching (in-memory, Redis, CDN) to improve API response times
- You are setting up async task processing with background jobs, message queues, and idempotency guarantees
- You need to implement structured logging, distributed tracing (OpenTelemetry), and health check endpoints
- You are preparing a service for production with rate limiting, graceful shutdown, and deployment checklists
- You need to add resilience patterns — circuit breakers, retries with backoff, graceful degradation

## Decision Trees **(QUICK)**

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Language & Framework Selection

```
Startup/Small team, rapid prototyping?
├── YES → Python/FastAPI or Node.js/Express
│         Fastest dev speed, largest hiring pool, most libraries
└── NO → Performance-critical? (latency < 10ms, high concurrency)
    ├── YES → Go or Rust
    │         Go: simpler, great concurrency, fast compile
    │         Rust: maximum performance, memory safety, steep learning
    └── NO → Team already skilled in one? → Use what they know

Data-heavy with complex business logic? → Python/FastAPI
Real-time, WebSocket-heavy? → Go or Node.js
Enterprise, Java ecosystem? → Kotlin/Spring Boot

```

### Caching Strategy Decision Tree

```
Data freshness requirement?
├── < 1 second → In-memory cache (application-level, no network)
├── 1-60 seconds → Redis/Memcached (shared, TTL-based)
├── 1-60 minutes → Redis + CDN for static, DB query cache
└── > 1 hour → CDN, precomputed materialized views

Read:write ratio > 100:1? → Aggressive caching, denormalized reads
Read:write ratio < 10:1? → Minimal caching, focus on write performance

**What good looks like:** `curl http://localhost:8000/health` returns `{"status":"ok"}` within 200ms. OpenAPI spec renders at `/docs`. All endpoints respond within p95 < 200ms.

```

## Core Workflow **(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): API Design
1. **Contract-first**: Design OpenAPI 3.1 spec before writing code. Share with frontend/mobile teams.
2. **Endpoints**: Resources (nouns), not actions (verbs). `GET /orders/{id}` not `GET /getOrder`.
3. **Pagination**: Cursor-based for large datasets. `?cursor=xxx&limit=50`. Avoid offset pagination beyond page 10.
4. **Error responses**: Consistent format: `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }`. Include request ID for tracing.
5. **Versioning**: URL prefix (`/v1/`) or header-based. Avoid query param versioning. Have a deprecation policy.

### Phase 2 (~30 min): Implementation
<!-- DEEP: 10+min -->
1. **Project structure**: Feature-based, not layer-based. `src/orders/` contains routes, service, repository, models together.
2. **Validation**: Validate at boundary (API layer). Use Pydantic (Python), Zod (Node.js), or `go-playground/validator` (Go). Reject invalid data early.
3. **Error handling**: Never expose stack traces. Use error codes. Log full error with context server-side. Return sanitized error to client.
4. **Database access**: Repository pattern. Never expose ORM models directly to API layer. Use Data Transfer Objects (DTOs).
5. **Async tasks**: Offload non-critical work to background jobs. Ensure idempotency (idempotency keys, deduplication).

### Phase 3 (~20 min): Testing
1. **Unit tests**: Business logic, validation, transformations. Mock external dependencies.
2. **Integration tests**: Database, cache, message queue. Use test containers or in-memory alternatives.
3. **Contract tests**: Verify API responses match OpenAPI spec. Catch breaking changes before deploy.
4. **Load tests**: k6 or Locust. Test at 2× expected peak QPS. Find bottlenecks before users do.

### Phase 4 (~15 min): Deployment Readiness
1. **Health checks**: `/health` (liveness — is process alive), `/health/ready` (readiness — can serve traffic). Kubernetes uses both.
2. **Graceful shutdown**: Handle SIGTERM. Stop accepting new requests, drain in-flight requests, close DB connections.
3. **Migrations**: Run before deploy. Backward-compatible changes only. Rollback plan for every migration.
4. **Secrets**: Environment variables for config, secrets manager for credentials. Never in code or config files.

### Phase 5 (~20 min): Real-Time & Streaming

1. **Choose the right protocol**: WebSocket for bidirectional (chat, collaboration), SSE for server→client streaming (dashboards, logs), Polling for simple/legacy clients.

| Factor | WebSocket | SSE | Polling |
|--------|-----------|-----|---------|
| Direction | Bidirectional | Server→Client | Client→Server |
| Connection | Persistent | Persistent | Per-request |
| Reconnect | Manual | Auto (EventSource) | Built-in |
| Binary | Yes | No (text only) | Via HTTP |
| HTTP/2 Friendly | Re

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.


## Best Practices

1. **Design APIs contract-first with OpenAPI 3.1.** Share the spec with frontend/mobile teams before writing a single route handler. Use `openapi-generator` or `fastapi-codegen` to generate typed server stubs and client SDKs. The spec IS the source of truth — code that diverges from it creates integration bugs.

2. **Centralize error handling in middleware, not route handlers.** Every route handler should throw or return a domain error; middleware translates it to a consistent HTTP response envelope (`{ error: { code, message, details } }`). Never `res.status(500).json({ error: err.message })` inline — stack traces leak implementation details and error shape inconsistency forces frontend teams to write brittle parsing logic.

3. **Set explicit timeouts on every external call.** HTTP clients, database queries, cache operations — all need timeouts configured (e.g., 5s for DB queries, 10s for upstream HTTP). Unbounded waits during cascading failures exhaust connection pools and block health checks. Combine with circuit breakers (50% failure rate over 30s → open circuit) to prevent thundering-herd retries.

4. **Validate at the boundary, not in business logic.** Use Pydantic (FastAPI), Zod (Express/Hono), or `go-playground/validator` (Go) at the API layer to reject invalid data before it reaches services. Business logic should operate on validated, typed data. Never validate inside service functions — it mixes concerns and leads to duplicated validation across callers.

5. **Apply database query hygiene as a first-class practice.** Use parameterized queries always — never string-interpolate SQL. Explicitly `.select()` columns with ORMs to avoid `SELECT *` pulling large TEXT/BLOB columns. Set statement timeouts: `SET statement_timeout = '5s'` in PostgreSQL session config. Monitor slow queries with `pg_stat_statements` and set alerts on p95 > 100ms.

6. **Cache with intent, not as a band-aid.** Choose cache strategy by read:write ratio and staleness tolerance. Read-heavy (>100:1): aggressive Redis caching with TTL-based invalidation. Write-heavy (<10:1): skip caching, optimize write path. Always populate cache on read (cache-aside), never on write — write-triggered cache updates create inconsistency when the write succeeds but cache update fails.

7. **Implement structured logging with correlation IDs from day one.** Every log line must include `request_id`, `user_id` (if authenticated), and `service`. Propagate `request_id` via headers (`X-Request-ID`) to all downstream services. Use structured JSON logging (Pino for Node.js, `structlog` for Python, `zerolog` for Go) — never `console.log` string interpolation. PII redaction must be configured in the logging pipeline, not left to developer discipline.

8. **Design database migrations to be backward-compatible with the currently deployed code.** Add columns as nullable first; deploy code that writes to both old and new; deploy code that reads from new only; drop the old column in a follow-up migration. Never rename or drop a column in the same migration that adds its replacement. Rolling deployments guarantee old code + new schema will coexist for minutes.

9. **Use connection pooling appropriate to your runtime.** Async runtimes (Node.js event loop, Python asyncio, Go goroutines): pool size = `(CPU cores × 2) + 1`. Sync runtimes (WSGI, Rails): pool size = `2 × CPU cores + 1`. Serverless/lambda: use external poolers (PgBouncer, RDS Proxy) because connection count multiplies by concurrent invocations. Monitor pool utilization — >80% is a warning, >95% means requests are queuing.

10. **Graceful shutdown is not optional.** Handle SIGTERM: stop accepting new requests, drain in-flight requests (with a configurable deadline, e.g., 25s for a 30s Kubernetes `terminationGracePeriodSeconds`), close DB connections and message queue consumers. Liveness probes (`/health`) should return 200 until the process exits; readiness probes (`/health/ready`) should return 503 during draining so the load balancer stops routing new traffic.


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "backend-developer",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist **(STANDARD)**

Before any production deployment, verify ALL of:

1. `npm test` / `pytest` / `go test ./...` — all tests pass, no regressions
2. Linter zero issues: `eslint .` / `ruff check .` / `golangci-lint run`
3. Type checker: `tsc --noEmit` / `mypy .` — zero type errors
4. Health endpoints: `/health` returns 200 within 200ms, `/health/ready` checks DB + cache + queue
5. OpenAPI spec validates: `npx @redocly/cli lint openapi.yaml` — no breaking changes
6. Database migrations are backward-compatible: can old code run against new schema?
7. All external calls have timeouts configured (HTTP: 10s, DB: 5s, cache: 1s)
8. Circuit breakers tested: inject failure, verify open → half-open → closed cycle
9. Graceful shutdown tested: `kill -TERM $PID`, verify no dropped requests, connections drained
10. PII scan of logs: `grep -rE '[0-9]{3}-[0-9]{2}-[0-9]{4}'` or equivalent — zero sensitive data in plaintext
11. Rate limiting configured: per-endpoint limits match capacity plan, 429 response documented
12. Secrets: verified in secrets manager (not env vars, not code, not config files). Environment scan: `grep -r 'API_KEY|SECRET|PASSWORD' --include='*.env*'` returns empty
13. Alert rules configured: p95 latency >500ms, error rate >1%, DB pool utilization >80%, consumer lag >1000
14. Runbook exists for top 3 failure modes with step-by-step recovery and escalation contacts

## What Good Looks Like

> Every endpoint is contract-first, validated at the boundary, and fully documented. Authentication is airtight — JWTs validated, RBAC enforced, secrets never leaked.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | api-designer | OpenAPI specs, error models, pagination conventions, auth patterns |
| **This** | backend-developer | Implementation: routes, validation, business logic, database access, caching, async tasks |
| **After** | code-reviewer | Reviews code quality, security vulnerabilities, error handling completeness |

Common chains:
- **API to production**: api-designer → backend-developer → code-reviewer — API contract drives implementation, code review ensures quality before merge
- **Schema to service**: database-designer → backend-developer → qa-engineer — Schema defines data model, backend builds the service layer, QA validates behavior

## Deliberate Practice

<!-- DEEP: 10+min — how to improve, not just what to do -->

### The Backend Improvement Loop
1. **Profile under load** — Run `wrk` or `k6` at 2× expected peak QPS. Find the slowest endpoint.
2. **Flame graph the bottleneck** — Is it a missing index? N+1 query? Serialization overhead?
3. **Fix one thing** — Optimize the single biggest bottleneck. Re-profile. Did it move?
4. **Repeat monthly** — Systems degrade. Last month's profile is not this month's reality.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Build the same API in 3 different frameworks; compare ergonomics, performance, error handling | Monthly | Can articulate when to use FastAPI vs Express vs Go based on actual data |
| Competent → Expert | Design a system for 1000 QPS, then 10,000, then 100,000. Find the breaking point of your architecture | Quarterly | Can identify the bottleneck before writing code |
| Expert → Master | Contribute a performance fix to an open-source framework you use. Read 1000 lines of its source code | Quarterly | Understands why the framework works, not just how to use it |

### The One Thing
**Write a production service from scratch with zero frameworks every 6 months.** No FastAPI. No Express. Just the standard library and a database driver. You'll learn what your frameworks actually do, what abstractions are worth the cost, and where the real complexity lives. Framework fluency ≠ backend mastery.


## Error Recovery **(STANDARD)**

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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `api-designer` | OpenAPI 3.1 spec, auth scheme, rate limits, error codes, pagination conventions | Before implementing any endpoint; contract-first development |
| `database-designer` | ERD, schema DDL, indexing strategy, migration scripts, query performance baselines | Before implementing data access layer; schema changes |
| `system-architect` | Service boundaries, technology stack decisions, inter-service contracts, deployment topology | Before choosing framework/language or defining service boundaries |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `frontend-developer` | OpenAPI spec, type-safe SDK, error response formats, pagination conventions | Frontend builds against wrong API shapes — costly rework |
| `fullstack-developer` | API implementation, type definitions, validation schemas, middleware behavior | Fullstack features blocked on backend availability |
| `devops-engineer` | Resource requirements (CPU/memory), health check endpoints, migration steps, build commands | Infrastructure can't be provisioned or CI/CD can't be configured |
| `qa-engineer` | Test data requirements, API test scenarios, mock service endpoints, error response patterns | QA can't author integration tests without API implementation |
| `security-reviewer` | Auth implementation details, data classification, dependency inventory, API surface | Security review can't assess implementation without understanding the code |
| `mobile-developer` | API implementation with mobile-specific concerns (rate limiting, push notification payloads) | Mobile client development blocked on backend availability |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| API breaking change (field removal, type change) | Frontend, Mobile, Fullstack | Coordinated migration to avoid production errors |
| Database migration with locking/downtime | DevOps, CI/CD Builder, QA | Deploy sequencing, test environment updates |
| New external service dependency | Security Engineer, DevOps | Security review, network egress rules, secrets setup |
| Auth flow change (token format, session behavior) | Security Engineer, Frontend, Mobile | Auth integration testing across all clients |
| Performance degradation discovered | Observability Engineer, DevOps | Metrics review, incident readiness |

### Escalation Path

```
Blocked by infrastructure? → DevOps Engineer → Cloud Architect
Auth/security concern? → Security Engineer → Compliance Officer
Data contract dispute? → System Architect → CTO Advisor
Cross-team dependency blocking? → System Architect → Project Manager

```

## Proactive Triggers

| Trigger | Response |
|---------|----------|
| "WebSocket connections dropping after every deploy" | Implement connection draining: on SIGTERM, stop accepting new WebSocket connections (`server.close()` in ws), send close frames (code 1001) to existing clients with a `Retry-After` header equivalent, and wait for in-flight messages to complete before process exit. Add a readiness probe that returns 503 while draining so the load balancer stops routing new traffic. |
| "SSE clients getting 502 after exactly 60 seconds" | Proxy timeout is killing the stream. Configure `proxy_read_timeout 300s;` in nginx or increase the ALB idle timeout to 120s+. Send SSE keepalive comments (`: heartbeat\n\n`) every 15–30 seconds to prevent idle connection drops. Disable response buffering with `proxy_buffering off;` and set the `X-Accel-Buffering: no` response header from the application. |
| "Memory leak in production — WebSocket connections growing unbounded over days" | Set `MAX_CONNECTIONS` cap at server startup. Add idle timeout (5 min) that terminates inactive connections after two missed heartbeats. Implement per-user connection deduplication — reject new connections from the same user if one already exists. Monitor `wss.clients.size` in health checks and alert on growth trends. |
| "Broadcast to 50K connections causes event loop lag and request timeouts" | Shard connections across multiple processes/instances (1 per CPU core). Use Redis pub/sub for cross-instance fan-out. Batch broadcasts: accumulate 50ms of events, send once instead of per-message. Consider SSE instead of WebSocket for one-way broadcasts — lower overhead per connection, no per-frame ACK overhead. |
| "Client reconnects after 30s disconnect and misses events — data loss" | Assign monotonically increasing sequence numbers to each broadcast event. Store the last N events (e.g., 1,000) in a ring buffer per connection/channel. On reconnect, client sends `{ lastSeq: 42 }` and server replays events 43+. For disconnects longer than the ring buffer, fall back to a REST endpoint for historical data. |
| "WebSocket upgrade fails with 426/400 behind a proxy or load balancer" | Ensure the proxy forwards WebSocket upgrade headers. In nginx: `proxy_set_header Upgrade $http_upgrade;` and `proxy_set_header Connection "upgrade";`. In AWS ALB: the listener protocol must be HTTP/HTTPS (not HTTP/2, which doesn't support protocol upgrade). Verify the backend route matches the WebSocket path exactly. |
| "Zombie connections — server thinks 5K clients are connected, only 2K are actually reachable" | Implement application-level ping/pong heartbeat (30s interval, 2 missed pongs = terminate). TCP keepalive defaults to 2+ hours — always do application-level heartbeats. On the client side, use `EventSource` auto-reconnect (SSE) or implement exponential backoff reconnection with jitter (WebSocket). |
| "Fan-out broadcast storm — one incoming event triggers cascading broadcasts that amplify" | Rate-limit broadcasts per room/channel (e.g., max 10/sec). Use a debounce pattern: if the same event type fires within 100ms, coalesce into one broadcast. Attach a `broadcastId` UUID to each message and deduplicate at the receiving end. Never broadcast raw upstream events without sanitizing/aggregating first. |

## Anti-Patterns

### 1. No Database Connection Pooling
**What it looks like:** Every request opens a new database connection instead of reusing from a pool. Under 500 concurrent requests, the database connection limit (typically 100) is exhausted. New requests queue, time out, and cascade into 503 errors. Instead of fixing the pool, teams scale up the database tier.
**Cost:** $5,000-$50,000/month in unnecessary database scaling.
**Fix:** Configure connection pool size `(CPU cores × 2) + 1` for async frameworks. Use PgBouncer or RDS Proxy for serverless/lambda. Monitor pool utilization as a first-class metric with alerts at >80%.

### 2. Missing Request Timeouts
**What it looks like:** An upstream service or database call hangs indefinitely with no timeout. Threads accumulate, the event loop blocks, health checks fail. Load balancers mark instances unhealthy, traffic shifts to remaining instances which then also hang — cascading failure.
**Cost:** $10,000-$100,000 in cascading outages and lost transactions.
**Fix:** Set explicit timeouts on every external call (HTTP: 10s, DB: 5s, cache: 1s). Implement circuit breakers (>50% failures in 30s → open). Configure graceful shutdown with a maximum drain deadline.

### 3. Cross-Platform Environment Variable Loading
**What it looks like:** `process.env` vs. `os.environ` vs. dotenv priority order varies between Docker, local, and deployment platforms. A variable works locally but is absent in production with no startup error.
**Fix:** Always log which env source is active on startup. Use strict schema validation (Zod, Pydantic Settings, dotenv-safe) that fails fast on missing or malformed variables.

### 4. JWT Timestamp Precision Mismatch
**What it looks like:** JWT `exp` claim requires UNIX timestamp in seconds. Python's `datetime.timestamp()` returns float with microseconds. Tokens are rejected as expired when they shouldn't be.
**Fix:** Truncate with `int(datetime.utcnow().timestamp())`. Use `python-jose` or `PyJWT` which handle this automatically if you pass `datetime` objects.

### 5. CORS Preflight Breaking Auth
**What it looks like:** `OPTIONS` preflight requests don't carry auth headers. Auth middleware rejects them with 401, and the browser never sends the real POST/PUT/DELETE.
**Fix:** Auth middleware must skip `OPTIONS` requests. Return 200 with appropriate CORS headers for preflight. Test with `curl -X OPTIONS` from the frontend origin.

### 6. Migration Ordering by Timestamp
**What it looks like:** Alembic/Drizzle/Knex uses file timestamps for ordering. Two developers create migrations simultaneously — the merge produces an ordering that breaks foreign key constraints.
**Fix:** Review migration ordering after every merge. Use `alembic history` / `npx drizzle-kit check` to verify the chain. CI gate: run migrations against a fresh database before merge.

### 7. Shallow Health Checks
**What it looks like:** `/health` returns 200 even when the database is unreachable, Redis is down, or the message queue is disconnected. Load balancer routes traffic to a dead instance.
**Fix:** `/health` (liveness): is the process alive? Lightweight. `/health/ready` (readiness): ping DB, cache, and message queue. Return 503 on dependency failure so the load balancer stops routing traffic.

### 8. ORM `SELECT *` with Large Columns
**What it looks like:** ORMs generate `SELECT *` from model definitions, pulling every column including TEXT/BLOB fields. Query latency spikes as row width increases. Memory usage balloons for large text fields.
**Fix:** Explicitly `.select()` or `columns=` in every query. Audit with `EXPLAIN ANALYZE` on top-10 queries. Set `max_row_size` limits at the connection level.

### 9. PII in Plaintext Logs
**What it looks like:** `console.log(user)` or `logger.info({ body: req.body })` during debugging ships passwords, credit cards, and SSNs into CloudWatch/Datadog/ELK. Logs are accessible to every engineer with production access and discoverable in breach investigations.
**Cost:** $25,000-$500,000 in GDPR/CCPA fines, forensic audit costs, and customer notification.
**Fix:** PII redaction in the logging pipeline (pino-redact, logstash filter). Never log request bodies by default in production. Run automated scheduled scans for PII patterns in log storage.

### 10. Synchronous Long-Running Tasks in HTTP Handlers
**What it looks like:** File uploads, PDF generation, or bulk emails run inside the request handler for 30-120 seconds. All available workers are busy on long tasks. Health checks time out. Load balancer marks every instance unhealthy — traffic death spiral.
**Cost:** $10,000-$50,000 in production outages and lost in-flight transactions.
**Fix:** Offload any task >500ms to a background job queue (BullMQ, Celery, Sidekiq, SQS). Return `202 Accepted` with a `Location` header to a status-check URL. Configure web server timeouts and max request duration limits.

### 11. Backward-Incompatible Database Migrations
**What it looks like:** A migration drops or renames a column while old application code still runs in a rolling deployment. Instances reference the dropped column — which no longer exists — and error on every request touching that path.
**Cost:** $15,000-$75,000 in deployment outages, data corruption, and complex rollback procedures.
**Fix:** Add columns as nullable first. Deploy code that writes to both old and new. Deploy code that reads from new only. Drop old column in a follow-up migration. Never rename/drop a column in the same migration that adds its replacement.

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When backend services go wrong, they go wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Service responds instantly at 10 req/s, times out at 100 req/s — health checks fail, load balancer removes all instances | Connection pool exhausted because connections aren't returned after use. Every request opens a new connection, hits the pool limit, and blocks waiting. All workers are idle waiting for connections that never come | Set `pool.max = 20` and `pool.idleTimeoutMillis = 30000`. Audit every query path — every connection acquired must be released in a `finally` block. Add metrics on pool utilization: alert at >80% | Connection pools fail silently. Your app doesn't crash — it just waits forever. Pool exhaustion looks exactly like a deadlock in your monitoring dashboard |
| Cache stampede kills database at midnight UTC — every cache key expires simultaneously, all traffic hits the DB at once | All cache entries set with the same TTL from the same base time (e.g., all cached at deploy time with 86400s TTL). At expiry, 10K requests simultaneously compute and repopulate — database melts | Add random jitter to every TTL: `ttl = baseTTL * (0.8 + Math.random() * 0.4)`. Implement request coalescing: only one request recomputes while others wait. Use Redis `SET NX` for distributed lock on cache miss | Deterministic TTLs create synchronized thundering herds. One second of randomness in TTL distribution spreads the recompute load over hours instead of microseconds |
| All timestamps off by 5 hours in production, correct in development — billing dates, event logs, and audit trails are wrong | Server timezone is UTC, database connection uses local timezone, application code calls `new Date()` without offset. Development machine is in the same timezone as the DB — the bug is invisible locally | Store all timestamps as UTC in the database. Set `TZ=UTC` in the application environment. Use `DateTime.utcnow()` / `new Date().toISOString()` for all timestamps. Parse incoming timestamps with explicit timezone | Timezone bugs are Heisenbugs — they only reproduce when the server, database, and developer are in different timezones. UTC-everywhere is the only defense |
| SIGTERM causes 500 errors for in-flight requests — graceful shutdown is configured but requests are dropped mid-response | The process receives SIGTERM, stops accepting new connections, but doesn't wait for existing requests to complete. Load balancer hasn't deregistered the instance yet — new requests arrive and get refused while old ones are killed | In the shutdown handler: (1) stop accepting new connections, (2) `server.close()` with a 30s timeout, (3) `await Promise.allSettled(activeRequests)`, (4) close DB pools and exit. Set `terminationGracePeriodSeconds` in k8s to 5s longer than your longest expected request | Graceful shutdown isn't a boolean — it's a sequence. Every step in the sequence matters. If k8s sends SIGKILL before your handler finishes, you lose in-flight transactions |
| File descriptor leak — service runs fine for days, then `EMFILE: too many open files` crashes everything | HTTP keep-alive connections, database connections, or log file handles opened but never closed. Each leaked FD stays open until the process dies. After 1-2 weeks, the process hits the ulimit ceiling | Set `agent.keepAlive = true` with `maxSockets` limit. Audit every `fs.createReadStream` and `client.connect()` — each needs a corresponding close/destroy. Monitor `process._getActiveHandles().length` in health checks. Set `ulimit -n 65536` as a safety net, not a fix | File descriptor leaks are the stealthiest resource leak. No memory spike, no CPU spike — just a sudden crash after days of perfect operation. The only fix is auditing every resource acquisition path |
| Rate limiter blocks legitimate traffic from corporate proxies — entire offices can't access the API | Rate limiting by IP address when thousands of users share a single NAT gateway IP (office building, university, mobile carrier CG-NAT). The shared IP exceeds the limit while individual users are well under it | Rate limit by authenticated user ID as primary key, with IP as secondary fallback for unauthenticated endpoints. Add `X-Forwarded-For` trust for proxy headers. Use token bucket algorithm with per-key granularity | IP-based rate limiting is broken architecture for any service with authenticated users. Corporate NAT gateways, mobile carriers, and VPNs make IP addresses meaningless as user identifiers |

## Verification

- [ ] Run `npm test` / `pytest` / `go test ./...` — all tests pass, no regressions
- [ ] Run linter: `eslint .` / `ruff check .` / `golangci-lint run` — zero new issues
- [ ] Run type checker: `tsc --noEmit` / `mypy .` — zero type errors
- [ ] Start the service and hit the health endpoint: `curl <http://localhost:${PORT}/health`> returns 200
- [ ] Verify all new endpoints have integration tests covering success, auth failure, validation error, and not-found cases

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

