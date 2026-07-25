## 5. Core Architecture Models

The three fundamental multiplayer topologies, each with distinct tradeoffs in cheat resistance, cost, latency, and complexity.

### Server-Authoritative (Dedicated Server)

The industry standard for competitive multiplayer. A headless game process runs on cloud infrastructure, accepting client inputs, simulating game state, and broadcasting authoritative snapshots.

**Reference:** [client-server-architecture-games.md](references/client-server-architecture-games.md)

**Key equation — Per-player bandwidth:**
```
BW_per_player = (entities_relevant × state_size × tick_rate) + overhead
             = (15 × 40 bytes × 60 Hz) + 200 bytes/s
             = 36,200 bytes/s ≈ 36 KB/s
```

**When to use:** Competitive shooters, MOBAs, battle royales, racing sims, any game with ranked mode.

### Client-Hosted (Listen Server)

One player's machine is both client and authority. Simplest to implement, hardest to secure.

**When to use:** Co-op only, small-party games without competitive mode. Never for PvP with stakes.

### Peer-to-Peer Lockstep

All peers simulate the complete game state deterministically. Only inputs are exchanged.

**When to use:** RTS games, turn-based strategy, games where full information is acceptable.

### Protocol Stack Layers

Every game networking implementation needs these layers:

```
Layer 5: Game Logic Messages      — spawn, shoot, move, ability, chat
Layer 4: Serialization            — bit-packing, compression, integer quantization
Layer 3: Reliability & Ordering   — sequenced reliable/unreliable channels
Layer 2: Connection Management    — handshake, keepalive, timeout, reconnection
Layer 1: Transport                — UDP sockets (or WebRTC DataChannel for browser)
```
