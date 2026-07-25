## Core Workflow

### Phase 1: OAuth2/OIDC Design

Execute in order. Do not skip steps.

```
1. IDENTIFY CLIENT TYPE AND ARCHITECTURE
   |-- Public client (SPA, mobile app, CLI): Cannot securely store a client secret
   |   |-- Authorization Code with PKCE (RFC 7636) — MANDATORY
   |   |-- Code verifier: 43-128 character random string, SHA-256 hashed for code challenge
   |   |-- NO implicit grant, NO client secret in frontend code
   |-- Confidential client (server-side web app, backend service): Can store client secret
   |   |-- Authorization Code with PKCE (preferred) OR client_secret_post/client_secret_basic
   |   |-- Client secret stored in secrets manager, rotated every 90 days
   |   |-- Confidential client designation requires: server-side execution, no source-visible secret
   |-- Machine-to-machine (service account): No user involved
   |   |-- Client Credentials grant with mTLS or private_key_jwt for client authentication
   |   |-- JWT profile (RFC 7523) or client_assertion with short-lived tokens
   |   |-- Scopes MUST be whitelisted per client — never grant openid or admin scopes to service accounts

2. SELECT GRANT TYPE
   |-- Authorization Code + PKCE: For any flow involving user interaction (web, mobile, SPA, CLI, TV)
   |   |-- S256 code challenge method ONLY (plain is vulnerable to code interception)
   |   |-- State parameter (CSRF protection): cryptographically random, one-time use, validated on callback
   |   |-- Redirect URI: exact match validation (no pattern matching, no open redirect)
   |-- Client Credentials: For service-to-service with no user context
   |   |-- Client authentication: mTLS > private_key_jwt > client_secret_post > client_secret_basic
   |   |-- NEVER use client credentials for user-facing flows (loses user context, no consent prompt)
   |-- Device Code (RFC 8628): For input-constrained devices (TV, IoT, CLI on remote machine)
   |   |-- Rate limit /device/code endpoint (5 requests/minute per IP to prevent polling abuse)
   |   |-- Interval: minimum 5 seconds between polling — slower for long-lived devices
   |-- Refresh Token: For offline access and silent token renewal
   |   |-- Rotation: issue new refresh token on each use, invalidate old one (RFC 6819 §5.2.2.1)
   |   |-- Reuse detection: if a revoked refresh token is reused, revoke ALL tokens for that user+client
   |   |-- Maximum lifetime: 90 days (confidential), 30 days (public), configurable

3. CONFIGURE TOKEN LIFETIMES AND CLAIMS
   |-- Access token: 5-15 minutes (shorter = smaller stolen token window)
   |   |-- Longer allowed only with: token introspection on every request OR DPoP (RFC 9449) binding
   |-- Refresh token: 90 days rotating, 7 days absolute max for public clients
   |-- ID token (OIDC): 5-10 minutes — only needed at authentication time, not for API access
   |-- Claim minimization: include only what resource servers actually need
   |   |-- sub (subject identifier): unique, stable, pairwise by default (prevent correlation across clients)
   |   |-- NEVER include: internal user IDs, database row IDs, email unless explicitly needed
   |   |-- NEVER include: passwords, hashes, PII (SSN, DOB), internal role names without review
   |-- audience (aud): MUST match the resource server's expected identifier — strict string comparison
   |-- issuer (iss): MUST be the authorization server URL, HTTPS only

4. IMPLEMENT TOKEN VALIDATION (Resource Server Side)
   |-- Algorithm validation: only accept RS256/ES256 — reject none, HS256, and any algorithm not in allowlist
   |-- Signature verification: fetch JWKS from authorization server, cache with 5-minute TTL
   |-- Claim validation: exp (not expired), nbf (not before now), iss (matches expected), aud (contains this server)
   |-- Scope validation: token scopes cover the requested operation — scp claim (RFC 8693) or scope claim
   |-- Token introspection (optional but recommended): call /introspect endpoint for active state check
   |   |-- Cache introspection results for 30 seconds to reduce load
   |   |-- Fallback: if introspection server is unreachable, deny (fail closed, NEVER fail open)

5. SECURE THE AUTHORIZATION SERVER
   |-- Signing keys: RSA 2048-bit minimum or ECDSA P-256, stored in HSM or KMS (never on disk in plaintext)
   |-- Key rotation: publish new keys to JWKS endpoint 24 hours before using them for signing
   |   |-- Overlap period: both old and new keys valid for 24 hours (prevent validation failures)
   |   |-- Revoke old keys: remove from JWKS after all tokens signed with old key have expired
   |-- Rate limiting: /authorize (100/min/IP), /token (20/min/client), /introspect (1000/min/service)
   |-- Open redirect prevention: exact redirect_uri matching, no wildcards, no unregistered URIs
```

### Phase 2: Access Control Model Design

```
1. CLASSIFY ACCESS PATTERNS
   |-- Coarse-grained, static: User type determines access broadly (admin, editor, viewer)
   |   |-- -> RBAC: roles assigned at user creation, permissions attached to roles
   |-- Context-sensitive: Access depends on attributes (department, clearance, geo, time, device)
   |   |-- -> ABAC: policies evaluate user attributes + resource attributes + environment attributes
   |-- Relationship-based: Access depends on how entities relate (user is member of project, document owned by team)
   |   |-- -> ReBAC: authorization decisions traverse relationship graph (Google Zanzibar model)
   |-- Complex, multi-dimensional: Mix of roles, attributes, and relationships
   |   |-- -> Hybrid: RBAC for base roles + ABAC for context + ReBAC for ownership/group membership

2. SELECT MODEL
   |-- RBAC: Best for internal tools, admin panels, CMS — where roles are few and well-defined
   |   |-- FLAT roles preferred: max 20-30 roles, max 2-3 hierarchy levels
   |   |-- Role explosion prevention: permission groups (composable) instead of role-per-permission
   |   |-- Example: editor_read + editor_write + editor_publish = 3 permission groups, not 7 roles
   |   |-- Audit: who-has-permission query must return in <1 second
   |-- ABAC: Best for regulated industries, multi-tenant SaaS, government — where context drives access
   |   |-- Policy engine: OPA (Rego), AWS Verified Permissions (Cedar), or custom PDP
   |   |-- Attribute sources: LDAP/AD (user attrs), CMDB (resource attrs), device management (device attrs)
   |   |-- Watch for: attribute staleness — cached attributes that don't reflect real-time changes
   |   |-- Performance: attribute retrieval at decision time creates latency — precompute where possible
   |-- ReBAC: Best for collaboration tools, social platforms, project management — where relationships matter
   |   |-- Schema design: namespace -> relation -> object (e.g., document:viewer@user:alice)
   |   |-- Zanzibar consistency model: eventually consistent with zookies for staleness protection
   |   |-- Implementation options: SpiceDB (Authzed), OpenFGA, or custom Zanzibar-inspired
   |   |-- Beware: relationship graph traversal can be unbounded — set max depth (default: 5)

3. DEFINE POLICY ENFORCEMENT ARCHITECTURE
   |-- PEP (Policy Enforcement Point): Intercepts requests, enforces decision (API gateway, middleware, sidecar)
   |-- PDP (Policy Decision Point): Evaluates policies against request context (OPA, Cedar, custom engine)
   |-- PIP (Policy Information Point): Retrieves attributes (user store, resource DB, device manager)
   |-- PAP (Policy Administration Point): Policy authoring, versioning, testing, deployment
   |-- Decision caching: cache PDP decisions for 30-60 seconds (with forced invalidation on role/permission change)
   |-- Fail closed: if PDP is unreachable, deny access (never fail open)
```

### Phase 3: Zero Trust Architecture

```
1. MAP IDENTITY-AWARE PERIMETER
   |-- Identity-centric segmentation: boundaries defined by identity, not IP address
   |   |-- Every service-to-service call authenticated (mTLS or SPIFFE)
   |   |-- Every user-to-service call authenticated (OAuth2 token or session)
   |-- Microsegmentation: service A can only call service B on port 443 with valid identity
   |   |-- Default-deny policy between all services, explicit allows for known flows
   |   |-- Service identity: SPIFFE (X.509 SVIDs) or cloud-native (AWS IAM roles, GCP service accounts)
   |-- Device trust: access decisions incorporate device posture
   |   |-- Signals: OS patch level, disk encryption status, firewall enabled, MDM enrollment, jailbreak detection
   |   |-- Trust score threshold: deny access if device score < 80/100
   |   |-- Continuous re-evaluation: recheck device posture every 5-15 minutes, not just at authentication

2. IMPLEMENT CONTINUOUS AUTHENTICATION
   |-- Session-bound risk scoring: user behavior signals feed risk score
   |   |-- Signals: location change (impossible travel), new device, unusual hour, anomalous API pattern
   |   |-- Risk-based step-up: request MFA re-authentication when risk score exceeds threshold
   |-- Just-in-time access: no standing privileges — request elevation only when needed
   |   |-- Time-bound: elevation expires after 1-4 hours, auto-revocation
   |   |-- Approval workflow: manager or security lead approves elevation (change ticket integration)
   |   |-- Audit trail: who requested, who approved, what was accessed, when elevation ended

3. POLICY AUTHORING AND TESTING
   |-- Policy-as-code: OPA/Rego, Cedar, or custom DSL stored in version control
   |-- Unit tests for policies: test allow/deny for every policy path before deployment
   |-- Integration tests: simulate user journeys with different roles/attributes/relationships
   |-- Policy diff on PR: automated policy impact analysis for every policy change
   |-- Rollback plan: policy changes deployed with canary (10% traffic) -> 50% -> 100%
```

### Phase 4: Privileged Access Management

```
1. ELIMINATE STANDING PRIVILEGES
   |-- Inventory: catalog every user with admin/root/superuser access — this is your attack surface
   |-- Convert to JIT: replace standing admin roles with just-in-time elevation
   |-- Break-glass accounts: 1-2 emergency accounts with maximum privileges, stored in offline vault
   |   |-- Break-glass usage triggers: pager alert to security team within 60 seconds
   |   |-- Password: 40+ character random string, split across 2+ people (Shamir's Secret Sharing)
   |   |-- Automatic rotation after ANY break-glass use

2. SESSION MANAGEMENT FOR PRIVILEGED ACCESS
   |-- Session recording: capture every keystroke and screen for privileged sessions
   |   |-- Storage: encrypted, immutable, 1-year retention minimum
   |   |-- Review: random audit of 5% of sessions monthly, 100% of sessions post-incident
   |-- Command filtering: block dangerous commands (rm -rf /, DROP TABLE, iptables -F) without override
   |-- Session termination: auto-terminate after 4 hours idle, immediate termination on risk score spike

3. CREDENTIAL VAULTING
   |-- Vault design: HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault
   |-- Dynamic secrets: generate per-use credentials, auto-expire after lease TTL (max 24 hours)
   |-- Static secret rotation: API keys, database passwords rotated every 30-90 days automatically
   |-- Access audit: who accessed which secret, when, from which IP — log for minimum 1 year
```

### Phase 5: Secrets Remediation (Credential Leak Response)

```
IMMEDIATE (first 15 minutes):
1. CONFIRM THE LEAK
   |-- Identify: what credential (password, API key, token, private key)?
   |-- Scope: which systems/services/users are affected?
   |-- Exposure window: when was it leaked? Is it in git history? Log files? Public paste sites?
   |-- Evidence collection: screenshot or clone the exposure (for post-mortem, not remediation)

2. REVOKE IMMEDIATELY
   |-- Revoke the leaked credential in identity provider / secrets manager
   |-- Rotate all related credentials (if API key leaked, rotate ALL keys in that scope)
   |-- Invalidate all active sessions for affected users
   |-- If JWT signing key leaked: rotate key in JWKS, invalidate ALL tokens signed with old key
   |-- If database credential leaked: rotate password, check for unauthorized schema changes or data access

3. CONTAIN
   |-- Audit access logs for the exposure window: any anomalous activity?
   |-- Force password reset for all users in affected scope
   |-- Block IP ranges associated with anomalous activity
   |-- If exfiltration suspected: engage incident-responder skill

SHORT-TERM (first 24 hours):
4. ROOT CAUSE ANALYSIS
   |-- How was the secret exposed? (committed to git, hardcoded in config, logged in debug output, phishing)
   |-- Why wasn't it caught? (no pre-commit hooks, no secret scanning in CI, no log redaction)
   |-- Who had access to the exposed credential? (least privilege audit)

5. PREVENT RECURRENCE
   |-- Pre-commit hooks: git-secrets, detect-secrets, or truffleHog on every developer machine
   |-- CI/CD scanning: truffleHog / gitleaks in pipeline, block merge on secret detection
   |-- Log redaction: strip Authorization headers, api_key params, and Bearer tokens from logs
   |-- .gitignore audit: ensure .env, credentials.json, *.pem, service-account.json are excluded
   |-- Developer training: 15-minute mandatory training on secrets hygiene within 1 week
```
