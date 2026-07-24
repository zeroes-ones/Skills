# Threshold Signature Patterns — FROST, BLS, GG20

## FROST (RFC 9591 — IETF CFRG)

Flexible Round-Optimized Schnorr Threshold Signatures.

### Protocol Flow
1. **Key Generation:** Distributed Key Generation (DKG) or trusted dealer
   - Each signer `i` holds secret share `s_i`
   - Group public key: `PK = g^s` (standard Schnorr, indistinguishable from single-key)

2. **Round 1 (Preprocessing):** Each signer generates nonce pair
   - `(d_i, e_i)` = random scalars (hiding + binding nonces)
   - `(D_i, E_i)` = `(g^d_i, g^e_i)` commitments broadcast

3. **Round 2 (Signing):** Each signer produces share
   - Aggregate commitment: `R = prod(D_i) * prod(E_i)^rho_i`
   - Challenge: `c = H(R, PK, msg)`
   - Signature share: `z_i = d_i + e_i*rho_i + lambda_i * s_i * c`
   
4. **Aggregation:** `z = sum(z_i)`, signature = `(R, z)` — standard Schnorr

### Security Properties
- Identifiable aborts: if signer `i` misbehaves, aggregator identifies `i`
- Unforgeable: `t` of `n` signers required (threshold security)
- Compatible: output is standard Schnorr, verifiable by any Schnorr verifier

## BLS Threshold (Non-Interactive)

Boneh-Lynn-Shacham: pairings enable non-interactive threshold aggregation.

### Properties
- **Non-interactive:** Each signer produces share independently
- **Aggregation:** `O(n)` to aggregate, result is a single BLS signature (96 bytes)
- **Verification:** Pairing check `e(g, sig) = e(PK, H(msg))`
- **No signer coordination required** — ideal for async/offline signers

### Trade-offs
- Requires pairing-friendly curve (BLS12-381, BN254)
- Pairing verification is 10-100x slower than elliptic curve ops
- No identifiable abort (can't tell which signer failed)
- DKG required for key generation

## GG20/CGGMP (Threshold ECDSA)

Multi-party ECDSA for Bitcoin/Ethereum compatibility.

### Protocol Complexity
- **GG20:** 5-7 rounds, Paillier homomorphic encryption, ZK range proofs
- **CGGMP:** 4-6 rounds (optimized), replaces Paillier with OT-based multiplication
- **Key refresh:** Supports proactive refresh without changing public key

### When to Use
- Blockchain custody requiring ECDSA signatures (secp256k1)
- When Schnorr (FROST) or BLS upgrade path is not available
- Multi-chain support requiring legacy ECDSA

## Key Resharing (Proactive Security)

Committee rotation without key regeneration using Herzberg scheme:
1. Old committee: each holder creates `t_new`-of-`n_new` sub-shares of their share
2. New committee: each member sums weighted sub-shares from `t_old` old holders
3. Result: same group secret, new committee — no new key ceremony
