# Qualified Dividend Window — the 61-of-121 test

## The rule

For a dividend to be treated as a qualified dividend — taxed at the long-term capital gain
rates rather than at ordinary rates — the holder must hold the share for **more than 60 days
during the 121-day period that begins 60 days before the ex-dividend date**.
`[VERIFIED — IRC §1(h)(11)(B)(iii)(I), §246(c)]`

Read that as three separate constraints, because each one has tripped people up:

1. The window is **121 days long**, and it **straddles the ex-dividend date**. It starts 60
   days before it and ends 60 days after it.
2. The required holding is **more than 60 days**, so **at least 61 days**, of holding
   *inside* that window.
3. The days that count are days the shares are **held**, so a purchase inside the window
   contributes only the days after the purchase, and a sale inside the window contributes
   only the days before the sale.

A separate rule applies to certain preferred dividends where the dividend is attributable to
a period of **more than 366 days**: the requirement becomes **90 days of a 181-day period**.
`[VERIFIED — IRC §246(c)(2)]`

## The window, drawn

```text
        day −60                        day 0                      day +60
   ─────────┬───────────────────────────┬───────────────────────────┬─────────
            │                           │                           │
      window opens                 EX-DIVIDEND DATE           window closes
            │                           │                           │
            └──── you must hold at least 61 of these 121 days ──────┘
```

`[COMPUTED]` The window is `60 + 1 + 60` = **121 days** inclusive. The requirement is
**61 held days**, so exactly one more than half.

## The two ways to satisfy it

| Situation | What it takes |
|---|---|
| **Already held for a long time** | The shares were bought long before the window opened. The days held inside the window accumulate automatically from day −60 to the ex-date and beyond. Sixty-one days of holding inside a 121-day window is reached easily if the position was not recently bought or recently sold |
| **Buying into the dividend** | The purchase happens inside the window, so only the days after the purchase count. A purchase on the trading day before the ex-date has the whole ex-date-to-day-+60 stretch available, which is **61 days** including the ex-date `[COMPUTED]` |

The second row is the one that surprises people, and it is the honest answer to the
"dividend capture" question: **the trade is roughly a two-month commitment to the position**,
not a one-day event. Buying the day before the ex-date and selling the day after leaves the
holder with a dividend taxed at ordinary rates, a price that has dropped, and possibly a
short-term loss.

## Worked day counts

### Case A — buying into the dividend

- Shares bought on the trading day before the ex-date.
- Ex-date: day 0. The window closes at day +60.
- Days available inside the window after the purchase: the ex-date plus 60 more =
  **61 days** `[COMPUTED]`.
- Conclusion: the 61-day requirement can be met, but **only by holding to approximately the
  60th day after the ex-date**. The position is held for about two months `[COMPUTED]`, and
  it is exposed to two months of price movement.

### Case B — an existing position sold too soon after

- Shares held for years. Ex-date: day 0.
- The holder sells on **day +12**.
- Days held inside the window: from day −60 through day +12 = **73 days** `[COMPUTED]`.
- `73 ≥ 61` → the dividend is still qualified `[COMPUTED]`. An early sale does not
  automatically disqualify a long-held position, because the pre-ex-date days inside the
  window already count.

Case B is the one people over-panic about, and Case A is the one people under-plan.

## The counting traps

| Trap | What happens | Guard |
|---|---|---|
| Counting days outside the window | Days held before day −60 or after day +60 do not count toward the 61 | Draw the window first, then count inside it |
| Counting the settlement date of the purchase | The holding clock starts at the trade date, not at settlement | Use trade dates throughout |
| Assuming the ex-date is the record date | True for distributions under 25% of value; **not** true at or above 25% | Apply the 25% test — see `(references/ex-dividend-under-t-plus-one.md)` |
| Treating all preferred dividends as ordinary | Some preferred dividends can qualify, with the longer 90-of-181 test | Ask, do not assume |
| Ignoring a partial sale | A partial sale reduces held days for the shares sold, and can disqualify those shares' dividends | Count per share, not per position |
| Assuming the broker reports the right character | The 1099-DIV shows a character, but the holder is the one who has to be able to defend it | Keep the purchase and sale records so the window can be reconstructed |

## What disqualifies a dividend, and what it costs

If the holding test fails, the dividend is taxed at ordinary rates. The cost is the rate
difference on the dividend.

Worked `[ESTIMATED]`: a **$0.60 dividend** per share on 1,000 shares = **$600 value**
`[COMPUTED]` of dividends. At a 23.8% qualified rate the tax is `0.238 × 600` = **$143 cost**
`[COMPUTED]`. At a 40.8% ordinary rate it is `0.408 × 600` = **$245 cost** `[COMPUTED]`. The
difference is **$102** `[COMPUTED]` — real, and small compared with one session's price
movement on a 1,000-share position. The lesson is not "always chase qualification"; it is
"know which rate applies, and do not build a strategy on the difference".

## Interaction with the other clock

Two different dates govern a dividend purchase, and they are not the same date:

- **Ownership**: whether the buyer is a holder of record, which depends on the ex-dividend
  date and settlement. See `(references/ex-dividend-under-t-plus-one.md)`.
- **Qualification**: whether the held days pass the 61-of-121 test.

A trade can pass the first and fail the second. That is the ordinary, unremarkable outcome of
a one-day dividend capture, and it is the reason the two-clock check exists.

## Failure modes

1. **What goes wrong — the one-day capture.** Bought the day before the ex-date, sold the day after, received a dividend that is taxed at ordinary rates.
2. **What goes wrong — the window drawn in the wrong place.** Days counted from the dividend payment date instead of from the ex-dividend date, moving the whole count.
3. **What goes wrong — settlement dates used as holding dates.** A day or two of error at the boundary, on a test that turns on a single day.
4. **Worst case — the whole position sold inside the window before day 61.** A recently bought position's dividend is disqualified on a trade that looked like a rounding error.
5. **What goes wrong — the 25% distribution treated as ordinary.** A large special distribution moves the ex-date, and the last day to buy changes with it.
6. **What goes wrong — the preferred assumption.** A preferred dividend assumed ordinary, or assumed qualified, without the 90-of-181 test being applied.
7. **Known limitation — this skill cannot determine the qualification of a specific dividend.** It can only require that the window be drawn and the count made.
8. **Edge case — partial sales.** Shares sold inside the window lose their contributed days; shares retained keep theirs. A position is not a single qualifying unit.
9. **Edge case — a wash-sale replacement lot.** Replacement shares inherit the old shares' holding period, so the days held may not begin at the new purchase.

## Checklist

- [ ] Ex-dividend date established, applying the 25%-of-value test.
- [ ] Window drawn: day −60 to day +60, inclusive.
- [ ] Held days counted strictly inside the window, on trade dates.
- [ ] Whether the 61-of-121 or the 90-of-181 test applies, decided and recorded.
- [ ] If the test cannot be met, the dividend priced at ordinary rates before the trade.
- [ ] Both clocks computed — ownership and qualification — not just one.
- [ ] Purchase and sale records kept so the window can be reconstructed later.
