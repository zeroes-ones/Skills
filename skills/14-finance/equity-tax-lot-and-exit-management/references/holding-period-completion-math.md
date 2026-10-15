# Holding-Period Completion Math — is the date worth waiting for?

## The rule, and the day count

- A gain on a capital asset held **more than one year** is long-term. `[VERIFIED — IRC §1222]`
- The holding period **begins the day after the acquisition trade date** and **ends on the
  sale trade date**. `[VERIFIED — IRS Pub 550]`
- Therefore the **earliest long-term sale** for a lot acquired on trade date **D** is
  **D + 1 year + 1 day**.

Worked, as the research pass established it: bought **January 31, 2024**. The holding period
begins **February 1, 2024**. Selling **January 31, 2025** is 366 days — still short-term.
Selling **February 1, 2025** is **367 days** — long-term. `[VERIFIED — IRC §1222; IRS Pub 550]`

The "+1 year +1 day" form exists because of the two conventions pointing in opposite
directions: the clock starts the day *after* the buy, and it includes the day *of* the sale.

## Boundary table

| Buy trade date | Holding period begins | Last short-term sale | First long-term sale |
|---|---|---|---|
| 2024-01-31 | 2024-02-01 | 2025-01-31 | **2025-02-01** |
| 2024-03-15 | 2024-03-16 | 2025-03-15 | **2025-03-16** |
| 2024-12-31 | 2025-01-01 | 2025-12-31 | **2026-01-01** |
| 2024-02-29 (leap day) | 2024-03-01 | 2025-02-28 | **2025-03-01** |

`[COMPUTED]` All rows are derived by applying buy date + 1 year + 1 day and then adjusting
for the next available trading session, which is a separate, venue-specific question. The last
row is the leap case: **2024-02-29** exists only because 2024 is a leap year, its holding period
begins **2024-03-01**, and its anniversary resolves to **2025-02-28** — the last day of February
— because 2025 has no February 29.

**Leap-year caution.** "One year later" is not a fixed day count: a one-year holding window is
365 or 366 days depending on whether a February 29 falls inside it. A lot bought on the leap day
itself is the extreme case — the last row above — where the boundary is a convention (the
anniversary resolves to the last day of February in a non-leap year) rather than a count.
Compute the boundary as a **date**, never as "365 days", and write the date on the record.

## The cushion: what the rate differential is actually worth

A holder is selling anyway. The question is whether moving the sale across the boundary
improves the after-tax result, and by how much.

Let `G` be the gain now, `r_s` the short-term rate, `r_l` the long-term rate, and `G_w` the
gain at the boundary date.

```text
   sell now        → proceeds keep   G × (1 − r_s)
   wait, then sell → proceeds keep   G_w × (1 − r_l)

   waiting is better  ⟺  G_w × (1 − r_l) > G × (1 − r_s)
                      ⟺  G_w / G > (1 − r_s) / (1 − r_l)

   the gain may fall by at most  1 − (1 − r_s) / (1 − r_l)   before waiting loses
```

That last term is the **cushion**: the price decline the position may absorb inside the wait
and still leave the holder better off. It is bounded, it is computable, and it is usually much
smaller than the holder expects. It is the honest size of the tax-date bet.

### Worked cushion

Rates assumed `[ESTIMATED]`: `r_s` = 40.8% (37% ordinary + 3.8% net investment income),
`r_l` = 23.8% (20% + 3.8%).

```text
   cushion = 1 − (1 − 0.408) / (1 − 0.238)
           = 1 − 0.592 / 0.762
           = 1 − 0.7769
           = 0.2231   →  22.3%
```

`[COMPUTED]` So the wait is worth taking while the gain falls by less than 22.3% of itself.

Applied to a position of **$40,000** `[ESTIMATED]` with a **$10,000 gain** `[ESTIMATED]`:

- Short-term sale: `0.408 × 10,000` = **$4,080 cost** `[COMPUTED]`; keep
  `40,000 − 4,080` = **$35,920 value** `[COMPUTED]`.
- Long-term sale: `0.238 × 10,000` = **$2,380 cost** `[COMPUTED]`; keep
  `40,000 − 2,380` = **$37,620 value** `[COMPUTED]`.
- The date is worth **$1,700 saved** `[COMPUTED]`.
- The gain may fall to `0.2231` below: `10,000 × 0.7769` = **$7,769 gain** `[COMPUTED]` — a
  tolerance of `10,000 − 7,769` = **$2,231 cost** `[COMPUTED]`, which on a $40,000 position is
  `2,231 / 40,000` = **5.58%** `[COMPUTED]`.

**Read that number twice.** Five and a half percent is the whole bet. A single volatile
session can exceed it.

### The annualised framing, for perspective

The wait priced here is the **remaining distance to the boundary** — not the whole holding
period, and not the one-day gap between the last short-term sale and the first long-term sale.
On the lot worked above (bought **2024-01-31**, first long-term sale **2025-02-01**), a decision
taken on **2024-12-02** leaves `December 2 → February 1` = **61 days** `[COMPUTED]` to the
boundary.

Earning **$1,700 saved** `[COMPUTED]` while carrying **$40,000** `[ESTIMATED]` of exposure
for those **61 days** is:

```text
   return on risk capital = 1,700 / (40,000 × 61 / 365) = 1,700 / 6,685 = 25.4%
```

`[COMPUTED]` A 25% annualised return on the risk capital sounds excellent, and it is a real
return. It is also **not a tax strategy** — it is a leveraged bet on one position not falling
more than 5.58% inside the window. The headline moves with the remaining distance, which is
exactly why the distance is written as two dates and not as "about two months".
`[COMMON-PRACTICE]`

## When waiting is plainly wrong

| Situation | Why the wait loses |
|---|---|
| The thesis has broken | The rate is worth a few percent; the thesis is worth the position. R5 fires: write the non-tax reason, or sell |
| The position's plausible downside inside the wait exceeds the cushion | The arithmetic says so. The cushion is the bound; if the bound is exceeded, the wait is a losing trade |
| The wait is long and the boundary is not in sight | A rate is not a thesis. If the boundary is months away, the tax question has not arrived yet |
| The holder cannot fund the wait | Capital needs are not a tax question, but they are a real constraint; the position does not exist to serve the rate |
| The lot is already long-term | There is no date question at all. Stop looking for one |
| The rate differential is unknown or assumed | An unmeasured benefit cannot justify a measured risk. Get the rates, or do not act |

## The rate pair is an input, not a guess

The formula needs `r_s` and `r_l` for this holder. Sources:

- The holder's own marginal rate, including any net investment income surtax and any state or
  local rate that applies. **State and local tax is out of scope for this skill** and can
  change the ordering conclusion entirely.
- A stated assumption, labelled `[ESTIMATED]`, when the real figure is not available.

Never present a cushion computed from an unstated rate pair. If the rates are assumed, the
row says so, and the reader knows the number moves with the assumption.

## What the tax does and does not do

```text
   Tax changes WHEN you sell a position you were going to sell.
   Tax does not change WHETHER the position should exist.
   Tax never converts a sell into a hold.
```

`[COMMON-PRACTICE]` The first line is the entire justification for this file. The last two
lines are why R5 runs before any tax reasoning in this skill: if there is no non-tax reason to
hold, the holding-period question is moot.

## Failure modes

1. **What goes wrong — "one year later".** The boundary is computed as buy date + 1 year, one day short, and the sale is still short-term.
2. **What goes wrong — the settlement-date clock.** The holding period is measured from settlement rather than the trade date.
3. **What goes wrong — the leap-year slip.** The boundary is computed as 365 days rather than as a date.
4. **Worst case — holding a broken thesis for the rate.** The cushion is exceeded, the position falls more than the tax saved, and the rate never arrives because the position was sold later, lower.
5. **What goes wrong — the unstated rate pair.** A convincing cushion presented from rates the holder never confirmed for their own situation.
6. **What goes wrong — the tax-date decision made alone.** The date is moved without the position's outlook being restated, so nothing detects that the reason to hold had already gone.
7. **Known limitation — the cushion is a bound, not a prediction.** It says how much decline the tax saving can absorb; it says nothing about how likely any decline is.
8. **Edge case — the corporate action.** A lot's acquisition date can change through a reorganization, and the boundary moves with it.
9. **Edge case — the partial lot.** After a specific identification, part of a lot may already be gone, and the remaining shares keep the original date while the quantity is different.
10. **What goes wrong — the wash-sale interaction.** A replacement lot acquired inside a box inherits the old shares' holding period, so its boundary is not its own acquisition date.

## Checklist

- [ ] Boundary computed as a date: buy trade date + 1 year + 1 day.
- [ ] Days remaining computed against the intended sale date.
- [ ] Rate pair stated, with its `source:` or an explicit `[ESTIMATED]` label.
- [ ] Cushion computed with the formula shown.
- [ ] The position's plausible downside inside the wait compared against the cushion, in numbers.
- [ ] Non-tax reason to hold written before the date decision.
- [ ] Stop condition written: the level at which the wait is abandoned.
