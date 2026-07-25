---
name: game-networking-developer
description: Game networking engineering covering client-server architecture, peer-to-peer, prediction and reconciliation, lag compensation, dedicated server infrastructure, and multiplayer synchronization. Use when implementing multiplayer game networking, designing client-server protocols, implementing server-authoritative game logic, building matchmaking systems, optimizing network bandwidth for real-time games, or debugging desync and rubber-banding issues. Handles UDP vs TCP decisions, snapshot interpolation, delta compression, interest management, NAT traversal, and relay server architecture. Do NOT use for REST API development, web backend development, or non-real-time networking.
author: Sandeep Kumar Penchala
license: MIT
version: 1.0.0
updated: 2026-07-24
tags: [game-networking, multiplayer, client-server, udp, prediction, synchronization, netcode]
token_budget: 4500
chain:
  consumes_from:
    - game-developer
    - gameplay-programmer
    - game-engine-architect
    - backend-developer
    - networking-engineer
  feeds_into:
    - game-developer
    - qa-engineer
    - performance-engineer
    - devops-engineer
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Game Networking Developer — Multiplayer Netcode & Real-Time Synchronization

Game networking is the difference between a game feeling crisp at 200ms ping and unplayable at 30ms. This skill covers the full stack: transport protocols, client-server architecture, prediction & reconciliation, lag compensation, snapshot interpolation, NAT traversal, matchmaking, and dedicated server operations. Every decision made here directly impacts player retention — bad netcode is the #2 reason players quit multiplayer games (after cheating).

## Route the Request

### Auto-Route (No User Input Required)
| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.cs", "NetworkManager|UNetTransport|NetcodeForGameObjects")` OR `file_contains("*.cpp", "UNetDriver|ReplicationGraph|FNetworkPrediction")` | This is your skill. Jump to **Decision Trees** for architecture selection. |
| A2 | `file_contains("*.cs", "ClientRpc|ServerRpc|NetworkVariable")` OR `file_contains("*.cpp", "UFUNCTION.*Server|UFUNCTION.*Client|DOREPLIFETIME")` | Working on RPC/replication. Jump to **Core Workflow — Phase 4 (Prediction & Reconciliation)**. |
| A3 | User mentions "lag", "rubber-banding", "desync", "jitter", "packet loss" | Debug session. Jump to **Decision Trees > Debug & Diagnostics**. |
| A4 | User mentions "matchmaking", "lobby", "party system" | Matchmaking architecture. Jump to **Core Workflow — Phase 3 (Matchmaking)**. |
| A5 | User mentions "dedicated server", "headless", "server build" | Server operations. Jump to **Core Workflow — Phase 5 (Dedicated Servers)**. |
| A6 | User mentions "anti-cheat", "server authority", "validation" | Security. Jump to **Core Workflow — Phase 6 (Anti-Cheat)**. |
| A7 | User mentions "NAT", "STUN", "TURN", "relay", "hole punching" | NAT traversal. Jump to **Decision Trees > NAT Traversal Strategy**. |

## The Expert's Mindset

You are a senior netcode engineer who has shipped multiplayer games serving 100K+ concurrent users. You've debugged desync at 3 AM before launch, rewritten prediction algorithms during beta, and optimized bandwidth to fit within mobile carrier limits. You know that every millisecond of added latency costs player retention — a 10ms increase in perceived lag reduces session time by 7%. You default to server authority for competitive integrity, client prediction for responsiveness, and bandwidth budgets measured in *bytes per second per player*, not megabytes. You've memorized Glenn Fiedler's "Gaffer On Games" articles and can recite the differences between snapshot interpolation, state synchronization, and deterministic lockstep from memory.

## Operating at Different Levels

| Level | Scope | Deliverable |
|-------|-------|-------------|
| **L2 (Practitioner)** | Single feature networking (e.g., replicating player health, implementing a ClientRPC) | Working RPC with bandwidth profiling. Prediction error < 50ms for this feature |
| **L3 (Senior)** | Full multiplayer mode (e.g., 64-player battle royale netcode) | Complete replication architecture. Interest management. Bandwidth budget per player < 8KB/s |
| **L4 (Staff)** | Cross-project networking standards, custom transport layer, backend service mesh for game servers | Netcode SDK. Automated load testing framework. Latency budgets across all game systems |
| **L5 (Principal)** | Novel networking paradigms (e.g., deterministic rollback for fighting games, mesh networking for AR), industry contributions | Published papers or GDC talks. Reference implementations that shift industry practice |

## When to Use

- Implementing multiplayer game networking: client-server, peer-to-peer, or hybrid architectures
- Designing client-side prediction with server reconciliation for responsive gameplay
- Debugging desync, rubber-banding, jitter, or packet loss issues in production
- Building matchmaking systems, lobby services, and party management
- Optimizing bandwidth for real-time games (FPS, MOBA, battle royale, fighting games)
- Implementing lag compensation (backwards reconciliation, hit registration)
- Setting up dedicated server infrastructure with auto-scaling for game sessions
- Designing NAT traversal with STUN/TURN/relay for peer-to-peer games
- Implementing anti-cheat at the network layer (server validation, replay verification)

## Core Workflow

Game networking follows a 6-phase pipeline. Each phase builds on the previous — skipping phases guarantees desync in production.

### Phase 1 (~15 min): Transport & Protocol Selection
Choose UDP for real-time gameplay (FPS, fighting, racing), TCP for turn-based or slow-state games. Implement reliability layers: reliable-ordered for critical events (scoring, kills), unreliable for transient state (positions every frame < 50ms). Use flatbuffers or bit-packed custom serialization — never JSON/XML for runtime gameplay state.

### Phase 2 (~20 min): Server-Authoritative Architecture
Server is the source of truth for all gameplay state. Clients send inputs only. Server processes inputs, updates simulation, sends snapshots. Never trust client-reported state (position, health, inventory). Implement server-side validation for every client action.

### Phase 3 (~20 min): Client-Side Prediction & Reconciliation
Predict local player movement immediately (don't wait for server ack). Store unacknowledged inputs in a circular buffer. When server state arrives, reconcile: re-simulate from last acknowledged state with stored inputs. If prediction error > threshold, snap to server position (with interpolation to prevent popping).

### Phase 4 (~25 min): Lag Compensation & Hit Registration
For shooter hit detection: rewind server state to what the shooter saw at their ping time. Use a ring buffer of recent world states (configurable history, typically 500ms). Validate shot against rewound state. Apply damage to current state. Handle high-ping edge cases: cap compensation window at 200ms.

### Phase 5 (~20 min): Interest Management & Bandwidth
Only send entities relevant to each player. Spatial: grid-based or distance-based relevance. Prioritize: critical entities at high frequency, distant at low frequency. Budget: aim for < 8KB/s per player for competitive games. Implement delta compression — only send changed properties.

### Phase 6 (~25 min): Testing, Profiling & Anti-Cheat
Simulate network conditions: 0-300ms latency, 0-10% packet loss, jitter 0-50ms. Profile bandwidth per-player with real gameplay sessions. Implement server-side replay validation. Detect impossible actions (speed hacks, teleport hacks) via server-side simulation comparison.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When |
|---|---|---|
| `gameplay-programmer` | Gameplay systems needing replication (combat, movement, inventory) | Before designing replication for specific gameplay features |
| `backend-developer` | Matchmaking services, player data APIs, backend infrastructure | Before designing matchmaking and lobby integration |
| `system-architect` | Overall system architecture, cloud provider, scaling requirements | Before dedicated server architecture decisions |

| Downstream Skill | What You Provide | When |
|---|---|---|
| `qa-engineer` | Network simulation test scenarios, latency budgets, bandwidth baselines | After netcode implementation for QA test planning |
| `performance-engineer` | Bandwidth profiles, CPU budgets for replication, memory for snapshot buffers | After profiling pass for performance optimization |
| `security-reviewer` | Server-authoritative validation points, anti-cheat architecture | After anti-cheat design for security audit |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "game-networking-developer",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

> Players on 100ms connections report the game "feels local" — client prediction hides latency, server reconciliation is imperceptible. Bandwidth per player stays under 8KB/s even in 64-player matches. Zero desync bugs in the last 100K game sessions. Server CPU for netcode stays under 15% per core at full load. Matchmaking finds games in under 30 seconds at any hour. Dedicated servers auto-scale from 0 to 1000 instances in under 2 minutes. Anti-cheat catches 99% of speed hacks and teleport hacks before they affect other players.

## Deliberate Practice

| Exercise | Skill Targeted | Success Metric |
|----------|---------------|----------------|
| Implement client prediction for a simple 2D platformer in 4 hours | Prediction mechanics, input buffering, reconciliation | Player at 150ms ping reports no perceived lag; prediction error < 20ms average |
| Build a server-authoritative FPS prototype with lag compensation in 1 week | Server authority, hit registration, snapshot management | Headshot hitreg works at 200ms ping; server processes 64 players at 60Hz tick rate |
| Optimize bandwidth from 20KB/s to 5KB/s per player for a battle royale | Delta compression, interest management, priority scheduling | 64 players in relevance range; no visual pop-in; < 5KB/s per player measured |
| Debug and fix 10 synthetic desync scenarios within 2 hours | Debugging methodology, rollback verification, state comparison | All 10 scenarios resolved with root cause identified; no regression introduced |
| Implement NAT traversal with relay fallback for a peer-to-peer game | STUN/TURN, ICE, hole punching, relay server selection | 95% of player pairs connect via direct peer; relay latency < 50ms additional |

## Proactive Triggers

| Trigger | Action | Rationale |
|---|---|---|
| `[Command]` RPC without server-side validation | Block merge — every `[Command]` must validate caller authority and input bounds | Client-to-server RPCs without validation is the #1 exploit vector in Unity netcode games — enables god mode, item duplication, teleport hacks |
| Tick rate changed without bandwidth re-budgeting | Flag — doubling tick rate doubles snapshot bandwidth; recalculate per-player budget | 60Hz vs 30Hz doubles network traffic — most teams don't realize their 30Hz bandwidth budget is blown after "just bumping tick rate" |
| New gameplay system added without replication plan | Require replication design doc before implementation | Gameplay programmers often design systems as single-player, then bolt on replication — guaranteed desync. Every gameplay feature needs a replication plan before a single line of netcode |
| Interpolation buffer > 100ms in production config | Warn — > 100ms buffer means players perceive 100ms+ of artificial delay on top of network latency | Interpolation adds perceived lag equal to buffer size. Competitive games should target 50ms or less. 100ms+ feels sluggish |
| Single point of failure in dedicated server region | Escalate — if one region's server fleet goes down, players must be redirected within 5 seconds | Regional outages during peak hours (launch day) cause review bombing. Automated failover is not optional for production multiplayer |


## Ground Rules — Read Before Anything Else

### Non-Negotiable Rules

**Rule 1: NEVER trust the client — client-side hit detection without server validation is the #1 cause of cheating, costing $100K+ in lost players.** The server is the sole authority for hit registration, damage application, inventory changes, score updates, and any state that affects competitive fairness. Client input is a *suggestion* the server validates.

**Rule 2: UDP is the default transport for real-time gameplay. TCP is only acceptable for turn-based, chat, or matchmaking.** TCP head-of-line blocking destroys real-time game feel. A single lost packet stops all subsequent packets from being delivered until retransmission completes. UDP lets you decide what to resend and what to discard.

**Rule 3: Every server-authoritative game MUST implement client-side prediction with server reconciliation.** Players perceive latency as lag. Prediction gives instant feedback; reconciliation corrects drift. Without both, your game feels 100-200ms slower than it actually is.

**Rule 4: Lag compensation is mandatory for any game with hit registration.** Unless you want players to "lead" their shots based on ping — a skill no one enjoys learning — you must rewind server state to what the shooter saw. Cap compensation at 150-200ms to limit peeker's advantage.

**Rule 5: Measure before optimizing.** Profile tick duration, packet loss, and bandwidth per-player before implementing delta compression or interest management. Premature optimization of netcode creates bugs that are harder to debug than bandwidth waste.

**Rule 6: Determinism is a requirement for lockstep, not a luxury.** If you choose P2P lockstep, floating-point operations MUST produce identical results across all platforms and compilers. One divergent `sin()` call desyncs the entire simulation. Use fixed-point or deterministic float libraries.

**Rule 7: Plan for host migration from day one if using client-hosted architecture.** Players WILL disconnect. A game that ends because the host left is a game players stop launching. Design your state transfer and leader election before writing game logic.


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## Decision Trees

### Decision Tree 1: Server-Authoritative vs P2P vs Client-Hosted

```
Is this a competitive/ranked game?
├── YES → Server-authoritative (dedicated server)
│         └── Sub-decision: Player count?
│             ├── <12 players → Single server instance per match
│             ├── 12-64 → Single instance with interest management
│             └── >64 → Spatial partitioning or MMO-style zoning
│
└── NO → Is cheating tolerance high AND player count <= 8?
    ├── YES → Consider P2P lockstep (RTS, turn-based, co-op)
    │         ├── Needs full determinism? → Lockstep
    │         └── Can tolerate some drift? → P2P with host authority
    │
    └── NO → Client-hosted (listen server)
              └── MUST implement host migration
```

### Decision Tree 2: UDP vs TCP vs WebRTC

```
Is this real-time gameplay (FPS, racing, fighting, action)?
├── YES → UDP
│         └── Sub-decision: Need reliability for some messages?
│             ├── YES → Custom reliable layer over UDP (ENet, GNS)
│             └── NO → Raw UDP with sequencing
│
├── Is this turn-based, chat, or lobby system?
│   └── YES → TCP or WebSocket
│         └── Sub-decision: Browser-based?
│             ├── YES → WebSocket
│             └── NO → TCP
│
└── Is this browser-based real-time?
    └── YES → WebRTC (DataChannel, unordered/unreliable mode)
              └── Fallback: WebSocket with aggressive interpolation
```

### Decision Tree 3: Rollback vs Delay-Based Netcode

```
Game genre?
├── Fighting game → Rollback (mandatory)
│   └── Frame window: 2-8 frames rollback, 0-3 frame input delay
│
├── Fast FPS (arena shooter, tactical) → Can use either
│   ├── Server-authoritative? → Delay-based with prediction (industry standard)
│   └── P2P? → Rollback (less common, requires determinism)
│
├── MOBA, Battle Royale → Delay-based (rollback too expensive with 10+ entities)
│
└── Racing → Delay-based with aggressive prediction
```

### Decision Tree 4: Dedicated Server vs Listen Server

```
Budget for server infrastructure?
├── ZERO → Listen server
│         └── MANDATORY: host migration, anti-cheat for host
│
├── LIMITED ($500-$5K/month) → Hybrid
│   ├── Competitive → Dedicated (small fleet)
│   └── Casual → Listen server
│
└── ADEQUATE ($10K+/month) → Full dedicated fleet
    └── Sub-decision: Build vs buy orchestration?
        ├── Custom requirements → Agones on Kubernetes
        └── Standard needs, AWS shop → GameLift
```

### Decision Tree 5: Snapshot Interpolation vs Extrapolation

```
What to render between server snapshots?
├── Local player → Extrapolate (prediction)
│   └── Reconcile on server correction
│
├── Remote players:
│   ├── Snapshot buffer healthy (>2 snapshots ahead)?
│   │   └── Interpolate between last two snapshots
│   │       └── Render delay: 2 × (1/tick_rate)
│   │
│   └── Snapshot buffer starved?
│       └── Extrapolate from last known velocity (capped at 200ms)
│           └── Blend back to interpolation when snapshot arrives
│
└── Critical targets (crosshair)?
    └── Use latest snapshot directly (no interpolation delay)
```

### Decision Tree 6: Lockstep vs State Sync

```
Game has <100 entities AND full determinism possible?
├── YES → Lockstep
│   └── Bandwidth: ~1-5 KB/s regardless of entity count
│
├── NO → State sync (server sends entity states)
│   └── Sub-decision: Full state or delta?
│       ├── New connections or periodic → Full state (keyframe)
│       └── Regular updates → Delta (changed fields only)
│
└── Hybrid → State sync for most entities, lockstep for critical physics
```

## 3. Gotchas

### Gotcha 1: Client-side authority for game state ($100K+)

Assigning authority for game-critical state (health, position, score) to the client without server validation. Memory editors and packet injectors can modify any client-side value. Within 48 hours of launch, cheat tools will exist. **Fix:** Server validates every state mutation. Client sends *intent* ("I want to move here"), server sends *results* ("You are now here"). Never: client says "I have 100 HP" and server accepts it.

### Gotcha 2: TCP for real-time game communication ($75K+)

Using TCP for gameplay packets. On packet loss, TCP stalls ALL subsequent data until retransmission — the dreaded "head-of-line blocking." At 1% packet loss (common on WiFi), TCP throughput drops 50-80%. Players experience sudden freezes followed by teleportation. **Fix:** Use UDP with a custom reliability layer where needed. Send movement/aim as unreliable-sequenced (drop old, use newest). Send events (fire, reload) as reliable-ordered.

### Gotcha 3: Interpolation delay set to zero ($50K+)

Attempting to render entities at the exact moment a snapshot arrives, with no buffer against jitter. Network jitter of ±10ms at 60 tick produces visible stuttering. Players perceive "laggy servers" even when ping is low. **Fix:** Always interpolate with a buffer of at least 2× the expected tick interval (33ms at 60Hz, 16ms at 128Hz). Smooth jitter with an adaptive buffer that grows during jitter spikes.

### Gotcha 4: No server reconciliation after prediction ($60K+)

Implementing client-side prediction without server reconciliation. The predicted position drifts from the authoritative position by 1-5cm per tick due to floating-point differences, physics divergence, and other players' interference. After 60 ticks (1 second at 60Hz), the player is 60-300cm from where the server says they are. Next server snapshot snaps them back — "rubber banding." **Fix:** Store pending input commands. On server snapshot, remove acknowledged commands, re-apply unacknowledged commands from the server position.

### Gotcha 5: Rewinding all entities for lag compensation on every shot ($40K+ infrastructure)

Naively deep-copying all entity states for lag compensation on every hitscan shot. With 64 players, 100 physics objects, and 10 shots/second per player, this is 64,000 deep copies/second. **Fix:** Use a fixed-size ring buffer of entity snapshots per tick. On shot processing, rewind only entities along the raycast path. Use copy-on-write for static geometry. Budget ~0.05ms per shot, not 2ms.

### Gotcha 6: Ignoring NAT traversal for P2P games ($30K+ support tickets)

Shipping a P2P game without STUN/TURN/ICE. 90% of home users are behind NAT. 8-15% have symmetric NAT that STUN cannot traverse. These players simply cannot connect. Support tickets pile up: "Can't join friend's game." **Fix:** Implement ICE with STUN server(s) and TURN relay fallback. Budget TURN bandwidth for 5-15% of peak concurrent players. Use WebRTC/DataChannel for browser games.

### Gotcha 7: No backfill for casual matchmaking ($25K+ player churn)

One player leaves a casual match, and the remaining 9-99 players suffer through an imbalanced game or disconnect. Without backfill, a single leaver cascades into the lobby emptying. **Fix:** Implement priority backfill queue. Relax skill constraints for backfill (shorter expected match duration makes skill less important). Target <10 second fill time.

## 4. Domain-Specific Anti-Patterns

| The temptation | Why it sounds right | Why it's wrong | What to do instead |
|---|---|---|---|
| "TCP is simpler, we'll just use that for everything" | One connection, automatic reliability, fewer lines of code | Head-of-line blocking destroys real-time feel at any packet loss. Games feel laggy on WiFi/LTE even at 30ms ping | UDP with sequenced channels. Reliable for events, unreliable-sequenced for movement/aim |
| "We don't need prediction, our game targets low ping only" | Simpler code, no reconciliation bugs, no rubber-banding | "Low ping" is relative. Even 20ms = 1 frame at 60fps. Perception of input lag starts at ~50ms round-trip | Always predict local player. Keep prediction simple — just movement. Omit for abilities if complex |
| "The client can handle hit detection, we'll add server validation later" | Faster to implement, feels instant, server code is simpler | "Later" never comes. Cheat tools ship in week one. Every kill by a cheater costs ~10 player-hours of engagement | Start with server-authoritative hit detection. Client shows blood/sparks predictively but server confirms damage |
| "We'll use the same tick rate for everything" | Simple to implement and reason about, uniform code path | 60-tick projectile updates waste bandwidth when 30-tick would suffice. 20-tick movement in a fighting game is unplayable. Different game aspects need different update frequencies | Variable update rate: position at 60Hz, inventory at 5Hz, chat at event-driven. Interest-manage per-entity |
| "P2P lockstep works for our fighting game, no need for rollback" | Deterministic, low bandwidth, no server costs | 100ms ping means 100ms input delay in lockstep. Fighting game inputs require sub-50ms response. Players across regions can't play each other | Implement GGPO-style rollback netcode. 0-frame input delay. ~3 frames rollback. Save/restore state every frame |
| "We'll just spin up EC2 instances manually for launch" | Quick to set up, familiar workflow, no K8s complexity | Manual scaling during launch spike = servers full → players can't play → launch day disaster. Player count oscillates 5-10x daily | Use Agones Fleet with buffer autoscaling or GameLift. Pre-warm capacity. Practice 5x scale-up drill before launch |

## 5. Core Architecture Models

The three fundamental multiplayer topologies, each with distinct tradeoffs in cheat resistance, cost, latency, and complexity.

### Server-Authoritative (Dedicated Server)

The industry standard for competitive multiplayer. A headless game process runs on cloud infrastructure, accepting client inputs, simulating game state, and broadcasting authoritative snapshots.

**Reference:** [client-server-architecture-games.md](client-server-architecture-games.md)

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

## 7. Client-Side Prediction & Server Reconciliation

**Reference:** [prediction-reconciliation-patterns.md](prediction-reconciliation-patterns.md)

### The Core Loop

```
Client sends input → applies locally (prediction) → stores command
Server receives input → validates → simulates → broadcasts authoritative state
Client receives snapshot → removes acknowledged commands → checks for error
  ├── Error < threshold: smooth interpolate toward server
  └── Error >= threshold: snap to server, re-apply unacked commands
```

### Prediction for Non-Local Entities

Don't predict remote players. Interpolate them from snapshots. The only entity you predict is the local player, because you have the input that drives it.

**Exception:** In fighting games with rollback, all entities are predicted because all inputs are deterministic.

### Reconciliation Thresholds

| Error Magnitude | Response | Visual Result |
|---|---|---|
| < 0.01m | Ignore | None — player won't notice |
| 0.01m - 0.1m | Smooth correct over ~100ms | Subtle, barely visible |
| > 0.1m | Snap to server, replay inputs | Visible micro-correction |
| > 2.0m | Teleport to server position | Rubber-banding — investigate cause |

## 8. Lag Compensation & Hit Registration

**Reference:** [lag-compensation-techniques.md](lag-compensation-techniques.md)

### The Rewind Algorithm

On receiving a fire command at server tick T, rewind all entities to where they were at the shooter's tick T_shooter:

```
1. Store current entity positions
2. Rewind all entities to T_shooter using history buffer
3. Raycast from shooter's eye position in aim direction
4. If hit → validate damage, apply at current tick
5. Restore entity positions
```

### Critical Parameters

| Parameter | Recommended Value | Rationale |
|---|---|---|
| Max rewind window | 200ms | Beyond this, positions too stale to be fair |
| History buffer duration | 1 second | Covers max ping + jitter buffer |
| Max compensated ping | 150ms | Reject shots from extreme high-ping players |
| Sub-tick precision | On | Eliminates tick-boundary artifacts |

### Hitscan vs Projectile

- **Hitscan:** Rewind once, raycast. Cost: O(entities_in_history).
- **Projectile:** Rewind at each timestep along projectile path. Cost: O(entities × flight_time/step).

## 9. Snapshot Interpolation & Jitter Management

**Reference:** [snapshot-interpolation.md](snapshot-interpolation.md)

### The Interpolation Buffer

Render remote entities with a deliberate delay to absorb jitter:

```
Render time = server_time - interpolation_delay
            = server_time - (2 × tick_interval)

Example: 60 tick, 16.67ms interval → 33ms render delay
```

### Jitter Buffer Adaptation

```cpp
target_delay = max(target_delay, measured_jitter * 2.0f);
target_delay = clamp(target_delay, 16ms, 150ms);
```

The buffer grows during jitter spikes (WiFi interference, mobile handoff) and slowly shrinks when the network stabilizes.

### Extrapolation Fallback

When snapshots run dry (packet loss):

1. Extrapolate from last known velocity (linear dead reckoning).
2. Cap extrapolation at **200ms maximum**.
3. On snapshot arrival, blend from extrapolated to interpolated over 100ms.
4. After **500ms with no snapshots**, freeze the entity (don't extrapolate into walls).

## 10. Interest Management & Bandwidth Optimization

**Reference:** [interest-management.md](interest-management.md)

### The Bandwidth Budget

```
Target: <50 KB/s per player (downstream)
         <10 KB/s per player (upstream)

Without interest management (100-player BR):
  = 100 entities × 40 bytes × 60 Hz = 240 KB/s — 5x over budget

With interest management:
  = 12 entities × 40 bytes × 60 Hz = 28.8 KB/s — within budget
```

### Priority Tiers

| Tier | Update Rate | Entities Included | Budget Share |
|---|---|---|---|
| Critical | Every tick | Crosshair target, local player | 40% |
| High | Every 2 ticks | Enemies <50m in frustum | 30% |
| Medium | Every 4 ticks | Enemies 50-150m, teammates | 20% |
| Low | Every 8 ticks | Distant entities | 8% |
| Awareness | Every 16 ticks | Minimap indicators, footsteps | 2% |

### Relevance Checks (ordered by cost)

1. **Distance** (cheapest) — cull beyond max relevance range
2. **View frustum** (cheap) — low priority for behind-player entities
3. **Occlusion/LoS** (expensive) — only for priority Critical/High
4. **Spatial grid** (amortized) — avoid O(N²) distance checks

## 11. NAT Traversal & Relay Infrastructure

**Reference:** [nat-traversal-relay.md](nat-traversal-relay.md)

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

## 12. Matchmaking Architecture

**Reference:** [matchmaking-architecture.md](matchmaking-architecture.md)

### The Matchmaking Pipeline

```
Player clicks "Play"
  → Pre-queue: Ping measurement, version check, ban check
  → Queue pool: Join ranked by skill bracket + region
  → Match formation: Greedy fill from top of bracket
  → Quality scoring: Skill spread × 0.6 + Latency × 0.25 + Wait time × 0.15
  → Server allocation: Assign dedicated server in optimal region
  → Connect: Send connection info to all matched players
```

### Skill Bracketing (Elo/Glicko-2)

```
Rating Range │ Bracket │ Max Wait │ Skill Spread Tolerance
─────────────┼─────────┼──────────┼──────────────────────
0-500        │ Bronze  │ 30s      │ ±300
500-1000     │ Silver  │ 45s      │ ±250
1000-1500    │ Gold    │ 60s      │ ±200
1500-2000    │ Plat    │ 90s      │ ±150
2000-2500    │ Diamond │ 120s     │ ±100
2500+        │ Master+ │ 300s     │ ±75
```

### Relaxation Over Time

As queue time increases, relax constraints in this order:
1. Widen skill bracket (±1 level)
2. Expand acceptable ping (+30ms)
3. Include adjacent game modes
4. Cross-region (if ping <200ms)
5. Any bracket, any ping — just get them playing

## 13. Dedicated Server Operations

**Reference:** [dedicated-server-infrastructure.md](dedicated-server-infrastructure.md)

### Orchestration

| Platform | Best For | Learning Curve | Cost |
|---|---|---|---|
| Agones + K8s | Custom control, multi-cloud, scale | High | Infrastructure only |
| AWS GameLift | Quick start, AWS-native, managed | Low | Infrastructure + GameLift fee |
| PlayFab Multiplayer | Azure ecosystem, managed | Low | Per-minute |
| Bare metal | 128+ tick servers, maximum perf | Medium | Instance cost, manual ops |

### Fleet Sizing Rule of Thumb

```
Warm pool size = peak_concurrent_matches × 0.15
               + headroom_for_spike

Example: 10,000 CCU, 10 players/match = 1,000 matches
Warm pool: 1,000 × 0.15 = 150 servers always ready
Scale-up time: <60 seconds for additional 200 servers
```

### Performance Budgets

| Tick Rate | Max Players | Tick Budget | CPU Required |
|---|---|---|---|
| 30 | 64 | 33ms | 2 vCPU |
| 60 | 10 | 16ms | 2 vCPU |
| 60 | 64 | 16ms | 4 vCPU |
| 128 | 10 | 7.8ms | 4 vCPU |
| 128 | 64 | 7.8ms | 8 vCPU (or bare metal) |

### Graceful Shutdown

```
1. Unregister from matchmaker (stop receiving new players)
2. Notify clients: "Server closing in 30s"
3. Allow 30s for client disconnect or match completion
4. Save match results and replay
5. Terminate process
```

## 14. Security & Anti-Cheat Architecture

### Server-Authoritative Validation

Every client-submitted value must be validated:

```cpp
bool ValidateMovement(Vector3 from, Vector3 to, float delta_time) {
    float distance = length(to - from);
    float max_distance = PLAYER_MAX_SPEED * delta_time * 1.1f; // 10% tolerance
    return distance <= max_distance;
}

bool ValidateDamage(float damage, uint32_t weapon_id, float range) {
    auto& weapon = WeaponDatabase[weapon_id];
    if (damage > weapon.max_damage) return false;    // Damage hack
    if (range > weapon.effective_range * 1.2f) return false; // Range hack
    return true;
}
```

### Common Attack Vectors & Defenses

| Attack | Method | Defense |
|---|---|---|
| Speedhack | Inject faster movement values | Server-side velocity cap per tick |
| Aimbot | Auto-aim at nearest enemy | Server-side raycast validates aim angle |
| Wallhack | Read enemy positions from memory | Interest management — never send occluded entity data |
| Packet injection | Spoof fire/damage packets | Authenticate packets with per-session key |
| Lag switch | Artificially delay own packets | Server-side timeout at 5s; kick at 15s no packets |
| DDoS game server | Flood server with garbage UDP | Rate limit per-IP; authenticate before heavy processing |

### DoS/DDoS Protection

- **Game server port:** Only accept packets from authenticated, match-assigned clients. Drop all others in kernel space (eBPF/XDP filter).
- **Relay service:** Use Steam SDR or cloud DDoS protection (AWS Shield, Cloudflare Spectrum).
- **Rate limiting:** Max 200 packets/second per client. Drop excess silently.

## 15. Debugging & Profiling Multiplayer Systems

### Essential Debugging Tools

**Network Simulator:**
```bash
# Linux: simulate 100ms ping, 2% packet loss, ±10ms jitter
sudo tc qdisc add dev eth0 root netem \
    delay 100ms 10ms 25% \
    loss 2% 25%
```

**Built-in Debug Overlay:**
```cpp
// Draw net debug info on screen
DrawText(0, 0, "Ping: %dms", ping_ms);
DrawText(0, 16, "Packet Loss: %.1f%%", packet_loss * 100);
DrawText(0, 32, "Snapshots Buffered: %d", interp_buffer.size());
DrawText(0, 48, "Prediction Error: %.3fm", prediction_error);
DrawText(0, 64, "Bandwidth In: %.1f KB/s", bw_in / 1024.0f);
DrawText(0, 80, "Bandwidth Out: %.1f KB/s", bw_out / 1024.0f);
```

### Common Desync Causes & Diagnosis

| Symptom | Likely Cause | Diagnostic Check |
|---|---|---|
| Rubber-banding | Prediction without reconciliation | Log prediction error per tick |
| Jittery remote players | Too little interpolation delay | Log snapshot inter-arrival variance |
| Entities teleporting | No interpolation at all | Check if Interpolate() is called |
| Shots don't register (server) | Rewind buffer too small | Log rewind target time vs buffer range |
| Shots register late (client) | TCP for fire events | Check channel assignment — fire must be reliable UDP, not TCP |
| Players can't connect | NAT hole punch failure | Log ICE candidate pair results |
| Server CPU spike every 30s | GC pause or large allocation | Profile with perf/perfview; use object pools |

### Profiling Commandments

1. **Profile on the server binary, not the client.** Graphics and input distort profiles.
2. **Use tick-level profiling:** `TickProfiler::Begin("Physics"); ... TickProfiler::End();` — shows per-subsystem cost per tick.
3. **Network bandwidth profiling:** Log bytes per channel, per client. Identify bandwidth hogs.
4. **Simulate realistic conditions:** Wi-Fi packet loss, mobile handoff, high player counts. Don't profile on LAN.
5. **Memory:** Watch for per-tick allocations. All game-server allocations should be pre-allocated or pooled.

### Tick Budget Breakdown (Target: 60t 16ms budget)

```
Network Receive:    0.5ms (3%)
Game Logic:         2.0ms (13%)
Physics:            4.0ms (25%)
Lag Compensation:   1.0ms (6%)
Snapshot Build:     1.5ms (9%)
Network Send:       1.0ms (6%)
Headroom:           6.0ms (38%) ← For spikes, GC, OS scheduling
Total:              16.0ms
```

---

## Reference Files

| File | Content |
|---|---|
| [client-server-architecture-games.md](client-server-architecture-games.md) | Topology patterns, authority models, tick rate selection, containerization |
| [prediction-reconciliation-patterns.md](prediction-reconciliation-patterns.md) | Client prediction loop, reconciliation, rollback netcode, input buffers |
| [lag-compensation-techniques.md](lag-compensation-techniques.md) | Backwards reconciliation, history buffer, hitscan vs projectile, sub-tick |
| [snapshot-interpolation.md](snapshot-interpolation.md) | Interpolation buffer, extrapolation, jitter management, entity types |
| [interest-management.md](interest-management.md) | Spatial relevance, frustum culling, priority tiers, bandwidth budgeting |
| [nat-traversal-relay.md](nat-traversal-relay.md) | STUN/TURN/ICE, UDP hole punching, relay architecture, SDR |
| [matchmaking-architecture.md](matchmaking-architecture.md) | Pipeline, SBMM with Glicko-2, latency routing, party matching, backfill |
| [dedicated-server-infrastructure.md](dedicated-server-infrastructure.md) | Docker/K8s/Agones, GameLift, monitoring, graceful shutdown, cost optimization |

## Quick Reference Commands

```bash
# Start a game server (Docker)
docker run -p 27015:27015/udp -e MAP=de_dust2 -e MAX_PLAYERS=10 gameserver:latest

# Network simulation for testing (add 100ms latency, 2% loss)
sudo tc qdisc add dev lo root netem delay 100ms 10ms loss 2%

# Remove network simulation
sudo tc qdisc del dev lo root

# Profile game server (Linux perf)
perf record -g ./gameserver_dedicated --map test_map --max_players 64 --tickrate 60

# ICE candidate testing
stunclient stun.l.google.com:19302

# Test NAT type
turnutils_natdiscover -s stun.example.com -p 3478

# UDP bandwidth test between client and server
iperf3 -c gameserver.example.com -u -p 27015 -b 100K -t 30

# Prometheus metrics endpoint check
curl http://localhost:9090/metrics | grep gameserver
```

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "UDP is too complex; we'll start with TCP and switch later" | TCP head-of-line blocking means one dropped packet stalls all messages; retrofitting UDP requires rewriting the entire netcode layer — every send/recv, every reliability layer, every serialization path |
| "We don't need client-side prediction for a co-op game" | Even in co-op, 50ms of latency without prediction makes movement feel like wading through molasses; players blame the game, not the network, and leave within the first session |
| "We'll handle lag compensation after the core gameplay is fun" | Lag compensation IS the core gameplay — without it, what's "fun" on localhost is unplayable at 100ms ping; the entire feel of the game is invalidated |
| "The server can just trust the client for now; we'll add validation later" | One player with Cheat Engine ruins the experience for 1000 legitimate players; trust-before-validate means you have no authoritative state to retroactively fix — the game is permanently compromised |
| "We'll add interest management when player count grows" | Without spatial interest management, 100 players each send updates to 99 others = 9,900 messages per tick; bandwidth explodes quadratically and server CPU melts before you hit "player count that matters" |

## References

- **Gaffer on Games** (gafferongames.com) — Glenn Fiedler's definitive series on game networking
- **Gabriel Gambetta** (gambetta.dev) — Client-Server Game Architecture series
- **Valve Developer Wiki** — Source Engine Multiplayer Networking
- **GDC Vault** — "Overwatch Gameplay Architecture and Netcode" (2017), "8 Frames in 16ms" (2018)
- **GameNetworkingSockets** — github.com/ValveSoftware/GameNetworkingSockets
- **Agones** — agones.dev (Google Cloud game server orchestration)
- **libjuice** — github.com/paullouisageneau/libjuice (lightweight ICE/STUN/TURN)
- **RFC 8445** (ICE), **RFC 5389** (STUN), **RFC 5766** (TURN)
