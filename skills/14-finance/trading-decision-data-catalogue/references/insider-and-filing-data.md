# Insider and Filing Data

Filings are the most over-read datasets in trading, and the reason is uniform: **every form has a
deadline and a content limit, and the content limit is where the misreading happens.** A 13F is not a
portfolio. A Form 4 is not a conviction. A Form 144 is not a sale.

## §1 — The Form Ladder

| Form | Who files | Deadline | What it structurally cannot contain |
|---|---|---|---|
| **Form 4** | insiders (officers, directors, 10% holders) | before the end of the **2nd business day after execution** `[VERIFIED — 17 CFR 240.16a-3(g)]` | intent, motive, or a distinction between a conviction buy and a mechanical one — you must make that distinction yourself |
| **Form 144** | affiliates proposing to sell restricted stock | at or before the placement of the sell order `[VERIFIED — 17 CFR 230.144]` | an actual sale. It is an **INTENT to sell** |
| **Schedule 13D** | beneficial owners above 5% | initial within **5 business days**; amendments within **2 business days** `[VERIFIED — 17 CFR 240.13d-1, 13d-2; effective 2024-02-05]` | small positions, and anything the filer does not consider material |
| **Schedule 13G** | qualified institutional and passive holders | variants at **45 days after quarter-end / 5 business days after month-end / 5 business days after acquisition** `[VERIFIED — 17 CFR 240.13d-1]` | the short side, and any change between the variant's own reporting points |
| **Form 13F** | institutions managing **≥ $100M** | within **45 days after quarter-end** `[VERIFIED — 17 CFR 240.13f-1]` | **shorts, most of the book, and any position under confidential treatment** — which now files on EDGAR so the position is simply absent `[VERIFIED — SEC 13F FAQ]` |
| **Form SHO / Rule 13f-2** | managers, monthly short positions | **does not exist yet** — exempt until **Jan 2, 2028** `[VERIFIED — SEC exemptive order, FR 2025-22158]` | everything. First reports would cover Jan 2028, due within 14 calendar days after month-end |

## §2 — Form 4: Only Open-Market Code-P Cluster Buys Carry Information

**Source:** 17 CFR 240.16a-3 and SEC guidance. `[VERIFIED — 17 CFR 240.16a-3; SEC guidance]`.

Form 4 is a **transaction form**, not a sentiment form. Almost everything on it is mechanical:

| Transaction code | What it is | Information content |
|---|---|---|
| **P** — open-market or private purchase | a discretionary buy at market | **the only code that carries a buy signal** |
| **S** — open-market or private sale | a discretionary sale | weak; often diversification or a plan |
| **M** — option exercise | converting an option | none by itself; the resulting shares may then be sold |
| **F** — tax withholding | shares withheld to cover tax | none |
| **A** — grant or award | compensation | none |
| **G** — gift | a transfer for no consideration | none |
| **D** — disposition to the issuer | a sale back to the company | none about the market's view |

### 2.1 — The three filters that turn Form 4 into a signal

1. **Open market only.** Discard M, F, A, G, D.
2. **Code P only.** Discard S, and note that a P followed by an S in the same week is not a buy.
3. **Exclude plan trades.** A **10b5-1 plan** trade dates from broker notification, and where that
   notice is late the deemed execution date is the **3rd business day** `[VERIFIED — 17 CFR 240.16a-3(g)]`.
   A plan trade is scheduled, not informed.

*Then* the cluster rule: **≥3 insiders, open market, code P, no plan, over a short window**, is the
event people actually mean when they say "insider buying".

### 2.2 — How Form 4 lies

1. **The code table makes everything look like a transaction.** A reader who does not parse codes is
   reading compensation paperwork as conviction.
2. **A cluster of plan sales in one week looks like distribution.** It is a calendar.
3. **The 2-business-day deadline makes it fast, which makes it tempting.** Fast is not the same as
   informative.

## §3 — Form 13F: The 45-Day Lag and the "Delta" Trap

**Source:** 17 CFR 240.13f-1 and the SEC 13F FAQ. `[VERIFIED — 17 CFR 240.13f-1]`, `[VERIFIED — SEC 13F FAQ]`.

### 3.1 — The lag, stated flatly

| Event | Timing |
|---|---|
| Quarter ends | — |
| Filing due | within **45 days after quarter-end** |
| Realistic staleness when you read it | up to **4.5 months** after the positions were held |

### 3.2 — The trap

A quarter-over-quarter change — the "delta" — is computed and traded as if it were current news about
a manager's view. It is a difference between two snapshots taken at unknown dates up to four and a
half months ago, of a **partial, long-only** book.

### 3.3 — The four structural limits

1. **Long-only.** No shorts appear. A manager's short thesis is invisible.
2. **Not the whole book.** Only the listed, reported categories; many instruments are out of scope.
3. **Confidential treatment.** Requests are now filed on EDGAR, so a position under treatment is
   **absent** rather than hidden — the file does not tell you it is missing.
4. **Duplicate and managed filings.** The same book is reported by several entities. **Aggregate by
   CIK family, not manager name.** Two rows with identical holdings in the same quarter are one
   position, not two.

### 3.4 — The ticker↔CIK mapping caveat

The ticker↔CIK mapping files are explicitly **"not guaranteed for accuracy"** and are **cumulative**,
so one CIK can map to several historical names `[VERIFIED — SEC]`. A naive join on ticker will
silently merge or split entities.

## §4 — EDGAR Operational Limits

**Source:** SEC, "Accessing EDGAR Data". `[VERIFIED — SEC Accessing EDGAR Data]`.

| Property | Value |
|---|---|
| Acceptance window | **6:00am – 10:00pm ET** |
| Late-filing dissemination | filings after **5:30pm ET** (**10:00pm ET** for Forms 3/4/5) disseminate the **next business day** |
| Rate limit | **10 requests/second** |
| Required header | a declared **User-Agent** |
| Corrections and deletions | **not backfilled** into prior daily or feed indexes; full/quarterly indexes rebuild weekly, early Saturday |

**The operational consequence, in one sentence:** *a correction to a filing you already read will not
appear in the index you read it from, so your snapshot of EDGAR is permanently and silently
incomplete.*

## §5 — Ranked: Filing Datasets for an Insider or Ownership Question

| Rank | Dataset | Kind | Verdict |
|---|---|---|---|
| 1 | **Form 4, filtered to open-market code-P cluster buys excluding 10b5-1** | SIGNAL | the highest-signal insider dataset, and only with the filters applied `[VERIFIED — 17 CFR 240.16a-3; SEC guidance]` |
| 2 | **Schedule 13D, initial and amendments** | SIGNAL | the fastest public window on a large new stake; the 5-business-day and 2-business-day windows are recent `[VERIFIED — 17 CFR 240.13d-1, 13d-2]` |
| 3 | **Schedule 13G variants** | SIGNAL | slower by construction; useful for the passive book |
| 4 | **EDGAR full-text search and the `data.sec.gov` APIs** | STATE (infrastructure) | free, and the only way to build a point-in-time own snapshot |
| 5 | **Form 144** | STATE (intent) | a supply signal at best, never a sale |
| 6 | **Form 13F** | STATE (partial snapshot) | ranked low deliberately: long-only, 45 days late, incomplete |
| 7 | **Form SHO / Rule 13f-2** | **does not exist** | exempt until Jan 2, 2028. Any catalogue listing it as available is wrong |

## §6 — Ten Failure Modes in Filing Analysis

1. **The 13F delta read as fresh news.** Detection: compute the actual number of days between
   quarter-end and your read date before drawing a conclusion.
2. **Manager-name aggregation across a family of entities.** Detection: count distinct CIKs behind
   the manager name.
3. **A Form 4 code that is not P read as a buy.** Detection: print the code column.
4. **A 10b5-1 plan trade counted as a cluster member.** Detection: check the plan footnote before the
   trade enters any cluster.
5. **A Form 144 read as a completed sale.** Detection: quote the form's own title — it is a notice of
   proposed sale.
6. **Insider analysis applied to someone who is not an insider.** Detection: does the person file
   Forms 3/4/5? If not, the clock is not theirs.
7. **A correction assumed to have propagated into your index.** Detection: EDGAR does not backfill
   corrections into prior index files `[VERIFIED — SEC Accessing EDGAR Data]`; re-query when it
   matters.
8. **A rate-limit or User-Agent violation mistaken for an absence of filings.** Detection: check the
   response status before concluding the filing does not exist.
9. **Confidential treatment read as a zero position.** Detection: the position is absent, not zero.
   Absence of a row is not absence of a holding.
10. **A 13F option-exposure inference treated as a disclosed position.** Detection: does the form
    report it, or did someone derive it? If derived, it is `[COMMON-PRACTICE]` at best.

**Source:** 17 CFR 240.16a-3(g) for the Form 4 deadline and the 10b5-1 deemed-execution rule; 17 CFR
230.144 for Form 144; 17 CFR 240.13d-1 and 240.13d-2 for the Schedule 13D/13G deadlines and the
2024-02-05 effective date; 17 CFR 240.13f-1 and the SEC 13F FAQ for the 13F threshold, deadline and
structural limits; the SEC's "Accessing EDGAR Data" page for the acceptance window, dissemination
timing, rate limit, User-Agent requirement and the non-backfilling of corrections; the SEC exemptive
order at FR 2025-22158 for the Form SHO and Rule 13f-2 dates; and the SEC's own statement that the
ticker↔CIK mapping files are not guaranteed for accuracy. Re-read each before a live decision depends
on it.
