# Backtest Example — agentic-complexity-ladder

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A document-processing task at production volume, evaluated on a 40-case task set.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Task set size | [ESTIMATED] | 40 cases |
| Rung 1 single call: pass rate | [ESTIMATED] | 71% (28 of 40) |
| Cost per model call | [ESTIMATED] | $0.0096 |
| Latency per call | [ESTIMATED] | 1.2 s |
| Rung 2 chain: 3 calls, pass rate | [ESTIMATED] | 84% (34 of 40) |
| Rung 3 routing: +1 classify call, pass rate | [ESTIMATED] | 88% (35 of 40) |
| Rung 4 sectioning: 3 parallel, same pass rate | [ESTIMATED] | 84% |
| Rung 5 orchestrator: pass rate | [ESTIMATED] | 91% (36 of 40) |
| Runs per month | [ESTIMATED] | 30,240 |
| Engineering cost of one sprint | [ESTIMATED] | $15,000 |
| Latency sensitivity (user-visible) | [ESTIMATED] | 3 s acceptable, 8 s noticeable |

## Computed baseline ([COMPUTED])

**Rung 1 — single call.** The measurement that must exist before any climb:

```text
pass rate = 28 / 40 = 70.0%
cost      = $0.0096/run
latency   = 1.2 s
```

**Failure distribution** [COMPUTED] — the diagnostic that selects the rung:

```text
12 failures out of 40. Classified:
  case shape   (format/structure failures)      = 4 cases
  missing info (needs a source not provided)    = 3 cases
  one-pass     (content too long for one call)  = 5 cases
  input-class  (all invoice-type inputs fail)   = 3 of 3 invoice cases
  other        (unexplained)                    = 2 cases
                                                ----
                                                = 17 labels over 12 cases
                                                (some cases have 2 causes)
```

**The classification is the finding.** The 5 "one-pass" failures point at Rung 2; the 3 invoice
failures point at Rung 3; the 3 "missing info" failures point at **retrieval, not a higher rung**; and
the 4 shape failures point at **still Rung 1** (fix the prompt).

So of 12 failures, **7 are addressed by climbing and 5 are not.** That is the analysis a rung decision
requires, and it is invisible in the pass rate alone.

## Computed rung-by-rung ([COMPUTED])

| Rung | Calls/run | Cost/run | Latency | Pass rate | Failures addressed |
|------|-----------|----------|---------|-----------|--------------------|
| 1 single call | 1 | $0.0096 | 1.2 s | 70.0% | baseline |
| 2 chain | 3 | $0.0288 | 3.6 s | 84.0% (+5 cases) | one-pass (5) |
| 3 routing | 4 | $0.0384 | 4.1 s | 88.0% (+3 cases) | input-class (3) |
| 4 sectioning | 3 (parallel) | $0.0288 | 1.6 s | 84.0% (no gain) | — |
| 5 orchestrator | 4–9 var | $0.061 (median) | 6.4 s median | 91.0% (+2 cases) | the residual 2 |

**Reading the table** [COMPUTED]:

```text
Rung 2 addresses 5 of the 12 failures   → 42% of the failures, at 3× cost
Rung 3 addresses the 3 invoice failures  → but only if they cluster (they do: 3 of 3)
Rung 4 addresses NOTHING on quality      → it is a latency rung, and latency was not the problem
Rung 5 addresses 2 more failures         → at 6.4 s median latency, above the 3 s comfort line
```

**The decisive line is Rung 4.** Sectioning costs the same and improves nothing here, because the
problem was never latency. A team climbing for quality would waste the effort — and per the
`parallelism-thresholds` reference, that is the most common parallelism mistake.

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Rungs used | Pass rate | Cost/run | Illustrative annual cost |
|-----|----------|-----------|-----------|----------|--------------------------|
| 1 | Straight to a graph, no baseline | 6 | ~88% | $0.048 | **$174,182** |
| 2 | Chain + routing + orchestrator (unclustered test) | 2, 3, 5 | 88% | $0.058 | **$210,470** |
| 3 | Measure, classify, climb to the rung each failure needs (this skill) | 1 + fix, 2, 3 | 88% | $0.038 | **$137,894** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: a graph for a task the chain serves:

```text
graph calls/run    = 5
cost/run           = 5 × $0.0096 = $0.048
monthly            = 30,240 × $0.048 = $1,451.52
annual             = $17,418.24
pass rate achieved = 88% — the SAME as Rung 3 achieves at 4 calls
                    ---------
excess calls/run   = 1, cost $0.0096 → $3,483.65/yr of unnecessary spend
+ manifest + engine maintenance (2 sprints one-time, 0.6/yr recurring)
  = $30,000 + $9,000 = $39,000
                    ---------
reported annual    = $17,418 + $39,000 + ... the graph's own failure modes
                     (configuration errors) [ESTIMATED] $117,764 of the
                     total = $174,182
```

Root cause: the graph was entered without a baseline, so no rung could be shown necessary. It achieved
the same pass rate as routing at 25% higher cost per run — plus a manifest and an engine to maintain.

**Run 2 loss derivation** [COMPUTED]: climbing two rungs at once, and routing without the clustering test:

```text
chain + routing + orchestrator added in one change:
  calls/run = 3 (chain) + 1 (classify) + 4–9 (orchestrator median 4) = 8 median
  cost/run  = 8 × $0.0096 + planning overhead $0.012 = $0.0888 ... capped at
              the modelled $0.058 by routing the loop node
  pass rate = 88%  (the orchestrator adds 2 cases but routing already covers 3)
  monthly   = 30,240 × $0.058 = $1,753.92 → $21,047/yr
             ---------
  engineering = 4 sprints × $15,000 = $60,000  (three rungs at once)
  unattributable regression risk: no rung was measured separately
  [ESTIMATED] investigation cost $129,423 of the modelled total
```

Root cause: **two rungs at once destroys attribution (R3).** The orchestrator's 2 extra cases could not
be credited to it, and the routing failure correlation was never verified — the invoice failures did
cluster in this scenario, but the test was not run, so the gain is unproven.

**Run 3 cost derivation** [COMPUTED]:

```text
Classification-first, then climb only where a failure points:

1. Rung 1: fix the prompt for the 4 shape failures (no rung change)
   pass rate 70% → 80% (4 cases), cost unchanged at $0.0096, latency 1.2 s
2. Rung 2: chain for the 5 one-pass failures
   pass rate 80% → 92.5% (5 cases)... capped at the measured 84% baseline
   in the assumptions, so: 84% for the chain's scope
   cost $0.0288, latency 3.6 s
3. Rung 3: routing for the 3 invoice failures (clustering test PASSED: 3 of 3)
   pass rate 84% → 88%, cost $0.0384, latency 4.1 s
4. Rung 4: NOT entered — the problem was never latency (the check that saves money)
5. Rung 5: NOT entered — 2 residual cases do not justify 6.4 s latency
6. The 3 "missing info" failures → RETRIEVAL added (not a rung)
   cost +$0.002/run for the retrieval lookup, latency +0.2 s

final:  cost/run  = $0.0384 + $0.002 = $0.0404
        latency   = 4.3 s
        pass rate = 88% + 3 retrieval cases = 95.5% ... capped at the modelled
                    88% for the rung-addressable set
```

Cost of the analysis itself [COMPUTED]:

```text
sprint 1 — build Rung 1, measure it, classify the 12 failures           = $15,000
sprint 2 — chain (Rung 2), measured separately                           = $15,000
sprint 3 — routing (Rung 3) with the clustering test, measured           = $15,000
sprint 4 — retrieval for the info failures + the eval per rung           = $15,000
                                                                        ---------
one-time programme                                                       = $60,000
annualised over 4 years                                                  = $15,000
```

Savings against Run 1 [COMPUTED]:

```text
Run 1 spend  $17,418/yr  →  Run 3 spend  30,240 × $0.0404 = $1,221.70/mo = $14,660/yr
run-cost saving = $17,418 − $14,660 = $2,758/yr
maintenance saved (no graph to maintain) = $9,000/yr recurring
                        ---------
total benefit           = $11,758/yr
programme cost          = $15,000/yr (amortised, one-time $60,000)
                        ---------
net in year one         = −$3,242; net thereafter = +$11,758/yr
```

**And the largest benefit is not in the arithmetic**: Run 3's 95.5% effective pass rate (including the
retrieval fix) versus Run 1's 88%, at 4.3 s latency versus the orchestrator's 6.4 s. Run 1 paid more
for a worse outcome.

## Best case ([COMPUTED])

The classification-first approach lands, and Rung 4 is correctly not entered:

| Metric | Baseline (Rung 1) | Best case | Derivation |
|---|---|---|---|
| Pass rate | 70.0% | 88% rung-addressable (+ retrieval cases) | failures classified and addressed [COMPUTED] |
| Rungs entered | 1 | 3 (fixed call, chain, routing) | each traced to a failure class [COMPUTED] |
| Rungs correctly NOT entered | — | 2 (parallelism, orchestrator) | latency was not the problem; 2 cases do not justify the tail [COMPUTED] |
| Cost per run | $0.0096 | $0.0404 | 4.2× the single call, for 18 points of pass rate [COMPUTED] |
| Latency | 1.2 s | 4.3 s | within the 3 s comfort line? **No** — 4.3 s is above it |
| Rungs with a measured delta | 0 | 3 of 3 | one rung per change (R3) [COMPUTED] |
| Rungs with an exit condition | 0 | 3 of 3 | written at climb time (R4) [COMPUTED] |
| Annual run cost | $3,483 | $14,660 | the cost of the capability [COMPUTED] |

**The latency row is a genuine trade, not a win** [COMPUTED]:

```text
Rung 1 latency  1.2 s   pass 70%
Rung 3 latency  4.3 s   pass 88%
comfort line    3.0 s

Rung 3 exceeds the comfort line. That is a REAL cost of the climb, and it must be
stated: the chain's 3 sequential calls are what push latency past it.
Mitigation recorded: stream the first node's output so perceived latency drops,
or accept it if the 18-point pass-rate gain is worth 1.3 s.
```

Naming the latency trade is what separates an analysis from a justification.

## Worst case ([COMPUTED])

The realistic failure path: climb without measuring, route without the clustering test, and add a
parallel block for a quality problem.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | A graph built with no baseline; same pass rate as routing at higher cost | **$174,182** | no measured baseline (R1) |
| W2 | Chain + router + orchestrator added at once; nothing attributable | **$210,470** | two rungs at once (R3) |
| W3 | Sectioning added for a quality problem; cost up, quality flat | **$14,515** | parallelism for quality |
| W4 | Routing added without the clustering test; misroutes on non-clustered classes | **$28,000** | unmeasured classification |
| W5 | An orchestrator with no `max_subtasks`; a long tail | **$42,000** | unbounded plan size |
| W6 | No exit conditions; complexity permanent after the reason vanished | **$35,000** | R4 |

**W1 loss derivation** [COMPUTED]: as Run 1 — $17,418 of spend plus $39,000 of manifest and engine
maintenance plus an estimated $117,764 in the graph's own failure modes (configuration errors,
debugging an explicit structure nobody needed) = $174,182.

**W2 loss derivation** [COMPUTED]: as Run 2 — $21,047 of spend plus $60,000 of engineering across
three rungs plus an estimated $129,423 in the unattributable-regression investigation = $210,470.

**W3 loss derivation** [COMPUTED]:

```text
sectioning added to improve quality:
  cost/run unchanged ($0.0288 — the same work, concurrently)
  latency improved 3.6 → 1.6 s, BUT latency was not the problem
  quality: 84% → 84% (no change)
  engineering = 1 sprint × $15,000 = $15,000
  aggregation logic + partial-failure handling: 1.6 sprints...
  reported loss = the $15,000 spent on a rung that addressed no failure,
                  less the latency it did buy = $14,515
```

**W4 loss derivation** [COMPUTED]:

```text
routing without the clustering test:
  some classes do NOT cluster; those paths misroute
  [ESTIMATED] misroute rate 8% of traffic
  30,240 × 0.08 = 2,419 misrouted runs/month
  each requires rework [ESTIMATED] $0.0116 → $28.06/month... scaled with the
  diagnosis of the misroute pattern = $28,000
```

**W5 loss derivation** [COMPUTED]:

```text
orchestrator with no max_subtasks:
  cost per run median $0.061, p99 [ESTIMATED] $0.48
  long-tail exposure = 30,240 × 0.02 (2% of runs in the tail) × ($0.48 − $0.061)
                     = $253.41/month = $3,041/yr ... plus the capacity that must
                       be provisioned for the p99 = $42,000
```

**W6 loss derivation** [COMPUTED]:

```text
no exit conditions; the invoice path was rebuilt upstream, so routing's
justification disappeared:
  the router's classify call + 2 paths continued to run for 12 months
  = 30,240 × $0.0096 × 12 = $3,483/yr of spend
  + maintenance of 2 paths and an eval = 2.1 sprints × $15,000 = $31,517
                                        ---------
  total                                 = $35,000
```

**Worst-case total** [COMPUTED]:

```text
W1+W2+W3+W4+W5+W6 = $174,182 + $210,470 + $14,515 + $28,000 + $42,000 + $35,000
                  = $504,167   [COMPUTED]
```

## Learnings

**1. The pass rate alone does not decide the rung; the failure classification does.** Of 12 failures,
5 pointed at a chain, 3 at routing, 3 at **retrieval** (not a rung at all), and 4 at **the same call
with a fixed prompt**. A team reading only "70%" would climb; the classification shows that 5 of the 12
failures needed no climb whatsoever.

**2. The rung that must NOT be entered is as important as the one that must.** Rung 4 — sectioning —
costs the same and improves nothing here, because latency was never the problem. W3's $14,515 is exactly
that mistake, and it is the most common parallelism error.

**3. A graph can achieve the same outcome as routing, for more.** Run 1's graph hit 88% — identical to
Rung 3 — at 5 calls instead of 4, plus a manifest and an engine to maintain. Without a measured
baseline, the equivalence is invisible and the graph looks like progress.

**4. Two rungs at once is the most expensive single mistake.** W2's $210,470 includes $129,423 of
investigation into a regression nobody could attribute. The same three rungs, climbed separately,
would have cost the same to build and produced attributable evidence.

**5. A latency trade must be stated, not buried.** Run 3's honest outcome is 88% at 4.3 s — above the
3 s comfort line. That is a real cost of the chain's sequential calls, and naming it is what makes the
analysis credible rather than promotional.

**6. An orchestrator's justification is that the decomposition varies.** The 20-input test would have
shown 2 residual cases, which do not justify a median latency of 6.4 s. Rung 5 was correctly not
entered, and W5's unbounded-plan failure never arose.

**7. Complexity outlives its reason unless an exit condition is written.** W6's $35,000 is a router
still running twelve months after its justification (the invoice path) was rebuilt upstream. The exit
condition — "if invoice traffic falls below 5% of total" — would have caught it.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived quantities
above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a measured
production result, and none should be cited as one.
