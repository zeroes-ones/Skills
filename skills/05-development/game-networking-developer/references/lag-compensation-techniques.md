# Lag Compensation Techniques

> **Reference:** Server-side hit registration, backwards reconciliation, and latency fairness for competitive multiplayer games.

## The Problem: "I Shot Him on My Screen"

Without lag compensation, a player must lead their target by the target's ping. With lag compensation, the server rewinds time to what the shooter saw, making aiming feel consistent regardless of ping (within limits).

## Backwards Reconciliation (Server-Side Rewind)

The core algorithm: when server receives a "fire" command from shooter at tick T_server, it rewinds all entity positions to what they were at T_shooter (when the shot actually happened on the shooter's screen).

### Algorithm

```
OnReceiveFire(shooter_id, fire_tick, aim_direction):
    1. rewind_time = ServerTime - (CurrentTick - fire_tick)*TickDuration
    2. stored_state = SaveAllEntityStates()
    3. RewindAllEntitiesToTick(fire_tick)  // Use history buffer
    4. hit_result = Raycast(shooter_eye_position, aim_direction)
    5. RestoreAllEntityStates(stored_state)
    6. If hit_result.hit:
       a. Validate hit was possible (damage range, line of sight)
       b. Apply damage on current tick (not rewound)
       c. Return hit confirmation to shooter
    7. Else: return miss
```

### History Buffer Implementation

```cpp
class LagCompensationHistory {
    struct SnapshotEntry {
        float time;
        Vector3 position;
        Vector3 velocity;
        BoundingBox hitbox;    // Pre-computed for hit detection
        uint32_t tick;
        bool is_crouching;     // Affects hitbox height
    };

    static const int MAX_HISTORY = 64; // ~1 second at 60tick
    std::deque<SnapshotEntry> history[MAX_PLAYERS];

    void RecordSnapshot(int player_id, float time, EntityState state) {
        auto& player_history = history[player_id];

        // Adaptive sampling: record more when velocity changes
        if (player_history.empty() ||
            (state.velocity - player_history.back().velocity).length() > 0.1f ||
            player_history.size() > 0 &&
            time - player_history.back().time > 0.015f) {

            SnapshotEntry entry;
            entry.time = time;
            entry.position = state.position;
            entry.velocity = state.velocity;
            entry.hitbox = ComputeHitbox(state);
            entry.is_crouching = state.flags & CROUCHING;
            player_history.push_back(entry);

            // Prune old entries
            while (!player_history.empty() &&
                   time - player_history.front().time > MAX_HISTORY_DURATION) {
                player_history.pop_front();
            }
        }
    }

    bool GetInterpolatedState(int player_id, float target_time,
                              Vector3& out_position, BoundingBox& out_hitbox) {
        auto& h = history[player_id];
        if (h.size() < 2) return false;

        // Find two entries bracketing target_time
        auto it = std::lower_bound(h.begin(), h.end(), target_time,
            [](const SnapshotEntry& e, float t) { return e.time < t; });

        if (it == h.begin() || it == h.end()) return false;

        auto& prev = *(it - 1);
        auto& next = *it;

        float t = (target_time - prev.time) / (next.time - prev.time);
        t = std::clamp(t, 0.0f, 1.0f);

        out_position = lerp(prev.position, next.position, t);
        out_hitbox = lerp(prev.hitbox, next.hitbox, t);
        return true;
    }
};
```

## Lag Compensation Limits

| Parameter | Typical Value | Reasoning |
|---|---|---|
| Max rewind window | 200ms | Beyond this, positions too stale |
| Max compensated ping | 150ms | Reject shots from high-ping players |
| Hitbox expansion | 0-5% | Slight generosity for networking |
| Tick resolution | Same as server tick | No sub-tick interpolation needed |
| History buffer size | 1 second | Covers max ping + jitter buffer |

## Choosing the Rewind Target Time

```cpp
float CalculateRewindTime(uint32_t fire_tick, float shooter_rtt) {
    // Base: rewind to when shooter fired (expressed as server time)
    float base_rewind = ServerTimeAtTick(fire_tick);

    // Option A: Pure shooter-time (standard)
    return base_rewind;

    // Option B: Fair-play midpoint
    // Rewind to halfway between shooter time and server time
    // Reduces peeker's advantage at cost of perceived fairness
    float midpoint = base_rewind + (current_time - base_rewind) * 0.5f;
    return midpoint;
}
```

## Peeker's Advantage

A high-ping player peeking a corner sees the defender before the defender sees them. Lag compensation amplifies this: the shooter gets their "old" view validated.

### Mitigation Strategies

1. **Ping cap at matchmaking** — Match only within ±30ms regions.
2. **Damage delay** — Apply damage after round-trip confirmation. Feels bad for shooter.
3. **Server-side only hit detection for high-ping** — Fall back to non-compensated for >100ms ping.
4. **Limited rewind window** — 150ms max means extreme peekers aren't compensated.
5. **Backward reconciliation with interpolation** — Interpolate target position between two snapshots rather than using exact packet time.

## Projectile vs Hitscan Compensation

### Hitscan (Instant)
- Rewind to fire tick, raycast. Simple.
- Only shooter lag matters for hit registration.
- Example: CS2 rifles, Valorant rifles, Overwatch hitscan.

### Projectile (Travel Time)
- Rewind to fire tick, then simulate projectile forward to current tick.
- Both shooter AND target lag matter.
- More complex: must advance projectile through rewound world.
- Example: Overwatch Pharah rockets, Quake rockets, Battlefield sniper bullets.

```cpp
// Projectile hit detection with lag compensation
bool CheckProjectileHit(Projectile& proj, float fire_time, float current_time) {
    float elapsed = current_time - fire_time;
    Vector3 projected_position = proj.origin + proj.velocity * elapsed;

    // Step through projectile path, checking each tick's hit state
    float step = SERVER_TICK_DURATION; // e.g., 0.016s
    for (float t = fire_time; t <= current_time; t += step) {
        RewindAllEntitiesToTime(t);
        Vector3 pos_at_t = proj.origin + proj.velocity * (t - fire_time);
        HitResult hit = SphereSweep(pos_at_t - proj.velocity*step, pos_at_t, proj.radius);
        if (hit.entity_id != INVALID_ENTITY) return true;
    }
    RestoreEntitiesToTime(current_time);
    return false;
}
```

## Sub-Tick Timing

Modern games (CS2, Valorant) process shots at sub-tick precision. Instead of quantizing the shot to the nearest server tick, the exact client timestamp is preserved.

```cpp
struct SubTickShot {
    uint32_t tick;              // Server tick
    uint16_t sub_tick_fraction; // 0-65535, fraction of tick elapsed
    Vector3 aim_origin;
    Vector3 aim_direction;
};

// During rewind:
float exact_time = TickToTime(shot.tick) +
                   shot.sub_tick_fraction / 65536.0f * TICK_DURATION;
RewindTo(exact_time); // Sub-tick precision rewind
```

## Common Pitfalls

1. **Rewinding ALL entities, not just the target** — Line-of-sight blockers (walls, boxes) must also rewind.
2. **Not capping rewind buffer memory** — 100+ entities × 1 second × 64 snapshots = RAM explosion. Cap aggressively.
3. **Interpolation artifacts on rewind** — Jitter in rewinded positions causes missed shots that looked correct. Use high-resolution history.
4. **Client shows hit, server says miss** — Always trust server. Communicate miss clearly to avoid "I definitely hit him!" frustration.
5. **Lag compensation + prediction interaction** — The predicted local position must not be used for hit registration. Isolate.

## Performance Considerations

| Technique | CPU Cost | Memory Cost | Notes |
|---|---|---|---|
| Per-player history ring buffer | ~0.01ms/frame | ~4KB/player | 64 entries × 64 bytes |
| Rewind copy (full state) | ~0.1ms/shot | 0 (stack) | Only copy what raycast touches |
| Raycast in rewound state | Same as physics | 0 | Use same collision as simulation |
| Sub-tick interpolation | ~0.005ms | 0 | Lerp between two snapshots |

## References

- Valve Developer Wiki: "Lag Compensation" (Source Engine)
- "Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization" — Yahn Bernier (Valve), GDC 2001
- CS2 Sub-tick Update — Valve, 2023
- "Overwatch Gameplay Architecture and Netcode" — GDC 2017
