# Stablecoin Risk Assessment

## Collateral Composition
| Stablecoin | Peg | Collateral | Over-Collateralized? | Auditable? |
|------------|-----|------------|---------------------|------------|
| USDC | USD | Cash + short-duration Treasuries | No (1:1) | Yes (Deloitte, monthly) |
| USDT | USD | Cash, T-bills, commercial paper, "other" | No (1:1, ~85% T-bills) | Yes (BDO, quarterly) |
| DAI | USD | ETH, USDC, RWA (multi-collateral) | Yes (~150%+) | Yes (on-chain) |
| FRAX | USD | USDC, sFRAX, AMO strategies | Partial (~85-100%) | Yes (on-chain) |
| USDe (Ethena) | USD | ETH + short ETH perps (delta-neutral) | Yes (via hedging) | Yes (on-chain) |

## Depeg History
| Stablecoin | Worst Depeg | Date | Cause | Recovery Time |
|------------|------------|------|-------|---------------|
| USDC | $0.87 | Mar 2023 | SVB collapse (8.25% of reserves trapped) | 3 days |
| USDT | $0.92 | May 2022 | LUNA/UST contagion fear | 2 days |
| USDT | $0.95 | Oct 2018 | Bitfinex banking concern | Weeks |
| DAI | $0.91 | Mar 2020 | Black Thursday liquidation cascade | 1 day |
| UST | $0.00 | May 2022 | Death spiral (algorithmic) | Never recovered |

## Redemption Mechanisms
- **Fiat-backed (USDC/USDT)**: KYC/AML gate, minimum amounts, T+1 to T+3 settlement
- **Crypto-overcollateralized (DAI)**: Permissionless mint/burn via Maker Vaults
- **Algorithmic (defunct category)**: Seigniorage mechanism → all failed (UST, IRON, BAC)

## Depeg Monitoring
- **Curve 3pool balance**: Imbalance signals depeg pressure
- **CEX order books**: Bid depth at $0.99 and below
- **Redemption arbitrage**: Premium/discount to NAV
- **On-chain redemptions**: Spike in redemption transactions = stress signal

## Provenance
[VERIFIED] Depeg data from on-chain records and market data
[AS OF 2026-01]

