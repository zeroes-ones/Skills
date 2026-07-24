# Calibration: Finding the Right Repo Granularity

Calibration is the art of choosing the right number of repositories for your team size, architecture, and operational maturity. Too few → monolith pain. Too many → orchestration hell.

## The Granularity Spectrum

```
MONOLITH ←——————————————————————————————→ ATOMIZED
    1 repo                              1 repo per function
    "everything"                        "each lambda"
```

## Calibration Factors

### Team Topology
| Team Count | Recommended Repos | Rationale |
|------------|-------------------|-----------|
| 1-3 teams | 1-5 repos | Monorepo or few repos; coordination is cheap |
| 4-10 teams | 5-20 repos | One repo per team + shared infrastructure |
| 10-30 teams | 20-60 repos | Domain-aligned repos; shared contracts repo |
| 30-100 teams | 60-150 repos | Federated ownership emerges; InnerSource required |
| 100+ teams | 150+ repos | Platform team required; strict governance needed |

### Coupling Heat Map
For each pair of proposed repos, rate coupling on 1-5:
- **1 (Independent):** No shared data, no API calls
- **3 (Loose):** Async events or infrequent API calls
- **5 (Tight):** Synchronous calls, shared schema, must deploy together

**Rule:** If any pair scores 5, they should be the same repo. If all pairs score ≤ 2, split aggressively.

### Change Frequency
```
High change velocity → Co-locate in same repo (easier coordination)
Low change velocity  → Split into separate repo (less noise)
```

Example:
- `contracts/` changes weekly → deserves its own repo (low churn, high blast radius)
- `user-service/` changes daily → keep focused, own repo
- `ci-templates/` changes monthly → perfect for shared repo

## Calibration Checklist

Before creating a new repo, answer YES to at least 4 of these:
- [ ] Does it have a distinct team owner?
- [ ] Can it deploy independently?
- [ ] Does it have its own data store (or clearly share one)?
- [ ] Is its release cadence different from related repos?
- [ ] Would merging it into another repo create > 50k LOC?
- [ ] Does it expose a well-defined API consumed by others?

## Recalibration Triggers

Merge repos back together when:
- Two repos always deploy together (merge them)
- A repo has < 500 LOC and no independent value (absorb it)
- Cross-repo PRs outnumber single-repo PRs (boundary is wrong)

Split repos when:
- A repo has > 5 CODEOWNERS from different teams (split by team)
- CI takes > 15 minutes (split by domain)
- Onboarding requires understanding > 10 unrelated domains (split by bounded context)
