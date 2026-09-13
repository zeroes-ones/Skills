# Backtest Example — verification-independence-engineer

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A research-briefing agent runs daily; a writer node drafts, a verifier node approves.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Value | Tag |
|---|---|---|
| Runs per month | 1,000 | [ESTIMATED] |
| Artifacts per run | 1 briefing | [ESTIMATED] |
| Verifier false-accept rate, producer-only check (self-verification) | 18% | [ESTIMATED] |
| Verifier false-accept rate, independent + calibrated (measured on known-bad set) | 4% | [ESTIMATED] |
| Cost of one escaped briefing defect (correction, re-brief, trust) | $120 | [ESTIMATED] |
| Cost per run, self-check only | $0.19 | [ESTIMATED] |
| Cost per run, with an independent verifier node | $0.26 | [ESTIMATED] |
| Ticket-resolution leak: monthly resolution-rate gain from the cheapest path | +9 pts | [ESTIMATED] |
| Ticket-resolution leak: renewal churn attributable, per month | 0.6 pts of base | [ESTIMATED] |
| Monthly recurring revenue exposed per churn point | $40,000 | [ESTIMATED] |

## Computed scenario ([COMPUTED])

### Part 1 — the verification cost is not the comparison; the re-work is

False-accept rate is the number that decides whether a verifier is worth its price, because every
false accept is an escaped defect paid for downstream.

```
escaped defects/month, self-check only = 1000 * 0.18 = 180
escaped defects/month, independent     = 1000 * 0.04 =  40

escaping defect reduction = 180 - 40 = 140/month

cost of escaped defects, self-check only = 180 * $120 = $21,600/month
cost of escaped defects, independent     =  40 * $120 = $ 4,800/month
downstream saving                        = $16,800/month

verifier overhead = 1000 * ($0.26 - $0.19) = $70/month

net = $16,800 - $70 = $16,730/month saved by adding the verifier
```

The verifier costs 37% more per run and returns ~239× its cost. **The relevant ratio is cost per
*verified* output, not cost per call** — the same argument `cost-accounting` makes.

| Run | Configuration | False-accept | Escaped defects/mo | Downstream cost | Run cost | Net/mo |
|-----|---------------|--------------|--------------------|-----------------|----------|--------|
| 1 | Producer self-check only | 18% | 180 | $21,600 | $190 | — |
| 2 | Separate node, same model + shared context | 15% | 150 | $18,000 | $260 | +$3,530 |
| 3 | Separate node, fresh context, claim + evidence only | 4% | 40 | $4,800 | $260 | **+$16,730** |

**Reading the rows.** Run 2 shows why role alone is nearly worthless: a separate node that shares
the model *and* the context reduces false-accepts only 18% → 15%, recovering ~$3.5k of a possible
$16.7k. Run 3 shows the leverage — fresh context plus the information boundary (R2, R3) is where the
value is, and it costs the same as Run 2.

### Part 2 — the metric that looks right and is not

The same team adds a support agent optimised on ticket resolution rate. The target improves every
month while the thing it stood for degrades:

```
month 1: resolution rate +9 pts   churn +0.00 pts   → green
month 2: resolution rate +9 pts   churn +0.00 pts   → green
month 3: resolution rate +9 pts   churn +0.30 pts   → green (harm still inside lag)
month 4: resolution rate +9 pts   churn +0.60 pts   → green (harm visible on the dashboard)
month 5: resolution rate +9 pts   churn +0.60 pts   → green (gate reads resolution only)
month 6: renewal: churn realised  → the 6 months of "improvement" are re-read as loss
```

```
monthly MRR exposed at 0.6 churn points = 0.6 * $40,000 = $24,000/month
vs. the resolution-rate "gain" the gate was celebrating
```

Under the skill's Phase 6–7 (find the targets, pair the guards), the fix is available **before** the
optimisation ships: write the intent ("support resolves real problems"), find the leak ("close the
conversation"), and gate on the pair (`resolution rate up` **AND** `reopen rate + churn flat`). The
same dashboard would then have shown the gate failing in month 3, when the harm first exceeded noise
— four months earlier than the renewal cycle revealed it.

| Run | Gate configuration | Month 3 signal | Month 6 outcome |
|-----|--------------------|----------------|-----------------|
| 1 | Resolution rate only (target alone) | Green | ~$144k of churn ($24k × 6) |
| 2 | Resolution rate + reopen/churn pair | **Red at month 3** | Caught with ~$72k avoided (3 months) |

## Best case

Run 3 — the independent, fresh-context, information-bounded verifier. False-accepts fall 18% → 4%,
escaped defects drop 180 → 40 per month, and the verifier costs $70/month more while saving $16,800
([COMPUTED] from Part 1). The gate is a real check: its verdict is not a restatement of the
producer's reasoning, it has rejected things known to be bad, and every metric it gates is paired
with the harm that metric could cause.

## Worst case

Run 1 — the producer reviewing itself. Every check passes, the reported quality is high, and 180
defects a month escape because the evaluation inherits the reasoning that produced the output. The
downstream cost is $21,600/month ([COMPUTED]) and the system reports *more* confidence as it gets
worse, because approval is being counted as quality.

Run 2 is the subtler failure: a genuinely separate node that shares the model *and* the context.
It recovers only 18% → 15% — about $3,530 of a possible $16,730 ([COMPUTED]) — because agreement
between two reasoners with the same blind spots is one opinion counted twice.

Part 2 is the failure that costs the most while looking healthiest: the resolution-rate gate is
green for all six months while churn accumulates to roughly $144,000 of exposed MRR
([COMPUTED] from $24,000/month × 6). The metric worked exactly as specified.

## Learnings / key takeaways

- **Lesson learned:** role separation alone is nearly worthless. Runs 1 → 2 show a separate node
  with a shared model and shared context recovers only about a fifth of the available value; the
  fresh context and information boundary in Run 3 carry the rest — at the same cost per run
  ([COMPUTED] from Part 1).
- **Actionable lesson:** verifier cost is not the comparison; the re-work it prevents is. A 37%
  higher cost per run returns roughly 239× in avoided escaped defects in this scenario
  ([COMPUTED]).
- **Actionable lesson:** the harm metric becomes readable *before* the business consequence does.
  Churn crossed noise in month 3 and was only realised at renewal in month 6, so pairing the metric
  buys about three months of warning ([COMPUTED] from Part 2).
- **What this validated:** the skill's workflow (map the split → find self-checks → declare the four
  properties → enforce the boundary → calibrate → find targets → pair guards → verify) produced a
  consistent, tag-annotated plan across three configurations and named the specific property
  responsible for each change in outcome.

## What this does not show

- No real agent pipeline was measured. False-accept rates, defect costs and churn figures are all
  [ESTIMATED] model inputs chosen to make the arithmetic legible.
- A verifier's false-accept rate is not constant: it drifts with the model, and re-calibration is
  the only thing that keeps the 4% figure meaningful (CR12).


## What this backtest validates

1. **R1/R2/R3:** the three-row table in Part 1 shows role-only separation is weak, and that the
   information boundary plus fresh context carries the value — at no extra cost per run.
2. **R4:** Part 2 is goal blindness made arithmetic: the gate was green for the entire period the
   business was degrading, because the target had no pair.
3. **The cost comparison:** verification is judged against the re-work it prevents (239× here), not
   against its own token cost.
4. **The lag:** the harm metric becomes readable before the business consequence does — which is the
   only reason pairing the metric is worth doing at all.

## Provenance

- False-accept rates, defect costs, churn points, and MRR figures are **[ESTIMATED]** model inputs
  chosen to make the arithmetic legible. They are not measured from any real system.
- All ratios, totals and the 239× figure are **[COMPUTED]** from those inputs.
- **Do not quote any number here as a benchmark.** Run the same arithmetic on your own workload; the
  *structure* of the result transfers, the magnitudes do not.
