# Parallelism Thresholds

<!-- STANDARD: 3min -- sectioning versus voting, and when aggregation is the cost -->

## Two forms, two purposes, not interchangeable

| Form | Shape | Buys | The metric it improves |
|---|---|---|---|
| **Sectioning** | one task split into independent subtasks, run concurrently, results combined | **latency** | wall-clock time |
| **Voting** | the same task run N times, results aggregated | **reliability** | accuracy, via redundancy |

**The trap:** adding parallelism for a *quality* problem. Neither form improves a single run's accuracy
by doing the work better — sectioning splits the work, and voting repeats it. A quality shortfall needs
a different rung, and parallelism will add cost and failure modes while leaving it unaddressed.

## Sectioning: when it works

| Requirement | Why |
|---|---|
| Genuinely independent subtasks | dependent subtasks cannot run concurrently |
| No shared mutable state between branches | otherwise the concurrency is a correctness bug |
| A combination step that is cheaper than the work | otherwise aggregation dominates |
| Branch latencies that are comparable | total latency equals the **slowest** branch, so one slow branch wastes the rest |

**The last row is the arithmetic that decides it:**

```text
serial:     1.0 + 1.0 + 1.0 + 1.0     = 4.0 s
parallel:   max(1.0, 1.0, 1.0, 1.0)   = 1.0 s   → 4× faster

but with one slow branch:
serial:     1.0 + 1.0 + 1.0 + 9.0     = 12.0 s
parallel:   max(1.0, 1.0, 1.0, 9.0)   =  9.0 s   → only 1.33× faster
```

**The slowest branch sets the floor.** Where branch latencies vary widely, section the fast work and
handle the slow branch separately, or the parallelism buys little.

## Voting: when it works

| Requirement | Why |
|---|---|
| Failures are **uncorrelated** | correlated failures repeat, and repetition does not fix them |
| A defensible aggregation policy | majority, first-success, or a weighted vote — it is code to write and test |
| The value of correctness exceeds N× the cost | voting multiplies spend by N |
| The outcome is checkable | without verification, the vote is a popularity contest among errors |

**The correlation test is decisive:**

```text
Uncorrelated failures (voting helps):
  run 1 wrong on case 7, run 2 wrong on case 12, run 3 wrong on case 3
  → majority vote on each case: 2 of 3 correct → majority is right

Correlated failures (voting does not help):
  all three runs wrong on case 7, for the same reason (a prompt gap)
  → majority vote: 3 of 3 wrong → majority is confidently wrong
```

A model's failures are often correlated — the same prompt gap breaks the same cases every time. So
voting frequently buys less than its N× cost suggests, and the correlation must be **measured** before
committing.

## The aggregation policy

The hidden cost, and the place partial failures surface.

| Policy | Use | Failure handling |
|---|---|---|
| **All must succeed** | every branch's output is required | any failure fails the whole operation |
| **Majority** | voting | a tie must be broken — state how |
| **First success** | any valid result suffices | the others are wasted work |
| **Weighted** | branches have different reliability | the weights must be justified |
| **Best of N (judged)** | a model or rule picks | an extra call, and a judge to trust |

**Decide the policy before building the parallel block.** An undecided policy is discovered at the
first partial failure, in production, under pressure.

## The cost arithmetic

```text
sectioning:  cost = sum(branch costs) + aggregation cost
             latency = max(branch latencies) + aggregation latency

voting:      cost = N × per-run cost + aggregation cost
             accuracy improves only if failures are uncorrelated
```

**Parallelism multiplies cost.** Sectioning does not (the same total work is done, concurrently), but
voting does (the same work is done N times). That asymmetry is worth stating explicitly, because
"make it parallel" is often said without distinguishing the two.

## When parallel is the wrong rung

| Situation | Better |
|---|---|
| The problem is accuracy, not latency or reliability | a better prompt, a stronger model, or retrieval |
| Branches are dependent | a chain (Rung 2) |
| One branch dominates the latency | handle the slow branch separately |
| Failures are correlated | voting will not help; fix the shared cause |
| N× cost is not justified by the accuracy gain | do not vote |
| The aggregation is as expensive as the work | it is not a saving |

## Recording a parallel decision

```text
Rung:      4 (parallelisation — sectioning)
Baseline:  Rung 2 chain — 12.0 s mean latency, quality acceptable
Problem:   LATENCY, not quality (stated explicitly)
Sections:  3 independent document sections, mean 3.8 s each, variance ±0.4 s
Policy:    all-must-succeed; any branch failure fails the operation
Trade:     cost unchanged (same total work), latency 12.0 → 4.2 s
New failure mode: partial failure — 2 sections succeed, 1 fails
Test:      a branch failure produces a clean operation failure, not a partial output
Exit:      if branch latencies diverge beyond 2×, revisit the sectioning (check 2027-01)
```

The `Problem: LATENCY` line is the load-bearing one — it is what distinguishes a justified parallel
block from one added for quality, which is the common mistake.

## Checklist

- [ ] The problem is latency (sectioning) or reliability (voting), not quality — stated explicitly
- [ ] Sections are genuinely independent, with no shared mutable state
- [ ] Branch latencies are comparable, or the slow branch is handled separately
- [ ] For voting, failure correlation was **measured**, not assumed
- [ ] The aggregation policy is decided and tested before the block is built
- [ ] The cost arithmetic is stated (sectioning is ~flat; voting is N×)
- [ ] The partial-failure mode has a test and a defined behaviour
- [ ] An exit condition exists, tied to latency spread or the correlation result
