## 16. Gotchas & Pitfalls

### Critical Failures by Domain

| # | Domain | Pitfall | Impact | Mitigation |
|---|--------|---------|--------|------------|
| 1 | FHE | CKKS used for exact equality checks — comparison always fails due to approximation noise | $500K+ financial calculation error, incorrect access control decisions | Use BGV/BFV for equality; CKKS only for approximate statistics/ML |
| 2 | MPC | Garbled circuit evaluation timing leaks circuit depth — attacker correlates wall-clock time with computation structure | Partial key leakage, circuit structure recovery | Uniform circuit padding, random gate scheduling, fixed-time evaluation |
| 3 | TEE | SGX LVI/Plundervolt speculative execution bypass reads enclave memory through voltage fault injection | $1M+ key material exfiltration from production enclaves | Apply LVI/MMIO mitigations, update microcode, monitor TCB recovery |
| 4 | Threshold | Signature share reuse across committee rotations — adversary who compromises t parties across epochs reconstructs key | Full key compromise, irreversible in most custody systems | Proactive resharing with fresh randomness each epoch, verify share freshness |
| 5 | PQC | Hybrid implementation silently falls back to classical-only on PQC negotiation failure | Classical-only security despite claiming quantum resistance | Fail closed: reject connection if either KEM fails, log both results |
| 6 | TEE | Attestation verification omits certificate chain validation — accepts revoked TCB signatures | Attacker signs arbitrary quotes with compromised but unexpired PCK | Full chain: quote -> PCK -> processor CA -> root, check CRL freshness |
| 7 | FHE | Bootstrapping budget exhausted mid-computation — ciphertext decrypts to random noise with no error signal | $200K+ encrypted data corruption, irreversible data loss | Static budget analysis + runtime level tracking, conservative margin (2+ levels) |
| 8 | Entropy | /dev/urandom on freshly-booted VM/container returns deterministic output before entropy pool initialized | Predictable keys generated in early boot sequence | Block boot until entropy pool seeded (getrandom with GRND_RANDOM), mix hardware RNG |
| 9 | MPC | OT extension correlation reuse across sessions — attacker correlates transcripts to break OT security | Loss of OT security = loss of MPC security for all GMW/Yao protocols | Fresh base OTs per session, use OT extension with random oracle model proofs |
| 10 | PQC | X.509 hybrid certificate with single signature — verifier accepts classical-only path | Downgrade to classical-only certificate validation | Dual signature verification required, reject certs with only one valid signature |

### Code-Level Gotchas

```python
# GOTCHA 1: Non-constant-time comparison in MPC
# WRONG — leaks secret through branch timing
if secret_value == 0:
    result = compute_path_a()
else:
    result = compute_path_b()

# CORRECT — both paths computed, selection via arithmetic
path_a = compute_path_a()
path_b = compute_path_b()
result = path_a + (secret_value != 0) * (path_b - path_a)

# GOTCHA 2: CKKS equality check
# WRONG — CKKS is approximate, equality is meaningless
if enc_a == enc_b:  # NEVER true, even for semantically equal values
    execute_high_value_action()

# CORRECT — Use BFV/BGV for equality-dependent logic
# Or compute: |a-b| < epsilon (approximate comparison)
diff = enc_a - enc_b
threshold_test = (diff * diff).decrypt() < epsilon**2

# GOTCHA 3: Unvalidated attestation nonce
# WRONG — No nonce binding, attacker replays old attestation
quote = generate_quote(enclave_pk, b"")

# CORRECT — Bind to fresh challenge
nonce = os.urandom(32)
quote = generate_quote(enclave_pk, nonce)
assert verify_quote(quote, nonce)  # Nonce prevents replay
```

---
