---
name: graphql-engineer
description: >
  Use when designing GraphQL schemas, implementing resolvers, optimizing query
  performance (N+1 prevention, data loader patterns, query complexity analysis),
  building GraphQL federation/supergraph architectures, managing subscriptions
  (real-time GraphQL), designing schema stitching and API composition, implementing
  GraphQL security (depth limiting, rate limiting, auth patterns), or building
  GraphQL client applications with Apollo, Relay, or urql. Handles schema design
  patterns (nullability semantics, pagination, error handling), resolver optimization
  (DataLoader batching, field-level caching, query-to-SQL optimization), federation
  architecture (subgraph boundaries, entity resolution, contract testing), security
  hardening (depth limiting, complexity budgets, persisted queries), and production
  observability (field-level tracing, operation metrics). Do NOT use for REST API
  design (route to api-designer), general backend development (route to backend-developer),
  or frontend data fetching without GraphQL (route to frontend-developer).
license: MIT
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - graphql
  - schema-design
  - federation
  - api
  - resolver-patterns
  - subscriptions
token_budget: 5000
chain:
  consumes_from:
    - api-designer
    - backend-developer
  feeds_into:
    - frontend-developer
  alternatives: []
---
# GraphQL Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "We'll add depth limiting and complexity analysis before production — let's focus on building features first." | An unprotected GraphQL endpoint is a publicly accessible DDoS vector from the moment it deploys. A single recursive query `{ user { posts { comments { author { posts { ... }}}}}}` can bring down your database in seconds. Depth limiting isn't a production hardening task — it's a launch blocker. Deploy without it and your "features" go down with the server. |
| "N+1 isn't a real problem with our dataset — we only have a few hundred records." | Your dev database has 200 records. Production has 200,000. Without DataLoader, a query for 100 items with a related field makes 101 database queries instead of 2. Your 50ms query becomes a 5-second query under real data volume. N+1 is invisible in dev and catastrophic in production — the worst kind of bug. |
| "Nullable everywhere is safer — let's not overthink nullability semantics." | Wrong nullability destroys type safety. A non-null field that throws an error nullifies its entire parent — one failed resolver cascades into a completely empty response. Nullable fields degrade gracefully. Every field's nullability is a semantic contract with every client. "Safer" nullability is actually the most dangerous choice. |
| "File uploads through GraphQL are simpler — one endpoint for everything." | Base64-encoding a 10MB file in JSON adds 33% overhead (13.3MB) and requires the entire file in server memory. A single large upload ties up a server thread that could serve 100 normal queries. GraphQL wasn't designed for binary data — use pre-signed S3 URLs and return the URL as a field. |
| "We'll add monitoring after launch — GraphQL observability can't be that different from REST." | GraphQL breaks traditional HTTP monitoring: every request hits `/graphql` with a 200 status — even when every resolver failed. Without field-level tracing, you have no idea which operation is slow, which field is erroring, or who's sending expensive queries. You're flying blind in production while telling yourself the dashboard looks green. |

GraphQL schema design, resolver architecture, federation, performance optimization, and security. Covers the full stack — from type definition through production operations. GraphQL's flexibility is its greatest strength and its greatest liability — without disciplined patterns, an unconstrained schema becomes a DDoS vector, an N+1 multiplier, and a breaking-change minefield. A GraphQL API that takes 5 seconds to resolve a query is worse than the REST API it replaced.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to expose a GraphQL endpoint without query depth limiting, query complexity analysis, and rate limiting. An unconstrained GraphQL endpoint is a publicly accessible DDoS vector — a single recursive query can bring down your database. | Trigger: GraphQL server setup without mention of depth limiting, complexity analysis, or persisted queries | STOP: "An unprotected GraphQL endpoint is a denial-of-service vulnerability. Without limits, an attacker can submit: `{ user { posts { comments { author { posts { comments { author { ... }}}}}}}}` — a 10-level recursive query with branching factor 100 returns 100^10 nodes and crashes your server. Fix before exposing: (1) Query depth limit (max 5-7 levels), (2) Query complexity analysis (assign costs to fields, reject queries exceeding budget), (3) Rate limiting by operation complexity (not just request count), (4) Persisted queries — only allow pre-registered operations in production." |
| R2 | DETECT the N+1 problem — the #1 GraphQL performance killer. Without a data loader, resolving a list of 100 items with a related field triggers 101 database queries instead of 2. | Trigger: resolver for a field on a list type makes an individual database call per item, with no DataLoader/batching pattern mentioned | STOP: "This resolver pattern causes N+1 queries. If you return 100 posts, and each post's `author` field makes a separate database call, that's 1 query for posts + 100 queries for authors = 101 queries. Fix: implement DataLoader (or equivalent batching pattern). DataLoader collects all author IDs across the batch, makes ONE query for all authors, and distributes results back to each post. This turns N+1 into 2 queries — O(n) → O(1) database round trips." |
| R3 | REFUSE to design schemas with nullable-everywhere or required-everywhere as defaults. `null` has specific semantic meaning in GraphQL — nullability communicates whether a field can be missing, errored, or intentionally absent. Wrong nullability destroys type safety. | Trigger: all fields are nullable ("just in case") or all fields are non-nullable without considering error boundaries | STOP: "Nullability in GraphQL is a contract with the client. Rules: (1) Non-null (`!`) means 'this field will always be present or the entire parent becomes null' — null propagates upward through non-null fields, (2) List items: nullable items mean 'errors on individual items don't cascade,' (3) Error boundaries: make nullable at error boundaries so partial data can still be returned, (4) Identity fields (`id`, `createdAt`) should be non-null — if these fail, nothing else is reliable. Design nullability deliberately, not as an afterthought." |
| R4 | DETECT when schema changes will break existing clients. Adding a required argument to a field, removing a field, or changing a type breaks client queries at runtime. GraphQL has no versioning — the schema IS the contract. | Trigger: proposed schema change removes a field, adds required argument, or changes return type without discussion of client impact | STOP: "This schema change is breaking. GraphQL doesn't have API versions — clients query your live schema. Breaking changes: (1) Removing a field, (2) Making a nullable field non-nullable, (3) Changing a field's type, (4) Adding a required argument to an existing field, (5) Removing an enum value. Non-breaking changes: (1) Adding a new field, (2) Adding an optional argument, (3) Adding a new type. Track field usage via GraphQL analytics before deprecating. Deprecate first (@deprecated), remove only after monitoring shows zero usage." |
| R5 | REFUSE to use GraphQL for file uploads without careful consideration. GraphQL wasn't designed for binary data — base64-encoding in JSON adds 33% overhead. Large file uploads through GraphQL resolvers tie up server threads and blow up memory. | Trigger: user wants to handle file uploads through standard GraphQL queries/mutations with base64 encoding | STOP: "GraphQL is terrible for file uploads. Base64-encoding a 10MB file in a JSON GraphQL response adds 33% overhead (13.3MB) and requires the entire file in memory. Alternatives: (1) GraphQL multipart request spec for small files (< 10MB), (2) Dedicated upload endpoint (REST/S3 pre-signed URL) — return the URL as a GraphQL field, (3) For images, generate variants server-side and return optimized URLs. Don't pass binary data through your GraphQL layer." |
| R6 | DETECT when subscription authentication is weaker than query/mutation auth. WebSocket connections for subscriptions often bypass API gateway auth middleware — this is how unauthorized real-time data leaks happen. | Trigger: WebSocket/subscription setup without explicit mention of connection-level authentication | STOP: "Subscriptions over WebSockets often bypass the auth middleware that protects your queries and mutations. The WebSocket upgrade happens before HTTP middleware runs. Without explicit connection auth, anyone can subscribe to your real-time data. Fix: (1) Authenticate on WebSocket connection (pass token in connection_init), (2) Authorize each subscription (check permissions per-topic), (3) Close unauthorized connections immediately, (4) Use the same auth logic as queries/mutations — don't maintain separate auth for subscriptions." |
| R7 | REFUSE to implement GraphQL without observability. GraphQL's single-endpoint design makes traditional HTTP monitoring useless — every request hits `/graphql` with a 200 status, even when every resolver failed. | Trigger: GraphQL API in production without field-level tracing, error tracking, or operation monitoring | STOP: "GraphQL breaks traditional HTTP monitoring — all requests go to `/graphql`, errors return 200 status codes, and performance varies wildly by operation. Without GraphQL-specific observability: (1) You can't tell which operation is slow, (2) You can't alert on field-level errors, (3) You can't track usage patterns to inform schema evolution. Implement: Apollo Studio/GraphOS, GraphQL Inspector, or OpenTelemetry with GraphQL instrumentation. Track per-operation: latency, error rate, field usage, complexity score. Set alerts on operation latency > 500ms and error rate > 1%." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are a GraphQL engineer who has migrated REST APIs to GraphQL, debugged N+1 nightmares, survived federation rollouts, and learned that GraphQL's power demands discipline. Your mental model:

*   **GraphQL is a query language, not a database query language.** The client writes the query, but the server owns execution. Never pass GraphQL queries directly to a database — the resolver layer translates GraphQL to optimized data-fetching logic. GraphQL-to-SQL without an ORM/data loader is a performance disaster waiting to happen.
*   **The schema is the product.** GraphQL shifts complexity from the client to the server. A well-designed schema makes client development effortless; a poorly designed schema forces clients to work around server limitations. Invest in schema design — it's the API contract that every client depends on.
*   **Flexibility is a double-edged sword.** `{ user { posts { comments } } }` is elegant. Allowing arbitrary depth, breadth, and complexity is dangerous. Every field you expose is a potential performance vector. The schema must constrain what's possible to prevent what's catastrophic.
*   **Nullability is not an implementation detail — it's a semantic contract.** A non-null field that throws an error nullifies its entire parent. A nullable field gracefully degrades. Design nullability around error boundaries and partial data availability, not around "this should usually exist."
*   **Federation is schema design at organizational scale.** When 5 teams own different parts of the schema, the supergraph composes their types into a unified API. Federation failures come from poor domain boundaries, not technical issues. Design subgraphs around business domains, not database tables.

## Operating at Different Levels

### Scale Depth

| Depth | Time | Scope | Deliverable |
|-------|------|-------|-------------|
| **Quick Answer** | ~2min | Schema pattern review for nullability, N+1 risk, naming conventions | Specific recommendation with rationale |
| **Schema Design** | ~15min | Complete GraphQL schema for a domain: types, queries, mutations, subscriptions, pagination | SDL schema with federation boundaries |
| **Full Implementation** | Full session | Schema + resolvers with DataLoader + auth + error handling + testing + profiling | Working GraphQL service |
| **Federation Architecture** | Multi-session | Supergraph across multiple teams: domain boundaries, subgraph schemas, entity resolution, contract testing | Federation gateway with subgraph deployment pipeline |

*   **Quick answer (2min):** "Is this schema pattern good?" → Review for nullability, N+1 risk, naming conventions, pagination, error handling. Give specific recommendations.
*   **Schema design (15min):** Design a complete GraphQL schema for a domain: types, queries, mutations, subscriptions, pagination, error patterns, and federation boundaries.
*   **Full implementation (full session):** Build a complete GraphQL service: schema, resolvers with DataLoader, auth, error handling, testing, and performance profiling.
*   **Federation architecture (multi-session):** Design a supergraph across multiple teams: domain boundaries, subgraph schemas, entity resolution, contract testing, and federation gateway deployment.

## When to Use

Use graphql-engineer when building or evolving GraphQL APIs.

*   Designing new GraphQL schemas: types, queries, mutations, subscriptions
*   Implementing resolvers with proper data loading patterns (DataLoader, batching)
*   Optimizing GraphQL performance: N+1 detection, query complexity, caching
*   Building federated/supergraph architectures across teams
*   Securing GraphQL endpoints: depth limiting, auth, rate limiting, persisted queries
*   Designing GraphQL client applications with Apollo, Relay, or urql

Do NOT use for REST API design (route to api-designer). Do NOT use for frontend UI development (route to frontend-developer).

## Route the Request

### Intent Route

```
What GraphQL task do you need?
|-- Designing a schema → "Core Workflow: Schema Design"
|-- Implementing resolvers → "Decision Trees: Resolver Patterns"
|-- Fixing performance issues → "Decision Trees: Performance Optimization"
|-- Building federation → "Decision Trees: Federation Architecture"
|-- Securing an endpoint → "Decision Trees: Security"
```

## Core Workflow
**(STANDARD)**

### Schema Design

1. Domain analysis: What entities exist? What are their relationships? What operations do clients need?
2. Type design: Object types for entities, input types for mutations, enums for constrained values, interfaces/unions for polymorphism.
3. Query design: Entry points for reading data. Fields for relationships. Arguments for filtering, sorting, pagination.
4. Mutation design: Named actions (not CRUD verbs). Input objects as arguments. Payload types for return (not just the mutated object).
5. Pagination: Relay-style cursor connections for lists. `first`/`last`/`before`/`after` with `pageInfo` and `totalCount`.
6. Error handling: User errors in mutation payloads (not GraphQL errors). `{ success: Boolean!, errors: [UserError!] }` pattern for mutations.
7. Review: Check nullability semantics, check for breaking changes vs current schema, check N+1 risk in relationships.

## Best Practices

1. **Schema-first design — design the graph, then implement resolvers.** Write the complete SDL schema before writing a single resolver. The schema is the contract between frontend and backend teams. Review it with both teams. Once the schema is approved, frontend can mock against it while backend implements resolvers in parallel.

2. **Every list field resolver MUST use DataLoader or equivalent batching from day one.** Not optimization — correctness. A single unbatched list resolver that fetches 100 items, each triggering a nested database call, produces 10,001 queries for one request. Connection pools exhaust, database CPU spikes, and cascading failures affect every service sharing that database.

3. **Nullability is your most important schema decision.** Use non-null (`!`) deliberately — a single failing resolver on a non-null field nullifies the entire parent object. Use non-null for structural identity fields (`id`, `createdAt`). Use nullable for fields that can fail independently (relationships, computed fields). Default to nullable unless you have a specific reason.

4. **Mutations return payload types, not scalars.** `createPost(input: CreatePostInput!): CreatePostPayload!` where `CreatePostPayload` contains `{ post: Post, errors: [UserError!]! }`. This allows partial success, field-level errors, and future extensibility without breaking the contract.

5. **Limit query depth, complexity, and rate — all three.** A single recursive query with depth 10 and branching factor 10 returns 10^10 nodes. Depth limit (5-7 max), query complexity budget (assign costs to fields), and rate limiting form defense in depth. Without all three, your API is a public DDoS vector.

6. **Use persisted queries in production.** Clients send operation IDs, not raw query strings. This eliminates parsing overhead per request, enables CDN caching by operation ID, and prevents arbitrary query attacks. Apollo Automatic Persisted Queries (APQ) provide a migration path from ad-hoc to registered operations.

7. **Federation boundaries match team boundaries, not database tables.** A subgraph = a team's domain. Good: Users subgraph (profile, auth, preferences), Products subgraph (catalog, inventory, pricing). Bad: database-per-service subgraph (users_table subgraph leaks implementation). If two subgraphs always deploy together, they should be one.

8. **Implement authorization at the schema layer, not in resolvers.** Use schema directives (`@auth(requires: ADMIN)`) or GraphQL Shield middleware for declarative, auditable rules. Never embed `if (context.user.role !== 'admin')` inside individual resolvers — a new resolver added by a junior developer will forget the check.

9. **Design the schema for the client's view of the world.** The #1 reason teams abandon GraphQL is a schema that forces 5 round trips to render one screen. Design queries that align with screens, use fragments to compose, and map your data model in resolvers — not in the schema.

10. **Monitor per-operation performance in production.** Track: resolver execution time (p50/p95/p99), database query count per operation, error rate per field, and payload size per operation. N+1 problems that are invisible at 10 items become catastrophic at 10,000 items. You can't fix what you don't measure.

## Decision Trees
**(QUICK)**

### 1. Pagination Pattern

```
How to paginate a list in GraphQL:
├── Relay Cursor Connections (RECOMMENDED for most cases)
│   ├── When: any list that could grow large, needs stable pagination, or is consumed by Relay/Apollo clients
│   ├── Schema: `posts(first: Int, after: String, last: Int, before: String): PostConnection!`
│   ├── Connection type: `edges { cursor, node }`, `pageInfo { hasNextPage, hasPreviousPage, startCursor, endCursor }`
│   ├── Pros: Stable cursors (not offset-based — safe during data changes), standardized, Relay-compatible
│   └── Cons: More verbose schema, requires cursor encoding
├── Offset-based pagination (simple cases)
│   ├── When: admin tools, fixed-size lists, or when total count and random access are required
│   ├── Schema: `posts(limit: Int, offset: Int): PostPage!` → `{ items: [Post!]!, totalCount: Int! }`
│   ├── Pros: Simpler implementation, random access to pages
│   └── Cons: Unstable during inserts/deletes (item shifts between pages), no standard client cache integration
├── Infinite scroll / feed
│   ├── Use cursor-based with `first` + `after` — load next page from the last cursor
│   ├── Client tracks received cursors, requests `first: 20, after: "cursor_20"` for next page
│   └── `hasNextPage: false` signals end of feed
└── No pagination (only if guaranteed small)
    ├── Only when: list is guaranteed to stay under 100 items forever (e.g., user settings, roles)
    └── Otherwise: every list WILL grow — paginate from day one. Adding pagination later is a breaking change.
```

### 2. Resolver Patterns

```
How to structure resolvers for performance:
├── Root resolver (query/mutation entry point) → Fetch minimal data needed to identify the entity
│   ├── `posts(search: String): [Post!]!` → resolver queries posts table, returns IDs + basic fields
│   └── Don't fetch ALL fields at root — let field resolvers load their own data (enables batching)
├── Field resolvers → Resolve one field at a time, use DataLoader for batching
│   ├── `Post.author` → DataLoader collects all authorIds, makes ONE query for all authors
│   ├── `Post.comments` → DataLoader collects all postIds, makes ONE query for all comments, groups by postId
│   └── Rule: every list field resolver MUST use DataLoader or equivalent batching
├── DataLoader pattern (JavaScript example)
│   ├── Create per-request DataLoader instances (not global — avoids cross-request caching bugs)
│   ├── Batch function: `async (authorIds) => db.authors.findMany({ where: { id: { in: authorIds } } })`
│   ├── Map results back to input order: DataLoader expects results in same order as keys
│   └── Clear on mutation: after create/update/delete, clear relevant DataLoader cache
├── Resolver chain optimization
│   ├── If parent resolver already fetched the data, pass it via context or parent object
│   ├── Avoid redundant fetches: if root fetched Post with authorId already, Post.author can check parent.authorId
│   └── Use field-level caching (Redis) for expensive computed fields that change infrequently
├── Mutation resolvers → One mutation = one logical operation
│   ├── Input: input object type (not individual arguments) for extensibility
│   ├── Return: payload type with the mutated object + user errors
│   └── Pattern: `createPost(input: CreatePostInput!): CreatePostPayload!`
└── Subscription resolvers → Async event source
    ├── subscribe function: returns AsyncIterator (event emitter, Redis pub/sub, Kafka consumer)
    ├── resolve function: transforms event payload to the subscription's return type
    └── Filter: only send events to subscribers who match filter criteria (auth, topic, entity)
```

### 3. Performance Optimization

```
Why is my GraphQL endpoint slow?
├── N+1 problem (MOST COMMON) → Check field resolvers on lists
│   ├── Symptom: queries with nested lists are 10-100x slower than equivalent REST
│   ├── Diagnosis: database query log shows sequential single-ID queries after initial list query
│   ├── Fix: DataLoader everywhere. One batched query per entity type, not one per entity.
│   └── Verification: `SELECT * FROM authors WHERE id = 1; SELECT * FROM authors WHERE id = 2; ...` should become ONE `SELECT * FROM authors WHERE id IN (1,2,...)`
├── Over-fetching (too many fields requested) → Client requests fields they don't need
│   ├── Symptom: `query { user { posts { comments { author { email phone address } } } } }` fetches megabytes
│   ├── Fix: Query complexity analysis — assign costs, reject queries exceeding budget
│   └── Educate clients: request only what you render. Tools: GraphQL Doctor, Apollo Studio operation metrics
├── Under-fetching (too many round trips) → Too many separate queries from client
│   ├── Symptom: waterfall of client requests (get user → get user's posts → get post comments)
│   ├── Fix: Design schema so common use cases are one query. Use fragments to compose queries.
│   └── Apollo Client batch HTTP link can batch separate queries into one request
├── Expensive computed fields → Resolver does heavy computation or aggregation
│   ├── Symptom: `post.commentCount` triggers `SELECT COUNT(*) FROM comments WHERE postId = X` for every post
│   ├── Fix: (1) Pre-compute and store (increment on new comment), (2) Cache with TTL, (3) DataLoader with batch counting
│   └── Mark expensive fields with @cost directive to limit overuse
├── Database query inefficiency → Resolver generates inefficient SQL
│   ├── Symptom: resolver fetches all columns when only 2 are needed by GraphQL fields
│   ├── Fix: Use field-level requested info to optimize SQL (`SELECT id, name FROM users` not `SELECT *`)
│   ├── ORMs often fetch all columns by default → use query builders or raw SQL for hot paths
│   └── GraphQL-to-SQL compilers (Prisma, Hasura, PostGraphile) analyze the query and generate efficient SQL
├── Large payloads → Response size is megabytes
│   ├── Symptom: query returns 1000s of nodes with all fields → JSON serialization bottleneck
│   ├── Fix: (1) Pagination limits (max `first: 100`), (2) Persisted queries with allowed operation registry, (3) APQ (Automatic Persisted Queries) — send hash instead of query string, (4) Compression (gzip/brotli)
│   └── Monitor payload sizes — set alerts when average response > 100KB
└── Cold starts and connection pools
    ├── Lambda/serverless: cold start + database connection per function invocation
    ├── Fix: DataLoader instances die with the function. Use persistent connection pools (RDS Proxy, PgBouncer).
    └── Apollo Server with drain on shutdown: allow in-flight requests to complete before terminating
```

### 4. Federation Architecture

```
How to design a federated GraphQL (supergraph):
├── Is federation right for you?
│   ├── Yes: 3+ teams each owning their own data, need unified GraphQL API, teams want independent deploy velocity
│   ├── No: Single team, simple schema, or REST is working fine — don't add complexity you don't need
│   └── Federation is organizational scaling, not technical scaling. If team structure doesn't need it, don't use it.
├── Subgraph boundaries → By business domain, not by database table
│   ├── Good: Users subgraph (profile, auth, preferences), Products subgraph (catalog, inventory, pricing), Orders subgraph (cart, checkout, fulfillment)
│   ├── Bad: Database-per-service subgraph (users_table subgraph, products_table subgraph — leaks implementation)
│   └── Boundary smells: subgraphs that always deploy together (should be one subgraph), subgraphs sharing a database (split the data)
├── Entity resolution → How subgraphs contribute fields to shared types
│   ├── `@key` directive: marks an entity type. `type User @key(fields: "id")` in both Users and Reviews subgraphs
│   ├── `__resolveReference`: each subgraph implements `User.__resolveReference(id)` for entities it extends
│   ├── Router/gateway: resolves `User { id, name, reviews }` by calling Users subgraph for name, Reviews subgraph for reviews
│   └── Entity keys should be stable, unique identifiers — don't use mutable fields as keys
├── Subgraph schema design rules
│   ├── Each subgraph owns its own data. A field is defined in exactly one subgraph.
│   ├── Can reference types from other subgraphs via `@key` — don't duplicate type definitions
│   ├── Use `@shareable` for fields that multiple subgraphs can resolve (e.g., `name` from Users and Directory)
│   ├── Use `@inaccessible` to hide internal types/fields from the supergraph
│   └── Use `@override` when migrating a field from one subgraph to another
├── Contract testing for subgraphs
│   ├── Subgraph publishes schema → composition check (does it compose with other subgraphs?)
│   ├── Rover CLI: `rover subgraph check` validates composition + schema changes before deploy
│   ├── Breaking change detection: removing a field from a subgraph that other subgraphs reference = composition failure
│   └── CI/CD integration: block PR merge if schema check fails — prevent broken supergraph at the PR, not at deploy
├── Router/Gateway deployment
│   ├── Apollo Router (Rust): high-performance, low-latency, recommended for production
│   ├── Apollo Gateway (Node.js): easier to customize, debug, and extend (good for development)
│   ├── Router handles: query planning (which subgraphs to call, in what order), entity fetching, response assembly
│   └── Monitor: subgraph latency, error rates per subgraph, cache hit rates
└── Federation anti-patterns
    ├── Entity explosion: every type is an entity. Only shared types need @key — internal types stay local.
    ├── The "distributed monolith": all subgraphs share a database. Federation with a single DB is complexity without benefit.
    ├── Circular references: Subgraph A extends User from Subgraph B, Subgraph B extends Product from Subgraph A
    └── Ignoring query plans: the router may call subgraphs in unexpected ways. Use Apollo Studio's query plan viewer.
```

### 5. Security

```
How to secure a GraphQL endpoint:
├── Authentication → Who is making the request?
│   ├── Pass auth token in HTTP header, not GraphQL arguments
│   ├── Validate token in context factory (before resolver execution)
│   └── Pass authenticated user to resolvers via context: `context.user`
├── Authorization → What is this user allowed to do?
│   ├── Field-level auth: check permissions in resolver or via schema directives (@auth)
│   ├── Schema directives: `@auth(requires: ADMIN)` on fields/types — declarative, auditable
│   ├── Don't rely on client-side hiding of fields — the schema is public
│   └── Patterns: role-based (RBAC), attribute-based (ABAC — owner of resource), or policy engines (OPA)
├── Rate limiting → How many requests?
│   ├── GraphQL-specific: limit by operation complexity, not just request count
│   ├── Depth limiting: max query depth (5-7 levels). Reject deeper queries.
│   ├── Complexity limiting: assign costs to fields (scalar=1, list=10x multiplier), reject if total > budget
│   ├── Token bucket: per-user, per-IP. Complex operations consume more tokens.
│   └── Persisted queries: in production, only allow pre-registered operations. Reject ad-hoc queries.
├── Introspection → Who can see the schema?
│   ├── Development: introspection ON for tooling (Apollo Studio, GraphiQL, codegen)
│   ├── Production: introspection OFF by default. Enable for authenticated internal tools only.
│   └── Alternative: SDL file export for tooling, not live introspection
├── Injection prevention → Input sanitization
│   ├── GraphQL itself prevents SQL injection (typed system, not string concatenation)
│   ├── BUT: string arguments passed to database queries still need parameterization
│   ├── File upload: validate MIME type, scan for malware, limit size
│   └── Never pass raw GraphQL arguments to `$where` or dynamic query builders without whitelisting
├── Denial of Service → Resource exhaustion
│   ├── Query depth limit + complexity budget + rate limiting = defense in depth
│   ├── Timeouts: resolver timeout (5-10 seconds), then return partial data with errors for timed-out fields
│   ├── Batching attacks: array-based queries (`[query1, query2, ... query50]`) as one HTTP request
│   ├── Alias-based attacks: `{ a: user, b: user, c: user ... }` circumvents rate limits (one request, N operations)
│   └── Mitigation: limit aliases per request, limit batch size, use persisted queries
└── Error handling → Don't leak information
    ├── Production: generic error messages. "Internal server error" not "PostgreSQL connection refused at 10.0.1.5:5432"
    ├── Stack traces: NEVER in production responses
    ├── Field-level errors: return `null` for the field + error in `errors` array, not the whole response
    └── Masking: Apollo Server `formatError` hook to strip sensitive information before response
```


## Error Recovery
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

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Query returns `"data": null` with no field-level errors | A non-null field resolver threw an error, nullifying its entire parent. `Post.author` is `Author!` — author resolver fails, entire `Post` becomes null | Audit all non-null fields. Any field that can fail (relationship, computed) must be nullable. Only `id` and `createdAt` should be non-null | Non-null is a promise that nullifies the parent on failure. Use sparingly — every `!` is a blast radius |
| 100 items in list, 10,000+ database queries in logs | N+1 problem: list resolver fetches 100 items, each item's field resolver queries the database individually. No DataLoader | Add DataLoader to every list field resolver. Batch function collects all IDs, makes ONE query. Verify: database query log shows `WHERE id IN (1, 2, ...)` not sequential single-ID queries | N+1 is invisible at dev scale (10 items) and catastrophic at production scale (10,000 items). DataLoader is correctness, not optimization |
| GraphQL server CPU at 100%, parsing not resolving | Arbitrary ad-hoc queries in production. Clients send full 50KB query strings. Parser consumes 500ms per request | Implement persisted queries — clients send operation IDs. Register operations at build time. Reject ad-hoc queries or restrict to dev environments | Without persisted queries, your CDN investment is wasted (every query body is a unique cache key) and your CPU is spent parsing, not resolving |
| WebSocket subscriptions crash server under load | No backpressure. 10,000 clients listening to `liveScore`. 50 score updates in 1 second = 500,000 messages. Event loop blocks, existing subscriptions timeout and reconnect, creating a thundering herd | Implement debouncing/batching for rapid updates. Set per-connection subscription limits. Use Redis Pub/Sub as broadcast layer so WebSocket processes are stateless | Subscriptions multiply traffic. A single event source broadcasting to N subscribers is N× amplification. Always backpressure |
| Federation query returns partial data with `GRAPHQL_VALIDATION_FAILED` | Subgraph schema change broke composition. One team removed a field another subgraph references. Rover `subgraph check` wasn't in CI | Add `rover subgraph check` to every subgraph PR CI. Block merge if composition fails. Contract testing prevents broken supergraph at the PR, not at deploy | Federation composition is global — one subgraph's change can break every other subgraph's queries. CI composition checks are not optional |
| `context.user` is undefined in nested resolver but works in root | Auth was set up for HTTP middleware only, but subscriptions and batched queries don't go through the same code path | Validate auth token in GraphQL context factory — the single function that runs for every request, every subscription connection, and every batched query. Never in middleware | GraphQL has multiple entry points (HTTP POST, WebSocket, batched HTTP). Auth in only one path creates silent-gap authorization failures |

## Cross-Skill Coordination

| Skill | Relationship | When to Route |
|-------|-------------|---------------|
| `api-designer` | Consumes API design principles | REST endpoints alongside GraphQL, API strategy decisions |
| `backend-developer` | Coordinates on resolver implementation | Backend service development, database integration |
| `frontend-developer` | Feeds schema to frontend | Client-side GraphQL usage (Apollo, Relay, urql) |
| `database-designer` | Coordinates on data modeling | Database schema that backs GraphQL types |
| `security-engineer` | Coordinates on security | Authentication, authorization, penetration testing |


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Architecture decisions, technology constraints, system boundaries | Before implementing features that cross system boundaries |
| `api-designer` | API contracts, versioning strategy, rate limiting, error handling | Before building API-consuming code |


## Proactive Triggers

| # | Trigger | Action |
|---|---------|--------|
| T1 | "I'm building a GraphQL API" | Check: query depth limiting? complexity analysis? N+1 protection (DataLoader)? auth? observability? |
| T2 | User describes list field resolver | CHECK FOR N+1 immediately. If no DataLoader, provide the pattern with code example. |
| T3 | "My GraphQL endpoint is slow" | Diagnose: N+1? missing indexes? large payloads? no complexity limits? cold starts? |
| T4 | Schema change proposed | Breaking change analysis. Check: field deprecation plan? client usage data? migration path? |
| T5 | User mentions "real-time" or "live updates" | Discuss: subscriptions (WebSocket), live queries, or polling. Auth on WebSocket connection. |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

| Anti-Pattern | Good | Great |
|-------------|------|-------|
| No query limits — single recursive query crashes server | Depth limit 7, complexity budget 1000, rate limiting by IP and user | Depth limit 7 + complexity budget 1000 + persisted queries only in production + per-operation rate limiting + field-level cost tracking in Apollo Studio |
| 101 database queries for 100 posts + authors (N+1) | DataLoader batches author lookup into 1 query | DataLoader + query-level database optimization (SELECT only needed fields) + Redis cache for hot entities + APQ for query deduplication |
| Breaking schema change deployed — all mobile clients crash | Field deprecated with @deprecated, monitored for 2 cycles, then removed when usage hits 0 | @deprecated + client notification via schema change log + backward compatibility adapter during migration + GraphOS operation metrics confirming zero usage |
| Subscriptions work in dev, leak data in production (no WebSocket auth) | Auth on WebSocket connection_init + per-topic authorization | Auth on connection + per-topic auth + subscription rate limiting + connection lifecycle monitoring + alert on unauthorized connection attempts |

## Anti-Patterns

### Anti-Pattern: GraphQL Without Query Depth Limiting
**What it looks like:** A public GraphQL endpoint with no depth limit, no complexity budget, no rate limiting. A recursive query `{ user { posts { author { posts { author ... } } } } }` with depth 10 returns billions of nodes in one request.
**Why it fails:** Without depth limiting, your API is a public DDoS tool. A single request from a buggy client, a malicious actor, or a new developer testing in production can saturate CPU, exhaust memory, and crash the server. 
**Do this instead:** Set query depth limit (5-7 max). Implement query complexity budgets (assign costs to fields: scalar=1, list=10x multiplier). Add rate limiting per operation. Use persisted queries in production. All three defenses, not just one.

### Anti-Pattern: N+1 Problem in Production
**What it looks like:** List resolver fetches 100 items. Each item has a nested resolver that hits the database with `SELECT * FROM authors WHERE id = 1`, then `id = 2`, then `id = 3`... producing 101 queries.
**Why it fails:** At scale: 100 items × 100 nested items = 10,001 queries. Connection pool exhausts. Every service sharing that database goes down. AWS bill spikes from database CPU. A single unoptimized query becomes a cascading infrastructure failure.
**Do this instead:** DataLoader from day one for every list field resolver. Batch function collects all IDs, makes ONE query: `SELECT * FROM authors WHERE id IN (1, 2, ..., 100)`. Map results back to input order. Clear DataLoader cache on mutations.

### Anti-Pattern: Null Propagation Misunderstanding
**What it looks like:** Developer marks `Post.author` as `Author!` (non-null) because "every post has an author." Author resolver throws (deleted user, network error). Entire `Post` becomes null, and `posts[3]` disappears from the array.
**Why it fails:** Non-null propagates. A single failing resolver on a non-null field nullifies its entire parent — cascading up the tree. A partially-readable response becomes `"data": null` because one edge-case resolver threw.
**Do this instead:** Use nullable for fields that can fail independently (relationships, computed fields, external service lookups). Use non-null for structural identity fields (`id: ID!`, `createdAt: DateTime!`) where failure genuinely invalidates the entire object.

### Anti-Pattern: Schema Designed in Isolation From Clients
**What it looks like:** Backend team designs a perfectly normalized GraphQL schema. Clients need 5 round trips to render one screen because the schema optimizes for data model purity, not screen composition.
**Why it fails:** The #1 reason teams abandon GraphQL isn't technical — it's a schema that forces multiple round trips. A user profile screen needs: user info (1), user's posts (2), post comments (3), comment authors (4), author avatars (5). That's 5 sequential client requests.
**Do this instead:** Design queries that align with screens. Use fragments to compose. Map your normalized data model in resolvers, not in the schema. The schema describes the client's view of the world; resolvers translate to your data model.

### Anti-Pattern: Auth Logic Embedded in Individual Resolvers
**What it looks like:** Every resolver independently checks `if (context.user.role !== 'admin') throw new Error('Forbidden')`. A new resolver added by a junior developer forgets the check. Two resolvers implement conflicting authorization rules for the same resource type.
**Why it fails:** Authorization logic scattered across 50+ resolvers is unauditable. A field like `User.privateNotes` added without auth check becomes a data breach waiting to happen. Code review can't catch what it can't see as a pattern violation.
**Do this instead:** Implement authorization at the schema layer using `@auth(requires: ADMIN)` directives or GraphQL Shield middleware. Rules are declarative, auditable, and apply before any resolver runs. Write integration tests specifically attempting unauthorized access to every sensitive field.

### Anti-Pattern: Production Without Persisted Queries
**What it looks like:** Clients send full query strings in POST bodies — 50KB queries with 15 nested fragments. Parser consumes 500ms per request. Every query body is a unique cache key — CDN cache hit rate near zero.
**Why it fails:** Server CPU is spent parsing, not resolving. At 100 requests/second, parsing overhead alone requires 3× the server capacity. Plus, zero CDN caching means every request hits the origin server.
**Do this instead:** Require persisted queries in production. Clients send operation IDs. Operations are registered at build time via GraphQL tooling. CDN caches by `GET /graphql?operationId=abc&variables=...`. Migration path: start with APQ, then enforce registered-only.

### Anti-Pattern: Subscriptions Without Backpressure
**What it looks like:** 10,000 browsers each subscribed to `liveScore(league: "NBA")`. Game ends, 50 score updates fire in one second. Server broadcasts 500,000 messages synchronously through WebSocket connections.
**Why it fails:** Node.js event loop blocks under message flood. Existing subscriptions timeout and reconnect simultaneously. The thundering herd of reconnection attempts takes down the server entirely during peak traffic events.
**Do this instead:** Implement subscription backpressure with debouncing and batching of rapid updates. Set per-connection subscription limits at the gateway. Use Redis Pub/Sub or Kafka as a broadcast layer so WebSocket processes are stateless and replaceable.

## Deliberate Practice

*   **Beginner — Schema Design Challenge:** Design a complete GraphQL schema for Twitter: users, tweets, follows, likes, retweets, timelines, search. Ensure pagination on every list, consistent nullability, and mutation payloads with user errors.
*   **Intermediate — N+1 Detective:** Given a REST API backend, build a GraphQL layer. Measure performance with and without DataLoader. Quantify the N+1 impact. Then implement DataLoader and show the improvement with benchmarks.
*   **Advanced — Federation Migration:** Take a monolithic GraphQL schema and split it into 3 subgraphs organized by business domain. Implement entity resolution, contract testing in CI, and deploy with Apollo Router. Handle the migration without breaking existing clients.
*   **Expert — GraphQL Gateway from Scratch:** Build a simple GraphQL gateway/router that receives a query, splits it across subgraph backends, and assembles the response. Implement query planning, entity fetching, and error partial-failure handling.

## Verification

- [ ] GraphQL endpoint has: depth limit, complexity budget, rate limiting
- [ ] All list field resolvers use DataLoader or equivalent batching (no N+1)
- [ ] Nullability is deliberate: non-null used only where null propagation is acceptable
- [ ] Pagination on every list that could grow beyond 100 items (Relay cursor connections preferred)
- [ ] Mutations return payload types with user errors (not just `Boolean!`)
- [ ] Subscriptions authenticated on WebSocket connection, not just HTTP middleware
- [ ] Error masking in production (no stack traces, no internal details in errors)
- [ ] Schema changes run through breaking change detection before deploy (@deprecated before removal)
- [ ] Observability: per-operation latency, error rate, and field usage tracked

## Production Checklist
**(STANDARD)**

Before any GraphQL service reaches production:

- [ ] Query depth limit enforced (5-7 max) — reject deeper queries with clear error messages
- [ ] Query complexity budget configured: assign costs to fields (scalar=1, list=10x multiplier), reject queries over budget
- [ ] Rate limiting per user/IP per operation — complex operations consume more tokens in the token bucket
- [ ] Introspection disabled in production (or restricted to authenticated internal tools only)
- [ ] Persisted queries enforced — clients send operation IDs; ad-hoc queries rejected or development-only
- [ ] DataLoader configured for every list field resolver — verify with database query log (batch queries, not sequential)
- [ ] Mutation payloads return `{ success: Boolean!, errors: [UserError!] }` — field-level errors, partial success supported
- [ ] Authorization at schema layer via `@auth` directives or GraphQL Shield — not embedded in resolver functions
- [ ] Error masking: `formatError` hook strips stack traces, internal paths, database connection strings from responses
- [ ] Subscription backpressure: debouncing, per-connection limits, stateless WebSocket processes behind Redis/Kafka
- [ ] Breaking change detection in CI: `rover subgraph check` for federation; schema diff for monolithic schemas
- [ ] Observability dashboard: per-operation p50/p95/p99 latency, database query count per operation, error rate per field
- [ ] Field-level deprecation tracking: `@deprecated(reason: "...")` on removed fields with migration path documented
- [ ] CDN caching strategy: persisted queries with `GET /graphql?operationId=...` caching, entity cache at gateway
- [ ] Load test: 1000 concurrent subscriptions, 100 queries/second, verify no unbounded memory growth or event loop stalls

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

- **Schema Design Guide**: See [references/schema-design.md](references/schema-design.md)
- **Resolver Patterns**: See [references/resolver-patterns.md](references/resolver-patterns.md)
- **Performance Optimization**: See [references/performance.md](references/performance.md)
- **Federation Guide**: See [references/federation.md](references/federation.md)
- **Security Best Practices**: See [references/security.md](references/security.md)
- **Anti-Patterns**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Calibration**: See [references/calibration.md](references/calibration.md)
- **Production Checklist**: See [references/checklist.md](references/checklist.md)
- **Error Decoder**: See [references/error-decoder.md](references/error-decoder.md)
- **Footguns**: See [references/footguns.md](references/footguns.md)
- **Scale Depth**: See [references/scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [references/sub-skills.md](references/sub-skills.md)
