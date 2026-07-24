# DeFi Attack Surfaces

## Lending Protocols
- **Oracle manipulation**: TWAP < 30min → flash loan distorts price → false liquidation
- **Bad debt accumulation**: Unchecked collateral ratios → protocol insolvency
- **Interest rate manipulation**: Low-liquidity pools with manipulable utilization curves
- **Liquidation griefing**: Gas griefing prevents timely liquidation

## AMM / DEX
- **Sandwich attacks**: Frontrun user tx → move price → backrun for profit
- **Impermanent loss exploitation**: Manipulated fee structures
- **Pool imbalance attacks**: Flash loan to unbalance pool → exploit pricing

## Bridges
- **Validator takeover**: Small validator set (< 10) → collusion risk
- **Message replay**: Missing nonce/timestamp → cross-chain replay
- **False deposit events**: Insecure event verification → mint unbacked tokens
- **Upgrade key compromise**: Bridge admin key = $100M+ attack surface

## Yield Aggregators
- **Strategy migration risk**: Vault strategy upgrade can drain all funds
- **Harvest timing manipulation**: MEV on harvest functions
- **Fee-on-transfer tokens**: Accounting mismatch on fee-bearing tokens

## Staking / LSD
- **Slashing conditions exploit**: Trigger validator slashing for profit
- **Withdrawal credential manipulation**: BLS key substitution in withdrawal address
- **Exchange rate manipulation**: First depositor inflation attack (donate 1 wei, profit)
