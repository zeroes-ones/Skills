# Ex-Dividend Under T+1 — the last day to buy, exactly

## Two rules, one date

The date a buyer must own shares by, and the date the price drops, are both set by the
**ex-dividend date**. Getting it wrong means buying a day late and receiving nothing, or
selling a day early and giving the dividend away.

### Rule 1 — how the ex-dividend date is set

`[VERIFIED — FINRA Rule 11140]`

| Distribution size | Ex-dividend date |
|---|---|
| **Under 25%** of the security's value | The **record date** |
| **25% or more** of the security's value | The **first business day after the payable date** |

The 25%-of-value threshold is what separates an ordinary quarterly dividend from a large
special distribution. A large distribution moves the ex-date far later than the record date,
which moves the last day to buy with it.

FINRA Rule 11140 was **amended effective 2024-05-28**. Any procedure written before that date
should be treated as possibly stale.

### Rule 2 — settlement is T+1

`[VERIFIED — SEC Release 34-96930]` US securities settle on a **T+1** cycle, and the
Regulation T payment or margin-call window runs to **settlement plus two business days**,
which is **three business days** from the trade. `[VERIFIED — 12 CFR 220.2, 220.4(c)(3)(i)]`

T+1 is why the practical rule below holds. Ownership for the dividend is determined by who is
a holder of record on the record date, and a purchase only becomes a settled holding on the
following business day.

## The practical rule

```text
   The LAST day to buy and receive the dividend is
   the TRADING DAY BEFORE the ex-dividend date.
```

`[COMPUTED]` A purchase made on the trading day before the ex-date settles on the ex-date,
which is the record date for a distribution under 25% of value, so the buyer is a holder of
record. A purchase made **on** the ex-date settles the next business day — after the record
date — and receives nothing.

## Worked date example

A quarterly dividend of **$0.50** `[ESTIMATED]` on a stock trading at **$100.00** `[ESTIMATED]`.

- Dividend as a share of value: `0.50 / 100.00` = **0.50%** `[COMPUTED]` — far below 25%, so
  the ex-date equals the record date.
- Suppose the record date, and therefore the ex-date, is a **Tuesday**.
- Last day to buy: **Monday** — the trading day before the ex-date `[COMPUTED]`.
- A Monday purchase settles Tuesday, in time to be a holder of record.
- A Tuesday purchase settles Wednesday, too late.
- The price is expected to open lower on Tuesday by roughly the dividend, about **$0.50
  cost** of value given up in price `[COMPUTED]`.

## The price-drop arithmetic — the capture is not free

A dividend is not money created by owning a stock for a day. The price of the shares is
expected to fall on the ex-date by approximately the dividend amount, so the holder's
position value plus the dividend is roughly unchanged before tax.

Worked `[ESTIMATED]`: 1,000 shares at **$100.00** = **$100,000 value** `[COMPUTED]` the day
before the ex-date.

| Line | Amount |
|---|---|
| Position value, day before ex-date | **$100,000 value** `[COMPUTED]` |
| Dividend received, $0.50 × 1,000 | **$500 value** `[COMPUTED]` |
| Expected price on the ex-date, $99.50 | **$99,500 value** `[COMPUTED]` |
| Position value plus dividend | **$100,000 value** `[COMPUTED]` — unchanged before tax |

And then tax is paid on the dividend — at 40.8% if the holding window fails, which is
`0.408 × 500` = **$204 cost** `[COMPUTED]`, or at 23.8% if it holds, which is
`0.238 × 500` = **$119 cost** `[COMPUTED]`.

The honest reading: the capture trade's pre-tax result is approximately zero by construction.
Its post-tax result is negative unless the position also gains on its own merits. That is not
a strategy; it is a way of paying tax to hold a position for two months.

## The full pre-trade checklist for any dividend-motivated buy

- [ ] Ex-dividend date established, applying the 25%-of-value test to the distribution.
- [ ] Last day to buy computed as the trading day before the ex-date, on the venue's calendar.
- [ ] The 61-of-121 qualified-dividend window drawn from the ex-date (or 90-of-181 for the
      longer-attribution preferred case).
- [ ] The earliest sale date that still satisfies the window identified, and its price risk
      accepted in writing.
- [ ] The dividend's own size compared with the position's normal daily movement — if the
      dividend is smaller than one ordinary session's range, the trade is a position trade
      with a dividend attached, and should be judged as one.
- [ ] The ordinary-versus-qualified rate difference stated in dollars on the trade.
- [ ] Any hedging or short leg checked against its own dividend clock — see
      `(references/short-side-tax-and-dividend-costs.md)`.

## Failure modes

1. **What goes wrong — buying on the ex-date.** The shares settle after the record date, so no dividend is received, and the price has already dropped by roughly the dividend.
2. **What goes wrong — the pre-2024 rule of thumb.** A procedure built on an older settlement cycle produces a last-day-to-buy that is a day late.
3. **Worst case — the large special distribution.** A distribution of 25% of value or more moves the ex-date to the business day after the payable date; the "record date" assumption is wrong by weeks.
4. **What goes wrong — the capture priced as free money.** The position value drops by roughly the dividend, so the pre-tax result is approximately zero and the after-tax result is negative.
5. **Worst case — the capture that fails the holding window.** Two months of exposure taken to earn a dividend that is taxed at ordinary rates.
6. **What goes wrong — the ex-date on a foreign issuer or a foreign-listed security.** Local convention and settlement cycles differ; the T+1 rule is not universal.
7. **Known limitation — this file does not model market reaction.** The price drop is an expectation, not a mechanism, and the actual move on any given ex-date can be larger or smaller.
8. **Edge case — the suspended or halted security.** A halt across the record date changes who can be a holder of record.
9. **Edge case — the dividend paid in shares or in a different currency.** The mechanics and the timing differ, and the arithmetic above does not apply unchanged.
10. **What goes wrong — the short leg.** A hedged position that is short the security owes a payment in lieu and has its own deductibility clock; see the short-side reference.

## Verification note

The ex-date rule, the 25% threshold, the effective date of the amendment and the T+1
settlement cycle are all cited to named sources above. **What is not verified here:** any
individual broker's dividend-eligibility cut-off, its order-entry rules around an ex-date, or
its payment-timing convention. Those are `[BROKER-VERIFIED]` questions and must be asked of
the broker, not assumed from this file.
