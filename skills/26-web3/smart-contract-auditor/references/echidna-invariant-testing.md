# Echidna Invariant Testing

## Core Pattern
```solidity
// Property: Total supply always equals sum of all balances
function echidna_totalSupply_equals_sum() public view returns (bool) {
    return token.totalSupply() == sumAllBalances();
}

// Property: No user can withdraw more than deposited
function echidna_no_overdraw() public returns (bool) {
    uint pre = token.balanceOf(address(this));
    // ... attempt withdrawal
    return token.balanceOf(address(this)) <= pre;
}
```

## Invariant Categories
1. **Token invariants:** supply = Σ balances, no double-spend
2. **Lending invariants:** collateral > debt, healthy factor > 1
3. **AMM invariants:** x*y = k (constant product), fee accounting
4. **Vault invariants:** shares * price = assets, no free shares
5. **Governance invariants:** quorum invariant, timelock enforcement

## Configuration (echidna.yaml)
```yaml
testMode: assertion
corpusDir: corpus
testLimit: 100000
shrinkLimit: 5000
seqLen: 100
sender: ["0x10000", "0x20000", "0x30000"]
```

## Running
```bash
echidna . --contract TestContract --config echidna.yaml
```

## CI Integration
```yaml
- name: Echidna Fuzzing
  run: echidna . --contract EchidnaTest --test-limit 50000 --corpus-dir corpus
```
