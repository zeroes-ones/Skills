# Upgradeable Contract Audit Checklist

## Proxy Patterns
| Pattern | Storage Risk | Initialization Risk | Upgrade Gate |
|---------|-------------|--------------------|--------------|
| UUPS | Low (impl stores) | Initialize in same tx | onlyOwner on _authorizeUpgrade |
| Transparent | Admin/User separation | Same as UUPS | Proxy admin contract |
| Diamond (EIP-2535) | Facet selector clash | DiamondCut must be audited | Multi-sig preferred |
| Beacon | Shared impl risk | Factory must enforce init | Beacon owner |

## Critical Checks
1. [ ] Storage layout: v1 vs v2 — no variable insertion before existing slots
2. [ ] `__gap` array correctly sized (uint256[50] default)
3. [ ] No `selfdestruct` in any implementation contract
4. [ ] No `delegatecall` to user-controlled addresses from implementation
5. [ ] `initialize()` has `initializer` modifier — cannot be called twice
6. [ ] Proxy admin is multi-sig or DAO — not single EOA
7. [ ] Implementation contract does NOT use constructor for state
8. [ ] Upgrade timelock enforced (≥48h for >$10M TVL)
9. [ ] Upgrade event emitted with old/new implementation addresses
10. [ ] Storage gap verification: `forge inspect MyContract storage --pretty`

## Metamorphic Contract Attack
CREATE2 + SELFDESTRUCT allows redeploying different code at same address.
- **Mitigation**: `initializable` with version tracking
- **Detection**: Flag any SELFDESTRUCT in upgradeable contracts
