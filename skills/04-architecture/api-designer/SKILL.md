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

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "We'll add error responses and pagination later — right now we just need the happy path." | The moment your first consumer integrates, undocumented errors become de facto behavior they depend on. Adding pagination after launch means every client breaks when a list grows past what fits in memory. Cost of deferred API completeness: $30K-$100K in client breakage and emergency rework per endpoint. |
| "We don't need versioning yet — we'll never make breaking changes." | You will. Every API does. Without versioning infrastructure from day one, your first breaking change forces every client to update simultaneously. Mobile apps stuck in app review. Third-party integrations you forgot existed. Cost of deferred versioning: $50K-$200K in synchronized client breakage. |
| "Rate limiting is premature — we're not at scale yet." | A single buggy client retrying in a loop, or a malicious actor with a 20-line script, saturates your API servers and database with trivial requests. Cloud auto-scaling amplifies the cost into thousands of dollars in compute before you notice. Cost of no rate limiting: $10K-$100K in DDoS vulnerability and auto-scaling cost explosion. |
| "Sequential IDs in API responses are fine — nobody cares about revealing order counts." | Competitors scrape `/orders/4261` through `/orders/50000` and extract your entire customer count, growth rate, and order volume in 10 minutes. Every internal metric becomes public intelligence. Cost of exposing sequential IDs: $30K-$200K in competitive intelligence leakage and bulk data scraping incidents. |
| "Auth tokens in query parameters are fine — it's temporary." | Every CDN log, proxy log, browser history entry, and referrer header copies that token. Five+ locations you cannot audit or revoke. One log file leak = every token ever passed that way is compromised. Cost of query-param tokens: $50K-$500K in credential leak incidents and mandatory key rotation across all integrators. |

Design production-grade APIs across REST, GraphQL, and gRPC paradigms. This skill covers full API lifecycle design: specification-first development with OpenAPI 3.1, consistent error modeling, authentication and authorization patterns, rate limiting, pagination strategies, versioning approaches, and developer experience (DX) including SDK generation and documentation.

## Route the Request
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

**(QUICK)**

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
<!-- STANDARD: 3min -->

**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): API Paradigm Selection
1. **REST**: CRUD-heavy, document/collection-oriented, wide client audience, caching needs (HTTP caching), simple data shapes. Use when you need cacheability, discoverability (HATEOAS), and broad compatibility.
2. **GraphQL**: Complex client-driven data fetching, multiple frontend clients, nested/relational data, over-fetching/under-fetching problems. Use when frontend teams need flexible queries.
3. **gRPC**: High-performance service-to-service, streaming (bidirectional), strongly-typed contracts, polyglot microservices. Use Protocol Buffers for internal service mesh.
4. **WebSocket/SSE**: Real-time push, live updates, collaborative features, streaming events to browsers.

Complete when:
- API paradigm (REST/GraphQL/gRPC/WebSocket) selected with written rationale tied to use case requirements
- Decision documented with trade-offs: caching needs, client flexibility, performance requirements, team expertise
- Paradigm selection approved or acknowledged by consuming frontend/backend teams

### Phase 2 (~30 min): Specification-First Design
<!-- DEEP: 10+min -->
1. Write the OpenAPI 3.1 specification before implementation.
2. Define **paths** with clear resource naming: plural nouns (`/users`, `/orders`), nested for sub-resources (`/users/{id}/orders`), no verbs in URLs (except for non-CRUD actions like `/orders/{id}/cancel`).
3. Define **schemas** with complete property types, formats, constraints (minLength, pattern, enum), examples, and descriptions.
4. Define **responses** for all status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500) with consistent error body schema.
5. Add **security schemes** (Bearer JWT, OAuth2, API Key) and `security` requirements per operation.
6. Include `servers` with environment URLs, `tags` for grouping, `info` with version and contact.

Complete when:
- OpenAPI 3.1 specification written with all paths, schemas, responses, and security schemes defined
- Resource naming follows conventions: plural nouns, nested sub-resources, no verbs in URLs
- Spec validated by linter (e.g., spectral, redocly) with zero errors

### Phase 3 (~20 min): Consistency & Governance
<!-- DEEP: 10+min -->
1. **Error Schema** — Standardize on RFC 7807 Problem Details:

   ```json
   { "type": "https://api.example.com/errors/validation-error", "title": "Validation Error", "status": 422, "detail": "The 'email' field is required.", "instance": "/users/abc123", "errors": [{ "field": "email", "code": "required", "message": "Email is required" }] }

   ```

2. **Pagination** — Cursor-based (preferred for large/real-time datasets) or offset-based (simpler, acceptable for small datasets). Use envelope: `{ "data": [...], "pagination": { "cursor": "...", "hasMore": true } }`.
3. **Filtering & Sorting** — Query parameters: `?filter[status]=active&filter[createdAt][gte]=2024-01-01&sort=-createdAt&fields=id,name,email` (sparse fieldsets).
4. **Idempotency** — Require `Idempotency-Key` header for mutating operations (POST/PUT/PATCH/DELETE); return stored response for duplicate keys.

Complete when:
- RFC 7807 Problem Details error schema standardized and applied across all endpoints
- Pagination strategy (cursor-based or offset-based) selected and enforced with consistent envelope format
- Filtering, sorting, sparse fieldsets, and idempotency conventions documented in API style guide

### Phase 4 (~15 min): Versioning & Lifecycle
1. **URL path versioning** (`/v1/users`) — explicit, simple, allows major breaking changes. Preferred for public APIs.
2. **Header versioning** (`Accept: application/vnd.api+json; version=1`) — cleaner URLs but harder to explore.
3. **Deprecation** — Use `Sunset` and `Deprecation` HTTP headers; emit `Deprecation` notice in API changelog at least 6 months before removal.
4. **Sunset policy**: vN supported for 12 months after vN+1 release.

Complete when:
  Complete when: Architecture decision record (ADR) created with context, options, and rationale.
  Complete when: Non-functional requirements documented — performance, security, scalability targets.
  Complete when: Dependency graph reviewed — no circular dependencies between bounded contexts.
  Complete when: Capacity planning estimates validated with load testing at 2x expected peak.
- Versioning strategy (URL path vs header) selected and documented with rationale
- Deprecation policy defined: Sunset/Deprecation headers, changelog notification process, minimum 6-month notice
- Sunset timeline documented: vN supported for 12 months after vN+1 release

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | system-architect | System boundaries, service topology, API surface area decisions |
| **This** | api-designer | OpenAPI 3.1 specs, error models, pagination conventions, rate limiting policies |
| **After** | backend-developer | Consumes API contract to implement endpoints, validation, and middleware |

Common chains:
- **Greenfield service**: system-architect → api-designer → backend-developer — Architecture defines boundaries, API design formalizes the contract, backend implements it
- **Data-driven API**: database-designer → api-designer → frontend-developer — Schema shapes the resources, API exposes them, frontend consumes them

## Best Practices
<!-- STANDARD: 3min -->

1. **Specification-first, never code-first.** Write OpenAPI 3.1 before implementation. The spec is the contract — nothing ships that isn't documented. Generate mock servers from specs during development.

2. **Use RFC 7807 Problem Details for all errors.** Consistent error schema with `type`, `title`, `status`, `detail`, and `instance` fields. Every 4xx and 5xx response conforms to the same envelope — no per-endpoint error formats.

3. **Version with URL path for public APIs.** `/v1/users` is explicit, cacheable, and discoverable. Header versioning only for internal APIs with <10 consumers. Maintain N-1 version for the full deprecation window.

4. **Cursor-based pagination for mutable datasets.** Stable sort order with tiebreaker column (UUID or `id`). Offset-based pagination acceptable only for static datasets <10K records with simple jump-to-page UX.

5. **Require Idempotency-Key for all mutating endpoints.** Server-side key storage with 24h TTL in Redis. Payments, order creation, and resource provisioning must be idempotent — network retries are inevitable.

6. **Rate limit at the gateway, not in application code.** Per-consumer quotas with burst allowance. Return `429 Too Many Requests` with `Retry-After` header. Use `RateLimit-*` IETF draft headers for transparency.

7. **Deprecate before you remove.** Announce with `Sunset` and `Deprecation` HTTP headers. 6-month minimum grace period for public APIs, 3-month for internal. Enforce sunset dates in infrastructure — automated shutdown after deadline.

8. **Design from the consumer's perspective.** Write the client code first before designing endpoints. If the consumer needs 3 API calls to assemble a single view, the API resource model is wrong.

9. **Never expose internal database IDs.** Use UUIDv7 or ULID for all external-facing identifiers. Sequential IDs leak business metrics (customer count, growth rate) and enable enumeration attacks.

10. **Rotate API keys with overlapping validity windows.** Short-lived access tokens (1-24h) with refresh token rotation. Log and alert on anomalous key usage patterns. Never accept API keys in URL query strings — they land in server access logs.

## Error Recovery
<!-- STANDARD: 3min -->

**(STANDARD)**

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
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---------|--------|-----|
| Designing a new endpoint consumed by a mobile app | Propose response size budgets (≤50KB per payload), partial response via sparse fieldsets (`?fields=`), and delta sync endpoints. Discuss offline-first patterns (ETag + If-None-Match) before designing the resource shape | Mobile clients on spotty networks need lean payloads. A 2MB JSON response that works in the browser will crash a mobile app on 3G. Retroactively trimming payloads after mobile integration causes cascading rework |
| Choosing between REST and GraphQL for a multi-client platform | Before deciding, map each client's data needs: web needs aggregated dashboards, mobile needs flat lists, third-party needs stable envelopes. If 3+ clients need different field subsets from the same resources, strongly recommend GraphQL with persisted queries and query cost analysis | REST forces over-fetching when clients have heterogeneous data needs — mobile pulls 40 fields to render 3, third-party clients break when new fields appear. GraphQL shifts the shaping burden to the server where it belongs |
| Designing a public API consumed by external developers | Propose an API gateway layer with per-consumer rate limiting, API key rotation policies, and a developer portal with interactive docs BEFORE the first endpoint is built. Plan SDK generation pipeline (OpenAPI Generator) and consumer notification channels (changelog, deprecation calendar) | Public APIs are products, not internal plumbing. Without gateway-level consumer management from day one, you'll be retrofitting auth, rate limiting, and documentation after external devs have already built brittle integrations against raw endpoints |
| Adding a new field to an existing API response | Before making the field `required`, ship it as optional for 2+ release cycles. Add deprecation headers to any fields being replaced. If the field changes response semantics (e.g., price format, status enum), propose a minor version bump with backward compatibility | Required fields in additive changes break strict deserializers (mobile, TypeScript strict mode). A "minor" addition that crashes every iOS app is a production incident disguised as a feature. Grace periods save consumer relationships |
| Designing an endpoint that connects to an upstream backend service mesh | Propose circuit breaker configuration (e.g., 50% error rate → open), request timeouts aligned to upstream SLOs, retry budgets (max 3 with exponential backoff + jitter), and bulkhead isolation. Discuss whether the API should return stale cached data vs 503 when upstreams degrade | APIs that blindly forward failures from 5 upstream services cascade latency. A 200ms P95 backend timeout combined with 3 retries and no circuit breaker becomes a 2.5s response — 12x worse. Graceful degradation keeps the API responsive even when backends are not |
| Switching an existing REST endpoint to WebSocket for real-time updates | Before upgrading, verify: (a) load balancer config supports WebSocket upgrade headers and connection draining, (b) CDN/proxy layers don't buffer or strip `Upgrade: websocket`, (c) auth tokens are passed on connect (not per-message), (d) reconnection with exponential backoff is client-implemented | Load balancers and CDNs configured for short-lived HTTP/1.1 connections silently drop WebSocket upgrades. Connection count per instance skyrockets. Without proper reconnection logic, clients hang forever on stale sockets thinking they're connected |
| Designing idempotency for payment or order-creation endpoints | Propose `Idempotency-Key` header with server-side key storage (Redis with 24h TTL). The key must be generated by the client, not the server. Response includes `Idempotency-Replay: true` header when returning a cached response. Implement key collision detection for duplicate submissions from different clients | Payment gateways charge twice when retries aren't idempotent. Network blips cause client retries that create duplicate orders. Telling users "check if your order went through" is not a production strategy — idempotency keys make retries safe by design |

## State Log
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

- [ ] **[API1]** OpenAPI 3.1 spec validated with zero errors (`redocly lint` or `spectral lint`)
- [ ] **[API2]** All endpoints have request/response examples and complete error schemas (400, 401, 403, 404, 409, 422, 429, 500)
- [ ] **[API3]** Pagination on all list endpoints — cursor-based for mutable data, offset-based only for static datasets <10K
- [ ] **[API4]** Idempotency-Key required on all POST/PUT/PATCH/DELETE, server-side key storage with 24h TTL
- [ ] **[API5]** Rate limiting at API gateway — per-consumer quotas, 429 with `Retry-After` header, `RateLimit-*` headers
- [ ] **[API6]** Versioning strategy documented — URL path for public, header for internal. Deprecation: 6-month grace with `Sunset`/`Deprecation` headers
- [ ] **[API7]** Public identifiers are non-sequential (UUIDv7/ULID) — no auto-increment database keys exposed in responses
- [ ] **[API8]** Authentication: short-lived tokens (1-24h) with refresh rotation, API key rotation with overlapping validity windows
- [ ] **[API9]** SDK generation pipeline from OpenAPI spec — OpenAPI Generator with CI validation on every spec change
- [ ] **[API10]** Contract tests in CI: consumer-driven contract tests verify that responses match spec schemas
- [ ] **[API11]** All breaking changes go through new API version — never remove, rename, or change types of fields in-place
- [ ] **[API12]** `additionalProperties: false` set on all request body schemas — silent field acceptance caught at validation
- [ ] **[API13]** API changelog published, consumer notification channel active, deprecation calendar visible to all integrators

## What Good Looks Like
<!-- STANDARD: 3min -->

> API consumers integrate in hours, not weeks. The specification is the source of truth — nothing ships that isn't documented. Breaking changes are rare and always communicated 6+ months ahead.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice
<!-- STANDARD: 3min -->

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

## Anti-Patterns
<!-- STANDARD: 3min -->

- **Breaking API change without versioning.** Renaming a field, changing a type, or removing an endpoint without a deprecation window breaks every client that depends on the old contract. Mobile apps that update slowly, third-party integrations you didn't know existed, and internal services all fail simultaneously. The support tickets, incident response, and emergency hotfix cost dwarf the time saved by "just changing it." **Total cost: $50,000-$200,000 in client integration breaks, support escalations, and emergency rollbacks.** Fix: Never remove or rename — only deprecate with a documented sunset window; use API versioning (URL path or header-based) before any breaking change; run contract tests in CI.
- **REST API without rate limiting.** An unauthenticated endpoint with no rate limit is a DDoS vector. A buggy client retrying in a loop, or a malicious actor, can saturate your API servers and database with trivial requests — taking down the entire service for all users. Cloud auto-scaling can amplify the cost into thousands of dollars in compute before you notice. **Total cost: $10,000-$100,000 in DDoS vulnerability, auto-scaling cost explosion, and incident response.** Fix: Apply rate limiting at the API gateway layer (per IP for unauthenticated, per API key/token for authenticated); implement exponential backoff guidance in error responses; set aggressive rate limits as the default, not an afterthought.
- **OpenAPI `additionalProperties` defaults to `true`** in JSON Schema. If your spec doesn't explicitly set it to `false`, clients will silently accept extra fields. Every request body schema needs `"additionalProperties": false`.
- **PATCH with `application/merge-patch+json`** (RFC 7396) uses `null` to mean "delete this field." But `application/json-patch+json` (RFC 6902) uses `{"op": "remove", "path": "/field"}`. Clients that send the wrong content type will corrupt data — `null` becomes a literal null value instead of a deletion.
- **Cursor-based pagination** with `?after=xxx` requires a stable, unique sort order. Using `created_at` alone breaks when two records have the same timestamp. Always add a tiebreaker column (usually `id`).
- **Rate limit headers** `X-RateLimit-Remaining` — if your gateway strips custom headers or renames them, the client sees no rate info. `RateLimit-*` (IETF draft) headers are increasingly preferred. Support both.
- **`202 Accepted`** means "I queued this, no guarantee of completion." Clients that treat 202 as success will assume the resource exists when it may still be processing. Always include a `Location` header pointing to a status endpoint.
- **API versioning in the URL path** (`/v1/users`) means every route has a version prefix. When you add `/v2/users`, the old `/v1/users` route still needs maintenance until deprecated. URL versioning creates N copies of every endpoint.
- **Exposing sequential internal database IDs in API responses.** Using auto-increment integer IDs (`/users/4261`) leaks competitive intelligence — anyone can scrape your API and estimate total customer counts, growth rate, and order volume by sampling IDs. Sequential IDs also enable trivial enumeration attacks: an attacker iterates `/orders/1` through `/orders/100000` and extracts every customer's purchase history, shipping address, and payment metadata. **Total cost: $30,000-$200,000 in data exposure incidents, competitive intelligence leakage, and security incident response from bulk data scraping.** Fix: Use non-sequential, non-guessable identifiers (UUIDv4, ULID, or Snowflake-style IDs) in every public API response; never expose internal primary keys or auto-increment values; add authorization checks that verify the requesting principal owns the resource, not just that the ID resolves.
- **No published deprecation and sunset policy.** APIs evolve and endpoints are replaced, but without a communicated deprecation timeline clients never migrate. Years later you're maintaining `/v1/reports` (XML-SOAP), `/v2/reports` (REST-JSON), and `/v3/reports` (GraphQL) simultaneously — each with independent bugs, security vulnerabilities, and infrastructure costs. Three versions of the same feature drain 3x engineering budget on maintenance alone. **Total cost: $20,000-$60,000 per year per deprecated-but-not-sunset API version in maintenance engineering time, security patching, and server costs.** Fix: Publish a deprecation policy with fixed timelines (announcement → 6-month grace → 3-month sunset warning → removal); communicate via `Sunset` and `Deprecation` HTTP headers on every versioned response; track active client versions at the API gateway and proactively reach out to stragglers; enforce the sunset date in infrastructure (automated shutdown after deadline).
- **Static API keys that never expire.** Long-lived API keys hardcoded in client configs, mobile app binaries, and third-party integration scripts are never rotated. When a key leaks — via an accidental GitHub commit, a former employee's laptop, or a compromised CI pipeline — every system using that key is exposed until someone notices, and there's no audit trail of which keys are active, who owns them, or when they were last used. **Total cost: $50,000-$500,000 in security breach costs from leaked static API keys, including incident response, mandatory customer notification, and credential rotation across all integrators.** Fix: Issue short-lived access tokens (1-24 hours) with refresh token rotation; support API key rotation with overlapping validity windows so clients transition without downtime; log and alert on anomalous key usage patterns; never accept API keys in URL query strings where they land in server access logs.

## Gotchas
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| No pagination on list endpoints from day 1 — breaking change when data grows | $100K-$300K in breaking changes when clients break after adding pagination | Add pagination (cursor-based preferred) to ALL list endpoints in v1. Default page size: 25-100. Document pagination contract in OpenAPI |
| Inconsistent error response format across endpoints | $50K-$200K in client-side parsing bugs and integration delays | Define a single ErrorResponse schema (code, message, details, request_id). Use it for ALL 4xx and 5xx responses |
| No rate limiting design in API contract — uncontrolled traffic spikes | $200K-$1M in infrastructure costs from uncontrolled client traffic spikes | Document rate limits in OpenAPI spec using X-RateLimit headers. Implement per-user/per-endpoint throttles before launch |
| Versioning strategy not decided upfront | $150K-$500K in migration costs when breaking changes force a new version | Choose URL path vs header vs query param versioning before v1 ships. Document sunset policy. Never remove fields without deprecation period |

## Verification
<!-- STANDARD: 3min -->

- [ ] Run OpenAPI validator: `redocly lint openapi.yaml` or `spectral lint openapi.yaml` — zero errors
- [ ] Generate and inspect docs: `redocly build openapi.yaml` — all endpoints documented, all schemas have examples
- [ ] Test with mock server: `prism mock openapi.yaml` and `curl` each endpoint — responses match schema
- [ ] Verify pagination: all list endpoints return `next`/`cursor` link when more results exist
- [ ] Verify error responses: every endpoint's 4xx and 5xx responses match `ErrorResponse` schema
- [ ] Check `servers[].url` in OpenAPI: matches all environments (dev/staging/prod), no localhost URLs

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| API v1 client breaks after deploying v2 — clients get HTTP 400 or deserialization errors | Field removed from response schema without deprecation window. API assumed single client version, but mobile apps lag backend deploys by weeks | Never remove fields — deprecate first with `deprecated: true` in OpenAPI. Add new field alongside old. Remove only after monitoring shows zero traffic to deprecated field for 2 release cycles | APIs are forever. The cost of carrying a deprecated field for 6 months is near zero. The cost of breaking a mobile client is an emergency App Store review and angry users. |
| `GET /users` returns 200 with empty array when auth token is expired — client thinks user has no data | API uses HTTP 200 for business-layer errors. Authentication failure, authorization failure, and "no results" all return 200 with different JSON shapes | Use HTTP status codes as designed: 401 for expired/missing auth, 403 for insufficient permissions, 200 for successful empty result set. Clients can then handle auth errors globally instead of parsing every response body | HTTP status codes are part of your API contract. When you misuse them, every client must implement custom error parsing that will be wrong in subtle ways. |
| Pagination cursor breaks after database migration — clients loop forever on the same page | Cursor encoded database-internal ID that changed during migration (auto-increment reset, UUID format change). Clients held cursors across the migration window | Use opaque, signed tokens for cursors: `base64(json({id, seq}) + hmac)`. Decode server-side to resolve actual database offset. Cursors survive schema changes, database migrations, and replica lag | Never leak internal IDs in pagination tokens. Opaque cursors with HMAC signatures let you change internal representation without breaking every client's pagination state. |
| Rate limit of 100 req/min per user is bypassed by creating multiple API keys | Rate limit keyed on API key, not user identity. Malicious user generates 50 API keys and gets 5000 req/min effective limit | Key rate limits on `(user_id, endpoint)` not `(api_key, endpoint)`. Enforce per-user concurrency limits independent of key count. Alert on rapid API key creation | Rate limit on identity — not credentials. If your limit is per API key, you haven't limited anything; you've just added a key generation step. |
| `POST /orders` succeeds (201) but order never ships — no idempotency, client retried after network timeout | Network timeout on client side after server processed request. Client retried with same payload, creating duplicate order. No idempotency key on the endpoint | Require `Idempotency-Key` header on all mutating endpoints. Server stores (key, response) for 24h. Duplicate key returns stored response — not a new resource | Every POST/PATCH/PUT that changes state needs idempotency. Network is unreliable; retries are inevitable. Without idempotency, retries are duplicates. |
| OpenAPI spec says `price` is `integer` but actual response is `"19.99"` — client's strict parser rejects it | Spec written manually, diverged from implementation. No contract testing to catch the mismatch. API evolved in code but spec wasn't updated | Generate OpenAPI spec from code (not manually). Run contract tests in CI: `openapi-enforcer` or `dredd` validates actual responses against spec. Spec becomes build artifact, not documentation | If your spec and your code live in different files and aren't tested together, they diverged the moment you wrote the first line. Contract tests or spec generation — pick one, but enforce it. |

## References
<!-- STANDARD: 3min -->
- **"Is REST Overkill?" Decision Tree**: See ["is-rest-overkill?"-decision-tree.md](references/"is-rest-overkill?"-decision-tree.md)
- **Versioning Cost Analysis**: See [versioning-cost-analysis.md](references/versioning-cost-analysis.md)
