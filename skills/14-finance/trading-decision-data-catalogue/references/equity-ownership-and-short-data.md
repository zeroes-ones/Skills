# Equity Ownership and Short-Side Data

Four datasets, four questions, one word — "short". This file exists because those four are conflated
in a single sentence roughly every day, and the conflation produces a thesis out of a settlement
mechanic.

| The question | The dataset | Kind | The word people use for all four |
|---|---|---|---|
| How many shares are **held** short? | FINRA Rule 4560 short interest | STATE | "short interest" |
| How much **short selling happened** today? | FINRA daily short-sale volume | STATE (flow) | "short interest" |
| Is delivery **failing**? | SEC fails-to-deliver | STATE (settlement) | "naked shorting" |
| Can I **borrow** it? | the broker's own inventory | CONSTRAINT | "shortable" |

## §1 — FINRA Rule 4560 Equity Short Interest

**Source:** FINRA Rule 4560. `[VERIFIED — FINRA Rule 4560]`.

### 1.1 — The cycle, stated in full

| Step | When |
|---|---|
| Settlement date | the **15th** of the month, or the prior settlement business day if the 15th is not one; and the **last settlement business day** of the month |
| Firm reporting deadline | by **6pm ET on the 2nd business day** after the settlement date |
| Publication | the **7th business day after settlement** |
| History available | **5 rolling years** |
| Corrections | carry a **Revision Flag** and **overwrite history** |

### 1.2 — How it lies

1. **The revision overwrites the original.** This is the single most damaging property. A rising
   line can be a correction to an old period, not new shorting, and the flag is the only way to tell.
2. **It is bi-monthly, so it is slow.** A two-week cadence is fine for a crowding question and useless
   for an intraday one. Do not use it as a timing input.
3. **It is a position count, not a directional view.** A high short interest in a small float is a
   crowding fact; whether it is bullish or bearish depends on which side can be forced to cover.
4. **It does not cover everything you think it covers.** Read the rule's scope rather than assuming
   the file is the whole market.

### 1.3 — What decision it changes

Whether a short is crowded — and the honest answer to "how short is this name really" is this
dataset or nothing.

## §2 — FINRA Daily Short Sale Volume

**Source:** FINRA dataset documentation. `[VERIFIED — FINRA dataset documentation]`.

- **Daily**, which is why it is so popular.
- **Off-exchange only** — TRF, ADF, ORF. It is **not consolidated** with exchange-reported short
  volume, so it is a subset of the day's short selling by construction.
- **FINRA states it does not equate to the bi-monthly short interest figure.**

### 2.1 — The trap in one line

A trader reads a spike in daily short-sale volume as "shorts are piling in". Three things are wrong:
it is a **flow** not a **position**; it is **partial**; and much of daily short volume is
**market-making and hedging**, which is not a directional bet at all.

**Detection rule:** *if the number is daily, it is not short interest.* Say it out loud.

### 2.2 — Where it is legitimately useful

| Use | Legitimate? |
|---|---|
| Reading intraday short-side activity in a name you are already short | Yes, with the subset caveat |
| Detecting a change in who is trading a name | Weakly — it has no participant identity |
| Concluding that short interest rose | **No.** Wrong dataset entirely |
| Concluding that a name is being manipulated | **No.** It cannot support that |

## §3 — SEC Fails-to-Deliver

**Source:** the SEC's fails-to-deliver dataset, published **twice a month**, free, with history from
**2004Q1** `[VERIFIED — SEC]`.

### 3.1 — The SEC's own statement of what a fail is not

The SEC states that a fail **"may result from either a short or a long sale"** and that naked short
selling **"is not necessarily a violation"** `[VERIFIED — SEC Reg SHO investor page]`.

**Read that page for what it is.** It is authoritative for the two Reg SHO propositions quoted here,
and it is **stale on settlement**: it still teaches **T+2** for US equities and predates the
2024-05-28 T+1 compliance date. **Do not inherit settlement facts from it** — take settlement from
SEC Release 34-96930 (`constraint-data-and-calendars.md` §2). The same warning applies to every other
citation of that page in this skill.

Read that once more, because it removes the entire evidentiary basis of a widely traded thesis. A
fail is a **settlement event**. It means a delivery did not happen on time. It does not identify who
failed, which side they were on, or why.

### 3.2 — The three legitimate uses

1. **As a settlement-stress indicator** alongside the threshold list, which is the only configuration
   in which it says anything.
2. **As a data-quality check** on your own clearing understanding — the file is a rare public window
   into settlement mechanics.
3. **As a research artifact** for studying the plumbing, which is what it actually is.

### 3.3 — The one illegitimate use

Arguing manipulation. Do not do it. If someone hands you an FTD chart captioned "naked shorting", the
correct response is the SEC's own sentence, quoted.

## §4 — The Reg SHO Threshold List and the 13-Settlement-Day Clock

**Source:** 17 CFR 242.203 and the SEC's threshold-security documentation. `[VERIFIED — 17 CFR 242.203; SEC]`.

### 4.1 — The two-leg test

```
fail-to-deliver positions ≥ 10,000 shares
        AND
fail-to-deliver positions ≥ 0.5% of the security's shares outstanding
for 5 consecutive settlement days
        →  the security is a THRESHOLD SECURITY
        →  close out after 13 consecutive settlement days
```

Which leg binds, by share count `[COMPUTED]`:

| Shares outstanding | Binding leg | Threshold in shares |
|---|---|---|
| 1,000,000 | the 10,000-share leg (0.5% would be 5,000) | 10,000 |
| 2,000,000 | both, exactly (0.5% = 10,000) | 10,000 |
| 20,000,000 | the 0.5% leg (0.5% = 100,000) | 100,000 |

So a small-cap name can be placed on the list by a fail that would be invisible in a large cap.

### 4.2 — Publication: one list is not the universe

**Only the exchange with the primary listing publishes a name.** The commonly cited Nasdaq list is
therefore **not** the market's threshold universe. If a name's primary listing is elsewhere, its
absence from the list you are reading means nothing.

**Detection rule:** record which exchange published the list you read, and check the primary listing
of the name.

### 4.3 — The SEC's scope statement

Appearance on the threshold list **"should not be interpreted as connoting anything negative about
the particular issuer"** `[VERIFIED — SEC]`. The list is a **CONSTRAINT** — it changes what a short
seller can do — not a **SIGNAL** about the company.

### 4.4 — Rule 204 close-out clocks

**Source:** 17 CFR 242.204(a). `[VERIFIED — 17 CFR 242.204(a)]`.

| Case | Close-out deadline |
|---|---|
| General fail to deliver | by the **beginning of regular trading on the settlement day following** the settlement date |
| Fail from a **long sale** | by the **3rd consecutive settlement day** |
| Fail on a **Rule 144** / deemed-to-own position | within **35 consecutive calendar days** |

Three clocks, three lengths, one shared property: **all of them are counts, not announcements.**
Nobody calls to say the count has started.

## §5 — Borrow: The Constraint With No Public Source

**Source:** SEC exemptive relief (FR 2025-22158). `[VERIFIED — SEC exemptive order, FR 2025-22158]`.

- **Rule 10c-1a securities-lending reporting is exempt until Sept 28, 2028, and FINRA public
  dissemination is exempt until March 29, 2029.** The same order exempts **Form SHO / Rule 13f-2
  monthly manager short positions until Jan 2, 2028**, with first reports covering Jan 2028 and due
  within 14 calendar days after month-end.
- **Therefore borrow has no primary public source.** Anything sold as a market-wide borrow feed is a
  broker's inventory or an aggregation of broker inventories, and it is `[BROKER-VERIFIED]` at best.
- **A broker's "shortable shares" is that broker's inventory, not the market's, and it changes
  intraday.** Record the broker and the read timestamp, always.

### 5.1 — How to record a borrow

| Field | Value |
|---|---|
| `broker` | the desk named |
| `read_timestamp` | with timezone |
| `borrow_status` | easy / hard / unavailable |
| `borrow_fee_annual_pct` | as quoted |
| `recall_terms` | from the lending agreement, not from a rule |

**There is no rule-fixed recall notice period.** Commonly quoted practice is 1–2 business days and
that is `[COMMON-PRACTICE]`, not a rule.

## §6 — The Five Ways This File's Datasets Get Misread

1. **Substituting the daily flow for the bi-monthly position.** Detection: check the cadence of the
   number before reading its level. Daily means flow.
2. **Treating a fail as a short-sale fact.** Detection: quote the SEC sentence. If the FTD chart
   cannot survive that sentence, it is not evidence.
3. **Reading the threshold list as an accusation.** Detection: quote the SEC's scope statement, then
   ask which exchange published the list.
4. **Quoting a borrow figure as a market fact.** Detection: is the broker named, and is there a read
   timestamp?
5. **Ignoring the revision flag on short interest.** Detection: does the record contain a field for
   it? If not, the record cannot distinguish new shorting from a correction.

6. **Assuming a short is maintainable because it is currently short.** Detection: is there a borrow
   status with a read timestamp inside the last trading session? If not, the maintainability claim is
   unmeasured.
7. **Reading a rising short interest into a falling price as confirmation.** Detection: state the
   base rate for that pattern before reading the chart. Without it, the observation is a story.
8. **Using fails-to-deliver without the threshold list.** Detection: is the threshold list in the
   record? Without it, the FTD number has no anchor and no rule attached.
9. **Treating a de-listing from the threshold list as an all-clear.** Detection: the security drops
   off only after returning below **both** legs for **5 consecutive settlement days**
   `[VERIFIED — 17 CFR 242.203(b)(3), (c)(6)]`. A one-day improvement is not a de-listing.
10. **Confusing "shortable" with "locatable".** Detection: a locate is an affirmative confirmation for
    a specific size at a specific time; a shortable flag is a column. They are not the same fact.

**Source:** FINRA Rule 4560 and FINRA's daily short-sale-volume dataset documentation; the SEC's
fails-to-deliver dataset page and its Reg SHO investor page (authoritative for the fail's stated
non-meaning, **stale on settlement** — it still teaches T+2, so settlement comes from SEC Release
34-96930 alone); 17 CFR 242.203(b)(3) and (c)(6) for the
threshold-security test and the 13-settlement-day close-out, and 17 CFR 242.204(a) for the Rule 204
close-out clocks; the SEC exemptive order published at FR 2025-22158 for the Form SHO / Rule 13f-2
and Rule 10c-1a effective dates. Each was read from the publisher; re-read before a live short
decision depends on it.
