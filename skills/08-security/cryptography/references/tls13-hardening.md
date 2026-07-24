# TLS 1.3 Hardening Reference

## Cipher Suite Preference Order

| Priority | Cipher Suite | Use Case | Hardware Acceleration |
|----------|-------------|----------|----------------------|
| 1 | TLS_AES_128_GCM_SHA256 | General purpose, best performance | AES-NI (x86), ARMv8 CE |
| 2 | TLS_AES_256_GCM_SHA384 | FedRAMP High, CNSA 2.0, BSI compliance | AES-NI (x86) |
| 3 | TLS_CHACHA20_POLY1305_SHA256 | Mobile, embedded, no AES-NI | Constant-time software |

## Key Exchange Group Priority

1. X25519 (RFC 7748) — 128-bit security, fastest ECDH, constant-time
2. secp256r1 (NIST P-256) — required for FIPS 140-2 compliance
3. secp384r1 — 192-bit security, CNSA 2.0 compliant
4. X448 — 224-bit security, post-quantum safety margin

## Certificate Verification Requirements

- OCSP Stapling (RFC 6961): server provides time-stamped OCSP response in TLS handshake
- OCSP Must-Staple: X.509 extension id-pkix-ocsp-muststaple (1.3.6.1.5.5.7.1.24)
- Certificate Transparency: minimum 2 SCTs from independent log operators
- SCT delivery: embedded in certificate (preferred), TLS extension, or OCSP stapling

## HSTS Configuration

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- Submit domain to https://hstspreload.org for browser preload list inclusion
- Preload ensures first-visit HTTPS enforcement (no TOFU vulnerability)

## JA3/JA4 Fingerprinting Awareness

- JA3: MD5 hash of TLS ClientHello fields (SSLVersion, Ciphers, Extensions, EllipticCurves, EllipticCurvePointFormats)
- JA4: improved hash incorporating SNI, ALPN, and QUIC support
- Mitigation: randomize cipher ordering within security constraints
- Full fingerprint elimination is impossible without breaking compatibility

## Prohibited Configurations

- SSLv3, TLS 1.0, TLS 1.1 (deprecated by IETF RFC 8996, March 2021)
- Static RSA key exchange (no forward secrecy)
- CBC-mode ciphers (padding oracle vulnerable)
- RC4, 3DES, EXPORT ciphers
- Compression (CRIME attack)
- TLS 1.2 renegotiation (if not strictly required)
