# Orchestra Platform — Backend Architecture

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Go | 1.22 |
| Internal RPC | gRPC (Protocol Buffers) | protobuf v3 |
| External API | REST + GraphQL via Next.js BFF | — |
| Primary Database | PostgreSQL (RDS Aurora) | 15.x |
| Cache | Redis (ElastiCache) | 7.x |
| Message Queue | RabbitMQ (Amazon MQ) | 3.12 |
| Object Storage | S3 | — |
| Service Mesh | Istio on EKS | 1.20 |

## Service Architecture

```
cmd/
  catalog-service/      # main.go entry point
  template-engine/
  plugin-registry/
  auth-service/
internal/
  catalog/              # domain logic (handlers, repository, models)
  templates/
  plugins/
  auth/
pkg/
  middleware/            # shared: request ID, logging, auth, rate limit, recovery
  telemetry/             # shared: OpenTelemetry spans, metrics, structured logging
  errors/                # shared: RFC 7807 problem details builder
config.yaml              # per-service configuration (loaded via Viper)
```

Every service follows this identical directory structure. A developer can open any service directory and immediately understand where to find things. The `pkg/` directory contains shared libraries versioned independently; services pin to specific versions via Go modules.

## Service Responsibilities

### catalog-service
- CRUD for services, teams, and organization metadata
- Full-text search via PostgreSQL `tsvector` with trigram indexes
- Ownership tracking (service → team → organization)
- CQRS: writes to PostgreSQL, read models cached in Redis

### template-engine
- Scaffolder that executes Backstage-compatible templates
- Execution sandbox: gVisor runtime, no network egress by default
- TTL-based execution timeout (default 10 minutes, configurable per template)
- Emits `template.execution.started`, `template.execution.completed`, `template.execution.failed` events

### plugin-registry
- CRUD for plugins (metadata, version, compatibility matrix)
- Plugin artifact storage in S3 with signed URLs for download
- Dependency resolution: "Plugin A v2.3 requires Backstage >=1.18"
- Plugin installation/uninstallation lifecycle events

### auth-service
- JWT verification and refresh-token rotation
- RBAC enforcement (org:admin, org:member, org:viewer)
- API key management (generation, revocation, scope validation)
- Delegates primary authentication to Auth0; acts as policy enforcement point

## Key Design Patterns

### Repository Pattern
Every service uses a repository interface for data access, with PostgreSQL and Redis implementations. This keeps domain logic testable (mock the interface) and allows swapping storage backends:

```go
type ServiceRepository interface {
    Create(ctx context.Context, svc *Service) error
    GetByID(ctx context.Context, id string) (*Service, error)
    Search(ctx context.Context, filter SearchFilter) ([]*Service, error)
    Update(ctx context.Context, svc *Service) error
    Delete(ctx context.Context, id string) error
}
```

### Circuit Breaker
All outbound calls (to other services, Auth0, Stripe) use `gobreaker` with default settings: 5 failures in 60 seconds opens the circuit; half-open after 30 seconds with a single trial request. Failed calls return degraded responses rather than crashing the caller.

### CQRS (Catalog Service)
The catalog uses Command Query Responsibility Segregation: writes go to PostgreSQL, and a background worker refreshes read-optimized views in Redis. This keeps `/v1/catalog/services?filter=` queries fast (<50ms p95) even as the catalog grows to thousands of services.

### Outbox Pattern
Instead of writing to the database and publishing to RabbitMQ in a single transaction (risking inconsistency), services write events to an `outbox` table in PostgreSQL. A separate relay process polls the outbox and publishes to RabbitMQ with at-least-once delivery guarantees.

## Middleware Pipeline

Every HTTP/gRPC request passes through a consistent middleware chain:

1. **Request ID** — UUID generated or propagated from `X-Request-ID` header
2. **Structured Logging** — All log entries include request ID, service name, and trace ID
3. **Authentication** — Extracts and validates JWT from `Authorization: Bearer` header
4. **Authorization** — Checks required scopes against user's roles
5. **Rate Limiting** — Token-bucket algorithm per user/API key
6. **Recovery** — Catches panics, logs stack traces, returns 500

## Health Checks

- `GET /health` — Lightweight liveness check. Returns `{"status": "ok"}` within 200ms. Must not depend on external services.
- `GET /ready` — Readiness check. Verifies database connectivity, Redis ping, and RabbitMQ channel status. Returns `{"status": "ok", "checks": {"postgres": "ok", "redis": "ok", "rabbitmq": "ok"}}` only if all dependencies are healthy.
