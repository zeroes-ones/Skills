# Orchestra Platform — System Architecture

## C4 Container Diagram (Text)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Orchestra Platform                       │
│                                                                 │
│  ┌──────────┐     ┌──────────────┐     ┌───────────────────┐   │
│  │ Web App  │────▶│   BFF/API    │────▶│  Catalog Service  │   │
│  │ (React)  │     │  Gateway     │     │     (Go)          │   │
│  └──────────┘     │  (Next.js)   │     └────────┬──────────┘   │
│                   └──────┬───────┘              │              │
│                          │              ┌───────┴───────────┐   │
│                          │              │ Template Engine   │   │
│                          │              │     (Go)          │   │
│                          │              └───────┬───────────┘   │
│                          │              ┌───────┴───────────┐   │
│                          │              │ Plugin Registry   │   │
│                          │              │     (Go)          │   │
│                          │              └───────────────────┘   │
│                          │                                      │
│  ┌───────────────────────┼──────────────────────────────────┐   │
│  │              Data & Infrastructure Layer                 │   │
│  │                                                        │   │
│  │  ┌────────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │ PostgreSQL │  │  Redis   │  │ RabbitMQ │           │   │
│  │  │ (RDS       │  │(Elasti-  │  │ (MQ for  │           │   │
│  │  │  Aurora)   │  │  Cache)  │  │  events) │           │   │
│  │  └────────────┘  └──────────┘  └──────────┘           │   │
│  │                                                        │   │
│  │  ┌──────────┐  ┌──────────────────────────────┐       │   │
│  │  │  Auth0   │  │         S3 (Templates,       │       │   │
│  │  │ (Auth)   │  │       Plugin Artifacts)      │       │   │
│  │  └──────────┘  └──────────────────────────────┘       │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture Decision Records (ADRs)

### ADR-001: Microservices over Monolith

**Context:** The platform must support independent evolution of the catalog, template engine, and plugin registry.

**Decision:** We will deploy as independently-shippable microservices, each owning its own data store schema.

**Rationale:** Team autonomy (squads own services), independent scaling (template execution is CPU-intensive, catalog is read-heavy), and fault isolation. The BFF layer (Next.js) aggregates responses for the web client and handles cross-cutting concerns like auth.

**Trade-off:** Increased operational complexity (service mesh, distributed tracing). Accepted because of Istio and OpenTelemetry adoption from day one.

### ADR-002: PostgreSQL over MongoDB

**Context:** We need a primary database for the service catalog, user data, and billing records.

**Decision:** Use PostgreSQL (RDS Aurora) as the primary data store.

**Rationale:** The domain is inherently relational (services belong to teams, teams belong to organizations). ACID guarantees are essential for billing accuracy. PostgreSQL's JSONB column type accommodates semi-structured data when needed (e.g., service metadata).

**Trade-off:** Horizontal scaling requires read replicas and careful connection pooling (PgBouncer). Accepted; our scale projections do not require NoSQL horizontal write scaling within 3 years.

### ADR-003: REST + GraphQL Hybrid API

**Context:** Different consumers have different data-fetching needs.

**Decision:** REST (OpenAPI 3.1) for CRUD operations on services, templates, and plugins. GraphQL for catalog queries where consumers need flexible field selection (e.g., "give me all Go services owned by Team X with their last deploy timestamp").

**Rationale:** REST is simpler for writes and predictable operations. GraphQL eliminates over-fetching and N+1 query problems for complex read scenarios. The BFF gateway exposes both under a unified domain.

### ADR-004: Event-Driven with RabbitMQ

**Context:** Template execution is inherently asynchronous (can take minutes) and plugins need to react to platform events.

**Decision:** Use RabbitMQ for inter-service messaging. Core events include: `service.created`, `template.execution.completed`, `plugin.installed`, `plugin.uninstalled`.

**Rationale:** Decouples services for resilience — if the plugin registry is down, template execution still works. Enables future event-driven features (Slack notifications on service creation, webhooks for CI/CD). Dead-letter queues handle transient failures with exponential backoff.

### ADR-005: Istio Service Mesh

**Context:** Microservices require consistent traffic management, security, and observability.

**Decision:** Deploy Istio as the service mesh on EKS.

**Rationale:** mTLS for all inter-service communication without application code changes. Traffic shifting enables canary deployments (10% → 50% → 100%). Envoy sidecars provide uniform metrics (request rate, latency, error rate) without per-service instrumentation.

## Non-Functional Requirements

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Availability | 99.9% (43.8 min downtime/month max) | Uptime checks every 60s from 3 regions |
| Latency | p95 < 200ms for API reads | Datadog APM percentiles |
| Concurrency | 10,000 concurrent users | Load test with k6 before every release |
| Compliance | SOC 2 Type II within 12 months | Annual audit, continuous control monitoring |
| Recovery (RPO) | < 5 minutes (point-in-time recovery) | Aurora automated backups |
| Recovery (RTO) | < 1 hour (full regional failover) | Multi-AZ deployment, tested quarterly |
