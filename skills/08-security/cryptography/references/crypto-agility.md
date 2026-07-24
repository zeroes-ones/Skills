# Crypto Agility Reference

## What Is Crypto Agility?

Crypto agility is the ability to replace cryptographic algorithms, key sizes, and protocols without rewriting the system, redeploying all clients, or requiring a flag-day migration. It is the architectural property that allows a system to survive an algorithmic break.

## Core Design Patterns

### 1. Algorithm Identifier in Every Artifact

Every encrypted, signed, or hashed artifact MUST include:
- **Protocol version** (1 byte): enables backward-compatible upgrades
- **Algorithm identifier** (1-2 bytes): maps to a registry of supported algorithms
- **Key ID / version** (variable): identifies which key was used

```
Encrypted Blob Format:
[version: 1 byte] [algo_id: 2 bytes] [key_id: 4 bytes] [nonce: 12 bytes] [ciphertext: variable] [auth_tag: 16 bytes]
```

### 2. Multi-Algorithm Support

During transitions, support BOTH old and new algorithms simultaneously:
- **Accept**: decrypt/verify with either old or new algorithm
- **Issue**: encrypt/sign with new algorithm only
- **Phase**: after migration window, reject old algorithm

### 3. Key Rotation Without Downtime

- Keys identified by version, not position
- New keys added alongside old keys
- Old keys retired after rotation window (data still decryptable)
- Rotation events: scheduled (calendar), emergency (compromise), version (new algorithm)

### 4. Negotiation Protocols

For interactive protocols (TLS, SSH, WireGuard):
- Advertise supported algorithms in preference order
- Agree on strongest mutually-supported algorithm
- Fail securely if no overlap (no downgrade to weak)

## Migration Framework

### Phase 1: Dual-Write (Old + New)
- Encrypt/sign with BOTH old and new algorithms
- Store both ciphertexts/signatures in artifact
- Verifiers accept either

### Phase 2: Preferred-New
- Encrypt/sign with new algorithm only
- Verifiers accept either (for backward compatibility)
- Monitor: alert on old-algorithm usage

### Phase 3: New-Only
- Encrypt/sign with new algorithm only
- Verifiers reject old algorithm
- Remove old algorithm from codebase

## Real-World Examples

### SHA-1 Deprecation (2005-2017)
- 2005: First theoretical collision (Wang, 2^69)
- 2012: NIST disallows SHA-1 for digital signatures
- 2014: Chrome shows warning for SHA-1 certificates
- 2017: SHAttered — practical collision (2^63.1, ~$110K compute)
- 2017: Major browsers block SHA-1 certificates
- Lesson: 12-year migration from deprecation to removal

### TLS 1.0 → 1.3 Migration (2006-2021)
- TLS 1.0/1.1 deprecated by IETF RFC 8996 in March 2021
- Many systems still not migrated by 2025
- Lesson: Protocol version negotiation is essential; flag-day impossible at Internet scale

## Crypto Inventory Template

For each cryptographic operation, document:
1. What: algorithm, mode, key size, parameters
2. Where: service, library, configuration file
3. Why: compliance requirement? performance? legacy interop?
4. Data sensitivity: how long must data remain confidential?
5. Migration plan: target algorithm, timeline, blocking dependencies
