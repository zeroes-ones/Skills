# leg-count-test — does adding option legs buy edge, or only shape?

A pre-registered, run-once study that holds the **market view constant** and
varies **only the number of option legs**, to measure what the extra legs
actually buy.

- **Source pull date: 2026-10-14** (TradingView MCP, the sibling study's pull;
  re-validated this session against its own 2026-10-15 fresh pull).
- **Carry date: 2026-10-15.**
- **Run date: 2026-10-15.**
- **Window: 2001-03-13 … 2026-10-14** — 6 436 sessions, **24 complete calendar
  years (2002–2025)**, 102 complete quarters, 306 complete months.
- **Headline answer:** on every one of the three views, `E_net` is **not**
  monotone in leg count, and a 4-leg structure beat its 1-/2-leg comparator on
  `E_net` in **one** of the four comparisons available.  The extra legs bought
  **shape** (skew, balance, tail) far more reliably than they bought **edge**.
  **No 4-leg structure survives the conservative skew direction in any view.**
  See [`FINDINGS.md`](FINDINGS.md) and [`RESULTS.md`](RESULTS.md).

---

## 1. The question

`skills/14-finance/options-trading-playbook/references/payoff-corners-for-options.md`
says a structure's whole economics reduce to two numbers, `p` and `b`, and that
`E = p·b − (1−p)`.  `references/cost-drag-per-leg-and-per-rung.md` says cost is
charged **per contract per leg**, so a 4-leg structure pays roughly twice what a
2-leg one does. Neither file answers the question this study asks:

> If the **view** is identical and only the leg count changes, does the extra
> leg buy expected value net of cost, or does it buy only shape?

The sibling study `../index-options-test` found one related thing: a 4-leg
hedged premium variant repaired 2008 from −11.97 % to −5.63 % but cost
−2.72 pp of CAGR.  That is a statement about adding a **hedge leg**, not about
leg count per se.  This study isolates leg count.

**The three views, declared before the first run:**

| view | the view | structures that express it |
|---|---|---|
| **A** | the index stays INSIDE ±1σ over the next 30 days (range) | A1 short put spread, A2 iron condor, A3 iron butterfly, A4 short strangle |
| **B** | the index RISES over the next 30 days (directional) | B1 long call, B2 bull call debit spread, B3 risk reversal, B4 call ratio backspread |
| **C** | harvest premium with NO directional view (carry) | C1 cash-secured put, C2 covered call, C3 put spread, C4 short ATM put |

**An honest caveat about "the same view", stated up front.** The structures in a
view do **not** express byte-identical views, and this study does not pretend
they do.  A short put spread expresses only the *lower half* of the ±1σ range; an
iron condor expresses both halves.  An iron butterfly sells the ATM straddle, so
it expresses "stays *near* the money", a **tighter** range than ±1σ.  The
study reports the entry Greeks (§5 of `study.py`'s output, `out/shape_greeks.csv`)
precisely so the reader can see how much view drift the extra legs introduce:
the 2-leg put spread runs at net delta **+10.7** while the 4-leg condor runs at
**−0.1** and the 4-leg iron fly at **−1.2**.  *Part of what "more legs" buys is a
different view.*  That is finding, not flaw.

---

## 2. THE OPTIONS MODELLING PROBLEM — read this first

**Historical option quotes are not available from the sources used here.** Every
option price in this study is therefore computed, not observed.  Every
options-derived number is labelled **`[MODELED]`** and never `[VERIFIED]`.

What IS real: the daily OHLC of `AMEX:SPY`, `NASDAQ:QQQ`, `AMEX:IWM`; the VIX
index level (`TVC:VIX`); and the 3-month T-bill yield index (`TVC:US03M`).  Each
series sits in `data/*.csv` behind its own `# PROVENANCE:` header.

### The model, stated exactly

```
IV_leg  = VIX(t − 3 sessions) / 100
          × kappa(index, t − 3 sessions)
          × iv_off(variant)              # 0 in the primary run

kappa(index) = clip( RV60(index) / RV60(SPY), 0.60, 2.00 )
               both realised vols measured at t − 3 sessions

price   = Black-Scholes, European, q = 0, T = ACTUAL calendar days / 365
strike  = solved from the SIGNAL close so the leg's delta hits its target
settle  = intrinsic, against the REAL closing price of the expiry session
```

The IV construction, the 3-session VIX lag, `kappa`, the window rule and the
monthly-expiry cap are **carried verbatim from `../index-options-test`**, and the
section below is carried forward from its README because it still applies.

### What the model cannot see

1. **No bid/ask spread in the quote.** A flat per-contract spread IS charged as a
   cost (§7), but the quote itself is a mid.
2. **No skew.** One implied vol prices every strike, so the *sold* leg is priced
   at the same vol as the wings. A real seller of an out-of-the-money option
   collects **less** than the flat-vol Black-Scholes value. §6 of the run sizes
   this by re-pricing with the sold strikes charged ±1.5 vol points; it is the
   single largest bias in the study and the one that most affects the structures
   with the most strikes.
3. **No term structure.** One vol prices every tenor (`alpha = 0`).
4. **No early exercise and no assignment.** SPY/QQQ/IWM options are **American
   and physically settled**; they are priced here as **European** and
   cash-settled. An American short put can be assigned early, and this model
   would never show it.
5. **No pin risk.** The expiry session's close decides everything.
6. **No dividends.** The price series is price-only, so the modelled call is too
   expensive and the modelled put too cheap. This bias is inherited by **every**
   call and put leg, so it bites **harder** the more legs a structure has.
7. **No margin, no buying-power constraint, no liquidity limit, no partial
   fills, and NO LEGGING RISK.** A 4-leg structure is assumed to fill as one
   ticket at the modelled mid. In reality a 4-leg structure has four legs' worth
   of legging risk and a 1-leg structure has none; this study cannot see that.
8. **Strikes are not rounded to exchange increments.** A real SPY chain is
   $1-wide; the solved strikes here may sit up to $0.50 off a listed strike.
9. **One contract per unit, integer, always fillable at the modelled mid.**

### Two further limitations this study adds

10. **A fixed risk budget is era-sensitive.** `R` for a long option IS its debit,
    which tracks the index level, which rose ~6× (SPY) over this window. The
    risk budget is therefore `10 × R` **of the position actually open that
    session**, not one constant dollar figure. `R$med` and `R$5yr` are both
    reported because the capital question is **not** era-free.
11. **R is a maximum loss measured on the terminal payoff, and for the flagged
    structures it is not.** For a structure with an unbounded call side (A4) `R`
    is the loss at a **stated** ±1.5σ stop, not a structural maximum loss, and a
    real broker margins a short strangle against far more than that. For B3 the
    risk reversal's short put is uncovered, so its `R` is a **cash-secured**
    requirement (97 % of notional) — i.e. B3 is a cash-secured put plus a long
    call, and is reported as such.

**What this means for the reader.** A `[MODELED]` `E_net` that survives a
1.5 vol-point skew haircut, a doubling of costs, and the fixed-budget identity
check is worth reading. One that does not is a statement about the model.

---

## 3. Data

**Primary source.** TradingView MCP tool `mcp__tradingview__mcp-tv-get-ohlcv`,
interval `1D`, `format="columns"`. Every series is **split-adjusted, regular
session only, and price-only — no dividends or distributions**.

**This study carries the five long series rather than re-pulling them.**
`carry_data.py` reads them from `../index-options-test/data/`, and before writing
each one it **re-checks the source header's own `rows`/`first`/`last` claims
against the body it sits above** and re-computes a SHA-256 of the body. It then
re-checks the sibling's `_check_<SYM>_recent.csv` **validation fixtures** — a
fresh 1 500-session pull the sibling made from the same tool on 2026-10-15 —
against the carried series, session by session. Those fixtures are an **audit
trail and never a strategy input**.

**Why not re-pull.** A fresh MCP pull returns ~1 500 raw bars through a tool
result, putting a price series into a reasoning context for no gain. The series
are the same series.

| series | source symbol | rows | first | last |
|---|---|---|---|---|
| SPY | `AMEX:SPY` | 8 485 | 1993-01-29 | 2026-10-14 |
| QQQ | `NASDAQ:QQQ` | 6 943 | 1999-03-10 | 2026-10-14 |
| IWM | `AMEX:IWM` | 6 635 | 2000-05-26 | 2026-10-14 |
| VIX | `TVC:VIX` | 9 283 | 1990-01-03 | 2026-10-14 |
| US03M | `TVC:US03M` | 18 197 | 1954-01-04 | 2026-10-14 |

**Validation fixtures, re-checked at carry:**

| series | fresh rows | overlap | OHLC mismatch |
|---|---|---|---|
| SPY | 1500 | 1500 | 0 |
| QQQ | 1500 | 1500 | 0 |
| IWM | 1500 | 1500 | 0 |
| VIX | 1500 | 1500 | 0 |
| **TOTAL** | | **6 000** | **0** |

**`TVC:US03M` is NOT a price series.** Its `close` column is a
**percent-per-annum yield index**, used only as the risk-free rate `r` for
pricing (lagged three sessions, floored at zero). Nothing compounds it as a
price return.

---

## 4. The pre-registration

Declared before the first run. Entries at the **next open** after the monthly
roll signal.

### Shared discipline — identical for every structure

| element | rule |
|---|---|
| tenor | 30 calendar days, **capped** at the last session before the next monthly roll, so a monthly programme never holds two cycles at once (measured 27–30 days; pricing uses the actual days) |
| signal / entry | signal at the **last session of a month**, struck from that **close**, entered at the **next session's open** |
| strikes | solved from the signal close on the base vol; **held FIXED across every variant**, so a difference between two variants is a pure pricing effect |
| settlement | **intrinsic** against the REAL close of the expiry session (European, cash-settled) |
| delta targets | 16Δ / 25Δ / 30Δ / 50Δ as named per structure |
| wings | $5.00-wide, both sides |
| `R` | the structure's own **maximum loss**, measured on a terminal grid `[0, 3·S]` whose kink set is `{endpoints} ∪ {strikes}`. For a structure with an **unbounded call side**, `R` is instead the loss at a **stated ±1.5·σ√T stop** and the structure is flagged. A modelled max loss ≤ 0 means the model says the structure **cannot lose**; `R` is then the wing width as a stated normalisation and the trade is flagged `ARB` and counted. **No intra-trade stop is simulated anywhere** — every structure is held to expiry, so for the flagged ones `R` is a *normalisation of the payoff*, not an enforced exit. `R` excludes cost, so a trade that hits the structural max loss shows `R_mult = −(1 + c_R)`. |
| budget | a **fixed** `10 × R` of the position open that session; daily return = dollar P&L ÷ that budget. **Not a compounding account.** |
| cost | `(fee + half_spread × 100) × contracts`, charged once per leg (**one ticket**, because a leg that expires has no closing ticket), plus a round-trip bps charge on the covered call's stock leg |
| the underlying leg | is NOT a premium: it enters the book at its **P&L against the entry price**, so buying the shares is not a cash outflow and cannot be double-counted |

### The structures, ordered by leg count within each view

| id | view | legs | contracts | the structure |
|---|---|---|---|---|
| A1 | A | 2 | 2 | short put spread ~16Δ / 5-wide |
| A2 | A | 4 | 4 | iron condor ~16Δ shorts / 5-wide wings |
| A3 | A | 4 | 4 | iron butterfly ATM short / 5-wide wings |
| A4 | A | 2 | 2 | short strangle ~16Δ both sides **(UNDEFINED on the call side — flagged)** |
| B1 | B | 1 | 1 | long call ~30Δ |
| B2 | B | 2 | 2 | bull call debit spread ~50Δ long / ~25Δ short |
| B3 | B | 2 | 2 | risk reversal long ~30Δ call / short ~30Δ put **(short put uncovered → R is a cash-secured requirement)** |
| B4 | B | 2 | 3 | call ratio backspread long 2× ~25Δ / short 1× ~50Δ |
| C1 | C | 1 | 1 | cash-secured put ~16Δ |
| C2 | C | 2 | 1 | covered call: long underlying + short ~30Δ call |
| C3 | C | 2 | 2 | put spread ~16Δ / 5-wide (**the same instrument as A1**, relabelled to give the carry view a comparator) |
| C4 | C | 1 | 1 | short ATM put — the 1-leg carry comparator |

**On B4, the brief's wording is wrong and the study says so.** The brief flags
B4 as "undefined on the upside". Its *gain* is unbounded above; its *loss* is
**defined**, attained at the short call's strike and equal to
`debit + (K_long − K_short)`. It is therefore NOT flagged `UNDEFINED`, and that
is a correction to the brief, not a silent reclassification. The one structure
in the whole set with an unbounded **loss** is A4.

### Cost settings

`[MODELED]` — a cost assumption, not an observed quote.

| setting | fee / contract / leg | half-spread / share / side | all-in per contract | tickets / leg | stock round trip |
|---|---|---|---|---|---|
| **FREE** | $0.00 | $0.000 | $0.00 | 1 | 0 bps |
| **LOW** *(headline)* | $0.65 | $0.025 | **$3.15** | 1 | 5 bps |
| **HIGH** | $0.65 | $0.050 | **$5.65** | 1 | 20 bps |
| **RT_LOW** | $0.65 | $0.025 | $6.30 | **2** | 10 bps |

`references/cost-drag-per-leg-and-per-rung.md` charges **two** tickets per leg (a
round trip). A leg that **expires** has no closing ticket, so the headline
convention here is **one** ticket per leg and `RT_LOW` bounds the other reading.
Both are reported.

### The seven runs

`iv_mode` changes only the **pricing vol**; strikes never move.

| variant | cost | iv_mode | what it is |
|---|---|---|---|
| FREE | FREE | BASE | gross edge reference |
| LOW | LOW | BASE | **headline** |
| HIGH | HIGH | BASE | high prices |
| RT_LOW | RT_LOW | BASE | round trip at LOW prices |
| SKEW_SOLD_P15 | LOW | SOLD_P15 | SOLD legs' pricing vol **+1.5** points (seller collects more) |
| SKEW_SOLD_M15 | LOW | SOLD_M15 | SOLD legs' pricing vol **−1.5** points (seller collects less — the sibling's conservative direction) |
| SKEW_ALL_P15 | LOW | ALL_P15 | EVERY option leg **+1.5** points (the only test that is not vacuous for a long-only structure) |

### The selection rule, declared before the run

Rank within a view by **`edge_per_tail` = `E_net` ÷ |mean R of the worst 1 % of
trades|**, ties broken by higher `E_net`. The highest-`E_net` structure is **also**
named separately, because the two rules can disagree and the reader should see
when they do.

### The measured unit of comparison, and its trap

`E_net` in `R` units **is** the return on a risk budget, because capital per unit
= `R`. So the structures are comparable in `R` units — **provided you can commit
10 `R`**. They are not comparable in **capital**: one contract of C1
(cash-secured put) risks **93.9 %** of the index notional while one contract of
A2 (iron condor) risks **3.3 %**. `R/notional %` is printed for exactly this
reason, and so is `R$5yr`.

---

## 5. How to re-run

`python3` is not on `PATH` on this machine; use `py -3` (Python 3.10.11).

```bash
cd skills/14-finance/options-trading-playbook/examples/leg-count-test
export PYTHONIOENCODING=utf-8

# 1. carry the five series from the sibling study, verifying them on the way
py -3 carry_data.py | tee logs/carry-output.txt

# 2. the study  (deterministic, stdlib only, no network)
py -3 study.py > run-output.txt

# 3. the INDEPENDENT re-derivation  (does not import study.py)
py -3 handcheck.py > handcheck-output.txt     # expect HANDCHECK PASSED

# 4. rebuild RESULTS.md from the captured run
py -3 make-results.py

# 5. check every number transcribed by hand into FINDINGS.md / README.md
py -3 verify-claims.py | tee logs/verify-claims-output.txt   # expect PASSED
```

Steps 2–5 need **no network at all**.  Nothing in this directory touches the
network.

**Determinism** (verified, 2026-10-15): three consecutive runs produced **0
differing lines of stdout** and **0 differing bytes across all `out/*.csv`**.
There is no clock, no RNG and no set iteration in `study.py` that reaches a
number.

**Scope** (verified): this directory is self-contained.  Every write call in
`carry_data.py`, `study.py`, `make-results.py` and `verify-claims.py` targets a
path inside this directory; `handcheck.py` and `verify-claims.py` write nothing
at all.  No `SKILL.md` and no file belonging to another skill was modified.

---

## 6. Files

| file | what it is |
|---|---|
| `carry_data.py` | carries the five series from `../index-options-test/data/`, re-checking each source header against its body, re-hashing the body, and re-checking the sibling's fresh-pull validation fixtures. No network. |
| `study.py` | the study: pre-registration echo, Black-Scholes engine, the 12 structures, the 7 variants, the cost model, the maximum-loss/R convention, the daily mark loop, the six headline tests, and internal self-checks. Deterministic, stdlib only, LF output |
| `handcheck.py` | an **independent** re-derivation from `data/*.csv`: own CSV reader, own Black-Scholes, own delta solver, own vol context, own structure builders, own R scan, own month grid, own simulator. **Does not import `study.py`** |
| `make-results.py` | renders `RESULTS.md` from `run-output.txt` and `out/*.csv`. Formats; never calculates |
| `verify-claims.py` | a **transcription** check: every number typed by hand into `FINDINGS.md` / `README.md` is looked up in the study's own output (662 checks). It is not a re-derivation — `handcheck.py` is |
| `data/*.csv` | the five series, each behind a `# PROVENANCE:` block |
| `data/_check_*_recent.csv` | the sibling's fresh 2026-10-15 pull, re-checked here — audit trail only |
| `out/*.csv` | every table the study produces (10 files) |
| `logs/carry-output.txt` | complete stdout of the data step |
| `logs/verify-claims-output.txt` | complete stdout of the transcription check |
| `run-output.txt` | complete stdout of `study.py` — the source of every number in `RESULTS.md` |
| `handcheck-output.txt` | complete stdout of `handcheck.py` |
| `RESULTS.md` | every table, pasted from the real run |
| `FINDINGS.md` | the honest narrative: what legs buy, what they cost, where complex wins, what the model cannot see |

---

## 7. Verification performed

```bash
py -3 study.py > r1.txt ; py -3 study.py > r2.txt ; py -3 study.py > r3.txt
diff r1.txt r2.txt && diff r1.txt r3.txt             # 0 lines
diff -r out_snapshot out                             # 0 files differ
py -3 handcheck.py                                   # HANDCHECK PASSED
py -3 verify-claims.py                               # VERIFY CLAIMS PASSED
```

| check | result |
|---|---|
| Determinism (three runs) | **0** differing stdout lines, **0** differing `out/*.csv` |
| Daily P&L == trade ledger, **all 84 sleeves** | worst gap **5.8×10⁻¹¹** |
| Reported leg count == built leg count, all 12 | **PASS** |
| `c_R` == 0 at the FREE setting | max **0** |
| No book return ≤ −100 % (positivity unambiguous) | worst book day **−31 %** |
| Independent re-derivation, **11 016 trades × 13 fields** | worst field gap **5.0×10⁻⁵** (the CSV's own 6-decimal rounding), **0 rows missing** |
| Independent re-derivation, headline `p`, `b`, `E_R`, `c_R`, `R$med` | worst gap **0.000×10⁰** — exact |
| Independent re-derivation, daily-vs-ledger identity | worst gap **4.4×10⁻¹¹** |
| **Transcription**, every hand-typed number in FINDINGS/README | **662 checks, 0 mismatches** |
| **By hand**: one Black-Scholes price | S = 100, K = 95, T = 30/365, r = 4 %, σ = 20 % → **P = 0.5088781574**, every intermediate (`d1`, `d2`, `N(·)`, discount factors) printed |
| **By hand**: one leg of **each** of the 12 structures re-priced from stated inputs and compared with the ledger's own credit | worst gap **4.4×10⁻⁷** |
| **By hand**: `c_R` for A2 at LOW prices, from the stated fee and half-spread | cost gap **0**; `c_R` gap **1.3×10⁻¹⁶** |
| **By hand**: one 4-leg iron condor settled against the real path | gross P&L, net P&L and `R` all match; worst gap **1.6×10⁻¹²** |
| Data provenance | 8 485 / 6 943 / 6 635 / 9 283 / 18 197 rows, every header claim re-checked against its body |
| Fresh-pull overlap | **6 000** overlapping sessions, **0** OHLC mismatches |
| **Cross-check against the sibling study's engine** | the by-hand A1 trade reproduces the sibling's own handcheck exactly: `K1 = 108.9730`, `K2 = 103.9730`, credit `0.606128`, `R = 439.387189`. This study's engine and the sibling's agree to the printed digit. |
| All files UTF-8, **LF**, no trailing whitespace, no tabs, final newline | **PASS** (checked byte-wise) |
| Scope: no write outside this directory | **PASS** (audited every write call; the newest file changed outside this directory predates the first write made here) |

**Structures whose 10`R` budget is TOO SMALL**, reported as a finding rather
than asserted: **A3 (iron butterfly), worst single session −69 % of the budget**.
A 5-wide iron fly on a $100–$700 index has a **terminal max loss of 1.17 % of
notional** but a **mark-to-market swing far larger than that**, so `R` cannot
normalise it. Its tail columns are still valid in `R`; its compounded CAGR and
percentage columns are not, and are flagged as such.

**What was NOT verified, and cannot be with these sources:** that the modelled
option prices resemble any price that ever existed. They are a construction from
VIX, not a quotation.

---

## 8. What this cannot promise

- It cannot tell you what any of these structures would have **filled** at.
  There is no bid/ask, no legging risk, no partial fill, no liquidity limit.
- It cannot price **skew**, so the whole study is a *flat-vol* world. §6 of the
  run bounds the size of that by moving the sold legs ±1.5 vol points and
  reports how much each structure's answer moves. The structures with the most
  strikes move the most — but not monotonically in leg count, and the ranking in
  *dollars* is not the ranking in *R*.
- It cannot see **assignment**, so the short-put structures never get assigned.
  A real American short put would.
- It cannot see **dividends**, so every modelled call is too expensive and every
  modelled put too cheap, and a call leg costs more the more call legs a
  structure has.
- It cannot say anything about a structure **not** in the pre-registered set. The
  twelve were chosen before the run and were not changed after it.

Do not modify a `SKILL.md` from this directory; the study is evidence, not a
skill.
