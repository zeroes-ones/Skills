## 3. Constraint Security (Decision Tree + Gotchas)

### Under-Constraint Detection Decision Tree

```
┌───────────────────────────────────────────────────────────────┐
│           UNDER-CONSTRAINT DETECTION DECISION TREE             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Signal declared as output? ──YES──> Is it constrained?       │
│       │                              │                        │
│      NO                           ┌──┴──┐                    │
│       │                          YES    NO ──> CRITICAL BUG   │
│       │                           │      (forgery possible)   │
│  Is signal intermediate?          │                           │
│       │                    All output signals                 │
│  ┌────┴────┐               properly constrained               │
│ YES       NO                                                 │
│  │         │                                                 │
│  │    No constraint     Check: Is intermediate used           │
│  │    needed               in constraint chain?               │
│  │    (private signal)         │                              │
│  │                        ┌────┴────┐                         │
│  │                       YES       NO ──> WARNING             │
│  │                        │         (unused signal)           │
│  │                   Path leads                               │
│  │                   to === or <==                            │
│  │                   constraint                               │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Gotcha #1: Under-Constrained Circuit (CRITICAL — $10M+ exploited)

**The vulnerability:** A signal that should be constrained is left unconstrained, allowing a malicious prover to forge proofs for invalid statements.

```circom
// VULNERABLE: Under-constrained output signal
// Taken from real exploit pattern in zk-bridge incident
pragma circom 2.1.6;

template VulnerableTransfer() {
    signal input sender;
    signal input recipient;
    signal input amount;
    signal input senderBalance;

    // BUG: balanceAfter is declared but never constrained!
    signal output balanceAfter;

    // Only this check exists — balanceAfter is free
    signal validAmount;
    validAmount <== amount * (amount > 0);  // Boolean check

    // balanceAfter is an output signal with NO constraints!
    // Attacker can set balanceAfter to any value in witness
    balanceAfter <-- senderBalance - amount;  // <-- assigns but does NOT constrain!
}

// FIXED: Properly constrain the output
template SecureTransfer() {
    signal input sender;
    signal input recipient;
    signal input amount;
    signal input senderBalance;

    signal output balanceAfter;

    // Fix 1: Use <== (constrains AND assigns)
    balanceAfter <== senderBalance - amount;

    // Fix 2: Add range check on balanceAfter
    component rangeCheck = Num2Bits(64);
    rangeCheck.in <== balanceAfter;

    // Fix 3: Ensure balance doesn't overflow
    signal zeroCheck;
    zeroCheck <== (senderBalance - amount) * (senderBalance >= amount);
    zeroCheck === 0;  // Enforces non-negative when senderBalance < amount
}
```

**Key operators in Circom 2:**
- `<==` : Constrain AND assign (safe default)
- `<--` : Assign ONLY, no constraint (DANGEROUS — use only for witness computation)
- `===` : Constrain equality

### Gotcha #2: Missing Range Check on Public Input

```circom
// VULNERABLE: No range check on public input
template VulnerableWithdraw() {
    signal input nullifier;  // Public input — no range check!
    signal input secret;
    signal input root;

    // Poseidon hash check
    component hash = Poseidon(1);
    hash.inputs[0] <== secret;

    component tree = MerkleInclusionProof(20);
    tree.leaf <== hash.out;
    tree.root <== root;

    // BUG: nullifier is unconstrained public input
    // Attacker can provide same nullifier twice → double-spend
    // Or overflow nullifier beyond field modulus
    nullifier === Poseidon(1)([secret, 0]);  // Only constrains equality
    // Missing: nullifier < 21888242871839275222246405745257275088548364400416034343698204186575808495617
}

// FIXED: Range check public inputs
template SecureWithdraw() {
    signal input nullifier;
    signal input secret;
    signal input root;

    // Fix: Range check nullifier (must be less than SNARK scalar field)
    component nullifierCheck = Num2Bits(254);
    nullifierCheck.in <== nullifier;

    component hash = Poseidon(1);
    hash.inputs[0] <== secret;

    component tree = MerkleInclusionProof(20);
    tree.leaf <== hash.out;
    tree.root <== root;

    signal nullifierConstraint;
    nullifierConstraint <== Poseidon(1)([secret, 0]) - nullifier;
    nullifierConstraint === 0;
}
```

### Gotcha #3: Incorrect Bit Decomposition (Witness Malleability)

```circom
// VULNERABLE: Bit decomposition without Boolean enforcement
template VulnerableBits(n) {
    signal input in;
    signal output bits[n];

    var acc = 0;
    for (var i = 0; i < n; i++) {
        bits[i] <-- (in >> i) & 1;  // <-- No constraint!
        acc += bits[i] * (1 << i);
    }
    in === acc;  // Only constrains sum, not individual bits

    // BUG: bits[i] can be any value as long as sum matches
    // e.g., in=5, bits could be [5, 0, 0, ...] or [-3, 8, 0, ...]
}

// FIXED: Enforce each bit is binary
template SecureBits(n) {
    signal input in;
    signal output bits[n];

    var acc = 0;
    for (var i = 0; i < n; i++) {
        bits[i] <-- (in >> i) & 1;

        // Critical: Enforce bits[i] is 0 or 1
        bits[i] * (bits[i] - 1) === 0;  // Boolean constraint

        acc += bits[i] * (1 << i);
    }
    in === acc;
}
```

### Gotcha #4: Trusted Setup Compromise (Groth16)

A single dishonest participant in the Powers of Tau ceremony can forge proofs. The ceremony requires at least one honest participant — but verifying which participants were honest is impossible post-ceremony. Mitigations: Use community ceremonies with hundreds of participants (Perpetual Powers of Tau had 80+), implement circuit-specific phase 2 ceremonies, or choose transparent-setup systems (STARKs, Halo2).

### Gotcha #5: Non-Deterministic Witness Generation

```circom
// BUG: Signal ordering depends on witness assignment order
template NonDeterministic() {
    signal input a;
    signal input b;
    signal output c;

    // If a=0, division by zero causes witness generation failure
    // But constraint still exists — proof generation crashes
    c <-- b / a;  // May crash in witness generation
    c * a === b;  // Constraint is fine, but witness calc fails
}

// FIXED: Handle edge cases in witness computation
template Deterministic() {
    signal input a;
    signal input b;
    signal output c;

    signal aIsZero;
    aIsZero <== IsZero()(a);

    // Use safe division or branch in witness
    signal safeA;
    safeA <-- aIsZero == 1 ? 1 : a;
    c <-- b / safeA;

    // Constraint: if a!=0, c*a == b; if a==0, b must be 0
    (1 - aIsZero) * (c * a - b) === 0;
    aIsZero * b === 0;
}
```

### Gotcha #6: Gas Cost Underestimation for On-Chain Verifiers

Groth16 verification on Ethereum: ~230K gas ($50-100 at 30 gwei). STARK verification: ~2.5M gas ($500-1000). For zk-rollup batches, a single Groth16 proof verifies thousands of transactions, making per-tx cost negligible. However, STARK verification for the same batch is ~10x more expensive on L1. **Always benchmark with actual Solidity verifier deployment** — theoretical gas estimates from whitepapers often underestimate by 2-3x.

### Gotcha #7: Missing Nullifier Collision Prevention

```circom
// VULNERABLE: No nullifier uniqueness enforcement
template VulnerableNullifier() {
    signal input secret;
    signal input externalNullifier;
    signal output nullifierHash;

    // BUG: Same secret + same externalNullifier = same nullifier
    // Allows double-spend if externalNullifier is reused
    nullifierHash <== Poseidon(2)([secret, externalNullifier]);
}

// FIXED: Enforce externalNullifier uniqueness at contract level
// AND add domain separator to nullifier computation
template SecureNullifier() {
    signal input secret;
    signal input externalNullifier;
    signal input scope;  // Unique per-application scope
    signal output nullifierHash;

    // Domain separation prevents cross-application replay
    nullifierHash <== Poseidon(3)([secret, externalNullifier, scope]);

    // Contract must track used nullifiers:
    // mapping(uint256 => bool) public nullifierHashes;
}
```

### Gotcha #8: Public Input Exposure via Side Channels

Intermediate signals that appear in public inputs (for debugging or verification convenience) can leak private state. Every public signal is visible to verifiers and on-chain observers. **Audit rule:** Every `signal input` that is also a public input to `snarkjs groth16 prove` must be explicitly justified. Never expose partial computation results as public inputs.
