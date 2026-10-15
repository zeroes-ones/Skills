# Settlement and the Reg T Payment Period

Two dates decide whether a trade is a trade or a violation: the **settlement date** (T+1) and the
**Reg T payment date** (settlement + 2 business days). Everything else in the equity time axis is
either a barrier or a window. These two are deadlines with an actor on the other side.

## §1 — T+1: What Changed and When

The U.S. securities settlement cycle moved from T+2 to **T+1** effective **2024-05-28**.
**Source:** SEC Release 34-96930, "Shortening the Securities Transaction Settlement Cycle". The
same release is why every date-based procedure in this skill reads "business day", not "day".

| Concept | Value |
|---|---|
| Standard settlement | **T+1** — the first business day after the trade date |
| Trade date | The day the order executes (not the day it was entered, not the day it filled after hours) |
| Business day | A day on which the relevant market is open. Weekends and market holidays are not business days. T+1 across a Friday trade lands on Monday; across a Friday trade before a Monday holiday it lands on Tuesday |
| Who settles | The clearing broker and the depository, not the customer |
| What the customer owes | Cash in the account by the settlement date for a purchase; deliverable shares by the settlement date for a sale |

**The consequence that is almost always missed:** the customer's obligation is a *date*, not a
*sequence*. A purchase made using the proceeds of a sale that has not itself settled is not funded,
even though the sale has "already happened". In a **margin** account the broker may front the funds
against buying power; in a **cash** account it may not, and doing so is the violation, not the
convenience.

## §2 — The Reg T Payment Period: Three Business Days

| Step | Rule | Source |
|---|---|---|
| Payment period | **2 business days after the settlement date** — i.e. **3 business days after the trade** | 12 CFR 220.2 (definitions), 220.4(c)(3)(i) |
| What must arrive | Payment of the margin deficiency in **settled funds** (or the account must otherwise be brought into compliance) | 12 CFR 220.4(c) |
| What happens on default | The firm **must** liquidate or otherwise act; **no action is required if the deficiency is $1,000 or less**; **no advance notice is required** | 12 CFR 220.4(d) |
| The outer bound on the *member* | Margin and mark-to-market calls "as promptly as possible and in any event **within 15 business days**" | FINRA Rule 4210(f)(6) |

**Read the fourth row twice.** The 15 business days is a ceiling on how long a *member firm* may take
to demand satisfaction — it is **not an entitlement of the customer**, and it does not extend the
Reg T payment period. A holder who plans against "15 business days" is planning against a rule that
was written to constrain their broker, not to protect them. The operative number for the customer is
**3 business days**.

## §3 — A Worked Timeline [COMPUTED]

Both dates below are arithmetic on the §1–§2 rules for a trade executed on **Monday 2026-03-02**
(US equity market open, no intervening holiday):

```
TRADE DATE            Mon 2026-03-02
SETTLEMENT  (T+1)     Tue 2026-03-03      cash must be present / shares deliverable
REG T PAYMENT PERIOD  settlement + 2 business days
                      Wed 2026-03-04  (+1)
                      Thu 2026-03-05  (+2)  ← payment deadline
ELAPSED               3 business days; 3 calendar days in this particular week
```

Now the same trade executed on **Friday 2026-03-06** (weekend intervenes):

```
TRADE DATE            Fri 2026-03-06
SETTLEMENT  (T+1)     Mon 2026-03-09      (Sat and Sun are not business days)
REG T PAYMENT PERIOD  +1 = Tue 2026-03-10
                      +2 = Wed 2026-03-11  ← payment deadline
ELAPSED               3 business days; 5 calendar days
```

The two cases are the same rule and five days apart on the wall calendar. **A deadline stored as
"3 days" rather than as a date is a deadline that is missed on the 5-day week.** Both figures are
[COMPUTED] from the T+1 and settlement+2-business-day rules stated in §1 and §2.

## §4 — Cash Accounts: Good Faith, Free-Riding, and the 90-Day Freeze

A cash account that buys with unsettled sale proceeds commits a **good-faith / free-riding
violation**. The consequence is not a warning:

- **Payment-privilege freeze: 90 calendar days** during which the account may only buy with settled
  cash on hand. **Source:** 12 CFR 220.8(c)(1).

This is the equity analogue of a margin call that cannot be cured by adding collateral: for 90 days
the account's *ability to transact* is restricted, regardless of how much cash it holds. It is also
completely invisible to a P&L view of the position.

Three ways to stay out of it:

1. Trade the sequence, not the intent: sell, wait for that sale's T+1 settlement, then buy.
2. Hold enough settled cash that no purchase ever depends on an unsettled sale.
3. If a violation has already occurred, treat the 90-day window as a hard planning constraint on
   every subsequent ticket — the reserve floor in `capital-reserve-and-deployment.md` is tested
   against buying power that is now restricted, not against NAV.

## §5 — Settlement Failure, From the Other Side

Delivery obligations are not only a buyer's problem. Every failed delivery starts a clock:

- A fail to deliver must be closed out by the **beginning of regular trading hours on the settlement
  day following the settlement date**.
- A fail resulting from a **long sale** must be closed out by the **third consecutive settlement day**.
- A fail on a Rule 144 / deemed-to-own position must be closed out within **35 consecutive calendar
  days**.

**Source:** 17 CFR 242.204(a). Full mechanics, including the threshold-security rolling clock, are in
`reg-sho-and-threshold-list.md`.

## §6 — Holidays, Half-Days and the Business-Day Count

Business-day arithmetic is where most hand-computed deadlines go wrong:

- **Market holidays** shift T+1 and therefore shift the Reg T date by a full business day each.
- **Half-days** (early closes) are *business days*: they count. They shorten the trading session,
  which matters for liquidity (`liquidity-and-exit-cost-planning.md`), not for the count.
- **Good Friday, Juneteenth, Independence Day (observed), Thanksgiving, Christmas** — the observed
  date, not the nominal date, is the holiday when it falls on a weekend.
- The count is on the **market's** business days, not the holder's. A personal day off is not a
  settlement day off.

**Rule of practice:** never compute a business-day deadline in the head. Resolve it to a date, write
the date down, and re-read the market calendar when the year rolls.

## §7 — Failure Modes of the Settlement Discipline

1. **Deadline stored as a duration, not a date.** "Three days" spans three or five calendar days
   depending on the weekday of the trade.
2. **Buying with unsettled proceeds in a cash account.** A free-riding violation and an automatic
   90-calendar-day payment-privilege restriction.
3. **Assuming the broker's 15-business-day ceiling is the customer's grace period.** It is a ceiling
   on the member.
4. **Treating a half-day as a non-day.** It counts as a business day; it just has less liquidity.
5. **Ignoring the second T+1.** A sale funding a purchase has its own settlement date, and the two
   dates can be one business day apart in the wrong direction.
6. **Assuming cash "in the account" is settled cash.** Position value is not settled cash, and
   money-market holdings are not cash until they settle.
7. **Forgetting that a delivery failure is a clock on the seller too.** A fail to deliver can force a
   buy-in against the account and liability of the party in default.

## §8 — Verification

- [ ] Every open purchase has a written settlement date and Reg T payment date.
- [ ] Cash-account purchases are funded by settled cash only.
- [ ] The market holiday calendar for the current year has been consulted, not remembered.
- [ ] No deadline in any output is expressed as a duration where a date is what the user needs.
- [ ] Where a payment period has been quoted to a user, the 15-business-day figure has been labelled
      as a ceiling on the member, not an entitlement of the customer.
