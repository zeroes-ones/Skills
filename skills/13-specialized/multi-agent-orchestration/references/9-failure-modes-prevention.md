## 9. Failure Modes & Prevention

### 9.1 Hallucination Cascade

**Pattern:** Agent A hallucinates → Agent B uses hallucinated output → Agent C amplifies → cascading wrong decisions.

**Detection:**

```python
def detect_cascade(outputs: list[dict], threshold: float = 0.3) -> bool:
    for i in range(1, len(outputs)):
        consistency = cosine_similarity(
            embed(outputs[i-1]["claim"]),
            embed(outputs[i]["claim"])
        )
        if consistency < threshold:
            return True  # Cascade detected — halt and verify
    return False
```

**Prevention:** Inter-agent consistency check after every handoff. If consistency < 0.7, inject verification step before continuing.

### 9.2 State Corruption Across Handoffs

**Pattern:** Agent A mutates shared state → Agent B reads stale value → decision based on wrong state.

**Prevention:**

```python
def verify_state_integrity(handoff: AgentHandoff) -> bool:
    expected_hash = handoff.handoff_id
    actual_hash = sha256(
        json.dumps(handoff.state_snapshot, sort_keys=True).encode()
    ).hexdigest()[:16]
    return expected_hash == actual_hash
```

### 9.3 Infinite Delegation Loop

**Pattern:** Agent A → B → C → A (cycle) or unbounded depth recursion.

**Detection:**

```python
visited = set()
def delegate(current: str, target: str, state: dict):
    edge = (current, target)
    if edge in visited:
        raise InfiniteLoopError(f"Cycle detected: {edge}")
    if state["delegation_depth"] >= MAX_DEPTH:
        raise DelegationDepthExceeded(state["delegation_depth"])
    visited.add(edge)
    state["delegation_depth"] += 1
```

### 9.4 Debate Topology Indefinite Refinement

**Pattern:** Proposer and Critic iteratively "improving" past optimal without convergence check.

**Prevention:** Configure convergence guards:

```python
DEBATE_CONFIG = {
    "max_rounds": 5,
    "improvement_threshold": 0.05,  # 5% delta minimum
    "stagnation_rounds": 2,         # Halt after 2 rounds with no improvement
}
```
