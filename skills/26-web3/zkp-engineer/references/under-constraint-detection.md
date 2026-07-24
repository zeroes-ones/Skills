# Under-Constraint Detection

## Overview

Under-constrained circuits are the #1 security vulnerability in ZKP systems. An under-constrained output signal allows a malicious prover to forge proofs for invalid statements.

## Detection Methods

### 1. Static Analysis

```bash
# circom-ecdsa: Check for under-constrained signals
circom circuit.circom --r1cs --sym -o build/
snarkjs r1cs info build/circuit.r1cs

# Look for:
# - Non-linear constraints: 0 (all linear = under-constrained risk)
# - Signals: 100, Constraints: 50 (signals > constraints = suspicious)
```

### 2. Manual Audit Checklist

For each `signal output`:
- [ ] Is it assigned with `<==` (constrained) or `<--` (unconstrained)?
- [ ] If `<--`, is there a corresponding `===` constraint?
- [ ] Can the prover set this output to any value and still satisfy all constraints?

For each `signal input` (public):
- [ ] Is there a range check (Num2Bits or LessThan)?
- [ ] Can overflow bypass protocol invariants?

### 3. Common Pitfalls

#### Pitfall 1: `<--` without `===`

```circom
// VULNERABLE
signal output result;
result <-- a + b;  // No constraint — prover chooses any value

// FIXED
result <== a + b;  // Constrained — prover bound to a + b
```

#### Pitfall 2: Conditional Constraint Gap

```circom
// VULNERABLE: Only constrains one branch
if (condition == 1) {
    output <== someValue;
}
// BUG: When condition != 1, output is unconstrained!

// FIXED: Always constrain output
signal case1;
signal case2;
case1 <== someValue;
case2 <== default;
output <== condition * case1 + (1 - condition) * case2;
```

#### Pitfall 3: Partial Constraint in Array

```circom
// VULNERABLE: Only first element constrained
for (var i = 0; i < n; i++) {
    if (i == 0) {
        arr[i] <== input;
    } else {
        arr[i] <-- input + i;  // BUG: Not constrained!
    }
}
```

#### Pitfall 4: Witness-Only Computation

```circom
// VULNERABLE: intermediate used only in <--, not in ===
signal intermediate;
intermediate <-- compute(a, b);
// intermediate not used anywhere! Constraint-free signal.

// FIXED
result <== compute(a, b);  // Direct constraint
```

### 4. Automated Detection Tools

| Tool | Method | Notes |
|------|--------|-------|
| `circom-ecdsa` | Static R1CS analysis | Flags unconstrained signals |
| `snarkjs r1cs info` | Constraint count audit | Check signal:constraint ratio |
| `ecne` | Under-constraint verifier | Formal verification approach |
| `picus` | Symbolic execution | Detects constraint gaps |
| Manual code review | Grep for `<--` | Most reliable, labor-intensive |

### 5. Red Flags During Code Review

- Any use of `<--` without immediate `===` on the same signal
- `signal output` that's never used in a `===` constraint
- Branches (if/else) where not all paths constrain outputs
- Array elements assigned but not all constrained
- Intermediate signals that are computed but never "consumed" by a constraint

## Case Studies

### zk-Bridge Exploit ($10M+)
- **Root cause:** Under-constrained balance output in withdrawal circuit
- **Mechanism:** Prover could inflate balanceAfter by choosing unconstrained witness value
- **Fix:** Replace `<--` with `<==` on output signals, add range checks

### Tornado Cash Governance Exploit
- **Root cause:** Missing Boolean constraint on proposal validity flag
- **Mechanism:** Attacker could set "valid" signal to 1 even for invalid proposals
- **Fix:** `valid * (valid - 1) === 0` and proper constraint chain

## Prevention Checklist

1. [ ] Every `signal output` is constrained via `<==` or `===`
2. [ ] Every use of `<--` is paired with a `===` on the same signal
3. [ ] All array elements are constrained (not just some)
4. [ ] All branches constrain outputs
5. [ ] Public inputs have range checks
6. [ ] Bit signals have Boolean constraints
7. [ ] `snarkjs r1cs info` shows expected constraint count
8. [ ] Circuit passes negative tests (invalid witnesses fail)
