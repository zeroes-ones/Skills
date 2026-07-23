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
<!-- QUICK: 90s -- 4-column machine-checkable format. Every anti-pattern has a grep to find it and a lint/prevention config. -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Designing an API without rate limiting because "we're small" | Implement tiered rate limiting from day one with `X-RateLimit-*` headers. Fixed-window is easy; token bucket is better. Even 100 RPM prevents runaway scripts | `grep -L 'rate.limit\|RateLimit\|X-RateLimit\|throttle' openapi.*` — spec files with no rate limit configuration | CI gate: `scripts/check-rate-limits.sh` validates every API gateway config has rate limiting enabled. Block deploy if rate limits are missing |
| Returning unstructured error bodies (`{"error": "Something went wrong"}`) | Standardize on RFC 7807 Problem Details: `type`, `title`, `status`, `detail`, `instance` fields. Machine-readable `code` field for programmatic handling | `grep -rn '"error"' openapi.* \| grep -v 'ProblemDetails\|RFC.7807\|type.*title.*status.*detail'` — unstructured error fields | Spectral rule: `problem-details-required` — any error response schema MUST include `type`, `title`, `status`, `detail`. CI blocks non-conforming error responses |
| Embedding auth tokens in URL query parameters (`?token=...`) | Use `Authorization: Bearer <token>` header exclusively. Query params leak tokens into access logs, CDN logs, browser history | `grep -rn 'token.*query\|query.*token\|in:\s*query' openapi.*` — security scheme using query parameter | Spectral rule: `no-query-param-auth` — block any `securityScheme` with `in: query` for Bearer/OAuth2 tokens. Header-only enforcement |
| Using server-side pagination without cursor stability guarantees (exposing DB row IDs as cursors) | Cursor-based pagination with opaque cursors (base64-encoded UUID). Never expose database row IDs — they break on migrations and leak data patterns | `grep -rn 'cursor.*:.*integer\|cursor.*:.*number' openapi.*` — cursors typed as integers (likely row IDs) | Pagination validator: `scripts/check-cursors.sh` verifies cursor fields are opaque strings (base64 or UUID format), not integers or timestamps |
| Designing file upload endpoints without size limits and streaming support | Enforce `Content-Length` at gateway (e.g., 10MB). Stream to object storage — never buffer in app memory. Return `202 Accepted` for large uploads | `grep -rn 'multipart/form-data\|file.*upload' openapi.* \| grep -v 'maxLength\|maxSize\|Content-Length\|202'` — upload endpoints without limits | Gateway config rule: all upload endpoints must have `maxBodySize` set. CI validates `Content-Length` enforcement exists |
| Versioning every single endpoint change (v2, v3, v4...) when only additive changes were made | Version only on breaking changes. Additive changes (new fields, new endpoints) are backward-compatible. Run `openapi-diff` in CI to classify automatically | `grep -c '/v[2-9]/' openapi.*` — count of active versions. > 3 active versions = versioning fatigue | CI job: `npx openapi-diff main..feature` — classifies changes as breaking/non-breaking. Blocks PR if breaking change detected without major version bump |
| Exposing internal service error details (stack traces, DB connection strings) in 500 responses | Strip all internal details from 500 responses. Return RFC 7807 with correlation ID. Log full error server-side with matching `trace_id` | `grep -rn 'stack\|traceback\|Exception\|at\s+\w+\.\w+:\d+' responses/*` — stack trace patterns in response schemas | Response sanitizer: `scripts/sanitize-error-responses.sh` strips stack traces, file paths, and connection strings from all 500 response bodies before egress |
| Designing synchronous POST endpoints for operations that take > 2 seconds — no async pattern | Return `202 Accepted` with `Location: /operations/{id}/status`. Long-running sync requests tie up connections and create retry storms | `grep -rn 'POST\|PUT\|DELETE' openapi.* \| grep -v '202\|Accepted\|async\|Location.*status'` — mutating endpoints without async pattern when description implies long-running | Async validator: `scripts/check-async-patterns.sh` — for any POST/PUT/DELETE with body size > 100KB or description containing "process/generate/import/export/batch", require `202 Accepted` response defined |

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
<!-- DEEP: 10+min -- 5-column format with grep matches and auto-recovery loops -->

| 🖥️ Console Match (grep) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|--------------------------|---------|-----------|-----|----------------------|
| `grep -iP '(status.*422\|Unprocessable\|validation.*failed\|request.*invalid)' logs/api-errors.log` | Clients receive 422/400 errors on fields that worked previously — API rejects known-good payloads | Breaking change: field type changed (e.g., `int` → `string`), required field added, or enum value removed — shipped in a minor version without versioning | Revert the breaking change. Restore backward compatibility. Publish new version with `Deprecation` + `Sunset` headers. Implement `openapi-diff` in CI to block breaking changes in minor versions | 1. Run `npx openapi-diff v1.yaml v2.yaml`. 2. List all breaking changes. 3. For each: revert in the current version OR create a new major version. 4. Add `Sunset: [date 12 months out]` and `Deprecation: true` to deprecated fields. 5. Monitor usage of deprecated fields via analytics. 6. Add `openapi-diff` to CI — block PRs that introduce breaking changes without major version bump |
| `grep -iP '(timeout\|gateway.timeout\|504\|upstream.*timed.out\|request.*timed.out)' logs/api-errors.log` | Clients get 504 Gateway Timeout on specific endpoints — API appears down intermittently | Long-running synchronous operation (> 2s) tying up connections. Load balancer or proxy has 60s timeout; the operation takes 90s. Clients retry, creating connection exhaustion | Convert to `202 Accepted` with status polling URL. Add webhook callback pattern for completion notification. Set `timeout` on HTTP client to 2s for all sync endpoints | 1. Identify endpoints with P95 latency > 2s. 2. Convert each: POST → 202 Accepted + `Location: /ops/{id}/status`. 3. Add GET /ops/{id}/status returning `{ status: "processing"\|"completed"\|"failed", result }`. 4. Optionally add `webhook_url` parameter for push-based completion. 5. Set load balancer timeout to 120s for async endpoints, 2s for sync |
| `grep -iP '(429\|Too.Many.Requests\|rate.*limit.*exceeded\|throttle)' logs/api-errors.log` | Healthy users hitting 429 at traffic peaks — API returns rate limit errors for legitimate clients during flash crowds | Rate limiting uses fixed-window algorithm. At window boundary (e.g., 00:00), all clients reset simultaneously → thundering herd. No burst allowance for short traffic spikes | Switch to token bucket algorithm with burst allowance (2x base rate for 5s). Return `Retry-After` and `X-RateLimit-Reset` headers. Add tiered limits (free tier: 100/min, pro: 1000/min) | 1. Identify rate limit algorithm in gateway config. 2. If fixed-window: replace with token-bucket (refill_rate: base_rpm, capacity: 2× base). 3. Add burst allowance to all tiers. 4. Verify `Retry-After` header in 429 responses. 5. Load-test with burst traffic pattern — should accept 2x for 5s, then throttle |
| `grep -iP '(missing.*page\|pagination.*missing\|unbounded.*response\|response.*too.*large\|OOM)' logs/api-errors.log` | Client or server OOM on list endpoints — response payloads grow unbounded over months | List endpoint returns unfiltered full dataset. As data grows from 100 → 100,000 rows, response time balloons and clients allocate progressively more memory | Add cursor-based pagination: `limit` (max 100), `cursor` (opaque string). Response includes `next_cursor`, `has_more: boolean`. Set hard cap on `limit` parameter (e.g., max 100) at API gateway | 1. Audit all GET /resources endpoints. 2. For each returning arrays: add `cursor` and `limit` query params. 3. Set `limit` default=25, max=100, validate at gateway. 4. Return `{ data: [...], pagination: { next_cursor, has_more } }`. 5. Load-test with 100,000 items — P95 latency must be < 500ms regardless of dataset size |
| `grep -iP '(error.*format.*differ\|inconsistent.*error\|unexpected.*error.*body\|error.*parse.*fail)' logs/api-errors.log` | Consumer can't parse error responses — different endpoints return different error formats (`{"error": "..."}`, `{"message": "..."}`, bare string) | Different teams implemented different error schemas with no governance. Consumer must handle N different error formats, leading to missed errors and silent failures | Standardize on RFC 7807 Problem Details across ALL endpoints. Add response schema to OpenAPI `components/responses/ProblemDetails`. Enforce in CI with Spectral rule — any 4xx/5xx response must use ProblemDetails schema or CI fails | 1. Document standard error format: `{ type, title, status, detail, instance, code }`. 2. Add `ProblemDetails` schema to OpenAPI components. 3. Create Spectral rule: all 4xx/5xx responses → `$ref: '#/components/responses/ProblemDetails'`. 4. Scan all endpoints for non-conforming error schemas. 5. Migrate incrementally: start with new endpoints, then P0 existing endpoints. 6. Add CI check for ProblemDetails compliance |

| `grep -iP '(auth.*header.*missing\|unauthorized.*bearer\|token.*not.*found\|missing.*auth)' logs/api-errors.log` | Auth token works in some environments but not others — same JWT works in dev, fails in staging | Token sent via query parameter in one client, via header in another. Some gateways strip query params. Accepting tokens in both header AND query creates inconsistent auth behavior | Standardize: `Authorization: Bearer <token>` header ONLY. Block query-param tokens at API gateway. Add middleware that rejects requests with token in query string with a 400 and migration message | 1. Audit auth middleware: search for `req.query.token` or `request.args.get('token')`. 2. Remove all query-param token extraction. 3. Add gateway rule: if query contains `token=` → 400 with `{ detail: "Tokens in query parameters are deprecated. Use Authorization: Bearer header." }`. 4. Notify consumers with migration timeline. 5. Monitor and hard-block after 90 days |


## Production Checklist
<!-- QUICK: 30s -- all items are machine-verifiable. Every item gets a validation command and auto-fix path. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **API1** | OpenAPI 3.1 specification complete with all paths, schemas, and security schemes | `npx spectral lint openapi.yaml --ruleset .spectral.yaml` — 0 errors, 0 warnings | Run `npx @redocly/cli lint openapi.yaml` to auto-fix simple issues. Template: `templates/openapi-baseline.yaml` |
| **API2** | Error responses follow RFC 7807 Problem Details across all endpoints | `grep -cP 'ProblemDetails\|type.*title.*status.*detail' openapi.yaml` — must match count of 4xx/5xx responses | Spectral rule: `scripts/check-problem-details.sh` — auto-adds ProblemDetails schema ref to any 4xx/5xx response missing it |
| **API3** | Pagination strategy defined (cursor-based for lists > 1000 items) | `grep -cP 'cursor\|next_cursor\|has_more\|page\|offset\|limit' openapi.yaml` — >= 1 pagination pattern per list endpoint | Add `scripts/check-pagination.sh` — flags any GET endpoint returning array without pagination params |
| **API4** | Authentication (JWT/OAuth2/API Key) and authorization (RBAC/ABAC) defined per endpoint | `grep -c 'security:' openapi.yaml` — every path must have security defined at operation or root level | `scripts/check-auth-coverage.sh` — reports endpoints without security requirements; auto-adds global security scheme |
| **API5** | Rate limiting configured with tiered quotas and appropriate headers | `grep -cP 'X-RateLimit\|429\|Retry-After' openapi.yaml` — must show rate limit headers in 429 response | Gateway config template: `templates/rate-limit-config.yaml` — deploy with default 100/min free, 1000/min pro tiers |
| **API6** | Idempotency key support for all mutating endpoints (POST/PUT/PATCH/DELETE) | `grep -c 'Idempotency-Key' openapi.yaml` — every mutating endpoint must document this header | Add `scripts/check-idempotency.sh` — reports POST/PUT/PATCH/DELETE ops without `Idempotency-Key` header documented |
| **API7** | API versioning and deprecation policy documented and communicated | `grep -cP 'version\|deprecat\|sunset\|migration' api-policy.md` — >= 3 policy references | Template: `templates/api-versioning-policy.md` — includes sunset timeline, deprecation headers, migration guide template |
| **API8** | SDKs generated and published for target languages (TypeScript, Python, Go at minimum) | `ls sdks/ \| grep -c 'typescript\|python\|go'` — >= 3 SDK directories exist and are published | Run `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g <lang>` for each missing SDK |
| **API9** | Interactive documentation (Swagger UI/Scalar/Redoc) deployed and accessible | `curl -s -o /dev/null -w '%{http_code}' <docs-url>` must return 200 | Deploy `npx @redocly/cli build-docs openapi.yaml -o docs/` to CDN or static host |
| **API10** | Health check endpoints implemented (GET /health, GET /health/ready, GET /health/live) | `curl -s <base-url>/health \| jq '.status'` must return "healthy"; status code 200 | Add health endpoints from `templates/health-endpoints.yaml`. Kubernetes: configure livenessProbe + readinessProbe |
| **API11** | Bulk/async operations use 202 Accepted with status tracking; not synchronous 200 for 2s+ operations | `grep -cP 'POST.*process\|POST.*bulk\|POST.*import\|POST.*export' openapi.yaml \| grep -v '202'` — must return 0 | Async validator: `scripts/check-async-patterns.sh` — converts long-running POST endpoints to 202 + status polling |
| **API12** | Webhook/event subscription design documented with retry strategy and payload signing | `grep -cP 'webhook\|event.*subscription\|signature\|webhook.secret' openapi.yaml` | Template: `templates/webhook-design.md` — includes HMAC-SHA256 signing, exponential backoff retry, delivery dashboard |
| **API13** | API observability dashboards deployed (P50/P95/P99 latency, error rates by endpoint, consumer usage) | `curl -s -o /dev/null -w '%{http_code}' <grafana-dashboard-url>` must return 200 | Deploy `templates/api-dashboard.json` to Grafana — pre-configured with RED metrics (Rate, Errors, Duration) |
| **API14** | Consumer-facing changelog maintained with deprecation timelines and migration guides | `curl -s <changelog-url> \| grep -cP 'deprecat\|migration\|breaking\|upgrade'` — >= 1 entry | Template: `templates/api-changelog.md` — auto-generated from `openapi-diff` output with deprecation timeline |

## What Good Looks Like

> API consumers integrate in hours, not weeks. The specification is the source of truth — nothing ships that isn't documented. Breaking changes are rare and always communicated 6+ months ahead. SDKs in every target language stay in sync with the spec. Error messages tell consumers exactly what to fix. Your API feels like a product, not an afterthought.

## Footguns
<!-- DEEP: 10+min — war stories from production API design -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| API versioned 17 endpoints as `/v2/...` but 9 of them returned v1 response shapes because the version was in the URL path but not in the backend routing logic | A payment platform released API v2 with a new RFC 7807 Problem Details error format. They updated the gateway to route `/v2/*` to the v2 service. But 9 endpoints shared backend logic between v1 and v2 — the service didn't inspect which version was requested. V2 consumers received v1 error format: `{"error": "invalid_card"}` instead of `{"type": "https://...", "title": "Invalid Card", "status": 422, "detail": "..."}`. Client SDKs written against the v2 OpenAPI spec threw deserialization errors. Three large integrators spent 2 weeks debugging before the platform acknowledged the bug. The "v2" label was cosmetic for 53% of endpoints. | Versioning was implemented at the routing layer (URL prefix matching) without auditing whether every endpoint actually served the version it advertised. The URL path `/v2/` became a "namespace claim" rather than a behavioral contract. No contract testing verified that v2 responses matched the v2 OpenAPI response schemas. | **Contract-test every versioned endpoint against its published OpenAPI spec.** Use schema validation in integration tests: `assert response matches GET /v2/payments/200.schema.json`. Run these tests in CI on every PR. Maintain a version-to-schema mapping that's machine-readable, not documented in Confluence. If v2 shares logic with v1, add explicit version checks: `if (request.version === 'v2') return ProblemDetails.from(error)`. |
| Offset-based pagination with `?page=10000` on a 200M-row table took 45 seconds and locked the database — API consumers who scraped "all records" accidentally ran a DoS attack | A data export API used offset pagination: `GET /orders?offset=0&limit=100`. A customer's data pipeline called this endpoint in a loop: offset=0, 100, 200, ..., 99900. At offset=99900, PostgreSQL scanned 100,000 rows and discarded 99,900 of them to return the last 100. Query time grew linearly: page 1 = 8ms, page 100 = 450ms, page 1000 = 11 seconds, page 10000 = 45 seconds. Three customers ran simultaneous full exports during month-end close — the database CPU hit 100% for 22 minutes. The API was effectively self-DoS'd by its own pagination design. | Offset pagination on large datasets requires the database to count and skip rows — it scans every row up to the offset. This is O(n) in offset position. The API didn't enforce a maximum offset or offer cursor-based pagination as the default for large collections. | **Use cursor-based pagination for any collection that can exceed 1,000 records.** Pattern: `GET /orders?cursor=eyJpZCI6MTIzfQ&limit=100`. Cursors are opaque, stable, and O(1) regardless of position. If you must support offset, enforce a hard maximum (`max_offset=1000`) and return a `413 Payload Too Large` or `400 Bad Request` with a helpful error explaining how to use cursors. Expose cursor-based pagination as the default in SDKs and documentation. |
| Bulk operation endpoint returned `200 OK` when 30% of individual operations failed — the response body listed the failures but consumers only checked HTTP status codes | A bulk user import API accepted an array of 1,000 user records: `POST /users/bulk`. For 700 records, the import succeeded. For 300, it failed with validation errors (duplicate emails, missing required fields). The API returned `200 OK` with a response body: `{"succeeded": 700, "failed": 300, "errors": [...]}`. The customer's integration only checked `response.status === 200` and assumed full success. 300 users never got their welcome emails. The customer discovered this 48 hours later when support tickets arrived from users who "signed up but got nothing." Their data team spent 3 days reconciling the missing records. | The HTTP status code signaled "the request was processed" but not "the request was fully successful." Most HTTP clients treat any 2xx as success, and the consumer's integration predictably stopped at the status code check. The API violated the principle: status codes should reflect the worst outcome in the batch. | **Bulk endpoints with partial failures must return `207 Multi-Status` or `200 OK` with a top-level `hasFailures: true` flag that consumers can't ignore.** Better: return `200 OK` with a consistently structured response where consumers must iterate `results[].status` to confirm each item. SDKs should expose a method like `bulkCreate()` that throws if ANY item failed. Document the partial-failure contract in the API description: "This endpoint may return partial success. Always check per-item status." |
| Webhook signature verification was implemented but never tested with an actual webhook — HMAC validation silently accepted any payload because the comparison used `==` instead of a constant-time comparison function | A platform sent webhooks to customer endpoints with an `X-Signature: sha256=abc123...` header. The customer's verification code computed the HMAC and compared: `if (computed_signature == received_signature)`. This worked — the signatures matched. Six months later, a security audit revealed the comparison was vulnerable to timing attacks. Worse: when the webhook provider rotated their signing secret, the customer's verification silently failed. But the comparison logic had an unrelated bug where an empty `received_signature` evaluated to `true` (truthy string comparison). For 3 weeks, all webhooks were accepted without any signature validation — including 11 forged webhooks from an attacker who discovered the bug by probing the endpoint. | The HMAC comparison used `==` (standard string equality) instead of a constant-time comparison like `crypto.timingSafeEqual()`. Standard string equality short-circuits on the first differing byte, leaking timing information. The secondary bug (empty signature accepted) was never caught because there was no test for the "no signature" or "wrong signature" case. | **Always use constant-time comparison for HMAC validation:** `crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(received))`. Write webhook tests that cover: valid signature, invalid signature, missing signature header, expired timestamp, and replayed payload. Use the webhook provider's test mode or a mock server. Add a metric: `webhook_signature_validation_failures_total` — if this drops to zero unexpectedly, the validation may be silently broken. |
| Rate limiting configured per-endpoint at 100 req/min — but 40 consumers shared one corporate NAT gateway IP, so one consumer hitting the limit blocked all 39 others | A B2B API used IP-based rate limiting: each IP address got 100 requests per minute per endpoint. This worked for consumers with dedicated IPs. But 40 enterprise customers were behind a corporate NAT gateway — they all appeared as the same source IP. When Customer A ran a bulk export at 95 req/min, the rate limiter had only 5 req/min remaining for the other 39 companies. Customer B's real-time dashboard queries were throttled with `429 Too Many Requests`. Customer B's ops team was paged at 3:00 AM for "API outage" — the API was up, they were just sharing a rate limit bucket with someone else's batch job. | IP-based rate limiting assumes one IP = one consumer. This holds for server-side integrations with dedicated egress IPs but fails catastrophically for corporate networks, shared hosting, and mobile carriers — where hundreds of consumers share one IP. The rate limiter had no concept of consumer identity beyond the TCP source address. | **Use API-key-based rate limiting as the primary mechanism; fall back to IP-based only for unauthenticated endpoints.** Each API key gets its own rate limit bucket. If you must support IP-based limiting, use it as a secondary, more permissive limit (e.g., 1000 req/min per IP as a DoS protection floor, with 100 req/min per API key as the actual limit). Expose rate limit headers per consumer: `X-RateLimit-Remaining: 42` — so consumers can self-monitor. Add a `429` response body that names which limit was hit (key vs IP). |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You design endpoints by thinking about what your database schema looks like and exposing CRUD operations on each table | You design APIs by writing the consumer code first — the ideal client experience drives the endpoint shape, not the database schema — and you test every endpoint by integrating with it from a real SDK | A new developer integrates with your API in under 2 hours without reading documentation beyond the Quick Start guide — and when they hit an error, the response tells them exactly what to fix |
| Your error responses are `{"error": "something went wrong"}` with no structured format, no error codes, and no remediation hints | Every error response follows RFC 7807 with `type`, `title`, `status`, `detail`, and `instance` — and includes an actionable `hint` extension field telling the consumer what to do next | You deprecate a v1 endpoint used by 500+ active consumers and migrate 98% of them to v2 before the sunset date — with zero Sev1 incidents during the transition |
| You version APIs by slapping `/v2` on the URL and calling it a day — no deprecation policy, no migration guide, no sunset timeline | You maintain a public changelog, a deprecation calendar with 6-month notice periods, and automated emails to consumers whose traffic still hits deprecated endpoints | Your API design guidelines are adopted by 3+ teams outside your org, and an external developer writes a blog post titled "Why [Your Company]'s API is the best-designed I've ever used" |

**The Litmus Test:** Can a developer you've never met integrate with your API — authentication, first request, error handling, pagination — in under 15 minutes, without reading any documentation beyond the OpenAPI reference and the Quick Start guide?

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
