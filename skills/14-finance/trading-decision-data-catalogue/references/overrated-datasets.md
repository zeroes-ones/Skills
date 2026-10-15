# Over-Rated Datasets

**A catalogue that ranks everything as useful is worthless**, so this file is the counterweight: the
datasets that are widely believed and do not earn their keep. Each entry states **why it is believed**
and **what it actually supports**, because a dataset is rarely useless in the abstract — it is
useless *for the decision it is being used for*.

Ranked most over-rated first.

## §1 — The Twelve, Ranked

| Rank | Dataset | Why it is believed | What it actually supports |
|---|---|---|---|
| **1** | **Form SHO / Rule 13f-2 monthly manager short positions** | a regulator adopted a rule, so the data sounds like it exists | **Nothing — it does not exist yet.** Exempt until **Jan 2, 2028**; first reports would cover Jan 2028, due within 14 calendar days after month-end `[VERIFIED — SEC exemptive order, FR 2025-22158]`. Any catalogue listing it as available is wrong |
| **2** | **13F "smart money" deltas** | 13F is the most-cited institutional dataset and the delta looks like a signal | A **long-only, partial** snapshot filed within **45 days after quarter-end** `[VERIFIED — 17 CFR 240.13f-1]`, omitting shorts and much of the book, with confidential-treatment positions now absent from EDGAR rather than hidden `[VERIFIED — SEC 13F FAQ]`. At best a slow, incomplete state of the long book |
| **3** | **Daily short-sale volume as a bearish signal** | it is daily, so it looks actionable | A **flow**, **off-exchange (TRF/ADF/ORF) only** and not consolidated, which FINRA states **does not equate** to bi-monthly short interest `[VERIFIED — FINRA dataset documentation]`. Much of it is market-making and hedging, with no directional content |
| **4** | **Fails-to-deliver as naked-shorting evidence** | the file is public, free, and the narrative is compelling | A **settlement** event. The SEC states a fail "may result from either a short or a long sale" and that naked short selling "is not necessarily a violation" `[VERIFIED — SEC Reg SHO investor page]`. Use it only alongside the threshold list |
| **5** | **GEX heatmaps** | they render beautifully and appear to show dealer positioning | An **inference** from open interest under a vendor's sign convention `[COMMON-PRACTICE — vendor product documentation]`. No exchange publishes dealer gamma by strike, and flipping the convention flips the conclusion |
| **6** | **Free-tier "unusual options activity" flags** | they are free, they fire often, and the prints are real | A single-leg print that may be one leg of a spread, a hedge, a roll, or a close. The public tape does not say which; **open-close volume by participant capacity** is what would `[VERIFIED — Cboe DataShop]` |
| **7** | **Social sentiment** | it is free, large, and feels like a crowd read | An aggregated tone measure over a self-selected sample, with no base rate and no demonstrated horizon. See [text-and-language-data.md](text-and-language-data.md) for the four construction failure modes |
| **8** | **COT as a timing tool** | it is official, weekly positioning data from a named regulator | Positioning **as of the preceding Tuesday, published Friday 3:30pm ET**, with the CFTC stating processing takes three days `[VERIFIED — CFTC]`. It is a **crowdedness regime** input, not a timing signal, and it silently drops markets below **20** reportable traders |
| **9** | **Dark-pool print feeds** | they carry the word "dark" and a big notional number | Prints with **no counterparty identity and no direction** in the public tape. A feed that assigns a direction is attributing something the data does not contain |
| **10** | **13F option/exposure inferences** | 13F rows can be combined into a picture of institutional options exposure | A **derivation**, not a disclosure. The form does not report it as such, so the conclusion carries the analyst's assumptions with the form's authority attached |
| **11** | **Alternative-data panels sold with the vendor's backtest as the evidence** | the backtest looks strong and the vendor is professional | A backtest over the **period, universe and metric the seller chose**. Until it is re-run on a period you choose, point-in-time, it is not evidence `[COMMON-PRACTICE — the seller's-holdout problem]` |
| **12** | **The undated 0DTE share-of-volume statistic ("59% of SPX volume")** | it is quoted everywhere and sounds precise | **Nothing, as stated.** The figure sits on a marketing page with **no as-of date** `[ESTIMATED — undated vendor marketing page]`. An undated market-share statistic can be neither right nor wrong, so it cannot be used. Do not put it in a chart, and say why when asked |

## §2 — The Pattern Behind the Twelve

Every entry on this list fails one of four tests. Naming which test an entry fails is a faster way to
evaluate a thirteenth than re-deriving the whole thing.

| The test | The question | Who fails it |
|---|---|---|
| **The existence test** | does the dataset exist today, with an effective date that has passed? | Form SHO / Rule 13f-2 (rank 1) |
| **The measurement test** | is the quantity observed, or inferred? | GEX (5), dark-pool direction (9), 13F option inferences (10) |
| **The comparison test** | is it compared against the right base rate, over a period you chose? | alt-data backtests (11), social sentiment (7), the 0DTE statistic (12) |
| **The decision test** | does it change an action, and by how much in dollars? | 13F deltas (2), daily short-sale volume (3), FTD (4), COT as timing (8), free-tier UOA (6) |

**Two useful consequences.** First, **the existence test is free and takes one API call** — the
Federal Register API. Second, **the decision test disqualifies most of this list by itself**, which is
why the nine-field record makes "what decision does this change?" a required field and not a
nice-to-have.

## §3 — The Honest Version of Each

An over-rated dataset usually has a legitimate, narrower use. That use is worth stating, because it is
the version a good catalogue keeps.

| Over-rated as | Legitimately used as |
|---|---|
| Form SHO for monthly short positions | nothing yet — **check the Federal Register API annually**; the relief expires 2028-01-02 |
| 13F for "smart money" | a slow census of the reported long book, useful for ownership structure and for spotting a manager's style, never for a trade trigger |
| Daily short-sale volume for shorting pressure | an intraday activity read in a name already under analysis, with the TRF-only caveat stated |
| FTD for manipulation | a settlement-stress measure **alongside** the threshold list, and a research artifact on market plumbing |
| GEX for dealer positioning | a **scenario** input, with the sign assumption named and a falsifier attached |
| Free-tier UOA for conviction | a **watchlist generator** — a list of names to investigate, not a list of conclusions |
| Social sentiment for a forecast | a **coincident** interest measure, useful for attention and for nothing else |
| COT for timing | a crowdedness and positioning **regime** input, weekly, with the trader-count check |
| Dark-pool feeds for accumulation | a **volume-location** read — where liquidity traded, not who traded it or which way |
| 13F option inferences | a hypothesis to be checked against another source, labelled as derived |
| Alt-data panels with a vendor backtest | the panel itself, **after** a point-in-time re-run on your period |
| The 0DTE statistic | nothing until someone publishes the same measure **with an as-of date** |

## §4 — Ten Ways to End Up Over-Rating a Dataset

1. **Judging by the chart.** Detection: name the publisher before reading the line.
2. **Judging by the frequency.** Detection: is the lag stated next to the frequency?
3. **Judging by availability.** Detection: is the decision it changes written down? If not, mark it
   nice-to-know.
4. **Judging by price.** Detection: an expensive dataset is not thereby informative; check the free
   substitute first.
5. **Judging by a citation.** Detection: does the citation resolve to the **publisher's own page**?
6. **Judging by a backtest whose period you did not choose.** Detection: whose dates are they?
7. **Judging by name recognition.** Detection: the most-quoted dataset in a category is often the
   most-misread one, which is exactly why it is quoted.
8. **Judging by precision.** Detection: a number with four decimals and no as-of date is a
   precision-shaped claim, not a precise one.
9. **Judging by the number of users.** Detection: popularity is not provenance.
10. **Never revisiting the judgement.** Detection: was this dataset re-checked this quarter? A
    dataset can move — an exemption expires, a lag shortens, a vendor changes a methodology.

## §5 — The Quarterly Re-Audit

This list is a living document. Datasets move, and the direction of movement is usually toward being
*less* over-rated, because a rule takes effect or a lag shortens. Four events would change an entry:

1. **An exemption expiring** — Form SHO and Rule 13f-2 on **2028-01-02**, and Rule 10c-1a on
   **2028-09-28** with dissemination on **2029-03-29** `[VERIFIED — SEC exemptive order, FR 2025-22158]`.
   On those dates, ranks 1 and part of the borrow discussion move from "does not exist" to "exists
   but unproven".
2. **A vendor publishing its methodology and a point-in-time sample** — which would move rank 11 out
   of the inadmissible column and into the testable one.
3. **A venue publishing dealer gamma**, or a documented correction to the sign convention — which
   would move rank 5 from `[COMMON-PRACTICE]` toward `[VERIFIED]`.
4. **A dated version of the 0DTE statistic**, published by the venue with an as-of — which would move
   rank 12 out of the list entirely.

**The re-audit procedure:** re-read the publisher's own page for each entry, check the Federal Register
API for anything under relief, and **write down what changed**. An entry that did not change is
recorded as unchanged, with the read date. An entry that is no longer over-rated is **deleted from the
list** rather than softened, because a list of twelve that has quietly become a list of nine is a
signal that the document is maintained.

**Source:** the SEC exemptive order published at FR 2025-22158 for the Form SHO / Rule 13f-2 and Rule
10c-1a dates; 17 CFR 240.13f-1 and the SEC 13F FAQ for the 13F structure and lag; FINRA's dataset
documentation for the daily short-sale-volume scope and its non-equivalence to short interest; the
SEC's Reg SHO investor page for the meaning of a fail; Cboe DataShop for the participant-capacity
dataset; the CFTC's Commitments of Traders documentation for the as-of, the publication time and the
reportable-trader thresholds; vendor product documentation, tagged `[COMMON-PRACTICE]`, for the GEX
construction; and an undated vendor marketing page, tagged `[ESTIMATED]`, for the 0DTE
share-of-volume claim. No vendor other than Unusual Whales is priced anywhere in this skill; where a
price would be needed, check the vendor's own page.
