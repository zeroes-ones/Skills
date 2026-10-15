# Partial Scale-Out Lot Ordering — taking a third off a four-lot position

## The problem stated plainly

A position is four lots of 100 shares each, acquired at four different prices. The holder
wants to take **a third** of the position off. There is no lot called "a third". The sale must
be expressed as some number of shares drawn from some combination of lots, and that expression
is what determines the tax cost.

The position: 400 shares, price **$120.00** `[ESTIMATED]`.

| Lot | Qty | Basis/sh | Basis total | Gain/(loss) at $120 | Character |
|---|---|---|---|---|---|
| L1 | 100 | $50 | $5,000 | **$7,000 gain** `[COMPUTED]` | long-term |
| L2 | 100 | $90 | $9,000 | **$3,000 gain** `[COMPUTED]` | short-term |
| L3 | 100 | $140 | $14,000 | **$2,000 loss** `[COMPUTED]` | short-term |
| L4 | 100 | $95 | $9,500 | **$2,500 gain** `[COMPUTED]` | short-term |

A third of 400 shares is **133.33 shares** `[COMPUTED]`. That is not a lot boundary, and it is
not even a whole share. The first decision is therefore not "which lot" but "how to express
the size".

## Step 1 — express the trim in whole lots, or accept a split

| Approach | What it means | Cost |
|---|---|---|
| **Round to one whole lot** | Sell 100 shares = a quarter of the position, not a third | The trim is 25% instead of 33%. The difference is a re-sizing decision, not a tax one |
| **Round to 100 + part of a second lot** | Sell 133 shares: 100 from one lot, 33 from another | Two lots are touched; the partial 33-share identification must be recorded, and 67 shares of that lot remain |
| **Sell pro-rata across all four lots** | Each lot contributes 33.33 shares — which is not a whole share | Not expressible without rounding, and it forfeits the entire lot-selection advantage |

The recommendation is almost always the first: **re-size the trim to whole lots.** A trim
target expressed in percentages of a position is a soft target; the tax and operational cost
of a fractional lot identification is real. "Sell a quarter" is easier to explain, easier to
record, and easier to defend than "sell a third, split across L2 and L3".

## Step 2 — pick the lot with the four objectives, in order

The four objectives from the skill body, applied to a partial sale:

```text
   (a) Realize the LOSS first, if there are gains to offset.
   (b) Among gains, prefer the LONG-TERM lot on an equal gross gain.
   (c) Among equal tax outcomes, prefer the lot with the WORST risk-adjusted
       forward outlook.
   (d) NEVER let the tax tail create a worse economic position.
```

Applied to the table above, with **$3,000 gain** `[ESTIMATED]` of realized short-term gains
available to offset, and short-term rate 40.8% `[ESTIMATED]` / long-term 23.8% `[ESTIMATED]`:

| Choice | Gross realized | Tax effect | Net after-tax at $120 |
|---|---|---|---|
| Sell 100 × L1 (FIFO) | **$7,000 gain** `[COMPUTED]` | `0.238 × 7,000` = **$1,666 cost** `[COMPUTED]` | **$5,334** `[COMPUTED]` |
| Sell 100 × L3 | **$2,000 loss** `[COMPUTED]` | `0.408 × 2,000` = **$816 saved** `[COMPUTED]` | **−$1,184** `[COMPUTED]`: −2,000 + 816 = −1,184 |
| Sell 100 × L4 | **$2,500 gain** `[COMPUTED]` | `0.408 × 2,500` = **$1,020 cost** `[COMPUTED]` | **$1,480** `[COMPUTED]` |

Objective (a) says L3, but two quantities must not be conflated here: the "net" column above
is realized gain net of tax, while the lot choice is really between two after-tax **proceeds**
figures on the same **$12,000 gross** `[COMPUTED]`.

- **Tax-liability difference:** the FIFO answer books `0.238 × 7,000` = **$1,666 cost**
  `[COMPUTED]` where the L3 answer books **$816 saved** `[COMPUTED]` — `1,666 + 816` =
  **$2,482** `[COMPUTED]` of tax the default would have given away.
- **After-tax P&L swing:** on the bottom line of the table above, L1's **$5,334** `[COMPUTED]`
  against L3's **−$1,184** `[COMPUTED]` is `5,334 − (−1,184)` = **$6,518** `[COMPUTED]`.

Both are true, and they answer different questions. Neither of them is objective (d) — that
test is next.

But objective (d) then applies: L3 only wins if it is also a defensible thing to sell. If L3
is the strongest lot on outlook, the tax saving is being bought by giving up the better
position, and the arithmetic is a mirage.

## Step 3 — keep the remaining basis reportable

This is the operational half of a partial sale, and it is where records quietly rot.

When 33 shares of a 100-share lot are sold:

- The lot's **per-share basis does not change**. It remains $90.00, not a blended figure.
- The lot's **open quantity becomes 67 shares**.
- The remaining 67 shares keep the **original acquisition date** and therefore the original
  holding-period clock. No part of the date resets.
- The broker's lot export shows the surviving 67-share lot — confirm it does after settlement.
- The ledger row records: lot consumed, quantity consumed, quantity remaining, basis per
  share unchanged, box dates, re-entry date.

Write the remaining quantity as a **per-lot fact**, not a per-position one. A position record
that says "400 shares bought at various prices, now 367" has destroyed the information the
next sale depends on.

## Worked partial sale

Sell 133 shares: **100 from L2** and **33 from L3**.

```text
   L2 portion:  100 × (120.00 − 90.00)  =  $3,000 gain
   L3 portion:   33 × (120.00 − 140.00) =    $660 loss
   net realized                          =  $2,340 gain
```

`[COMPUTED]` Tax effect: the L3 portion's loss is short-term and offsets the short-term L2
gain, so the taxable amount is `3,000 − 660` = **$2,340 gain** `[COMPUTED]`, taxed at
`0.408 × 2,340` = **$955 cost** `[COMPUTED]`. Remaining: L2 zero shares, L3 **67 shares** at
**$140.00** per share `[COMPUTED]`.

Compare with selling 100 shares of L1 alone, which realizes **$7,000 gain** `[COMPUTED]` at
the long-term rate, `0.238 × 7,000` = **$1,666 cost** `[COMPUTED]`. The split sale costs
`955` against `1,666` — **$711 less** `[COMPUTED]` — and leaves the low-basis L1 lot intact.

Which is better depends entirely on what happens next. Keeping L1 means a **$7,000 gain**
`[COMPUTED]` of deferred tax still travels with the account. The point of the arithmetic is
not that one answer is always right; it is that the answer is computable and the default
answer is usually not the chosen one.

## Ordering a trim ladder

A scale-out is usually a series, not a single sale. Sequence it deliberately:

1. **First rung:** the loss lot, if a real offset exists and the 61-day box is clear.
2. **Second rung:** the long-term lot with the weakest forward outlook.
3. **Third rung:** the short-term lot with the weakest forward outlook.
4. **Last:** the strongest lot, and only if the objective genuinely requires selling it.

Pre-commit the ladder before the first rung. A ladder invented at the moment of the second
rung is a rationalization.

## Failure modes

1. **What goes wrong — the fractional trim.** A trim sized as a third of a four-lot position cannot be expressed in lots, and the broker defaults the remainder without anyone deciding.
2. **What goes wrong — the blended basis.** After a partial sale, someone averages the remaining shares and the lot table loses the per-share basis and the original acquisition date.
3. **Worst case — the FIFO default.** The lowest-basis, long-term lot is consumed because the ticket carried no instruction; on the worked numbers that is **$1,666 cost** `[COMPUTED]` where a loss worth **$816 saved** `[COMPUTED]` was available.
4. **What goes wrong — the mirage.** The loss lot is sold because the tax column looks best, when it is also the strongest lot on outlook.
5. **What goes wrong — the ladder invented mid-way.** Rungs two and three are chosen after rung one has already changed the position, with no written plan to check them against.
6. **What goes wrong — the box across rungs.** Rung two is a loss sale within 30 days of a purchase made for rung one, and the box is now open.
7. **Known limitation — this file does not price the forward outlook.** Objective (c) and (d) depend on inputs from `fundamental-analyst` and `technical-signals-engineer`, which this skill consumes but does not produce.
8. **Edge case — the odd-share lot.** A position with an odd-lot component (for example 37 shares) cannot be trimmed in round lots at all, and every rung becomes a partial-lot identification.
9. **Edge case — the corporate action between rungs.** A split between rung one and rung two changes every quantity and every per-share basis; the pre-committed ladder must be restated after it.
10. **What goes wrong — the unrecorded partial.** The ledger row recorded the position, not the lot, so the next sale cannot tell how many shares of which lot remain.

## Checklist

- [ ] Trim expressed in whole lots, or the split named lot by lot with quantities.
- [ ] Four objectives applied in order, with the winner named by acquisition date and basis.
- [ ] After-tax figure shown for every candidate, plus the FIFO default's figure.
- [ ] Remaining quantity and unchanged per-share basis recorded **per lot**.
- [ ] 61-day box checked for every loss rung of the ladder.
- [ ] Trim ladder pre-committed before the first rung is placed.
- [ ] Ledger row created before the order, tagged `PS`, carrying the per-lot outcome.
- [ ] Lot table refreshed from the broker's export after settlement.
