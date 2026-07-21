---
name: api-designer
description: REST, GraphQL, and gRPC API design with OpenAPI 3.1, versioning strategies, authentication, rate limiting, error handling, pagination, and SDK generation. Trigger: API design, OpenAPI, REST, GraphQL, gRPC, versioning, rate limiting, pagination, SDK.
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - api-designer
token_budget: 2064
output:
  type: "code"
  path_hint: "./"
---
# API Designer

Design production-grade APIs across REST, GraphQL, and gRPC paradigms. This skill covers full API lifecycle design: specification-first development with OpenAPI 3.1, consistent error modeling, authentication and authorization patterns, rate limiting, pagination strategies, versioning approaches, and developer experience (DX) including SDK generation and documentation.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing a new REST, GraphQL, or gRPC API from scratch
- Creating OpenAPI 3.1 specifications for existing or new APIs
- Deciding between API paradigms (REST, GraphQL, gRPC, WebSocket) for a use case
- Designing API versioning, deprecation, and migration strategies
- Implementing rate limiting, quotas, and throttling policies
- Standardizing error responses, pagination, filtering, and sorting conventions
- Generating SDKs, API reference documentation, or Postman collections from specs
- Reviewing API designs for consistency, security, and DX quality

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### REST vs GraphQL vs gRPC
```
                     ┌──────────────────────────┐
                     │ START: New API endpoint   │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Multiple client types with │
                    │ different data needs?      │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ GraphQL     │   │ Service-to-     │
                    │             │   │ service comms?  │
                    └─────────────┘   └────┬────────┬───┘
                                           │ YES    │ NO
                                      ┌────▼────┐ ┌▼──────┐
                                      │ gRPC    │ │ REST  │
                                      └─────────┘ └───────┘
```
**When to choose REST:** Public-facing CRUD APIs, >3 consumer types, need HTTP caching, team has REST experience. **When to choose GraphQL:** 3+ client platforms with divergent data needs, nested/relational data, over-fetching problem measured at >40% unused fields. **When to choose gRPC:** Internal microservices, >1000 req/s, need bidirectional streaming, polyglot service mesh.

### URL Path vs Header Versioning
```
                     ┌──────────────────────────┐
                     │ START: Breaking API       │
                     │ change required           │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Public API with external   │
                    │ third-party consumers?     │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ URL Path    │   │ Header or no    │
                    │ (/v1/,/v2/) │   │ versioning yet  │
                    └─────────────┘   └────────────────┘
```
**When to choose URL Path:** Public API, >100 consumers, need discoverability and caching by version. **When to choose Header:** Internal-only API, <10 consumers, want clean URLs, can mandate Accept header usage.

### Cursor vs Offset Pagination
```
                     ┌──────────────────────────┐
                     │ START: List endpoint      │
                     │ with >1000 items          │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Real-time data with        │
                    │ frequent inserts/deletes?  │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Cursor-based│   │ Offset is fine  │
                    │ (stable,     │   │ (simpler for    │
                    │  consistent) │   │ static datasets)│
                    └─────────────┘   └────────────────┘
```
**When to choose Cursor:** Data changes frequently (>10 writes/sec), need stable pagination during mutations, dataset >10K records. **When to choose Offset:** Static or slowly-changing data (<1 write/min), need jump-to-page-N UX, dataset <10K records, simpler client implementation acceptable.

### API Key vs OAuth2 vs JWT
```
                     ┌──────────────────────────┐
                     │ START: Auth mechanism     │
                     │ for API endpoints         │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ End-user context needed    │
                    │ (scoped access per user)?  │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ OAuth2 +    │   │ Machine-to-     │
                    │ OIDC        │   │ machine only?   │
                    └─────────────┘   └────┬────────┬───┘
                                           │ YES    │ NO
                                      ┌────▼────┐ ┌▼──────────┐
                                      │ API Key │ │ JWT (self- │
                                      │ (simple) │ │ contained) │
                                      └─────────┘ └────────────┘
```
**When to choose OAuth2:** User-facing APIs, delegated access, need refresh tokens and scope-based permissions. **When to choose API Key:** Server-to-server, <10 internal consumers, no user context needed, simplest integration. **When to choose JWT:** Stateless auth, distributed systems, need claims without token lookup, short-lived tokens (<15 min).

### Rate Limiting Tier Design
```
                     ┌──────────────────────────┐
                     │ START: Rate limit         │
                     │ per consumer              │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Revenue-generating API     │
                    │ with paid tiers?           │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Tiered: Free │   │ Flat per-IP:   │
                    │ 100/min, Pro │   │ 1000 req/min   │
                    │ 1000/min,    │   │ with burst 2x  │
                    │ Ent 10000/min│   └────────────────┘
                    └──────────────┘
```
**When to choose Tiered:** Monetized API, >3 consumer tiers, need overage billing integration. **When to choose Flat:** Internal API, <100 consumers, no billing complexity needed, simple protection against abuse.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): API Paradigm Selection
1. **REST**: CRUD-heavy, document/collection-oriented, wide client audience, caching needs (HTTP caching), simple data shapes. Use when you need cacheability, discoverability (HATEOAS), and broad compatibility.
2. **GraphQL**: Complex client-driven data fetching, multiple frontend clients, nested/relational data, over-fetching/under-fetching problems. Use when frontend teams need flexible queries.
3. **gRPC**: High-performance service-to-service, streaming (bidirectional), strongly-typed contracts, polyglot microservices. Use Protocol Buffers for internal service mesh.
4. **WebSocket/SSE**: Real-time push, live updates, collaborative features, streaming events to browsers.

### Phase 2 (~30 min): Specification-First Design
1. Write the OpenAPI 3.1 specification before implementation.
2. Define **paths** with clear resource naming: plural nouns (`/users`, `/orders`), nested for sub-resources (`/users/{id}/orders`), no verbs in URLs (except for non-CRUD actions like `/orders/{id}/cancel`).
3. Define **schemas** with complete property types, formats, constraints (minLength, pattern, enum), examples, and descriptions.
4. Define **responses** for all status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500) with consistent error body schema.
5. Add **security schemes** (Bearer JWT, OAuth2, API Key) and `security` requirements per operation.
6. Include `servers` with environment URLs, `tags` for grouping, `info` with version and contact.

### Phase 3 (~20 min): Consistency & Governance
1. **Error Schema** — Standardize on RFC 7807 Problem Details:
   ```json
   { "type": "https://api.example.com/errors/validation-error", "title": "Validation Error", "status": 422, "detail": "The 'email' field is required.", "instance": "/users/abc123", "errors": [{ "field": "email", "code": "required", "message": "Email is required" }] }
   ```
2. **Pagination** — Cursor-based (preferred for large/real-time datasets) or offset-based (simpler, acceptable for small datasets). Use envelope: `{ "data": [...], "pagination": { "cursor": "...", "hasMore": true } }`.
3. **Filtering & Sorting** — Query parameters: `?filter[status]=active&filter[createdAt][gte]=2024-01-01&sort=-createdAt&fields=id,name,email` (sparse fieldsets).
4. **Idempotency** — Require `Idempotency-Key` header for mutating operations (POST/PUT/PATCH/DELETE); return stored response for duplicate keys.

### Phase 4 (~15 min): Versioning & Lifecycle
1. **URL path versioning** (`/v1/users`) — explicit, simple, allows major breaking changes. Preferred for public APIs.
2. **Header versioning** (`Accept: application/vnd.api+json; version=1`) — cleaner URLs but harder to explore.
3. **Deprecation** — Use `Sunset` and `Deprecation` HTTP headers; emit `Deprecation` notice in API changelog at least 6 months before removal.
4. **Sunset policy**: vN supported for 12 months after vN+1 release.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `rest-design` | CRUD, resource-oriented APIs | This file — Phase 2: API Design |
| `graphql-design` | Flexible clients, mobile, complex data | This file — Phase 2 + schema design patterns |
| `grpc-design` | Service-to-service, high-performance | This file — Phase 2 + Protobuf patterns |
| `api-security` | Auth, rate limiting, threat protection | This file — Phase 3 + OAuth2/mTLS patterns |
| `api-versioning` | Evolution without breaking | This file — Phase 4 + Versioning Cost Analysis |
| `api-documentation` | Developer experience, SDK generation | This file — Phase 1: Spec-First Design |
| `api-testing` | Contract testing, integration | `references/` (create as needed) |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
API design is a social contract. The spec is the agreement, but coordination ensures that agreement holds — across teams, across services, and over time as the API evolves.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **System Architect** | New service boundaries, API style selection (REST/GraphQL/gRPC), cross-service contracts | Bounded contexts, communication patterns, API principles, versioning strategy |
| **Database Designer** | API endpoints that map to new data models, query complexity, N+1 risks | Access patterns, expected query volume, data shape, consistency vs. availability tradeoffs |
| **Frontend Developer** | API contract design, response shape, error format, pagination | Client needs (data requirements, latency tolerance, offline support), BFF patterns, GraphQL fragments |
| **Mobile Developer** | API design for mobile (bandwidth, battery, intermittent connectivity) | Response size optimization, partial responses, delta updates, push notification integration |
| **Security Engineer** | AuthN/AuthZ, rate limiting, data exposure, API threat surface | OAuth2/OIDC flow design, scope model, rate limit tiers, PII handling, audit logging |
| **QA / Test Engineer** | Contract testing, integration test design, API test automation | OpenAPI spec as test source of truth, expected behaviors, error scenarios, edge cases |
| **Documentation Engineer** | API reference generation, interactive explorer, developer portal | OpenAPI spec (source of truth), authentication setup guides, code samples, SDK generation |
| **DevOps / Platform Engineer** | API gateway configuration, deployment, monitoring, rate limiting at edge | API routing, WAF rules, DDoS protection, API key management, observability requirements |
| **Product Manager** | API-first features, public API launch, partner integration | API as product: developer experience, pricing tiers, SLA, deprecation policy |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Breaking API change proposed | All API consumers (internal + external), Product Manager, Documentation Engineer | Deprecation timeline, migration guide, versioning decision (new version vs. sunset) |
| New API endpoint or resource added | Documentation Engineer, Frontend/Mobile, QA | SDK regeneration, client implementation, contract test updates, docs update |
| API security vulnerability discovered (OWASP API Top 10) | Security Engineer, DevOps, All consumers | Severity assessment, mitigation timeline, communication plan |
| Rate limit or quota change | DevOps, Product Manager, External developer relations | Developer communication, billing implications, migration window |
| Auth model change (new scope, new grant type, new identity provider) | Security Engineer, Frontend/Mobile, External consumers | Implementation guide, migration instructions, deprecation warning |
| API performance degradation (p95 latency > 2x baseline) | System Architect, Database Designer, Performance Engineer | Root cause analysis, query optimization, caching strategy, architecture review |
| API version approaching EOL (end of life) | All consumers, Product Manager, Documentation Engineer | Sunet timeline, migration support, redirect/alias plan |

### Escalation Path

```
API breaking incident (auth bypass, data leak, API-wide outage)
  └── API Designer + Security Engineer + System Architect + DevOps. War room. Hotfix or rollback within hours.

Breaking API change needed for >50% of consumers
  └── API Designer + System Architect + Product Manager + affected team leads. New major version or extended deprecation.

Minor API addition or non-breaking change
  └── API Designer reviews, team implements. No escalation needed. Changelog and docs updated.
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Spec-first, not code-first**: OpenAPI spec is the source of truth; generate server stubs and client SDKs from it.
- **Naming consistency**: camelCase for JSON properties, kebab-case for headers and query params, UPPER_SNAKE for enum values.
- **Use HTTP semantics correctly**: GET (safe, idempotent), PUT (idempotent replace), PATCH (partial update), POST (create), DELETE (idempotent).
- **Rate limiting headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`.
- **HATEOAS links** where practical: include `_links` in responses for discoverability and self-documenting APIs.
- **SDK generation**: Use OpenAPI Generator or fern for multi-language SDKs; publish to package registries (npm, PyPI, Maven).
- **Contract testing**: Use Pact or Spring Cloud Contract to verify API compatibility between services.

## "Is REST Overkill?" Decision Tree

```
Need real-time bidirectional streaming?
├── YES → WebSocket/SSE. REST is wrong here.
└── NO → Multiple client types (web, mobile, third-party)?
    ├── NO and only 1-2 clients, simple CRUD → JSON-RPC is fine. REST adds ceremony.
    └── YES → Do clients need flexible, nested queries (avoid over-fetching)?
        ├── YES → GraphQL. REST N+1 problems will kill you.
        └── NO → Is this internal service-to-service?
            ├── YES → gRPC. Better performance, strongly typed, streaming.
            └── NO → REST. Use REST. It's the right choice.
```

### When to Use Simple JSON-RPC Instead of REST
```
POST /rpc  { "method": "createOrder", "params": {...}, "id": 1 }
```

| Scenario | REST | JSON-RPC |
|----------|------|----------|
| Internal microservices (2-5 services) | ❌ Overkill | ✅ Simple, fast |
| Single client (your own frontend) | ❌ Overkill | ✅ Sufficient |
| Actions/commands > resources | ❌ Verb-mapping pain | ✅ Natural |
| Small team (< 5 eng) | ❌ Too much ceremony | ✅ Ship faster |
| Public API or > 3 clients | ✅ Standard, cacheable | ❌ Not standard |

## Versioning Cost Analysis

| Strategy | Implementation Cost | Maintenance Cost | Breaking Change Cost |
|----------|-------------------|-----------------|---------------------|
| **No versioning** | $0 | $0 | Full rewrite of all clients |
| **URL path (/v1/)** | Low (routing config) | Medium (N active versions × server cost) | Low (old version still works) |
| **Header versioning** | Medium (custom middleware) | Medium | High (clients must update headers) |
| **Query param (?v=1)** | Low | Medium | Low |
| **Content negotiation** | High (Accept header parsing) | Medium | High |
| **API Gateway routing** | High (gateway infra) | Low (route per version in gateway) | Low |

**Recommended:** URL path versioning (`/v1/`) for public APIs. Sunset vN 12 months after vN+1 release. Never run >2 versions simultaneously (cost grows linearly).

### Versioning Anti-Patterns
- **Versioning too early:** < 100 API consumers → don't version. Just change the API and notify.
- **Versioning everything:** Version only when breaking backward compatibility. Non-breaking additions don't need v2.
- **Keeping v1 forever:** Cost of maintaining v1 = hosting + bug fixes + security patches + support. Set a sunset date.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: API = simple REST endpoints in your framework (FastAPI, Express). No OpenAPI spec (generate from code). No versioning. No pagination. No rate limiting. Auth = a simple API key or session cookie.
- **What to skip**: OpenAPI spec-first. GraphQL. gRPC. API versioning. Rate limiting. SDK generation. Pagination. Idempotency keys.
- **Coordination**: You own client + server. Change API whenever needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: OpenAPI 3.1 spec (code-first or spec-first). REST with proper HTTP semantics. Cursor-based pagination for large lists. Basic rate limiting (100 req/min per user). JWT authentication. Error responses follow RFC 7807. Health check endpoint. Interactive docs (Swagger UI).
- **What to skip**: GraphQL (REST is fine). gRPC (unless internal service-to-service). API versioning (<100 consumers). SDK generation (consumers read OpenAPI). Idempotency keys (add when payments involved).
- **Coordination**: API design review in eng sync. OpenAPI spec in shared repo. Breaking changes communicated in Slack.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Spec-first OpenAPI with code generation. API versioning (URL path). GraphQL for complex client needs. gRPC for internal service-to-service. Tiered rate limiting with headers. Idempotency keys for all mutating endpoints. SDK generation (TypeScript, Python, Go). API changelog + deprecation policy (6 months). API gateway for routing + auth.
- **What to skip**: gRPC-web (unless need streaming in browser). Full HATEOAS. Multiple API gateway layers.
- **Coordination**: API design RFC process. Monthly API review. Deprecation calendar published. SDK release coordination with consumers.

### Enterprise (50+ people, 1M+ users)
- **What changes**: API platform team. Multi-protocol (REST + GraphQL + gRPC + WebSocket). API gateway with developer portal. API analytics (usage, latency, errors per consumer). Rate limiting with dynamic quotas. API versioning with automated migration tooling. SDKs for 5+ languages with CI/CD. API style guide. API linting in CI (Spectral). Contract testing (Pact). API product management.
- **What's full production**: API platform as a product. Developer portal with onboarding. API analytics dashboard. Automated breaking change detection. API consumer communication pipeline.
- **Coordination**: API platform team weekly. API design review board bi-weekly. Consumer office hours monthly. Breaking change notification pipeline.

### Transition Triggers
- **Solo → Small**: Second consumer of your API (frontend team or external). Need documented contract.
- **Small → Medium**: >100 API consumers or external developers. First breaking change requires versioning.
- **Medium → Enterprise**: >1000 API consumers. Multi-product API surface. Developer portal needed.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `relation "..." does not exist` | Migration not run or wrong database | `npx prisma migrate dev` or check `DATABASE_URL` |
| `deadlock detected` | Concurrent transactions in wrong order | Enforce consistent lock ordering; use `NOWAIT` where appropriate |
| `connection pool exhausted` | Too many concurrent connections | Increase pool size; add connection timeout; check for leaked connections |
| `414 URI Too Long` | Request URI exceeds server limit | Use POST for data-heavy requests; paginate `?filter=` params |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  OpenAPI 3.1 specification complete with all paths, schemas, and security schemes
- [ ] **[S2]**  Error responses follow RFC 7807 Problem Details across all endpoints
- [ ] **[S3]**  Pagination strategy defined (cursor-based for lists > 1000 items)
- [ ] **[S4]**  Authentication (JWT/OAuth2/API Key) and authorization (RBAC/ABAC) defined per endpoint
- [ ] **[S5]**  Rate limiting configured with tiered quotas and appropriate headers
- [ ] **[S6]**  Idempotency key support for all mutating endpoints
- [ ] **[S7]**  API versioning and deprecation policy documented and communicated
- [ ] **[S8]**  SDKs generated and published for target languages (TypeScript, Python, Go at minimum)
- [ ] **[S9]**  Interactive documentation (Swagger UI/Scalar/Redoc) deployed
- [ ] **[S10]**  Health check endpoint (`GET /health`, `GET /health/ready`) implemented

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0)
- [RFC 7807 — Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)
- [JSON:API Specification](https://jsonapi.org/)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [Google API Design Guide](https://cloud.google.com/apis/design)
- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [gRPC API Design](https://grpc.io/docs/guides/design/)
