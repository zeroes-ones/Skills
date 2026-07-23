# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Threat Modeling with STRIDE During Code Review
Apply STRIDE per component by examining the code, not just architecture diagrams. For each component (API endpoint, service, database query, UI element), ask:

**Spoofing**: Can an attacker impersonate a user, service, or system?
- Grep for: missing auth middleware, hardcoded tokens, weak crypto algorithms (MD5, SHA1)
- Verify: JWT signature validation, certificate validation, MFA enforcement
- Code smell: `if (req.headers.authorization === 'Bearer static-token')`

**Tampering**: Can an attacker modify data in transit, at rest, or in processing?
- Grep for: missing TLS config, unsigned payloads, writable S3 buckets
- Verify: HTTPS enforcement, signed JWTs (JWS), input validation before processing
- Code smell: `http.createServer` instead of `https.createServer`

**Repudiation**: Can a user deny performing an action due to insufficient logging?
- Grep for: missing audit logs on sensitive operations
- Verify: append-only audit logs, tamper-proof timestamps, user identity in every log
- Code smell: `console.log` instead of structured audit logging with user context

**Information Disclosure**: Can sensitive data leak through errors, logs, or responses?
- Grep for: `console.log(error)`, stack traces in responses, PII in URLs
- Verify: error messages expose no internals, responses return only needed fields
- Code smell: `res.status(500).json({ error: err.message, stack: err.stack })`

**Denial of Service**: Can an attacker overwhelm the system?
- Grep for: unbounded queries (no LIMIT), regex without timeout, missing rate limits
- Verify: request size limits, query timeouts, rate limiting per user/IP
- Code smell: `db.collection.find({})` without pagination

**Elevation of Privilege**: Can a user gain unauthorized access?
- Grep for: role checks in client code only, missing ownership verification
- Verify: server-side authZ on every endpoint, resource ownership checks, JWT scope validation
- Code smell: `if (user.role === 'admin')` checked ONLY on the client

### Phase 2 (~30 min): OWASP Top 10 2021 -- Language-Specific Code Patterns

#### A01:2021 Broken Access Control
| Language | Detection Pattern | Fix Pattern |
|----------|------------------|-------------|
| **TypeScript/Express** | `router.get('/api/orders/:id')` without auth middleware | Add `authenticate` middleware + ownership check: `where: { id, userId: req.user.id }` |
| **Python/FastAPI** | `@app.get("/api/users/{user_id}")` without Depends(auth) | Add `Depends(get_current_user)` + verify `user_id == current_user.id` |
| **Go/net/http** | Handler reads `r.URL.Query().Get("user_id")` directly | Extract user from context (middleware-injected), verify against JWT sub claim |
| **Ruby on Rails** | `before_action :set_order` without ownership scope | `current_user.orders.find(params[:id])` instead of `Order.find(params[:id])` |

#### A02:2021 Cryptographic Failures
- **Weak hashing**: `md5()`, `sha1()` -- replace with bcrypt (cost >= 12) or argon2id.
- **Weak encryption**: AES-ECB, DES, 3DES, RC4 -- replace with AES-256-GCM + random IV.
- **Hardcoded keys**: `const SECRET = 'my-secret-key'` -- move to env vars or secrets manager.
- **Missing TLS**: `http://` URLs in production configs -- enforce HTTPS + HSTS header.
- **Weak random**: `Math.random()` for tokens -- use `crypto.randomBytes()` or `secrets.token_urlsafe()`.
- **Sensitive data in URLs**: `GET /api?token=eyJ...` -- use Authorization header or POST body.

#### A03:2021 Injection
| Injection Type | Detection | TypeScript Fix | Python Fix | Go Fix |
|---------------|-----------|---------------|------------|--------|
| **SQL Injection** | String interpolation in queries | Use parameterized queries: `db.$queryRaw\`SELECT * FROM users WHERE id = ${id}\`` | Use `cursor.execute("SELECT * FROM users WHERE id = %s", (id,))` | Use `db.Query("SELECT * FROM users WHERE id = $1", id)` |
| **NoSQL Injection** | User input as query object: `find({ username: req.body.username })` | Validate input is string: `if (typeof username !== 'string') throw Error` | Use schema validation (Pydantic) before MongoDB query | Use struct tags and validate type |
| **Command Injection** | `exec()`, `spawn()` with user input | Use `execFile()` with argument array | Use `subprocess.run([cmd, arg])` with list, not `os.system()` | Use `exec.Command(name, arg...)` not string formatting |
| **LDAP Injection** | String concatenation in LDAP filters | Escape special chars: `* ( ) \ \0` and `/` | Use ldap3 with proper escaping | Use go-ldap with `ldap.EscapeFilter()` |
| **XSS (Reflected)** | User input in HTML without escaping | React auto-escapes, but watch `dangerouslySetInnerHTML` | Auto-escape in Jinja2 (`{{ }}`), avoid `|safe` without sanitization | `html/template` auto-escapes; `text/template` does NOT |

#### A04:2021 Insecure Design
Review for design-level gaps during PR review:
- Missing rate limiting on auth endpoints (login, password reset, MFA verify)
- Missing account lockout after N failed attempts
- No request size limits (unbounded file uploads, JSON body parsing)
- Debug/detailed error mode in production (`NODE_ENV=development`, `DEBUG=True`)
- Missing security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- No threat model exists for features handling auth, payments, or PII

#### A05:2021 Security Misconfiguration
- Default admin credentials not changed in deployment configs
- Unnecessary HTTP methods enabled (PUT/DELETE on static files, TRACE method)
- Verbose server headers: `X-Powered-By: Express`, `Server: Apache/2.4.1`
- CORS: `Access-Control-Allow-Origin: *` with `credentials: true`
- Cloud storage: S3 buckets with public read/write ACLs
- Debug endpoints (`/debug`, `/graphiql`, `/swagger-ui`) exposed in production

#### A06:2021 Vulnerable and Outdated Components
- `package.json`: un-pinned versions (`^`, `~`, `*`, `latest`)
- `requirements.txt`: no version pinning, no hash checking
- `Dockerfile`: `FROM node:latest` (no digest pinning)
- Run `npm audit --audit-level=high`, `pip-audit`, `osv-scanner` in CI
- Establish SLAs: Critical CVEs (>=9.0) fixed within 24h, High (7.0-8.9) within 7 days

#### A07:2021 Authentication Failures
**JWT Review Checklist:**
- Token signed with RS256/ES256 (asymmetric) or HS256 with strong secret (>=256 bits)
- Short expiration: access token <=15 min, refresh token <=7 days with rotation
- Validate all standard claims: `iss`, `aud`, `exp`, `nbf`, `iat`
- Unique `jti` claim for token revocation support
- Refresh token rotation with reuse detection (invalidate entire token family on reuse)
- No sensitive data in JWT payload (it is base64-encoded, NOT encrypted)

**Session Management Checklist:**
- Cookies: `HttpOnly`, `Secure`, `SameSite=Lax`, `__Host-` prefix
- Server-side session store (Redis with persistence)
- Session fixation protection: regenerate session ID on login
- Idle timeout (30 min) and absolute timeout (8 hours)
- Logout invalidates session server-side, not just clears cookie

**OAuth2/OIDC Review:**
- State parameter used and validated (CSRF protection for OAuth flow)
- PKCE (Proof Key for Code Exchange) for SPAs and mobile apps
- `redirect_uri` validated against allowlist (exact match, no open redirect)
- Authorization code is single-use with short lifetime (< 10 minutes)
- ID token validated: `iss`, `aud`, `exp`, `nonce`

#### A08:2021 Software and Data Integrity Failures
- Insecure deserialization: `pickle.loads()`, `yaml.load()`, `eval()`, `new Function()`
- Missing integrity checks: no `integrity` hashes on CDN scripts, no lockfile hashes
- CI/CD pipeline: `pull_request_target` with checkout of untrusted PR code
- Unsigned commits merged to main branch
- npm packages without provenance attestation

#### A09:2021 Security Logging and Monitoring Failures
- Login attempts (success and failure) not logged with user ID, IP, timestamp
- Sensitive operations (role change, data export, password reset) not logged
- Logs contain secrets: passwords, tokens, credit card numbers, PII
- No alerting on: multiple failed logins, privilege changes, data exfiltration patterns
- Logs stored in mutable storage (can be deleted by attacker)

#### A10:2021 Server-Side Request Forgery (SSRF)
- User-controlled URLs in `fetch()`, `axios()`, `requests.get()`, `http.Get()`
- No validation of target hostname against allowlist
- No blocking of private/reserved IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.169.254)
- Redirect following enabled on outbound HTTP clients (SSRF via open redirect)

### Phase 3 (~20 min): Data Protection Review

#### Encryption at Rest
- Database: TDE (Transparent Data Encryption) or column-level encryption for PII
- File storage: S3 server-side encryption (SSE-S3, SSE-KMS), client-side encryption for highly sensitive data
- Backups: encrypted with separate key from production data
- Key management: KMS with automatic rotation, HSM for high-security environments

#### Encryption in Transit
- TLS 1.2 minimum (TLS 1.3 preferred)
- Certificate validation enforced (no `rejectUnauthorized: false` in production)
- Mutual TLS (mTLS) for service-to-service communication
- HSTS header with `max-age=31536000; includeSubDomains; preload`

#### PII Handling Audit
- Identify all PII fields in the codebase: name, email, phone, address, SSN, passport, biometric, IP, geolocation
- Verify data classification labels applied to all PII fields
- Verify PII is not logged (grep log statements for PII variable names)
- Verify PII is not in URLs or query parameters
- Verify PII masking in non-production environments (data anonymization/synthetic data)
- Verify data retention policies enforced (automated deletion after retention period)
- Right to access, rectify, delete (GDPR Articles 15-17): API endpoints exist and are tested

#### Data Minimization
- API responses return only fields the client needs (no `SELECT *`)
- GraphQL: field-level authorization, query depth limiting, query cost analysis
- Logging: redact sensitive fields before logging (PII, tokens, passwords)
- Database queries: select specific columns, not `SELECT *`

### Phase 4 (~15 min): Input Validation & Injection Defense

#### Defense-in-Depth Strategy
**Layer 1 -- Network**: WAF rules (SQL injection patterns, XSS patterns, path traversal)
**Layer 2 -- API Gateway**: Request size limits, content-type validation, rate limiting
**Layer 3 -- Application Boundary**: Schema validation (Zod, Pydantic, go-playground/validator)
**Layer 4 -- Business Logic**: Domain-specific validation rules, invariants

#### Cross-Site Scripting (XSS) Defense
- React JSX auto-escapes, BUT `dangerouslySetInnerHTML` requires DOMPurify sanitization first
- EJS: `<%= %>` escapes, `<%- %>` does NOT (avoid with user data)
- Jinja2: `{{ }}` auto-escapes; `{{ \| safe }}` marks content as safe (dangerous)
- Go `html/template`: `{{.}}` auto-escapes; `template.HTML()` bypasses
- CSP header: `script-src 'self'` -- no `'unsafe-inline'` or `'unsafe-eval'`

#### SQL Injection Defense
- ALWAYS use parameterized queries. Parameterized queries. Parameterized queries.
- ORMs provide safety: Prisma, Drizzle, SQLAlchemy ORM, GORM (when used correctly)
- Raw queries: Prisma `$queryRaw\`...\`` (template literal is safe), `db.raw()` with bind parameters
- Stored procedures: still vulnerable if concatenating strings inside the procedure
- Never, ever concatenate user input into SQL strings. No exceptions.

### Phase 5 (~25 min): API Security Review

#### Rate Limiting
- All endpoints rate-limited, especially: auth (login, signup, password reset), API mutations, file upload
- Per-user (by ID) AND per-IP rate limiting
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`
- Distributed rate limiting (Redis) for multi-instance deployments
- Graduated response: 429 -> temporary block -> permanent block

#### CORS Review
- No `Access-Control-Allow-Origin: *` with credentials
- Explicit origin allowlist, not wildcard
- Only needed HTTP methods (GET, POST, PUT, DELETE -- not TRACE, CONNECT)
- `Access-Control-Allow-Credentials: true` only when necessary

#### Mass Assignment Protection
- Allowlist fields in create/update operations, never pass `req.body` directly to ORM
- Zod `.pick()` or `.omit()` to control allowed fields
- Role, permissions, isAdmin, verified -- never allow client setting via mass update

#### GraphQL Security
- Query depth limiting (max 5-7 levels)
- Query cost/complexity analysis (prevent expensive queries)
- Introspection disabled in production
- Field-level authorization (not just resolver-level)
- Rate limiting based on query cost, not just request count

### Phase 6 (~25 min): Dependency Security

#### Audit Commands
```bash
npm audit --audit-level=high      # JavaScript
pip-audit                         # Python
govulncheck ./...                 # Go
cargo audit                       # Rust
```


**What good looks like:** OWASP Top 10 checklist completed with zero unmitigated critical/high findings. SAST/SCA scan passes with no exploitable vulnerabilities. Dependency audit shows zero known CVEs in production dependencies. Threat model covers authentication, authorization, data flow, and deployment.

#### Triage: Exploitability x Reachability x Impact
For each CVE, assess:
1. **Exploitability**: Public PoC? Actively exploited (CISA KEV)? Attack vector?
2. **Reachability**: Does vulnerable code path execute? Used in production or dev only?
3. **Impact**: Confidentiality (data leak), Integrity (tampering), Availability (DoS)?

#### CVSS-to-Response SLA
| CVSS | Severity | Response Time |
|------|----------|---------------|
| 9.0-10.0 | Critical | 24 hours |
| 7.0-8.9 | High | 7 days |
| 4.0-6.9 | Medium | 30 days |
| 0.1-3.9 | Low | 90 days or accept risk |

#### Supply Chain Checks
- `npx socket audit` -- typosquatting, protestware, telemetry detection
- `npm audit signatures` -- verify registry signatures
- Pin dependencies by digest for critical packages
- Review new dependencies: maintenance status, contributor activity, security history

### Phase 7 (~25 min): Container Security Review

#### Dockerfile Hardening Checklist
- [ ] Base image pinned by SHA256 digest (not floating tag like `:latest`)
- [ ] Minimal base image (Alpine or distroless -- no package manager in production)
- [ ] Non-root user: `USER 1001` (not root / UID 0)
- [ ] Read-only root filesystem where possible (`--read-only`)
- [ ] ALL capabilities dropped except those needed (`--cap-drop=ALL --cap-add=NET_BIND_SERVICE`)
- [ ] No `--privileged` flag under any circumstances
- [ ] Resource limits set (CPU and memory)
- [ ] Health check configured (`HEALTHCHECK` instruction)
- [ ] Multi-stage builds: build dependencies in stage 1, copy artifacts to stage 2
- [ ] Secrets never in ENV or image layers (use BuildKit secrets or runtime injection)
- [ ] Image scanned: Trivy/Grype/Snyk scan in CI with blocking on Critical findings
- [ ] `COPY --chown=appuser:appgroup` to set ownership during copy

### Phase 8 (~30 min): Infrastructure as Code Security

#### Terraform Security Audit
| Resource | What to Check | Finding if Missing |
|----------|--------------|-------------------|
| S3 Buckets | `block_public_access` enabled, KMS encryption, access logging, versioning | CRITICAL if public bucket |
| Security Groups | No 0.0.0.0/0 ingress (except 80/443), DB ports restricted to VPC CIDR | HIGH |
| RDS | `storage_encrypted = true`, `deletion_protection = true`, `publicly_accessible = false` | HIGH |
| IAM | No `*` in `Action` or `Resource`, roles for services not users, no long-lived access keys | HIGH |
| KMS | `enable_key_rotation = true`, least-privilege key policies | MEDIUM |
| Lambda | Environment variables encrypted, VPC-attached (not public), no hardcoded secrets | MEDIUM |
| ECS/EKS | Non-root containers, read-only root FS, no privileged pods, image digest not tag | HIGH |

#### IaC Scanning Tools
```bash
tfsec .                           # Terraform security scanner
checkov --directory .             # Multi-IaC scanner (Terraform, CloudFormation, K8s)
trivy config .                    # Misconfiguration scanning
```

### Phase 9 (~20 min): Mobile Security Review

#### Secure Storage Requirements
| Platform | Never Use | Must Use |
|----------|-----------|----------|
| **iOS** | UserDefaults, plain files | Keychain with `.complete` protection class |
| **Android** | SharedPreferences, plain SQLite | EncryptedSharedPreferences, Android Keystore |
| **React Native** | AsyncStorage | react-native-keychain, expo-secure-store |
| **Flutter** | shared_preferences | flutter_secure_storage |

#### Mobile Security Checklist
- [ ] Auth tokens in Keychain (iOS) / EncryptedSharedPreferences (Android) -- never plain storage
- [ ] Certificate pinning or network security config for API communication
- [ ] App Transport Security (iOS) enabled; cleartext HTTP blocked
- [ ] Code obfuscation: ProGuard/R8 (Android), commercial obfuscator (iOS)
- [ ] Root/jailbreak detection with graceful degradation (restrict, don't crash)
- [ ] Screenshot prevention on sensitive screens (auth codes, banking)
- [ ] No sensitive data in app logs (NSLog, Log.d, console.log)
- [ ] Deep links validated against allowlist (no open redirect to attacker WebView)
- [ ] WebView: JavaScript disabled unless required, no `setAllowUniversalAccessFromFileURLs`
- [ ] Biometric auth with device passcode fallback (never biometric-only for primary auth)

### Phase 10: Severity Classification (CVSS-Aligned)

| Severity | CVSS Range | Criteria | Required Response |
|----------|-----------|----------|-------------------|
| **Critical** | 9.0-10.0 | RCE, unauthenticated data breach, complete system compromise | Fix immediately -- block release |
| **High** | 7.0-8.9 | SQL injection, auth bypass, privilege escalation, PII exposure | Fix before merge -- cannot deploy |
| **Medium** | 4.0-6.9 | XSS with mitigation bypass, missing security header, minor info disclosure | Fix in current sprint |
| **Low** | 0.1-3.9 | Missing HSTS on non-sensitive subdomain, verbose server headers | Fix within 30 days |
| **Info** | N/A | Best practice suggestion, hardening opportunity | Backlog at team's discretion |

**Severity Decision Tree:**
```
Can an UNAUTHENTICATED attacker exploit this?
  Yes -> Is RCE or mass data breach possible?
    Yes -> CRITICAL
    No -> Can they access another user's data?
      Yes -> HIGH
      No -> MEDIUM
  No (requires authentication) -> What is the impact?
    Privilege escalation to admin -> HIGH
    Access same-role data of other users -> MEDIUM
    Minor information leak -> LOW
```

### Phase 11: Review Report Template

Every finding must follow this structured format:

```markdown
