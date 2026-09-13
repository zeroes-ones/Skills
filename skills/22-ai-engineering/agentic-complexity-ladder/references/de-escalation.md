# De-escalation

<!-- STANDARD: 3min -- auditing by removal, and simplifying without a regression -->

## The principle

**Removing a rung that has outlived its reason is an engineering win, not a retreat.** There is no
metric on which a justified removal is worse: cost falls, latency falls, failure modes fall, code to
read falls, and the security surface shrinks.

The reason it does not happen is social, not technical: complexity feels like progress, and removing
it reads as admitting the previous decision was wrong. The counter is to make removal the *normal*
outcome of the audit, expected rather than embarrassing.

## The removal audit

The cheapest, most convincing test of whether a rung is needed.

```text
1. Control:  record the eval result on the real task set
             (quality, cost, latency — all three)
2. Remove:   take the rung out, or bypass it
3. Measure:  re-run the SAME eval, same task set, same model, same price basis
4. Decide:
             eval passes, cost/latency better   → remove. Record the win.
             eval passes, nothing changed       → it was free complexity. Remove it.
             eval fails                          → it was justified. Keep it, and record
                                                   the eval case as its evidence.
5. Confirm:  if removed, re-run once to rule out noise
```

**Why this beats argument:** a debate about whether a node is needed can run weeks and end
inconclusively. A removal test answers it in an hour with evidence anyone can re-check. Make it the
default audit, not a special effort.

## Reading a design for removal candidates

| Candidate | Signal | Test |
|---|---|---|
| A node that "improves quality" with no eval | no failing case points at it | remove it; does the eval pass? |
| A node whose work another implies | its output is derivable from a neighbour's | bypass it; is the eval unchanged? |
| A router with unreliable classification | routing accuracy is unmeasured or low | merge the paths; does the eval hold? |
| A parallel block whose aggregation always succeeds | aggregation is dead code | serialise it; is latency still acceptable? |
| An orchestrator over an enumerable decomposition | 20 inputs decompose the same way | replace with a chain |
| A chain link that passes through unchanged | its output resembles its input | remove the link |
| A graph for a task the lower rungs serve | no governance/repeatability requirement | run it as a workflow |

**The first row is the most common.** A node added for "quality" with no eval attached has no evidence
behind it, and removal tests that.

## Simplifying without a regression

| Requirement | Why |
|---|---|
| Measure quality on both sides | a simpler system that regresses is not a win |
| Hold the task set constant | a changed set makes the comparison meaningless |
| Hold the model and price constant | otherwise the delta includes the model change |
| Report the cost, latency and quality deltas | the win must be legible, not asserted |
| Check downstream consumers | a contract change may break a caller |
| Delete the eval case the rung tested | or it fails forever against a design that does not need it |
| Record the removal and its reason | so the old design is not reconstructed from memory |

**The sixth row is the one that gets forgotten**, and it leaves a permanently red test that the next
engineer will either disable or spend a day investigating.

## The order of operations

```text
1. Remove FIRST, rewrite only if removal is impossible.
   Subtracting a rung is safer than reworking it in place: no new code, no new
   failure modes, and the eval tells you immediately whether it was needed.

2. Prefer the largest removal that the eval permits.
   Removing a router (and its paths) beats optimising the router.

3. One removal at a time.
   Two removals at once means neither delta is attributable (the same rule as
   climbing, R3, applied downward).

4. Re-run the eval before committing.
   A removal that fails the eval is a revert, not a lesson.
```

## Reporting a de-escalation

```text
De-escalation: <workflow> — removed Rung 3 (routing)
Reason:        exit condition met (invoice traffic 15% → 1.2%)

Control:   eval 94% | $0.0610/run | 2.9 s
After:     eval 94% | $0.0523/run | 2.5 s
Delta:     quality 0 | cost −14.3% | latency −13.8%

Method:    same 40-case set, same model, same price basis (<date>)
Removed:   1 classify call, 2 routed paths, 1 misroute failure mode, 1 eval case
Verdict:   adopted
```

The `Removed` line is what makes de-escalation legible to the organisation: it names the machinery the
system no longer carries. Without it, the change reads as "we deleted some code" rather than "we
removed a maintenance liability and a failure mode".

## When NOT to de-escalate

| Situation | Why removal is wrong |
|---|---|
| The eval fails without the rung | it is justified; record the failing case as its evidence |
| A governance or audit requirement exists | the requirement is the justification, not the outcome |
| The rung is load-bearing for a consumer | a contract change needs coordination, not a quiet removal |
| The volume is about to rise measurably | the exit condition has not been met yet; wait for the measurement |
| The team cannot run the eval | without it, removal is a guess — build the eval first |

**The last row is a common trap.** Removing complexity without an eval is not simplification; it is an
unmeasured change with a worse failure profile (a regression is silent rather than caught).

## The quarterly rung audit

```text
For every rung in every production workflow:
  1. Can someone name the measured failure it addresses?
     ├── Yes → is the failing case still in the eval?
     │   ├── Yes → it is justified. Leave it.
     │   └── No  → the evidence was lost. Re-test by removal.
     └── No  → removal candidate. Test it.
  2. Has the exit condition been met?
     ├── Yes → remove it.
     └── No  → is the condition still checkable?
         ├── Yes → leave it, dated.
         └── No  → rewrite the condition, or acknowledge permanent complexity.
```

**Outcome of a healthy audit:** some rungs justified and confirmed, some removed, and a short list of
exit conditions still pending. An audit that removes nothing every quarter is either a very stable
system or an audit that is not really running.

## Checklist

- [ ] Removal is the default audit, not a special effort
- [ ] Every removal is measured against the eval on both sides
- [ ] The task set, model and price basis are held constant
- [ ] One removal at a time, so the delta is attributable
- [ ] Cost, latency and quality deltas are all reported
- [ ] Downstream consumers are checked before a contract change
- [ ] The eval case the rung tested is deleted along with it
- [ ] De-escalation is reported as a win, with the machinery removed named
- [ ] A quarterly audit runs, and can name what it removed
