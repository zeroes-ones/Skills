# Signal Validation Protocol

**A dataset that cannot change a decision is not evidence.** That sentence is the whole protocol
compressed into one line: the purpose of validation is not to find out whether a signal "works" in
the abstract, but to find out whether it changes what you will do, and by how much, with what
confidence, and against what comparison.

Run the six steps below **in this order**. The order is not stylistic — steps 4 and 5 are worthless if
they run after step 6's results are visible.

## §1 — The Six Steps

```
1. NAME THE CLAIM            one falsifiable sentence
2. NAME THE COUNTERFACTUAL   what happens without the signal, same period, same size
3. GET A POINT-IN-TIME SAMPLE restated data is not a sample
4. DEFINE THE BASE RATE      BEFORE looking at any signal output
5. HOLD OUT A PERIOD THE SELLER DID NOT CHOOSE
6. PRE-COMMIT THE DECISION   and the size, in writing, with a timestamp
```

### Step 1 — Name the claim

One falsifiable sentence. Not "this indicates strength" — **"when X occurs, the name's return over the
next N sessions exceeds the base rate by at least M points, before costs."**

| Bad claim | Why it fails step 1 | Better claim |
|---|---|---|
| "Insider buying is bullish" | unfalsifiable as written; no horizon, no magnitude, no comparison | "Open-market code-P cluster buys of ≥3 insiders, excluding 10b5-1, are followed by a return above the base rate over 20 sessions" |
| "Unusual options activity precedes moves" | names no threshold, no horizon, no baseline | "Single-leg volume above a stated multiple of the 20-day average, in the top decile of the day's prints, precedes an absolute move above base rate over 5 sessions" |
| "My backtest works" | a backtest is not a claim; it is a result | "Strategy S beats its benchmark net of a stated cost model over period P" |

**Complete when** a stranger could collect the data and falsify the sentence without asking you a
question.

### Step 2 — Name the counterfactual

**The counterfactual is the only honest comparison.** It is what happens over the same period, at the
same size, in the same instrument, when the signal is ignored.

| Counterfactual | What it catches |
|---|---|
| The **base rate** for the event | a signal that is just the market's drift |
| A **naive rule** (always long, always short, a coin flip) | a signal that adds nothing over a trivial alternative |
| **The same signal on a random date** | overfitting to a date pattern |
| **The signal with a lagged input** | a signal that only works because it sees the future |

**Complete when** the counterfactual is stated in **dollars** for the same size and period, not in
adjectives. "The exit was better" is an opinion; a $1,200 cost avoided on the same position over the
same window `[ILLUSTRATIVE]` is a claim that can be wrong, and therefore a claim that can be tested.

### Step 3 — Get a point-in-time sample

**Restated data is not a sample.** This step fails most often in macro work, where FRED serves only
the **restated** series and **ALFRED vintages** are needed for what was actually published
`[VERIFIED — FRED/ALFRED]`. It fails in equity work when a constituent file is a *current* file, and
in filings work when the archive is re-crawled after corrections that EDGAR does not backfill into
prior indexes `[VERIFIED — SEC Accessing EDGAR Data]`.

| Data class | Point-in-time requirement | The trap if skipped |
|---|---|---|
| Macro series | an ALFRED vintage per observation | look-ahead through revision |
| Index membership | a point-in-time membership source | survivorship bias |
| Filings | your own forward-crawled snapshot | corrections you could not have seen |
| Prices | an explicit adjustment convention, documented per series | a split reading as a −50% day |
| Open interest | the exchange's as-of date per observation | next-day information in a same-day position |

**Complete when** every observation in the sample carries a date on which it was **obtainable**.

### Step 4 — Define the base rate BEFORE looking

**Write it down, with a timestamp, before loading the signal's output.** A hit rate is meaningless
without the base rate it is compared against: 62% looks like an edge against 50% and is a *deficit*
against a 65% base rate, which is what "the stock went up" produces in an uptrend.

Define four:

1. **Unconditional** — how often the event happens over the full sample.
2. **Regime-conditional** — how often within each of the four regimes. Most published base rates were
   computed in an uptrend `[COMMON-PRACTICE — a base-rate caveat, not a measurement]`.
3. **Liquidity- and size-conditional** — within the universe actually under test.
4. **Horizon-conditional** — within the holding period.

**Complete when** the base-rate line appears **before** the results line in the document, and the
document shows that ordering. If it does not, the validation is **void** and must be re-run — not
re-read charitably.

### Step 5 — Hold out a period the seller did not choose

Any dataset sold with a backtest attached has a holdout chosen by someone whose revenue depends on it
looking good. That is not fraud; it is selection pressure across five degrees of freedom — universe,
period, metric, rebalance rule, and the exclusion list.

**If the seller will not supply a point-in-time sample for a period you chose, the panel is
inadmissible as evidence.** Stop there. No amount of diligence repairs a sample you cannot choose.

### Step 6 — Pre-commit the decision

Write the action **and the size**, with a timestamp, before the results are known.

| Field | Example |
|---|---|
| The action | "if confirmed, add a 2% NAV satellite to the existing position" |
| The size | in NAV percentage and in dollars, with the formula |
| The condition | the specific threshold the results must meet, decided in advance |
| The falsifier | what result would make me abandon the signal entirely |
| The review date | when the decision is re-read, so it cannot be quietly abandoned |

**Complete when** the pre-commitment exists in writing and is dated before the results. A
pre-commitment written after the results is a rationalisation with a form attached.

## §2 — The Grading Rubric for the Validation Itself

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| **Claim** | unfalsifiable as written | falsifiable but vague on horizon or magnitude | one sentence, falsifiable, with horizon and magnitude |
| **Counterfactual** | absent | a percentage with no dollars | dollars, same size and period, with the formula |
| **Point-in-time** | restated data used as if it were live | provenance stated but incomplete | every observation carries its obtainable-on date |
| **Base rate** | written after the results, or absent | written before but only unconditional | all four base rates, written before the results, ordered correctly in the document |
| **Holdout** | the seller's period | a second period, but not point-in-time | a period you chose, point-in-time, with the vendor's data dictionary |
| **Pre-commitment** | none | an action with no size | an action, a size in dollars, a condition and a falsifier, dated before the results |

A validation scoring **below 8 of 12 is not a validation.** It is a description of the sample.

## §3 — What "the Signal Works" Is Allowed to Mean

Four permitted statements, and nothing else:

1. **"The signal's hit rate exceeded the stated base rate by X points over period P, in universe U,
   net of a stated cost model."**
2. **"The signal's hit rate did not exceed the base rate over period P."**
3. **"The sample is too small to distinguish the signal from its base rate."** The arithmetic:
   a 60% hit rate on `n = 100` carries a ±2-standard-error band of
   `2 × sqrt(0.60 × 0.40 / 100) = ±9.80pp` `[COMPUTED]`, which is larger than any realistic edge.
4. **"The signal cannot be validated because the seller will not supply a point-in-time sample."**

**Forbidden:** "the signal works", "this is a real edge", "backtested and confirmed", or any phrasing
that drops the universe, the period, the base rate or the cost model.

## §4 — Ten Failure Modes in the Validation Itself

1. **Running step 4 after step 6.** Detection: check the document ordering of the base-rate line and
   the results line. This is the defect that voids everything downstream.
2. **Using restated data as a sample.** Detection: is there an ALFRED vintage per macro observation
   `[VERIFIED — FRED/ALFRED]`?
3. **A current constituent file used as history.** Detection: count delisted names.
4. **A counterfactual in adjectives.** Detection: is there a `$` figure next to it?
5. **A hit rate compared to 50% instead of the base rate.** Detection: is the base rate printed
   beside it?
6. **Overlapping observations counted as independent.** Detection: divide the trade count by the
   overlap factor before computing an error band.
7. **A holdout period that is the seller's.** Detection: whose dates are they?
8. **A universe that quietly excludes the names that hurt.** Detection: ask for the exclusion list.
9. **A cost model that is not stated.** Detection: state the spread and impact assumption in numbers.
10. **A decision pre-commitment with no size.** Detection: is there a dollar figure and a formula?

**Source:** FRED and ALFRED documentation for the restated-versus-vintage distinction; the SEC's
"Accessing EDGAR Data" page for the non-backfilling of post-acceptance corrections; and the arithmetic
in §3 stated as `[COMPUTED]` from the normal-approximation formula on the stated hypothetical inputs.
The regime-conditional base-rate caveat is labelled `[COMMON-PRACTICE]` because it is a convention
about how published base rates are usually computed, not a measurement of any vendor's data.
