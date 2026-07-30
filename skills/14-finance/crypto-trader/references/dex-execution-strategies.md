# DEX Execution Strategies

## AMM Math
### Constant Product (Uniswap V2)
```
x * y = k
Price = y / x
Price Impact = Δx / (x + Δx)  (approximate for small trades)
```

### Concentrated Liquidity (Uniswap V3)
Liquidity provided within price ranges [P_a, P_b]
Higher capital efficiency but amplified IL within range

## DEX Aggregator Comparison
| Aggregator | MEV Protection | Gas Optimization | Cross-Chain? |
|------------|---------------|-----------------|--------------|
| 1inch | Partial (Fusion mode) | Yes | Multi-chain |
| Matcha (0x) | Via 0x protocol | Yes | Multi-chain |
| CowSwap | Full (batch auctions) | Yes (gasless orders) | Yes (via bridges) |
| Paraswap | Partial | Yes | Multi-chain |
| Odos | No | Yes (path optimization) | Multi-chain |

## MEV Protection Strategies
1. **Flashbots Protect**: Send tx to private relay, bypass public mempool
2. **CowSwap**: Batch auction — no mempool, no frontrunning
3. **Limit orders vs market orders**: Limit orders = passive, less MEV-vulnerable
4. **TWAP execution**: Split large order over time → reduce footprint
5. **Dark pools**: Request-for-quote systems (Hashflow, AirSwap)

## Slippage Tolerance Guidelines
| Asset Type | Standard Slippage | Volatile Periods |
|------------|------------------|-----------------|
| Stablecoin pairs | 0.1% | 0.3% |
| ETH, BTC | 0.5% | 1-2% |
| Major DeFi tokens | 1% | 2-3% |
| Mid-cap tokens | 2-3% | 5%+ |
| Low-cap/memecoins | 5-10% | 15%+ |

## Provenance
[VERIFIED] AMM math from Uniswap whitepapers; aggregator data from project docs
[AS OF 2026-01]

