# Entry Criteria

<!-- STANDARD: 3min -- the measured failure each rung entry requires -->

## The rule

**No rung without a measured failure of the rung below** (R1, R6). The failure is the justification;
the measurement is the evidence. Both are required, and the measurement must exist *before* the climb.

## The general shape

```text
entry to Rung N requires:
  1. Rung N−1 exists and ran on the REAL task set
  2. Rung N−1 was measured on quality (and cost, and latency)
  3. Rung N−1 fails in a specific, named way on specific cases
  4. The failure maps to what Rung N buys
  5. The failing cases are recorded — they become Rung N's eval
```

Step 5 matters: **the failing cases become the new rung's acceptance test.** A climb without them has
no way to show it worked.

## Per-rung entry criteria

### Rung 2 — Chain

| Require | Because |
|---|---|
| A measured single-call baseline | the chain is a response to a measured shortfall |
| The failure is "one pass is insufficient", not "the format is wrong" | a format fix is still Rung 1 |
| Failing cases recorded | they become the chain's eval |

**Not sufficient to enter:** "the task is long". Long tasks can be one call if the context fits.

### Rung 3 — Routing

| Require | Because |
|---|---|
| A measured chain baseline | the chain must be shown worse for some inputs |
| Failures that **cluster by input class** | routing is separation of concerns; if the failures do not cluster, there is nothing to separate |
| A separable classification | if you cannot reliably tell the classes apart, the router will misroute |
| Per-class traffic counts | a path for 2% of traffic costs as much to maintain as a path for 50% |

**The clustering test is decisive.** If failures are randomly distributed across inputs, a router
cannot help — the failure is in the work, not in the input class.

### Rung 4 — Parallelisation

| Require | Because |
|---|---|
| A measured serial baseline with a **latency** or **reliability** problem | that is what parallelisation buys; nothing else |
| Genuinely independent subtasks (sectioning) | dependent subtasks cannot run concurrently |
| Uncorrelated failures (voting) | correlated failures are not fixed by repetition |
| An aggregation policy decided | all/majority/first-success is code to write and test |

**The trap:** adding parallelism for a *quality* problem. Parallelism buys latency and reliability,
not accuracy — a quality shortfall needs a different rung.

### Rung 5 — Orchestrator

| Require | Because |
|---|---|
| A measured chain or routing baseline | the orchestrator must be shown necessary |
| Evidence that the decomposition **varies** across inputs | the orchestrator's whole justification |
| A bounded action space | unbounded agency is a security decision (see `workflow-vs-agent.md`) |
| An accepted variance in cost and latency | the orchestrator makes both unpredictable |
| A verifiable outcome | an unverifiable orchestrator cannot be gated |

**The 20-input test:** decompose 20 real inputs by hand. If the decompositions repeat, the pattern was
knowable and a chain (or routing) is the right rung — cheaper, faster, debuggable.

### Rung 6 — Bounded graph

| Require | Because |
|---|---|
| A measured baseline at the current rung | the graph must be shown necessary |
| One of the five specific justifications (below) | "grown-up agent" is not one |
| The operational capacity to run an engine | a graph has a maintenance cost |

**The five justifications, and only these:**

| Justification | The requirement it serves |
|---|---|
| **Repeatability** | the same input must produce the same path, auditably |
| **Governance** | a regulated flow needs a reviewable route, not just a correct outcome |
| **Verification** | nodes must substantiate completion, with gates that can fail |
| **Escalation** | a bounded failure must route somewhere deliberate |
| **Scale of operation** | many workflows sharing a common execution contract |

Any other reason is a lower rung wearing a manifest.

## The failure taxonomy

Classify the baseline's failures before choosing a rung. The class *is* the rung.

| Failure class | What it looks like | The rung it implies |
|---|---|---|
| **Format/structure** | correct content, wrong shape | still Rung 1 — fix the prompt or add structured output |
| **Missing information** | confident but wrong; needs a source | **retrieval**, not a higher rung |
| **One-pass insufficient** | too much for one pass, or quality degrades with length | Rung 2 |
| **Input-class variance** | some inputs work, others fail, and the split correlates with input type | Rung 3 |
| **Latency or reliability** | correct but slow, or correct but occasionally fails | Rung 4 |
| **Unknown decomposition** | the steps genuinely differ per input, in ways you cannot enumerate | Rung 5 |
| **Audit/governance/repeatability** | correct, but the requirement is a reviewable path | Rung 6 |

**The retrieval row is the one teams miss.** "It does not have the information" is not a complexity
problem; adding rungs will not supply a fact.

## Recording an entry decision

```text
Entry to: Rung 3 (routing)
From:     Rung 2 (chain) — measured, 20-run task set

Baseline figures:   chain pass rate 71%; cost $0.048/run; latency 2.4 s
Measured failure:   failures CLUSTER: 3 of 20 cases are "invoice" inputs, and all 3
                    fail; the other 17 pass. Failures are not randomly distributed.
Classification:     input-class variance (the clustering test passes)
Failing cases:      cases 04, 11, 19 — recorded as Rung 3's acceptance eval
Trade accepted:     +1 classify call (~$0.004), +0.3 s latency, N paths to maintain
New failure mode:   misrouting — needs a measured routing accuracy
Exit condition:     if invoice traffic exceeds 20% of total, consider a dedicated
                    pipeline instead of a routed path (revisit 2027-01)
```

Every field is required. The `Classification` line is what distinguishes a justified climb from a
hopeful one, and the `Exit condition` is what makes it reversible (R4).

## Checklist

- [ ] The rung below exists, ran on the real task set, and has measured figures (R1)
- [ ] The failure is named specifically, not described as "worse" (R6)
- [ ] The failure is classified, and the class maps to the rung being entered
- [ ] The failing cases are recorded, and become the new rung's eval
- [ ] For routing, the clustering test passes
- [ ] For parallelism, the problem is latency or reliability, not quality
- [ ] For an orchestrator, the 20-input test showed the decomposition varies
- [ ] For a graph, one of the five specific justifications applies
- [ ] The trade (cost, latency, new failure mode) is recorded
- [ ] The exit condition is written, with a date
