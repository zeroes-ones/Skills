## 8. Lag Compensation & Hit Registration

**Reference:** [lag-compensation-techniques.md](references/lag-compensation-techniques.md)

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
