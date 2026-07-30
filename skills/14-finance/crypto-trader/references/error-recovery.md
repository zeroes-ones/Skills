# Crypto Error Recovery

## Additional Error Patterns

### 1. Oracle Manipulation
**Symptom**: Liquidation triggered by anomalous price feed
**Root Cause**: DEX/CEX price used as oracle was manipulated (low-liquidity pair, flash loan attack)
**Fix**: Use time-weighted average price (TWAP) oracles. Check oracle source diversity. For DeFi, prefer Chainlink with multiple aggregators.
**Lesson**: The price that liquidates you might not be the "real" price. Oracle manipulation kills leveraged positions.

### 2. Governance Attack
**Symptom**: Protocol parameters changed overnight, causing position losses
**Root Cause**: Governance token concentrated → malicious proposal passed
**Fix**: Monitor governance proposals for protocols with significant TVL exposure. Exit positions before contentious governance votes.
**Lesson**: Protocol rules can change. Governance concentration = single point of failure.

### 3. Reentrancy / Flash Loan Exploit
**Symptom**: Protocol drained despite audits
**Root Cause**: Smart contract bug exploited via reentrancy or flash-loan-enabled manipulation
**Fix**: Diversify across protocols. Use protocols with circuit breakers and pause mechanisms. Monitor security discords for early warnings.
**Lesson**: Audits reduce probability of exploits but don't eliminate them. Assume every protocol can be exploited.

### 4. Exchange Freeze During Volatility
**Symptom**: Cannot close position during crash because exchange disabled trading
**Root Cause**: Exchanges halt trading during extreme volatility ("market circuit breakers" or less charitable: "we're insolvent")
**Fix**: Pre-position stop orders on multiple exchanges. Keep portion of positions on DEXs (permissionless, no circuit breakers). Diversify across venues.
**Lesson**: CEXs are centralized by definition. When you most need to trade, they may not let you.

## Provenance
[VERIFIED] Error patterns from documented crypto incidents
[AS OF 2026-01]

