# Symmetric Encryption Reference

## Algorithm Selection Matrix

| Algorithm | Mode | Key Size | Nonce/IV Size | Auth Tag | Best For |
|-----------|------|----------|---------------|----------|----------|
| AES-256-GCM | AEAD | 256 bits | 96 bits (must not repeat) | 128 bits | Hardware-accelerated, high throughput |
| ChaCha20-Poly1305 | AEAD | 256 bits | 96 bits (counter) | 128 bits | Software-only, constant-time |
| XChaCha20-Poly1305 | AEAD | 256 bits | 192 bits (random safe) | 128 bits | Random nonce safety, simpler API |

## AES-GCM Nonce Management (CRITICAL)

### The Rule
AES-GCM nonce (96-bit IV) **MUST NEVER** repeat with the same key. A single nonce reuse reveals the GHASH authentication subkey H, enabling:
- Universal forgery of arbitrary ciphertexts
- Decryption of all past and future ciphertexts under that key

### Safe Strategies

1. **Deterministic Counter** (preferred for most applications)
   - 96-bit strictly monotonic counter
   - Persisted atomically with ciphertext storage
   - Reset only on key rotation
   - Safe up to 2^64 encryptions per key

2. **Deterministic Derivation** (for encrypting many independent items)
   - `nonce = HKDF-SHA256(DEK, item_id || version)[0:12]`
   - Requires unique item_id for each encryption

3. **Random Nonce** — DO NOT USE with standard AES-GCM
   - Birthday bound collision at ~2^48 encryptions
   - Approximately 1% collision probability after 2^40 encryptions

## XChaCha20-Poly1305

- 192-bit random nonce: collision probability negligible (2^-96)
- 256-bit key
- Designed by Daniel J. Bernstein
- Implementations: libsodium `crypto_aead_xchacha20poly1305_ietf_*`
- Best choice when random nonces are required

## AES-CBC Legacy Support

### Requirements (if unavoidable)
- **Encrypt-then-MAC**: encrypt first, then HMAC-SHA256(ciphertext || IV)
- **Random IV**: CBC IV must be unpredictable (not just unique, unlike GCM nonce)
- **Constant-time comparison**: of MAC tags to prevent timing oracle
- **No padding oracle**: handle decryption and MAC verification atomically

### Migration Path
- Replace with AES-GCM or XChaCha20-Poly1305
- TLS: upgrade to TLS 1.3 (eliminates CBC entirely)
