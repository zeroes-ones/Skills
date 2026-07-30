# On-Chain Data Guide

## Exchange Flows
- **Inflows**: Coins moving TO exchange wallets → potential selling pressure
- **Outflows**: Coins moving FROM exchange wallets → potential holding/accumulation
- **Net flow** = Outflows - Inflows (positive = accumulation signal)
- Data sources: Glassnode, CryptoQuant, CoinMetrics, Arkham

## Whale Wallet Tracking
| Entity Type | Known Labels | Data Provider |
|-------------|-------------|---------------|
| Exchange wallets | Binance, Coinbase, Kraken, etc. | Arkham, Nansen |
| Miner wallets | Foundry, AntPool, F2Pool | CoinMetrics |
| Institutional | MicroStrategy, Tesla, Grayscale | Arkham, public filings |
| DeFi protocols | Uniswap, AAVE, Maker | DeFiLlama |
| Market makers | Jump, Wintermute, GSR | Arkham (estimated) |

## TVL Interpretation
- **Total Value Locked**: Sum of all assets deposited in protocol smart contracts
- **Caution**: TVL can be inflated by:
  - Recursive/looping deposits (counted multiple times)
  - Double-counting (LP tokens deposited elsewhere)
  - Transient liquidity (flash-loan-inflated TVL)
- **Better metric**: Protocol revenue (30D annualized) / TVL = capital efficiency ratio

## Gas Economics
| Chain | Gas Token | Typical Cost | Congestion Driver |
|-------|-----------|-------------|-------------------|
| Ethereum L1 | ETH | $5-50 (transfer), $20-200 (DeFi) | NFT mints, airdrops |
| Arbitrum | ETH | $0.10-2 | High-activity dApps |
| Optimism | ETH | $0.10-2 | Similar to Arbitrum |
| Base | ETH | $0.05-1 | Consumer apps, memecoins |
| Solana | SOL | $0.0001-0.01 | Bot activity, airdrops |

## Mempool Monitoring
- **Public mempool**: Pending transactions visible before inclusion
- **Private mempool**: MEV-relay transactions (Flashbots) - hidden from sandwich bots
- **Gas auction**: Priority fee bidding during congestion

## Provenance
[VERIFIED] Data provider capabilities from official documentation
[AS OF 2026-01 — VERIFY LIVE DATA]

