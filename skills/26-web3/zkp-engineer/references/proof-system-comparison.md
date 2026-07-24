# Proof System Comparison Matrix

## Overview

Detailed comparison of production ZKP proof systems for engineering decision-making.

## Quick Reference

| Criterion | Groth16 | STARKs | Halo2 | Plonky3 |
|-----------|---------|--------|-------|---------|
| Proving time (2^16 constr) | 8.2s | 78.3s | 15.7s | 2.1s |
| Proving time (2^20 constr) | 142s | 1200s | 240s | 38s |
| Verification (native) | 2.1ms | 42ms | 8.9ms | 4.2ms |
| EVM verification gas | 237K | 2.5M | 350K | 280K |
| Proof size | 128B | 185KB | 1088B | 2048B |
| Trusted setup | Required | None | None | None |
| Post-quantum | No | Yes | No | No |
| Recursive native | Via composition | FRI recursion | Native | Folding |
| Setup size | 8.2MB | 0B | 0B | 0B |
| Maturity | High | Medium-High | Medium | Medium |
| Curve/Field | BN254/BLS12-381 | Any | Pasta (Pallas/Vesta) | Goldilocks/M31 |

## Groth16

**Best for:** Fixed circuits, minimal on-chain verification cost.

**Strengths:**
- Smallest proof size (128 bytes for BN254)
- Fastest on-chain verification (~230K gas)
- Mature ecosystem: snarkjs, circomlib, circomkit
- Widely deployed: Zcash Sapling, Tornado Cash, Semaphore

**Weaknesses:**
- Circuit-specific trusted setup (Phase 2 required per circuit)
- Cannot change circuit without new ceremony
- No post-quantum security
- Proving time scales linearly with constraints

**When to choose:**
- Fixed circuit won't change after deployment
- On-chain verification gas is a primary concern
- Project can run trusted setup ceremony
- Need production-grade tooling and libraries

## STARKs

**Best for:** Post-quantum security, large computation statements.

**Strengths:**
- Transparent setup (no trusted ceremony)
- Post-quantum secure
- No per-circuit setup
- FRI protocol is well-understood
- Works with any field

**Weaknesses:**
- Large proof size (50-200KB)
- Expensive on-chain verification (~2.5M gas)
- Slow proving time
- Limited zkEVM deployments compared to SNARK-based

**When to choose:**
- Post-quantum security is a hard requirement
- Proof is verified off-chain or on L2
- Large computation statements (zkEVM execution traces)
- Cannot run trusted setup

## Halo2

**Best for:** Recursive proofs, evolving circuits, lookup tables.

**Strengths:**
- No trusted setup (transparent)
- Native recursion support
- Efficient lookup tables (single constraint per range check)
- Custom gates for performance
- Used by Zcash Orchard, Scroll zkEVM

**Weaknesses:**
- Steeper learning curve (Rust library, not DSL)
- Proving time slower than Plonky3
- Limited EVM verifier optimization
- Pasta curves not natively supported on Ethereum

**When to choose:**
- Need recursive proof composition
- Circuit may evolve over time
- Require efficient lookup tables (SHA256, keccak, range checks)
- Team comfortable with Rust

## Plonky3

**Best for:** Maximum proving throughput, cost-sensitive deployments.

**Strengths:**
- Fastest proving time (ultra-fast)
- No trusted setup
- Small field (Goldilocks-64, Mersenne31) enables fast arithmetic
- Plonkish arithmetization with custom gates
- Used by Polygon Zero, SP1

**Weaknesses:**
- Newer ecosystem (fewer libraries than Circom)
- Small field may limit some applications
- EVM verification requires field emulation
- Documentation still evolving

**When to choose:**
- High-frequency proving required
- Cost-sensitive deployment
- SP1 or custom zkVM integration
- Team wants maximum performance

## Selection Flowchart

```
Need post-quantum? → STARKs
Need smallest on-chain gas? → Groth16
Need fastest proving? → Plonky3
Need recursion + lookups? → Halo2
Need mature ecosystem? → Groth16 (Circom 2)
Need Rust-native development? → Halo2 (Rust) or Noir
```
