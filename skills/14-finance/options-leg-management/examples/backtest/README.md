# Backtest / Evidence Format — options-leg-management

> **This file defines a FORMAT. It contains no measured results.**
> Everything numeric below is either a column definition, an arithmetic example explicitly
> marked `[COMPUTED]` from stated `[ESTIMATED]` inputs, or a placeholder. The desk has not
> published measured outcomes here, and none are invented. Where a real number would go, a
> placeholder is shown instead.

## Why this format exists

A leg operation is only justifiable if it beats the alternative of doing nothing to the legs and
closing the whole structure at the same moment. That comparison cannot be made from memory, so
every operation is recorded in a fixed shape that makes the comparison mechanical later. The
format is the deliverable; the numbers arrive when the book is scored.

## The unit of record: one leg operation

One row per leg operation. A structure that is operated on five times produces five rows, and the
rows for one structure are read together.

| # | Column | Type | Definition |
|---|---|---|---|
| 1 | `op_id` | string | Stable id, e.g. `OLM-<structure>-<seq>` |
| 2 | `tag` | enum | One of `SC` `RU` `VD` `HM` `PG` `CD` `CR` `UD` — exactly one |
| 3 | `timestamp` | ISO 8601 | The moment the operation was executed, not drafted |
| 4 | `structure_id` | string | Links rows belonging to one position |
| 5 | `pre_leg_list` | list | Live leg list before the order: signed quantity, strike, right, expiry, avg price |
| 6 | `package` | list | The legs submitted, as one complex order, with sides and a net price |
| 7 | `post_leg_list` | list | Resulting leg list, with the R1 test result written beside it |
| 8 | `r1_result` | enum | `PASS` / `FAIL` — `FAIL` must be followed by the repair row |
| 9 | `units_before` / `units_after` | integer | Structure-unit counts; drives whether a later scale-out is legal |
| 10 | `net_cash_usd` | decimal | Signed cash from the package, in dollars per unit and in total |
| 11 | `slippage_vs_natural_usd` | decimal | Fill versus the natural at drafting time, in structure units |
| 12 | `basis_after_usd` | decimal | Surviving structure's basis, **re-derived from the fill** |
| 13 | `max_loss_after_usd` | decimal | Per unit and in total, with the strike arithmetic that produces it |
| 14 | `counterfactual_close_usd` | decimal | The price of closing the WHOLE structure at the same timestamp |
| 15 | `provenance` | enum | Per figure: `[COMPUTED]` `[ESTIMATED]` `[VERIFIED]` `[BROKER-VERIFIED]` `[COMMON-PRACTICE]` |
| 16 | `validity_condition` | string | The condition under which the operation remains the right decision |
| 17 | `recheck_date` | date | When the row's outcome is revisited |

`[COMMON-PRACTICE]` This column set is the desk's evidence convention. It is not prescribed by
any exchange, clearing organisation or regulator.

## The comparison that gives the format its purpose

```text
  leg_op_outcome      =  value of the surviving position at the scoring date
                         + net cash taken out by the operation
                         + net cash taken out by LATER operations on the same structure

  counterfactual      =  value, at the SAME scoring date, of the position that would
                         have existed if the whole structure had been closed at
                         `counterfactual_close_usd` at the operation's timestamp

  delta               =  leg_op_outcome - counterfactual

  verdict             =  delta > 0   ->  the operation added value; keep the tag
                         delta = 0   ->  neutral; keep the tag only if it reduced a
                                         risk that was actually carried
                         delta < 0   ->  the operation destroyed value; the tag is
                                         retired after a second confirming case
```

Two rules keep the comparison honest:

1. **Same timestamp, same scoring date.** Both sides are marked at the operation's timestamp and
   scored on the same later date.
2. **Whole-structure counterfactual.** The comparison is never "leg op versus holding everything
   forever"; it is "leg op versus closing the whole structure at that moment". The second is a
   decision the desk could actually have taken.

## Record shape (one row, filled with placeholders)

```text
  op_id                    OLM-<structure>-001
  tag                      VD
  timestamp                <ISO 8601>
  structure_id             <id>
  pre_leg_list             +2x K1C / -4x K2C / +2x K3C   (2 units)
  package                  { sell 2x K3C ; buy 2x K2C }   net <net price>
  post_leg_list            +2x K1C / -2x K2C              R1: PASS
  units_before / after     2 / 2
  net_cash_usd             <$ per unit> / <$ total>      [COMPUTED]
  slippage_vs_natural_usd  <$>                          [COMPUTED]
  basis_after_usd          <$>                          [COMPUTED from the fill]
  max_loss_after_usd       <$ per unit> / <$ total>     [COMPUTED]
  counterfactual_close_usd <$ at this timestamp>        [COMPUTED]
  provenance               see per-figure tags above
  validity_condition       "far wing value >= ~30% of structure value AND DTE <= 7"
  recheck_date             <date>
```

## Arithmetic example of the format (not a measured outcome)

Using the illustrative strike set from
`../references/leg-arithmetic-worked-examples.md` (all inputs `[ESTIMATED]`, all results
`[COMPUTED]`):

| Field | Value | Tag |
|---|---|---|
| Fly entry debit | `$135` per unit | `[COMPUTED]` from `[ESTIMATED]` leg premiums `6.10 / 3.05 / 1.35` |
| Vertical-downgrade package | net `$170` per unit (`+135` from the wing, `−305` on the body) | `[COMPUTED]` |
| Basis after | `$305` per unit | `[COMPUTED]` |
| Max loss after | `$305` per unit; `$610` for 2 units | `[COMPUTED]` |
| Scale-out trigger | `1.8 × 135 = $243` profit per unit | `[COMPUTED]` |

These are arithmetic identities on stated inputs. They are shown so a reader can verify the
column definitions by recomputing them, not as a report of what any position earned.

## Best case — what the format records

The **best case** field is not a forecast. It records, for a completed operation, the largest
positive `delta` observed across the rows that share a tag, together with the conditions that
produced it. The format requires:

- the tag and the number of rows behind it (a `delta` from one row is an anecdote, not a finding);
- the market conditions recorded at the operation's timestamp — trend, implied-volatility
  percentile band, and the days-to-expiry bucket;
- the counterfactual used, so a reader can re-derive the number;
- an explicit statement that it is `past performance` on one book and not a `guarantee`.

## Worst case — what the format records

The **worst case** field records the most negative `delta` seen for a tag, and it must carry a
linked failure-mode entry — the row is incomplete without it. It also records the exit condition
that would have prevented it: for example, the pin band that should have fired at `≤ 2 DTE`, or
the cost cap that should have stopped a calendar roll at `~50%` of the current mark. A worst case
without a named exit condition is data the desk cannot act on.

## Learnings — what the format records

Each review writes **actionable lessons**, in the form: *condition → operation → observed
delta → keep or retire the tag*. Examples of the shape (content pending real rows):

- Key takeaway to record: whether a tag's positive delta concentrates in one volatility regime,
  which would make it a regime tool rather than a general one.
- Actionable lesson to record: whether the sequencing fallback (shorts-first after a rejection)
  correlates with worse fills than a package that filled on the first attempt.
- What this format exists to validate: that `VD` and `HM` add value relative to closing the whole
  structure, and that `RU` (financed roll-up) does not quietly behave like an add.

A tag that fails to produce a positive `delta` on two independent samples is retired from the
playbook. Retiring a tag is a successful outcome of this format, not a failure of the skill.

## Regime segmentation

Every summary of these rows is segmented by regime, because a tag that wins in one and loses in
another is a regime-specific tool:

| Regime | Segmentation field to record |
|---|---|
| Bull market / uptrend | Trend classification at the operation's timestamp |
| Correction / pullback | Drawdown band from the local high |
| Bear market / downturn / recession | Trend classification, plus a longer lookback |
| Crash / tail event / black swan (e.g. March 2020, the 2008 financial crisis) | Flagged as a tail event, with a note on liquidity conditions at the timestamp |

Regime classification uses the Pattern Recognition Engine meta-layer referenced by the skill;
its thresholds and the thresholds in this format are data-backed desk thresholds derived from
data on this desk's own study — approximate, not exchange rules, and not a guarantee.

## Provenance and uncertainty

- `[VERIFIED]` The two structural facts the format depends on: a listed option is a separable,
  independently exercisable instrument, and a multi-leg position is not one instrument to the
  exchange (OCC standard options disclosure document; US options exchange rules). Both matter
  because they are what make "close the whole structure" a real counterfactual and a leg
  operation a real decision.
- `[COMPUTED]` Every figure in the arithmetic example above follows deterministically from the
  stated inputs; recompute it rather than quoting it.
- `[ESTIMATED]` All price inputs in that example are illustrative. Real quotes on cheap legs are
  indicative and can be stale; a fill is not a guarantee of the model.
- `[BROKER-VERIFIED]` The fill prices, commissions and assignment notices this format depends on
  are broker-specific. Read them from the broker's records, not from a summary screen.
- `[COMMON-PRACTICE]` The column set, the two-sample retirement rule and the no-op review row are
  desk conventions.
- Limits: this format does not measure portfolio-level risk, capital efficiency or margin
  utilization. Those belong to `options-risk-engineer`. It is also approximate wherever a quote
  is stale or a fill is partial, and `past performance` recorded here does not predict the next
  result. No row in this file is a measured outcome.
