---
name: security-reviewer
description: >
  Use when performing security-focused code reviews, conducting STRIDE threat
  modeling, auditing authentication and authorization, reviewing data protection
  and encryption, or assessing API security posture. Handles OWASP Top 10 per-language
  patterns, dependency and container security, IaC hardening, and CVSS-aligned
  severity grading. Do NOT use for general code review, penetration testing execution,
  compliance auditing, or incident response.
author: Sandeep Kumar Penchala
license: MIT
type: quality
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- security
- stride
- owasp
- vulnerability
- threat-modeling
- authentication
- encryption
- cvss
token_budget: 4000
chain:
  consumes_from:
  - backend-developer
  - devops-engineer
  - firmware-developer
  - fullstack-developer
  - mobile-developer
  - qa-engineer
  - security-engineer
  feeds_into:
  - api-test-suite-builder
  - backend-developer
  - code-reviewer
  - incident-responder
  - qa-engineer
---
# Security Reviewer

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Comprehensive security review of applications, APIs, infrastructure, and mobile platforms. Covers STRIDE threat modeling during code review, OWASP Top 10 2021 mapped to language-specific patterns, authentication and authorization hardening, data protection and encryption, injection defense across all vectors, API security posture, dependency and supply chain analysis, container and IaC hardening, mobile security review, CVSS-aligned severity classification, and structured review reports with reproduction and verification steps.

## Route the Request
<!-- TWO-TIER ROUTING: Auto-Route table (machine) → Intent Route tree (human fallback) -->

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "security-reviewer")` — this is your skill | Redirect: "I am Security Reviewer. Route by intent matching below." |
| A2 | `file_contains("diff", "auth/\|jwt\|oauth\|session\|csrf\|password\|login")` OR `file_contains("PR description", "auth\|login\|token\|session")` | **AUTH** — JWT validation (reject `none`), session hardening (HttpOnly/Secure/SameSite), OAuth2 with PKCE. STRIDE: Spoofing, Elevation of Privilege. Auto-assign security-reviewer. |
| A3 | `file_contains("diff", "sql\|query\|where\|mongo\|graphql\|resolver")` AND `file_contains("diff", "$\|concat\|interpolat\|+.*user\|template")` | **INJECTION** — SQL/NoSQL injection audit. Every query must use parameterized or ORM-safe patterns. STRIDE: Tampering. Gate: any string interpolation in query = block merge. |
| A4 | `file_exists("**/package-lock.json\|**/requirements.txt\|**/Cargo.toml\|**/go.mod")` AND `file_contains("diff", "version\|resolved\|integrity\|checksum")` | **DEPENDENCY** — CVE audit across all layers (direct + transitive + vendored). SBOM generation. Supply chain posture check. Gate: any Critical CVE = block merge. |
| A5 | `file_exists("**/*.tf\|**/*.k8s.*\|**/Dockerfile\|**/docker-compose*")` | **INFRA/IaC** — Open security groups (0.0.0.0/0), public S3 buckets, overly permissive IAM. Non-root container, read-only FS, pinned digests. STRIDE: Information Disclosure. |
| A6 | `file_contains("diff", "upload\|multipart\|file.*stream\|form-data")` | **FILE UPLOAD** — Path traversal, unrestricted file types, stored file access controls, filename sanitization. STRIDE: Tampering + Elevation. |
| A7 | `file_contains("diff", "PII\|GDPR\|CCPA\|personal\|privacy\|encrypt\|decrypt\|hash\|bcrypt\|argon")` | **DATA PROTECTION** — PII field classification, encryption at rest (KMS) and transit (TLS 1.3). PII not in logs. Data minimization. STRIDE: Information Disclosure. |
| A8 | `file_contains("diff", "rate.limit\|throttle\|CORS\|csp\|csrf\|helmet\|security.*header")` | **API DEFENSE** — Rate limiting per endpoint. Strict CORS allowlist. CSP without unsafe-eval/inline. Mass assignment protection. STRIDE: Denial of Service. |
| A9 | None of the above — general security review | **STANDARD** — OWASP Top 10 audit. STRIDE per component. CVSS-aligned severity grading. Reproduction steps for every finding. |
```
What are you trying to do?
├── STRIDE threat modeling (design/architecture review) → Jump to "Core Workflow > Phase 1" and "Threat Modeling (STRIDE)"
├── OWASP Top 10 audit (code review against known vuln patterns) → Go to "OWASP Top 10 (2021) — Per-Language Patterns"
│   ├── Web application → Start at A01 (Broken Access Control), work through A10
│   ├── API security → Focus on A01, A02, A03, A05, A07
│   └── Mobile security → Jump to "Mobile Security Review"
├── Dependency/container scan (known CVEs, supply chain) → Go to "Dependency & Container Security"
├── API security review (rate limiting, CORS, auth, mass assignment) → Jump to "API Security Review"
├── Cloud/IaC security review → Go to "Core Workflow > Phase 3" and "Infrastructure as Code Security"
├── Mobile security review (secure storage, cert pinning, obfuscation) → Go to "Mobile Security Review"
├── Need security architecture and threat model → Invoke security-engineer skill instead
├── Need backend security implementation → Invoke backend-developer skill instead
├── Need code review (general, not security-specific) → Invoke code-reviewer skill instead
├── Need DevOps security (containers, IaC) → Invoke devops-engineer skill instead
├── Need incident response for active breach → Invoke incident-responder skill instead
└── Not sure where to start? → "Core Workflow > Phase 1" — define scope, identify threat actors, then follow STRIDE
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never claim "secure" — say "no vulnerabilities found at this confidence level."** Security is a spectrum, not a binary. Every review has blind spots. State your confidence and what you did NOT test.
- **CVSS scores need justification.** Every severity rating must reference the attack vector, complexity, privileges required, and impact. A number without reasoning is just a guess.
- **Always note what you did NOT test.** If you reviewed the API but not the infrastructure, reviewed the code but didn't run a dynamic scan, or focused on OWASP Top 10 but skipped mobile-specific threats — say so explicitly.
- **Never recommend rolling your own crypto.** If the answer involves implementing AES, RSA, or any cryptographic primitive yourself, stop. Use well-audited libraries and standard protocols.
- **Every finding needs a reproduction path.** Include the exact input, endpoint, or code path that triggers the vulnerability. Without reproduction, a finding can't be verified or fixed.
- **Admit what you don't know.** If a vulnerability class or technology is outside your expertise, flag it and recommend the appropriate specialist — don't extrapolate from adjacent knowledge.

## The Expert's Mindset

Security review is not about finding every vulnerability — it's about **understanding the attacker's perspective and ensuring that the cost of exploiting your system exceeds the value of what's protected**. The best security reviewers think like adversaries: creative, persistent, and indifferent to the developer's intentions.

### Mental Models

| Model | Description |
|---|---|
| **Security is economics, not perfection** | No system is perfectly secure. The goal is to make the cost of attack > value of the target for your threat model. A bank needs different security than a blog. Match defense to threat. |
| **Every input is hostile until proven otherwise** | Assume every input — from users, APIs, files, environment variables — is crafted by an adversary trying to break your system. Validate, sanitize, and bound everything. |
| **Defense in depth, not defense in a single layer** | No single security control is sufficient. A WAF without input validation, auth without rate limiting, encryption without key management — each is a single point of failure. Layers. |
| **You can't secure what you don't understand** | If you don't understand how a crypto primitive, authentication flow, or protocol works, you cannot review its security. Flag it for specialist review; don't guess. |

### Cognitive Biases in Security

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Optimism bias** | "Nobody would bother attacking us" — underestimating both motivation and automation | Assume automated scanners are probing your systems constantly. They are. |
| **Normalcy bias** | "It's been fine for years" — assuming past safety predicts future safety | Attack techniques evolve. A system that was secure in 2020 may be trivially exploitable today. |
| **Focusing on the spectacular, missing the mundane** | Worrying about zero-days while running dependencies with known CVEs from 2022 | Fix known vulns first. Attackers use known exploits 99% of the time. |
| **False sense of security from tools** | "Snyk/CodeQL/SonarQube says we're clean" — tools catch patterns, not novel attacks | Tools are necessary but insufficient. Human review catches logic flaws and business logic bugs that tools can't. |

### What Masters Know That Others Don't

- **The most dangerous vulnerabilities are in business logic, not technology.** SQL injection has known defenses. A flaw in how your refund logic works — approving refunds before verifying the item was returned — won't show up in any scanner. Review the business logic.
- **Security is everyone's job, but security review is a specialty.** Every developer should write secure code. But security review requires adversarial thinking that takes years to develop. Don't pretend expertise you don't have.
- **The best security finding is a design change that eliminates the vulnerability class.** Don't just fix the bug — ask: "What design decision allowed this bug to exist? How do we prevent this entire class of vulnerability?"
- **Your threat model determines your security posture.** A system with no threat model has no security strategy — it has a collection of security controls with no coherence. Start every review by asking: "Who are we defending against? What are we protecting?"

## Operating at Different Levels

Security review scales from single-PR review to org-wide security program design.

| Level | Security Reviewer Output Characteristics |
|---|---|
| **L1 — Apprentice** | Learns OWASP Top 10 and basic vulnerability patterns. Reviews with checklists. Flags obvious issues (hardcoded secrets, missing input validation). |
| **L2 — Practitioner** | Reviews PRs independently for security vulnerabilities. Familiar with STRIDE threat modeling. Covers auth, injection, and data protection. |
| **L3 — Senior** | Performs architectural security review. Threat models complex systems. Business logic vulnerability analysis. "This design creates a vulnerability class." |
| **L4 — Staff/Security Lead** | Sets security review standards for the org. Defines security architecture patterns, secure-by-default frameworks. "This is our security baseline." |
| **L5 — Industry-level** | Creates security methodologies and vulnerability taxonomies adopted across the industry. |

**Usage**: Say "as an L3 security reviewer, review this authentication flow." Default: **L2** (PR-level review, independent execution).

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Performing a security code review on a pull request, feature branch, or release candidate
- Threat modeling during design or architecture review sessions
- Auditing authentication flows: JWT validation, OAuth2/OIDC, session management
- Reviewing data protection: encryption at rest/transit, PII handling, data minimization
- Auditing input validation and injection defenses (SQL, NoSQL, Command, LDAP, XSS)
- Reviewing API security posture: rate limiting, CORS, CSP headers, mass assignment
- Scanning dependencies for known CVEs and supply chain risks
- Hardening container images and auditing Infrastructure as Code
- Reviewing mobile app security: secure storage, cert pinning, root detection, code obfuscation

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Review Depth by Change Type
```
                     ┌──────────────────────────┐
                     │ START: Security review   │
                     │ depth?                   │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Change involves auth, payments,     │
              │ PII, or crypto?                     │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Full STRIDE +    │  │ Change touches input │
        │ OWASP All 10 +   │  │ validation, API     │
        │ manual code      │  │ surface, or deps?   │
        │ review. No       │  └──┬───────────────┬───┘
        │ exceptions.      │     │ YES           │ NO
        └──────────────────┘     ▼               ▼
                          ┌────────────┐  ┌──────────────┐
                          │ Focused    │  │ Light:       │
                          │ review on  │  │ SAST +       │
                          │ relevant   │  │ dependency   │
                          │ OWASP cats │  │ scan only    │
                          └────────────┘  └──────────────┘
```
**When full STRIDE + OWASP All:** Auth flows, payment processing, PII handling, cryptographic operations. Any change that could expose user data or enable privilege escalation.  
**When light review suffices:** Documentation changes, test-only changes, configuration changes with no security surface. SAST passes + `npm audit` clean = approve.

### Auth Vulnerability Severity
```
                     ┌──────────────────────────────┐
                     │ START: Auth finding found    │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Allows unauthenticated access to        │
              │ protected resources or privilege        │
              │ escalation?                             │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ CRITICAL. Block  │    │ Token sent over HTTP │
        │ merge. Notify    │    │ or stored in         │
        │ Security Lead.   │    │ localStorage?       │
        │ Fix within 24hrs.│    └──┬───────────────┬───┘
        └──────────────────┘       │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ HIGH. Fix  │  │ MEDIUM. JWT  │
                            │ before     │  │ missing exp  │
                            │ merge.     │  │ claim, weak  │
                            │            │  │ algorithm.   │
                            └────────────┘  └──────────────┘
```
**When CRITICAL:** Auth bypass discovered. Any user can access another user's data (IDOR). Admin functions accessible without role check.  
**When MEDIUM:** JWT with `algorithm: none` possible but mitigated elsewhere. Session timeout is too long (72h+). Missing `SameSite` on non-critical cookie.

### Dependency Risk Triage
```
                     ┌──────────────────────────────┐
                     │ START: CVE found in dep      │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ CVSS ≥ 9.0 OR has known public exploit? │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ CRITICAL. Patch  │    │ Is the vulnerable    │
        │ immediately.      │    │ code path reachable │
        │ Hotfix deploy     │    │ in your app?        │
        │ outside band.     │    └──┬───────────────┬───┘
        └──────────────────┘       │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ HIGH. Fix  │  │ MEDIUM. Fix  │
                            │ within 7   │  │ within 30    │
                            │ days.      │  │ days.        │
                            └────────────┘  └──────────────┘
```
**When immediate hotfix:** Log4Shell-level vulnerability. RCE with public exploit. Dependency used in request path. CVSS ≥ 9.0 with network attack vector.  
**When 30-day fix:** Vulnerable in dev dependency only. Reachable code path requires non-default config. CVSS < 7.0 with local attack vector only.

### Tool vs Manual Review
```
                     ┌──────────────────────────────┐
                     │ START: SAST flag or manual?  │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Is this a SQL injection, XSS, hardcoded │
              │ secret, or known CWE pattern?           │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ SAST catches     │    │ Requires manual      │
        │ consistently.    │    │ review: auth logic   │
        │ Verify + auto-fix│    │ flaws, business      │
        │ if low FP rate.  │    │ logic bypass, race   │
        │                   │    │ conditions.          │
        └──────────────────┘    └──────────────────────┘
```
**When SAST is sufficient:** SQL injection via string concatenation. Hardcoded API keys. Missing CSRF tokens. XSS via innerHTML. High true-positive rate.  
**When manual review required:** Authorization logic (role checks, ownership verification). Race conditions in financial transactions. Cryptographic algorithm misuse.

## Core Workflow
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
## Finding #[N]: [SEVERITY] [CATEGORY] - [Brief Title]

**Severity:** Critical | High | Medium | Low | Info
**CWE:** CWE-[Number] ([Name])
**OWASP Category:** A0[X]:2021 - [Name]
**CVSS Vector:** CVSS:3.1/AV:X/AC:X/PR:X/UI:X/S:X/C:X/I:X/A:X (Score: X.X)

### Description
[One-paragraph summary understandable by non-security stakeholders]

### Location
- **File(s):** `src/...`
- **Lines:** [start]-[end]
- **Component/Endpoint:** [name]

### Vulnerability Details
[Technical explanation of the vulnerability: how it works, what an attacker can achieve]

### Reproduction Steps
1. [Step-by-step instructions to reproduce]
2. [Include exact curl commands, request bodies, etc.]
3. [Observed result vs expected result]

### Risk Assessment
- **Exploitability:** [Trivial/Moderate/Difficult] -- [reasoning]
- **Impact:** [Data exposed, system compromised, etc.]
- **Data at Risk:** [Specific data types or resources]

### Fix Recommendation
[Specific actionable code changes with before/after examples]

**Before (Vulnerable):**
```[language]
[actual vulnerable code from the codebase]
```

**After (Fixed):**
```[language]
[corrected code]
```

### Verification Steps
1. [How to confirm the fix works]
2. [Tests to run]
3. [Automated scan to verify]

### References
- [Link to CWE, OWASP, or vendor advisory]
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
> **War story:** A startup passed SOC 2 Type I with a clean audit. Three months later, a researcher found an unauthenticated GraphQL introspection endpoint that exposed the entire schema, including internal mutation names like `adminResetUserPassword`. The endpoint had no rate limiting and no auth check — it was added in a 'minor refactor' that didn't trigger a security review because the PR title said 'clean up resolver naming.' **Fix:** Security review gates must trigger on file patterns, not PR labels. Any PR touching `graphql/`, `resolver/`, or `mutation/` paths gets an automatic security reviewer assignment regardless of how minor it looks.

- **Defense in depth**: Validate at every layer. A WAF does NOT excuse missing input validation in application code.
- **Assume breach**: Design for containment. Segment networks. Implement anomaly detection. A single vulnerability shouldn't compromise everything.
- **Shift-left**: Catch vulnerabilities in code review, not penetration testing. SAST in CI on every PR. DAST on every staging deploy.
- **Context is everything**: A theoretical XSS in an internal admin tool differs from XSS on a public e-commerce checkout. Adjust severity based on exposure, data sensitivity, and user population.
- **Fix root cause, not symptom**: Don't add WAF rules for SQL injection -- use parameterized queries. Don't sanitize output for XSS -- use context-aware encoding and CSP.
- **Positive reinforcement**: Highlight secure patterns. "Good use of parameterized queries here" and "Nice job validating with Zod at the boundary" reinforce good habits.
- **Security is quality**: Frame findings as bugs. Don't appeal to fear -- appeal to correctness and engineering excellence.
- **Know thy threat model**: A startup MVP has a different threat model than a bank. Calibrate review depth and severity to the actual risk.

## Anti-Patterns

| ❌ | ✅ | 🔍 Detect (grep/lint) | 🛡️ Auto-Prevent |
|----|----|----------------------|------------------|
| WAF-as-fix — slapping Web Application Firewall rules on injection vulns instead of fixing parameterized queries | Fix at code level first: parameterized queries, input validation, output encoding. Then add WAF as defense-in-depth | `grep -rn "query.*[(]\s*[`'\"]\|\$.*\{.*\}\|" + \w+ +" src/ \| wc -l` → > 0 AND WAF rule exists = violation | CI: Semgrep rule `detect-sql-injection` as blocking error. WAF rules must have linked code fix ticket. Auto-label `sql-injection` on any string-interpolated query |
| Checkbox security — running SAST/DAST and accepting report as "security done" without triaging findings or verifying exploitability | Triage every finding: verify exploitability, assess impact in deployed context, fix root cause. Tool output = input to human process | `gh pr checks \| grep "sast\|sast\|codeql" \| grep "pass" \| wc -l` → > 0 AND `gh pr view --json comments -q '[.comments[] \| select(.body \| contains("verified\|exploitable\|triaged"))] \| length'` → 0 = violation | CI: SAST pass alone doesn't satisfy security gate — must have `@security-reviewer verified` comment on every High/Critical finding. Auto-label `needs-security-triage` |
| Severity inflation — marking everything "Critical" to get attention, destroying prioritization | Use CVSS-aligned grading: Critical (≥9.0, actively exploitable), High (7.0-8.9), Medium (4.0-6.9), Low/Info. Objective criteria per grade | `grep -rn "Critical\|CRITICAL" review_report.md \| wc -l` / `grep -rn "High\|Medium\|Low" review_report.md \| wc -l` → Critical > 20% of findings = inflation | CI: Severity ratio check — Critical must not exceed 10% of total findings. Auto-comment: "Justify Critical severity per CVSS criteria." Block report until balanced |
| Scope-by-label — triggering security review only when PR has `security` label. Attackers don't label their PRs | Gate on file patterns: `auth/`, `crypto/`, `payment/`, `admin/`, `graphql/`, `resolver/`. Labels are human — humans forget | `gh pr diff \| grep -l "auth/\|crypto/\|payment/\|admin/"` AND `gh pr view --json labels -q '.labels[].name' \| grep -v "security" \| wc -l` → > 0 = violation | CI: CODEOWNERS — `auth/** crypto/** payment/** admin/**` → @security-team. Auto-assign on file pattern match, not label. `danger.js`: warn if sensitive files touched without security label |
| Theoretical-only findings — reporting vulnerabilities requiring unrealistic conditions (physical access, admin already compromised) | Focus on exploitable findings. Threat model actual attack surface. A finding without a realistic attack path is noise | `grep -rn "requires\|needs\|assumes\|if the attacker" review_report.md \| grep -c "physical\|admin\|already\|prior"` → > 10% of findings = violation | CI: Every High+ finding must include a reproducible attack path ≤ 5 steps. Auto-reject findings with "requires physical access" or "requires admin credentials" as premise |
| Secrets in codebase tolerated — filing "Low" ticket because "it's in a private repo" | Private repos become public. All secrets must be rotated and moved to secrets manager. Zero tolerance for hardcoded credentials | `gitleaks detect --no-git -v \| grep -c "leak\|found\|secret\|key\|token\|password"` → > 0 = violation | CI: `gitleaks detect --no-git` as blocking pre-commit + CI check. Block merge if any secret detected. Auto-rotate compromised secret. Auto-label `secret-exposure` |
| Security review as gatekeeper — sole approval gate without empowering developers to self-service security scanning | Shift-left: run SAST in CI, let developers self-remediate. Security reviewer escalates only when automation can't decide | `gh pr list --search "status:pending review:requested @security-team" --json createdAt -q '.[] \| select((now - .createdAt) > 86400)' \| wc -l` → > 5 PRs blocked > 24h = violation | CI: Self-service SAST results in PR annotations. Only block on Critical/High findings. Auto-approve Low/Info. Track security-review turnaround as KPI — SLA < 24h |
| Compliance ≠ security — passing SOC 2 audit does not mean system is secure | Compliance = minimum bar. Security review assesses current active threat vectors beyond compliance checklist | `grep -rn "SOC 2\|compliant\|certified\|audit" review_report.md \| wc -l` → > 0 AND `grep -rn "OWASP\|STRIDE\|exploit\|bypass\|race\|inject" review_report.md \| wc -l` → < 3 = compliance-theater | CI: Security review template must include OWASP Top 10 AND STRIDE sections BEFORE compliance section. Auto-reject reviews that cite compliance as security evidence |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `security-engineer` | Threat model, security architecture, trust boundaries, defense-in-depth strategy | Before reviewing code; ensures review aligns with organizational security posture |
| `backend-developer` | API implementation, auth code, database queries, dependency inventory, data classification | When PR is submitted for security review; understanding implementation is prerequisite |
| `devops-engineer` | IaC (Terraform/Pulumi), container configs, CI/CD pipeline, secrets management, IAM policies | When infrastructure changes are submitted; infrastructure misconfiguration is a top attack vector |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `code-reviewer` | Security findings for joint severity assessment, patterns to add to code review checklist | Code reviewers merge without security expertise — vulnerabilities reach production |
| `backend-developer` | Vulnerability location with line numbers, proposed fix code, exploitation path context | Developer can't fix vulnerabilities without actionable guidance from security review |
| `qa-engineer` | Auth test scenarios, input validation edge cases, security test cases derived from findings | QA can't write targeted security regression tests without security context |
| `incident-responder` | IoCs identified, CVSS vector, affected components, mitigation priority, detection rules to add | Incident response delayed — missing critical threat intelligence from code analysis |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Critical vulnerability found in production | Incident Responder, DevOps Lead, CTO | Incident response activation; may require hotfix or rollback |
| Data breach confirmed (PII, PHI, financial data) | Compliance Officer, Legal Advisor, CISO | Regulatory notification clock starts; evidence preservation required |
| Vulnerability pattern found across 5+ services | System Architect, Engineering Manager | Systemic issue — root cause may be architectural or framework-level |
| Dependency with critical CVE in production | DevOps Engineer, Backend Lead | Patch or remove; assess exploitability in deployed context |
| Security finding blocking release | Engineering Manager, Product Strategist | Go/no-go decision; risk acceptance or deferral process |

### Escalation Path

```
Critical (CVSS ≥ 9.0, actively exploitable, data breach)?
  └── CISO + Incident Responder + CTO. Immediate war room. Fix within 24 hours.

High (CVSS 7.0–8.9, no public exploit, significant impact)?
  └── Security Lead + Engineering Manager. Fix before next deployment. Review within 48 hours.

Medium (CVSS 4.0–6.9, limited impact, requires non-default config)?
  └── Development team. Fix within sprint. Security reviewer validates fix.

Low / Info?
  └── Log in backlog. No escalation needed. Fix when refactoring.
```

## Proactive Triggers

| Trigger | Action | Rationale |
|---|---|---|
| JWT/OAuth2/SAML implementation or modification found | Verify algorithm validation (reject `none`), signature verification, claims validation (exp, nbf, aud, iss), and key management | JWT misconfiguration is the #1 auth vulnerability — algorithm confusion, missing signature checks, and weak secrets enable privilege escalation |
| File upload or file-serving endpoint added | Check for path traversal, unrestricted file types, stored file access controls, and filename sanitization | File upload is a triple threat: path traversal to overwrite, unrestricted upload for webshells, and insecure storage for data leaks |
| User input flows to database query | Check for SQL/NoSQL injection — verify parameterized queries or ORM-safe patterns on every data path | Injection remains #3 on the OWASP Top 10 — and every new query path is a new injection surface |
| New third-party dependency or SDK added | Audit for known CVEs, license compatibility, supply chain posture, and transitive dependency risk | The average npm package pulls in 79 transitive dependencies — any one of them can be compromised |
| IaC change (Terraform, Pulumi, CloudFormation, K8s manifests) | Scan for open security groups, public S3 buckets, overly permissive IAM policies, and unencrypted data stores | Infrastructure misconfiguration is the #1 cause of cloud data breaches — one `0.0.0.0/0` rule exposes everything |
| Container image or Dockerfile change | Verify non-root user, read-only filesystem, pinned base image digest, no secrets in layers, and dropped capabilities | Container escape CVEs are published monthly — hardened containers contain the blast radius when the next one hits |
| Devops pipeline or CI/CD configuration change | Audit for secret management in CI, pipeline injection risks, and artifact signing | CI/CD pipelines have access to production credentials — pipeline compromise = full infrastructure compromise |

**Service Interaction Designs:**

| Interaction | Design Detail |
|---|---|
| Security ↔ DevOps | Secret rotation audit: verify all secrets are in a secrets manager (Vault, AWS Secrets Manager), not in env vars or config files. IaC scanning (tfsec, Checkov, cfn_nag) runs on every IaC PR. Container image signing (Cosign/Notary) enforced before deployment. Network policy audit ensures least-privilege egress from production. |
| Security ↔ CI/CD | SAST (Semgrep/CodeQL) runs as blocking check on every PR. Dependency scanning (Dependabot/Snyk/osv-scanner) with auto-PR for patch versions. Secret detection (truffleHog/gitleaks) blocks commits containing credentials. SBOM generated and signed at build time. |
| Security ↔ Compliance | Regulatory scope mapping: classify systems by data type (PII, PHI, PCI) and map to compliance frameworks (GDPR, HIPAA, PCI DSS, SOC 2). Automated evidence collection from review findings for auditor-ready reports. Breach notification clock workflow triggered from finding severity. |
| Security ↔ Code Review | Security findings from SAST posted as inline PR annotations. Dependency vulnerability alerts surfaced in PR diff view. Security reviewer auto-assigned by file pattern (`auth/`, `payment/`, `crypto/`, `admin/`). |
| Security ↔ Observability | Security-relevant logs (auth failures, permission denials, suspicious patterns) shipped to SIEM. Detection rules aligned to MITRE ATT&CK framework. Anomaly detection on authentication and data access patterns. |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Security review = run `npm audit` / `pip audit`. Check for hardcoded secrets. Don't use `eval()`. Use parameterized queries. Use HTTPS. That's it.
- **What to skip**: STRIDE threat modeling. OWASP Top 10 full assessment. Penetration testing. SAST/DAST tools. Security review process. Compliance frameworks. Dependency audit beyond `audit`.
- **Coordination**: You review your own code. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Lightweight security review for auth, payment, and PII code. OWASP Top 10 checklist (critical items). Automated dependency scanning (Dependabot/Snyk). Secrets detection in CI (truffleHog/gitleaks). Basic CSP headers. Input validation review.
- **What to skip**: Full STRIDE threat model. Penetration testing. SAST/DAST pipeline. Compliance mapping. SBOM generation. Container scanning.
- **Coordination**: Security reviewer assigned for sensitive PRs. Weekly security check-in. Security findings in shared backlog.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated security reviewer. STRIDE threat model for critical components. SAST in CI (Semgrep/CodeQL). DAST for deployed environments. Dependency scanning with SLA for fixes. Container image scanning. OWASP Top 10 full assessment per release. Compliance mapping (SOC 2, GDPR). SBOM generation. Security review process with gates.
- **What to skip**: Full-time security team (1-2 specialists is enough). Penetration testing every release. Bug bounty program. Red team exercises.
- **Coordination**: Security review required for auth/payment/PII changes. Monthly security posture review. Vulnerability management process.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Security team (3+ engineers). Full SSDLC (secure software development lifecycle). STRIDE threat model for all components. SAST + DAST + IAST + SCA in CI/CD. Penetration testing per release + annual external audit. Bug bounty program. Red team exercises. Compliance automation (SOC 2, PCI DSS, HIPAA, FedRAMP). Security champions program. Incident response team.
- **What's full production**: Security operations center (SOC). Continuous security monitoring. Automated compliance evidence collection. Threat intelligence integration. Secure code training program.
- **Coordination**: Weekly security review. Monthly threat modeling session. Quarterly penetration test. Annual compliance audit. Incident response drills quarterly.

### Transition Triggers
- **Solo → Small**: First security incident or enterprise customer asking about security practices.
- **Small → Medium**: SOC 2 or compliance audit required. First penetration test finding critical issues. >10K users.
- **Medium → Enterprise**: Regulatory compliance (PCI DSS, HIPAA, FedRAMP). Public breach in similar company. >100K users.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | backend-developer | Feature implementation with auth/data handling |
| **This** | security-reviewer | Vulnerability report with CVSS scores and reproduction steps |
| **After** | security-engineer | Remediation plan and security control hardening |

Common chains:
- **Chain**: backend-developer → security-reviewer → security-engineer — Security review finds vulnerabilities; security engineer designs fixes
- **Chain**: devops-engineer → security-reviewer → compliance-officer — Infrastructure reviewed for security gaps; compliance validates against frameworks (SOC 2, PCI DSS)

## What Good Looks Like

> Every code change and infrastructure modification is systematically scanned against the OWASP Top 10 and CWE Top 25, with zero critical or high findings reaching production. Auth flows, data handling, and dependency chains are reviewed against the principle of least privilege. Each finding includes exploitation steps and concrete remediation guidance so developers can fix issues without being security experts. The organization's security posture improves incrementally with every review, developers internalize secure coding patterns, and auditors find no surprises because the review trail is complete and self-documenting.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `auth-security-review` | JWT/OAuth2/SAML/OIDC implementation, session management, MFA bypass attempts | Token validation gaps, algorithm confusion, missing claims verification, session fixation, CSRF |
| `injection-defense-review` | SQL, NoSQL, command injection, LDAP, XSS, SSTI, path traversal | Parameterization audit, ORM escape analysis, context-aware encoding, CSP bypass testing |
| `data-protection-review` | PII/PHI handling, encryption at rest/transit, data minimization, logging | Field classification, KMS key management, TLS configuration, PII-in-logs grep, GDPR/CCPA retention |
| `api-security-review` | REST/GraphQL/gRPC endpoint hardening, rate limiting, CORS, mass assignment | Auth middleware coverage (every endpoint), input allowlists, CORS origin validation, resource ownership checks |
| `dependency-audit` | SBOM generation, CVE triage, supply chain risk, transitive dependency analysis | `npm audit`/`pip audit`/`govulncheck`, reachability analysis, pinned versions, lockfile integrity |
| `container-iac-review` | Dockerfile hardening, Kubernetes manifests, Terraform/Pulumi security | Non-root containers, read-only fs, capability dropping, least-privilege IAM, network policy audit |
| `mobile-security-review` | React Native/Flutter/native app security: storage, transport, code integrity | Keychain/Keystore usage, cert pinning, ProGuard/R8 rules, root/jailbreak detection, screenshot blocking |
| `threat-modeling` | STRIDE per component during code review (not just architecture diagrams) | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |


## Error Decoder

| 🖥️ Console Match | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|-------------------|---------|------------|-----|------------------------|
| `npm audit \| grep "critical\|high" \| wc -l` → 0 AND `grep -rn "import\|require\|copy-paste\|vendor" src/ -l \| xargs grep -l "jsonwebtoken\|bcrypt\|crypto" \| wc -l` → > 0 | Dependency audit passed — production server compromised via Log4Shell in vendored code | Audit only scanned declared dependencies in package manifests, not vendored/copy-pasted libraries in `src/vendor/` | Audit ALL dependencies: direct, transitive, OS-level, container-image, AND vendored. SCA must scan across languages and layers. Ban vendored deps unless registered in `vendor-manifest.json` | 1. `find src/ -name "*.js\|*.py\|*.java" \| xargs grep -l "require\|import" \| xargs npm audit --json` 2. Register all vendored code in `vendor-manifest.json` with name, version, origin 3. CI: scan ALL source files, not just package manifests 4. `gitleaks detect --no-git` for copy-pasted secrets in vendor 5. Monthly vendored-dep audit |
| `semgrep --config=auto --json \| jq '.results \| length'` → > 200 AND `semgrep --config=auto --json \| jq '[.results[] \| select(.extra.severity=="ERROR")] \| length'` → < 90% true positive rate | SAST flagged 200+ "critical" findings — team ignores all SAST results because 85% were false positives | SAST rules not tuned to codebase risk profile. 200 findings = 170 false positives = alert fatigue = team stops looking at SAST | Tune SAST rules to actual risk. Suppress known false positives with inline comments (`# nosemgrep: reason`). Target false positive rate < 20%. Replace tools exceeding this threshold | 1. `semgrep --config=auto --json \| jq '.results[] \| select(.extra.is_ignored==false)'` 2. For each false positive → add `# nosemgrep: <reason>` 3. Track FP rate monthly: `FP / (FP + TP)` 4. If FP rate > 20% for 2 months → evaluate tool replacement 5. CI: auto-label `needs-sast-tuning` when FP rate > threshold |
| `grep -rn "admin.*role\|role.*admin\|isAdmin" src/routes/ \| wc -l` → > 0 AND `grep -rn "\.pick\|allowlist\|allowedFields\|body\." src/routes/register* \| wc -l` → 0 | Auth review passed — attacker registered as admin via mass assignment | Code review checked admin role exists but didn't verify registration endpoints cannot assign admin role. Mass-assignment protection missing on user creation handler | Review registration and user creation endpoints for mass-assignment. Use allowlists (Zod `.pick()`, Pydantic field allowlists) to explicitly define which fields client can set | 1. `grep -rn "create\|insert\|save\|register" src/routes/ -A 5 \| grep "body\|req\.\|input"` 2. Verify allowlist pattern: `.pick(['email','password'])` NOT `.parse(req.body)` 3. CI: Semgrep rule — `mass-assignment` detection on all create/update handlers 4. Add test: `POST /register {role:"admin"}` → expect 400 5. Post-deploy: audit log for unexpected role assignments |
| `grep -rn "app\.set.*trust proxy\|\| req\.ip\|X-Forwarded-For\|X-Real-IP" src/ \| wc -l` → > 0 AND `grep -rn "X-Forwarded-For.*127\|X-Forwarded-For.*10\.\|X-Forwarded-For.*192\.168" tests/ \| wc -l` → 0 | Rate limiting was implemented and tested — bypassed trivially with `X-Forwarded-For: 127.0.0.1` | Rate limiter used `req.ip` which Express populates from `X-Forwarded-For` when behind proxy. `trust proxy` not configured — attacker's spoofed IP trusted | Set `app.set('trust proxy', 1)` to trust only first proxy. Use rightmost IP in `X-Forwarded-For` chain. Test: send with spoofed header, verify real IP used for rate limiting | 1. `grep -rn "trust proxy\|req\.ip\|X-Forwarded-For" src/` 2. Ensure `app.set('trust proxy', 1)` or equivalent 3. Integration test: `curl -H 'X-Forwarded-For: 127.0.0.1' /api/` → rate limiter uses real IP 4. CI: test 101 requests with different spoofed IPs → rate limiter blocks all 5. Post-deploy: monitor rate-limit bypass attempts via WAF logs |
| `grep -rn "Content-Security-Policy-Report-Only\|Report-Only" nginx/\|src/\|config/ \| wc -l` → > 0 AND `grep -rn "Content-Security-Policy[^-]" nginx/\|src/\|config/ \| wc -l` → 0 | CSP header configured as Report-Only for 14 months — team believed they had CSP enforcement, violations silently logged | Team confused "CSP deployed" with "CSP enforced." Report-Only added during testing, never promoted. No alerts on violation dashboard | CSP must graduate from Report-Only to enforced within 30 days: deploy Report-Only → monitor 2 weeks → fix violations → switch to enforced `Content-Security-Policy`. Alert on violation rate spikes | 1. `curl -I https://app.example.com \| grep -i "content-security-policy"` 2. If `-Report-Only` present → check violation dashboard: `curl /csp-report/stats` 3. Fix all legitimate violations 4. Switch to `Content-Security-Policy` (no Report-Only) 5. CI: block deployment if CSP header missing or Report-Only for > 30 days |
| `gitleaks detect --no-git \| grep -c "found"` → > 0 AND `grep -rn "JWT_SECRET=my-secret\|password=changeme\|API_KEY=test\|TODO-change" .env* config/ \| wc -l` → > 0 | JWT signing secret found in `.env.example` committed to public repo — same value in production | Security review scoped to `auth.ts`, not entire auth system. `.env.example` excluded from review. DevOps copy-pasted default secret to production | Trace every secret from creation to consumption: generation, storage, access, rotation, leak response. CI: `gitleaks detect --no-git` as blocking check. Pre-commit: block commits with default secret patterns | 1. `gitleaks detect --no-git -v` → rotate ALL found secrets immediately 2. Pre-commit hook: `gitleaks protect --staged` 3. CI: `gitleaks detect --no-git` as blocking gate 4. Add secret rotation playbook: generate → store in Vault → update app → verify → revoke old 5. Monthly: `gitleaks detect --no-git` on all historical commits |


## Production Checklist

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|--------------------|----------|
| SR1 | STRIDE threat model conducted for components handling auth, payments, PII, or admin functions | `find docs/ -name "*threat*model*\|*stride*" \| wc -l` → ≥ 1 per P0 component | Generate STRIDE template per component: Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation. Link in PR template |
| SR2 | OWASP Top 10 2021 assessed: no Critical or High findings outstanding | `semgrep --config=auto --json \| jq '[.results[] \| select(.extra.severity=="ERROR")] \| length'` → 0 Critical; `grep -rn "Critical\|High" security_report.md \| wc -l` → 0 unresolved | CI: Semgrep/CodeQL as blocking check. Auto-label `security-blocker` on Critical/High findings. Block merge until resolved |
| SR3 | Authentication: JWT claims validated, sessions hardened (HttpOnly/Secure/SameSite), OAuth2 with PKCE | `grep -rn "jwt\.verify\|verify(" src/ \| wc -l` → ≥ 1; `grep -rn "httpOnly\|SameSite\|secure" src/ \| wc -l` → ≥ 3; `grep -rn "PKCE\|code_verifier\|code_challenge" src/ \| wc -l` → ≥ 2 | CI: eslint-plugin-security rules for JWT. Auto-check session cookie flags via `curl -I \| grep -i "set-cookie"`. Block if missing HttpOnly/Secure/SameSite |
| SR4 | Authorization: auth middleware on every endpoint, resource ownership verified, RBAC enforced server-side | `grep -rn "app\.\(get\|post\|put\|delete\|patch\)" src/routes/ -A 1 \| grep -c "auth\|middleware\|requireAuth\|authenticate"` → ratio ≥ 0.95 | CI: For each route file → verify auth middleware on every endpoint. Auto-label `missing-auth-middleware` on PRs adding routes without auth |
| SR5 | Data protection: PII fields classified, encryption at rest (KMS) and in transit (TLS 1.3), PII not logged | `grep -rn "email\|phone\|ssn\|address\|passport\|dob\|credit" src/ -l \| xargs grep -c "PII\|@Pii\|@Sensitive"` → all PII fields annotated; `grep -rn "console\.log\|logger\.\(" src/ \| grep -c "email\|phone\|ssn\|token\|password\|secret"` → 0 | CI: `detect-secrets` scan. PII-in-logs grep as blocking check. Auto-label `pii-exposure` if PII found in logs |
| SR6 | Input validation: parameterized SQL queries everywhere, schema validation at boundaries, output encoding for XSS | `grep -rn "query.*[(]\s*[`'\"]\|execute.*[(]\s*[`'\"]" src/ \| wc -l` → 0 raw queries; `grep -rn "\.parse\|\.validate\|z\.\|yup\." src/routes/ \| wc -l` → ≥ route count | CI: Semgrep `detect-sql-injection` + `detect-xss` rules as blocking errors. Auto-label `injection-risk` on string-interpolated queries |
| SR7 | API security: rate limiting, strict CORS allowlist, CSP without unsafe-eval/inline, mass assignment protection | `grep -rn "rate.limit\|rateLimit\|express-rate-limit" src/ \| wc -l` → ≥ 1; `grep -rn "cors\|CORS\|origin" src/ \| grep -v "\*\|localhost:3000" \| wc -l` → ≥ 1; `grep -rn "\.pick\|allowlist\|allowedFields" src/routes/ \| wc -l` → ≥ route count | CI: `helmet` middleware check. CSP header validation. Rate limit test: send 101 requests, expect 429. Auto-label `missing-rate-limit` |
| SR8 | Dependencies: audit clean (no Critical/High CVEs), SBOM generated, supply chain checks passing | `npm audit --json \| jq '.metadata.vulnerabilities.critical'` → 0; `syft dir:. -o spdx-json \| wc -l` → ≥ 1 SBOM | CI: `npm audit --audit-level=high` as blocking. Auto-generate SBOM on build. Block merge on Critical CVE. Auto-PR for patch updates |
| SR9 | Containers: non-root user, read-only FS where possible, pinned base image digest, image scan clean | `docker run --rm <image> whoami` → not "root"; `docker inspect <image> \| jq '.[].Config.User'` → not empty; `trivy image <image> \| grep "CRITICAL\|HIGH" \| wc -l` → 0 | CI: `trivy image` as blocking check. Dockerfile lint (hadolint). Auto-label `container-hardening` if USER missing or root detected |
| SR10 | IaC: no public S3 buckets, no 0.0.0.0/0 security groups, least-privilege IAM, scanned in CI | `tfsec . \| grep "CRITICAL\|HIGH" \| wc -l` → 0; `checkov -d . \| grep "FAILED" \| wc -l` → 0 | CI: `tfsec` + `checkov` as blocking checks. Auto-label `iac-security-violation` on open security groups or public buckets |
| SR11 | Mobile: Keychain/Keystore for auth tokens, cert pinning, root/jailbreak detection, no plaintext logs | `grep -rn "AsyncStorage\|SharedPreferences\|NSUserDefaults" mobile/ \| wc -l` → 0 for secrets; `grep -rn "Keychain\|Keystore\|SecureStore" mobile/ \| wc -l` → ≥ 1 | CI: `grep -rn "AsyncStorage\|NSUserDefaults" mobile/ \| grep "token\|secret\|password"` — if found, block merge. Auto-label `mobile-insecure-storage` |
| SR12 | Every finding documented: description, reproduction, severity, fix, verification, and references | `gh pr view --json comments -q '[.comments[] \| select(.body \| contains("CVE\|CVSS\|vulnerability"))]' \| jq '.[].body' \| grep -c "repro\|steps\|fix\|verify"` → ≥ 3 per finding | CI: Security finding template with required fields. Auto-reject findings missing reproduction steps or fix guidance |
## Negative Constraints
<!-- HARD GATES: these are non-negotiable — the agent must REFUSE/STOP/DETECT -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|---------------------|
| NC1 | REFUSE: Do not merge if any secret is detected in the diff (API keys, tokens, passwords, private keys) | `gitleaks detect --no-git -v \| grep -c "leak\|found"` → > 0 = violation | STOP. Immediately rotate ALL detected secrets. Block merge. CI: `gitleaks detect --no-git` as blocking pre-commit + CI gate. Auto-label `secret-exposure-critical`. Notify security-team Slack channel. |
| NC2 | REFUSE: Do not merge if any string interpolation exists in SQL/NoSQL query — use parameterized queries only | `semgrep --config=p/sql-injection --json \| jq '.results \| length'` → > 0 OR `grep -rn "query.*\`\$\|where.*\${\|find(\$" src/ \| wc -l` → > 0 = violation | STOP. Auto-comment with fix: replace `db.query(\`SELECT * WHERE id=${userId}\`)` with `db.query('SELECT * WHERE id=$1', [userId])`. CI: Semgrep rule as blocking error. Auto-label `sql-injection-critical`. |
| NC3 | DETECT: CSP header in Report-Only mode for > 30 days — surveillance without enforcement | `curl -sI https://app \| grep -i "Content-Security-Policy-Report-Only" \| wc -l` → > 0 AND deployment date > 30 days ago = violation | BLOCK deploy until CSP promoted to enforced `Content-Security-Policy`. Auto-label `csp-report-only-stale`. Automated SLA: Report-Only → enforced within 30 days. Weekly CSP violation dashboard review. |
| NC4 | REFUSE: Do not merge if `trust proxy` is misconfigured — attacker can spoof `X-Forwarded-For` to bypass rate limiting | `grep -rn "trust proxy\|app.set.*proxy" src/ \| wc -l` → 0 AND `grep -rn "req\.ip\|X-Forwarded-For" src/ \| wc -l` → > 0 = violation | STOP. Set `app.set('trust proxy', 1)` or equivalent. CI: rate-limit test with spoofed `X-Forwarded-For` headers — must block by real IP, not spoofed. Auto-label `trust-proxy-misconfig`. |
| NC5 | DETECT: SAST false positive rate > 20% for 2 consecutive months — alert fatigue destroys security signal | Track: `semgrep_findings_suppressed / (semgrep_findings_suppressed + semgrep_findings_fixed)` > 0.2 for 2 months = violation | BLOCK SAST gate enforcement until rules are retuned. Auto-label `sast-needs-tuning`. Schedule SAST rules review with security team. Consider tool replacement if FP rate cannot be brought below 20%. |
| NC6 | REFUSE: Do not merge if security-sensitive file paths (`auth/`, `payment/`, `crypto/`, `admin/`) are modified without security reviewer approval | `gh pr diff \| grep -l "auth/\|payment/\|crypto/\|admin/"` AND `gh pr view --json reviews -q '[.reviews[] \| select(.author.login \| test("@security-team\|security"))] \| length'` → 0 = violation | STOP. Auto-assign @security-team via CODEOWNERS. Block merge until security reviewer approves. CI: file-pattern gate — `auth/** payment/** crypto/** admin/**` → mandatory security review. |
| NC7 | REFUSE: Do not approve if any dependency has a Critical CVE (CVSS ≥ 9.0) without documented exploitability assessment | `npm audit --json \| jq '.vulnerabilities \| to_entries \| map(select(.value.severity=="critical")) \| length'` → > 0 AND no linked exploitability assessment doc = violation | STOP. For each Critical CVE: (1) assess exploitability in deployed context, (2) document assessment, (3) if exploitable → patch within 24h, (4) if not exploitable → document why with VP Eng sign-off. Block merge until all Critical CVEs have documented disposition. |
## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| Your security reviews find SQL injection and XSS but you've never found an authorization bypass, a business logic flaw, or a race condition | You find vulnerabilities at the seams between components — the interaction between the auth system and the rate limiter, between the ORM and the raw SQL escape, between the CSP and the third-party script loader | You've found a vulnerability that would have caused a data breach affecting >10,000 users — and the fix was deployed to production before anyone exploited it |
| You run `npm audit` and believe "zero CVEs = secure" — you don't know what a transitive dependency is | You trace every dependency to its origin: direct vs. transitive vs. vendored — and your scan pipeline covers all three categories | You've designed a vulnerability management program where mean time to patch Critical CVEs dropped from 30 days to 48 hours — with automated canary deployments and rollback verification |
| You check for secrets in code but not in Terraform state, CI logs, or Docker image layers | You've built a multi-layer secret detection pipeline: pre-commit hooks, CI scanning (gitleaks, truffleHog), and regular scans of all state files and build artifacts | An external penetration test finds zero Critical or High findings in a system you reviewed — and the pentest report says "the security posture exceeds industry standards" |

**The Litmus Test:** Given a codebase you've never seen, can you find a vulnerability that a SAST tool (Semgrep, CodeQL, Snyk Code) would miss — in under 30 minutes? If you've never compared your manual findings against what a SAST tool caught on the same codebase, you don't actually know how much value you add beyond automation.

## Deliberate Practice

Security instinct is built through repeated adversarial thinking — learning to see systems the way an attacker sees them. This is a mindset that must be practiced, not just studied.

```mermaid
graph LR
    A[Study a real vulnerability or CVE] --> B[Can you reproduce it in your own codebase?]
    B --> C[Fix it and write a detection rule]
    C --> D[Add that vulnerability class to your mental threat model]
    D --> A
```

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Solve one OWASP WebGoat or PortSwigger Web Security Academy lab | Weekly |
| **Competent** | Review a real PR with the question: "How would I break this?" | Weekly |
| **Expert** | Run a threat modeling session for a system you don't know well — practice the STRIDE questions cold | Monthly |
| **Master** | Publish a security finding with a novel attack vector or a new detection technique | Annually |

**The One Highest-Leverage Activity**: Every time a major CVE is published, ask: "Is our system vulnerable to this class of attack?" Don't wait for a scanner to tell you — read the CVE, understand the vulnerability class, and hunt for it manually in your codebase.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- [CWE Top 25 Most Dangerous Weaknesses](https://cwe.mitre.org/top25/)
- [NIST CVSS v3.1 Calculator](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [OWASP Mobile Top 10](https://owasp.org/www-project-mobile-top-10/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [HashiCorp Terraform Security](https://developer.hashicorp.com/terraform/tutorials/aws/aws-security)
