# Failure Mode Prevention

Reference for multi-agent-orchestration SKILL.md — detection and prevention of common failures.

## 1. Hallucination Cascade ($500K+)

**Mechanism:** Agent A hallucinates → Agent B trusts hallucinated output → Agent C amplifies.

**Detection pipeline:**

```python
import numpy as np

def detect_hallucination_cascade(
    outputs: list[dict], threshold: float = 0.3
) -> bool:
    for i in range(1, len(outputs)):
        prev_claim = embed(outputs[i-1]["claim"])
        curr_claim = embed(outputs[i]["claim"])
        similarity = cosine_similarity(prev_claim, curr_claim)
        if similarity < threshold:
            log_alert(f"Cascade at agent {i}: similarity={similarity:.2f}")
            return True
    return False
```

**Prevention:** Cross-reference check after every handoff. If consistency < 0.7, inject
independent verification agent before continuing chain.

## 2. State Corruption ($100K+)

**Mechanism:** Agent A mutates shared state → Agent B reads stale/wrong value.

**Prevention:**

```python
from hashlib import sha256
import json

class StateGuard:
    @staticmethod
    def seal(state: dict) -> str:
        return sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()[:16]

    @staticmethod
    def verify(state: dict, expected_hash: str) -> bool:
        actual = StateGuard.seal(state)
        if actual != expected_hash:
            raise StateCorruptionError(f"Expected {expected_hash}, got {actual}")
        return True
```

**Rule:** Seal state hash on handoff send; verify on receipt. Mismatch → reject handoff,
replay from last verified checkpoint.

## 3. Infinite Delegation Loop ($50K+)

**Mechanism:** Agent A → B → C → A (cycle) or unbounded depth recursion.

**Detection:**

```python
class LoopDetector:
    def __init__(self, max_depth: int = 5):
        self.visited = set()
        self.max_depth = max_depth

    def check(self, source: str, target: str, depth: int):
        edge = (source, target)
        if edge in self.visited:
            raise InfiniteLoopError(f"Cycle: {edge}")
        if depth >= self.max_depth:
            raise DelegationDepthExceeded(f"Depth {depth} >= {self.max_depth}")
        self.visited.add(edge)
```

## 4. Debate Stagnation ($30K+)

**Mechanism:** Proposer and Critic iterate past optimal without convergence.

**Prevention:**

```python
def check_debate_convergence(
    rounds: list[dict], threshold: float = 0.05, stagnation: int = 2
) -> bool:
    if len(rounds) > stagnation:
        recent = rounds[-stagnation:]
        deltas = [abs(recent[i]["score"] - recent[i-1]["score"])
                  for i in range(1, len(recent))]
        if all(d < threshold for d in deltas):
            return True  # Converged — stop debate
    return False
```

## 5. Context Window Overflow ($20K+)

**Mechanism:** Long delegation chain appends to message history → overflow → truncation.

**Prevention:**

```python
def summarize_on_handoff(state: dict) -> dict:
    return {
        "summary": compress(state["messages"][-50:]),  # Last 50 messages
        "decisions": state["decision_log"][-10:],      # Last 10 decisions
        "current_state": state["agent_outputs"],
        "handoff_hash": StateGuard.seal(state)
    }
```

## Failure Mode Matrix

| Failure | Impact | Detection | Prevention |
|---------|--------|-----------|------------|
| Hallucination cascade | $500K+ | Similarity < 0.3 | Cross-ref check |
| State corruption | $100K+ | Hash mismatch | Seal + verify |
| Infinite loop | $50K+ | Cycle/hit max depth | Visited set + counter |
| Debate stagnation | $30K+ | Delta < threshold x2 | Convergence guard |
| Context overflow | $20K+ | Token count > limit | Summarize on handoff |
