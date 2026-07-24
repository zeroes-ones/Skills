# Snapshot Interpolation

> **Reference:** Smooth entity rendering from discrete server snapshots — the foundation of visually smooth multiplayer.

## Core Concept

The server sends entity state at a fixed tick rate (20-128Hz). Clients must smoothly interpolate between these discrete snapshots to avoid jittery, stuttering motion. Interpolation adds intentional display delay (typically 2× server tick interval) in exchange for perfectly smooth movement.

## Interpolation Buffer

### Buffer Design

```cpp
class InterpolationBuffer {
    struct Snapshot {
        float server_time;          // When server sent this
        float arrival_time;         // When client received this
        uint32_t tick;
        std::vector<EntityState> entities; // Full or partial entity list

        EntityState* FindEntity(uint16_t id) {
            auto it = std::find_if(entities.begin(), entities.end(),
                [id](const EntityState& e) { return e.id == id; });
            return (it != entities.end()) ? &(*it) : nullptr;
        }
    };

    static const int MAX_SNAPSHOTS = 64; // ~1s at 60Hz
    static const float INTERP_DELAY = 0.100f; // 100ms render delay

    std::deque<Snapshot> snapshots;

public:
    void AddSnapshot(Snapshot snap) {
        // Insert sorted by server_time
        auto pos = std::lower_bound(snapshots.begin(), snapshots.end(),
            snap.server_time, [](const Snapshot& s, float t) {
                return s.server_time < t;
            });

        // Replace if same tick
        if (pos != snapshots.end() && pos->tick == snap.tick)
            *pos = std::move(snap);
        else
            snapshots.insert(pos, std::move(snap));

        // Prune old
        float cutoff = snapshots.back().server_time - 1.0f;
        while (snapshots.size() > 1 && snapshots.front().server_time < cutoff)
            snapshots.pop_front();
    }

    bool GetInterpolatedState(uint16_t entity_id, float render_time,
                               EntityState& out_state) {
        float target_time = render_time - INTERP_DELAY;

        // Find two snapshots bracketing target_time
        const Snapshot* prev = nullptr;
        const Snapshot* next = nullptr;

        for (size_t i = 0; i < snapshots.size() - 1; i++) {
            if (snapshots[i].server_time <= target_time &&
                snapshots[i+1].server_time > target_time) {
                prev = &snapshots[i];
                next = &snapshots[i+1];
                break;
            }
        }

        if (!prev || !next) return false;

        // Find entity in both snapshots
        EntityState* prev_state = prev->FindEntity(entity_id);
        EntityState* next_state = next->FindEntity(entity_id);
        if (!prev_state || !next_state) return false;

        // Interpolate
        float range = next->server_time - prev->server_time;
        float t = (target_time - prev->server_time) / range;
        t = std::clamp(t, 0.0f, 1.0f);

        out_state.id = entity_id;
        out_state.position = lerp(prev_state->position, next_state->position, t);
        out_state.rotation = slerp(prev_state->rotation, next_state->rotation, t);
        out_state.velocity = lerp(prev_state->velocity, next_state->velocity, t);
        return true;
    }
};
```

## Interpolation Delay Selection

| Game Type | Target Render Delay | Server Tick Rate | Snapshots Behind |
|---|---|---|---|
| Competitive FPS | 30-50ms | 64-128t | 2-3 snapshots |
| Casual FPS | 66-100ms | 20-30t | 2 snapshots |
| MOBA | 66-100ms | 30-60t | 2-3 snapshots |
| Battle Royale | 100ms | 20-30t | 2 snapshots |
| MMO | 100-200ms | 1-10t | 1-2 snapshots |

## Extrapolation (Dead Reckoning)

When snapshots run out (packet loss, jitter spike), extrapolate forward from last known state.

### Linear Extrapolation

```cpp
EntityState Extrapolate(const EntityState& last_state, float time_delta) {
    EntityState result = last_state;
    result.position += last_state.velocity * time_delta;
    // Apply acceleration if known
    result.position += last_state.acceleration * 0.5f * time_delta * time_delta;
    return result;
}
```

### Extrapolation Limits

```cpp
bool ShouldExtrapolate(float time_since_last_snapshot) {
    // Never extrapolate more than 200ms
    if (time_since_last_snapshot > 0.200f) {
        // Entity is stale — freeze at last position or hide
        return false;
    }
    return true;
}
```

**Critical:** Extrapolation is error-prone. Always:
1. Cap extrapolation time (100-200ms max).
2. Smoothly snap back when snapshot arrives (blend over 100ms, not instant).
3. Never extrapolate entities that can change direction instantly (players — use velocity, but clamp).

## Jitter Buffer

Network jitter (variance in packet arrival time) causes snapshots to arrive irregularly. A jitter buffer smooths this.

```cpp
class JitterBuffer {
    static const int BUFFER_SIZE = 32;
    struct Packet {
        uint32_t sequence;
        float arrival_time;
        std::vector<uint8_t> data;
    };
    Packet buffer[BUFFER_SIZE];
    uint32_t next_expected;

    // Adaptive jitter: dynamically adjust target delay
    float target_delay = 0.050f; // Start at 50ms
    float current_jitter = 0.0f;

    void UpdateJitter(float inter_arrival_time) {
        // EWMA jitter estimation
        static const float ALPHA = 0.1f;
        current_jitter = (1.0f - ALPHA) * current_jitter +
                         ALPHA * std::abs(inter_arrival_time - expected_interval);

        // Target delay = 2x jitter for safety margin
        target_delay = 2.0f * current_jitter;
        target_delay = std::clamp(target_delay, 0.016f, 0.150f);
    }
};
```

## Entity Interpolation Types

### Position (Vector3)
```cpp
Vector3 lerp(Vector3 a, Vector3 b, float t) {
    return a + (b - a) * t;
}
```
Always use linear interpolation for position. Cubic/monotone splines add smoothing at cost of overshoot.

### Rotation (Quaternion)
```cpp
Quaternion slerp(Quaternion a, Quaternion b, float t) {
    // Spherical linear interpolation
    float cos_omega = dot(a, b);
    if (cos_omega < 0) { b = -b; cos_omega = -cos_omega; }

    // Use lerp for small angles (faster, avoids singularity)
    if (cos_omega > 0.9995f) {
        return normalize(lerp(a, b, t));
    }

    float omega = acos(cos_omega);
    float sin_omega = sin(omega);
    return (sin((1-t)*omega)/sin_omega)*a + (sin(t*omega)/sin_omega)*b;
}
```

### Animation State
Discrete states (running, jumping, idle) should NOT be interpolated. Instead:
1. Snap to next animation state on new snapshot.
2. Blend between animation poses over ~50ms for visual smoothness.
3. Use animation time synchronization: server sends `animation_time` float.

### Aim Direction (Yaw/Pitch)
- **Yaw:** lerp with wrap-around handling (`lerp_angle`).
- **Pitch:** Clamped lerp (-89 to +89 degrees typically).

## Prioritization for Large Player Counts

In battle royales (100 players), interpolating all entities is wasteful. Most are out of view.

```cpp
enum InterpolationPriority {
    PRIORITY_CRITICAL = 0,  // Local player, crosshair target
    PRIORITY_HIGH     = 1,  // Within 50m, in frustum
    PRIORITY_MEDIUM   = 2,  // Within 100m, in frustum
    PRIORITY_LOW      = 3,  // Out of view, >100m
    PRIORITY_OFF      = 4,  // >200m, don't interpolate at all
};
```

## Common Artifacts & Solutions

| Artifact | Cause | Solution |
|---|---|---|
| Jitter/stutter | Insufficient interpolation delay | Increase INTERP_DELAY |
| "Swimming" motion | Interpolating between divergent angles | slerp for rotations |
| "Rubber banding" | Prediction correction + interpolation fighting | Disable interpolation for predicted entity |
| Entity teleports | New snapshot with large position delta | Detect teleports > threshold, snap instead of interpolate |
| Pop-in | Entity spawning mid-interpolation | Spawn at interpolated start position, not origin |

## Bandwidth Optimization for Snapshots

1. **Delta encoding:** Send only changed fields since last acknowledged snapshot.
2. **Quantization:** Compress floats to 16-bit or lower precision per-field.
3. **Interest management:** Don't send entities that can't be seen/needed.
4. **Priority-based update rate:** Close/important entities update every tick; distant entities every Nth tick.

```cpp
struct QuantizedPosition {
    int16_t x, y, z; // 1mm precision over ±32m range
    Vector3 ToFloat() { return Vector3(x/1000.0f, y/1000.0f, z/1000.0f); }
};
```

## References

- Source Engine: "Entity Interpolation" — Valve Developer Wiki
- "Snapshot Interpolation" — Gabriel Gambetta, gambetta.dev
- Gaffer on Games: "Networked Physics" — Glenn Fiedler
- Unreal Engine: CharacterMovementComponent networking guide
