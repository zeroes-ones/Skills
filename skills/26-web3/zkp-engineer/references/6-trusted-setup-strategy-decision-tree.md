## 6. Trusted Setup Strategy (Decision Tree)

```
┌───────────────────────────────────────────────────────────────┐
│              TRUSTED SETUP STRATEGY DECISION TREE              │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Is trusted setup acceptable?                                 │
│       │                                                       │
│  ┌────┴────┐                                                  │
│ YES       NO ──> Use STARKs or Halo2 (transparent/no setup)   │
│  │                                                             │
│  │                                                             │
│  Circuit is fixed (won't change)?                              │
│       │                                                       │
│  ┌────┴────┐                                                  │
│ YES       NO ──> Use Halo2/Plonky3 (no per-circuit setup)     │
│  │                                                             │
│  │                                                             │
│  Using Groth16? ──YES──> Powers of Tau Phase 1 + Phase 2      │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Using PLONK? ──YES──> Universal setup (reusable SRS)         │
│                                                               │
│  Phase 1 (Powers of Tau):                                     │
│  - Universal, circuit-independent                             │
│  - Can use existing ceremonies (Perpetual Powers of Tau)      │
│  - Requires at least 1 honest participant                     │
│                                                               │
│  Phase 2 (Circuit-Specific):                                  │
│  - Per-circuit, must re-run if circuit changes                │
│  - Can be deterministic with MPC                              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Powers of Tau Ceremony Checklist

1. **Phase 1:** Use existing Perpetual Powers of Tau (BN254, BLS12-381) — do NOT run your own for standard curves
2. **Phase 2:** Implement multi-party computation (MPC) with independent participants
3. **Verification:** Verify contribution transcripts with `snarkjs powersoftau verify`
4. **Circuit changes:** ANY change to constraints requires a new Phase 2
5. **Key management:** Proving key is non-sensitive; verification key is public
6. **Toxic waste:** Each participant generates and destroys random toxic waste — one honest participant breaks collusion

```bash
# Phase 1: Download Powers of Tau (BN254, 2^21 constraints)
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_21.ptau

# Phase 2: Circuit-specific setup
snarkjs groth16 setup circuit.r1cs powersOfTau28_hez_final_21.ptau circuit_0000.zkey
snarkjs zkey contribute circuit_0000.zkey circuit_0001.zkey --name="Participant 1"
snarkjs zkey beacon circuit_0001.zkey circuit_final.zkey 0102030405060708090a0b0c0d0e0f
snarkjs zkey verify circuit.r1cs powersOfTau28_hez_final_21.ptau circuit_final.zkey

# Export verification key
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json

# Generate Solidity verifier
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol
```
