# API Authentication Patterns — Reference

## Token Type Comparison

| Dimension | JWT (Self-Contained) | Opaque Token (Reference) |
|-----------|---------------------|--------------------------|
| Validation | Stateless — verify signature locally | Stateful — call introspection endpoint |
| Latency | ~0ms (no network call) | ~5-20ms (introspection RTT + cache lookup) |
| Revocation | Requires token denylist (cache of revoked JTIs) | Instant — delete from auth server DB |
| Information exposure | Claims are base64-encoded (NOT encrypted by default) | No information in token — random string only |
| Size | ~800-2000 bytes (header + payload + signature) | ~40-80 bytes (random string) |
| Best for | Internal microservices, low-latency requirements | External APIs, third-party clients, high security |

## JWT Validation Checklist

Every JWT validation call MUST verify all of these:

1. **Algorithm pinning:** `algorithms: ['RS256']` — reject any token with an unexpected `alg` header value
2. **Signature verification:** Verify using the public key from JWKS, matching `kid` header to the correct key
3. **Expiration (`exp`):** Reject if `now > exp + 30s` (30s clock skew tolerance maximum)
4. **Not Before (`nbf`):** Reject if `now < nbf - 30s`
5. **Issuer (`iss`):** Exact string match against expected issuer URL (case-sensitive)
6. **Audience (`aud`):** Must contain this API's `client_id` or service identifier
7. **Subject (`sub`):** Must be present and non-empty
8. **Issued At (`iat`):** Should be in the past (not unreasonably far in the future)

## JWKS Key Rotation Strategy

- **Rotation interval:** 90 days (or 30 days for high-security environments)
- **Overlap window:** Maintain 2 active keys during rotation (current + next)
- **JWKS endpoint:** `/.well-known/jwks.json` — publicly accessible, cached by clients
- **Key retirement:** After rotation, keep the old key available for `max_token_lifetime + clock_skew` before deletion
- **Emergency rotation:** Support forced rotation via operational toggle — publish new key, set old key expiry to now, wait `max_token_lifetime`, delete old key

## API Key Hashing & Scanning

API keys MUST be treated like passwords in storage:
- **Generation:** `secrets.token_urlsafe(32)` — 256 bits of entropy from `secrets` module
- **Storage:** `SHA-256(key)` — store only the hash, never the plaintext
- **Prefix:** Store first 8 characters as plaintext for display/identification (e.g., `sk_live_abc12345`)
- **Lookup:** `SELECT * FROM api_keys WHERE prefix = $1 AND key_hash = $2`
- **Scanning:** Define regex pattern (`sk_live_[a-zA-Z0-9]{32,}`) for GitHub secret scanning

## mTLS Configuration

For service-to-service authentication, mTLS provides stronger security than API keys:
- **CA:** Private CA (step-ca, cert-manager, Vault PKI) — not public CA
- **Client certificate validation:** Verify CN matches expected service identity, check not revoked (CRL or OCSP), check within validity period
- **Certificate rotation:** 30-90 day lifetime, automated renewal
- **Defense in depth:** Combine mTLS (proves service identity) + token (proves end-user identity)
