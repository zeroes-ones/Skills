# MEV Mitigation Patterns

## Sandwich Attack Mitigation
```solidity
// Slippage protection
uint minOut = expectedOut * (10000 - maxSlippageBps) / 10000;
require(amountOut >= minOut, "slippage");
```

## Commit-Reveal
```solidity
// Phase 1: Commit (off-chain secret hash)
function commit(bytes32 hash) external { commits[msg.sender] = hash; }

// Phase 2: Reveal (after mempool window closes)
function reveal(uint value, bytes32 secret) external {
    require(keccak256(abi.encode(value, secret)) == commits[msg.sender]);
    // Execute with value
}
```

## Private Mempool / Flashbots
```solidity
// Send bundle to Flashbots relay instead of public mempool
// Users: use flashbots-protect RPC endpoint
// Protocol: use mev-share for orderflow auctions
```

## MEV Auction / PBS
- Proposer-Builder Separation (PBS) — protocol-level anti-MEV
- SUAVE — cross-chain MEV infrastructure
- Skip Protocol — Cosmos MEV recapture

## Protocol-Level Defenses
1. **TWAP oracles** — 30+ min to prevent single-block manipulation
2. **Batch auctions (CoWSwap)** — settle off-chain, no mempool exposure
3. **Max extractable value caps** — per-block profit limits
4. **Fair sequencing** — Chainlink FSS, Espresso sequencer

## Auditor's MEV Checklist
- [ ] Any single-transaction profit > 1 ETH? Risk of MEV extraction
- [ ] DEX slippage defaults: ≤ 0.5% for stable, ≤ 2% for volatile pairs
- [ ] Liquidation bonuses: 5-10% — if >15%, sandwich risk escalates
- [ ] Oracle freshness: < 1 block for critical pricing
