# Additional Resources — defi-protocol-engineer

> Deep knowledge loaded on demand. Mechanism math, attack classes, and reference material.

## Mechanism Math Quick Reference

### Constant-Product AMM (x·y = k)
- Swap: `dx` in → `dy = y - (x·y)/(x + dx·(1-fee))`. Price impact grows with trade size relative to pool depth.
- LP value: concentrated liquidity (v3) expresses position as a price range; IL = divergence between holding and providing. `IL = 2·sqrt(price_ratio)/(1+price_ratio) - 1` at the extremes.
- Invariant to property-test: **k never decreases except by fees**; LP shares × price always reconcile to pool value.

### Lending (Aave-style)
- Health factor = `collateral·price·LTV / debt`. Below 1 → liquidatable.
- Liquidation: liquidator repays debt, receives collateral + bonus. Invariant: **no user's health factor can go below 1 without a liquidation being possible**; collateral cannot be withdrawn below the liquidation threshold.
- Oracle manipulation attack: attacker pumps collateral price → borrows to the max → price crashes → positions underwater before liquidations fire.

### Stable-swap (Curve-style)
- Invariant blends constant-sum (flat center) with constant-product (steep ends): `k = x + y - D` near 1:1 plus the product term. The peg holds because arbitrageurs profit from any deviation > trading costs.

## Attack Classes to Model and Test (checklist)

| Attack | Where it lives | Defense |
|--------|----------------|---------|
| Reentrancy | Withdrawal/claim paths | Checks-effects-interactions; guards; fuzz withdrawal sequences |
| Oracle manipulation | Any price-dependent action | TWAP/bounds; manipulation analysis; fallback |
| First-depositor / donation | Share-based vaults/accounting | Virtual shares or min-liquidity lock; precision tests |
| Precision/rounding drain | Fees, interest, shares | Round in protocol's favor; test the 1-wei edges |
| Governance capture | Parameter changes, upgrades | Timelock, pause, bounded changes, multi-sig |
| Flash-loan exploits | Any large-capital assumption | Model max leverage; invariant tests over flash-loan-style sequences |
| Economic extraction (no code bug) | Incentive design | Adversarial incentive modeling; scenario tests |
| Integration risk | Oracles, routers, rewarders, bridges | Each integration gets its own risk analysis |

## Historical Post-Mortem Study List

For deliberate practice, study these patterns (not as "current facts" — verify the details):
- Reentrancy drains (the classic 2016 pattern and its modern variants)
- Oracle manipulation incidents on lending and leveraged platforms
- The algorithmic-stablecoin death spiral (design-level lesson: model the confidence loop)
- First-depositor/share-inflation findings on vault-style protocols
- Governance/upgrade incidents (compromised control paths)

For each: state the invariant that failed, the attack that broke it, and the defense that would have held.

## Audit-Readiness Package Contents

- Mechanism spec (invariant in one sentence + math)
- Risk model (parameters, worst cases, residual DAO-accepted risks)
- Invariant property-test suite (runs in CI, blocks merges)
- Unit + fork tests (real mainnet state scenarios: crash, mass withdrawal, oracle delay)
- Architecture doc + known-limitations section
- Threat list (failure modes × trigger × impact × mitigation)

## Reference Material

- Uniswap v2/v3 whitepapers — constant product, concentrated liquidity
- Curve whitepaper — stable-swap invariant
- Aave docs — LTV, health factor, liquidation engine
- ERC-4626 tokenized vault standard — share accounting conventions and rounding guidance
- OpenZeppelin audits + Solidity security patterns — reentrancy, oracle, precision guidance
