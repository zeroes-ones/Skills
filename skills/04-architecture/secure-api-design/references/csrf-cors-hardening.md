# CSRF & CORS Hardening — Reference

## SameSite Cookie Attributes

| Value | Behavior | Security | Use Case |
|-------|----------|----------|----------|
| `Strict` | Cookie sent ONLY for same-site requests | Highest — blocks all cross-site requests | Auth/session cookies (most secure) |
| `Lax` | Cookie sent for same-site + top-level navigation GET | High — allows link clicks from external sites | Session cookies when UX requires external link support |
| `None` | Cookie sent for all requests | Low — MUST be combined with `Secure` | Cross-site embeds, OAuth flows (use sparingly) |

**Default in modern browsers (Chrome 80+): `SameSite=Lax`.** Always explicitly set SameSite — do not rely on defaults.

## Secure Cookie Configuration
```
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=3600
```
- `HttpOnly` — Not accessible via `document.cookie` (prevents XSS-based cookie theft)
- `Secure` — Only transmitted over HTTPS
- `SameSite=Strict` — Not sent on cross-site requests (prevents CSRF)
- `Path=/` — Available to all paths on the origin
- `Max-Age` — Short lifetime for session cookies

## Double-Submit Cookie Pattern

For APIs that cannot use SameSite cookies (e.g., cross-origin SPA):

1. Server sets a random CSRF token in a cookie: `csrf_token=<random>; SameSite=None; Secure`
2. Client reads the cookie value (accessible because SameSite=None)
3. Client sends the token back in a custom header: `X-CSRF-Token: <token_value>`
4. Server compares: cookie value === header value
5. Attacker on evil.com cannot read the cookie (different origin) and cannot set the header (browser blocks custom headers in cross-origin requests without CORS)

```javascript
// Server: Set CSRF cookie
res.cookie('csrf_token', crypto.randomBytes(32).toString('hex'), {
    httpOnly: false,  // Must be readable by JavaScript
    secure: true,
    sameSite: 'none'  // Allow cross-origin access
});

// Server: Validate CSRF
const cookieToken = req.cookies.csrf_token;
const headerToken = req.headers['x-csrf-token'];
if (!cookieToken || !headerToken || cookieToken !== headerToken) {
    return res.status(403).json({ error: 'CSRF token mismatch' });
}
```

## Origin Header Validation (Never Reflect!)

### Vulnerable (Origin Reflection Attack):
```javascript
// 😱 NEVER: Unvalidated reflection
res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
```

### Secure (Allowlist Validation):
```javascript
const ALLOWED_ORIGINS = new Set([
    'https://app.example.com',
    'https://admin.example.com',
]);

const origin = req.headers.origin;
if (ALLOWED_ORIGINS.has(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
}
// If origin is not in allowlist: DO NOT add CORS headers
```

### Origin Validation Gotchas:
- `null` origin: Comes from sandboxed iframes, `file://` URLs, data: URLs — never allow
- Regex matching: `/.*\.example\.com$/` matches `attacker.example.com.evil.com` — use exact string comparison
- `Origin` header can be spoofed by non-browser clients — CORS only protects browser-based users

## CORS Preflight Configuration

```
OPTIONS /api/users HTTP/1.1
Origin: https://app.example.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Content-Type, Authorization

HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 3600
```

Key points:
- Preflight uses OPTIONS method — do not require authentication for OPTIONS
- Return 204 No Content (no body needed)
- `Access-Control-Max-Age: 3600` — cache preflight for 1 hour (max browser limit is 86400)
- `Access-Control-Allow-Credentials: true` REQUIRES explicit origin (never `*`)
