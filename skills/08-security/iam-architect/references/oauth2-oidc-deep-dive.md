# OAuth2/OIDC Deep Dive

## Grant Type Decision Matrix

| Grant Type | Client Type | User Present? | PKCE Required? | Client Auth | Use Case |
|-----------|-------------|---------------|----------------|-------------|----------|
| Authorization Code + PKCE | Public, Confidential | Yes | Yes (S256) | None (public) / client_secret (confidential) | Web apps, SPAs, mobile, CLI, TV |
| Client Credentials + mTLS | Confidential | No | No | mTLS or private_key_jwt | Service-to-service, machine-to-machine |
| Device Code (RFC 8628) | Public | Yes | No | None | Input-constrained devices (TV, IoT, CLI) |
| Refresh Token Rotation | Public, Confidential | N/A | N/A | client_secret or none | Offline access, silent token renewal |

## PKCE Implementation Guide

### Code Verifier Generation
The code verifier is a cryptographically random string of 43-128 characters from the unreserved character set: [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"

Python: secrets.token_urlsafe(96)[:128]
Node.js: crypto.randomBytes(96).toString('base64url').slice(0, 128)
Go: base64.RawURLEncoding.EncodeToString(randomBytes[:96])

### Code Challenge Derivation
code_challenge = BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))

### Flow Validation Checklist
- State parameter: cryptographically random, one-time use, validated on callback
- Redirect URI: exact match, no pattern matching, no wildcards
- Code challenge method: S256 only -- reject plain
- Authorization code: single-use, expiry <=10 minutes
- Token endpoint: validate code_verifier against stored code_challenge

## Token Validation Pipeline (Resource Server)

1. Extract token from Authorization header: Bearer <token>
2. Decode JWT header, check alg is in allowlist (RS256, ES256)
3. Fetch JWKS from authorization server (cache 5 minutes)
4. Verify signature using matching kid from JWKS
5. Validate claims: exp (not expired), nbf (not before now), iss (matches auth server URL), aud (contains this resource server)
6. Validate scopes cover the requested operation
7. Optional: call token introspection endpoint for active state check
