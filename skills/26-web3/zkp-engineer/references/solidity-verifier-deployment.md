# Solidity Verifier Deployment

## Overview

Deploying on-chain verifiers for ZKP systems, with gas cost optimization and production patterns.

## Groth16 Verifier (snarkjs-generated)

### Quick Deployment

```bash
# 1. Export Solidity verifier
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol

# 2. Export calldata for specific proof
snarkjs zkey export soliditycalldata public.json proof.json

# 3. Deploy verifier
forge create --rpc-url $RPC_URL Verifier --private-key $PRIVATE_KEY

# 4. Verify proof on-chain
cast send $VERIFIER_ADDRESS "verifyProof(uint256[2],uint256[2][2],uint256[2],uint256[4])" \
  $PROOF_A $PROOF_B $PROOF_C $PUBLIC_INPUTS --rpc-url $RPC_URL
```

### Standard Wrapper Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Verifier} from "./Verifier.sol";

contract ZKApplication {
    Verifier public immutable verifier;
    mapping(uint256 => bool) public nullifiers;

    constructor() {
        verifier = new Verifier();
    }

    function verify(
        uint256[2] calldata a,
        uint256[2][2] calldata b,
        uint256[2] calldata c,
        uint256[4] calldata publicInputs
    ) internal view returns (bool) {
        return verifier.verifyProof(a, b, c, publicInputs);
    }

    function processWithZKP(
        uint256[2] calldata a,
        uint256[2][2] calldata b,
        uint256[2] calldata c,
        uint256[4] calldata publicInputs
    ) external {
        uint256 nullifierHash = publicInputs[1];
        require(!nullifiers[nullifierHash], "Nullifier used");
        require(verify(a, b, c, publicInputs), "Invalid proof");

        nullifiers[nullifierHash] = true;

        // Application logic after ZK verification
        _executeAction(publicInputs);
    }

    function _executeAction(uint256[4] memory publicInputs) internal {
        // e.g., transfer, mint, vote
    }
}
```

## Gas Cost Breakdown

### Groth16 Verification Gas

| Component | Gas | Notes |
|-----------|-----|-------|
| Pairing check (3 pairs) | ~180K | BN254 precompile |
| Public input processing | ~30K | Depends on input count |
| Base overhead | ~20K | Function call, memory |
| **Total** | **~230K** | Per verification |

### PLONK Verification Gas

| Component | Gas | Notes |
|-----------|-----|-------|
| Pairing check (2 pairs) | ~120K | Fewer pairings |
| Opening proofs | ~100K | KZG commitments |
| Public inputs | ~40K | More complex than Groth16 |
| Base overhead | ~30K | |
| **Total** | **~290K** | ~25% more than Groth16 |

### STARK Verification Gas

| Component | Gas | Notes |
|-----------|-----|-------|
| FRI verification | ~1.5M | Merkle path checks |
| FFT verification | ~500K | Field operations in EVM |
| Public inputs | ~200K | |
| Base overhead | ~300K | |
| **Total** | **~2.5M** | ~10x Groth16 |

## Gas Optimization Strategies

### 1. Proof Aggregation (SnarkPack)

```solidity
// Verify 100 Groth16 proofs in one aggregated proof
// Gas savings: ~220K per proof → ~30K per proof
contract AggregatedVerifier {
    SnarkPackVerifier public immutable aggregator;

    function verifyBatch(
        uint256[2] calldata aggregatedProof,
        uint256[100] calldata publicInputs
    ) external {
        // Single verification for 100 proofs
        require(
            aggregator.verifyAggregatedProof(aggregatedProof, publicInputs),
            "Invalid batch"
        );
    }
}
```

### 2. BLS12-381 vs BN254

```solidity
// BN254: ~230K gas, 100-bit security
// BLS12-381: ~340K gas, 128-bit security
// Choose BN254 for EVM unless >100-bit security required
```

### 3. Verifier as Library (Immutable)

```solidity
// Deploy verifier once, use as library
// Saves deployment gas for each application
library Groth16Verifier {
    function verifyProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[] memory input
    ) internal view returns (bool) {
        // Verification logic
    }
}

contract AppA {
    using Groth16Verifier for *;
    // Reuses library — no additional deployment
}
```

### 4. Calldata Compression

```solidity
// Compress proof data before L1 submission (rollup pattern)
// Saves calldata gas (16 gas/byte zero, 4 gas/byte non-zero)
function submitBatch(bytes calldata compressedProof) external {
    // Decompress in contract
    bytes memory proof = decompress(compressedProof);
    // Verify decompressed proof
}
```

### 5. EIP-4844 Blobs

```solidity
// For zk-rollups: store proof data in blobs
// Blob gas: ~128K per blob (128KB) vs ~700K in calldata
// Requires EIP-4844 (Cancun upgrade)
```

## Production Deployment Checklist

- [ ] Verifier contract deployed to testnet first
- [ ] Gas benchmarked with actual proof (not estimate)
- [ ] Gas limit set appropriately (230K-350K per proof)
- [ ] `verification_key.json` published for audit
- [ ] Circuit source and compilation parameters documented
- [ ] Nullifier mapping uses `mapping(uint256 => bool)` (not array)
- [ ] Re-entrancy protection (if ETH transfers follow verification)
- [ ] Upgrade mechanism defined (immutable or governed)
- [ ] Emergency pause for verifier (optional, trade-off)
- [ ] Event emitted on proof verification for indexing

## Common Issues

### Issue 1: Proof Verification Fails on-chain but Succeeds Off-chain

```solidity
// Common causes:
// 1. Different field order (BN254 scalar field vs EVM uint256)
// 2. Public input ordering mismatch
// 3. Verifier compiled with wrong Powers of Tau
// Fix: Verify proof against on-chain verifier in fork test
```

### Issue 2: Out of Gas During Verification

```solidity
// Groth16 verifier needs ~230K gas
// Always set gas limit > 300K
// For aggregated proofs: gas limit > 500K
```

### Issue 3: Public Input Array Too Large

```solidity
// snarkjs generates fixed-size public input arrays
// Must match circuit output signal count exactly
// Extra: signal output x; → 1 public input
// Fixed: signal output x[10]; → 10 public inputs
```
