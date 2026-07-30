# DeFi Yield Frameworks

## APR vs APY Conversion
```
APY = (1 + APR/n)^n - 1
```
Where n = compounding periods per year

| APR | Daily Compound APY | Continuous APY |
|-----|-------------------|----------------|
| 5% | 5.13% | 5.13% |
| 10% | 10.52% | 10.52% |
| 20% | 22.13% | 22.14% |
| 50% | 64.82% | 64.87% |

## LP Impermanent Loss
For Uniswap V2 constant-product AMM:
```
IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
```
| Price Change | IL |
|-------------|-----|
| 1.25x | -0.6% |
| 1.50x | -2.0% |
| 2.00x | -5.7% |
| 3.00x | -13.4% |
| 5.00x | -25.5% |
| 10.00x | -42.5% |

Uniswap V3 concentrated liquidity: IL is amplified within the price range.

## Lending Protocol Mechanics
| Protocol | Chain | Model | Key Feature |
|----------|-------|-------|-------------|
| AAVE V3 | Multi-chain | Pool-based | Isolation mode, e-mode, portal |
| Compound III | Ethereum | Single-asset pools | Governance-minimized |
| Morpho | Ethereum/Base | P2P matching | Better rates via peer-to-peer |
| Spark | Ethereum | Fork of AAVE V3 | MakerDAO ecosystem |

## Recursive Lending (Looping)
```
Max Position = Deposit * (1 / (1 - LTV)) ^ rounds
```
- ETH on AAVE: LTV = 80%, 4x looping → 1 + 0.8 + 0.64 + 0.51 = ~3x leverage
- Liquidation risk: price drop * leverage multiplier

## Yield Sources to Distrust
- Yields >30% APY that are "sustainable" → probably emissions-inflated
- "Real yield" claims without protocol revenue data → verify on Token Terminal/DefiLlama
- Wrapped/liquid staking tokens trading at premium → check redemption mechanism

## Provenance
[VERIFIED] AMM math from Uniswap whitepapers; protocol data from official docs
[AS OF 2026-01 — VERIFY LIVE YIELDS]

