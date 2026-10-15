# Text and Language Data

Text is the cheapest dataset and the most misused, because **it arrives with a timestamp that looks
precise and a meaning that is not precise at all.** This file covers what free text sources exist,
what they can support, and the four ways a text-derived signal quietly becomes a look-ahead artefact.

## §1 — EDGAR Full-Text Search and the `data.sec.gov` APIs

**Source:** SEC EDGAR. `[VERIFIED — SEC Accessing EDGAR Data]`.

| Facility | What it gives you | Cost |
|---|---|---|
| **EDGAR full-text search** | search across filing text, including forms that predate structured data | free |
| **`data.sec.gov` APIs** | structured submissions, company facts and financial-statement data | free |
| **Daily index files** | every filing accepted that day, by form type | free |
| **Full and quarterly index files** | the rebuildable indexes; **rebuilt weekly, early Saturday** | free |
| **`company_tickers.json`-style ticker↔CIK mappings** | the join key | free, but **explicitly "not guaranteed for accuracy"** and cumulative — one CIK can map to several historical names `[VERIFIED — SEC]` |

### 1.1 — The operational limits that change what you can build

| Property | Value | Consequence |
|---|---|---|
| Acceptance window | **6:00am – 10:00pm ET** | a filing can arrive after your batch job ran |
| Late-filing dissemination | after **5:30pm ET** (**10:00pm ET** for Forms 3/4/5) disseminates the **next business day** | the filing date in the header is not always the date you could have seen it |
| Rate limit | **10 requests/second** | a naive crawler gets throttled, and a throttled crawler that swallows errors looks like an empty result |
| Required header | a declared **User-Agent** | without it, requests are refused |
| Corrections and deletions | **not backfilled** into prior daily or feed indexes | **your EDGAR snapshot is permanently and silently incomplete** |

**The design consequence, in one line:** if you want a point-in-time text corpus, **you must build it
by crawling forward in time and keeping your own snapshots.** EDGAR is the source; it is not the
archive of what you saw.

## §2 — Filing Text as Data

Filing text is the highest-quality free text corpus in finance, for one reason: **it is timestamped by
a regulator, and its authors have legal exposure.** That is a rare combination.

### 2.1 — What filing text supports

1. **Risk-factor language change detection** — comparing year-over-year language in the same
   company's filings, using a point-in-time corpus of what you actually had.
2. **Disclosure-event detection** — a new 8-K item, a new 13D, a new insider cluster.
3. **Language-complexity and obfuscation measures** — reading-level and sentence-length measures on
   the MD&A section.
4. **Named-entity extraction** — counterparties, subsidiaries and jurisdictions.

### 2.2 — What filing text does not support

| Claim | Why not |
|---|---|
| "The tone improved, so the quarter was good" | tone is a measure of the document, not of the business |
| "Risk factors increased, so risk increased" | risk-factor sections grow from legal caution as much as from risk |
| "The filing was late, so something is wrong" | EDGAR's dissemination timing has mechanical causes `[VERIFIED — SEC Accessing EDGAR Data]` |

### 2.3 — The point-in-time rule for filing text

**A backtest on filing text must use the filing as it existed on the decision date.** If you re-crawl
the archive today, you get the corrected version, and EDGAR does not backfill corrections into its
prior indexes `[VERIFIED — SEC Accessing EDGAR Data]`. The difference between the two versions is
exactly the information your backtest is not allowed to have.

## §3 — News and Its Timestamp Problems

| Problem | Detail | Detection |
|---|---|---|
| **First-report timestamp vs wire timestamp** | the same story has several times | pick one source and state it |
| **Backfill and silent correction** | vendors rewrite headlines and body text | capture the body at read time, not the headline at query time |
| **Duplicate syndication** | one wire story appears in many feeds | de-duplicate by normalised first sentence before counting |
| **Aggregator lag** | your feed is not the fastest one | measure it: fetch the same story from two sources and compare |
| **Retraction** | a story is withdrawn and the withdrawal is not surfaced | capture the story, not the link, or the link will change |

**The rule:** for any news-derived feature, **record the timestamp you observed it, not the timestamp
the source claims.** The claimed timestamp is a claim about the world; your read timestamp is a fact
about your data.

## §4 — Sentiment Construction: The Four Failure Modes

1. **Domain shift.** A model trained on general text underperforms on financial text, because
   "liability", "yield" and "exposure" mean something different here. Detection: check the training
   corpus, not the accuracy number.
2. **The negation and hedge problem.** "Not unprofitable" and "could be catastrophic" are hard; a
   bag-of-words model reads both wrong. Detection: hand-check twenty sentences containing a negation.
3. **Score aggregation hides the distribution.** A mean sentiment of +0.2 can be one +1 and four −0.2s.
   Detection: plot the distribution, not the mean.
4. **Target leakage through the corpus.** A model trained on text published after the decision date
   has seen the answer. Detection: check the training cutoff against the backtest period.

## §5 — The One Text Dataset That Is Underused

**EDGAR full-text search combined with your own forward-crawled corpus.** It is free, it is
regulator-timestamped, it covers a period no vendor's panel covers, and the only cost is the
discipline of crawling forward instead of re-reading history. Everything else in this file is about
reading that corpus without lying to yourself.

## §6 — Ranked: Text Datasets for a Trading Decision

| Rank | Dataset | Kind | Cost | Verdict |
|---|---|---|---|---|
| 1 | **Your own forward-crawled EDGAR corpus** | STATE (point-in-time) | free | the only text dataset that survives a backtest audit |
| 2 | **EDGAR full-text search** | STATE | free | the discovery layer for the corpus |
| 3 | **`data.sec.gov` structured facts** | STATE | free | numbers rather than words, which removes a class of error |
| 4 | **Daily and full index files** | STATE | free | the schedule; remember the weekly Saturday rebuild |
| 5 | **A named news wire with a stated timestamp convention** | STATE | paid | useful, if the timestamp convention is stated in the record |
| 6 | **A vendor sentiment score** | SIGNAL | paid | rank low until the four failure modes in §4 are addressed |
| 7 | **Social text** | SIGNAL | free or paid | see the over-rated list; a crowd's tone is not a forecast |

## §7 — Ten Failure Modes in Text Data

1. **Re-crawling the archive and backtesting on corrected filings.** Detection: EDGAR does not
   backfill corrections into prior indexes `[VERIFIED — SEC Accessing EDGAR Data]`; was the corpus
   forward-crawled?
2. **Using the claimed publication timestamp instead of the read timestamp.** Detection: does the
   record have a `read_timestamp`?
3. **Counting a syndicated story many times.** Detection: de-duplicate by normalised first sentence.
4. **Treating a late filing as a signal.** Detection: check EDGAR's dissemination rules.
5. **A sentiment model trained on the backtest period.** Detection: training cutoff versus backtest
   period.
6. **A general-domain sentiment model applied to financial text.** Detection: read the training
   corpus description.
7. **A mean sentiment with no distribution.** Detection: plot the distribution.
8. **A ticker↔CIK join that silently merges entities.** Detection: the mapping files are cumulative
   and "not guaranteed for accuracy" `[VERIFIED — SEC]`; check for multi-name CIKs.
9. **A crawler that treats a throttled or refused request as an absence of filings.** Detection: check
   status codes; the rate limit is **10 requests/second** and a User-Agent is required.
10. **Text features whose values change when you re-read them.** Detection: snapshot the body text,
    not the URL.

**Source:** the SEC's "Accessing EDGAR Data" page for the acceptance window, late-filing
dissemination, the 10-requests-per-second rate limit, the User-Agent requirement, the weekly
Saturday index rebuild and the non-backfilling of corrections; the SEC's own statement that the
ticker↔CIK mapping files are not guaranteed for accuracy and are cumulative; and EDGAR full-text
search and the `data.sec.gov` APIs as the free discovery and structured-data layers. Sentiment
construction failure modes are general NLP-engineering facts and are asserted as such, with no vendor
named or priced.
