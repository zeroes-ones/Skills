## Core Workflow

### Phase 1: Cryptographic Inventory & Threat Model

Execute in order. Do not skip steps.

```
1. INVENTORY EVERY CRYPTOGRAPHIC OPERATION
   |-- Enumerate all places cryptography is used: TLS termination, data-at-rest encryption,
   |   password storage, token signing (JWT/SAML), message authentication, digital signatures,
   |   key exchange, random number generation, certificate validation, XML encryption
   |-- For each operation, document: algorithm, key size, key source, key lifecycle,
   |   protocol version, library/framework, configuration parameters
   |-- Flag unknowns: any operation where the algorithm or parameters are not explicitly configured

2. DEFINE THREAT MODEL
   |-- What are you protecting? (data at rest, data in transit, authentication, integrity)
   |-- From whom? (network adversary, cloud provider insider, malicious tenant, nation-state)
   |-- For how long? (1 year, 10 years, 50 years — determines key sizes and PQC urgency)
   |-- What are the consequences of failure? (financial loss, regulatory penalty, loss of life)
   |-- Harvest-now-decrypt-later assessment: does the data have long-term sensitivity?

3. ASSESS CURRENT STATE AGAINST STANDARDS
   |-- Map each operation to: NIST SP 800-57 (key management), NIST SP 800-52 (TLS),
   |   FIPS 140-2/3, PCI DSS 4.0, OWASP ASVS, BSI TR-02102-1, ANSSI RGS
   |-- Flag gaps: prohibited algorithms, insufficient key sizes, missing controls

4. PRIORITIZE REMEDIATION
   |-- CRITICAL: Broken/deprecated primitives (SHA-1, MD5, RC4, 3DES, RSA PKCS#1 v1.5, CBC without HMAC)
   |-- HIGH: Insufficient key sizes (RSA < 2048, ECC < 256), missing authenticated encryption,
   |   nonce-reuse-prone AES-GCM, TLS < 1.2, passwords with fast hashes
   |-- MEDIUM: Missing crypto agility, suboptimal algorithm selection (RSA over Ed25519),
   |   no certificate automation, wildcard cert overuse
   |-- LOW: Performance tuning (AES-NI not utilized, suboptimal cipher ordering)
```

### Phase 2: TLS 1.3 Configuration

```
1. MINIMUM PROTOCOL VERSION
   |-- TLS 1.3 ONLY for new deployments (RFC 8446)
   |-- TLS 1.2 minimum for backward compatibility — but NO TLS 1.0/1.1 (deprecated by IETF RFC 8996)
   |-- Disable SSLv3 and below unconditionally

2. CIPHER SUITE SELECTION (TLS 1.3 — only 5 AEAD ciphers defined)
   |-- PREFERRED (order matters — first is negotiated):
   |   |-- TLS_AES_128_GCM_SHA256 (hardware-accelerated on x86/ARM, safest choice)
   |   |-- TLS_AES_256_GCM_SHA384 (compliance: CNSA 2.0, FedRAMP High, BSI)
   |   |-- TLS_CHACHA20_POLY1305_SHA256 (mobile/embedded without AES-NI, constant-time software)
   |-- The remaining two (TLS_AES_128_CCM_SHA256, TLS_AES_128_CCM_8_SHA256) are for constrained IoT only

3. KEY EXCHANGE GROUPS
   |-- X25519 (RFC 7748): fastest, safest, 128-bit security, constant-time implementations
   |-- X448: 224-bit security, post-quantum margin, slower
   |-- secp256r1 (NIST P-256): required for FIPS compliance, widely supported
   |-- secp384r1: 192-bit security, CNSA 2.0 compliance
   |-- NEVER: secp256k1 (Bitcoin curve, not TLS-standard), static RSA, FFDHE < 2048-bit

4. CERTIFICATE VERIFICATION
   |-- OCSP Stapling (RFC 6961): server includes time-stamped OCSP response in handshake,
   |   eliminating client OCSP lookup (privacy + latency win)
   |-- OCSP Must-Staple (id-pkix-ocsp-muststaple extension): cert will be rejected if not stapled
   |-- Certificate Transparency: require at least 2 SCTs (Signed Certificate Timestamps)
   |   from different CT log operators. Chrome requires CT for all publicly-trusted certs.

5. HSTS & ADDITIONAL HARDENING
   |-- Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   |-- Submit to HSTS preload list (hstspreload.org) for browser-enforced HTTPS
   |-- TLS fingerprinting defense: be aware of JA3/JA4 — your cipher ordering creates a fingerprint.
   |   Randomize cipher order within security constraints to avoid trivially identifying your stack.
```

### Phase 3: Incident Response — Cryptographic Compromise

```
1. TRIAGE — Determine Compromise Scope (first 30 minutes)
   |-- WHICH KEYS? Private key on disk? In memory? In transit? HSM boundary breached?
   |-- WHAT DATA? All data encrypted with compromised key. All sessions using compromised cert.
   |   All authentications verified with compromised signing key.
   |-- WHEN? Key creation date → compromise detection date = exposure window.
   |-- HOW? Exfiltration, insider, side-channel, implementation bug, weak RNG, supply chain.

2. CONTAIN — Stop the Bleeding (hours 1-4)
   |-- Revoke affected certificates (CRL + OCSP with immediate nextUpdate)
   |-- Rotate compromised keys: generate new keys on clean system (NOT the potentially compromised one)
   |-- Re-encrypt data-at-rest: if DEK compromised via KEK compromise, rotate KEK and rewrap all DEKs
   |-- Invalidate sessions: force re-authentication, rotate session signing keys
   |-- Block compromised key IDs at API gateway / auth service

3. ERADICATE — Fix Root Cause (days 1-7)
   |-- Determine how key was exposed: audit logs, access patterns, deployment artifacts
   |-- Fix the vulnerability: move keys to HSM/TPM, implement key access controls,
   |   harden RNG seeding, fix side-channel, patch library
   |-- Regenerate entire key hierarchy if root or intermediate compromised

4. RECOVER — Restore Cryptographic Integrity (days 3-14)
   |-- Issue new certificates with new keys, new serial numbers, new CT SCTs
   |-- Distribute new public keys/trust anchors to all relying parties
   |-- Verify all cryptographic operations now use new (uncompromised) keys
   |-- Post-incident review: update threat model, improve key ceremony procedures,
   |   enhance monitoring (key usage alerts, anomalous certificate issuance detection)
```
