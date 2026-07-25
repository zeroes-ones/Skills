# Interest Management

> **Reference:** Spatial and behavioral relevance filtering — send only what each player needs to know.

## Problem Statement

In a 100-player battle royale, broadcasting every entity's full state to every player requires 100 × 99 × ~200 bytes = ~2 MB/s per player. Interest management reduces this to entities the player can actually see, interact with, or needs to be aware of — typically 5-15% of total entities.

## Relevance Dimensions

### 1. Spatial Relevance (Distance)

The most fundamental filter: entities beyond a certain distance are irrelevant.

```cpp
struct RelevanceDistance {
    float full_update_range;   // Full tick-rate updates
    float partial_update_range; // Every Nth tick
    float awareness_range;     // Minimal update (position only)
    float cull_range;          // No updates at all

    UpdatePriority GetPriority(float distance) {
        if (distance <= full_update_range)   return PRIORITY_FULL;
        if (distance <= partial_update_range) return PRIORITY_PARTIAL;
        if (distance <= awareness_range)     return PRIORITY_AWARENESS;
        return PRIORITY_CULL;
    }
};
```

### Per-Genre Distance Settings

| Entity Type | Full (m) | Partial (m) | Awareness (m) | Cull (m) |
|---|---|---|---|---|
| Player (FPS) | 100 | 200 | 400 | >400 |
| Player (BR) | 150 | 300 | 500 | >500 |
| Player (MMO) | 50 | 100 | 250 | >250 |
| Vehicle | 200 | 500 | 1000 | >1000 |
| Projectile | 50 | 100 | 150 | >150 |
| Pickup/Item | 30 | 60 | 100 | >100 |

### 2. View Frustum Relevance

Entities behind the player are lower priority than those in front.

```cpp
bool IsInViewFrustum(Vector3 entity_pos, Vector3 view_pos,
                     Vector3 view_forward, float fov_degrees,
                     float aspect_ratio) {
    Vector3 to_entity = normalize(entity_pos - view_pos);

    // Horizontal FOV check
    float dot_h = dot(to_entity, view_forward);
    float half_fov = cos(radians(fov_degrees * 0.5f));

    // Expand frustum slightly for networking margin
    float margin = 0.1f; // ~10% overscan
    return dot_h > (half_fov - margin);
}
```

### 3. Line of Sight (Occlusion)

Entities behind walls don't need full updates — only awareness-level data.

```cpp
RelevanceLevel ComputeRelevance(Vector3 viewer, Vector3 target) {
    float distance = length(target - viewer);

    // Spatial check first (cheapest)
    if (distance > MAX_RELEVANCE_DISTANCE) return IRRELEVANT;

    // Frustum check (moderately cheap)
    if (!IsInViewFrustum(target, viewer, view_forward, fov)) {
        if (distance <= AWARENESS_RANGE)
            return AWARENESS_ONLY; // Footsteps, gunshots
        return IRRELEVANT;
    }

    // Line of sight check (most expensive — amortize)
    RayCastResult hit = TraceLine(viewer, target);
    if (hit.blocked && hit.entity != target) {
        if (hit.distance < 5.0f) // Just behind thin wall
            return HIGH_RELEVANCE;
        return AWARENESS_ONLY; // Deeply occluded
    }

    return FULL_RELEVANCE;
}
```

## Priority-Based Update Scheduling

Instead of binary relevant/irrelevant, use priority tiers with proportional bandwidth:

### Update Priority Tiers

```
Tier 0 (CRITICAL): Every tick, full state
  - Crosshair target / aimed-at enemy
  - Local player's own entity (prediction target)
  - Entities within 5m and in front

Tier 1 (HIGH): Every 2 ticks, full state
  - Enemies in view frustum within 50m
  - Teammates at any distance
  - Active threats (shooting, visible)

Tier 2 (MEDIUM): Every 4 ticks, partial state
  - Enemies in view frustum, 50-150m
  - Entities behind player within 20m
  - Important pickups and objectives

Tier 3 (LOW): Every 8 ticks, position-only
  - Distant enemies (150-300m, in frustum)
  - Entities behind player (20-50m)

Tier 4 (AWARENESS): Every 16+ ticks, minimal
  - Gunshot indicators
  - Footstep events
  - Minimap-only entities

Tier 5 (CULL): Never sent
  - Beyond max range
  - Irrelevant entity types
```

### Bandwidth Budgeting

```cpp
class InterestManager {
    static const int MAX_BYTES_PER_TICK = 1200; // 1200 bytes/tick = ~72 KB/s at 60tick

    int CalculateBudget(int total_players) {
        // Headline budget: scale with player count
        return std::min(MAX_BYTES_PER_TICK, 200 + total_players * 10);
    }

    void AssignUpdates(Player* viewer, int bytes_budget) {
        std::vector<Entity*> candidates = GatherRelevantEntities(viewer);

        // Sort by priority (primary) and distance (secondary)
        std::sort(candidates.begin(), candidates.end(),
            [viewer](Entity* a, Entity* b) {
                if (a->relevance_tier != b->relevance_tier)
                    return a->relevance_tier < b->relevance_tier;
                return distance(viewer->pos, a->pos) <
                       distance(viewer->pos, b->pos);
            });

        int bytes_used = 0;
        for (auto* entity : candidates) {
            int entity_bytes = EstimateUpdateSize(entity);
            if (bytes_used + entity_bytes > bytes_budget) break;

            AddEntityToSnapshot(entity);
            bytes_used += entity_bytes;
        }
    }
};
```

## Relevance Groups (Spatial Partitioning)

Use a spatial grid to avoid O(N²) distance checks:

```cpp
class InterestGrid {
    static const float CELL_SIZE = 50.0f; // 50m cells
    struct Cell {
        std::vector<uint16_t> entity_ids;
        uint32_t last_update_tick;
    };
    std::unordered_map<uint64_t, Cell> cells;

    uint64_t CellKey(float x, float z) {
        int cx = static_cast<int>(floor(x / CELL_SIZE));
        int cz = static_cast<int>(floor(z / CELL_SIZE));
        return (static_cast<uint64_t>(cx) << 32) | static_cast<uint32_t>(cz);
    }

    void GetRelevantEntities(Vector3 position, float radius,
                             std::vector<uint16_t>& out) {
        int cell_radius = static_cast<int>(ceil(radius / CELL_SIZE));
        int cx = static_cast<int>(floor(position.x / CELL_SIZE));
        int cz = static_cast<int>(floor(position.z / CELL_SIZE));

        for (int dx = -cell_radius; dx <= cell_radius; dx++) {
            for (int dz = -cell_radius; dz <= cell_radius; dz++) {
                auto* cell = GetCell(cx + dx, cz + dz);
                if (cell) {
                    for (uint16_t id : cell->entity_ids) {
                        auto* entity = GetEntity(id);
                        if (distance(position, entity->position) <= radius)
                            out.push_back(id);
                    }
                }
            }
        }
    }
};
```

## World Streaming Relevance

For large open worlds, relevance is also about which world chunks to stream:

```cpp
struct WorldRelevance {
    uint16_t chunk_x, chunk_z;
    uint8_t lod_level; // 0=full, 1=simplified, 2=heightmap-only

    static uint8_t ComputeLOD(float distance) {
        if (distance < 200.0f) return 0; // Full geometry
        if (distance < 500.0f) return 1; // Simplified
        return 2; // Just terrain height for bullet traces
    }
};
```

## Anti-Cheat Considerations

Interest management creates information asymmetry — cheaters can exploit this:
- **Wallhacks rely on server sending hidden enemy positions.** Ensure CULL tier entities truly have zero data sent.
- **Radar hacks from awareness data.** Minimap-only entities should contain only coarse position (quantized to cell size).
- **Sound-based wallhacks.** Footstep events sent as awareness data can be processed by cheats. Consider server-side audio mixing.

## Performance Benchmarks

| Scenario | Without Interest Mgmt | With Interest Mgmt | Reduction |
|---|---|---|---|
| 100-player BR, flat terrain | 100 entities/player | 8-15 entities/player | 85-92% |
| 64-player FPS, indoor map | 64 entities/player | 3-8 entities/player | 87-95% |
| 1000-player MMO, city hub | 1000 entities/player | 20-50 entities/player | 95-98% |
| 32-player racing | 32 entities/player | 5-10 entities/player | 69-84% |

## References

- "Interest Management for Networked Games" — Glenn Fiedler, Gaffer on Games
- Spatial OS Interest Management documentation
- Unreal Engine: Replication Graph & Net Culling documentation
- Unity Netcode: NetworkTransform interest management
