# JWT Hardening

## Algorithm Confusion Attack Prevention

The algorithm confusion attack exploits servers accepting both HS256 and RS256/ES256:
1. Attacker obtains RS256 public key from JWKS endpoint
2. Crafts JWT header: {"alg": "HS256", "typ": "JWT"}
3. Uses RS256 public key as HMAC secret to sign arbitrary claims
4. Server validates with HS256 using public key as HMAC secret -> success
5. Attacker has forged a valid admin token

**Mitigation:**
- Never configure JWT library to accept both symmetric and asymmetric algorithms with shared key material
- Use separate key instances for signing and HMAC
- Algorithm allowlist: algorithms=["RS256", "ES256"] -- reject everything else
- Reject "none" algorithm explicitly on every validation call

## Key Rotation Schedule

| Phase | Action | Timing |
|-------|--------|--------|
| 1. Pre-publish | Generate new key pair, add public key to JWKS endpoint | T minus 24 hours |
| 2. Overlap | Both old and new keys present in JWKS. Old key still used for signing. | T minus 24h to T |
| 3. Switch | Authorization server begins signing with new key | T (zero hour) |
| 4. Drain | Old tokens still valid until expiry (max 15 min). Both keys in JWKS. | T to T + 15min |
| 5. Retire | Remove old key from JWKS. All old tokens expired. | T + 15min |

## DPoP (Demonstration of Proof-of-Possession -- RFC 9449)

DPoP binds access tokens to a specific client instance:
- Client generates DPoP key pair (one per client instance, not per request)
- Each request includes DPoP proof JWT in DPoP header with:
  - ath claim: SHA-256 hash of the access token (binds proof to token)
  - htm claim: HTTP method (binds proof to method)
  - htu claim: HTTP URL (binds proof to URL)
  - jti claim: unique nonce (prevents proof replay)
- Server validates: proof signature, ath matches token, htm/htu match request, jti not reused

## Claim Minimization Principles

- sub: pairwise by default (unique per client) to prevent correlation across services
- NEVER include: internal user IDs, database row IDs, raw email without explicit need
- NEVER include: passwords, hashes, PII (SSN, DOB), internal role names without review
- aud: MUST match the resource server's expected identifier with strict string comparison
- exp: 5-15 minutes for access tokens (shorter = smaller stolen token window)
- Custom claims: namespace with service prefix (e.g., urn:myapp:department) to prevent collisions
