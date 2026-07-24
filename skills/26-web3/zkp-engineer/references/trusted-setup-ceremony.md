# Trusted Setup Ceremony

## Overview

Groth16 requires a two-phase trusted setup ceremony. Phase 1 (Powers of Tau) is universal and reusable. Phase 2 is circuit-specific.

## Powers of Tau (Phase 1)

### Existing Ceremonies

| Ceremony | Curve | Size | Participants | Status |
|----------|-------|------|-------------|--------|
| Perpetual Powers of Tau | BN254 | 2^28 | 88+ | Complete |
| Hermez Powers of Tau | BN254 | 2^21 | 200+ | Complete |
| Filecoin Powers of Tau | BLS12-381 | 2^27 | 50+ | Complete |
| Zcash Sapling | BLS12-381 | 2^21 | 87 | Complete |
| Aztec Ignition | BN254 | 2^19 | 176 | Complete |

### Downloading Phase 1 Artifacts

```bash
# BN254 (most common for Ethereum)
# Supports up to 2^28 constraints
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final.ptau

# BN254 (smaller, 2^21 constraints — Tornado Cash size)
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_21.ptau

# Verify checksums
sha256sum powersOfTau28_hez_final_21.ptau
# Expected: 8b026...
```

### Running Your Own Phase 1 (NOT recommended)

Only run your own Phase 1 if:
1. Using a curve not covered by existing ceremonies
2. Need constraint count > 2^28
3. Will have independent participants (at least 3, ideally 10+)

```bash
# Start new ceremony
snarkjs powersoftau new bn128 21 pot21_0000.ptau -v

# Each participant contributes
snarkjs powersoftau contribute pot21_0000.ptau pot21_0001.ptau --name="Alice" -v

# Apply random beacon (REQUIRED)
snarkjs powersoftau beacon pot21_000N.ptau pot21_beacon.ptau \
  0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f 10 -n="Final Beacon"

# Prepare for Phase 2
snarkjs powersoftau prepare phase2 pot21_beacon.ptau pot21_final.ptau -v
```

## Circuit-Specific Setup (Phase 2)

### Standard Phase 2 Workflow

```bash
# 1. Compile circuit
circom circuit.circom --r1cs --wasm -o build/

# 2. Initialize Phase 2
snarkjs groth16 setup build/circuit.r1cs pot21_final.ptau circuit_0000.zkey

# 3. Each participant contributes
snarkjs zkey contribute circuit_0000.zkey circuit_0001.zkey --name="Participant 1" -v
snarkjs zkey contribute circuit_0001.zkey circuit_0002.zkey --name="Participant 2" -v
# ... more participants

# 4. Apply random beacon (REQUIRED for final contribution)
snarkjs zkey beacon circuit_000N.zkey circuit_final.zkey \
  0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f 10 -n="Final Beacon"

# 5. Verify final zkey
snarkjs zkey verify build/circuit.r1cs pot21_final.ptau circuit_final.zkey

# 6. Export verification key (public)
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json
```

### Participant Requirements

- **Independence:** Participants must not collude; at least one honest participant required
- **Entropy:** Each participant must introduce high-quality entropy
- **Verification:** Each participant should verify the previous contribution
- **Toxic waste destruction:** Each participant must destroy their generated randomness after contribution
- **No trust assumption:** If ANY one participant is honest, the ceremony is secure

### Key Management

| Key | Sensitive? | Usage |
|-----|-----------|-------|
| Proving key (.zkey) | No | Generate proofs |
| Verification key | No | Verify proofs (public) |
| Phase 1 toxic waste | YES — MUST DESTROY | Can forge proofs if leaked |
| Phase 2 toxic waste | YES — MUST DESTROY | Can forge proofs if leaked |
| Witness (.wtns) | YES — contains private inputs | Never share |

## Alternatives to Trusted Setup

If a trusted setup ceremony is not feasible:

1. **STARKs:** Fully transparent, no setup required
2. **Halo2:** No setup, uses inner product arguments
3. **Plonky3:** No trusted setup, plonkish arithmetization
4. **PLONK:** Universal SRS (one-time, reusable across circuits)

### PLONK Universal Setup

```bash
# One-time universal setup for PLONK
snarkjs plonk setup build/circuit.r1cs pot21_final.ptau circuit.zkey
# Reusable SRS — no per-circuit ceremony
# But: larger proofs than Groth16, higher verification gas
```

## Ceremony Verification Checklist

- [ ] Phase 1 artifact downloaded from reputable source (Hermez, Perpetual)
- [ ] SHA256 checksum verified
- [ ] Minimum 3 independent participants for Phase 2
- [ ] Random beacon applied as final contribution
- [ ] `snarkjs zkey verify` passes
- [ ] All participants confirm toxic waste destruction
- [ ] Verification key published for public audit
- [ ] Circuit source code published and reproducible
