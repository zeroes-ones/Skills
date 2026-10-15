# Short Borrow and Buy-In Mechanics

A short position has two holders: the short seller, and the lender of the shares. The lender can take
the shares back, and the desk that lent them is under no obligation to keep lending. This file
covers what is rule-governed, what is contract, and what is simply the desk's commercial decision —
and it is explicit about which is which, because the difference is the whole point.

## §1 — What Is Rule-Governed and What Is Not

| Item | Status | Tag |
|---|---|---|
| The definition of "easy to borrow" vs "hard to borrow" | **No regulatory definition.** The classification is set by the broker's stock-loan desk. It is not a legal category and cannot be looked up in a rule | [BROKER-VERIFIED] |
| Borrow fee (the stock-loan rebate/fee) | **Negotiable, and it moves daily with supply and demand.** Not a published rate; not a regulated maximum | [BROKER-VERIFIED] |
| Recall notice period | **No SEC or FINRA rule fixes a period.** The terms are the lending agreement's | [BROKER-VERIFIED] |
| "Usually one to two business days' notice" | Widely quoted desk practice, **not a rule** | [COMMON-PRACTICE] |
| Buy-in procedure and timings once delivery has failed | **Rule-governed** — FINRA Rule 11810 | [VERIFIED — FINRA Rule 11810] |

**The sentence that matters: there is no rule that entitles a short seller to a certain number of
days' notice before their borrow is recalled.** A user asking "how long do I have?" must be told
that the answer depends on their specific lending agreement, that the commonly quoted one-to-two
business days is practice rather than rule, and that the desk's fee and availability move daily.

## §2 — The Buy-In: FINRA Rule 11810, Step by Step

A buy-in is the mechanism by which a counterparty closes an uncompleted contract when shares are not
delivered. It is executed **for the account and liability of the party in default** — the defaulting
party pays, in a market it did not choose.

| Step | Rule |
|---|---|
| Earliest close-out | A buyer may close an uncompleted contract **no sooner than the third business day** after delivery was due |
| Notice | The buy-in notice must reach the seller **not later than 12:00 noon ET, two business days before** the proposed execution |
| Acceptance | The seller must reject **in writing** by **6:00 p.m. ET on the notice date**, or the notice is **deemed accepted** |
| Cure | Delivery must be cured by **3:00 p.m. ET on the effective date** |
| In-transit extension | Securities **in transit** receive a **7-calendar-day** extension |
| Who pays | The buy-in is executed **for the account and liability of the party in default** |

**Source:** FINRA Rule 11810 (buy-in and close-out procedures).

Three practical consequences the timings table does not spell out:

1. **Silence is acceptance.** Failing to reject in writing by 6:00 p.m. ET on the notice date means
   the buy-in proceeds. There is no second chance to argue about it afterwards.
2. **You cannot cure by 3:00 p.m. on the effective date without having located shares before it.**
   The cure deadline is a deadline for a *locate*, not a deadline for intending to locate.
3. **The in-transit extension is about paper, not about intent.** A claim that the shares are in
   transit has to be true, and 7 calendar days is short.

## §3 — The Economics of a Short [COMPUTED]

Borrow cost is a running charge on notional, not a one-time fee. Short **2,000 shares at $25.00**:

```
NOTIONAL              2,000 × $25.00 = $50,000
BORROW FEE 3.0%/yr    $50,000 × 0.030 = $1,500/yr  = $4.11/day   (÷365)
BORROW FEE 20%/yr     $50,000 × 0.200 = $10,000/yr = $27.40/day
BORROW FEE 100%/yr    $50,000 × 1.000 = $50,000/yr = $136.99/day
```

Read the third row again: at a **100% annualised borrow fee** the position must appreciate by 100%
of notional in a year for the short to break even, before commissions. A hard-to-borrow name with a
high fee is not a cheap trade with a headwind; it is a position that pays its own notional away.

**A buy-in, priced.** Short 2,000 shares at $30.00; delivery fails; a buy-in executes at $42.00:

```
BUY-IN COST          (42.00 − 30.00) × 2,000 = $24,000, before fees
POSITION AFTER       gone — the short no longer exists, at a price nobody chose
THESIS AFTER         unchanged, and irrelevant: the clock, not the view, closed it
```

[COMPUTED] from the stated inputs; the fees and any interest adjustments are broker-specific and
must be [BROKER-VERIFIED].

## §4 — Recall and the Short-Side Asymmetry

A borrow recall returns the shares to the lender. The short seller must either:

- **locate new borrow** — available at a price the desk names, if at all, or
- **buy the position back** — into whatever the market is offering, or
- **fail to deliver** — which starts the Reg SHO clock in `reg-sho-and-threshold-list.md`.

Only the third option has a rule-governed clock. The first two are commercial events with no
notice period guaranteed by any regulation. **That asymmetry — a rule-governed clock for the
failure, no rule-governed clock for the recall — is the single most under-appreciated fact about
short equity positions.**

Where the recall lands inside a wash-sale window or a holding period, the interaction is the
holder's problem, not the desk's. Route the tax consequence to
`equity-tax-lot-and-exit-management`.

## §5 — The Short-Side Risk Ledger

Every short position carries five things that a long position does not, and each one needs an entry
in the record before the trade is taken:

| Item | Why it matters | Where it is recorded |
|---|---|---|
| `borrow_status` | easy / hard / unavailable, **as of a timestamp** | position record |
| `borrow_fee_annual_pct` | a running charge, re-priced daily | position record, refreshed |
| `recall_terms` | the lending agreement's terms — read, not assumed | attached to the position |
| `fail_age_settlement_days` | the Reg SHO clock, once a fail exists | position record, daily |
| `buy_in_liability` | whether the position can be bought in, and by when | exit plan |

A short with no `recall_terms` recorded is a short whose exit has no owner.

## §6 — Failure Modes

1. **Assuming a guaranteed recall notice period.** No rule fixes one; the agreement does.
2. **Assuming "easy to borrow" is a property of the security.** It is a property of the desk's
   inventory on that day.
3. **Treating borrow fee as fixed.** It moves daily with supply; a 3% name can become a 20% name in
   a week.
4. **Missing the 12:00 noon ET notice deadline.** The buy-in notice arrives and is not seen.
5. **Failing to reject a buy-in notice in writing.** Silence is deemed acceptance.
6. **Planning a cure on the effective date rather than before it.** The 3:00 p.m. ET cure needs a
   locate that exists.
7. **Sizing a short on the borrow fee rather than on the requirement.** A sub-$5 short's maintenance
   requirement can be 100% of market value (see `margin-regimes-and-forced-liquidation.md` §2).
8. **Ignoring the interaction between a recall and a wash-sale window.** A forced repurchase can
   disallow a loss the holder was counting on.
9. **Assuming the desk will call before acting.** It is not required to.
10. **Holding a short into a tender, rights, or redemption event without reading Rule 11810(j).**
    See `corporate-action-and-halt-playbook.md` §3.

## §7 — Verification

- [ ] Every short has a borrow status with a timestamp, and its fee.
- [ ] Every short has the lending agreement's recall terms attached to the position record.
- [ ] The buy-in notice deadlines (noon ET, two business days out; rejection by 6:00 p.m. ET) are
      written into the position's calendar, not remembered.
- [ ] Every short's `fail_age_settlement_days` is reported.
- [ ] Where a user asks "how long do I have?", the answer names the agreement and the desk, and does
      not invent a rule.
