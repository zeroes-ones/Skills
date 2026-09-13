# Exit Criteria

<!-- DEEP: 5+min -- writing the return path at the moment of climbing, and re-evaluating -->

## Why exit criteria are the load-bearing part

Entry criteria get all the attention because they justify the build. **Exit criteria are what keep the
system maintainable** — and they are written at entry, because that is the only moment when the reason
for climbing is actually known.

```text
Climb now:  "we need routing because 3 of 20 cases are invoice inputs and all 3 fail"
             → recorded

Two years on: nobody remembers why the router exists, so nobody removes it
             → the reason disappeared (the invoice path was rebuilt upstream)
             → the router is now pure cost: a classify call, N paths to maintain,
               a misroute failure mode, and a maintenance liability
```

That is the failure R4 prevents, and it is the normal outcome without an exit condition.

## What makes a good exit condition

It must be **falsifiable** and **checkable**, which rules out most of what gets written.

| Good exit condition | Why it works |
|---|---|
| "if mean input length halves, re-test the single call" | measurable, and a real trigger |
| "if invoice traffic drops below 5% of total, retire the routed path" | measurable |
| "if the decomposition becomes enumerable from observed inputs, replace the orchestrator with a chain" | checkable by the 20-input test |
| "if the governance requirement is lifted, remove the graph" | specific and dated |

| Bad exit condition | Why it fails |
|---|---|
| "if it is no longer needed" | not falsifiable — nothing can check it |
| "revisit in a year" | a date with no condition attached |
| "if performance becomes a problem" | every system has a performance problem eventually |
| "when the team has time" | never |
| "if the model improves" | models always improve; the condition does not say by how much or what would then be true |

**The test:** could someone other than the author check this condition and get a yes/no? If not, it is
an aspiration.

## The exit condition per rung

| Rung | Exit condition | How to check |
|---|---|---|
| **2 Chain** | the model's usable context doubles, or mean input length halves | re-run the single call on the same task set |
| **3 Routing** | a class's traffic falls below a threshold, or the classes stop being separable | count traffic per class; re-run the clustering test |
| **4 Parallel** | the aggregation cost exceeds the latency saved, or branches become dependent | measure the aggregation's share of runtime |
| **5 Orchestrator** | the decomposition becomes enumerable from observed inputs | decompose 20 inputs by hand; do they repeat? |
| **6 Graph** | the governance or audit requirement is lifted, or the workflows are retired | the requirement's owner confirms |

Each is a *measurement plus a threshold*, which is what makes it checkable.

## The re-evaluation cadence

An exit condition that is never checked is the same as no exit condition.

| Cadence | What runs |
|---|---|
| Per release | the rungs' evals, so a rung that no longer helps is visible in the deltas |
| Quarterly | the exit conditions themselves, against their recorded thresholds |
| On a trigger | a model change, a task-set change, a traffic-shape change, a requirement change |
| Annually | a full rung audit — every node names its failure, or it is a removal candidate |

**The trigger-based checks matter most.** A rung's justification often disappears not on a schedule but
because something changed: the task set grew, one input class became dominant, a model absorbed the
job the chain was doing. Those are the moments the exit condition is met, and nothing detects them
except a check tied to the trigger.

## De-escalation as an engineering win

Removing a rung that has outlived its reason is a **strict improvement**:

| Metric | Before | After | Why |
|---|---|---|---|
| Cost | N calls | fewer | fewer steps |
| Latency | multiplied | shorter | fewer round trips |
| Failure modes | N + the rung's own | fewer | fewer things to break |
| Debuggability | the rung's structure to learn | less to learn | less code to read |
| Security surface | more actions, more data in more prompts | smaller | fewer places to be wrong |

There is no metric on which a justified removal is worse. It should be reported as a win, not as a
retreat — teams that treat de-escalation as an admission of failure keep the complexity forever.

## The removal audit

The cheapest way to find out whether a rung is still needed: **take it out and run the eval.**

```text
1. Record the current eval result (quality, cost, latency) — the control.
2. Remove or bypass the rung.
3. Re-run the same eval on the same task set.
4. Compare:
   ├── eval passes and cost/latency improved  → remove it. Record the win.
   ├── eval passes and nothing changed        → it was free complexity; remove it anyway
   └── eval fails                             → it was justified. Record the failure it
                                                fixes and the eval case, and KEEP it.
5. If removed, re-run once more to confirm the result was not noise.
```

**Why removal beats argument:** a debate about whether a node is needed can run for weeks and end
inconclusively. A removal test answers it in an hour, with evidence, and the answer is checkable by
anyone.

**Step 4's middle case is worth noticing:** a rung that costs nothing measurable and changes nothing is
still worth removing, because it is code to read, review and maintain — and it will confuse the next
engineer about why it exists.

## What de-escalation must not do

| Requirement | Why |
|---|---|
| The eval must pass on both sides | a simpler system that regresses is not a win |
| The cost and latency change must be measured | the point is to show the improvement |
| A downstream consumer must be checked | a contract change may break a caller |
| The removal is recorded | so it is not re-added by someone reconstructing the old design |
| The failing eval case is deleted with the rung | or it will fail forever against a design that does not need it |

The last row is easy to forget and produces a permanently red test that nobody understands.

## Recording a de-escalation

```text
De-escalation: removed Rung 3 (routing) from <workflow>
Reason:        exit condition met — invoice traffic fell from 15% to 1.2% of total

Control:  eval 94% pass, $0.061/run, 2.9 s
After:    eval 94% pass, $0.052/run, 2.5 s

Method:  same task set (40 cases), same model, same price basis
Verdict: eval holds, cost −14.8%, latency −13.8% → removal adopted
Removed: the classify call, 2 routed paths, 1 misroute failure mode, 1 eval case
```

The `Removed` line is the part that makes the win legible: it names what the system no longer has to
carry.

## Checklist

- [ ] Every rung has an exit condition written at climb time (R4)
- [ ] Each exit condition is falsifiable and checkable by someone other than its author
- [ ] Each has a threshold or a specific trigger, not a date alone
- [ ] Re-evaluation runs on a cadence, and on the relevant triggers
- [ ] Removals are audited by testing removal, not by argument
- [ ] A removal requires the eval to pass on both sides
- [ ] De-escalation is reported as a win, with the removed machinery named
- [ ] The failing eval case is deleted along with the rung it tested
