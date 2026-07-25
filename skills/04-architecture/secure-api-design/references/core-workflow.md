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
