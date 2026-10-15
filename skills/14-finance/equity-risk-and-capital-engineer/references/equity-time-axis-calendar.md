# The Equity Time Axis — The Clocks That Force Action

Equities have no days-to-expiration. That fact is the reason most equity risk work is under-built:
the options trader has a countdown printed on the contract and an equity holder believes they have
time. They do not. An equity position is governed by **calendars written in regulation, statute and
contract**, and every one of them can force a sale, a delivery, a close-out or a taxable event at a
price the holder did not choose.

This file is the single consolidated clock table for the skill. Everything else in the skill
(margin, borrow, liquidity, the reserve floor) references these clocks rather than restating them.

## §1 — The Four Clocks (and the two that follow them)

| Clock | Rule | Source | Forces |
|---|---|---|---|
| **Settlement** | **T+1** since 2024-05-28 (previously T+2) | SEC Release 34-96930 ("Shortening the Securities Transaction Settlement Cycle") | funding and delivery deadline: cash must be there and shares must be deliverable one business day after the trade |
| **Reg T payment / margin call** | settlement **+ 2 business days = 3 business days** from the trade | 12 CFR 220.2 (definition of "payment period"), 220.4(c)(3)(i) | fund the call with settled funds — or the firm acts |
| **Tax holding period** | long-term = **more than 1 year**; the period runs from the day **after** the buy trade date to the **sale trade date** | IRC §1222; IRS Publication 550 | a **barrier, not a deadline**: it does not force a sale, it changes the tax on one |
| **Wash sale** | **61-day window, ±30 days around the sale** | IRC §1091 | a **window to stay out of**, not a date to act on |
| **Short-swing (insiders)** | **less than six months** between a purchase and a sale by an insider | 15 U.S.C. §78p(b) | disgorgement — the insider's real DTE |
| **Reg SHO close-out** | Close out a fail to deliver: (a) by the **beginning of regular trading hours on the settlement day following the settlement date**; (b) by the **third consecutive settlement day** for a fail resulting from a long sale; (c) within **35 consecutive calendar days** for a fail on a Rule 144 / deemed-to-own position | 17 CFR 242.204(a) | forced close-out of a short position, at any price, by the firm |
| **Threshold securities** | A security is on the SRO threshold list when fail-to-deliver positions are **≥ 10,000 shares AND ≥ 0.5% of shares outstanding for 5 consecutive settlement days**; a member holding a threshold position must close out after **13 consecutive settlement days** of fails; the security drops off the list after **5 consecutive settlement days** back below both thresholds | 17 CFR 242.203(b)(3) and 242.203(c)(6) | a rolling clock that removes borrow, then removes the position |

> **The honest scope line on the clock table.** The first two rows, the holding period, the wash-sale
> window and the Reg SHO rows are structural: they apply to any holder of the security. The
> short-swing row and the threshold-security row apply to specific parties — insiders and members
> with delivery obligations respectively. See §4 before you build a risk list out of them.

**Source:** SEC Release 34-96930 (T+1 effective 2024-05-28); 12 CFR 220.2 and 220.4(c)(3)(i) (Reg T
payment period); IRC §1222 and IRS Publication 550 (holding period); IRC §1091 (wash sales);
15 U.S.C. §78p(b) (short-swing); 17 CFR 242.204(a) (Reg SHO close-out); 17 CFR 242.203(b)(3),
(c)(6) (threshold securities).

## §2 — Reading the Table as a Countdown

The table is not a list of facts to look up; it is the equity analogue of the options DTE ladder.
Read it as a sequence of *moments when the holder loses control of the price*:

1. **The trade is done and nothing is settled.** Between the trade and T+1 the cash is not the
   broker's yet and the shares are not the buyer's yet. A position opened "today" is not funded
   today.
2. **T+1 — settlement.** Cash or shares change hands. The first hard moment. If the cash is not
   there for a purchase, the firm is now carrying a delivery obligation it did not agree to carry.
3. **T+3 — the Reg T payment deadline** (settlement + 2 business days). The second hard moment. Past
   it, the firm **must** act (see §3 below and `margin-regimes-and-forced-liquidation.md`).
4. **"More than one year" — the long-term barrier.** Crossing it is worth money and forces nothing.
   It is on this table because it is the reason a holder *chooses* to do nothing, and "do nothing"
   is a decision the calendar is making for them.
5. **±30 days around a sale — the wash-sale window.** It does not force a sale. It forces a **61-day
   abstention** if the loss is to be deductible. It is the only clock here that constrains the
   *re-entry*, not the exit.
6. **Six months — the insider's clock.** For anyone who is an insider or an affiliate, a purchase
   and a sale inside six months is not a trade, it is a disgorgement claim.
7. **The Reg SHO clock on the other side of your short.** If the shares you are short are failing to
   deliver, the firm's clock — not yours — forces the close-out.

## §3 — What Happens If You Do Nothing

| Clock | You do nothing | Who acts | At what price |
|---|---|---|---|
| Settlement | A delivery failure is created | The firm, the clearing broker | Any price available — the seller has no say |
| Reg T payment (T+3) | The firm **must** liquidate the position or the account's deficiency | The firm, without advance notice | The market price of the liquidation moment |
| Holding period | Position is still held; the gain changes character | Nobody | No price risk created by the clock itself |
| Wash sale | The loss is disallowed and added to the replacement lot's basis | Nobody immediately; the tax return later | No price risk, but a real dollar cost |
| Short-swing | Disgorgement of the profit plus interest | The issuer (a derivative action) or the SEC | The profit, not the position |
| Reg SHO close-out | The firm closes the short out and buys in | The firm | Any price — for the account and liability of the party in default |
| Threshold security | Borrow disappears, then the position is closed out at 13 consecutive settlement days | The firm | Any price |

**Source:** 17 CFR 242.204(a); 12 CFR 220.4(d); FINRA Rule 4210(f)(6).

## §4 — The Insider / Institutional Clock Set, and Who It Binds

These are real clocks, with real sources, and they are **not** the retail holder's clocks. They are
listed here so the skill can route the insider case correctly — not so that a retail risk list can
be padded with them.

| Filing / constraint | Period | Source |
|---|---|---|
| Form 4 (insider change in beneficial ownership) | **2 business days** after the transaction date | 17 CFR 240.16a-3(g) |
| Form 3 (initial statement of beneficial ownership) | **10 days** after becoming an insider | 17 CFR 240.16a-3 |
| Schedule 13D initial filing (cross 5%) | **5 business days** after crossing | 17 CFR 240.13d-1 |
| Schedule 13D amendments | **2 business days** after a material change — effective **2024-02-05** | 17 CFR 240.13d-2 |
| Schedule 13G variants | **45 days after quarter end**; **5 business days after month end**; **5 business days after acquisition** (variant-dependent) | 17 CFR 240.13d-1 |
| Form 13F (≥ $100,000,000 under management) | **45 days after quarter end** | 17 CFR 240.13f-1 |
| Rule 10b5-1 plan cooling-off, directors and officers | later of **90 days** or **2 business days after the covering 10-Q/10-K**, **capped at 120 days** — effective **2023-02-27** | 17 CFR 240.10b5-1(c)(1)(ii)(B) |
| Rule 10b5-1 plan cooling-off, other persons | **30 days** | 17 CFR 240.10b5-1(c)(1)(ii)(B) |
| Rule 144 holding period, restricted securities of a reporting issuer | **6 months** (**1 year** for a non-reporting issuer) | 17 CFR 230.144 |

**If the reader is an ordinary retail holder, this table is "not you".** It does not belong in their
risk log, it does not change their exit plan, and it must never be used to make the risk picture look
more thorough than it is. Say which case the user is in before quoting any row of §4.

## §5 — How the Clocks Compose

The clocks are not independent, and the compound case is where money is actually lost:

- **Gap on the day before a settlement deadline.** A purchase settles T+1. If the account was funded
  by a sale in a **cash** account, the sale proceeds are themselves unsettled until their own T+1.
  The two T+1s can be one business day short of each other and the deficit is a free-riding
  violation, not a timing nuisance (see `settlement-and-payment-period.md` §4).
- **Margin call plus a wash-sale window.** Selling to meet a call at a loss inside ±30 days of a
  purchase creates a disallowed loss *while* the call is being cured. The tax consequence and the
  margin cure compete for the same 61 days.
- **Short call plus Reg SHO.** A short position whose fails cross the threshold clock is closed out
  whether or not the thesis still holds. The clock is not interested in the thesis.
- **Holding-period barrier plus a tender offer.** A position three weeks short of long-term that is
  subject to a tender deadline has two clocks pushing in opposite directions. See
  `corporate-action-and-halt-playbook.md` §2.
- **Six-month insider clock plus any sale.** For an insider, the position's risk is not the drawdown;
  it is the calendar.

## §6 — Operating the Calendar

1. **Record all clocks per position at entry.** For every position, the entry record carries: trade
   date, settlement date (T+1), Reg T payment date (settlement + 2 business days), the holding-period
   date (buy trade date + 1 year + 1 day), the wash-sale window (sale date ±30 days) if a loss is
   realised, and — for shorts — the borrow status and any fail-to-deliver age.
2. **Convert business-day clocks to dates, not to "about a week".** A Reg T call dated "3 business
   days" spanning a weekend and a holiday is five calendar days. A call dated "3 days" is a call
   missed.
3. **Put the clocks in the risk log, not in memory.** A clock that is not written down is a clock
   that is discovered on the day it fires.
4. **Never derive a new rule from a clock.** These are the rules. A new "roughly two weeks" invented
   in the moment is not a clock, it is a hope.
5. **Flag the cutoff.** Every clock entry carries the date it was read. A knowledge cutoff means a
   calendar that has not been re-read may be a calendar that has moved — the Russell reconstitution
   change to semi-annual from 2026 is exactly that kind of move.

## §7 — Verification

- [ ] Every open position has a settlement date and a Reg T payment date recorded.
- [ ] Every short position has a borrow status and a fail age recorded.
- [ ] Every realised loss has its 61-day wash-sale window recorded.
- [ ] Every position destined for long-term treatment has the holding-period date recorded.
- [ ] The insider clock table has been checked against the user's actual status before being quoted.
- [ ] No clock in this file has been silently rounded, shortened, or restated in the skill's output.
