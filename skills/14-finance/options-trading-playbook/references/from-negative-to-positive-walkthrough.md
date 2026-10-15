# From Negative to Positive: A Walkthrough

A worked case. Not a success story — a *sequence*, with the arithmetic at each step
and the honest verdict after each cycle. Every number is the tool's own output or a
`[COMPUTED]` derivation from the printed formula. Nothing here claims the strategy
made money, and the final state is a genuine uncertainty rather than a result.

The book in this walkthrough is invented for the purpose and is labelled as such
wherever it appears. Its arithmetic is checkable; its market behaviour is not a
finding.

---

## The starting position

A retail options book, six months in. Two corners are being traded at once, which
is itself the first finding.

| Cohort tag | Corner | Cards | Realised `p` | Realised `b` | Realised `E` gross | Cost | `E_net` |
|---|---|---|---|---|---|---|---|
| `credit-condor-50-2x` | short premium, 50% / 2× | 40 | 0.775 | 0.250 | **−0.03125R** | 0.0260R | **−0.05725R** |
| `debit-spread-2.5R` | long premium, 2.5R / 1R | 40 | 0.350 | 2.470 | **+0.21450R** | 0.0130R | **+0.20150R** |

Both rows are `[COMPUTED]` and both are reproducible from
`examples/logs/synthetic-options-log.csv` — a **SYNTHETIC** fixture invented by the
skill author, not market data, not a backtest, and carrying no market information:

```bash
cd skills/14-finance/options-trading-playbook
py -3 scripts/payoff_check.py --from-log examples/logs/synthetic-options-log.csv
```

### Finding 1 — the pooled book hides both corners

Pooled across all 80 rows: `p = 0.5625`, `b = 0.9407`, `E = +0.0916R`,
`E_net = +0.0721R`, `se_E = 0.1076R`.

The pooled verdict is **MARGINAL** (`0.0721 < 0.1076`). Pooling produced a number
that is neither corner's number and cannot be acted on. The `setup` tag is what
makes the two rows visible; without it, this book looks like a thin positive with no
way to improve it.

**Cycle 0 hypothesis — lever: measurement, not the card.** Change: separate the
cohorts. Prediction: at least one cohort is negative and at least one is positive,
and the pooled figure conceals both.

**Result:** confirmed. `credit-condor-50-2x` is at `−0.05725R`; `debit-spread-2.5R`
is at `+0.20150R`. Two corners were being run as one book, and the losing one was
financed by the winning one — which is the most expensive way to hold a losing
strategy.

---

## Cycle 1 — retire the negative corner, do not repair it

The tempting move is to fix the condor: tighten the stop, narrow the wings, add a
filter. That is the search `references/overfitting-by-iteration.md` prices.

Set up the decision properly. The condor's card is `b = 0.25`, so:

```
p* = 1 / (1 + 0.25) = 80.00%                             [COMPUTED]
realised p = 0.7750, so edge = 0.7750 - 0.8000 = -2.50 percentage points  [COMPUTED]
```

A repair has to move `p` by more than 2.5 points *net of the cost correction*:

```
p*_net = (1 + c_R) / (1 + b) = 1.0260 / 1.25 = 82.08%    [COMPUTED]
```

The book needs **4.58 percentage points of win rate** — from 77.50% to 82.08% — to
reach break-even. At 40 trades, `se_p = sqrt(0.775 × 0.225/40) = 0.0660`
`[COMPUTED]`, so the current estimate has an interval of roughly 71% to 84%. **The
required win rate is inside the measurement's own interval**, which means the card
cannot be shown either to clear it or to fail it on this record.

**Cycle 1 hypothesis — lever: `b` (a rules change), no new measurement needed.**
Change: move the condor's stop from 2× to 1× the credit, target unchanged at 50%.
Prediction: `b` rises from 0.250 to 0.500, so `p*` falls from 80.00% to 66.67%, and
the card becomes positive at the *same* realised win rate.

```bash
py -3 scripts/payoff_check.py --credit 1.00 --width 5.00 \
    --tp-money 50 --sl-money 100 --p 0.775 --fee-per-contract 0.65 --legs 4
```

Expected: `c_R = 5.20/400 = 0.0130R`, `E = 0.775 × 0.5 − 0.225 = +0.1625R`,
`E_net = +0.1495R` `[COMPUTED]`.

**The honest objection, and it is decisive.** The realised `p` of 0.775 was measured
with a 2×-credit stop. Moving the stop to 1× makes the stop fire more often. **The
`p` that will be realised after the change is not 0.775** — it is lower, by an amount
nobody in this book has measured. The prediction above is therefore not a prediction;
it is an arithmetic statement conditional on an input that the change itself moves.

So the cycle is designed correctly:

- **Lever:** `b`. **One change.** The stop moves; the target, the entry condition and
  the leg count do not.
- **Cycle length:** `n_req` for the *post-change* card. Take the conservative case
  `p = 0.70, b = 0.50` → `E = +0.0500R`, `sd = 0.6874R` → `n_req = 4 × (13.748)² = 756`
  `[COMPUTED]`. Round to 760 trades.
- **Holdout:** fit on trades 1–532, check on 533–760. Never re-fit.
- **Log:** every trade tagged `credit-condor-50-1x` — a **new** cohort tag, because
  the exits changed. Pooling with `credit-condor-50-2x` would merge two cards.
- **Bar:** `m = 1` for this new cohort, so `alpha_adjusted = 0.05` and the threshold
  is `z = 1.96`.

**Realism check before running it.** 760 trades of one card at a retail pace is
approximately 3 years. The cycle is affordable only if the account trades this card
as its main strategy. If it does not, the correct conclusion is that **the card
cannot be graded**, and the response is a card with a larger `E`, not a shorter
window.

---

## Cycle 2 — the cost lever, which is free

While Cycle 1 is running, pull the cost lever. It needs no new trades.

The condor pays `legs × 2 × fee = 4 × 2 × 0.65 = $5.20` per round trip
`[COMPUTED]`. On the `$400` max-loss structure that is `c_R = 0.0130R`.

Two cost changes are available without touching the market:

1. **Reduce the leg count.** A 2-leg vertical in place of the 4-leg condor pays
   `$2.60`, halving `c_R` to `0.0065R`. The cost is that a vertical is directional
   and the condor is not; this is a *different corner*, and it belongs to
   `options-strategist` to construct. It is a corner change, not a cost change, and
   a corner change resets `m`.
2. **Stop splitting the exit into rungs.** If the condor is being scaled out in
   thirds, the derived threshold is:

```
fee_negative  iff  position_value < rung_split x legs x fee_per_contract
                                     = 3 x 4 x 0.65 = $7.80              [COMPUTED]
```

```bash
py -3 scripts/payoff_check.py --scaling-check --legs 4 \
    --fee-per-contract 0.65 --rung-split 3 --position-value 5.00
```

At a `$5.00` mark the tool reports `FEE-NEGATIVE`, with a shortfall of `$0.93` per
rung and an extra fee of `$5.20` across the three rungs — exactly the round-trip
cost of opening the structure. Replacing the three-rung scale-out with a single
close saves `$5.20` per position, i.e. it removes a whole round trip from every
trade.

**Cycle 2 hypothesis — lever: `c_R`. Change: single close instead of a three-rung
scale-out. Prediction: `c_R` falls by `5.20/400 = 0.0130R`, and `E_net` rises by the
same amount on every trade regardless of outcome.**

That prediction is unusual and worth noting: **it does not depend on `p` or `b` at
all.** A cost reduction is the only lever in this skill whose effect is known before
the outcome is. It is therefore the first lever to pull, always.

---

## Cycle 3 — the winning corner, held as a card

`debit-spread-2.5R` realised `p = 0.350`, `b = 2.470`, `E = +0.21450R`, with 40
trades. Its `se_E` is `0.2617R`, so **its realised edge is inside its own noise**:

```
E_net = 0.2015R   vs   se_E = 0.2617R   ->  0.2015 < 0.2617            [COMPUTED]
```

The tool's own `n_req` line for this cohort says it needs **239 trades** to see the
edge at 2σ. Forty trades is not a result; it is the first sixth of a result.

**Cycle 3 hypothesis — lever: `p` (a measurement, not a change). Change: none. Run
the same card to 239 trades with no modification and check whether the realised `p`
stays near 0.35 and `b` near 2.47. Prediction: if the card is real, `E` stays in the
neighbourhood of `+0.21R`; if the 40-trade reading was a favourable draw, it decays
toward zero.**

This is the correct use of a winning streak: **not to size up, but to run the same
card until the sample supports it.** The `se_E` is large precisely because the sample
is small; the fix is more of the same, not a change.

---

## The state after three cycles, stated honestly

| Cohort | Cycles `m` | Realised `E_net` | `se_E` | Bonferroni bar | Status |
|---|---|---|---|---|---|
| `credit-condor-50-2x` | 1 | −0.05725R | 0.0825R | 0.0868R (m=1) | **retired** — negative, and the required `p` is inside the measurement interval |
| `credit-condor-50-1x` | 1 | not yet measured | — | 0.0868R (m=1) | running, 760-trade cycle |
| `debit-spread-2.5R` | 1 | +0.20150R | 0.2617R | 0.0868R (m=1) | **unproven** — edge inside its own noise; needs 239 trades |
| whole book | — | +0.0721R pooled | 0.1076R | — | **MARGINAL and meaningless as a pooled figure** |

**What this walkthrough has established:** one corner was negative and is retired; one
corner is positive on too little evidence to grade; one repair is designed but not yet
run; one free cost saving was identified.

**What it has NOT established:** that any strategy is profitable. Not one of the four
rows above is a positive result. The best row is a *candidate with a sample plan*.

---

## The four levers, ranked by cost of pulling

| Rank | Lever | Cost to change | Requires new trades? | Requires a forecast? |
|---|---|---|---|---|
| 1 | `c_R` | a commission schedule | No | No |
| 2 | `b` | one rules change on the card | Yes — `p` must be re-measured | No |
| 3 | corner | a new structure and a new tag | Yes — resets `m` to 1 | No |
| 4 | `p` | research, data, new entries | Yes | **Yes** |

Pull them in that order. Most books invert it, starting at 4 — the most expensive and
least certain lever — because it is the one that sounds like skill.

---

## Failure modes

1. **Failure mode — the positive corner is used to justify keeping the negative one.**
   A pooled `+0.0721R` containing a `−0.05725R` cohort is a book paying to hold a losing
   strategy. Pooling is how that decision gets hidden.
2. **Failure mode — the negative corner is repaired rather than retired.** Repair is a
   search; the five-cycle rule in `references/the-iteration-protocol.md` is what makes
   the search visible.
3. **Failure mode — a stop change is assumed to leave `p` unchanged.** It cannot. The
   stop is the input whose whole job is to set how often the trade loses.
4. **Failure mode — the winning cohort is pooled with the losing one for reporting.**
   Every cohort's number must be shown separately, and the pooled row must be labelled
   as what it is — an average of two strategies, not a strategy.
5. **Failure mode — the 760-trade cycle is quietly shortened.** The measurement window
   is the hypothesis. Shortening it converts the cycle into a peek.
6. **Failure mode — the cost saving is counted as an edge.** A `0.0130R` cost saving is
   real and unconditional; it is not evidence that the card works. Both facts must be
   reported, and separately.
7. **Failure mode — "the book is flat" is treated as a state to escape rather than a
   measurement to act on.** A flat pooled figure containing one negative and one
   unproven cohort is three findings, not a problem with the trader.
8. **Failure mode — the walkthrough is read as a template for a profitable book.** It
   is a template for a *disciplined sequence*. The outcome of that sequence is unknown
   and is not promised by anything in this skill.

---

## Reproduce it

```bash
cd skills/14-finance/options-trading-playbook

# both cohorts, realised p / b / E / E_net, and n_req per cohort
py -3 scripts/payoff_check.py --from-log examples/logs/synthetic-options-log.csv

# the retired corner beside the card it was traded on
py -3 scripts/payoff_check.py --from-log examples/logs/synthetic-options-log.csv \
    --setup credit-condor-50-2x --tp 0.5 --sl 2.0 --p 0.775

# the repair, priced
py -3 scripts/payoff_check.py --credit 1.00 --width 5.00 \
    --tp-money 50 --sl-money 100 --p 0.70 --fee-per-contract 0.65 --legs 4

# the free lever
py -3 scripts/payoff_check.py --scaling-check --legs 4 \
    --fee-per-contract 0.65 --rung-split 3 --position-value 5.00
```

`examples/logs/synthetic-options-log.csv` is **SYNTHETIC / ILLUSTRATIVE**. It is not
market data. Nothing derived from it is a finding about any instrument, strategy or
period.

See also: `references/the-iteration-protocol.md`,
`references/overfitting-by-iteration.md`,
`references/what-this-cannot-promise.md`, `references/cost-drag-per-leg-and-per-rung.md`.
