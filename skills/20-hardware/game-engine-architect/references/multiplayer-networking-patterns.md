# Multiplayer Networking Patterns

## Client-Side Prediction
- Client runs same simulation as server, predicts local player N ticks ahead
- Input buffer: `InputCommand inputs[MAX_INPUT_HISTORY]` indexed by tick number
- Send input with tick number (not frame number) — server can reorder by tick
- Prediction window: 2-4 ticks at 64Hz tickrate (30-60ms at 50ms typical ping)

## Server Reconciliation
```cpp
void Client::OnServerState(const ServerState& state, int32_t tick) {
    const PlayerState& authoritative = state.playerStates[localPlayerId];
    const PlayerState& predicted = predictionHistory[tick];

    float error = Distance(predicted.position, authoritative.position);
    if (error > RECONCILIATION_THRESHOLD) {
        currentState = authoritative;  // Rewind
        for (int32_t t = tick + 1; t <= currentTick; ++t) {
            simulate(currentState, inputHistory[t]);  // Replay
        }
    }
}
```
- Threshold: 1cm for FPS, 5cm for open-world
- Replay cost: O(inputs_replayed). Keep input history window small (<60 ticks)

## Rollback Netcode (GGPO-style)
- All clients simulate all players deterministically
- Input delay: 1-3 frames of artificial delay to absorb network jitter
- On remote input arrival: rewind state to that tick, replay all subsequent inputs
- Save state every frame (memory: ~1MB per frame for fighting games)
- For: fighting games, brawlers, sports. NOT for: >4 players, complex physics

## Snapshot Interpolation
- Server sends state snapshots at tickrate (e.g., 64Hz)
- Client buffers 2-3 snapshots (interp_delay = 2 ticks = 31ms at 64Hz)
- Render state between snapshot[N] and snapshot[N+1] using interpolation factor
- Jitter buffer: adaptive size based on measured network jitter
- Entity "drift" correction: smoothly blend to authoritative position over 100ms

## Network Topology
- **Client-Server:** Single authoritative server. Best for: FPS, BR, MMO. Requires server infrastructure
- **P2P Lockstep:** All clients simulate, wait for all inputs. Best for: RTS, turn-based. No server cost
- **P2P with Host Migration:** One client is host/server. Host advantage + migration complexity
