# How Databases Store Passwords Securely — Hashing, Not Encryption

> Original explainer for interview prep and learning. [research-source: title-only]
> Deep algorithm tables live in `cryptography/references/hashing-and-passwords.md` — this doc is the concept/interview layer.

## The core principle

**Never store passwords — store verifiers.** A password must be turned into something that (a) cannot be reversed to recover the password and (b) lets you confirm a login attempt. That means **hashing with a slow, salted, memory-hard KDF** — never reversible encryption, never plaintext, never a fast general-purpose hash like SHA-256/MD5 alone.

## Why hashing and not encryption?

- **Encryption is reversible** — whoever holds the key can decrypt every password. Breaches don't just leak the DB; they leak the key too (same box, same attacker).
- **Hashing is one-way** — even with the full DB dump, an attacker must *guess* passwords and check. The job of password storage is to make that guessing as slow and expensive as possible.

## The three requirements (know each)

1. **Salt (unique per user)** — a random value per password, stored alongside. Kills **rainbow tables** (precomputed hash dictionaries) and makes identical passwords hash differently.
2. **Slow KDF** — deliberately expensive so brute force is slow. The accepted family:
   - **Argon2id** — memory-hard, the current OWASP-recommended choice.
   - **scrypt** — memory-hard, battle-tested.
   - **bcrypt** — CPU-cost parameter (cost ≥ 12 today), widely deployed.
   - **PBKDF2** — iteration-based (600K+ iterations); FIPS-friendly but not memory-hard (ASIC-cheap).
   See the deep reference for exact parameters — parameters must be tuned to your hardware and reviewed over time.
3. **Pepper (optional, defense in depth)** — a server-side secret mixed into the hash. If only the DB leaks (not the app server), peppers block offline cracking. Trade-off: you now manage another secret.

## The login flow (correct shape)

1. On signup: generate salt → `hash = KDF(password, salt)` → store `salt` + `hash`.
2. On login: look up user → recompute `KDF(attempt, stored_salt)` → **constant-time compare** with stored hash.
3. On success: issue session/token (see jwt-tokens.md); consider rate limiting and breach-password checks.
4. **Never log the password, never email it back, never store it anywhere else.**

## Why fast hashes are forbidden

SHA-256 does ~billions of guesses/sec on GPUs — a leaked SHA-256("password") list falls in minutes. A memory-hard KDF like Argon2id is tuned so each guess costs ~0.1–1s of work, turning a $10 GPU rig into a years-long effort for the same list. That single property (guess cost) is the entire game.

## Breach response framing (interviews love this)

If the DB leaks: with salted slow KDFs, the *hashes* leak but passwords remain expensive to recover — you still force resets for all users (as defense), but the damage is bounded. With plaintext/reversible storage, the leak is total and immediate. That contrast is why "how do you store passwords?" is a security-interview staple.

## Interview answer skeleton

"Passwords are stored as salted, slow KDF hashes — Argon2id (or scrypt/bcrypt with sane parameters) — never encrypted and never with a fast hash. Each user gets a unique salt so rainbow tables fail, the KDF is memory-hard so brute force is expensive, and I compare in constant time. Optional pepper adds defense in depth if only the DB leaks. On a breach the hashes leak but the passwords stay expensive to crack."

## Anti-patterns

- ❌ Storing plaintext or reversible-encrypted passwords.
- ❌ Unsalted hashes, or fast hashes (MD5/SHA-1/SHA-256) for passwords.
- ❌ Reusing one global salt.
- ❌ Non-constant-time comparison (`==` on hashes can leak timing).
- ❌ Logging passwords or sending them back in emails.

## Deliberate-practice drills

1. **Compare drill:** hash "password" with SHA-256 vs bcrypt/Argon2id and measure the time difference — explain the security meaning.
2. **Flow drill:** write the correct signup/login pseudocode including salt, KDF, constant-time compare.
3. **Threat drill:** DB dumps leak — walk what an attacker can do with salted-Argon2 hashes vs unsalted-SHA1 vs plaintext.
4. **Parameter drill:** justify Argon2id parameters for your server (memory, time, parallelism) and a rotation policy.
5. **Interview drill:** "why not just encrypt passwords?" — answer with reversibility + key-on-same-box and pivot to salted memory-hard KDFs.

## References
- **Deep algorithm tables & parameters:** `cryptography/references/hashing-and-passwords.md`
- See also: jwt-tokens.md (this repo)
- `cryptography` SKILL.md — KDF selection, key management
- `secure-api-design` SKILL.md — auth flows, OWASP guidance
