# ZKP Applications Architecture

## Overview

Production architectures for the most common ZKP applications: private transactions, zk-rollups, zk-identity, zkML, and zk-email.

## 1. Private Transactions (Tornado Cash Pattern)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DEPOSIT PHASE                        │
├─────────────────────────────────────────────────────────┤
│  1. User generates: secret (random), nullifier (random) │
│  2. commitment = Poseidon(secret, nullifier)            │
│  3. Submit commitment + ETH to contract                 │
│  4. Contract inserts commitment into Merkle tree         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   WITHDRAW PHASE                        │
├─────────────────────────────────────────────────────────┤
│  1. User constructs ZK proof:                           │
│     - Knows (secret, nullifier) for some commitment     │
│     - Commitment is in Merkle tree (root)               │
│     - nullifierHash = Poseidon(nullifier)               │
│  2. Submit proof + [root, nullifierHash, recipient]      │
│  3. Contract verifies proof                             │
│  4. Contract checks nullifierHash is unused             │
│  5. Contract releases ETH to recipient                  │
└─────────────────────────────────────────────────────────┘
```

### Privacy Guarantees

- **Anonymity set:** Size of Merkle tree (e.g., 2^20 = 1M depositors)
- **Unlinkability:** Deposit and withdrawal are cryptographically unlinkable
- **Double-spend prevention:** Nullifier hash prevents reusing the same deposit

## 2. zk-Rollups

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    L1 (Ethereum)                        │
├─────────────────────────────────────────────────────────┤
│  Rollup Contract:                                       │
│  - Stores state root                                    │
│  - Verifier contract (validates state transition proof) │
│  - Data availability (calldata or EIP-4844 blobs)       │
│  - Bridge (L1 ↔ L2 asset transfers)                     │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │ proof
                           │
┌─────────────────────────────────────────────────────────┐
│                    L2 (Rollup)                          │
├─────────────────────────────────────────────────────────┤
│  Sequencer:                                             │
│  - Orders transactions into batches                     │
│  - Produces L2 blocks                                    │
│  - Publishes transaction data to L1                     │
│                                                         │
│  Prover:                                                │
│  - Executes all transactions in batch                   │
│  - Computes pre-state root and post-state root          │
│  - Generates ZK proof: state_root_prev → state_root_new │
│  - Submits proof to L1 verifier                         │
└─────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Options | Trade-offs |
|----------|---------|------------|
| Proof system | Groth16/Plonky3/STARK | Gas vs proving time |
| Data availability | Calldata / Blobs / Validium | Security vs cost |
| Prover centralization | Single prover / Decentralized | Latency vs censorship resistance |
| Forced transactions | L1 inclusion / L2-only | Censorship resistance |
| Upgrade mechanism | Security council / Timelock / Immutable | Security vs flexibility |

## 3. zk-Identity / DID

### Semaphore Architecture

```
┌─────────────────────────────────────────────────────────┐
│              SEMAPHORE IDENTITY SYSTEM                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Group Manager:                                         │
│  - Manages Merkle tree of identity commitments          │
│  - Adds/removes members                                  │
│                                                         │
│  User:                                                  │
│  - identityCommitment = Poseidon(identitySecret)        │
│  - identitySecret + identityNullifier = secret pair     │
│                                                         │
│  Signal (anonymous proof):                              │
│  - nullifierHash = Poseidon(identityNullifier, scope)   │
│  - signalHash = Poseidon(message)                       │
│  - Proof: "I'm in group AND this is my first signal     │
│            for this scope"                              │
│                                                         │
│  Verifier:                                              │
│  - Checks proof validity                                │
│  - Checks nullifierHash not seen before                 │
│  - Records nullifierHash                                │
└─────────────────────────────────────────────────────────┘
```

### Use Cases

- **Anonymous voting:** One vote per group member, unlinkable
- **Anonymous credentials:** Prove group membership without revealing identity
- **Rate limiting:** One action per identity per time period
- **Airdrop claims:** Prove eligibility without revealing address

## 4. zkML (Zero-Knowledge Machine Learning)

### Architecture Patterns

**Pattern A: Proof of Inference**
```
1. Model owner commits to model hash
2. User submits input (encrypted or public)
3. Prover runs inference: output = model(input)
4. Prover generates ZKP: "output is correct for committed model"
5. Verifier checks proof without seeing model weights
```

**Pattern B: Private Input Inference**
```
1. User commits to input (encrypted)
2. Service runs inference on committed input
3. Service generates ZKP: "output is correct for committed input"
4. User receives output; service never sees plaintext input
```

### Tools

| Tool | Approach | Performance |
|------|----------|-------------|
| ezkl | ONNX → Halo2 circuit | ~minutes for small models |
| zkonduit | Circom templates for ML ops | ~minutes for medium models |
| Risc Zero zkVM | Run inference in zkVM | ~minutes to hours |
| Daniel (Modulus Labs) | Specialized circuits | Variable |

## 5. zk-Email

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 zk-EMAIL ARCHITECTURE                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. User receives email from service (e.g., "confirm")  │
│  2. User proves in ZKP:                                 │
│     a. Email has valid DKIM signature from domain       │
│     b. Email body contains specific text ("confirmed")  │
│     c. Email was sent to user's address                 │
│  3. Contract verifies proof + checks domain whitelist   │
│  4. Contract executes logic (mint, transfer, verify)    │
│                                                         │
│  Technical challenge:                                    │
│  - RSA signature verification in circuit (~1M+ gates)  │
│  - Email body parsing in circuit                       │
│  - Header canonicalization per DKIM spec               │
│                                                         │
│  Reference: zk-email/zk-email-verify (Circom 2)        │
└─────────────────────────────────────────────────────────┘
```

### Circuit Breakdown (zk-email-verify)

```circom
// Simplified zk-email circuit structure
template EmailVerifier(maxHeaderLength, maxBodyLength) {
    // 1. DKIM signature verification (RSA, SHA256)
    // 2. Header parsing and canonicalization
    // 3. Body hash computation
    // 4. Regex matching on body/header fields
    // 5. Output: verified domain, matched fields
}
```

## Deployment Checklist by Application

### Private Transactions
- [ ] Poseidon hash library audited
- [ ] Nullifier uniqueness enforced in contract
- [ ] Merkle tree insertion/deletion correct
- [ ] ETH transfer handles revert cases
- [ ] Anonymity set size disclosed to users
- [ ] Front-running protection (commit-reveal or relay)

### zk-Rollup
- [ ] Prover uptime and redundancy
- [ ] Forced transaction mechanism
- [ ] Emergency exit (escape hatch)
- [ ] Upgrade mechanism defined
- [ ] Data availability guarantees documented
- [ ] Fraud proof window (if optimistic component)
- [ ] Fee market for L2 inclusion

### zk-Identity
- [ ] Group manager trust model documented
- [ ] Nullifier scope separation (prevent cross-app replay)
- [ ] Rate limiting per identity
- [ ] Identity recovery mechanism (if applicable)
- [ ] Privacy set size disclosed

### zkML
- [ ] Model commitment scheme (hash of weights)
- [ ] Input privacy guarantees documented
- [ ] Proving time acceptable for use case
- [ ] Model accuracy verified against reference
- [ ] Adversarial input handling

### zk-Email
- [ ] DKIM key rotation handling
- [ ] Domain whitelist maintained
- [ ] Email replay prevention (timestamp/nonce)
- [ ] Header injection prevention
- [ ] Body regex safety (ReDoS prevention)
