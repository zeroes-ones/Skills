# Client-Server Architecture for Games

> **Reference:** Game networking topology patterns, authority models, and deployment architectures for real-time multiplayer games.

## Architecture Models

### 1. Dedicated Server (Server-Authoritative)

The gold standard for competitive multiplayer. A headless game process running on infrastructure accepts client inputs, simulates, and broadcasts state.

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Client A │────▶│          │◀────│ Client C │
└──────────┘     │Dedicated │     └──────────┘
                 │  Server  │
┌──────────┐     │          │     ┌──────────┐
│ Client B │────▶│          │◀────│ Client D │
└──────────┘     └──────────┘     └──────────┘
```

**Key Properties:**
- Server owns all game state and physics
- Clients send input commands only
- Server broadcasts authoritative snapshots
- Anti-cheat effectiveness: HIGH
- Input latency: 1/2 RTT (server relays)
- Server costs: ~$0.05-$0.50/hour per instance

**When to use:** Competitive shooters, MOBAs, battle royales, fighting games, racing sims.

### 2. Client-Hosted (Listen Server)

One player acts as both client and server. Common in console and peer-to-peer-era games.

```
┌──────────────┐     ┌──────────┐
│ Client/Host  │────▶│ Client B │
│ (authority)  │◀────│          │
└──────────────┘     └──────────┘
       │
       ▼
┌──────────┐
│ Client C │
└──────────┘
```

**Key Properties:**
- Host player has zero-latency authority
- Host player can cheat trivially
- No server infrastructure costs
- Session dies if host disconnects (host migration required)
- Anti-cheat effectiveness: LOW

**When to use:** Co-op games, small-party games, games without ranked/competitive mode, console titles where dedicated servers are impractical.

### 3. Peer-to-Peer (Deterministic Lockstep)

All peers simulate the full game. Only inputs are exchanged — not state.

```
┌──────────┐     ┌──────────┐
│ Peer A   │◀───▶│ Peer B   │
└──────────┘     └──────────┘
      ▲               ▲
      │               │
      ▼               ▼
┌──────────┐     ┌──────────┐
│ Peer C   │◀───▶│ Peer D   │
└──────────┘     └──────────┘
```

**Key Properties:**
- Entirely deterministic simulation required (same binary, same seed)
- Bandwidth: minimal (inputs only, ~10-50 bytes/tick)
- Latency-bound by slowest peer
- All peers see all state — no fog-of-war privacy
- Anti-cheat: maphack trivial, but aimbot/speedhack impossible (simulation rejects)
- No server costs at all

**When to use:** RTS games (Age of Empires, StarCraft), turn-based strategy, games with small player counts and full information.

### 4. Peer-to-Peer with Relay

Hybrid: peers connect through a relay server that forwards packets without simulation.

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Peer A   │────▶│  Relay   │◀────│ Peer B   │
└──────────┘     │  Server  │     └──────────┘
                 └──────────┘
```

**When to use:** NAT traversal fallback, mobile games with unreliable connectivity, WebRTC-based games.

## Authority Models

### Server-Authoritative
- Server rejects invalid state (position, health, inventory changes)
- Client is a "dumb terminal" that renders server state
- Client prediction is cosmetic only — server always wins conflicts

### Server-Authoritative with Client Prediction
- Client predicts local player movement immediately
- Server validates and corrects on mismatch
- Smooth correction via interpolation, not snap

### Input-Authoritative (Shared)
- Server trusts inputs but validates them within constraints
- "Move at most X units per tick regardless of input"
- Catches speedhacks but allows subtle aim assist abuse

### Client-Authoritative (Anti-Pattern)
- Server relays whatever client says
- Trivial to cheat: modify memory, inject packets
- NEVER use for competitive or ranked games

## Network Topology Comparison

| Property | Dedicated Server | Client-Hosted | P2P Lockstep |
|---|---|---|---|
| Cheat Resistance | High | Low | Medium (maphack risk) |
| Server Cost | Per-instance | Zero | Zero |
| Latency Model | 1/2 RTT via server | Host 0ms, others 1 RTT | Slowest peer bound |
| Bandwidth | N × state size | N × state size | N × input size |
| Player Count | 100+ (with optimizations) | 4-16 (host CPU bound) | 2-8 (determinism bound) |
| Host Migration | N/A | Complex | Simple (any peer) |
| Replay/ Spectator | Easy | Medium | Hard (full state needed) |

## Tick Rate Selection

```
Game Genre          │ Tick Rate │ Bandwidth/Player │ Notes
────────────────────┼───────────┼──────────────────┼────────
FPS (competitive)   │ 60-128    │ 20-50 KB/s       │ CS2: 128t, Valorant: 128t
FPS (casual)        │ 20-30     │ 10-20 KB/s       │ Overwatch: 63t (was 20t)
MOBA                │ 30-60     │ 5-15 KB/s        │ League: 30t, Dota 2: 30t
Battle Royale       │ 20-30     │ 10-30 KB/s       │ High player count limits rate
Racing              │ 30-60     │ 10-25 KB/s       │ Physics precision matters
Fighting            │ 60        │ 5-10 KB/s        │ Rollback netcode
RTS                 │ 8-16      │ 1-5 KB/s         │ Lockstep, input-only
MMO                 │ 1-10      │ 2-8 KB/s         │ Interest-managed zones
```

## Server Fleet Architecture

### Regional Deployment
```
us-east (Virginia) ─── us-central (Dallas) ─── us-west (Oregon)
       │                       │                      │
       ▼                       ▼                      ▼
  [Game Servers]         [Game Servers]         [Game Servers]
       │                       │                      │
       └───────────────────────┼──────────────────────┘
                               │
                         [Matchmaker]
                               │
                         [Backend API]
```

### Containerization Strategy
- **Docker per game server:** Standard. One container = one match.
- **Orchestration:**
  - Agones (Kubernetes-native, Google-backed) — recommended
  - Custom K8s operator
  - AWS GameLift (managed)
  - Bare-metal for high-tick-rate (128+ tick) servers (avoid container overhead)
- **Warm pool:** Pre-allocate servers, swap in <100ms on match found.

### Scaling Rules
- **Scale-out trigger:** CPU >70%, or pending players > warm pool * max_players
- **Scale-in:** Drain mode, no new allocations, terminate after last match ends
- **Burst capacity:** 2x normal for launch day, 5x for free weekend events

## Protocol Stack

```
Application:    Game-specific messages (spawn, shoot, move, chat)
Transport:      ENET / GameNetworkingSockets / Raw UDP
Reliability:    Custom (sequenced reliable + unreliable channels)
Encryption:     DTLS 1.3 or custom (Steam Datagram Relay)
Compression:    Bit-packing + delta + dictionary
```

## References

- Source Engine Multiplayer Networking (Valve Developer Wiki)
- GDC 2018: "8 Frames in 16ms" — Overwatch netcode (Blizzard)
- Agones: github.com/googleforgames/agones
- GameNetworkingSockets: github.com/ValveSoftware/GameNetworkingSockets
- AWS GameLift documentation

## Quick Design Checklist

Before finalizing your game networking architecture, confirm:

- [ ] **Authority model chosen:** Server-authoritative, client-hosted, or P2P lockstep — with documented rationale.
- [ ] **Cheat vector analysis:** What can a malicious client do? Documented and mitigated at architecture level.
- [ ] **Tick rate selected** per game genre with bandwidth budget calculated.
- [ ] **Host migration plan** if using listen server — documented state transfer and leader election.
- [ ] **Protocol stack defined:** Transport, reliability layer, serialization, and encryption.
- [ ] **Regional deployment plan:** Target regions mapped to cloud provider availability zones.
- [ ] **Containerization strategy:** Agones, GameLift, or bare metal — with scaling plan.
- [ ] **Observability:** Metrics, logging, and tracing integrated from server binary to orchestration layer.
