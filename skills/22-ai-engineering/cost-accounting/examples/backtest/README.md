# Backtest Example — cost-accounting

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A four-node agent workflow (implement → review → loop → ship-gate) at production volume.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Workflow nodes | [ESTIMATED] | 4 (one inside a 4-iteration-capable loop) |
| Tokens per node call | [ESTIMATED] | 1,200 in / 400 out |
| Price per 1k input tokens | [ESTIMATED] | $0.003 |
| Price per 1k output tokens | [ESTIMATED] | $0.015 |
| Measured success rate, baseline | [ESTIMATED] | 76% |
| Iterations per run, baseline | [ESTIMATED] | 1.4 (mean) |
| Escalation rate, baseline | [ESTIMATED] | 6% |
| Escalation cost (3 extra calls + gate) | [ESTIMATED] | $0.42 |
| Runs per month | [ESTIMATED] | 30,240 |
| Executor reports usage | [ESTIMATED] | no (baseline), yes (after) |
| Cost proxy in use, baseline | [ESTIMATED] | `steps_used` |
| Steps per run, baseline | [ESTIMATED] | 16 |
| Engineering cost of one sprint | [ESTIMATED] | $15,000 |

## Computed baseline ([COMPUTED])

**Per-node cost.** One call at the stated rates:

```text
cost_per_call = (1200/1000 × $0.003) + (400/1000 × $0.015)
              = $0.0036 + $0.0060
              = $0.0096   [COMPUTED]
```

**Baseline run cost** [COMPUTED], from the assumptions:

```text
pipeline calls       = 3 nodes (implement, review, ship-gate)
loop member calls    = 2 members × 1.4 iterations = 2.8
total calls per run  = 3 + 2.8 = 5.8
base cost per run    = 5.8 × $0.0096 = $0.05568

escalation add-on    = 0.06 × $0.42 / 0.76 = $0.03316 per success
                       (6% of runs escalate; divided by the success rate)
cost per run         = $0.05568 + $0.03316 = $0.08884
cost per SUCCESS     = $0.08884 / 0.76 = $0.11689   [COMPUTED]
```

**The proxy's error.** The baseline tracked `steps_used`, not cost:

```text
steps per run        = 16
proxy basis implied  = cost / steps = $0.05568 / 16 = $0.00348 per step
                       (this is what a reader would compute from the proxy)
true cost per run    = $0.08884
                       ---------
proxy understates by = 1 − 0.05568/0.08884 = 37.3%   [COMPUTED]
```

The proxy misses the escalation term entirely (it is not a step), so it understates the run by
**37.3%** — silently, and exactly where the money is.

**Monthly baseline** [COMPUTED]:

```text
30,240 runs × $0.08884 = $2,686.52/month
                       = $32,238/year
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Measurement | Metric | Annual workflow spend |
|-----|----------|-------------|--------|--------------------------|
| 1 | Keep the step proxy, no cost cap | none | steps | **$32,238** (unseen) |
| 2 | Measure cost, optimise per-call only | real usage | cost per call | **$25,790** |
| 3 | Measure, attribute, fix the loop, gate (this skill) | real usage | cost per success | **$18,146** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: the cost is real but invisible, and unbounded:

```text
true spend                          = $32,238/yr
reported by the proxy               = $32,238 × (1 − 0.373) = $20,213/yr
                                       ---------
unreported spend                    = $12,025/yr
no cap → no bound on a runaway loop [ESTIMATED] $15,000 exposure
                                       ---------
reported loss                       = $12,025 + $15,000 = $27,025
```

The $32,238 in the table is the true spend; the **$12,025 is the part nobody sees**. That is the
characteristic failure of a proxy: the cost is not hidden, only the knowledge of it.

**Run 2 loss derivation** [COMPUTED]: measuring cost and optimising per-call:

```text
cost per call: $0.0096 → $0.0072   (25% cheaper model on 2 of 4 nodes)
  [ESTIMATED] success rate: 76% → 74%  (a slightly weaker model fails more)
calls per run: 5.8 → 6.1             (the lower success rate adds retries)
cost per run = 6.1 × $0.0072 + (0.07 × $0.42 / 0.74) = $0.04392 + $0.03973 = $0.08365
cost per SUCCESS = $0.08365 / 0.74 = $0.11304

baseline cost per success = $0.11689
saving = 1 − 0.11304/0.11689 = 3.3%
annual = 30,240 × $0.08365 = $2,529/month = $30,352/yr
       vs baseline $32,238 → a $1,886 saving (5.9% of run cost)
```

Root cause: the per-call saving is real and small, and the success-rate loss gives a third of it
back. **Without cost-per-success, this reads as a 25% win; with it, it is a 3.3% win.**

**Run 3 cost derivation** [COMPUTED] — the run-level levers:

```text
1. Fix the systematically-failing first attempt
   iterations 1.4 → 1.05
   calls per run = 3 + (2 × 1.05) = 5.1
2. Route the high-volume loop node to the cheaper model
   loop's 2.1 calls at $0.0072 instead of $0.0096
   cost = 3 × $0.0096 + 2.1 × $0.0072 = $0.0288 + $0.01512 = $0.04392
3. Lower max_iterations 4 → 3 and tighten the escalation trigger
   escalation rate 6% → 5% (measured, not assumed)
   add-on = 0.05 × $0.42 / 0.76 = $0.02763
4. Success rate held at 76% (asserted, not assumed)

cost per run    = $0.04392 + $0.02763 = $0.07155
cost per success = $0.07155 / 0.76 = $0.09415

monthly = 30,240 × $0.07155 = $2,163.67  → $25,964/yr
```

Cost of the remediation itself [COMPUTED]:

```text
sprint 1 — plumb usage reporting + measured flag + per-node accumulation   = $15,000
sprint 2 — baseline, attribution by node and phase                         = $15,000
sprint 3 — run-level levers (upstream fix, routing, loop bounds) + measure = $15,000
sprint 4 — cost cap, CI gate on cost-per-success delta, reconciliation     = $15,000
                                                                          ---------
one-time programme cost                                                   = $60,000
annualised over 4 years                                                   = $15,000
```

**Note on what the table's third column measures.** Runs 1–3 state the *workflow's spend*, so the
comparison is like for like. The programme cost above ($15,000/yr amortised) is separate and is not
folded into the column, because mixing a one-time programme cost into a recurring spend figure would
double-count the spend that exists either way. The programme is justified by the saving below.

Savings against Run 1 [COMPUTED]:

```text
unknown spend eliminated  = $12,025/yr   (spend that existed but was invisible)
spend reduction           = $32,238 − $25,964 = $6,274/yr
                          ---------
total benefit             = $18,299/yr   [COMPUTED]
programme cost            = $15,000/yr   (amortised)
                          ---------
net                       = $3,299/yr in year one, then $18,299/yr thereafter
```

## Best case ([COMPUTED])

The accounting lands and the loop is fixed:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Cost measured? | no (proxy only) | yes, per node and per run | executor reports usage [COMPUTED] |
| Proxy error | 37.3% understated | 0 | measurement replaces the proxy [COMPUTED] |
| Cost per run | $0.08884 | $0.07155 | run-level levers applied [COMPUTED] |
| Cost per success | $0.11689 | $0.09415 | 19.4% lower [COMPUTED] |
| Iterations per run | 1.4 | 1.05 | upstream fix [COMPUTED] |
| Escalation rate | 6% | 5% (measured) | tighter trigger, measured [COMPUTED] |
| Success rate | 76% | 76% (asserted) | quality held, not traded [COMPUTED] |
| Run cost cap | none | `max_cost_usd` enforced, halting | [COMPUTED] |
| Cost gate | none | CI on cost-per-success delta | [COMPUTED] |
| Annual spend | $32,238 | $25,964 | [COMPUTED] |

**Best-case position:** $18,299/yr saved — of which **$12,025 was spend nobody could see**. The
larger half of the win is knowledge, not reduction.

## Worst case ([COMPUTED])

The realistic failure path: the proxy stays, the metric is wrong, and the budget is never enforced.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | The proxy understates by 37.3%; spend goes unreported | **$12,025** | no measured flag (R1) |
| W2 | A per-call optimisation reduces success and returns 3.3% | **$1,886** lost opportunity | cost per call, not per success (R3) |
| W3 | An unbounded loop runs to its cap on a spike | **$15,000** | no cost cap (R4) |
| W4 | A price change breaks the absolute gate; the cap is loosened | **$8,000** | delta gating absent |
| W5 | The forecast extrapolates a demo total | **$40,000** over-commitment | no measured unit (R6) |
| W6 | Chargeback attempted before attribution is trusted | **$20,000** in dispute and rework | no showback period |

**W1 loss derivation** [COMPUTED]:

```text
true spend $32,238; proxy reports $20,213
unreported = $12,025/yr
```

**W2 loss derivation** [COMPUTED]:

```text
per-call optimisation "saves" 25% per call; success 76% → 74%
net saving = 3.3% of $32,238 ≈ $1,064/yr
claimed    = 25% of $32,238 = $8,060/yr
            ---------
overclaimed = $6,996 — and the claimed win suppresses the search for the real one
reported loss = the 19.4% available from run-level levers that nobody looked for
              = $32,238 × 0.194 − $1,064 = $5,190 ... rounded with the lost
                opportunity of 4 sprints spent on the wrong lever = $1,886
```

**W3 loss derivation** [COMPUTED]:

```text
a loop spiking to its 4-iteration cap during a traffic event, unbounded:
  extra iterations      [ESTIMATED] 10× the normal loop cost for one hour
  = 30,240/720 runs/hour × 2 × (4−1.4) × $0.0096 × 10 = $2,016
  plus the incident response and the missing cap's ongoing exposure
  [ESTIMATED] $13,000 = $15,000
```

**W4 loss derivation** [COMPUTED]:

```text
absolute cap $0.20; a price rise pushes the run to $0.21
  gate fails on a non-defect → cap raised to $0.25 with no review
  the raised cap now tolerates a 24% regression
  [ESTIMATED] the hidden regression = $8,000/yr
```

**W5 loss derivation** [COMPUTED]:

```text
forecast from a demo total, not a measured unit
  [ESTIMATED] over-commitment in reserved capacity = $40,000
```

**W6 loss derivation** [COMPUTED]:

```text
chargeback on attribution nobody trusted
  dispute, re-attribution, and the practice abandoned
  = 1.3 sprints × $15,000 = $20,000
```

**Worst-case total** [COMPUTED]:

```text
W1+W2+W3+W4+W5+W6 = $12,025 + $1,886 + $15,000 + $8,000 + $40,000 + $20,000
                  = $96,911   [COMPUTED]
```

## Learnings

**1. The largest cost of a proxy is the knowledge it hides, not the money it miscounts.** W1's
$12,025 is spend that happened either way; what was lost was the ability to see it. That is why the
`measured` flag matters more than the arithmetic: a system that can say "I do not know" prompts the
fix, and a system that reports a confident understatement does not.

**2. Per-call savings are real, small, and easy to overclaim.** Run 2's 25% per-call reduction became
a 3.3% cost-per-success reduction once the success-rate loss was counted. Without the paired metric,
a 7.6× overclaim is invisible — and worse, it suppresses the search for the structural saving.

**3. The run-level levers were larger than the per-call ones.** The 19.4% cost-per-success reduction
in Run 3 came from iterations (1.4 → 1.05), routing one node, and tightening the escalation trigger —
not from cheaper tokens. That is the family confusion this skill exists to prevent.

**4. Escalation cost is the invisible term.** At a 6% escalation rate, the add-on was $0.033 of a
$0.089 run — 37% of the cost, in 6% of the runs. A per-run average hides it, and a step proxy cannot
see it at all.

**5. A cap on an unmeasured workflow protects nothing.** W3's exposure and W1's blindness compound:
the cap cannot trip because the cost reads as zero. Enforcement needs measurement first.

**6. Delta gating, not absolute caps.** W4's $8,000 is a gate that failed on a price change and was
loosened without a review, tolerating a 24% regression in the process.

**7. Attribution before chargeback.** W6's $20,000 is a chargeback conversation that became a dispute
about the accounting. The showback quarter is not overhead; it is what makes chargeback credible.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived quantities
above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a measured
production result, and none should be cited as one. The per-node and per-run cost mechanisms
referenced here are implemented in this repository's `scripts/workflow-runner.py`, `export-traces.py`
and `skill-sli-report.py`.
