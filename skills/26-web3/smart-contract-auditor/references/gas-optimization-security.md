# Gas Optimization vs Security Trade-offs

## When Optimization Creates Vulnerabilities

### 1. Unchecked Arithmetic (Solidity < 0.8.0)
```solidity
// ❌ Gas-efficient but vulnerable to overflow
unchecked { balance += amount; }

// ✅ Safe: Solidity 0.8.x native checks (only ~50 gas more)
balance += amount;
```

### 2. Packed Storage Collisions
```solidity
// ❌ Risk: Packed variables can corrupt adjacent storage
uint128 public a; // slot 0
uint128 public b; // slot 0 (same slot, adjacent)
// Upgrade adds: uint256 public c; // slot 1 — OK
// But adding uint128 public d; before c would corrupt b

// ✅ Safer: Explicit slot assignment (ERC-7201)
bytes32 constant STORAGE = keccak256("my.storage.v1");
```

### 3. Immutable Removal
Removing `immutable` for gas savings ($100/deployment) → storage variable writes cost 20K gas per SSTORE. Breaks deployment-time verification.

### 4. Assembly Optimizations
```solidity
// ❌ Inline assembly for gas savings
assembly {
    let result := sload(slot)
    sstore(slot, add(result, amount))
}

// ✅ Solidity — compiler optimizes as well
storageVar += amount;
```
**Risk**: Assembly bypasses Solidity security checks, storage packing, and compiler guards.

### 5. Skipping Events
Removing events saves ~375 gas but eliminates:
- Off-chain monitoring for exploits
- MEV detection
- Post-mortem analysis

**Rule**: Never remove events from value-transfer or state-change functions.

## Auditor's Gas vs Security Heuristics
| Optimization | Max Gas Saved | Security Risk | Verdict |
|-------------|---------------|---------------|---------|
| unchecked block | 50 gas/op | Integer overflow → funds loss | ❌ Never use without formal proof |
| Remove events | 375 gas | No monitoring → delayed detection | ❌ Never on critical paths |
| Assembly rewrite | 100-500 gas | Bypasses compiler checks | ⚠️ Only with extensive fuzzing |
| Remove modifier | 200-500 gas | Access control bypass risk | ❌ Never on auth checks |
| Uint size reduction | 5K gas (SSTORE) | Packing corruption on upgrade | ⚠️ OK with storage gap |
