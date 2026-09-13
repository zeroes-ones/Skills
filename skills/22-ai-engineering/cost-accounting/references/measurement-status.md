# Measurement Status

<!-- STANDARD: 3min -- measured, computed, estimated and unknown, and why the distinction must live in the data -->

## The failure this file prevents

```text
Dashboard:  total agent spend this month = $12
Invoice:    total agent spend this month = $31,400
```

Both are "correct". The dashboard summed a field that defaulted to `0.0` because nothing
reported usage. This is the single most expensive accounting defect there is — not because the
number is wrong, but because it is *plausible*, and it suppresses exactly the alarm someone
needed.

## The four statuses

Every cost figure is in exactly one of these. The status is part of the figure, not a footnote.

| Status | Meaning | Tag | How you state it |
|---|---|---|---|
| **Measured** | usage was reported by the executor, priced at a known rate | `[VERIFIED]` | "the run cost $0.0288, measured" |
| **Computed** | tokens were reported but priced by you, or the figure is derived | `[COMPUTED]` | "$0.0341 computed from 8,400 tokens at the rate on <date>" |
| **Estimated** | derived from a comparable measured run, with an assumption | `[ESTIMATED]` | "≈$0.03 estimated from a comparable run; assumes similar node count" |
| **Unknown** | nothing was reported and no basis exists | — | "cost unknown — the executor reported no usage" |

**The critical rule:** *unknown* is a valid, reportable answer. It is not a zero, and it is not a
reason to invent a number. A system that cannot say "unknown" will say "zero", and zero reads as
"free".

## Why the flag lives in the data

If the distinction exists only in prose — a caveat in a doc, a note in a comment — it does not
survive being copied. Numbers travel: into a slide, a spreadsheet, a quarterly review, a vendor
conversation. The caveat does not travel with them.

```json
"cost": {
  "tokens_in": 3600,
  "tokens_out": 1200,
  "cost_usd": 0.0288,
  "measured": true,
  "unreported_nodes": []
}
```

```json
"cost": {
  "tokens_in": 0,
  "tokens_out": 0,
  "cost_usd": 0.0,
  "measured": false,            // ← the field that stops the zero being read as free
  "unreported_nodes": ["review", "fixer"]
}
```

The second record says, unambiguously: **nothing was reported, and here is which nodes failed to
report**. That is a diagnosable state, which is what makes it fixable.

## How a run reaches each status

```text
Did the executor return a usage object for this node?
├── No → the node's cost is UNKNOWN. Add it to unreported_nodes.
│        The run's cost is UNKNOWN if ANY node is unreported and matters.
└── Yes → tokens and cost are recorded for the node:
    ├── Did the executor supply cost_usd itself?
    │   ├── Yes → MEASURED (the executor priced it)
    │   └── No, tokens only → COMPUTED by you:
    │       └── price × tokens, with the price source and date recorded
    └── Was the run total reconciled against the provider's invoice?
        ├── Yes → confidence is high; state the variance
        └── No  → the internal figure is a model of the bill, not the bill
```

## The partial-reporting case

The hard case: some nodes report, some do not.

```text
run total (reported subset)  = $0.0180
unreported nodes             = ["review"]
→ the true cost is GREATER than $0.0180, by an unknown amount

Correct statement: "at least $0.0180; the review node reported no usage"
Incorrect:         "$0.0180"
```

**State a floor, not a total.** "At least X" is honest and useful; presenting the reported subset
as the total is the same silence-as-zero error, one level down.

## Reconciliation: the ground truth

The invoice is the only figure that is certainly real. Everything internal is a model of it.

| Practice | Why |
|---|---|
| Reconcile periodically (monthly at least) | the only check on the whole accounting chain |
| Record the variance, not just pass/fail | a 3% variance is normal; 40% means something is unmeasured |
| Reconcile per model, where the invoice breaks it down | locates the drift to a component |
| Record the date of reconciliation | a figure from an unreconciled month is weaker than one from a reconciled one |
| Investigate a *fall* in variance too | it can mean reporting broke, not that accounting improved |

**The variance is itself a metric.** A stable small variance says the accounting is trustworthy. A
growing one says something is being spent that nothing is measuring.

## What to say in each situation

| Situation | Say this |
|---|---|
| Reported and priced | "the run cost $0.0288, measured" |
| Tokens reported, you priced them | "$0.0341 computed from 8,400 tokens at the <date> rate" |
| Nothing reported, comparable run exists | "≈$0.03, estimated from a comparable 3-node run" |
| Nothing reported, no basis | "cost unknown — no usage was reported for this run" |
| Some nodes reported | "at least $0.0180; the review node reported no usage" |
| Reconciled against the invoice | "$0.0288 measured, reconciled to the invoice on <date>, 2% variance" |

Every one of those is defensible. None of them is a number presented without its provenance.

## Checklist

- [ ] Every cost figure in the data carries a `measured` flag (R1)
- [ ] Unreported nodes are named, so the gap is diagnosable
- [ ] "Unknown" is an available answer in the reporting, not an impossible one
- [ ] A partially reported run is stated as a floor, never as a total
- [ ] Computed figures name the price source and its date
- [ ] Estimated figures name the comparable run and the assumption
- [ ] Internal accounting is reconciled against the invoice, with the variance recorded
- [ ] The variance is tracked over time, including falls
- [ ] No figure reaches a decision-making context without its status
