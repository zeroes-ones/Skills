## 6. Protocol Design: UDP, Reliability, and Message Serialization

### Why UDP

TCP's head-of-line blocking is fatal for real-time games. A single lost packet at sequence 100 blocks delivery of packets 101-150 until 100 is retransmitted — even though packets 101-150 contain newer, more important data.

**The golden rule: Old state is worthless.** When a movement packet is lost, you don't want a retransmission of the old position — you want the newest position. UDP lets you make that choice per-packet.

### Custom Reliability Layer

Most games use a library that provides reliability channels over UDP:

| Library | Reliability Modes | NAT Traversal | Encryption | License |
|---|---|---|---|---|
| ENet | Reliable, unreliable sequenced | No | No | MIT |
| GameNetworkingSockets (Valve) | Reliable, unreliable, unreliable sequenced | Built-in (SDR) | Built-in | BSD |
| yojimbo (Glenn Fiedler) | Reliable ordered, unreliable | No | Optional | BSD |
| Photon Realtime | Managed service | Built-in | Built-in | Proprietary |
| LiteNetLib | Reliable ordered, unreliable, sequenced | No | Optional | MIT |

### Message Types and Channel Assignment

```
Message Type          │ Channel  │ Reliability        │ Ordering
──────────────────────┼──────────┼────────────────────┼───────────
Player input (move)   │ 0        │ Unreliable         │ Sequenced
Player input (fire)   │ 1        │ Reliable           │ Ordered
Server snapshot       │ 2        │ Unreliable         │ Sequenced
Chat message          │ 3        │ Reliable           │ Ordered
RPC / ability cast    │ 4        │ Reliable           │ Ordered
Voice (if not UDP)    │ 5        │ Unreliable         │ Unordered
Entity spawn/destroy  │ 6        │ Reliable           │ Ordered
```

**Critical:** Movement/aim on unreliable-sequenced channel (channel 0). If a movement packet is lost, the next one supersedes it. Never retransmit old positions.

### Serialization Strategy

Bit-pack positions to 16-bit integers (1mm precision, ±32m range), reducing from 12 bytes to 6. Delta-compress against last acknowledged snapshot — send only fields that changed. Track `last_ack_per_client` per entity per field. Target: 40 bytes per entity per tick, down from 200+ bytes naive.
