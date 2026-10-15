# Short-Side Tax and Dividend Costs — the short seller's own clock

## Why the short side is different

A long holder receives a dividend. A short seller **owes** a **payment in lieu of a dividend**
to the lender of the shares. It is economically a dividend, legally not one, and the tax
treatment is its own thing — with a holding test that has nothing to do with the 61-of-121
qualified-dividend window.

## The rule

A short seller's payment in lieu of a dividend may be deducted only if the short position was
held **at least 46 days** — and for an **extraordinary dividend**, only if it was held
**more than one year**. `[VERIFIED — IRC §263(h); IRS Pub 550]`

| Position's open duration when the payment was made or the short closed | Treatment of the payment in lieu |
|---|---|
| Fewer than 46 days | Not deductible. The cost is real, the deduction is not available |
| 46 days or more | Deductible, subject to the ordinary rules for the deduction |
| An extraordinary dividend, held one year or less | Not deductible; the test becomes more than one year |
| An extraordinary dividend, held more than one year | Deductible |

`[COMMON-PRACTICE]` The 46-day count and the "extraordinary" threshold each have their own
definition and their own measurement rules. This file states the shape of the test and the
arithmetic it implies; it does not restate the statute.

## What this does to a trade's result

The payment in lieu is a cost the short carries. Whether it is deductible changes whether the
trade was profitable, and by how much.

Worked `[ESTIMATED]`: a short position of 1,000 shares, closed after **40 days** with a price
gain of **$2,400 gain** `[ESTIMATED]`. A **$600** payment in lieu of a dividend was made
during the period. Marginal rate 40.8% `[ESTIMATED]`.

| Line | Payment disallowed (40 days) | Payment allowed (47 days) |
|---|---|---|
| Price gain on the short | **$2,400 gain** `[COMPUTED]` | **$2,400 gain** `[COMPUTED]` |
| Payment in lieu | −**$600 cost** `[COMPUTED]`, not deductible | −**$600 cost** `[COMPUTED]`, deductible |
| Taxable amount | **$2,400 gain** `[COMPUTED]` | `2,400 − 600` = **$1,800 gain** `[COMPUTED]` |
| Tax at 40.8% | `0.408 × 2,400` = **$979 cost** `[COMPUTED]` | `0.408 × 1,800` = **$734 cost** `[COMPUTED]` |
| After-tax result | `2,400 − 600 − 979` = **$821 value** `[COMPUTED]` | `2,400 − 600 − 734` = **$1,066 value** `[COMPUTED]` |

The difference is `1,066 − 821` = **$245** `[COMPUTED]` — seven days of holding on a 1,000-share
position. That is the whole content of the 46-day test as a practical matter: on some trades
it is small, and on trades where the dividend is large relative to the price move, it decides
whether there was a profit at all.

## The two clocks, side by side

The short side and the long side both have a dividend-related clock, and they are not the
same clock. Mixing them up is a common and expensive error.

| | Long holder | Short seller |
|---|---|---|
| What the clock governs | Whether the dividend is taxed at the favourable rate | Whether the payment in lieu is **deductible** at all |
| The test | More than 60 days held inside the 121-day window beginning 60 days before the ex-date `[VERIFIED — IRC §1(h)(11)(B)(iii)(I), §246(c)]` | At least 46 days of the short being open; more than one year for an extraordinary dividend `[VERIFIED — IRC §263(h)]` |
| Failing the test | The dividend is ordinary income | The payment is not deductible |
| The number to remember | 61 of 121 | 46 days |

A long-short pair that is long one security and short another does not merge the two clocks.
Each leg is measured on its own.

## Where the short-side cost hides

- **Inside a hedged position.** A "market-neutral" pair has a dividend cost on the short leg
  that is often omitted from the position's stated P&L until it is paid.
- **Inside a covered call.** Writing calls against long shares does not create a short stock
  position; the payment in lieu is not owed. But assignment of the call does create one, and
  the clock starts then.
- **Inside a reverse-conversion or a box.** Short stock is short stock for these purposes,
  however it is described.
- **Across an ex-date within an open short.** The payment is owed when the short is open
  across the ex-date, so the clock is tested against the period the position was open, not
  against the day the payment happened to be booked.

## Operational sequence for a short that owes a dividend

1. Record the short's **open date** and, when it closes, the **open duration** in days.
2. Record the **ex-date** and the amount of the payment in lieu.
3. Determine whether the distribution is an **extraordinary dividend** for this purpose, since
   it changes the test from 46 days to more than one year.
4. If the short is still open and the duration is under 46 days, compute the trade's result
   **both ways** — with the payment deducted and without — before deciding to close.
5. Close the trade with the after-tax number in front of you, not the gross one.
6. Record the duration, the test applied and the outcome in the ledger row, tagged `SC`.

## A note on why this is not "just a dividend"

The payment in lieu is not a dividend for the payer, which is precisely why the deduction
test exists. A holder who thinks of it as receiving a dividend has the arithmetic backwards
and will mis-size every affected position.

## Failure modes

1. **What goes wrong — the 40-day close.** The short is closed at a nominal profit, the payment in lieu is disallowed, and the trade is worth less than the screen said. On the worked numbers, **$245** `[COMPUTED]` of difference.
2. **What goes wrong — the two clocks confused.** The 61-of-121 qualified-dividend window is applied to a short position, and the 46-day test is never run.
3. **What goes wrong — the omitted cost.** The payment in lieu is not in the position's P&L until it is booked, so the trade's stated result is overstated for weeks.
4. **Worst case — the extraordinary dividend.** The test becomes more than one year, a horizon no short of realistic size can satisfy, and the payment is not deductible.
5. **What goes wrong — assignment creating a short nobody clocked.** A covered call is assigned, a short stock position appears, and the dividend clock that starts then is never started.
6. **Known limitation — borrow cost and locate availability are out of scope.** They belong to `equity-risk-and-capital-engineer`, and they change the trade's economics independently of the tax.
7. **Edge case — the short opened and closed repeatedly.** Each open period has its own duration; the test is not cumulative across separate positions.
8. **Edge case — the foreign dividend.** Withholding on the underlying dividend, and the treatment of the payment in lieu, can differ. Verify rather than assume.

## Checklist

- [ ] Short's open date and duration in days recorded.
- [ ] Ex-date and payment-in-lieu amount recorded.
- [ ] Extraordinary-dividend question asked, because it changes the test.
- [ ] Whether the duration meets the applicable threshold recorded, with the threshold named.
- [ ] Trade result computed both with and without the deduction before closing.
- [ ] Ledger row tagged `SC`, carrying duration, test applied and after-tax result.
