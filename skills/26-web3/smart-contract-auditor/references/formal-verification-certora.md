# Certora Formal Verification

## CVL Invariant Specification
```cvl
// Universal invariant: total collateral >= total debt
invariant collateralGtDebt()
    totalCollateral() >= totalDebt();

// Rule: deposit increases user balance by exact amount
rule depositIncreasesBalance(uint256 amount) {
    env e;
    requireInvariant collateralGtDebt();
    uint256 pre = balanceOf(e.msg.sender);
    deposit(e, amount);
    uint256 post = balanceOf(e.msg.sender);
    assert post == pre + amount, "deposit did not increase balance";
}
```

## Configuration (certora.conf)
```json
{
  "files": ["src/Protocol.sol"],
  "verify": "Protocol:certora/spec.spec",
  "solc": "solc8.19",
  "rule_sanity": "basic",
  "optimistic_loop": true
}
```

## Key Patterns
- **Parametric rules:** Verify property holds for ALL possible inputs
- **Ghost variables:** Track abstract state (totalCollateral, totalDebt)
- **Invariant strengthening:** Add invariants that make other rules provable
- **Preserved blocks:** Properties that must hold before AND after operations

## When to Use Certora
- Bridge protocols (>$100M TVL) — mandatory
- Lending protocols with complex liquidation — strongly recommended
- AMM forks with custom curves — verify curve properties
- Any protocol with >3 interacting contracts — reduces composition risk
