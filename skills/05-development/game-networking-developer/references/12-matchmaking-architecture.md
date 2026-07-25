## 12. Matchmaking Architecture

**Reference:** [matchmaking-architecture.md](references/matchmaking-architecture.md)

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
