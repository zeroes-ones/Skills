# Bridge & L2 Guide

## Bridge Security Models
| Bridge | Type | Security Model | Trust Assumptions |
|--------|------|---------------|-------------------|
| Native Rollup Bridge (Arbitrum, OP) | Canonical | L1 security (optimistic/zk proofs) | 7-day challenge period (optimistic) |
| LayerZero | Messaging | Oracle + Relayer (2-of-2) | Honest oracle + relayer |
| Wormhole | Messaging | Guardian network (19 validators) | 13/19 honest guardians |
| Across | Intent-based | Relayer competition | 1 honest relayer + UMA optimistic oracle |
| Stargate | Liquidity | Unified liquidity pools | Pool solvency |
| Hop Protocol | Liquidity | Bonded validators | Honest majority of bonded validators |

## Bridge Security Incidents
| Bridge | Loss | Year | Attack Vector |
|--------|------|------|--------------|
| Ronin | $624M | 2022 | Compromised validator keys (5/9) |
| Wormhole | $326M | 2022 | Smart contract exploit (recovered) |
| Nomad | $190M | 2022 | Validation logic bug |
| Multichain | $130M | 2023 | Insider/CEO key compromise |

## Bridge Cost & Time
| Bridge | ETH→Arbitrum | Arbitrum→ETH | Security |
|--------|-------------|-------------|----------|
| Native Arbitrum | ~10 min | 7 days (challenge) | Highest (L1 security) |
| Across | ~2 min | ~2 min | High (UMA optimistic oracle) |
| Stargate | ~5 min | ~5 min | Medium (liquidity pool) |
| Hop | ~15 min | ~15 min | Medium (bonded validators) |

## L2 Finality Times
| L2 | Soft Confirmation | Hard Finality | Withdrawal to L1 |
|----|------------------|---------------|-----------------|
| Arbitrum One | ~250ms | ~10 min | 7 days |
| Optimism | ~250ms | ~2 min | 7 days |
| Base | ~250ms | ~2 min | 7 days |
| zkSync Era | ~250ms | ~24 hours (proof generation) | ~24 hours |
| StarkNet | ~250ms | ~6 hours | ~6 hours |

## Bridge Strategy
- **< $1K**: Fast bridges fine (Across, Stargate)
- **$1K-$100K**: Native bridges preferred; split across time windows
- **> $100K**: Native bridges only; consider splitting across multiple bridges
- **Always**: Check bridge status page and recent incident history before large transfers

## Provenance
[VERIFIED] Bridge specs from official documentation; incident data from Rekt Leaderboard
[AS OF 2026-01]

