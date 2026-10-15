# RESULTS -- the leg-count test, verbatim from a real run

**Every number in this file is `[MODELED]`, not `[VERIFIED]`.**  No historical
option quotes are available from the sources used here.  Historical option
prices do not exist in `data/*.csv`; they are constructed with Black-Scholes
from the real VIX and settled against the real index closes.

Three views, twelve pre-registered structures, one unit of risk `R` per trade
defined as the structure's own maximum loss, 30-DTE monthly cycles, entry at the
next open after the monthly roll, settlement at intrinsic against the real path,
2001-03-13 to 2026-10-14 (6 436 sessions, 24 complete calendar years).

## How this file was produced

```bash
py -3 carry_data.py
py -3 study.py > run-output.txt
py -3 handcheck.py > handcheck-output.txt
py -3 make-results.py
```

`make-results.py` formats; it never calculates.  Section 1 below is the raw
stdout of `study.py`.  Section 2 is the small `out/*.csv` tables pasted in full.
Section 3 is the raw stdout of the INDEPENDENT re-derivation.

---

## 1. The raw stdout of `study.py`

```text


==============================================================================
LEG-COUNT TEST -- does adding option legs buy edge, or only shape?
==============================================================================
Pre-registered.  Deterministic.  No RNG, no clock, no network.

READ THIS BEFORE ANY NUMBER: every option price below is [MODELED].
Historical option quotes are not available from the sources used.
Legs are priced with Black-Scholes on a VIX-derived implied vol and
settled against the REAL index close on the expiry session.  The
model has: no quote spread, NO SKEW (one vol for every strike), no
term structure, NO EARLY EXERCISE AND NO ASSIGNMENT (SPY/QQQ/IWM
options are American and physically settled; they are priced here as
European and cash-settled), no pin risk, no dividends, no margin, no
liquidity limit, NO LEGGING RISK, unrounded strikes.  A flat
per-contract spread IS charged as a cost; the QUOTE is still a mid.

==============================================================================
0. DATA -- provenance echoed verbatim from data/*.csv
==============================================================================
  SPY    rows=8485   first=1993-01-29 last=2026-10-14
  QQQ    rows=6943   first=1999-03-10 last=2026-10-14
  IWM    rows=6635   first=2000-05-26 last=2026-10-14
  VIX    rows=9283   first=1990-01-03 last=2026-10-14
  US03M  rows=18197  first=1954-01-04 last=2026-10-14

  Provenance of the three index series (verbatim):
    source=TradingView MCP tool mcp__tradingview__mcp-tv-get-ohlcv
    symbol=AMEX:SPY  interval=1D  fields=OHLCV
    pulled=2026-10-14 (UTC date of the sibling pull)
    CARRIED from ../frontier-test/data/SPY_1d.csv -- same tool, same pull date
    carried_by=pull_data.py  carried=2026-10-15
    VERIFIED before carry: the sibling header's own rows/first/last claims were re-checked against its body and matched
    sha256(body of the carried file)=e104ae01aefea7444b25011c2aedd558793d24f7659f703ec54dfee5390149af
    rows=8485  first=1993-01-29  last=2026-10-14
    date is the exchange session date, rendered as the UTC calendar date of the bar timestamp
    split-adjusted, regular session only
    volume is as reported by the source, in shares (unadjusted for splits)
    PRICE-ONLY series. No dividends or distributions. Not a total-return series.
    carried_by=carry_data.py  carried=2026-10-15  from=C:\Users\sande\Documents\Projects\Skills\skills\14-finance\options-trading-playbook\examples\index-options-test\data\SPY_1d.csv
    CARRIED, not re-pulled. The five series are the same 1D series the sibling study already pulled on 2026-10-14; re-pulling returns raw bars through a tool result for no gain.
    VERIFIED at carry: the source header's own rows/first/last claims were re-checked against the body it sits above and matched.
    sha256(body of the carried file)=8c9fd9d9cc75fc7430e64df2a2b17218e73a6522bb0381fc7df7c4c32008a596

    US03M: *** NOT A PRICE SERIES ***. TVC:US03M is a YIELD INDEX (3-month US Treasury bill, percent per annum). The `close` column is an annualised yield in percent, not a tradable price. No price-return may be computed from it; it is used only as the cash-accrual rate.

  WINDOW: 6436 sessions, 2001-03-13 .. 2026-10-14
    complete M  periods = 306  (2001-04 .. 2026-09)
    complete Q  periods = 102  (2001-Q2 .. 2026-Q3)
    complete Y  periods = 24  (2002 .. 2025)
    cash CAGR over the same window (TVC:US03M, lagged 1 session, floored at 0) = +1.80%
    monthly cycles entering a trade: 306 per index; 918 trades per structure pooled over 3 indexes

==============================================================================
1. PRE-REGISTRATION (echoed BEFORE any result is shown)
==============================================================================
  THREE VIEWS.  Within a view, ONLY the leg count changes:
    View A -- the index stays INSIDE +-1 sigma over the next 30 days   (range)
    View B -- the index RISES over the next 30 days                   (directional)
    View C -- harvest premium with NO directional view               (carry)

  THE STRUCTURES, ordered by leg count within each view:
  id  view  legs  structure
  --  ----  ----  ----------------------------------------------------
  A1  A     2     short put spread ~16d / 5-wide
  A2  A     4     iron condor ~16d shorts / 5-wide wings
  A3  A     4     iron butterfly ATM short / 5-wide wings
  A4  A     2     short strangle ~16d both sides
  B1  B     1     long call ~30d
  B2  B     2     bull call debit spread ~50d long / ~25d short
  B3  B     2     risk reversal long ~30d call / short ~30d put
  B4  B     2     call ratio backspread long 2x ~25d / short 1x ~50d
  C1  C     1     cash-secured put ~16d
  C2  C     2     covered call: long underlying + short ~30d call
  C3  C     2     put spread ~16d / 5-wide (the same instrument as A1)
  C4  C     1     short ATM put -- the 1-leg carry comparator

  SHARED DISCIPLINE (identical for every structure):
    tenor            : 30 calendar days, capped at the last session
                       before the next monthly roll
    entry            : signal at the last session of a month,
                       position established at the NEXT open
    strikes          : solved from the SIGNAL close on the base
                       implied vol; HELD FIXED across all variants
    settlement       : INTRINSIC against the REAL close of the
                       expiry session (European, cash-settled)
    delta targets    : 16d / 25d / 30d / 50d as named per structure
    wings            : $5-wide
    R                : the structure's own MAXIMUM LOSS, measured on
                       a 4000-point terminal grid [0, 3*S]
                       for a bounded structure; for a structure
                       with an UNBOUNDED CALL SIDE, R is the loss at
                       a stated +1.5*sigma*sqrt(T) move and the
                       structure is flagged.  NO INTRA-TRADE STOP IS
                       SIMULATED: every structure is held to expiry,
                       so for the flagged ones R is a NORMALISATION
                       of the payoff, not an enforced exit.
    budget           : a fixed 10 x one R; daily return = dollar
                       P&L / that budget.  NOT a compounding account.

  COST SETTINGS (per contract, per leg, ONE side, plus a stated
  per-share half-spread; the stock leg pays round-trip bps):
  setting  fee    half-spread  per leg/side  tickets  stock
  -------  -----  -----------  ------------  -------  --------
  FREE     +0.00  +0.00        +0.00         1        0.0 bps
  LOW      +0.65  +0.03        +3.15         1        5.0 bps
  HIGH     +0.65  +0.05        +5.65         1        20.0 bps
  RT_LOW   +0.65  +0.03        +6.30         2        10.0 bps
    The skill's `cost-drag-per-leg-and-per-rung.md` charges TWO
    tickets per leg (a round trip).  A leg that EXPIRES has no
    closing ticket, so the headline convention here is ONE ticket
    per leg and RT_LOW bounds the other reading.

  THE SEVEN RUNS.  `iv_mode` changes only the PRICING vol; strikes
  never move, so a difference between two iv_modes is pure pricing:
  variant        cost    iv_mode   what it is
  -------------  ------  --------  --------------------------------------------------------------------
  FREE           FREE    BASE      gross, no cost, no skew haircut -- the gross-edge reference
  LOW            LOW     BASE      headline: $0.65/contract/leg + $0.025/share half-spread, 5 bps stock
  HIGH           HIGH    BASE      high: $0.65/contract/leg + $0.050/share half-spread, 20 bps stock
  RT_LOW         RT_LOW  BASE      round trip (2 tickets/leg, the skill's convention) at LOW prices
  SKEW_SOLD_P15  LOW     SOLD_P15  SOLD option legs charged +1.5 vol points at pricing (strikes fixed)
  SKEW_SOLD_M15  LOW     SOLD_M15  SOLD option legs charged -1.5 vol points at pricing (strikes fixed)
  SKEW_ALL_P15   LOW     ALL_P15   ALL option legs charged +1.5 vol points at pricing (strikes fixed)

  SELECTION RULE FOR 'BEST STRUCTURE IN A VIEW' (declared now):
    rank by edge_per_tail = E_net(R, LOW) / |worst 1%% of trades (R)|
    ties broken by higher E_net.  The highest-E_net structure is
    ALSO named separately, because the two rules can disagree.

==============================================================================
2. RUNNING -- 12 structures x 7 variants x 3 indexes = 252 sleeves
==============================================================================
  done.

==============================================================================
3. STRUCTURE SUMMARY AT THE HEADLINE COST (LOW)
==============================================================================
  E_form = p*b-(1-p) [the skill's identity]   E_R = sample mean in R
  c_R = mean(cost/R)   E_net = E_R - c_R      R/not = era-free R
  CAPITAL: one contract of a defined-risk structure posts capital = R.
  So dollars of expectancy per $10,000 of capital = 10,000 x E_net, and
  that is what E$_10k is: the same ordering as E_net, rescaled to a
  readable unit.  For A4 and B3, R is a STATED STOP, not a broker
  requirement -- a real short strangle is margined on the whole
  underlying, so their E$_10k is OPTIMISTIC and is flagged.
  id  view  legs  n    p       b      E_form   E_R      c_R      E_net    R$med      E$/10k/mo  u@25k
  --  ----  ----  ---  ------  -----  -------  -------  -------  -------  ---------  ---------  -----
  A1  A     2     918  0.8976  0.181  +0.0599  +0.0321  +0.0140  +0.0181  +454.35    +181.0     55
  A2  A     4     918  0.8573  0.353  +0.1596  +0.0915  +0.0313  +0.0602  +407.25    +602.3     61
  A3  A     4     918  0.4194  1.451  +0.0279  +0.0271  +0.1387  -0.1116  +139.38    -1116.4    179
  A4  A     2     918  0.8769  0.470  +0.2893  +0.2303  +0.0258  +0.2045  +287.44    +2045.3    86
  B1  B     1     918  0.2298  1.464  -0.4336  -0.4271  +0.0275  -0.4546  +134.59    -4545.6    185
  B2  B     2     918  0.4510  1.448  +0.1040  +0.0953  +0.0428  +0.0525  +171.95    +524.7     145
  B3  B     2     918  0.4946  0.963  -0.0290  -0.0005  +0.0007  -0.0012  +12063.68  -12.0      2
  B4  B     2     918  0.4804  0.262  -0.3939  -0.2121  +0.0263  -0.2384  +409.74    -2383.6    61
  C1  C     1     918  0.9031  0.220  +0.1021  +0.0027  +0.0004  +0.0023  +11754.07  +22.9      2
  C2  C     2     918  0.6841  0.880  +0.2858  +0.0118  +0.0008  +0.0109  +12271.05  +109.3     2
  C3  C     2     918  0.8976  0.181  +0.0599  +0.0321  +0.0140  +0.0181  +454.35    +181.0     55
  C4  C     1     918  0.7625  0.602  +0.2215  +0.0085  +0.0003  +0.0081  +12134.48  +81.2      2

  R is the structure's MAXIMUM LOSS on the payoff grid and it EXCLUDES
  cost, so a trade that hits the structural max loss shows
  R_mult = -(1 + c_R).  R$med is a MEDIAN over 2001-2026, when the
  index TRIPLED, so R$med is a MEDIAN-ERA dollar amount; R/notional%
  is the era-free version and R$recent is the last 5 years only.
  `arb` is the share of trades for which the MODEL gives a maximum
  loss <= 0, i.e. the model says the structure cannot lose.  That is
  an ARBITRAGE under flat-vol pricing, not an edge.
  id  view  legs  R/notional%  R$med      R$5yr      arb%  worstDay
  --  ----  ----  -----------  ---------  ---------  ----  --------
  A1  A     2     3.68%        +454.35    +426.50    0     -7%
  A2  A     4     3.34%        +407.25    +363.25    0     -9%
  A3  A     4     1.17%        +139.38    +43.63     0     -31%
  A4  A     2     2.51%        +287.44    +966.53    0     -25%
  B1  B     1     1.16%        +134.59    +424.31    0     -20%
  B2  B     2     1.47%        +171.95    +539.72    0     -14%
  B3  B     2     97.09%       +12063.68  +38322.67  0     -1%
  B4  B     2     3.56%        +409.74    +1405.98   0     -6%
  C1  C     1     93.91%       +11754.07  +37194.35  0     -1%
  C2  C     2     98.84%       +12271.05  +39122.75  0     -1%
  C3  C     2     3.68%        +454.35    +426.50    0     -7%
  C4  C     1     97.62%       +12134.48  +38515.75  0     -1%
  R$5yr is what one contract risks TODAY; R$med is what it risked in a
  median year of the window.  The capital question is not era-free.

  THE CORNER NUMBERS the skill defines, per structure:
  p* = 1/(1+b) is the break-even win rate; b* = (1-p)/p is the
  break-even payoff; sd is the sample sd of R_mult in R;
  n_req = 4(sd/|E_R|)^2 is the trades needed to see the edge at 2 sigma.
  id  view  legs  p       b      p*      b*      sd_R    E_R      n_req    L_act  L_exp  n<n_req
  --  ----  ----  ------  -----  ------  ------  ------  -------  -------  -----  -----  --------
  A1  A     2     0.8976  0.181  0.8469  0.1141  0.2349  0.0321   214.1    2      3.0
  A2  A     4     0.8573  0.353  0.7393  0.1665  0.3244  0.0915   50.3     3      3.5
  A3  A     4     0.4194  1.451  0.4080  1.3844  1.7803  0.0271   17265.7  29     12.5   OVER-REQ
  A4  A     2     0.8769  0.470  0.6801  0.1404  0.4711  0.2303   16.7     2      3.3
  B1  B     1     0.2298  1.464  0.4058  3.3507  1.2042  -0.4271  31.8     22     26.1
  B2  B     2     0.4510  1.448  0.4085  1.2174  1.2108  0.0953   646.1    10     11.4
  B3  B     2     0.4946  0.963  0.5093  1.0220  0.0294  -0.0005  13197.2  12     10.0   OVER-REQ
  B4  B     2     0.4804  0.262  0.7926  1.0816  0.4044  -0.2121  14.5     7      10.4
  C1  C     1     0.9031  0.220  0.8194  0.1074  0.0133  0.0027   99.9     2      2.9
  C2  C     2     0.6841  0.880  0.5321  0.4618  0.0462  0.0118   61.5     5      5.9
  C3  C     2     0.8976  0.181  0.8469  0.1141  0.2349  0.0321   214.1    2      3.0
  C4  C     1     0.7625  0.602  0.6243  0.3114  0.0329  0.0085   60.5     4      4.7

==============================================================================
TEST 1 -- IS E_net MONOTONIC IN LEG COUNT, HOLDING THE VIEW CONSTANT?
==============================================================================

  View A -- the index stays INSIDE +-1 sigma over the next 30 days   (range)
  id  legs  ctr  p       b      E_form   E_R      c_R      E_net    E$/10k   flag
  --  ----  ---  ------  -----  -------  -------  -------  -------  -------  --------
  A1  2     2    0.8976  0.181  +0.0599  +0.0321  +0.0140  +0.0181  +181.0
  A4  2     2    0.8769  0.470  +0.2893  +0.2303  +0.0258  +0.2045  +2045.3  UNDEF-UP
  A2  4     4    0.8573  0.353  +0.1596  +0.0915  +0.0313  +0.0602  +602.3
  A3  4     4    0.4194  1.451  +0.0279  +0.0271  +0.1387  -0.1116  -1116.4
    E_net order by leg count: A1 0.0181 -> A4 0.2045 -> A2 0.0602 -> A3 -0.1116
    MONOTONE FALLING IN LEG COUNT: NO
    highest E_net: A4 (+0.2045)

  View B -- the index RISES over the next 30 days                   (directional)
  id  legs  ctr  p       b      E_form   E_R      c_R      E_net    E$/10k   flag
  --  ----  ---  ------  -----  -------  -------  -------  -------  -------  ----
  B1  1     1    0.2298  1.464  -0.4336  -0.4271  +0.0275  -0.4546  -4545.6
  B2  2     2    0.4510  1.448  +0.1040  +0.0953  +0.0428  +0.0525  +524.7
  B3  2     2    0.4946  0.963  -0.0290  -0.0005  +0.0007  -0.0012  -12.0
  B4  2     3    0.4804  0.262  -0.3939  -0.2121  +0.0263  -0.2384  -2383.6
    E_net order by leg count: B1 -0.4546 -> B2 0.0525 -> B3 -0.0012 -> B4 -0.2384
    MONOTONE FALLING IN LEG COUNT: NO
    highest E_net: B2 (+0.0525)

  View C -- harvest premium with NO directional view               (carry)
  id  legs  ctr  p       b      E_form   E_R      c_R      E_net    E$/10k  flag
  --  ----  ---  ------  -----  -------  -------  -------  -------  ------  ----
  C1  1     1    0.9031  0.220  +0.1021  +0.0027  +0.0004  +0.0023  +22.9
  C4  1     1    0.7625  0.602  +0.2215  +0.0085  +0.0003  +0.0081  +81.2
  C2  2     1    0.6841  0.880  +0.2858  +0.0118  +0.0008  +0.0109  +109.3
  C3  2     2    0.8976  0.181  +0.0599  +0.0321  +0.0140  +0.0181  +181.0
    E_net order by leg count: C1 0.0023 -> C4 0.0081 -> C2 0.0109 -> C3 0.0181
    MONOTONE FALLING IN LEG COUNT: NO
    highest E_net: C3 (+0.0181)

  PLAIN ANSWER: more legs did NOT buy gross edge net of cost on any
  view.  See the per-view lines above for the ordering.

==============================================================================
TEST 2 -- COST DRAG BY LEG COUNT, AND THE BREAK-EVEN COST c_R* = E
==============================================================================
  c_R* = E_R is the cost (in R) at which the gross edge is exactly
  consumed.  `legs to eat edge` is the first leg count in the view
  at which some structure's c_R >= its own E_R.
  id  view  legs  ctr  cost$   c_R_LOW  E_net_LOW  c_R_HIGH  E_net_HIGH  c_R_RT   E_net_RT  c_R*      c_R*$    eats edge
  --  ----  ----  ---  ------  -------  ---------  --------  ----------  -------  --------  --------  -------  ---------
  A1  A     2     2    +6.30   0.01401  +0.0181    0.02512   +0.0070     0.02801  +0.0041   0.03211   +14.59
  A2  A     4     4    +12.60  0.03127  +0.0602    0.05609   +0.0354     0.06254  +0.0290   0.09150   +37.26
  A3  A     4     4    +12.60  0.13874  -0.1116    0.24884   -0.2217     0.27747  -0.2504   0.02710   +3.78    YES
  A4  A     2     2    +6.30   0.02576  +0.2045    0.04621   +0.1841     0.05153  +0.1788   0.23029   +66.20
  B1  B     1     1    +3.15   0.02746  -0.4546    0.04925   -0.4764     0.05492  -0.4820   -0.42710  -57.48   YES
  B2  B     2     2    +6.30   0.04280  +0.0525    0.07676   +0.0185     0.08559  +0.0097   0.09527   +16.38
  B3  B     2     2    +6.30   0.00069  -0.0012    0.00124   -0.0018     0.00139  -0.0019   -0.00051  -6.17    YES
  B4  B     2     3    +9.45   0.02629  -0.2384    0.04715   -0.2592     0.05257  -0.2646   -0.21207  -86.89   YES
  C1  C     1     1    +3.15   0.00036  +0.0023    0.00065   +0.0020     0.00072  +0.0019   0.00265   +31.17
  C2  C     2     1    +9.34   0.00085  +0.0109    0.00263   +0.0091     0.00169  +0.0101   0.01177   +144.48
  C3  C     2     2    +6.30   0.01401  +0.0181    0.02512   +0.0070     0.02801  +0.0041   0.03211   +14.59
  C4  C     1     1    +3.15   0.00034  +0.0081    0.00062   +0.0078     0.00069  +0.0078   0.00846   +102.67

  c_R scales LINEARLY in leg count at fixed R (cost = per-leg x
  contracts).  What makes it bite is that R does NOT scale with legs:
  id  view  legs  ctr  cost$   R$         c_R/E_R  eats
  --  ----  ----  ---  ------  ---------  -------  ----
  A1  A     2     2    +6.30   +454.35    0.4362   no
  A2  A     4     4    +12.60  +407.25    0.3418   no
  A3  A     4     4    +12.60  +139.38    5.1199   YES
  A4  A     2     2    +6.30   +287.44    0.1119   no
  B1  B     1     1    +3.15   +134.59    -0.0643  YES
  B2  B     2     2    +6.30   +171.95    0.4492   no
  B3  B     2     2    +6.30   +12063.68  -1.3550  YES
  B4  B     2     3    +9.45   +409.74    -0.1239  YES
  C1  C     1     1    +3.15   +11754.07  0.1361   no
  C2  C     2     1    +9.34   +12271.05  0.0718   no
  C3  C     2     2    +6.30   +454.35    0.4362   no
  C4  C     1     1    +3.15   +12134.48  0.0407   no

  THE LEG COUNT AT WHICH COST CONSUMES THE GROSS EDGE.
  EATEN      = c_R >= E_R while E_R > 0: the gross edge is gone.
  NO-EDGE    = E_R <= 0: there is no gross edge for cost to consume.

    AT LOW prices:
      view A: legs=2 A1 ok (0.436); legs=2 A4 ok (0.112); legs=4 A2 ok (0.342); legs=4 A3 EATEN (5.120)
        first leg count where cost eats the gross edge: legs=4 (A3)
      view B: legs=1 B1 NO-EDGE; legs=2 B2 ok (0.449); legs=2 B3 NO-EDGE; legs=2 B4 NO-EDGE
        first leg count where cost eats the gross edge: NONE
      view C: legs=1 C1 ok (0.136); legs=1 C4 ok (0.041); legs=2 C2 ok (0.072); legs=2 C3 ok (0.436)
        first leg count where cost eats the gross edge: NONE

    AT HIGH prices:
      view A: legs=2 A1 ok (0.782); legs=2 A4 ok (0.201); legs=4 A2 ok (0.613); legs=4 A3 EATEN (9.183)
        first leg count where cost eats the gross edge: legs=4 (A3)
      view B: legs=1 B1 NO-EDGE; legs=2 B2 ok (0.806); legs=2 B3 NO-EDGE; legs=2 B4 NO-EDGE
        first leg count where cost eats the gross edge: NONE
      view C: legs=1 C1 ok (0.244); legs=1 C4 ok (0.073); legs=2 C2 ok (0.224); legs=2 C3 ok (0.782)
        first leg count where cost eats the gross edge: NONE

==============================================================================
TEST 3 -- SKEW SENSITIVITY BY LEG COUNT (the model-risk test)
==============================================================================
  Hypothesis under test: THE MORE STRIKES A STRUCTURE TOUCHES, THE
  MORE ITS ANSWER DEPENDS ON THE SKEW ASSUMPTION.
  Strikes are held FIXED; only the pricing vol of the stated legs
  moves by 1.5 vol points.  `dE` is E_R after minus E_R before.
  id  view  legs  sold  strikes  E_R      dE_sold+1.5  dE_sold-1.5  dE_all+1.5  |dE|$med  ddBudget   dDD_sold-1.5
  --  ----  ----  ----  -------  -------  -----------  -----------  ----------  --------  ---------  ------------
  A1  A     2     1     2        +0.0321  +0.0477      -0.0378      +0.0172     +21.67    -31.69%    -32.03%
  A2  A     4     2     4        +0.0915  +0.1352      -0.0857      +0.0402     +55.06    -31.17%    -58.36%
  A3  A     4     2     4        +0.0271  +1.3680      -0.2924      +0.0620     +190.68   -402.05%   -469.53%
  A4  A     2     2     2        +0.2303  +0.1222      -0.0925      +0.1222     +35.13    -60.45%    -0.57%
  B1  B     1     0     1        -0.4271  +0.0000      +0.0000      -0.0666     +8.96     -1331.22%  +0.00%
  B2  B     2     1     2        +0.0953  +0.1187      -0.0925      -0.0218     +20.40    -188.70%   -63.55%
  B3  B     2     1     2        -0.0005  +0.0015      -0.0015      -0.0000     +17.98    -7.64%     -2.19%
  B4  B     2     1     2        -0.2121  +0.0399      -0.0358      -0.0238     +16.36    -650.38%   -109.19%
  C1  C     1     1     1        +0.0027  +0.0011      -0.0010      +0.0011     +12.95    -2.78%     -0.06%
  C2  C     2     1     1        +0.0118  +0.0015      -0.0015      +0.0015     +18.66    -5.20%     -0.18%
  C3  C     2     1     2        +0.0321  +0.0477      -0.0378      +0.0172     +21.67    -31.69%    -32.03%
  C4  C     1     1     1        +0.0085  +0.0017      -0.0017      +0.0017     +20.83    -4.30%     -0.09%

  ORDERED BY |dE| in R (most skew-sensitive first):
    A3  view A  legs=4  distinct option strikes=4  |dE|max=1.3680 R = +190.68 per trade   |dE|/|E_R|=50.484
    A2  view A  legs=4  distinct option strikes=4  |dE|max=0.1352 R = +55.06 per trade   |dE|/|E_R|=1.478
    A4  view A  legs=2  distinct option strikes=2  |dE|max=0.1222 R = +35.13 per trade   |dE|/|E_R|=0.531
    B2  view B  legs=2  distinct option strikes=2  |dE|max=0.1187 R = +20.40 per trade   |dE|/|E_R|=1.246
    B1  view B  legs=1  distinct option strikes=1  |dE|max=0.0666 R = +8.96 per trade   |dE|/|E_R|=0.156
    C3  view C  legs=2  distinct option strikes=2  |dE|max=0.0477 R = +21.67 per trade   |dE|/|E_R|=1.486
    A1  view A  legs=2  distinct option strikes=2  |dE|max=0.0477 R = +21.67 per trade   |dE|/|E_R|=1.486
    B4  view B  legs=2  distinct option strikes=2  |dE|max=0.0399 R = +16.36 per trade   |dE|/|E_R|=0.188
    C4  view C  legs=1  distinct option strikes=1  |dE|max=0.0017 R = +20.83 per trade   |dE|/|E_R|=0.203
    C2  view C  legs=2  distinct option strikes=1  |dE|max=0.0015 R = +18.66 per trade   |dE|/|E_R|=0.129
    B3  view B  legs=2  distinct option strikes=2  |dE|max=0.0015 R = +17.98 per trade   |dE|/|E_R|=2.916
    C1  view C  legs=1  distinct option strikes=1  |dE|max=0.0011 R = +12.95 per trade   |dE|/|E_R|=0.415

  ORDERED BY |dE| in DOLLARS (the economically meaningful order):
    A3  view A  legs=4  strikes=4  |dE|$=+190.68
    A2  view A  legs=4  strikes=4  |dE|$=+55.06
    A4  view A  legs=2  strikes=2  |dE|$=+35.13
    C3  view C  legs=2  strikes=2  |dE|$=+21.67
    A1  view A  legs=2  strikes=2  |dE|$=+21.67
    C4  view C  legs=1  strikes=1  |dE|$=+20.83
    B2  view B  legs=2  strikes=2  |dE|$=+20.40
    C2  view C  legs=2  strikes=1  |dE|$=+18.66
    B3  view B  legs=2  strikes=2  |dE|$=+17.98
    B4  view B  legs=2  strikes=2  |dE|$=+16.36
    C1  view C  legs=1  strikes=1  |dE|$=+12.95
    B1  view B  legs=1  strikes=1  |dE|$=+8.96

  Pearson(|dE| in R     , leg count)              = 0.6614
  Pearson(|dE| in R     , distinct option strikes)= 0.6675
  Pearson(|dE| in DOLLARS, leg count)             = 0.7528
  Pearson(|dE| in DOLLARS, distinct strikes)      = 0.7495
  HYPOTHESIS HELD (|dE| monotone in leg count): NO

==============================================================================
TEST 4 -- TAIL COMPARISON (did the extra legs buy tail protection?)
==============================================================================
  All the tail columns are in R units so they are comparable across
  structures with different R.  The book is the equal-weight mean of
  the SPY/QQQ/IWM sleeves' curves on a FIXED budget of 10 R; the book
  is NOT compounded, so `ddBudget` is the worst peak-to-trough of the
  CUMULATIVE P&L in R, and worstM/worstY are the SUM of daily returns
  inside the period, also in R.
  `compCAGR` and `compDD` are the COMPOUNDED versions, kept only for
  comparability with the sibling study -- a fixed-budget programme is
  not compounded, so those two are NOT the primary measures.
  id  view  legs  worst1%_R  worst1_R  ddBudget_R  worstM_R  worstY_R  L_act  L_exp  tot_R    compCAGR
  --  ----  ----  ---------  --------  ----------  --------  --------  -----  -----  -------  --------
  A1  A     2     -1.015     -1.015    -3.17       -1.02     -2.77     2      3.0    9.82     +3.49%
  A2  A     4     -1.035     -1.036    -3.12       -1.03     -2.41     3      3.5    28.00    +10.85%
  A3  A     4     -1.625     -1.766    -40.20      -1.54     -10.78    29     12.5   8.29     -4.02%
  A4  A     2     -2.475     -3.231    -6.04       -2.09     -1.23     2      3.3    70.47    +26.72%
  B1  B     1     -1.096     -1.146    -133.12     -1.10     -11.28    22     26.1   -130.69  -46.87%
  B2  B     2     -1.142     -1.182    -18.87      -1.10     -6.34     10     11.4   29.15    +5.73%
  B3  B     2     -0.132     -0.192    -0.76       -0.13     -0.33     12     10.0   -0.16    -0.07%
  B4  B     2     -1.021     -1.035    -65.04      -0.91     -5.78     7      10.4   -64.89   -22.81%
  C1  C     1     -0.089     -0.149    -0.28       -0.08     -0.10     2      2.9    0.81     +0.31%
  C2  C     2     -0.154     -0.213    -0.52       -0.16     -0.27     5      5.9    3.60     +1.40%
  C3  C     2     -1.015     -1.015    -3.17       -1.02     -2.77     2      3.0    9.82     +3.49%
  C4  C     1     -0.137     -0.196    -0.43       -0.14     -0.17     4      4.7    2.59     +1.01%

  STRESS WINDOWS (book total return in R / worst drawdown in R):
  id  view  legs  2008 GFC                2020 COVID                2022 bear
  --  ----  ----  ----------------------  ------------------------  ---------------------
  A1  A     2     2008 GFC -1.3 (-2.6)    2020 COVID 0.2 (-1.8)     2022 bear -2.8 (-2.9)
  A2  A     4     2008 GFC -0.3 (-2.4)    2020 COVID 0.8 (-2.0)     2022 bear -2.4 (-2.6)
  A3  A     4     2008 GFC 0.6 (-3.5)     2020 COVID -10.8 (-12.8)  2022 bear -1.2 (-7.9)
  A4  A     2     2008 GFC -0.1 (-6.0)    2020 COVID 0.5 (-5.6)     2022 bear 0.5 (-2.3)
  B1  B     1     2008 GFC -13.9 (-14.1)  2020 COVID -3.6 (-6.5)    2022 bear -7.0 (-7.1)
  B2  B     2     2008 GFC -6.8 (-9.1)    2020 COVID 6.7 (-3.6)     2022 bear -4.3 (-5.4)
  B3  B     2     2008 GFC -0.4 (-0.5)    2020 COVID 0.0 (-0.3)     2022 bear -0.2 (-0.2)
  B4  B     2     2008 GFC -1.4 (-1.9)    2020 COVID -3.6 (-3.8)    2022 bear -0.4 (-1.2)
  C1  C     1     2008 GFC -0.1 (-0.3)    2020 COVID 0.0 (-0.2)     2022 bear -0.0 (-0.1)
  C2  C     2     2008 GFC -0.3 (-0.5)    2020 COVID 0.3 (-0.3)     2022 bear -0.2 (-0.2)
  C3  C     2     2008 GFC -1.3 (-2.6)    2020 COVID 0.2 (-1.8)     2022 bear -2.8 (-2.9)
  C4  C     1     2008 GFC -0.2 (-0.4)    2020 COVID 0.2 (-0.3)     2022 bear -0.1 (-0.1)

==============================================================================
TEST 5 -- POSITIVITY BY HORIZON PER STRUCTURE (M / Q / Y)
==============================================================================
  `law` is the null Phi(Sharpe_annual * sqrt(period in years)).
  `gap` = law - observed.  A POSITIVE gap is the signature of
  NEGATIVE SKEW: the normal law says the horizon should be positive
  more often than it is.
  id  view  legs  Sharpe  M    M_law  M_gap  Q    Q_law  Q_gap  Y    Y_law  Y_gap  M>Y?
  --  ----  ----  ------  ---  -----  -----  ---  -----  -----  ---  -----  -----  --------
  A1  A     2     0.43    89%  55%    -33.7  80%  58%    -21.9  83%  67%    -16.8  INVERTED
  A2  A     4     0.97    84%  61%    -22.6  81%  69%    -12.8  88%  83%    -4.1
  A3  A     4     0.08    45%  51%    +6.2   54%  52%    -2.3   50%  53%    +3.3
  A4  A     2     1.00    87%  61%    -25.2  86%  69%    -17.1  92%  84%    -7.5
  B1  B     1     -1.04   23%  38%    +15.6  21%  30%    +9.5   4%   15%    +10.7  INVERTED
  B2  B     2     0.33    47%  54%    +6.5   57%  57%    -0.2   54%  63%    +8.9
  B3  B     2     -0.04   54%  49%    -4.1   58%  49%    -8.7   58%  48%    -10.1
  B4  B     2     -2.50   41%  24%    -17.6  17%  11%    -6.1   0%   1%     +0.6   INVERTED
  C1  C     1     0.39    89%  54%    -34.1  85%  58%    -27.7  83%  65%    -18.3  INVERTED
  C2  C     2     0.86    70%  60%    -10.2  79%  67%    -12.9  83%  80%    -3.0
  C3  C     2     0.43    89%  55%    -33.7  80%  58%    -21.9  83%  67%    -16.8  INVERTED
  C4  C     1     0.77    75%  59%    -16.4  77%  65%    -12.5  83%  78%    -5.5

  structures with monthly positivity ABOVE yearly positivity (the inversion): 5 of 12
  by leg count:
    legs=1: 2 of 3 inverted; mean Y gap = -4.4 pp
    legs=2: 3 of 7 inverted; mean Y gap = -6.4 pp
    legs=4: 0 of 2 inverted; mean Y gap = -0.4 pp

==============================================================================
TEST 6 -- WHAT THE EXTRA LEGS ACTUALLY CHANGE: THE GREEK SHAPE
==============================================================================
  Mean position Greeks AT ENTRY per one unit (share-equivalents per
  100 shares).  This is the 'shape' half of the question.
  id  view  legs  net_delta  net_gamma  net_vega  net_theta  R/S (x100)
  --  ----  ----  ---------  ---------  --------  ---------  ----------
  A1  A     2     10.7       -3.10      -4.92     1.91       0.049
  A2  A     4     -0.1       -6.13      -9.50     3.51       0.045
  A3  A     4     -1.2       -6.30      -5.63     2.03       0.021
  A4  A     2     -1.3       -8.09      -23.74    9.25       0.028
  B1  B     1     31.0       5.86       17.05     -6.30      0.013
  B2  B     2     25.1       1.21       3.70      -1.19      0.016
  B3  B     2     60.2       0.20       0.33      0.57       0.968
  B4  B     2     0.9        4.18       11.95     -4.62      0.040
  C1  C     1     15.5       -3.91      -11.65    4.74       0.934
  C2  C     2     69.0       -5.86      -17.05    6.30       0.987
  C3  C     2     10.7       -3.10      -4.92     1.91       0.049
  C4  C     1     46.6       -6.57      -19.29    8.06       0.974

==============================================================================
TEST 7 -- VERDICT: best E_net per unit of tail risk, and does any
==============================================================================
           4-leg beat its 1-/2-leg comparator on E_net?

  View A -- the index stays INSIDE +-1 sigma over the next 30 days   (range)
  id  legs  E_net    worst1%_R  ddBudget_R  E_net/|tail|  E$_10k    u@25k  UNDEF
  --  ----  -------  ---------  ----------  ------------  --------  -----  -----
  A1  2     +0.0181  -1.015     -3.17       0.0178        +181.01   55
  A4  2     +0.2045  -2.475     -6.04       0.0826        +2045.28  86     YES
  A2  4     +0.0602  -1.035     -3.12       0.0582        +602.25   61
  A3  4     -0.1116  -1.625     -40.20      -0.0687       -1116.39  179
    best by edge-per-unit-of-tail: A4 (0.0826, legs=2)
    best by raw E_net           : A4 (+0.2045, legs=2)
    A2 (4 legs) vs A1 (2 legs): dE_net = +0.0421  -> 4-LEG WINS
    A2 (4 legs) vs A4 (2 legs): dE_net = -0.1443  -> 4-leg LOSES
    A3 (4 legs) vs A1 (2 legs): dE_net = -0.1297  -> 4-leg LOSES
    A3 (4 legs) vs A4 (2 legs): dE_net = -0.3162  -> 4-leg LOSES

  View B -- the index RISES over the next 30 days                   (directional)
  id  legs  E_net    worst1%_R  ddBudget_R  E_net/|tail|  E$_10k    u@25k  UNDEF
  --  ----  -------  ---------  ----------  ------------  --------  -----  -----
  B1  1     -0.4546  -1.096     -133.12     -0.4146       -4545.63  185
  B2  2     +0.0525  -1.142     -18.87      0.0459        +524.71   145
  B3  2     -0.0012  -0.132     -0.76       -0.0091       -12.04    2
  B4  2     -0.2384  -1.021     -65.04      -0.2335       -2383.57  61
    best by edge-per-unit-of-tail: B2 (0.0459, legs=2)
    best by raw E_net           : B2 (+0.0525, legs=2)

  View C -- harvest premium with NO directional view               (carry)
  id  legs  E_net    worst1%_R  ddBudget_R  E_net/|tail|  E$_10k   u@25k  UNDEF
  --  ----  -------  ---------  ----------  ------------  -------  -----  -----
  C1  1     +0.0023  -0.089     -0.28       0.0256        +22.91   2
  C4  1     +0.0081  -0.137     -0.43       0.0591        +81.16   2
  C2  2     +0.0109  -0.154     -0.52       0.0709        +109.29  2
  C3  2     +0.0181  -1.015     -3.17       0.0178        +181.01  55
    best by edge-per-unit-of-tail: C2 (0.0709, legs=2)
    best by raw E_net           : C3 (+0.0181, legs=2)

  trades written to out/trades.csv: 11016 rows

==============================================================================
8. INTERNAL CHECKS, THEN DETERMINISM
==============================================================================
  These are checks the study makes on ITSELF.  A failure is printed
  as FAIL and the study does not claim the affected number.
  check                                             result      detail
  ------------------------------------------------  ----------  ---------------------------------------------------------------------------------------------------------------------------
  daily P&L == trade ledger, all 84 sleeves         PASS        worst |gap| = 5.82e-11 (B4/SKEW_ALL_P15/QQQ)
  R-budget large enough for one session             see detail  worst single session: A1 -10%, A2 -11%, A3 -69%, A4 -31%, B1 -29%, B2 -18%, B3 -1%, B4 -9%, C1 -1%, C2 -1%, C3 -10%, C4 -1%
  structures whose 10R budget is TOO SMALL          -           A3 (worst day -69%)
  reported leg count == built leg count             PASS        all 12 structures match
  c_R == 0 at the FREE setting                      PASS        max = 0
  no book return <= -100% (positivity unambiguous)  PASS        worst book day = -0.310
  undefined-call-side structures                    -           A4
  trades the MODEL says cannot lose                 -           none

  The 'TOO SMALL' line above is a FINDING, not a failure: a
  structure whose mark-to-market swing exceeds its terminal maximum
  loss cannot be normalised by that maximum loss.  Its tail columns
  are still valid in R; its compounded CAGR and % columns are not.

  No RNG, no clock, no set iteration, no network.  Two consecutive
  runs of this file produce byte-identical stdout and identical
  out/*.csv.  Verified in README.md section 'Verification'.

  EVERY OPTION NUMBER ABOVE IS [MODELED], NOT [VERIFIED].  This
  study measured the CONSEQUENCES OF AN ASSUMPTION SET, not the
  behaviour of any option that ever traded.
```

---

## 2. The tables, pasted from `out/*.csv`


### `out/structures.csv` -- the pre-registered structures and their headline stats

| sid | view | name | legs | contracts | undefined_up | n_trades | p | b | E_form | E_R | c_R | E_net | R_dollars_med | R_dollars_recent | cap_per_unit | E_net_per_10k | units_at_25k | units_at_25k_recent | E_month_at_25k | R_over_S100 | arb_frac | p_star | b_star | sd_R | n_req | n_under_n_req | L_actual | L_expected | worst_day_budget_frac | n_sold | n_distinct_strikes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | short put spread ~16d / 5-wide | 2 | 2 | False | 918 | 0.8976034858387799 | 0.1807743736213556 | 0.05986719375163069 | 0.03210683212592881 | 0.014005517906491849 | 0.018101314219436962 | 454.35338162037306 | 426.5019021653317 | 454.35338162037306 | 181.0131421943696 | 55 | 58 | 452.341633005577 | 0.036830834736704954 | 0.0 | 0.8469018487698604 | 0.11407766990291268 | 0.2349085169515403 | 214.12264665850535 | False | 2 | 2.993632709718354 | -0.07391754936427143 | 1 | 2 |
| A2 | A | iron condor ~16d shorts / 5-wide wings | 4 | 4 | False | 918 | 0.8572984749455338 | 0.35260094158806354 | 0.15958272443333993 | 0.09149757918046413 | 0.031272291815274966 | 0.06022528736518916 | 407.2489920015487 | 363.2541386758201 | 407.2489920015487 | 602.2528736518916 | 61 | 68 | 1496.1279419210905 | 0.0334240846805931 | 0.0 | 0.7393163565492706 | 0.16645489199491736 | 0.32438556620838843 | 50.27635998586913 | False | 3 | 3.5039533407222767 | -0.08625237958958491 | 2 | 4 |
| A3 | A | iron butterfly ATM short / 5-wide wings | 4 | 4 | False | 918 | 0.41938997821350765 | 1.4509617692808172 | 0.027908803020822104 | 0.027097544869271902 | 0.13873631141122222 | -0.11163876654195032 | 139.38343152778003 | 43.63031831147964 | 139.38343152778003 | -1116.3876654195033 | 179 | 572 | -2785.34639261409 | 0.011678952248535632 | 0.0 | 0.40800310006199275 | 1.3844155844155843 | 1.7802930258638674 | 17265.656017043515 | True | 29 | 12.548278407648915 | -0.3097484258137618 | 2 | 4 |
| A4 | A | short strangle ~16d both sides | 2 | 2 | True | 918 | 0.8769063180827886 | 0.47033136182341667 | 0.2893428608582248 | 0.230292019727974 | 0.025763561492005125 | 0.20452845823596888 | 287.44443300858774 | 966.5277124210572 | 287.44443300858774 | 2045.2845823596888 | 86 | 25 | 5055.988737211248 | 0.025144429922975723 | 0.0 | 0.6801187990439517 | 0.14037267080745347 | 0.47107207178445326 | 16.736973494167906 | False | 2 | 3.256714826067074 | -0.2485776004237079 | 2 | 2 |
| B1 | B | long call ~30d | 1 | 1 | False | 918 | 0.2298474945533769 | 1.464220637752311 | -0.4336050603859067 | -0.4271042835209946 | 0.027458685703341677 | -0.4545629692243363 | 134.58776240717805 | 424.3149681951735 | 134.58776240717805 | -4545.629692243363 | 185 | 58 | -11318.043386697276 | 0.011554348595815164 | 0.0 | 0.40580781796882026 | 3.3507109004739335 | 1.2041708733107237 | 31.79569874986792 | False | 22 | 26.122000794061012 | -0.19730455727993337 | 0 | 1 |
| B2 | B | bull call debit spread ~50d long / ~25d short | 2 | 2 | False | 918 | 0.45098039215686275 | 1.4479312513495348 | 0.10396899570665297 | 0.09526592839615868 | 0.042795142976762 | 0.052470785419396676 | 171.94531164464468 | 539.7171483325706 | 171.94531164464468 | 524.7078541939668 | 145 | 46 | 1308.2053049207288 | 0.014668237234002908 | 0.0 | 0.4085082044067635 | 1.2173913043478262 | 1.210779259885617 | 646.1222982407896 | False | 10 | 11.377513456527055 | -0.13653769114809128 | 1 | 2 |
| B3 | B | risk reversal long ~30d call / short ~30d put | 2 | 2 | False | 918 | 0.49455337690631807 | 0.9633083542295781 | -0.029039223507376477 | -0.0005110906058213612 | 0.0006925168995251955 | -0.001203607505346557 | 12063.683695991076 | 38322.66693644447 | 12063.683695991076 | -12.036075053465568 | 2 | 0 | -29.0398804772435 | 0.970889628648286 | 0.0 | 0.5093443410688333 | 1.0220264317180618 | 0.029356842928883294 | 13197.23326001438 | True | 12 | 9.99863553304368 | -0.009861792209359102 | 1 | 2 |
| B4 | B | call ratio backspread long 2x ~25d / short 1x ~50d | 2 | 3 | False | 918 | 0.4803921568627451 | 0.261687837120632 | -0.3938950586381277 | -0.21207166521905713 | 0.026285415387663703 | -0.23835708060672084 | 409.7365947486537 | 1405.9759107631494 | 409.7365947486537 | -2383.570806067208 | 61 | 17 | -5957.480731063718 | 0.035624224891545 | 0.0 | 0.7925890783588401 | 1.0816326530612244 | 0.40441172285658894 | 14.545952686481005 | False | 7 | 10.420645223362508 | -0.0590439888413672 | 1 | 2 |
| C1 | C | cash-secured put ~16d | 1 | 1 | False | 918 | 0.9030501089324618 | 0.2204636594863047 | 0.10213984064721848 | 0.0026517992838866033 | 0.0003609438097381298 | 0.0022908554741484736 | 11754.073376940301 | 37194.34977525511 | 11754.073376940301 | 22.908554741484735 | 2 | 0 | 53.85376667821305 | 0.9390877844444974 | 0.0 | 0.8193607341171484 | 0.10735826296743067 | 0.01325445178043767 | 99.93145996885616 | False | 2 | 2.9235136041239604 | -0.009014222962136212 | 1 | 1 |
| C2 | C | covered call: long underlying + short ~30d call | 2 | 1 | False | 918 | 0.6840958605664488 | 0.8795099760411916 | 0.28576499450312454 | 0.011773809656189743 | 0.0008450600556014499 | 0.010928749600588292 | 12271.052301372094 | 39122.75188566754 | 12271.052301372094 | 109.28749600588293 | 2 | 0 | 268.21451587483665 | 0.9884456514041848 | 0.0 | 0.5320535739354245 | 0.4617834394904459 | 0.04616595192458469 | 61.499213320669995 | False | 5 | 5.920419938624027 | -0.010374207690050902 | 1 | 1 |
| C3 | C | put spread ~16d / 5-wide (the same instrument as A1) | 2 | 2 | False | 918 | 0.8976034858387799 | 0.1807743736213556 | 0.05986719375163069 | 0.03210683212592881 | 0.014005517906491849 | 0.018101314219436962 | 454.35338162037306 | 426.5019021653317 | 454.35338162037306 | 181.0131421943696 | 55 | 58 | 452.341633005577 | 0.036830834736704954 | 0.0 | 0.8469018487698604 | 0.11407766990291268 | 0.2349085169515403 | 214.12264665850535 | False | 2 | 2.993632709718354 | -0.07391754936427143 | 1 | 2 |
| C4 | C | short ATM put -- the 1-leg carry comparator | 1 | 1 | False | 918 | 0.7625272331154684 | 0.6019170212427793 | 0.22150535388882964 | 0.008460681220132838 | 0.0003441921995151022 | 0.008116489020617736 | 12134.47657234961 | 38515.74706353156 | 12134.47657234961 | 81.16489020617736 | 2 | 0 | 196.9786917408375 | 0.9761728756475543 | 0.0 | 0.624252059712926 | 0.3114285714285714 | 0.03289944797643736 | 60.482056424206526 | False | 4 | 4.745208558513599 | -0.010086666655393508 | 1 | 1 |

### `out/cost_drag.csv` -- cost drag and the break-even cost c_R* = E_R

| sid | view | legs | contracts | cost_dollars_med | R_dollars_med | c_R_LOW | E_net_LOW | c_R_HIGH | E_net_HIGH | c_R_RT | E_net_RT | c_R_star_r | c_R_star_dollars | c_R_over_E_R_LOW | eats_edge |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | 2 | 2 | 6.3 | 454.35338162037306 | 0.014005517906491849 | 0.018101314219436962 | 0.025121008308469507 | 0.006985823817459304 | 0.028011035812983698 | 0.004095796312945113 | 0.03210683212592881 | 14.587847749533386 | 0.43621612532683607 | False |
| A2 | A | 4 | 4 | 12.6 | 407.2489920015487 | 0.031272291815274966 | 0.06022528736518916 | 0.056091571033747116 | 0.03540600814671701 | 0.06254458363054993 | 0.028952995549914193 | 0.09149757918046413 | 37.262296891825905 | 0.34178272360185014 | False |
| A3 | A | 4 | 4 | 12.6 | 139.38343152778003 | 0.13873631141122222 | -0.11163876654195032 | 0.24884449507092304 | -0.22174695020165114 | 0.27747262282244445 | -0.25037507795317254 | 0.027097544869271902 | 3.7769487898571072 | 5.119884922436149 | True |
| A4 | A | 2 | 2 | 6.3 | 287.44443300858774 | 0.025763561492005125 | 0.20452845823596888 | 0.04621083251740607 | 0.18408118721056793 | 0.05152712298401025 | 0.17876489674396376 | 0.230292019727974 | 66.19615903711 | 0.11187344451812795 | False |
| B1 | B | 1 | 1 | 3.15 | 134.58776240717805 | 0.027458685703341677 | -0.4545629692243363 | 0.04925129340440646 | -0.4763555769254011 | 0.05491737140668335 | -0.48202165492767796 | -0.4271042835209946 | -57.48300983361163 | -0.06429035428297672 | True |
| B2 | B | 2 | 2 | 6.3 | 171.94531164464468 | 0.042795142976762 | 0.052470785419396676 | 0.07675954216466847 | 0.0185063862314902 | 0.085590285953524 | 0.009675642442634677 | 0.09526592839615868 | 16.380529747193908 | 0.4492177182045663 | False |
| B3 | B | 2 | 2 | 6.3 | 12063.683695991076 | 0.0006925168995251955 | -0.001203607505346557 | 0.001242133486449957 | -0.0017532240922713182 | 0.001385033799050391 | -0.0018961244048717523 | -0.0005110906058213612 | -6.165635408621357 | -1.3549787290890791 | True |
| B4 | B | 2 | 3 | 9.45 | 409.7365947486537 | 0.026285415387663703 | -0.23835708060672084 | 0.047146856171523796 | -0.25921852139058094 | 0.052570830775327405 | -0.26464249599438455 | -0.21207166521905713 | -86.89352194953297 | -0.12394590932509757 | True |
| C1 | C | 1 | 1 | 3.15 | 11754.073376940301 | 0.0003609438097381298 | 0.0022908554741484736 | 0.0006474071508001375 | 0.0020043921330864657 | 0.0007218876194762596 | 0.0019299116644103437 | 0.0026517992838866033 | 31.16944336372088 | 0.13611279403059245 | False |
| C2 | C | 2 | 1 | 9.3415 | 12271.052301372094 | 0.0008450600556014499 | 0.010928749600588292 | 0.002633012257681388 | 0.009140797398508354 | 0.0016901201112028998 | 0.010083689544986844 | 0.011773809656189743 | 144.47703407750413 | 0.07177456407724273 | False |
| C3 | C | 2 | 2 | 6.3 | 454.35338162037306 | 0.014005517906491849 | 0.018101314219436962 | 0.025121008308469507 | 0.006985823817459304 | 0.028011035812983698 | 0.004095796312945113 | 0.03210683212592881 | 14.587847749533386 | 0.43621612532683607 | False |
| C4 | C | 1 | 1 | 3.15 | 12134.47657234961 | 0.0003441921995151022 | 0.008116489020617736 | 0.0006173606118286757 | 0.007843320608304163 | 0.0006883843990302044 | 0.007772296821102634 | 0.008460681220132838 | 102.66593805182023 | 0.04068138138759684 | False |

### `out/skew_sensitivity.csv` -- the skew / model-risk test

| sid | view | legs | n_sold_legs | n_distinct_strikes | E_R_base | dE_sold_plus1.5 | dE_sold_minus1.5 | dE_all_plus1.5 | abs_dE_max_R | abs_dE_max_dollars | abs_dE_over_absE | dd_budget_base | dd_budget_sold_minus | dd_budget_all_plus | d_dd_sold_minus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | 2 | 1 | 2 | 0.03210683212592881 | 0.04769889515218034 | -0.03784048423192606 | 0.017228351793241753 | 0.04769889515218034 | 21.67215431194876 | 1.4856306896020335 | -0.31685788000101195 | -0.6371430944467896 | -0.2863810768285808 | -0.3202852144457777 |
| A2 | A | 4 | 2 | 4 | 0.09149757918046413 | 0.13519523718569637 | -0.08572991916307372 | 0.04023544810677464 | 0.13519523718569637 | 55.05812406728514 | 1.477582668269788 | -0.3117263310747749 | -0.8953368558670959 | -0.28214705964497133 | -0.583610524792321 |
| A3 | A | 4 | 2 | 4 | 0.027097544869271902 | 1.367995328589345 | -0.2924042946160318 | 0.061983717254588705 | 1.367995328589345 | 190.6758832127559 | 50.48410603945989 | -4.020486777777239 | -8.715779897530581 | -3.7957864480313086 | -4.695293119753342 |
| A4 | A | 2 | 2 | 2 | 0.230292019727974 | 0.122219090832108 | -0.09245561979986608 | 0.122219090832108 | 0.122219090832108 | 35.131197267060365 | 0.5307135304839302 | -0.6044660934199533 | -0.6101352055851592 | -0.6245505420960566 | -0.005669112165205936 |
| B1 | B | 1 | 0 | 1 | -0.4271042835209946 | 0.0 | 0.0 | -0.06660713058374035 | 0.06660713058374035 | 8.96450466562833 | 0.15595050940402527 | -13.312161383641376 | -13.312161383641376 | -15.315967505935125 | 0.0 |
| B2 | B | 2 | 1 | 2 | 0.09526592839615868 | 0.1186544182786562 | -0.09247216556939927 | -0.02184435162604348 | 0.1186544182786562 | 20.402070928937565 | 1.245507394681944 | -1.8870046927269046 | -2.5224699369794052 | -2.036644781375216 | -0.6354652442525006 |
| B3 | B | 2 | 1 | 2 | -0.0005110906058213612 | 0.001490172606824336 | -0.0014557785094288054 | -4.173366685536234e-05 | 0.001490172606824336 | 17.976970981159262 | 2.9156720742881115 | -0.07635878411768192 | -0.09829711228888084 | -0.0767159115543042 | -0.021938328171198923 |
| B4 | B | 2 | 1 | 2 | -0.21207166521905713 | 0.03993299409607415 | -0.03580203012812466 | -0.023807373293423806 | 0.03993299409607415 | 16.362009019043516 | 0.18829952627016813 | -6.503777300630532 | -7.5956554172607 | -7.230155913568152 | -1.0918781166301672 |
| C1 | C | 1 | 1 | 1 | 0.0026517992838866033 | 0.0011015065507313311 | -0.0010244551543019701 | 0.0011015065507313311 | 0.0011015065507313311 | 12.94718882247648 | 0.41538081612153943 | -0.027820215538505756 | -0.02841217612301008 | -0.027396599083957248 | -0.0005919605845043224 |
| C2 | C | 2 | 1 | 1 | 0.011773809656189743 | 0.0015207364679290722 | -0.0014859436866851358 | 0.0015207364679290722 | 0.0015207364679290722 | 18.66103673456151 | 0.12916265103110347 | -0.05195185834148028 | -0.05377112994952592 | -0.050094482557247175 | -0.001819271608045639 |
| C3 | C | 2 | 1 | 2 | 0.03210683212592881 | 0.04769889515218034 | -0.03784048423192606 | 0.017228351793241753 | 0.04769889515218034 | 21.67215431194876 | 1.4856306896020335 | -0.31685788000101195 | -0.6371430944467896 | -0.2863810768285808 | -0.3202852144457777 |
| C4 | C | 1 | 1 | 1 | 0.008460681220132838 | 0.0017168800347767375 | -0.0017093149319197792 | 0.0017168800347767375 | 0.0017168800347767375 | 20.833440559533106 | 0.20292456246800672 | -0.04303666016285396 | -0.043887010960532595 | -0.042251824627191736 | -0.0008503507976786381 |

### `out/tails.csv` -- the tail comparison

| sid | view | legs | contracts | undefined_up | n_trades | worst1pct_R | worst1_trade_R | best_trade_R | dd_budget_R | worst_month_R | worst_month_key | worst_year_R | worst_year_key | best_year_R | L_actual | L_expected | tot_R | tot_budget_frac | cagr_compounded | maxdd_compounded | sharpe | worst_day_budget_frac | R_over_S100 | arb_frac | n_sold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | 2 | 2 | False | 918 | -1.0148613031142877 | -1.0154043378815099 | 0.32258088087344455 | -3.1685788000101196 | -1.0152541816160014 | 2022-09 | -2.7690949964204914 | 2022 | 1.4840462447171363 | 2 | 2.993632709718354 | 9.82469063053424 | 0.982469063053424 | 0.03491763534063064 | -0.2812072900219831 | 0.4266378699540805 | -0.07391754936427143 | 0.036830834736704954 | 0.0 | 1 |
| A2 | A | 4 | 4 | False | 918 | -1.0352999629259443 | -1.0359435371081902 | 0.4522319552483681 | -3.1172633107477488 | -1.0347878000793025 | 2022-09 | -2.4080172425444077 | 2022 | 3.183950733543222 | 3 | 3.5039533407222767 | 27.99825922922192 | 2.799825922922192 | 0.10848334838612272 | -0.2873285188745799 | 0.9695374720401037 | -0.08625237958958491 | 0.0334240846805931 | 0.0 | 2 |
| A3 | A | 4 | 4 | False | 918 | -1.625404469912716 | -1.766029915020821 | 16.675080577023497 | -40.20486777777239 | -1.5443706223692293 | 2026-04 | -10.77744938792078 | 2020 | 7.957534830343043 | 29 | 12.548278407648915 | 8.291848729997092 | 0.8291848729997091 | -0.04023652802648425 | -0.9928671912844695 | 0.08295688636842395 | -0.3097484258137618 | 0.011678952248535632 | 0.0 | 2 |
| A4 | A | 2 | 2 | True | 918 | -2.4751790212811473 | -3.2310215469184262 | 0.5011114949085291 | -6.044660934199532 | -2.090578285910819 | 2001-09 | -1.2279840709724108 | 2008 | 4.508213296290812 | 2 | 3.256714826067074 | 70.46935803675987 | 7.0469358036759875 | 0.2671719367723058 | -0.5037503612616553 | 1.0004934787992756 | -0.2485776004237079 | 0.025144429922975723 | 0.0 | 2 |
| B1 | B | 1 | 1 | False | 918 | -1.0962772042995674 | -1.1457295371868876 | 7.602647760457304 | -133.12161383641376 | -1.1016934800133602 | 2007-03 | -11.283796032806318 | 2008 | 4.821007178176606 | 22 | 26.122000794061012 | -130.69391075742374 | -13.069391075742374 | -0.4686990975299421 | -0.9999999239094535 | -1.0413862366571995 | -0.19730455727993337 | 0.011554348595815164 | 0.0 | 0 |
| B2 | B | 2 | 2 | False | 918 | -1.1419535663050975 | -1.1820242857507994 | 3.1833548899269806 | -18.870046927269048 | -1.0986150840493534 | 2005-08 | -6.340311019167505 | 2008 | 8.502190842868963 | 10 | 11.377513456527055 | 29.151374089224596 | 2.9151374089224595 | 0.057324586116806575 | -0.9044416640323072 | 0.3348266202048835 | -0.13653769114809128 | 0.014668237234002908 | 0.0 | 1 |
| B3 | B | 2 | 2 | False | 918 | -0.1318207262787532 | -0.19168493405014736 | 0.11886253702743078 | -0.7635878411768192 | -0.13183171464160034 | 2008-10 | -0.33125532146369485 | 2008 | 0.15042884021728212 | 12 | 9.99863553304368 | -0.15639372538133656 | -0.015639372538133654 | -0.0007038033869788407 | -0.07430503445870928 | -0.04489446969327645 | -0.009861792209359102 | 0.970889628648286 | 0.0 | 1 |
| B4 | B | 2 | 3 | False | 918 | -1.020724683343307 | -1.0352345471647857 | 1.5002290186179659 | -65.03777300630533 | -0.9080270367667169 | 2007-05 | -5.775141858253422 | 2013 | -0.3561803637609368 | 7 | 10.420645223362508 | -64.89392955703168 | -6.489392955703169 | -0.22810539219892423 | -0.9986919475152722 | -2.49941909241467 | -0.0590439888413672 | 0.035624224891545 | 0.0 | 1 |
| C1 | C | 1 | 1 | False | 918 | -0.08943992998081887 | -0.14934859717654564 | 0.03244156142056746 | -0.27820215538505755 | -0.0840977596942652 | 2008-10 | -0.10172934237507572 | 2008 | 0.1063940888480043 | 2 | 2.9235136041239604 | 0.8114505808693009 | 0.0811450580869301 | 0.0031422013122566206 | -0.027592506802832095 | 0.3853560096489815 | -0.009014222962136212 | 0.9390877844444974 | 0.0 | 1 |
| C2 | C | 2 | 1 | False | 918 | -0.15403665907954103 | -0.21254105012839739 | 0.20365847162590786 | -0.5195185834148028 | -0.15796998187952177 | 2008-10 | -0.2664909906892774 | 2008 | 0.4022488606287483 | 5 | 5.920419938624027 | 3.6027857547940405 | 0.36027857547940406 | 0.014041426814141333 | -0.05109760919505535 | 0.8550083399905362 | -0.010374207690050902 | 0.9884456514041848 | 0.0 | 1 |
| C3 | C | 2 | 2 | False | 918 | -1.0148613031142877 | -1.0154043378815099 | 0.32258088087344455 | -3.1685788000101196 | -1.0152541816160014 | 2022-09 | -2.7690949964204914 | 2022 | 1.4840462447171363 | 2 | 2.993632709718354 | 9.82469063053424 | 0.982469063053424 | 0.03491763534063064 | -0.2812072900219831 | 0.4266378699540805 | -0.07391754936427143 | 0.036830834736704954 | 0.0 | 1 |
| C4 | C | 1 | 1 | False | 918 | -0.13727534553491014 | -0.19590737539695965 | 0.11041791418846528 | -0.43036660162853957 | -0.13941788556337698 | 2008-10 | -0.16950631435662494 | 2008 | 0.29065189248247725 | 4 | 4.745208558513599 | 2.5889684533606454 | 0.25889684533606455 | 0.01008126089322614 | -0.042450679085239806 | 0.768103354337346 | -0.010086666655393508 | 0.9761728756475543 | 0.0 | 1 |

### `out/positivity.csv` -- positivity by horizon and the Phi-law gap

| sid | view | legs | sharpe | pos_M | pos_M_law | pos_M_gap | pos_M_n | pos_Q | pos_Q_law | pos_Q_gap | pos_Q_n | pos_Y | pos_Y_law | pos_Y_gap | pos_Y_n | inverted |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | 2 | 0.4266378699540805 | 0.8856209150326797 | 0.5490096989846482 | -0.33661121604803146 | 306 | 0.803921568627451 | 0.5844608972701901 | -0.21946067135726088 | 102 | 0.8333333333333334 | 0.6651784449122073 | -0.16815488842112603 | 24 | True |
| A2 | A | 4 | 0.9695374720401037 | 0.8366013071895425 | 0.6102157358399667 | -0.22638557134957582 | 306 | 0.8137254901960784 | 0.6860797988972644 | -0.12764569129881398 | 102 | 0.875 | 0.8338614533199292 | -0.041138546680070776 | 24 | False |
| A3 | A | 4 | 0.08295688636842395 | 0.4477124183006536 | 0.5095527932235704 | 0.061840374922916774 | 306 | 0.5392156862745098 | 0.5165427610455661 | -0.022672925228943708 | 102 | 0.5 | 0.5330570894542273 | 0.03305708945422725 | 24 | False |
| A4 | A | 2 | 1.0004934787992756 | 0.8660130718954249 | 0.6136395145646805 | -0.2523735573307444 | 306 | 0.8627450980392157 | 0.6915493243022478 | -0.17119577373696793 | 102 | 0.9166666666666666 | 0.841464124028624 | -0.0752025426380426 | 24 | False |
| B1 | B | 1 | -1.0413862366571995 | 0.22549019607843138 | 0.38185125775362777 | 0.1563610616751964 | 306 | 0.20588235294117646 | 0.3012902845423875 | 0.09540793160121103 | 102 | 0.041666666666666664 | 0.14884816382405186 | 0.1071814971573852 | 24 | True |
| B2 | B | 2 | 0.3348266202048835 | 0.4738562091503268 | 0.5385002559776352 | 0.0646440468273084 | 306 | 0.5686274509803921 | 0.5664775734879908 | -0.002149877492401364 | 102 | 0.5416666666666666 | 0.6311220607967655 | 0.08945539413009884 | 24 | False |
| B3 | B | 2 | -0.04489446969327645 | 0.5359477124183006 | 0.49482988585444543 | -0.04111782656385521 | 306 | 0.5784313725490197 | 0.4910456009358643 | -0.08738577161315536 | 102 | 0.5833333333333334 | 0.48209571247367744 | -0.10123762085965593 | 24 | False |
| B4 | B | 2 | -2.49941909241467 | 0.4117647058823529 | 0.2352947760560748 | -0.17646992982627813 | 306 | 0.16666666666666666 | 0.10570283441741457 | -0.06096383224925209 | 102 | 0.0 | 0.0062198550452336465 | 0.0062198550452336465 | 24 | True |
| C1 | C | 1 | 0.3853560096489815 | 0.8856209150326797 | 0.5442880531697288 | -0.34133286186295086 | 306 | 0.8529411764705882 | 0.576394424865192 | -0.2765467516053962 | 102 | 0.8333333333333334 | 0.6500131650910783 | -0.18332016824225505 | 24 | True |
| C2 | C | 2 | 0.8550083399905362 | 0.6993464052287581 | 0.5974760978884225 | -0.10187030734033564 | 306 | 0.7941176470588235 | 0.6654939257454189 | -0.1286237213134046 | 102 | 0.8333333333333334 | 0.8037267346474328 | -0.029606598685900543 | 24 | False |
| C3 | C | 2 | 0.4266378699540805 | 0.8856209150326797 | 0.5490096989846482 | -0.33661121604803146 | 306 | 0.803921568627451 | 0.5844608972701901 | -0.21946067135726088 | 102 | 0.8333333333333334 | 0.6651784449122073 | -0.16815488842112603 | 24 | True |
| C4 | C | 1 | 0.768103354337346 | 0.7516339869281046 | 0.5877388731757232 | -0.16389511375238142 | 306 | 0.7745098039215687 | 0.6495299269574778 | -0.12497987696409085 | 102 | 0.8333333333333334 | 0.778787107871325 | -0.05454622546200838 | 24 | False |

### `out/verdict.csv` -- the verdict columns

| sid | view | legs | E_net | worst1pct_R | dd_budget_R | edge_per_tail | E_net_per_10k | units_at_25k | R_dollars_med | E_net_$_per_month_at_25k | undefined_up | arb_frac | worst_day_budget_frac |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | 2 | 0.018101314219436962 | -1.0148613031142877 | -3.1685788000101196 | 0.017836244385207877 | 181.0131421943696 | 55 | 454.35338162037306 | 452.341633005577 | False | 0.0 | -0.07391754936427143 |
| A2 | A | 4 | 0.06022528736518916 | -1.0352999629259443 | -3.1172633107477488 | 0.058171824130063374 | 602.2528736518916 | 61 | 407.2489920015487 | 1496.1279419210905 | False | 0.0 | -0.08625237958958491 |
| A3 | A | 4 | -0.11163876654195032 | -1.625404469912716 | -40.20486777777239 | -0.06868368372823862 | -1116.3876654195033 | 179 | 139.38343152778003 | -2785.34639261409 | False | 0.0 | -0.3097484258137618 |
| A4 | A | 2 | 0.20452845823596888 | -2.4751790212811473 | -6.044660934199532 | 0.08263178399520589 | 2045.2845823596888 | 86 | 287.44443300858774 | 5055.988737211248 | True | 0.0 | -0.2485776004237079 |
| B1 | B | 1 | -0.4545629692243363 | -1.0962772042995674 | -133.12161383641376 | -0.41464236184201725 | -4545.629692243363 | 185 | 134.58776240717805 | -11318.043386697276 | False | 0.0 | -0.19730455727993337 |
| B2 | B | 2 | 0.052470785419396676 | -1.1419535663050975 | -18.870046927269048 | 0.04594826529520901 | 524.7078541939668 | 145 | 171.94531164464468 | 1308.2053049207288 | False | 0.0 | -0.13653769114809128 |
| B3 | B | 2 | -0.001203607505346557 | -0.1318207262787532 | -0.7635878411768192 | -0.0091306393108574 | -12.036075053465568 | 2 | 12063.683695991076 | -29.0398804772435 | False | 0.0 | -0.009861792209359102 |
| B4 | B | 2 | -0.23835708060672084 | -1.020724683343307 | -65.03777300630533 | -0.23351750427549192 | -2383.570806067208 | 61 | 409.7365947486537 | -5957.480731063718 | False | 0.0 | -0.0590439888413672 |
| C1 | C | 1 | 0.0022908554741484736 | -0.08943992998081887 | -0.27820215538505755 | 0.025613341542639473 | 22.908554741484735 | 2 | 11754.073376940301 | 53.85376667821305 | False | 0.0 | -0.009014222962136212 |
| C2 | C | 2 | 0.010928749600588292 | -0.15403665907954103 | -0.5195185834148028 | 0.0709490173695921 | 109.28749600588293 | 2 | 12271.052301372094 | 268.21451587483665 | False | 0.0 | -0.010374207690050902 |
| C3 | C | 2 | 0.018101314219436962 | -1.0148613031142877 | -3.1685788000101196 | 0.017836244385207877 | 181.0131421943696 | 55 | 454.35338162037306 | 452.341633005577 | False | 0.0 | -0.07391754936427143 |
| C4 | C | 1 | 0.008116489020617736 | -0.13727534553491014 | -0.43036660162853957 | 0.05912561348136365 | 81.16489020617736 | 2 | 12134.47657234961 | 196.9786917408375 | False | 0.0 | -0.010086666655393508 |

### `out/shape_greeks.csv` -- what the extra legs change: the Greek shape

| sid | view | legs | mean_net_delta | mean_net_gamma | mean_net_vega | mean_net_theta | mean_R_over_S100 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | 2 | 10.74853265901343 | -3.098173210638065 | -4.920548189963389 | 1.9067306502929655 | 0.048916831546211945 |
| A2 | A | 4 | -0.08742182518054491 | -6.129066707791662 | -9.50104774516662 | 3.506283331130502 | 0.04507816923205609 |
| A3 | A | 4 | -1.2413857718671881 | -6.2979070525334135 | -5.631731741472016 | 2.0308499683353713 | 0.021223188636751454 |
| A4 | A | 2 | -1.2940366034317847 | -8.086407476667071 | -23.74326868351815 | 9.254762382279587 | 0.027705151732176348 |
| B1 | B | 1 | 31.0359796626725 | 5.855274703144206 | 17.053751937634193 | -6.302269203101076 | 0.01259178673072462 |
| B2 | B | 2 | 25.082969363037645 | 1.2073607558027446 | 3.695154862572507 | -1.1895760146142949 | 0.015977767879623204 |
| B3 | B | 2 | 60.224532356685614 | 0.20337156206588955 | 0.33254128829305996 | 0.5699703782342261 | 0.9683531682204781 |
| B4 | B | 2 | 0.8935396808112395 | 4.176312814705411 | 11.952436826975369 | -4.6163366431877515 | 0.039807703177769355 |
| C1 | C | 1 | 15.502401230474343 | -3.908055228768356 | -11.651173823613522 | 4.7384309214675575 | 0.9335697385409039 |
| C2 | C | 2 | 68.96402033732738 | -5.855274703144206 | -17.053751937634193 | 6.302269203101076 | 0.9874082132692754 |
| C3 | C | 2 | 10.74853265901343 | -3.098173210638065 | -4.920548189963389 | 1.9067306502929655 | 0.048916831546211945 |
| C4 | C | 1 | 46.646312525741294 | -6.568177688584796 | -19.285610676527 | 8.056133198669585 | 0.973581187041462 |

### `out/stress_windows.csv` -- the stress windows, in R

| sid | view | legs | window | tot_R | dd_R |
| --- | --- | --- | --- | --- | --- |
| A1 | A | 2 | 2008 GFC | -1.27126589132956 | -2.562849090267982 |
| A1 | A | 2 | 2020 COVID | 0.17818253551868443 | -1.8205733736640872 |
| A1 | A | 2 | 2022 bear | -2.7690949964204914 | -2.9336668856152586 |
| A2 | A | 4 | 2008 GFC | -0.2630568873469837 | -2.356598742160021 |
| A2 | A | 4 | 2020 COVID | 0.7663764128628575 | -1.9702632339216397 |
| A2 | A | 4 | 2022 bear | -2.4080172425444077 | -2.5814671915482967 |
| A3 | A | 4 | 2008 GFC | 0.5509224940183315 | -3.512637521352727 |
| A3 | A | 4 | 2020 COVID | -10.77744938792078 | -12.789638966334442 |
| A3 | A | 4 | 2022 bear | -1.2120869551722833 | -7.948841132218644 |
| A4 | A | 2 | 2008 GFC | -0.12298627454924996 | -6.044660934199527 |
| A4 | A | 2 | 2020 COVID | 0.5428813029625463 | -5.568937570241936 |
| A4 | A | 2 | 2022 bear | 0.5012276202961281 | -2.25764244580829 |
| B1 | B | 1 | 2008 GFC | -13.945539220364893 | -14.136195132904287 |
| B1 | B | 1 | 2020 COVID | -3.557028234666955 | -6.507399226349689 |
| B1 | B | 1 | 2022 bear | -7.0077760094865225 | -7.0888135548640285 |
| B2 | B | 2 | 2008 GFC | -6.791382647046865 | -9.087808969999283 |
| B2 | B | 2 | 2020 COVID | 6.714588594297457 | -3.5954503008805565 |
| B2 | B | 2 | 2022 bear | -4.340615942886426 | -5.3711156137748 |
| B3 | B | 2 | 2008 GFC | -0.36493129048024425 | -0.5064637442788125 |
| B3 | B | 2 | 2020 COVID | 0.012564188125009524 | -0.3099146483581308 |
| B3 | B | 2 | 2022 bear | -0.20262328298767926 | -0.2246489641529348 |
| B4 | B | 2 | 2008 GFC | -1.4397716180661002 | -1.8926158273432403 |
| B4 | B | 2 | 2020 COVID | -3.567217274337102 | -3.844035873361469 |
| B4 | B | 2 | 2022 bear | -0.3561803637609368 | -1.1869451882042423 |
| C1 | C | 1 | 2008 GFC | -0.06315524950282082 | -0.2782021553850575 |
| C1 | C | 1 | 2020 COVID | 0.0032992286488030863 | -0.21360509959280627 |
| C1 | C | 1 | 2022 bear | -0.026359009862403117 | -0.07705758539229902 |
| C2 | C | 2 | 2008 GFC | -0.2657371016001884 | -0.5070733619182373 |
| C2 | C | 2 | 2020 COVID | 0.3257991674995785 | -0.3435858725597926 |
| C2 | C | 2 | 2022 bear | -0.16361251514331865 | -0.22027389665207978 |
| C3 | C | 2 | 2008 GFC | -1.27126589132956 | -2.562849090267982 |
| C3 | C | 2 | 2020 COVID | 0.17818253551868443 | -1.8205733736640872 |
| C3 | C | 2 | 2022 bear | -2.7690949964204914 | -2.9336668856152586 |
| C4 | C | 1 | 2008 GFC | -0.16699187434212842 | -0.43036660162853957 |
| C4 | C | 1 | 2020 COVID | 0.1526794526574465 | -0.30160046433387 |
| C4 | C | 1 | 2022 bear | -0.10970418674827136 | -0.14699329214526358 |

### Kept out of this file, by path

- `out/trades.csv` -- every trade, every structure, every index, every variant, **11016 rows**.  Not pasted here; read the file.
- `out/ledger.csv` -- per-trade strikes, credit, cost, R and P&L, **11016 rows**.  Not pasted here; read the file.

---

## 3. The raw stdout of the INDEPENDENT `handcheck.py`

This program does **not** import `study.py`.  It re-implements the spec from
`data/*.csv` with its own CSV reader, its own Black-Scholes, its own delta
solver, its own vol context, its own structure builder, its own maximum-loss
scan, its own month grid and its own simulator.  It also prints a by-hand
Black-Scholes price with every intermediate, a by-hand `c_R`, and a by-hand
settlement of one 4-leg iron condor against the real path.

```text

==============================================================================
HANDCHECK -- independent re-derivation for the leg-count test
==============================================================================
This file does NOT import study.py.  Every number below is produced
by code written a second time from the same pre-registration.

window: 6436 sessions, 2001-03-13 .. 2026-10-14

------------------------------------------------------------------------------
A. BY HAND: ONE BLACK-SCHOLES PRICE, EVERY INTERMEDIATE SHOWN
------------------------------------------------------------------------------
  inputs   : S=100.0000  K=95.0000  T=0.08219178  r=0.0400  sigma=0.2000  PUT
  sigma*sqrt(T)    = 0.05733821790809959
  ln(S/K)          = 0.05129329438755048
  d1               = 0.9805815961525242
  d2               = 0.9232433782444246
  N(-d1)           = 0.16339955678520623
  N(-d2)           = 0.17794019389203058
  exp(-rT)         = 0.9967177272404354
  K*exp(-rT)*N(-d2) = 16.84883383587478
  S*N(-d1)          = 16.339955678520624
  PUT = difference  = 0.5088781573541539

  A reader with a calculator should get 0.5088781574.

------------------------------------------------------------------------------
B. BY HAND: ONE LEG OF EACH STRUCTURE, RE-PRICED AND COMPARED WITH
   THE LEDGER'S OWN credit COLUMN (first SPY trade of each)
------------------------------------------------------------------------------
  id   entry      iv        legs built by hand                      hand credit$       ledger$        gap
  A1   2001-04-02 0.27040   P109.0@-1 P104.0@+1                        60.612811     60.612811  -2.89e-08
  A2   2001-04-02 0.27040   P109.0@-1 P104.0@+1 C126.5@-1 C131.5@+1    103.973953    103.973953   1.06e-07
  A3   2001-04-02 0.27040   P116.7@-1 C116.7@-1 P111.7@+1 C121.7@+1    387.652862    387.652862   2.95e-07
  A4   2001-04-02 0.27040   P109.0@-1 C126.5@-1                       147.741155    147.741155   3.36e-07
  B1   2001-04-02 0.27040   C122.1@+1                                -148.639238   -148.639238   2.23e-07
  B2   2001-04-02 0.27040   C117.4@+1 C123.5@-1                      -197.618296   -197.618296  -1.35e-07
  B3   2001-04-02 0.27040   C122.1@+1 P112.9@-1                        36.519798     36.519798   2.54e-07
  B4   2001-04-02 0.27040   C123.5@+2 C117.4@-1                        81.477461     81.477461  -2.56e-07
  C1   2001-04-02 0.27040   P109.0@-1                                  82.611700     82.611700   3.77e-07
  C2   2001-04-02 0.27040   S116.3@+1 C122.1@-1                       148.639238    148.639238  -2.23e-07
  C3   2001-04-02 0.27040   P109.0@-1 P104.0@+1                        60.612811     60.612811  -2.89e-08
  C4   2001-04-02 0.27040   P116.7@-1                                 347.968533    347.968533   4.43e-07
  worst |gap| across the 12 structures = 4.428e-07

  WORKED EXAMPLE, one leg: structure A1, first SPY trade
    the strike is solved from the SIGNAL close on the base vol:
      S_sig (signal close) = 116.690000
      iv  = VIX(t-3)/100 * kappa = 0.270400
      T   = calendar days / 365   = 0.07671233
      r   = US03M(t-3)/100, floored at 0 = 0.042400
      K   = 108.973017   (solved to the pre-registered delta target)
      delta of that leg   = -0.1711179313065757
    priced at the ENTRY open S = 116.300000:
      sigma*sqrt(T)    = 0.07489266255187879
      d1               = 0.9497567579015372
      d2               = 0.8748640953496585
      N(d1)            = 0.8288820686934243
      N(d2)            = 0.8091760714097045
      N(-d1)           = 0.1711179313065757
      N(-d2)           = 0.1908239285902955
      exp(-rT)         = 0.9967526812421148
      PER SHARE      = 0.8261170037725165
      LEG CASH FLOW  = qty x 100 x price = +82.6117003773  (qty -1)

------------------------------------------------------------------------------
C. BY HAND: c_R FOR ONE STRUCTURE AT ONE COST SETTING
------------------------------------------------------------------------------
  structure A2 (iron condor) on SPY, first trade 2001-04-02 -> 2001-04-30:
    credit per share        = 1.03973953
    contracts (sum |qty|)   = 4
    fee per contract / side = $0.6500
    half-spread / share     = $0.0250  -> $2.50 per contract
    all-in per contract     = $3.1500  (ONE side each)
    cost = 3.1500 x 4        = $12.600000
    R = (wing - credit) x 100 = $396.026047
    HAND c_R = cost / R       = 0.03181609
    LEDGER cost               = $12.600000
    LEDGER R                  = $396.026047
    LEDGER c_R                = 0.03181609
    gap cost = 0.000e+00    gap c_R = 1.318e-16
    same trade at HIGH prices : per contract $5.6500, cost $22.6000,
      c_R = 0.05706695
    same trade at the skill's ROUND-TRIP convention (2 tickets/leg):
      cost $25.2000, c_R = 0.06363218

------------------------------------------------------------------------------
D. BY HAND: SETTLE ONE 4-LEG IRON CONDOR AGAINST THE REAL PATH
------------------------------------------------------------------------------
  SPY 2001-04-02 (entry) -> 2001-04-30 (expiry close)
  signal close S_sig = 116.690000   entry open S = 116.300000
  expiry REAL close S = 124.910000
  T at entry = 0.07671233   r = 0.042400   iv = 0.270400
  kind           K   qty  entry px/share     intrinsic      leg P&L $
  P       108.9730    -1      0.82611700    0.00000000        82.6117
  P       103.9730     1      0.21998889    0.00000000       -21.9989
  C       126.4764    -1      0.65129455    0.00000000        65.1295
  C       131.4764     1      0.21768313    0.00000000       -21.7683
  credit received at entry  = $103.973953
  terminal intrinsic net    = $0.000000
  credit + intrinsic net    = $103.973953
  BY-HAND GROSS trade P&L   = $103.973953
  ledger GROSS P&L (FREE)   = $103.973953
  gap                       = 0.000e+00
  ledger cost (LOW)         = $12.600000
  BY-HAND NET = gross - cost = $91.373953
  ledger NET P&L (LOW)       = $91.373953
  gap                       = 0.000e+00
  BY-HAND R                 = $396.026047
  ledger  R                 = $396.026047
  gap                       = -1.592e-12
  worst gap across all four = 1.592e-12
  (The by-hand P&L is GROSS; the LOW ledger row is NET of cost, so the
   two differ by exactly the $12.6000 cost -- both comparisons are shown.)

------------------------------------------------------------------------------
E. INDEPENDENT RE-DERIVATION OF THE HEADLINE TABLE
   (pooled SPY/QQQ/IWM, LOW cost) vs out/structures.csv
------------------------------------------------------------------------------
  id    legs        p       b       E_R       c_R     E_net     R$med    gap_p    gap_E   gap_cR
  A1       2 0.897603  0.1808  0.032107  0.014006  0.018101    454.35  0.0e+00  0.0e+00  0.0e+00
  A2       4 0.857298  0.3526  0.091498  0.031272  0.060225    407.25  0.0e+00  0.0e+00  0.0e+00
  A3       4 0.419390  1.4510  0.027098  0.138736 -0.111639    139.38  0.0e+00  0.0e+00  0.0e+00
  A4       2 0.876906  0.4703  0.230292  0.025764  0.204528    287.44  0.0e+00  0.0e+00  0.0e+00
  B1       1 0.229847  1.4642 -0.427104  0.027459 -0.454563    134.59  0.0e+00  0.0e+00  0.0e+00
  B2       2 0.450980  1.4479  0.095266  0.042795  0.052471    171.95  0.0e+00  0.0e+00  0.0e+00
  B3       2 0.494553  0.9633 -0.000511  0.000693 -0.001204  12063.68  0.0e+00  0.0e+00  0.0e+00
  B4       2 0.480392  0.2617 -0.212072  0.026285 -0.238357    409.74  0.0e+00  0.0e+00  0.0e+00
  C1       1 0.903050  0.2205  0.002652  0.000361  0.002291  11754.07  0.0e+00  0.0e+00  0.0e+00
  C2       2 0.684096  0.8795  0.011774  0.000845  0.010929  12271.05  0.0e+00  0.0e+00  0.0e+00
  C3       2 0.897603  0.1808  0.032107  0.014006  0.018101    454.35  0.0e+00  0.0e+00  0.0e+00
  C4       1 0.762527  0.6019  0.008461  0.000344  0.008116  12134.48  0.0e+00  0.0e+00  0.0e+00

  trades pooled per structure = 918
  worst absolute gap across p, b, E_R, c_R, R$med = 0.000e+00
  p is a ratio of two integers; the compared CSV columns are
  6-decimal rounded, so 1e-10 is float noise and 1e-7 is rounding.

------------------------------------------------------------------------------
F. INDEPENDENT CHECK: EVERY TRADE IN out/trades.csv, ALL 12
   STRUCTURES x 3 INDEXES, LOW COST, 13 FIELDS PER TRADE
------------------------------------------------------------------------------
  trades matched  : 11016
  rows missing    : 0
  worst field gap : 5.000e-05  (C1/SPY/2005-01-03 theta)

------------------------------------------------------------------------------
G. INDEPENDENT CHECK: DAILY CURVE AND LEDGER ARE THE SAME MONEY,
   AND THE POSITIVITY SIGNS ARE UNAMBIGUOUS
------------------------------------------------------------------------------
  worst |sum(daily) - sum(trade pnl)| over 36 sleeves = 4.366e-11
  worst single daily return over 36 sleeves             = -0.6929
  No daily return reaches -1, so a period's SUM sign is also its
  compounded sign and the positivity column is unambiguous.

==============================================================================
HANDCHECK PASSED
==============================================================================
What was verified: the Black-Scholes engine, the delta solver, the
lagged-VIX context, the structure builders, the R convention, the
cost arithmetic, the expiry settlement, the daily mark loop, and the
headline p / b / E_R / c_R / E_net, all re-derived from data/*.csv by
code that does not import study.py.

What was NOT verified, and cannot be with these sources: that any
modelled option price resembles any price that ever existed.  These
are constructions from VIX, not quotations.
```
