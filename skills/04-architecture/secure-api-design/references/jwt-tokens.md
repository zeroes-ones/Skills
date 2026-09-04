# How JWT Works — Tokens, Verification, and the Security Reality

> Original explainer for interview prep and learning. [research-source: title-only]

## What a JWT is

A JSON Web Token is a compact, self-contained, signed token: the server signs it once, and any party holding the secret/public key can **verify it without a session lookup**. Structure: `header.payload.signature`, each part base64url-encoded, joined by dots.

```
header:  { "alg": "RS256", "typ": "JWT" }
payload: { "sub": "user_123", "scope": "read orders", "exp": 1730000000 }
signature: HMAC-SHA256( base64(header) + "." + base64(payload), secret )   // HS256
         or RSA/ECDSA signature with the private key                       // RS256 / ES256
```

## The token lifecycle (know it precisely)

1. **Issue** — client authenticates (password, OAuth code); server creates a JWT with claims (`sub`, `exp`, `iat`, scopes) and signs it.
2. **Present** — client sends it in the `Authorization: Bearer <jwt>` header on every request.
3. **Verify (stateless)** — the server checks: signature (with the shared secret for HS256 or the public key for RS256/ES256), **exp** not passed, issuer/audience if set, and then trusts the claims — **no session store hit**.

That statelessness is the appeal: horizontal scaling, no server-side session storage, works across services that share the verification key.

## The security traps (interview gold — most JWT systems fail on these)

- **Algorithm confusion / `alg: none`** — if the server trusts the token's `alg` header, an attacker can set `alg: none` (no signature) or `alg: HS256` against an RS256 public key (using the public key as the HMAC secret). Fix: **pin the algorithm server-side**; never derive it from the token; reject `none`.
- **Signature = integrity, not confidentiality** — the payload is base64, **not encrypted**. Anyone can read claims. Never put secrets in a JWT.
- **`exp` is advisory** — you must check it. Missing `exp` = token that never expires.
- **Revocation is the hard problem** — stateless tokens can't be "logged out" server-side until they expire. Real fixes:
  - **Short `exp`** (minutes) + **refresh token** (long-lived, stored server-side, revocable, rotated).
  - **Token version / allowlist** for high-risk actions (password change bumps the version and invalidates all older tokens).
  - **Denylist** (short list of revoked jti until exp) only for emergencies — keep it small.
- **Secret handling** — HS256 needs the shared secret on every verifier; prefer **asymmetric (RS256/ES256)** so services verify with a public key and only the issuer holds the private key.
- **Storage on the client** — localStorage is XSS-readable; httpOnly cookies reduce XSS exposure but need CSRF protection. Choose per threat model (SPA + httpOnly cookie vs mobile + secure storage).
- **Key rotation** — sign with a new key, verify with old+new during transition.

## JWT vs server sessions (the honest trade-off)

| | JWT (stateless) | Server session |
|---|---|---|
| Lookup cost | None (self-contained) | One store read per request |
| Horizontal scale | Trivial | Need shared session store |
| Revoke instantly | Hard (until exp) | Easy (delete session) |
| Payload visibility | Client-readable | Server-side |
| Fit | Distributed services, APIs, mobile | Classic web apps needing logout control |

Rule of thumb: prefer **short-lived JWT access + revocable refresh token** — you get stateless verification for the hot path and server-side control for logout.

## How Token Refresh Actually Works

Refresh is how you keep the JWT's stateless fast-path *and* get server-side revocation. The pattern: a short-lived **access token** (minutes) for API calls, plus a long-lived **refresh token** that is *not* a stateless JWT you trust blindly — it is an **opaque, server-stored, revocable credential** whose only job is to mint new access tokens.

### The refresh flow (step by step)

1. **Login** → server issues two things:
   - access token (JWT, `exp` ≈ 5–15 min)
   - refresh token (opaque random string, stored server-side with the user + family id + expiry ≈ 7–30 days), returned in an httpOnly cookie or secure storage.
2. **API calls** → client sends the access JWT in `Authorization: Bearer …`; services verify it statelessly.
3. **Access expires** → client calls `POST /auth/refresh` with the refresh token (cookie or body).
4. **Server validates** the refresh token: exists? not revoked? not expired? belongs to this user? Then it **rotates**: marks the presented refresh token used, issues a *new* access token **and a new refresh token**, and returns both.
5. **Repeat** — each refresh mints a fresh pair; the old refresh token is dead after use.

### Why rotate (and reuse detection)

Rotation means a stolen refresh token works **once**. The critical guard: if a refresh token is presented *again* after it was already rotated, that is **reuse** — a signal the token was stolen. Standard response: **revoke the whole token family** (all refresh tokens for that user/session) and force re-login. This turns refresh-token theft from "attacker has a 30-day key" into "attacker gets one token, then the family is killed."

### Concurrency: the refresh race

A mobile app can fire two API calls at once when the access token expires → two simultaneous refreshes. If both present the *same* refresh token, the naive rotation would treat the second as reuse and log the user out. Fixes:
- **Grace window:** allow the same refresh token twice within a few seconds (sliding reuse window), then rotate.
- **Atomic rotate-and-return:** the second request can return the *same* new pair if the rotation already happened (server stores the latest pair per family id) — idempotent refresh.
- Or accept that a race logs the user out and retry login — poor UX; avoid it.

### Where to store the refresh token

| Storage | XSS risk | CSRF risk | Best for |
|---|---|---|---|
| httpOnly + Secure + SameSite cookie | Low (JS can't read it) | Needs CSRF protection (SameSite helps) | Browser/SPA |
| Secure device storage (Keychain/Keystore) | Low | N/A | Mobile apps |
| localStorage / sessionStorage | High (XSS reads it) | N/A | Avoid unless accepted |

Access token stays in memory (or a short-lived cookie); refresh token lives where XSS can't reach it.

### Logout, revocation & the trade-off table

- **Logout** = revoke/delete the server-side refresh token (and bump a token-version claim if you want all sessions dead). The access token dies by its short `exp` — that is why it is short.
- **Password change / suspicious activity** = bump `token_version` or delete all refresh tokens for the user → all sessions die immediately regardless of access-token `exp` (services check the version claim).
- **Trade-off:** you gave up pure statelessness for the *refresh* endpoint (it needs the store) — but the hot path (every API call) stays stateless. That is the correct, common architecture.

## Interview answer skeleton

"A JWT is a signed, self-contained token: header, payload, signature. The server verifies the signature with a pinned algorithm and checks exp — no session lookup. The pitfalls are what matter: pin the algorithm (alg-confusion attacks), keep secrets out of the payload (it's not encrypted), handle revocation with short exp + a server-side refresh token, and use asymmetric signing so only the issuer holds the private key."

## Anti-patterns

- ❌ Trusting the `alg` header (algorithm confusion / `alg: none`).
- ❌ Putting sensitive data in the payload and calling it "encrypted."
- ❌ Long-lived access tokens with no revocation story.
- ❌ Storing tokens where XSS can read them without accepting that risk.
- ❌ Not checking `exp`/`iss`/`aud`.

## Deliberate-practice drills

1. **Anatomy drill:** decode a real JWT at jwt.io — identify header/payload/signature and which claims matter.
2. **Attack drill:** explain the `alg: none` and HS256-vs-RS256 confusion attacks and the server-side fix for each.
3. **Lifecycle drill:** design issue → short access → refresh → rotation → logout revocation for a mobile app.
4. **Comparison drill:** JWT vs session cookie for a fintech SPA — security and UX trade-offs.
5. **Interview drill:** "your JWT is stateless — how do you log a user out?" — answer with refresh-token revocation, token version, and short exp.

## References
- See also: how-databases-store-passwords.md (this repo)
- `secure-api-design` SKILL.md — OAuth2 validation, token handling, OWASP API Top 10
- `cryptography` SKILL.md — signature algorithms, key management and rotation
