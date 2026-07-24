# OWASP Top 10 — A02:2021 Cryptographic Failures

## Overview
Previously "Sensitive Data Exposure," Cryptographic Failures covers failures in cryptography that lead to exposure of sensitive data.

## Common Failure Patterns
1. **Hardcoded keys**: Encryption keys in source code, config files, env vars
2. **Weak algorithms**: MD5, SHA-1, RC4, DES, 3DES for security-sensitive operations
3. **Missing encryption**: Storing sensitive data in plaintext (passwords, PII, PCI, PHI)
4. **Weak key generation**: Predictable seeds, insufficient entropy
5. **Missing TLS**: HTTP instead of HTTPS for sensitive data transmission
6. **Weak TLS config**: TLS 1.0/1.1, weak ciphers, no HSTS
7. **No key rotation**: Same encryption key for years, no version tracking
8. **Improper certificate validation**: Accepting self-signed, expired, or wrong-host certificates

## Prevention
- Classify data before storing (don't encrypt what you don't need)
- Use authenticated encryption: AES-256-GCM, ChaCha20-Poly1305
- Never implement custom cryptography
- Store keys in KMS, never in code
- TLS 1.3 with strong ciphers, HSTS preload
- Key rotation at least every 90-365 days

## References
- OWASP A02:2021: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
