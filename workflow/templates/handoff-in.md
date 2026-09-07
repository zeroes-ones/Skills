# handoff-in.md — Handoff Intake Prompt (Node Entry)

**Boundary:** INTAKE (node protocol Phase 0)
**Used by:** `iterative-task-execution` (downstream agent starting a node)
**Reads:** incoming handoff payload + run-state.

## Behavior rules

Before touching any work, answer three questions in order:

1. **What did I receive?** List the payload's artifacts and the state fields relevant to this
   node. Confirm the paths exist and the hashes match. If hashes mismatch or files are missing,
   STOP and report corruption — do not start.
2. **What do I owe?** Restate this node's outputs from the manifest (`outputs:`) or the skill's
   `workflow:` contract. If this node has no declared outputs, restate the request.
3. **What did upstream leave open?** Enumerate `open_questions`. Every one is either resolved (and
   logged as a decision) or carried forward in this node's own open_questions. None may silently
   vanish.

## Output markers

```
[INTAKE: received <n> artifacts (sha ok|mismatch), <k> open questions]
  owe: <node outputs / request>
  open: <carried-forward items>
[INTAKE RESULT: proceed | blocked-corruption | blocked-missing-input]
```

## Hard rules

- Refusal is a valid outcome. Missing artifacts or a hash mismatch ⇒ `blocked-corruption` with a
  request to replay from the last verified checkpoint. Starting anyway bakes corruption into your
  output.
- If upstream's `summary` disagrees with the artifacts you actually received, trust the artifacts
  and flag the disagreement in your intake marker — do not silently reconcile.
- Downstream must never re-derive what upstream already produced. If you find yourself rebuilding
  context from scratch, the handoff failed; say so rather than paying the cost silently.
