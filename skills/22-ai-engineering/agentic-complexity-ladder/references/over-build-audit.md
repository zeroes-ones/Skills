# Over-Build Audit

<!-- STANDARD: 3min -- the removal audit, and reading a graph for unjustified nodes -->

## The premise

An over-built system **works**. That is what makes it hard to find: nothing fails, so nothing prompts
an investigation. The audit therefore has to be scheduled, not triggered by a symptom.

**The audit's question, per node:** *which measured failure of a simpler design does this address?*
A node that cannot answer is a removal candidate, and the answer is obtained by testing, not by
discussion.

## Reading a design for candidates

| Candidate | Signal | The test |
|---|---|---|
| The "quality" node with no eval | no failing case points at it | remove it; does the eval pass? |
| The pass-through node | its output resembles its input | bypass it; is the eval unchanged? |
| The duplicate node | its work is derivable from a neighbour | merge them; does the eval hold? |
| The always-succeeding parallel block | the aggregation is dead code | serialise; is latency still acceptable? |
| The never-iterating loop | `max_iterations` is never approached | replace with a single step |
| The orchestrator over an enumerable decomposition | 20 inputs decompose the same way | replace with a chain |
| The router with unmeasured accuracy | routing accuracy was never measured | measure it; merge unreliable paths |
| The always-passing gate | it has never failed | is it verification, or decoration? |

**The last row is subtle.** A gate that has never failed may be a gate nobody has tested, or a check
that cannot fail. Either way it is not providing the assurance it appears to.

## The graph-specific tells

| Tell | What it means |
|---|---|
| One node contains the whole prompt; the others are pass-throughs | a single call wearing a manifest |
| No node has a `workflow:` contract | verification is not in use → why the engine? |
| No budgets declared | enforcement is not in use |
| No gates or escalation paths | the escalation justification does not apply |
| Nodes always run in strict sequence, with no conditionals | a chain, at higher cost |
| The manifest changes more often than the prompts | the graph is being used as configuration |
| More nodes than distinct failure modes | some nodes have no failure to address |

**The last tell is the general heuristic:** a node exists to address a failure. If the system has fewer
named failures than nodes, at least some nodes are unjustified.

## The audit procedure

```text
For each node/rung, in reverse order (last added first):

1. ASK: which measured failure of a simpler design does this address?
   ├── Cannot name one  → REMOVAL CANDIDATE. Go to step 2.
   └── Can name one     → is the failing case still in the eval?
       ├── Yes → justified. Record the case. Leave it.
       └── No  → the evidence was lost. Go to step 2.

2. TEST BY REMOVAL:
   a. Record the control: eval result, cost, latency
   b. Remove or bypass the node
   c. Re-run the SAME eval (same task set, model, price basis)
   d. Decide:
      eval passes, cost/latency better  → remove it. Record the win.
      eval passes, nothing changed      → free complexity. Remove it anyway.
      eval fails                        → justified. Record the failing case and keep it.

3. IF REMOVED: confirm once more against noise, then delete the eval case the
   node tested.

4. RECORD: what was removed, why, and the measured delta.
```

**The middle outcome in step 2d is worth acting on.** A node that costs nothing and changes nothing is
still code to read, review and maintain — and it will mislead the next engineer about why it exists.

## Reading a manifest alongside its failures

The most efficient audit compares two lists:

```text
List A: the nodes in the manifest
List B: the measured failures the system was built to address

For each node in A: does a failure in B point at it?
For each failure in B: does a node in A address it?

Nodes with no failure  → removal candidates
Failures with no node  → the system does not actually address what it was built for
```

**The second mismatch is the more serious one**, and the audit is often the first time it is noticed:
a system built to fix six failures, of which the manifest addresses four — and two nodes address
failures that were never observed.

## The cost of an over-built system

| Cost | Where it appears |
|---|---|
| Run cost | extra calls per run, every run |
| Latency | extra round trips |
| Failure modes | each node can fail in its own way |
| Maintenance | a manifest to update alongside prompts |
| Onboarding | the structure must be learned |
| Review burden | every node is reviewed on every change |
| False assurance | gates and budgets that nothing exercises |

**The false-assurance row is the one teams do not notice.** A budget that cannot trip, or a gate that
cannot fail, reads as a control that is operating — and the absence of the control is discovered when
it was needed.

## Reporting an audit

```text
Over-build audit — <workflow> — <date>

Nodes audited:  6
Justified:      4  (each names a measured failure with an eval case)
Removal tested: 2
  ├── node "normalise"  → eval passed without it; cost −$0.0096/run  → REMOVED
  └── node "validate-2" → eval FAILED without it (case 14); kept, case recorded

Failures with no addressing node:
  - "long inputs truncate" — reported 2026-06, no node addresses it  ← ACTION

Net: run cost $0.0610 → $0.0514 (−15.7%), latency 2.9 → 2.4 s, eval held at 94%.
```

Both lists appear in the report: what was removed, and what is unaddressed. The second is what turns an
audit from a cleanup exercise into a design review.

## Cadence

| Trigger | What runs |
|---|---|
| Quarterly | the full per-node audit above |
| On a model change | re-test the removals, since a stronger model may absorb a node |
| On a requirement change | re-check whether any justification still applies |
| On an incident | was a node involved that has no failure to address? |
| Before a major cost reduction target | the audit is where the reductions are |

**The model-change trigger is underused.** A node added because a model could not do X may be
unnecessary once it can — and nothing else reveals that.

## Checklist

- [ ] The audit is scheduled, not triggered by a symptom
- [ ] Every node is asked which measured failure it addresses (R6)
- [ ] Nodes that cannot answer become removal candidates, tested by removal
- [ ] The removal test holds the task set, model and price basis constant
- [ ] Cost, latency and quality deltas are all measured for each removal
- [ ] Both mismatches are reported: nodes with no failure, and failures with no node
- [ ] The eval case a removed node tested is deleted
- [ ] Removals are recorded, so the old design is not reconstructed from memory
