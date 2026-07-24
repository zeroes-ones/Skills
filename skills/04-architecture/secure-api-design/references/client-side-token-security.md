# Client-Side Token Security — Reference

## The Problem: SPAs Cannot Securely Store Tokens

Single-Page Applications have no secure persistence mechanism:
- **localStorage/sessionStorage:** Synchronously readable by any JavaScript on the origin. One XSS vulnerability = all tokens exfiltrated in milliseconds.
- **Closure variables (in-memory):** Lost on page refresh. Acceptable for short-lived access tokens only.
- **IndexedDB:** Asynchronously readable by JavaScript. Slightly harder to exploit but still vulnerable.
- **Cookies without httpOnly:** Readable via `document.cookie` — same vulnerability as localStorage.
- **Cookies with httpOnly:** ✅ Not accessible to JavaScript. The ONLY browser-native secure storage.

## The BFF (Backend-for-Frontend) Pattern

```
┌─────────────────┐     Session Cookie      ┌─────────────────┐     OAuth2 Token       ┌─────────────────┐
│   SPA (Browser)  │ ◄──────────────────────►│   BFF (Server)   │ ◄─────────────────────►│   API Server     │
│                  │   httpOnly, Secure,     │                  │   Bearer token in     │                  │
│  No tokens here  │   SameSite=Strict       │  Holds access +  │   Authorization       │  Validates JWT,  │
│  Just a cookie   │                         │  refresh tokens  │   header              │  enforces authZ  │
└─────────────────┘                         └─────────────────┘                        └─────────────────┘
```

### BFF Implementation (Node.js/Express):
```javascript
// BFF issues session cookie to SPA
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const tokens = await authServer.authenticate(username, password);
    
    // Store tokens server-side in session (Redis)
    req.session.tokens = tokens;
    
    // Issue httpOnly cookie to SPA (token never reaches browser)
    res.cookie('session_id', req.sessionID, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 3600000  // 1 hour
    });
    res.json({ user: tokens.user });
});

// BFF proxies API calls with real token
app.get('/api/*', async (req, res) => {
    const response = await fetch(`https://api.internal${req.path}`, {
        headers: {
            'Authorization': `Bearer ${req.session.tokens.access_token}`
        }
    });
    res.json(await response.json());
});

// BFF transparently refreshes tokens
app.use(async (req, res, next) => {
    if (req.session.tokens && isExpired(req.session.tokens.access_token)) {
        const newTokens = await authServer.refresh(req.session.tokens.refresh_token);
        req.session.tokens = newTokens;
    }
    next();
});
```

## Token Refresh Strategies

### Refresh Token Rotation
Every refresh operation issues a NEW refresh token and invalidates the old one:
```
1. Client (BFF) → POST /token { grant_type: "refresh_token", refresh_token: "RT_OLD" }
2. Auth Server: validates RT_OLD, issues { access_token: "AT_NEW", refresh_token: "RT_NEW" }
3. Auth Server: invalidates RT_OLD (single-use only)
4. If RT_OLD is ever used again → REVOKE ALL TOKENS FOR USER (token theft detected!)
```

### Service Worker Token Refresh (BFF Alternative)
For SPAs that cannot deploy a BFF, a Service Worker can intercept 401 responses:
```javascript
// service-worker.js
self.addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
    const response = await fetch(request);
    if (response.status === 401) {
        const newToken = await refreshAccessToken();
        // Retry with new token
        const newRequest = new Request(request, {
            headers: new Headers({...request.headers, 'Authorization': `Bearer ${newToken}`})
        });
        return fetch(newRequest);
    }
    return response;
}
```

## CSP (Content Security Policy) for API-Driven SPAs

```nginx
# HTTP response header
Content-Security-Policy:
    default-src 'self';
    script-src 'self' 'nonce-{random}';
    style-src 'self' 'unsafe-inline';
    img-src 'self' https://cdn.example.com;
    connect-src 'self' https://api.example.com;
    frame-ancestors 'none';
    base-uri 'self';
    form-action 'self';
    report-uri /csp-violation-report;
```

- `script-src 'self'`: No inline scripts, no `eval()` — prevents DOM XSS from executing arbitrary JS
- `connect-src https://api.example.com`: Restricts which origins the app can call — limits data exfiltration
- `frame-ancestors 'none'`: Prevents clickjacking
- `report-uri /csp-violation-report`: Monitor CSP violations — these indicate XSS attempts

## Mobile API Key Obfuscation

Mobile apps cannot truly secure secrets (everything in the APK/IPA is extractable):
- **Never** hardcode API keys or secrets in the app binary
- **Certificate pinning**: Pin the expected server certificate to prevent MITM via untrusted CA
- **Device attestation**: Use SafetyNet (Android) or DeviceCheck (iOS) to verify device integrity
- **Runtime secret delivery**: Fetch API keys at runtime after device attestation check
- **OAuth2 with PKCE**: For mobile OAuth2, use PKCE (Proof Key for Code Exchange) — mandatory for native apps
