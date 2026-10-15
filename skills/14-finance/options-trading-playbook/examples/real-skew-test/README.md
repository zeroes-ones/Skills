# real-skew-test — the skew, measured on real SPY prints, with its uncertainty

A run-once study that replaces the largest `[MODELED]` assumption in this body
of trading research with a **measured** number, at a sample size large enough to
carry a confidence interval. Every option price here is a **real Robinhood
option print**, never a Black-Scholes reconstruction.

- **Pull date: 2026-10-15.** Run date: 2026-10-15.
- **Source:** Robinhood MCP `get_option_instruments` → `get_option_historicals`
  (real daily option OHLC, regular session) + `get_option_quotes` for the live
  cross-check.
- **Underlying: SPY only.**
- **Headline `[MEASURED]`:** the skew is **8.19 vol points per 10% OTM**
  (median of **15** fittable ladders, 95% bootstrap CI **7.00 to 9.01**). The
  assumption under test is **1.5**, so the measured skew is **5.5×** the
  assumption and the CI's lower end is still **4.7×** it. All 15 of 15 slopes
  exceed 1.5.
- **The premium-selling verdict changes shape:** with real prices and n=20
  entries, `E_R` is **+0.0067 gross of costs / −0.0082 after LOW costs**, and
  the 95% CI for the mean R is **−0.184 to +0.171** — it **spans zero**, so at
  this sample the edge is **not measurable**, and the first pass's alarming
  −0.0908 does not survive.
- See [`RESULTS.md`](RESULTS.md) for every table verbatim and
  [`FINDINGS.md`](FINDINGS.md) for the narrative.

---

## 1. The question

The sibling study `../index-options-test/` established that a short-30-DTE
~16Δ index put-spread programme (S2) models at **+2.97% CAGR with 89% of months
positive** — but that it **flips sign at +1.5 vol points of skew** (−0.87%) and
gets worse at +3.0 (−4.03%). The sibling had to *assume* the skew because it
believed historical option quotes were unavailable.

The first pass, `../real-quotes-test/`, pulled them and measured a median skew of
**7.22 vol points per 10% OTM** and a **negative** re-run (−0.0908) — but on
only **4 ladders and 5 entries**. This study re-runs the measurement on a
systematically drawn sample of **20 dates** to see whether those readings hold.

## 2. The verified call path, and the history depth it actually has

1. `get_option_chains(underlying_symbol)` → chain `id` + the **upcoming**
   `expiration_dates` list. Upcoming only; no history.
2. `get_option_instruments(chain_symbol, expiration_dates=<ONE date>,
   strike_price="<S>.0000", state="expired")` → the instrument `id`.
3. `get_option_historicals(instrument_ids=[…], start_time, end_time,
   interval="day")` → real option OHLC. **Option bars carry no volume.**

**History depth, measured by pass one and re-confirmed here:**

| probe | result |
|---|---|
| SPY expired expiry **2017-09-15** and every later one tested | resolves |
| SPY **2017-08-18, 2017-07-21, 2017-06-16, 2017-03-17** | **empty** |
| SPY **2016-01-15, 2015-01-16** | **empty** |

> **Depth floor: the expired-contract catalogue starts at ~2017-09-15 for SPY.**
> **2008 and every pre-2017 crisis are therefore NOT reachable**, and the model
> is **not** substituted for them anywhere in this study.

### Four traps, all of which cost real calls

1. **`expiration_dates` must be a SINGLE date.** A comma-separated list returns
   empty. (Established by pass one; not re-tested here.)
2. **The `strike_price` filter is flaky.** Measured here: of the 122 declared
   rows, **22 (18%) needed more than one call**, and the mean is **1.34 calls
   per contract** (163 calls for 122 rows). It is much worse on strikes that
   genuinely are not listed. Every contract got up to 4 attempts at the exact
   strike and then an ordered neighbour probe; the attempt count is in
   `logs/instrument-ids.tsv` and in the `resolution_attempts` column of the CSV.
   **A single empty result is not evidence of absence.**
3. **The strike grid is not uniformly $1.** Substitutions are flagged
   `substituted=yes` in the CSV; **8 of the 120** ladder contracts needed one
   (e.g. 227 -> 225 on 2017-10-02, where the grid steps by $5 that far out).
4. **THE WINDOW TRAP — new, and it would have corrupted this study.** An
   `end_time` equal to the sample date's own `23:59:59Z` **truncates that
   session's bar**. The first three dates were pulled that way and reported
   the *previous* session's print; extending `end_time` by a few days made the
   sample date's own bar appear (verified on SPY 2018-11-09 P283: 1.80 on
   2018-09-28 with the short window, 1.57 on 2018-10-01 with the corrected one).
   All three dates were re-pulled. **The fix is to set `end_time` at least 2
   sessions AFTER the sample date** (this study used `sample_date + 2d` or
   `+3d`, with `start_time` 6–12 days before). A one-line window error would
   otherwise have put a uniform one-session lag into the entire measurement.

**One more discovery, about the data's shape.** Within any window, sessions
*before* a contract's first trade in that window come back `interpolated: true`
at $0.01. That means a strike showing only interpolated bars had **no trade at
all** in the window — it is genuinely unmeasured, not a flaky query. The
practical consequence is severe and is the main limitation of the whole study:
**out-of-the-money strikes beyond ~6–10% frequently have no print on a given
date at all.**

## 3. The sample, as declared

Declared in `pull_options.py` **before the first price was requested**, then
emitted as `logs/call-plan.tsv`:

- **Underlying:** SPY. QQQ was declared as a secondary and **was not pulled** —
  see §5.
- **Dates:** one sample date per half-year period from the earliest workable
  depth (20 dates), starting 2017-10-02 and ending 2026-04-01, **plus two
  declared stress dates inside the COVID window** (2020-02-24, 2020-03-02).
  2020-03-02 is pass one's own stress date, kept so the two studies share a
  panel.
- **Tenor:** the Friday expiry closest to **37.5 DTE** (centre of the 30–45
  band). Realised DTEs are 35–39, except the declared override below.
- **Ladder:** 4 puts at 3/6/10/15% below spot + 2 calls at 3/6% above — **6
  contracts per date**, 120 for SPY.
- **Risk-free proxy:** **`TVC:US03M`**, the 3-month T-bill yield index, divided
  by 100. `study.py` uses the rate at **t−3 sessions**, the sibling's no-lookahead
  convention.
- **Underlying closes:** the real daily SPY closes carried from the sibling
  `index-options-test` pull (TradingView, re-verified there).

### Two declared deviations from the plan, both reported

| deviation | why | effect |
|---|---|---|
| **2020-03-02 expires 2020-04-17 (46 DTE), not 2020-04-10 (39 DTE)** | 2020-04-10 is **Good Friday** — the market was closed, so that expiry does not exist (all six resolution calls returned empty). The in-band substitute 2020-04-09 (38 DTE) exists but carried a print for only **1 of 6** strikes. 2020-04-17 was the nearest expiry with a full set of prints. | the ladder is complete (4 puts + 2 calls) but sits **outside** the 30–45 DTE band; the DTE is printed in every table that uses it |
| **2 extra `panel=parity` rows** (SPY 2020-05-08 put 254, put 261) | resolved by mistake while hunting the **calls** at the same strikes (the vendor returns put and call together and the response order varies). Kept, because for European options put and call IVs at the same strike must be equal — a free parity check. | excluded from the skew fit; used only in §8 of the run |

### The reductions, reported in full

| stage | what | count |
|---|---|---|
| declared  | SPY contracts to resolve (20 dates × 6) | **120** (+2 parity) |
| resolved as an instrument | a `get_option_instruments` call returned an `id` | **108** |
| returned a usable bar | a **non-interpolated** bar at or before the sample date | **82** |
| passed the $0.10 print floor | the dominant data-quality filter, see §4 | **81** |
| passed the IV band [2%, 150%] | no further loss | **81** |
| **usable date panels** | | **20 of 20** |
| **ladders with ≥2 put prints (the skew-slope sample)** | | **15** |

Of the 40 rows with no usable print, **14 never resolved as an instrument**
(despite 1-4 ordered probes each: 209, 286, 341, 361, 369, 312, 553, 444, 483,
512, 568, 602, 628, 557) and **26 resolved but had no non-interpolated bar** at
or before the sample date. Every one is itemised in `logs/ingest-output.txt`.
Both are reported, not hidden.

### Reductions that were **not** taken, and why

- **QQQ not pulled.** Declared as a secondary, deferred for budget. The budget
  went on the SPY grid instead: the flaky filter cost **1.34 resolution calls
  per contract** (161 calls for the 120 ladder contracts, of which 6 were wasted
  on the Good Friday expiry, plus 2 for the parity rows). Adding QQQ at 6 contracts × 20 dates would have
  cost another ~160 calls and, on pass one's evidence, produced no fittable
  ladder at all.
- **The date grid was not extended** to raise n above 15. Adding hand-picked
  dates would have meant choosing them *after* seeing which regimes print
  densely — i.e. selecting on the outcome. The grid is systematic (one date per
  half-year) and stays that way, and 15 ladders is inside the target band.

## 4. The data-quality rules, and how many contracts each removed

| rule | floor / band | contracts removed |
|---|---|---|
| **no non-interpolated bar** | interpolated bars are never used | **40** |
| **print floor** | `< $0.10` — ten ticks, the smallest print distinguishable from a stale or nominal last trade. Pass one measured $0.01–$0.04 prints implying 7–8% IV, which is not a credible market level. | **1** (a $0.06 call) |
| **IV ceiling / floor** | `> 150%` or `< 2%` | **0** |
| **bar staleness** | bar more than **7 calendar days** before the sample date | **0** (the window makes this redundant, but the rule is enforced) |
| **monotonicity** | IV must not **rise** with moneyness by more than 2.0 vol points between adjacent strikes | **0 dropped** — no violation was detected, on either side |
| *(flags, not exclusions)* | | |
| **flat bar** | `open == high == low == close`: the session's only information is one print | **6** flagged |
| **suspect range** | `low <= $0.01` while `close > $1`: a bad tick inside the bar; only the CLOSE is used | **6** flagged |

Because 6 of 81 contracts are flat bars and 6 more carry an impossible low tick,
and because all 81 values are last-trade prints, **the single biggest threat to
this study is that a print is not a mark.** That is stated again in
[`FINDINGS.md`](FINDINGS.md) §7 and it is not fixable from this source.

**Cross-checks that were run:**

- **Live cross-check (4 contracts).** The historical bar close for 2026-10-13
  equals the vendor's own **official settled close** for that session
  **exactly** for all four (11.35 / 5.34 / 13.50 / 33.72). Payloads in
  `data/raw/live-crosscheck.json`. The vendor's live IVs on the same contracts
  are a fourth independent confirmation of the put skew: on SPY 2027-01-15 the
  750 put prints 16.56% and the 700 put 21.00%, against the 800 call's 11.99%.
- **Put-call parity (2 pairs).** At the same strike and expiry, put IV and call
  IV should be equal. Measured gaps: **+3.20 and +3.35 vol points**. That is a
  real, quantified inconsistency, and it is the American early-exercise premium
  on a deep-ITM put plus print noise — see FINDINGS §7.

## 5. What was measured

| section | result | label |
|---|---|---|
| real IV per contract | 81 contracts, 6.4%–56.0% | [MEASURED] |
| **skew slope** | **median 8.19** vol pts per 10% OTM (n=15, 95% CI 7.00–9.01, range 6.02–11.12) | **[MEASURED]** |
| put-call IV spread | median **5.51** vol pts (n=18, 95% CI 4.72–7.73, range 2.88–14.41) | [MEASURED] |
| model price error | median +$0.01; **+$0.72 too rich at 3–6% OTM, −$0.88 too cheap at 6–12%** | [MODELED] vs [MEASURED] |
| premium re-run | E_R = **+0.0067 gross / −0.0082 net**, p=0.85, CI −0.184…+0.171, **n=20** | [MEASURED] |
| skew by era | median slope 7.52–9.05 across five eras — **stable**; the put-call spread is **not** (4.93 → 9.19 in COVID) | [MEASURED] |

## 6. The call budget, audited

**Total MCP calls: 201.** Auditable from `logs/mcp-call-log.tsv`:

| purpose | calls |
|---|---|
| discovery (`get_option_chains` 1, unfiltered expiry listing 1, flakiness probes 2) | 4 |
| **instrument resolution for the 122 declared rows** (sum of the `attempts` column in `logs/instrument-ids.tsv`: 161 ladder + 2 parity) | **163** |
| live cross-check instrument lookups | 4 |
| `get_option_historicals` batches (20 dates, 3 corrected re-pulls, 3 diagnostics, live) | 29 |
| `get_option_quotes` | 1 |
| **total** | **201** |

That is **1.34 resolution calls per declared row** — the flaky
`strike_price` filter is the dominant cost, and it is 6x the call count a
working exact-strike query would need. Nothing was cut for budget beyond
the QQQ secondary, which is reported in §3.

## 7. Files

| file | what |
|---|---|
| `pull_options.py` | the declared sample, the call plan, and ingest of the raw call transcripts |
| `study.py` | the analysis (stdlib, deterministic, LF) |
| `handcheck.py` | independent re-derivation; shares no code with `study.py` |
| `make-results.py` | wraps the verbatim stdout into `RESULTS.md` |
| `data/real_quotes_skew.csv` | the measured panel, with a `# PROVENANCE:` header |
| `data/underlying/*.csv` | real SPY / VIX / US03M closes, carried |
| `data/raw/live-crosscheck.json` | the live cross-check payloads |
| `logs/call-plan.tsv` | the declared sample, one row per contract |
| `logs/instrument-ids.tsv` | instrument resolution + **attempt counts** |
| `logs/bar-log.tsv` | the historical-bar transcript (raw OHLC) |
| `logs/mcp-call-log.tsv` | the call budget, block by block |
| `logs/study-output.txt`, `run-output.txt`, `plan-output.txt`, `ingest-output.txt` | raw stdout |
| `handcheck-output.txt` | raw stdout of `handcheck.py` |
| `RESULTS.md` | every table verbatim |
| `FINDINGS.md` | the narrative |

## 8. Determinism and verification

- **Determinism:** `study.py` and `handcheck.py` were each run twice and
  `diff`ed; both pairs are **byte-identical**. The bootstrap uses a
  **fixed-seed LCG implemented in `study.py`**, not the Mersenne Twister, so
  the percentile CI is reproducible across Python versions.
- **Hand check:** `handcheck.py` re-derives the IVs, one ladder's slope and one
  spread settlement with its own code — an Abramowitz & Stegun 7.1.26 `erf`
  instead of `math.erf`, a bracket-expansion bisection, and OLS through the
  normal equations. Largest IV gap across the 5 spot-checked contracts:
  **0.0042 vol points**. Slope gap on the 2020-03-02 ladder: **0.0024 vol
  points**. R gap on the settled spread: **0.0000** to 6 dp (the 0.0040 printed
  is study.py's 2-decimal table rounding). Section A of its output prints every
  Black-Scholes intermediate for each price so the number can be reproduced by
  hand.
- **Live cross-check:** 4 of 4 exact matches against the vendor's official
  settled close.

## 9. Limitations — read these before quoting any number

1. **The history does not reach 2008.** The catalogue starts ~2017-09-15. Only
   two crises are measurable (2020 and 2022), and each contributes 2–3 dates.
   "Does skew widen in stress" is answered from **n=5 stress dates**, of which
   **4 have a fittable slope**.
2. **15 fittable ladders, not 20, and 81 usable prints from 120 declared
   contracts.** The dominant exclusion is that **40 contracts had no print at
   all** on or within a week of the sample date. The measured skew is therefore
   the skew of the strikes that *traded*, which is not the same as the skew of
   the surface.
3. **Bars are last-trade prints, not marks.** For illiquid strikes the print can
   be far from fair value, and the call side is systematically the worse
   offender — see FINDINGS §5. No volume, bid, ask or open interest is available
   to tell a print from a quote.
4. **There is no true at-the-money measurement.** Every put ladder starts at 3%
   OTM, so any d=0 figure is an extrapolation. The slope is unaffected; the
   *level* is.
5. **European Black-Scholes on American options.** SPY options are American and
   physically settled. The put-call parity check (§4 of this file) quantifies
   what that costs: +3.2 and +3.4 vol points on two deep-ITM puts.
6. **One ladder sits at 46 DTE**, outside the declared 30–45 band, because of
   Good Friday (§3).
7. **The premium re-run is 20 entries, not 306 months.** Its confidence interval
   spans zero, so it does **not** establish that the edge is positive, negative
   or zero — it establishes that this sample cannot tell, and that the two
   earlier point estimates are both outside what 20 measured entries support.
8. **QQQ was not pulled**, so nothing here is cross-index.
9. **`.skills` no: no `SKILL.md` was modified.** This study writes only inside
   its own directory.

## 10. How to re-run

```bash
cd skills/14-finance/options-trading-playbook/examples/real-skew-test
export PYTHONIOENCODING=utf-8

py -3 pull_options.py --plan      # re-declare the sample -> logs/call-plan.tsv
# issue the MCP calls listed there, retrying empties, and record the transcripts
py -3 pull_options.py --ingest    # logs/*.tsv -> data/real_quotes_skew.csv
py -3 study.py                    # the analysis; writes logs/study-output.txt
py -3 handcheck.py                # independent re-derivation
py -3 make-results.py             # -> RESULTS.md
```

An independent re-pull will not reproduce the *attempt counts* (the flaky filter
is nondeterministic) but will reproduce every analysed price, provided the
window rule in §2 is followed.
