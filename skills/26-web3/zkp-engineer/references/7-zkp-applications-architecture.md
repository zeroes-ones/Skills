## 7. ZKP Applications Architecture

### Private Transactions (Tornado Cash Pattern)

```
┌──────────────────────────────────────────────────────────────┐
│                  TORNADO CASH ARCHITECTURE                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Deposit:                                                    │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  User    │───>│ Poseidon(2)  │───>│ Merkle Tree      │   │
│  │ secret+  │    │ commitment = │    │ root updated     │   │
│  │ nullifier│    │ H(secret,n)  │    │ on-chain         │   │
│  └──────────┘    └──────────────┘    └──────────────────┘   │
│                                                              │
│  Withdraw:                                                   │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  ZKP     │───>│ Prove:       │───>│ Contract checks: │   │
│  │  Circuit │    │ - Know secret │    │ - Valid root      │   │
│  │          │    │ - commitment  │    │ - No nullifier    │   │
│  │          │    │   in tree     │    │   replay          │   │
│  │          │    │ - nullifier = │    │ - Execute tx      │   │
│  │          │    │   H(secret)   │    │                   │   │
│  └──────────┘    └──────────────┘    └──────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### zk-Rollup Architecture

```
L1 (Ethereum)
├── Rollup Contract
│   ├── State root commitment
│   ├── Verifier (Groth16/Plonky3)
│   └── Data availability (calldata/blob)
│
L2 (Rollup)
├── Sequencer: orders transactions
├── Prover: generates validity proof
│   ├── Executes all L2 transactions
│   ├── Computes new state root
│   └── Generates ZKP of state transition
└── Proof submitted to L1 → Verifier validates → State root updated
```

### zk-Identity / DID

```circom
// Semaphore-style anonymous group membership
template ProveMembership() {
    signal input identitySecret;
    signal input groupId;
    signal input merkleRoot;
    signal input merkleProof[20];
    signal input merklePathIndices[20];
    signal input signal_hash;  // External signal (message)

    // 1. Compute identity commitment
    component idCommitment = Poseidon(1);
    idCommitment.inputs[0] <== identitySecret;

    // 2. Prove membership in Merkle tree
    component tree = MerkleInclusionProof(20);
    tree.leaf <== idCommitment.out;
    tree.root <== merkleRoot;
    // ... path elements assigned

    // 3. Compute nullifier (prevents double-signaling)
    component nullifier = Poseidon(2);
    nullifier.inputs[0] <== identitySecret;
    nullifier.inputs[1] <== signal_hash;
    // nullifier uniquely identifies (identity, signal) pair
}
```

### zkML

Prove that an ML inference was computed correctly without revealing the model or input. Approaches:
- **ezkl:** Compile ONNX models to Halo2 circuits
- **zkonduit:** Circom-based ML inference proofs
- **Risc Zero:** Run inference inside zkVM, prove execution trace

### zk-Email

Prove ownership of an email address or verify email content without revealing the full email. Pattern: DKIM signature verification inside a ZKP circuit. Reference: `references/zkp-applications-architecture.md`
