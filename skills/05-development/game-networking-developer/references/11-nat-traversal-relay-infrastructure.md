## 11. NAT Traversal & Relay Infrastructure

**Reference:** [nat-traversal-relay.md](references/nat-traversal-relay.md)

### The Connectivity Stack

```
ICE (Interactive Connectivity Establishment)
 ├── Host candidates (direct LAN IP)
 ├── Server Reflexive candidates (STUN-discovered public IP)
 └── Relay candidates (TURN relay)
```

### Success Rates

| Scenario | Direct P2P Success | Need TURN Relay |
|---|---|---|
| Both home NAT (non-symmetric) | ~82% | ~18% |
| One symmetric NAT | ~50% | ~50% |
| Both symmetric NAT | ~5% | ~95% |
| Corporate/enterprise | ~30% | ~70% |
| Carrier-grade NAT (CGNAT) | ~10% | ~90% |

### Relay Economics

TURN relay costs dominate for P2P games. Budget for 5-15% of peak concurrents on relay. Use geographic relay placement — latency through relay should be <30ms for in-region.

### SDR (Steam Datagram Relay)

For Steam games: Valve's SDR provides STUN + relay + DDoS protection + encryption as a managed service. Free for Steamworks developers. Strongly preferred over rolling your own STUN/TURN.
