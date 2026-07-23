---
name: api-designer
description: >
  Use when designing REST, GraphQL, or gRPC APIs, writing OpenAPI 3.1 specifications,
  defining versioning strategies, or architecting authentication and rate limiting.
  Handles API lifecycle design, error modeling, pagination strategies, SDK generation,
  developer portal design, and API security patterns. Do NOT use for implementing APIs,
  database schema design, or frontend API consumption.
license: MIT
tags:
- api
- rest
- graphql
- grpc
- openapi
- versioning
- sdk
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
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
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design production-grade APIs across REST, GraphQL, and gRPC paradigms. This skill covers full API lifecycle design: specification-first development with OpenAPI 3.1, consistent error modeling, authentication and authorization patterns, rate limiting, pagination strategies, versioning approaches, and developer experience (DX) including SDK generation and documentation.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("openapi.yaml")` OR `file_exists("openapi.json")` OR `file_exists("swagger.yaml")` | OpenAPI spec exists. Jump to **Decision Trees** — REST vs GraphQL vs gRPC (start with the existing paradigm). |
| A2 | `file_contains("package.json", "graphql\|apollo\|@graphql\|type-graphql")` | GraphQL in use. Jump to **Decision Trees** — REST vs GraphQL vs gRPC (GraphQL branch). |
| A3 | `file_exists("*.proto")` AND `file_contains("*.proto", "service\s+\w+")` | gRPC proto files exist. Jump to **Decision Trees** — REST vs GraphQL vs gRPC (gRPC branch). |
| A4 | `file_contains("openapi.yaml\|openapi.json", "version.*v[2-9]")` AND `file_contains("openapi.yaml\|openapi.json", "deprecated")` | Multiple API versions with deprecations. Jump to **Versioning Cost Analysis**. |
| A5 | `file_contains("*", "429\|rate.limit\|RateLimit\|X-RateLimit\|throttle")` | Rate limiting concerns. Jump to **Decision Trees** — Rate Limiting Tier Design. |
| A6 | `file_contains("*", "JWT\|OAuth\|Bearer\|API.Key\|auth")` AND `file_contains("openapi.*", "securityScheme\|bearerAuth\|oauth2")` | Auth configuration exists. Jump to **Decision Trees** — API Key vs OAuth2 vs JWT. |
| A7 | `file_contains("*", "pagination\|cursor\|page\|offset\|limit\|nextPage")` | Pagination concerns. Jump to **Decision Trees** — Cursor vs Offset Pagination. |
| A8 | `file_contains("*", "bulk\|batch\|import\|export\|long.running\|async")` | Bulk/async operations. Jump to **Core Workflow** — Phase 2 (Async patterns). |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a new REST API from scratch → Start at "Decision Trees > REST vs GraphQL vs gRPC"
├── Create an OpenAPI 3.1 specification → Jump to "Core Workflow > Phase 1 (Specification-First Design)"
├── Design a GraphQL schema → Go to "Decision Trees > REST vs GraphQL vs gRPC" then Phase 2
├── Define gRPC service definitions → Jump to "Core Workflow > Phase 2 (Protocol Buffer Design)"
├── Version an existing API (breaking changes) → Go to "Versioning Cost Analysis"
├── Document an existing API → Jump to "Core Workflow > Phase 3 (Documentation & DX)"
├── Set up rate limiting or authentication → Go to "Decision Trees > Rate Limiting Tier Design" or "API Key vs OAuth2 vs JWT"
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

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to design without consumer context.** Before writing any endpoint, identify: who calls this, what is their latency budget, what is their data volume, and what is their error-handling capability. An API designed in a vacuum optimizes for the designer's preferences, not the consumer's reality. | Trigger: producing an API design or endpoint spec without mentioning consumer persona, latency budget, data volume, or client capability (mobile/web/backend) | STOP. Ask: "Who calls this API? What's their latency budget (< 200ms? < 2s?)? What's the typical payload size? What client type (mobile, web SPA, server-to-server)? Without consumer context, you're designing for an imaginary user." |
| **R2** | **REFUSE to ship an endpoint without error responses documented.** A 200 response is not a complete contract. Every endpoint MUST document 400 (validation), 401/403 (auth), 404 (not found), 409 (conflict), 429 (rate limit), and 500 (server error) with RFC 7807 Problem Details format. Unspecified errors become undocumented behavior that consumers depend on. | Trigger: OpenAPI spec has a path/operation with only a 200/201 response and no 4xx/5xx responses defined, or error responses lack a schema reference | STOP. Insert: "**Missing error responses:** [endpoint]. Every operation must define: 400, 401, 403, 404, 409, 429, 500 with `$ref: '#/components/responses/ProblemDetails'`. Errors are part of the API contract — not specifying them is specifying that they don't exist." |
| **R3** | **DETECT and WARN about breaking changes in minor/patch versions.** Field removal, type change (`int` → `string`), enum value removal, or semantic change (same type, different meaning) = breaking change = new major version. Never ship breaking changes in minor versions — this is the #1 cause of API consumer trust erosion. | Trigger: running `npx openapi-diff old.yaml new.yaml` returns breaking changes with severity: error, and the version bump in the spec is not a major version increment | WARN. Report: "Breaking change detected: [change description]. This MUST ship as a new major version with a deprecation window. Run `openapi-diff` in CI to catch these automatically. Breaking change in a minor version = silent client breakage and consumer trust loss." |
| **R4** | **REFUSE to accept auth tokens in URL query parameters.** Tokens in URLs are logged in access logs, browser history, CDN logs, proxy logs, and referrer headers. JWT in a query string is a credential leak in 5+ locations. Use `Authorization` header exclusively. | Trigger: OpenAPI spec or code contains: `security: - apiKey: []` with `in: query` for a Bearer/JWT token, or endpoint documentation shows `?token=...` or `?access_token=...` | STOP. Rewrite: "Use `Authorization: Bearer <token>` header only. Query parameter tokens are credential leaks — every CDN log, proxy log, and browser history entry copies the token. If you MUST support query-param tokens for a legacy client, mark the parameter as deprecated with a migration timeline." |
| **R5** | **DETECT and WARN when pagination is missing for list endpoints.** Any endpoint returning a collection MUST have pagination. Without it: a growing dataset causes unbounded response times, memory exhaustion in clients, and eventual timeout failures that cascade. | Trigger: OpenAPI path returns an array/collection (schema type: array or items property present) without `page`/`cursor`/`offset`/`limit`/`after`/`before` parameters defined | WARN. Insert: "List endpoint [path] returns a collection without pagination. Add cursor-based pagination for datasets > 100 items: `parameters: { cursor, limit }`, response includes `next_cursor` and `has_more: boolean`. Offset pagination is acceptable for small, stable datasets (< 1000 items). Unbounded collections = guaranteed production incident at scale." |
| **R6** | **STOP and WARN about synchronous POST for > 2-second operations.** Long-running synchronous requests tie up server connections, timeout unpredictably in load balancers and proxies, and create retry storms when clients timeout and resend. | Trigger: endpoint spec is POST/PUT/DELETE with a 200/201 response, the description mentions "process", "generate", "import", "export", "batch", "bulk", or "convert", and no `202 Accepted` response is defined | STOP. Rewrite: "Operation [method] [path] appears long-running. Return `202 Accepted` with `Location: /operations/{id}/status` for polling, or provide a `webhook_url` parameter for async notification. Synchronous POST for operations > 2 seconds will fail at scale — proxies time out at 60s, clients retry, creating stampedes." |

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

## Operating at Different Levels

API design skill manifests in the scope of the API — from single endpoints to org-wide API governance.

| Level | API Design Output Characteristics |
|---|---|
| **L1 — Apprentice** | Implements API endpoints from a spec. Learns REST/GraphQL conventions. "Here's the endpoint that returns user data." |
| **L2 — Practitioner** | Designs API surfaces for a single domain. Produces OpenAPI specs. Handles error responses, pagination, and versioning correctly. |
| **L3 — Senior** | Designs the API strategy for a product. Paradigm selection (REST vs GraphQL vs gRPC). Auth, rate limiting, and deprecation strategy. Trade-off rationale included. |
| **L4 — Staff** | Sets API design standards for the organization. API governance: naming conventions, error formats, versioning policy. "Every API at this company follows this contract." |
| **L5 — Principal** | Creates API design paradigms adopted across the industry. "Here's a new API pattern for this class of problem." |

**Usage**: Say "as an L3 API designer, design the API surface for..." Default: **L2** (domain-level API design, independent execution).

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

## What Good Looks Like

> API consumers integrate in hours, not weeks. The specification is the source of truth — nothing ships that isn't documented. Breaking changes are rare and always communicated 6+ months ahead.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


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

## Gotchas

- **OpenAPI `additionalProperties` defaults to `true`** in JSON Schema. If your spec doesn't explicitly set it to `false`, clients will silently accept extra fields. Every request body schema needs `"additionalProperties": false`.
- **PATCH with `application/merge-patch+json`** (RFC 7396) uses `null` to mean "delete this field." But `application/json-patch+json` (RFC 6902) uses `{"op": "remove", "path": "/field"}`. Clients that send the wrong content type will corrupt data — `null` becomes a literal null value instead of a deletion.
- **Cursor-based pagination** with `?after=xxx` requires a stable, unique sort order. Using `created_at` alone breaks when two records have the same timestamp. Always add a tiebreaker column (usually `id`).
- **Rate limit headers** `X-RateLimit-Remaining` — if your gateway strips custom headers or renames them, the client sees no rate info. `RateLimit-*` (IETF draft) headers are increasingly preferred. Support both.
- **`202 Accepted`** means "I queued this, no guarantee of completion." Clients that treat 202 as success will assume the resource exists when it may still be processing. Always include a `Location` header pointing to a status endpoint.
- **API versioning in the URL path** (`/v1/users`) means every route has a version prefix. When you add `/v2/users`, the old `/v1/users` route still needs maintenance until deprecated. URL versioning creates N copies of every endpoint.


## Verification

- [ ] Run OpenAPI validator: `redocly lint openapi.yaml` or `spectral lint openapi.yaml` — zero errors
- [ ] Generate and inspect docs: `redocly build openapi.yaml` — all endpoints documented, all schemas have examples
- [ ] Test with mock server: `prism mock openapi.yaml` and `curl` each endpoint — responses match schema
- [ ] Verify pagination: all list endpoints return `next`/`cursor` link when more results exist
- [ ] Verify error responses: every endpoint's 4xx and 5xx responses match `ErrorResponse` schema
- [ ] Check `servers[].url` in OpenAPI: matches all environments (dev/staging/prod), no localhost URLs


## References
- **"Is REST Overkill?" Decision Tree**: See ["is-rest-overkill?"-decision-tree.md](references/"is-rest-overkill?"-decision-tree.md)
- **Versioning Cost Analysis**: See [versioning-cost-analysis.md](references/versioning-cost-analysis.md)
