# Year-End Harvest Calendar — working backwards from December 31

## The two deadlines that are actually one

A year-end harvest has two dates attached to it, and a plan that sets only the first is half
a plan:

1. **The last day to realize a loss that counts in this tax year.** The tax year is
   determined by the **trade date**, not the settlement date, so this is the last trading
   session of the calendar year — normally December 31, or the preceding business day if the
   market is closed.
2. **The first day the position can be re-acquired without creating a wash sale.** That is
   **day 31 after the loss sale**, counting from the sale. `[VERIFIED — IRC §1091(a)]`

Set them together. The distance between them decides whether the holder is out of the
position into January, and that is a market-exposure decision, not a tax one.

## The calendar, drawn

```text
   Nov 30            Dec 1                                         Dec 31
     │                 │                                              │
     │  sell here ─────┼───── day 31 lands on Dec 31 → can re-enter   │
     │                 │        inside the SAME tax year              │
     │                 │                                              │
     │                 └── sell after Dec 1 → day 31 lands in January │
     │                        → out of the position into the new year │
     └── last day to sell a loss AND be back in the position this year
```

`[COMPUTED]` The arithmetic: a loss sale on **November 30** has a box ending
`November 30 + 30` = **December 30**, so **December 31** is day 31 and the first safe
re-entry. A loss sale on **December 1** has a box ending **December 31**, so the first safe
re-entry is **January 1** of the next year.

That one-day shift is the entire shape of the December decision:

- **Sell by November 30** → the loss counts in this year *and* the position can be re-entered
  before the year ends, with no gap into January.
- **Sell in December** → the loss still counts in this year (the trade date is in December),
  but the position cannot be re-entered until January, so the holder spends the year boundary
  out of the market, or in a cleared substitute.

Both are legitimate. Only one of them was usually intended.

**The day-numbering convention used throughout this file.** Every "day N" here is
**sale-relative**: the **loss sale is day 0**, the box runs **day −30 to day +30**, and the first
safe re-entry is **day +31**. The wash-sale playbook counts the other way, from the box itself
(**box day 1 = the box start**), so one date carries two numbers — January 5 is **day +16** here
and **box day 47** there `(references/wash-sale-window-playbook.md)`.

## Worked: the December 20 harvest

A holder sells at a loss on **December 20** to book the loss this year, then re-buys on
**January 5** because the new tax year has begun.

| Step | Date | Arithmetic |
|---|---|---|
| Loss sale | December 20 | day 0 |
| Box opens | November 20 | `December 20 − 30` `[COMPUTED]` |
| Box closes | January 19 | `December 20 + 30` `[COMPUTED]` |
| Planned re-buy | January 5 | **day +16** from the sale `[COMPUTED]`, which is **box day 47** |
| Outcome | — | The re-buy is **inside the box**. Part or all of the loss is disallowed, and the disallowed amount becomes basis in the January lot |
| First safe re-entry | January 20 | day 31 `[COMPUTED]` |

The tax year boundary is irrelevant. The window is 61 consecutive days measured from the
sale, and it crosses the year end as easily as it crosses a month end.

## The substitute route in December

When the holder does not want to spend the year boundary out of the market, the options are
the four from `(references/loss-harvesting-and-replacement.md)`:

| Route | December feasibility |
|---|---|
| Stay out | Always available, and free. The exposure given up is the position's move over the gap |
| Re-buy the same security on day 31 | Requires selling by November 30 to re-enter in the same year |
| Buy a cleared substitute | Available immediately if the substantially-identical question has been answered in writing. The substitute's tracking error is a real cost |
| Double-up | Requires the acquisition dates to be checked against the actual 61-day box, not against the intent |

The substitute route is the one that most often goes wrong in December, because December is
when a holder is most motivated to find a substitute and least likely to do the analysis
properly.

## Building the calendar, step by step

1. **Start at the last trading day of the year.** Mark it. That is the final date a loss
   counts in this year.
2. **Subtract 31 days.** A loss sale permits same-year re-entry only while its day-31 date
   lands inside the year, so the sale must be at least 31 days before the last trading day —
   `December 31 − 31` = **November 30** `[COMPUTED]` on the worked numbers. (Subtracting 30
   gives the box end, one day too late.) That is the last day on which a loss sale still permits
   same-year re-entry of the same security.
3. **List every position with an unrealized loss** and its lot detail.
4. **Establish the offset inventory** — realized gains by character for the year.
5. **Sweep each candidate loss sale's 61-day box**, remembering the backward half: purchases
   already made in the last 30 days count.
6. **Choose the re-entry route** for each candidate, and write its cost in dollars.
7. **Check automatic purchases** that will fire in December and January — reinvestment,
   automatic investment, plan purchases. These are the classic contaminant.
8. **Place the sales in the order the ladder dictates**, one ledger row each.
9. **Record the day-31 re-entry date** for every loss sale, as a date.

## The January counterpart

January is, in behavioural terms, the quiet month for harvesting — most holders have already
done it or already missed it. `[COMMON-PRACTICE]` The behavioural concentration of tax-loss
selling in November and December is a well-known market pattern, not a rule of law, and it does
not change any of the arithmetic above.

What January *does* bring is the consequence of December's decisions: re-entry dates arriving,
boxes still open, and disallowed losses discovering themselves when the 1099-B arrives.

## What must not happen

- **A harvest with no re-entry date.** The date is half the decision. A sale without it is an
  unplanned exit.
- **A January purchase made without checking the box.** The most common single error in this
  file.
- **A December substitute chosen under time pressure.** The identity question does not get
  easier because the year is ending.
- **A loss sold to satisfy a calendar rather than an offset.** Losses are worth something only
  against something.
- **A loss sale whose settlement is confused with its trade date.** The tax year follows the
  trade; the box follows the trade too.

## Failure modes

1. **What goes wrong — the January re-buy.** A December loss sale followed by an early-January purchase is disallowed, and the current year's offset is gone. On the worked dates, the re-buy on January 5 is **day +16** from the sale — **box day 47** — inside a box that runs from November 20 to January 19.
2. **What goes wrong — the missing re-entry date.** A loss sale was planned without the day-31 date, so the holder is out of the position into January by accident.
3. **What goes wrong — the December automatic purchase.** A reinvestment or plan purchase fires inside the box; the loss is partly or wholly disallowed.
4. **Worst case — the rush.** Time pressure in the last two weeks of December produces a substitute that was never cleared, or a sale sized to a calendar rather than to an offset.
5. **What goes wrong — the trade date and settlement confused.** A last-day sale recorded on its settlement date appears to fall in January, and the year's planning is wrong.
6. **What goes wrong — the box forgotten into January.** The re-entry date was never recorded, and the January buy happens on a date nobody checked.
7. **Known limitation — the calendar depends on the venue's trading days.** Holidays move the last trading day; the arithmetic above uses dates and must be re-run against the actual calendar for the year in question.
8. **Edge case — a loss sale on the last trading day.** The box then runs deep into January, and the re-entry is out of the market for a month.
9. **Edge case — a substituted security bought in December.** Its own 61-day box is a separate window and may overlap with the first one.
10. **What goes wrong — the carry-forward presented as a saving.** A harvest with nothing to offset produces a carry-forward, real but not a current-year benefit.

## Checklist

- [ ] The year's last trading day established for the relevant venue.
- [ ] The last sale date that still permits same-year re-entry computed: last trading day − 31 days.
- [ ] Every candidate loss sale's box written out in both directions, with explicit dates.
- [ ] Day-31 re-entry date recorded as a date for each loss sale.
- [ ] Automatic purchases in December and January listed per account.
- [ ] Offset inventory established by character before any sale is placed.
- [ ] Re-entry route chosen per sale, with its cost in dollars.
- [ ] Substitute securities cleared in writing, if any.
- [ ] Trade dates — not settlement dates — used throughout.
- [ ] One ledger row per sale, tagged `YE`, carrying the delta against the FIFO default.
