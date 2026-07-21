# Code Reviewer - Security Rules

Comprehensive OWASP Top 10 (2021) security review rules with per-language patterns and detection regex.

---

## A01: Broken Access Control

**What to look for:**
- Missing authentication checks on API endpoints
- Direct Object Reference (IDOR) — user-supplied IDs used without ownership verification
- CORS misconfiguration (`Access-Control-Allow-Origin: *` with credentials)
- Path traversal in file downloads (`../../../etc/passwd`)
- Missing CSRF tokens on state-changing requests
- JWT without signature verification or `alg: none`

**Detection Regex:**
```regex
# Missing auth decorator/annotation
@app\.route\(.*\)\n(?!.*@login_required|@require_auth|@authenticated)

# IDOR pattern — user ID from request directly in query
(\.findById|\.get\(|SELECT.*WHERE.*id\s*=).*(req\.params|request\.params|@PathVariable)

# Path traversal
\.\.\/|\.\.\\|path\.join.*request|os\.path\.join.*request
```

**Python:**
- Check all endpoints have `@login_required` or equivalent
- Validate object ownership in views: `obj = get_object_or_404(Model, pk=pk, owner=request.user)`
- Use Django's `PermissionRequiredMixin` for class-based views

**JavaScript:**
- Express: Every route must have auth middleware; avoid `app.use('*', handler)` without auth
- Next.js: Check `getServerSideProps` for session validation; don't rely on client-side only
- Check `req.user` is validated before use in authorized routes

**Go:**
- Every handler must check auth; avoid `// TODO: add auth` comments
- Use middleware chaining: `r.Use(authMiddleware)`
- Verify resource ownership before mutations: `if resource.UserID != currentUser.ID { ... }`

**Java:**
- `@PreAuthorize` on all secured methods
- Spring Security filter chain covers all endpoints
- Check `@PathVariable` values against `SecurityContextHolder` principal

---

## A02: Cryptographic Failures

**What to look for:**
- Hardcoded secrets, API keys, tokens, passwords
- Weak hashing: MD5, SHA1 for passwords
- Plaintext data transmission (HTTP, not HTTPS)
- Missing encryption at rest
- Weak random number generation (`Math.random()`, `rand()`)
- Insufficient key lengths (RSA < 2048, EC < 256)

**Detection Regex:**
```regex
# Hardcoded secrets
(api_key|API_KEY|secret|SECRET|password|PASSWORD|token|TOKEN)\s*[:=]\s*['"][A-Za-z0-9_\-\.]{8,}['"]
(?i)(private\s*key|private_key).*-----

# Weak hashes
md5\(|\.update\(.*\)\.hexdigest\(\)|MessageDigest\.getInstance\("MD5"\)|crypto\.createHash\('md5'\)

# HTTP instead of HTTPS
http://(?!localhost|127\.0\.0\.1)

# Weak random
Math\.random\(\)|rand\.Int\(\)(?!.*crypto/rand)|random\.randint\(
```

**Python:**
- Use `secrets` module for tokens, `hashlib` with SHA-256+ for non-password hashing
- Passwords: `bcrypt` or `argon2` via `passlib`; never `hashlib.sha256(password.encode())`
- Use `cryptography` library for encryption; never roll your own

**JavaScript:**
- Use `crypto.randomBytes()` not `Math.random()`
- Passwords: `bcryptjs` or `argon2`; never `sha256(password)`
- Store secrets in environment variables or secret manager; never in source

**Go:**
- Use `crypto/rand` not `math/rand`
- Passwords: `golang.org/x/crypto/bcrypt`
- Use `crypto/aes` + `crypto/cipher` for encryption; GCM mode preferred

**Java:**
- Use `java.security.SecureRandom` not `java.util.Random`
- Passwords: `BCryptPasswordEncoder` from Spring Security
- AES-GCM via `javax.crypto.Cipher`; never ECB mode

---

## A03: Injection

**What to look for:**
- SQL concatenation with user input
- Dynamic command execution (`exec`, `subprocess`, `os.system`)
- NoSQL injection (MongoDB `$where`, unvalidated JSON queries)
- LDAP injection (unfiltered search filters)
- XPath injection
- Template injection (Jinja2, EJS, Pug with user input)
- Log injection (`\n`, `\r` in log messages)

**Detection Regex:**
```regex
# SQL injection patterns
(execute|executemany|cursor\.execute|cursor\.executemany)\(['"](.*?)\+
['"].*?SELECT.*?['"].*?\+(.*?req|request|params|input|form)
\.format\(.*(req|request|params|input)\).*SELECT

# Command injection
os\.system\(|subprocess\.call\(|exec\(|eval\(|Popen\(.*shell\s*=\s*True
child_process\.exec\(|\.execSync\(

# NoSQL injection
\$where|\.find\(\{.*req\.(body|params|query)

# Template injection
render_template_string\(|\.render\(.*request|ejs\.render\(.*req

# XSS (reflected in HTML)
innerHTML\s*=|dangerouslySetInnerHTML|v-html=
document\.write\(|\.outerHTML\s*=
```

**Python:**
- Always use parameterized queries: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
- ORM filtering: `User.objects.filter(id=user_id)` — never raw SQL with f-strings
- Use `shlex.quote()` if shell commands unavoidable; prefer `subprocess.run([cmd, arg])` with list args
- Sanitize with `bleach` library for HTML

**JavaScript:**
- Use parameterized queries: `db.query('SELECT * FROM users WHERE id = $1', [userId])`
- ORMs: Prisma, Sequelize, TypeORM parameterize by default — watch for raw queries
- Sanitize HTML with `DOMPurify` on client, `sanitize-html` on server
- Avoid `eval()`, `new Function()`, `vm.runInNewContext()` with user input

**Go:**
- Use placeholders: `db.Query("SELECT * FROM users WHERE id = $1", userID)`
- Never `fmt.Sprintf` into SQL strings
- Use `html/template` not `text/template` for HTML output (auto-escapes)

**Java:**
- JDBC `PreparedStatement`: `conn.prepareStatement("SELECT * FROM users WHERE id = ?")`
- JPA parameter binding: `entityManager.createQuery("...").setParameter("id", id)`
- OWASP ESAPI for encoding; Spring's `HtmlUtils.htmlEscape()`

---

## A04: Insecure Design

**What to look for:**
- Missing rate limiting on login, password reset, API endpoints
- No input validation on critical fields
- Missing confirmation steps for sensitive operations
- User-controlled security decisions (e.g., `isAdmin` in request body)
- Insecure defaults (debug mode on, verbose errors)

**Detection Regex:**
```regex
# Rate limit absence check
(?:login|signin|reset).*?(???!rate.limit|throttle)

# Admin flag in request body
req\.body\.isAdmin|request\.data\.get\('role'|@RequestParam.*role
```

**All Languages:**
- Implement rate limiting (express-rate-limit, django-ratelimit, golang.org/x/time/rate)
- Validate all inputs with schema validation (Joi, Pydantic, go-playground/validator, Jakarta Validation)
- Sensitive operations (delete account, transfer funds) require re-authentication

---

## A05: Security Misconfiguration

**What to look for:**
- Debug mode enabled in production (`DEBUG=True`, `NODE_ENV=development`)
- Verbose error messages with stack traces to users
- Default credentials in config files
- Unnecessary HTTP methods (PUT, DELETE, TRACE) enabled
- Missing security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- Directory listing enabled
- Cloud storage buckets with public access

**Detection Regex:**
```regex
# Debug mode
DEBUG\s*=\s*True|NODE_ENV\s*=\s*['"]development['"]
DEBUG\s*=\s*True|app\.run\(debug\s*=\s*True\)

# Default credentials  
admin\s*:\s*admin|root\s*:\s*root|password\s*:\s*['"]password['"]

# Stack traces
traceback\.print_exc\(\)|console\.error\(err\.stack\)|e\.printStackTrace\(\)
```

---

## A06: Vulnerable & Outdated Components

**What to look for:**
- Dependencies with known CVEs (run `npm audit`, `pip audit`, `go mod tidy`, `mvn dependency-check`)
- Unpinned versions (`^1.0.0`, `~1.0.0`, `>=1.0.0`, `*`)
- Unmaintained packages (no commits in 1+ year)
- Transitive dependencies not scanned

**Detection Regex:**
```regex
# Unpinned versions
"[*^~>]=?\s*\d|version\s*=\s*">="|:latest|@latest
```

---

## A07: Identification & Authentication Failures

**What to look for:**
- Weak password policy (no length/complexity requirements)
- No brute-force protection (account lockout, progressive delays)
- Session tokens in URL parameters
- Session not invalidated on logout
- Missing MFA for sensitive operations
- Weak password reset tokens (predictable, no expiry)
- Sessions without `HttpOnly`, `Secure`, `SameSite` flags
- JWT without expiry (`exp` claim)

**Detection Regex:**
```regex
# Session in URL
[sS]essionId=|\?token=|&token=

# Weak password validation
password\.length\s*<\s*[1-7]|min_length\s*=\s*[1-7]

# JWT without expiry
jwt\.(sign|encode)\(.*,\s*['"]secret.*\)(?!.*expiresIn|exp)
```

---

## A08: Software & Data Integrity Failures

**What to look for:**
- Insecure deserialization (`pickle.loads()`, `yaml.load()` without SafeLoader, `unserialize()`)
- Unsigned or unverified updates
- Missing Subresource Integrity (SRI) on CDN scripts
- CI/CD pipeline without artifact signing
- Dependencies from untrusted sources

**Detection Regex:**
```regex
# Unsafe deserialization
pickle\.loads\(|yaml\.load\((?!.*SafeLoader)|unserialize\(|ObjectInputStream|JSON\.parse\(.*res\.body

# CDN without SRI
<script.*src="https://(?:cdn|unpkg|jsdelivr).*"(?!.*integrity=)
```

---

## A09: Security Logging & Monitoring Failures

**What to look for:**
- Login failures not logged
- No audit trail for sensitive operations (data access, privilege changes)
- Logs without sufficient context (no user ID, timestamp, IP)
- PII/credentials in log messages
- No alerts for suspicious patterns (multiple failed logins, unusual IPs)

**Detection Regex:**
```regex
# PII in logs
logger\.(info|debug|error)\(.*password|log\(.*token|console\.log\(.*secret

# Missing error logging
except\s+\w+:\s*\n\s+pass|catch\s*\(.*\)\s*\{\s*\}
```

---

## A10: Server-Side Request Forgery (SSRF)

**What to look for:**
- User-supplied URLs fetched without validation
- No allowlist for outbound requests
- DNS rebinding potential
- Internal service URLs accessible from user-controlled parameters

**Detection Regex:**
```regex
# Unvalidated URL fetch
requests\.get\((?:.*req|params|input|body)|fetch\(.*(?:req|params|input|body)
axios\.(get|post)\((?:.*req|params)|http\.Get\((?:.*req|params)
URL\(.*(?:req|params|input)\).*openConnection

# Internal URL pattern
url\s*=\s*['"]http://(?:localhost|127\.|10\.|172\.1[6-9]|172\.2|192\.168)
```

**All Languages:**
- Validate URLs against allowlist of domains
- Block internal IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16)
- Use URL parsing library to validate scheme (only http/https) and resolve hostname
- Disable redirect following or validate redirect targets

---

## Language-Specific Quick Reference

### Python
| Issue | Bad | Good |
|-------|-----|------|
| SQL Injection | `cursor.execute(f"SELECT * FROM users WHERE id={user_id}")` | `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))` |
| Command Injection | `os.system(f"ping {host}")` | `subprocess.run(["ping", host])` |
| Deserialization | `pickle.loads(data)` | `json.loads(data)` |
| Secrets | `API_KEY = "sk-abc123"` | `API_KEY = os.environ["API_KEY"]` |
| Passwords | `hashlib.md5(pw.encode()).hexdigest()` | `bcrypt.hashpw(pw.encode(), bcrypt.gensalt())` |

### JavaScript/TypeScript
| Issue | Bad | Good |
|-------|-----|------|
| SQL Injection | `` db.query(`SELECT * FROM users WHERE id = ${id}`) `` | `db.query('SELECT * FROM users WHERE id = $1', [id])` |
| XSS | `element.innerHTML = userInput` | `element.textContent = userInput` |
| Eval | `eval(userCode)` | Use parser or sandbox |
| Secrets | Hardcoded in `.js` | `process.env.SECRET` via `dotenv` |
| Random | `Math.random().toString(36)` | `crypto.randomBytes(32).toString('hex')` |

### Go
| Issue | Bad | Good |
|-------|-----|------|
| SQL Injection | `db.Query("SELECT * FROM users WHERE id = " + id)` | `db.Query("SELECT * FROM users WHERE id = $1", id)` |
| HTML XSS | `text/template` for HTML | `html/template` (auto-escapes) |
| Random | `rand.Intn(100)` | `crypto/rand.Int(rand.Reader, big.NewInt(100))` |
| Passwords | Custom hash | `bcrypt.GenerateFromPassword([]byte(pw), bcrypt.DefaultCost)` |

### Java
| Issue | Bad | Good |
|-------|-----|------|
| SQL Injection | `statement.executeQuery("SELECT * FROM users WHERE id = " + id)` | `preparedStatement.setInt(1, id)` |
| XXE | `DocumentBuilderFactory.newInstance()` | Factory with `FEATURE_SECURE_PROCESSING` and disable DTDs |
| Serialization | `ObjectInputStream` on untrusted data | Use `SerializationFilter` or JSON |
| Passwords | `MessageDigest.getInstance("MD5")` | `BCryptPasswordEncoder` from Spring Security |
