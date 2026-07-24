# Secure Code Review

## The Security Reviewer's Triangle

Every security code review must explicitly cover these three areas. Coverage of authN + authZ + input validation catches 90%+ of critical vulnerabilities.

### 1. Authentication (AuthN)
Questions to ask:
- How is the user/service identity verified? JWT? Session cookie? API key? mTLS?
- JWT: Is the algorithm validated against an allowlist? Is exp checked? Is the signature verified?
- Session: Are cookies HttpOnly, Secure, SameSite? Is session ID rotated on login?
- API Key: Is it compared using constant-time comparison? Is it hashed for storage?
- Password: Is bcrypt/argon2 used? What's the minimum length? Is there account lockout?

### 2. Authorization (AuthZ)
Questions to ask:
- Is there an authorization check on EVERY endpoint? Not just "most" -- every single one.
- Insecure Direct Object Reference (IDOR): Can user X access user Y's data by changing an ID parameter?
- Privilege escalation: Can a user change their role by modifying a request parameter?
- Client-side vs server-side: Are permission checks done server-side? Client-side checks are decoration, not security.
- Multi-tenancy: If this is a multi-tenant app, are tenant boundaries enforced on every query?

### 3. Input Validation
Questions to ask:
- SQL: Are all queries parameterized? Any string concatenation is a finding.
- HTML: Is output encoded contextually (HTML, JS, CSS, URL)? DangerouslySetInnerHTML and innerHTML with user data are findings.
- File uploads: Is the type validated server-side? Is there a size limit? Are files stored outside web root?
- Commands: Is user input passed to exec/system/spawn? If so, how is it sanitized? Shell=False, args as list?
- XML: Is external entity processing disabled? Is DTD processing disabled?
- Deserialization: Is deserialization from untrusted source happening? RED FLAG -- find a different approach.

## Language-Specific Anti-Patterns Quick Reference

### Python
- eval()/exec() with user input -> RCE
- pickle.loads() on untrusted data -> RCE
- yaml.load() instead of yaml.safe_load() -> RCE
- os.system() with user input -> Command injection
- SQL string formatting (f"SELECT * FROM users WHERE id={user_id}") -> SQL injection
- DEBUG=True and detailed error pages in production -> Information disclosure

### JavaScript/TypeScript
- eval()/Function() with user input -> RCE
- dangerouslySetInnerHTML / innerHTML with user data -> XSS
- NoSQL injection: { "$gt": "" } in MongoDB queries -> Auth bypass
- JWT without algorithms option (jsonwebtoken) -> Algorithm confusion
- JSON.parse() on untrusted input without try/catch -> DoS via prototype pollution

### Java
- Runtime.exec() with user input -> Command injection
- ObjectInputStream deserialization from untrusted source -> RCE
- XML parsing without disabling XXE -> XXE injection
- String comparison for secrets (== instead of MessageDigest.isEqual) -> Timing attack
- Log4j 1.x or Log4j 2.x < 2.17.0 in classpath -> RCE (Log4Shell)

### Go
- template.HTML() with user data (no auto-escaping in html/template) -> XSS
- os/exec with user input -> Command injection
- crypto/md5 or crypto/sha1 for security purposes -> Weak hashing
- math/rand for token generation -> Predictable tokens (use crypto/rand)
- database/sql with fmt.Sprintf -> SQL injection

## Crypto API Misuse Detection

Red flags that should stop a code review:
- AES in ECB mode (patterns visible in ciphertext)
- RSA with PKCS#1 v1.5 padding (Bleichenbacher attack)
- Custom random number generator or non-cryptographic PRNG (Math.random, rand())
- Custom hash construction (HMAC-SHA256 is standard, anything else is suspect)
- Hardcoded encryption keys, IVs, or salts
- Key derived from password without KDF (use PBKDF2, bcrypt, or argon2 for key derivation)
