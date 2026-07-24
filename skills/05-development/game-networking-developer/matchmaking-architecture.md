# Matchmaking Architecture

> **Reference:** Player-to-game-server assignment, skill-based matchmaking (SBMM), latency-based routing, and party management.

## Core Responsibilities

Matchmaking answers: "Which server should these players connect to, and with whom should they play?"

```
Players → [Matchmaker] → Game Server Assignment
              │
              ├─ Skill rating lookup & balancing
              ├─ Latency measurement (ping to all regions)
              ├─ Party/group preservation
              ├─ Map/mode preference resolution
              └─ Server capacity & health awareness
```

## Matchmaking Pipeline

### Stage 1: Pre-Queue

```
1. Client measures ping to all regional endpoints
   → GET /ping/us-east, /ping/eu-west, /ping/ap-seoul, ...
2. Client reports: { region: "us-east", pings: {us-east:12, us-west:48, eu-west:95} }
3. Optional: Client reports hardware profile (for fairness in cross-play)
4. Server validates: is client on latest version? Banned? Region-locked?
```

### Stage 2: Queue Pool

```cpp
struct MatchmakingTicket {
    std::string ticket_id;
    std::string player_id;
    std::string party_id;         // Empty if solo
    int         skill_rating;     // e.g., Elo 1200
    float       skill_uncertainty; // Higher = less confident rating
    std::vector<std::string> preferred_regions; // ["us-east", "us-west"]
    std::map<std::string, int> region_pings;   // Latency per region
    std::vector<std::string> preferred_modes;  // ["ranked", "casual"]
    std::vector<std::string> preferred_maps;   // ["dust2", "inferno"]
    bool        crossplay_enabled;
    uint64_t    joined_timestamp_ms;
};
```

### Stage 3: Match Formation

```cpp
struct MatchCandidate {
    std::vector<MatchmakingTicket> players;
    std::string region;
    std::string game_server_ip;    // Pre-allocated or to-be-allocated
    int         total_skill;
    int         skill_range;       // Max - min skill
    int         max_ping;          // Highest ping among players
    uint64_t    age_ms;            // How long oldest player has been waiting
};

MatchCandidate FormMatch(std::vector<MatchmakingTicket>& pool) {
    // 1. Group by region preference (intersection)
    auto region_groups = GroupByRegion(pool);

    // 2. Within each region, apply skill brackets
    for (auto& [region, tickets] : region_groups) {
        auto brackets = SplitBySkill(tickets);

        // 3. Sort by wait time (oldest first)
        for (auto& bracket : brackets) {
            std::sort(bracket.begin(), bracket.end(),
                [](auto& a, auto& b) { return a.joined_timestamp_ms < b.joined_timestamp_ms; });
        }

        // 4. Fill match from top of bracket
        MatchCandidate match;
        for (auto& ticket : brackets.front()) {
            if (match.players.size() < MAX_PLAYERS) {
                match.players.push_back(ticket);
            }
        }

        // 5. Validate quality thresholds
        if (VerifyMatchQuality(match)) return match;
    }

    return {}; // No valid match yet
}
```

### Stage 4: Match Quality Scoring

```cpp
float ScoreMatchQuality(const MatchCandidate& match) {
    float score = 0.0f;

    // Skill fairness (60% weight) — lower spread = better
    float skill_spread = (match.skill_range / 1000.0f); // Normalized
    score += 0.60f * (1.0f - skill_spread);

    // Latency quality (25% weight)
    float latency_penalty = (match.max_ping > 80) ?
        (match.max_ping - 80) / 100.0f : 0.0f;
    score += 0.25f * (1.0f - latency_penalty);

    // Wait time (15% weight) — longer wait = more lenient
    float wait_seconds = match.age_ms / 1000.0f;
    float wait_bonus = std::min(wait_seconds / 120.0f, 1.0f); // Max at 2 min
    score += 0.15f * wait_bonus;

    return score;
}
```

## Skill-Based Matchmaking (SBMM) Algorithms

### Elo/Glicko Rating Integration

```cpp
struct PlayerRating {
    float rating;         // e.g., 1500
    float deviation;      // Glicko RD — confidence interval
    float volatility;     // Glicko-2 volatility
    uint64_t last_match_timestamp;
};

// Glicko-2 rating update after match
void UpdateRating(PlayerRating& player,
                  const std::vector<PlayerRating>& opponents,
                  const std::vector<float>& scores) { // 1.0=win, 0.0=loss, 0.5=draw
    // g(RD_j) factor
    auto g = [](float RD) {
        return 1.0f / sqrt(1.0f + 3.0f * RD * RD / (M_PI * M_PI));
    };

    // Expected score
    auto E = [&](float rating, float opponent_rating, float opponent_RD) {
        return 1.0f / (1.0f + exp(-g(opponent_RD) * (rating - opponent_rating) / 400.0f));
    };

    float variance = 0.0f;
    float delta = 0.0f;
    for (size_t i = 0; i < opponents.size(); i++) {
        float e = E(player.rating, opponents[i].rating, opponents[i].deviation);
        variance += g(opponents[i].deviation) * g(opponents[i].deviation) * e * (1.0f - e);
        delta += g(opponents[i].deviation) * (scores[i] - e);
    }
    variance = 1.0f / variance;
    delta *= variance;

    // Update rating
    player.rating += delta;
    // Update deviation (simplified — full Glicko-2 has volatility update)
    player.deviation = 1.0f / sqrt(1.0f / (player.deviation * player.deviation) + 1.0f / variance);
}
```

### Skill Bracketing

```
Rating Range    │ Bracket      │ Max Wait (s) │ Skill Spread Allowance
────────────────┼──────────────┼──────────────┼───────────────────────
0-500           │ Bronze       │ 30           │ 300
500-1000        │ Silver       │ 45           │ 250
1000-1500       │ Gold         │ 60           │ 200
1500-2000       │ Platinum     │ 90           │ 150
2000-2500       │ Diamond      │ 120          │ 100
2500+           │ Master+      │ 300          │ 75
```

### Relaxation Over Time

As wait time increases, constraints relax:

```
t=0s:    Must be same bracket, <50ms ping, same mode
t=30s:   Adjacent bracket allowed, <80ms ping
t=60s:   ±2 brackets, <120ms ping, any mode
t=120s:  Any bracket, <200ms ping, any mode
t=300s:  Any bracket, any ping, any mode — just get them in a game
```

## Latency-Based Matchmaking

Prefer routing players to the datacenter that minimizes worst-case ping:

```cpp
std::string SelectOptimalRegion(
    const std::vector<MatchmakingTicket>& players) {

    struct RegionScore {
        std::string region;
        int max_ping;
        int avg_ping;
    };

    std::vector<RegionScore> scores;
    for (auto& region : AVAILABLE_REGIONS) {
        int max_ping = 0, sum_ping = 0, count = 0;
        for (auto& player : players) {
            if (player.region_pings.contains(region)) {
                max_ping = std::max(max_ping, player.region_pings[region]);
                sum_ping += player.region_pings[region];
                count++;
            }
        }

        // Skip regions where any player has >150ms ping
        if (max_ping > PING_HARD_LIMIT) continue;

        scores.push_back({region, max_ping, sum_ping / count});
    }

    // Pick region with best worst-case ping
    std::sort(scores.begin(), scores.end(),
        [](auto& a, auto& b) { return a.max_ping < b.max_ping; });

    return scores.empty() ? "us-east" : scores[0].region;
}
```

## Party/Group Matchmaking

### Party Formation Rules

1. **Party leader's rating** is the base for matchmaking.
2. **Weighted average** when party skill gap > threshold:
   ```
   party_rating = (leader_rating * 0.6) + (avg_other_ratings * 0.4)
   ```
3. **Hard cap on party skill spread:**
   - Ranked: ±200 rating points (no boosting/smurfing)
   - Casual: ±500 rating points
4. **Party size limits:**
   - 5v5: Max party of 3 in ranked (prevents 5-stack stomping solos)
   - Larger modes: Max party of 50% of team size

### Backfill & Leaver Handling

```cpp
void HandlePlayerLeave(std::string match_id, std::string player_id) {
    auto match = GetMatch(match_id);

    // Option A: End match (competitive)
    if (match.is_ranked) {
        CancelMatch(match_id);
        ApplyLeaverPenalty(player_id);  // Rating loss + timeout
        return;
    }

    // Option B: Backfill (casual)
    auto backfill_ticket = CreateBackfillTicket(match);
    // Inherit match constraints but relax skill requirement
    backfill_ticket.skill_range = match.skill_range * 1.5f;

    // Prioritize backfill over new matches
    // (backfill has shorter expected duration — players want in NOW)
    PriorityMatchmake(backfill_ticket, priority=HIGH);
}
```

## Matchmaker Scalability

### Architecture for Scale

```
                   ┌────────────┐
                   │  API/Edge  │ (Player-facing: join queue, get status)
                   └─────┬──────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
        ┌─────▼─────┐ ┌──▼────┐ ┌──▼──────────┐
        │Matchmaker │ │Match..│ │Matchmaker    │
        │ Shard 1   │ │Shard 2│ │ Shard N      │
        │(EU players)│ │(US)  │ │(AP players)  │
        └─────┬─────┘ └──┬────┘ └──┬───────────┘
              │          │          │
              └──────────┼──────────┘
                         │
                   ┌─────▼─────┐
                   │Game Server│
                   │ Allocator │
                   └───────────┘

Each shard owns a player pool — no cross-shard coordination needed.
Shard assignment: hash(player_id) % num_shards (sticky).
Region-based sharding reduces latency variance within pools.
```

### Performance Targets

| Metric | Target |
|---|---|
| Queue time (90th percentile) | <60 seconds |
| Queue time (99th percentile) | <180 seconds |
| Skill fairness (average spread) | <150 Elo |
| Ping quality (90th percentile) | <80ms |
| Matchmaker throughput | 10,000 matches/minute |
| Backfill speed (casual) | <10 seconds |

## Common Pitfalls

1. **Matching only on skill** — A perfectly balanced 50ms match is worse than a slightly unbalanced 20ms match. Latency is a harder constraint.
2. **No ping measurement before queue** — Player with 200ms ping joins 20ms region. Measure first, queue second.
3. **Starving high-skill players** — Top 1% have tiny pools. Must relax constraints aggressively or they quit.
4. **No backfill for casual** — One leaver ruins 11 other players' experience.
5. **Ignoring party dynamics** — 4-stack + 1 solo vs 5-stack is unfair. Enforce party symmetry.

## References

- "Matchmaking Systems" — Josh Menke (ex-Blizzard, Halo matchmaking), GDC talks
- Glicko-2 Rating System — Mark Glickman, glicko.net
- TrueSkill & TrueSkill2 — Microsoft Research
- OpenMatch: open-match.dev (Google-backed matchmaking framework)
- Amazon GameLift FlexMatch documentation
