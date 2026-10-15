# frontier-test — what "profitable every time" actually costs

## The question

> "Be profitable every time — in every market condition, at
> daily / weekly / biweekly / monthly / quarterly / half-yearly / yearly."

## The provable, constructive answer

Positivity is bought with return, and the exchange rate is measurable. Take a
book of risky sleeves and mix it with cash at exposure `λ`:

```
r(λ)[j] = λ · r_risky[j] + (1 − λ) · r_cash[j]
```

At `λ = 1` you hold the book and get the book's positivity. At `λ = 0` the return
*is* the cash rate, term by term, and every month, quarter and year is positive
because cash does not fall. In between, positivity rises as return falls.

This study measures that curve on real data, at all seven bucket widths, and
reports **where it ends** — the largest `λ` at which 100 % of periods are still
positive, and the return that `λ` actually earns.

The measured answer for the primary book over 2005-09-02 … 2026-10-14:

| horizon | largest λ with 100 % positive | CAGR there | cash CAGR | excess |
|---|---|---|---|---|
| year | 0.008 | 1.81 % | 1.78 % | **+0.03 %/yr** |
| half-year | 0.004 | 1.79 % | 1.78 % | +0.01 %/yr |
| quarter | 0.001 | 1.78 % | 1.78 % | +0.00 %/yr |
| month | 0.000 | 1.78 % | 1.78 % | +0.00 %/yr |
| day / week / 2 weeks | *n/a* | — | — | not even cash clears it |

**The frontier ends at essentially zero exposure.** To be positive in every month
of this 20-year window you must hold no risky exposure at all. To be positive in
every year you may hold 0.8 % of the book, which earns 3 basis points a year over
cash. That is not an opinion about the book; it is the arithmetic of the mixing
line, and section 4 of `RESULTS.md` shows it at every `λ`.

---

## Files

| file | what it is |
|---|---|
| `pull_ohlcv.py` | persists the MCP `get_ohlcv` payloads on disk as `data/*.csv` with provenance headers. No network of its own. |
| `reuse_sibling_data.py` | extends `SPY` and `VIX` backwards from a sibling study's already-pulled file, **after verifying the overlap row-for-row** against this study's own pull. |
| `study.py` | the study: sleeves, book, cash series, `λ` grid, frontier, costs, artefacts. Deterministic, stdlib-only, LF output. |
| `handcheck.py` | an **independent** re-derivation from `data/*.csv`. Does not import `study.py`, does not use the sibling engine. Own reader, own SMA, own alignment, own simulator, own cash accrual, own bucket keys, own CAGR. |
| `make-results.py` | renders `RESULTS.md` from `out/*.csv` and the captured stdout. Formats; never calculates. |
| `data/*.csv` | the price/level series, each behind its own `# PROVENANCE:` block. |
| `out/*.csv` | every table the study produces (59 files). |
| `RESULTS.md` | every table and figure, pasted from the real run. |
| `FINDINGS.md` | the honest narrative: what the frontier shows, where it ends, what it costs, and what remains untested. |
| `run-output.txt` | complete stdout of `study.py`. |
| `handcheck-output.txt` | complete stdout of `handcheck.py`. |
| `pull-output.txt`, `reuse-output.txt`, `reuse-vix-output.txt` | complete stdout of the data steps. |

---

## Data

**Source.** TradingView MCP tool `mcp__tradingview__mcp-tv-get-ohlcv`, interval
`1D`, `format="columns"`, paginated with `date_to=next_date_to` until
`has_more=false`. **Pull date 2026-10-14.** Series are split-adjusted, regular
session only, and **price-only — no dividends or distributions**. Every number
here is therefore a price return, not a total return; that deflates the bond and
high-yield sleeves in particular, and it deflates cash-as-a-price entirely (see
the proxy limitations below).

**What was asked for, and what exists.** Report of the actual probe:

| requested | result |
|---|---|
| `AMEX:SHY` | **INVALID SYMBOL** — dropped |
| `TVC:IRX` | **INVALID SYMBOL** — dropped |
| `AMEX:PDBC` | **INVALID SYMBOL** — dropped |
| `AMEX:SHV` | **INVALID SYMBOL** — dropped |
| `AMEX:DBC` | exists — used (commodities) |
| `AMEX:VNQ` | exists — used (REITs) |
| `NASDAQ:IEF` | exists — used (7–10y Treasuries) |
| `AMEX:EFA` | exists — used (developed ex-US) |
| `AMEX:HYG` | exists — used (credit) |
| `AMEX:BIL` | exists — used as a **cross-check**, not as the cash series |
| `TVC:US03M` | exists — used as the **cash proxy** (3-month T-bill yield index) |
| `AMEX:SPY`, `NASDAQ:QQQ`, `NASDAQ:TLT`, `AMEX:GLD`, `AMEX:EEM`, `AMEX:IWM`, `TVC:VIX` | exist — used |

The four cash-proxy candidates the brief named (`SHY`, `IRX`) and one commodity
alternative (`PDBC`) do not resolve. Nothing was silently substituted: the
substitutes are `TVC:US03M` (cash) and `AMEX:DBC` (commodities), and both are
named wherever they are used.

**Series inventory** (rows / first / last, read back from the provenance blocks):

| series | source | rows | first | last |
|---|---|---|---|---|
| SPY | AMEX:SPY | 8485 | 1993-01-29 | 2026-10-14 |
| QQQ | NASDAQ:QQQ | 6943 | 1999-03-10 | 2026-10-14 |
| IWM | AMEX:IWM | 6635 | 2000-05-26 | 2026-10-14 |
| TLT | NASDAQ:TLT | 6094 | 2002-07-26 | 2026-10-14 |
| IEF | NASDAQ:IEF | 6094 | 2002-07-26 | 2026-10-14 |
| EFA | AMEX:EFA | 6326 | 2001-08-17 | 2026-10-14 |
| EEM | AMEX:EEM | 5915 | 2003-04-11 | 2026-10-14 |
| GLD | AMEX:GLD | 5510 | 2004-11-18 | 2026-10-14 |
| VNQ | AMEX:VNQ | 5546 | 2004-09-29 | 2026-10-14 |
| DBC | AMEX:DBC | 5206 | 2006-02-03 | 2026-10-14 |
| HYG | AMEX:HYG | 4910 | 2007-04-11 | 2026-10-14 |
| BIL | AMEX:BIL | 4876 | 2007-05-30 | 2026-10-14 |
| VIX | TVC:VIX | 9283 | 1990-01-03 | 2026-10-14 |
| US03M | TVC:US03M | 18197 | 1954-01-04 | 2026-10-14 |

**How the two long series were extended.** A single `get_ohlcv` response caps at
8000 bars, and the host only persists a tool result to disk when it is long
enough to be truncated. SPY from 1993 is 8485 bars and VIX from 1990 is 9283, so
the oldest page of each came back inline and was never written to a file.
`reuse_sibling_data.py` therefore carries those oldest rows from
`../regime-study/data/SPY_1d.csv` and `../weather-test/data/VIX_1d.csv` — same
tool, same pull date — **only after proving the overlap is identical**:

* SPY: 8000 overlapping rows, **7999 byte-identical**, the single difference
  being the *volume of the final bar* (2026-10-14), which the data source itself
  flags as still forming.
* VIX: 8000 overlapping rows, **all 8000 identical**.
* Independently, this study's own fresh pulls of TLT, GLD, QQQ and EEM were
  compared against the sibling files: each was identical except the final bar's
  volume. Four symbols, four checks, one systematic and disclosed difference.

---

## The cash proxy, and its limitations

`TVC:US03M` is the **3-month US Treasury bill yield index**, in percent per
annum. The daily accrual used here is

```
r_cash[j] = (yield at the close of book date j−1 / 100) / 252
```

using the *previous* book date's observation, the same no-lookahead convention
the sleeves use for their position, with the last known rate carried forward
across missing prints.

**A T-bill yield index is not a tradable fund, and it is an upper bound.** In
particular it:

1. **ignores management fees.** A real 1–3 month T-bill ETF charges roughly
   10–15 bp a year. `study.py` accepts `CASH_FEE_BPS` so the sensitivity can be
   shown; the headline run uses 0 bp, i.e. the optimistic case.
2. **ignores the bid/offer and the roll** of an actual T-bill portfolio, and the
   difference between 3-month paper and the daily reinvestment the formula
   assumes.
3. **has no volume and is not a price.** It is a quotation series; nothing may be
   compounded as a price return from it.
4. **credits the full quoted yield every business day.** A fund's NAV accrues
   over calendar days with a different convention.
5. **prints zero and negative.** Measured: in R4's window, 21 of 5311 days have a
   non-positive cash accrual — 8 days at exactly 0.00 %, and 11 days at a
   *negative* yield (2015-09-18 … 2020-03-30, down to −0.0406 %). A cash-only
   plan therefore fails "profitable every day" **by itself**, before any risky
   asset is added.

**Why not a price series?** Because a T-bill fund distributes its yield and its
price goes nowhere. Measured cross-check: `AMEX:BIL` price-only returns **−0.00 %
CAGR** over 2007-05-30 … 2026-10-14 with only **42.5 %** of days up. Using BIL's
price as "cash" would have reported cash as a zero-return coin flip. That is why
the series is the yield index, and the limitation above is why the yield index is
an *upper* bound rather than a fact about a portfolio.

---

## The books, and the window each covers

The sleeve rule and the simulator are the weather-test's (`../weather-test`),
reproduced with its conventions intact. Sleeve = long iff close > SMA(200),
position changed only on a **book** date, equal weights, monthly rebalance, cost
charged against the return. **This study's simulator exactly reproduces that
study's published four-sleeve book**: CAGR gap 6×10⁻⁸, max-drawdown gap
1.6×10⁻⁷, identical window and identical count of losing years.

| book | sleeves | window | days | complete Y / Q / M |
|---|---|---|---|---|
| **R4** (primary) | SPY, TLT, GLD, EEM trend @ 25 % | 2005-09-02 … 2026-10-14 | 5311 | 20 / 84 / 252 |
| R9 | R4 + IWM, DBC, VNQ, IEF, EFA @ 1/9 | 2006-11-16 … 2026-10-14 | 5007 | 19 / 79 / 238 |
| R10 | R9 + HYG @ 10 % | 2008-01-24 … 2026-10-14 | 4711 | 17 / 74 / 224 |
| **R2L** (long) | SPY, QQQ trend @ 50 % | 1999-12-21 … 2026-10-14 | 6744 | 26 / 107 / 321 |
| **R1L** (longest) | SPY trend only | 1993-11-11 … 2026-10-14 | 8286 | 32 / 131 / 394 |

**Which years each book covers.** R4 covers complete years 2006–2025. R9 covers
2007–2025. R10 covers 2009–2025. **R2L covers 2000–2025 and therefore contains
the whole dot-com bear (2000, 2001, 2002 — three losing years for that book).**
R1L covers 1994–2025, the longest window the data allows, and it too contains
2000–2002. Nothing here covers 1993's own partial year, and the risky books
before 1999 are single-sleeve by construction because no second instrument exists
that far back.

The five-sleeve book the brief warns about (the weather-test's `BOOK_5`, with a
long-volatility sleeve) is **not** used: this study starts from the working
four-sleeve book and *adds* sleeves only where real data exists, which is what
R9 and R10 are. That failure is not reproduced here, and it is not hidden either
— see `../weather-test/FINDINGS.md`.

---

## Verification

```bash
export PYTHONIOENCODING=utf-8

# determinism: two runs, byte-identical stdout and byte-identical CSVs
py -3 study.py > run-output.txt 2>&1
cp -r out /tmp/out_run1
py -3 study.py > /tmp/run2.txt 2>&1
diff run-output.txt /tmp/run2.txt     # 0 lines
diff -r /tmp/out_run1 out             # 0 lines

# independent re-derivation from data/*.csv
py -3 handcheck.py                    # HANDCHECK PASSED

# rebuild the documents
py -3 make-results.py
```

**Results of those checks, as run:**

* **Determinism** — two consecutive runs produced 0 differing lines of stdout and
  0 differing bytes across all 59 `out/*.csv`. There is no clock, no RNG and no
  set iteration in `study.py`.
* **Independent re-derivation** — `HANDCHECK PASSED`. Max absolute gap over both
  frontier tables (21 λ × 7 buckets, two books): **4.932×10⁻⁷**, which is the
  6-decimal rounding of the written CSVs, not a disagreement. The cash identity
  (`r(0)` CAGR vs an independently computed cash CAGR) held to **0.000×10⁰
  exactly**. The endpoint bisection agreed **exactly** at λ = 0.008.
* **By hand** — 2015 at λ = 0.25, compounded over the year's 252 book dates from
  the sleeve returns: **−0.0134072270**, against the study's **−0.013407** from
  `out/yearly_R4_rt0.csv` (a 6-decimal file) and **−0.013407288446** recomputed
  from the study's 8-decimal daily trail. `handcheck.py` also prints a four-day
  day-by-day trace in February 2015 showing the sleeve returns, the weights
  **actually held** (which drift away from 25 % between rebalances), the gross
  return, the cash accrual and `r(0.25)`.
* **λ = 0 is the cash rate** — shown as an identity gap of exactly 0.000000000000
  for every one of the five books, and re-derived independently to 0.000×10⁰.
* **Cost re-runs** at 5 and 20 bps round trip are in section 11 of `RESULTS.md`.

**A note on what the first run got wrong and how it was caught.** The first
attempt at the worked example computed the book's daily return as a fixed 25 %
blend of the sleeve returns. The comparison against the study's own daily trail
disagreed by ~1×10⁻⁴, because the book's weights *drift* between monthly
rebalances. The example was changed to print the weights actually held, and now
agrees to 4×10⁻⁹. The disagreement was real, small, and found by the hand-check
rather than smoothed over.

---

## Scope and what is not tested

* **Price-only data.** No dividends or distributions anywhere. Bond, credit and
  gold sleeves are understated; a total-return version would raise the risky
  book's return and therefore raise the bar the frontier has to clear.
* **One book family.** All books are the same SMA(200) trend rule on different
  assets. Mean-reversion, carry, cross-asset relative value and held long-vol are
  absent. A different sleeve shape could move the frontier; nothing here shows it
  cannot.
* **Parameter sensitivity untested.** SMA(200) was fixed before the run, as it
  had to be. Nothing here shows 200 beats 150, or rules it out.
* **Costs are a round-trip number applied to flips and monthly turnover**, not a
  modelled execution of a real portfolio.
* **The leverage/short side is untested.** `λ ≤ 1` only; no shorting, no funding,
  no margin.
* **"Every period" is a statement about a finite sample.** 20 years for R4, 32
  for R1L. `100 % of years positive` is a statement about 20 or 32 periods. It is
  not a guarantee, and it is not an out-of-sample claim.
* **Tax, slippage beyond the fixed bps, and the practical cost of daily
  rebalancing a 0.8 % position** are all outside the model.

Do not modify a `SKILL.md` from this directory; the study is evidence, not a
skill.
