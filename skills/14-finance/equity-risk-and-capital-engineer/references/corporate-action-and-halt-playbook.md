# Corporate Action and Halt Playbook

A corporate action interrupts whatever plan the holder had. This file lists, per event type, **which
clock the event starts, what it forces, and what the holder must have decided before it starts** —
and it separates the periods the rule text fixes from the ones that are convention, and the issuer's
clock from the holder's.

## §1 — Tender Offers and Exchange Offers: 17 CFR 240.14e-1

| Rule | Value | Source |
|---|---|---|
| Minimum open period | **at least 20 business days** from first publication | 17 CFR 240.14e-1(a) |
| Change in the percentage sought, the consideration offered, or the soliciting dealer's fee | the offer must remain open **at least 10 more business days** from the date of the change | 17 CFR 240.14e-1(b) |
| Payment for securities tendered | consideration paid "**promptly**" after termination or withdrawal of the offer | 17 CFR 240.14e-1(c) |
| Who the clock binds | the **offeror**, not the holder — but the holder's decision window is the offer's open period | 17 CFR 240.14e-1 |

**What it forces the holder to do.** Two things, and both have deadlines that are not the offer's
last day:

1. **A tender decision has to be made before the offer closes**, and a tender that is later withdrawn
   after the offer closes is not a thing — the offer has expired. A holder who "will decide next week"
   has decided to remain a holder.
2. **A hedged or short position in the subject security has a delivery obligation inside the offer
   window.** That is where `FINRA Rule 11810(j)` enters — see §2.

**Practical note on the 10-business-day extension:** it applies to changes in the percentage sought,
the consideration, or the soliciting fee. A change outside those categories does not extend the
offer. Do not assume any amendment buys the holder ten more days.

## §2 — The Equity Analogue of an Option's Expiry Wall: FINRA Rule 11810(j)

An option has an expiration wall. An equity holder's nearest equivalent is a **security whose
delivery obligation sits inside a corporate-action window**:

- For contracts in **warrants, rights, convertibles, or securities subject to a tender or exchange
  offer, redemption, or expiry**, if the delivery deadline falls **on or after the contract
  settlement date**, the receiving member may serve a **Liability Notice instead of a buy-in**.
- The Liability Notice must be sent **no later than two hours before the cutoff time specified in
  the offer's instructions**.
- **Source:** FINRA Rule 11810(j).

**Why this is the file's most important paragraph.** The buy-in procedure in
`short-borrow-and-buy-in-mechanics.md` §2 gives a seller notice, a written-rejection window and a
3:00 p.m. cure. Rule 11810(j) does not: where the security is subject to a tender, exchange,
redemption or expiry, the member may substitute a **Liability Notice** for the buy-in, and the only
timing anchor in the rule is tied to the **offer's own instructions** — not to a fixed number of
days. The deadline is the offer document's, and it is not negotiable.

**The operational consequence:** for any position in a security with a pending corporate action, the
holder must read the **offer's instructions** and find the cutoff time, then work backwards. There is
no default to fall back on.

## §3 — Merger and Cash-Out Events

A merger cash-out has **no fixed clock**. The date on which holders receive cash is the **merger
effective date**, disclosed in the proxy statement and in the Current Report on Form 8-K filed on
completion. **Tag:** [COMMON-PRACTICE] for the mechanism; the specific date is a matter of reading
the filing, not of applying a rule.

What the risk engineer must record:

| Item | Why |
|---|---|
| Expected effective date, with its source | It is the date the position stops being a position |
| Whether consideration is cash, stock, or a mix | A stock consideration creates a *new* position with its own exit cost and its own concentration weight, on a date nobody chose |
| Whether the deal is subject to a financing or regulatory condition | A deal break resets everything; the position's exit plan must survive a break |
| The break price | The price at which the position re-opens as an ordinary holding if the deal fails |

A merger is not an exit plan. It is an exit *event* whose terms the holder did not negotiate. Where a
position's whole thesis is the deal, the drawdown if the deal breaks is the risk — and that is a
different skill's question (see `## Cross-Skill Coordination` in the skill body).

## §4 — Delisting, Deficiency and Halt: Nasdaq Rule 5810

| Item | Value | Source |
|---|---|---|
| Compliance plan submission | generally **45 calendar days** to submit a plan to regain compliance — as read in the rule version at the time of writing; see the version note below | Nasdaq Rule 5810(c)(2)(C)/(F) |
| The "(v)" case | **60 calendar days** — same version caveat | Nasdaq Rule 5810(c)(2)(F) |
| **Bid-price deficiency cure — the 180-day clock** | the rule grants an **automatic compliance period of 180 calendar days** from the date of the deficiency notice, for the **$1.00 bid-price** requirement | **Nasdaq Rule 5810(c)(3)(A)** `[VERIFIED — Nasdaq Rule 5810(c)(3)(A)]` |
| **The 360-day figure** | a security is **suspended if non-compliant with the $1.00 bid-price requirement for more than 360 days** — a **suspension trigger in the rule**, not merely Listing Council discretion | Nasdaq Rule 5810, as amended |
| Listing Council discretion | may grant additional time beyond the automatic periods | Nasdaq Rule 5810 |
| **Rule version** | Rule 5810 has been **amended — SEC approval 2024-10-07, and again in February 2025**. Any citation to the **eff. 2023-10-02** version is **superseded** | Nasdaq Rule 5810 amendment filings |

### §4.1 — The 180-day bid-price cure is real — and it is the issuer's clock, not yours

The widely repeated claim that a listing deficiency based on a **bid price below $1.00** gives the
issuer **180 calendar days** to cure is **confirmed by the rule text**: Nasdaq Rule 5810(c)(3)(A)
grants an **automatic compliance period of 180 calendar days** from the date of the deficiency
notice. `[VERIFIED — Nasdaq Rule 5810(c)(3)(A)]` An earlier draft of this file hedged that number as
unverifiable; it is asserted here as a rule because the primary text supports it, and because a hedge
where the rule is plain removes a real clock from the reader's calendar.

Three things come with that number, and each one is a way it gets misread:

- **180 days is an automatic period, not a favour.** It runs from the deficiency notice. It is not
  discretionary relief the issuer must ask for.
- **The 360-day figure is a suspension trigger, not an extension.** The security is **suspended if
  non-compliant with the $1.00 bid-price requirement for more than 360 days**. Reading it as "the
  issuer really has 360 days" inverts it: it is the point at which the listing stops.
- **The rule version matters.** Rule 5810 was amended with **SEC approval 2024-10-07** and again in
  **February 2025**, so the **eff. 2023-10-02** text is superseded. Re-read the current text before
  relying on any period above, including the **45-day** and **60-day** compliance-plan windows, which
  are quoted here from the rule version read at the time of writing and were not re-verified against
  the amended text.

**The clock that matters to a holder is still the announcement, not the cure period.** The point of a
delisting clock for a *holder* has never been the issuer's cure period. It is that a delisting
announcement produces (a) a liquidity break, (b) a possible move to a different venue with a different
margin treatment, and (c) an exit whose schedule is now set by an event rather than by the holder.
Those three consequences are true whether the issuer has 45, 60, 180 or 360 days — which is exactly
why the holder's actionable clock is the announcement and never the issuer's 180.

### §4.2 — Halts

A trading halt is operational, not scheduled: continuous trading stops, and the holder's ability to
act stops with it. No rule in this file governs the holder's remedy during a halt, because there is
none. The correct treatment is pre-emptive: **a position whose exit plan requires trading on a day
that might be halted is a position whose exit plan is not a plan.** Size for the halt, not for the
average day. **Tag:** [COMMON-PRACTICE].

## §5 — Splits, Reverse Splits and Spin-Offs

| Event | What changes | Where the decision belongs |
|---|---|---|
| **Forward split** | Share count up, price down; position value unchanged | Nothing to decide. Re-check `position_shares / ADV` (the ratio is unchanged if volume splits proportionally — verify, do not assume) |
| **Reverse split** | Share count down, price up; the position may cross the **$5.00** boundary in `margin-regimes-and-forced-liquidation.md` §2, changing a short's maintenance requirement between the `$2.50/share or 100%` row and the `$5.00/share or 30%` row | Margin: this file; tax lot identification and basis: `equity-tax-lot-and-exit-management` |
| **Spin-off** | A new security arrives, with its own ticker, its own liquidity, its own concentration weight and its own T+1 settlement | Concentration and exit cost: this skill. Cost-basis allocation and lot identification: `equity-tax-lot-and-exit-management` |
| **Cash dividend** | No position change; but it is the driver of early exercise on short calls — an options-book concern | `options-risk-engineer` |

**The spin-off is the one people miss.** A holder receives a position they never sized, in a security
whose ADV nobody measured, whose exit cost nobody recorded, and which immediately counts toward the
book's concentration. It must be sized and given an exit route on the day it arrives, not at the next
monthly review. If the spin-off's value is large enough to breach a concentration cap, that is a
decision for the same week.

## §6 — Failure Modes

1. **Treating a tender offer's open period as an entitlement.** The clock binds the offeror; the
   holder's window is the offer's.
2. **Assuming any amendment extends an offer by 10 business days.** Only changes in the percentage
   sought, the consideration, or the soliciting fee do.
3. **Not reading the offer's instructions for the Rule 11810(j) cutoff.** The Liability Notice
   deadline is anchored to that document, not to a fixed number of days.
4. **Expecting a buy-in-style notice and cure window on a security inside a corporate action.**
   Rule 11810(j) substitutes a Liability Notice for the buy-in.
5. **Holding a merger-arbitrage position with no plan for a deal break.** The break price is the
   position's real risk.
6. **Accepting stock consideration and forgetting that it is a new position** with an unrecorded exit
   cost and concentration weight.
7. **Quoting the 180-day bid-price cure from a superseded rule version, or reading the issuer's
   180 days as the holder's own clock.** The cure period is real — Nasdaq Rule 5810(c)(3)(A), an
   **automatic 180 calendar days** from the deficiency notice — and Rule 5810 was amended in 2024 and
   again in 2025, so the version cited matters. For a holder the actionable clock is the
   **announcement**, never the issuer's cure period.
8. **Assuming a delisting clock gives the holder time.** The holder's clock is the announcement, not
   the issuer's cure period.
9. **Planning an exit that requires trading during a possible halt.** Size for the halt.
10. **Ignoring a spin-off's arrival.** New position, new concentration, new exit cost, unmeasured.
11. **Treating a reverse split as a non-event.** It can move a short across the $5.00 maintenance
    boundary.

## §7 — Verification

- [ ] Every position in a security with a pending corporate action has the event date and its source
      recorded.
- [ ] Where a tender, exchange, redemption or expiry is pending, the **offer's instruction cutoff
      time** has been read and the Rule 11810(j) deadline computed from it.
- [ ] Where a delisting deficiency exists, the **180-calendar-day** bid-price cure is quoted from
      **Nasdaq Rule 5810(c)(3)(A)** in its current form, the holder's own clock is stated as the
      **announcement**, and the 360-day figure is characterised as the suspension trigger.
- [ ] No period from a **superseded** rule version is cited without the version caveat (Rule 5810 was
      amended 2024-10-07 and again February 2025).
- [ ] Every spin-off received has been sized and given an exit route within the same week.
- [ ] No event has been given a made-up clock. Where a rule was not retrieved, the text says so.
