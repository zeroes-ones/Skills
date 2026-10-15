# Decision to Data Map — and the 12 Datasets That Most Change a Decision

This is the catalogue's entry point. It answers one question: **for this decision, which datasets
actually change what you do?** Everything else in this skill is a detail of one of these entries.

The map is organised by decision class, because a dataset cannot be ranked against a mood. If the
decision has not been named with an action verb and a horizon, stop here and go back to Phase 0.

## §1 — The Decision Classes

The eight names below are **decision classes**, not skill names. None of them is a skill in this
library and none of them is a routing target — they are the vocabulary this catalogue ranks datasets
against, and nothing in this file should be read as a cross-skill reference.

| Decision class | The action verb | The horizon that usually applies | The constraint that usually binds |
|---|---|---|---|
| **short-entry** | consider shorting | days to weeks | can you borrow it at all; the Reg SHO threshold clock |
| **short-carry** | consider holding a short | weeks to months | borrow fee drift; a recall; a buy-in |
| **event-hold** | consider holding through a print or an event | hours to days | the exchange calendar; the options expiration |
| **flow-read** | consider acting on observed options flow | hours to days | OI is end-of-day; the print may be one leg |
| **thesis-underwrite** | consider buying or adding on a fundamental case | months to years | point-in-time data; the 13F lag |
| **signal-triage** | consider trusting a signal | any | the base rate; the seller's holdout |
| **budget-prune** | consider subscribing or cancelling | a quarter | whether a decision changed at all |
| **backtest-audit** | consider believing a backtest | the backtest's period | survivorship; restatement; adjustment |

## §2 — The Twelve Datasets That Most Change a Decision, Ranked Best First

The ranking criterion is narrow and stated so it can be argued with: **how much does this dataset
change the action, and how often?** A dataset that prevents a loss ranks above one that offers a
gain, because the loss is certain once it happens and the gain is not. A dataset that binds many
decisions ranks above one that binds a few. Nice-to-know entries are not on this list.

| Rank | Dataset | Kind | Publisher | Update frequency | **Lag** | What decision it changes |
|---|---|---|---|---|---|---|
| **1** | **FINRA equity short interest (Rule 4560)** | STATE | FINRA | semi-monthly | settlement on the 15th or the last settlement business day; reported by 6pm ET on the **2nd business day**; **published the 7th business day after settlement**; revisions carry a Revision Flag and overwrite history; 5 rolling years `[VERIFIED — FINRA Rule 4560]` | It is the only real short-**position** number in public data. It sizes the crowding question and disqualifies the alternatives (daily volume is a flow, FTD is a settlement artefact) |
| **2** | **Reg SHO threshold list + the 13-settlement-day clock** | CONSTRAINT | the exchange with the primary listing | daily | as published by each SRO; **only the exchange with the primary listing publishes a name, so one list is not the universe** `[VERIFIED — 17 CFR 242.203; SEC]` | It is binary. If the name is a threshold security, a close-out clock is running and the borrow may disappear entirely. It can remove the trade, which no signal can |
| **3** | **Exchange holiday and early-close calendars** | CONSTRAINT | NYSE / Nasdaq | annual, with revisions | published in advance for the year | Equities close **4:00pm ET**, options **4:15pm ET**; **equity** early close **1:00pm ET** on the day after Thanksgiving, **July 3** and Dec 24 `[VERIFIED — NYSE and Nasdaq published calendars]`. The **options** early close is **venue-specific** (1:15pm ET for eligible options on some venues; **13:00** at Cboe) — check your venue's calendar. Every intraday statistic you own is distorted on those days |
| **4** | **Your broker's borrow availability and fee** | CONSTRAINT | the broker, in the platform | continuous, **changes intraday near the open** | read time only; there is no publication lag because there is no publication. **No primary public source exists** — Rule 10c-1a is exempt until Sept 28, 2028 `[VERIFIED — SEC exemptive order, FR 2025-22158]` | It is the binding constraint on every short. "Shortable" at one desk is not shortable at another, and the fee can exceed the entire thesis |
| **5** | **CFTC Commitments of Traders** | SIGNAL (positioning) | CFTC | weekly | **data as of the close of the preceding Tuesday; published Friday 3:30pm ET**; the CFTC states processing takes three days; historical data is **never updated** | It distinguishes commercial from non-commercial positioning by market, which changes a contrarian or crowdedness read. It is not a timing tool |
| **6** | **Form 4, filtered to open-market code-P cluster buys excluding 10b5-1** | SIGNAL | SEC EDGAR | continuous | due before the end of the **2nd business day after execution** `[VERIFIED — 17 CFR 240.16a-3(g)]` | It is the highest-signal insider event available, and only when filtered: plan trades, option exercises, tax withholding and gifts all print as Form 4 `[VERIFIED — 17 CFR 240.16a-3; SEC guidance]` |
| **7** | **Federal Reserve H.4.1 balance sheet** | STATE | Federal Reserve | weekly | **as of Wednesday, released Thursdays generally 4:30pm ET**, shifted to the next business day on holidays `[VERIFIED — Federal Reserve]` | It is the reserve-supply backdrop against which every liquidity argument is made, and it is the input to the reserve-scarcity question that drives risk appetite |
| **8** | **Cboe open-close volume by participant capacity** | SIGNAL (structural) | Cboe DataShop | daily | sold as a dataset; read the product's own as-of documentation | It tells you **who** traded — Customer, Pro-Customer, Broker, Firm, Market Maker `[VERIFIED — Cboe DataShop]` — which is what most retail flow tools cannot. It converts "unusual activity" from a claim into a classified print |
| **9** | **SEC fails-to-deliver** | STATE (settlement) | SEC | **twice a month**, history from 2004Q1, free | publication follows the half-monthly reporting cycle `[VERIFIED — SEC]` | **Meaningful only alongside the threshold list.** On its own it is not a shorting measure: a fail "may result from either a short or a long sale" `[VERIFIED — SEC Reg SHO investor page]` |
| **10** | **FRED + ALFRED vintages** | STATE (point-in-time) | Federal Reserve Bank of St. Louis | daily for FRED; vintage-by-vintage for ALFRED | ALFRED exposes the series **as published on each vintage date** | Without ALFRED vintages every macro backtest is look-ahead biased, because FRED gives only the restated series `[VERIFIED — FRED/ALFRED]`. This entry changes backtests, not trades — which is why it ranks here rather than higher |
| **11** | **Schedule 13D / 13G** | SIGNAL (ownership) | SEC EDGAR | event-driven | **13D: initial within 5 business days, amendments within 2 business days**; 13G variants at 45 days after quarter-end / 5 business days after month-end / 5 business days after acquisition `[VERIFIED — 17 CFR 240.13d-1, 13d-2; effective 2024-02-05]` | It is the fastest public signal that a large holder has taken a stake — and the 5-business-day deadline is new, so older intuitions about the lag are wrong |
| **12** | **BLS and BEA release calendars (ICS)** | CONSTRAINT | BLS / BEA | annual, with updates | published in advance; calendar subscriptions available | It schedules the macro events that dominate the tape. A position carried into a release it did not know about is a position with an unplanned event risk |

### Why the ordering is what it is

**Ranks 1–4 are constraints and positions, and they are not interchangeable with the rest.** Each
one can remove the trade rather than inform it. A catalogue that ranked the CFTC's positioning data
above the borrow status would be a catalogue written by someone who has never been recalled.

**Ranks 5–8 are the signals worth the time.** They share one property: each has a **short, readable
lag** and a **named publisher**. That combination is rare. Most signals fail one of the two.

**Ranks 9–12 earn their place by changing a decision someone else already made.** ALFRED changes
your backtest rather than your trade; the release calendar changes your *calendar* rather than your
view. Both are legitimate, and both rank below anything that changes an open position.

## §3 — The Nine-Field Record for the Top Four

The same nine fields apply to all twelve; these four are shown in full because they are the ones
most likely to be misread.

### 3.1 — FINRA Rule 4560 equity short interest

- **Question it answers:** how many shares are actually held short in this name?
- **Kind:** STATE.
- **Exact source:** FINRA, Equity Short Interest (Rule 4560), the semi-monthly settlement-cycle file.
- **Cost:** free.
- **Frequency / lag:** semi-monthly; settlement on the 15th or the prior settlement business day, and
  the last settlement business day of the month; firms report by **6pm ET on the 2nd business day**;
  **publication on the 7th business day after settlement**; 5 rolling years available.
- **How it lies:** revisions **overwrite history**, so an apparent change can be a correction to a
  prior period. Duplicate and managed filings, and the difference between the position file and the
  daily volume file, are the other two ways it is misread.
- **What decision it changes:** whether a short is crowded, and whether the crowding is rising.
- **Timestamp rule:** record the settlement date, the publication date, and the **Revision Flag**.
- **Rank:** 1.

### 3.2 — The Reg SHO threshold list

- **Question it answers:** is a close-out clock running on a name I am short, or about to short?
- **Kind:** CONSTRAINT.
- **Exact source:** each exchange with a primary listing publishes its own list; Nasdaq's is the
  commonly cited one. **One list is not the universe.**
- **Cost:** free.
- **Frequency / lag:** daily, on the exchange's own schedule.
- **How it lies:** it reads as an accusation, and the SEC says the opposite — appearance "should not
  be interpreted as connoting anything negative about the particular issuer" `[VERIFIED — SEC]`. It
  also lies by omission: a name can be a threshold security on an exchange whose list you are not
  reading.
- **What decision it changes:** whether the short is maintainable at all.
- **Timestamp rule:** record the list's own as-of date and the exchange that published it.
- **Rank:** 2.

### 3.3 — The exchange calendar

- **Question it answers:** was the session a normal session?
- **Kind:** CONSTRAINT.
- **Exact source:** the exchange's own holiday and early-close calendar for the year.
- **Cost:** free.
- **Frequency / lag:** published in advance for the year.
- **How it lies:** it lies by omission — the half day is forgotten until a volume or volatility
  statistic looks wrong, and then the wrong conclusion is drawn from a short session.
- **What decision it changes:** whether any intraday statistic is comparable at all.
- **Timestamp rule:** record the year of the calendar and the date it was read.
- **Rank:** 3.

### 3.4 — Your broker's borrow availability

- **Question it answers:** can this position be established and maintained at this desk?
- **Kind:** CONSTRAINT.
- **Exact source:** the broker's own platform, recorded with the broker's name.
- **Cost:** free to read; the fee is a cost of the position, not of the data.
- **Frequency / lag:** continuous, and it changes intraday.
- **How it lies:** the number is **one broker's inventory**, presented in a column that looks like a
  market fact. It is not. And a "shortable" flag is not a locate.
- **What decision it changes:** every short decision, at the size the inventory can bear.
- **Timestamp rule:** record the broker, the platform, and the read timestamp.
- **Rank:** 4.

## §4 — The Decision → Data Lookup

| If the decision class is… | Start with | Then | Then rule out |
|---|---|---|---|
| **short-entry** | broker borrow (4) | threshold list (2) | short-sale volume as a position; FTD as manipulation |
| **short-carry** | broker borrow fee and recall terms (4) | short interest trend with the revision flag (1) | treating the fee as fixed |
| **event-hold** | exchange calendar (3) | the release calendar (12) | intraday statistics measured on a half day |
| **flow-read** | Cboe capacity data (8) | end-of-day open interest | single-leg UOA as a signal; GEX as an observation |
| **thesis-underwrite** | Form 4 filtered (6) | 13D/13G (11) | 13F deltas as smart money |
| **signal-triage** | base rate | a point-in-time sample | the seller's holdout |
| **budget-prune** | the decision each line changes | the free substitute | any vendor price not read from the vendor |
| **backtest-audit** | ALFRED vintages (10) | survivorship and adjustment status | a "history" restated after the fact |

## §5 — Ten Rules for Building This Map

1. **Name the decision before naming the dataset.** A dataset list without a decision is a shopping
   list.
2. **Kind first, rank second.** The kind decides what you may do with the number.
3. **Positions outrank signals.** A dataset that tells you what is held beats one that guesses what
   will happen.
4. **Constraints outrank both**, because a constraint can delete the decision.
5. **Lag outranks frequency.** Frequency is a publisher's habit; lag is your information delay.
6. **A dataset that changes no decision is nice-to-know.** Write it down, rank it low, do not pay.
7. **The twelve above are ordered deliberately.** Argue with the order by changing the criterion,
   not by adding entries.
8. **Re-read the publisher's page every quarter.** Exemptions expire and lags shorten.
9. **Two sources per fact where the fact is load-bearing.** One source is a claim.
10. **Record the read date on everything.** A dataset's age is part of the dataset.

**Source:** FINRA Rule 4560 for the reporting and publication cycle; 17 CFR 242.203 for the
threshold-security test and 242.204(a) for the close-out requirement; SEC exemptive relief
(FR 2025-22158) for the Form SHO and Rule 10c-1a effective dates; NYSE and Nasdaq calendars for the
session times; the CFTC for the Commitments of Traders as-of and publication schedule; 17 CFR
240.16a-3(g) for the Form 4 deadline; the Federal Reserve for the H.4.1 release schedule; Cboe
DataShop for the participant-capacity dataset; the SEC for the fails-to-deliver file; FRED/ALFRED
for vintages; 17 CFR 240.13d-1 and 13d-2 for the Schedule 13D/13G deadlines; BLS and BEA for the
release calendars. Each was read from the publisher in the state described above and must be re-read
before a live decision depends on it.
