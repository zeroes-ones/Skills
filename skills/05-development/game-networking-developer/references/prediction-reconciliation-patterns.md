# Prediction & Reconciliation Patterns

> **Reference:** Client-side prediction, server reconciliation, and rollback — the core of responsive netcode.

## The Fundamental Problem

Without prediction, a player pressing "move forward" waits RTT/2 for the server to acknowledge, then sees movement. At 100ms ping, that's 50ms of perceived lag — unacceptable for any action game.

## Client-Side Prediction

### Basic Prediction Loop

```
Client Tick:
  1. Sample local input (keyboard, mouse, controller)
  2. Apply input to local predicted state immediately
  3. Send input command to server (sequenced, tick-stamped)
  4. Render predicted state (feels instant)

Server Tick:
  1. Receive input commands from all clients
  2. Validate: is command physically possible this tick?
  3. Simulate authoritative state
  4. Broadcast snapshot: {tick, entities[], last_processed_input[]}
```

### Input Command Structure

```cpp
struct InputCommand {
    uint32_t sequence;       // Monotonically increasing per-client
    uint32_t tick;           // Server tick this input targets
    float delta_time;        // Time since last command
    // --- Movement ---
    float move_forward;      // -1.0 to 1.0 (W/S)
    float move_right;        // -1.0 to 1.0 (A/D)
    // --- View ---
    float yaw, pitch;        // Camera angles
    // --- Actions ---
    uint32_t button_mask;    // Bitfield: fire, jump, reload, ability_1, ...
    // --- Aim ---
    float aim_yaw, aim_pitch; // If separate from view
};
```

This compresses to 16-24 bytes with bit-packing.

### Prediction Steps

**Step 1: Immediate Local Application**
```
predicted_velocity = input.move_direction * max_speed
predicted_position += predicted_velocity * delta_time
```

**Step 2: Store Unacknowledged Commands**
```cpp
struct PendingCommand {
    InputCommand input;
    Vector3    predicted_position;  // Where we moved to
    Quaternion predicted_rotation;
    uint32_t   tick;
};
// Ring buffer of last 1024 commands
std::deque<PendingCommand> pending_commands;
```

**Step 3: On Server Snapshot Arrival**
```
snapshot = deserialize(packet)
last_acked = snapshot.last_processed_input[local_player_id]

// Remove old acknowledged commands
pending_commands.erase(
    pending_commands.begin(),
    find(pending_commands, last_acked)
);
```

## Server Reconciliation

### When Prediction Fails

The server-authoritative position differs from client-predicted position. Causes:
1. Latency: server processed different inputs at different times
2. Physics divergence: floating-point differences, different tick rates
3. Correction from other entities: another player blocked your path
4. Cheat detection: server rejected impossible movement

### Reconcilation Algorithm

```cpp
void Reconcile(uint32_t server_tick, Vector3 server_position,
               uint32_t last_ack_sequence) {
    // 1. Remove acknowledged commands
    RemoveAckedCommands(last_ack_sequence);

    // 2. Check prediction error
    Vector3 error = server_position - predicted_entity_position;

    if (error.length() > RECONCILE_THRESHOLD) {
        // 3. Snap to server position
        predicted_entity_position = server_position;

        // 4. Replay unacknowledged inputs from corrected position
        for (auto& cmd : pending_commands) {
            ApplyInput(cmd.input);
        }
    }
    // Else: small error, interpolate smoothly
    else if (error.length() > SMOOTH_THRESHOLD) {
        // Blend toward server state over ~100ms
        correction_velocity = error * CORRECTION_SPEED;
    }
}
```

### Threshold Tuning

| Game Type | Snap Threshold | Smooth Threshold | Correction Speed |
|---|---|---|---|
| FPS (competitive) | 0.5m | 0.05m | 10.0 units/s |
| FPS (casual) | 1.0m | 0.10m | 5.0 units/s |
| Racing | 2.0m | 0.20m | 15.0 units/s |
| Third-person action | 1.5m | 0.15m | 8.0 units/s |

## Rollback Netcode (Fighting Games / Fast-Paced)

Rollback netcode assumes every local input is correct AND immediately applied, then "rolls back" and re-simulates if remote inputs arrive that change history.

### Rollback Algorithm

```
1. Advance frame N with predicted remote inputs
2. Store full game state snapshot at frame N
3. Remote input for frame N arrives at frame N+K
4. If remote_input[N] != predicted_input[N]:
   a. Restore state from snapshot[N]
   b. Re-simulate frames N through N+K with correct remote input
   c. Render corrected frame N+K
```

### Implementation Requirements

- **Save state every frame:** Full game state must be serializable and restorable in <1ms.
- **Deterministic simulation:** Same inputs MUST produce identical results. Floating-point determinism is critical.
- **State buffer:** Store last ~8 frames of state (8 frames at 60fps = 133ms of rollback window).
- **Input delay:** Optional fixed delay (1-3 frames) to reduce visible rollbacks.

### Rollback vs Delay-Based

| Property | Rollback | Delay-Based |
|---|---|---|
| Responsiveness | 0 frame delay | 2-7 frame delay |
| Visual artifacts | Occasional "snap" on rollback | Consistent delay |
| Implementation complexity | High | Medium |
| CPU overhead | Higher (re-simulation) | Lower |
| Netcode quality at 100ms ping | Playable | Unplayable |
| Best for | Fighting, fast FPS | Slower-paced games, casual |

## Input Buffer & Jitter Management

```cpp
class InputBuffer {
    static const int BUFFER_SIZE = 128; // ~2 seconds at 60tick
    InputCommand commands[BUFFER_SIZE];
    uint32_t base_sequence;

    void Add(InputCommand cmd) {
        int idx = (cmd.sequence - base_sequence) % BUFFER_SIZE;
        commands[idx] = cmd;
    }

    InputCommand* Get(uint32_t sequence) {
        if (sequence < base_sequence) return nullptr; // Too old
        if (sequence >= base_sequence + BUFFER_SIZE) return nullptr; // Too new
        return &commands[(sequence - base_sequence) % BUFFER_SIZE];
    }
};
```

## Common Pitfalls

1. **Prediction without reconciliation** — Entities drift apart permanently. Always reconcile.
2. **Replaying from wrong tick** — Must replay from the exact server-confirmed tick.
3. **Ignoring delta time accumulation** — Replayed frames must use original delta times, not accumulated.
4. **Not handling packet loss** — Missing input packets require extrapolation or last-known-input replay.
5. **NaN propagation from prediction** — Validate every float after prediction; NaN positions crash renderers.

## Optimization: Delta Prediction State

Instead of sending full entity state (position, rotation, velocity), send only what changed:

```cpp
struct DeltaState {
    uint16_t entity_id;
    uint8_t  changed_fields; // Bitmask
    // Only include fields with corresponding bit set:
    Vector3F position;       // If POSITION bit set
    Quat16  rotation;        // If ROTATION bit set
    Vector3F velocity;       // If VELOCITY bit set
};
```

This reduces per-entity bandwidth from 64 bytes to 8-32 bytes (60-85% reduction).

## References

- Gabriel Gambetta, "Client-Server Game Architecture" — gambetta.dev
- GDC 2014: "This Is Your Brain on Netcode" — Glenn Fiedler
- "Fighting Game Rollback Netcode" — Infil's guide at mizuumi.net
- Source Engine Multiplayer (Valve) — client prediction & lag compensation
