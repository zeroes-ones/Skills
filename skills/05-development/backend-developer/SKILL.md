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

## When to Use

- You are building a new REST API or GraphQL service and need to choose the right language and framework
- You need to implement authentication (JWT, OAuth 2.0) and role-based access control (RBAC)
- You are designing a database schema, writing migrations, or optimizing queries for a relational database
- You need to add caching (in-memory, Redis, CDN) to improve API response times
- You are setting up async task processing with background jobs, message queues, and idempotency guarantees
- You need to implement structured logging, distributed tracing (OpenTelemetry), and health check endpoints
- You are preparing a service for production with rate limiting, graceful shutdown, and deployment checklists
- You need to add resilience patterns — circuit breakers, retries with backoff, graceful degradation

## Decision Trees

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

## Core Workflow

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

## Gotchas

- **Environment variables** are loaded differently in Docker vs. local — `process.env` vs. `os.environ` vs. dotenv priority order varies. Always log which env source is active on startup.
- **Database connection pools** default to 10 connections. Under load with async frameworks, this silently queues requests. Set pool size to `2 * CPU cores + 1` for sync, `(CPU cores * 2) + 1` for async.
- **JWT `exp` claim** is UNIX timestamp in seconds. Python's `datetime.timestamp()` returns float with microseconds. Truncate with `int(datetime.utcnow().timestamp())` or tokens will be rejected.
- **CORS preflight** (`OPTIONS`) requests don't carry auth headers. Your auth middleware must skip OPTIONS or every CORS request will 401.
- **Alembic/Drizzle/Knex migration ordering** depends on file timestamps, not logical dependency order. If two developers create migrations simultaneously, the merge may produce an ordering that breaks foreign keys.
- **Health check endpoints** that only return 200 mask dependency failures. The `/health` endpoint should ping the database, cache, and message queue — not just the web server.
- **`SELECT *` with ORMs** fetches all columns including large TEXT/BLOB fields. When the ORM generates the query from your model, it pulls every column unless you explicitly `.select()` or `columns=`.


## Verification

- [ ] Run `npm test` / `pytest` / `go test ./...` — all tests pass, no regressions
- [ ] Run linter: `eslint .` / `ruff check .` / `golangci-lint run` — zero new issues
- [ ] Run type checker: `tsc --noEmit` / `mypy .` — zero type errors
- [ ] Start the service and hit the health endpoint: `curl http://localhost:${PORT}/health` returns 200
- [ ] Verify all new endpoints have integration tests covering success, auth failure, validation error, and not-found cases


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

