# Digital Signatures Reference

## Scheme Selection Matrix

| Scheme | Security (bits) | Key Size | Signature Size | Speed | Best For |
|--------|----------------|----------|---------------|-------|----------|
| Ed25519 | ~128 | 32 bytes | 64 bytes | Fastest | Greenfield, modern systems |
| ECDSA P-256 | ~128 | 32 bytes | 64-72 bytes | Fast | FIPS compliance |
| ECDSA P-384 | ~192 | 48 bytes | 96-104 bytes | Medium | High-security, CNSA |
| RSA-PSS 4096 | ~152 | 512 bytes | 512 bytes | Slow (verify fast) | Legacy interop |
| Dilithium3 (PQ) | ~192 | 3368 bytes | 1776 bytes | Medium-fast | Post-quantum readiness |

## Ed25519 (RFC 8032)

### Advantages
- Deterministic nonce derivation (RFC 8032 §5.1.6): immune to weak-RNG attacks
- Constant-time reference implementation
- No point validation required for public keys
- 32-byte keys, 64-byte signatures — smallest of any scheme at equivalent security
- FIPS 186-5 approved (2023), pending FIPS 140-3 validation

### Implementation Notes
- Use libsodium `crypto_sign_*` or `ed25519-dalek` (Rust), `golang.org/x/crypto/ed25519`
- Never implement Ed25519 from scratch (subtle point encoding edge cases)

## ECDSA with RFC 6979 (Deterministic)

### The Nonce Reuse Problem
- Non-RFC 6979 ECDSA: nonce k must be random and unique per signature
- Reusing k with same private key: attacker solves for private key algebraically
- Real-world exploit: Sony PlayStation 3 (2010) — reused ECDSA nonce → root signing key extracted

### RFC 6979 Solution
- Derives k deterministically from: HMAC_DRBG(private_key || hash(message))
- Eliminates RNG dependency for nonce generation
- Same message + same key = same signature (deterministic, not a bug)

## RSA-PSS vs PKCS#1 v1.5

| Property | RSA-PSS (RFC 8017) | PKCS#1 v1.5 |
|----------|-------------------|-------------|
| Security proof | Provable reduction to RSA problem | No security proof |
| Padding oracle | Immune | Bleichenbacher vulnerable |
| Randomized | Yes (salt) | Partially deterministic |
| Adoption | TLS 1.3, modern systems | Legacy everywhere |
| Status | RECOMMENDED | DEPRECATED |

## JWT Signing Algorithm Selection

| Algorithm | JWT `alg` | Key Type | Token Size | Recommendation |
|-----------|-----------|----------|------------|----------------|
| EdDSA | `EdDSA` | Ed25519 key | ~86 bytes | Best choice for new systems |
| ECDSA P-256 | `ES256` | P-256 key | ~86 bytes | Good, widely supported |
| ECDSA P-384 | `ES384` | P-384 key | ~104 bytes | High-security |
| RSA-PSS 2048 | `PS256` | RSA 2048 key | ~300 bytes | Acceptable, larger tokens |
| RSA-PSS 4096 | `PS512` | RSA 4096 key | ~500 bytes | Large tokens, slow signing |
| HMAC-SHA256 | `HS256` | >= 256-bit secret | ~86 bytes | Symmetric only, key distribution problem |
| `none` | `none` | None | Any | NEVER USE — algorithm confusion attack |

## Never Use
- DSA (deprecated by FIPS 186-4)
- RSA PKCS#1 v1.5 signatures
- ECDSA without deterministic nonces (RFC 6979)
- secp256k1 for TLS or JWT (Bitcoin curve, not standardized for non-blockchain use)
