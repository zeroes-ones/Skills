# Loop Detection Patterns

Detect and break unproductive agent loops before they consume context budget.

## Core Algorithm: Action-Outcome Hashing

```python
def detect_loop(action_history, window=10, max_repeats=3):
    """Return (is_loop, pattern) if detected."""
    recent = action_history[-window:]
    for i in range(len(recent) - max_repeats + 1):
        chunk = recent[i:i+max_repeats]
        if len(set(chunk)) == 1:
            return True, chunk[0]
    return False, None
```

## Loop Type 1: Identical Action-Outcome
- **Pattern:** Agent repeats same action expecting different result
- **Hash:** `sha256(action + outcome)`
- **Threshold:** 3 identical hashes in 10-turn window
- **Response:** Halt; inject "This approach has failed 3x — escalate or pivot"

## Loop Type 2: Oscillation
- **Pattern:** Agent alternates between 2 approaches (A→B→A→B)
- **Detection:** Track state transitions; detect A→B→A cycles
- **Threshold:** 3 full oscillation cycles (A→B→A counts as 1)
- **Response:** Force decision; present both options with cost estimates

## Loop Type 3: Expanding Search
- **Pattern:** Agent widens scope without converging: searches 3→5→8→12 files
- **Detection:** Monitor search breadth per turn; increasing despite no progress
- **Threshold:** Search breadth grows > 50% across 5 turns with zero actionable outputs
- **Response:** Narrow scope; require explicit NARROWING before further expansion

## Escalation Context Injection
When a loop is detected, inject structured context:
```
[LOOP_DETECTED] type=<TYPE> turns=<N> pattern=<HASH>
[ESCALATION] Last 3 outcomes were identical — this approach is not converging.
[REQUIRED] Choose: (1) ESCALATE to human, (2) PIVOT to alternative strategy,
           (3) NARROW scope to single sub-problem
```

## Prevention Patterns
1. **Diverge-on-repeat:** After any 2 identical outcomes, force strategy change
2. **Max-depth gate:** Limit recursion/iteration depth (default: 10)
3. **Timeout decay:** Per-turn timeout decreases by 20% each cycle
4. **Novelty check:** Reject actions with < 5% token difference from prior actions
