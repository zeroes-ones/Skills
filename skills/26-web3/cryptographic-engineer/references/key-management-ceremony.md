# Key Management Ceremony — HSM, Shamir, Entropy

## Ceremony Types

### Type A: HSM-Based (Enterprise PKI)
- Hardware: FIPS 140-2 Level 3 HSM (Thales Luna, Gemalto, Utimaco)
- Activation: M-of-N smart cards (split-knowledge)
- Procedure:
  1. Security officers present smart cards (physical presence)
  2. PIN entry for each card (secret, different per officer)
  3. HSM activated → key generation inside secure boundary
  4. Private key NEVER exported (CKA_SENSITIVE=true, CKA_EXTRACTABLE=false)
  5. Public key exported for certificate issuance

### Type B: MPC-Based (Decentralized)
- No single point of key compromise
- Protocol: GG20 DKG (Distributed Key Generation) or FROST DKG
- Each party generates share independently
- Group public key computed via polynomial commitment
- No trusted dealer required

### Type C: Air-Gapped Cold Storage (Treasury)
- Physically isolated machine (no network connectivity)
- Entropy: dice rolls (min 100 rolls) + hardware RNG + timing jitter
- Key derivation: BIP-39 mnemonic (24 words, 256-bit entropy)
- Shamir backup: 3-of-5 shares on metal plates stored in safe deposit boxes
- Ceremony: video recorded, witnessed, tamper-evident seals

## Shamir Secret Sharing with Verification

### Standard Shamir (1979)
```
Split: f(x) = s + a1*x + a2*x^2 + ... + a_{t-1}*x^{t-1} mod p
Share i: (i, f(i)) for i in [1, n]
Reconstruct: Lagrange interpolation at x=0
```

### Feldman VSS (Verifiable)
```
Split: Same polynomial
Commitments: A_j = g^{a_j} mod p  (published)
Verification: g^{f(i)} == prod_{j=0}^{t-1} A_j^{i^j} mod p
```
Allows each shareholder to verify their share against public commitments without reconstructing the secret. Enables detection of dealer misbehavior.

## Entropy Health Monitoring (NIST SP 800-90B)

### Multi-Source Architecture
1. **Primary:** Hardware RNG (Intel RDRAND, AMD RDRAND, ARM TRNG)
2. **Secondary:** OS CSPRNG (getrandom syscall, ChaCha20-based)
3. **Tertiary:** Timing jitter (CPU cycle jitter, scheduler noise)

### Health Tests
- **Repetition Count Test:** Alarm if same value repeats > threshold
- **Adaptive Proportion Test:** Alarm if value frequency exceeds expected
- **Continuous:** Monitor min-entropy estimate per source
- **Fail closed:** Reject key generation if any source fails

### /dev/urandom Bootstrap Problem
On VMs and containers, `/dev/urandom` may return deterministic output before the entropy pool is seeded. Mitigation:
- Use `getrandom(GRND_RANDOM)` which blocks until pool seeded
- Seed from host hypervisor via virtio-rng
- Cross-boot entropy persistence (seed file)
