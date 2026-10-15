# Trim and Scale-Out Ladder

Profit is booked by taking positions off, not by watching them. This reference defines the ladder, the whole-unit rule that keeps it structurally legal, the trailing rule for the runner, and the minimum-size conditions under which trimming is simply not available.

## The whole-unit rule

**Trim whole structure units. Never fractionate a leg.**

An options structure is a package. A four-leg condor trimmed by "half" is not a smaller condor; it is a condor whose legs have mismatched ratios, which is a different risk profile with different margin treatment and a different worst case. The market does not care that the trim was intended as a partial reduction.

Consequences of the rule:

| Structure | Unit | Legal trim |
|-----------|------|-----------|
| Single long option | 1 contract | Any number of contracts |
| Vertical spread | 1 spread (2 legs) | Whole spreads only |
| Iron condor / butterfly | 1 structure (4 legs) | Whole structures only |
| Calendar / diagonal | 1 pair | Whole pairs only |
| Ratio structure | 1 ratio unit | Whole ratio units only |

**If the remaining position would not divide into whole units, the action is CLOSE, not TRIM.** One spread cannot be trimmed by a third; it can only be closed. This is not a technicality — it is the reason the minimum unit count matters (below).

## The ladder

The standard ladder for a position with three or more units:

| Rung | Fraction of units | Trigger | Rationale |
|------|-------------------|---------|-----------|
| Rung 1 | 1/3 of units | That family's **TP rung 1** in `trade-sizing-recovery`'s Canonical Threshold Table — read the row, do not restate it | Books a win while the position is still working; converts an unrealised number into a fact |
| Rung 2 | 1/3 of units | That family's **TP rung 2**, from the same row, when the row has one; a row with no rung 2 by design makes rung 1 a full exit | Banks the middle of the distribution; the trade is now financed by itself |
| Runner | Remaining 1/3 | Written trailing rule, defined before the runner exists | Keeps the tail — the part of the distribution that pays for the losers |

Rung levels come from `trade-sizing-recovery`, and they are settled **at entry**, not at the moment the price arrives. A rung selected under the influence of a live quote is not a rung.

### Why thirds, and not halves or all-at-once

- **All-at-once** converts every winner into a fixed, small outcome. The tail — the position that goes to 4× — never happens, and the strategy loses the only mechanism that pays for the losers.
- **Halves** leave a runner that is too large to trail comfortably and too large to ignore. Twice the size of a third, it dominates the attention budget while contributing nothing different.
- **Thirds** produce a booked win, a second booked win, and a runner small enough to trail mechanically.

The fractions are a convention [COMMON-PRACTICE]; what matters structurally is that the *first* trim happens before the position is allowed to be a "runner", and that every trim is in whole units.

## Trailing rule for the runner

Write the trailing rule **before** the runner exists, because that is the only moment at which it will be written by a calm decision-maker. It must name:

1. **What is trailed** — the mark of the remaining structure, or a level on the underlying, or a moving average on the underlying. Not "the high".
2. **The trail distance** — an absolute amount, a percentage, or a structural condition (for example: "close below the 20-day", "the mark gives back a third of the peak mark").
3. **The measurement and the session** — closing basis versus intraday; RTH only.
4. **What happens at the trail** — close the runner, or reduce it by half, with the same whole-unit constraint.
5. **The hard deadline** — the DTE at which the runner is closed regardless (usually 3–7 DTE for long premium, because extrinsic stops being worth paying for).

A runner without a written trail is not a runner; it is an unmanaged position that started life as a good trade.

### Trailing rule examples

```text
Long call, runner = 2 contracts of the original 6
  trail on:      the option mark
  distance:      give back 35% of the highest mark reached
  measurement:   closing mark
  action:        close both contracts
  hard deadline: 5 DTE, close whatever remains

Debit vertical, runner = 1 of 3 spreads
  trail on:      the underlying
  distance:      closing basis below the 20-day
  action:        close the spread
  hard deadline: none; the spread's own rungs govern
```

## Minimum unit count (when trimming is unavailable)

| Units held | Trimming available? | The only options |
|-----------|---------------------|------------------|
| 1 | No | Hold to the target, or CLOSE. There is no third option |
| 2 | Barely | 1/1 split only — one unit at rung 1, one at rung 2 / trailing |
| 3+ | Yes | The full thirds ladder |

This is a sizing fact, not a position-management fact, and it is worth saying plainly: **a one-unit position cannot be scaled out of, so its exit must be a single, fully specified decision.** If a strategy's edge depends on scaling out, it needs at least three units, which means the size must be chosen with that in mind at entry. That decision belongs to `trade-sizing-recovery`, and this skill should say so rather than invent a fractional trim to compensate.

## The trim decision, step by step

```text
1. Read the structure's current unit count from the position record (not memory).
2. Read the rung level for that family from trade-sizing-recovery.
3. Is the mark at or above the rung?
   ├─ NO  → no trim. Continue the review.
   └─ YES → continue
4. Does the remaining size divide into whole units after a trim of the ladder fraction?
   ├─ NO  → CLOSE the whole position (or hold to the next rung — but write the choice)
   └─ YES → continue
5. Does the trim leave the intended runner with a written trailing rule?
   ├─ NO  → write the rule FIRST, then trim
   └─ YES → continue
6. Execute the trim as structure trades, not as legs.
7. Re-price the remaining brackets for the new size — a bracket sized for the old
   unit count is a latent order to open an unplanned position.
8. Record: units trimmed, fill, remaining units, the runner's trail, the next rung.
```

Step 7 is the one that gets skipped, and it is the one that creates the incident: a resting sell order for four condors when only two remain is a request to open two naked structures.

## Worked example — a three-rung ladder

```text
Position: 6 call debit spreads on a $5.00-wide spread, debit $1.90 each = $1,140 total
  max profit per spread = $5.00 - $1.90 = $3.10  [COMPUTED]
  rung 1 = 50% of max profit = $1.90 + (0.5 x $3.10) = $3.45    [COMPUTED]
  rung 2 = 75% of max profit = $1.90 + (0.75 x $3.10) = $4.23   [COMPUTED]
  (both rungs read from the debit-vertical row of trade-sizing-recovery's
   Canonical Threshold Table; this file states the order, not the levels)

Day 14
  mark $3.55 -> rung 1 reached
  trim 2 spreads (1/3) at $3.55 -> books $330 profit      [COMPUTED]
  remaining: 4 spreads
  runner rule written: trail on the mark, give back 35% of the highest mark,
    closing mark, hard deadline 5 DTE
  brackets re-priced for 4 spreads (not 6)                 <- step 7

Day 19
  mark $5.10 -> above rung 2
  trim 2 more at $5.10 -> books another $640 profit        [COMPUTED]
  remaining: 2 spreads, peak mark $5.10 -> trail level $3.32

Day 23
  mark falls to $3.28 on the close -> trail fires
  close 2 spreads at $3.28 -> books $276 profit            [COMPUTED]

Total booked: $330 + $640 + $276 = $1,246 on a $1,140 debit  [COMPUTED]
Max drawdown of the winner from peak: the runner gave back roughly 36% of its peak,
  which is exactly what the trail said it would do.
```

Note three things. First, every action was in whole spreads. Second, the trail fired on the *mark*, according to the rule written on day 14 — not according to how the trader felt on day 23. Third, the total outcome includes a runner that gave back a third of its peak, and that is a success: the rule worked.

## The trim-versus-hold argument

The most common argument against trimming is "it might go further". That argument is true and irrelevant. The question is not whether the position might rise; it is whether the remaining reward justifies the remaining risk relative to the capital tied up.

A useful framing at each rung:

| Question | What a "yes" means |
|----------|--------------------|
| Has the position already delivered more than its expected value for the time it consumed? | Trim is early, not late |
| Is the remaining extrinsic a price you would pay to take this position fresh at this mark? | If not, trim |
| Is the position's risk now entirely house money? | Trim the first third without further debate |
| Would you open this position today, at this mark, with this DTE? | If no, the *rest* of the position should go too |

That last question is the strictest and the most useful: applying it to the runner on every review is how a runner becomes a position rather than a souvenir.

## Interaction with the health check

A trim is an action above HOLD, so it triggers the post-action rules:

1. **Re-run step 2** (structure integrity) on the remaining position. The leg counts changed; verify the remaining structure is intact.
2. **Re-run step 7** (instruments). Brackets must match the new size.
3. **Record the action** with its expectation and a grading date. The expectation for a trim is usually "the remainder reaches the next rung, or the trail fires" — state it.
4. **Report the freed capital.** A trim returns buying power; that is relevant to the book and belongs with `options-risk-engineer`.

## Anti-patterns

| ❌ | ✅ |
|----|-----|
| "Sell one leg to take some off" | Whole units only; a leg sale is a structure change, not a trim |
| Trimming at a level chosen while watching the price | Rungs are set at entry; a mid-trade rung is a rule change with a reason and a date |
| Letting the runner have no written trail "for now" | Write the trail before the runner exists — it is the only chance to write it calmly |
| Trimming everything at rung 1 because the market feels heavy | That is a risk-tightening adjustment to an existing plan — allowed, because it reduces exposure, but it needs a written reason and a grading date |
| Forgetting to re-price the brackets | Brackets are sized to the position; re-price them in the same action |
| Trimming a one-unit position "half way" | Impossible; the choice is hold-to-target or CLOSE |
| Treating a booked rung as permission to add without the gate | Rung 1 unlocks the *evaluation* of an add, not the add itself |

## Provenance

- The thirds ladder is a convention derived from the shape of option payoffs [COMMON-PRACTICE]. The rung *levels* it references are not stated here at all: they are the structure-family rows of `trade-sizing-recovery`'s Canonical Threshold Table, and this file owns only the whole-unit ordering of the trims. The ladder fractions are operating bands, not measured constants [ESTIMATED].
- All dollar figures in the worked examples are `[COMPUTED]` from the stated debit, unit count and fills, and are reproducible by hand.
- The whole-unit rule follows from how exchange-listed structures are margined and matched [VERIFIED] Cboe margin manual — strategies are margined as strategies, and a fractionated structure is no longer the strategy it was sized as. Confirm the treatment your own broker applies and tag it `[BROKER-VERIFIED]`.
- Past performance is not a guarantee. A ladder that produced a good average last quarter does not promise anything about the next position; it promises that the decision was made before the pressure arrived.
