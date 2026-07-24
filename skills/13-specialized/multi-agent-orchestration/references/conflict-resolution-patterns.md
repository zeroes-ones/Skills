# Conflict Resolution Patterns

Reference for multi-agent-orchestration SKILL.md — voting, override, consensus, escalation.

## Resolution Ladder

```
DISAGREEMENT (N agents, K opinions)
    │
    ├── STEP 1: Simple Majority
    │   ├── N >= 3, majority > 50% → RESOLVED
    │   └── No majority → STEP 2
    │
    ├── STEP 2: Weighted Voting
    │   ├── Senior agents 2x weight
    │   ├── Majority with weights → RESOLVED
    │   └── Still deadlocked → STEP 3
    │
    ├── STEP 3: Supervisor Override
    │   ├── Supervisor decides → DECIDED (logged)
    │   └── Budget > threshold → STEP 4
    │
    └── STEP 4: Human Escalation
        ├── Present: options, reasoning, vote distribution
        └── Human decision → RESOLVED (recorded)
```

## 1. Simple Majority Voting

```python
from collections import Counter

def simple_majority(votes: list[str], threshold: float = 0.5) -> str | None:
    counter = Counter(votes)
    total = len(votes)
    winner, count = counter.most_common(1)[0]
    return winner if count / total > threshold else None
```

**When:** Low-stakes decisions (style choices, naming), 3+ agents.
**Limit:** Fails with even number of agents or polarized opinions.

## 2. Weighted Voting

```python
def weighted_vote(opinions: list[tuple[str, float]]) -> str:
    """opinions: [(decision, weight), ...]"""
    scores = {}
    for decision, weight in opinions:
        scores[decision] = scores.get(decision, 0) + weight
    return max(scores, key=scores.get)
```

**When:** Agents have different expertise levels, seniority matters.

## 3. Consensus Threshold (2/3 Quorum)

```python
def consensus(votes: list[str], quorum: float = 0.67) -> str | None:
    counter = Counter(votes)
    total = len(votes)
    winner, count = counter.most_common(1)[0]
    return winner if count / total >= quorum else None
```

**When:** Architecture decisions, security choices, irreversible actions.

## 4. Supervisor Override

```python
def supervisor_override(agent_votes: Counter, supervisor_decision: str) -> str:
    log_override(agent_votes, supervisor_decision)
    return supervisor_decision
```

**When:** Deadline pressure, clear authority hierarchy.

## 5. Human-in-the-Loop Escalation

```python
def escalate(conflict: dict) -> dict:
    return {
        "status": "blocked",
        "options": conflict["options"],
        "agent_reasoning": conflict["reasoning"],
        "vote_distribution": conflict["votes"],
        "budget_impact": conflict["budget"],
        "sla": "15 minutes"
    }
```

**When:** Budget > threshold, P0 criticality, irreversible actions.
**Trigger:** Any decision with `cost_impact > $5,000` or `criticality == "P0"`.

## Resolution Strategy Selection

| Decision Type | Strategy | Quorum | Escalation |
|--------------|----------|--------|------------|
| Naming/style | Simple majority | 50% | Never |
| Implementation | Weighted vote | 50% | If deadlocked |
| Architecture | Consensus | 67% | Always available |
| Budget > $5K | Supervisor | N/A | Mandatory |
| Security/P0 | Consensus + human | 67% | Mandatory |
