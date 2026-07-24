# Post-Quantum Cryptography Readiness Reference

## The Harvest-Now-Decrypt-Later Threat

Adversaries are collecting encrypted traffic today, storing it, and will decrypt it when a cryptographically relevant quantum computer (CRQC) becomes available. Any data with >10-year confidentiality requirements is already at risk.

### Timeline Estimates
- NIST: "CRQC could break RSA-2048 within 15-20 years"
- NSA (CNSA 2.0): mandated PQC migration starting 2025, complete by 2033
- BSI (Germany): recommends hybrid schemes for all new deployments
- ANSSI (France): PQC-only for long-term secrets by 2030

## NIST PQC Standards (August 2024)

### ML-KEM (FIPS 203, CRYSTALS-Kyber) — Key Encapsulation

| Parameter Set | NIST Level | Classical Security | PQ Security | Public Key | Ciphertext | Shared Secret |
|--------------|------------|-------------------|-------------|------------|------------|---------------|
| Kyber-512 | 1 | ~AES-128 | ~AES-128 | 800 bytes | 768 bytes | 32 bytes |
| Kyber-768 | 3 | ~AES-192 | ~AES-192 | 1184 bytes | 1088 bytes | 32 bytes |
| Kyber-1024 | 5 | ~AES-256 | ~AES-256 | 1568 bytes | 1568 bytes | 32 bytes |

### ML-DSA (FIPS 204, CRYSTALS-Dilithium) — Signatures

| Parameter Set | NIST Level | Public Key | Signature | Security |
|--------------|------------|------------|-----------|----------|
| Dilithium2 | 2 | 1312 bytes | 2420 bytes | ~AES-128 |
| Dilithium3 | 3 | 1952 bytes | 3293 bytes | ~AES-192 |
| Dilithium5 | 5 | 2592 bytes | 4595 bytes | ~AES-256 |

### SLH-DSA (FIPS 205, SPHINCS+) — Hash-Based Signatures

| Variant | Public Key | Signature | Speed | Use Case |
|---------|------------|-----------|-------|----------|
| SPHINCS+-128s | 32 bytes | 7856 bytes | Very slow | Conservative, stateless |
| SPHINCS+-128f | 32 bytes | 17088 bytes | Slow | Conservative, stateless |
| SPHINCS+-192s | 48 bytes | 16224 bytes | Very slow | Higher security |
| SPHINCS+-256s | 64 bytes | 29792 bytes | Very slow | Maximum security |

## Hybrid Scheme Design

### Key Exchange: X25519 + Kyber-1024

```
X25519:   client_eph_sk → client_eph_pk
Kyber:    (kyber_sk, kyber_pk) = Kyber.KeyGen()

Client → Server: client_eph_pk, kyber_pk
Server:  ss_x25519 = X25519(server_sk, client_eph_pk)
         (ss_kyber, kyber_ct) = Kyber.Encaps(kyber_pk)
         combined = HKDF-Extract(ss_x25519 || ss_kyber, salt="")

Server → Client: server_eph_pk, kyber_ct
Client:  ss_x25519 = X25519(client_eph_sk, server_eph_pk)
         ss_kyber = Kyber.Decaps(kyber_sk, kyber_ct)
         combined = HKDF-Extract(ss_x25519 || ss_kyber, salt="")
```

### Migration Strategy

| Phase | Timeline | Action |
|-------|----------|--------|
| Inventory | Now | Catalog all crypto usage, identify long-lived data |
| Experiment | 2025-2026 | Test hybrid schemes in non-critical paths |
| Deploy | 2027-2028 | Hybrid everywhere with >5yr sensitivity |
| Sunset | 2029+ | PQC-only for new deployments, phase out RSA/ECDH |
| Verify | Ongoing | Monitor cryptanalysis of PQC algorithms, be ready to switch |
