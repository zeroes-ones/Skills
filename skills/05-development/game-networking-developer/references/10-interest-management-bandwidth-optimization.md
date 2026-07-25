## 10. Interest Management & Bandwidth Optimization

**Reference:** [interest-management.md](references/interest-management.md)

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
