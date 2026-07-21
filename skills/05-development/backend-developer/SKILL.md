---
name: backend-developer
description: Multi-language backend development with Python/FastAPI, Node.js/Express, Go, REST APIs, JWT/OAuth authentication, database integration, caching strategies, async task processing, structured logging, and testing. Trigger: backend, FastAPI, Express, Go, JWT, OAuth, caching, async tasks, API development.
author: Sandeep Kumar Penchala
type: development
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - backend-developer
token_budget: 2835
output:
  type: "code"
  path_hint: "./"
---
# Backend Developer

Build production-grade backend services with polyglot expertise across Python (FastAPI), Node.js (Express/Fastify), and Go. This is the internal playbook for FAANG-level backend engineering — every section contains concrete, actionable implementation patterns, not generic advice. Covers the full lifecycle: language selection with tradeoff matrices, API design with framework-specific patterns, authentication and authorization (JWT, OAuth 2.0, RBAC), database integration with ORMs and raw SQL, multi-level caching architecture, asynchronous task processing with idempotency guarantees, structured logging with OpenTelemetry tracing, resilience patterns (circuit breakers, retries, graceful degradation), and comprehensive testing.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design a new REST API or GraphQL service → Jump to "Core Workflow" — Phase 1 (API Design)
├── Implement authentication (JWT, OAuth) or RBAC → Go to "Decision Trees" — then Phase 2
├── Optimize database queries or set up caching → Jump to "Decision Trees" — Caching Strategy
├── Handle errors, retries, and resilience patterns → Jump to "Best Practices" — idempotency & resilience
├── Set up a project from scratch → Jump to "Scale Depth" — pick your team size, follow the stack
├── Design the database schema → Invoke database-designer skill instead
├── Need deployment or infrastructure → Invoke devops-engineer skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never write code without understanding the data model.** Before implementing an endpoint, know the schema, relationships, and query patterns. Do not build API handlers against an unknown database.
- **Always handle errors explicitly.** Every external call (database, API, queue, file system) must have explicit error handling with appropriate status codes, logging, and fallback behavior. Do not let exceptions propagate to the client as 500s with stack traces.
- **Never trust client input.** Validate everything at the boundary — types, ranges, formats, sizes, and business rules. Do not pass request bodies directly to database queries or external services.
- **Always version your API contract.** Breaking changes need a new version or a migration window. Use deprecation headers (Sunset, Deprecation) before removal.
- **Admit what you don't know.** If you don't know the database schema, expected QPS, deployment environment, or auth provider, say so and ask before writing code.

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

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **Stack**: Python/FastAPI or Node.js/Express. Fastest path to working API.
- **Database**: SQLite for dev, managed Postgres (Render/Railway free tier) for prod.
- **Deploy**: Single server or PaaS (Railway, Render, Fly.io). Dockerfile + `git push`.
- **Skip**: Kubernetes, microservices, message queues, distributed tracing. All overkill.
- **Coordination**: None. You are the API designer, developer, and reviewer.

### Small Team (2-10 people, 100-10K users)
- **Add**: CI/CD pipeline (GitHub Actions), structured logging, basic monitoring (health checks + error alerts).
- **Database**: Managed Postgres with connection pooling (PgBouncer). Redis for caching and sessions.
- **API**: OpenAPI spec as contract between frontend and backend. API versioning policy.
- **Queue**: Redis or SQS for async tasks. Keep simple — one queue, one worker.
- **Skip**: Kubernetes (use PaaS or docker-compose), multi-service architecture, event sourcing.

### Medium Team (10-50 people, 10K-1M users)
- **Add**: Distributed tracing (OpenTelemetry), metrics dashboard (Grafana), SLO-based alerting.
- **Architecture**: Modular monolith or 2-3 services around clear bounded contexts.
- **Database**: Read replicas for read-heavy endpoints. Connection pooling per service.
- **Queue**: Dedicated message broker (RabbitMQ, SQS). Dead letter queues for failed jobs.
- **Testing**: Contract tests in CI. Load tests before major releases.

### Enterprise (50+ people, 1M+ users)
- **Architecture**: Microservices or service-oriented. Event-driven where appropriate.
- **Database**: Multi-region with sharding. Dedicated DBRE (Database Reliability Engineer).
- **Security**: API gateway with rate limiting, WAF, regular penetration testing.
- **Compliance**: SOC 2, GDPR, PCI DSS controls implemented. Audit logging everywhere.
- **Coordination**: Cross-team API governance. Shared infrastructure team.

### Transition Triggers
- Solo → Small: You're the bottleneck. Hire backend dev #2.
- Small → Medium: P95 latency > 200ms sustained. DB CPU > 60%. Team can't ship independently.
- Medium → Enterprise: 3+ teams need to coordinate per deploy. Compliance mandates separation of concerns.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | api-designer | OpenAPI specs, error models, pagination conventions, auth patterns |
| **This** | backend-developer | Implementation: routes, validation, business logic, database access, caching, async tasks |
| **After** | code-reviewer | Reviews code quality, security vulnerabilities, error handling completeness |

Common chains:
- **API to production**: api-designer → backend-developer → code-reviewer — API contract drives implementation, code review ensures quality before merge
- **Schema to service**: database-designer → backend-developer → qa-engineer — Schema defines data model, backend builds the service layer, QA validates behavior

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `api-design` | New service, new endpoint | Phase 1 |
| `auth-implementation` | Login, permissions, API keys | Decision Trees |
| `database-integration` | Schema design, queries, migrations | `database-designer` skill |
| `caching-strategy` | Performance optimization, scaling reads | Decision Trees |
| `async-processing` | Background jobs, webhooks, notifications | Phase 2 |
| `testing-strategy` | Test pyramid, contract testing | Phase 3 |
| `performance-tuning` | Latency issues, throughput bottlenecks | `performance-engineer` skill |
| `containerization` | Docker, deployment | Phase 4 |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **API contract first**: Design the API before writing code. Share with consumers. Use OpenAPI.
- **Fail fast, fail loud**: Validate at boundaries. Invalid data should never reach business logic.
- **Idempotency for mutations**: Every POST/PUT/PATCH that affects state should be idempotent via idempotency keys.
- **Observability from day one**: Structured logging (JSON), request IDs on every log line, health checks.
- **Database per service** (if microservices): Never share databases across services. API is the contract.
- **Connection pooling**: Always pool database connections. Set statement timeout and idle-in-transaction timeout.
- **Migrate forward, rollback tested**: Every migration has a tested reversal. Expand-contract for zero-downtime schema changes.


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
- [ ] **[S1]**  API documented with OpenAPI 3.1 spec — shared with consumers, validated in CI
- [ ] **[S2]**  Authentication and authorization implemented — JWT validated, RBAC enforced, secrets managed
- [ ] **[S3]**  Input validation on all endpoints — server-side, not client-side only
- [ ] **[S4]**  Error responses consistent format with request IDs for tracing
- [ ] **[S5]**  Database migrations versioned and backward-compatible with rollback plan
- [ ] **[S6]**  Health checks: liveness (`/health`) and readiness (`/health/ready`) endpoints
- [ ] **[S7]**  Structured logging with correlation IDs propagated across services
- [ ] **[S8]**  Graceful shutdown handling SIGTERM with connection draining
- [ ] **[S9]**  Rate limiting and throttling on public endpoints
- [ ] **[S10]**  Integration tests on database, cache, and external service interactions
- [ ] **[S11]**  Load tested at 2× expected peak QPS before production launch
- [ ] **[S12]**  Monitoring: error rate, P95 latency, throughput, DB connection pool, queue depth

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [12 Factor App](https://12factor.net/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [OpenTelemetry](https://opentelemetry.io/docs/)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/) — Andy Hunt & Dave Thomas
- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Martin Kleppmann

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Backend services are integration hubs — they connect databases, external APIs, frontends, and infrastructure. Proactive coordination prevents integration surprises.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Frontend Developer** | API contract changes, new endpoints | OpenAPI spec, field deprecation timeline, breaking change migration path |
| **Mobile Developer** | API changes affecting mobile clients | Same as frontend + rate limiting changes, push notification payload design |
| **Fullstack Developer** | Shared monorepo features, tRPC/GraphQL schema changes | Type definitions, validation schemas, middleware behavior |
| **Security Engineer** | Auth flows, PII handling, new dependencies | Auth implementation details, data classification, dependency inventory |
| **DevOps Engineer** | Infrastructure changes, CI/CD, secrets | Resource requirements (CPU/memory), health check endpoints, migration steps |
| **CI/CD Builder** | Pipeline design, deploy strategy | Build/test commands, environment variables, database migration scripts |
| **QA Engineer** | Test environments, API testing | Test data requirements, API test scenarios, mock service endpoints |
| **System Architect** | Service boundaries, data ownership | API design decisions, database schema changes, inter-service contracts |
| **Data Engineer** | Data produced/consumed, event schemas | Event payload schemas, data freshness SLAs, webhook endpoints |
| **Observability Engineer** | Instrumentation, SLOs | Metrics requirements, log format, trace context propagation, alert thresholds |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| API breaking change (field removal, type change) | Frontend, Mobile, Fullstack | Coordinated migration to avoid production errors |
| Database migration with locking/downtime | DevOps, CI/CD Builder, QA | Deploy sequencing, test environment updates |
| New external service dependency | Security Engineer, DevOps | Security review, network egress rules, secrets setup |
| Auth flow change (token format, session behavior) | Security Engineer, Frontend, Mobile | Auth integration testing across all clients |
| Performance degradation discovered | Observability Engineer, DevOps | Metrics review, incident readiness |
| New async job/task worker | DevOps, Data Engineer | Queue setup, monitoring, retry/dead-letter configuration |
| Schema change to shared event payloads | Data Engineer | Downstream pipeline compatibility |

### Escalation Path

```
Blocked by infrastructure? → DevOps Engineer → Cloud Architect
Auth/security concern? → Security Engineer → Compliance Officer
Data contract dispute? → System Architect → CTO Advisor
Cross-team dependency blocking? → System Architect → Project Manager
```

