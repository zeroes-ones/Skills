# ZKP Security Hardening

## Overview

Comprehensive security hardening checklist for ZKP circuits, covering constraint completeness, signal privacy, and deployment hardening.

## Constraint Completeness Audit

### Step 1: Output Signal Audit

For every `signal output` in the circuit:
- [ ] Constrained via `<==` (direct assignment AND constraint)
- [ ] If assigned via `<--`, paired with `===` constraint
- [ ] Not assignable to arbitrary value by prover

```circom
// BAD: Output can be any value
signal output x;
x <-- someValue;  // Unconstrained!

// GOOD: Output is properly constrained
signal output x;
x <== someValue;  // Constrained!
```

### Step 2: Signal Flow Graph

Trace every signal from input to output:
- Every intermediate signal must participate in at least one constraint path
- No orphan signals (computed but never used in constraints)
- No cycles that could create unsatisfiable constraints

### Step 3: Branch Coverage

Verify all execution branches constrain outputs:

```circom
// BAD: Only constrains output when condition == 1
if (condition == 1) {
    output <== someValue;
}
// BUG: When condition != 1, output is free

// GOOD: Always constrains output
signal trueCase;
signal falseCase;
trueCase <== someValue;
falseCase <== defaultValue;
output <== condition * trueCase + (1 - condition) * falseCase;
```

### Step 4: Array Completeness

For array signals, verify ALL elements are constrained:

```circom
// BAD: Only first element constrained
for (var i = 0; i < n; i++) {
    if (i == 0) {
        results[i] <== compute(i);
    } else {
        results[i] <-- compute(i);  // Unconstrained!
    }
}

// GOOD: All elements constrained
for (var i = 0; i < n; i++) {
    results[i] <== compute(i);
}
```

## Signal Privacy Audit

### Public Input Review

Every `signal input` passed as public to `snarkjs groth16 prove` is visible to verifiers. Audit:
- [ ] Only necessary outputs are public (root, nullifier, commitment)
- [ ] No intermediate values exposed as public inputs
- [ ] No private state derivable from public inputs
- [ ] Public inputs don't leak information about private inputs

### Information Leakage via Public Inputs

```circom
// LEAK: Exposes partial computation as public input
signal input privateBalance;
signal output publicBalanceChange;  // Leaks balance delta!
publicBalanceChange <== newBalance - privateBalance;

// FIX: Only expose commitment, not delta
signal output newCommitment;
newCommitment <== Poseidon(1)([newBalance]);
```

## Common Vulnerability Patterns

### 1. Unconstrained Division

```circom
// BAD: Division by potentially zero denominator
result <-- a / b;     // Witness computation
result * b === a;     // Constraint

// If b == 0:
// - Witness generation with a/0 CRASHES
// - But constraint 0 * b == 0 is satisfiable
// - Adversary can craft malicious witness

// FIX: Handle zero case explicitly
signal bIsZero;
bIsZero <== IsZero()(b);
signal safeB;
safeB <-- bIsZero == 1 ? 1 : b;
result <-- a / safeB;
(1 - bIsZero) * (result * b - a) === 0;
bIsZero * a === 0;  // If b=0, a must be 0
```

### 2. Modulo in Constraints

```circom
// BAD: Modulo in field doesn't behave like integer modulo
result <-- a % b;  // Field division, NOT integer modulo
// Fix: Use Num2Bits + comparison for integer-like modulo
```

### 3. Overflow Without Range Check

```circom
// BAD: balance can overflow field, wrapping around
signal output newBalance;
newBalance <== oldBalance - amount;  // May underflow in field

// FIX: Enforce non-negative with range check
component rangeCheck = Num2Bits(64);
rangeCheck.in <== newBalance;
// Also check: oldBalance >= amount
```

### 4. Boolean Without Constraint

```circom
// BAD: flag appears to be Boolean but isn't constrained
flag <-- someCondition;  // Could be any value

// FIX: Enforce Boolean
flag <-- someCondition;
flag * (flag - 1) === 0;  // Must be 0 or 1
```

## Security Audit Checklist

### Pre-Deployment
- [ ] All output signals constrained
- [ ] All public inputs have range checks
- [ ] All bit signals have Boolean constraints
- [ ] No division by unconstrained variable
- [ ] No `<--` without corresponding `===`
- [ ] Running `snarkjs r1cs info` shows expected constraint count
- [ ] Circuit passes fuzz testing with random inputs
- [ ] Circuit passes negative tests (invalid witnesses fail)
- [ ] Gas benchmarked with realistic inputs on testnet
- [ ] Verification key published and reproduced independently

### Trusted Setup
- [ ] Phase 1 artifact from reputable ceremony (not self-generated)
- [ ] Minimum 3 independent Phase 2 contributions
- [ ] Random beacon applied as final contribution
- [ ] `snarkjs zkey verify` passes
- [ ] Participants destroyed toxic waste

### Contract Integration
- [ ] Nullifier mapping prevents double-spend
- [ ] Re-entrancy protection for post-verification ETH transfers
- [ ] Public input ordering matches circuit output signals
- [ ] Gas limit sufficient for worst-case proof
- [ ] Events emitted for proof verification
- [ ] Upgrade mechanism documented

### Operational
- [ ] Prover key is not sensitive (can be public)
- [ ] Witness files never shared or persisted
- [ ] Proving infrastructure can handle expected load
- [ ] Monitoring for proof verification failures
- [ ] Circuit and ceremony artifacts backed up securely
