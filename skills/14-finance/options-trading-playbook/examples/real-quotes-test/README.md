# real-quotes-test — REAL option prices, the measured skew, and how wrong the model was

A run-once study that replaces the largest `[MODELED]` assumption in this body
of trading research with **measured** numbers. Every option price here is a
**real Robinhood option bar**, not a Black-Scholes reconstruction.

- **Pull date: 2026-10-15.** Run date: 2026-10-15.
- **Source:** Robinhood MCP `get_option_instruments` → `get_option_historicals`
  (real daily option OHLC, regular session).
- **Headline:** the real skew is **7.2 vol points per 10% OTM** (median,
  range 4.87–10.87) and the real put-call IV spread is **6.05 vol points**
  (median). The old model assumed **1.5**. Re-run with the measured skew, the
  premium-selling programme's mean R **flips negative (−0.0908)**.
- See [`RESULTS.md`](RESULTS.md) for every table verbatim and
  [`FINDINGS.md`](FINDINGS.md) for the narrative.

---

## 1. The question

The sibling study `../index-options-test/` established that a short-30-DTE
~16Δ index put-spread programme (S2) models at **+2.97% CAGR with 89% of months
positive** — but that it **flips sign at +1.5 vol points of skew** (−0.87%) and
gets worse at +3.0 (−4.03%). The sibling had to *assume* the skew because it
believed historical option quotes were unavailable.

They are available. This study pulls them, measures the skew, and re-runs the
programme on measured input.

## 2. The verified call path, and the history depth it actually has

The working path, confirmed end to end:

1. `get_option_chains(underlying_symbol)` → chain `id` + the **upcoming**
   `expiration_dates` list. Upcoming expiries only; no history.
2. `get_option_instruments(chain_symbol, expiration_dates=<ONE date>,
   type=call|put, strike_price="<S>.0000", state="expired")` → the instrument
   `id`. **`expiration_dates` must be a SINGLE date** — passing a
   comma-separated list returns an empty result (verified twice).
3. `get_option_historicals(instrument_ids=[…], start_time, end_time,
   interval="day")` → real option OHLC. **Option bars carry no volume.**

**History depth, measured (this is the gating fact for the whole study):**

| probe | result |
|---|---|
| SPY expired expiry **2017-09-15** | resolves |
| SPY 2017-11-17, 2017-12-15, 2018-01-19, 2018-02-02, 2018-02-16 | resolve |
| SPY **2017-08-18, 2017-07-21, 2017-06-16, 2017-03-17** | **empty** |
| SPY **2016-01-15, 2015-01-16** | **empty** |
| QQQ, IWM at 2018-01-19 and 2018-02-09 | resolve |

> **Depth floor: the expired-contract catalogue starts at ~2017-09-15 for SPY.**
> Everything before that is absent. **2008 and every pre-2017 crisis are
> therefore NOT reachable**, and no question about skew in 2008 can be answered
> from this data. (Robinhood's options product began in early 2017, which is
> consistent with this floor.)

I did **not** separately probe the QQQ/IWM floor; both resolve at 2018-01-19 and
2018-02-09 and that is all I can assert.

**Two traps found the hard way, both recorded here so a re-runner does not
repeat them:**

1. **The strike filter is flaky.** A `strike_price` query for a contract that
   *provably exists* — 2018-02-09 P260, which appears in that expiry's own
   paginated listing — returned empty on the first attempt and non-empty on
   retry. Roughly 45% of filtered strike queries returned empty on the first
   attempt. Every contract in the declared plan was therefore retried (up to 6
   attempts); the attempt count is in `logs/instrument-ids.tsv` and in the
   `resolution_attempts` column of the CSV. A single empty result is **not**
   evidence of absence.
2. **The strike grid is not uniformly $1.** For 2018-02-09 the grid steps by
   **$2.50** below 245, so the rounded target 242 does not exist. Substitutions
   are recorded explicitly in `STRIKE_SUBSTITUTIONS` in `pull_options.py` and
   flagged with `substituted=yes` in the CSV.

**Per-contract bar history is short.** The first non-interpolated bar observed:

| contract | first real bar |
|---|---|
| SPY 2018-02-09 P261 | 2017-12-28 |
| SPY 2020-02-07 P315 | 2019-12-26 |
| SPY 2020-04-17 P300 | on or before 2020-02-25 (window start) |

So the history window varies by contract; it is **not** a fixed rule and I do
not claim one. Many contracts have **no trade at all** in a wide window and
return only `interpolated: true` bars at 0.01 — those are dropped, never used.

## 3. The sample, as declared

Declared in `pull_options.py` **before the first price was requested**, then
emitted as `logs/call-plan.tsv`:

- **Underlyings:** SPY, QQQ, IWM.
- **Dates:** first business day of Q1 for each year from the depth floor, plus
  two declared stress dates (2020-03-02 COVID, 2022-06-01 the 2022 bear).
- **Tenor:** the Friday expiry closest to **37 DTE** (centre of the 30–45 band).
  Weeklies are used because monthly expiries cannot reach the band from a
  first-business-day-of-Q1 start (they jump 14 → 49 DTE).
- **Ladder:** 5 puts at 3/6/10/15/20% OTM and 3 calls at 3/6/10% OTM.
- **Risk-free proxy:** **`TVC:US03M`**, the 3-month T-bill yield index, divided
  by 100. `study.py` uses the rate at **t−3 sessions** to match the sibling
  study's no-lookahead convention.
- **Underlying closes:** the real daily closes carried from the sibling
  `index-options-test` pull (same TradingView source, re-verified there against
  a fresh pull). Copied into `data/underlying/`.

### The reduction, reported in full

The full three-underlying × eleven-date × eight-strike grid is **~288
contracts**, and each (underlying, date, strike) costs one resolution call
because `strike_price` is an exact match. That was not affordable, so the
sample was **reduced twice**, and the reduction is reported rather than hidden:

| stage | SPY dates | QQQ dates | IWM dates | contracts |
|---|---|---|---|---|
| declared | 10 | 6 | 6 | 152 |
| **pulled** | 4 | 1 | 1 | **56** |

**What was actually pulled** (the CSV has 56 declared contracts):

| underlying | dates pulled | ladder complete? |
|---|---|---|
| SPY | 2018-01-02, 2020-01-02, 2020-03-02, 2022-06-01 | **2020-03-02 is complete (5 puts + 3 calls)**; 2022-06-01 is 3 puts + 2 calls; 2020-01-02 is 3 puts + 2 calls; 2018-01-02 is 2 puts + 1 call |
| QQQ | 2018-01-02 | 1 put + 1 call |
| IWM | 2018-01-02 | 1 put |

The 2020-03-02 stress ladder was pulled on the **2020-04-17** expiry (46 DTE,
because 2020-04-10 could not be resolved at all), which is **outside** the
30–45 band; the actual DTE is printed in every table that uses it.

**Of 56 declared contracts, 27 produced a usable real bar** and are analysed.
The other 29 are itemised with their reason by `pull_options.py --ingest`:
**11** never resolved as instruments despite 2–6 attempts, and **18** resolved as
instruments but had **no non-interpolated bar** at or before the sample date
(12 of those 18 are QQQ/IWM legs).

## 4. What was measured

| section | result | label |
|---|---|---|
| real IV per contract | 27 contracts, 7.48%–49.18% | [MEASURED] |
| skew slope | median **7.22** vol pts per 10% OTM (4.87–10.87, n=4) | [MEASURED] |
| put-call IV spread | median **6.05** vol pts (3.61–14.19, n=4) | [MEASURED] |
| model price error | median −$0.14; **+$0.53 too rich at 3–6% OTM, −$1.52 too cheap beyond 12%** | [MODELED] vs [MEASURED] |
| term structure | 2020-03-02 **inverted**: P300 40.67% at 18 DTE → 33.44% at 46 DTE | [MEASURED] |
| premium re-run | E_R = **−0.0908**, p = 0.80, n = 5 | [MEASURED] |

## 5. What the numbers say

**The assumption was far too small.** The sibling's 1.5 vol points is a *level*
offset on the sold leg; the measured comparable is the put-call IV spread, whose
median is **6.05** vol points — **four times** the assumption — and the measured
*slope* is **7.22 vol points per 10% OTM**, five times it. On the one complete
ladder (SPY 2020-03-02) the 16-delta-ish short put is credited at **~35.9%**,
not at the 27.56% the VIX model gives.

**And the programme flips.** Re-priced on the measured per-strike IV, over the
5 measured entries, the short-put-spread book returns **E_R = −0.0908** with
p = 0.80 — a **negative** sign, agreeing with the direction of the sibling's
own flip, and disagreeing with the sibling's headline +2.97%. The single
largest contributor is the COVID entry, which finished in the money and lost
**−0.83R**. This is **5 entries, not 306 months** — it is a partial measured
window and is **not** a CAGR.

**The model is wrong in a structured way, not randomly.** A flat vol prices
near-money options ~$0.53 too high and the far wings ~$1.52 too low. That is
exactly the shape a missing skew produces, and it means the old study
systematically **under-credited** the wing it bought and (at 3–6%) over-credited
the leg it sold.

## 6. How to re-run

```bash
cd skills/14-finance/options-trading-playbook/examples/real-quotes-test
export PYTHONIOENCODING=utf-8

py -3 pull_options.py --plan      # re-declare the sample -> logs/call-plan.tsv
# (issue the MCP calls listed there, retrying empties, and record the two logs)
py -3 pull_options.py --ingest    # logs/*.tsv -> data/real_quotes_ladder.csv
py -3 study.py                    # the analysis; writes logs/study-output.txt
py -3 handcheck.py                 # independent re-derivation; writes handcheck-output.txt
```

## 7. Determinism and verification

- **Determinism:** `study.py` and `handcheck.py` were each run twice and
  `diff`ed; both pairs are **byte-identical**. The analysis depends only on the
  CSVs, so the snapshot is reproducible.
- **Hand check:** `handcheck.py` re-derives the IVs and skew slopes with its own
  code — a different `erf` (A&S 7.1.26 series vs `math.erf`), bracket-expansion
  bisection, and OLS through the normal equations — and does **not** import
  `study.py`. Largest absolute gap across all 27 contracts: **0.1195 vol
  points**; skew slopes agree to **0.016 vol points**. The residual gap is
  *intended*: `study.py` discounts at the t−3 rate, `handcheck.py` at the sample
  date's own rate. Section A of `handcheck-output.txt` prints every
  Black-Scholes intermediate for one real price so the number can be reproduced
  by hand.
- **Live cross-check:** three still-live contracts were compared against
  `get_option_quotes`. For **all three**, the historical bar close for
  2026-10-13 equals the official settled close for that session **exactly**
  (175.90 / 59.60 / 21.44). Payloads in `data/raw/live-crosscheck.json`. The
  live IVs are a fourth independent confirmation of a put skew: the 600 put
  (22.4% OTM) prints 24.56% IV against the 700 call's 19.07%.
- **Total MCP calls: ~164.** The per-contract call log is
  `logs/instrument-ids.tsv` (with attempt counts) and the declared plan is
  `logs/call-plan.tsv`.

## 8. Limitations — read these before quoting any number

1. **The history does not reach 2008.** The catalogue starts ~2017-09-15. Only
   one crisis (2020) is measurable. The "does skew widen in stress" question is
   answered from **n=1** stress date.
2. **4 usable date-underlying panels, 27 prices, and only ONE complete ladder.**
   The skew slope rests on 4 observations (n_puts = 2, 3, 7, 3).
3. **The sample was cut to fit a call budget**, not to be representative. QQQ
   and IWM are single-date cross-checks, not panels.
4. **Bars are last-trade prints, not marks.** For illiquid strikes the print can
   be far from fair value: the SPY 2018-01-02 285 call printed **$0.02** where a
   flat 10.47% vol gives $0.17 and a 15% vol gives ~$1. A $0.02 print implies a
   7.48% IV, which is not a credible market level. **Contracts priced at the
   $0.01–0.04 minimum tick should be treated as unmeasured**, and the
   wide-percentage errors in section 3 of `RESULTS.md` are dominated by them.
5. **No volume, no bid/ask, no open interest** in the historical bars, so
   liquidity cannot be assessed per contract from this source.
6. **The re-run is 5 entries.** p = 0.80, E_R = −0.0908. No CAGR, no
   significance, no confidence interval worth quoting.
7. **European Black-Scholes on American options.** SPY/QQQ/IWM options are
   American and physically settled; they are priced here as European, as the
   sibling did.
8. **`study.py` uses the t−3 rate** (sibling convention). `handcheck.py` uses
   the sample-date rate. The 0.12 vol-point gap in section B is that difference.
9. **Not all raw MCP JSON is on disk.** The analysed values are persisted at
   full precision as transcripts; see `data/raw/README.txt` for exactly what is
   and is not kept.

## 9. Files

| file | what |
|---|---|
| `pull_options.py` | declared sample, call plan, and ingest of the call transcripts |
| `study.py` | the analysis (stdlib, deterministic, LF) |
| `handcheck.py` | independent re-derivation; does not import `study.py` |
| `data/real_quotes_ladder.csv` | the measured panel, `# PROVENANCE:` header |
| `data/underlying/*.csv` | real underlying / VIX / US03M closes, carried |
| `data/raw/` | live cross-check payloads + a note on what raw data is kept |
| `logs/call-plan.tsv` | the declared sample, one row per contract |
| `logs/instrument-ids.tsv` | instrument resolution transcript + attempt counts |
| `logs/bar-log.tsv` | historical-bar transcript (raw OHLC) |
| `logs/study-output.txt`, `run-output.txt` | raw stdout of `study.py` |
| `handcheck-output.txt` | raw stdout of `handcheck.py` |
| `RESULTS.md` | every table verbatim |
| `FINDINGS.md` | the narrative |
