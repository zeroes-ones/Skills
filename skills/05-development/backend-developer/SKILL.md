---
name: backend-developer
description: Multi-language backend development with Python/FastAPI, Node.js/Express, Go, REST APIs, JWT/OAuth authentication, database integration, caching strategies, async task processing, structured logging, and testing. Trigger: backend, FastAPI, Express, Go, JWT, OAuth, caching, async tasks, API development.
author: Sandeep Kumar Penchala
---

# Backend Developer

Build production-grade backend services with polyglot expertise across Python (FastAPI), Node.js (Express/Fastify), and Go. This is the internal playbook for FAANG-level backend engineering — every section contains concrete, actionable implementation patterns, not generic advice. Covers the full lifecycle: language selection with tradeoff matrices, API design with framework-specific patterns, authentication and authorization (JWT, OAuth 2.0, RBAC), database integration with ORMs and raw SQL, multi-level caching architecture, asynchronous task processing with idempotency guarantees, structured logging with OpenTelemetry tracing, resilience patterns (circuit breakers, retries, graceful degradation), and comprehensive testing.

## Decision Trees

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
```

## Core Workflow

### Phase 1: API Design
1. **Contract-first**: Design OpenAPI 3.1 spec before writing code. Share with frontend/mobile teams.
2. **Endpoints**: Resources (nouns), not actions (verbs). `GET /orders/{id}` not `GET /getOrder`.
3. **Pagination**: Cursor-based for large datasets. `?cursor=xxx&limit=50`. Avoid offset pagination beyond page 10.
4. **Error responses**: Consistent format: `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }`. Include request ID for tracing.
5. **Versioning**: URL prefix (`/v1/`) or header-based. Avoid query param versioning. Have a deprecation policy.

### Phase 2: Implementation
1. **Project structure**: Feature-based, not layer-based. `src/orders/` contains routes, service, repository, models together.
2. **Validation**: Validate at boundary (API layer). Use Pydantic (Python), Zod (Node.js), or `go-playground/validator` (Go). Reject invalid data early.
3. **Error handling**: Never expose stack traces. Use error codes. Log full error with context server-side. Return sanitized error to client.
4. **Database access**: Repository pattern. Never expose ORM models directly to API layer. Use Data Transfer Objects (DTOs).
5. **Async tasks**: Offload non-critical work to background jobs. Ensure idempotency (idempotency keys, deduplication).

### Phase 3: Testing
1. **Unit tests**: Business logic, validation, transformations. Mock external dependencies.
2. **Integration tests**: Database, cache, message queue. Use test containers or in-memory alternatives.
3. **Contract tests**: Verify API responses match OpenAPI spec. Catch breaking changes before deploy.
4. **Load tests**: k6 or Locust. Test at 2× expected peak QPS. Find bottlenecks before users do.

### Phase 4: Deployment Readiness
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

## Sub-Skills

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

- **API contract first**: Design the API before writing code. Share with consumers. Use OpenAPI.
- **Fail fast, fail loud**: Validate at boundaries. Invalid data should never reach business logic.
- **Idempotency for mutations**: Every POST/PUT/PATCH that affects state should be idempotent via idempotency keys.
- **Observability from day one**: Structured logging (JSON), request IDs on every log line, health checks.
- **Database per service** (if microservices): Never share databases across services. API is the contract.
- **Connection pooling**: Always pool database connections. Set statement timeout and idle-in-transaction timeout.
- **Migrate forward, rollback tested**: Every migration has a tested reversal. Expand-contract for zero-downtime schema changes.

## Production Checklist
- [ ] API documented with OpenAPI 3.1 spec — shared with consumers, validated in CI
- [ ] Authentication and authorization implemented — JWT validated, RBAC enforced, secrets managed
- [ ] Input validation on all endpoints — server-side, not client-side only
- [ ] Error responses consistent format with request IDs for tracing
- [ ] Database migrations versioned and backward-compatible with rollback plan
- [ ] Health checks: liveness (`/health`) and readiness (`/health/ready`) endpoints
- [ ] Structured logging with correlation IDs propagated across services
- [ ] Graceful shutdown handling SIGTERM with connection draining
- [ ] Rate limiting and throttling on public endpoints
- [ ] Integration tests on database, cache, and external service interactions
- [ ] Load tested at 2× expected peak QPS before production launch
- [ ] Monitoring: error rate, P95 latency, throughput, DB connection pool, queue depth

## References
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [12 Factor App](https://12factor.net/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [OpenTelemetry](https://opentelemetry.io/docs/)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/) — Andy Hunt & Dave Thomas
- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Martin Kleppmann

## Cross-Skill Coordination

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

