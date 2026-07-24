# Hashing & Password Storage Reference

## Algorithm Selection

| Algorithm | Type | Recommended Parameters | Use Case |
|-----------|------|----------------------|----------|
| Argon2id | Memory-hard KDF | m=46MB, t=1, p=1 (OWASP minimum) | Password hashing (best choice) |
| bcrypt | Blowfish-based KDF | cost >= 12 | Password hashing (legacy, proven) |
| scrypt | Memory-hard KDF | N=2^17, r=8, p=1 | Password hashing (where bcrypt unavailable) |
| PBKDF2-SHA256 | Iteration-based KDF | 600,000+ iterations (OWASP 2023) | Legacy compatibility, FIPS compliance |

## Argon2id Parameter Tuning

### OWASP Minimum (2023)
- m = 46 MiB memory
- t = 1 iteration
- p = 1 degree of parallelism

### Tuning Process
1. Start with OWASP minimum parameters
2. Measure hash time on production hardware
3. Increase m (memory) until hash takes ~500ms
4. If m is constrained, increase t (iterations) instead
5. Never exceed 1 second total hash time (login UX degrades)

### Parameter Selection by Hardware Tier

| Hardware | m (MiB) | t | p | Approx. Time |
|----------|---------|---|---|--------------|
| Raspberry Pi 4 | 16 | 3 | 1 | ~500ms |
| AWS t3.medium | 64 | 3 | 1 | ~500ms |
| AWS c5.xlarge | 128 | 4 | 2 | ~500ms |
| Dedicated server | 256 | 4 | 4 | ~500ms |

## bcrypt Details

- Maximum input: 72 bytes (silently truncated)
- Salt: 128 bits (16 bytes), automatically generated
- Output format: `$2a$<cost>$<22-char-salt><31-char-hash>`
- Cost vs. time (AWS t3.medium):
  - cost=10: ~80ms
  - cost=12: ~320ms
  - cost=14: ~1.3s

## Migration Strategy: SHA-256 → Argon2id

1. Add `algorithm` field to password storage: `{algo: "argon2id", params: {...}, salt, hash}`
2. On user login: verify using old SHA-256 hash
3. If valid, re-hash with Argon2id and store new hash
4. Mark old SHA-256 entries for migration
5. After migration window, force password reset for unmigrated accounts
6. Delete all SHA-256 hashes after migration complete

## Pepper Strategy (Defense in Depth)

- 128-bit random pepper, stored in HSM/KMS (NOT in database)
- `intermediate = HMAC-SHA256(password, pepper)`
- `final_hash = Argon2id(intermediate, salt, params)`
- If pepper compromised: all passwords must be rehashed
- If database leaked without pepper: attacker cannot crack any passwords
