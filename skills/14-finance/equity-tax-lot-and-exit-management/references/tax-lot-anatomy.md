# Tax Lot Anatomy — what a share position actually is

## The one idea

A brokerage screen shows a position. The tax code sees a stack of **tax lots**. A tax lot
is one acquisition event: a quantity of one security, bought or acquired on one date, at
one cost basis per share, held in one account. Sell 100 shares of a four-lot position and
you have consumed part of one lot — not "some of the position".

Every decision in this skill is a lot decision. There is no such thing as the tax cost of
selling "the position", only the tax cost of the lots the sale consumes.

## The five attributes of a lot

| Attribute | Why it matters | Where it comes from |
|---|---|---|
| Acquisition date | Sets the holding period and therefore the character of the gain | The broker's trade record; the **trade date**, never the settlement date |
| Open quantity | How much of this lot is still available to a sale | Purchases less prior sales and prior lot identifications |
| Cost basis per share | The subtrahend of every gain computation | Purchase price, plus or minus every adjustment since |
| Basis adjustments to date | A lot's basis is not fixed at purchase | Wash sales, return of capital, corporate actions, commissions, option premium, inheritance step-up |
| Account | The same security in two accounts is two separate lot sets and can interact through the wash-sale rule | Each account's own records |

A lot table without all five columns is not a lot table. It is a share count with a wish.

## Where lots come from

| Event | What appears in the lot table |
|---|---|
| Initial purchase | One lot: buy date, quantity, price, commission |
| Add-on purchase | A second lot with its own date and basis — this is where the averaging illusion begins |
| Reinvested dividend | A small lot on the payment date, quantity = dividend ÷ reinvestment price. Repeated quarterly, this produces the largest lot counts in most retail accounts |
| Automatic investment plan | One lot per purchase period, every period, forever |
| Employee Stock Purchase Plan (ESPP) | Lots per purchase period, often with a discount element that may itself have its own holding-period rule |
| Restricted Stock Unit (RSU) vesting | One lot per vest, basis = value at vest |
| Option exercise and same-day sale | A lot with a basis equal to the exercise price plus any compensation element, per the broker's 1099-B |
| Stock split | Every existing lot's quantity multiplied and basis per share divided; the dates are unchanged |
| Spinoff | A new lot in the spun security, with basis apportioned across the two positions |
| Merger, cash-and-stock deal | Lots replaced or combined; basis may be carried over or partly recognized |
| Inheritance | Generally a new basis measured at the decedent's date of death; the holding period treatment differs |
| Gift | Generally carry-over basis and a carry-over holding period |

`[COMMON-PRACTICE]` The list above is a working checklist for reading a broker's lot
export, not a statement of tax law. Each row has its own governing rule and several have
exceptions; verify the treatment that applies to you.

## Basis adjustments are where the number actually lives

The purchase price is the beginning of basis, not the end of it. A lot table that has not
been refreshed since purchase is a lot table with a stale number in the one column that
decides everything.

| Adjustment | Direction | Typical trigger |
|---|---|---|
| Wash-sale disallowance | Increases the replacement lot's basis | A purchase of the same or a substantially identical security inside the 61-day box around a loss sale `[VERIFIED — IRC §1091(a)]` |
| Return of capital distribution | Decreases basis; once basis reaches zero, further distributions are generally gain | A fund distribution that is not from earnings |
| Nondividend distribution | Decreases basis | Reported on the 1099-DIV |
| Corporate action | Varies: splittable into two bases, or combined | A spinoff, merger or reorganization |
| Commission and fees | Increases basis on a buy, reduces proceeds on a sell | The trade confirmation |
| Reinvested capital gains distribution | Increases basis; the amount is also taxable that year | Fund year-end distributions |

## The lot-count explosion, and why it breaks judgment

Consider a single $24,000 position built by a $10,000 initial purchase and $2,000 of
automatic investment each quarter for seven quarters, with dividends reinvested quarterly.

- Initial purchase: **1 lot** `[COMPUTED]`.
- Automatic investment: 7 lots `[COMPUTED]`.
- Dividend reinvestment: roughly 7 additional lots `[COMPUTED]` if a dividend was paid each
  quarter.
- Total: about **15 lots** `[COMPUTED]` on a position a holder thinks of as "my fund".

Fifteen lots, each with its own date and basis, in a position whose screen shows one
average. The screen is not lying; it is answering a different question. The tax question
is answered only by the lot table.

## Average cost versus the lot view

| View | What it answers | When it is the right tool |
|---|---|---|
| Average cost | "What did I pay on average?" | A holding where an average-cost election applies and lot choice does not exist |
| Lot view | "What will this specific sale cost me after tax?" | Every sale where lots can be identified |

`[BROKER-VERIFIED]` Average cost is not available for all security types, and where it
applies it may only be elected or changed under conditions set by the broker and the tax
rules. Some holdings can never be converted back to individual-lot reporting. Confirm your
account's position before relying on either view.

## Character is a property of the lot on the sale date

Character is not a property of the position, and not a property of the security. It is
computed per lot, on the sale date, from that lot's holding period.

- A lot held more than one year on the sale date produces long-term gain or loss.
  `[VERIFIED — IRC §1222]`
- The holding period begins the day after the acquisition trade date and ends on the sale
  trade date. `[VERIFIED — IRS Pub 550]`
- Therefore the earliest long-term sale for a lot bought on date **D** is **D + 1 year + 1
  day**.

Two lots of the same security, sold on the same day at the same price, can produce one
long-term and one short-term result. That is the entire reason this skill exists.

## Worked lot table

Four purchases of one 100-share lot each, current price **$120.00** `[ESTIMATED]`.

| Lot | Acquired | Qty | Basis/sh | Basis total | Sale value | Gain/(loss) | Character if sold today |
|---|---|---|---|---|---|---|---|
| L1 | 14 months ago | 100 | $50 | $5,000 | $12,000 | **$7,000 gain** `[COMPUTED]` | long-term |
| L2 | 3 months ago | 100 | $90 | $9,000 | $12,000 | **$3,000 gain** `[COMPUTED]` | short-term |
| L3 | 8 months ago | 100 | $140 | $14,000 | $12,000 | **$2,000 loss** `[COMPUTED]` | short-term |
| L4 | 4 months ago | 100 | $95 | $9,500 | $12,000 | **$2,500 gain** `[COMPUTED]` | short-term |

The position's average basis is `(5,000 + 9,000 + 14,000 + 9,500) / 400` = **$93.75 per
share** `[COMPUTED]`, and the position's average gain is `(7,000 + 3,000 − 2,000 + 2,500) /
400` = **$26.25 per share** `[COMPUTED]`. Both averages are arithmetically correct and both
are useless for deciding which 100 shares to sell.

## What breaks a lot table

1. **Stale basis.** A wash sale or a return of capital adjusted the basis and the table was
   never refreshed.
2. **Settlement dates recorded instead of trade dates.** The holding-period clock starts on
   the trade date; a table built from settlement dates is off by the settlement lag.
3. **A spinoff.** The original lot's basis had to be apportioned across two positions, and
   only one of them was updated.
4. **Reinvested distributions.** Small lots that exist but were never written into the
   table — and which then trip a wash-sale window nobody knew was open.
5. **Multiple accounts.** The same security held in two accounts is two lot sets. The
   wash-sale rule, however, does not respect the account boundary.
6. **A prior specific identification.** A sale that consumed part of one lot leaves a
   partial lot; a table that still shows the original quantity is wrong.

## Verification checklist before using any lot table

- [ ] Every row carries an acquisition **trade** date, not a settlement date.
- [ ] Every row carries a per-share basis and a basis-total that reconcile.
- [ ] Every basis adjustment in the last 12 months is reflected, with its reason.
- [ ] Purchase quantities less sold quantities equal the open quantities, per lot.
- [ ] The table's total quantity equals the account's position quantity.
- [ ] Corporate actions in the last 12 months have been checked against the table.
- [ ] Reinvestment lots have been checked, because they are the usual source of an
      unnoticed purchase inside a wash-sale window.
- [ ] The account's lot-relief default is known and written down. `[BROKER-VERIFIED]`

## Failure modes

1. **What goes wrong — averaging a multi-lot position.** The holder reasons from the
   average and believes a loss exists where every lot is a gain, or the reverse.
2. **What goes wrong — the settlement-date clock.** A boundary date computed from settlement
   is a day or two late and the sale is still short-term when it was believed long-term.
3. **What goes wrong — the invisible reinvestment lot.** A DRIP purchase inside a
   wash-sale window disallows part of a loss the holder believed was banked.
4. **Worst case — average cost assumed reversibly.** A holding under an average-cost
   election is planned as though lots could be chosen, and the plan is unimplementable.
5. **Known limitation — this skill reads the lot table you give it.** A wrong lot table
   produces a confidently wrong after-tax answer, faster than no answer at all.
6. **Edge case — the partial lot.** After a specific identification, a lot can hold a
   quantity that matches no purchase record; that is correct and must be carried forward.
