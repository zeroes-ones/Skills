# Failure Recovery Patterns

## Pattern 1: Retry with Backoff
```
Agent fails → wait 2s → retry → wait 4s → retry → wait 8s → give up
```
Only for **idempotent** operations.

## Pattern 2: Fallback Agent
```
Agent A fails → Agent A_fallback takes over with same state
```
Requires: fallback agent with same specialization, state checkpoint.

## Pattern 3: Degrade Gracefully
```
Agent C of [A, B, C, D] fails → merge A, B, D results → flag C as incomplete
```
Accept partial results. Document what's missing.

## Pattern 4: Escalate to Human
```
Critical path agent fails → pause topology → notify human with context
```
For non-automatable failures. Present: what failed, why, current state.

## Pattern 5: Checkpoint and Restart
```
Agent fails at turn 25 → load checkpoint from turn 20 → retry from 20
```
Requires: periodic state snapshots during agent execution.
