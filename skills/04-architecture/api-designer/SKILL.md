---
name: api-designer
description: 'REST, GraphQL, and gRPC API design with OpenAPI 3.1, versioning strategies,
  authentication, rate limiting, error handling, pagination, and SDK generation. Trigger:
  API design, OpenAPI, REST, GraphQL, gRPC, versioning, rate limiting, pagination,
  SDK.'
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- api-designer
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - backend-developer
  - database-designer
  - idea-to-spec
  - system-architect
  feeds_into:
  - api-test-suite-builder
  - backend-developer
  - database-designer
  - documentation-engineer
  - frontend-developer
  - fullstack-developer
  - mobile-developer
  - qa-engineer
  - technical-writer
---
# API Designer

Design production-grade APIs across REST, GraphQL, and gRPC paradigms. This skill covers full API lifecycle design: specification-first development with OpenAPI 3.1, consistent error modeling, authentication and authorization patterns, rate limiting, pagination strategies, versioning approaches, and developer experience (DX) including SDK generation and documentation.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design a new REST API from scratch → Start at "Decision Trees > REST vs GraphQL vs gRPC"
├── Create an OpenAPI 3.1 specification → Jump to "Core Workflow > Phase 1 (Specification-First Design)"
├── Design a GraphQL schema → Go to "Decision Trees > REST vs GraphQL vs gRPC" then Phase 2
├── Define gRPC service definitions → Jump to "Core Workflow > Phase 2 (Protocol Buffer Design)"
├── Version an existing API (breaking changes) → Go to "Best Practices > API Versioning"
├── Document an existing API → Jump to "Core Workflow > Phase 3 (Documentation & DX)"
├── Set up rate limiting or authentication → Go to "Best Practices > Security & Rate Limiting"
├── Generate SDKs or Postman collections → Go to "references/openapi-generator-guide.md"
├── Need backend implementation of this API → Invoke backend-developer skill instead
├── Need frontend to consume this API → Invoke frontend-developer skill instead
├── Need fullstack feature delivery → Invoke fullstack-developer skill instead
├── Need mobile client consuming this API → Invoke mobile-developer skill instead
├── Need to design the overall system → Invoke system-architect skill instead
├── Need database schema for this API → Invoke database-designer skill instead
├── Need security review of this API → Invoke security-reviewer skill instead
└── Not sure where to start? → Describe the API you need and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never design without consumer context.** Before writing any endpoint, ask: "Who calls this, and what do they need?" Do not design APIs in a vacuum.
- **Every endpoint needs error responses documented.** A 200 response is not enough — document 400, 401, 403, 404, 409, 429, and 500 for every endpoint. Do not leave error handling as an afterthought.
- **Breaking changes need versioning.** Field removal, type change, or semantic change = new version. Do not break consumers silently — use deprecation headers and migration windows.
- **Always design contract-first.** Write the OpenAPI spec before writing code. Share with consumers before implementation begins.
- **Admit what you don't know.** If you don't know the consumer's latency budget, data volume, or client capabilities, say so and ask before designing.

## The Expert's Mindset
<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent API designers build endpoints that return data. Masters build **contracts that survive years of evolution without breaking consumers.** The shift: your API is a product, and your consumers are customers. Every field you add, every response shape you commit to, every error format you choose — consumers will build dependencies on all of it. Changing your mind later means breaking their code. Design with the humility that you cannot predict the future, but you can design interfaces that accommodate it.

### Cognitive Biases That Kill APIs
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Database-model leak** | Exposing your database schema through your API — consumers learn your table structure and build dependencies on it | Design API resources from consumer use cases, not database tables. A `/checkout` endpoint returns what checkout needs, not a join of 5 tables. The database schema is an implementation detail. |
| **Over-fetching tolerance** | Returning full objects because "the consumer might need it someday" — bloated payloads, slow mobile, unused data | Return exactly what the consumer asked for. Use sparse fieldsets (`?fields=id,name`), GraphQL, or BFF pattern. Every unused field is bandwidth your users pay for. |
| **Versioning procrastination** | Avoiding versioning because "we'll never need it" — until you do, and 500 clients break simultaneously | Version from v1.0. Assume every API will need breaking changes eventually. The cost of versioning infrastructure at day zero is near zero. The cost of adding it after 500 consumers is astronomical. |

### What API Masters Know That Others Don't
- **The API is the UI for developers.** Developer experience matters as much as user experience. Consistent naming, predictable error formats, clear pagination, SDK generation — these determine whether integration takes hours or weeks. A great API makes the happy path obvious and the error path informative.
- **Backward compatibility is additive-only.** You can add fields, add endpoints, add optional parameters. You cannot remove, rename, retype, or re-semantic fields. If you need to change something, deprecate the old, create the new, and maintain both during a migration window. The window is measured in months, not days.
- **Rate limiting is not punitive — it's protective.** A rate limit protects your system AND your consumers from each other. Without rate limits, one misbehaving consumer degrades the experience for everyone. Rate limits with clear headers (`Retry-After`, `X-RateLimit-Remaining`) turn failures into retryable events.

### When to Break Your Own Rules
- **Skip REST for internal service-to-service communication.** gRPC with protobuf gives you type safety, performance, and code generation that REST can't match. REST is for external consumers. Internal services can use faster contracts.
- **Return 200 with an error body for legacy consumers.** If you have consumers that crash on non-200 status codes (it happens), wrap errors in a 200 response with an `error` field. It's not pure REST, but it keeps legacy consumers running while you migrate them.

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
<!-- DEEP: 10+min -->
1. Write the OpenAPI 3.1 specification before implementation.
2. Define **paths** with clear resource naming: plural nouns (`/users`, `/orders`), nested for sub-resources (`/users/{id}/orders`), no verbs in URLs (except for non-CRUD actions like `/orders/{id}/cancel`).
3. Define **schemas** with complete property types, formats, constraints (minLength, pattern, enum), examples, and descriptions.
4. Define **responses** for all status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500) with consistent error body schema.
5. Add **security schemes** (Bearer JWT, OAuth2, API Key) and `security` requirements per operation.
6. Include `servers` with environment URLs, `tags` for grouping, `info` with version and contact.

### Phase 3 (~20 min): Consistency & Governance
<!-- DEEP: 10+min -->
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


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | system-architect | System boundaries, service topology, API surface area decisions |
| **This** | api-designer | OpenAPI 3.1 specs, error models, pagination conventions, rate limiting policies |
| **After** | backend-developer | Consumes API contract to implement endpoints, validation, and middleware |

Common chains:
- **Greenfield service**: system-architect → api-designer → backend-developer — Architecture defines boundaries, API design formalizes the contract, backend implements it
- **Data-driven API**: database-designer → api-designer → frontend-developer — Schema shapes the resources, API exposes them, frontend consumes them

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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Bounded context map, service topology, non-functional requirements (latency/throughput/availability), API principles and versioning strategy | Before defining service boundaries or choosing REST/GraphQL/gRPC |
| `database-designer` | ERD, schema design, access patterns, consistency vs. availability tradeoffs, query complexity estimates | Before designing endpoints that map to new data models; N+1 risk assessment |
| `backend-developer` | Implementation feasibility feedback, framework constraints, performance benchmarks for proposed query patterns | Before finalizing resource shapes that backend must implement |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `backend-developer` | OpenAPI 3.1 spec, auth scheme, rate limits, error codes, pagination conventions | Backend can't implement without contract — blocked sprints |
| `frontend-developer` | Same API contract for client generation, BFF patterns, type-safe SDK | Frontend builds against wrong shapes — costly rework |
| `fullstack-developer` | API contract, endpoint specs, error models for full-stack integration | Fullstack features blocked on contract ambiguity |
| `mobile-developer` | API contract optimized for mobile (response size budgets, delta updates, partial responses) | Mobile integration builds against stale or bloated contracts |
| `qa-engineer` | OpenAPI spec as test source of truth, expected error scenarios, edge cases | QA can't author contract tests without the contract |

### Escalation Path

```
API breaking incident (auth bypass, data leak, API-wide outage)
  └── API Designer + Security Engineer + System Architect + DevOps. War room. Hotfix or rollback within hours.

Breaking API change needed for >50% of consumers
  └── API Designer + System Architect + Product Manager + affected team leads. New major version or extended deprecation.

Minor API addition or non-breaking change
  └── API Designer reviews, team implements. No escalation needed. Changelog and docs updated.
```


**What good looks like:** OpenAPI 3.1 spec renders cleanly in Swagger UI with no validation warnings. Every endpoint has at least one request example, one response example, and all error schemas documented. A frontend developer can generate a type-safe client from the spec and start integrating without asking a single question about pagination, filtering, sorting, or error handling.

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Designing a new endpoint consumed by a mobile app | Propose response size budgets (≤50KB per payload), partial response via sparse fieldsets (`?fields=`), and delta sync endpoints. Discuss offline-first patterns (ETag + If-None-Match) before designing the resource shape | Mobile clients on spotty networks need lean payloads. A 2MB JSON response that works in the browser will crash a mobile app on 3G. Retroactively trimming payloads after mobile integration causes cascading rework |
| Choosing between REST and GraphQL for a multi-client platform | Before deciding, map each client's data needs: web needs aggregated dashboards, mobile needs flat lists, third-party needs stable envelopes. If 3+ clients need different field subsets from the same resources, strongly recommend GraphQL with persisted queries and query cost analysis | REST forces over-fetching when clients have heterogeneous data needs — mobile pulls 40 fields to render 3, third-party clients break when new fields appear. GraphQL shifts the shaping burden to the server where it belongs |
| Designing a public API consumed by external developers | Propose an API gateway layer with per-consumer rate limiting, API key rotation policies, and a developer portal with interactive docs BEFORE the first endpoint is built. Plan SDK generation pipeline (OpenAPI Generator) and consumer notification channels (changelog, deprecation calendar) | Public APIs are products, not internal plumbing. Without gateway-level consumer management from day one, you'll be retrofitting auth, rate limiting, and documentation after external devs have already built brittle integrations against raw endpoints |
| Adding a new field to an existing API response | Before making the field `required`, ship it as optional for 2+ release cycles. Add deprecation headers to any fields being replaced. If the field changes response semantics (e.g., price format, status enum), propose a minor version bump with backward compatibility | Required fields in additive changes break strict deserializers (mobile, TypeScript strict mode). A "minor" addition that crashes every iOS app is a production incident disguised as a feature. Grace periods save consumer relationships |
| Designing an endpoint that connects to an upstream backend service mesh | Propose circuit breaker configuration (e.g., 50% error rate → open), request timeouts aligned to upstream SLOs, retry budgets (max 3 with exponential backoff + jitter), and bulkhead isolation. Discuss whether the API should return stale cached data vs 503 when upstreams degrade | APIs that blindly forward failures from 5 upstream services cascade latency. A 200ms P95 backend timeout combined with 3 retries and no circuit breaker becomes a 2.5s response — 12x worse. Graceful degradation keeps the API responsive even when backends are not |
| Switching an existing REST endpoint to WebSocket for real-time updates | Before upgrading, verify: (a) load balancer config supports WebSocket upgrade headers and connection draining, (b) CDN/proxy layers don't buffer or strip `Upgrade: websocket`, (c) auth tokens are passed on connect (not per-message), (d) reconnection with exponential backoff is client-implemented | Load balancers and CDNs configured for short-lived HTTP/1.1 connections silently drop WebSocket upgrades. Connection count per instance skyrockets. Without proper reconnection logic, clients hang forever on stale sockets thinking they're connected |
| Designing idempotency for payment or order-creation endpoints | Propose `Idempotency-Key` header with server-side key storage (Redis with 24h TTL). The key must be generated by the client, not the server. Response includes `Idempotency-Replay: true` header when returning a cached response. Implement key collision detection for duplicate submissions from different clients | Payment gateways charge twice when retries aren't idempotent. Network blips cause client retries that create duplicate orders. Telling users "check if your order went through" is not a production strategy — idempotency keys make retries safe by design |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Spec-first, not code-first**: OpenAPI spec is the source of truth; generate server stubs and client SDKs from it.
- **Naming consistency**: camelCase for JSON properties, kebab-case for headers and query params, UPPER_SNAKE for enum values.
- **Use HTTP semantics correctly**: GET (safe, idempotent), PUT (idempotent replace), PATCH (partial update), POST (create), DELETE (idempotent).
- **Rate limiting headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`.
- **HATEOAS links** where practical: include `_links` in responses for discoverability and self-documenting APIs.
- **SDK generation**: Use OpenAPI Generator or fern for multi-language SDKs; publish to package registries (npm, PyPI, Maven).
- **Contract testing**: Use Pact or Spring Cloud Contract to verify API compatibility between services.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Designing an API without rate limiting because "we're small" | Implement tiered rate limiting from day one with `X-RateLimit-*` headers. Even 100 RPM per client with a burst allowance of 200 prevents a runaway client script from taking down your service. Fixed-window is easy; token bucket is better |
| Returning unstructured error bodies (`{"error": "Something went wrong"}`) | Standardize on RFC 7807 Problem Details: `{"type": "...", "title": "...", "status": 400, "detail": "...", "instance": "..."}`. Machine-readable error codes (`INSUFFICIENT_FUNDS`) in a `code` field. Consumers should never need to parse error strings |
| Embedding auth tokens in URL query parameters | Use `Authorization: Bearer <token>` header. Query params are logged in access logs, browser history, and CDN logs. JWT tokens in URLs are credential leaks waiting to happen. Also: never accept tokens in both header and query — pick one |
| Using server-side pagination without cursor stability guarantees | Cursor-based pagination with stable, opaque cursors (UUID or base64-encoded timestamp+ID). Never expose database row IDs as cursors — they leak implementation details and break on migrations. Always include `has_more: boolean` in responses |
| Designing file upload endpoints without size limits and streaming support | Accept `multipart/form-data` with `Content-Length` enforced at the API gateway (e.g., 10MB max). Stream uploads to object storage (S3) — never buffer in application memory. Return `202 Accepted` with a status-polling URL for large uploads. Add virus scanning at the gateway |
| Versioning every single endpoint change (v2, v3, v4...) when only additive changes were made | Version only on breaking changes (field removal, type change, semantic change). Additive changes (new fields, new endpoints) are backward-compatible. Run `openapi-diff` in CI to classify changes automatically. Running 4+ concurrent versions is a maintenance nightmare |
| Exposing internal service error details (stack traces, DB connection strings) in 500 responses | Strip all internal details from production error responses. Log the full error server-side with a correlation ID (`X-Request-Id`). Return `{"status": 500, "title": "Internal Server Error", "instance": "/orders/12345", "trace_id": "abc-123"}` — enough to debug, nothing to exploit |
| Designing synchronous POST endpoints for operations that take >2 seconds | Return `202 Accepted` with a `Location` header pointing to a status endpoint (`/orders/12345/status`). If the client must be notified on completion, provide a webhook URL parameter. Synchronous long-running requests tie up connections, timeout unpredictably, and create retry storms |

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


## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| All mobile clients broke after a minor API update | Breaking change (field type changed from `int` to `string`) shipped in a minor version (`v1.1`) with no versioning strategy | Revert the breaking change, restore backward compatibility, publish a v2 with proper deprecation. Implement OpenAPI diff CI to detect breaking changes automatically | **Never ship breaking changes in minor versions.** Use URL path versioning (`/v1/`, `/v2/`) for public APIs. Run `openapi-diff` in CI to catch accidental breaking changes before deploy |
| Mobile app shows blank UI, web client works fine | API returns a new required field; web client ignores unknown fields, mobile client crashes on unexpected key | Remove the `required` constraint from the new field, roll back mobile SDK version, add a grace period where new fields are optional | **Additive changes stay additive.** Never make new fields required at the same time you add them. Soft-launch new fields as optional for two release cycles |
| Error responses format differs between endpoints | Different teams built different error schemas (`{"error": "..."}` vs `{"message": "..."}` vs `{"errors": [...]}`) | Standardize on RFC 7807 Problem Details across the entire API surface. Audit all endpoints, create a migration plan. Add OpenAPI schema enforcement in CI | **Error format must be part of the API contract from day one.** Document the error schema in the OpenAPI spec before any endpoint is built. Inconsistent errors cost hours of debugging per incident |
| API gateway returned 429 for all users, blocking legitimate traffic | Rate limiting was set based on average traffic without considering burst patterns; a flash crowd triggered the per-IP limit | Implement tiered rate limiting (free: 100/min, pro: 1000/min) with burst allowance (2x for 5s). Add `Retry-After` headers. Use token bucket instead of fixed window | **Rate limits must be tiered, documented, and include burst allowance.** Fixed-window rate limiting causes thundering herd on window boundaries. Always return meaningful headers (`X-RateLimit-Remaining`) for client-side backoff |
| Client integration failed silently for 3 days before discovery | API contract changed (endpoint merged two query params) but consumer was not notified; no deprecation headers were sent | Implement `Sunset` and `Deprecation` HTTP headers on deprecated endpoints. Create a consumer notification pipeline (email + changelog). Add monitoring for usage of deprecated endpoints | **APIs need a deprecation policy before the first breaking change.** Document sunset timelines (12 months minimum), send deprecation headers, and monitor consumer migration progress. Silent breaks destroy developer trust |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[API1]**  OpenAPI 3.1 specification complete with all paths, schemas, and security schemes
- [ ] **[API2]**  Error responses follow RFC 7807 Problem Details across all endpoints
- [ ] **[API3]**  Pagination strategy defined (cursor-based for lists > 1000 items)
- [ ] **[API4]**  Authentication (JWT/OAuth2/API Key) and authorization (RBAC/ABAC) defined per endpoint
- [ ] **[API5]**  Rate limiting configured with tiered quotas and appropriate headers
- [ ] **[API6]**  Idempotency key support for all mutating endpoints
- [ ] **[API7]**  API versioning and deprecation policy documented and communicated
- [ ] **[API8]**  SDKs generated and published for target languages (TypeScript, Python, Go at minimum)
- [ ] **[API9]**  Interactive documentation (Swagger UI/Scalar/Redoc) deployed
- [ ] **[API10]**  Health check endpoint (`GET /health`, `GET /health/ready`) implemented
- [ ] **[API11]**  Bulk operation endpoints use 202 Accepted with status tracking where synchronous 200 is insufficient
- [ ] **[API12]**  Webhook/event subscription design documented with retry and signing strategy
- [ ] **[API13]**  API observability dashboards deployed (latency percentiles, error rates by endpoint, consumer usage)
- [ ] **[API14]**  Consumer-facing changelog maintained with deprecation timelines and migration guides

## What Good Looks Like

> API consumers integrate in hours, not weeks. The specification is the source of truth — nothing ships that isn't documented. Breaking changes are rare and always communicated 6+ months ahead. SDKs in every target language stay in sync with the spec. Error messages tell consumers exactly what to fix. Your API feels like a product, not an afterthought.

## Deliberate Practice
<!-- DEEP: 10+min — how to improve, not just what you do -->

### The API Design Improvement Loop
1. **Review a real API integration** — Watch a developer integrate with your API for the first time. Time them. Where do they get stuck? What confused them? What did they have to read the docs for?
2. **Fix the biggest friction point** — Simplify the confusing endpoint. Add the missing error message. Clarify the authentication docs.
3. **Re-test with a new developer** — Did integration time decrease? If not, the fix wasn't the real bottleneck.
4. **Repeat every time you onboard a new API consumer** — Every new integration is a UX test.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Design the same API in REST, GraphQL, and gRPC. Write a consumer for each. Compare: lines of client code, error handling clarity, type safety | Monthly | Can articulate paradigm tradeoffs from consumer experience, not documentation |
| Competent → Expert | Take a public API (Stripe, GitHub, Twilio) and reverse-engineer their design decisions. Why did they version this way? Why this pagination pattern? Write an analysis | Monthly | Develops taste — can distinguish great API design from merely functional |
| Expert → Master | Deprecate an endpoint in your own API with zero consumer complaints. Achieve 100% migration to the new endpoint before removing the old one | Per deprecation cycle | Masters API lifecycle management — deprecation without disruption is the hardest API skill |

### The One Thing
**Design an API by writing the consumer code first.** Before you write a single endpoint spec, write the code you wish you could write as a consumer. `const order = await api.orders.create({...})`. Let the ideal consumer experience drive the API design. An API that's easy to consume was designed from the outside in.

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
