# Post-Quantum Cryptography Migration Guide

## NIST Standardized Algorithms

| Algorithm | FIPS | Type | Security Level | Public Key | Ciphertext/Signature |
|-----------|------|------|---------------|------------|---------------------|
| ML-KEM-512 | 203 | KEM | 1 (AES-128) | 800 B | 768 B |
| ML-KEM-768 | 203 | KEM | 3 (AES-192) | 1184 B | 1088 B |
| ML-KEM-1024 | 203 | KEM | 5 (AES-256) | 1568 B | 1568 B |
| ML-DSA-44 | 204 | Signature | 2 | 1312 B | 2420 B |
| ML-DSA-65 | 204 | Signature | 3 | 1952 B | 3309 B |
| ML-DSA-87 | 204 | Signature | 5 | 2592 B | 4627 B |
| SLH-DSA-128s | 205 | Signature | 1 | 32 B | 7856 B |
| SLH-DSA-128f | 205 | Signature | 1 | 32 B | 17088 B |
| SLH-DSA-256s | 205 | Signature | 5 | 64 B | 29792 B |

## Migration Phases

### Phase 1: Inventory & Assessment (0-6 months)
- Scan all TLS endpoints: cipher suite enumeration
- Map key exchange: RSA-2048, ECDH-P256, X25519 locations
- Assess harvest-now-decrypt-later (HNDL) risk:
  - Long-lived secrets (>10yr): full PQC mandatory
  - Short-lived secrets (<1yr): hybrid acceptable temporarily
- Classify systems by criticality and migration complexity

### Phase 2: Hybrid Deployment (6-18 months)
- Deploy TLS 1.3 hybrid key exchange: X25519 + ML-KEM-768
- Issue hybrid X.509 certificates: ECDSA + ML-DSA-44 dual signatures
- Key material: `KDF(ecdh_shared_secret || mlkem_shared_secret)`
- **Critical:** Both KEMs MUST succeed, or connection fails

### Phase 3: PQC-Only (18-36 months)
- Migrate internal services to PQC-only
- External endpoints: PQC-first with classical backup
- Deprecation timeline: announce classical deprecation dates

### Phase 4: Classical Removal (36-60 months)
- Remove RSA/ECDH from all endpoints
- Retain classical verification for legacy system support
- Full PQC ecosystem: certificates, code signing, document signing

## Hybrid Certificate Structure (X.509)

```
TBSCertificate:
  subjectPublicKeyInfo: ML-KEM-768 public key (or classical key)
  extensions:
    - altSignatureAlgorithm: id-ML-DSA-44 (2.16.840.1.101.3.4.3.17)
    - altSignatureValue: ML-DSA-44 signature over TBSCertificate

signatureAlgorithm: ecdsa-with-SHA256
signatureValue: ECDSA signature over TBSCertificate
```

## TLS 1.3 Hybrid Ciphersuites

IETF draft-ietf-tls-hybrid-design:
- `TLS_AES_256_GCM_SHA384` with X25519MLKEM768 hybrid key exchange
- Key share extension carries both X25519 + ML-KEM public keys
- Server selects hybrid or rejects (no fallback to classical-only)
