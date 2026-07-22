---
name: owasp-top10-2021-checklist
description: Complete OWASP Top 10 2021 detection patterns, exploitation risks, and fix patterns with before/after code examples for every vulnerability category.
author: Sandeep Kumar Penchala
---

# OWASP Top 10 2021 — Complete Audit Checklist

Production-grade reference for identifying, exploiting, and fixing every OWASP Top 10 2021 vulnerability. Each entry includes detection patterns (what to grep for), exploitation risk assessment, and fix patterns with concrete before/after code.

---

## A01:2021 — Broken Access Control

**Prevalence:** 94% of applications tested. **Severity:** Critical.

### Detection Patterns

```bash
# Grep for missing authorization checks
grep -rn "router\.(get|post|put|delete|patch)" --include="*.ts" | grep -v "auth\|authorize\|middleware"
grep -rn "@Public\|isPublic\|skipAuth" --include="*.ts"  # Find intentionally public endpoints

# Find direct object references without ownership checks
grep -rn "\.findById\|\.findOne\|\.findByPk" --include="*.ts" | grep -v "userId\|orgId\|ownerId"

# Find role checks that can be bypassed
grep -rn "req\.user\.role\|user\.role ===" --include="*.ts"
```

### Exploitation Risk

- **IDOR (Insecure Direct Object Reference):** Change `/api/orders/123` to `/api/orders/124` — if you see another user's order, IDOR exists.
- **Privilege escalation:** User changes `role: "admin"` in a PATCH request body.
- **Missing function-level access:** Non-admin accesses `/admin/users` directly by URL.
- **CORS misconfiguration:** `Access-Control-Allow-Origin: *` with credentials.

### Fix Patterns

**Before (Vulnerable):**
```typescript
// Express — IDOR: no ownership verification
app.get('/api/orders/:id', async (req, res) => {
  const order = await db.order.findUnique({ where: { id: req.params.id } });
  res.json(order); // Any user can see any order!
});

// Next.js API route — missing auth check entirely
export async function GET(request: Request) {
  const orders = await db.order.findMany(); // No user context!
  return Response.json(orders);
}
```

**After (Fixed):**
```typescript
// Express — ownership verified
app.get('/api/orders/:id', authenticate, async (req, res) => {
  const order = await db.order.findFirst({
    where: {
      id: req.params.id,
      userId: req.user.id, // Ownership check
    },
  });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});

// Next.js — auth + ownership
export async function GET(request: Request) {
  const session = await auth();
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 });

  const orders = await db.order.findMany({
    where: { orgId: session.user.orgId }, // Scoped to organization
  });
  return Response.json(orders);
}

// Role-based access in middleware
function requireRole(...roles: string[]) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}
app.delete('/api/users/:id', authenticate, requireRole('admin'), handler);
```

### Checklist
- [ ] Every API endpoint has authentication middleware (unless intentionally public)
- [ ] Every resource query includes user/org ownership filter
- [ ] Admin routes have role verification middleware
- [ ] CORS configuration allows only specific origins (not `*`)
- [ ] JWT scopes are validated per endpoint
- [ ] Row-Level Security (RLS) enabled in PostgreSQL for multi-tenant tables

---

## A02:2021 — Cryptographic Failures

**Prevalence:** 65%. **Severity:** High.

### Detection Patterns

```bash
# Weak algorithms
grep -rn "MD5\|SHA1\|SHA-1\|DES\|RC4\|RC2\|3DES\|ECB" --include="*.ts"
grep -rn "md5\|sha1\|sha-1" --include="*.py"
grep -rn "crypto/md5\|crypto/sha1\|crypto/des" --include="*.go"

# Hardcoded keys / secrets
grep -rn "secret\|password\|apiKey\|api_key\|AES_KEY\|PRIVATE_KEY" --include="*.ts" | grep -v "process\.env\|import\.meta\.env"

# Missing TLS
grep -rn "http\.createServer\|http\.Server" --include="*.ts"
grep -rn "http://" --include="*.{ts,js,py,go}" | grep -v "localhost\|127.0.0.1"

# Sensitive data in URLs
grep -rn "token=\|api_key=\|password=\|secret=" --include="*.ts"
```

### Fix Patterns

**Before (Vulnerable):**
```typescript
// Weak hashing
import { createHash } from 'crypto';
const hash = createHash('md5').update(password).digest('hex');

// Hardcoded key
const API_KEY = 'sk_live_abc123xyz';

// ECB mode
const cipher = createCipheriv('aes-128-ecb', key, null);
```

**After (Fixed):**
```typescript
// Strong hashing
import { hash, verify } from 'argon2';
const hashedPassword = await hash(password, {
  type: argon2id,
  memoryCost: 65536, // 64MB
  timeCost: 3,
  parallelism: 4,
});
const isValid = await verify(hashedPassword, inputPassword);

// Secrets from env
const API_KEY = process.env.API_KEY;
if (!API_KEY) throw new Error('API_KEY not configured');

// AES-256-GCM with random IV
import { randomBytes, createCipheriv } from 'crypto';
const iv = randomBytes(12);
const cipher = createCipheriv('aes-256-gcm', key, iv);
const encrypted = Buffer.concat([cipher.update(data), cipher.final()]);
const authTag = cipher.getAuthTag();
// Store: iv + authTag + encrypted
```

### Checklist
- [ ] Passwords hashed with bcrypt (cost ≥ 12) or argon2id (OWASP-recommended params)
- [ ] AES-256-GCM for symmetric encryption (never ECB/CBC without HMAC)
- [ ] TLS 1.3 enforced; HTTP Strict Transport Security (HSTS) header set
- [ ] All secrets stored in environment variables or secrets manager (never in code)
- [ ] No sensitive data in URLs (query params) — use POST body or headers
- [ ] Encryption keys managed via KMS with automatic rotation
- [ ] TLS certificates auto-renewed (Let's Encrypt or managed)

---

## A03:2021 — Injection

**Prevalence:** 94%. **Severity:** Critical.

### SQL Injection

**Detection:**
```bash
grep -rn "\`SELECT.*\$\{\|\`INSERT.*\$\{\|\`UPDATE.*\$\{" --include="*.ts"
grep -rn "db\.raw\|\\.query\|\\.execute\|\\.exec" --include="*.ts"
grep -rn "format.*%s.*user\|f\".*SELECT" --include="*.py"
```

**Before (Vulnerable):**
```typescript
// String interpolation — SQL injection
const user = await db.$queryRawUnsafe(
  `SELECT * FROM users WHERE email = '${email}'`
);

// Python — f-string SQL injection
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

// Go — fmt.Sprintf SQL injection
db.Query(fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", email))
```

**After (Fixed):**
```typescript
// Parameterized query — TypeScript (Prisma)
const user = await db.user.findUnique({ where: { email } });

// Parameterized raw query
const users = await db.$queryRaw<User[]>`
  SELECT * FROM users WHERE email = ${email}
`; // Prisma template literal is safe — parameterized

// Python — parameterized
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

// Go — parameterized
db.Query("SELECT * FROM users WHERE email = $1", email)
```

### NoSQL Injection

**Before (Vulnerable):**
```typescript
// MongoDB — user input passed directly to query
const user = await db.collection('users').findOne({ username: req.body.username });
// Attacker sends: { "username": { "$ne": "" } } → returns first user
```

**After (Fixed):**
```typescript
// Explicitly cast to expected type
const username = String(req.body.username);
if (typeof username !== 'string' || username.length === 0) {
  return res.status(400).json({ error: 'Invalid username' });
}
const user = await db.collection('users').findOne({ username });

// Or use a schema validation layer
import { z } from 'zod';
const schema = z.object({ username: z.string().min(1).max(50) });
const { username } = schema.parse(req.body);
```

### Command Injection

**Detection:**
```bash
grep -rn "child_process\|exec\|spawn\|execSync\|subprocess\|os\.system\|os\.popen" --include="*.ts"
```

**Before (Vulnerable):**
```typescript
exec(`ffmpeg -i ${userInput} output.mp4`);
```

**After (Fixed):**
```typescript
import { execFile } from 'child_process';
// execFile never spawns a shell — no injection possible
execFile('ffmpeg', ['-i', validatedPath, 'output.mp4'], (err, stdout) => { ... });
```

### Checklist
- [ ] All SQL queries use parameterized queries (no string interpolation)
- [ ] No `$queryRawUnsafe` or string-format raw queries without thorough review
- [ ] MongoDB queries validated that inputs are strings (not objects like `$ne`)
- [ ] No shell-based `exec()` or `system()` calls — use `execFile()` or array-form `spawn()`
- [ ] ORMs used as primary data access layer (Prisma, Drizzle, SQLAlchemy ORM)

---

## A04:2021 — Insecure Design

**Prevalence:** 77%. **Severity:** High.

### Detection Patterns

```bash
# Missing rate limiting
grep -rn "rate.limit\|rateLimit\|express-rate-limit\|bottleneck\|p-limit" --include="*.ts"

# Missing input validation
grep -rn "req\.body\." --include="*.ts" | grep -v "validate\|schema\|parse\|zod\|joi"

# Unsafe defaults
grep -rn "debug.*true\|DEBUG.*true\|NODE_ENV.*development" --include="*.{ts,js,env}"

# Missing security headers
grep -rn "helmet\|CSP\|HSTS\|X-Frame" --include="*.ts"
```

### Fix Patterns

**Rate limiting (Express):**
```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

const limiter = rateLimit({
  store: new RedisStore({ client: redis }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.user?.id ?? req.ip, // Per-user or per-IP
});

app.use('/api/', limiter);
```

**Security headers (Helmet for Express):**
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'wasm-unsafe-eval'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https://cdn.example.com"],
      connectSrc: ["'self'", "https://api.example.com"],
      frameAncestors: ["'none'"],
      formAction: ["'self'"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
  frameguard: { action: 'deny' },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
}));
```

### Checklist
- [ ] Rate limiting on all API endpoints (per-user and per-IP)
- [ ] Input validation on all user-supplied data (Zod/Joi at API boundary)
- [ ] Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] Debug mode disabled in production
- [ ] Threat model documented for features touching auth, payments, or PII
- [ ] Account lockout / brute-force protection on login
- [ ] Request size limits configured (body parser `limit` option)

---

## A05:2021 — Security Misconfiguration

**Prevalence:** 90%. **Severity:** Medium.

### Detection

```bash
# Check for verbose error responses
grep -rn "stack\|stacktrace\|traceback" --include="*.ts" | grep -v "console\."
grep -rn "NODE_ENV.*development\|DEBUG=true" --include="*.{env,ts}"

# Default credentials
grep -rn "admin.*admin\|password.*password\|root.*root" --include="*.{env,ts,json,yaml}"

# Open ports / unnecessary services
grep -rn "app\.listen\|server\.listen" --include="*.ts"
```

### Fix Patterns

```typescript
// Production error handler — never leak stack traces
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error({ err, reqId: req.id }, 'Unhandled error');

  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({
      error: 'Internal Server Error',
      requestId: req.id, // Reference for support, not internal details
    });
  } else {
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});

// Docker — non-root user
// Dockerfile
FROM node:20-alpine
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
USER app
```

### Checklist
- [ ] Error responses in production never include stack traces or internals
- [ ] All default credentials changed (databases, admin panels, third-party services)
- [ ] CORS configured with explicit origin allowlist (not `*`)
- [ ] HTTP methods restricted to those needed (only GET/POST/PUT/DELETE)
- [ ] `X-Powered-By` and server version headers removed
- [ ] Container runs as non-root user
- [ ] Unnecessary services/ports disabled

---

## A06:2021 — Vulnerable and Outdated Components

### Detection

```bash
# npm audit
npm audit --audit-level=high
# Check for packages with known CVEs but no fix available
npm audit --json | jq '.vulnerabilities | to_entries | map(select(.value.fixAvailable == false))'

# Python
pip-audit
safety check

# Check for unpinned versions
grep -rn '"[~^]' package.json  # Caret/tilde versions — run updates
grep -rn '"latest"\|"\*"' package.json  # Floating versions — dangerous
```

### Fix Strategy

1. **Triage CVEs by exploitability:** Check CVSS vector (`AV:N/AC:L/PR:N/UI:N` = remotely exploitable without auth = critical).
2. **Triage by reachability:** Is the vulnerable function actually called with user-controlled input? Use `snyk test --reachability` or manual code review.
3. **Patch immediately:** CVSS ≥ 9.0 and exploitable → fix same day.
4. **Schedule:** CVSS 7.0-8.9 → fix within 7 days.
5. **Monitor:** CVSS 4.0-6.9 → fix within 30 days.
6. **Accept risk (document):** CVSS < 4.0 or unreachable → document acceptance.

### Automation

```yaml
# GitHub Actions — Dependabot auto-merge patches
name: Dependabot auto-merge
on: pull_request_target
permissions:
  contents: write
  pull-requests: write
jobs:
  dependabot:
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Auto-merge patch updates
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Checklist
- [ ] Dependency scanning in CI (`npm audit --audit-level=high`, `pip-audit`, `osv-scanner`)
- [ ] Dependabot/Renovate enabled with auto-merge for patch versions
- [ ] CVSS ≥ 9.0 vulnerabilities patched within 24 hours
- [ ] Unpinned dependencies (`*`, `latest`) eliminated from production
- [ ] Container base images scanned for vulnerabilities (Trivy, Grype)
- [ ] SBOM (Software Bill of Materials) generated as part of the build

---

## A07:2021 — Identification and Authentication Failures

### Detection

```bash
# Weak password policies
grep -rn "password.*min\|password.*minimum" --include="*.ts" | grep -v "[8-9]\|[1-9][0-9]"

# Missing MFA
grep -rn "mfa\|2fa\|two.factor\|totp\|otp" --include="*.ts"

# Session issues
grep -rn "maxAge\|expires\|cookie.*secure\|cookie.*httpOnly" --include="*.ts"
```

### Fix Patterns

**JWT hardening:**
```typescript
// Before: Weak JWT configuration
const token = jwt.sign({ userId: user.id }, 'hardcoded-secret');
// Problems: no expiry, weak secret, HS256, missing standard claims

// After: Production JWT
import { SignJWT, jwtVerify } from 'jose'; // Use jose, not jsonwebtoken

const accessToken = await new SignJWT({
  sub: user.id,                       // Subject
  email: user.email,
  role: user.role,
})
  .setProtectedHeader({ alg: 'RS256' }) // Asymmetric for multi-service
  .setIssuedAt()
  .setIssuer('https://api.example.com')
  .setAudience('https://app.example.com')
  .setExpirationTime('15 minutes')      // Short-lived
  .setJti(crypto.randomUUID())          // Unique token ID
  .sign(privateKey);

// Verification (every service)
const { payload } = await jwtVerify(token, publicKey, {
  issuer: 'https://api.example.com',
  audience: 'https://app.example.com',
  algorithms: ['RS256'],
  clockTolerance: 30, // seconds
});
```

**Session management:**
```typescript
app.use(session({
  store: new RedisStore({ client: redis, prefix: 'sess:' }),
  cookie: {
    httpOnly: true,    // Not accessible via JavaScript
    secure: true,      // HTTPS only
    sameSite: 'lax',   // CSRF protection
    maxAge: 8 * 60 * 60 * 1000, // 8 hours absolute
    domain: '.example.com', // Or exact domain
  },
  name: '__Host-session', // __Host- prefix requires Secure + Path=/
  rolling: true,      // Refresh on activity
  resave: false,
  saveUninitialized: false,
  secret: process.env.SESSION_SECRET,
}));
```

### Checklist
- [ ] JWT: RS256/ES256, short expiry (≤ 15 min), validated claims (iss, aud, exp, nbf)
- [ ] Passwords: bcrypt cost ≥ 12 or argon2id; min 8 chars with complexity
- [ ] Brute force protection: account lockout after 5 failed attempts; rate limiting on login
- [ ] MFA available and enforced for admin/sensitive operations
- [ ] Session cookies: HttpOnly, Secure, SameSite=Lax, `__Host-` prefix
- [ ] Refresh token rotation with reuse detection
- [ ] Password reset tokens: single-use, short expiry (< 1 hour), cryptographically random

---

## A08:2021 — Software and Data Integrity Failures

### Detection

```bash
# Insecure deserialization
grep -rn "eval\|new Function\|Function(" --include="*.ts"
grep -rn "pickle\|yaml\.load\|marshal\.load" --include="*.py" | grep -v "yaml\.safe_load"

# Missing integrity checks
grep -rn "integrity\|subresource\|SRI" --include="*.html"

# CI/CD pipeline risks
grep -rn "pull_request_target\|workflow_run" --include="*.yml"
```

### Fix Patterns

**Safe deserialization:**
```python
# Before: Unsafe YAML deserialization
data = yaml.load(user_input)  # Allows arbitrary code execution!

# After: Safe loading
data = yaml.safe_load(user_input)  # Only basic types

# Or use a schema-validated approach
from pydantic import BaseModel, ValidationError

class UserInput(BaseModel):
    name: str
    email: str
    age: int

try:
    data = UserInput.model_validate_json(user_input)
except ValidationError:
    return error_response()
```

**CI/CD pipeline security:**
```yaml
# GitHub Actions: Use pull_request, not pull_request_target
# pull_request_target runs in the context of the base repo — dangerous!
on:
  pull_request:  # Safe: runs in a restricted context
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }} # Check out PR code safely
      - run: npm ci && npm test
```

### Checklist
- [ ] No insecure deserialization (`pickle`, `yaml.load`, `eval`, `new Function`)
- [ ] npm integrity hashes committed to `package-lock.json` (not regenerated in CI)
- [ ] Subresource Integrity (SRI) hashes on CDN-loaded scripts
- [ ] CI/CD: no `pull_request_target` with checkout of untrusted code; secrets not exposed to forks
- [ ] Artifact signing and SLSA provenance for builds
- [ ] GPG-signed commits enforced for production repositories

---

## A09:2021 — Security Logging and Monitoring Failures

### Detection

```bash
# Missing logging on critical operations
grep -rn "login\|signin\|signup\|password.*reset\|role.*change\|admin" --include="*.ts" | grep -v "log\|audit\|logger"

# Console.log in production
grep -rn "console\.log\|console\.error" --include="*.ts" | grep -v "__tests__\|test\|spec"
```

### Fix Patterns

```typescript
// Structured audit logging
import pino from 'pino';

const auditLogger = pino({
  level: 'info',
  redact: ['password', 'token', 'secret', 'authorization', 'cookie'],
  formatters: {
    level(label) { return { level: label }; },
  },
});

// Audit events — immutable record of what happened
function auditLog(event: string, details: Record<string, unknown>) {
  auditLogger.info({
    event,
    ...details,
    timestamp: new Date().toISOString(),
    // Immutable: append-only log, never modify
  });
}

// Usage
auditLog('user.login', { userId: user.id, ip: req.ip, success: true });
auditLog('user.password_changed', { userId: user.id, ip: req.ip });
auditLog('admin.role_changed', {
  adminId: req.user.id,
  targetUserId: target.id,
  oldRole: target.role,
  newRole: newRole,
});
```

### Checklist
- [ ] Login attempts (success and failure) logged with user ID, IP, timestamp, user agent
- [ ] Sensitive operations logged: role changes, password resets, data exports, admin actions
- [ ] Logs are structured (JSON) and centralized (ELK, Datadog, Grafana Loki)
- [ ] Logs never contain passwords, tokens, or full credit card numbers
- [ ] Alerts configured for: multiple failed logins, privilege escalation, data exfiltration patterns
- [ ] Log integrity protected (append-only storage, tamper detection)

---

## A10:2021 — Server-Side Request Forgery (SSRF)

### Detection

```bash
# User-controlled URLs in outbound requests
grep -rn "fetch\|axios\|got\|http\.get\|http\.request\|requests\.get" --include="*.ts" | grep -v "const\|import"
```

### Exploitation

- **Classic SSRF:** Attacker supplies `http://169.254.169.254/latest/meta-data/` (AWS metadata endpoint).
- **Blind SSRF:** Outbound request succeeds but response not returned (still useful for port scanning internal network).

### Fix Patterns

**Before (Vulnerable):**
```typescript
// User supplies URL — SSRF risk
const { url } = req.body;
const response = await fetch(url); // Could hit internal services!
```

**After (Fixed):**
```typescript
import { URL } from 'url';

function safeFetch(userProvidedUrl: string) {
  const parsed = new URL(userProvidedUrl);

  // Block non-HTTP(S) protocols
  if (!['http:', 'https:'].includes(parsed.protocol)) {
    throw new Error('Invalid protocol');
  }

  // Resolve hostname to IP
  const { address } = await dns.resolve4(parsed.hostname);

  // Block private/reserved IP ranges
  const privateRanges = [
    /^10\./, /^172\.(1[6-9]|2\d|3[01])\./, /^192\.168\./,
    /^127\./, /^169\.254\./, /^0\./, /^::1$/, /^fc00:/, /^fe80:/,
  ];
  if (privateRanges.some(r => r.test(address))) {
    throw new Error('Requests to private IPs are not allowed');
  }

  return fetch(userProvidedUrl);
}
```

**Or use an allowlist:**
```typescript
const ALLOWED_HOSTS = [
  'api.example.com',
  'cdn.example.com',
  'public-api.thirdparty.com',
];

function safeFetch(url: string) {
  const hostname = new URL(url).hostname;
  if (!ALLOWED_HOSTS.includes(hostname)) {
    throw new Error(`Host ${hostname} not in allowlist`);
  }
  return fetch(url);
}
```

### Checklist
- [ ] Validation/allowlist on all user-supplied URLs before outbound requests
- [ ] Internal IP ranges blocked (RFC 1918, loopback, link-local, AWS metadata)
- [ ] Protocol restriction (only HTTP/HTTPS; no `file://`, `gopher://`, `dict://`)
- [ ] Redirection disabled on outbound HTTP clients (followRedirects: false, or validate each redirect)
- [ ] Network-level egress filtering if possible (security group rules blocking internal traffic)

---

## References
- [OWASP Top 10 (2021) Official](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE Top 25](https://cwe.mitre.org/top25/archive/2023/2023_stubborn_weaknesses.html)
