# loop-reflect.md — Post-Exit Reflection Prompt

**Boundary:** loop complete / run end (node protocol Phase 4)
**Used by:** `iterative-task-execution` (agent after DONE or ESCALATE)
**Reads:** expected plan vs. actual run (run-state log, decisions, iteration counts).

## Behavior rules

Answer four questions concisely:

1. **Expected vs. actual.** What did the plan predict about this node/loop, and what actually
   happened? (Passes used vs. allowed; gate fires vs. expected; criteria that failed unexpectedly.)
2. **What did diagnostics teach?** What did the failures reveal that the initial plan did not
   predict? (This is the loop's real output.)
3. **The one learning.** What single pattern is worth writing to the decision ledger? For library
   authors: which skill's Gotchas should it update?
4. **Calibration.** Was `max_iterations` right, too tight, or too loose? Was the exit condition
   reachable in practice? (Feeds back into `workflow-graph-authoring` budget calibration.)

## Output markers

```
[REFLECT: <node | loop | run>]
  expected: <...>
  actual: <...>
  delta: <passes/gates/criteria delta>
  learning: <one pattern, ledger-ready>
  calibration: <budget too tight | right | too loose — evidence>
```

## Hard rules

- Reflection is 2 minutes, not 20. The discipline is *doing it at every exit*, not doing it deeply.
- Learnings go to the decision ledger as entries with rationale — a reflection nobody can find
  later did not happen.
- Calibration notes are evidence, not opinions: "hit max_iterations in 3 of 3 runs" is a fact;
  "feels tight" is not.
