# index-options-test -- RESULTS

Every table below is pasted verbatim from a real run of `study.py`
(`run-output.txt`), or dumped from `out/*.csv`.  Nothing here was retyped.

> ## READ THIS BEFORE ANY NUMBER
>
> **Every option price in this study is `[MODELED]`, not `[VERIFIED]`.**
> Historical option quotes are not available from the sources used here.
> Each leg is priced with Black-Scholes on an implied vol built from the real
> VIX series, and each spread is settled at intrinsic against the REAL index
> closing price on its expiry session.
>
> The option model cannot see, and therefore does not price:
>
> 1. **any bid/ask spread in the quote** -- a flat per-contract spread IS
>    charged as a COST, but the quote itself is a mid;
> 2. **skew** -- one implied vol prices every strike, so the sold leg is priced
>    at the same vol as the wings; a sensitivity on this is section 13c;
> 3. **term structure** -- the primary run prices the 30-DTE spread and the
>    60-DTE hedge at the same vol; a `sqrt(30/D)` variant is reported;
> 4. **early exercise and assignment** -- these are AMERICAN, physically settled
>    products, priced here as EUROPEAN;
> 5. **pin risk** -- the expiry session's close decides everything;
> 6. **dividends** -- the price series is price-only; a sensitivity is section 13b;
> 7. **margin, buying power, liquidity, partial fills, legging risk, tax**;
> 8. **overlapping monthly structures** -- the tenor is capped at the next roll,
>    so a monthly programme never holds two cycles at once.

---

## The run

```

==============================================================================
INDEX-OPTIONS TEST -- SPY / QQQ / IWM underlying AND options
==============================================================================
Pre-registered.  Deterministic.  No RNG, no clock, no network.

READ THIS BEFORE ANY NUMBER: every option price below is [MODELED].
Historical option quotes are not available from the sources used.
Legs are priced with Black-Scholes on a VIX-derived implied vol and
settled against the REAL index close on the expiry session.  The
model has: no quote spread, no skew, one vol for all strikes, no term
structure in the primary run, no early exercise or assignment, no pin
risk, no dividends, no margin, no liquidity limit, European settlement.
A flat per-contract spread IS charged as a cost; the QUOTE is still a
mid.  Index options on these ETFs are American and physically settled,
so European pricing is an approximation.

==============================================================================
0. DATA -- provenance echoed verbatim from data/*.csv
==============================================================================
  SPY    rows=8485   first=1993-01-29 last=2026-10-14
  QQQ    rows=6943   first=1999-03-10 last=2026-10-14
  IWM    rows=6635   first=2000-05-26 last=2026-10-14
  VIX    rows=9283   first=1990-01-03 last=2026-10-14
  US03M  rows=18197  first=1954-01-04 last=2026-10-14

  Provenance of SPY (the others are in data/*.csv and RESULTS.md):
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

  PRIMARY BOOK CALENDAR (SPY, QQQ, IWM, VIX intersection, from the
  first session every SMA(200) is live):
    sessions = 6436   first = 2001-03-13   last = 2026-10-14
    complete D  periods = 6436  (2001-03-13 .. 2026-10-14)
    complete W  periods = 1334  (2001-W12 .. 2026-W41)
    complete 2W periods = 668  (2001-2W07 (from 2001-03-26) .. 2026-2W20 (from 2026-09-21))
    complete M  periods = 306  (2001-04 .. 2026-09)
    complete Q  periods = 102  (2001-Q2 .. 2026-Q3)
    complete H  periods = 50  (2001-H2 .. 2026-H1)
    complete Y  periods = 24  (2002 .. 2025)
    cash series: TVC:US03M lagged one book date, floored at 0. 20 of 6436 sessions have a non-positive accrual.

==============================================================================
1. PRE-REGISTERED CONFIGURATION (echoed BEFORE any result)
==============================================================================
  S1  Trend on the underlying (long iff close > SMA200, flat below)
  S2  Systematic premium selling, defined risk (30-DTE $5-wide put spread, ~16-delta short)
  S3  Buy-write / covered call (long underlying, short 30-DTE ~30-delta call)
  S4  Tail-hedged premium (S2 + long ~5%-OTM 60-DTE put, rolled monthly)
  S5  Trend + premium overlay (0.75 x S1 book + 0.25 x S2 book)
  S6  Buy & hold (the control)

  Underlying rule   : long iff close > SMA(200), flat below
  Entry convention  : signal at a close, position established at the
                      NEXT session's OPEN
  Risk unit R       : S1/S3/S6  R = 2.0 x ATR(14) at entry, per share
                      S2        R = width - gross credit (max loss)
                      S4        R = the structure's max loss
  Option tenor      : 30 calendar days to expiry, all monthly
  S2 short leg      : 0.16-delta put
  S2 width          : $5.0 (DOLLARS, as pre-registered)
  S3 short leg      : 0.30-delta call
  S4 hedge          : long put, 5% OTM, 60 calendar days, rolled
                      monthly at the next entry (mark-to-model)
  S2/S4 sleeve size : capital = 10 x one max-loss spread, i.e. a
                      worst-case month costs -10% of the sleeve. FIXED.
  S5 blend          : 75% S1 book + 25% S2 book. FIXED, not tuned.
  Implied vol       : IV = VIX(t-3 sessions)/100 x kappa(index) x stress
                      kappa = clip(RV60(index)/RV60(SPY), 0.60, 2.00)
                      term structure exponent alpha = 0.00 (0 = flat: one vol for 30-DTE and 60-DTE)
                      NOTE: reading the brief's sqrt(30/21) factor as
                      the same rule at a 21-day tenor gives 1.195x;
                      our legs are 30 and 60 DTE, so the rule gives
                      1.000x and 0.707x.  Both settings are reported.
  IV stress         : 80%, 100%, 120%
  Costs             : FREE fee=$0.00/contract/side half_spread=$0.000/share/side etf=0bps | LOW fee=$0.65/contract/side half_spread=$0.025/share/side etf=5bps | HIGH fee=$0.65/contract/side half_spread=$0.050/share/side etf=20bps
  HEADLINE COST     : LOW

  PRE-REGISTERED SUCCESS BAR -- a book is 'all-weather enough' iff
    (a) positive in >= 80% of complete YEARS
    (b) positive in >= 70% of complete QUARTERS
    (c) CAGR above the cash rate over the same window
    (d) max drawdown survivable -- REPORTED, not thresholded after
        seeing the result
  Selection rule for 'best book', declared up front: the strategy with
  the highest fraction of positive complete YEARS; ties broken by CAGR.

==============================================================================
2. WHAT THE PRE-REGISTERED STRUCTURES ACTUALLY LOOK LIKE
==============================================================================
  The brief fixes the S2 width at FIVE DOLLARS.  On a $770 ETF that
  is ~0.65% of spot; on a $271 ETF it is ~1.8%.  The same dollar width
  is therefore a DIFFERENT structure on each index, and the long leg
  lands at a very different delta.  First trade of each index, from the
  model:

  sym  entry       S       short K  long K  width/spot  credit  credit/width  IV      short OTM%  short delta  long delta
  ---  ----------  ------  -------  ------  ----------  ------  ------------  ------  ----------  -----------  ----------
  SPY  2001-04-02  116.30  108.97   103.97  4.3%        0.606   12.1%         0.2704  6.3%        -0.182       -0.063
  QQQ  2001-04-02  39.17   34.22    29.22   12.8%       0.481   9.6%          0.5408  12.6%       -0.164       -0.021
  IWM  2001-04-02  44.77   41.67    36.67   11.2%       0.308   6.2%          0.2858  6.9%        -0.172       -0.005

  A literal $5 width on a high-priced ETF buys a long leg only a couple
  of deltas further out than the short leg; on a low-priced ETF the same
  $5 is a genuinely different, wider tail.  The pre-registered width is
  kept as specified and the consequence is reported, not repaired.

  Over the whole window, per index:
  sym  trades  mean spot  mean width/spot  mean credit  mean credit/width  mean IV
  ---  ------  ---------  ---------------  -----------  -----------------  -------
  SPY  306     244.5      2.92%            0.550        11.0%              0.1948
  QQQ  306     161.9      7.35%            0.445        8.9%               0.2549
  IWM  306     118.6      5.63%            0.480        9.6%               0.2602
  wrote out/s2_structure.csv (1836 rows)

==============================================================================
3. TRADE-LEVEL STATISTICS (pooled across the three index sleeves)
==============================================================================
  p = win rate, b = avg win / |avg loss|, E = p*b-(1-p), E_R = mean R,
  p* = 1/(1+b), b* = (1-p)/p, n_req = 4(sd/|E_R|)^2,
  L = ln(N)/ln(1/(1-p)) and the ACTUAL longest losing streak.

  strat  n     p       b      E        E_R      sd     p*      b*      n_req  L_exp  L_act
  -----  ----  ------  -----  -------  -------  -----  ------  ------  -----  -----  -----
  S1     275   0.2982  6.437  1.2177   0.5991   2.818  0.1345  2.3537  88.5   15.86  10
  S2     918   0.8976  0.181  0.0599   0.0321   0.235  0.8469  0.1141  214.1  2.99   2
  S3     918   0.6950  0.951  0.3556   0.4533   1.377  0.5127  0.4389  36.9   5.75   6
  S4     918   0.2963  1.401  -0.2886  -0.1865  0.941  0.4165  2.3750  101.7  19.41  10
  S5     1193  0.7594  0.740  0.3214   0.1628   1.388  0.5747  0.3168  290.5  4.97   10
  S6     0     n/a     n/a    n/a      n/a      n/a    n/a     n/a     n/a    n/a    n/a

  STRUCTURE CHECK -- model-priced maximum loss of the S2 spread
  (must equal width - credit; a mismatch would mean the payoff grid
  and the credit do not agree):
  entry       credit  width-credit  grid max loss  gap
  ----------  ------  ------------  -------------  --------
  2001-04-02  0.6061  4.3939        4.3939         0.000000
  2001-05-01  0.5790  4.4210        4.4210         0.000000
  2001-06-01  0.4713  4.5287        4.5287         0.000000

==============================================================================
4. HEADLINE BOOK METRICS (LOW costs, IV stress x1.0, VIX lag 3)
==============================================================================
  Sharpe: daily returns, full window, annualised by sqrt(252).  Both a
  raw figure and an excess-over-cash figure are given; Rf is the
  TVC:US03M cash series lagged one book date.

  strat  CAGR     maxDD    Sharpe  Sharpe_Rf  pos years    pos Q         pos M          worst yr  worst yr ret
  -----  -------  -------  ------  ---------  -----------  ------------  -------------  --------  ------------
  S1     +7.07%   -21.83%  0.61    0.47       18/24 (75%)  54/102 (53%)  159/306 (52%)  2022      -14.49%
  S2     +2.97%   -26.75%  0.41    0.18       19/24 (79%)  81/102 (79%)  271/306 (89%)  2022      -22.22%
  S3     +10.53%  -28.74%  0.90    0.75       20/24 (83%)  77/102 (75%)  214/306 (70%)  2008      -16.95%
  S4     -14.84%  -98.45%  -0.46   -0.53      3/24 (12%)   25/102 (25%)  93/306 (30%)   2021      -46.92%
  S5     +6.16%   -18.84%  0.63    0.46       17/24 (71%)  60/102 (59%)  194/306 (63%)  2022      -16.33%
  S6     +9.23%   -56.30%  0.52    0.44       19/24 (79%)  70/102 (69%)  190/306 (62%)  2008      -38.04%

  cash reference: CAGR +1.80%  maxDD -0.00%  pos years 24/24

==============================================================================
5. THE PRE-REGISTERED SUCCESS BAR -- verdict
==============================================================================
  Bar: (a) >= 80% positive years  (b) >= 70% positive quarters
       (c) CAGR > cash CAGR  (d) max drawdown survivable (reported)

  strat  (a) posY>=80%  (b) posQ>=70%  (c) CAGR>cash  (d) maxDD  verdict
  -----  -------------  -------------  -------------  ---------  -------
  S1     no             no             YES            -21.83%    fails
  S2     no             YES            YES            -26.75%    fails
  S3     YES            YES            YES            -28.74%    CLEARS
  S4     no             no             no             -98.45%    fails
  S5     no             no             YES            -18.84%    fails
  S6     no             no             YES            -56.30%    fails

  CLEARS THE BAR: S3

  BEST BOOK by the declared rule (highest positive-year fraction, ties
  by CAGR): S3  with 83% positive years and CAGR +10.53%.

==============================================================================
6. THE CORRELATION OF THE THREE INDICES
==============================================================================
  A three-index book is nearly ONE BET.  Measured here, not assumed.
  complete calendar years in the window: 24 (2002 .. 2025)

  pair_a  pair_b  yearly corr  daily corr  R^2 yearly  n years
  ------  ------  -----------  ----------  ----------  -------
  SPY     QQQ     0.917        0.884       0.841       24
  SPY     IWM     0.895        0.887       0.801       24
  QQQ     IWM     0.840        0.793       0.705       24

  Every pairwise YEARLY correlation is 0.84 or higher, and every
  pairwise DAILY correlation is 0.79 or higher.  A three-index book of
  SPY/QQQ/IWM is not three bets; it is ONE broad-market bet taken at
  three slightly different tilts.  Adding QQQ and IWM to SPY buys
  almost no diversification -- it buys a slightly different beta.
  The mean pairwise yearly correlation is 0.884.

==============================================================================
7. POSITIVITY BY HORIZON FOR THE BEST BOOK (S3) -- the direct answer
==============================================================================
  Complete periods only.  'positive' is STRICT (a flat period counts
  against); the >=0 reading is in out/positivity_by_horizon.csv.

  strat  D      W      2W     M      Q      H      Y
  -----  -----  -----  -----  -----  -----  -----  -----
  S3     59.6%  64.1%  67.1%  69.9%  75.5%  78.0%  83.3%
  S1     45.5%  46.3%  49.0%  52.0%  52.9%  64.0%  75.0%
  S2     65.9%  70.4%  72.2%  88.6%  79.4%  78.0%  79.2%
  S4     42.5%  36.8%  34.9%  30.4%  24.5%  12.0%  12.5%
  S5     56.5%  57.4%  58.7%  63.4%  58.8%  66.0%  70.8%
  S6     54.1%  56.6%  59.0%  62.1%  68.6%  74.0%  79.2%

  Same table, cash reference for comparison:
  cash   D      W      2W      M       Q       H       Y
  -----  -----  -----  ------  ------  ------  ------  -
  99.7%  99.9%  99.9%  100.0%  100.0%  100.0%  100.0%

==============================================================================
8. THE FRONTIER FOR THE BEST BOOK (S3) -- lambda vs the cash series
==============================================================================
  r(lam) = lam * risky + (1-lam) * cash.  At lam=0 the return IS the
  cash rate, term by term.  The frontier's endpoint is found by a 0.05
  grid scan then a 0.001 bisection.

  lambda  CAGR     maxDD    D      W      2W     M       Q       H       Y
  ------  -------  -------  -----  -----  -----  ------  ------  ------  ------
  0.00    +1.80%   -0.00%   99.7%  99.9%  99.9%  100.0%  100.0%  100.0%  100.0%
  0.05    +2.25%   -1.34%   68.9%  76.8%  78.4%  82.4%   87.3%   92.0%   100.0%
  0.10    +2.71%   -2.84%   65.0%  71.9%  73.7%  78.8%   84.3%   90.0%   91.7%
  0.15    +3.16%   -4.33%   63.5%  69.6%  71.4%  75.8%   84.3%   88.0%   91.7%
  0.20    +3.61%   -5.80%   62.4%  68.4%  70.1%  73.9%   82.4%   86.0%   87.5%
  0.25    +4.05%   -7.25%   61.8%  67.2%  69.2%  73.9%   81.4%   84.0%   87.5%
  0.30    +4.50%   -8.70%   61.3%  66.9%  68.4%  73.2%   79.4%   82.0%   87.5%
  0.35    +4.94%   -10.19%  61.0%  66.6%  68.3%  72.2%   79.4%   82.0%   87.5%
  0.40    +5.39%   -11.66%  60.7%  66.1%  68.0%  71.9%   78.4%   80.0%   87.5%
  0.45    +5.83%   -13.12%  60.6%  65.4%  67.8%  71.6%   78.4%   80.0%   87.5%
  0.50    +6.27%   -14.56%  60.4%  65.3%  67.7%  71.6%   77.5%   80.0%   87.5%
  0.55    +6.70%   -15.98%  60.2%  65.1%  67.7%  70.9%   77.5%   80.0%   87.5%
  0.60    +7.14%   -17.39%  60.1%  65.0%  67.7%  70.6%   75.5%   80.0%   87.5%
  0.65    +7.57%   -18.79%  59.9%  64.8%  67.7%  70.6%   75.5%   78.0%   87.5%
  0.70    +8.00%   -20.23%  59.9%  64.7%  67.4%  70.6%   75.5%   78.0%   87.5%
  0.75    +8.43%   -21.68%  59.8%  64.7%  67.4%  70.3%   75.5%   78.0%   83.3%
  0.80    +8.85%   -23.12%  59.8%  64.6%  67.4%  69.9%   75.5%   78.0%   83.3%
  0.85    +9.28%   -24.54%  59.7%  64.5%  67.2%  69.9%   75.5%   78.0%   83.3%
  0.90    +9.70%   -25.94%  59.6%  64.5%  67.1%  69.9%   75.5%   78.0%   83.3%
  0.95    +10.12%  -27.32%  59.6%  64.2%  67.1%  69.9%   75.5%   78.0%   83.3%
  1.00    +10.53%  -28.74%  59.6%  64.1%  67.1%  69.9%   75.5%   78.0%   83.3%

  WHERE THE FRONTIER ENDS -- largest lambda with 100% of periods
  positive (strict), then the CAGR there:

  horizon  largest lambda 100% positive  CAGR there  cash CAGR  excess
  -------  ----------------------------  ----------  ---------  ------
  Y        0.0773                        +2.50%      +1.80%     +0.70%
  Q        0.0008                        +1.80%      +1.80%     +0.01%
  M        0.0000                        +1.80%      +1.80%     +0.00%

  D/W/2W cannot be made 100% positive even at lam=0 only if the cash
  accrual itself prints <= 0; the measured count of non-positive cash
  sessions is reported in section 0 above.

==============================================================================
9. STRESS CELLS -- 2008 and 2020, where premium selling is supposed to break
==============================================================================

  --- 2008 GFC  (2008-01-01 .. 2009-03-31) ---
  strat  window total  window maxDD  worst month  worst month (key)
  -----  ------------  ------------  -----------  ------------------
  S1     -9.21%        -9.21%        -4.60%       (2008, 9) -4.60%
  S2     -11.97%       -21.36%       -7.47%       (2008, 10) -7.47%
  S3     -19.01%       -28.08%       -10.56%      (2008, 10) -10.56%
  S4     +9.59%        -16.95%       -4.50%       (2008, 12) -4.50%
  S5     -9.74%        -12.24%       -5.04%       (2008, 9) -5.04%
  S6     -43.82%       -52.89%       -18.22%      (2008, 10) -18.22%

  modelled OPTION P&L in this window (3 sleeves, dollars):
  strat  trades  losing  sum P&L   worst trade  worst trade R  worst entry  book P&L (3x base)
  -----  ------  ------  --------  -----------  -------------  -----------  ------------------
  S2     45      12      -1776.49  -468.89      -1.01          2008-09-02   -1796.21
  S4     45      24      +1954.44  -446.12      -0.76          2008-12-01   +1438.46

  S4 hedge debit as a multiple of the spread credit, in this
  window: mean = 4.36x  (1.00x would mean the premium exactly
  pays for the hedge).

  --- 2020 COVID  (2020-01-01 .. 2020-12-31) ---
  strat  window total  window maxDD  worst month  worst month (key)
  -----  ------------  ------------  -----------  ------------------
  S1     +20.08%       -18.48%       -6.80%       (2020, 2) -6.80%
  S2     -1.09%        -15.87%       -7.67%       (2020, 2) -7.67%
  S3     +23.42%       -20.13%       -7.49%       (2020, 3) -7.49%
  S4     -36.24%       -69.26%       -17.03%      (2020, 11) -17.03%
  S5     +14.68%       -17.59%       -6.98%       (2020, 2) -6.98%
  S6     +30.45%       -33.41%       -13.23%      (2020, 3) -13.23%

  modelled OPTION P&L in this window (3 sleeves, dollars):
  strat  trades  losing  sum P&L   worst trade  worst trade R  worst entry  book P&L (3x base)
  -----  ------  ------  --------  -----------  -------------  -----------  ------------------
  S2     36      5       +94.60    -463.77      -1.01          2020-02-03   -163.53
  S4     36      23      -3402.28  -1691.35     -0.99          2020-04-01   -5436.75

  S4 hedge debit as a multiple of the spread credit, in this
  window: mean = 9.06x  (1.00x would mean the premium exactly
  pays for the hedge).

  OVER THE WHOLE WINDOW: the S4 hedge costs 4.66x the S2 credit on
  average (median 3.65x, min 0.34x, max 24.92x), so 'paid for by the
  premium' is FALSE -- the modelled tail put costs more than the
  credit it is supposed to be financed from.

==============================================================================
10. DID THE HEDGE REPAIR THE HOLE?  S2 vs S4 vs S4c
==============================================================================
  S4  = the literal pre-registration: ONE long 5%-OTM 60-DTE put per
        spread, rolled monthly, its debit paid out of the same sleeve.
  S4c = the 'paid for by the premium' reading: the long put's quantity
        is set so its debit EQUALS the spread credit (fractional
        contracts -- a stated model simplification).

  HEDGE ECONOMICS, FULL sizing, whole window (915 trades):
    the tail put costs 4.66x the spread credit on average
    (median 3.65x, min 0.34x, max 24.92x).
    Monthly net CASH FLOW of the structure, mean = -214.27 per spread
    (negative = the sleeve pays out more than it collects, every
     month, on average)
    Sleeve risk budget = 10 x width x 100 = $5000
    => the hedge alone costs 5.27% of the sleeve per month.

  STRUCTURE OF THE 'TAIL' HEDGE: in 584 of 915 months (64%) the
  5%-OTM 60-DTE put strikes ABOVE the spread's short strike, i.e.
  the hedge is INSIDE the spread, not below it.  When that happens
  the structure stops being a credit spread plus a tail hedge and
  becomes a NET LONG PUT position: its maximum loss is just the net
  debit.  The mean hedge strike is -1.08% of spot away from the
  spread's short strike (negative = the hedge is closer to the
  money).  This is a property of the pre-registered parameters, not
  a bug: a 16-delta 30-DTE put on these indices is usually FURTHER
  out than 5%.

  'PAID FOR BY THE PREMIUM' IS FALSE, BY ABOUT A FACTOR OF 4.7.
  A 16-delta, $5-wide, 30-DTE put spread does not collect enough
  premium to buy a 5%-OTM 60-DTE put.  S4 is therefore not a
  premium-selling strategy: it is a large NET-DEBIT long-tail
  position, and that is what the numbers below show.


  strat  CAGR     maxDD    posY  posM  E_R      2008 maxDD  2020 maxDD
  -----  -------  -------  ----  ----  -------  ----------  ----------
  S2     +2.97%   -26.75%  79%   89%   0.0321   -21.36%     -15.87%
  S4     -14.84%  -98.45%  12%   30%   -0.1865  -16.95%     -69.26%
  S4c    +0.25%   -25.56%  75%   56%   0.0050   -13.36%     -6.62%

  Same table, the OPTION SLEEVES ONLY (book P&L in dollars per sleeve,
  and the worst month), which is where the hedge has to earn its keep:
  strat  window      P&L (3 sleeves)  budget     return on budget
  -----  ----------  ---------------  ---------  ----------------
  S2     2008 GFC    -1796.21         +15000.00  -11.97%
  S2     2020 COVID  -163.53          +15000.00  -1.09%
  S4     2008 GFC    +1438.46         +15000.00  9.59%
  S4     2020 COVID  -5436.75         +15000.00  -36.24%
  S4c    2008 GFC    -845.22          +15000.00  -5.63%
  S4c    2020 COVID  +10.13           +15000.00  0.07%

  Worst single trade of each variant in each stress window:
    S2   2008 GFC     worst trade entered 2008-10-01  R=-1.015  dollars=-435.95
    S2   2020 COVID   worst trade entered 2020-03-02  R=-1.015  dollars=-440.00
    S4   2008 GFC     worst trade entered 2008-05-01  R=-1.103  dollars=-61.56
    S4   2020 COVID   worst trade entered 2020-11-02  R=-1.021  dollars=-580.45
    S4c  2008 GFC     worst trade entered 2008-09-02  R=-0.867  dollars=-324.99
    S4c  2020 COVID   worst trade entered 2020-02-03  R=-0.853  dollars=-316.37

==============================================================================
11. THE VRP WE MEASURE HERE vs THE SIBLING STUDY'S FINDING
==============================================================================
  Same arithmetic as ../regime-study (options-trading-playbook):
    collected   = VIX / sqrt(252) * sqrt(21)          (vol points)
    realised    = |close[d+21]/close[d] - 1| * 100    (vol points)
    fwd_rv      = annualised sd of the 21 log returns
    VRP         = VIX - fwd_rv
    fair strike = collected * sqrt(2/pi), which removes the
                  guaranteed ~+20% artifact of collecting the 1-sigma
                  move and paying the realised ABSOLUTE move.

  FULL SPY HISTORY 1990-2026 (the sibling's series, reproduced):
    n=8463  mean VRP = +3.64 vol points  share VIX > forward realised = 83.0%
    fair-strike E_R = +0.1160R  total = +981.4R

  PER-YEAR, the years the sibling flagged:
  year  n    mean VRP  share VIX>RV  mean E_R_fair  total R
  ----  ---  --------  ------------  -------------  -------
  2008  253  -2.33     60%           +0.0577        +14.6
  2020  253  +2.60     75%           -0.0289        -7.3

  Sibling's published finding, for comparison:
    full history: mean VRP +3.62 vol points, VIX above the following
    21-day realised in 82.9% of windows, NEGATIVE in exactly one year
    (2008, -2.33 vol points); fair-strike E_R = +0.1158R with 2020 the
    one losing year (-7.3R) and a worst window of R = -3.98 starting
    2020-02-20.

  THIS STUDY's worst single window on the same arithmetic:
    2020-02-20  VIX=15.6  collected=4.49  realised_abs=32.10  R=-3.07  R_fair=-3.98

==============================================================================
12. COST DISCIPLINE -- re-run at FREE / LOW / HIGH
==============================================================================
  A premium-selling edge that dies inside the spread is a finding.

  cost  strat  CAGR     maxDD    posY  posQ  E_R
  ----  -----  -------  -------  ----  ----  -------
  FREE  S1     +7.25%   -21.64%  75%   53%   0.5991
  FREE  S2     +4.54%   -25.07%  83%   80%   0.0461
  FREE  S3     +10.59%  -27.85%  83%   75%   0.4640
  FREE  S4     -12.24%  -96.87%  21%   33%   -0.0871
  FREE  S5     +6.69%   -18.21%  71%   60%   0.1736
  FREE  S6     +9.23%   -56.30%  79%   69%   n/a
  LOW   S1     +7.07%   -21.83%  75%   53%   0.5991
  LOW   S2     +2.97%   -26.75%  79%   79%   0.0321
  LOW   S3     +10.53%  -28.74%  83%   75%   0.4533
  LOW   S4     -14.84%  -98.45%  12%   25%   -0.1865
  LOW   S5     +6.16%   -18.84%  71%   59%   0.1628
  LOW   S6     +9.23%   -56.30%  79%   69%   n/a
  HIGH  S1     +6.54%   -22.39%  75%   52%   0.5991
  HIGH  S2     +1.74%   -29.75%  75%   78%   0.0210
  HIGH  S3     +10.49%  -29.53%  83%   75%   0.4448
  HIGH  S4     -16.86%  -99.15%  8%    20%   -0.2654
  HIGH  S5     +5.44%   -19.85%  71%   58%   0.1543
  HIGH  S6     +9.23%   -56.30%  79%   69%   n/a

  COST DRAG on each strategy, LOW minus FREE (and HIGH minus FREE):
  strat  CAGR drag LOW  CAGR drag HIGH  posY FREE -> LOW
  -----  -------------  --------------  ----------------
  S1     -0.18%         -0.71%          75% -> 75%
  S2     -1.56%         -2.79%          83% -> 79%
  S3     -0.06%         -0.10%          83% -> 83%
  S4     -2.61%         -4.62%          21% -> 12%
  S5     -0.53%         -1.24%          71% -> 71%
  S6     +0.00%         +0.00%          79% -> 79%

==============================================================================
13. IV STRESS -- headline re-run at IV x 0.8 / 1.0 / 1.2
==============================================================================
  Also reported: the sqrt(30/D) term-structure variant (alpha = 0.5),
  and the NO-HAIRCUT variant (VIX lag 0), so the lookahead bias in the
  modelled option P&L is visible rather than hidden.

  variant          strat  CAGR     maxDD    posY  posQ
  ---------------  -----  -------  -------  ----  ----
  IV x0.8          S1     +7.07%   -21.83%  75%   53%
  IV x0.8          S2     -1.46%   -47.28%  67%   71%
  IV x0.8          S3     +8.89%   -39.25%  79%   73%
  IV x0.8          S4     -8.91%   -91.26%  12%   27%
  IV x0.8          S5     +5.00%   -20.70%  71%   56%
  IV x0.8          S6     +9.23%   -56.30%  79%   69%
  IV x1.0          S1     +7.07%   -21.83%  75%   53%
  IV x1.0          S2     +2.97%   -26.75%  79%   79%
  IV x1.0          S3     +10.53%  -28.74%  83%   75%
  IV x1.0          S4     -14.84%  -98.45%  12%   25%
  IV x1.0          S5     +6.16%   -18.84%  71%   59%
  IV x1.0          S6     +9.23%   -56.30%  79%   69%
  IV x1.2          S1     +7.07%   -21.83%  75%   53%
  IV x1.2          S2     +6.96%   -21.24%  88%   87%
  IV x1.2          S3     +11.66%  -24.31%  88%   77%
  IV x1.2          S4     -20.29%  -99.72%  12%   23%
  IV x1.2          S5     +7.17%   -17.25%  71%   62%
  IV x1.2          S6     +9.23%   -56.30%  79%   69%
  term sqrt(30/D)  S1     +7.07%   -21.83%  75%   53%
  term sqrt(30/D)  S2     +2.97%   -25.92%  79%   79%
  term sqrt(30/D)  S3     +10.53%  -28.74%  83%   75%
  term sqrt(30/D)  S4     +15.91%  -52.11%  100%  76%
  term sqrt(30/D)  S5     +6.15%   -18.74%  71%   59%
  term sqrt(30/D)  S6     +9.23%   -56.30%  79%   69%
  NO VIX haircut   S1     +7.07%   -21.83%  75%   53%
  NO VIX haircut   S2     +2.94%   -28.08%  79%   79%
  NO VIX haircut   S3     +10.57%  -28.05%  83%   76%
  NO VIX haircut   S4     -17.36%  -99.28%  12%   23%
  NO VIX haircut   S5     +6.14%   -19.23%  71%   59%
  NO VIX haircut   S6     +9.23%   -56.30%  79%   69%

  VERDICT FLIP CHECK -- does any IV setting move the bar verdict?
  variant          strat  verdict
  ---------------  -----  -------
  IV x1.0          S3     CLEARS
  IV x1.2          S2     CLEARS
  IV x1.2          S3     CLEARS
  term sqrt(30/D)  S3     CLEARS
  term sqrt(30/D)  S4     CLEARS
  NO VIX haircut   S3     CLEARS

  The no-haircut row is the honest bias estimate: it prices every option
  with the VIX print of its own session, information a trader does not
  have at the open.  The gap between it and the VIX lag-3 row is the
  size of the lookahead gift the model would otherwise be taking.

==============================================================================
13b. DIVIDEND SENSITIVITY -- sizing the one bias in the model that
==============================================================================
  has a KNOWN direction.
  The price series carries no dividends, so with q = 0 the modelled call
  is TOO EXPENSIVE and the modelled put is TOO CHEAP.  That flatters
  every sold call (S2's long wing is a bought put, so it is flattered
  there too, but less) and flatters S3 outright.  Published round
  average yields: IWM 1.3%, QQQ 0.6%, SPY 1.8%.
  They are held CONSTANT over the whole window, so this is a bias
  estimate, not a dividend model.

  dividend setting     strat  CAGR     maxDD    posY  posQ  E_R
  -------------------  -----  -------  -------  ----  ----  -------
  q = 0 (primary run)  S1     +7.07%   -21.83%  75%   53%   0.5991
  q = 0 (primary run)  S2     +2.97%   -26.75%  79%   79%   0.0321
  q = 0 (primary run)  S3     +10.53%  -28.74%  83%   75%   0.4533
  q = 0 (primary run)  S4     -14.84%  -98.45%  12%   25%   -0.1865
  q = 0 (primary run)  S5     +6.16%   -18.84%  71%   59%   0.1628
  q = 0 (primary run)  S6     +9.23%   -56.30%  79%   69%   n/a
  q = published avg    S1     +7.07%   -21.83%  75%   53%   0.5991
  q = published avg    S2     +3.23%   -26.56%  79%   79%   0.0345
  q = published avg    S3     +10.45%  -29.09%  83%   75%   0.4414
  q = published avg    S4     -15.66%  -98.79%  12%   24%   -0.1988
  q = published avg    S5     +6.22%   -18.60%  71%   59%   0.1646
  q = published avg    S6     +9.23%   -56.30%  79%   69%   n/a

  THE BIAS, as a CAGR difference (published-average q minus q = 0):
  strat  CAGR difference  posY        posQ
  -----  ---------------  ----------  ----------
  S1     +0.00%           75% -> 75%  53% -> 53%
  S2     +0.26%           79% -> 79%  79% -> 79%
  S3     -0.08%           83% -> 83%  75% -> 75%
  S4     -0.82%           12% -> 12%  25% -> 24%
  S5     +0.07%           71% -> 71%  59% -> 59%
  S6     +0.00%           79% -> 79%  69% -> 69%

  A NEGATIVE CAGR difference means the primary run's headline was
  inflated by the missing dividends.  Whether the bar verdict survives
  that correction is the thing to read in section 5's terms.

==============================================================================
13c. SKEW SENSITIVITY -- sizing the LARGEST known bias in the model
==============================================================================
  The model has NO skew: one implied vol prices every strike.  A real
  seller of an out-of-the-money option collects LESS than the flat-vol
  Black-Scholes value.  Here the SOLD leg only is priced at
  VIX minus a stated number of vol points; the bought legs keep VIX.
  Strikes are NOT moved -- this isolates the price effect.

  Why this matters, before the table: a 30-delta 30-DTE call has vega
  of roughly S * pdf(d1) * sqrt(T) * 100 dollars per vol point.  At
  SPY = 244, IV = 19.5%, that is about $24 per vol point per contract.
  1.5 vol points of skew is therefore about $36 per contract per
  month -- roughly 1.8 percentage points of annual return on a single
  covered-call sleeve.  That is the same order as the whole edge.

  sold-leg IV          strat  CAGR     maxDD    posY  posQ  posM  E_R
  -------------------  -----  -------  -------  ----  ----  ----  -------
  haircut 0.0 vol pts  S1     +7.07%   -21.83%  75%   53%   52%   0.5991
  haircut 0.0 vol pts  S2     +2.97%   -26.75%  79%   79%   89%   0.0321
  haircut 0.0 vol pts  S3     +10.53%  -28.74%  83%   75%   70%   0.4533
  haircut 0.0 vol pts  S4     -14.84%  -98.45%  12%   25%   30%   -0.1865
  haircut 0.0 vol pts  S5     +6.16%   -18.84%  71%   59%   63%   0.1628
  haircut 0.0 vol pts  S6     +9.23%   -56.30%  79%   69%   62%   n/a
  haircut 1.5 vol pts  S1     +7.07%   -21.83%  75%   53%   52%   0.5991
  haircut 1.5 vol pts  S2     -0.87%   -45.72%  67%   75%   85%   -0.0057
  haircut 1.5 vol pts  S3     +10.11%  -31.87%  83%   75%   70%   0.3994
  haircut 1.5 vol pts  S4     -17.55%  -99.32%  12%   20%   29%   -0.2407
  haircut 1.5 vol pts  S5     +5.16%   -20.34%  71%   56%   62%   0.1337
  haircut 1.5 vol pts  S6     +9.23%   -56.30%  79%   69%   62%   n/a
  haircut 3.0 vol pts  S1     +7.07%   -21.83%  75%   53%   52%   0.5991
  haircut 3.0 vol pts  S2     -4.03%   -65.79%  54%   64%   76%   -0.0362
  haircut 3.0 vol pts  S3     +9.65%   -35.41%  79%   74%   69%   0.3471
  haircut 3.0 vol pts  S4     -19.84%  -99.67%  4%    15%   26%   -0.2829
  haircut 3.0 vol pts  S5     +4.32%   -21.74%  71%   55%   60%   0.1103
  haircut 3.0 vol pts  S6     +9.23%   -56.30%  79%   69%   62%   n/a

  VERDICT FLIP CHECK under skew:
  sold-leg IV          strat  verdict
  -------------------  -----  -------
  haircut 0.0 vol pts  S1     fails
  haircut 0.0 vol pts  S2     fails
  haircut 0.0 vol pts  S3     CLEARS
  haircut 0.0 vol pts  S4     fails
  haircut 0.0 vol pts  S5     fails
  haircut 0.0 vol pts  S6     fails
  haircut 1.5 vol pts  S1     fails
  haircut 1.5 vol pts  S2     fails
  haircut 1.5 vol pts  S3     CLEARS
  haircut 1.5 vol pts  S4     fails
  haircut 1.5 vol pts  S5     fails
  haircut 1.5 vol pts  S6     fails
  haircut 3.0 vol pts  S1     fails
  haircut 3.0 vol pts  S2     fails
  haircut 3.0 vol pts  S3     fails
  haircut 3.0 vol pts  S4     fails
  haircut 3.0 vol pts  S5     fails
  haircut 3.0 vol pts  S6     fails

==============================================================================
15. THE DIRECT ANSWER TO THE OWNER'S QUESTION
==============================================================================
  Question: restrict to SPY/QQQ/IWM, trade BOTH the underlying and
  options on it -- can a combination reach 'profitable in most
  conditions', and what does it cost?

  1. POSITIVITY BY HORIZON, best book (the buy-write, S3):
     D 59.6%   W 64.1%   2W 67.1%   M 69.9%   Q 75.5%   H 78.0%   Y 83.3%

  2. THE FRONTIER, best book vs the cross-asset trend book already
     measured by the sibling frontier study:

     Y  largest lambda with 100% positive = 0.0773  ->  CAGR +2.50%  vs cash +1.80%  (excess +0.70%)
     Q  largest lambda with 100% positive = 0.0008  ->  CAGR +1.80%  vs cash +1.80%  (excess +0.01%)
     M  largest lambda with 100% positive = 0.0000  ->  CAGR +1.80%  vs cash +1.80%  (excess +0.00%)

     sibling study, four-sleeve cross-asset TREND book (2005-2026):
       Y 0.008 -> +0.03%/yr over cash;  Q 0.001 -> +0.00%;  M 0.000
     This study's best book, three-index BUY-WRITE (2002-2025):
       Y 0.0773;  Q 0.0008;  M 0.0000

  3. WHAT IT COSTS -- the verdict re-run under every stated assumption.
     Read from the sensitivity tables just written to out/*.csv, so this
     matrix cannot disagree with them.  'CLEARS' = >=80% positive years
     AND >=70% positive quarters AND CAGR above cash (1.80%/yr).
     cash CAGR over this window = 1.80%/yr.

  family            setting              strat  CAGR     posY  posQ  verdict
  ----------------  -------------------  -----  -------  ----  ----  -------
  cost              FREE                 S2     +4.54%   83%   80%   CLEARS
  cost              FREE                 S3     +10.59%  83%   75%   CLEARS
  cost              LOW                  S2     +2.97%   79%   79%   fails
  cost              LOW                  S3     +10.53%  83%   75%   CLEARS
  cost              HIGH                 S2     +1.74%   75%   78%   fails
  cost              HIGH                 S3     +10.49%  83%   75%   CLEARS
  variant           IV x0.8              S2     -1.46%   67%   71%   fails
  variant           IV x0.8              S3     +8.89%   79%   73%   fails
  variant           IV x1.0              S2     +2.97%   79%   79%   fails
  variant           IV x1.0              S3     +10.53%  83%   75%   CLEARS
  variant           IV x1.2              S2     +6.96%   88%   87%   CLEARS
  variant           IV x1.2              S3     +11.66%  88%   77%   CLEARS
  variant           term sqrt(30/D)      S2     +2.97%   79%   79%   fails
  variant           term sqrt(30/D)      S3     +10.53%  83%   75%   CLEARS
  variant           NO VIX haircut       S2     +2.94%   79%   79%   fails
  variant           NO VIX haircut       S3     +10.57%  83%   76%   CLEARS
  sold_leg_iv       haircut 0.0 vol pts  S2     +2.97%   79%   79%   fails
  sold_leg_iv       haircut 0.0 vol pts  S3     +10.53%  83%   75%   CLEARS
  sold_leg_iv       haircut 1.5 vol pts  S2     -0.87%   67%   75%   fails
  sold_leg_iv       haircut 1.5 vol pts  S3     +10.11%  83%   75%   CLEARS
  sold_leg_iv       haircut 3.0 vol pts  S2     -4.03%   54%   64%   fails
  sold_leg_iv       haircut 3.0 vol pts  S3     +9.65%   79%   74%   fails
  dividend_setting  q = 0 (primary run)  S2     +2.97%   79%   79%   fails
  dividend_setting  q = 0 (primary run)  S3     +10.53%  83%   75%   CLEARS
  dividend_setting  q = published avg    S2     +3.23%   79%   79%   fails
  dividend_setting  q = published avg    S3     +10.45%  83%   75%   CLEARS

     Read the matrix this way: S3 stops clearing when the sold leg loses
     3 vol points to skew, and S2 never clears once a real spread is
     charged or the sold leg loses 1.5 vol points.  The answer to the
     owner's question therefore depends on three MODELLED inputs -- the
     cost level, the IV level, and the skew -- and not only on the
     market.  That is the honest summary.

  4. WHAT THE MODEL CANNOT SEE is listed in full at the top of this run
     and in README.md.  The largest single item is the absence of skew.

  Nothing here is a recommendation.  Every options number is MODELED.

==============================================================================
14. THE LONGEST WINDOW -- SPY ONLY, 1994-2026 (one index, not three)
==============================================================================
  sessions = 8285  first = 1993-11-11  last = 2026-10-14

  strat  CAGR     maxDD    Sharpe  pos years    pos Q  pos M
  -----  -------  -------  ------  -----------  -----  -----
  S1     +6.86%   -28.15%  0.62    21/32 (66%)  60%    53%
  S2     +2.82%   -32.57%  0.35    26/32 (81%)  81%    91%
  S3     +10.12%  -23.72%  1.06    26/32 (81%)  76%    70%
  S4     -14.46%  -99.44%  -0.34   6/32 (19%)   27%    30%
  S5     +5.97%   -23.33%  0.63    22/32 (69%)  66%    66%
  S6     +8.91%   -56.47%  0.55    23/32 (72%)  71%    63%

  cash CAGR over the same window: +2.52%

==============================================================================
DONE
==============================================================================
  out/*.csv holds every table above in machine-readable form.
  Every options-derived number is [MODELED]. See README.md.
```

---

## Artefact tables (`out/*.csv`)
### Headline book metrics -- `out/headline.csv` (6 rows)

```
strat,cagr,max_dd,sharpe_raw,sharpe_excess_cash,frac_pos_years,n_pos_years,n_years,frac_pos_quarters,n_pos_quarters,n_quarters,frac_pos_months,n_pos_months,n_months,worst_year,worst_year_ret
S1,0.07068137248533923,-0.2183194015454839,0.6149143134797072,0.4706953817158653,0.75,18,24,0.5294117647058824,54,102,0.5196078431372549,159,306,2022,-0.14490276576514394
S2,0.029711035910462424,-0.2674837865078208,0.40678300027665565,0.18368394499823992,0.7916666666666666,19,24,0.7941176470588235,81,102,0.8856209150326797,271,306,2022,-0.22222112850313502
S3,0.10534004258303176,-0.2874174323649873,0.899157639997355,0.7498142065360835,0.8333333333333334,20,24,0.7549019607843137,77,102,0.6993464052287581,214,306,2008,-0.16948176016541883
S4,-0.1484387676467014,-0.9844978820755043,-0.46339768515411206,-0.5295958459062808,0.125,3,24,0.24509803921568626,25,102,0.30392156862745096,93,306,2021,-0.46918033553977956
S5,0.061554480983161186,-0.18835163212285433,0.6302620480583172,0.457753296089816,0.7083333333333334,17,24,0.5882352941176471,60,102,0.6339869281045751,194,306,2022,-0.16332432885585457
S6,0.09226470278664989,-0.5629928128556088,0.5204950838941094,0.43705532260309454,0.7916666666666666,19,24,0.6862745098039216,70,102,0.6209150326797386,190,306,2008,-0.380427571061843
```
### Trade-level statistics -- `out/trade_stats.csv` (5 rows)

```
strat,n,p,b,E_form,E_R,sd,p_star,b_star,n_req,L_expected,L_actual,total_R
S1,275,0.29818181818181816,6.437302979669376,1.2176685248468682,0.5991247080001175,2.8181963601951177,0.13445734330490525,2.353658536585366,88.5050455598674,15.862959449889301,10,164.7592947000323
S2,918,0.8976034858387799,0.1807743736213558,0.059867193751630854,0.03210683212592892,0.23490851695154075,0.8469018487698603,0.11407766990291268,214.12264665850466,2.993632709718354,2,29.47407189160275
S3,918,0.6949891067538126,0.9505394651924208,0.35560368060214,0.45327315891561965,1.3769689739475959,0.5126786808701407,0.43887147335423193,36.91376097511632,5.745454478839381,6,416.10475988453885
S4,918,0.2962962962962963,1.4011150407137944,-0.28855850645517206,-0.18652455422330316,0.9405674653268198,0.4164731731065763,2.375,101.71098830586386,19.414451953627697,10,-171.2295407769923
S5,1193,0.7594300083822296,0.7400229867828481,0.32142567143777057,0.16281086889491578,1.387506425150823,0.5747050513676911,0.3167770419426049,290.5114198779026,4.972279508547669,10,194.23336659163454
```
### Positivity by horizon -- `out/positivity_by_horizon.csv` (6 rows)

```
strat,D_frac_gt0,W_frac_gt0,2W_frac_gt0,M_frac_gt0,Q_frac_gt0,H_frac_gt0,Y_frac_gt0,D_frac_ge0,W_frac_ge0,2W_frac_ge0,M_frac_ge0,Q_frac_ge0,H_frac_ge0,Y_frac_ge0,D_npos,W_npos,2W_npos,M_npos,Q_npos,H_npos,Y_npos,D_ntot,W_ntot,2W_ntot,M_ntot,Q_ntot,H_ntot,Y_ntot
S1,0.4546302050963331,0.6303604723430702,2926,6436,0.4625187406296852,0.610944527736132,617,1334,0.48952095808383234,0.6062874251497006,327,668,0.5196078431372549,0.6176470588235294,159,306,0.5294117647058824,0.5588235294117647,54,102,0.64,0.64,32,50,0.75,0.75,18,24
S2,0.6589496581727782,0.6786824114356743,4241,6436,0.7038980509745127,0.7061469265367316,939,1334,0.7215568862275449,0.7215568862275449,482,668,0.8856209150326797,0.8856209150326797,271,306,0.7941176470588235,0.7941176470588235,81,102,0.78,0.78,39,50,0.7916666666666666,0.7916666666666666,19,24
S3,0.5957116221255438,0.5958669981354879,3834,6436,0.6409295352323838,0.6409295352323838,855,1334,0.6706586826347305,0.6706586826347305,448,668,0.6993464052287581,0.6993464052287581,214,306,0.7549019607843137,0.7549019607843137,77,102,0.78,0.78,39,50,0.8333333333333334,0.8333333333333334,20,24
S4,0.42464263517712864,0.4283716594157862,2733,6436,0.36806596701649175,0.37031484257871067,491,1334,0.34880239520958084,0.34880239520958084,233,668,0.30392156862745096,0.30392156862745096,93,306,0.24509803921568626,0.24509803921568626,25,102,0.12,0.12,6,50,0.125,0.125,3,24
S5,0.5651025481665631,0.5692977004350528,3637,6436,0.5742128935532234,0.5757121439280359,766,1334,0.5868263473053892,0.5868263473053892,392,668,0.6339869281045751,0.6339869281045751,194,306,0.5882352941176471,0.5882352941176471,60,102,0.66,0.66,33,50,0.7083333333333334,0.7083333333333334,17,24
S6,0.5414853946550653,0.5416407706650094,3485,6436,0.5659670164917541,0.5659670164917541,755,1334,0.5898203592814372,0.5898203592814372,394,668,0.6209150326797386,0.6209150326797386,190,306,0.6862745098039216,0.6862745098039216,70,102,0.74,0.74,37,50,0.7916666666666666,0.7916666666666666,19,24
```
### The lambda frontier -- `out/frontier.csv` (21 rows)

```
lambda,cagr,max_dd,frac_D,frac_W,frac_2W,frac_M,frac_Q,frac_H,frac_Y
0.0,0.017973793123799764,-5.079355560155818e-06,0.9968924798011187,0.9985007496251874,0.9985029940119761,1.0,1.0,1.0,1.0
0.05,0.02252130809887465,-0.01340505775034373,0.6887818520820386,0.767616191904048,0.7844311377245509,0.8235294117647058,0.8725490196078431,0.92,1.0
0.1,0.02705240099207984,-0.028405259988355747,0.6502486016159105,0.7188905547226386,0.7365269461077845,0.7875816993464052,0.8431372549019608,0.9,0.9166666666666666
0.15,0.031566666141292776,-0.043255738949554035,0.6348663766314481,0.6956521739130435,0.7140718562874252,0.7581699346405228,0.8431372549019608,0.88,0.9166666666666666
0.2,0.036063697433145636,-0.05795640289507775,0.6235239279055313,0.684407796101949,0.7005988023952096,0.738562091503268,0.8235294117647058,0.86,0.875
0.25,0.04054308835298315,-0.07250719835509256,0.617775015537601,0.671664167916042,0.6916167664670658,0.738562091503268,0.8137254901960784,0.84,0.875
0.3,0.04500443203513971,-0.08700474848980477,0.6126476072094469,0.6686656671664168,0.6841317365269461,0.7320261437908496,0.7941176470588235,0.82,0.875
0.35,0.04944732131354379,-0.10189934630905562,0.6096954630205096,0.6656671664167916,0.6826347305389222,0.7222222222222222,0.7941176470588235,0.82,0.875
0.4,0.05387134877263455,-0.11663108559418489,0.6068986948415165,0.6611694152923538,0.6796407185628742,0.7189542483660131,0.7843137254901961,0.8,0.875
0.45,0.05827610679858353,-0.13120002814989684,0.6055003107520199,0.6544227886056971,0.6781437125748503,0.7156862745098039,0.7843137254901961,0.8,0.875
0.5,0.06266118763081252,-0.14560627840429463,0.6036357986326911,0.6529235382308846,0.6766467065868264,0.7156862745098039,0.7745098039215687,0.8,0.875
0.55,0.06702618341380417,-0.15984998259784833,0.6020820385332505,0.651424287856072,0.6766467065868264,0.7091503267973857,0.7745098039215687,0.8,0.875
0.6,0.07137068624919007,-0.17393132797042365,0.6008390304536979,0.6499250374812594,0.6766467065868264,0.7058823529411765,0.7549019607843137,0.8,0.875
0.65,0.07569428824811553,-0.18785054194677775,0.5994406463642014,0.6484257871064468,0.6766467065868264,0.7058823529411765,0.7549019607843137,0.78,0.875
0.7,0.07999658158386524,-0.2022972318638292,0.5989745183343692,0.6469265367316341,0.6736526946107785,0.7058823529411765,0.7549019607843137,0.78,0.875
0.75,0.0842771585447486,-0.2168273172356353,0.5983530142945929,0.6469265367316341,0.6736526946107785,0.7026143790849673,0.7549019607843137,0.78,0.8333333333333334
0.8,0.08853561158723267,-0.2311850313897006,0.5977315102548166,0.6461769115442278,0.6736526946107785,0.6993464052287581,0.7549019607843137,0.78,0.8333333333333334
0.85,0.09277153338930733,-0.24537016394176292,0.5969546302050963,0.6454272863568216,0.6721556886227545,0.6993464052287581,0.7549019607843137,0.78,0.8333333333333334
0.9,0.09698451690409171,-0.25938256905266843,0.5964885021752642,0.6446776611694153,0.6706586826347305,0.6993464052287581,0.7549019607843137,0.78,0.8333333333333334
0.95,0.10117415541365071,-0.2732221642502688,0.5960223741454319,0.6424287856071964,0.6706586826347305,0.6993464052287581,0.7549019607843137,0.78,0.8333333333333334
1.0,0.10534004258303176,-0.2874174323649873,0.5957116221255438,0.6409295352323838,0.6706586826347305,0.6993464052287581,0.7549019607843137,0.78,0.8333333333333334
```
### Where the frontier ends -- `out/frontier_end.csv` (3 rows)

```
horizon,lambda,cagr,cash_cagr,excess
Y,0.0773,+2.50%,+1.80%,+0.70%
Q,0.0008,+1.80%,+1.80%,+0.01%
M,0.0000,+1.80%,+1.80%,+0.00%
```
### Correlation of the three indices -- `out/correlation.csv` (3 rows)

```
pair_a,pair_b,yearly_corr,daily_corr,r2_yearly
SPY,QQQ,0.9172750901243445,0.8841680389382212,0.8413935909626243
SPY,IWM,0.895119826381356,0.8866610410698422,0.8012395035809889
QQQ,IWM,0.8396165267251603,0.7926390311073526,0.7049559119500218
```
### Cost sensitivity -- `out/cost_sensitivity.csv` (18 rows)

```
cost,strat,cagr,max_dd,frac_pos_years,frac_pos_quarters,E_R
FREE,S1,0.07246011525038787,-0.21643517263526613,0.75,0.5294117647058824,0.5991247080001175
FREE,S2,0.04535942399999904,-0.25065376355796454,0.8333333333333334,0.803921568627451,0.04611235003242082
FREE,S3,0.1058985560237311,-0.27852074970385954,0.8333333333333334,0.7549019607843137,0.4639635261774883
FREE,S4,-0.1223873168208286,-0.968747214795205,0.20833333333333334,0.3333333333333333,-0.08711579861088331
FREE,S5,0.06688515806934991,-0.18211473491717067,0.7083333333333334,0.5980392156862745,0.17358795643738031
FREE,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,None
LOW,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824,0.5991247080001175
LOW,S2,0.029711035910462424,-0.2674837865078208,0.7916666666666666,0.7941176470588235,0.03210683212592892
LOW,S3,0.10534004258303176,-0.2874174323649873,0.8333333333333334,0.7549019607843137,0.45327315891561965
LOW,S4,-0.1484387676467014,-0.9844978820755043,0.125,0.24509803921568626,-0.18652455422330316
LOW,S5,0.061554480983161186,-0.18835163212285433,0.7083333333333334,0.5882352941176471,0.16281086889491578
LOW,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,None
HIGH,S1,0.06536700736362544,-0.22394909382108052,0.75,0.5196078431372549,0.5991247080001175
HIGH,S2,0.017444790771229624,-0.29745590434544655,0.75,0.7843137254901961,0.02099134172395124
HIGH,S3,0.10489178567430102,-0.29525640532642905,0.8333333333333334,0.7450980392156863,0.4447887404538203
HIGH,S4,-0.16860803442121708,-0.9915074521869456,0.08333333333333333,0.19607843137254902,-0.26542039201093764
HIGH,S5,0.05444443597766657,-0.19847009851287822,0.7083333333333334,0.5784313725490197,0.15425762481359545
HIGH,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,None
```
### Skew sensitivity -- `out/skew_sensitivity.csv` (18 rows)

```
sold_leg_iv,strat,cagr,max_dd,frac_pos_years,frac_pos_quarters,frac_pos_months,E_R
haircut 0.0 vol pts,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824,0.5196078431372549,0.5991247080001175
haircut 0.0 vol pts,S2,0.029711035910462424,-0.2674837865078208,0.7916666666666666,0.7941176470588235,0.8856209150326797,0.03210683212592892
haircut 0.0 vol pts,S3,0.10534004258303176,-0.2874174323649873,0.8333333333333334,0.7549019607843137,0.6993464052287581,0.45327315891561965
haircut 0.0 vol pts,S4,-0.1484387676467014,-0.9844978820755043,0.125,0.24509803921568626,0.30392156862745096,-0.18652455422330316
haircut 0.0 vol pts,S5,0.061554480983161186,-0.18835163212285433,0.7083333333333334,0.5882352941176471,0.6339869281045751,0.16281086889491578
haircut 0.0 vol pts,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,0.6209150326797386,None
haircut 1.5 vol pts,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824,0.5196078431372549,0.5991247080001175
haircut 1.5 vol pts,S2,-0.008666802123524553,-0.45717592957962616,0.6666666666666666,0.7549019607843137,0.8496732026143791,-0.005733652105997265
haircut 1.5 vol pts,S3,0.1010947594644791,-0.3186988769149415,0.8333333333333334,0.7450980392156863,0.696078431372549,0.3994088849714149
haircut 1.5 vol pts,S4,-0.17554593801682272,-0.9931690646359839,0.125,0.19607843137254902,0.29411764705882354,-0.24069558208617503
haircut 1.5 vol pts,S5,0.05157905465949053,-0.20343236894320882,0.7083333333333334,0.5588235294117647,0.6176470588235294,0.1336930444817492
haircut 1.5 vol pts,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,0.6209150326797386,None
haircut 3.0 vol pts,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824,0.5196078431372549,0.5991247080001175
haircut 3.0 vol pts,S2,-0.04029725318171695,-0.6579263388782581,0.5416666666666666,0.6372549019607843,0.761437908496732,-0.036187795257525295
haircut 3.0 vol pts,S3,0.09653234142015266,-0.35406336769736935,0.7916666666666666,0.7352941176470589,0.6862745098039216,0.347097178332965
haircut 3.0 vol pts,S4,-0.19844508044844944,-0.9966517385024457,0.041666666666666664,0.14705882352941177,0.2581699346405229,-0.2828975132989528
haircut 3.0 vol pts,S5,0.04315612000675073,-0.21741267091701544,0.7083333333333334,0.5490196078431373,0.6013071895424836,0.1102589259460391
haircut 3.0 vol pts,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,0.6209150326797386,None
```
### IV and term-structure stress -- `out/iv_stress.csv` (30 rows)

```
variant,strat,cagr,max_dd,frac_pos_years,frac_pos_quarters
IV x0.8,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824
IV x0.8,S2,-0.01461330373878078,-0.472805251087146,0.6666666666666666,0.7058823529411765
IV x0.8,S3,0.08887061019978848,-0.39252102101069897,0.7916666666666666,0.7254901960784313
IV x0.8,S4,-0.08909843778716786,-0.9125694840849274,0.125,0.27450980392156865
IV x0.8,S5,0.049960488511143764,-0.2070170754133538,0.7083333333333334,0.5588235294117647
IV x0.8,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216
IV x1.0,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824
IV x1.0,S2,0.029711035910462424,-0.2674837865078208,0.7916666666666666,0.7941176470588235
IV x1.0,S3,0.10534004258303176,-0.2874174323649873,0.8333333333333334,0.7549019607843137
IV x1.0,S4,-0.1484387676467014,-0.9844978820755043,0.125,0.24509803921568626
IV x1.0,S5,0.061554480983161186,-0.18835163212285433,0.7083333333333334,0.5882352941176471
IV x1.0,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216
IV x1.2,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824
IV x1.2,S2,0.0696166165542833,-0.21235839175140958,0.875,0.8725490196078431
IV x1.2,S3,0.11662070932274049,-0.2431029222333746,0.875,0.7745098039215687
IV x1.2,S4,-0.20287176021231412,-0.9971892377882009,0.125,0.22549019607843138
IV x1.2,S5,0.07170464471888671,-0.1724749774512816,0.7083333333333334,0.6176470588235294
IV x1.2,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216
term sqrt(30/D),S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824
term sqrt(30/D),S2,0.029687114778275125,-0.2591525527448537,0.7916666666666666,0.7941176470588235
term sqrt(30/D),S3,0.10534004258303176,-0.2874174323649873,0.8333333333333334,0.7549019607843137
term sqrt(30/D),S4,0.1591041990753823,-0.5210782365670472,1.0,0.7647058823529411
term sqrt(30/D),S5,0.06151604337212291,-0.18738971762905332,0.7083333333333334,0.5882352941176471
term sqrt(30/D),S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216
NO VIX haircut,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824
NO VIX haircut,S2,0.02938578940298653,-0.2807738623989111,0.7916666666666666,0.7941176470588235
NO VIX haircut,S3,0.1057141125425829,-0.2804827577596565,0.8333333333333334,0.7647058823529411
NO VIX haircut,S4,-0.1735636797125416,-0.9927871855153513,0.125,0.22549019607843138
NO VIX haircut,S5,0.06136919449019285,-0.1922772391206664,0.7083333333333334,0.5882352941176471
NO VIX haircut,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216
```
### Dividend sensitivity -- `out/dividend_sensitivity.csv` (12 rows)

```
dividend_setting,strat,cagr,max_dd,frac_pos_years,frac_pos_quarters,E_R
q = 0 (primary run),S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824,0.5991247080001175
q = 0 (primary run),S2,0.029711035910462424,-0.2674837865078208,0.7916666666666666,0.7941176470588235,0.03210683212592892
q = 0 (primary run),S3,0.10534004258303176,-0.2874174323649873,0.8333333333333334,0.7549019607843137,0.45327315891561965
q = 0 (primary run),S4,-0.1484387676467014,-0.9844978820755043,0.125,0.24509803921568626,-0.18652455422330316
q = 0 (primary run),S5,0.061554480983161186,-0.18835163212285433,0.7083333333333334,0.5882352941176471,0.16281086889491578
q = 0 (primary run),S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,None
q = published avg,S1,0.07068137248533923,-0.2183194015454839,0.75,0.5294117647058824,0.5991247080001175
q = published avg,S2,0.032278503660899904,-0.2656411833127128,0.7916666666666666,0.7941176470588235,0.034493225166128315
q = published avg,S3,0.10453924600552411,-0.2908663735474779,0.8333333333333334,0.7450980392156863,0.4413953909309477
q = published avg,S4,-0.15662186528715727,-0.9878762790339044,0.125,0.23529411764705882,-0.19884280948316577
q = published avg,S5,0.062224051664323765,-0.18601129864872212,0.7083333333333334,0.5882352941176471,0.164647171334902
q = published avg,S6,0.09226470278664989,-0.5629928128556088,0.7916666666666666,0.6862745098039216,None
```
### VRP by 21-day window (SPY, 1990-2026) -- `out/vrp.csv` (8463 rows)

First 25 rows only; the full file is on disk.

```
date,vix,collected,realised_abs,R,R_fair,fwd_rv,vrp
1993-01-29,12.42,3.5853451716675755,2.2747963038827423,0.1827646718844765,0.10240447841689304,13.12391022424762,-0.7039102242476201
1993-02-01,12.33,3.5593644095540427,1.9774011299435124,0.22222552927767467,0.1518613288583792,12.994158140484705,-0.6641581404847052
1993-02-02,12.25,3.5362703987864577,1.1980267794221344,0.33060871422144905,0.28769950679569206,13.176578778331086,-0.9265787783310859
1993-02-03,12.12,3.498742631289131,0.1394700139469962,0.4800685519563913,0.47501963438977585,12.708648365911616,-0.5886483659116166
1993-02-04,12.29,3.5478174041702495,1.6666666666666607,0.26511380423530356,0.2056138101878498,14.806318474988773,-2.5163184749887737
1993-02-05,12.9,3.723909236273086,1.3898540653231484,0.31338776308171734,0.2661162452742468,14.870682271414864,-1.970682271414864
1993-02-08,13.22,3.816285279343426,1.5983321751216195,0.29059057982732817,0.2375442132105487,14.876265618158197,-1.656265618158196
1993-02-09,13.48,3.8913408143380774,2.0293911826452016,0.2392426827319154,0.17318916785944635,14.669985797750027,-1.189985797750026
1993-02-10,13.43,3.876907057608337,0.8385744234800763,0.39185007390951065,0.36445416868116326,15.180260947080097,-1.750260947080097
1993-02-11,12.69,3.663287458008175,0.8344923504867818,0.38610061863115197,0.3572482950989331,15.178761312263605,-2.4887613122636054
1993-02-12,12.38,3.5737981662837837,1.6117729502452605,0.27450140225444464,0.2173794195006743,14.894480076508737,-2.514480076508736
1993-02-16,15.76,4.54952012121425,3.5945363048166756,0.10495434583798402,0.004883696753695494,11.769411789442916,3.9905882105570836
1993-02-17,15.9,4.589934640057525,4.316546762589923,0.029781238613037744,-0.0893318212772636,11.836625527467094,4.063374472532907
1993-02-18,15.56,4.491785094295288,3.7437005039596905,0.08327252691649131,-0.022290433423326022,12.146419442404694,3.4135805575953064
1993-02-19,15.02,4.3359005216140885,2.7977044476327206,0.17737907803852898,0.09565463751192764,12.383474874047424,2.6365251259525753
1993-02-22,14.7,4.2435244785437485,2.6447462473195182,0.18837858003506597,0.10944046886761752,12.359856796744431,2.3401432032555682
1993-02-23,15.04,4.341674024305985,2.7181688125894166,0.18696765379294975,0.10767213506166383,12.348059843829109,2.69194015617089
1993-02-24,14.72,4.249297981235645,2.0480225988700473,0.2590163589475423,0.19797179580719088,11.77370472511975,2.946295274880251
1993-02-25,13.76,3.9721698520246247,1.2684989429175397,0.34032669923832903,0.299879194803568,11.977143259659842,1.7828567403401578
1993-02-26,13.16,3.798964771267737,1.5482054890921804,0.29623323953915803,0.24461623839944568,12.038548676692344,1.1214513233076566
1993-03-01,13.6,3.925981830489455,2.117148906139721,0.2303669505424361,0.16206508722734572,11.986393166301488,1.6136068336985119
1993-03-02,12.49,3.6055524310892126,0.5563282336578546,0.4228511796332703,0.4033082927571637,10.904746406794928,1.5852535932050724
1993-03-03,13.13,3.790304517229893,0.20775623268698418,0.47259372805765737,0.46565133192354885,10.881152824889023,2.2488471751109778
1993-03-04,13.44,3.8797938089542847,1.7409470752089096,0.2756392271167956,0.21880547148644783,12.979079751735034,0.4609202482649657
1993-03-05,14.08,4.064545895094965,0.9776536312849138,0.37973396579618746,0.34926887909349225,13.108526509507973,0.971473490492027
```
### Per-trade option structure (S2 and S4) -- `out/s2_structure.csv` (1836 rows)

```
strat,sym,entry,expiry,S_entry,S_settle,K1,K2,credit,width,width_over_spot,short_delta,long_delta,R_dollars,pnl_dollars,hedge_K,hedge_debit,hedge_net,hedge_qty
S2,SPY,2001-04-02,2001-04-30,116.300000,124.910000,108.973017,103.973017,0.606128,5.00,0.0430,-0.1824,-0.0626,439.387189,54.312811,,,,0.000000
S2,SPY,2001-05-01,2001-05-31,125.070010,125.950000,116.237412,111.237412,0.578959,5.00,0.0400,-0.1656,-0.0628,442.104102,51.595898,,,,0.000000
S2,SPY,2001-06-01,2001-06-29,126.200000,122.600010,119.524264,114.524264,0.471264,5.00,0.0396,-0.1633,-0.0418,452.873633,40.826367,,,,0.000000
S2,SPY,2001-07-02,2001-07-31,122.800000,121.350010,116.049861,111.049861,0.483911,5.00,0.0407,-0.1645,-0.0434,451.608882,42.091118,,,,0.000000
S2,SPY,2001-08-01,2001-08-31,121.970000,114.149990,114.217544,109.217544,0.467961,5.00,0.0410,-0.1519,-0.0439,453.203921,33.740648,,,,0.000000
S2,SPY,2001-09-04,2001-09-28,113.850010,104.440000,108.331935,103.331935,0.509036,5.00,0.0439,-0.1817,-0.0404,449.096436,-344.589924,,,,0.000000
S2,SPY,2001-10-01,2001-10-31,103.899990,105.800000,94.983450,89.983450,0.688271,5.00,0.0481,-0.1774,-0.0732,431.172918,62.527082,,,,0.000000
S2,SPY,2001-11-01,2001-11-30,106.600010,114.050000,98.176168,93.176168,0.475794,5.00,0.0469,-0.1428,-0.0427,452.420644,41.279356,,,,0.000000
S2,SPY,2001-12-03,2001-12-31,113.649990,114.300000,107.145109,102.145109,0.568831,5.00,0.0440,-0.1788,-0.0506,443.116901,50.583099,,,,0.000000
S2,SPY,2002-01-02,2002-01-31,115.110000,113.179990,107.736212,102.736212,0.413486,5.00,0.0434,-0.1389,-0.0328,458.651421,35.048579,,,,0.000000
S2,SPY,2002-02-01,2002-02-28,113.090000,111.149990,107.201701,102.201701,0.484980,5.00,0.0442,-0.1688,-0.0368,451.501964,42.198036,,,,0.000000
S2,SPY,2002-03-01,2002-03-28,111.720000,114.520000,105.094595,100.094595,0.411158,5.00,0.0448,-0.1448,-0.0301,458.884227,34.815773,,,,0.000000
S2,SPY,2002-04-01,2002-04-30,114.230000,107.860000,109.041334,104.041334,0.485687,5.00,0.0438,-0.1792,-0.0344,451.431305,-75.864745,,,,0.000000
S2,SPY,2002-05-01,2002-05-31,107.970000,107.220000,101.933698,96.933698,0.459728,5.00,0.0463,-0.1616,-0.0340,454.027208,39.672792,,,,0.000000
S2,SPY,2002-06-03,2002-06-28,107.090000,98.960010,101.963451,96.963451,0.451591,5.00,0.0467,-0.1712,-0.0290,454.840885,-261.484960,,,,0.000000
S2,SPY,2002-07-01,2002-07-31,99.187000,91.160000,91.826523,86.826523,0.513953,5.00,0.0504,-0.1572,-0.0439,448.604736,-21.557028,,,,0.000000
S2,SPY,2002-08-01,2002-08-30,90.880000,91.780000,83.046960,78.046960,0.622282,5.00,0.0550,-0.1709,-0.0581,437.771839,55.928161,,,,0.000000
S2,SPY,2002-09-03,2002-09-30,90.735000,81.789990,84.988993,79.988993,0.662555,5.00,0.0551,-0.2005,-0.0570,433.744478,-259.944752,,,,0.000000
S2,SPY,2002-10-01,2002-10-31,82.438000,88.520000,74.053259,69.053259,0.516998,5.00,0.0607,-0.1455,-0.0437,448.300211,45.399789,,,,0.000000
S2,SPY,2002-11-01,2002-11-29,88.350010,93.980000,81.658858,76.658858,0.553586,5.00,0.0566,-0.1690,-0.0453,444.641422,49.058578,,,,0.000000
S2,SPY,2002-12-02,2002-12-31,95.470000,88.230000,88.136101,83.136101,0.309928,5.00,0.0524,-0.1128,-0.0191,469.007180,24.692820,,,,0.000000
S2,SPY,2003-01-02,2003-01-31,88.850010,86.060000,82.033173,77.033173,0.423450,5.00,0.0563,-0.1416,-0.0295,457.655037,36.044963,,,,0.000000
S2,SPY,2003-02-03,2003-02-28,86.140000,84.899990,79.537552,74.537552,0.505856,5.00,0.0580,-0.1596,-0.0381,449.414360,44.285640,,,,0.000000
S2,SPY,2003-03-03,2003-03-31,85.259990,84.740010,78.164865,73.164865,0.486837,5.00,0.0586,-0.1510,-0.0372,451.316285,42.383715,,,,0.000000
S2,SPY,2003-04-01,2003-04-30,85.250000,91.910000,78.613530,73.613530,0.433866,5.00,0.0587,-0.1450,-0.0298,456.613389,37.086611,,,,0.000000
S2,SPY,2003-05-01,2003-05-30,91.920000,96.950000,86.930928,81.930928,0.418601,5.00,0.0544,-0.1633,-0.0232,458.139904,35.560096,,,,0.000000
S2,SPY,2003-06-02,2003-06-30,97.530000,97.630000,91.974604,86.974604,0.343649,5.00,0.0513,-0.1385,-0.0180,465.635090,28.064910,,,,0.000000
S2,SPY,2003-07-01,2003-07-31,97.253010,99.390000,92.237451,87.237451,0.495419,5.00,0.0514,-0.1795,-0.0320,450.458109,43.241891,,,,0.000000
S2,SPY,2003-08-01,2003-08-29,99.190000,101.440000,94.681508,89.681508,0.427435,5.00,0.0504,-0.1736,-0.0224,457.256490,36.443510,,,,0.000000
S2,SPY,2003-09-02,2003-09-30,101.640000,99.950000,96.350637,91.350637,0.396265,5.00,0.0492,-0.1546,-0.0225,460.373520,33.326480,,,,0.000000
S2,SPY,2003-10-01,2003-10-31,100.240010,105.300000,94.066204,89.066204,0.435042,5.00,0.0499,-0.1520,-0.0298,456.495832,37.204168,,,,0.000000
S2,SPY,2003-11-03,2003-11-28,105.750000,106.450000,100.952506,95.952506,0.311077,5.00,0.0473,-0.1408,-0.0129,468.892290,24.807710,,,,0.000000
S2,SPY,2003-12-01,2003-12-31,106.929990,111.280000,101.491611,96.491611,0.351131,5.00,0.0468,-0.1425,-0.0188,464.886947,28.813053,,,,0.000000
S2,SPY,2004-01-02,2004-01-30,111.740010,113.480000,106.251207,101.251207,0.356188,5.00,0.0447,-0.1431,-0.0195,464.381185,29.318815,,,,0.000000
S2,SPY,2004-02-02,2004-02-27,113.700000,115.020000,109.190382,104.190382,0.335001,5.00,0.0440,-0.1521,-0.0141,466.499902,27.200098,,,,0.000000
S2,SPY,2004-03-01,2004-03-31,115.429990,113.100010,110.122628,105.122628,0.353601,5.00,0.0433,-0.1456,-0.0190,464.639941,29.060059,,,,0.000000
S2,SPY,2004-04-01,2004-04-30,113.070010,110.960010,107.945528,102.945528,0.427427,5.00,0.0442,-0.1651,-0.0259,457.257262,36.442738,,,,0.000000
S2,SPY,2004-05-03,2004-05-28,111.370000,112.860000,106.845487,101.845487,0.297952,5.00,0.0449,-0.1420,-0.0111,470.204787,23.495213,,,,0.000000
S2,SPY,2004-06-01,2004-06-30,112.460010,114.530000,108.122484,103.122484,0.456789,5.00,0.0445,-0.1849,-0.0256,454.321125,39.378875,,,,0.000000
S2,SPY,2004-07-01,2004-07-30,114.250000,110.840000,109.968205,104.968205,0.428323,5.00,0.0438,-0.1805,-0.0227,457.167668,36.532332,,,,0.000000
S2,SPY,2004-08-02,2004-08-31,110.190000,111.110000,106.051060,101.051060,0.501895,5.00,0.0454,-0.1993,-0.0301,449.810455,43.889545,,,,0.000000
S2,SPY,2004-09-01,2004-09-30,110.940000,111.759990,106.785826,101.785826,0.398089,5.00,0.0451,-0.1764,-0.0192,460.191124,33.508876,,,,0.000000
S2,SPY,2004-10-01,2004-10-29,112.259990,113.200000,107.576403,102.576403,0.296738,5.00,0.0445,-0.1417,-0.0123,470.326212,23.373788,,,,0.000000
S2,SPY,2004-11-01,2004-11-30,113.560000,117.890000,108.394157,103.394157,0.359189,5.00,0.0440,-0.1513,-0.0200,464.081133,29.618867,,,,0.000000
S2,SPY,2004-12-01,2004-12-31,118.160000,120.870000,113.967214,108.967214,0.310307,5.00,0.0423,-0.1565,-0.0126,468.969321,24.730679,,,,0.000000
S2,SPY,2005-01-03,2005-01-31,121.560000,118.160000,117.204321,112.204321,0.237816,5.00,0.0411,-0.1325,-0.0076,476.218357,17.481643,,,,0.000000
S2,SPY,2005-02-01,2005-02-28,118.250000,120.630000,114.218067,109.218067,0.336540,5.00,0.0423,-0.1667,-0.0142,466.346015,27.353985,,,,0.000000
S2,SPY,2005-03-01,2005-03-31,120.780000,117.960010,116.768852,111.768852,0.325528,5.00,0.0414,-0.1664,-0.0139,467.447217,26.252783,,,,0.000000
S2,SPY,2005-04-01,2005-04-29,118.630000,115.750000,113.902044,108.902044,0.273512,5.00,0.0421,-0.1385,-0.0117,472.648847,21.051153,,,,0.000000
S2,SPY,2005-05-02,2005-05-31,116.070010,119.480000,111.360209,106.360209,0.341242,5.00,0.0431,-0.1571,-0.0179,465.875810,27.824190,,,,0.000000
S2,SPY,2005-06-01,2005-06-30,119.520000,119.179990,115.677121,110.677121,0.338030,5.00,0.0418,-0.1738,-0.0144,466.196996,27.503004,,,,0.000000
S2,SPY,2005-07-01,2005-07-29,119.450000,123.740010,115.481968,110.481968,0.298627,5.00,0.0419,-0.1607,-0.0117,470.137335,23.562665,,,,0.000000
S2,SPY,2005-08-01,2005-08-31,123.830000,122.580000,120.311388,115.311388,0.306950,5.00,0.0404,-0.1760,-0.0114,469.305015,24.394985,,,,0.000000
S2,SPY,2005-09-01,2005-09-30,122.509990,123.039990,118.369383,113.369383,0.386160,5.00,0.0408,-0.1818,-0.0215,461.384046,32.315954,,,,0.000000
S2,SPY,2005-10-03,2005-10-31,122.960010,120.130000,119.174521,114.174521,0.362876,5.00,0.0407,-0.1834,-0.0172,463.712409,29.987591,,,,0.000000
S2,SPY,2005-11-01,2005-11-30,120.580000,125.410000,115.761738,110.761738,0.329097,5.00,0.0415,-0.1557,-0.0185,467.090274,26.609726,,,,0.000000
S2,SPY,2005-12-01,2005-12-30,126.020000,124.509990,122.074037,117.074037,0.234491,5.00,0.0397,-0.1462,-0.0078,476.550891,17.149109,,,,0.000000
S2,SPY,2006-01-03,2006-01-31,125.100010,127.500000,121.028175,116.028175,0.247349,5.00,0.0400,-0.1472,-0.0090,475.265103,18.434897,,,,0.000000
S2,SPY,2006-02-01,2006-02-28,127.820010,128.230000,123.755114,118.755114,0.303403,5.00,0.0391,-0.1651,-0.0141,469.659689,24.040311,,,,0.000000
S2,SPY,2006-03-01,2006-03-31,128.600010,129.830000,124.492455,119.492455,0.300675,5.00,0.0389,-0.1658,-0.0148,469.932517,23.767483,,,,0.000000
S2,SPY,2006-04-03,2006-04-28,130.070010,131.470000,126.425044,121.425044,0.287978,5.00,0.0384,-0.1703,-0.0112,471.202157,22.497843,,,,0.000000
S2,SPY,2006-05-01,2006-05-31,131.470000,127.509990,127.700147,122.700147,0.355510,5.00,0.0380,-0.1893,-0.0194,464.449012,10.235279,,,,0.000000
S2,SPY,2006-06-01,2006-06-30,127.380000,127.230000,122.664279,117.664279,0.440951,5.00,0.0393,-0.1880,-0.0330,455.904946,37.795054,,,,0.000000
S2,SPY,2006-07-03,2006-07-31,127.429990,127.850010,122.192829,117.192829,0.408426,5.00,0.0392,-0.1719,-0.0310,459.157360,34.542640,,,,0.000000
S2,SPY,2006-08-01,2006-08-31,127.340000,130.640000,123.240677,118.240677,0.485717,5.00,0.0393,-0.2114,-0.0367,451.428289,42.271711,,,,0.000000
S2,SPY,2006-09-01,2006-09-29,131.140000,133.580000,126.881818,121.881818,0.287057,5.00,0.0381,-0.1598,-0.0144,471.294278,22.405722,,,,0.000000
S2,SPY,2006-10-02,2006-10-31,133.539990,137.789990,129.890374,124.890374,0.355572,5.00,0.0374,-0.1925,-0.0189,464.442829,29.257171,,,,0.000000
S2,SPY,2006-11-01,2006-11-30,138.220000,140.530000,134.360927,129.360927,0.274290,5.00,0.0362,-0.1670,-0.0125,472.570987,21.129013,,,,0.000000
S2,SPY,2006-12-01,2006-12-29,140.530000,141.620000,136.441648,131.441648,0.377239,5.00,0.0356,-0.1884,-0.0239,462.276083,31.423917,,,,0.000000
S2,SPY,2007-01-03,2007-01-31,142.250000,143.750000,137.876126,132.876126,0.271386,5.00,0.0351,-0.1546,-0.0139,472.861415,20.838585,,,,0.000000
S2,SPY,2007-02-01,2007-02-28,144.149990,140.929990,140.068135,135.068135,0.295055,5.00,0.0347,-0.1675,-0.0152,470.494508,23.205492,,,,0.000000
S2,SPY,2007-03-01,2007-03-30,139.340000,142.000000,137.422954,132.422954,0.643766,5.00,0.0359,-0.3158,-0.0425,435.623386,58.076614,,,,0.000000
S2,SPY,2007-04-02,2007-04-30,142.160000,148.289990,137.437552,132.437552,0.385455,5.00,0.0352,-0.1779,-0.0277,461.454463,32.245537,,,,0.000000
S2,SPY,2007-05-01,2007-05-31,148.420000,153.320010,143.478691,138.478691,0.406034,5.00,0.0337,-0.1806,-0.0322,459.396562,34.303438,,,,0.000000
S2,SPY,2007-06-01,2007-06-29,153.880000,150.429990,148.429588,143.429588,0.355725,5.00,0.0325,-0.1600,-0.0273,464.427456,29.272544,,,,0.000000
S2,SPY,2007-07-02,2007-07-31,150.870000,145.720000,143.401920,138.401920,0.479367,5.00,0.0331,-0.1635,-0.0498,452.063308,41.636692,,,,0.000000
S2,SPY,2007-08-01,2007-08-31,145.179990,147.590000,138.131203,133.131203,0.610588,5.00,0.0344,-0.1930,-0.0685,438.941192,54.758808,,,,0.000000
S2,SPY,2007-09-04,2007-09-28,147.450000,152.580000,138.683954,133.683954,0.604352,5.00,0.0339,-0.1730,-0.0685,439.564763,54.135237,,,,0.000000
S2,SPY,2007-10-01,2007-10-31,152.600010,154.649990,145.339676,140.339676,0.528840,5.00,0.0328,-0.1734,-0.0551,447.115982,46.584018,,,,0.000000
S2,SPY,2007-11-01,2007-11-30,153.289990,148.660000,147.072034,142.072034,0.705540,5.00,0.0326,-0.2181,-0.0799,429.446049,64.253951,,,,0.000000
S2,SPY,2007-12-03,2007-12-31,148.190000,146.210010,138.974337,133.974337,0.658899,5.00,0.0337,-0.1792,-0.0775,434.110102,59.589898,,,,0.000000
S2,SPY,2008-01-02,2008-01-31,146.530000,137.370000,139.309160,134.309160,0.480453,5.00,0.0341,-0.1618,-0.0463,451.954654,-152.170684,,,,0.000000
S2,SPY,2008-02-01,2008-02-29,137.940000,133.820010,127.852719,122.852719,0.559674,5.00,0.0362,-0.1526,-0.0613,444.032650,49.667350,,,,0.000000
S2,SPY,2008-03-03,2008-03-31,133.140000,131.970000,126.421095,121.421095,0.615234,5.00,0.0376,-0.1883,-0.0607,438.476574,55.223426,,,,0.000000
S2,SPY,2008-04-01,2008-04-30,133.710010,138.259990,123.123603,118.123603,0.433190,5.00,0.0374,-0.1233,-0.0425,456.680963,37.019037,,,,0.000000
S2,SPY,2008-05-01,2008-05-30,138.390000,140.350010,131.208610,126.208610,0.501252,5.00,0.0361,-0.1604,-0.0449,449.874795,43.825205,,,,0.000000
S2,SPY,2008-06-02,2008-06-30,139.830000,127.980000,133.346409,128.346409,0.578056,5.00,0.0358,-0.1841,-0.0545,442.194407,-448.494407,,,,0.000000
S2,SPY,2008-07-01,2008-07-31,126.520000,126.830000,120.884703,115.884703,0.711678,5.00,0.0395,-0.2171,-0.0696,428.832169,64.867831,,,,0.000000
S2,SPY,2008-08-01,2008-08-29,127.120000,128.789990,119.063627,114.063627,0.520835,5.00,0.0393,-0.1564,-0.0496,447.916515,45.783485,,,,0.000000
S2,SPY,2008-09-02,2008-09-30,130.030000,115.990010,122.072476,117.072476,0.374109,5.00,0.0385,-0.1269,-0.0302,462.589078,-468.889078,,,,0.000000
S2,SPY,2008-10-01,2008-10-31,115.270000,96.830000,106.172704,101.172704,0.703549,5.00,0.0434,-0.1786,-0.0759,429.645099,-435.945099,,,,0.000000
S2,SPY,2008-11-03,2008-11-28,96.780000,90.090000,82.637082,77.637082,0.808427,5.00,0.0517,-0.1613,-0.0893,419.157287,74.542713,,,,0.000000
S2,SPY,2008-12-01,2008-12-31,87.509990,90.240010,76.222599,71.222599,1.018324,5.00,0.0571,-0.2012,-0.1145,398.167592,95.532408,,,,0.000000
S2,SPY,2009-01-02,2009-01-30,90.440000,82.830000,80.658987,75.658987,0.632863,5.00,0.0553,-0.1556,-0.0611,436.713675,56.986325,,,,0.000000
S2,SPY,2009-02-02,2009-02-27,81.570010,73.929990,74.666542,69.666542,0.747992,5.00,0.0613,-0.1963,-0.0692,425.200773,-5.155947,,,,0.000000
S2,SPY,2009-03-02,2009-03-31,72.520000,79.520000,65.633115,60.633115,0.787034,5.00,0.0689,-0.1998,-0.0721,421.296556,72.403444,,,,0.000000
S2,SPY,2009-04-01,2009-04-30,78.530000,87.420000,71.482292,66.482292,0.714398,5.00,0.0637,-0.1885,-0.0642,428.560197,65.139803,,,,0.000000
S2,SPY,2009-05-01,2009-05-29,87.440000,92.530000,79.115554,74.115554,0.598720,5.00,0.0572,-0.1597,-0.0536,440.127956,53.572044,,,,0.000000
S2,SPY,2009-06-01,2009-06-30,93.670000,91.950000,85.247743,80.247743,0.427545,5.00,0.0534,-0.1282,-0.0332,457.245525,36.454475,,,,0.000000
S2,SPY,2009-07-01,2009-07-31,92.340000,98.810000,85.550235,80.550235,0.455178,5.00,0.0541,-0.1472,-0.0325,454.482245,39.217755,,,,0.000000
S2,SPY,2009-08-03,2009-08-31,99.850010,102.460010,92.467525,87.467525,0.377645,5.00,0.0501,-0.1264,-0.0258,462.235465,31.464535,,,,0.000000
S2,SPY,2009-09-01,2009-09-30,101.950000,105.590000,95.787031,90.787031,0.573363,5.00,0.0490,-0.1783,-0.0461,442.663677,51.036323,,,,0.000000
S2,SPY,2009-10-01,2009-10-30,105.340000,103.560000,98.539868,93.539868,0.555500,5.00,0.0475,-0.1684,-0.0463,444.450020,49.249980,,,,0.000000
S2,SPY,2009-11-02,2009-11-30,104.130000,109.940000,96.948427,91.948427,0.439400,5.00,0.0480,-0.1415,-0.0326,456.060037,37.639963,,,,0.000000
S2,SPY,2009-12-01,2009-12-31,110.920000,111.440000,103.890501,98.890501,0.359859,5.00,0.0451,-0.1261,-0.0235,464.014130,29.685870,,,,0.000000
S2,SPY,2010-01-04,2010-01-29,112.370000,107.390000,105.958962,100.958962,0.328818,5.00,0.0445,-0.1246,-0.0188,467.118189,26.581811,,,,0.000000
S2,SPY,2010-02-01,2010-02-26,108.149990,110.740010,100.956011,95.956011,0.406861,5.00,0.0462,-0.1349,-0.0291,459.313896,34.386104,,,,0.000000
S2,SPY,2010-03-01,2010-03-31,111.200000,117.000000,104.400477,99.400477,0.432960,5.00,0.0450,-0.1445,-0.0313,456.704037,36.995963,,,,0.000000
S2,SPY,2010-04-01,2010-04-30,117.800000,118.812500,111.466991,106.466991,0.344603,5.00,0.0424,-0.1296,-0.0205,465.539696,28.160304,,,,0.000000
S2,SPY,2010-05-03,2010-05-28,119.380000,109.369000,112.176373,107.176373,0.433930,5.00,0.0419,-0.1418,-0.0332,456.606989,-243.644291,,,,0.000000
S2,SPY,2010-06-01,2010-06-30,108.350010,103.220000,99.743890,94.743890,0.734041,5.00,0.0461,-0.1848,-0.0772,426.595948,67.104052,,,,0.000000
S2,SPY,2010-07-01,2010-07-30,103.149990,110.270000,95.605175,90.605175,0.561700,5.00,0.0485,-0.1624,-0.0492,443.830023,49.869977,,,,0.000000
S2,SPY,2010-08-02,2010-08-31,111.990010,105.310000,103.563351,98.563351,0.330344,5.00,0.0446,-0.1095,-0.0235,466.965577,26.734423,,,,0.000000
S2,SPY,2010-09-01,2010-09-30,106.730000,114.130000,97.835020,92.835020,0.402896,5.00,0.0468,-0.1217,-0.0324,459.710360,33.989640,,,,0.000000
S2,SPY,2010-10-01,2010-10-29,114.990010,118.490010,107.482343,102.482343,0.405870,5.00,0.0435,-0.1329,-0.0303,459.413023,34.286977,,,,0.000000
S2,SPY,2010-11-01,2010-11-30,119.070010,118.492490,112.155393,107.155393,0.416166,5.00,0.0420,-0.1405,-0.0302,458.383414,35.316586,,,,0.000000
S2,SPY,2010-12-01,2010-12-31,120.200000,125.750000,112.256609,107.256609,0.300159,5.00,0.0416,-0.1062,-0.0197,469.984140,23.715860,,,,0.000000
S2,SPY,2011-01-03,2011-01-31,126.710010,128.679990,119.980836,114.980836,0.339905,5.00,0.0395,-0.1253,-0.0214,466.009475,27.690525,,,,0.000000
S2,SPY,2011-02-01,2011-02-28,129.460010,133.149990,123.157571,118.157571,0.343017,5.00,0.0386,-0.1302,-0.0206,465.698327,28.001673,,,,0.000000
S2,SPY,2011-03-01,2011-03-31,133.570010,132.590000,125.272876,120.272876,0.503399,5.00,0.0374,-0.1486,-0.0460,449.660074,44.039926,,,,0.000000
S2,SPY,2011-04-01,2011-04-29,133.410000,136.429990,125.869211,120.869211,0.406548,5.00,0.0375,-0.1340,-0.0314,459.345175,34.354825,,,,0.000000
S2,SPY,2011-05-02,2011-05-31,137.070010,134.899990,130.718225,125.718225,0.367697,5.00,0.0365,-0.1357,-0.0235,463.230332,30.469668,,,,0.000000
S2,SPY,2011-06-01,2011-06-30,134.509990,131.970000,128.751216,123.751216,0.519397,5.00,0.0372,-0.1753,-0.0395,448.060297,45.639703,,,,0.000000
S2,SPY,2011-07-01,2011-07-29,132.090000,129.330000,124.909514,119.909514,0.499258,5.00,0.0379,-0.1562,-0.0420,450.074170,43.625830,,,,0.000000
S2,SPY,2011-08-01,2011-08-31,130.840000,122.220000,122.295313,117.295313,0.358878,5.00,0.0382,-0.1163,-0.0279,464.112191,22.056557,,,,0.000000
S2,SPY,2011-09-01,2011-09-30,122.289990,113.149990,111.174398,106.174398,0.659276,5.00,0.0409,-0.1586,-0.0723,434.072403,59.627597,,,,0.000000
S2,SPY,2011-10-03,2011-10-31,112.490010,125.500000,102.546619,97.546619,0.721493,5.00,0.0444,-0.1740,-0.0783,427.850743,65.849257,,,,0.000000
S2,SPY,2011-11-01,2011-11-30,122.030000,124.990010,115.834571,110.834571,1.019336,5.00,0.0410,-0.2543,-0.1179,398.066391,95.633609,,,,0.000000
S2,SPY,2011-12-01,2011-12-30,124.850010,125.500000,114.016929,109.016929,0.672873,5.00,0.0400,-0.1629,-0.0743,432.712671,60.987329,,,,0.000000
S2,SPY,2012-01-03,2012-01-31,127.759990,131.320010,118.369915,113.369915,0.303700,5.00,0.0391,-0.0988,-0.0228,469.629953,24.070047,,,,0.000000
S2,SPY,2012-02-01,2012-02-29,132.289990,137.020000,124.942037,119.942037,0.372620,5.00,0.0378,-0.1278,-0.0268,462.738007,30.961993,,,,0.000000
S2,SPY,2012-03-01,2012-03-30,137.310000,140.810000,130.696127,125.696127,0.442142,5.00,0.0364,-0.1501,-0.0332,455.785795,37.914205,,,,0.000000
S2,SPY,2012-04-02,2012-04-30,140.640000,139.870000,135.026687,130.026687,0.470423,5.00,0.0356,-0.1673,-0.0330,452.957727,40.742273,,,,0.000000
S2,SPY,2012-05-01,2012-05-31,139.789990,131.470000,133.485896,128.485896,0.489011,5.00,0.0358,-0.1633,-0.0381,451.098889,-158.988519,,,,0.000000
S2,SPY,2012-06-01,2012-06-29,129.410000,136.105000,124.055528,119.055528,0.803076,5.00,0.0386,-0.2323,-0.0787,419.692427,74.007573,,,,0.000000
S2,SPY,2012-07-02,2012-07-31,136.480000,137.710010,128.993993,123.993993,0.471997,5.00,0.0366,-0.1486,-0.0397,452.800279,40.899721,,,,0.000000
S2,SPY,2012-08-01,2012-08-31,138.700000,141.160000,131.174037,126.174037,0.377887,5.00,0.0360,-0.1281,-0.0282,462.211333,31.488667,,,,0.000000
S2,SPY,2012-09-04,2012-09-28,141.039990,143.970000,135.479026,130.479026,0.458351,5.00,0.0355,-0.1654,-0.0313,454.164859,39.535141,,,,0.000000
S2,SPY,2012-10-01,2012-10-31,144.520000,141.350010,137.921201,132.921201,0.395829,5.00,0.0346,-0.1404,-0.0279,460.417075,33.282925,,,,0.000000
S2,SPY,2012-11-01,2012-11-30,141.649990,142.155000,134.461839,129.461839,0.468010,5.00,0.0353,-0.1506,-0.0386,453.199003,40.500997,,,,0.000000
S2,SPY,2012-12-03,2012-12-31,142.800000,142.410000,136.199181,131.199181,0.380317,5.00,0.0350,-0.1367,-0.0260,461.968269,31.731731,,,,0.000000
S2,SPY,2013-01-02,2013-01-31,145.110000,149.700000,135.052250,130.052250,0.278481,5.00,0.0345,-0.0908,-0.0216,472.151909,21.548091,,,,0.000000
S2,SPY,2013-02-01,2013-02-28,150.649990,151.610000,144.412138,139.412138,0.305414,5.00,0.0332,-0.1222,-0.0170,469.458594,24.241406,,,,0.000000
S2,SPY,2013-03-01,2013-03-28,151.090000,156.670000,144.224968,139.224968,0.582366,5.00,0.0331,-0.1772,-0.0538,441.763382,51.936618,,,,0.000000
S2,SPY,2013-04-01,2013-04-30,156.590000,159.679990,150.872848,145.872848,0.455896,5.00,0.0319,-0.1636,-0.0322,454.410432,39.289568,,,,0.000000
S2,SPY,2013-05-01,2013-05-31,159.330000,163.445010,153.722527,148.722527,0.499340,5.00,0.0314,-0.1744,-0.0372,450.065991,43.634009,,,,0.000000
S2,SPY,2013-06-03,2013-06-28,163.830000,160.420000,157.518303,152.518303,0.403696,5.00,0.0305,-0.1456,-0.0283,459.630359,34.069641,,,,0.000000
S2,SPY,2013-07-01,2013-07-31,161.259990,168.710010,152.412510,147.412510,0.457589,5.00,0.0310,-0.1374,-0.0425,454.241122,39.458878,,,,0.000000
S2,SPY,2013-08-01,2013-08-30,169.990010,163.649990,162.908466,157.908466,0.300708,5.00,0.0294,-0.1142,-0.0190,469.929185,23.770815,,,,0.000000
S2,SPY,2013-09-03,2013-09-30,165.230000,168.009990,156.560472,151.560472,0.345598,5.00,0.0303,-0.1142,-0.0277,465.440179,28.259821,,,,0.000000
S2,SPY,2013-10-01,2013-10-31,168.140000,175.790000,161.564378,156.564378,0.459486,5.00,0.0297,-0.1555,-0.0362,454.051432,39.648568,,,,0.000000
S2,SPY,2013-11-01,2013-11-29,176.020000,181.000000,169.582953,164.582953,0.434635,5.00,0.0284,-0.1517,-0.0328,456.536507,37.163493,,,,0.000000
S2,SPY,2013-12-02,2013-12-31,181.090000,184.690000,174.749876,169.749876,0.453017,5.00,0.0276,-0.1571,-0.0350,454.698288,39.001712,,,,0.000000
S2,SPY,2014-01-02,2014-01-31,183.980000,178.180000,178.533890,173.533890,0.554427,5.00,0.0272,-0.1889,-0.0446,444.557309,13.753714,,,,0.000000
S2,SPY,2014-02-03,2014-02-28,177.950000,186.290000,171.154077,166.154077,0.526477,5.00,0.0281,-0.1679,-0.0465,447.352277,46.347723,,,,0.000000
S2,SPY,2014-03-03,2014-03-31,184.690000,187.010000,179.541473,174.541473,0.705737,5.00,0.0271,-0.2219,-0.0653,429.426334,64.273666,,,,0.000000
S2,SPY,2014-04-01,2014-04-30,187.620000,188.310000,179.511237,174.511237,0.451569,5.00,0.0266,-0.1421,-0.0407,454.843095,38.856905,,,,0.000000
S2,SPY,2014-05-01,2014-05-30,188.220000,192.680000,181.177127,176.177127,0.512009,5.00,0.0266,-0.1630,-0.0457,448.799085,44.900915,,,,0.000000
S2,SPY,2014-06-02,2014-06-30,192.950000,195.720000,186.767255,181.767255,0.412333,5.00,0.0259,-0.1497,-0.0295,458.766714,34.933286,,,,0.000000
S2,SPY,2014-07-01,2014-07-31,196.190000,193.090000,189.467671,184.467671,0.406264,5.00,0.0255,-0.1432,-0.0307,459.373618,34.326382,,,,0.000000
S2,SPY,2014-08-01,2014-08-29,192.560000,200.710000,186.641539,181.641539,0.539335,5.00,0.0260,-0.1802,-0.0450,446.066516,47.633484,,,,0.000000
S2,SPY,2014-09-02,2014-09-30,200.970000,197.020000,194.488618,189.488618,0.428274,5.00,0.0249,-0.1506,-0.0327,457.172630,36.527370,,,,0.000000
S2,SPY,2014-10-01,2014-10-31,196.700000,201.660000,188.618928,183.618928,0.581376,5.00,0.0254,-0.1690,-0.0597,441.862385,51.837615,,,,0.000000
S2,SPY,2014-11-03,2014-11-28,201.920000,207.200000,194.387683,189.387683,0.475915,5.00,0.0248,-0.1519,-0.0427,452.408502,41.291498,,,,0.000000
S2,SPY,2014-12-01,2014-12-31,206.400000,205.540000,200.009601,195.009601,0.599132,5.00,0.0242,-0.1874,-0.0562,440.086762,53.613238,,,,0.000000
S2,SPY,2015-01-02,2015-01-30,206.380000,199.450000,197.653755,192.653755,0.441983,5.00,0.0242,-0.1366,-0.0415,455.801720,37.898280,,,,0.000000
S2,SPY,2015-02-02,2015-02-27,200.050000,210.660000,190.906275,185.906275,0.492086,5.00,0.0250,-0.1444,-0.0495,450.791351,42.908649,,,,0.000000
S2,SPY,2015-03-02,2015-03-31,210.780000,206.430000,202.884250,197.884250,0.509697,5.00,0.0237,-0.1566,-0.0489,449.030310,44.669690,,,,0.000000
S2,SPY,2015-04-01,2015-04-30,206.390000,208.460000,197.688837,192.688837,0.560664,5.00,0.0242,-0.1612,-0.0588,443.933582,49.766418,,,,0.000000
S2,SPY,2015-05-01,2015-05-29,209.400000,211.140000,201.196495,196.196495,0.404555,5.00,0.0239,-0.1318,-0.0351,459.544472,34.155528,,,,0.000000
S2,SPY,2015-06-01,2015-06-30,211.940000,205.850000,203.142800,198.142800,0.449501,5.00,0.0236,-0.1380,-0.0429,455.049885,38.650115,,,,0.000000
S2,SPY,2015-07-01,2015-07-31,207.730000,210.500000,197.949830,192.949830,0.351869,5.00,0.0241,-0.1111,-0.0316,464.813123,28.886877,,,,0.000000
S2,SPY,2015-08-03,2015-08-31,210.460000,197.670000,203.000019,198.000019,0.517156,5.00,0.0238,-0.1615,-0.0487,448.284376,-454.584376,,,,0.000000
S2,SPY,2015-09-01,2015-09-30,193.120000,191.630000,182.237103,177.237103,1.066470,5.00,0.0259,-0.2353,-0.1476,393.353027,100.346973,,,,0.000000
S2,SPY,2015-10-01,2015-10-30,192.080000,207.930000,179.751166,174.751166,0.609776,5.00,0.0260,-0.1516,-0.0731,439.022362,54.677638,,,,0.000000
S2,SPY,2015-11-02,2015-11-30,208.320000,208.690000,199.468030,194.468030,0.507812,5.00,0.0240,-0.1498,-0.0514,449.218809,44.481191,,,,0.000000
S2,SPY,2015-12-01,2015-12-31,209.440000,203.870000,199.658695,194.658695,0.494873,5.00,0.0239,-0.1423,-0.0520,450.512691,43.187309,,,,0.000000
S2,SPY,2016-01-04,2016-01-29,200.490000,193.720800,195.310144,190.310144,0.985417,5.00,0.0249,-0.2697,-0.1151,401.458280,-66.692703,,,,0.000000
S2,SPY,2016-02-01,2016-02-29,192.530000,193.560000,182.477827,177.477827,0.738240,5.00,0.0260,-0.1863,-0.0905,426.176043,67.523957,,,,0.000000
S2,SPY,2016-03-01,2016-03-31,195.010000,205.520000,182.829651,177.829651,0.499988,5.00,0.0256,-0.1323,-0.0568,450.001180,43.698820,,,,0.000000
S2,SPY,2016-04-01,2016-04-29,204.350000,206.330800,197.290996,192.290996,0.675123,5.00,0.0245,-0.1966,-0.0719,432.487667,61.212333,,,,0.000000
S2,SPY,2016-05-02,2016-05-31,206.920000,209.840000,198.605630,193.605630,0.461109,5.00,0.0242,-0.1441,-0.0436,453.889062,39.810938,,,,0.000000
S2,SPY,2016-06-01,2016-06-30,209.120000,209.475000,202.022592,197.022592,0.608676,5.00,0.0239,-0.1838,-0.0617,439.132410,54.567590,,,,0.000000
S2,SPY,2016-07-01,2016-07-29,209.360000,217.120000,196.624586,191.624586,0.670372,5.00,0.0239,-0.1628,-0.0849,432.962786,60.737214,,,,0.000000
S2,SPY,2016-08-01,2016-08-31,217.190000,217.380000,209.389482,204.389482,0.514150,5.00,0.0230,-0.1595,-0.0503,448.584976,45.115024,,,,0.000000
S2,SPY,2016-09-01,2016-09-30,217.370000,216.300000,209.428584,204.428584,0.530745,5.00,0.0230,-0.1619,-0.0532,446.925531,46.774469,,,,0.000000
S2,SPY,2016-10-03,2016-10-31,215.820000,212.550000,208.817152,203.817152,0.568244,5.00,0.0232,-0.1769,-0.0553,443.175567,50.524433,,,,0.000000
S2,SPY,2016-11-01,2016-11-30,212.930000,220.380000,204.444634,199.444634,0.496271,5.00,0.0235,-0.1508,-0.0495,450.372892,43.327108,,,,0.000000
S2,SPY,2016-12-01,2016-12-30,220.730000,223.530000,213.100348,208.100348,0.467105,5.00,0.0227,-0.1518,-0.0435,453.289460,40.410540,,,,0.000000
S2,SPY,2017-01-03,2017-01-31,225.040000,227.530000,216.474650,211.474650,0.344341,5.00,0.0222,-0.1180,-0.0295,465.565923,28.134077,,,,0.000000
S2,SPY,2017-02-01,2017-02-28,228.255000,236.470000,221.256879,216.256879,0.379933,5.00,0.0219,-0.1375,-0.0299,462.006728,31.693272,,,,0.000000
S2,SPY,2017-03-01,2017-03-31,238.390000,235.740000,228.930076,223.930076,0.332255,5.00,0.0210,-0.1107,-0.0300,466.774527,26.925473,,,,0.000000
S2,SPY,2017-04-03,2017-04-28,235.800000,238.080000,228.997404,223.997404,0.476789,5.00,0.0212,-0.1623,-0.0430,452.321085,41.378915,,,,0.000000
S2,SPY,2017-05-01,2017-05-31,238.680000,241.440000,231.154450,226.154450,0.426541,5.00,0.0209,-0.1459,-0.0390,457.345868,36.354132,,,,0.000000
S2,SPY,2017-06-01,2017-06-30,241.970000,241.800000,235.040346,230.040346,0.410213,5.00,0.0207,-0.1478,-0.0352,458.978714,34.721286,,,,0.000000
S2,SPY,2017-07-03,2017-07-31,242.880000,246.770000,234.837290,229.837290,0.381415,5.00,0.0206,-0.1325,-0.0346,461.858532,31.841468,,,,0.000000
S2,SPY,2017-08-01,2017-08-31,247.460000,247.490000,240.422046,235.422046,0.392491,5.00,0.0202,-0.1441,-0.0339,460.750902,32.949098,,,,0.000000
S2,SPY,2017-09-01,2017-09-29,247.920000,251.230000,240.201434,235.201434,0.460096,5.00,0.0202,-0.1528,-0.0450,453.990385,39.709615,,,,0.000000
S2,SPY,2017-10-02,2017-10-31,251.490000,257.150000,244.474779,239.474779,0.456455,5.00,0.0199,-0.1584,-0.0425,454.354501,39.345499,,,,0.000000
S2,SPY,2017-11-01,2017-11-30,258.040000,265.010000,249.477351,244.477351,0.430293,5.00,0.0194,-0.1411,-0.0435,456.970732,36.729268,,,,0.000000
S2,SPY,2017-12-01,2017-12-29,264.760000,266.860000,258.247190,253.247190,0.516641,5.00,0.0189,-0.1775,-0.0505,448.335873,45.364127,,,,0.000000
S2,SPY,2018-01-02,2018-01-31,267.840000,281.900000,259.686311,254.686311,0.402219,5.00,0.0187,-0.1391,-0.0394,459.778138,33.921862,,,,0.000000
S2,SPY,2018-02-01,2018-02-28,281.070000,271.650000,273.975679,268.975679,0.621749,5.00,0.0178,-0.1944,-0.0705,437.825124,-176.692991,,,,0.000000
S2,SPY,2018-03-01,2018-03-29,271.410000,263.150000,260.186644,255.186644,0.642577,5.00,0.0184,-0.1717,-0.0850,435.742303,57.957697,,,,0.000000
S2,SPY,2018-04-02,2018-04-30,262.550000,264.510000,249.104619,244.104619,0.716077,5.00,0.0190,-0.1758,-0.1003,428.392349,65.307651,,,,0.000000
S2,SPY,2018-05-01,2018-05-31,263.870000,270.940000,252.098259,247.098259,0.694640,5.00,0.0189,-0.1793,-0.0952,430.536018,63.163982,,,,0.000000
S2,SPY,2018-06-01,2018-06-29,272.410000,271.280000,261.809262,256.809262,0.439889,5.00,0.0184,-0.1352,-0.0517,456.011094,37.688906,,,,0.000000
S2,SPY,2018-07-02,2018-07-31,269.510000,281.330000,260.100176,255.100176,0.778357,5.00,0.0186,-0.2077,-0.1062,422.164281,71.535719,,,,0.000000
S2,SPY,2018-08-01,2018-08-31,281.560000,290.310000,272.371188,267.371188,0.542161,5.00,0.0178,-0.1658,-0.0664,445.783940,47.916060,,,,0.000000
S2,SPY,2018-09-04,2018-09-28,289.840000,290.720000,281.740099,276.740099,0.599049,5.00,0.0173,-0.1840,-0.0723,440.095137,53.604863,,,,0.000000
S2,SPY,2018-10-01,2018-10-31,292.110000,270.630000,281.292402,276.292402,0.458061,5.00,0.0171,-0.1406,-0.0569,454.193869,-460.493869,,,,0.000000
S2,SPY,2018-11-01,2018-11-30,271.600000,275.650000,253.965737,248.965737,0.655119,5.00,0.0184,-0.1539,-0.0948,434.488146,59.211854,,,,0.000000
S2,SPY,2018-12-03,2018-12-31,280.280000,249.920000,262.426906,257.426906,0.379638,5.00,0.0178,-0.1010,-0.0504,462.036222,-468.336222,,,,0.000000
S2,SPY,2019-01-02,2019-01-31,245.980000,269.930000,230.789299,225.789299,0.988702,5.00,0.0203,-0.2158,-0.1487,401.129779,92.570221,,,,0.000000
S2,SPY,2019-02-01,2019-02-28,270.150000,278.680000,257.291668,252.291668,0.631874,5.00,0.0185,-0.1646,-0.0872,436.812649,56.887351,,,,0.000000
S2,SPY,2019-03-01,2019-03-29,280.440000,282.480000,268.241395,263.241395,0.463795,5.00,0.0178,-0.1353,-0.0595,453.620478,40.079522,,,,0.000000
S2,SPY,2019-04-01,2019-04-30,284.700000,294.020000,271.849686,266.849686,0.438052,5.00,0.0176,-0.1278,-0.0564,456.194784,37.505216,,,,0.000000
S2,SPY,2019-05-01,2019-05-31,294.720000,275.270000,283.887959,278.887959,0.535469,5.00,0.0170,-0.1575,-0.0704,446.453133,-452.753133,,,,0.000000
S2,SPY,2019-06-03,2019-06-28,275.310000,293.000000,263.715015,258.715015,0.622537,5.00,0.0182,-0.1679,-0.0837,437.746295,55.953705,,,,0.000000
S2,SPY,2019-07-01,2019-07-31,296.680000,297.430000,280.510549,275.510549,0.404069,5.00,0.0169,-0.1105,-0.0538,459.593105,34.106895,,,,0.000000
S2,SPY,2019-08-01,2019-08-30,297.600000,292.450000,288.117158,283.117158,0.556861,5.00,0.0168,-0.1680,-0.0704,444.313900,49.386100,,,,0.000000
S2,SPY,2019-09-03,2019-09-30,290.570000,296.770000,277.649745,272.649745,0.814009,5.00,0.0172,-0.1974,-0.1190,418.599100,75.100900,,,,0.000000
S2,SPY,2019-10-01,2019-10-31,297.740000,303.330000,284.293319,279.293319,0.568881,5.00,0.0168,-0.1508,-0.0777,443.111852,50.588148,,,,0.000000
S2,SPY,2019-11-01,2019-11-29,304.920000,314.310000,293.133587,288.133587,0.461534,5.00,0.0164,-0.1348,-0.0573,453.846634,39.853366,,,,0.000000
S2,SPY,2019-12-02,2019-12-31,314.590000,321.860000,304.579294,299.579294,0.553705,5.00,0.0159,-0.1627,-0.0697,444.629526,49.070474,,,,0.000000
S2,SPY,2020-01-02,2020-01-31,323.540000,321.730000,311.235562,306.235562,0.466522,5.00,0.0155,-0.1345,-0.0594,453.347784,40.352216,,,,0.000000
S2,SPY,2020-02-03,2020-02-28,323.350000,296.260000,308.995409,303.995409,0.524933,5.00,0.0155,-0.1385,-0.0708,447.506740,-453.806740,,,,0.000000
S2,SPY,2020-03-02,2020-03-31,298.210000,257.750000,275.193000,270.193000,0.663000,5.00,0.0168,-0.1440,-0.0975,433.699959,-439.999959,,,,0.000000
S2,SPY,2020-04-01,2020-04-30,247.980000,290.480000,220.474696,215.474696,1.267147,5.00,0.0202,-0.2207,-0.1832,373.285299,120.414701,,,,0.000000
S2,SPY,2020-05-01,2020-05-29,285.310000,304.320000,266.180456,261.180456,1.046826,5.00,0.0175,-0.2122,-0.1576,395.317430,98.382570,,,,0.000000
S2,SPY,2020-06-01,2020-06-30,303.620000,308.360000,282.251473,277.251473,0.796741,5.00,0.0165,-0.1676,-0.1170,420.325866,73.374134,,,,0.000000
S2,SPY,2020-07-01,2020-07-31,309.570000,326.520000,282.532463,277.532463,0.746657,5.00,0.0162,-0.1502,-0.1096,425.334255,68.365745,,,,0.000000
S2,SPY,2020-08-03,2020-08-31,328.320000,349.310000,305.204007,300.204007,0.660624,5.00,0.0152,-0.1420,-0.0958,433.937640,59.762360,,,,0.000000
S2,SPY,2020-09-01,2020-09-30,350.210000,334.890000,327.984694,322.984694,0.697598,5.00,0.0143,-0.1509,-0.1026,430.240169,63.459831,,,,0.000000
S2,SPY,2020-10-01,2020-10-30,337.690000,326.540000,311.905260,306.905260,0.637533,5.00,0.0148,-0.1345,-0.0930,436.246679,57.453321,,,,0.000000
S2,SPY,2020-11-02,2020-11-30,330.200000,362.060000,299.176773,294.176773,0.665094,5.00,0.0151,-0.1326,-0.0974,433.490601,60.209399,,,,0.000000
S2,SPY,2020-12-01,2020-12-31,365.570000,373.880000,341.077249,336.077249,0.571613,5.00,0.0137,-0.1253,-0.0827,442.838669,50.861331,,,,0.000000
S2,SPY,2021-01-04,2021-01-29,375.310000,370.070000,353.942744,348.942744,0.649418,5.00,0.0133,-0.1444,-0.0949,435.058190,58.641810,,,,0.000000
S2,SPY,2021-02-01,2021-02-26,373.720000,380.360000,349.201416,344.201416,0.562193,5.00,0.0134,-0.1237,-0.0814,443.780689,49.919311,,,,0.000000
S2,SPY,2021-03-01,2021-03-31,385.590000,396.330000,356.899058,351.899058,0.539081,5.00,0.0130,-0.1150,-0.0788,446.091890,47.608110,,,,0.000000
S2,SPY,2021-04-01,2021-04-30,398.400000,417.300000,376.458495,371.458495,0.613381,5.00,0.0126,-0.1374,-0.0895,438.661867,55.038133,,,,0.000000
S2,SPY,2021-05-03,2021-05-28,419.430000,420.040000,399.083186,394.083186,0.582724,5.00,0.0119,-0.1346,-0.0839,441.727561,51.972439,,,,0.000000
S2,SPY,2021-06-01,2021-06-30,422.570000,428.060000,399.105923,394.105923,0.603363,5.00,0.0118,-0.1339,-0.0891,439.663684,54.036316,,,,0.000000
S2,SPY,2021-07-01,2021-07-30,428.870000,438.510000,410.146937,405.146937,0.647359,5.00,0.0117,-0.1500,-0.0942,435.264050,58.435950,,,,0.000000
S2,SPY,2021-08-02,2021-08-31,440.340000,451.560000,415.993875,410.993875,0.651874,5.00,0.0114,-0.1423,-0.0982,434.812556,58.887444,,,,0.000000
S2,SPY,2021-09-01,2021-09-30,452.560000,429.140000,428.942740,423.942740,0.688300,5.00,0.0110,-0.1503,-0.1046,431.170003,62.529997,,,,0.000000
S2,SPY,2021-10-01,2021-10-29,430.980000,459.250000,408.081481,403.081481,0.635255,5.00,0.0116,-0.1409,-0.0945,436.474515,57.225485,,,,0.000000
S2,SPY,2021-11-01,2021-11-30,460.300000,455.560000,439.610205,434.610205,0.652538,5.00,0.0109,-0.1482,-0.0971,434.746224,58.953776,,,,0.000000
S2,SPY,2021-12-01,2021-12-31,461.640000,474.960000,432.702861,427.702861,0.486882,5.00,0.0108,-0.1070,-0.0720,451.311845,42.388155,,,,0.000000
S2,SPY,2022-01-03,2022-01-31,476.300000,449.910000,453.126952,448.126952,0.661498,5.00,0.0105,-0.1465,-0.1003,433.850227,-261.845442,,,,0.000000
S2,SPY,2022-02-01,2022-02-28,450.680000,436.630000,414.284895,409.284895,0.797822,5.00,0.0111,-0.1557,-0.1246,420.217802,73.482198,,,,0.000000
S2,SPY,2022-03-01,2022-03-31,435.040000,451.640000,401.391011,396.391011,0.875366,5.00,0.0115,-0.1711,-0.1376,412.463432,81.236568,,,,0.000000
S2,SPY,2022-04-01,2022-04-29,453.310000,412.000000,428.700954,423.700954,0.663330,5.00,0.0110,-0.1459,-0.1020,433.667046,-439.967046,,,,0.000000
S2,SPY,2022-05-02,2022-05-31,412.070000,412.930000,376.988295,371.988295,0.827685,5.00,0.0121,-0.1613,-0.1291,417.231515,76.468485,,,,0.000000
S2,SPY,2022-06-01,2022-06-30,415.170000,377.250000,382.901355,377.901355,0.718988,5.00,0.0120,-0.1465,-0.1120,428.101239,-434.401239,,,,0.000000
S2,SPY,2022-07-01,2022-07-29,376.560000,411.990000,351.710379,346.710379,0.805064,5.00,0.0133,-0.1706,-0.1264,419.493584,74.206416,,,,0.000000
S2,SPY,2022-08-01,2022-08-31,409.150000,395.180000,385.726301,380.726301,0.896542,5.00,0.0122,-0.1925,-0.1462,410.345778,83.354222,,,,0.000000
S2,SPY,2022-09-01,2022-09-30,392.890000,357.180000,369.657983,364.657983,0.872902,5.00,0.0127,-0.1888,-0.1420,412.709799,-419.009799,,,,0.000000
S2,SPY,2022-10-03,2022-10-31,361.080000,386.210000,328.691654,323.691654,0.668081,5.00,0.0138,-0.1387,-0.1045,433.191937,60.508063,,,,0.000000
S2,SPY,2022-11-01,2022-11-30,390.140000,407.680000,360.003981,355.003981,0.635231,5.00,0.0128,-0.1391,-0.1027,436.476860,57.223140,,,,0.000000
S2,SPY,2022-12-01,2022-12-30,408.770000,382.430000,386.863579,381.863579,0.683877,5.00,0.0122,-0.1631,-0.1138,431.612282,-381.270165,,,,0.000000
S2,SPY,2023-01-03,2023-01-31,384.370000,406.480000,362.148640,357.148640,0.641830,5.00,0.0130,-0.1530,-0.1046,435.817005,57.882995,,,,0.000000
S2,SPY,2023-02-01,2023-02-28,405.211000,396.260000,388.253417,383.253417,0.782811,5.00,0.0123,-0.1935,-0.1314,421.718943,71.981057,,,,0.000000
S2,SPY,2023-03-01,2023-03-31,395.410000,409.390000,375.244252,370.244252,0.782061,5.00,0.0126,-0.1858,-0.1325,421.793879,71.906121,,,,0.000000
S2,SPY,2023-04-03,2023-04-28,408.850000,415.930000,390.469628,385.469628,0.746415,5.00,0.0122,-0.1823,-0.1244,425.358510,68.341490,,,,0.000000
S2,SPY,2023-05-01,2023-05-31,415.470000,417.850000,396.523902,391.523902,0.747919,5.00,0.0120,-0.1854,-0.1290,425.208096,68.491904,,,,0.000000
S2,SPY,2023-06-01,2023-06-30,418.090000,443.280000,398.288825,393.288825,0.713441,5.00,0.0120,-0.1770,-0.1228,428.655869,65.044131,,,,0.000000
S2,SPY,2023-07-03,2023-07-31,442.920000,457.790000,428.891146,423.891146,0.692349,5.00,0.0113,-0.1934,-0.1202,430.765067,62.934933,,,,0.000000
S2,SPY,2023-08-01,2023-08-31,456.270000,450.350000,443.196233,438.196233,0.772175,5.00,0.0110,-0.2153,-0.1382,422.782478,70.917522,,,,0.000000
S2,SPY,2023-09-01,2023-09-29,453.170000,427.480000,434.229513,429.229513,0.538352,5.00,0.0110,-0.1485,-0.0934,446.164804,-452.464804,,,,0.000000
S2,SPY,2023-10-02,2023-10-31,426.620000,418.200000,407.743783,402.743783,0.770135,5.00,0.0117,-0.1908,-0.1344,422.986462,70.713538,,,,0.000000
S2,SPY,2023-11-01,2023-11-30,419.200000,456.400000,397.051564,392.051564,0.693359,5.00,0.0119,-0.1683,-0.1193,430.664133,63.035867,,,,0.000000
S2,SPY,2023-12-01,2023-12-29,455.770000,475.310000,442.845986,437.845986,0.701143,5.00,0.0110,-0.2014,-0.1230,429.885675,63.814325,,,,0.000000
S2,SPY,2024-01-02,2024-01-31,472.160000,482.880000,460.597059,455.597059,0.888034,5.00,0.0106,-0.2432,-0.1600,411.196556,82.503444,,,,0.000000
S2,SPY,2024-02-01,2024-02-29,484.630000,508.080000,467.810637,462.810637,0.574728,5.00,0.0103,-0.1633,-0.1014,442.527154,51.172846,,,,0.000000
S2,SPY,2024-03-01,2024-03-28,508.980000,523.070000,491.866208,486.866208,0.635735,5.00,0.0098,-0.1750,-0.1135,436.426531,57.273469,,,,0.000000
S2,SPY,2024-04-01,2024-04-30,523.830000,501.980000,506.572547,501.572547,0.647630,5.00,0.0095,-0.1791,-0.1179,435.237040,-400.791769,,,,0.000000
S2,SPY,2024-05-01,2024-05-31,501.380000,527.370000,483.048510,478.048510,0.744154,5.00,0.0100,-0.1930,-0.1351,425.584647,68.115353,,,,0.000000
S2,SPY,2024-06-03,2024-06-28,529.020000,544.220000,512.125639,507.125639,0.579157,5.00,0.0095,-0.1642,-0.1024,442.084302,51.615698,,,,0.000000
S2,SPY,2024-07-01,2024-07-31,545.630000,550.810000,527.339776,522.339776,0.618597,5.00,0.0092,-0.1724,-0.1144,438.140346,55.559654,,,,0.000000
S2,SPY,2024-08-01,2024-08-30,552.570000,563.680000,528.874906,523.874906,0.656024,5.00,0.0090,-0.1654,-0.1194,434.397576,59.302424,,,,0.000000
S2,SPY,2024-09-03,2024-09-30,560.470000,573.760000,543.174857,538.174857,0.884651,5.00,0.0089,-0.2211,-0.1614,411.534922,82.165078,,,,0.000000
S2,SPY,2024-10-01,2024-10-31,573.400000,568.640000,551.742498,546.742498,0.746271,5.00,0.0087,-0.1856,-0.1356,425.372941,68.327059,,,,0.000000
S2,SPY,2024-11-01,2024-11-29,571.320000,602.550000,541.190571,536.190571,0.666605,5.00,0.0088,-0.1549,-0.1180,433.339547,60.360453,,,,0.000000
S2,SPY,2024-12-02,2024-12-31,602.970000,586.080000,580.945711,575.945711,0.705611,5.00,0.0083,-0.1777,-0.1284,429.438905,64.261095,,,,0.000000
S2,SPY,2025-01-02,2025-01-31,589.390000,601.820000,564.818939,559.818939,0.579768,5.00,0.0085,-0.1475,-0.1036,442.023151,51.676849,,,,0.000000
S2,SPY,2025-02-03,2025-02-28,592.670000,594.180000,578.876563,573.876563,1.214722,5.00,0.0084,-0.2845,-0.2203,378.527825,115.172175,,,,0.000000
S2,SPY,2025-03-03,2025-03-31,596.180000,559.390000,565.909945,560.909945,0.693303,5.00,0.0084,-0.1597,-0.1229,430.669739,-436.969739,,,,0.000000
S2,SPY,2025-04-01,2025-04-30,557.450000,554.540000,533.919243,528.919243,0.833301,5.00,0.0090,-0.1946,-0.1484,416.669904,77.030096,,,,0.000000
S2,SPY,2025-05-01,2025-05-30,560.370000,589.390000,520.287470,515.287470,0.631728,5.00,0.0089,-0.1368,-0.1088,436.827152,56.872848,,,,0.000000
S2,SPY,2025-06-02,2025-06-30,587.760000,617.850000,562.052942,557.052942,0.823601,5.00,0.0085,-0.1899,-0.1472,417.639873,76.060127,,,,0.000000
S2,SPY,2025-07-01,2025-07-31,616.360000,632.080000,591.819783,586.819783,0.811012,5.00,0.0081,-0.1921,-0.1476,418.898828,74.801172,,,,0.000000
S2,SPY,2025-08-01,2025-08-29,626.300000,645.050000,608.981261,603.981261,1.013339,5.00,0.0080,-0.2438,-0.1862,398.666144,95.033856,,,,0.000000
S2,SPY,2025-09-02,2025-09-30,637.500000,666.180000,622.088167,617.088167,1.112386,5.00,0.0078,-0.2661,-0.2050,388.761437,104.938563,,,,0.000000
S2,SPY,2025-10-01,2025-10-31,663.170000,682.060000,637.956840,632.956840,0.874262,5.00,0.0075,-0.2027,-0.1596,412.573772,81.126228,,,,0.000000
S2,SPY,2025-11-03,2025-11-28,685.670000,683.390000,655.886968,650.886968,0.611595,5.00,0.0073,-0.1456,-0.1087,438.840482,54.859518,,,,0.000000
S2,SPY,2025-12-01,2025-12-31,678.810000,681.920000,647.722910,642.722910,0.935472,5.00,0.0074,-0.2042,-0.1689,406.452779,87.247221,,,,0.000000
S2,SPY,2026-01-02,2026-01-30,685.710000,691.970000,659.131525,654.131525,0.571211,5.00,0.0073,-0.1429,-0.1021,442.878923,50.821077,,,,0.000000
S2,SPY,2026-02-02,2026-02-27,689.580000,685.990000,665.400642,660.400642,0.843584,5.00,0.0073,-0.1963,-0.1512,415.641605,78.058395,,,,0.000000
S2,SPY,2026-03-02,2026-03-31,678.700000,650.340000,652.281689,647.281689,1.035255,5.00,0.0074,-0.2273,-0.1875,396.474467,-96.943342,,,,0.000000
S2,SPY,2026-04-01,2026-04-30,653.900000,718.660000,605.787085,600.787085,0.742772,5.00,0.0076,-0.1522,-0.1283,425.722802,67.977198,,,,0.000000
S2,SPY,2026-05-01,2026-05-29,721.250000,756.480000,686.648131,681.648131,0.688681,5.00,0.0069,-0.1562,-0.1238,431.131926,62.568074,,,,0.000000
S2,SPY,2026-06-01,2026-06-30,755.360000,746.770000,724.216015,719.216015,0.806791,5.00,0.0066,-0.1834,-0.1475,419.320932,74.379068,,,,0.000000
S2,SPY,2026-07-01,2026-07-31,745.000000,747.030000,710.862241,705.862241,0.838871,5.00,0.0067,-0.1858,-0.1529,416.112873,77.587127,,,,0.000000
S2,SPY,2026-08-03,2026-08-31,749.440000,767.050000,713.475403,708.475403,0.701944,5.00,0.0067,-0.1585,-0.1271,429.805620,63.894380,,,,0.000000
S2,SPY,2026-09-01,2026-09-30,762.010000,762.630000,737.900600,732.900600,0.949548,5.00,0.0066,-0.2204,-0.1764,405.045188,88.654812,,,,0.000000
S2,QQQ,2001-04-02,2001-04-30,39.170000,46.149990,34.223598,29.223598,0.480668,5.00,0.1276,-0.1645,-0.0211,451.933166,41.766834,,,,0.000000
S2,QQQ,2001-05-01,2001-05-31,46.200000,44.730000,40.087957,35.087957,0.552097,5.00,0.1082,-0.1631,-0.0336,444.790312,48.909688,,,,0.000000
S2,QQQ,2001-06-01,2001-06-29,45.539990,45.700000,40.302853,35.302853,0.319163,5.00,0.1098,-0.1297,-0.0111,468.083712,25.616288,,,,0.000000
S2,QQQ,2001-07-02,2001-07-31,45.651990,41.759990,40.981539,35.981539,0.454323,5.00,0.1095,-0.1678,-0.0201,454.567692,39.132308,,,,0.000000
S2,QQQ,2001-08-01,2001-08-31,42.636990,36.630000,37.050809,32.050809,0.344034,5.00,0.1173,-0.1292,-0.0129,465.596629,-13.977480,,,,0.000000
S2,QQQ,2001-09-04,2001-09-28,36.518010,28.980000,33.023759,28.023759,0.374052,5.00,0.1369,-0.1716,-0.0081,462.594788,-373.270703,,,,0.000000
S2,QQQ,2001-10-01,2001-10-31,28.850010,33.899990,24.308998,19.308998,0.516507,5.00,0.1733,-0.1680,-0.0169,448.349282,45.350718,,,,0.000000
S2,QQQ,2001-11-01,2001-11-30,34.440000,39.649990,29.329373,24.329373,0.388727,5.00,0.1452,-0.1395,-0.0122,461.127282,32.572718,,,,0.000000
S2,QQQ,2001-12-03,2001-12-31,39.289990,38.910000,35.098605,30.098605,0.495581,5.00,0.1273,-0.1801,-0.0192,450.441944,43.258056,,,,0.000000
S2,QQQ,2002-01-02,2002-01-31,39.570010,38.509990,34.658764,29.658764,0.325571,5.00,0.1264,-0.1319,-0.0092,467.442949,26.257051,,,,0.000000
S2,QQQ,2002-02-01,2002-02-28,38.401000,33.780000,34.619997,29.619997,0.395468,5.00,0.1302,-0.1688,-0.0103,460.453197,-50.752849,,,,0.000000
S2,QQQ,2002-03-01,2002-03-28,34.154010,36.060000,30.290533,25.290533,0.292733,5.00,0.1464,-0.1408,-0.0046,470.726707,22.973293,,,,0.000000
S2,QQQ,2002-04-01,2002-04-30,35.800000,31.730000,32.796344,27.796344,0.362139,5.00,0.1397,-0.1815,-0.0057,463.786147,-76.720526,,,,0.000000
S2,QQQ,2002-05-01,2002-05-31,31.670000,30.039990,28.451466,23.451466,0.337564,5.00,0.1579,-0.1669,-0.0046,466.243632,27.456368,,,,0.000000
S2,QQQ,2002-06-03,2002-06-28,30.008000,26.100010,27.211508,22.211508,0.285754,5.00,0.1666,-0.1652,-0.0020,471.424628,-88.874442,,,,0.000000
S2,QQQ,2002-07-01,2002-07-31,25.978000,23.850010,22.585412,17.585412,0.389983,5.00,0.1925,-0.1694,-0.0058,461.001710,32.698290,,,,0.000000
S2,QQQ,2002-08-01,2002-08-30,23.740010,23.490010,20.400585,15.400585,0.389346,5.00,0.2106,-0.1685,-0.0049,461.065425,32.634575,,,,0.000000
S2,QQQ,2002-09-03,2002-09-30,23.060000,20.720000,21.037587,16.037587,0.325811,5.00,0.2168,-0.2035,-0.0010,467.418912,-5.477626,,,,0.000000
S2,QQQ,2002-10-01,2002-10-31,20.910000,24.550000,18.111114,13.111114,0.246340,5.00,0.2391,-0.1475,-0.0006,475.366014,18.333986,,,,0.000000
S2,QQQ,2002-11-01,2002-11-29,24.378010,27.720000,22.170538,17.170538,0.267200,5.00,0.2051,-0.1789,-0.0006,473.280047,20.419953,,,,0.000000
S2,QQQ,2002-12-02,2002-12-31,28.420000,24.370000,25.521934,20.521934,0.123654,5.00,0.1759,-0.1026,-0.0001,487.634586,-109.127972,,,,0.000000
S2,QQQ,2003-01-02,2003-01-31,24.720000,24.440000,22.016316,17.016316,0.184468,5.00,0.2023,-0.1320,-0.0003,481.553237,12.146763,,,,0.000000
S2,QQQ,2003-02-03,2003-02-28,24.528000,25.160000,21.596091,16.596091,0.278859,5.00,0.2038,-0.1550,-0.0015,472.114092,21.585908,,,,0.000000
S2,QQQ,2003-03-03,2003-03-31,25.270000,25.250000,22.419019,17.419019,0.261755,5.00,0.1979,-0.1533,-0.0012,473.824539,19.875461,,,,0.000000
S2,QQQ,2003-04-01,2003-04-30,25.440000,27.450000,22.873741,17.873741,0.207516,5.00,0.1965,-0.1454,-0.0004,479.248418,14.451582,,,,0.000000
S2,QQQ,2003-05-01,2003-05-30,27.440000,29.789990,25.628423,20.628423,0.175049,5.00,0.1822,-0.1642,-0.0000,482.495141,11.204859,,,,0.000000
S2,QQQ,2003-06-02,2003-06-30,30.080000,29.950000,27.760514,22.760514,0.151578,5.00,0.1662,-0.1329,-0.0001,484.842230,8.857770,,,,0.000000
S2,QQQ,2003-07-01,2003-07-31,29.700000,31.800000,27.649392,22.649392,0.264824,5.00,0.1684,-0.1876,-0.0006,473.517566,20.182434,,,,0.000000
S2,QQQ,2003-08-01,2003-08-29,31.690000,33.390000,29.520168,24.520168,0.236268,5.00,0.1578,-0.1734,-0.0005,476.373236,17.326764,,,,0.000000
S2,QQQ,2003-09-02,2003-09-30,33.490010,32.420000,30.797533,25.797533,0.234314,5.00,0.1493,-0.1537,-0.0010,476.568603,17.131397,,,,0.000000
S2,QQQ,2003-10-01,2003-10-31,32.610000,35.179990,29.254425,24.254425,0.283926,5.00,0.1533,-0.1490,-0.0031,471.607431,22.092569,,,,0.000000
S2,QQQ,2003-11-03,2003-11-28,35.429990,35.380000,32.584549,27.584549,0.210975,5.00,0.1411,-0.1414,-0.0009,478.902464,14.797536,,,,0.000000
S2,QQQ,2003-12-01,2003-12-31,35.710010,36.460010,32.366921,27.366921,0.243882,5.00,0.1400,-0.1391,-0.0022,475.611775,18.088225,,,,0.000000
S2,QQQ,2004-01-02,2004-01-30,36.660000,37.070010,33.295196,28.295196,0.276165,5.00,0.1364,-0.1482,-0.0032,472.383521,21.316479,,,,0.000000
S2,QQQ,2004-02-02,2004-02-27,37.200000,36.570010,34.588153,29.588153,0.214925,5.00,0.1344,-0.1506,-0.0008,478.507475,15.192525,,,,0.000000
S2,QQQ,2004-03-01,2004-03-31,36.679990,35.840000,33.977769,28.977769,0.230207,5.00,0.1363,-0.1531,-0.0011,476.979325,16.720675,,,,0.000000
S2,QQQ,2004-04-01,2004-04-30,35.810000,34.770000,33.470180,28.470180,0.229456,5.00,0.1396,-0.1654,-0.0007,477.054364,16.645636,,,,0.000000
S2,QQQ,2004-05-03,2004-05-28,35.000000,36.550000,32.827608,27.827608,0.147579,5.00,0.1429,-0.1372,-0.0001,485.242057,8.457943,,,,0.000000
S2,QQQ,2004-06-01,2004-06-30,36.259990,37.740010,34.340582,29.340582,0.258927,5.00,0.1379,-0.1948,-0.0006,474.107268,19.592732,,,,0.000000
S2,QQQ,2004-07-01,2004-07-30,37.660000,34.890000,35.447222,30.447222,0.229764,5.00,0.1328,-0.1718,-0.0006,477.023648,-39.045813,,,,0.000000
S2,QQQ,2004-08-02,2004-08-31,34.610000,34.020000,32.572263,27.572263,0.269727,5.00,0.1445,-0.1926,-0.0008,473.027280,20.672720,,,,0.000000
S2,QQQ,2004-09-01,2004-09-30,33.929990,35.140000,31.862129,26.862129,0.220303,5.00,0.1474,-0.1739,-0.0003,477.969738,15.730262,,,,0.000000
S2,QQQ,2004-10-01,2004-10-29,35.450000,36.899990,32.937557,27.937557,0.164870,5.00,0.1410,-0.1349,-0.0002,483.512990,10.187010,,,,0.000000
S2,QQQ,2004-11-01,2004-11-30,36.980000,39.121990,34.500360,29.500360,0.217231,5.00,0.1352,-0.1577,-0.0007,478.276889,15.423111,,,,0.000000
S2,QQQ,2004-12-01,2004-12-31,39.270000,39.914990,37.213098,32.213098,0.158150,5.00,0.1273,-0.1510,-0.0001,484.185010,9.514990,,,,0.000000
S2,QQQ,2005-01-03,2005-01-31,40.080000,37.399990,38.184397,33.184397,0.138124,5.00,0.1248,-0.1479,-0.0000,486.187586,-70.928298,,,,0.000000
S2,QQQ,2005-02-01,2005-02-28,37.470000,37.220000,35.537840,30.537840,0.165402,5.00,0.1334,-0.1595,-0.0001,483.459757,10.240243,,,,0.000000
S2,QQQ,2005-03-01,2005-03-31,37.370000,36.570010,35.362099,30.362099,0.154669,5.00,0.1338,-0.1519,-0.0001,484.533145,9.166855,,,,0.000000
S2,QQQ,2005-04-01,2005-04-29,36.820010,34.980000,34.773270,29.773270,0.135030,5.00,0.1358,-0.1400,-0.0000,486.496995,7.203005,,,,0.000000
S2,QQQ,2005-05-02,2005-05-31,35.070010,38.080000,33.237491,28.237491,0.152743,5.00,0.1426,-0.1586,-0.0000,484.725717,8.974283,,,,0.000000
S2,QQQ,2005-06-01,2005-06-30,38.030000,36.780000,36.640042,31.640042,0.145288,5.00,0.1315,-0.1818,-0.0000,485.471248,8.228752,,,,0.000000
S2,QQQ,2005-07-01,2005-07-29,36.860000,39.575000,35.388753,30.388753,0.120405,5.00,0.1356,-0.1611,-0.0000,487.959540,5.740460,,,,0.000000
S2,QQQ,2005-08-01,2005-08-31,39.640000,38.980000,38.176493,33.176493,0.124708,5.00,0.1261,-0.1668,-0.0000,487.529245,6.170755,,,,0.000000
S2,QQQ,2005-09-01,2005-09-30,38.990010,39.460010,37.158146,32.158146,0.174096,5.00,0.1282,-0.1719,-0.0001,482.590391,11.109609,,,,0.000000
S2,QQQ,2005-10-03,2005-10-31,39.550000,38.870000,37.934560,32.934560,0.132549,5.00,0.1264,-0.1618,-0.0000,486.745115,6.954885,,,,0.000000
S2,QQQ,2005-11-01,2005-11-30,38.759990,41.240010,37.323635,32.323635,0.168320,5.00,0.1290,-0.1938,-0.0000,483.167952,10.532048,,,,0.000000
S2,QQQ,2005-12-01,2005-12-30,41.509990,40.412000,39.938633,34.938633,0.089403,5.00,0.1205,-0.1377,-0.0000,491.059663,2.640337,,,,0.000000
S2,QQQ,2006-01-03,2006-01-31,40.640000,42.000000,39.027216,34.027216,0.101828,5.00,0.1230,-0.1440,-0.0000,489.817195,3.882805,,,,0.000000
S2,QQQ,2006-02-01,2006-02-28,41.759990,41.100010,40.040025,35.040025,0.232345,5.00,0.1197,-0.2048,-0.0004,476.765546,16.934454,,,,0.000000
S2,QQQ,2006-03-01,2006-03-31,41.220000,41.929990,39.226029,34.226029,0.165783,5.00,0.1213,-0.1636,-0.0002,483.421723,10.278277,,,,0.000000
S2,QQQ,2006-04-03,2006-04-28,42.149990,41.850010,40.193894,35.193894,0.136244,5.00,0.1186,-0.1492,-0.0001,486.375554,7.324446,,,,0.000000
S2,QQQ,2006-05-01,2006-05-31,41.929990,38.820010,40.001276,35.001276,0.169895,5.00,0.1192,-0.1695,-0.0002,483.010509,-107.437159,,,,0.000000
S2,QQQ,2006-06-01,2006-06-30,38.910000,38.770000,36.872591,31.872591,0.177757,5.00,0.1285,-0.1662,-0.0002,482.224253,11.475747,,,,0.000000
S2,QQQ,2006-07-03,2006-07-31,38.880000,37.100010,36.757873,31.757873,0.181162,5.00,0.1286,-0.1638,-0.0003,481.883815,11.816185,,,,0.000000
S2,QQQ,2006-08-01,2006-08-31,36.789990,38.870000,35.294302,30.294302,0.234431,5.00,0.1359,-0.2203,-0.0002,476.556933,17.143067,,,,0.000000
S2,QQQ,2006-09-01,2006-09-29,39.070010,40.649990,37.080161,32.080161,0.146626,5.00,0.1280,-0.1539,-0.0001,485.337371,8.362629,,,,0.000000
S2,QQQ,2006-10-02,2006-10-31,40.600010,42.580000,38.595110,33.595110,0.210444,5.00,0.1232,-0.1821,-0.0005,478.955615,14.744385,,,,0.000000
S2,QQQ,2006-11-01,2006-11-30,42.730000,44.039990,40.362932,35.362932,0.196023,5.00,0.1170,-0.1618,-0.0007,480.397712,13.302288,,,,0.000000
S2,QQQ,2006-12-01,2006-12-29,44.000000,43.160000,41.524410,36.524410,0.253733,5.00,0.1136,-0.1781,-0.0019,474.626746,19.073254,,,,0.000000
S2,QQQ,2007-01-03,2007-01-31,43.460010,44.070010,41.032005,36.032005,0.165631,5.00,0.1150,-0.1466,-0.0004,483.436859,10.263141,,,,0.000000
S2,QQQ,2007-02-01,2007-02-28,44.270000,43.330000,42.096010,37.096010,0.164140,5.00,0.1129,-0.1561,-0.0002,483.586024,10.113976,,,,0.000000
S2,QQQ,2007-03-01,2007-03-30,42.550000,43.530000,41.430949,36.430949,0.350576,5.00,0.1175,-0.2897,-0.0009,464.942409,28.757591,,,,0.000000
S2,QQQ,2007-04-02,2007-04-30,43.670000,45.960010,41.768373,36.768373,0.152500,5.00,0.1145,-0.1630,-0.0001,484.750021,8.949979,,,,0.000000
S2,QQQ,2007-05-01,2007-05-31,45.970000,47.410000,44.230755,39.230755,0.170078,5.00,0.1088,-0.1818,-0.0001,482.992243,10.707757,,,,0.000000
S2,QQQ,2007-06-01,2007-06-29,47.580000,47.600010,45.523699,40.523699,0.159887,5.00,0.1051,-0.1603,-0.0002,484.011282,9.688718,,,,0.000000
S2,QQQ,2007-07-02,2007-07-31,47.710010,47.530000,45.144705,40.144705,0.223598,5.00,0.1048,-0.1658,-0.0015,477.640183,16.059817,,,,0.000000
S2,QQQ,2007-08-01,2007-08-31,47.390000,48.870000,45.220303,40.220303,0.250476,5.00,0.1055,-0.1917,-0.0014,474.952382,18.747618,,,,0.000000
S2,QQQ,2007-09-04,2007-09-28,48.920000,51.410000,46.094135,41.094135,0.258386,5.00,0.1022,-0.1659,-0.0027,474.161417,19.538583,,,,0.000000
S2,QQQ,2007-10-01,2007-10-31,51.450000,55.030000,48.966851,43.966851,0.229575,5.00,0.0972,-0.1703,-0.0015,477.042506,16.657494,,,,0.000000
S2,QQQ,2007-11-01,2007-11-30,54.679990,51.310000,52.014175,47.014175,0.348219,5.00,0.0914,-0.2001,-0.0066,465.178053,-41.895506,,,,0.000000
S2,QQQ,2007-12-03,2007-12-31,51.140000,51.220000,47.194481,42.194481,0.412229,5.00,0.0978,-0.1757,-0.0151,458.777065,34.922935,,,,0.000000
S2,QQQ,2008-01-02,2008-01-31,51.270000,45.130000,48.268379,43.268379,0.274477,5.00,0.0975,-0.1661,-0.0038,472.552337,-292.690199,,,,0.000000
S2,QQQ,2008-02-01,2008-02-29,45.520000,42.950000,41.366500,36.366500,0.303829,5.00,0.1098,-0.1429,-0.0073,469.617143,24.082857,,,,0.000000
S2,QQQ,2008-03-03,2008-03-31,42.929990,43.720000,40.076753,35.076753,0.277475,5.00,0.1165,-0.1669,-0.0028,472.252521,21.447479,,,,0.000000
S2,QQQ,2008-04-01,2008-04-30,44.450000,47.210010,40.225237,35.225237,0.234512,5.00,0.1125,-0.1211,-0.0038,476.548761,17.151239,,,,0.000000
S2,QQQ,2008-05-01,2008-05-30,47.240010,50.009990,44.264728,39.264728,0.271934,5.00,0.1058,-0.1615,-0.0030,472.806577,20.893423,,,,0.000000
S2,QQQ,2008-06-02,2008-06-30,49.920000,45.170000,46.891403,41.891403,0.307627,5.00,0.1002,-0.1717,-0.0048,469.237335,-147.677668,,,,0.000000
S2,QQQ,2008-07-01,2008-07-31,44.860000,45.460010,41.810666,36.810666,0.370133,5.00,0.1115,-0.1856,-0.0074,462.986663,30.713337,,,,0.000000
S2,QQQ,2008-08-01,2008-08-29,45.520000,46.120000,41.911944,36.911944,0.327483,5.00,0.1098,-0.1599,-0.0070,467.251730,26.448270,,,,0.000000
S2,QQQ,2008-09-02,2008-09-30,46.860000,38.910000,43.259167,38.259167,0.172359,5.00,0.1067,-0.1131,-0.0013,482.764143,-423.980840,,,,0.000000
S2,QQQ,2008-10-01,2008-10-31,38.830000,32.890000,35.455852,30.455852,0.345191,5.00,0.1288,-0.1669,-0.0062,465.480899,-228.366070,,,,0.000000
S2,QQQ,2008-11-03,2008-11-28,32.810000,29.120000,28.428772,23.428772,0.462006,5.00,0.1524,-0.1644,-0.0144,453.799369,39.900631,,,,0.000000
S2,QQQ,2008-12-01,2008-12-31,28.500000,29.740010,25.053661,20.053661,0.523094,5.00,0.1754,-0.1940,-0.0135,447.690579,46.009421,,,,0.000000
S2,QQQ,2009-01-02,2009-01-30,29.770000,29.060000,26.882543,21.882543,0.276186,5.00,0.1680,-0.1578,-0.0018,472.381422,21.318578,,,,0.000000
S2,QQQ,2009-02-02,2009-02-27,28.770000,27.530000,26.386508,21.386508,0.311273,5.00,0.1738,-0.1852,-0.0016,468.872718,24.827282,,,,0.000000
S2,QQQ,2009-03-02,2009-03-31,27.120000,30.320010,24.503385,19.503385,0.375714,5.00,0.1844,-0.1914,-0.0035,462.428582,31.271418,,,,0.000000
S2,QQQ,2009-04-01,2009-04-30,29.940000,34.280000,27.402236,22.402236,0.352321,5.00,0.1670,-0.1904,-0.0030,464.767934,28.932066,,,,0.000000
S2,QQQ,2009-05-01,2009-05-29,34.280000,35.380000,31.269163,26.269163,0.290986,5.00,0.1459,-0.1602,-0.0027,470.901420,22.798580,,,,0.000000
S2,QQQ,2009-06-01,2009-06-30,35.730000,36.380000,32.826473,27.826473,0.191286,5.00,0.1399,-0.1318,-0.0006,480.871354,12.828646,,,,0.000000
S2,QQQ,2009-07-01,2009-07-31,36.539990,39.450000,34.014346,29.014346,0.197516,5.00,0.1368,-0.1458,-0.0005,480.248362,13.451638,,,,0.000000
S2,QQQ,2009-08-03,2009-08-31,39.850010,40.030000,37.001713,32.001713,0.171517,5.00,0.1255,-0.1265,-0.0005,482.848311,10.851689,,,,0.000000
S2,QQQ,2009-09-01,2009-09-30,39.870000,42.250000,37.362231,32.362231,0.276411,5.00,0.1254,-0.1743,-0.0017,472.358886,21.341114,,,,0.000000
S2,QQQ,2009-10-01,2009-10-30,42.110000,40.960010,39.313984,34.313984,0.297822,5.00,0.1187,-0.1712,-0.0029,470.217818,23.482182,,,,0.000000
S2,QQQ,2009-11-02,2009-11-30,41.009990,43.560000,38.294525,33.294525,0.241017,5.00,0.1219,-0.1560,-0.0013,475.898317,17.801683,,,,0.000000
S2,QQQ,2009-12-01,2009-12-31,43.880000,45.750000,41.174574,36.174574,0.173143,5.00,0.1139,-0.1315,-0.0004,482.685692,11.014308,,,,0.000000
S2,QQQ,2010-01-04,2010-01-29,46.320010,42.789990,43.507771,38.507771,0.128939,5.00,0.1079,-0.1091,-0.0002,487.106091,-65.184201,,,,0.000000
S2,QQQ,2010-02-01,2010-02-26,42.910000,44.759990,40.081811,35.081811,0.233459,5.00,0.1165,-0.1504,-0.0014,476.654056,17.045944,,,,0.000000
S2,QQQ,2010-03-01,2010-03-31,44.950000,48.160000,41.919824,36.919824,0.235262,5.00,0.1112,-0.1457,-0.0018,476.473818,17.226182,,,,0.000000
S2,QQQ,2010-04-01,2010-04-30,48.340000,49.237500,45.639654,40.639654,0.203808,5.00,0.1034,-0.1447,-0.0008,479.619173,14.080827,,,,0.000000
S2,QQQ,2010-05-03,2010-05-28,49.429990,45.600010,46.633112,41.633112,0.209696,5.00,0.1012,-0.1442,-0.0011,479.030450,-88.640610,,,,0.000000
S2,QQQ,2010-06-01,2010-06-30,45.450000,42.710010,41.286762,36.286762,0.425206,5.00,0.1100,-0.1680,-0.0145,457.479358,36.220642,,,,0.000000
S2,QQQ,2010-07-01,2010-07-30,42.820010,45.810000,39.399676,34.399676,0.295023,5.00,0.1168,-0.1530,-0.0044,470.497738,23.202262,,,,0.000000
S2,QQQ,2010-08-02,2010-08-31,46.380000,43.460010,42.842060,37.842060,0.197377,5.00,0.1078,-0.1211,-0.0016,480.262270,13.437730,,,,0.000000
S2,QQQ,2010-09-01,2010-09-30,44.100010,49.070010,40.198503,35.198503,0.219185,5.00,0.1134,-0.1207,-0.0026,478.081536,15.618464,,,,0.000000
S2,QQQ,2010-10-01,2010-10-29,49.460010,52.179990,46.158238,41.158238,0.212510,5.00,0.1011,-0.1320,-0.0018,478.749029,14.950971,,,,0.000000
S2,QQQ,2010-11-01,2010-11-30,52.380000,52.085010,49.131933,44.131933,0.249714,5.00,0.0955,-0.1460,-0.0028,475.028571,18.671429,,,,0.000000
S2,QQQ,2010-12-01,2010-12-31,52.870000,54.460010,49.094620,44.094620,0.171853,5.00,0.0946,-0.1083,-0.0014,482.814654,10.885346,,,,0.000000
S2,QQQ,2011-01-03,2011-01-31,54.959000,56.000000,51.632334,46.632334,0.188392,5.00,0.0910,-0.1236,-0.0013,481.160807,12.539193,,,,0.000000
S2,QQQ,2011-02-01,2011-02-28,56.419400,57.768910,53.300835,48.300835,0.185789,5.00,0.0886,-0.1275,-0.0011,481.421139,12.278861,,,,0.000000
S2,QQQ,2011-03-01,2011-03-31,57.990010,57.429990,53.431652,48.431652,0.358535,5.00,0.0862,-0.1492,-0.0126,464.146487,29.553513,,,,0.000000
S2,QQQ,2011-04-01,2011-04-29,57.720000,59.080000,53.867528,48.867528,0.281627,5.00,0.0866,-0.1426,-0.0057,471.837317,21.862683,,,,0.000000
S2,QQQ,2011-05-02,2011-05-31,59.190000,58.360000,56.163905,51.163905,0.247161,5.00,0.0845,-0.1517,-0.0025,475.283917,18.416083,,,,0.000000
S2,QQQ,2011-06-01,2011-06-30,58.220000,57.050000,55.256721,50.256721,0.304043,5.00,0.0859,-0.1707,-0.0043,469.595714,24.104286,,,,0.000000
S2,QQQ,2011-07-01,2011-07-29,57.100010,58.000000,53.389098,48.389098,0.324747,5.00,0.0876,-0.1570,-0.0076,467.525298,26.174702,,,,0.000000
S2,QQQ,2011-08-01,2011-08-31,58.670000,55.060000,54.272903,49.272903,0.247790,5.00,0.0852,-0.1232,-0.0053,475.221021,18.478979,,,,0.000000
S2,QQQ,2011-09-01,2011-09-30,55.210010,52.490010,49.846191,44.846191,0.442183,5.00,0.0906,-0.1538,-0.0217,455.781742,37.918258,,,,0.000000
S2,QQQ,2011-10-03,2011-10-31,52.039990,57.950000,47.567420,42.567420,0.510188,5.00,0.0961,-0.1809,-0.0242,448.981184,44.718816,,,,0.000000
S2,QQQ,2011-11-01,2011-11-30,56.560000,56.390000,53.545173,48.545173,0.641209,5.00,0.0884,-0.2414,-0.0298,435.879115,57.820885,,,,0.000000
S2,QQQ,2011-12-01,2011-12-30,56.370000,55.830000,51.689552,46.689552,0.423156,5.00,0.0887,-0.1610,-0.0179,457.684414,36.015586,,,,0.000000
S2,QQQ,2012-01-03,2012-01-31,56.910000,60.530000,52.687481,47.687481,0.153692,5.00,0.0879,-0.0946,-0.0015,484.630834,9.069166,,,,0.000000
S2,QQQ,2012-02-01,2012-02-29,60.850010,64.410000,57.575139,52.575139,0.220455,5.00,0.0822,-0.1366,-0.0022,477.954510,15.745490,,,,0.000000
S2,QQQ,2012-03-01,2012-03-30,64.660000,67.550000,61.402747,56.402747,0.233750,5.00,0.0773,-0.1420,-0.0026,476.625050,17.074950,,,,0.000000
S2,QQQ,2012-04-02,2012-04-30,67.460010,66.759990,64.569311,59.569311,0.281696,5.00,0.0741,-0.1674,-0.0035,471.830380,21.869620,,,,0.000000
S2,QQQ,2012-05-01,2012-05-31,66.679990,62.060000,63.166468,58.166468,0.333806,5.00,0.0750,-0.1655,-0.0080,466.619388,-83.566164,,,,0.000000
S2,QQQ,2012-06-01,2012-06-29,60.970000,64.160000,57.716669,52.716669,0.572899,5.00,0.0820,-0.2236,-0.0254,442.710148,50.989852,,,,0.000000
S2,QQQ,2012-07-02,2012-07-31,64.230000,64.800000,60.130273,55.130273,0.349115,5.00,0.0778,-0.1564,-0.0109,465.088546,28.611454,,,,0.000000
S2,QQQ,2012-08-01,2012-08-31,65.250000,68.160000,61.159995,56.159995,0.263500,5.00,0.0766,-0.1339,-0.0057,473.649999,20.050001,,,,0.000000
S2,QQQ,2012-09-04,2012-09-28,68.030000,68.570010,64.985118,59.985118,0.305297,5.00,0.0735,-0.1700,-0.0050,469.470300,24.229700,,,,0.000000
S2,QQQ,2012-10-01,2012-10-31,68.899990,64.950000,65.230995,60.230995,0.251256,5.00,0.0726,-0.1388,-0.0043,474.874439,-9.273971,,,,0.000000
S2,QQQ,2012-11-01,2012-11-30,65.320010,65.800000,61.086869,56.086869,0.293108,5.00,0.0765,-0.1396,-0.0077,470.689179,23.010821,,,,0.000000
S2,QQQ,2012-12-03,2012-12-31,66.320010,65.130100,62.524610,57.524610,0.222075,5.00,0.0754,-0.1267,-0.0033,477.792494,15.907506,,,,0.000000
S2,QQQ,2013-01-02,2013-01-31,66.690000,66.870000,61.100821,56.100821,0.180275,5.00,0.0750,-0.0886,-0.0042,481.972458,11.727542,,,,0.000000
S2,QQQ,2013-02-01,2013-02-28,67.340000,67.100010,64.032903,59.032903,0.188647,5.00,0.0743,-0.1251,-0.0015,481.135331,12.564669,,,,0.000000
S2,QQQ,2013-03-01,2013-03-28,66.860000,68.970000,63.120417,58.120417,0.390902,5.00,0.0748,-0.1745,-0.0127,460.909808,32.790192,,,,0.000000
S2,QQQ,2013-04-01,2013-04-30,69.009990,70.720000,65.959396,60.959396,0.263311,5.00,0.0725,-0.1573,-0.0033,473.668892,20.031108,,,,0.000000
S2,QQQ,2013-05-01,2013-05-31,70.710010,73.250000,67.718830,62.718830,0.269683,5.00,0.0707,-0.1610,-0.0034,473.031656,20.668344,,,,0.000000
S2,QQQ,2013-06-03,2013-06-28,73.310000,71.270000,70.254316,65.254316,0.257639,5.00,0.0682,-0.1556,-0.0032,474.236057,19.463943,,,,0.000000
S2,QQQ,2013-07-01,2013-07-31,71.759990,75.770000,67.602303,62.602303,0.257827,5.00,0.0697,-0.1316,-0.0058,474.217322,19.482678,,,,0.000000
S2,QQQ,2013-08-01,2013-08-30,76.300000,75.470000,73.172305,68.172305,0.158177,5.00,0.0655,-0.1172,-0.0008,484.182276,9.517724,,,,0.000000
S2,QQQ,2013-09-03,2013-09-30,76.100010,78.880000,72.046232,67.046232,0.218357,5.00,0.0657,-0.1215,-0.0038,478.164324,15.535676,,,,0.000000
S2,QQQ,2013-10-01,2013-10-31,78.870000,82.790000,75.498685,70.498685,0.300360,5.00,0.0634,-0.1608,-0.0060,469.964020,23.735980,,,,0.000000
S2,QQQ,2013-11-01,2013-11-29,83.040000,85.730000,79.536890,74.536890,0.250386,5.00,0.0602,-0.1430,-0.0041,474.961445,18.738555,,,,0.000000
S2,QQQ,2013-12-02,2013-12-31,85.830000,87.960000,82.402450,77.402450,0.277796,5.00,0.0583,-0.1535,-0.0052,472.220362,21.479638,,,,0.000000
S2,QQQ,2014-01-02,2014-01-31,87.550000,86.270000,84.672418,79.672418,0.358224,5.00,0.0571,-0.1912,-0.0076,464.177622,29.522378,,,,0.000000
S2,QQQ,2014-02-03,2014-02-28,86.140000,90.340000,82.429990,77.429990,0.354376,5.00,0.0580,-0.1681,-0.0109,464.562376,29.137624,,,,0.000000
S2,QQQ,2014-03-03,2014-03-31,89.480000,87.670000,86.715798,81.715798,0.469686,5.00,0.0559,-0.2217,-0.0147,453.031447,40.668553,,,,0.000000
S2,QQQ,2014-04-01,2014-04-30,88.100000,87.390000,83.543728,78.543728,0.297171,5.00,0.0568,-0.1374,-0.0098,470.282858,23.417142,,,,0.000000
S2,QQQ,2014-05-01,2014-05-30,87.530000,91.310000,82.911501,77.911501,0.362473,5.00,0.0571,-0.1530,-0.0151,463.752698,29.947302,,,,0.000000
S2,QQQ,2014-06-02,2014-06-30,91.430000,93.910000,87.233817,82.233817,0.333769,5.00,0.0547,-0.1534,-0.0114,466.623075,27.076925,,,,0.000000
S2,QQQ,2014-07-01,2014-07-31,94.210000,95.020000,89.459302,84.459302,0.336623,5.00,0.0531,-0.1451,-0.0137,466.337742,27.362258,,,,0.000000
S2,QQQ,2014-08-01,2014-08-29,94.830000,99.780000,90.863949,85.863949,0.384831,5.00,0.0527,-0.1709,-0.0147,461.516899,32.183101,,,,0.000000
S2,QQQ,2014-09-02,2014-09-30,100.040000,98.790000,96.329394,91.329394,0.262333,5.00,0.0500,-0.1432,-0.0055,473.766670,19.933330,,,,0.000000
S2,QQQ,2014-10-01,2014-10-31,98.540000,101.400000,93.791112,88.791112,0.449168,5.00,0.0507,-0.1718,-0.0245,455.083191,38.616809,,,,0.000000
S2,QQQ,2014-11-03,2014-11-28,101.530000,106.010000,97.114667,92.114667,0.345189,5.00,0.0492,-0.1532,-0.0135,465.481090,28.218910,,,,0.000000
S2,QQQ,2014-12-01,2014-12-31,105.720000,103.250000,101.601525,96.601525,0.414963,5.00,0.0473,-0.1758,-0.0184,458.503708,35.196292,,,,0.000000
S2,QQQ,2015-01-02,2015-01-30,103.760000,101.100000,98.794746,93.794746,0.307420,5.00,0.0482,-0.1351,-0.0123,469.258010,24.441990,,,,0.000000
S2,QQQ,2015-02-02,2015-02-27,101.330000,108.400000,96.254620,91.254620,0.371527,5.00,0.0493,-0.1494,-0.0183,462.847320,30.852680,,,,0.000000
S2,QQQ,2015-03-02,2015-03-31,108.610000,105.600000,104.112074,99.112074,0.332709,5.00,0.0460,-0.1490,-0.0130,466.729123,26.970877,,,,0.000000
S2,QQQ,2015-04-01,2015-04-30,105.600000,107.630000,100.754863,95.754863,0.401255,5.00,0.0473,-0.1602,-0.0204,459.874474,33.825526,,,,0.000000
S2,QQQ,2015-05-01,2015-05-29,108.050000,110.050000,103.510439,98.510439,0.292565,5.00,0.0463,-0.1376,-0.0100,470.743540,22.956460,,,,0.000000
S2,QQQ,2015-06-01,2015-06-30,110.640000,107.070000,105.104383,100.104383,0.330870,5.00,0.0452,-0.1341,-0.0164,466.913029,26.786971,,,,0.000000
S2,QQQ,2015-07-01,2015-07-31,108.130000,111.950000,101.825235,96.825235,0.300501,5.00,0.0462,-0.1181,-0.0156,469.949940,23.750060,,,,0.000000
S2,QQQ,2015-08-03,2015-08-31,111.970000,104.310000,107.094490,102.094490,0.397433,5.00,0.0447,-0.1593,-0.0205,460.256679,-245.005670,,,,0.000000
S2,QQQ,2015-09-01,2015-09-30,101.710000,101.760000,94.639338,89.639338,0.924391,5.00,0.0492,-0.2268,-0.1011,407.560912,86.139088,,,,0.000000
S2,QQQ,2015-10-01,2015-10-30,101.940000,113.330000,94.483018,89.483018,0.518343,5.00,0.0490,-0.1545,-0.0429,448.165710,45.534290,,,,0.000000
S2,QQQ,2015-11-02,2015-11-30,113.630000,114.020000,107.999228,102.999228,0.390658,5.00,0.0440,-0.1476,-0.0227,460.934204,32.765796,,,,0.000000
S2,QQQ,2015-12-01,2015-12-31,114.475000,111.860000,108.506675,103.506675,0.383654,5.00,0.0437,-0.1424,-0.0233,461.634623,32.065377,,,,0.000000
S2,QQQ,2016-01-04,2016-01-29,109.430000,104.130000,106.704293,101.704293,0.860988,5.00,0.0457,-0.2941,-0.0636,413.901159,-177.630475,,,,0.000000
S2,QQQ,2016-02-01,2016-02-29,103.620000,102.500000,97.125357,92.125357,0.587492,5.00,0.0483,-0.1778,-0.0496,441.250758,52.449242,,,,0.000000
S2,QQQ,2016-03-01,2016-03-31,103.450000,109.200000,95.695502,90.695502,0.412462,5.00,0.0483,-0.1316,-0.0311,458.753814,34.946186,,,,0.000000
S2,QQQ,2016-04-01,2016-04-29,108.580000,105.720000,103.781031,98.781031,0.526038,5.00,0.0460,-0.1888,-0.0346,447.396205,46.303795,,,,0.000000
S2,QQQ,2016-05-02,2016-05-31,105.970000,110.340000,100.719894,95.719894,0.379034,5.00,0.0472,-0.1497,-0.0201,462.096558,31.603442,,,,0.000000
S2,QQQ,2016-06-01,2016-06-30,110.000000,107.540000,105.179510,100.179510,0.469446,5.00,0.0455,-0.1768,-0.0281,453.055438,40.644562,,,,0.000000
S2,QQQ,2016-07-01,2016-07-29,107.490000,115.230000,99.701748,94.701748,0.566546,5.00,0.0465,-0.1620,-0.0512,443.345428,50.354572,,,,0.000000
S2,QQQ,2016-08-01,2016-08-31,115.310000,116.440000,110.491714,105.491714,0.382079,5.00,0.0434,-0.1575,-0.0192,461.792098,31.907902,,,,0.000000
S2,QQQ,2016-09-01,2016-09-30,116.480000,118.720000,111.569541,106.569541,0.395982,5.00,0.0429,-0.1595,-0.0210,460.401792,33.298208,,,,0.000000
S2,QQQ,2016-10-03,2016-10-31,118.530000,116.990000,114.191851,109.191851,0.406059,5.00,0.0422,-0.1713,-0.0195,459.394123,34.305877,,,,0.000000
S2,QQQ,2016-11-01,2016-11-30,117.190000,117.500000,112.093744,107.093744,0.375838,5.00,0.0427,-0.1520,-0.0197,462.416152,31.283848,,,,0.000000
S2,QQQ,2016-12-01,2016-12-30,117.460000,118.480000,112.891397,107.891397,0.390868,5.00,0.0426,-0.1644,-0.0193,460.913234,32.786766,,,,0.000000
S2,QQQ,2017-01-03,2017-01-31,119.310000,124.570000,113.393543,108.393543,0.313878,5.00,0.0419,-0.1274,-0.0167,468.612152,25.087848,,,,0.000000
S2,QQQ,2017-02-01,2017-02-28,125.420000,130.020000,119.914408,114.914408,0.280777,5.00,0.0399,-0.1236,-0.0127,471.922270,21.777730,,,,0.000000
S2,QQQ,2017-03-01,2017-03-31,130.810000,132.380000,124.749123,119.749123,0.328009,5.00,0.0382,-0.1301,-0.0189,467.199062,26.500938,,,,0.000000
S2,QQQ,2017-04-03,2017-04-28,132.480000,135.990000,128.476413,123.476413,0.320630,5.00,0.0377,-0.1583,-0.0114,467.937049,25.762951,,,,0.000000
S2,QQQ,2017-05-01,2017-05-31,136.460000,141.290000,132.134979,127.134979,0.268495,5.00,0.0366,-0.1386,-0.0089,473.150517,20.549483,,,,0.000000
S2,QQQ,2017-06-01,2017-06-30,141.570000,137.640000,136.862047,131.862047,0.334358,5.00,0.0353,-0.1511,-0.0158,466.564242,27.135758,,,,0.000000
S2,QQQ,2017-07-03,2017-07-31,138.250000,143.230000,131.198756,126.198756,0.416945,5.00,0.0362,-0.1430,-0.0329,458.305536,35.394464,,,,0.000000
S2,QQQ,2017-08-01,2017-08-31,143.700000,146.200000,136.546627,131.546627,0.444141,5.00,0.0348,-0.1489,-0.0373,455.585904,38.114096,,,,0.000000
S2,QQQ,2017-09-01,2017-09-29,146.360000,145.450000,138.533940,133.533940,0.520472,5.00,0.0342,-0.1587,-0.0495,447.952784,45.747216,,,,0.000000
S2,QQQ,2017-10-02,2017-10-31,145.670000,152.150000,139.294338,134.294338,0.444799,5.00,0.0343,-0.1564,-0.0348,455.520061,38.179939,,,,0.000000
S2,QQQ,2017-11-01,2017-11-30,152.750000,155.150000,145.333231,140.333231,0.434344,5.00,0.0327,-0.1450,-0.0371,456.565631,37.134369,,,,0.000000
S2,QQQ,2017-12-01,2017-12-29,154.190000,155.760000,147.880307,142.880307,0.637490,5.00,0.0324,-0.1970,-0.0626,436.251014,57.448986,,,,0.000000
S2,QQQ,2018-01-02,2018-01-31,156.500000,169.400000,148.108982,143.108982,0.459307,5.00,0.0319,-0.1438,-0.0436,454.069277,39.630723,,,,0.000000
S2,QQQ,2018-02-01,2018-02-28,168.120000,167.210000,161.807642,156.807642,0.685250,5.00,0.0297,-0.2073,-0.0715,431.474952,62.225048,,,,0.000000
S2,QQQ,2018-03-01,2018-03-29,167.290000,160.130000,158.955505,153.955505,0.547861,5.00,0.0299,-0.1636,-0.0575,445.213912,48.486088,,,,0.000000
S2,QQQ,2018-04-02,2018-04-30,159.000000,160.940000,150.203948,145.203948,0.723288,5.00,0.0314,-0.1921,-0.0857,427.671250,66.028750,,,,0.000000
S2,QQQ,2018-05-01,2018-05-31,160.520000,170.070000,151.715454,146.715454,0.633019,5.00,0.0311,-0.1764,-0.0718,436.698069,57.001931,,,,0.000000
S2,QQQ,2018-06-01,2018-06-29,170.880000,171.650000,162.234172,157.234172,0.459826,5.00,0.0293,-0.1446,-0.0461,454.017368,39.682632,,,,0.000000
S2,QQQ,2018-07-02,2018-07-31,170.040000,176.450000,162.181416,157.181416,0.762983,5.00,0.0294,-0.2081,-0.0915,423.701717,69.998283,,,,0.000000
S2,QQQ,2018-08-01,2018-08-31,176.870000,186.650000,168.532723,163.532723,0.500970,5.00,0.0283,-0.1564,-0.0522,449.903046,43.796954,,,,0.000000
S2,QQQ,2018-09-04,2018-09-28,186.100000,185.790000,177.832620,172.832620,0.627482,5.00,0.0269,-0.1815,-0.0715,437.251775,56.448225,,,,0.000000
S2,QQQ,2018-10-01,2018-10-31,186.820000,169.820000,175.512886,170.512886,0.528433,5.00,0.0268,-0.1456,-0.0630,447.156679,-453.456679,,,,0.000000
S2,QQQ,2018-11-01,2018-11-30,170.080000,169.370000,154.561828,149.561828,0.717146,5.00,0.0294,-0.1608,-0.0943,428.285418,65.414582,,,,0.000000
S2,QQQ,2018-12-03,2018-12-31,173.100000,154.260000,157.132944,152.132944,0.422080,5.00,0.0289,-0.1071,-0.0501,457.792001,-251.386407,,,,0.000000
S2,QQQ,2019-01-02,2019-01-31,150.990000,168.160000,138.298917,133.298917,0.992115,5.00,0.0331,-0.2124,-0.1340,400.788543,92.911457,,,,0.000000
S2,QQQ,2019-02-01,2019-02-28,167.370000,173.190000,157.840547,152.840547,0.695511,5.00,0.0299,-0.1844,-0.0847,430.448916,63.251084,,,,0.000000
S2,QQQ,2019-03-01,2019-03-29,174.410000,179.660000,164.909519,159.909519,0.443479,5.00,0.0287,-0.1374,-0.0466,455.652078,38.047922,,,,0.000000
S2,QQQ,2019-04-01,2019-04-30,181.420000,189.540000,170.673144,165.673144,0.427100,5.00,0.0276,-0.1279,-0.0468,457.290021,36.409979,,,,0.000000
S2,QQQ,2019-05-01,2019-05-31,190.760000,173.950000,181.205088,176.205088,0.443528,5.00,0.0262,-0.1387,-0.0480,455.647244,-461.947244,,,,0.000000
S2,QQQ,2019-06-03,2019-06-28,173.520000,186.740000,164.457244,159.457244,0.637544,5.00,0.0288,-0.1772,-0.0747,436.245572,57.454428,,,,0.000000
S2,QQQ,2019-07-01,2019-07-31,190.300000,191.100000,175.661975,170.661975,0.384151,5.00,0.0263,-0.1045,-0.0448,461.584910,32.115090,,,,0.000000
S2,QQQ,2019-08-01,2019-08-30,191.510000,187.470000,182.587506,177.587506,0.521471,5.00,0.0261,-0.1577,-0.0578,447.852894,45.847106,,,,0.000000
S2,QQQ,2019-09-03,2019-09-30,186.260000,188.810000,175.914568,170.914568,0.750487,5.00,0.0268,-0.1902,-0.0963,424.951252,68.748748,,,,0.000000
S2,QQQ,2019-10-01,2019-10-31,189.540000,197.080000,179.240610,174.240610,0.527829,5.00,0.0264,-0.1499,-0.0608,447.217088,46.482912,,,,0.000000
S2,QQQ,2019-11-01,2019-11-29,197.930000,205.100000,189.202339,184.202339,0.451736,5.00,0.0253,-0.1435,-0.0460,454.826368,38.873632,,,,0.000000
S2,QQQ,2019-12-02,2019-12-31,205.110000,212.610000,196.984019,191.984019,0.542846,5.00,0.0244,-0.1670,-0.0586,445.715408,47.984592,,,,0.000000
S2,QQQ,2020-01-02,2020-01-31,214.400000,219.070000,204.152894,199.152894,0.392947,5.00,0.0233,-0.1230,-0.0412,460.705255,32.994745,,,,0.000000
S2,QQQ,2020-02-03,2020-02-28,220.140000,205.800000,208.029420,203.029420,0.536066,5.00,0.0227,-0.1437,-0.0656,446.393417,-175.635376,,,,0.000000
S2,QQQ,2020-03-02,2020-03-31,208.880000,190.400000,188.390073,183.390073,0.580133,5.00,0.0239,-0.1274,-0.0774,441.986702,51.713298,,,,0.000000
S2,QQQ,2020-04-01,2020-04-30,184.810000,218.910000,162.803809,157.803809,1.150978,5.00,0.0271,-0.2057,-0.1580,384.902174,108.797826,,,,0.000000
S2,QQQ,2020-05-01,2020-05-29,214.540000,233.360000,200.592304,195.592304,1.034291,5.00,0.0233,-0.2192,-0.1472,396.570868,97.129132,,,,0.000000
S2,QQQ,2020-06-01,2020-06-30,232.400000,247.600000,216.588114,211.588114,0.782865,5.00,0.0215,-0.1735,-0.1077,421.713477,71.986523,,,,0.000000
S2,QQQ,2020-07-01,2020-07-31,247.660000,265.790000,227.552265,222.552265,0.757616,5.00,0.0202,-0.1597,-0.1065,424.238365,69.461635,,,,0.000000
S2,QQQ,2020-08-03,2020-08-31,268.050000,294.880000,248.396655,243.396655,0.591955,5.00,0.0187,-0.1328,-0.0806,440.804465,52.895535,,,,0.000000
S2,QQQ,2020-09-01,2020-09-30,297.600000,277.840000,274.664804,269.664804,0.610859,5.00,0.0168,-0.1320,-0.0862,438.914141,54.785859,,,,0.000000
S2,QQQ,2020-10-01,2020-10-30,281.790000,269.380000,249.183529,244.183529,0.694877,5.00,0.0177,-0.1324,-0.0986,430.512253,63.187747,,,,0.000000
S2,QQQ,2020-11-02,2020-11-30,271.730000,299.620000,237.384644,232.384644,0.795550,5.00,0.0184,-0.1451,-0.1125,420.445033,73.254967,,,,0.000000
S2,QQQ,2020-12-01,2020-12-31,301.870000,313.740000,275.760587,270.760587,0.683557,5.00,0.0166,-0.1402,-0.0987,431.644255,62.055745,,,,0.000000
S2,QQQ,2021-01-04,2021-01-29,315.110000,314.560000,291.397005,286.397005,0.697316,5.00,0.0159,-0.1469,-0.1014,430.268401,63.431599,,,,0.000000
S2,QQQ,2021-02-01,2021-02-26,318.110000,314.140000,288.863102,283.863102,0.651678,5.00,0.0157,-0.1316,-0.0946,434.832238,58.867762,,,,0.000000
S2,QQQ,2021-03-01,2021-03-31,319.270000,319.130000,287.706885,282.706885,0.606098,5.00,0.0157,-0.1212,-0.0873,439.390157,54.309843,,,,0.000000
S2,QQQ,2021-04-01,2021-04-30,323.070000,337.990000,294.852733,289.852733,0.615315,5.00,0.0155,-0.1267,-0.0888,438.468465,55.231535,,,,0.000000
S2,QQQ,2021-05-03,2021-05-28,339.230000,333.930000,314.197710,309.197710,0.712776,5.00,0.0147,-0.1486,-0.1052,428.722423,64.977577,,,,0.000000
S2,QQQ,2021-06-01,2021-06-30,335.300000,354.430000,307.049094,302.049094,0.741587,5.00,0.0149,-0.1490,-0.1100,425.841342,67.858658,,,,0.000000
S2,QQQ,2021-07-01,2021-07-30,354.070000,364.570000,334.128165,329.128165,0.749549,5.00,0.0141,-0.1642,-0.1106,425.045052,68.654948,,,,0.000000
S2,QQQ,2021-08-02,2021-08-31,366.280000,379.950000,341.007145,336.007145,0.683048,5.00,0.0137,-0.1443,-0.1015,431.695165,62.004835,,,,0.000000
S2,QQQ,2021-09-01,2021-09-30,381.040000,357.960000,359.160949,354.160949,0.675632,5.00,0.0131,-0.1485,-0.0997,432.436820,-58.831699,,,,0.000000
S2,QQQ,2021-10-01,2021-10-29,358.600000,386.110000,339.209083,334.209083,0.677700,5.00,0.0139,-0.1525,-0.0981,432.230000,61.470000,,,,0.000000
S2,QQQ,2021-11-01,2021-11-30,386.560000,393.820000,366.416169,361.416169,0.694300,5.00,0.0129,-0.1550,-0.1023,430.570010,63.129990,,,,0.000000
S2,QQQ,2021-12-01,2021-12-31,398.280000,397.850000,368.912280,363.912280,0.585290,5.00,0.0126,-0.1232,-0.0870,441.470984,52.229016,,,,0.000000
S2,QQQ,2022-01-03,2022-01-31,399.050000,363.050000,373.978383,368.978383,0.701115,5.00,0.0125,-0.1490,-0.1057,429.888463,-436.188463,,,,0.000000
S2,QQQ,2022-02-01,2022-02-28,364.430000,346.800000,324.101271,319.101271,0.833784,5.00,0.0137,-0.1528,-0.1246,416.621642,77.078358,,,,0.000000
S2,QQQ,2022-03-01,2022-03-31,345.750000,362.540000,307.951194,302.951194,0.912197,5.00,0.0145,-0.1664,-0.1365,408.780303,84.919697,,,,0.000000
S2,QQQ,2022-04-01,2022-04-29,362.810000,313.250000,336.083939,331.083939,0.773638,5.00,0.0138,-0.1591,-0.1178,422.636204,-428.936204,,,,0.000000
S2,QQQ,2022-05-02,2022-05-31,312.830000,308.280000,276.212519,271.212519,0.901129,5.00,0.0160,-0.1636,-0.1327,409.887111,83.812889,,,,0.000000
S2,QQQ,2022-06-01,2022-06-30,310.470000,280.280000,278.239527,273.239527,0.757205,5.00,0.0161,-0.1466,-0.1120,424.279532,69.420468,,,,0.000000
S2,QQQ,2022-07-01,2022-07-29,278.950000,315.460000,255.873515,250.873515,0.857952,5.00,0.0179,-0.1757,-0.1285,414.204842,79.495158,,,,0.000000
S2,QQQ,2022-08-01,2022-08-31,313.650000,299.270000,289.678354,284.678354,0.875456,5.00,0.0159,-0.1813,-0.1358,412.454375,81.245625,,,,0.000000
S2,QQQ,2022-09-01,2022-09-30,296.720000,267.260000,274.525985,269.525985,0.910243,5.00,0.0169,-0.1898,-0.1411,408.975709,-415.275709,,,,0.000000
S2,QQQ,2022-10-03,2022-10-31,269.070000,277.950000,240.173616,235.173616,0.763151,5.00,0.0186,-0.1515,-0.1131,423.684936,70.015064,,,,0.000000
S2,QQQ,2022-11-01,2022-11-30,281.495000,293.360000,255.525957,250.525957,0.628763,5.00,0.0178,-0.1363,-0.0948,437.123689,56.576311,,,,0.000000
S2,QQQ,2022-12-01,2022-12-30,293.690000,266.280000,274.883361,269.883361,0.715871,5.00,0.0170,-0.1679,-0.1113,428.412911,-434.712911,,,,0.000000
S2,QQQ,2023-01-03,2023-01-31,268.650000,294.620000,248.414351,243.414351,0.608485,5.00,0.0186,-0.1429,-0.0910,439.151497,54.548503,,,,0.000000
S2,QQQ,2023-02-01,2023-02-28,294.410000,293.560000,277.027763,272.027763,0.734981,5.00,0.0170,-0.1755,-0.1147,426.501902,67.198098,,,,0.000000
S2,QQQ,2023-03-01,2023-03-31,293.260000,320.930000,272.049285,267.049285,0.782713,5.00,0.0170,-0.1749,-0.1239,421.728688,71.971312,,,,0.000000
S2,QQQ,2023-04-03,2023-04-28,318.770000,322.560000,301.225224,296.225224,0.857971,5.00,0.0157,-0.1976,-0.1376,414.202917,79.497083,,,,0.000000
S2,QQQ,2023-05-01,2023-05-31,322.090000,347.990000,302.389209,297.389209,0.770924,5.00,0.0155,-0.1800,-0.1256,422.907643,70.792357,,,,0.000000
S2,QQQ,2023-06-01,2023-06-30,347.730000,369.420000,328.552678,323.552678,0.747907,5.00,0.0144,-0.1796,-0.1238,425.209255,68.490745,,,,0.000000
S2,QQQ,2023-07-03,2023-07-31,370.070000,383.680000,352.362754,347.362754,0.669612,5.00,0.0135,-0.1710,-0.1113,433.038807,60.661193,,,,0.000000
S2,QQQ,2023-08-01,2023-08-31,382.310000,377.990000,364.982967,359.982967,0.796607,5.00,0.0131,-0.1972,-0.1364,420.339320,73.360680,,,,0.000000
S2,QQQ,2023-09-01,2023-09-29,380.400000,358.270000,356.723925,351.723925,0.638086,5.00,0.0131,-0.1521,-0.1063,436.191354,57.508646,,,,0.000000
S2,QQQ,2023-10-02,2023-10-31,358.540000,350.870000,334.292470,329.292470,0.762269,5.00,0.0139,-0.1717,-0.1265,423.773066,69.926934,,,,0.000000
S2,QQQ,2023-11-01,2023-11-30,351.720000,388.830000,326.437468,321.437468,0.743951,5.00,0.0142,-0.1659,-0.1224,425.604884,68.095116,,,,0.000000
S2,QQQ,2023-12-01,2023-12-29,387.750000,409.520000,373.743230,368.743230,0.750740,5.00,0.0129,-0.2004,-0.1272,424.926011,68.773989,,,,0.000000
S2,QQQ,2024-01-02,2024-01-31,405.840000,416.970000,392.999279,387.999279,0.931671,5.00,0.0123,-0.2387,-0.1626,406.832885,86.867115,,,,0.000000
S2,QQQ,2024-02-01,2024-02-29,418.790000,439.000000,399.505458,394.505458,0.609637,5.00,0.0119,-0.1588,-0.1038,439.036283,54.663717,,,,0.000000
S2,QQQ,2024-03-01,2024-03-28,439.900000,444.010000,419.947234,414.947234,0.672651,5.00,0.0114,-0.1697,-0.1160,432.734900,60.965100,,,,0.000000
S2,QQQ,2024-04-01,2024-04-30,444.970000,424.590000,423.424292,418.424292,0.686307,5.00,0.0112,-0.1698,-0.1195,431.369298,62.330702,,,,0.000000
S2,QQQ,2024-05-01,2024-05-31,423.150000,450.710000,402.294700,397.294700,0.815159,5.00,0.0118,-0.1935,-0.1419,418.484055,75.215945,,,,0.000000
S2,QQQ,2024-06-03,2024-06-28,454.570000,479.110000,432.244772,427.244772,0.526233,5.00,0.0110,-0.1362,-0.0892,447.376706,46.323294,,,,0.000000
S2,QQQ,2024-07-01,2024-07-31,480.040000,471.070000,457.546270,452.546270,0.694216,5.00,0.0104,-0.1719,-0.1235,430.578424,63.121576,,,,0.000000
S2,QQQ,2024-08-01,2024-08-30,471.760000,476.270000,441.434120,436.434120,0.765827,5.00,0.0106,-0.1694,-0.1326,423.417336,70.282664,,,,0.000000
S2,QQQ,2024-09-03,2024-09-30,473.200000,488.070000,450.063921,445.063921,0.895331,5.00,0.0106,-0.2030,-0.1564,410.466915,83.233085,,,,0.000000
S2,QQQ,2024-10-01,2024-10-31,487.700000,483.850000,460.270532,455.270532,0.789468,5.00,0.0103,-0.1777,-0.1373,421.053176,72.646824,,,,0.000000
S2,QQQ,2024-11-01,2024-11-29,485.500000,509.740000,451.450761,446.450761,0.748961,5.00,0.0103,-0.1604,-0.1273,425.103921,68.596079,,,,0.000000
S2,QQQ,2024-12-02,2024-12-31,511.010000,511.230000,483.418049,478.418049,0.714278,5.00,0.0098,-0.1646,-0.1245,428.572176,65.127824,,,,0.000000
S2,QQQ,2025-01-02,2025-01-31,514.300000,522.290000,485.432063,480.432063,0.643114,5.00,0.0097,-0.1494,-0.1113,435.688582,58.011418,,,,0.000000
S2,QQQ,2025-02-03,2025-02-28,513.470000,508.170000,494.210357,489.210357,1.152215,5.00,0.0097,-0.2535,-0.2027,384.778542,108.921458,,,,0.000000
S2,QQQ,2025-03-03,2025-03-31,511.520000,468.920000,473.570125,468.570125,0.709109,5.00,0.0098,-0.1499,-0.1201,429.089136,-400.401650,,,,0.000000
S2,QQQ,2025-04-01,2025-04-30,467.300000,475.470000,439.533090,434.533090,0.847281,5.00,0.0107,-0.1847,-0.1449,415.271899,78.428101,,,,0.000000
S2,QQQ,2025-05-01,2025-05-30,483.410000,519.110000,441.611421,436.611421,0.586075,5.00,0.0103,-0.1237,-0.0973,441.392527,52.307473,,,,0.000000
S2,QQQ,2025-06-02,2025-06-30,517.240000,551.640000,491.504647,486.504647,0.842271,5.00,0.0097,-0.1897,-0.1470,415.772870,77.927130,,,,0.000000
S2,QQQ,2025-07-01,2025-07-31,549.730000,565.010000,525.626209,520.626209,0.834771,5.00,0.0091,-0.1940,-0.1488,416.522869,77.177131,,,,0.000000
S2,QQQ,2025-08-01,2025-08-29,558.830000,570.400000,540.653456,535.653456,1.035365,5.00,0.0089,-0.2416,-0.1864,396.463515,97.236485,,,,0.000000
S2,QQQ,2025-09-02,2025-09-30,561.310000,600.370000,545.341077,540.341077,1.186127,5.00,0.0089,-0.2722,-0.2142,381.387269,112.312731,,,,0.000000
S2,QQQ,2025-10-01,2025-10-31,597.170000,629.070000,568.796816,563.796816,0.893015,5.00,0.0084,-0.1978,-0.1591,410.698489,83.001511,,,,0.000000
S2,QQQ,2025-11-03,2025-11-28,635.110000,619.250000,596.748680,591.748680,0.597559,5.00,0.0079,-0.1325,-0.1036,440.244103,53.455897,,,,0.000000
S2,QQQ,2025-12-01,2025-12-31,613.630000,614.310000,574.411038,569.411038,0.979590,5.00,0.0081,-0.1990,-0.1706,402.041013,91.658987,,,,0.000000
S2,QQQ,2026-01-02,2026-01-30,620.060000,621.870000,584.629303,579.629303,0.582749,5.00,0.0081,-0.1324,-0.1013,441.725100,51.974900,,,,0.000000
S2,QQQ,2026-02-02,2026-02-27,618.700000,607.290000,588.241756,583.241756,0.892533,5.00,0.0081,-0.1927,-0.1563,410.746725,82.953275,,,,0.000000
S2,QQQ,2026-03-02,2026-03-31,598.860000,577.180000,565.859132,560.859132,1.066311,5.00,0.0083,-0.2192,-0.1867,393.368887,100.331113,,,,0.000000
S2,QQQ,2026-04-01,2026-04-30,581.480000,667.740000,526.506381,521.506381,0.772997,5.00,0.0086,-0.1494,-0.1284,422.700331,70.999669,,,,0.000000
S2,QQQ,2026-05-01,2026-05-29,669.160000,738.310000,629.279032,624.279032,0.762694,5.00,0.0075,-0.1626,-0.1341,423.730625,69.969375,,,,0.000000
S2,QQQ,2026-06-01,2026-06-30,737.040000,736.400000,697.109964,692.109964,0.838702,5.00,0.0068,-0.1787,-0.1503,416.129825,77.570175,,,,0.000000
S2,QQQ,2026-07-01,2026-07-31,729.190000,687.990000,679.609587,674.609587,1.004258,5.00,0.0069,-0.1985,-0.1759,399.574154,94.125846,,,,0.000000
S2,QQQ,2026-08-03,2026-08-31,688.300000,716.760000,629.883957,624.883957,0.860585,5.00,0.0073,-0.1663,-0.1465,413.941473,79.758527,,,,0.000000
S2,QQQ,2026-09-01,2026-09-30,707.390000,739.770000,665.760716,660.760716,1.060492,5.00,0.0071,-0.2137,-0.1874,393.950781,99.749219,,,,0.000000
S2,IWM,2001-04-02,2001-04-30,44.775000,48.500000,41.674331,36.674331,0.308351,5.00,0.1117,-0.1720,-0.0052,469.164883,24.535117,,,,0.000000
S2,IWM,2001-05-01,2001-05-31,48.324995,49.550005,45.062164,40.062164,0.358696,5.00,0.1035,-0.1811,-0.0087,464.130432,29.569568,,,,0.000000
S2,IWM,2001-06-01,2001-06-29,49.875000,50.949995,47.025636,42.025636,0.195526,5.00,0.1003,-0.1443,-0.0012,480.447421,13.252579,,,,0.000000
S2,IWM,2001-07-02,2001-07-31,50.800005,48.115000,47.880308,42.880308,0.318213,5.00,0.0984,-0.1813,-0.0055,468.178667,25.521333,,,,0.000000
S2,IWM,2001-08-01,2001-08-31,48.525000,46.945000,44.766103,39.766103,0.263844,5.00,0.1030,-0.1432,-0.0050,473.615640,20.084360,,,,0.000000
S2,IWM,2001-09-04,2001-09-28,46.850000,40.100000,44.101571,39.101571,0.287099,5.00,0.1067,-0.1757,-0.0033,471.290131,-377.747195,,,,0.000000
S2,IWM,2001-10-01,2001-10-31,40.100000,42.550005,36.188349,31.188349,0.380365,5.00,0.1247,-0.1642,-0.0104,461.963485,31.736515,,,,0.000000
S2,IWM,2001-11-01,2001-11-30,42.670000,45.800005,39.199013,34.199013,0.303712,5.00,0.1172,-0.1568,-0.0053,469.628819,24.071181,,,,0.000000
S2,IWM,2001-12-03,2001-12-31,45.449995,48.175005,42.860613,37.860613,0.338047,5.00,0.1100,-0.1934,-0.0044,466.195335,27.504665,,,,0.000000
S2,IWM,2002-01-02,2002-01-31,48.550005,48.100000,44.919615,39.919615,0.253233,5.00,0.1030,-0.1400,-0.0039,474.676684,19.023316,,,,0.000000
S2,IWM,2002-02-01,2002-02-28,47.750000,46.600000,45.037570,40.037570,0.347374,5.00,0.1047,-0.1916,-0.0053,465.262554,28.437446,,,,0.000000
S2,IWM,2002-03-01,2002-03-28,46.824995,50.050005,43.676526,38.676526,0.242331,5.00,0.1068,-0.1478,-0.0025,475.766877,17.933123,,,,0.000000
S2,IWM,2002-04-01,2002-04-30,50.050005,50.650000,47.499662,42.499662,0.239134,5.00,0.0999,-0.1663,-0.0015,476.086647,17.613353,,,,0.000000
S2,IWM,2002-05-01,2002-05-31,50.750000,48.250000,47.664663,42.664663,0.265074,5.00,0.0985,-0.1579,-0.0033,473.492598,20.207402,,,,0.000000
S2,IWM,2002-06-03,2002-06-28,48.475000,45.324995,45.743570,40.743570,0.200763,5.00,0.1031,-0.1455,-0.0009,479.923670,-28.081193,,,,0.000000
S2,IWM,2002-07-01,2002-07-31,45.449995,39.275000,42.125027,37.125027,0.284789,5.00,0.1100,-0.1557,-0.0043,471.521060,-262.823711,,,,0.000000
S2,IWM,2002-08-01,2002-08-30,39.150000,39.025000,35.912604,30.912604,0.344966,5.00,0.1277,-0.1717,-0.0060,465.503387,28.196613,,,,0.000000
S2,IWM,2002-09-03,2002-09-30,38.324995,35.775000,36.252025,31.252025,0.396484,5.00,0.1305,-0.2272,-0.0041,460.351555,-14.354073,,,,0.000000
S2,IWM,2002-10-01,2002-10-31,36.250000,37.250000,32.368653,27.368653,0.267419,5.00,0.1379,-0.1347,-0.0039,473.258125,20.441875,,,,0.000000
S2,IWM,2002-11-01,2002-11-29,37.135000,40.405000,34.386522,29.386522,0.294666,5.00,0.1346,-0.1725,-0.0027,470.533428,23.166572,,,,0.000000
S2,IWM,2002-12-02,2002-12-31,41.250000,37.905000,37.868932,32.868932,0.133115,5.00,0.1212,-0.0999,-0.0004,486.688469,7.011531,,,,0.000000
S2,IWM,2003-01-02,2003-01-31,38.250000,37.120005,35.167003,30.167003,0.211526,5.00,0.1307,-0.1364,-0.0012,478.847351,14.852649,,,,0.000000
S2,IWM,2003-02-03,2003-02-28,37.199995,36.004995,34.289142,29.289142,0.258978,5.00,0.1344,-0.1561,-0.0020,474.102163,19.597837,,,,0.000000
S2,IWM,2003-03-03,2003-03-31,36.250000,36.000000,33.320045,28.320045,0.221156,5.00,0.1379,-0.1432,-0.0012,477.884361,15.815639,,,,0.000000
S2,IWM,2003-04-01,2003-04-30,36.350000,39.699995,33.848243,28.848243,0.153011,5.00,0.1376,-0.1294,-0.0002,484.698902,9.001098,,,,0.000000
S2,IWM,2003-05-01,2003-05-30,39.750000,44.015000,37.921136,32.921136,0.156701,5.00,0.1258,-0.1581,-0.0000,484.329949,9.370051,,,,0.000000
S2,IWM,2003-06-02,2003-06-30,44.375000,44.449995,42.029718,37.029718,0.132855,5.00,0.1127,-0.1261,-0.0001,486.714462,6.985538,,,,0.000000
S2,IWM,2003-07-01,2003-07-31,44.405000,47.339995,41.864047,36.864047,0.248889,5.00,0.1126,-0.1668,-0.0014,475.111104,18.588896,,,,0.000000
S2,IWM,2003-08-01,2003-08-29,47.375000,49.605005,44.602966,39.602966,0.249649,5.00,0.1055,-0.1600,-0.0019,475.035117,18.664883,,,,0.000000
S2,IWM,2003-09-02,2003-09-30,49.875000,48.525000,46.347674,41.347674,0.264071,5.00,0.1003,-0.1446,-0.0040,473.592894,20.107106,,,,0.000000
S2,IWM,2003-10-01,2003-10-31,48.685000,52.750000,44.503437,39.503437,0.351626,5.00,0.1027,-0.1534,-0.0102,464.837363,28.862637,,,,0.000000
S2,IWM,2003-11-03,2003-11-28,53.095000,54.725000,49.340784,44.340784,0.265668,5.00,0.0942,-0.1405,-0.0047,473.433235,20.266765,,,,0.000000
S2,IWM,2003-12-01,2003-12-31,54.935000,55.400000,50.498574,45.498574,0.356406,5.00,0.0910,-0.1514,-0.0121,464.359420,29.340580,,,,0.000000
S2,IWM,2004-01-02,2004-01-30,55.583505,57.800005,50.685895,45.685895,0.399725,5.00,0.0900,-0.1533,-0.0170,460.027464,33.672536,,,,0.000000
S2,IWM,2004-02-02,2004-02-27,57.920000,58.350000,54.045918,49.045918,0.324937,5.00,0.0863,-0.1550,-0.0084,467.506343,26.193657,,,,0.000000
S2,IWM,2004-03-01,2004-03-31,58.501000,58.800005,53.848400,48.848400,0.384191,5.00,0.0855,-0.1549,-0.0154,461.580916,32.119084,,,,0.000000
S2,IWM,2004-04-01,2004-04-30,58.790000,55.555000,54.528838,49.528838,0.387639,5.00,0.0850,-0.1628,-0.0143,461.236057,32.463943,,,,0.000000
S2,IWM,2004-05-03,2004-05-28,55.800005,56.750000,52.249891,47.249891,0.268213,5.00,0.0896,-0.1463,-0.0045,473.178727,20.521273,,,,0.000000
S2,IWM,2004-06-01,2004-06-30,56.500000,58.995005,53.059081,48.059081,0.378538,5.00,0.0885,-0.1787,-0.0103,462.146167,31.553833,,,,0.000000
S2,IWM,2004-07-01,2004-07-30,58.910005,55.000000,55.098636,50.098636,0.368908,5.00,0.0849,-0.1684,-0.0115,463.109190,20.727168,,,,0.000000
S2,IWM,2004-08-02,2004-08-31,54.600000,54.705000,50.961466,45.961466,0.434815,5.00,0.0916,-0.1866,-0.0153,456.518509,37.181491,,,,0.000000
S2,IWM,2004-09-01,2004-09-30,54.545000,56.925005,51.218955,46.218955,0.348928,5.00,0.0917,-0.1749,-0.0081,465.107192,28.592808,,,,0.000000
S2,IWM,2004-10-01,2004-10-29,57.285005,58.095000,53.442188,48.442188,0.271150,5.00,0.0873,-0.1425,-0.0056,472.885006,20.814994,,,,0.000000
S2,IWM,2004-11-01,2004-11-30,58.269995,63.440000,54.428176,49.428176,0.313379,5.00,0.0858,-0.1548,-0.0081,468.662091,25.037909,,,,0.000000
S2,IWM,2004-12-01,2004-12-31,63.405000,64.750000,60.518070,55.518070,0.277965,5.00,0.0789,-0.1714,-0.0039,472.203452,21.496548,,,,0.000000
S2,IWM,2005-01-03,2005-01-31,65.095000,62.120005,62.095101,57.095101,0.197817,5.00,0.0768,-0.1412,-0.0016,480.218295,13.481705,,,,0.000000
S2,IWM,2005-02-01,2005-02-28,62.125000,63.140000,59.009196,54.009196,0.288923,5.00,0.0805,-0.1675,-0.0050,471.107673,22.592327,,,,0.000000
S2,IWM,2005-03-01,2005-03-31,63.330000,61.074995,59.917210,54.917210,0.273340,5.00,0.0790,-0.1564,-0.0053,472.665981,21.034019,,,,0.000000
S2,IWM,2005-04-01,2005-04-29,61.365000,57.620005,58.029470,53.029470,0.243749,5.00,0.0815,-0.1488,-0.0037,475.625137,-22.871656,,,,0.000000
S2,IWM,2005-05-02,2005-05-31,57.780000,61.345000,54.689163,49.689163,0.252856,5.00,0.0865,-0.1577,-0.0034,474.714369,18.985631,,,,0.000000
S2,IWM,2005-06-01,2005-06-30,61.339995,63.700000,58.709113,53.709113,0.250266,5.00,0.0815,-0.1724,-0.0024,474.973383,18.726617,,,,0.000000
S2,IWM,2005-07-01,2005-07-29,63.700000,67.890000,60.762835,55.762835,0.277063,5.00,0.0785,-0.1715,-0.0043,472.293736,21.406264,,,,0.000000
S2,IWM,2005-08-01,2005-08-31,67.940000,66.530000,64.737123,59.737123,0.290025,5.00,0.0736,-0.1696,-0.0061,470.997456,22.702544,,,,0.000000
S2,IWM,2005-09-01,2005-09-30,66.420000,66.390000,62.587089,57.587089,0.380904,5.00,0.0753,-0.1767,-0.0146,461.909557,31.790443,,,,0.000000
S2,IWM,2005-10-03,2005-10-31,66.490010,63.780000,62.775316,57.775316,0.321857,5.00,0.0752,-0.1644,-0.0096,467.814303,25.885697,,,,0.000000
S2,IWM,2005-11-01,2005-11-30,64.050000,67.450000,60.115107,55.115107,0.305070,5.00,0.0781,-0.1555,-0.0092,469.492974,24.207026,,,,0.000000
S2,IWM,2005-12-01,2005-12-30,67.789990,66.720000,64.555425,59.555425,0.227737,5.00,0.0738,-0.1503,-0.0034,477.226291,16.473709,,,,0.000000
S2,IWM,2006-01-03,2006-01-31,67.210010,72.350010,63.757890,58.757890,0.214069,5.00,0.0744,-0.1398,-0.0033,478.593138,15.106862,,,,0.000000
S2,IWM,2006-02-01,2006-02-28,72.590000,72.580000,69.155438,64.155438,0.268416,5.00,0.0689,-0.1595,-0.0062,473.158352,20.541648,,,,0.000000
S2,IWM,2006-03-01,2006-03-31,72.770000,75.970000,69.675846,64.675846,0.252972,5.00,0.0687,-0.1657,-0.0047,474.702832,18.997168,,,,0.000000
S2,IWM,2006-04-03,2006-04-28,76.120000,76.200000,73.093316,68.093316,0.252828,5.00,0.0657,-0.1665,-0.0044,474.717238,18.982762,,,,0.000000
S2,IWM,2006-05-01,2006-05-31,76.289990,71.870000,72.439386,67.439386,0.340044,5.00,0.0655,-0.1717,-0.0133,465.995558,-29.234120,,,,0.000000
S2,IWM,2006-06-01,2006-06-30,71.880000,71.730000,67.267751,62.267751,0.415762,5.00,0.0696,-0.1723,-0.0226,458.423848,35.276152,,,,0.000000
S2,IWM,2006-07-03,2006-07-31,72.000000,69.679990,66.930545,61.930545,0.395235,5.00,0.0694,-0.1600,-0.0221,460.476514,33.223486,,,,0.000000
S2,IWM,2006-08-01,2006-08-31,69.170000,71.770000,65.281775,60.281775,0.482471,5.00,0.0723,-0.2015,-0.0263,451.752860,41.947140,,,,0.000000
S2,IWM,2006-09-01,2006-09-29,72.080000,72.000000,67.715980,62.715980,0.333575,5.00,0.0694,-0.1580,-0.0141,466.642491,27.057509,,,,0.000000
S2,IWM,2006-10-02,2006-10-31,71.970000,76.230000,67.892188,62.892188,0.384994,5.00,0.0695,-0.1762,-0.0176,461.500617,32.199383,,,,0.000000
S2,IWM,2006-11-01,2006-11-30,76.450000,78.070010,72.260834,67.260834,0.338935,5.00,0.0654,-0.1644,-0.0146,466.106476,27.593524,,,,0.000000
S2,IWM,2006-12-01,2006-12-29,78.149990,78.030000,73.401503,68.401503,0.408449,5.00,0.0640,-0.1700,-0.0233,459.155073,34.544927,,,,0.000000
S2,IWM,2007-01-03,2007-01-31,78.679990,79.350010,73.908469,68.908469,0.294788,5.00,0.0635,-0.1422,-0.0127,470.521223,23.178777,,,,0.000000
S2,IWM,2007-02-01,2007-02-28,79.670000,78.830000,75.604646,70.604646,0.305868,5.00,0.0628,-0.1585,-0.0115,469.413224,24.286776,,,,0.000000
S2,IWM,2007-03-01,2007-03-30,77.470000,79.509990,75.491664,70.491664,0.585168,5.00,0.0645,-0.2894,-0.0249,441.483231,52.216769,,,,0.000000
S2,IWM,2007-04-02,2007-04-30,79.610000,80.740010,75.962020,70.962020,0.320941,5.00,0.0628,-0.1723,-0.0113,467.905919,25.794081,,,,0.000000
S2,IWM,2007-05-01,2007-05-31,80.990010,84.200000,77.343774,72.343774,0.288522,5.00,0.0617,-0.1644,-0.0092,471.147789,22.552211,,,,0.000000
S2,IWM,2007-06-01,2007-06-29,84.539990,82.960010,80.138453,75.138453,0.327132,5.00,0.0591,-0.1583,-0.0148,467.286824,26.413176,,,,0.000000
S2,IWM,2007-07-02,2007-07-31,83.380000,77.100010,77.801478,72.801478,0.396338,5.00,0.0600,-0.1554,-0.0255,460.366175,-36.813000,,,,0.000000
S2,IWM,2007-08-01,2007-08-31,76.870000,78.740010,71.737364,66.737364,0.497508,5.00,0.0650,-0.1819,-0.0347,450.249226,43.450774,,,,0.000000
S2,IWM,2007-09-04,2007-09-28,78.679990,80.060000,72.889792,67.889792,0.497626,5.00,0.0635,-0.1698,-0.0356,450.237423,43.462577,,,,0.000000
S2,IWM,2007-10-01,2007-10-31,80.130000,82.320010,75.159423,70.159423,0.421132,5.00,0.0624,-0.1676,-0.0248,457.886760,35.813240,,,,0.000000
S2,IWM,2007-11-01,2007-11-30,81.370000,76.580000,76.861607,71.861607,0.603578,5.00,0.0614,-0.2123,-0.0449,439.642165,25.897175,,,,0.000000
S2,IWM,2007-12-03,2007-12-31,76.550000,75.920000,69.979505,64.979505,0.538551,5.00,0.0653,-0.1669,-0.0423,446.144923,47.555077,,,,0.000000
S2,IWM,2008-01-02,2008-01-31,76.149990,70.940000,71.232630,66.232630,0.384544,5.00,0.0657,-0.1584,-0.0200,461.545625,2.891348,,,,0.000000
S2,IWM,2008-02-01,2008-02-29,71.330000,68.860000,64.765062,59.765062,0.466874,5.00,0.0701,-0.1509,-0.0321,453.312555,40.387445,,,,0.000000
S2,IWM,2008-03-03,2008-03-31,68.390000,68.289990,63.760168,58.760168,0.512542,5.00,0.0731,-0.1862,-0.0299,448.745842,44.954158,,,,0.000000
S2,IWM,2008-04-01,2008-04-30,69.460010,71.399990,62.428890,57.428890,0.360685,5.00,0.0720,-0.1228,-0.0211,463.931492,29.768508,,,,0.000000
S2,IWM,2008-05-01,2008-05-30,71.460010,74.670000,66.684855,61.684855,0.404378,5.00,0.0700,-0.1607,-0.0193,459.562243,34.137757,,,,0.000000
S2,IWM,2008-06-02,2008-06-30,74.570010,69.050000,70.022588,65.022588,0.422111,5.00,0.0671,-0.1700,-0.0208,457.788926,-61.347733,,,,0.000000
S2,IWM,2008-07-01,2008-07-31,68.240010,71.320010,64.546528,59.546528,0.529799,5.00,0.0733,-0.2088,-0.0266,447.020138,46.679862,,,,0.000000
S2,IWM,2008-08-01,2008-08-29,71.440000,73.870000,65.766942,60.766942,0.456477,5.00,0.0700,-0.1589,-0.0279,454.352262,39.347738,,,,0.000000
S2,IWM,2008-09-02,2008-09-30,75.009990,68.000000,69.174112,64.174112,0.273693,5.00,0.0667,-0.1159,-0.0116,472.630695,-96.341932,,,,0.000000
S2,IWM,2008-10-01,2008-10-31,67.190000,53.750000,61.148497,56.148497,0.658373,5.00,0.0744,-0.1886,-0.0514,434.162739,-440.462739,,,,0.000000
S2,IWM,2008-11-03,2008-11-28,53.480000,47.340000,46.074311,41.074311,0.671976,5.00,0.0935,-0.1679,-0.0507,432.802407,60.897593,,,,0.000000
S2,IWM,2008-12-01,2008-12-31,46.120000,49.240010,39.970504,34.970504,0.800304,5.00,0.1084,-0.1963,-0.0587,419.969617,73.730383,,,,0.000000
S2,IWM,2009-01-02,2009-01-30,49.740010,44.480000,43.663950,38.663950,0.438647,5.00,0.1005,-0.1418,-0.0220,456.135308,37.564692,,,,0.000000
S2,IWM,2009-02-02,2009-02-27,43.660000,39.149990,39.151702,34.151702,0.616468,5.00,0.1145,-0.1952,-0.0322,438.353202,55.175631,,,,0.000000
S2,IWM,2009-03-02,2009-03-31,38.259990,42.050000,33.660595,28.660595,0.658844,5.00,0.1307,-0.1964,-0.0342,434.115607,59.584393,,,,0.000000
S2,IWM,2009-04-01,2009-04-30,41.340000,48.520000,36.911558,31.911558,0.591167,5.00,0.1209,-0.1913,-0.0285,440.883251,52.816749,,,,0.000000
S2,IWM,2009-05-01,2009-05-29,48.649990,50.170000,42.824027,37.824027,0.496473,5.00,0.1028,-0.1554,-0.0265,450.352722,43.347278,,,,0.000000
S2,IWM,2009-06-01,2009-06-30,51.360000,51.080000,44.940648,39.940648,0.330908,5.00,0.0974,-0.1166,-0.0141,466.909157,26.790843,,,,0.000000
S2,IWM,2009-07-01,2009-07-31,51.350010,55.570010,46.255901,41.255901,0.401321,5.00,0.0974,-0.1485,-0.0167,459.867911,33.832089,,,,0.000000
S2,IWM,2009-08-03,2009-08-31,56.240010,57.200000,50.969093,45.969093,0.326371,5.00,0.0889,-0.1305,-0.0120,467.362921,26.337079,,,,0.000000
S2,IWM,2009-09-01,2009-09-30,56.860000,60.240010,52.454448,47.454448,0.473773,5.00,0.0879,-0.1767,-0.0215,452.622652,41.077348,,,,0.000000
S2,IWM,2009-10-01,2009-10-30,60.130000,56.330000,54.983832,49.983832,0.473679,5.00,0.0832,-0.1649,-0.0249,452.632110,41.067890,,,,0.000000
S2,IWM,2009-11-02,2009-11-30,56.630000,58.090000,51.535040,46.535040,0.387328,5.00,0.0883,-0.1468,-0.0163,461.267168,32.432832,,,,0.000000
S2,IWM,2009-12-01,2009-12-31,58.640000,62.440000,53.849456,48.849456,0.307063,5.00,0.0853,-0.1329,-0.0097,469.293661,24.406339,,,,0.000000
S2,IWM,2010-01-04,2010-01-29,63.289990,60.110000,58.105576,53.105576,0.276606,5.00,0.0790,-0.1204,-0.0089,472.339420,21.360580,,,,0.000000
S2,IWM,2010-02-01,2010-02-26,60.390000,62.800000,55.360541,50.360541,0.382002,5.00,0.0828,-0.1474,-0.0161,461.799844,31.900156,,,,0.000000
S2,IWM,2010-03-01,2010-03-31,63.259990,67.802510,58.292079,53.292079,0.337055,5.00,0.0790,-0.1386,-0.0127,466.294516,27.405484,,,,0.000000
S2,IWM,2010-04-01,2010-04-30,68.330000,71.649990,63.874310,58.874310,0.277168,5.00,0.0732,-0.1319,-0.0075,472.283200,21.416800,,,,0.000000
S2,IWM,2010-05-03,2010-05-28,72.100010,66.250000,66.715081,61.715081,0.365033,5.00,0.0693,-0.1408,-0.0170,463.496665,-16.304776,,,,0.000000
S2,IWM,2010-06-01,2010-06-30,65.600010,61.115010,58.535134,53.535134,0.682712,5.00,0.0762,-0.1789,-0.0562,431.728790,61.971210,,,,0.000000
S2,IWM,2010-07-01,2010-07-30,61.200000,65.020000,55.206407,50.206407,0.492816,5.00,0.0817,-0.1571,-0.0298,450.718408,42.981592,,,,0.000000
S2,IWM,2010-08-02,2010-08-31,66.170000,60.179990,59.725353,54.725353,0.319842,5.00,0.0756,-0.1172,-0.0152,468.015766,25.684234,,,,0.000000
S2,IWM,2010-09-01,2010-09-30,61.230000,67.500000,54.272182,49.272182,0.383231,5.00,0.0817,-0.1250,-0.0213,461.676900,32.023100,,,,0.000000
S2,IWM,2010-10-01,2010-10-29,68.140000,70.300000,61.697217,56.697217,0.410010,5.00,0.0734,-0.1373,-0.0238,458.998962,34.701038,,,,0.000000
S2,IWM,2010-11-01,2010-11-30,70.660000,72.750000,64.657501,59.657501,0.428483,5.00,0.0708,-0.1466,-0.0248,457.151651,36.548349,,,,0.000000
S2,IWM,2010-12-01,2010-12-31,74.120000,78.240010,67.231853,62.231853,0.307821,5.00,0.0675,-0.1116,-0.0158,469.217921,24.482079,,,,0.000000
S2,IWM,2011-01-03,2011-01-31,78.940000,77.950000,73.436969,68.436969,0.321027,5.00,0.0633,-0.1297,-0.0141,467.897257,25.802743,,,,0.000000
S2,IWM,2011-02-01,2011-02-28,78.580000,82.268010,73.124011,68.124011,0.331094,5.00,0.0636,-0.1327,-0.0148,466.890564,26.809436,,,,0.000000
S2,IWM,2011-03-01,2011-03-31,82.580000,84.170000,74.900318,69.900318,0.526794,5.00,0.0605,-0.1511,-0.0421,447.320600,46.379400,,,,0.000000
S2,IWM,2011-04-01,2011-04-29,84.770000,86.390000,78.130732,73.130732,0.414592,5.00,0.0590,-0.1391,-0.0267,458.540781,35.159219,,,,0.000000
S2,IWM,2011-05-02,2011-05-31,86.780000,84.840000,81.509725,76.509725,0.359474,5.00,0.0576,-0.1427,-0.0171,464.052605,29.647395,,,,0.000000
S2,IWM,2011-06-01,2011-06-30,84.710010,82.800000,79.392515,74.392515,0.467019,5.00,0.0590,-0.1656,-0.0279,453.298147,40.401853,,,,0.000000
S2,IWM,2011-07-01,2011-07-29,82.880000,79.740010,76.321624,71.321624,0.502988,5.00,0.0603,-0.1573,-0.0362,449.701200,43.998800,,,,0.000000
S2,IWM,2011-08-01,2011-08-31,80.690000,72.649990,73.759591,68.759591,0.376280,5.00,0.0620,-0.1275,-0.0230,462.371982,-79.632079,,,,0.000000
S2,IWM,2011-09-01,2011-09-30,72.700000,64.300000,64.316710,59.316710,0.620624,5.00,0.0688,-0.1587,-0.0530,437.937645,54.091330,,,,0.000000
S2,IWM,2011-10-03,2011-10-31,63.810000,74.009990,56.652500,51.652500,0.663925,5.00,0.0784,-0.1740,-0.0533,433.607545,60.092455,,,,0.000000
S2,IWM,2011-11-01,2011-11-30,71.179990,73.730000,66.340043,61.340043,0.976172,5.00,0.0702,-0.2544,-0.0916,402.382835,91.317165,,,,0.000000
S2,IWM,2011-12-01,2011-12-30,73.470000,73.750000,64.888621,59.888621,0.676230,5.00,0.0681,-0.1663,-0.0606,432.376987,61.323013,,,,0.000000
S2,IWM,2012-01-03,2012-01-31,75.679990,79.020000,67.734047,62.734047,0.292027,5.00,0.0661,-0.0998,-0.0163,470.797345,22.902655,,,,0.000000
S2,IWM,2012-02-01,2012-02-29,79.759990,81.050000,73.893460,68.893460,0.339607,5.00,0.0627,-0.1298,-0.0166,466.039252,27.660748,,,,0.000000
S2,IWM,2012-03-01,2012-03-30,81.380000,82.810000,75.682181,70.682181,0.404267,5.00,0.0614,-0.1468,-0.0225,459.573316,34.126684,,,,0.000000
S2,IWM,2012-04-02,2012-04-30,82.539990,81.470000,77.423478,72.423478,0.484307,5.00,0.0606,-0.1718,-0.0288,451.569289,42.130711,,,,0.000000
S2,IWM,2012-05-01,2012-05-31,81.560000,76.110000,75.909201,70.909201,0.447244,5.00,0.0613,-0.1566,-0.0268,455.275566,38.424434,,,,0.000000
S2,IWM,2012-06-01,2012-06-29,74.399990,79.560000,70.277030,65.277030,0.744645,5.00,0.0672,-0.2350,-0.0544,425.535508,68.164492,,,,0.000000
S2,IWM,2012-07-02,2012-07-31,79.920000,78.350010,74.210911,69.210911,0.400233,5.00,0.0626,-0.1456,-0.0220,459.976722,33.723278,,,,0.000000
S2,IWM,2012-08-01,2012-08-31,78.910000,81.120000,73.755682,68.755682,0.321472,5.00,0.0634,-0.1343,-0.0131,467.852790,25.847210,,,,0.000000
S2,IWM,2012-09-04,2012-09-28,81.179990,83.440000,76.997226,71.997226,0.349726,5.00,0.0616,-0.1570,-0.0122,465.027444,28.672556,,,,0.000000
S2,IWM,2012-10-01,2012-10-31,83.960010,81.630000,79.140386,74.140386,0.301275,5.00,0.0596,-0.1343,-0.0108,469.872517,23.827483,,,,0.000000
S2,IWM,2012-11-01,2012-11-30,81.820010,82.080000,76.880912,71.880912,0.378471,5.00,0.0611,-0.1514,-0.0174,462.152869,31.547131,,,,0.000000
S2,IWM,2012-12-03,2012-12-31,82.710010,84.317790,78.197148,73.197148,0.255033,5.00,0.0605,-0.1260,-0.0068,474.496739,19.203261,,,,0.000000
S2,IWM,2013-01-02,2013-01-31,86.340000,89.580000,79.517353,74.517353,0.192129,5.00,0.0579,-0.0833,-0.0071,480.787106,12.912894,,,,0.000000
S2,IWM,2013-02-01,2013-02-28,89.960010,90.480000,86.043371,81.043371,0.255561,5.00,0.0556,-0.1367,-0.0055,474.443913,19.256087,,,,0.000000
S2,IWM,2013-03-01,2013-03-28,89.880000,94.429990,85.426461,80.426461,0.510087,5.00,0.0556,-0.1890,-0.0292,448.991322,44.708678,,,,0.000000
S2,IWM,2013-04-01,2013-04-30,94.270000,94.100010,90.379786,85.379786,0.372830,5.00,0.0530,-0.1696,-0.0134,462.716951,30.983049,,,,0.000000
S2,IWM,2013-05-01,2013-05-31,93.810000,97.800000,89.507537,84.507537,0.431038,5.00,0.0533,-0.1752,-0.0204,456.896179,36.803821,,,,0.000000
S2,IWM,2013-06-03,2013-06-28,98.140000,97.000000,92.637053,87.637053,0.380245,5.00,0.0509,-0.1456,-0.0205,461.975452,31.724548,,,,0.000000
S2,IWM,2013-07-01,2013-07-31,97.649990,103.655000,90.763607,85.763607,0.412620,5.00,0.0512,-0.1378,-0.0282,458.738003,34.961997,,,,0.000000
S2,IWM,2013-08-01,2013-08-30,104.679990,100.380000,99.396815,94.396815,0.234564,5.00,0.0478,-0.1108,-0.0078,476.543558,17.156442,,,,0.000000
S2,IWM,2013-09-03,2013-09-30,101.860000,106.610000,95.037567,90.037567,0.268990,5.00,0.0491,-0.1052,-0.0137,473.100968,20.599032,,,,0.000000
S2,IWM,2013-10-01,2013-10-31,106.560000,109.190000,101.114018,96.114018,0.448262,5.00,0.0469,-0.1622,-0.0279,455.173784,38.526216,,,,0.000000
S2,IWM,2013-11-01,2013-11-29,109.410000,113.510000,104.213609,99.213609,0.379194,5.00,0.0457,-0.1502,-0.0198,462.080624,31.619376,,,,0.000000
S2,IWM,2013-12-02,2013-12-31,113.700000,115.360000,108.545983,103.545983,0.381267,5.00,0.0440,-0.1516,-0.0201,461.873259,31.826741,,,,0.000000
S2,IWM,2014-01-02,2014-01-31,115.090000,112.160000,110.204939,105.204939,0.456324,5.00,0.0434,-0.1727,-0.0269,454.367581,39.332419,,,,0.000000
S2,IWM,2014-02-03,2014-02-28,111.870000,117.520000,106.233682,101.233682,0.502505,5.00,0.0447,-0.1716,-0.0355,449.749523,43.950477,,,,0.000000
S2,IWM,2014-03-03,2014-03-31,116.520000,116.340000,112.003978,107.003978,0.587358,5.00,0.0429,-0.2057,-0.0408,441.264238,52.435762,,,,0.000000
S2,IWM,2014-04-01,2014-04-30,116.630000,111.980000,110.121410,105.121410,0.443139,5.00,0.0429,-0.1498,-0.0319,455.686106,38.013894,,,,0.000000
S2,IWM,2014-05-01,2014-05-30,111.750000,112.860000,105.922919,100.922919,0.501155,5.00,0.0447,-0.1689,-0.0361,449.884512,43.815488,,,,0.000000
S2,IWM,2014-06-02,2014-06-30,113.070000,118.810000,107.274422,102.274422,0.417661,5.00,0.0442,-0.1516,-0.0262,458.233868,35.466132,,,,0.000000
S2,IWM,2014-07-01,2014-07-31,119.260000,111.189900,112.389537,107.389537,0.434725,5.00,0.0419,-0.1446,-0.0321,456.527536,-82.791205,,,,0.000000
S2,IWM,2014-08-01,2014-08-29,111.160000,116.560000,104.073107,99.073107,0.528752,5.00,0.0450,-0.1610,-0.0441,447.124795,46.575205,,,,0.000000
S2,IWM,2014-09-02,2014-09-30,116.980000,109.350000,111.119243,106.119243,0.381795,5.00,0.0427,-0.1430,-0.0227,461.820495,-145.044822,,,,0.000000
S2,IWM,2014-10-01,2014-10-31,109.290000,116.560000,102.863404,97.863404,0.502549,5.00,0.0457,-0.1621,-0.0384,449.745128,43.954872,,,,0.000000
S2,IWM,2014-11-03,2014-11-28,116.750000,116.690000,111.197260,106.197260,0.405385,5.00,0.0428,-0.1520,-0.0241,459.461535,34.238465,,,,0.000000
S2,IWM,2014-12-01,2014-12-31,116.320000,119.620000,111.338542,106.338542,0.481342,5.00,0.0430,-0.1765,-0.0302,451.865794,41.834206,,,,0.000000
S2,IWM,2015-01-02,2015-01-30,120.070000,115.700000,113.718498,108.718498,0.405013,5.00,0.0416,-0.1432,-0.0270,459.498654,34.201346,,,,0.000000
S2,IWM,2015-02-02,2015-02-27,116.120000,122.580000,109.557907,104.557907,0.423845,5.00,0.0431,-0.1450,-0.0297,457.615518,36.084482,,,,0.000000
S2,IWM,2015-03-02,2015-03-31,122.550000,124.370000,117.117339,112.117339,0.438420,5.00,0.0408,-0.1614,-0.0276,456.157996,37.542004,,,,0.000000
S2,IWM,2015-04-01,2015-04-30,124.230000,121.180000,118.414725,113.414725,0.479572,5.00,0.0402,-0.1656,-0.0341,452.042812,41.657188,,,,0.000000
S2,IWM,2015-05-01,2015-05-29,121.520000,123.890000,116.314977,111.314977,0.353100,5.00,0.0411,-0.1444,-0.0177,464.690000,29.010000,,,,0.000000
S2,IWM,2015-06-01,2015-06-30,124.690000,124.860000,118.510931,113.510931,0.332146,5.00,0.0401,-0.1282,-0.0188,466.785379,26.914621,,,,0.000000
S2,IWM,2015-07-01,2015-07-31,125.770000,122.960000,119.189233,114.189233,0.338462,5.00,0.0398,-0.1259,-0.0206,466.153802,27.546198,,,,0.000000
S2,IWM,2015-08-03,2015-08-31,123.030000,115.200000,118.078197,113.078197,0.389568,5.00,0.0406,-0.1570,-0.0204,461.043218,-255.162908,,,,0.000000
S2,IWM,2015-09-01,2015-09-30,113.110000,109.200000,106.605390,101.605390,0.833927,5.00,0.0442,-0.2210,-0.0870,416.607284,77.092716,,,,0.000000
S2,IWM,2015-10-01,2015-10-30,109.370000,115.340000,103.015181,98.015181,0.458393,5.00,0.0457,-0.1538,-0.0327,454.160710,39.539290,,,,0.000000
S2,IWM,2015-11-02,2015-11-30,115.450000,119.100000,110.806496,105.806496,0.362485,5.00,0.0433,-0.1547,-0.0163,463.751536,29.948464,,,,0.000000
S2,IWM,2015-12-01,2015-12-31,119.610000,112.620000,113.192383,108.192383,0.399445,5.00,0.0418,-0.1416,-0.0268,460.055480,-23.593747,,,,0.000000
S2,IWM,2016-01-04,2016-01-29,110.610000,102.960000,106.931706,101.931706,0.776071,5.00,0.0452,-0.2557,-0.0608,422.392944,-325.863533,,,,0.000000
S2,IWM,2016-02-01,2016-02-29,102.140000,102.730000,96.272544,91.272544,0.616113,5.00,0.0490,-0.1902,-0.0509,438.388683,55.311317,,,,0.000000
S2,IWM,2016-03-01,2016-03-31,103.620000,110.630000,96.394798,91.394798,0.391092,5.00,0.0483,-0.1314,-0.0274,460.890777,32.809223,,,,0.000000
S2,IWM,2016-04-01,2016-04-29,109.610000,112.480000,105.129007,100.129007,0.593150,5.00,0.0456,-0.2075,-0.0413,440.685040,53.014960,,,,0.000000
S2,IWM,2016-05-02,2016-05-31,112.830000,115.000000,106.794367,101.794367,0.407687,5.00,0.0443,-0.1472,-0.0262,459.231347,34.468653,,,,0.000000
S2,IWM,2016-06-01,2016-06-30,114.610000,114.980000,107.894377,102.894377,0.570455,5.00,0.0436,-0.1736,-0.0492,442.954480,50.745520,,,,0.000000
S2,IWM,2016-07-01,2016-07-29,115.050000,121.070000,105.425113,100.425113,0.616246,5.00,0.0435,-0.1589,-0.0631,438.375379,55.324621,,,,0.000000
S2,IWM,2016-08-01,2016-08-31,121.200000,123.230000,115.252743,110.252743,0.439863,5.00,0.0413,-0.1561,-0.0301,456.013702,37.686298,,,,0.000000
S2,IWM,2016-09-01,2016-09-30,123.340000,124.210000,117.125333,112.125333,0.457434,5.00,0.0405,-0.1571,-0.0334,454.256564,39.443436,,,,0.000000
S2,IWM,2016-10-03,2016-10-31,123.830000,118.500000,118.059643,113.059643,0.522401,5.00,0.0404,-0.1756,-0.0397,447.759948,45.940052,,,,0.000000
S2,IWM,2016-11-01,2016-11-30,118.660000,131.610000,112.093410,107.093410,0.468860,5.00,0.0421,-0.1553,-0.0357,453.114040,40.585960,,,,0.000000
S2,IWM,2016-12-01,2016-12-30,132.250000,134.850000,124.994091,119.994091,0.422164,5.00,0.0378,-0.1406,-0.0331,457.783632,35.916368,,,,0.000000
S2,IWM,2017-01-03,2017-01-31,136.490000,135.230000,127.376450,122.376450,0.370903,5.00,0.0366,-0.1169,-0.0312,462.909748,30.790252,,,,0.000000
S2,IWM,2017-02-01,2017-02-28,136.220000,137.840000,128.480544,123.480544,0.392126,5.00,0.0367,-0.1304,-0.0308,460.787418,32.912582,,,,0.000000
S2,IWM,2017-03-01,2017-03-31,139.650000,137.480000,129.574421,124.574421,0.394856,5.00,0.0358,-0.1171,-0.0361,460.514361,33.185639,,,,0.000000
S2,IWM,2017-04-03,2017-04-28,137.970000,139.060000,129.928966,124.928966,0.482369,5.00,0.0362,-0.1479,-0.0437,451.763052,41.936948,,,,0.000000
S2,IWM,2017-05-01,2017-05-31,139.640000,136.320000,131.658512,126.658512,0.466586,5.00,0.0358,-0.1457,-0.0418,453.341380,40.358620,,,,0.000000
S2,IWM,2017-06-01,2017-06-30,136.720000,140.920000,130.056676,125.056676,0.430900,5.00,0.0366,-0.1494,-0.0333,456.909966,36.790034,,,,0.000000
S2,IWM,2017-07-03,2017-07-31,141.340000,141.510000,133.922818,128.922818,0.464419,5.00,0.0354,-0.1502,-0.0402,453.558105,40.141895,,,,0.000000
S2,IWM,2017-08-01,2017-08-31,142.170000,139.730000,135.499945,130.499945,0.388304,5.00,0.0352,-0.1410,-0.0287,461.169575,32.530425,,,,0.000000
S2,IWM,2017-09-01,2017-09-29,139.980000,148.180000,133.519058,128.519058,0.445045,5.00,0.0357,-0.1550,-0.0347,455.495472,38.204528,,,,0.000000
S2,IWM,2017-10-02,2017-10-31,148.310000,149.260000,142.221763,137.221763,0.444929,5.00,0.0337,-0.1598,-0.0339,455.507093,38.192907,,,,0.000000
S2,IWM,2017-11-01,2017-11-30,150.500000,153.650000,142.769433,137.769433,0.354157,5.00,0.0332,-0.1245,-0.0276,464.584306,29.115694,,,,0.000000
S2,IWM,2017-12-01,2017-12-29,153.670000,152.460000,146.941471,141.941471,0.494149,5.00,0.0325,-0.1643,-0.0433,450.585088,43.114912,,,,0.000000
S2,IWM,2018-01-02,2018-01-31,153.200000,156.360000,145.146362,140.146362,0.444871,5.00,0.0326,-0.1429,-0.0406,455.512859,38.187141,,,,0.000000
S2,IWM,2018-02-01,2018-02-28,155.730000,150.350000,148.888621,143.888621,0.602134,5.00,0.0321,-0.1852,-0.0597,439.786568,53.913432,,,,0.000000
S2,IWM,2018-03-01,2018-03-29,150.050000,151.830000,144.115435,139.115435,0.515063,5.00,0.0333,-0.1783,-0.0437,448.493733,45.206267,,,,0.000000
S2,IWM,2018-04-02,2018-04-30,151.520000,153.320000,144.229671,139.229671,0.571456,5.00,0.0330,-0.1757,-0.0572,442.854426,50.845574,,,,0.000000
S2,IWM,2018-05-01,2018-05-31,153.010000,162.770000,146.605905,141.605905,0.537608,5.00,0.0327,-0.1786,-0.0496,446.239206,47.460794,,,,0.000000
S2,IWM,2018-06-01,2018-06-29,163.830000,163.770000,157.329483,152.329483,0.314963,5.00,0.0305,-0.1286,-0.0216,468.503713,25.196287,,,,0.000000
S2,IWM,2018-07-02,2018-07-31,162.760000,165.870000,157.093154,152.093154,0.626675,5.00,0.0307,-0.2060,-0.0607,437.332493,56.367507,,,,0.000000
S2,IWM,2018-08-01,2018-08-31,165.700000,173.020000,159.938520,154.938520,0.484695,5.00,0.0302,-0.1772,-0.0410,451.530455,42.169545,,,,0.000000
S2,IWM,2018-09-04,2018-09-28,172.790000,168.550000,166.013624,161.013624,0.535314,5.00,0.0289,-0.1756,-0.0517,446.468601,47.231399,,,,0.000000
S2,IWM,2018-10-01,2018-10-31,169.290000,150.030000,161.203145,156.203145,0.448072,5.00,0.0295,-0.1473,-0.0439,455.192836,-461.492836,,,,0.000000
S2,IWM,2018-11-01,2018-11-30,150.890000,152.620000,139.511962,134.511962,0.563509,5.00,0.0331,-0.1482,-0.0653,443.649079,50.050921,,,,0.000000
S2,IWM,2018-12-03,2018-12-31,154.390000,133.900000,144.266917,139.266917,0.405656,5.00,0.0324,-0.1240,-0.0409,459.434435,-465.734435,,,,0.000000
S2,IWM,2019-01-02,2019-01-31,132.170000,149.060000,122.842541,117.842541,0.821751,5.00,0.0378,-0.2022,-0.1001,417.824915,75.875085,,,,0.000000
S2,IWM,2019-02-01,2019-02-28,149.350000,156.780000,141.468785,136.468785,0.508135,5.00,0.0335,-0.1592,-0.0504,449.186461,44.513539,,,,0.000000
S2,IWM,2019-03-01,2019-03-29,157.950000,153.090000,150.487473,145.487473,0.356710,5.00,0.0317,-0.1312,-0.0295,464.329009,29.370991,,,,0.000000
S2,IWM,2019-04-01,2019-04-30,154.290000,158.290000,145.743818,140.743818,0.408261,5.00,0.0324,-0.1344,-0.0386,459.173890,34.526110,,,,0.000000
S2,IWM,2019-05-01,2019-05-31,158.670000,145.860000,149.923008,144.923008,0.528216,5.00,0.0315,-0.1583,-0.0567,447.178425,-359.779211,,,,0.000000
S2,IWM,2019-06-03,2019-06-28,146.130000,155.500000,136.735768,131.735768,0.568568,5.00,0.0342,-0.1592,-0.0620,443.143184,50.556816,,,,0.000000
S2,IWM,2019-07-01,2019-07-31,157.540000,156.560000,146.716063,141.716063,0.402364,5.00,0.0317,-0.1199,-0.0415,459.763589,33.936411,,,,0.000000
S2,IWM,2019-08-01,2019-08-30,156.880000,148.840000,149.957271,144.957271,0.459121,5.00,0.0319,-0.1581,-0.0411,454.087868,-72.115001,,,,0.000000
S2,IWM,2019-09-03,2019-09-30,147.450000,151.340000,140.059956,135.059956,0.733101,5.00,0.0339,-0.2042,-0.0825,426.689871,67.010129,,,,0.000000
S2,IWM,2019-10-01,2019-10-31,152.110000,155.450000,143.458604,138.458604,0.470342,5.00,0.0329,-0.1452,-0.0464,452.965850,40.734150,,,,0.000000
S2,IWM,2019-11-01,2019-11-29,156.400000,161.770000,149.299054,144.299054,0.365839,5.00,0.0320,-0.1340,-0.0285,463.416082,30.283918,,,,0.000000
S2,IWM,2019-12-02,2019-12-31,162.150000,165.670000,154.671074,149.671074,0.471492,5.00,0.0308,-0.1545,-0.0438,452.850823,40.849177,,,,0.000000
S2,IWM,2020-01-02,2020-01-31,166.740000,160.530000,159.361699,154.361699,0.361066,5.00,0.0300,-0.1313,-0.0290,463.893376,29.806624,,,,0.000000
S2,IWM,2020-02-03,2020-02-28,161.600000,146.330000,152.914278,147.914278,0.425319,5.00,0.0309,-0.1350,-0.0399,457.468128,-463.768128,,,,0.000000
S2,IWM,2020-03-02,2020-03-31,147.970000,114.460000,135.346476,130.346476,0.519024,5.00,0.0338,-0.1327,-0.0586,448.097591,-454.397591,,,,0.000000
S2,IWM,2020-04-01,2020-04-30,108.700000,130.310000,96.888732,91.888732,1.257046,5.00,0.0460,-0.2373,-0.1582,374.295363,119.404637,,,,0.000000
S2,IWM,2020-05-01,2020-05-29,127.150000,138.900000,118.238064,113.238064,0.981332,5.00,0.0393,-0.2249,-0.1201,401.866791,91.833209,,,,0.000000
S2,IWM,2020-06-01,2020-06-30,139.260000,143.180000,127.177477,122.177477,0.641672,5.00,0.0359,-0.1536,-0.0733,435.832832,57.867168,,,,0.000000
S2,IWM,2020-07-01,2020-07-31,143.650000,147.360000,125.807122,120.807122,0.771545,5.00,0.0348,-0.1546,-0.0957,422.845456,70.854544,,,,0.000000
S2,IWM,2020-08-03,2020-08-31,148.290000,155.430000,132.379446,127.379446,0.681684,5.00,0.0337,-0.1471,-0.0830,431.831612,61.868388,,,,0.000000
S2,IWM,2020-09-01,2020-09-30,155.220000,149.790000,141.609053,136.609053,0.725716,5.00,0.0322,-0.1636,-0.0894,427.428391,66.271609,,,,0.000000
S2,IWM,2020-10-01,2020-10-30,150.810000,153.090000,136.850117,131.850117,0.618838,5.00,0.0332,-0.1435,-0.0729,438.116197,55.583803,,,,0.000000
S2,IWM,2020-11-02,2020-11-30,154.770000,181.020000,138.367101,133.367101,0.622485,5.00,0.0323,-0.1367,-0.0753,437.751517,55.948483,,,,0.000000
S2,IWM,2020-12-01,2020-12-31,183.595000,196.060000,168.596312,163.596312,0.481691,5.00,0.0272,-0.1183,-0.0561,451.830854,41.869146,,,,0.000000
S2,IWM,2021-01-04,2021-01-29,197.540000,205.560000,182.707106,177.707106,0.572452,5.00,0.0253,-0.1366,-0.0705,442.754791,50.945209,,,,0.000000
S2,IWM,2021-02-01,2021-02-26,208.170000,218.310000,187.069878,182.069878,0.622764,5.00,0.0240,-0.1313,-0.0820,437.723599,55.976401,,,,0.000000
S2,IWM,2021-03-01,2021-03-31,223.480000,220.940000,196.871034,191.871034,0.565037,5.00,0.0224,-0.1137,-0.0748,443.496321,50.203679,,,,0.000000
S2,IWM,2021-04-01,2021-04-30,222.400000,224.890000,202.548404,197.548404,0.670624,5.00,0.0225,-0.1432,-0.0903,432.937601,60.762399,,,,0.000000
S2,IWM,2021-05-03,2021-05-28,227.210000,225.500000,206.927626,201.927626,0.615725,5.00,0.0220,-0.1332,-0.0821,438.427539,55.272461,,,,0.000000
S2,IWM,2021-06-01,2021-06-30,227.460000,229.370000,205.772036,200.772036,0.666771,5.00,0.0220,-0.1392,-0.0905,433.322877,60.377123,,,,0.000000
S2,IWM,2021-07-01,2021-07-30,230.810000,221.050000,214.098431,209.098431,0.607074,5.00,0.0217,-0.1399,-0.0794,439.292570,54.407430,,,,0.000000
S2,IWM,2021-08-02,2021-08-31,222.470000,225.920000,202.125103,197.125103,0.682253,5.00,0.0225,-0.1442,-0.0923,431.774731,61.925269,,,,0.000000
S2,IWM,2021-09-01,2021-09-30,226.830000,218.750000,205.437998,200.437998,0.730972,5.00,0.0220,-0.1506,-0.1005,426.902849,66.797151,,,,0.000000
S2,IWM,2021-10-01,2021-10-29,219.950000,228.050000,199.621507,194.621507,0.698464,5.00,0.0227,-0.1467,-0.0946,430.153576,63.546424,,,,0.000000
S2,IWM,2021-11-01,2021-11-30,229.250000,218.170000,214.042152,209.042152,0.594842,5.00,0.0218,-0.1416,-0.0761,440.515783,53.184217,,,,0.000000
S2,IWM,2021-12-01,2021-12-31,223.170000,222.450000,202.221184,197.221184,0.441905,5.00,0.0224,-0.1005,-0.0556,455.809488,37.890512,,,,0.000000
S2,IWM,2022-01-03,2022-01-31,223.710000,201.240000,207.211512,202.211512,0.619980,5.00,0.0224,-0.1423,-0.0809,438.001988,-444.301988,,,,0.000000
S2,IWM,2022-02-01,2022-02-28,201.660000,203.320000,177.635348,172.635348,0.819059,5.00,0.0248,-0.1565,-0.1111,418.094080,75.605920,,,,0.000000
S2,IWM,2022-03-01,2022-03-31,202.660000,205.270000,181.874587,176.874587,0.840467,5.00,0.0247,-0.1673,-0.1155,415.953306,77.746694,,,,0.000000
S2,IWM,2022-04-01,2022-04-29,206.180000,184.950000,192.416335,187.416335,0.596794,5.00,0.0243,-0.1461,-0.0747,440.320602,-446.620602,,,,0.000000
S2,IWM,2022-05-02,2022-05-31,184.900000,185.310000,166.561266,161.561266,0.778771,5.00,0.0270,-0.1620,-0.1043,422.122850,71.577150,,,,0.000000
S2,IWM,2022-06-01,2022-06-30,186.270000,169.360000,170.201944,165.201944,0.656295,5.00,0.0268,-0.1487,-0.0851,434.370503,-24.864918,,,,0.000000
S2,IWM,2022-07-01,2022-07-29,169.050000,187.250000,156.642691,151.642691,0.704022,5.00,0.0296,-0.1695,-0.0893,429.597782,64.102218,,,,0.000000
S2,IWM,2022-08-01,2022-08-31,185.790000,183.500000,173.676501,168.676501,0.802665,5.00,0.0269,-0.1913,-0.1086,419.733470,73.966530,,,,0.000000
S2,IWM,2022-09-01,2022-09-30,181.780000,164.920000,169.936865,164.936865,0.825947,5.00,0.0275,-0.1967,-0.1124,417.405310,-423.705310,,,,0.000000
S2,IWM,2022-10-03,2022-10-31,167.340000,183.330000,149.755569,144.755569,0.590188,5.00,0.0299,-0.1338,-0.0761,440.981201,52.718799,,,,0.000000
S2,IWM,2022-11-01,2022-11-30,185.240000,187.370000,169.060003,164.060003,0.587724,5.00,0.0270,-0.1412,-0.0787,441.227620,52.472380,,,,0.000000
S2,IWM,2022-12-01,2022-12-30,188.151000,174.360000,176.493766,171.493766,0.573380,5.00,0.0266,-0.1572,-0.0745,442.661963,-162.338592,,,,0.000000
S2,IWM,2023-01-03,2023-01-31,175.930000,191.480000,164.035472,159.035472,0.499796,5.00,0.0284,-0.1403,-0.0617,450.020400,43.679600,,,,0.000000
S2,IWM,2023-02-01,2023-02-28,191.190000,188.180000,181.764142,176.764142,0.632654,5.00,0.0262,-0.1820,-0.0818,436.734554,56.965446,,,,0.000000
S2,IWM,2023-03-01,2023-03-31,188.190000,178.400000,176.615586,171.615586,0.653543,5.00,0.0266,-0.1739,-0.0889,434.645658,59.054342,,,,0.000000
S2,IWM,2023-04-03,2023-04-28,178.950000,175.200000,167.523597,162.523597,0.593653,5.00,0.0279,-0.1607,-0.0762,440.634714,53.065286,,,,0.000000
S2,IWM,2023-05-01,2023-05-31,175.000000,173.770000,163.738465,158.738465,0.673682,5.00,0.0286,-0.1780,-0.0908,432.631803,61.068197,,,,0.000000
S2,IWM,2023-06-01,2023-06-30,173.860000,187.270000,162.134318,157.134318,0.654959,5.00,0.0288,-0.1720,-0.0879,434.504082,59.195918,,,,0.000000
S2,IWM,2023-07-03,2023-07-31,186.910000,198.710000,177.447690,172.447690,0.645299,5.00,0.0268,-0.1856,-0.0854,435.470136,58.229864,,,,0.000000
S2,IWM,2023-08-01,2023-08-31,197.430000,188.610000,187.673142,182.673142,0.752027,5.00,0.0253,-0.2050,-0.1065,424.797312,68.902688,,,,0.000000
S2,IWM,2023-09-01,2023-09-29,190.070000,176.740000,177.519409,172.519409,0.532636,5.00,0.0263,-0.1477,-0.0708,446.736358,-30.977224,,,,0.000000
S2,IWM,2023-10-02,2023-10-31,176.330000,164.520000,165.756787,160.756787,0.680511,5.00,0.0284,-0.1838,-0.0919,431.948879,-61.927539,,,,0.000000
S2,IWM,2023-11-01,2023-11-30,164.460000,179.660000,153.915955,148.915955,0.645901,5.00,0.0304,-0.1760,-0.0844,435.409931,58.290069,,,,0.000000
S2,IWM,2023-12-01,2023-12-29,179.200000,200.710000,170.693494,165.693494,0.635422,5.00,0.0279,-0.1902,-0.0814,436.457811,57.242189,,,,0.000000
S2,IWM,2024-01-02,2024-01-31,199.400000,192.880000,188.417511,183.417511,0.771749,5.00,0.0251,-0.2003,-0.1107,422.825071,70.874929,,,,0.000000
S2,IWM,2024-02-01,2024-02-29,194.310000,203.730000,180.528507,175.528507,0.568356,5.00,0.0257,-0.1494,-0.0776,443.164378,50.535622,,,,0.000000
S2,IWM,2024-03-01,2024-03-28,204.530000,210.300000,190.436607,185.436607,0.629511,5.00,0.0244,-0.1603,-0.0886,437.048920,56.651080,,,,0.000000
S2,IWM,2024-04-01,2024-04-30,210.770000,195.900000,197.586379,192.586379,0.638629,5.00,0.0237,-0.1672,-0.0910,436.137078,-111.074997,,,,0.000000
S2,IWM,2024-05-01,2024-05-31,195.880000,205.770000,183.108844,178.108844,0.680822,5.00,0.0255,-0.1751,-0.0964,431.917838,61.782162,,,,0.000000
S2,IWM,2024-06-03,2024-06-28,207.530000,202.890000,196.685191,191.685191,0.438728,5.00,0.0241,-0.1378,-0.0547,456.127235,37.572765,,,,0.000000
S2,IWM,2024-07-01,2024-07-31,203.520000,223.860000,192.958060,187.958060,0.560220,5.00,0.0246,-0.1658,-0.0756,443.978000,49.722000,,,,0.000000
S2,IWM,2024-08-01,2024-08-30,223.770000,220.080000,207.932896,202.932896,0.728931,5.00,0.0223,-0.1741,-0.1083,427.106858,66.593142,,,,0.000000
S2,IWM,2024-09-03,2024-09-30,218.130000,220.890000,206.797810,201.797810,0.828987,5.00,0.0229,-0.2089,-0.1218,417.101256,76.598744,,,,0.000000
S2,IWM,2024-10-01,2024-10-31,220.170000,217.760000,207.587556,202.587556,0.731977,5.00,0.0227,-0.1863,-0.1063,426.802260,66.897740,,,,0.000000
S2,IWM,2024-11-01,2024-11-29,219.500000,241.870000,202.522879,197.522879,0.606824,5.00,0.0228,-0.1469,-0.0863,439.317608,54.382392,,,,0.000000
S2,IWM,2024-12-02,2024-12-31,242.240000,220.960000,226.850416,221.850416,0.677784,5.00,0.0206,-0.1672,-0.1001,432.221586,-438.521586,,,,0.000000
S2,IWM,2025-01-02,2025-01-31,222.930000,226.480000,206.910683,201.910683,0.565285,5.00,0.0224,-0.1424,-0.0795,443.471510,50.228490,,,,0.000000
S2,IWM,2025-02-03,2025-02-28,221.510000,214.650000,213.071858,208.071858,1.102788,5.00,0.0226,-0.2687,-0.1651,389.721227,103.978773,,,,0.000000
S2,IWM,2025-03-03,2025-03-31,215.400000,199.490000,200.881199,195.881199,0.636808,5.00,0.0232,-0.1594,-0.0895,436.319185,-81.739077,,,,0.000000
S2,IWM,2025-04-01,2025-04-30,198.990000,194.860000,188.740993,183.740993,0.673307,5.00,0.0251,-0.1848,-0.0905,432.669286,61.030714,,,,0.000000
S2,IWM,2025-05-01,2025-05-30,195.710000,205.070000,183.136386,178.136386,0.588915,5.00,0.0255,-0.1567,-0.0787,441.108512,52.591488,,,,0.000000
S2,IWM,2025-06-02,2025-06-30,205.320000,215.790000,195.672090,190.672090,0.571431,5.00,0.0244,-0.1701,-0.0731,442.856904,50.843096,,,,0.000000
S2,IWM,2025-07-01,2025-07-31,214.620000,219.390000,206.796789,201.796789,0.701067,5.00,0.0233,-0.2104,-0.0934,429.893328,63.806672,,,,0.000000
S2,IWM,2025-08-01,2025-08-29,216.220000,235.170000,206.950784,201.950784,0.933366,5.00,0.0231,-0.2372,-0.1363,406.663392,87.036608,,,,0.000000
S2,IWM,2025-09-02,2025-09-30,231.990000,241.960000,219.102189,214.102189,0.935462,5.00,0.0216,-0.2185,-0.1411,406.453751,87.246249,,,,0.000000
S2,IWM,2025-10-01,2025-10-31,240.570000,246.230000,221.680307,216.680307,0.846586,5.00,0.0208,-0.1839,-0.1275,415.341363,78.358637,,,,0.000000
S2,IWM,2025-11-03,2025-11-28,246.170000,248.750000,228.959392,223.959392,0.734211,5.00,0.0203,-0.1691,-0.1080,426.578917,67.121083,,,,0.000000
S2,IWM,2025-12-01,2025-12-31,245.570000,246.160000,228.197307,223.197307,0.945946,5.00,0.0204,-0.2047,-0.1447,405.405392,88.294608,,,,0.000000
S2,IWM,2026-01-02,2026-01-30,247.630000,259.650000,232.885657,227.885657,0.568643,5.00,0.0202,-0.1476,-0.0798,443.135654,50.564346,,,,0.000000
S2,IWM,2026-02-02,2026-02-27,258.480000,261.410000,244.008535,239.008535,0.779983,5.00,0.0193,-0.1867,-0.1155,422.001667,71.698333,,,,0.000000
S2,IWM,2026-03-02,2026-03-31,257.810000,248.000000,241.103745,236.103745,0.964223,5.00,0.0194,-0.2107,-0.1488,403.577681,90.122319,,,,0.000000
S2,IWM,2026-04-01,2026-04-30,249.920000,277.970000,222.477816,217.477816,0.751669,5.00,0.0200,-0.1504,-0.1103,424.833134,68.866866,,,,0.000000
S2,IWM,2026-05-01,2026-05-29,278.660000,290.430000,260.680300,255.680300,0.682170,5.00,0.0179,-0.1612,-0.1026,431.782968,61.917032,,,,0.000000
S2,IWM,2026-06-01,2026-06-30,288.370000,300.450000,272.303989,267.303989,0.850682,5.00,0.0173,-0.1972,-0.1323,414.931822,78.768178,,,,0.000000
S2,IWM,2026-07-01,2026-07-31,299.930000,291.200000,280.229705,275.229705,0.777357,5.00,0.0167,-0.1759,-0.1214,422.264266,71.435734,,,,0.000000
S2,IWM,2026-08-03,2026-08-31,292.900000,293.930000,273.122573,268.122573,0.637389,5.00,0.0171,-0.1500,-0.0966,436.261058,57.438942,,,,0.000000
S2,IWM,2026-09-01,2026-09-30,291.980000,277.890000,280.369319,275.369319,0.812462,5.00,0.0171,-0.2095,-0.1240,418.753751,-172.985616,,,,0.000000
S4,SPY,2001-04-02,2001-04-30,116.300000,124.910000,108.973017,103.973017,0.606128,5.00,0.0430,-0.1824,-0.0626,172.357857,-162.469619,110.485000,2.329707,19.338238,1.000000
S4,SPY,2001-05-01,2001-05-31,125.070010,125.950000,116.237412,111.237412,0.578959,5.00,0.0400,-0.1656,-0.0628,208.906918,-153.486437,118.816509,2.668028,64.870480,1.000000
S4,SPY,2001-06-01,2001-06-29,126.200000,122.600010,119.524264,114.524264,0.471264,5.00,0.0396,-0.1633,-0.0418,103.011722,35.439370,119.890000,1.501381,147.901092,1.000000
S4,SPY,2001-07-02,2001-07-31,122.800000,121.350010,116.049861,111.049861,0.483911,5.00,0.0407,-0.1645,-0.0434,107.630647,-21.875399,116.660000,1.560218,95.205249,1.000000
S4,SPY,2001-08-01,2001-08-31,121.970000,114.149990,114.217544,109.217544,0.467961,5.00,0.0410,-0.1519,-0.0439,139.057248,223.557800,115.871500,1.858533,378.820478,1.000000
S4,SPY,2001-09-04,2001-09-28,113.850010,104.440000,108.331935,103.331935,0.509036,5.00,0.0439,-0.1817,-0.0404,128.032249,177.029507,108.157509,1.614933,686.262706,1.000000
S4,SPY,2001-10-01,2001-10-31,103.899990,105.800000,94.983450,89.983450,0.688271,5.00,0.0481,-0.1774,-0.0732,279.302586,-196.927762,98.704990,3.481297,91.824823,1.000000
S4,SPY,2001-11-01,2001-11-30,106.600010,114.050000,98.176168,93.176168,0.475794,5.00,0.0469,-0.1428,-0.0427,197.921651,-193.780259,101.270009,2.455010,13.591393,1.000000
S4,SPY,2001-12-03,2001-12-31,113.649990,114.300000,107.145109,102.145109,0.568831,5.00,0.0440,-0.1788,-0.0506,136.963295,-98.161842,107.967490,1.938464,48.251453,1.000000
S4,SPY,2002-01-02,2002-01-31,115.110000,113.179990,107.736212,102.736212,0.413486,5.00,0.0434,-0.1389,-0.0328,132.311159,12.592554,109.354500,1.736597,154.353713,1.000000
S4,SPY,2002-02-01,2002-02-28,113.090000,111.149990,107.201701,102.201701,0.484980,5.00,0.0442,-0.1688,-0.0368,102.674436,-2.995616,107.435500,1.511725,109.128819,1.000000
S4,SPY,2002-03-01,2002-03-28,111.720000,114.520000,105.094595,100.094595,0.411158,5.00,0.0448,-0.1448,-0.0301,118.170816,-112.982370,106.134000,1.592866,14.638446,1.000000
S4,SPY,2002-04-01,2002-04-30,114.230000,107.860000,109.041334,104.041334,0.485687,5.00,0.0438,-0.1792,-0.0344,117.949132,97.672522,108.518500,1.142344,290.921654,1.000000
S4,SPY,2002-05-01,2002-05-31,107.970000,107.220000,101.933698,96.933698,0.459728,5.00,0.0463,-0.1616,-0.0340,97.903629,-37.738431,102.571500,1.438764,69.615198,1.000000
S4,SPY,2002-06-03,2002-06-28,107.090000,98.960010,101.963451,96.963451,0.451591,5.00,0.0467,-0.1712,-0.0290,109.334144,70.902707,101.735500,1.316982,467.235850,1.000000
S4,SPY,2002-07-01,2002-07-31,99.187000,91.160000,91.826523,86.826523,0.513953,5.00,0.0504,-0.1572,-0.0439,171.204104,261.344679,94.227650,2.225994,508.651075,1.000000
S4,SPY,2002-08-01,2002-08-30,90.880000,91.780000,83.046960,78.046960,0.622282,5.00,0.0550,-0.1709,-0.0581,241.893378,-110.780793,86.336000,3.041215,140.562585,1.000000
S4,SPY,2002-09-03,2002-09-30,90.735000,81.789990,84.988993,79.988993,0.662555,5.00,0.0551,-0.2005,-0.0570,172.813261,60.198039,86.198250,2.390688,562.361574,1.000000
S4,SPY,2002-10-01,2002-10-31,82.438000,88.520000,74.053259,69.053259,0.516998,5.00,0.0607,-0.1455,-0.0437,253.632797,-230.305176,78.316100,3.053326,32.777621,1.000000
S4,SPY,2002-11-01,2002-11-29,88.350010,93.980000,81.658858,76.658858,0.553586,5.00,0.0566,-0.1690,-0.0453,183.932839,-186.521435,83.932509,2.392914,6.861404,1.000000
S4,SPY,2002-12-02,2002-12-31,95.470000,88.230000,88.136101,83.136101,0.309928,5.00,0.0524,-0.1128,-0.0191,135.762391,246.206270,90.696500,1.667552,391.418661,1.000000
S4,SPY,2003-01-02,2003-01-31,88.850010,86.060000,82.033173,77.033173,0.423450,5.00,0.0563,-0.1416,-0.0295,153.574870,46.546383,84.407509,1.959198,209.571253,1.000000
S4,SPY,2003-02-03,2003-02-28,86.140000,84.899990,79.537552,74.537552,0.505856,5.00,0.0580,-0.1596,-0.0381,195.322103,-37.979778,81.833000,2.459077,166.792326,1.000000
S4,SPY,2003-03-03,2003-03-31,85.259990,84.740010,78.164865,73.164865,0.486837,5.00,0.0586,-0.1510,-0.0372,192.276432,-98.005795,80.996990,2.409601,103.720638,1.000000
S4,SPY,2003-04-01,2003-04-30,85.250000,91.910000,78.613530,73.613530,0.433866,5.00,0.0587,-0.1450,-0.0298,160.355861,-169.199914,80.987500,2.037425,0.605946,1.000000
S4,SPY,2003-05-01,2003-05-30,91.920000,96.950000,86.930928,81.930928,0.418601,5.00,0.0544,-0.1633,-0.0232,79.294277,-87.635427,87.324000,1.211544,1.108850,1.000000
S4,SPY,2003-06-02,2003-06-30,97.530000,97.630000,91.974604,86.974604,0.343649,5.00,0.0513,-0.1385,-0.0180,84.152974,-39.829229,92.653500,1.185179,53.773744,1.000000
S4,SPY,2003-07-01,2003-07-31,97.253010,99.390000,92.237451,87.237451,0.495419,5.00,0.0514,-0.1795,-0.0320,86.048303,-74.563425,92.390360,1.355902,20.934878,1.000000
S4,SPY,2003-08-01,2003-08-29,99.190000,101.440000,94.681508,89.681508,0.427435,5.00,0.0504,-0.1736,-0.0224,103.249531,-53.462269,94.230500,1.008922,14.136459,1.000000
S4,SPY,2003-09-02,2003-09-30,101.640000,99.950000,96.350637,91.350637,0.396265,5.00,0.0492,-0.1546,-0.0225,81.965470,21.347616,96.558000,1.215919,112.763086,1.000000
S4,SPY,2003-10-01,2003-10-31,100.240010,105.300000,94.066204,89.066204,0.435042,5.00,0.0499,-0.1520,-0.0298,111.054463,-122.073617,95.228009,1.545586,-1.569154,1.000000
S4,SPY,2003-11-03,2003-11-28,105.750000,106.450000,100.952506,95.952506,0.311077,5.00,0.0473,-0.1408,-0.0129,106.105206,-45.231150,100.462500,0.882123,21.323447,1.000000
S4,SPY,2003-12-01,2003-12-31,106.929990,111.280000,101.491611,96.491611,0.351131,5.00,0.0468,-0.1425,-0.0188,61.897614,-70.524854,101.583490,0.970107,0.822760,1.000000
S4,SPY,2004-01-02,2004-01-30,111.740010,113.480000,106.251207,101.251207,0.356188,5.00,0.0447,-0.1431,-0.0195,76.082978,-62.481728,106.153009,1.018821,13.231518,1.000000
S4,SPY,2004-02-02,2004-02-27,113.700000,115.020000,109.190382,104.190382,0.335001,5.00,0.0440,-0.1521,-0.0141,160.123171,-41.390873,108.015000,0.760851,10.644108,1.000000
S4,SPY,2004-03-01,2004-03-31,115.429990,113.100010,110.122628,105.122628,0.353601,5.00,0.0433,-0.1456,-0.0190,95.130209,15.827881,109.658490,0.840766,73.994378,1.000000
S4,SPY,2004-04-01,2004-04-30,113.070010,110.960010,107.945528,102.945528,0.427427,5.00,0.0442,-0.1651,-0.0259,113.172638,-12.914567,107.416509,1.030136,56.806266,1.000000
S4,SPY,2004-05-03,2004-05-28,111.370000,112.860000,106.845487,101.845487,0.297952,5.00,0.0449,-0.1420,-0.0111,145.478210,-32.031708,105.801500,0.708747,18.497789,1.000000
S4,SPY,2004-06-01,2004-06-30,112.460010,114.530000,108.122484,103.122484,0.456789,5.00,0.0445,-0.1849,-0.0256,168.346060,-34.572152,106.837009,0.854775,14.676433,1.000000
S4,SPY,2004-07-01,2004-07-30,114.250000,110.840000,109.968205,104.968205,0.428323,5.00,0.0438,-0.1805,-0.0227,173.279412,76.345159,108.537500,0.730412,116.004041,1.000000
S4,SPY,2004-08-02,2004-08-31,110.190000,111.110000,106.051060,101.051060,0.501895,5.00,0.0454,-0.1993,-0.0301,173.447685,-32.593488,104.680500,0.865813,13.248238,1.000000
S4,SPY,2004-09-01,2004-09-30,110.940000,111.759990,106.785826,101.785826,0.398089,5.00,0.0451,-0.1764,-0.0192,167.590018,-30.767877,105.393000,0.681163,6.989533,1.000000
S4,SPY,2004-10-01,2004-10-29,112.259990,113.200000,107.576403,102.576403,0.296738,5.00,0.0445,-0.1417,-0.0123,126.855656,-30.562968,106.646991,0.635882,12.801423,1.000000
S4,SPY,2004-11-01,2004-11-30,113.560000,117.890000,108.394157,103.394157,0.359189,5.00,0.0440,-0.1513,-0.0200,100.721801,-61.351597,107.882000,0.854250,-2.395491,1.000000
S4,SPY,2004-12-01,2004-12-31,118.160000,120.870000,113.967214,108.967214,0.310307,5.00,0.0423,-0.1565,-0.0126,185.270042,-25.657354,112.252000,0.447793,-2.458748,1.000000
S4,SPY,2005-01-03,2005-01-31,121.560000,118.160000,117.204321,112.204321,0.237816,5.00,0.0411,-0.1325,-0.0076,185.694892,41.997161,115.482000,0.372445,64.909994,1.000000
S4,SPY,2005-02-01,2005-02-28,118.250000,120.630000,114.218067,109.218067,0.336540,5.00,0.0423,-0.1667,-0.0142,207.607331,-29.648706,112.337500,0.532046,-0.648059,1.000000
S4,SPY,2005-03-01,2005-03-31,120.780000,117.960010,116.768852,111.768852,0.325528,5.00,0.0414,-0.1664,-0.0139,212.039963,32.718535,114.741000,0.418075,51.423251,1.000000
S4,SPY,2005-04-01,2005-04-29,118.630000,115.750000,113.902044,108.902044,0.273512,5.00,0.0421,-0.1385,-0.0117,146.332136,23.495861,112.698500,0.533289,58.923615,1.000000
S4,SPY,2005-05-02,2005-05-31,116.070010,119.480000,111.360209,106.360209,0.341242,5.00,0.0431,-0.1571,-0.0179,140.613036,-42.625137,110.266509,0.653673,-1.932026,1.000000
S4,SPY,2005-06-01,2005-06-30,119.520000,119.179990,115.677121,110.677121,0.338030,5.00,0.0418,-0.1738,-0.0144,221.248799,-10.966027,113.544000,0.417397,6.420628,1.000000
S4,SPY,2005-07-01,2005-07-29,119.450000,123.740010,115.481968,110.481968,0.298627,5.00,0.0419,-0.1607,-0.0117,210.216117,-22.270138,113.477500,0.396320,-3.050806,1.000000
S4,SPY,2005-08-01,2005-08-31,123.830000,122.580000,120.311388,115.311388,0.306950,5.00,0.0404,-0.1760,-0.0114,262.388038,21.428757,117.638500,0.257942,25.978012,1.000000
S4,SPY,2005-09-01,2005-09-30,122.509990,123.039990,118.369383,113.369383,0.386160,5.00,0.0408,-0.1818,-0.0215,212.501911,-17.926905,116.384490,0.526287,5.535797,1.000000
S4,SPY,2005-10-03,2005-10-31,122.960010,120.130000,119.174521,114.174521,0.362876,5.00,0.0407,-0.1834,-0.0172,242.449501,53.790009,116.812009,0.424859,69.438332,1.000000
S4,SPY,2005-11-01,2005-11-30,120.580000,125.410000,115.761738,110.761738,0.329097,5.00,0.0415,-0.1557,-0.0185,152.654715,-43.832353,114.551000,0.644906,-2.801474,1.000000
S4,SPY,2005-12-01,2005-12-30,126.020000,124.509990,122.074037,117.074037,0.234491,5.00,0.0397,-0.1462,-0.0078,236.295644,-2.758332,119.719000,0.242411,7.483633,1.000000
S4,SPY,2006-01-03,2006-01-31,125.100010,127.500000,121.028175,116.028175,0.247349,5.00,0.0400,-0.1472,-0.0090,225.126559,-16.788326,118.845009,0.315449,-0.528323,1.000000
S4,SPY,2006-02-01,2006-02-28,127.820010,128.230000,123.755114,118.755114,0.303403,5.00,0.0391,-0.1651,-0.0141,241.161343,-14.748223,121.429009,0.388912,3.252660,1.000000
S4,SPY,2006-03-01,2006-03-31,128.600010,129.830000,124.492455,119.492455,0.300675,5.00,0.0389,-0.1658,-0.0148,235.383816,-13.766059,122.170009,0.332067,-1.176820,1.000000
S4,SPY,2006-04-03,2006-04-28,130.070010,131.470000,126.425044,121.425044,0.287978,5.00,0.0384,-0.1703,-0.0112,286.978871,-8.802723,123.566509,0.299233,1.772736,1.000000
S4,SPY,2006-05-01,2006-05-31,131.470000,127.509990,127.700147,122.700147,0.355510,5.00,0.0380,-0.1893,-0.0194,276.360043,60.097704,124.896500,0.315463,84.558747,1.000000
S4,SPY,2006-06-01,2006-06-30,127.380000,127.230000,122.664279,117.664279,0.440951,5.00,0.0393,-0.1880,-0.0330,193.752667,-14.591128,121.011000,0.725198,23.283668,1.000000
S4,SPY,2006-07-03,2006-07-31,127.429990,127.850010,122.192829,117.192829,0.408426,5.00,0.0392,-0.1719,-0.0310,156.382172,-28.728572,121.058491,0.837910,23.669746,1.000000
S4,SPY,2006-08-01,2006-08-31,127.340000,130.640000,123.240677,118.240677,0.485717,5.00,0.0393,-0.2114,-0.0367,241.250635,-25.750807,120.973000,0.630546,-1.817902,1.000000
S4,SPY,2006-09-01,2006-09-29,131.140000,133.580000,126.881818,121.881818,0.287057,5.00,0.0381,-0.1598,-0.0144,236.212268,-17.113188,124.583000,0.350362,-1.332755,1.000000
S4,SPY,2006-10-02,2006-10-31,133.539990,137.789990,129.890374,124.890374,0.355572,5.00,0.0374,-0.1925,-0.0189,296.910938,-6.551968,126.862990,0.297298,-2.929382,1.000000
S4,SPY,2006-11-01,2006-11-30,138.220000,140.530000,134.360927,129.360927,0.274290,5.00,0.0362,-0.1670,-0.0125,301.053464,-5.129911,131.309000,0.232898,0.180844,1.000000
S4,SPY,2006-12-01,2006-12-29,140.530000,141.620000,136.441648,131.441648,0.377239,5.00,0.0356,-0.1884,-0.0239,294.981411,-12.379486,133.503500,0.388906,-1.762829,1.000000
S4,SPY,2007-01-03,2007-01-31,142.250000,143.750000,137.876126,132.876126,0.271386,5.00,0.0351,-0.1546,-0.0139,276.208497,-11.287080,135.137500,0.294845,0.508839,1.000000
S4,SPY,2007-02-01,2007-02-28,144.149990,140.929990,140.068135,135.068135,0.295055,5.00,0.0347,-0.1675,-0.0152,310.670238,58.845246,136.942490,0.276113,66.401024,1.000000
S4,SPY,2007-03-01,2007-03-30,139.340000,142.000000,137.422954,132.422954,0.643766,5.00,0.0359,-0.3158,-0.0425,457.400192,37.906877,132.373000,0.217768,4.757070,1.000000
S4,SPY,2007-04-02,2007-04-30,142.160000,148.289990,137.437552,132.437552,0.385455,5.00,0.0352,-0.1779,-0.0277,253.148273,-26.518834,135.052000,0.531386,-2.475810,1.000000
S4,SPY,2007-05-01,2007-05-31,148.420000,153.320010,143.478691,138.478691,0.406034,5.00,0.0337,-0.1806,-0.0322,261.978769,-24.599930,140.999000,0.546131,-1.140270,1.000000
S4,SPY,2007-06-01,2007-06-29,153.880000,150.429990,148.429588,143.429588,0.355725,5.00,0.0325,-0.1600,-0.0273,245.021683,44.085395,146.186000,0.562354,74.198228,1.000000
S4,SPY,2007-07-02,2007-07-31,150.870000,145.720000,143.401920,138.401920,0.479367,5.00,0.0331,-0.1635,-0.0498,101.856473,182.125468,143.326500,1.422512,285.889948,1.000000
S4,SPY,2007-08-01,2007-08-31,145.179990,147.590000,138.131203,133.131203,0.610588,5.00,0.0344,-0.1930,-0.0685,131.199609,-56.246770,137.920990,1.712371,63.381564,1.000000
S4,SPY,2007-09-04,2007-09-28,147.450000,152.580000,138.683954,133.683954,0.604352,5.00,0.0339,-0.1730,-0.0685,230.475537,-225.913360,140.077500,2.909108,14.012177,1.000000
S4,SPY,2007-10-01,2007-10-31,152.600010,154.649990,145.339676,140.339676,0.528840,5.00,0.0328,-0.1734,-0.0551,128.310699,-41.007263,144.970010,1.442280,59.786755,1.000000
S4,SPY,2007-11-01,2007-11-30,153.289990,148.660000,147.072034,142.072034,0.705540,5.00,0.0326,-0.2181,-0.0799,235.258889,159.747579,145.625490,1.611585,259.802125,1.000000
S4,SPY,2007-12-03,2007-12-31,148.190000,146.210010,138.974337,133.974337,0.658899,5.00,0.0337,-0.1792,-0.0775,224.062131,-124.133680,140.780500,2.899520,109.378451,1.000000
S4,SPY,2008-01-02,2008-01-31,146.530000,137.370000,139.309160,134.309160,0.480453,5.00,0.0341,-0.1618,-0.0463,106.612784,188.864259,139.203500,1.440921,488.277044,1.000000
S4,SPY,2008-02-01,2008-02-29,137.940000,133.820010,127.852719,122.852719,0.559674,5.00,0.0362,-0.1526,-0.0613,247.992553,-26.411957,131.043000,3.039599,231.030596,1.000000
S4,SPY,2008-03-03,2008-03-31,133.140000,131.970000,126.421095,121.421095,0.615234,5.00,0.0376,-0.1883,-0.0607,127.279731,-11.678758,126.483000,1.888032,125.050973,1.000000
S4,SPY,2008-04-01,2008-04-30,133.710010,138.259990,123.123603,118.123603,0.433190,5.00,0.0374,-0.1233,-0.0425,234.363654,-224.147855,127.024510,2.776827,19.665799,1.000000
S4,SPY,2008-05-01,2008-05-30,138.390000,140.350010,131.208610,126.208610,0.501252,5.00,0.0361,-0.1604,-0.0449,109.851145,-81.838685,131.470500,1.599763,37.462460,1.000000
S4,SPY,2008-06-02,2008-06-30,139.830000,127.980000,133.346409,128.346409,0.578056,5.00,0.0358,-0.1841,-0.0545,152.365038,132.920548,132.838500,1.593798,743.944720,1.000000
S4,SPY,2008-07-01,2008-07-31,126.520000,126.830000,120.884703,115.884703,0.711678,5.00,0.0395,-0.2171,-0.0696,175.106910,-34.939873,120.194000,1.772044,80.546688,1.000000
S4,SPY,2008-08-01,2008-08-29,127.120000,128.789990,119.063627,114.063627,0.520835,5.00,0.0393,-0.1564,-0.0496,169.832408,-155.877253,120.764000,2.219159,23.405155,1.000000
S4,SPY,2008-09-02,2008-09-30,130.030000,115.990010,122.072476,117.072476,0.374109,5.00,0.0385,-0.1269,-0.0302,131.233674,364.268838,123.528500,1.686446,1004.952512,1.000000
S4,SPY,2008-10-01,2008-10-31,115.270000,96.830000,106.172704,101.172704,0.703549,5.00,0.0434,-0.1786,-0.0759,280.028811,792.995454,109.506500,3.503837,1582.474265,1.000000
S4,SPY,2008-11-03,2008-11-28,96.780000,90.090000,82.637082,77.637082,0.808427,5.00,0.0517,-0.1613,-0.0893,709.673302,167.311733,91.941000,7.905160,886.435034,1.000000
S4,SPY,2008-12-01,2008-12-31,87.509990,90.240010,76.222599,71.222599,1.018324,5.00,0.0571,-0.2012,-0.1145,585.768196,-446.121392,83.134490,6.876006,149.096805,1.000000
S4,SPY,2009-01-02,2009-01-30,90.440000,82.830000,80.658987,75.658987,0.632863,5.00,0.0553,-0.1556,-0.0611,354.377854,262.319577,85.918000,4.176642,626.147431,1.000000
S4,SPY,2009-02-02,2009-02-27,81.570010,73.929990,74.666542,69.666542,0.747992,5.00,0.0613,-0.1963,-0.0692,287.516774,317.422428,77.491509,3.623160,688.044376,1.000000
S4,SPY,2009-03-02,2009-03-31,72.520000,79.520000,65.633115,60.633115,0.787034,5.00,0.0689,-0.1998,-0.0721,277.874857,-232.732648,68.894000,3.565783,54.592209,1.000000
S4,SPY,2009-04-01,2009-04-30,78.530000,87.420000,71.482292,66.482292,0.714398,5.00,0.0637,-0.1885,-0.0642,259.059298,-241.475657,74.603500,3.304991,27.033641,1.000000
S4,SPY,2009-05-01,2009-05-29,87.440000,92.530000,79.115554,74.115554,0.598720,5.00,0.0572,-0.1597,-0.0536,277.152472,-254.542780,83.068000,3.370245,32.059692,1.000000
S4,SPY,2009-06-01,2009-06-30,93.670000,91.950000,85.247743,80.247743,0.427545,5.00,0.0534,-0.1282,-0.0332,212.187140,-91.498573,88.986500,2.549416,130.138567,1.000000
S4,SPY,2009-07-01,2009-07-31,92.340000,98.810000,85.550235,80.550235,0.455178,5.00,0.0541,-0.1472,-0.0325,152.523101,-156.285919,87.723000,1.980409,5.687182,1.000000
S4,SPY,2009-08-03,2009-08-31,99.850010,102.460010,92.467525,87.467525,0.377645,5.00,0.0501,-0.1264,-0.0258,154.570990,-108.749687,94.857509,1.923355,55.271303,1.000000
S4,SPY,2009-09-01,2009-09-30,101.950000,105.590000,95.787031,90.787031,0.573363,5.00,0.0490,-0.1783,-0.0461,144.204270,-109.853536,96.852500,2.015406,43.800734,1.000000
S4,SPY,2009-10-01,2009-10-30,105.340000,103.560000,98.539868,93.539868,0.555500,5.00,0.0475,-0.1684,-0.0463,156.614307,-16.737953,100.073000,2.121643,149.326354,1.000000
S4,SPY,2009-11-02,2009-11-30,104.130000,109.940000,96.948427,91.948427,0.439400,5.00,0.0480,-0.1415,-0.0326,163.511602,-167.494075,98.923500,2.074516,5.467528,1.000000
S4,SPY,2009-12-01,2009-12-31,110.920000,111.440000,103.890501,98.890501,0.359859,5.00,0.0451,-0.1261,-0.0235,115.542620,-91.540220,105.374000,1.515285,33.452400,1.000000
S4,SPY,2010-01-04,2010-01-29,112.370000,107.390000,105.958962,100.958962,0.328818,5.00,0.0445,-0.1246,-0.0188,107.535097,108.540254,106.751500,1.404169,225.525351,1.000000
S4,SPY,2010-02-01,2010-02-26,108.149990,110.740010,100.956011,95.956011,0.406861,5.00,0.0462,-0.1349,-0.0291,170.465724,-149.987603,102.742491,2.111518,29.928120,1.000000
S4,SPY,2010-03-01,2010-03-31,111.200000,117.000000,104.400477,99.400477,0.432960,5.00,0.0450,-0.1445,-0.0313,116.481411,-126.379133,105.640000,1.597774,-0.447722,1.000000
S4,SPY,2010-04-01,2010-04-30,117.800000,118.812500,111.466991,106.466991,0.344603,5.00,0.0424,-0.1296,-0.0205,82.790125,-47.317628,111.910000,1.172504,44.922497,1.000000
S4,SPY,2010-05-03,2010-05-28,119.380000,109.369000,112.176373,107.176373,0.433930,5.00,0.0419,-0.1418,-0.0332,150.854948,303.345602,113.411000,1.942480,744.387853,1.000000
S4,SPY,2010-06-01,2010-06-30,108.350010,103.220000,99.743890,94.743890,0.734041,5.00,0.0461,-0.1848,-0.0772,293.575724,35.240181,102.932509,3.669798,338.265905,1.000000
S4,SPY,2010-07-01,2010-07-30,103.149990,110.270000,95.605175,90.605175,0.561700,5.00,0.0485,-0.1624,-0.0492,193.876813,-200.337710,97.992491,2.500468,2.989102,1.000000
S4,SPY,2010-08-02,2010-08-31,111.990010,105.310000,103.563351,98.563351,0.330344,5.00,0.0446,-0.1095,-0.0235,154.994022,113.015838,106.390509,1.880284,277.459860,1.000000
S4,SPY,2010-09-01,2010-09-30,106.730000,114.130000,97.835020,92.835020,0.402896,5.00,0.0468,-0.1217,-0.0324,204.163816,-209.160221,101.393500,2.444535,4.453595,1.000000
S4,SPY,2010-10-01,2010-10-29,114.990010,118.490010,107.482343,102.482343,0.405870,5.00,0.0435,-0.1329,-0.0303,142.340208,-134.423177,109.240509,1.829272,17.367030,1.000000
S4,SPY,2010-11-01,2010-11-30,119.070010,118.492490,112.155393,107.155393,0.416166,5.00,0.0420,-0.1405,-0.0302,111.470397,-56.788650,113.116509,1.530870,64.131748,1.000000
S4,SPY,2010-12-01,2010-12-31,120.200000,125.750000,112.256609,107.256609,0.300159,5.00,0.0416,-0.1062,-0.0197,116.712904,-126.300942,114.190000,1.467288,-0.138039,1.000000
S4,SPY,2011-01-03,2011-01-31,126.710010,128.679990,119.980836,114.980836,0.339905,5.00,0.0395,-0.1253,-0.0214,85.957070,-83.166071,120.374509,1.199476,12.240999,1.000000
S4,SPY,2011-02-01,2011-02-28,129.460010,133.149990,123.157571,118.157571,0.343017,5.00,0.0386,-0.1302,-0.0206,95.838414,-50.980399,122.987009,1.130839,37.251862,1.000000
S4,SPY,2011-03-01,2011-03-31,133.570010,132.590000,125.272876,120.272876,0.503399,5.00,0.0374,-0.1486,-0.0460,161.578763,-110.932568,126.891509,2.119187,60.096195,1.000000
S4,SPY,2011-04-01,2011-04-29,133.410000,136.429990,125.869211,120.869211,0.406548,5.00,0.0375,-0.1340,-0.0314,117.746864,-122.445027,126.739500,1.584017,4.751837,1.000000
S4,SPY,2011-05-02,2011-05-31,137.070010,134.899990,130.718225,125.718225,0.367697,5.00,0.0365,-0.1357,-0.0235,113.029114,11.144376,130.216510,0.996272,83.451915,1.000000
S4,SPY,2011-06-01,2011-06-30,134.509990,131.970000,128.751216,123.751216,0.519397,5.00,0.0372,-0.1753,-0.0395,167.568665,40.209068,127.784490,1.228358,120.555145,1.000000
S4,SPY,2011-07-01,2011-07-29,132.090000,129.330000,124.909514,119.909514,0.499258,5.00,0.0379,-0.1562,-0.0420,126.366546,-9.181031,125.485500,1.762924,126.635515,1.000000
S4,SPY,2011-08-01,2011-08-31,130.840000,122.220000,122.295313,117.295313,0.358878,5.00,0.0382,-0.1163,-0.0279,132.842551,401.903689,124.298000,1.687304,551.727491,1.000000
S4,SPY,2011-09-01,2011-09-30,122.289990,113.149990,111.174398,106.174398,0.659276,5.00,0.0409,-0.1586,-0.0723,356.846151,354.064044,116.175490,4.227737,720.360195,1.000000
S4,SPY,2011-10-03,2011-10-31,112.490010,125.500000,102.546619,97.546619,0.721493,5.00,0.0444,-0.1740,-0.0783,351.996160,-352.152644,106.865509,4.241454,9.293516,1.000000
S4,SPY,2011-11-01,2011-11-30,122.030000,124.990010,115.834571,110.834571,1.019336,5.00,0.0410,-0.2543,-0.1179,230.825482,-95.680864,115.928500,3.327591,144.594618,1.000000
S4,SPY,2011-12-01,2011-12-30,124.850010,125.500000,114.016929,109.016929,0.672873,5.00,0.0400,-0.1629,-0.0743,343.662371,-308.558073,118.607509,4.109497,44.554297,1.000000
S4,SPY,2012-01-03,2012-01-31,127.759990,131.320010,118.369915,113.369915,0.303700,5.00,0.0391,-0.0988,-0.0228,169.118929,-163.149511,121.371990,1.994890,15.419419,1.000000
S4,SPY,2012-02-01,2012-02-29,132.289990,137.020000,124.942037,119.942037,0.372620,5.00,0.0378,-0.1278,-0.0268,108.118380,-105.975405,125.675490,1.453804,11.592976,1.000000
S4,SPY,2012-03-01,2012-03-30,137.310000,140.810000,130.696127,125.696127,0.442142,5.00,0.0364,-0.1501,-0.0332,107.710024,-85.938497,130.444500,1.267616,6.058853,1.000000
S4,SPY,2012-04-02,2012-04-30,140.640000,139.870000,135.026687,130.026687,0.470423,5.00,0.0356,-0.1673,-0.0330,196.427398,-8.755891,133.608000,1.016009,55.252779,1.000000
S4,SPY,2012-05-01,2012-05-31,139.789990,131.470000,133.485896,128.485896,0.489011,5.00,0.0358,-0.1633,-0.0381,145.171298,226.786633,132.800490,1.255318,514.456981,1.000000
S4,SPY,2012-06-01,2012-06-29,129.410000,136.105000,124.055528,119.055528,0.803076,5.00,0.0386,-0.2323,-0.0787,224.099017,-117.392771,122.939500,1.928037,4.553404,1.000000
S4,SPY,2012-07-02,2012-07-31,136.480000,137.710010,128.993993,123.993993,0.471997,5.00,0.0366,-0.1486,-0.0397,119.784023,-109.373406,129.656000,1.669837,19.860617,1.000000
S4,SPY,2012-08-01,2012-08-31,138.700000,141.160000,131.174037,126.174037,0.377887,5.00,0.0360,-0.1281,-0.0282,96.330475,-88.985865,131.765000,1.341191,16.794611,1.000000
S4,SPY,2012-09-04,2012-09-28,141.039990,143.970000,135.479026,130.479026,0.458351,5.00,0.0355,-0.1654,-0.0313,224.133870,-64.149126,133.987990,1.208655,20.331186,1.000000
S4,SPY,2012-10-01,2012-10-31,144.520000,141.350010,137.921201,132.921201,0.395829,5.00,0.0346,-0.1404,-0.0279,124.837056,42.799736,137.294000,1.016999,114.366690,1.000000
S4,SPY,2012-11-01,2012-11-30,141.649990,142.155000,134.461839,129.461839,0.468010,5.00,0.0353,-0.1506,-0.0386,101.569835,-91.560901,134.567490,1.483708,19.458933,1.000000
S4,SPY,2012-12-03,2012-12-31,142.800000,142.410000,136.199181,131.199181,0.380317,5.00,0.0350,-0.1367,-0.0260,124.361681,-39.806243,135.660000,1.084754,40.087384,1.000000
S4,SPY,2013-01-02,2013-01-31,145.110000,149.700000,135.052250,130.052250,0.278481,5.00,0.0345,-0.0908,-0.0216,148.412546,-158.904967,137.854500,1.762606,-1.042422,1.000000
S4,SPY,2013-02-01,2013-02-28,150.649990,151.610000,144.412138,139.412138,0.305414,5.00,0.0332,-0.1222,-0.0170,175.002161,-6.479606,143.117491,0.760788,48.507788,1.000000
S4,SPY,2013-03-01,2013-03-28,151.090000,156.670000,144.224968,139.224968,0.582366,5.00,0.0331,-0.1772,-0.0538,181.343725,-123.615284,143.535500,1.706336,-1.768347,1.000000
S4,SPY,2013-04-01,2013-04-30,156.590000,159.679990,150.872848,145.872848,0.455896,5.00,0.0319,-0.1636,-0.0322,247.471334,-39.368293,148.760500,0.818261,6.318219,1.000000
S4,SPY,2013-05-01,2013-05-31,159.330000,163.445010,153.722527,148.722527,0.499340,5.00,0.0314,-0.1744,-0.0372,269.200169,-39.248071,151.363500,0.832315,3.499427,1.000000
S4,SPY,2013-06-03,2013-06-28,163.830000,160.420000,157.518303,152.518303,0.403696,5.00,0.0305,-0.1456,-0.0283,246.115424,45.104548,155.638500,0.985048,112.689673,1.000000
S4,SPY,2013-07-01,2013-07-31,161.259990,168.710010,152.412510,147.412510,0.457589,5.00,0.0310,-0.1374,-0.0425,126.260816,-138.324948,153.196990,1.720197,-2.614132,1.000000
S4,SPY,2013-08-01,2013-08-30,169.990010,163.649990,162.908466,157.908466,0.300708,5.00,0.0294,-0.1142,-0.0190,183.527108,88.086071,161.490510,0.718023,139.267521,1.000000
S4,SPY,2013-09-03,2013-09-30,165.230000,168.009990,156.560472,151.560472,0.345598,5.00,0.0303,-0.1142,-0.0277,113.125593,-109.611917,156.968500,1.476854,12.963677,1.000000
S4,SPY,2013-10-01,2013-10-31,168.140000,175.790000,161.564378,156.564378,0.459486,5.00,0.0297,-0.1555,-0.0362,234.145172,-62.233800,159.733000,0.969559,-1.776460,1.000000
S4,SPY,2013-11-01,2013-11-29,176.020000,181.000000,169.582953,164.582953,0.434635,5.00,0.0284,-0.1517,-0.0328,277.387947,-50.597349,167.219000,0.844562,-0.154679,1.000000
S4,SPY,2013-12-02,2013-12-31,181.090000,184.690000,174.749876,169.749876,0.453017,5.00,0.0276,-0.1571,-0.0350,303.605469,-38.089381,172.035500,0.774696,3.528526,1.000000
S4,SPY,2014-01-02,2014-01-31,183.980000,178.180000,178.533890,173.533890,0.554427,5.00,0.0272,-0.1889,-0.0446,390.556434,139.479422,174.781000,0.707101,199.585856,1.000000
S4,SPY,2014-02-03,2014-02-28,177.950000,186.290000,171.154077,166.154077,0.526477,5.00,0.0281,-0.1679,-0.0465,290.537827,-87.893430,169.052500,1.330278,1.936669,1.000000
S4,SPY,2014-03-03,2014-03-31,184.690000,187.010000,179.541473,174.541473,0.705737,5.00,0.0271,-0.2219,-0.0653,433.354327,-18.267350,175.455500,0.953307,15.939707,1.000000
S4,SPY,2014-04-01,2014-04-30,187.620000,188.310000,179.511237,174.511237,0.451569,5.00,0.0266,-0.1421,-0.0407,209.143897,-61.311042,178.239000,1.270771,30.059187,1.000000
S4,SPY,2014-05-01,2014-05-30,188.220000,192.680000,181.177127,176.177127,0.512009,5.00,0.0266,-0.1630,-0.0457,290.568901,-64.478208,178.809000,1.049571,-1.272056,1.000000
S4,SPY,2014-06-02,2014-06-30,192.950000,195.720000,186.767255,181.767255,0.412333,5.00,0.0259,-0.1497,-0.0295,365.406943,-26.153920,183.302500,0.601647,2.227519,1.000000
S4,SPY,2014-07-01,2014-07-31,196.190000,193.090000,189.467671,184.467671,0.406264,5.00,0.0255,-0.1432,-0.0307,335.579415,45.388631,186.380500,0.674887,81.700904,1.000000
S4,SPY,2014-08-01,2014-08-29,192.560000,200.710000,186.641539,181.641539,0.539335,5.00,0.0260,-0.1802,-0.0450,395.391537,-36.678446,182.932000,0.783711,-2.790804,1.000000
S4,SPY,2014-09-02,2014-09-30,200.970000,197.020000,194.488618,189.488618,0.428274,5.00,0.0249,-0.1506,-0.0327,382.030156,92.539855,190.921500,0.681457,127.308185,1.000000
S4,SPY,2014-10-01,2014-10-31,196.700000,201.660000,188.618928,183.618928,0.581376,5.00,0.0254,-0.1690,-0.0597,263.911315,-90.786330,186.865000,1.466562,7.182212,1.000000
S4,SPY,2014-11-03,2014-11-28,201.920000,207.200000,194.387683,189.387683,0.475915,5.00,0.0248,-0.1519,-0.0427,328.407992,-78.830610,191.824000,1.196312,2.659043,1.000000
S4,SPY,2014-12-01,2014-12-31,206.400000,205.540000,200.009601,195.009601,0.599132,5.00,0.0242,-0.1874,-0.0562,418.346159,6.476606,196.080000,0.852993,41.312697,1.000000
S4,SPY,2015-01-02,2015-01-30,206.380000,199.450000,197.653755,192.653755,0.441983,5.00,0.0242,-0.1366,-0.0415,239.852940,189.931224,196.061000,1.247757,279.958678,1.000000
S4,SPY,2015-02-02,2015-02-27,200.050000,210.660000,190.906275,185.906275,0.492086,5.00,0.0250,-0.1444,-0.0495,229.996713,-154.498966,190.047500,1.933279,-0.929742,1.000000
S4,SPY,2015-03-02,2015-03-31,210.780000,206.430000,202.884250,197.884250,0.509697,5.00,0.0237,-0.1566,-0.0489,322.723428,54.307783,200.241000,1.093681,122.156222,1.000000
S4,SPY,2015-04-01,2015-04-30,206.390000,208.460000,197.688837,192.688837,0.560664,5.00,0.0242,-0.1612,-0.0588,263.258226,-104.052911,196.070500,1.574909,6.821570,1.000000
S4,SPY,2015-05-01,2015-05-29,209.400000,211.140000,201.196495,196.196495,0.404555,5.00,0.0239,-0.1318,-0.0351,282.864404,-54.558083,198.930000,0.966704,11.106805,1.000000
S4,SPY,2015-06-01,2015-06-30,211.940000,205.850000,203.142800,198.142800,0.449501,5.00,0.0236,-0.1380,-0.0429,253.196851,17.049798,201.343000,1.181669,99.716601,1.000000
S4,SPY,2015-07-01,2015-07-31,207.730000,210.500000,197.949830,192.949830,0.351869,5.00,0.0241,-0.1111,-0.0316,142.809805,-86.135108,197.343500,1.173637,5.491725,1.000000
S4,SPY,2015-08-03,2015-08-31,210.460000,197.670000,203.000019,198.000019,0.517156,5.00,0.0238,-0.1615,-0.0487,358.219607,432.767283,199.937000,1.036334,994.135038,1.000000
S4,SPY,2015-09-01,2015-09-30,193.120000,191.630000,182.237103,177.237103,1.066470,5.00,0.0259,-0.2353,-0.1476,425.761476,-162.671735,183.464000,5.324084,272.539742,1.000000
S4,SPY,2015-10-01,2015-10-30,192.080000,207.930000,179.751166,174.751166,0.609776,5.00,0.0260,-0.1516,-0.0731,274.146832,-286.661891,182.476000,3.351245,-3.065059,1.000000
S4,SPY,2015-11-02,2015-11-30,208.320000,208.690000,199.468030,194.468030,0.507812,5.00,0.0240,-0.1498,-0.0514,261.614164,-67.620702,197.904000,1.559923,47.040438,1.000000
S4,SPY,2015-12-01,2015-12-31,209.440000,203.870000,199.658695,194.658695,0.494873,5.00,0.0239,-0.1423,-0.0520,184.785245,154.195356,198.968000,1.652031,279.361151,1.000000
S4,SPY,2016-01-04,2016-01-29,200.490000,193.720800,195.310144,190.310144,0.985417,5.00,0.0249,-0.2697,-0.1151,560.672596,175.739980,190.465500,1.747499,420.332575,1.000000
S4,SPY,2016-02-01,2016-02-29,192.530000,193.560000,182.477827,177.477827,0.738240,5.00,0.0260,-0.1863,-0.0905,230.015889,-178.085468,182.903500,3.038398,61.380422,1.000000
S4,SPY,2016-03-01,2016-03-31,195.010000,205.520000,182.829651,177.829651,0.499988,5.00,0.0256,-0.1323,-0.0568,220.321462,-231.029441,185.259500,2.703203,-1.257980,1.000000
S4,SPY,2016-04-01,2016-04-29,204.350000,206.330800,197.290996,192.290996,0.675123,5.00,0.0245,-0.1966,-0.0719,386.593876,-67.216214,194.132500,1.382566,12.978056,1.000000
S4,SPY,2016-05-02,2016-05-31,206.920000,209.840000,198.605630,193.605630,0.461109,5.00,0.0242,-0.1441,-0.0436,268.842759,-60.710111,196.574000,1.117907,14.419607,1.000000
S4,SPY,2016-06-01,2016-06-30,209.120000,209.475000,202.022592,197.022592,0.608676,5.00,0.0239,-0.1838,-0.0617,388.894541,33.743867,198.664000,1.139029,96.229177,1.000000
S4,SPY,2016-07-01,2016-07-29,209.360000,217.120000,196.624586,191.624586,0.670372,5.00,0.0239,-0.1628,-0.0849,302.120474,-312.904231,198.892000,3.691577,-1.333756,1.000000
S4,SPY,2016-08-01,2016-08-31,217.190000,217.380000,209.389482,204.389482,0.514150,5.00,0.0230,-0.1595,-0.0503,351.555030,-32.119318,206.330500,0.970719,22.987552,1.000000
S4,SPY,2016-09-01,2016-09-30,217.370000,216.300000,209.428584,204.428584,0.530745,5.00,0.0230,-0.1619,-0.0532,349.670772,-36.027820,206.501500,1.100369,30.384569,1.000000
S4,SPY,2016-10-03,2016-10-31,215.820000,212.550000,208.817152,203.817152,0.568244,5.00,0.0232,-0.1769,-0.0553,419.645526,49.395599,205.029000,0.976548,99.675975,1.000000
S4,SPY,2016-11-01,2016-11-30,212.930000,220.380000,204.444634,199.444634,0.496271,5.00,0.0235,-0.1508,-0.0495,295.370279,-87.978240,202.283500,1.288840,0.728617,1.000000
S4,SPY,2016-12-01,2016-12-30,220.730000,223.530000,213.100348,208.100348,0.467105,5.00,0.0227,-0.1518,-0.0435,376.727572,-42.426408,209.693500,0.827533,3.066398,1.000000
S4,SPY,2017-01-03,2017-01-31,225.040000,227.530000,216.474650,211.474650,0.344341,5.00,0.0222,-0.1180,-0.0295,315.264790,-54.306251,213.788000,0.810339,1.743580,1.000000
S4,SPY,2017-02-01,2017-02-28,228.255000,236.470000,221.256879,216.256879,0.379933,5.00,0.0219,-0.1375,-0.0299,457.692395,-28.149141,216.842250,0.542228,-2.469622,1.000000
S4,SPY,2017-03-01,2017-03-31,238.390000,235.740000,228.930076,223.930076,0.332255,5.00,0.0210,-0.1107,-0.0300,290.653880,-23.673291,226.470500,0.779218,30.473036,1.000000
S4,SPY,2017-04-03,2017-04-28,235.800000,238.080000,228.997404,223.997404,0.476789,5.00,0.0212,-0.1623,-0.0430,521.204651,-28.701129,224.010000,0.701432,3.213120,1.000000
S4,SPY,2017-05-01,2017-05-31,238.680000,241.440000,231.154450,226.154450,0.426541,5.00,0.0209,-0.1459,-0.0390,454.273355,-24.140787,226.746000,0.560825,-1.262383,1.000000
S4,SPY,2017-06-01,2017-06-30,241.970000,241.800000,235.040346,230.040346,0.410213,5.00,0.0207,-0.1478,-0.0352,502.031868,-9.203789,229.871500,0.430532,2.278079,1.000000
S4,SPY,2017-07-03,2017-07-31,242.880000,246.770000,234.837290,229.837290,0.381415,5.00,0.0206,-0.1325,-0.0346,433.846153,-34.436466,230.736000,0.618586,-1.269339,1.000000
S4,SPY,2017-08-01,2017-08-31,247.460000,247.490000,240.422046,235.422046,0.392491,5.00,0.0202,-0.1441,-0.0339,500.161197,7.082864,235.087000,0.394103,16.694061,1.000000
S4,SPY,2017-09-01,2017-09-29,247.920000,251.230000,240.201434,235.201434,0.460096,5.00,0.0202,-0.1528,-0.0450,489.885192,-32.831838,235.524000,0.681514,-1.240078,1.000000
S4,SPY,2017-10-02,2017-10-31,251.490000,257.150000,244.474779,239.474779,0.456455,5.00,0.0199,-0.1584,-0.0425,501.697563,-13.716875,238.915500,0.473431,-2.569312,1.000000
S4,SPY,2017-11-01,2017-11-30,258.040000,265.010000,249.477351,244.477351,0.430293,5.00,0.0194,-0.1411,-0.0435,464.805948,-42.469359,245.138000,0.739001,-2.148498,1.000000
S4,SPY,2017-12-01,2017-12-29,264.760000,266.860000,258.247190,253.247190,0.516641,5.00,0.0189,-0.1775,-0.0505,492.071127,-1.054799,251.522000,0.437353,0.466328,1.000000
S4,SPY,2018-01-02,2018-01-31,267.840000,281.900000,259.686311,254.686311,0.402219,5.00,0.0187,-0.1391,-0.0394,513.424775,-23.530318,254.448000,0.536466,-0.655543,1.000000
S4,SPY,2018-02-01,2018-02-28,281.070000,271.650000,273.975679,268.975679,0.621749,5.00,0.0178,-0.1944,-0.0705,508.075199,45.645579,267.016500,0.702501,295.738644,1.000000
S4,SPY,2018-03-01,2018-03-29,271.410000,263.150000,260.186644,255.186644,0.642577,5.00,0.0184,-0.1717,-0.0850,379.866223,267.203538,257.839500,2.094095,421.805350,1.000000
S4,SPY,2018-04-02,2018-04-30,262.550000,264.510000,249.104619,244.104619,0.716077,5.00,0.0190,-0.1758,-0.1003,274.570440,-222.167270,249.422500,3.461781,61.853170,1.000000
S4,SPY,2018-05-01,2018-05-31,263.870000,270.940000,252.098259,247.098259,0.694640,5.00,0.0189,-0.1793,-0.0952,324.745617,-172.013020,250.676500,2.520337,20.006702,1.000000
S4,SPY,2018-06-01,2018-06-29,272.410000,271.280000,261.809262,256.809262,0.439889,5.00,0.0184,-0.1352,-0.0517,372.917227,67.117589,258.789500,1.149299,147.508632,1.000000
S4,SPY,2018-07-02,2018-07-31,269.510000,281.330000,260.100176,255.100176,0.778357,5.00,0.0186,-0.2077,-0.1062,516.909355,-121.417792,256.034500,1.881774,-1.626086,1.000000
S4,SPY,2018-08-01,2018-08-31,281.560000,290.310000,272.371188,267.371188,0.542161,5.00,0.0178,-0.1658,-0.0664,527.828973,-49.384272,267.482000,0.931263,-1.024062,1.000000
S4,SPY,2018-09-04,2018-09-28,289.840000,290.720000,281.740099,276.740099,0.599049,5.00,0.0173,-0.1840,-0.0723,546.707277,-28.587028,275.348000,1.066121,27.570249,1.000000
S4,SPY,2018-10-01,2018-10-31,292.110000,270.630000,281.292402,276.292402,0.458061,5.00,0.0171,-0.1406,-0.0569,433.024503,494.294514,277.504500,1.000405,1057.978867,1.000000
S4,SPY,2018-11-01,2018-11-30,271.600000,275.650000,253.965737,248.965737,0.655119,5.00,0.0184,-0.1539,-0.0948,397.794672,-382.122588,258.020000,4.633065,25.122084,1.000000
S4,SPY,2018-12-03,2018-12-31,280.280000,249.920000,262.426906,257.426906,0.379638,5.00,0.0178,-0.1010,-0.0504,254.110126,1429.766123,266.266000,2.920739,2193.326248,1.000000
S4,SPY,2019-01-02,2019-01-31,245.980000,269.930000,230.789299,225.789299,0.988702,5.00,0.0203,-0.2158,-0.1487,540.645360,-551.432932,233.681000,6.395156,-1.337572,1.000000
S4,SPY,2019-02-01,2019-02-28,270.150000,278.680000,257.291668,252.291668,0.631874,5.00,0.0185,-0.1646,-0.0872,278.416915,-216.473279,256.642500,2.766875,6.476835,1.000000
S4,SPY,2019-03-01,2019-03-29,280.440000,282.480000,268.241395,263.241395,0.463795,5.00,0.0178,-0.1353,-0.0595,295.252466,-98.170663,266.418000,1.592925,24.192332,1.000000
S4,SPY,2019-04-01,2019-04-30,284.700000,294.020000,271.849686,266.849686,0.438052,5.00,0.0176,-0.1278,-0.0564,251.527703,-122.923089,270.465000,1.568643,-0.414007,1.000000
S4,SPY,2019-05-01,2019-05-31,294.720000,275.270000,283.887959,278.887959,0.535469,5.00,0.0170,-0.1575,-0.0704,460.981948,198.626784,279.984000,1.241329,778.662838,1.000000
S4,SPY,2019-06-03,2019-06-28,275.310000,293.000000,263.715015,258.715015,0.622537,5.00,0.0182,-0.1679,-0.0837,392.330085,-186.293996,261.544500,2.375323,-1.565390,1.000000
S4,SPY,2019-07-01,2019-07-31,296.680000,297.430000,280.510549,275.510549,0.404069,5.00,0.0169,-0.1105,-0.0538,176.477614,-161.740878,281.846000,2.168845,24.186735,1.000000
S4,SPY,2019-08-01,2019-08-30,297.600000,292.450000,288.117158,283.117158,0.556861,5.00,0.0168,-0.1680,-0.0704,540.109867,223.485834,282.720000,0.957960,273.045701,1.000000
S4,SPY,2019-09-03,2019-09-30,290.570000,296.770000,277.649745,272.649745,0.814009,5.00,0.0172,-0.1974,-0.1190,445.008316,-262.324575,276.041500,3.655847,31.309263,1.000000
S4,SPY,2019-10-01,2019-10-31,297.740000,303.330000,284.293319,279.293319,0.568881,5.00,0.0168,-0.1508,-0.0777,305.452333,-164.149779,282.853000,2.183086,6.720656,1.000000
S4,SPY,2019-11-01,2019-11-29,304.920000,314.310000,293.133587,288.133587,0.461534,5.00,0.0164,-0.1348,-0.0573,427.332951,-92.423247,289.674000,1.275276,-1.598977,1.000000
S4,SPY,2019-12-02,2019-12-31,314.590000,321.860000,304.579294,299.579294,0.553705,5.00,0.0159,-0.1627,-0.0697,541.766660,-47.342327,298.860500,0.971371,3.874334,1.000000
S4,SPY,2020-01-02,2020-01-31,323.540000,321.730000,311.235562,306.235562,0.466522,5.00,0.0155,-0.1345,-0.0594,462.632587,2.032305,307.363000,1.220286,86.858663,1.000000
S4,SPY,2020-02-03,2020-02-28,323.350000,296.260000,308.995409,303.995409,0.524933,5.00,0.0155,-0.1385,-0.0708,371.386867,768.677124,307.182500,2.425893,1468.223124,1.000000
S4,SPY,2020-03-02,2020-03-31,298.210000,257.750000,275.193000,270.193000,0.663000,5.00,0.0168,-0.1440,-0.0975,605.468965,3113.318973,283.299500,6.717690,4228.237938,1.000000
S4,SPY,2020-04-01,2020-04-30,247.980000,290.480000,220.474696,215.474696,1.267147,5.00,0.0202,-0.2207,-0.1832,1702.773041,-1691.345765,235.581000,18.294877,20.877276,1.000000
S4,SPY,2020-05-01,2020-05-29,285.310000,304.320000,266.180456,261.180456,1.046826,5.00,0.0175,-0.2122,-0.1576,783.605211,-724.482304,271.044500,8.882878,68.572907,1.000000
S4,SPY,2020-06-01,2020-06-30,303.620000,308.360000,282.251473,277.251473,0.796741,5.00,0.0165,-0.1676,-0.1170,633.594566,-229.464929,288.439000,7.132687,413.579637,1.000000
S4,SPY,2020-07-01,2020-07-31,309.570000,326.520000,282.532463,277.532463,0.746657,5.00,0.0162,-0.1502,-0.1096,852.132723,-822.000632,294.091500,9.267985,39.582091,1.000000
S4,SPY,2020-08-03,2020-08-31,328.320000,349.310000,305.204007,300.204007,0.660624,5.00,0.0152,-0.1420,-0.0958,587.422460,-548.486435,311.904000,6.534848,48.386025,1.000000
S4,SPY,2020-09-01,2020-09-30,350.210000,334.890000,327.984694,322.984694,0.697598,5.00,0.0143,-0.1509,-0.1026,541.038310,251.369760,332.699500,6.107981,801.858070,1.000000
S4,SPY,2020-10-01,2020-10-30,337.690000,326.540000,311.905260,306.905260,0.637533,5.00,0.0148,-0.1345,-0.0930,652.735719,360.083371,320.805500,7.164890,1022.269090,1.000000
S4,SPY,2020-11-02,2020-11-30,330.200000,362.060000,299.176773,294.176773,0.665094,5.00,0.0151,-0.1326,-0.0974,1004.389473,-1010.280641,313.690000,10.708989,3.558832,1.000000
S4,SPY,2020-12-01,2020-12-31,365.570000,373.880000,341.077249,336.077249,0.571613,5.00,0.0137,-0.1253,-0.0827,499.076555,-386.152864,347.291500,5.562379,122.373691,1.000000
S4,SPY,2021-01-04,2021-01-29,375.310000,370.070000,353.942744,348.942744,0.649418,5.00,0.0133,-0.1444,-0.0949,491.161233,384.601711,356.544500,5.561030,885.212944,1.000000
S4,SPY,2021-02-01,2021-02-26,373.720000,380.360000,349.201416,344.201416,0.562193,5.00,0.0134,-0.1237,-0.0814,592.696117,-481.629213,355.034000,6.489154,120.516904,1.000000
S4,SPY,2021-03-01,2021-03-31,385.590000,396.330000,356.899058,351.899058,0.539081,5.00,0.0130,-0.1150,-0.0788,591.478449,-528.624458,366.310500,6.453866,72.303991,1.000000
S4,SPY,2021-04-01,2021-04-30,398.400000,417.300000,376.458495,371.458495,0.613381,5.00,0.0126,-0.1374,-0.0895,391.672587,-392.046191,378.480000,4.530107,9.076397,1.000000
S4,SPY,2021-05-03,2021-05-28,419.430000,420.040000,399.083186,394.083186,0.582724,5.00,0.0119,-0.1346,-0.0839,405.446756,-229.415347,398.458500,4.012506,123.012841,1.000000
S4,SPY,2021-06-01,2021-06-30,422.570000,428.060000,399.105923,394.105923,0.603363,5.00,0.0118,-0.1339,-0.0891,421.975787,-366.431822,401.441500,4.823121,64.993965,1.000000
S4,SPY,2021-07-01,2021-07-30,428.870000,438.510000,410.146937,405.146937,0.647359,5.00,0.0117,-0.1500,-0.0942,518.670313,-200.963782,407.426500,3.113626,55.112841,1.000000
S4,SPY,2021-08-02,2021-08-31,440.340000,451.560000,415.993875,410.993875,0.651874,5.00,0.0114,-0.1423,-0.0982,453.508045,-426.274727,418.323000,5.186955,36.683317,1.000000
S4,SPY,2021-09-01,2021-09-30,452.560000,429.140000,428.942740,423.942740,0.688300,5.00,0.0110,-0.1503,-0.1046,444.516604,653.399010,429.932000,5.133466,1107.365615,1.000000
S4,SPY,2021-10-01,2021-10-29,430.980000,459.250000,408.081481,403.081481,0.635255,5.00,0.0116,-0.1409,-0.0945,412.753124,-420.439846,409.431000,4.762786,1.763278,1.000000
S4,SPY,2021-11-01,2021-11-30,460.300000,455.560000,439.610205,434.610205,0.652538,5.00,0.0109,-0.1482,-0.0971,520.256086,261.285641,437.285000,3.529893,558.471193,1.000000
S4,SPY,2021-12-01,2021-12-31,461.640000,474.960000,432.702861,427.702861,0.486882,5.00,0.0108,-0.1070,-0.0720,458.420771,-437.228015,438.558000,5.071089,30.642756,1.000000
S4,SPY,2022-01-03,2022-01-31,476.300000,449.910000,453.126952,448.126952,0.661498,5.00,0.0105,-0.1465,-0.1003,451.127623,966.118849,452.485000,4.530822,1684.196472,1.000000
S4,SPY,2022-02-01,2022-02-28,450.680000,436.630000,414.284895,409.284895,0.797822,5.00,0.0111,-0.1557,-0.1246,1267.369460,-14.623511,428.146000,13.471517,1262.195948,1.000000
S4,SPY,2022-03-01,2022-03-31,435.040000,451.640000,401.391011,396.391011,0.875366,5.00,0.0115,-0.1711,-0.1376,1147.904863,-1115.329631,413.288000,12.354414,42.025232,1.000000
S4,SPY,2022-04-01,2022-04-29,453.310000,412.000000,428.700954,423.700954,0.663330,5.00,0.0110,-0.1459,-0.1020,473.294850,1598.926333,430.644500,5.396278,2581.671183,1.000000
S4,SPY,2022-05-02,2022-05-31,412.070000,412.930000,376.988295,371.988295,0.827685,5.00,0.0121,-0.1613,-0.1291,1195.850479,-797.250988,391.466500,12.786190,408.049491,1.000000
S4,SPY,2022-06-01,2022-06-30,415.170000,377.250000,382.901355,377.901355,0.718988,5.00,0.0120,-0.1465,-0.1120,917.991183,883.690231,394.411500,9.898899,2311.131414,1.000000
S4,SPY,2022-07-01,2022-07-29,376.560000,411.990000,351.710379,346.710379,0.805064,5.00,0.0133,-0.1706,-0.1264,716.084314,-711.584788,357.732000,7.965907,13.949526,1.000000
S4,SPY,2022-08-01,2022-08-31,409.150000,395.180000,385.726301,380.726301,0.896542,5.00,0.0122,-0.1925,-0.1462,635.154554,264.739075,388.692500,7.248088,909.343629,1.000000
S4,SPY,2022-09-01,2022-09-30,392.890000,357.180000,369.657983,364.657983,0.872902,5.00,0.0127,-0.1888,-0.1420,646.861744,704.888252,373.245500,7.341519,1861.199996,1.000000
S4,SPY,2022-10-03,2022-10-31,361.080000,386.210000,328.691654,323.691654,0.668081,5.00,0.0138,-0.1387,-0.1045,953.769771,-906.970881,343.026000,10.205778,56.248890,1.000000
S4,SPY,2022-11-01,2022-11-30,390.140000,407.680000,360.003981,355.003981,0.635231,5.00,0.0128,-0.1391,-0.1027,765.920354,-706.727058,370.633000,8.294435,68.643296,1.000000
S4,SPY,2022-12-01,2022-12-30,408.770000,382.430000,386.863579,381.863579,0.683877,5.00,0.0122,-0.1631,-0.1138,401.753897,208.785573,388.331500,4.701416,1063.347353,1.000000
S4,SPY,2023-01-03,2023-01-31,384.370000,406.480000,362.148640,357.148640,0.641830,5.00,0.0130,-0.1530,-0.1046,446.401980,-438.153671,365.151500,5.105850,17.698308,1.000000
S4,SPY,2023-02-01,2023-02-28,405.211000,396.260000,388.253417,383.253417,0.782811,5.00,0.0123,-0.1935,-0.1314,631.712174,205.078552,384.950450,3.796965,515.943985,1.000000
S4,SPY,2023-03-01,2023-03-31,395.410000,409.390000,375.244252,370.244252,0.782061,5.00,0.0126,-0.1858,-0.1325,406.634341,-378.629022,375.639500,4.848405,37.455319,1.000000
S4,SPY,2023-04-03,2023-04-28,408.850000,415.930000,390.469628,385.469628,0.746415,5.00,0.0122,-0.1823,-0.1244,566.959515,-269.175089,388.407500,4.353882,101.021639,1.000000
S4,SPY,2023-05-01,2023-05-31,415.470000,417.850000,396.523902,391.523902,0.747919,5.00,0.0120,-0.1854,-0.1290,485.425026,-205.445517,394.696500,3.774767,106.689265,1.000000
S4,SPY,2023-06-01,2023-06-30,418.090000,443.280000,398.288825,393.288825,0.713441,5.00,0.0120,-0.1770,-0.1228,434.723179,-336.470214,397.185500,3.957348,-2.629545,1.000000
S4,SPY,2023-07-03,2023-07-31,442.920000,457.790000,428.891146,423.891146,0.692349,5.00,0.0113,-0.1934,-0.1202,601.808797,-100.419496,420.774000,1.710437,10.839301,1.000000
S4,SPY,2023-08-01,2023-08-31,456.270000,450.350000,443.196233,438.196233,0.772175,5.00,0.0110,-0.2153,-0.1382,583.189270,16.258235,433.456500,1.604068,108.897505,1.000000
S4,SPY,2023-09-01,2023-09-29,453.170000,427.480000,434.229513,429.229513,0.538352,5.00,0.0110,-0.1485,-0.0934,547.682434,291.785387,430.511500,2.297163,977.116539,1.000000
S4,SPY,2023-10-02,2023-10-31,426.620000,418.200000,407.743783,402.743783,0.770135,5.00,0.0117,-0.1908,-0.1344,559.617032,77.366124,405.289000,3.911522,400.954831,1.000000
S4,SPY,2023-11-01,2023-11-30,419.200000,456.400000,397.051564,392.051564,0.693359,5.00,0.0119,-0.1683,-0.1193,416.071701,-428.632751,398.240000,4.854076,-3.111049,1.000000
S4,SPY,2023-12-01,2023-12-29,455.770000,475.310000,442.845986,437.845986,0.701143,5.00,0.0110,-0.2014,-0.1230,565.143039,-75.734325,432.981500,1.352574,-1.141286,1.000000
S4,SPY,2024-01-02,2024-01-31,472.160000,482.880000,460.597059,455.597059,0.888034,5.00,0.0106,-0.2432,-0.1600,569.741390,-67.917038,448.552000,1.585448,11.274353,1.000000
S4,SPY,2024-02-01,2024-02-29,484.630000,508.080000,467.810637,462.810637,0.574728,5.00,0.0103,-0.1633,-0.1014,609.422702,-119.900473,460.398500,1.668955,-1.027771,1.000000
S4,SPY,2024-03-01,2024-03-28,508.980000,523.070000,491.866208,486.866208,0.635735,5.00,0.0098,-0.1750,-0.1135,632.093285,-137.008830,483.531000,1.956668,4.534455,1.000000
S4,SPY,2024-04-01,2024-04-30,523.830000,501.980000,506.572547,501.572547,0.647630,5.00,0.0095,-0.1791,-0.1179,613.484465,6.269805,497.638500,1.782474,588.458999,1.000000
S4,SPY,2024-05-01,2024-05-31,501.380000,527.370000,483.048510,478.048510,0.744154,5.00,0.0100,-0.1930,-0.1351,700.777072,-211.656832,476.311000,2.751924,-1.429761,1.000000
S4,SPY,2024-06-03,2024-06-28,529.020000,544.220000,512.125639,507.125639,0.579157,5.00,0.0095,-0.1642,-0.1024,609.102532,-115.408386,502.569000,1.670182,3.144147,1.000000
S4,SPY,2024-07-01,2024-07-31,545.630000,550.810000,527.339776,522.339776,0.618597,5.00,0.0092,-0.1724,-0.1144,607.514910,-39.436943,518.348500,1.693746,77.527967,1.000000
S4,SPY,2024-08-01,2024-08-30,552.570000,563.680000,528.874906,523.874906,0.656024,5.00,0.0090,-0.1654,-0.1194,682.960082,-226.654270,524.941500,3.552219,72.415203,1.000000
S4,SPY,2024-09-03,2024-09-30,560.470000,573.760000,543.174857,538.174857,0.884651,5.00,0.0089,-0.2211,-0.1614,731.849817,-193.908898,532.446500,3.203149,47.390919,1.000000
S4,SPY,2024-10-01,2024-10-31,573.400000,568.640000,551.742498,546.742498,0.746271,5.00,0.0087,-0.1856,-0.1356,759.837110,33.854335,544.730000,3.344642,303.141445,1.000000
S4,SPY,2024-11-01,2024-11-29,571.320000,602.550000,541.190571,536.190571,0.666605,5.00,0.0088,-0.1549,-0.1180,533.679584,-544.167654,542.754000,6.003400,-1.038071,1.000000
S4,SPY,2024-12-02,2024-12-31,602.970000,586.080000,580.945711,575.945711,0.705611,5.00,0.0083,-0.1777,-0.1284,723.094223,129.961027,572.821500,2.936553,362.505250,1.000000
S4,SPY,2025-01-02,2025-01-31,589.390000,601.820000,564.818939,559.818939,0.579768,5.00,0.0085,-0.1475,-0.1036,727.949257,-133.737841,559.920500,2.960822,113.817547,1.000000
S4,SPY,2025-02-03,2025-02-28,592.670000,594.180000,578.876563,573.876563,1.214722,5.00,0.0084,-0.2845,-0.2203,780.082570,-58.830991,563.036500,4.015547,230.701579,1.000000
S4,SPY,2025-03-03,2025-03-31,596.180000,559.390000,565.909945,560.909945,0.693303,5.00,0.0084,-0.1597,-0.1229,537.615633,541.170938,566.371000,6.069459,1588.236571,1.000000
S4,SPY,2025-04-01,2025-04-30,557.450000,554.540000,533.919243,528.919243,0.833301,5.00,0.0090,-0.1946,-0.1484,863.015416,37.420430,529.577500,5.121712,475.711531,1.000000
S4,SPY,2025-05-01,2025-05-30,560.370000,589.390000,520.287470,515.287470,0.631728,5.00,0.0089,-0.1368,-0.1088,891.809614,-872.664038,532.351500,9.549825,28.595576,1.000000
S4,SPY,2025-06-02,2025-06-30,587.760000,617.850000,562.052942,557.052942,0.823601,5.00,0.0085,-0.1899,-0.1472,850.544699,-477.622114,558.372000,5.648106,14.278364,1.000000
S4,SPY,2025-07-01,2025-07-31,616.360000,632.080000,591.819783,586.819783,0.811012,5.00,0.0081,-0.1921,-0.1476,881.334034,-310.926483,585.542000,4.624352,79.857551,1.000000
S4,SPY,2025-08-01,2025-08-29,626.300000,645.050000,608.981261,603.981261,1.013339,5.00,0.0080,-0.2438,-0.1862,733.011487,-205.467464,594.985000,3.343453,36.994023,1.000000
S4,SPY,2025-09-02,2025-09-30,637.500000,666.180000,622.088167,617.088167,1.112386,5.00,0.0078,-0.2661,-0.2050,718.311851,-209.475819,605.625000,3.295504,18.286033,1.000000
S4,SPY,2025-10-01,2025-10-31,663.170000,682.060000,637.956840,632.956840,0.874262,5.00,0.0075,-0.2027,-0.1596,899.719400,-375.673628,630.011500,4.871456,33.495772,1.000000
S4,SPY,2025-11-03,2025-11-28,685.670000,683.390000,655.886968,650.886968,0.611595,5.00,0.0073,-0.1456,-0.1087,861.605510,4.956805,651.386500,4.727182,425.965483,1.000000
S4,SPY,2025-12-01,2025-12-31,678.810000,681.920000,647.722910,642.722910,0.935472,5.00,0.0074,-0.2042,-0.1689,985.138522,-656.358284,644.869500,7.933447,52.889204,1.000000
S4,SPY,2026-01-02,2026-01-30,685.710000,691.970000,659.131525,654.131525,0.571211,5.00,0.0073,-0.1429,-0.1021,727.747637,-99.819189,651.424500,2.848687,137.378447,1.000000
S4,SPY,2026-02-02,2026-02-27,689.580000,685.990000,665.400642,660.400642,0.843584,5.00,0.0073,-0.1963,-0.1512,918.352256,96.745613,655.101000,5.027107,524.547868,1.000000
S4,SPY,2026-03-02,2026-03-31,678.700000,650.340000,652.281689,647.281689,1.035255,5.00,0.0074,-0.2273,-0.1875,1114.740052,967.396335,644.765000,7.182656,1785.755262,1.000000
S4,SPY,2026-04-01,2026-04-30,653.900000,718.660000,605.787085,600.787085,0.742772,5.00,0.0076,-0.1522,-0.1283,1306.719448,-1317.636465,621.205000,13.809966,-1.467017,1.000000
S4,SPY,2026-05-01,2026-05-29,721.250000,756.480000,686.648131,681.648131,0.688681,5.00,0.0069,-0.1562,-0.1238,709.120101,-558.940679,685.187500,6.319251,13.566318,1.000000
S4,SPY,2026-06-01,2026-06-30,755.360000,746.770000,724.216015,719.216015,0.806791,5.00,0.0066,-0.1834,-0.1475,993.934825,-17.897430,717.592000,5.746139,485.487395,1.000000
S4,SPY,2026-07-01,2026-07-31,745.000000,747.030000,710.862241,705.862241,0.838871,5.00,0.0067,-0.1858,-0.1529,965.165687,-352.655008,707.750000,7.378287,310.736566,1.000000
S4,SPY,2026-08-03,2026-08-31,749.440000,767.050000,713.475403,708.475403,0.701944,5.00,0.0067,-0.1585,-0.1271,750.016324,-552.842045,711.968000,6.694704,55.883976,1.000000
S4,SPY,2026-09-01,2026-09-30,762.010000,762.630000,737.900600,732.900600,0.949548,5.00,0.0066,-0.2204,-0.1764,405.045188,88.654812,,,,0.000000
S4,QQQ,2001-04-02,2001-04-30,39.170000,46.149990,34.223598,29.223598,0.480668,5.00,0.1276,-0.1645,-0.0211,184.967866,-171.667424,37.211500,2.330347,22.750442,1.000000
S4,QQQ,2001-05-01,2001-05-31,46.200000,44.730000,40.087957,35.087957,0.552097,5.00,0.1082,-0.1631,-0.0336,232.172779,-93.366619,43.890000,2.873825,148.256161,1.000000
S4,QQQ,2001-06-01,2001-06-29,45.539990,45.700000,40.302853,35.302853,0.319163,5.00,0.1098,-0.1297,-0.0111,153.297949,-59.513777,43.262991,1.852142,103.234172,1.000000
S4,QQQ,2001-07-02,2001-07-31,45.651990,41.759990,40.981539,35.981539,0.454323,5.00,0.1095,-0.1678,-0.0201,148.742751,86.418756,43.369390,1.941751,244.611508,1.000000
S4,QQQ,2001-08-01,2001-08-31,42.636990,36.630000,37.050809,32.050809,0.344034,5.00,0.1173,-0.1292,-0.0129,172.114509,219.065464,40.505140,2.065179,442.710824,1.000000
S4,QQQ,2001-09-04,2001-09-28,36.518010,28.980000,33.023759,28.023759,0.374052,5.00,0.1369,-0.1716,-0.0081,130.527508,101.824443,34.692109,1.679327,646.177866,1.000000
S4,QQQ,2001-10-01,2001-10-31,28.850010,33.899990,24.308998,19.308998,0.516507,5.00,0.1733,-0.1680,-0.0169,190.322509,-177.508453,27.407509,2.419732,22.264056,1.000000
S4,QQQ,2001-11-01,2001-11-30,34.440000,39.649990,29.329373,24.329373,0.388727,5.00,0.1452,-0.1395,-0.0122,185.503820,-174.021675,32.718000,2.243765,20.932145,1.000000
S4,QQQ,2001-12-03,2001-12-31,39.289990,38.910000,35.098605,30.098605,0.495581,5.00,0.1273,-0.1801,-0.0192,154.423538,-70.572645,37.325491,2.039816,93.300893,1.000000
S4,QQQ,2002-01-02,2002-01-31,39.570010,38.509990,34.658764,29.658764,0.325571,5.00,0.1264,-0.1319,-0.0092,155.075464,6.704425,37.591510,1.876325,171.229889,1.000000
S4,QQQ,2002-02-01,2002-02-28,38.401000,33.780000,34.619997,29.619997,0.395468,5.00,0.1302,-0.1688,-0.0103,127.321290,91.412667,36.480950,1.668681,312.183609,1.000000
S4,QQQ,2002-03-01,2002-03-28,34.154010,36.060000,30.290533,25.290533,0.292733,5.00,0.1464,-0.1408,-0.0046,124.558967,-108.523960,32.446309,1.538323,25.485007,1.000000
S4,QQQ,2002-04-01,2002-04-30,35.800000,31.730000,32.796344,27.796344,0.362139,5.00,0.1397,-0.1815,-0.0057,86.977158,98.963948,34.010000,1.231910,302.025485,1.000000
S4,QQQ,2002-05-01,2002-05-31,31.670000,30.039990,28.451466,23.451466,0.337564,5.00,0.1579,-0.1669,-0.0046,100.261245,24.320264,30.086500,1.340176,134.031509,1.000000
S4,QQQ,2002-06-03,2002-06-28,30.008000,26.100010,27.211508,22.211508,0.285754,5.00,0.1666,-0.1652,-0.0020,94.364044,115.063830,28.507600,1.229394,330.027688,1.000000
S4,QQQ,2002-07-01,2002-07-31,25.978000,23.850010,22.585412,17.585412,0.389983,5.00,0.1925,-0.1694,-0.0058,126.451194,52.234757,24.679100,1.654495,188.135951,1.000000
S4,QQQ,2002-08-01,2002-08-30,23.740010,23.490010,20.400585,15.400585,0.389346,5.00,0.2106,-0.1685,-0.0049,133.598313,-51.073637,22.553010,1.725329,91.974676,1.000000
S4,QQQ,2002-09-03,2002-09-30,23.060000,20.720000,21.037587,16.037587,0.325811,5.00,0.2168,-0.2035,-0.0010,75.530030,57.293335,21.907000,1.081111,174.032079,1.000000
S4,QQQ,2002-10-01,2002-10-31,20.910000,24.550000,18.111114,13.111114,0.246340,5.00,0.2391,-0.1475,-0.0006,97.936558,-105.618817,19.864500,1.225705,1.767741,1.000000
S4,QQQ,2002-11-01,2002-11-29,24.378010,27.720000,22.170538,17.170538,0.267200,5.00,0.2051,-0.1789,-0.0006,69.833215,-80.895208,23.159109,0.965532,-1.611993,1.000000
S4,QQQ,2002-12-02,2002-12-31,28.420000,24.370000,25.521934,20.521934,0.123654,5.00,0.1759,-0.1026,-0.0001,65.672576,72.367998,26.999000,0.780380,262.683960,1.000000
S4,QQQ,2003-01-02,2003-01-31,24.720000,24.440000,22.016316,17.016316,0.184468,5.00,0.2023,-0.1320,-0.0003,76.586772,-2.043339,23.484000,0.950335,83.993433,1.000000
S4,QQQ,2003-02-03,2003-02-28,24.528000,25.160000,21.596091,16.596091,0.278859,5.00,0.2038,-0.1550,-0.0015,112.887358,-69.754047,23.301600,1.407733,52.583311,1.000000
S4,QQQ,2003-03-03,2003-03-31,25.270000,25.250000,22.419019,17.419019,0.261755,5.00,0.1979,-0.1533,-0.0012,94.892496,-57.771341,24.006500,1.210680,46.571155,1.000000
S4,QQQ,2003-04-01,2003-04-30,25.440000,27.450000,22.873741,17.873741,0.207516,5.00,0.1965,-0.1454,-0.0004,75.212189,-83.877003,24.168000,0.959638,0.785186,1.000000
S4,QQQ,2003-05-01,2003-05-30,27.440000,29.789990,25.628423,20.628423,0.175049,5.00,0.1822,-0.1642,-0.0000,36.881978,-47.425069,26.068000,0.543868,-1.093091,1.000000
S4,QQQ,2003-06-02,2003-06-30,30.080000,29.950000,27.760514,22.760514,0.151578,5.00,0.1662,-0.1329,-0.0001,49.426498,-13.415365,28.576000,0.645843,45.461133,1.000000
S4,QQQ,2003-07-01,2003-07-31,29.700000,31.800000,27.649392,22.649392,0.264824,5.00,0.1684,-0.1876,-0.0006,51.623207,-54.101391,28.215000,0.781056,6.971815,1.000000
S4,QQQ,2003-08-01,2003-08-29,31.690000,33.390000,29.520168,24.520168,0.236268,5.00,0.1578,-0.1734,-0.0005,51.180832,-50.946216,30.105500,0.748076,9.684615,1.000000
S4,QQQ,2003-09-02,2003-09-30,33.490010,32.420000,30.797533,25.797533,0.234314,5.00,0.1493,-0.1537,-0.0010,70.190948,28.514887,31.815509,0.936223,108.155835,1.000000
S4,QQQ,2003-10-01,2003-10-31,32.610000,35.179990,29.254425,24.254425,0.283926,5.00,0.1533,-0.1490,-0.0031,97.751354,-104.147199,30.979500,1.261439,3.054155,1.000000
S4,QQQ,2003-11-03,2003-11-28,35.429990,35.380000,32.584549,27.584549,0.210975,5.00,0.1411,-0.1414,-0.0009,75.507490,-35.190700,33.658490,0.966050,49.766790,1.000000
S4,QQQ,2003-12-01,2003-12-31,35.710010,36.460010,32.366921,27.366921,0.243882,5.00,0.1400,-0.1391,-0.0022,83.893250,-58.431699,33.924509,1.082815,34.911551,1.000000
S4,QQQ,2004-01-02,2004-01-30,36.660000,37.070010,33.295196,28.295196,0.276165,5.00,0.1364,-0.1482,-0.0032,93.550840,-68.573687,34.827000,1.211673,34.427153,1.000000
S4,QQQ,2004-02-02,2004-02-27,37.200000,36.570010,34.588153,29.588153,0.214925,5.00,0.1344,-0.1506,-0.0008,63.750279,-23.026762,35.340000,0.852428,50.173517,1.000000
S4,QQQ,2004-03-01,2004-03-31,36.679990,35.840000,33.977769,28.977769,0.230207,5.00,0.1363,-0.1531,-0.0011,56.989773,-15.269063,34.845990,0.800104,51.170710,1.000000
S4,QQQ,2004-04-01,2004-04-30,35.810000,34.770000,33.470180,28.470180,0.229456,5.00,0.1396,-0.1654,-0.0007,48.626669,-6.880719,34.019500,0.715723,51.195949,1.000000
S4,QQQ,2004-05-03,2004-05-28,35.000000,36.550000,32.827608,27.827608,0.147579,5.00,0.1429,-0.1372,-0.0001,41.942589,-43.643913,33.250000,0.567005,7.748677,1.000000
S4,QQQ,2004-06-01,2004-06-30,36.259990,37.740010,34.340582,29.340582,0.258927,5.00,0.1379,-0.1948,-0.0006,35.847206,-34.251430,34.446990,0.617399,11.045776,1.000000
S4,QQQ,2004-07-01,2004-07-30,37.660000,34.890000,35.447222,30.447222,0.229764,5.00,0.1328,-0.1718,-0.0006,39.824702,53.779284,35.777000,0.628011,158.776151,1.000000
S4,QQQ,2004-08-02,2004-08-31,34.610000,34.020000,32.572263,27.572263,0.269727,5.00,0.1445,-0.1926,-0.0008,41.675305,-5.719195,32.879500,0.686480,45.406109,1.000000
S4,QQQ,2004-09-01,2004-09-30,33.929990,35.140000,31.862129,26.862129,0.220303,5.00,0.1474,-0.1739,-0.0003,40.413276,-44.916635,32.233490,0.624435,4.946641,1.000000
S4,QQQ,2004-10-01,2004-10-29,35.450000,36.899990,32.937557,27.937557,0.164870,5.00,0.1410,-0.1349,-0.0002,48.278484,-51.784879,33.677500,0.647655,5.943605,1.000000
S4,QQQ,2004-11-01,2004-11-30,36.980000,39.121990,34.500360,29.500360,0.217231,5.00,0.1352,-0.1577,-0.0007,48.567415,-59.887867,35.131000,0.702905,-1.870451,1.000000
S4,QQQ,2004-12-01,2004-12-31,39.270000,39.914990,37.213098,32.213098,0.158150,5.00,0.1273,-0.1510,-0.0001,24.492667,-32.990859,37.306500,0.403077,0.951808,1.000000
S4,QQQ,2005-01-03,2005-01-31,40.080000,37.399990,38.184397,33.184397,0.138124,5.00,0.1248,-0.1479,-0.0000,30.034891,5.480806,38.076000,0.330076,112.566697,1.000000
S4,QQQ,2005-02-01,2005-02-28,37.470000,37.220000,35.537840,30.537840,0.165402,5.00,0.1334,-0.1595,-0.0001,28.898049,-21.815131,35.596500,0.454383,16.532918,1.000000
S4,QQQ,2005-03-01,2005-03-31,37.370000,36.570010,35.362099,30.362099,0.154669,5.00,0.1338,-0.1519,-0.0001,25.528820,-4.304763,35.501500,0.409957,30.674057,1.000000
S4,QQQ,2005-04-01,2005-04-29,36.820010,34.980000,34.773270,29.773270,0.135030,5.00,0.1358,-0.1400,-0.0000,26.928388,28.137754,34.979010,0.404314,64.516142,1.000000
S4,QQQ,2005-05-02,2005-05-31,35.070010,38.080000,33.237491,28.237491,0.152743,5.00,0.1426,-0.1586,-0.0000,23.056109,-35.631326,33.316510,0.383304,-3.125217,1.000000
S4,QQQ,2005-06-01,2005-06-30,38.030000,36.780000,36.640042,31.640042,0.145288,5.00,0.1315,-0.1818,-0.0000,58.307566,7.041112,36.128500,0.216821,23.644506,1.000000
S4,QQQ,2005-07-01,2005-07-29,36.860000,39.575000,35.388753,30.388753,0.120405,5.00,0.1356,-0.1611,-0.0000,46.643923,-22.057016,35.017000,0.215090,-3.138436,1.000000
S4,QQQ,2005-08-01,2005-08-31,39.640000,38.980000,38.176493,33.176493,0.124708,5.00,0.1261,-0.1668,-0.0000,57.050926,6.919928,37.658000,0.176724,21.571570,1.000000
S4,QQQ,2005-09-01,2005-09-30,38.990010,39.460010,37.158146,32.158146,0.174096,5.00,0.1282,-0.1719,-0.0001,31.203997,-28.210470,37.040509,0.368499,0.679849,1.000000
S4,QQQ,2005-10-03,2005-10-31,39.550000,38.870000,37.934560,32.934560,0.132549,5.00,0.1264,-0.1618,-0.0000,47.389752,7.546574,37.572500,0.244386,28.180332,1.000000
S4,QQQ,2005-11-01,2005-11-30,38.759990,41.240010,37.323635,32.323635,0.168320,5.00,0.1290,-0.1938,-0.0000,59.512499,-21.874155,36.821990,0.261801,-3.076128,1.000000
S4,QQQ,2005-12-01,2005-12-30,41.509990,40.412000,39.938633,34.938633,0.089403,5.00,0.1205,-0.1377,-0.0000,55.407125,-1.979120,39.434491,0.139332,12.463745,1.000000
S4,QQQ,2006-01-03,2006-01-31,40.640000,42.000000,39.027216,34.027216,0.101828,5.00,0.1230,-0.1440,-0.0000,50.651542,-14.827489,38.608000,0.189127,3.352419,1.000000
S4,QQQ,2006-02-01,2006-02-28,41.759990,41.100010,40.040025,35.040025,0.232345,5.00,0.1197,-0.2048,-0.0004,56.448690,-6.542206,39.671990,0.428796,22.552986,1.000000
S4,QQQ,2006-03-01,2006-03-31,41.220000,41.929990,39.226029,34.226029,0.165783,5.00,0.1213,-0.1636,-0.0002,26.228666,-27.654486,39.159000,0.361041,1.321315,1.000000
S4,QQQ,2006-04-03,2006-04-28,42.149990,41.850010,40.193894,35.193894,0.136244,5.00,0.1186,-0.1492,-0.0001,36.429901,-14.662965,40.042490,0.349140,16.076539,1.000000
S4,QQQ,2006-05-01,2006-05-31,41.929990,38.820010,40.001276,35.001276,0.169895,5.00,0.1192,-0.1695,-0.0002,33.299540,-20.663041,39.833490,0.335104,123.434549,1.000000
S4,QQQ,2006-06-01,2006-06-30,38.910000,38.770000,36.872591,31.872591,0.177757,5.00,0.1285,-0.1662,-0.0002,25.242076,-18.332754,36.964500,0.430178,16.359323,1.000000
S4,QQQ,2006-07-03,2006-07-31,38.880000,37.100010,36.757873,31.757873,0.181162,5.00,0.1286,-0.1638,-0.0003,29.682834,42.962909,36.936000,0.477990,82.095743,1.000000
S4,QQQ,2006-08-01,2006-08-31,36.789990,38.870000,35.294302,30.294302,0.234431,5.00,0.1359,-0.2203,-0.0002,48.915946,-25.646272,34.950491,0.379779,-1.661483,1.000000
S4,QQQ,2006-09-01,2006-09-29,39.070010,40.649990,37.080161,32.080161,0.146626,5.00,0.1280,-0.1539,-0.0001,22.224209,-29.757661,37.116509,0.368868,1.916547,1.000000
S4,QQQ,2006-10-02,2006-10-31,40.600010,42.580000,38.595110,33.595110,0.210444,5.00,0.1232,-0.1821,-0.0005,27.105710,-32.829468,38.570009,0.456400,1.216194,1.000000
S4,QQQ,2006-11-01,2006-11-30,42.730000,44.039990,40.362932,35.362932,0.196023,5.00,0.1170,-0.1618,-0.0007,33.912860,-32.774731,40.593500,0.535151,10.588129,1.000000
S4,QQQ,2006-12-01,2006-12-29,44.000000,43.160000,41.524410,36.524410,0.253733,5.00,0.1136,-0.1781,-0.0019,40.633000,-28.836082,41.800000,0.660063,21.246918,1.000000
S4,QQQ,2007-01-03,2007-01-31,43.460010,44.070010,41.032005,36.032005,0.165631,5.00,0.1150,-0.1466,-0.0004,32.009846,-33.562932,41.287009,0.485730,7.896914,1.000000
S4,QQQ,2007-02-01,2007-02-28,44.270000,43.330000,42.096010,37.096010,0.164140,5.00,0.1129,-0.1561,-0.0002,28.213125,28.290476,42.056500,0.406761,62.002565,1.000000
S4,QQQ,2007-03-01,2007-03-30,42.550000,43.530000,41.430949,36.430949,0.350576,5.00,0.1175,-0.2897,-0.0009,100.349148,-6.686885,40.422500,0.345618,2.267342,1.000000
S4,QQQ,2007-04-02,2007-04-30,43.670000,45.960010,41.768373,36.768373,0.152500,5.00,0.1145,-0.1630,-0.0001,43.269068,-27.285764,41.486500,0.303318,-2.753971,1.000000
S4,QQQ,2007-05-01,2007-05-31,45.970000,47.410000,44.230755,39.230755,0.170078,5.00,0.1088,-0.1818,-0.0001,64.403801,-18.091918,43.671500,0.254861,-0.163606,1.000000
S4,QQQ,2007-06-01,2007-06-29,47.580000,47.600010,45.523699,40.523699,0.159887,5.00,0.1051,-0.1603,-0.0002,47.954516,-15.767465,45.201000,0.316733,9.367116,1.000000
S4,QQQ,2007-07-02,2007-07-31,47.710010,47.530000,45.144705,40.144705,0.223598,5.00,0.1048,-0.1658,-0.0015,33.690851,-5.549796,45.324509,0.560507,37.591054,1.000000
S4,QQQ,2007-08-01,2007-08-31,47.390000,48.870000,45.220303,40.220303,0.250476,5.00,0.1055,-0.1917,-0.0014,42.940224,-24.057436,45.020500,0.480075,8.352483,1.000000
S4,QQQ,2007-09-04,2007-09-28,48.920000,51.410000,46.094135,41.094135,0.258386,5.00,0.1022,-0.1659,-0.0027,60.088086,-69.905666,46.474000,0.859267,-0.367580,1.000000
S4,QQQ,2007-10-01,2007-10-31,51.450000,55.030000,48.966851,43.966851,0.229575,5.00,0.0972,-0.1703,-0.0015,34.770447,-33.599038,48.877500,0.487928,1.686305,1.000000
S4,QQQ,2007-11-01,2007-11-30,54.679990,51.310000,52.014175,47.014175,0.348219,5.00,0.0914,-0.2001,-0.0066,45.211874,80.830765,51.945990,0.732154,199.091689,1.000000
S4,QQQ,2007-12-03,2007-12-31,51.140000,51.220000,47.194481,42.194481,0.412229,5.00,0.0978,-0.1757,-0.0151,104.916901,-74.784577,48.583000,1.461398,39.582323,1.000000
S4,QQQ,2008-01-02,2008-01-31,51.270000,45.130000,48.268379,43.268379,0.274477,5.00,0.0975,-0.1661,-0.0038,50.004603,0.093501,48.706500,0.774523,373.385967,1.000000
S4,QQQ,2008-02-01,2008-02-29,45.520000,42.950000,41.366500,36.366500,0.303829,5.00,0.1098,-0.1429,-0.0073,109.247351,24.922281,43.244000,1.396302,143.619632,1.000000
S4,QQQ,2008-03-03,2008-03-31,42.929990,43.720000,40.076753,35.076753,0.277475,5.00,0.1165,-0.1669,-0.0028,60.938647,-37.518039,40.783490,0.886861,32.870608,1.000000
S4,QQQ,2008-04-01,2008-04-30,44.450000,47.210010,40.225237,35.225237,0.234512,5.00,0.1125,-0.1211,-0.0038,103.542494,-108.102220,42.227500,1.269937,4.890274,1.000000
S4,QQQ,2008-05-01,2008-05-30,47.240010,50.009990,44.264728,39.264728,0.271934,5.00,0.1058,-0.1615,-0.0030,55.824309,-61.561491,44.878009,0.830177,3.712818,1.000000
S4,QQQ,2008-06-02,2008-06-30,49.920000,45.170000,46.891403,41.891403,0.307627,5.00,0.1002,-0.1717,-0.0048,59.476448,85.426581,47.424000,0.902391,326.493362,1.000000
S4,QQQ,2008-07-01,2008-07-31,44.860000,45.460010,41.810666,36.810666,0.370133,5.00,0.1115,-0.1856,-0.0074,73.905637,-43.313516,42.617000,1.109190,40.042122,1.000000
S4,QQQ,2008-08-01,2008-08-29,45.520000,46.120000,41.911944,36.911944,0.327483,5.00,0.1098,-0.1599,-0.0070,91.985521,-89.719887,43.244000,1.247338,11.715634,1.000000
S4,QQQ,2008-09-02,2008-09-30,46.860000,38.910000,43.259167,38.259167,0.172359,5.00,0.1067,-0.1131,-0.0013,69.144230,72.109458,44.517000,0.863801,585.620384,1.000000
S4,QQQ,2008-10-01,2008-10-31,38.830000,32.890000,35.455852,30.455852,0.345191,5.00,0.1288,-0.1669,-0.0062,93.566475,136.600657,36.888500,1.280856,496.202303,1.000000
S4,QQQ,2008-11-03,2008-11-28,32.810000,29.120000,28.428772,23.428772,0.462006,5.00,0.1524,-0.1644,-0.0144,192.245062,147.921578,31.169500,2.384457,349.616640,1.000000
S4,QQQ,2008-12-01,2008-12-31,28.500000,29.740010,25.053661,20.053661,0.523094,5.00,0.1754,-0.1940,-0.0135,140.519074,-121.025046,27.075000,1.928285,28.944028,1.000000
S4,QQQ,2009-01-02,2009-01-30,29.770000,29.060000,26.882543,21.882543,0.276186,5.00,0.1680,-0.1578,-0.0018,89.339622,-7.006752,28.281500,1.169582,91.782870,1.000000
S4,QQQ,2009-02-02,2009-02-27,28.770000,27.530000,26.386508,21.386508,0.311273,5.00,0.1738,-0.1852,-0.0016,83.236910,54.545910,27.331500,1.143642,147.232821,1.000000
S4,QQQ,2009-03-02,2009-03-31,27.120000,30.320010,24.503385,19.503385,0.375714,5.00,0.1844,-0.1914,-0.0035,91.475798,-91.224719,25.764000,1.290472,9.701080,1.000000
S4,QQQ,2009-04-01,2009-04-30,29.940000,34.280000,27.402236,22.402236,0.352321,5.00,0.1670,-0.1904,-0.0030,81.049961,-89.568910,28.443000,1.162820,0.931051,1.000000
S4,QQQ,2009-05-01,2009-05-29,34.280000,35.380000,31.269163,26.269163,0.290986,5.00,0.1459,-0.1602,-0.0027,86.844078,-80.176284,32.566000,1.159427,16.117794,1.000000
S4,QQQ,2009-06-01,2009-06-30,35.730000,36.380000,32.826473,27.826473,0.191286,5.00,0.1399,-0.1318,-0.0006,64.073710,-58.753964,33.943500,0.832024,14.769746,1.000000
S4,QQQ,2009-07-01,2009-07-31,36.539990,39.450000,34.014346,29.014346,0.197516,5.00,0.1368,-0.1458,-0.0005,49.098786,-59.220045,34.712991,0.688504,-0.671259,1.000000
S4,QQQ,2009-08-03,2009-08-31,39.850010,40.030000,37.001713,32.001713,0.171517,5.00,0.1255,-0.1265,-0.0005,54.753068,-25.735045,37.857509,0.719048,38.468023,1.000000
S4,QQQ,2009-09-01,2009-09-30,39.870000,42.250000,37.362231,32.362231,0.276411,5.00,0.1254,-0.1743,-0.0017,54.697381,-54.398785,37.876500,0.823385,9.748596,1.000000
S4,QQQ,2009-10-01,2009-10-30,42.110000,40.960010,39.313984,34.313984,0.297822,5.00,0.1187,-0.1712,-0.0029,61.665759,10.423237,40.004500,0.914479,81.538996,1.000000
S4,QQQ,2009-11-02,2009-11-30,41.009990,43.560000,38.294525,33.294525,0.241017,5.00,0.1219,-0.1560,-0.0013,60.611822,-70.291421,38.959491,0.847135,-0.229600,1.000000
S4,QQQ,2009-12-01,2009-12-31,43.880000,45.750000,41.174574,36.174574,0.173143,5.00,0.1139,-0.1315,-0.0004,42.024262,-51.950436,41.686000,0.593386,-0.476174,1.000000
S4,QQQ,2010-01-04,2010-01-29,46.320010,42.789990,43.507771,38.507771,0.128939,5.00,0.1079,-0.1091,-0.0002,44.547546,61.435409,44.004010,0.574415,187.211065,1.000000
S4,QQQ,2010-02-01,2010-02-26,42.910000,44.759990,40.081811,35.081811,0.233459,5.00,0.1165,-0.1504,-0.0014,69.529014,-71.092446,40.764500,0.928750,7.886568,1.000000
S4,QQQ,2010-03-01,2010-03-31,44.950000,48.160000,41.919824,36.919824,0.235262,5.00,0.1112,-0.1457,-0.0018,56.035091,-67.592471,42.702500,0.795613,-2.107380,1.000000
S4,QQQ,2010-04-01,2010-04-30,48.340000,49.237500,45.639654,40.639654,0.203808,5.00,0.1034,-0.1447,-0.0008,39.979057,-40.354120,45.923000,0.603599,9.074937,1.000000
S4,QQQ,2010-05-03,2010-05-28,49.429990,45.600010,46.633112,41.633112,0.209696,5.00,0.1012,-0.1442,-0.0011,51.028648,121.312034,46.958490,0.719982,285.100842,1.000000
S4,QQQ,2010-06-01,2010-06-30,45.450000,42.710010,41.286762,36.286762,0.425206,5.00,0.1100,-0.1680,-0.0145,131.098921,30.251953,43.177500,1.736196,170.800874,1.000000
S4,QQQ,2010-07-01,2010-07-30,42.820010,45.810000,39.399676,34.399676,0.295023,5.00,0.1168,-0.1530,-0.0044,83.939762,-92.370178,40.679009,1.134420,1.019584,1.000000
S4,QQQ,2010-08-02,2010-08-31,46.380000,43.460010,42.842060,37.842060,0.197377,5.00,0.1078,-0.1211,-0.0016,68.417044,46.480613,44.061000,0.881548,124.347657,1.000000
S4,QQQ,2010-09-01,2010-09-30,44.100010,49.070010,40.198503,35.198503,0.219185,5.00,0.1134,-0.1207,-0.0026,89.856688,-101.779526,41.895009,1.117752,-2.472837,1.000000
S4,QQQ,2010-10-01,2010-10-29,49.460010,52.179990,46.158238,41.158238,0.212510,5.00,0.1011,-0.1320,-0.0018,60.429303,-67.191545,46.987009,0.816803,2.687758,1.000000
S4,QQQ,2010-11-01,2010-11-30,52.380000,52.085010,49.131933,44.131933,0.249714,5.00,0.0955,-0.1460,-0.0028,56.098401,-30.326299,49.761000,0.810698,35.222102,1.000000
S4,QQQ,2010-12-01,2010-12-31,52.870000,54.460010,49.094620,44.094620,0.171853,5.00,0.0946,-0.1083,-0.0014,60.470321,-67.407851,50.226500,0.776557,2.512469,1.000000
S4,QQQ,2011-01-03,2011-01-31,54.959000,56.000000,51.632334,46.632334,0.188392,5.00,0.0910,-0.1236,-0.0013,49.913900,-53.161580,52.211050,0.687531,6.202320,1.000000
S4,QQQ,2011-02-01,2011-02-28,56.419400,57.768910,53.300835,48.300835,0.185789,5.00,0.0886,-0.1275,-0.0011,45.835039,-14.929308,53.598430,0.644139,40.355732,1.000000
S4,QQQ,2011-03-01,2011-03-31,57.990010,57.429990,53.431652,48.431652,0.358535,5.00,0.0862,-0.1492,-0.0126,109.131489,-69.941860,55.090509,1.449850,48.639628,1.000000
S4,QQQ,2011-04-01,2011-04-29,57.720000,59.080000,53.867528,48.867528,0.281627,5.00,0.0866,-0.1426,-0.0057,75.934782,-79.572965,54.834000,1.040975,5.811817,1.000000
S4,QQQ,2011-05-02,2011-05-31,59.190000,58.360000,56.163905,51.163905,0.247161,5.00,0.0845,-0.1517,-0.0025,39.118512,-2.933469,56.230500,0.638346,45.635042,1.000000
S4,QQQ,2011-06-01,2011-06-30,58.220000,57.050000,55.256721,50.256721,0.304043,5.00,0.0859,-0.1707,-0.0043,44.863635,21.438461,55.309000,0.752679,75.752095,1.000000
S4,QQQ,2011-07-01,2011-07-29,57.100010,58.000000,53.389098,48.389098,0.324747,5.00,0.0876,-0.1570,-0.0076,77.536091,-54.071342,54.245009,1.100108,32.914750,1.000000
S4,QQQ,2011-08-01,2011-08-31,58.670000,55.060000,54.272903,49.272903,0.247790,5.00,0.0852,-0.1232,-0.0053,81.692273,143.724933,55.736500,1.064713,234.867206,1.000000
S4,QQQ,2011-09-01,2011-09-30,55.210010,52.490010,49.846191,44.846191,0.442183,5.00,0.0906,-0.1538,-0.0217,162.131435,82.716903,52.449509,2.063497,254.298338,1.000000
S4,QQQ,2011-10-03,2011-10-31,52.039990,57.950000,47.567420,42.567420,0.510188,5.00,0.0961,-0.1809,-0.0242,145.443536,-153.273355,49.437990,1.964624,1.620181,1.000000
S4,QQQ,2011-11-01,2011-11-30,56.560000,56.390000,53.545173,48.545173,0.641209,5.00,0.0884,-0.2414,-0.0298,86.568134,-1.568850,53.732000,1.506890,94.449284,1.000000
S4,QQQ,2011-12-01,2011-12-30,56.370000,55.830000,51.689552,46.689552,0.423156,5.00,0.0887,-0.1610,-0.0179,127.443815,-108.307922,53.551500,1.697594,28.585892,1.000000
S4,QQQ,2012-01-03,2012-01-31,56.910000,60.530000,52.687481,47.687481,0.153692,5.00,0.0879,-0.0946,-0.0015,71.823805,-82.198177,54.064500,0.871930,-0.924372,1.000000
S4,QQQ,2012-02-01,2012-02-29,60.850010,64.410000,57.575139,52.575139,0.220455,5.00,0.0822,-0.1366,-0.0022,45.595017,-55.879687,57.807509,0.676405,-0.834670,1.000000
S4,QQQ,2012-03-01,2012-03-30,64.660000,67.550000,61.402747,56.402747,0.233750,5.00,0.0773,-0.1420,-0.0026,37.966278,-48.193691,61.427000,0.613412,-0.777413,1.000000
S4,QQQ,2012-04-02,2012-04-30,67.460010,66.759990,64.569311,59.569311,0.281696,5.00,0.0741,-0.1674,-0.0035,78.276216,9.053191,64.087009,0.582157,48.549280,1.000000
S4,QQQ,2012-05-01,2012-05-31,66.679990,62.060000,63.166468,58.166468,0.333806,5.00,0.0750,-0.1655,-0.0080,53.531128,155.273333,63.345990,0.869117,328.901237,1.000000
S4,QQQ,2012-06-01,2012-06-29,60.970000,64.160000,57.716669,52.716669,0.572899,5.00,0.0820,-0.2236,-0.0254,80.977653,-83.359276,57.921500,1.382675,7.068377,1.000000
S4,QQQ,2012-07-02,2012-07-31,64.230000,64.800000,60.130273,55.130273,0.349115,5.00,0.0778,-0.1564,-0.0109,80.041513,-70.958450,61.018500,1.149530,18.533063,1.000000
S4,QQQ,2012-08-01,2012-08-31,65.250000,68.160000,61.159995,56.159995,0.263500,5.00,0.0766,-0.1339,-0.0057,65.240047,-71.644034,61.987500,0.915900,3.046014,1.000000
S4,QQQ,2012-09-04,2012-09-28,68.030000,68.570010,64.985118,59.985118,0.305297,5.00,0.0735,-0.1700,-0.0050,86.616326,-32.841589,64.628500,0.814842,27.562950,1.000000
S4,QQQ,2012-10-01,2012-10-31,68.899990,64.950000,65.230995,60.230995,0.251256,5.00,0.0726,-0.1388,-0.0043,44.313238,85.655137,65.454990,0.694388,167.517907,1.000000
S4,QQQ,2012-11-01,2012-11-30,65.320010,65.800000,61.086869,56.086869,0.293108,5.00,0.0765,-0.1396,-0.0077,75.573796,-73.041272,62.054009,1.048846,11.982524,1.000000
S4,QQQ,2012-12-03,2012-12-31,66.320010,65.130100,62.524610,57.524610,0.222075,5.00,0.0754,-0.1267,-0.0033,53.443894,-17.500726,63.004009,0.756514,45.393168,1.000000
S4,QQQ,2013-01-02,2013-01-31,66.690000,66.870000,61.100821,56.100821,0.180275,5.00,0.0750,-0.0886,-0.0042,99.618439,-98.544721,63.355500,1.176460,10.523718,1.000000
S4,QQQ,2013-02-01,2013-02-28,67.340000,67.100010,64.032903,59.032903,0.188647,5.00,0.0743,-0.1251,-0.0015,42.222855,6.353407,63.973000,0.550972,52.035956,1.000000
S4,QQQ,2013-03-01,2013-03-28,66.860000,68.970000,63.120417,58.120417,0.390902,5.00,0.0748,-0.1745,-0.0127,75.034904,-84.894719,63.517000,1.141251,-0.409815,1.000000
S4,QQQ,2013-04-01,2013-04-30,69.009990,70.720000,65.959396,60.959396,0.263311,5.00,0.0725,-0.1573,-0.0033,69.345329,-36.254913,65.559490,0.556859,2.549897,1.000000
S4,QQQ,2013-05-01,2013-05-31,70.710010,73.250000,67.718830,62.718830,0.269683,5.00,0.0707,-0.1610,-0.0034,79.549298,-33.992659,67.174509,0.520856,0.574629,1.000000
S4,QQQ,2013-06-03,2013-06-28,73.310000,71.270000,70.254316,65.254316,0.257639,5.00,0.0682,-0.1556,-0.0032,95.213034,18.365644,69.644500,0.599954,62.047081,1.000000
S4,QQQ,2013-07-01,2013-07-31,71.759990,75.770000,67.602303,62.602303,0.257827,5.00,0.0697,-0.1316,-0.0058,56.200649,-68.707180,68.171990,0.819833,-3.056531,1.000000
S4,QQQ,2013-08-01,2013-08-30,76.300000,75.470000,73.172305,68.172305,0.158177,5.00,0.0655,-0.1172,-0.0008,84.850469,-1.560142,72.485000,0.319376,24.009782,1.000000
S4,QQQ,2013-09-03,2013-09-30,76.100010,78.880000,72.046232,67.046232,0.218357,5.00,0.0657,-0.1215,-0.0038,53.960325,-61.295346,72.295009,0.757960,2.114978,1.000000
S4,QQQ,2013-10-01,2013-10-31,78.870000,82.790000,75.498685,70.498685,0.300360,5.00,0.0634,-0.1608,-0.0060,87.947088,-42.284619,74.926500,0.607646,-2.106033,1.000000
S4,QQQ,2013-11-01,2013-11-29,83.040000,85.730000,79.536890,74.536890,0.250386,5.00,0.0602,-0.1430,-0.0041,93.343162,-38.688440,78.888000,0.534927,-0.784319,1.000000
S4,QQQ,2013-12-02,2013-12-31,85.830000,87.960000,82.402450,77.402450,0.277796,5.00,0.0583,-0.1535,-0.0052,109.777437,-31.147171,81.538500,0.511620,1.685218,1.000000
S4,QQQ,2014-01-02,2014-01-31,87.550000,86.270000,84.672418,79.672418,0.358224,5.00,0.0571,-0.1912,-0.0076,161.222132,48.791205,83.172500,0.470527,69.471563,1.000000
S4,QQQ,2014-02-03,2014-02-28,86.140000,90.340000,82.429990,77.429990,0.354376,5.00,0.0580,-0.1681,-0.0109,110.454573,-58.877785,81.833000,0.861932,1.327788,1.000000
S4,QQQ,2014-03-03,2014-03-31,89.480000,87.670000,86.715798,81.715798,0.469686,5.00,0.0559,-0.2217,-0.0147,184.866256,35.045641,85.006000,0.608550,58.382098,1.000000
S4,QQQ,2014-04-01,2014-04-30,88.100000,87.390000,83.543728,78.543728,0.297171,5.00,0.0568,-0.1374,-0.0098,58.596999,-13.375910,83.695000,0.883141,54.671089,1.000000
S4,QQQ,2014-05-01,2014-05-30,87.530000,91.310000,82.911501,77.911501,0.362473,5.00,0.0571,-0.1530,-0.0151,66.429420,-75.223421,83.153500,1.026767,0.655999,1.000000
S4,QQQ,2014-06-02,2014-06-30,91.430000,93.910000,87.233817,82.233817,0.333769,5.00,0.0547,-0.1534,-0.0114,85.301370,-50.428585,86.858500,0.811466,6.791131,1.000000
S4,QQQ,2014-07-01,2014-07-31,94.210000,95.020000,89.459302,84.459302,0.336623,5.00,0.0531,-0.1451,-0.0137,60.439611,-41.748744,89.499500,0.941019,28.140867,1.000000
S4,QQQ,2014-08-01,2014-08-29,94.830000,99.780000,90.863949,85.863949,0.384831,5.00,0.0527,-0.1709,-0.0147,119.181223,-54.027900,90.088500,0.801195,-2.941539,1.000000
S4,QQQ,2014-09-02,2014-09-30,100.040000,98.790000,96.329394,91.329394,0.262333,5.00,0.0500,-0.1432,-0.0055,150.214547,43.404772,95.038000,0.473085,73.929916,1.000000
S4,QQQ,2014-10-01,2014-10-31,98.540000,101.400000,93.791112,88.791112,0.449168,5.00,0.0507,-0.1718,-0.0245,83.236947,-67.417936,93.613000,1.103426,7.457821,1.000000
S4,QQQ,2014-11-03,2014-11-28,101.530000,106.010000,97.114667,92.114667,0.345189,5.00,0.0492,-0.1532,-0.0135,121.564831,-65.161763,96.453500,0.899671,-0.263592,1.000000
S4,QQQ,2014-12-01,2014-12-31,105.720000,103.250000,101.601525,96.601525,0.414963,5.00,0.0473,-0.1758,-0.0184,147.702939,26.271668,100.434000,0.724467,66.672074,1.000000
S4,QQQ,2015-01-02,2015-01-30,103.760000,101.100000,98.794746,93.794746,0.307420,5.00,0.0482,-0.1351,-0.0123,76.347605,73.591602,98.572000,0.848150,137.114617,1.000000
S4,QQQ,2015-02-02,2015-02-27,101.330000,108.400000,96.254620,91.254620,0.371527,5.00,0.0493,-0.1494,-0.0183,88.779212,-100.745559,96.263500,1.259319,-2.516347,1.000000
S4,QQQ,2015-03-02,2015-03-31,108.610000,105.600000,104.112074,99.112074,0.332709,5.00,0.0460,-0.1490,-0.0130,128.095428,50.349279,103.179500,0.681089,94.637265,1.000000
S4,QQQ,2015-04-01,2015-04-30,105.600000,107.630000,100.754863,95.754863,0.401255,5.00,0.0473,-0.1602,-0.0204,101.318278,-64.744218,100.320000,0.979575,2.537734,1.000000
S4,QQQ,2015-05-01,2015-05-29,108.050000,110.050000,103.510439,98.510439,0.292565,5.00,0.0463,-0.1376,-0.0100,121.937507,-38.469640,102.647500,0.649001,6.623981,1.000000
S4,QQQ,2015-06-01,2015-06-30,110.640000,107.070000,105.104383,100.104383,0.330870,5.00,0.0452,-0.1341,-0.0164,62.767155,27.527576,105.108000,0.958541,99.744731,1.000000
S4,QQQ,2015-07-01,2015-07-31,108.130000,111.950000,101.825235,96.825235,0.300501,5.00,0.0462,-0.1181,-0.0156,82.454566,-91.609375,102.723500,1.125046,0.295191,1.000000
S4,QQQ,2015-08-03,2015-08-31,111.970000,104.310000,107.094490,102.094490,0.397433,5.00,0.0447,-0.1593,-0.0205,125.229045,310.310602,106.371500,0.926734,651.139647,1.000000
S4,QQQ,2015-09-01,2015-09-30,101.710000,101.760000,94.639338,89.639338,0.924391,5.00,0.0492,-0.2268,-0.1011,283.595588,-126.433242,96.624500,3.760347,166.612346,1.000000
S4,QQQ,2015-10-01,2015-10-30,101.940000,113.330000,94.483018,89.483018,0.518343,5.00,0.0490,-0.1545,-0.0429,181.726428,-194.295256,96.843000,2.335607,-3.118828,1.000000
S4,QQQ,2015-11-02,2015-11-30,113.630000,114.020000,107.999228,102.999228,0.390658,5.00,0.0440,-0.1476,-0.0227,86.256621,-55.384707,107.948500,1.202496,35.249121,1.000000
S4,QQQ,2015-12-01,2015-12-31,114.475000,111.860000,108.506675,103.506675,0.383654,5.00,0.0437,-0.1424,-0.0233,79.268286,89.846139,108.751250,1.176337,178.564424,1.000000
S4,QQQ,2016-01-04,2016-01-29,109.430000,104.130000,106.704293,101.704293,0.860988,5.00,0.0457,-0.2941,-0.0636,306.928673,51.542418,103.958500,1.184482,350.771091,1.000000
S4,QQQ,2016-02-01,2016-02-29,103.620000,102.500000,97.125357,92.125357,0.587492,5.00,0.0483,-0.1778,-0.0496,159.306368,-82.035800,98.439000,2.180556,86.720568,1.000000
S4,QQQ,2016-03-01,2016-03-31,103.450000,109.200000,95.695502,90.695502,0.412462,5.00,0.0483,-0.1316,-0.0311,164.414720,-172.205073,98.277500,2.056609,1.659647,1.000000
S4,QQQ,2016-04-01,2016-04-29,108.580000,105.720000,103.781031,98.781031,0.526038,5.00,0.0460,-0.1888,-0.0346,133.321239,12.837943,103.151000,1.229219,92.606042,1.000000
S4,QQQ,2016-05-02,2016-05-31,105.970000,110.340000,100.719894,95.719894,0.379034,5.00,0.0472,-0.1497,-0.0201,70.509339,-71.210837,100.671500,1.035734,3.909114,1.000000
S4,QQQ,2016-06-01,2016-06-30,110.000000,107.540000,105.179510,100.179510,0.469446,5.00,0.0455,-0.1768,-0.0281,127.664417,81.261943,104.500000,1.066580,150.425357,1.000000
S4,QQQ,2016-07-01,2016-07-29,107.490000,115.230000,99.701748,94.701748,0.566546,5.00,0.0465,-0.1620,-0.0512,205.683684,-218.029759,102.115500,2.623383,-2.896075,1.000000
S4,QQQ,2016-08-01,2016-08-31,115.310000,116.440000,110.491714,105.491714,0.382079,5.00,0.0434,-0.1575,-0.0192,133.276637,-36.608259,109.544500,0.767631,11.396989,1.000000
S4,QQQ,2016-09-01,2016-09-30,116.480000,118.720000,111.569541,106.569541,0.395982,5.00,0.0429,-0.1595,-0.0210,136.212586,-51.564500,110.656000,0.844567,2.743956,1.000000
S4,QQQ,2016-10-03,2016-10-31,118.530000,116.990000,114.191851,109.191851,0.406059,5.00,0.0422,-0.1713,-0.0195,188.761383,24.409925,112.603500,0.705322,63.786249,1.000000
S4,QQQ,2016-11-01,2016-11-30,117.190000,117.500000,112.093744,107.093744,0.375838,5.00,0.0427,-0.1520,-0.0197,128.951239,-31.854474,111.330500,0.902107,30.222397,1.000000
S4,QQQ,2016-12-01,2016-12-30,117.460000,118.480000,112.891397,107.891397,0.390868,5.00,0.0426,-0.1644,-0.0193,163.396984,-25.649225,111.587000,0.720440,16.758039,1.000000
S4,QQQ,2017-01-03,2017-01-31,119.310000,124.570000,113.393543,108.393543,0.313878,5.00,0.0419,-0.1274,-0.0167,73.437193,-79.493017,113.344500,0.999207,-1.510151,1.000000
S4,QQQ,2017-02-01,2017-02-28,125.420000,130.020000,119.914408,114.914408,0.280777,5.00,0.0399,-0.1236,-0.0127,124.070391,-56.541289,119.149000,0.756073,0.438307,1.000000
S4,QQQ,2017-03-01,2017-03-31,130.810000,132.380000,124.749123,119.749123,0.328009,5.00,0.0382,-0.1301,-0.0189,100.821151,-62.727223,124.269500,0.856598,-0.418327,1.000000
S4,QQQ,2017-04-03,2017-04-28,132.480000,135.990000,128.476413,123.476413,0.320630,5.00,0.0377,-0.1583,-0.0114,273.475355,-23.516386,125.856000,0.434970,-2.632334,1.000000
S4,QQQ,2017-05-01,2017-05-31,136.460000,141.290000,132.134979,127.134979,0.268495,5.00,0.0366,-0.1386,-0.0089,252.201355,-14.529599,129.637000,0.292530,-2.676095,1.000000
S4,QQQ,2017-06-01,2017-06-30,141.570000,137.640000,136.862047,131.862047,0.334358,5.00,0.0353,-0.1511,-0.0158,248.765699,76.787204,134.491500,0.451468,97.948230,1.000000
S4,QQQ,2017-07-03,2017-07-31,138.250000,143.230000,131.198756,126.198756,0.416945,5.00,0.0362,-0.1430,-0.0329,95.013617,-93.363182,131.337500,1.367081,11.100435,1.000000
S4,QQQ,2017-08-01,2017-08-31,143.700000,146.200000,136.546627,131.546627,0.444141,5.00,0.0348,-0.1489,-0.0373,94.410063,-49.161978,136.515000,1.356614,51.535362,1.000000
S4,QQQ,2017-09-01,2017-09-29,146.360000,145.450000,138.533940,133.533940,0.520472,5.00,0.0342,-0.1587,-0.0495,134.312115,-103.933912,139.042000,1.863593,39.828203,1.000000
S4,QQQ,2017-10-02,2017-10-31,145.670000,152.150000,139.294338,134.294338,0.444799,5.00,0.0343,-0.1564,-0.0348,155.061448,-72.532434,138.386500,1.087576,1.195215,1.000000
S4,QQQ,2017-11-01,2017-11-30,152.750000,155.150000,145.333231,140.333231,0.434344,5.00,0.0327,-0.1450,-0.0371,114.655076,-61.960614,145.112500,1.360164,40.071401,1.000000
S4,QQQ,2017-12-01,2017-12-29,154.190000,155.760000,147.880307,142.880307,0.637490,5.00,0.0324,-0.1970,-0.0626,229.030873,-60.602543,146.480500,1.527991,37.897615,1.000000
S4,QQQ,2018-01-02,2018-01-31,156.500000,169.400000,148.108982,143.108982,0.459307,5.00,0.0319,-0.1438,-0.0436,126.183084,-128.867580,148.675000,1.721138,6.765504,1.000000
S4,QQQ,2018-02-01,2018-02-28,168.120000,167.210000,161.807642,156.807642,0.685250,5.00,0.0297,-0.2073,-0.0715,297.048612,-3.751981,159.714000,1.562094,93.382404,1.000000
S4,QQQ,2018-03-01,2018-03-29,167.290000,160.130000,158.955505,153.955505,0.547861,5.00,0.0299,-0.1636,-0.0575,134.531760,316.078075,158.925500,1.863174,457.059359,1.000000
S4,QQQ,2018-04-02,2018-04-30,159.000000,160.940000,150.203948,145.203948,0.723288,5.00,0.0314,-0.1921,-0.0857,211.839704,-156.724430,151.050000,2.841685,64.565274,1.000000
S4,QQQ,2018-05-01,2018-05-31,160.520000,170.070000,151.715454,146.715454,0.633019,5.00,0.0311,-0.1764,-0.0718,173.851215,-167.545987,152.494000,2.371531,15.755228,1.000000
S4,QQQ,2018-06-01,2018-06-29,170.880000,171.650000,162.234172,157.234172,0.459826,5.00,0.0293,-0.1446,-0.0461,116.611775,38.395312,162.336000,1.625944,164.457087,1.000000
S4,QQQ,2018-07-02,2018-07-31,170.040000,176.450000,162.181416,157.181416,0.762983,5.00,0.0294,-0.2081,-0.0915,220.252050,-152.592117,161.538000,2.322087,12.768334,1.000000
S4,QQQ,2018-08-01,2018-08-31,176.870000,186.650000,168.532723,163.532723,0.500970,5.00,0.0283,-0.1564,-0.0522,149.858949,-102.074045,168.026500,1.493336,6.612637,1.000000
S4,QQQ,2018-09-04,2018-09-28,186.100000,185.790000,177.832620,172.832620,0.627482,5.00,0.0269,-0.1815,-0.0715,267.701192,-41.069376,176.795000,2.266874,132.319772,1.000000
S4,QQQ,2018-10-01,2018-10-31,186.820000,169.820000,175.512886,170.512886,0.528433,5.00,0.0268,-0.1456,-0.0630,195.357631,431.556229,177.479000,2.482010,1136.363860,1.000000
S4,QQQ,2018-11-01,2018-11-30,170.080000,169.370000,154.561828,149.561828,0.717146,5.00,0.0294,-0.1608,-0.0943,505.181110,-389.393351,161.576000,5.768957,125.237759,1.000000
S4,QQQ,2018-12-03,2018-12-31,173.100000,154.260000,157.132944,152.132944,0.422080,5.00,0.0289,-0.1071,-0.0501,369.580419,909.926492,164.445000,4.117884,1576.251317,1.000000
S4,QQQ,2019-01-02,2019-01-31,150.990000,168.160000,138.298917,133.298917,0.992115,5.00,0.0331,-0.2124,-0.1340,555.002441,-560.492597,143.440500,6.542139,3.959844,1.000000
S4,QQQ,2019-02-01,2019-02-28,167.370000,173.190000,157.840547,152.840547,0.695511,5.00,0.0299,-0.1844,-0.0847,232.557008,-225.432935,159.001500,3.021081,16.574073,1.000000
S4,QQQ,2019-03-01,2019-03-29,174.410000,179.660000,164.909519,159.909519,0.443479,5.00,0.0287,-0.1374,-0.0466,136.018296,-127.322579,165.689500,1.803662,18.145717,1.000000
S4,QQQ,2019-04-01,2019-04-30,181.420000,189.540000,170.673144,165.673144,0.427100,5.00,0.0276,-0.1279,-0.0468,157.598666,-167.218943,172.349000,2.003086,-0.170278,1.000000
S4,QQQ,2019-05-01,2019-05-31,190.760000,173.950000,181.205088,176.205088,0.443528,5.00,0.0262,-0.1387,-0.0480,109.036249,296.835802,181.222000,1.533890,915.322051,1.000000
S4,QQQ,2019-06-03,2019-06-28,173.520000,186.740000,164.457244,159.457244,0.637544,5.00,0.0288,-0.1772,-0.0747,202.276123,-208.022440,164.844000,2.660306,3.703683,1.000000
S4,QQQ,2019-07-01,2019-07-31,190.300000,191.100000,175.661975,170.661975,0.384151,5.00,0.0263,-0.1045,-0.0448,253.892267,-207.676707,180.785000,2.923074,55.665560,1.000000
S4,QQQ,2019-08-01,2019-08-30,191.510000,187.470000,182.587506,177.587506,0.521471,5.00,0.0261,-0.1577,-0.0578,175.101619,153.777281,181.934500,1.619481,273.028279,1.000000
S4,QQQ,2019-09-03,2019-09-30,186.260000,188.810000,175.914568,170.914568,0.750487,5.00,0.0268,-0.1902,-0.0963,274.537999,-224.578011,176.947000,3.495867,59.409988,1.000000
S4,QQQ,2019-10-01,2019-10-31,189.540000,197.080000,179.240610,174.240610,0.527829,5.00,0.0264,-0.1499,-0.0608,162.722218,-169.436439,180.063000,2.155051,2.735779,1.000000
S4,QQQ,2019-11-01,2019-11-29,197.930000,205.100000,189.202339,184.202339,0.451736,5.00,0.0253,-0.1435,-0.0460,204.946127,-95.882273,188.033500,1.332359,1.629999,1.000000
S4,QQQ,2019-12-02,2019-12-31,205.110000,212.610000,196.984019,191.984019,0.542846,5.00,0.0244,-0.1670,-0.0586,287.613750,-79.921854,194.854500,1.289464,4.189997,1.000000
S4,QQQ,2020-01-02,2020-01-31,214.400000,219.070000,204.152894,199.152894,0.392947,5.00,0.0233,-0.1230,-0.0412,144.628867,-59.754039,203.680000,1.366342,47.035387,1.000000
S4,QQQ,2020-02-03,2020-02-28,220.140000,205.800000,208.029420,203.029420,0.536066,5.00,0.0227,-0.1437,-0.0656,233.814407,348.170512,209.133000,2.874210,814.376879,1.000000
S4,QQQ,2020-03-02,2020-03-31,208.880000,190.400000,188.390073,183.390073,0.580133,5.00,0.0239,-0.1274,-0.0774,583.255707,1628.161761,198.436000,6.412690,2220.867468,1.000000
S4,QQQ,2020-04-01,2020-04-30,184.810000,218.910000,162.803809,157.803809,1.150978,5.00,0.0271,-0.2057,-0.1580,1252.955686,-1251.258144,175.569500,13.680535,11.147542,1.000000
S4,QQQ,2020-05-01,2020-05-29,214.540000,233.360000,200.592304,195.592304,1.034291,5.00,0.0233,-0.2192,-0.1472,564.848073,-547.839112,203.813000,6.682772,26.458962,1.000000
S4,QQQ,2020-06-01,2020-06-30,232.400000,247.600000,216.588114,211.588114,0.782865,5.00,0.0215,-0.1735,-0.1077,458.777834,-344.494794,220.780000,5.370644,123.733040,1.000000
S4,QQQ,2020-07-01,2020-07-31,247.660000,265.790000,227.552265,222.552265,0.757616,5.00,0.0202,-0.1597,-0.1065,623.122025,-619.863021,235.277000,6.988837,12.709005,1.000000
S4,QQQ,2020-08-03,2020-08-31,268.050000,294.880000,248.396655,243.396655,0.591955,5.00,0.0187,-0.1328,-0.0806,476.788143,-465.513360,254.647500,5.359837,20.724783,1.000000
S4,QQQ,2020-09-01,2020-09-30,297.600000,277.840000,274.664804,269.664804,0.610859,5.00,0.0168,-0.1320,-0.0862,587.093562,803.650406,282.720000,6.481794,1400.193968,1.000000
S4,QQQ,2020-10-01,2020-10-30,281.790000,269.380000,249.183529,244.183529,0.694877,5.00,0.0177,-0.1324,-0.0986,1141.589977,376.903574,267.700500,12.110777,1527.943551,1.000000
S4,QQQ,2020-11-02,2020-11-30,271.730000,299.620000,237.384644,232.384644,0.795550,5.00,0.0184,-0.1451,-0.1125,1468.295296,-1436.516824,258.143500,15.478503,41.228473,1.000000
S4,QQQ,2020-12-01,2020-12-31,301.870000,313.740000,275.760587,270.760587,0.683557,5.00,0.0166,-0.1402,-0.0987,770.015229,-614.399790,286.776500,8.383710,165.065439,1.000000
S4,QQQ,2021-01-04,2021-01-29,315.110000,314.560000,291.397005,286.397005,0.697316,5.00,0.0159,-0.1469,-0.1014,741.202025,394.539319,299.354500,8.109336,1145.191344,1.000000
S4,QQQ,2021-02-01,2021-02-26,318.110000,314.140000,288.863102,283.863102,0.651678,5.00,0.0157,-0.1316,-0.0946,1013.119214,-547.111367,302.204500,10.782870,475.457847,1.000000
S4,QQQ,2021-03-01,2021-03-31,319.270000,319.130000,287.706885,282.706885,0.606098,5.00,0.0157,-0.1212,-0.0873,890.851115,-489.467533,303.306500,9.514610,410.833582,1.000000
S4,QQQ,2021-04-01,2021-04-30,323.070000,337.990000,294.852733,289.852733,0.615315,5.00,0.0155,-0.1267,-0.0888,778.018950,-654.281723,306.916500,8.395505,133.187227,1.000000
S4,QQQ,2021-05-03,2021-05-28,339.230000,333.930000,314.197710,309.197710,0.712776,5.00,0.0147,-0.1486,-0.1052,784.211248,-221.083916,322.268500,8.554888,572.577331,1.000000
S4,QQQ,2021-06-01,2021-06-30,335.300000,354.430000,307.049094,302.049094,0.741587,5.00,0.0149,-0.1490,-0.1100,901.294484,-865.733620,318.535000,9.754531,45.010864,1.000000
S4,QQQ,2021-07-01,2021-07-30,354.070000,364.570000,334.128165,329.128165,0.749549,5.00,0.0141,-0.1642,-0.1106,451.629386,-365.760483,336.366500,5.265843,95.318902,1.000000
S4,QQQ,2021-08-02,2021-08-31,366.280000,379.950000,341.007145,336.007145,0.683048,5.00,0.0137,-0.1443,-0.1015,624.943747,-611.897457,347.966000,6.932486,22.496290,1.000000
S4,QQQ,2021-09-01,2021-09-30,381.040000,357.960000,359.160949,354.160949,0.675632,5.00,0.0131,-0.1485,-0.0997,455.897592,677.288663,361.988000,5.234608,1262.731134,1.000000
S4,QQQ,2021-10-01,2021-10-29,358.600000,386.110000,339.209083,334.209083,0.677700,5.00,0.0139,-0.1525,-0.0981,389.673246,-391.714785,340.670000,4.574432,7.408461,1.000000
S4,QQQ,2021-11-01,2021-11-30,386.560000,393.820000,366.416169,361.416169,0.694300,5.00,0.0129,-0.1550,-0.1023,379.248183,61.418045,367.232000,4.486782,450.116228,1.000000
S4,QQQ,2021-12-01,2021-12-31,398.280000,397.850000,368.912280,363.912280,0.585290,5.00,0.0126,-0.1232,-0.0870,652.770299,-409.434751,378.366000,7.112993,252.785547,1.000000
S4,QQQ,2022-01-03,2022-01-31,399.050000,363.050000,373.978383,368.978383,0.701115,5.00,0.0125,-0.1490,-0.1057,603.972212,1550.013045,379.097500,6.740837,2663.435257,1.000000
S4,QQQ,2022-02-01,2022-02-28,364.430000,346.800000,324.101271,319.101271,0.833784,5.00,0.0137,-0.1528,-0.1246,1711.327441,157.064601,346.208500,17.947058,1877.842042,1.000000
S4,QQQ,2022-03-01,2022-03-31,345.750000,362.540000,307.951194,302.951194,0.912197,5.00,0.0145,-0.1664,-0.1365,1602.170867,-1469.056797,328.462500,16.933906,142.564070,1.000000
S4,QQQ,2022-04-01,2022-04-29,362.810000,313.250000,336.083939,331.083939,0.773638,5.00,0.0138,-0.1591,-0.1178,808.752752,2385.296971,344.669500,8.861165,3703.499723,1.000000
S4,QQQ,2022-05-02,2022-05-31,312.830000,308.280000,276.212519,271.212519,0.901129,5.00,0.0160,-0.1636,-0.1327,1577.362532,-837.101896,297.188500,16.674754,749.710636,1.000000
S4,QQQ,2022-06-01,2022-06-30,310.470000,280.280000,278.239527,273.239527,0.757205,5.00,0.0161,-0.1466,-0.1120,1150.517740,1010.040051,294.946500,12.262382,2170.007791,1.000000
S4,QQQ,2022-07-01,2022-07-29,278.950000,315.460000,255.873515,250.873515,0.857952,5.00,0.0179,-0.1757,-0.1285,837.483999,-827.494526,265.002500,9.232792,19.439473,1.000000
S4,QQQ,2022-08-01,2022-08-31,313.650000,299.270000,289.678354,284.678354,0.875456,5.00,0.0159,-0.1813,-0.1358,792.658355,355.194433,297.967500,8.802040,1157.302788,1.000000
S4,QQQ,2022-09-01,2022-09-30,296.720000,267.260000,274.525985,269.525985,0.910243,5.00,0.0169,-0.1898,-0.1411,779.943834,579.568817,281.884000,8.709681,1868.962651,1.000000
S4,QQQ,2022-10-03,2022-10-31,269.070000,277.950000,240.173616,235.173616,0.763151,5.00,0.0186,-0.1515,-0.1131,1062.114163,-882.156759,255.616500,11.384292,189.407404,1.000000
S4,QQQ,2022-11-01,2022-11-30,281.495000,293.360000,255.525957,250.525957,0.628763,5.00,0.0178,-0.1363,-0.0948,754.287811,-634.728105,267.420250,8.171641,129.009707,1.000000
S4,QQQ,2022-12-01,2022-12-30,293.690000,266.280000,274.883361,269.883361,0.715871,5.00,0.0170,-0.1679,-0.1113,448.398973,433.170276,279.005500,5.199861,1391.019249,1.000000
S4,QQQ,2023-01-03,2023-01-31,268.650000,294.620000,248.414351,243.414351,0.608485,5.00,0.0186,-0.1429,-0.0910,506.729241,-501.542173,255.217500,5.675777,14.637068,1.000000
S4,QQQ,2023-02-01,2023-02-28,294.410000,293.560000,277.027763,272.027763,0.734981,5.00,0.0170,-0.1755,-0.1147,432.114485,20.394075,279.689500,5.056126,461.958559,1.000000
S4,QQQ,2023-03-01,2023-03-31,293.260000,320.930000,272.049285,267.049285,0.782713,5.00,0.0170,-0.1749,-0.1239,601.184930,-594.860511,278.597000,6.794562,15.774418,1.000000
S4,QQQ,2023-04-03,2023-04-28,318.770000,322.560000,301.225224,296.225224,0.857971,5.00,0.0157,-0.1976,-0.1376,522.436186,-302.734430,302.831500,6.082333,229.151756,1.000000
S4,QQQ,2023-05-01,2023-05-31,322.090000,347.990000,302.389209,297.389209,0.770924,5.00,0.0155,-0.1800,-0.1256,467.723987,-469.035368,305.985500,5.448163,8.138619,1.000000
S4,QQQ,2023-06-01,2023-06-30,347.730000,369.420000,328.552678,323.552678,0.747907,5.00,0.0144,-0.1796,-0.1238,407.618550,-412.351055,330.343500,4.824093,4.717495,1.000000
S4,QQQ,2023-07-03,2023-07-31,370.070000,383.680000,352.362754,347.362754,0.669612,5.00,0.0135,-0.1710,-0.1113,364.002798,-218.976379,351.566500,3.513386,74.850999,1.000000
S4,QQQ,2023-08-01,2023-08-31,382.310000,377.990000,364.982967,359.982967,0.796607,5.00,0.0131,-0.1972,-0.1364,494.638386,-6.863154,363.194500,3.954523,318.378503,1.000000
S4,QQQ,2023-09-01,2023-09-29,380.400000,358.270000,356.723925,351.723925,0.638086,5.00,0.0131,-0.1521,-0.1063,488.455358,625.593001,361.380000,5.522640,1123.498360,1.000000
S4,QQQ,2023-10-02,2023-10-31,358.540000,350.870000,334.292470,329.292470,0.762269,5.00,0.0139,-0.1717,-0.1265,634.062052,-12.949242,340.613000,7.102890,630.562809,1.000000
S4,QQQ,2023-11-01,2023-11-30,351.720000,388.830000,326.437468,321.437468,0.743951,5.00,0.0142,-0.1659,-0.1224,695.712979,-707.975765,334.134000,7.701081,-2.812787,1.000000
S4,QQQ,2023-12-01,2023-12-29,387.750000,409.520000,373.743230,368.743230,0.750740,5.00,0.0129,-0.2004,-0.1272,667.369972,-173.795278,368.362500,2.424440,3.024694,1.000000
S4,QQQ,2024-01-02,2024-01-31,405.840000,416.970000,392.999279,387.999279,0.931671,5.00,0.0123,-0.2387,-0.1626,685.926809,-153.737948,385.548000,2.790939,41.638861,1.000000
S4,QQQ,2024-02-01,2024-02-29,418.790000,439.000000,399.505458,394.505458,0.609637,5.00,0.0119,-0.1588,-0.1038,420.925165,-249.979369,397.850500,3.163931,14.900045,1.000000
S4,QQQ,2024-03-01,2024-03-28,439.900000,444.010000,419.947234,414.947234,0.672651,5.00,0.0114,-0.1697,-0.1160,512.283455,-204.317085,417.905000,3.753252,113.193010,1.000000
S4,QQQ,2024-04-01,2024-04-30,444.970000,424.590000,423.424292,418.424292,0.686307,5.00,0.0112,-0.1698,-0.1195,413.614708,546.912287,422.721500,4.119662,899.697747,1.000000
S4,QQQ,2024-05-01,2024-05-31,423.150000,450.710000,402.294700,397.294700,0.815159,5.00,0.0118,-0.1935,-0.1419,456.076193,-430.646776,401.992500,5.073722,4.659441,1.000000
S4,QQQ,2024-06-03,2024-06-28,454.570000,479.110000,432.244772,427.244772,0.526233,5.00,0.0110,-0.1362,-0.0892,353.880495,-310.700772,431.841500,3.661766,12.302545,1.000000
S4,QQQ,2024-07-01,2024-07-31,480.040000,471.070000,457.546270,452.546270,0.694216,5.00,0.0104,-0.1719,-0.1235,482.578084,300.846124,456.038000,4.011727,642.047224,1.000000
S4,QQQ,2024-08-01,2024-08-30,471.760000,476.270000,441.434120,436.434120,0.765827,5.00,0.0106,-0.1694,-0.1326,754.004067,-405.633715,448.172000,8.305867,357.820353,1.000000
S4,QQQ,2024-09-03,2024-09-30,473.200000,488.070000,450.063921,445.063921,0.895331,5.00,0.0106,-0.2030,-0.1564,661.482679,-456.892163,449.540000,6.986236,161.648382,1.000000
S4,QQQ,2024-10-01,2024-10-31,487.700000,483.850000,460.270532,455.270532,0.789468,5.00,0.0103,-0.1777,-0.1373,625.722938,16.956482,463.315000,7.046698,652.129419,1.000000
S4,QQQ,2024-11-01,2024-11-29,485.500000,509.740000,451.450761,446.450761,0.748961,5.00,0.0103,-0.1604,-0.1273,919.310456,-900.653908,461.225000,9.942065,28.106549,1.000000
S4,QQQ,2024-12-02,2024-12-31,511.010000,511.230000,483.418049,478.418049,0.714278,5.00,0.0098,-0.1646,-0.1245,530.485451,-280.937189,485.459500,6.019133,258.998262,1.000000
S4,QQQ,2025-01-02,2025-01-31,514.300000,522.290000,485.432063,480.432063,0.643114,5.00,0.0097,-0.1494,-0.1113,512.128467,-157.533379,488.585000,5.764399,364.045087,1.000000
S4,QQQ,2025-02-03,2025-02-28,513.470000,508.170000,494.210357,489.210357,1.152215,5.00,0.0097,-0.2535,-0.2027,1140.598250,-2.568110,487.796500,7.558197,647.480140,1.000000
S4,QQQ,2025-03-03,2025-03-31,511.520000,468.920000,473.570125,468.570125,0.709109,5.00,0.0098,-0.1499,-0.1201,1011.145715,935.275455,485.944000,10.820566,2420.883684,1.000000
S4,QQQ,2025-04-01,2025-04-30,467.300000,475.470000,439.533090,434.533090,0.847281,5.00,0.0107,-0.1847,-0.1449,757.457942,-457.439587,443.935000,8.421860,309.468355,1.000000
S4,QQQ,2025-05-01,2025-05-30,483.410000,519.110000,441.611421,436.611421,0.586075,5.00,0.0103,-0.1237,-0.0973,1021.378273,-1008.793814,459.239500,10.799857,22.034459,1.000000
S4,QQQ,2025-06-02,2025-06-30,517.240000,551.640000,491.504647,486.504647,0.842271,5.00,0.0097,-0.1897,-0.1470,599.134085,-583.084547,491.378000,6.706965,12.834795,1.000000
S4,QQQ,2025-07-01,2025-07-31,549.730000,565.010000,525.626209,520.626209,0.834771,5.00,0.0091,-0.1940,-0.1488,792.202066,-332.116795,522.243500,5.374083,131.264373,1.000000
S4,QQQ,2025-08-01,2025-08-29,558.830000,570.400000,540.653456,535.653456,1.035365,5.00,0.0089,-0.2416,-0.1864,849.153430,-199.106524,530.888500,4.526899,159.496906,1.000000
S4,QQQ,2025-09-02,2025-09-30,561.310000,600.370000,545.341077,540.341077,1.186127,5.00,0.0089,-0.2722,-0.2142,873.397874,-363.415392,533.244500,4.920106,19.432482,1.000000
S4,QQQ,2025-10-01,2025-10-31,597.170000,629.070000,568.796816,563.796816,0.893015,5.00,0.0084,-0.1978,-0.1591,779.696297,-596.745743,567.311500,7.204663,43.869000,1.000000
S4,QQQ,2025-11-03,2025-11-28,635.110000,619.250000,596.748680,591.748680,0.597559,5.00,0.0079,-0.1325,-0.1036,793.373438,492.324079,603.354500,8.531293,1295.147517,1.000000
S4,QQQ,2025-12-01,2025-12-31,613.630000,614.310000,574.411038,569.411038,0.979590,5.00,0.0081,-0.1990,-0.1706,1279.888512,-1080.669161,582.948500,13.778475,208.669351,1.000000
S4,QQQ,2026-01-02,2026-01-30,620.060000,621.870000,584.629303,579.629303,0.582749,5.00,0.0081,-0.1324,-0.1013,596.155030,-138.890382,589.057000,6.544299,466.714649,1.000000
S4,QQQ,2026-02-02,2026-02-27,618.700000,607.290000,588.241756,583.241756,0.892533,5.00,0.0081,-0.1927,-0.1563,923.856936,374.323499,587.765000,9.654346,1259.954839,1.000000
S4,QQQ,2026-03-02,2026-03-31,598.860000,577.180000,565.859132,560.859132,1.066311,5.00,0.0083,-0.2192,-0.1867,1131.580968,830.839543,568.917000,12.382121,1971.870512,1.000000
S4,QQQ,2026-04-01,2026-04-30,581.480000,667.740000,526.506381,521.506381,0.772997,5.00,0.0086,-0.1494,-0.1284,1832.124736,-1842.581724,552.406000,19.094244,-1.006988,1.000000
S4,QQQ,2026-05-01,2026-05-29,669.160000,738.310000,629.279032,624.279032,0.762694,5.00,0.0075,-0.1626,-0.1341,949.287451,-953.937758,635.702000,10.255568,4.799693,1.000000
S4,QQQ,2026-06-01,2026-06-30,737.040000,736.400000,697.109964,692.109964,0.838702,5.00,0.0068,-0.1787,-0.1503,941.474415,325.697238,700.188000,10.253446,1276.621653,1.000000
S4,QQQ,2026-07-01,2026-07-31,729.190000,687.990000,679.609587,674.609587,1.004258,5.00,0.0069,-0.1985,-0.1759,1760.094504,1298.979601,692.730500,18.605203,3068.524105,1.000000
S4,QQQ,2026-08-03,2026-08-31,688.300000,716.760000,629.883957,624.883957,0.860585,5.00,0.0073,-0.1663,-0.1465,2058.570527,-1648.682140,653.885000,21.446291,419.338386,1.000000
S4,QQQ,2026-09-01,2026-09-30,707.390000,739.770000,665.760716,660.760716,1.060492,5.00,0.0071,-0.2137,-0.1874,393.950781,99.749219,,,,0.000000
S4,IWM,2001-04-02,2001-04-30,44.775000,48.500000,41.674331,36.674331,0.308351,5.00,0.1117,-0.1720,-0.0052,68.294242,-71.965098,42.536250,0.991294,5.779145,1.000000
S4,IWM,2001-05-01,2001-05-31,48.324995,49.550005,45.062164,40.062164,0.358696,5.00,0.1035,-0.1811,-0.0087,71.258626,-70.541087,45.908745,1.071282,10.167538,1.000000
S4,IWM,2001-06-01,2001-06-29,49.875000,50.949995,47.025636,42.025636,0.195526,5.00,0.1003,-0.1443,-0.0012,39.601231,-29.265597,47.381250,0.591538,19.785634,1.000000
S4,IWM,2001-07-02,2001-07-31,50.800005,48.115000,47.880308,42.880308,0.318213,5.00,0.0984,-0.1813,-0.0055,50.834596,61.752227,48.260005,0.826559,122.036823,1.000000
S4,IWM,2001-08-01,2001-08-31,48.525000,46.945000,44.766103,39.766103,0.263844,5.00,0.1030,-0.1432,-0.0050,76.349812,10.094223,46.098750,1.027342,95.894035,1.000000
S4,IWM,2001-09-04,2001-09-28,46.850000,40.100000,44.101571,39.101571,0.287099,5.00,0.1067,-0.1757,-0.0033,64.696631,6.083059,44.507500,0.934065,480.386755,1.000000
S4,IWM,2001-10-01,2001-10-31,40.100000,42.550005,36.188349,31.188349,0.380365,5.00,0.1247,-0.1642,-0.0104,114.208531,-104.387421,38.095000,1.522450,19.271110,1.000000
S4,IWM,2001-11-01,2001-11-30,42.670000,45.800005,39.199013,34.199013,0.303712,5.00,0.1172,-0.1568,-0.0053,84.968853,-88.327877,40.536500,1.153400,6.090977,1.000000
S4,IWM,2001-12-03,2001-12-31,45.449995,48.175005,42.860613,37.860613,0.338047,5.00,0.1100,-0.1934,-0.0044,53.045805,-58.003835,43.177495,0.868505,4.491970,1.000000
S4,IWM,2002-01-02,2002-01-31,48.550005,48.100000,44.919615,39.919615,0.253233,5.00,0.1030,-0.1400,-0.0039,75.433924,-7.595241,46.122505,1.007572,77.288683,1.000000
S4,IWM,2002-02-01,2002-02-28,47.750000,46.600000,45.037570,40.037570,0.347374,5.00,0.1047,-0.1916,-0.0053,58.097828,3.442052,45.362500,0.928353,70.989880,1.000000
S4,IWM,2002-03-01,2002-03-28,46.824995,50.050005,43.676526,38.676526,0.242331,5.00,0.1068,-0.1478,-0.0025,64.246914,-75.489413,44.483745,0.884800,-1.792500,1.000000
S4,IWM,2002-04-01,2002-04-30,50.050005,50.650000,47.499662,42.499662,0.239134,5.00,0.0999,-0.1663,-0.0015,33.752264,-16.507588,47.547505,0.576656,26.694676,1.000000
S4,IWM,2002-05-01,2002-05-31,50.750000,48.250000,47.664663,42.664663,0.265074,5.00,0.0985,-0.1579,-0.0033,51.716153,37.545612,48.212500,0.782236,98.711766,1.000000
S4,IWM,2002-06-03,2002-06-28,48.475000,45.324995,45.743570,40.743570,0.200763,5.00,0.1031,-0.1455,-0.0009,47.319613,76.274846,46.051250,0.673959,174.901983,1.000000
S4,IWM,2002-07-01,2002-07-31,45.449995,39.275000,42.125027,37.125027,0.284789,5.00,0.1100,-0.1557,-0.0043,69.652861,50.525278,43.177495,0.981318,414.630791,1.000000
S4,IWM,2002-08-01,2002-08-30,39.150000,39.025000,35.912604,30.912604,0.344966,5.00,0.1277,-0.1717,-0.0060,88.126721,-20.859713,37.192500,1.226233,76.717008,1.000000
S4,IWM,2002-09-03,2002-09-30,38.324995,35.775000,36.252025,31.252025,0.396484,5.00,0.1305,-0.2272,-0.0041,54.272815,43.447715,36.408745,0.939213,154.873048,1.000000
S4,IWM,2002-10-01,2002-10-31,36.250000,37.250000,32.368653,27.368653,0.267419,5.00,0.1379,-0.1347,-0.0039,108.993326,-82.354965,34.437500,1.357352,36.088361,1.000000
S4,IWM,2002-11-01,2002-11-29,37.135000,40.405000,34.386522,29.386522,0.294666,5.00,0.1346,-0.1725,-0.0027,69.650867,-80.459478,35.278250,0.991174,-1.358612,1.000000
S4,IWM,2002-12-02,2002-12-31,41.250000,37.905000,37.868932,32.868932,0.133115,5.00,0.1212,-0.0999,-0.0004,60.074060,110.081963,39.187500,0.733856,179.606022,1.000000
S4,IWM,2003-01-02,2003-01-31,38.250000,37.120005,35.167003,30.167003,0.211526,5.00,0.1307,-0.1364,-0.0012,67.673474,8.151833,36.337500,0.888261,85.275307,1.000000
S4,IWM,2003-02-03,2003-02-28,37.199995,36.004995,34.289142,29.289142,0.258978,5.00,0.1344,-0.1561,-0.0020,81.453346,-11.059332,35.339995,1.073512,79.844014,1.000000
S4,IWM,2003-03-03,2003-03-31,36.250000,36.000000,33.320045,28.320045,0.221156,5.00,0.1379,-0.1432,-0.0012,69.689597,-54.878907,34.437500,0.918052,24.260690,1.000000
S4,IWM,2003-04-01,2003-04-30,36.350000,39.699995,33.848243,28.848243,0.153011,5.00,0.1376,-0.1294,-0.0002,45.192233,-57.623918,34.532500,0.604933,-2.981686,1.000000
S4,IWM,2003-05-01,2003-05-30,39.750000,44.015000,37.921136,32.921136,0.156701,5.00,0.1258,-0.1581,-0.0000,34.327576,-31.040828,37.762500,0.341341,-3.126813,1.000000
S4,IWM,2003-06-02,2003-06-30,44.375000,44.449995,42.029718,37.029718,0.132855,5.00,0.1127,-0.1261,-0.0001,26.967850,-12.538914,42.156250,0.402534,23.878936,1.000000
S4,IWM,2003-07-01,2003-07-31,44.405000,47.339995,41.864047,36.864047,0.248889,5.00,0.1126,-0.1668,-0.0014,44.016343,-51.729795,42.184750,0.689052,1.736548,1.000000
S4,IWM,2003-08-01,2003-08-29,47.375000,49.605005,44.602966,39.602966,0.249649,5.00,0.1055,-0.1600,-0.0019,49.009526,-50.979846,45.006250,0.739744,7.479680,1.000000
S4,IWM,2003-09-02,2003-09-30,49.875000,48.525000,46.347674,41.347674,0.264071,5.00,0.1003,-0.1446,-0.0040,76.440243,36.813022,47.381250,1.028473,122.703264,1.000000
S4,IWM,2003-10-01,2003-10-31,48.685000,52.750000,44.503437,39.503437,0.351626,5.00,0.1027,-0.1534,-0.0102,107.480104,-114.786896,46.250750,1.426427,2.143209,1.000000
S4,IWM,2003-11-03,2003-11-28,53.095000,54.725000,49.340784,44.340784,0.265668,5.00,0.0942,-0.1405,-0.0047,87.393830,-64.525974,50.440250,1.139606,32.317856,1.000000
S4,IWM,2003-12-01,2003-12-31,54.935000,55.400000,50.498574,45.498574,0.356406,5.00,0.0910,-0.1514,-0.0121,104.556163,-48.037538,52.188250,1.401967,65.968625,1.000000
S4,IWM,2004-01-02,2004-01-30,55.583505,57.800005,50.685895,45.685895,0.399725,5.00,0.0900,-0.1533,-0.0170,137.624145,-121.205973,52.804330,1.775967,25.868172,1.000000
S4,IWM,2004-02-02,2004-02-27,57.920000,58.350000,54.045918,49.045918,0.324937,5.00,0.0863,-0.1550,-0.0084,93.005775,-43.112859,55.024000,1.254994,59.342916,1.000000
S4,IWM,2004-03-01,2004-03-31,58.501000,58.800005,53.848400,48.848400,0.384191,5.00,0.0855,-0.1549,-0.0154,110.587561,-69.119255,55.575950,1.490066,50.918306,1.000000
S4,IWM,2004-04-01,2004-04-30,58.790000,55.555000,54.528838,49.528838,0.387639,5.00,0.0850,-0.1628,-0.0143,101.209807,53.908036,55.850500,1.399738,164.567843,1.000000
S4,IWM,2004-05-03,2004-05-28,55.800005,56.750000,52.249891,47.249891,0.268213,5.00,0.0896,-0.1463,-0.0045,75.505314,-46.084861,53.010005,1.023266,38.870453,1.000000
S4,IWM,2004-06-01,2004-06-30,56.500000,58.995005,53.059081,48.059081,0.378538,5.00,0.0885,-0.1787,-0.0103,73.063163,-59.003262,53.675000,1.109170,23.509900,1.000000
S4,IWM,2004-07-01,2004-07-30,58.910005,55.000000,55.098636,50.098636,0.368908,5.00,0.0849,-0.1684,-0.0115,78.741039,142.298130,55.964505,1.156318,240.352811,1.000000
S4,IWM,2004-08-02,2004-08-31,54.600000,54.705000,50.961466,45.961466,0.434815,5.00,0.0916,-0.1866,-0.0153,87.025713,-48.938579,51.870000,1.305072,47.537135,1.000000
S4,IWM,2004-09-01,2004-09-30,54.545000,56.925005,51.218955,46.218955,0.348928,5.00,0.0917,-0.1749,-0.0081,66.396702,-68.722877,51.817750,1.012895,7.123825,1.000000
S4,IWM,2004-10-01,2004-10-29,57.285005,58.095000,53.442188,48.442188,0.271150,5.00,0.0873,-0.1425,-0.0056,72.721768,-58.810042,54.420755,0.998368,23.361726,1.000000
S4,IWM,2004-11-01,2004-11-30,58.269995,63.440000,54.428176,49.428176,0.313379,5.00,0.0858,-0.1548,-0.0081,73.191050,-85.493049,55.356495,1.045290,-2.851999,1.000000
S4,IWM,2004-12-01,2004-12-31,63.405000,64.750000,60.518070,55.518070,0.277965,5.00,0.0789,-0.1714,-0.0039,57.493254,-38.164077,60.234750,0.569578,0.447203,1.000000
S4,IWM,2005-01-03,2005-01-31,65.095000,62.120005,62.095101,57.095101,0.197817,5.00,0.0768,-0.1412,-0.0016,52.432538,83.524473,61.840250,0.467292,119.921957,1.000000
S4,IWM,2005-02-01,2005-02-28,62.125000,63.140000,59.009196,54.009196,0.288923,5.00,0.0805,-0.1675,-0.0050,47.384729,-44.169343,59.018750,0.762771,12.665386,1.000000
S4,IWM,2005-03-01,2005-03-31,63.330000,61.074995,59.917210,54.917210,0.273340,5.00,0.0790,-0.1564,-0.0053,45.640613,33.480691,60.163500,0.729746,88.571304,1.000000
S4,IWM,2005-04-01,2005-04-29,61.365000,57.620005,58.029470,53.029470,0.243749,5.00,0.0815,-0.1488,-0.0037,45.251386,50.173035,58.296750,0.696262,145.820939,1.000000
S4,IWM,2005-05-02,2005-05-31,57.780000,61.345000,54.689163,49.689163,0.252856,5.00,0.0865,-0.1577,-0.0034,40.842831,-52.643838,54.891000,0.661285,-2.351007,1.000000
S4,IWM,2005-06-01,2005-06-30,61.339995,63.700000,58.709113,53.709113,0.250266,5.00,0.0815,-0.1724,-0.0024,66.973032,-31.935755,58.272995,0.483878,0.875460,1.000000
S4,IWM,2005-07-01,2005-07-29,63.700000,67.890000,60.762835,55.762835,0.277063,5.00,0.0785,-0.1715,-0.0043,57.627070,-44.758189,60.515000,0.605499,-2.464588,1.000000
S4,IWM,2005-08-01,2005-08-31,67.940000,66.530000,64.737123,59.737123,0.290025,5.00,0.0736,-0.1696,-0.0061,51.504999,42.671055,64.543000,0.610952,84.213705,1.000000
S4,IWM,2005-09-01,2005-09-30,66.420000,66.390000,62.587089,57.587089,0.380904,5.00,0.0753,-0.1767,-0.0146,66.464898,-41.573884,63.099000,1.045553,34.341014,1.000000
S4,IWM,2005-10-03,2005-10-31,66.490010,63.780000,62.775316,57.775316,0.321857,5.00,0.0752,-0.1644,-0.0096,58.688745,67.168771,63.165509,0.908744,135.307516,1.000000
S4,IWM,2005-11-01,2005-11-30,64.050000,67.450000,60.115107,55.115107,0.305070,5.00,0.0781,-0.1555,-0.0092,68.278134,-77.654805,60.847500,0.987852,0.073329,1.000000
S4,IWM,2005-12-01,2005-12-30,67.789990,66.720000,64.555425,59.555425,0.227737,5.00,0.0738,-0.1503,-0.0034,45.070236,-12.942015,64.400491,0.523505,26.084725,1.000000
S4,IWM,2006-01-03,2006-01-31,67.210010,72.350010,63.757890,58.757890,0.214069,5.00,0.0744,-0.1398,-0.0033,39.005186,-51.013206,63.849509,0.604120,-2.558019,1.000000
S4,IWM,2006-02-01,2006-02-28,72.590000,72.580000,69.155438,64.155438,0.268416,5.00,0.0689,-0.1595,-0.0062,58.358574,-35.359069,68.960500,0.657064,12.955725,1.000000
S4,IWM,2006-03-01,2006-03-31,72.770000,75.970000,69.675846,64.675846,0.252972,5.00,0.0687,-0.1657,-0.0047,75.524225,-32.432598,69.131500,0.463868,-1.892998,1.000000
S4,IWM,2006-04-03,2006-04-28,76.120000,76.200000,73.093316,68.093316,0.252828,5.00,0.0657,-0.1665,-0.0044,103.325666,-1.357970,72.314000,0.506768,33.486061,1.000000
S4,IWM,2006-05-01,2006-05-31,76.289990,71.870000,72.439386,67.439386,0.340044,5.00,0.0655,-0.1717,-0.0133,44.734768,94.584376,72.475491,0.787392,205.707706,1.000000
S4,IWM,2006-06-01,2006-06-30,71.880000,71.730000,67.267751,62.267751,0.415762,5.00,0.0696,-0.1723,-0.0226,89.653919,-38.435732,68.286000,1.312301,60.668187,1.000000
S4,IWM,2006-07-03,2006-07-31,72.000000,69.679990,66.930545,61.930545,0.395235,5.00,0.0694,-0.1600,-0.0221,107.542750,37.104263,68.400000,1.470662,154.097013,1.000000
S4,IWM,2006-08-01,2006-08-31,69.170000,71.770000,65.281775,60.281775,0.482471,5.00,0.0723,-0.2015,-0.0263,74.272000,-69.897085,65.711500,1.225191,13.824915,1.000000
S4,IWM,2006-09-01,2006-09-29,72.080000,72.000000,67.715980,62.715980,0.333575,5.00,0.0694,-0.1580,-0.0141,72.340589,-31.896902,68.476000,1.056981,49.893687,1.000000
S4,IWM,2006-10-02,2006-10-31,71.970000,76.230000,67.892188,62.892188,0.384994,5.00,0.0695,-0.1762,-0.0176,65.953346,-73.212145,68.371500,1.044527,2.191201,1.000000
S4,IWM,2006-11-01,2006-11-30,76.450000,78.070010,72.260834,67.260834,0.338935,5.00,0.0654,-0.1644,-0.0146,61.852627,-39.288701,72.627500,0.957462,32.013926,1.000000
S4,IWM,2006-12-01,2006-12-29,78.149990,78.030000,73.401503,68.401503,0.408449,5.00,0.0640,-0.1700,-0.0233,87.661178,-71.733755,74.242491,1.285061,25.377423,1.000000
S4,IWM,2007-01-03,2007-01-31,78.679990,79.350010,73.908469,68.908469,0.294788,5.00,0.0635,-0.1422,-0.0127,72.443018,-54.607912,74.745991,1.019218,27.285106,1.000000
S4,IWM,2007-02-01,2007-02-28,79.670000,78.830000,75.604646,70.604646,0.305868,5.00,0.0628,-0.1585,-0.0115,51.832364,15.698105,75.686500,0.824191,76.980469,1.000000
S4,IWM,2007-03-01,2007-03-30,77.470000,79.509990,75.491664,70.491664,0.585168,5.00,0.0645,-0.2894,-0.0249,188.952423,1.767298,73.596500,0.579528,10.653296,1.000000
S4,IWM,2007-04-02,2007-04-30,79.610000,80.740010,75.962020,70.962020,0.320941,5.00,0.0628,-0.1723,-0.0113,71.071260,-39.906646,75.629500,0.699133,7.362575,1.000000
S4,IWM,2007-05-01,2007-05-31,80.990010,84.200000,77.343774,72.343774,0.288522,5.00,0.0617,-0.1644,-0.0092,71.002875,-33.917736,76.940509,0.595286,6.208698,1.000000
S4,IWM,2007-06-01,2007-06-29,84.539990,82.960010,80.138453,75.138453,0.327132,5.00,0.0591,-0.1583,-0.0148,55.946537,0.533909,80.312990,0.886597,65.930446,1.000000
S4,IWM,2007-07-02,2007-07-31,83.380000,77.100010,77.801478,72.801478,0.396338,5.00,0.0600,-0.1554,-0.0255,104.171591,208.705811,79.211000,1.438054,392.474228,1.000000
S4,IWM,2007-08-01,2007-08-31,76.870000,78.740010,71.737364,66.737364,0.497508,5.00,0.0650,-0.1819,-0.0347,112.059964,-69.519666,73.026500,1.618107,51.990298,1.000000
S4,IWM,2007-09-04,2007-09-28,78.679990,80.060000,72.889792,67.889792,0.497626,5.00,0.0635,-0.1698,-0.0356,176.490964,-146.685604,74.745991,2.262535,39.255360,1.000000
S4,IWM,2007-10-01,2007-10-31,80.130000,82.320010,75.159423,70.159423,0.421132,5.00,0.0624,-0.1676,-0.0248,88.383658,-42.931700,76.123500,1.304969,54.901958,1.000000
S4,IWM,2007-11-01,2007-11-30,81.370000,76.580000,76.861607,71.861607,0.603578,5.00,0.0614,-0.2123,-0.0449,98.954964,161.718137,77.301500,1.593128,298.283762,1.000000
S4,IWM,2007-12-03,2007-12-31,76.550000,75.920000,69.979505,64.979505,0.538551,5.00,0.0653,-0.1669,-0.0423,193.801688,-114.175404,72.722500,2.476568,89.076284,1.000000
S4,IWM,2008-01-02,2008-01-31,76.149990,70.940000,71.232630,66.232630,0.384544,5.00,0.0657,-0.1584,-0.0200,93.572601,200.912069,72.342490,1.320270,333.197697,1.000000
S4,IWM,2008-02-01,2008-02-29,71.330000,68.860000,64.765062,59.765062,0.466874,5.00,0.0701,-0.1509,-0.0321,188.747443,-0.607812,67.763500,2.354349,197.589631,1.000000
S4,IWM,2008-03-03,2008-03-31,68.390000,68.289990,63.760168,58.760168,0.512542,5.00,0.0731,-0.1862,-0.0299,119.126758,-36.137454,64.970500,1.703809,92.439304,1.000000
S4,IWM,2008-04-01,2008-04-30,69.460010,71.399990,62.428890,57.428890,0.360685,5.00,0.0720,-0.1228,-0.0211,188.288214,-162.238063,65.987009,2.243567,35.500150,1.000000
S4,IWM,2008-05-01,2008-05-30,71.460010,74.670000,66.684855,61.684855,0.404378,5.00,0.0700,-0.1607,-0.0193,99.780467,-96.613932,67.887009,1.402182,12.616535,1.000000
S4,IWM,2008-06-02,2008-06-30,74.570010,69.050000,70.022588,65.022588,0.422111,5.00,0.0671,-0.1700,-0.0208,92.082532,169.913912,70.841509,1.342936,368.705250,1.000000
S4,IWM,2008-07-01,2008-07-31,68.240010,71.320010,64.546528,59.546528,0.529799,5.00,0.0733,-0.2088,-0.0266,79.213514,-58.869815,64.828009,1.321934,29.793699,1.000000
S4,IWM,2008-08-01,2008-08-29,71.440000,73.870000,65.766942,60.766942,0.456477,5.00,0.0700,-0.1589,-0.0279,149.286028,-148.066074,67.868000,1.949338,10.669954,1.000000
S4,IWM,2008-09-02,2008-09-30,75.009990,68.000000,69.174112,64.174112,0.273693,5.00,0.0667,-0.1159,-0.0116,117.584358,334.251157,71.259490,1.449537,578.696753,1.000000
S4,IWM,2008-10-01,2008-10-31,67.190000,53.750000,61.148497,56.148497,0.658373,5.00,0.0744,-0.1886,-0.0514,207.901528,415.510087,63.830500,2.737388,1132.861615,1.000000
S4,IWM,2008-11-03,2008-11-28,53.480000,47.340000,46.074311,41.074311,0.671976,5.00,0.0935,-0.1679,-0.0507,352.836721,270.058489,50.806000,4.200343,632.345210,1.000000
S4,IWM,2008-12-01,2008-12-31,46.120000,49.240010,39.970504,34.970504,0.800304,5.00,0.1084,-0.1963,-0.0587,288.651602,-247.963182,43.814000,3.686820,50.138420,1.000000
S4,IWM,2009-01-02,2009-01-30,49.740010,44.480000,43.663950,38.663950,0.438647,5.00,0.1005,-0.1418,-0.0220,210.583819,246.780845,47.253009,2.544485,466.814664,1.000000
S4,IWM,2009-02-02,2009-02-27,43.660000,39.149990,39.151702,34.151702,0.616468,5.00,0.1145,-0.1952,-0.0322,201.434482,246.332044,41.477000,2.630813,457.387693,1.000000
S4,IWM,2009-03-02,2009-03-31,38.259990,42.050000,33.660595,28.660595,0.658844,5.00,0.1307,-0.1964,-0.0342,200.250137,-153.320712,36.346990,2.661345,56.379425,1.000000
S4,IWM,2009-04-01,2009-04-30,41.340000,48.520000,36.911558,31.911558,0.591167,5.00,0.1209,-0.1913,-0.0285,176.068866,-171.541334,39.273000,2.351856,13.977532,1.000000
S4,IWM,2009-05-01,2009-05-29,48.649990,50.170000,42.824027,37.824027,0.496473,5.00,0.1028,-0.1554,-0.0265,213.609439,-158.753098,46.217490,2.632567,64.306341,1.000000
S4,IWM,2009-06-01,2009-06-30,51.360000,51.080000,44.940648,39.940648,0.330908,5.00,0.0974,-0.1166,-0.0141,191.379342,-99.372113,48.792000,2.244702,101.457229,1.000000
S4,IWM,2009-07-01,2009-07-31,51.350010,55.570010,46.255901,41.255901,0.401321,5.00,0.0974,-0.1485,-0.0167,148.350825,-146.406412,48.782509,1.884829,11.394412,1.000000
S4,IWM,2009-08-03,2009-08-31,56.240010,57.200000,50.969093,45.969093,0.326371,5.00,0.0889,-0.1305,-0.0120,139.319821,-72.470916,53.428009,1.719569,76.298905,1.000000
S4,IWM,2009-09-01,2009-09-30,56.860000,60.240010,52.454448,47.454448,0.473773,5.00,0.0879,-0.1767,-0.0215,126.800721,-100.498666,54.017000,1.741781,35.752055,1.000000
S4,IWM,2009-10-01,2009-10-30,60.130000,56.330000,54.983832,49.983832,0.473679,5.00,0.0832,-0.1649,-0.0249,148.429837,107.314241,57.123500,1.957977,265.194077,1.000000
S4,IWM,2009-11-02,2009-11-30,56.630000,58.090000,51.535040,46.535040,0.387328,5.00,0.0883,-0.1468,-0.0163,149.897489,-122.078901,53.798500,1.886303,37.268588,1.000000
S4,IWM,2009-12-01,2009-12-31,58.640000,62.440000,53.849456,48.849456,0.307063,5.00,0.0853,-0.1329,-0.0097,108.658287,-110.149466,55.708000,1.393646,7.958821,1.000000
S4,IWM,2010-01-04,2010-01-29,63.289990,60.110000,58.105576,53.105576,0.276606,5.00,0.0790,-0.1204,-0.0089,127.911477,73.849781,60.125490,1.555721,211.211258,1.000000
S4,IWM,2010-02-01,2010-02-26,60.390000,62.800000,55.360541,50.360541,0.382002,5.00,0.0828,-0.1474,-0.0161,155.340997,-142.510553,57.370500,1.935412,22.280444,1.000000
S4,IWM,2010-03-01,2010-03-31,63.259990,67.802510,58.292079,53.292079,0.337055,5.00,0.0790,-0.1386,-0.0127,108.015584,-118.050343,60.096990,1.417211,-0.584760,1.000000
S4,IWM,2010-04-01,2010-04-30,68.330000,71.649990,63.874310,58.874310,0.277168,5.00,0.0732,-0.1319,-0.0075,77.935008,-71.467975,64.913500,1.056518,15.917033,1.000000
S4,IWM,2010-05-03,2010-05-28,72.100010,66.250000,66.715081,61.715081,0.365033,5.00,0.0693,-0.1408,-0.0170,138.184754,337.181954,68.495009,1.746881,531.324819,1.000000
S4,IWM,2010-06-01,2010-06-30,65.600010,61.115010,58.535134,53.535134,0.682712,5.00,0.0762,-0.1789,-0.0562,281.640207,49.583723,62.320009,3.499114,340.673931,1.000000
S4,IWM,2010-07-01,2010-07-30,61.200000,65.020000,55.206407,50.206407,0.492816,5.00,0.0817,-0.1571,-0.0298,187.334983,-179.389632,58.140000,2.366166,17.395351,1.000000
S4,IWM,2010-08-02,2010-08-31,66.170000,60.179990,59.725353,54.725353,0.319842,5.00,0.0756,-0.1172,-0.0152,159.249999,165.574823,62.861500,1.912342,334.274822,1.000000
S4,IWM,2010-09-01,2010-09-30,61.230000,67.500000,54.272182,49.272182,0.383231,5.00,0.0817,-0.1250,-0.0213,207.368717,-204.719731,58.168500,2.456918,12.098985,1.000000
S4,IWM,2010-10-01,2010-10-29,68.140000,70.300000,61.697217,56.697217,0.410010,5.00,0.0734,-0.1373,-0.0238,181.214117,-140.313897,64.733000,2.222152,50.350220,1.000000
S4,IWM,2010-11-01,2010-11-30,70.660000,72.750000,64.657501,59.657501,0.428483,5.00,0.0708,-0.1466,-0.0248,156.269673,-118.089335,67.127000,1.991180,47.630338,1.000000
S4,IWM,2010-12-01,2010-12-31,74.120000,78.240010,67.231853,62.231853,0.307821,5.00,0.0675,-0.1116,-0.0158,155.423659,-160.688502,70.414000,1.862057,4.185157,1.000000
S4,IWM,2011-01-03,2011-01-31,78.940000,77.950000,73.436969,68.436969,0.321027,5.00,0.0633,-0.1297,-0.0141,107.353375,-41.940959,74.993000,1.394561,74.862416,1.000000
S4,IWM,2011-02-01,2011-02-28,78.580000,82.268010,73.124011,68.124011,0.331094,5.00,0.0636,-0.1327,-0.0148,117.140628,-61.794383,74.651000,1.502501,64.796245,1.000000
S4,IWM,2011-03-01,2011-03-31,82.580000,84.170000,74.900318,69.900318,0.526794,5.00,0.0605,-0.1511,-0.0421,228.102107,-190.250399,78.451000,2.807815,47.301708,1.000000
S4,IWM,2011-04-01,2011-04-29,84.770000,86.390000,78.130732,73.130732,0.414592,5.00,0.0590,-0.1391,-0.0267,159.757658,-147.749197,80.531500,2.012169,21.458460,1.000000
S4,IWM,2011-05-02,2011-05-31,86.780000,84.840000,81.509725,76.509725,0.359474,5.00,0.0576,-0.1427,-0.0171,89.454118,25.355316,82.441000,1.254015,124.259435,1.000000
S4,IWM,2011-06-01,2011-06-30,84.710010,82.800000,79.392515,74.392515,0.467019,5.00,0.0590,-0.1656,-0.0279,113.977904,41.396776,80.474509,1.606798,164.824680,1.000000
S4,IWM,2011-07-01,2011-07-29,82.880000,79.740010,76.321624,71.321624,0.502988,5.00,0.0603,-0.1573,-0.0362,179.513712,10.051639,78.736000,2.298125,199.015351,1.000000
S4,IWM,2011-08-01,2011-08-31,80.690000,72.649990,73.759591,68.759591,0.376280,5.00,0.0620,-0.1275,-0.0230,158.332190,307.953593,76.655500,1.959602,586.695880,1.000000
S4,IWM,2011-09-01,2011-09-30,72.700000,64.300000,64.316710,59.316710,0.620624,5.00,0.0688,-0.1587,-0.0530,308.390490,391.222954,69.065000,3.704528,710.734470,1.000000
S4,IWM,2011-10-03,2011-10-31,63.810000,74.009990,56.652500,51.652500,0.663925,5.00,0.0784,-0.1740,-0.0533,286.143686,-281.118762,60.619500,3.525361,14.474924,1.000000
S4,IWM,2011-11-01,2011-11-30,71.179990,73.730000,66.340043,61.340043,0.976172,5.00,0.0702,-0.2544,-0.0916,221.703878,-71.292260,67.620991,3.193210,159.861617,1.000000
S4,IWM,2011-12-01,2011-12-30,73.470000,73.750000,64.888621,59.888621,0.676230,5.00,0.0681,-0.1663,-0.0606,333.852005,-274.804519,69.796500,4.014750,68.497486,1.000000
S4,IWM,2012-01-03,2012-01-31,75.679990,79.020000,67.734047,62.734047,0.292027,5.00,0.0661,-0.0998,-0.0163,202.398658,-191.648730,71.895990,2.316013,20.199928,1.000000
S4,IWM,2012-02-01,2012-02-29,79.759990,81.050000,73.893460,68.893460,0.339607,5.00,0.0627,-0.1298,-0.0166,125.271575,-76.213268,75.771991,1.592323,58.508307,1.000000
S4,IWM,2012-03-01,2012-03-30,81.380000,82.810000,75.682181,70.682181,0.404267,5.00,0.0614,-0.1468,-0.0225,120.960101,-81.677399,77.311000,1.613868,48.732702,1.000000
S4,IWM,2012-04-02,2012-04-30,82.539990,81.470000,77.423478,72.423478,0.484307,5.00,0.0606,-0.1718,-0.0288,114.735428,-20.117229,78.412990,1.631661,104.068198,1.000000
S4,IWM,2012-05-01,2012-05-31,81.560000,76.110000,75.909201,70.909201,0.447244,5.00,0.0613,-0.1566,-0.0268,126.375654,297.516072,77.482000,1.711001,433.341726,1.000000
S4,IWM,2012-06-01,2012-06-29,74.399990,79.560000,70.277030,65.277030,0.744645,5.00,0.0672,-0.2350,-0.0544,124.372142,-127.282511,70.679991,1.988366,6.539631,1.000000
S4,IWM,2012-07-02,2012-07-31,79.920000,78.350010,74.210911,69.210911,0.400233,5.00,0.0626,-0.1456,-0.0220,123.083371,-62.906728,75.924000,1.631066,69.626643,1.000000
S4,IWM,2012-08-01,2012-08-31,78.910000,81.120000,73.755682,68.755682,0.321472,5.00,0.0634,-0.1343,-0.0131,88.927012,-82.772769,74.964500,1.210742,15.604243,1.000000
S4,IWM,2012-09-04,2012-09-28,81.179990,83.440000,76.997226,71.997226,0.349726,5.00,0.0616,-0.1570,-0.0122,82.035357,-73.071300,77.120991,1.170079,18.414057,1.000000
S4,IWM,2012-10-01,2012-10-31,83.960010,81.630000,79.140386,74.140386,0.301275,5.00,0.0596,-0.1343,-0.0108,66.062068,26.280059,79.762009,0.961896,101.792127,1.000000
S4,IWM,2012-11-01,2012-11-30,81.820010,82.080000,76.880912,71.880912,0.378471,5.00,0.0611,-0.1514,-0.0174,87.759720,-81.889819,77.729009,1.256069,15.319901,1.000000
S4,IWM,2012-12-03,2012-12-31,82.710010,84.317790,78.197148,73.197148,0.255033,5.00,0.0605,-0.1260,-0.0068,58.582370,-57.270936,78.574509,0.840856,10.761434,1.000000
S4,IWM,2013-01-02,2013-01-31,86.340000,89.580000,79.517353,74.517353,0.192129,5.00,0.0579,-0.0833,-0.0071,109.633818,-120.006542,82.023000,1.288467,-0.922724,1.000000
S4,IWM,2013-02-01,2013-02-28,89.960010,90.480000,86.043371,81.043371,0.255561,5.00,0.0556,-0.1367,-0.0055,93.981390,4.365761,85.462009,0.614013,49.661022,1.000000
S4,IWM,2013-03-01,2013-03-28,89.880000,94.429990,85.426461,80.426461,0.510087,5.00,0.0556,-0.1890,-0.0292,88.974607,-96.429014,85.386000,1.359372,-2.050539,1.000000
S4,IWM,2013-04-01,2013-04-30,94.270000,94.100010,90.379786,85.379786,0.372830,5.00,0.0530,-0.1696,-0.0134,117.871267,-1.526775,89.556500,0.728258,43.465933,1.000000
S4,IWM,2013-05-01,2013-05-31,93.810000,97.800000,89.507537,84.507537,0.431038,5.00,0.0533,-0.1752,-0.0204,92.471579,-52.510785,89.119500,0.967717,10.607063,1.000000
S4,IWM,2013-06-03,2013-06-28,98.140000,97.000000,92.637053,87.637053,0.380245,5.00,0.0509,-0.1456,-0.0205,104.441020,-27.165949,93.233000,1.424656,86.725070,1.000000
S4,IWM,2013-07-01,2013-07-31,97.649990,103.655000,90.763607,85.763607,0.412620,5.00,0.0512,-0.1378,-0.0282,136.134739,-148.215338,92.767490,1.773967,-2.630599,1.000000
S4,IWM,2013-08-01,2013-08-30,104.679990,100.380000,99.396815,94.396815,0.234564,5.00,0.0478,-0.1108,-0.0078,49.024138,59.701362,99.445990,0.724806,118.175500,1.000000
S4,IWM,2013-09-03,2013-09-30,101.860000,106.610000,95.037567,90.037567,0.268990,5.00,0.0491,-0.1052,-0.0137,117.116787,-117.699288,96.767000,1.440158,8.867500,1.000000
S4,IWM,2013-10-01,2013-10-31,106.560000,109.190000,101.114018,96.114018,0.448262,5.00,0.0469,-0.1622,-0.0279,81.669770,-79.625806,101.232000,1.264960,11.493964,1.000000
S4,IWM,2013-11-01,2013-11-29,109.410000,113.510000,104.213609,99.213609,0.379194,5.00,0.0457,-0.1502,-0.0198,91.494417,-71.694964,103.939500,1.020029,1.838551,1.000000
S4,IWM,2013-12-02,2013-12-31,113.700000,115.360000,108.545983,103.545983,0.381267,5.00,0.0440,-0.1516,-0.0201,107.139203,-44.265522,108.015000,0.921676,19.225366,1.000000
S4,IWM,2014-01-02,2014-01-31,115.090000,112.160000,110.204939,105.204939,0.456324,5.00,0.0434,-0.1727,-0.0269,139.659230,114.157577,109.335500,0.983478,176.322932,1.000000
S4,IWM,2014-02-03,2014-02-28,111.870000,117.520000,106.233682,101.233682,0.502505,5.00,0.0447,-0.1716,-0.0355,112.441858,-112.284362,106.276500,1.626923,9.607496,1.000000
S4,IWM,2014-03-03,2014-03-31,116.520000,116.340000,112.003978,107.003978,0.587358,5.00,0.0429,-0.2057,-0.0408,188.621888,-5.403278,110.694000,1.163598,61.670796,1.000000
S4,IWM,2014-04-01,2014-04-30,116.630000,111.980000,110.121410,105.121410,0.443139,5.00,0.0429,-0.1498,-0.0319,110.669895,98.575244,110.798500,1.549838,218.695139,1.000000
S4,IWM,2014-05-01,2014-05-30,111.750000,112.860000,105.922919,100.922919,0.501155,5.00,0.0447,-0.1689,-0.0361,97.275449,-74.936740,106.162500,1.473909,31.788709,1.000000
S4,IWM,2014-06-02,2014-06-30,113.070000,118.810000,107.274422,102.274422,0.417661,5.00,0.0442,-0.1516,-0.0262,85.595750,-88.557859,107.416500,1.273619,6.487891,1.000000
S4,IWM,2014-07-01,2014-07-31,119.260000,111.189900,112.389537,107.389537,0.434725,5.00,0.0419,-0.1446,-0.0321,115.863490,214.709181,113.297000,1.593360,459.986340,1.000000
S4,IWM,2014-08-01,2014-08-29,111.160000,116.560000,104.073107,99.073107,0.528752,5.00,0.0450,-0.1610,-0.0441,160.235760,-168.701506,105.602000,2.131110,0.984254,1.000000
S4,IWM,2014-09-02,2014-09-30,116.980000,109.350000,111.119243,106.119243,0.381795,5.00,0.0427,-0.1430,-0.0227,81.380142,106.946623,111.131000,1.195596,374.701091,1.000000
S4,IWM,2014-10-01,2014-10-31,109.290000,116.560000,102.863404,97.863404,0.502549,5.00,0.0457,-0.1621,-0.0384,121.496354,-130.610292,103.825500,1.717512,0.336062,1.000000
S4,IWM,2014-11-03,2014-11-28,116.750000,116.690000,111.197260,106.197260,0.405385,5.00,0.0428,-0.1520,-0.0241,113.926971,-50.827596,110.912500,1.259894,44.073337,1.000000
S4,IWM,2014-12-01,2014-12-31,116.320000,119.620000,111.338542,106.338542,0.481342,5.00,0.0430,-0.1765,-0.0302,137.106134,-49.402223,110.504000,1.017862,13.699732,1.000000
S4,IWM,2015-01-02,2015-01-30,120.070000,115.700000,113.718498,108.718498,0.405013,5.00,0.0416,-0.1432,-0.0270,93.808502,133.064820,114.066500,1.343098,236.323321,1.000000
S4,IWM,2015-02-02,2015-02-27,116.120000,122.580000,109.557907,104.557907,0.423845,5.00,0.0431,-0.1450,-0.0297,136.384996,-144.066580,110.314000,1.787695,1.768415,1.000000
S4,IWM,2015-03-02,2015-03-31,122.550000,124.370000,117.117339,112.117339,0.438420,5.00,0.0408,-0.1614,-0.0276,129.676641,-46.868489,116.422500,1.040348,22.774275,1.000000
S4,IWM,2015-04-01,2015-04-30,124.230000,121.180000,118.414725,113.414725,0.479572,5.00,0.0402,-0.1656,-0.0341,118.956560,-25.994071,118.018500,1.272912,62.789952,1.000000
S4,IWM,2015-05-01,2015-05-29,121.520000,123.890000,116.314977,111.314977,0.353100,5.00,0.0411,-0.1444,-0.0177,134.594221,-52.300619,115.444000,0.828065,4.645907,1.000000
S4,IWM,2015-06-01,2015-06-30,124.690000,124.860000,118.510931,113.510931,0.332146,5.00,0.0401,-0.1282,-0.0188,71.630781,-48.560117,118.455500,0.993023,26.977607,1.000000
S4,IWM,2015-07-01,2015-07-31,125.770000,122.960000,119.189233,114.189233,0.338462,5.00,0.0398,-0.1259,-0.0206,75.721644,-28.455554,119.481500,1.095678,56.716090,1.000000
S4,IWM,2015-08-03,2015-08-31,123.030000,115.200000,118.078197,113.078197,0.389568,5.00,0.0406,-0.1570,-0.0204,162.449138,203.487588,116.878500,0.814362,543.236725,1.000000
S4,IWM,2015-09-01,2015-09-30,113.110000,109.200000,106.605390,101.605390,0.833927,5.00,0.0442,-0.2210,-0.0870,204.234297,19.885975,107.454500,2.876270,233.570272,1.000000
S4,IWM,2015-10-01,2015-10-30,109.370000,115.340000,103.015181,98.015181,0.458393,5.00,0.0457,-0.1538,-0.0327,113.095548,-125.177849,103.901500,1.589348,-2.632301,1.000000
S4,IWM,2015-11-02,2015-11-30,115.450000,119.100000,110.806496,105.806496,0.362485,5.00,0.0433,-0.1547,-0.0163,155.764951,-39.987004,109.677500,0.791139,12.328383,1.000000
S4,IWM,2015-12-01,2015-12-31,119.610000,112.620000,113.192383,108.192383,0.399445,5.00,0.0418,-0.1416,-0.0268,90.298051,261.330703,113.629500,1.302426,418.317020,1.000000
S4,IWM,2016-01-04,2016-01-29,110.610000,102.960000,106.931706,101.931706,0.776071,5.00,0.0452,-0.2557,-0.0608,253.847104,6.000713,105.079500,1.462336,481.247817,1.000000
S4,IWM,2016-02-01,2016-02-29,102.140000,102.730000,96.272544,91.272544,0.616113,5.00,0.0490,-0.1902,-0.0509,139.524823,-106.216852,97.033000,2.011361,42.757971,1.000000
S4,IWM,2016-03-01,2016-03-31,103.620000,110.630000,96.394798,91.394798,0.391092,5.00,0.0483,-0.1314,-0.0274,139.392772,-148.327925,98.439000,1.785020,0.514848,1.000000
S4,IWM,2016-04-01,2016-04-29,109.610000,112.480000,105.129007,100.129007,0.593150,5.00,0.0456,-0.2075,-0.0413,165.280498,-61.790322,104.129500,1.246448,12.989492,1.000000
S4,IWM,2016-05-02,2016-05-31,112.830000,115.000000,106.794367,101.794367,0.407687,5.00,0.0443,-0.1472,-0.0262,87.519770,-43.221122,107.188500,1.282884,53.748648,1.000000
S4,IWM,2016-06-01,2016-06-30,114.610000,114.980000,107.894377,102.894377,0.570455,5.00,0.0436,-0.1736,-0.0492,144.431864,-49.103115,108.879500,2.014774,104.778749,1.000000
S4,IWM,2016-07-01,2016-07-29,115.050000,121.070000,105.425113,100.425113,0.616246,5.00,0.0435,-0.1589,-0.0631,292.269330,-301.117812,109.297500,3.538940,0.601519,1.000000
S4,IWM,2016-08-01,2016-08-31,121.200000,123.230000,115.252743,110.252743,0.439863,5.00,0.0413,-0.1561,-0.0301,85.667955,-64.503341,115.140000,1.183799,19.340297,1.000000
S4,IWM,2016-09-01,2016-09-30,123.340000,124.210000,117.125333,112.125333,0.457434,5.00,0.0405,-0.1571,-0.0334,88.271399,-62.649299,117.173000,1.340148,35.072099,1.000000
S4,IWM,2016-10-03,2016-10-31,123.830000,118.500000,118.059643,113.059643,0.522401,5.00,0.0404,-0.1756,-0.0397,129.382605,156.513335,117.638500,1.395083,253.231592,1.000000
S4,IWM,2016-11-01,2016-11-30,118.660000,131.610000,112.093410,107.093410,0.468860,5.00,0.0421,-0.1553,-0.0357,117.051901,-128.536597,112.727000,1.639379,-2.034696,1.000000
S4,IWM,2016-12-01,2016-12-30,132.250000,134.850000,124.994091,119.994091,0.422164,5.00,0.0378,-0.1406,-0.0331,106.197390,-83.932370,125.637500,1.484138,31.715020,1.000000
S4,IWM,2017-01-03,2017-01-31,136.490000,135.230000,127.376450,122.376450,0.370903,5.00,0.0366,-0.1169,-0.0312,164.968455,-91.585692,129.665500,2.020587,82.832763,1.000000
S4,IWM,2017-02-01,2017-02-28,136.220000,137.840000,128.480544,123.480544,0.392126,5.00,0.0367,-0.1304,-0.0308,125.618935,-84.449250,129.409000,1.648315,50.619685,1.000000
S4,IWM,2017-03-01,2017-03-31,139.650000,137.480000,129.574421,124.574421,0.394856,5.00,0.0358,-0.1171,-0.0361,184.410403,-62.976484,132.667500,2.238960,130.883919,1.000000
S4,IWM,2017-04-03,2017-04-28,137.970000,139.060000,129.928966,124.928966,0.482369,5.00,0.0362,-0.1479,-0.0437,168.006649,-122.869009,131.071500,2.162436,54.587640,1.000000
S4,IWM,2017-05-01,2017-05-31,139.640000,136.320000,131.658512,126.658512,0.466586,5.00,0.0358,-0.1457,-0.0418,124.795885,-34.295350,132.658000,1.714545,99.950535,1.000000
S4,IWM,2017-06-01,2017-06-30,136.720000,140.920000,130.056676,125.056676,0.430900,5.00,0.0366,-0.1494,-0.0333,98.850585,-84.603833,129.884000,1.246730,6.429135,1.000000
S4,IWM,2017-07-03,2017-07-31,141.340000,141.510000,133.922818,128.922818,0.464419,5.00,0.0354,-0.1502,-0.0402,113.360704,-87.056738,134.273000,1.598026,35.753965,1.000000
S4,IWM,2017-08-01,2017-08-31,142.170000,139.730000,135.499945,130.499945,0.388304,5.00,0.0352,-0.1410,-0.0287,111.953291,18.595392,135.061500,1.069392,96.154152,1.000000
S4,IWM,2017-09-01,2017-09-29,139.980000,148.180000,133.519058,128.519058,0.445045,5.00,0.0357,-0.1550,-0.0347,131.960821,-89.570333,132.981000,1.226595,-1.965336,1.000000
S4,IWM,2017-10-02,2017-10-31,148.310000,149.260000,142.221763,137.221763,0.444929,5.00,0.0337,-0.1598,-0.0339,185.402223,-53.454441,140.894500,0.971688,8.671487,1.000000
S4,IWM,2017-11-01,2017-11-30,150.500000,153.650000,142.769433,137.769433,0.354157,5.00,0.0332,-0.1245,-0.0276,89.328158,-77.908898,142.975000,1.247439,20.869260,1.000000
S4,IWM,2017-12-01,2017-12-29,153.670000,152.460000,146.941471,141.941471,0.494149,5.00,0.0325,-0.1643,-0.0433,175.012396,-25.116080,145.986500,1.289302,63.849203,1.000000
S4,IWM,2018-01-02,2018-01-31,153.200000,156.360000,145.146362,140.146362,0.444871,5.00,0.0326,-0.1429,-0.0406,115.255576,-45.800277,145.540000,1.597427,78.905300,1.000000
S4,IWM,2018-02-01,2018-02-28,155.730000,150.350000,148.888621,143.888621,0.602134,5.00,0.0321,-0.1852,-0.0597,201.874691,47.815926,147.943500,1.675761,164.628561,1.000000
S4,IWM,2018-03-01,2018-03-29,150.050000,151.830000,144.115435,139.115435,0.515063,5.00,0.0333,-0.1783,-0.0437,216.137233,-8.166989,142.547500,1.108500,60.626735,1.000000
S4,IWM,2018-04-02,2018-04-30,151.520000,153.320000,144.229671,139.229671,0.571456,5.00,0.0330,-0.1757,-0.0572,145.364959,-106.896569,143.944000,1.739434,19.351252,1.000000
S4,IWM,2018-05-01,2018-05-31,153.010000,162.770000,146.605905,141.605905,0.537608,5.00,0.0327,-0.1786,-0.0496,194.929701,-81.558143,145.359500,1.240500,-1.818966,1.000000
S4,IWM,2018-06-01,2018-06-29,163.830000,163.770000,157.329483,152.329483,0.314963,5.00,0.0305,-0.1286,-0.0216,205.074049,34.667690,155.638500,0.674720,80.093438,1.000000
S4,IWM,2018-07-02,2018-07-31,162.760000,165.870000,157.093154,152.093154,0.626675,5.00,0.0307,-0.2060,-0.0607,295.016574,-42.516769,154.622000,1.105687,14.834416,1.000000
S4,IWM,2018-08-01,2018-08-31,165.700000,173.020000,159.938520,154.938520,0.484695,5.00,0.0302,-0.1772,-0.0410,281.309286,-36.707949,157.415000,0.774268,1.699343,1.000000
S4,IWM,2018-09-04,2018-09-28,172.790000,168.550000,166.013624,161.013624,0.535314,5.00,0.0289,-0.1756,-0.0517,281.246211,44.594645,164.150500,1.484652,148.978445,1.000000
S4,IWM,2018-10-01,2018-10-31,169.290000,150.030000,161.203145,156.203145,0.448072,5.00,0.0295,-0.1473,-0.0439,123.756694,521.104467,160.825500,1.307993,1116.546638,1.000000
S4,IWM,2018-11-01,2018-11-30,150.890000,152.620000,139.511962,134.511962,0.563509,5.00,0.0331,-0.1482,-0.0653,273.650245,-246.722062,143.345500,3.300012,36.378183,1.000000
S4,IWM,2018-12-03,2018-12-31,154.390000,133.900000,144.266917,139.266917,0.405656,5.00,0.0324,-0.1240,-0.0409,173.537249,823.469772,146.670500,2.141028,1506.457021,1.000000
S4,IWM,2019-01-02,2019-01-31,132.170000,149.060000,122.842541,117.842541,0.821751,5.00,0.0378,-0.2022,-0.1001,310.504901,-322.668418,125.561500,3.926800,-2.713516,1.000000
S4,IWM,2019-02-01,2019-02-28,149.350000,156.780000,141.468785,136.468785,0.508135,5.00,0.0335,-0.1592,-0.0504,133.344147,-143.121766,141.882500,1.841577,-0.327619,1.000000
S4,IWM,2019-03-01,2019-03-29,157.950000,153.090000,150.487473,145.487473,0.356710,5.00,0.0317,-0.1312,-0.0295,115.250644,67.222949,150.052500,1.074243,148.426301,1.000000
S4,IWM,2019-04-01,2019-04-30,154.290000,158.290000,145.743818,140.743818,0.408261,5.00,0.0324,-0.1344,-0.0386,114.338712,-93.298581,146.575500,1.551648,30.490130,1.000000
S4,IWM,2019-05-01,2019-05-31,158.670000,145.860000,149.923008,144.923008,0.528216,5.00,0.0315,-0.1583,-0.0567,141.451700,128.929591,150.736500,1.942733,686.132077,1.000000
S4,IWM,2019-06-03,2019-06-28,146.130000,155.500000,136.735768,131.735768,0.568568,5.00,0.0342,-0.1592,-0.0620,235.799452,-240.064178,138.823500,2.926563,5.185274,1.000000
S4,IWM,2019-07-01,2019-07-31,157.540000,156.560000,146.716063,141.716063,0.402364,5.00,0.0317,-0.1199,-0.0415,178.526734,-129.051991,149.663000,2.187631,58.924743,1.000000
S4,IWM,2019-08-01,2019-08-30,156.880000,148.840000,149.957271,144.957271,0.459121,5.00,0.0319,-0.1581,-0.0411,162.293143,242.625069,149.036000,1.160781,433.968212,1.000000
S4,IWM,2019-09-03,2019-09-30,147.450000,151.340000,140.059956,135.059956,0.733101,5.00,0.0339,-0.2042,-0.0825,180.754425,-158.420623,140.077500,2.540646,31.783802,1.000000
S4,IWM,2019-10-01,2019-10-31,152.110000,155.450000,143.458604,138.458604,0.470342,5.00,0.0329,-0.1452,-0.0464,136.503724,-137.254926,144.504500,1.835379,8.698798,1.000000
S4,IWM,2019-11-01,2019-11-29,156.400000,161.770000,149.299054,144.299054,0.365839,5.00,0.0320,-0.1340,-0.0285,137.886444,-71.837054,148.580000,1.025650,3.593978,1.000000
S4,IWM,2019-12-02,2019-12-31,162.150000,165.670000,154.671074,149.671074,0.471492,5.00,0.0308,-0.1545,-0.0438,148.034090,-82.258647,154.042500,1.323258,12.368017,1.000000
S4,IWM,2020-01-02,2020-01-31,166.740000,160.530000,159.361699,154.361699,0.361066,5.00,0.0300,-0.1313,-0.0290,154.393422,135.136147,158.403000,0.946301,203.109670,1.000000
S4,IWM,2020-02-03,2020-02-28,161.600000,146.330000,152.914278,147.914278,0.425319,5.00,0.0309,-0.1350,-0.0399,142.618475,177.896914,153.520000,1.851503,829.965389,1.000000
S4,IWM,2020-03-02,2020-03-31,147.970000,114.460000,135.346476,130.346476,0.519024,5.00,0.0338,-0.1327,-0.0586,316.002021,2478.638668,140.571500,3.679044,3304.090689,1.000000
S4,IWM,2020-04-01,2020-04-30,108.700000,130.310000,96.888732,91.888732,1.257046,5.00,0.0460,-0.2373,-0.1582,752.595021,-751.240423,103.265000,8.782997,10.804598,1.000000
S4,IWM,2020-05-01,2020-05-29,127.150000,138.900000,118.238064,113.238064,0.981332,5.00,0.0393,-0.2249,-0.1201,372.081585,-352.312272,120.792500,4.702148,29.219313,1.000000
S4,IWM,2020-06-01,2020-06-30,139.260000,143.180000,127.177477,122.177477,0.641672,5.00,0.0359,-0.1536,-0.0733,364.060090,0.429814,132.297000,4.282273,373.939904,1.000000
S4,IWM,2020-07-01,2020-07-31,143.650000,147.360000,125.807122,120.807122,0.771545,5.00,0.0348,-0.1546,-0.0957,712.735639,-528.264772,136.467500,7.898902,193.920867,1.000000
S4,IWM,2020-08-03,2020-08-31,148.290000,155.430000,132.379446,127.379446,0.681684,5.00,0.0337,-0.1471,-0.0830,570.302938,-427.524479,140.875500,6.384713,152.228460,1.000000
S4,IWM,2020-09-01,2020-09-30,155.220000,149.790000,141.609053,136.609053,0.725716,5.00,0.0322,-0.1636,-0.0894,462.546877,-31.168178,147.459000,5.351185,440.828700,1.000000
S4,IWM,2020-10-01,2020-10-30,150.810000,153.090000,136.850117,131.850117,0.618838,5.00,0.0332,-0.1435,-0.0729,420.894723,-122.465483,143.269500,4.827785,307.879240,1.000000
S4,IWM,2020-11-02,2020-11-30,154.770000,181.020000,138.367101,133.367101,0.622485,5.00,0.0323,-0.1367,-0.0753,568.663877,-580.448463,147.031500,6.309124,-2.334586,1.000000
S4,IWM,2020-12-01,2020-12-31,183.595000,196.060000,168.596312,163.596312,0.481691,5.00,0.0272,-0.1183,-0.0561,340.989068,-301.472767,174.415250,3.891582,48.966301,1.000000
S4,IWM,2021-01-04,2021-01-29,197.540000,205.560000,182.707106,177.707106,0.572452,5.00,0.0253,-0.1366,-0.0705,411.907646,149.085344,187.663000,4.691529,570.442989,1.000000
S4,IWM,2021-02-01,2021-02-26,208.170000,218.310000,187.069878,182.069878,0.622764,5.00,0.0240,-0.1313,-0.0820,764.694959,-620.605428,197.761500,8.269714,153.539531,1.000000
S4,IWM,2021-03-01,2021-03-31,223.480000,220.940000,196.871034,191.871034,0.565037,5.00,0.0224,-0.1137,-0.0748,808.552975,-342.794408,212.306000,8.650567,475.208567,1.000000
S4,IWM,2021-04-01,2021-04-30,222.400000,224.890000,202.548404,197.548404,0.670624,5.00,0.0225,-0.1432,-0.0903,609.878168,-366.331995,211.280000,6.769406,252.996172,1.000000
S4,IWM,2021-05-03,2021-05-28,227.210000,225.500000,206.927626,201.927626,0.615725,5.00,0.0220,-0.1332,-0.0821,652.741473,-292.440181,215.849500,7.143139,369.751292,1.000000
S4,IWM,2021-06-01,2021-06-30,227.460000,229.370000,205.772036,200.772036,0.666771,5.00,0.0220,-0.1392,-0.0905,696.581132,-522.070154,216.087000,7.632583,183.960978,1.000000
S4,IWM,2021-07-01,2021-07-30,230.810000,221.050000,214.098431,209.098431,0.607074,5.00,0.0217,-0.1399,-0.0794,401.768674,217.463094,219.269500,4.624761,628.681769,1.000000
S4,IWM,2021-08-02,2021-08-31,222.470000,225.920000,202.125103,197.125103,0.682253,5.00,0.0225,-0.1442,-0.0923,633.218449,-388.492421,211.346500,7.014437,254.176028,1.000000
S4,IWM,2021-09-01,2021-09-30,226.830000,218.750000,205.437998,200.437998,0.730972,5.00,0.0220,-0.1506,-0.1005,725.045291,100.699755,215.488500,7.981424,835.195046,1.000000
S4,IWM,2021-10-01,2021-10-29,219.950000,228.050000,199.621507,194.621507,0.698464,5.00,0.0227,-0.1467,-0.0946,668.846470,-606.548863,208.952500,7.386929,71.747607,1.000000
S4,IWM,2021-11-01,2021-11-30,229.250000,218.170000,214.042152,209.042152,0.594842,5.00,0.0218,-0.1416,-0.0761,333.220512,500.776868,217.787500,3.927047,843.447380,1.000000
S4,IWM,2021-12-01,2021-12-31,223.170000,222.450000,202.221184,197.221184,0.441905,5.00,0.0224,-0.1005,-0.0556,480.305581,-278.957669,212.011500,5.244961,210.797912,1.000000
S4,IWM,2022-01-03,2022-01-31,223.710000,201.240000,207.211512,202.211512,0.619980,5.00,0.0224,-0.1423,-0.0809,425.651901,803.980988,212.524500,4.876499,1739.082888,1.000000
S4,IWM,2022-02-01,2022-02-28,201.660000,203.320000,177.635348,172.635348,0.819059,5.00,0.0248,-0.1565,-0.1111,1059.841311,-535.164574,191.577000,11.417472,534.126736,1.000000
S4,IWM,2022-03-01,2022-03-31,202.660000,205.270000,181.874587,176.874587,0.840467,5.00,0.0247,-0.1673,-0.1155,817.358394,-711.780423,192.527000,9.014051,115.027971,1.000000
S4,IWM,2022-04-01,2022-04-29,206.180000,184.950000,192.416335,187.416335,0.596794,5.00,0.0243,-0.1461,-0.0747,318.228364,618.174639,195.871000,3.779078,1445.853003,1.000000
S4,IWM,2022-05-02,2022-05-31,184.900000,185.310000,166.561266,161.561266,0.778771,5.00,0.0270,-0.1620,-0.1043,668.633345,-440.229744,175.655000,7.465105,237.853601,1.000000
S4,IWM,2022-06-01,2022-06-30,186.270000,169.360000,170.201944,165.201944,0.656295,5.00,0.0268,-0.1487,-0.0851,478.733065,514.041248,176.956500,5.443626,1086.418728,1.000000
S4,IWM,2022-07-01,2022-07-29,169.050000,187.250000,156.642691,151.642691,0.704022,5.00,0.0296,-0.1695,-0.0893,361.909759,-361.760672,160.597500,4.323120,9.599087,1.000000
S4,IWM,2022-08-01,2022-08-31,185.790000,183.500000,173.676501,168.676501,0.802665,5.00,0.0269,-0.1913,-0.1086,339.848625,11.170255,176.500500,4.201152,360.468880,1.000000
S4,IWM,2022-09-01,2022-09-30,181.780000,164.920000,169.936865,164.936865,0.825947,5.00,0.0275,-0.1967,-0.1124,354.619221,74.771434,172.691000,4.372139,938.840655,1.000000
S4,IWM,2022-10-03,2022-10-31,167.340000,183.330000,149.755569,144.755569,0.590188,5.00,0.0299,-0.1338,-0.0761,544.121062,-527.246319,158.973000,6.031399,26.324743,1.000000
S4,IWM,2022-11-01,2022-11-30,185.240000,187.370000,169.060003,164.060003,0.587724,5.00,0.0270,-0.1412,-0.0787,446.257725,-328.651269,175.978000,5.050301,127.056456,1.000000
S4,IWM,2022-12-01,2022-12-30,188.151000,174.360000,176.493766,171.493766,0.573380,5.00,0.0266,-0.1572,-0.0745,225.909734,144.912328,178.743450,2.832478,593.648692,1.000000
S4,IWM,2023-01-03,2023-01-31,175.930000,191.480000,164.035472,159.035472,0.499796,5.00,0.0284,-0.1403,-0.0617,242.451416,-249.550478,167.133500,2.924310,2.350938,1.000000
S4,IWM,2023-02-01,2023-02-28,191.190000,188.180000,181.764142,176.764142,0.632654,5.00,0.0262,-0.1820,-0.0818,185.546047,75.734379,181.630500,2.354473,257.366238,1.000000
S4,IWM,2023-03-01,2023-03-31,188.190000,178.400000,176.615586,171.615586,0.653543,5.00,0.0266,-0.1739,-0.0889,246.830761,193.238079,178.780500,3.121851,449.518840,1.000000
S4,IWM,2023-04-03,2023-04-28,178.950000,175.200000,167.523597,162.523597,0.593653,5.00,0.0279,-0.1607,-0.0762,277.496930,9.536164,170.002500,3.368622,296.483094,1.000000
S4,IWM,2023-05-01,2023-05-31,175.000000,173.770000,163.738465,158.738465,0.673682,5.00,0.0286,-0.1780,-0.0908,255.796830,-88.282254,166.250000,3.231650,176.964576,1.000000
S4,IWM,2023-06-01,2023-06-30,173.860000,187.270000,162.134318,157.134318,0.654959,5.00,0.0288,-0.1720,-0.0879,279.485574,-286.333265,165.167000,3.449815,2.602309,1.000000
S4,IWM,2023-07-03,2023-07-31,186.910000,198.710000,177.447690,172.447690,0.645299,5.00,0.0268,-0.1856,-0.0854,170.153070,-148.139895,177.564500,2.346829,31.463175,1.000000
S4,IWM,2023-08-01,2023-08-31,197.430000,188.610000,187.673142,182.673142,0.752027,5.00,0.0253,-0.2050,-0.1065,206.512469,113.019364,187.558500,2.702510,317.517660,1.000000
S4,IWM,2023-09-01,2023-09-29,190.070000,176.740000,177.519409,172.519409,0.532636,5.00,0.0263,-0.1477,-0.0708,248.384176,345.839698,180.566500,3.016478,681.614741,1.000000
S4,IWM,2023-10-02,2023-10-31,176.330000,164.520000,165.756787,160.756787,0.680511,5.00,0.0284,-0.1838,-0.0919,234.842921,267.289607,167.513500,3.028940,635.261189,1.000000
S4,IWM,2023-11-01,2023-11-30,164.460000,179.660000,153.915955,148.915955,0.645901,5.00,0.0304,-0.1760,-0.0844,246.825203,-255.995498,156.237000,3.114153,0.279706,1.000000
S4,IWM,2023-12-01,2023-12-29,179.200000,200.710000,170.693494,165.693494,0.635422,5.00,0.0279,-0.1902,-0.0814,184.024019,-148.722482,170.240000,2.022168,-0.597841,1.000000
S4,IWM,2024-01-02,2024-01-31,199.400000,192.880000,188.417511,183.417511,0.771749,5.00,0.0251,-0.2003,-0.1107,265.025363,91.756097,189.430000,3.422003,366.231459,1.000000
S4,IWM,2024-02-01,2024-02-29,194.310000,203.730000,180.528507,175.528507,0.568356,5.00,0.0257,-0.1494,-0.0776,307.649967,-260.858468,184.594500,3.644856,56.241500,1.000000
S4,IWM,2024-03-01,2024-03-28,204.530000,210.300000,190.436607,185.436607,0.629511,5.00,0.0244,-0.1603,-0.0886,346.676456,-285.880526,194.303500,4.096275,70.245930,1.000000
S4,IWM,2024-04-01,2024-04-30,210.770000,195.900000,197.586379,192.586379,0.638629,5.00,0.0237,-0.1672,-0.0910,279.221754,310.794455,200.231500,3.430847,768.104128,1.000000
S4,IWM,2024-05-01,2024-05-31,195.880000,205.770000,183.108844,178.108844,0.680822,5.00,0.0255,-0.1751,-0.0964,296.913083,-296.860384,186.086000,3.649952,9.502699,1.000000
S4,IWM,2024-06-03,2024-06-28,207.530000,202.890000,196.685191,191.685191,0.438728,5.00,0.0241,-0.1378,-0.0547,155.058450,10.532904,197.153500,1.989312,175.041353,1.000000
S4,IWM,2024-07-01,2024-07-31,203.520000,223.860000,192.958060,187.958060,0.560220,5.00,0.0246,-0.1658,-0.0756,150.128488,-137.018781,193.344000,2.061505,22.559708,1.000000
S4,IWM,2024-08-01,2024-08-30,223.770000,220.080000,207.932896,202.932896,0.728931,5.00,0.0223,-0.1741,-0.1083,424.401277,-54.752157,212.581500,4.972944,379.099120,1.000000
S4,IWM,2024-09-03,2024-09-30,218.130000,220.890000,206.797810,201.797810,0.828987,5.00,0.0229,-0.2089,-0.1218,304.041171,-156.866304,207.223500,3.869399,156.624867,1.000000
S4,IWM,2024-10-01,2024-10-31,220.170000,217.760000,207.587556,202.587556,0.731977,5.00,0.0227,-0.1863,-0.1063,282.771652,17.308171,209.161500,3.559694,309.529823,1.000000
S4,IWM,2024-11-01,2024-11-29,219.500000,241.870000,202.522879,197.522879,0.606824,5.00,0.0228,-0.1469,-0.0863,427.166357,-432.370853,208.525000,4.878487,4.245505,1.000000
S4,IWM,2024-12-02,2024-12-31,242.240000,220.960000,226.850416,221.850416,0.677784,5.00,0.0206,-0.1672,-0.1001,349.085970,204.513863,230.128000,4.168644,1063.049833,1.000000
S4,IWM,2025-01-02,2025-01-31,222.930000,226.480000,206.910683,201.910683,0.565285,5.00,0.0224,-0.1424,-0.0795,345.449386,-131.465967,211.783500,4.019779,223.433419,1.000000
S4,IWM,2025-02-03,2025-02-28,221.510000,214.650000,213.071858,208.071858,1.102788,5.00,0.0226,-0.2687,-0.1651,548.447720,103.399731,210.434500,3.949907,397.561661,1.000000
S4,IWM,2025-03-03,2025-03-31,215.400000,199.490000,200.881199,195.881199,0.636808,5.00,0.0232,-0.1594,-0.0895,343.369754,301.739364,204.630000,4.070506,793.679010,1.000000
S4,IWM,2025-04-01,2025-04-30,198.990000,194.860000,188.740993,183.740993,0.673307,5.00,0.0251,-0.1848,-0.0905,197.266070,52.115716,189.040500,2.645968,258.831787,1.000000
S4,IWM,2025-05-01,2025-05-30,195.710000,205.070000,183.136386,178.136386,0.588915,5.00,0.0255,-0.1567,-0.0787,257.722866,-260.540609,185.924500,3.166144,6.632257,1.000000
S4,IWM,2025-06-02,2025-06-30,205.320000,215.790000,195.672090,190.672090,0.571431,5.00,0.0244,-0.1701,-0.0731,196.614371,-140.430578,195.054000,1.919484,3.824759,1.000000
S4,IWM,2025-07-01,2025-07-31,214.620000,219.390000,206.796789,201.796789,0.701067,5.00,0.0233,-0.2104,-0.0934,377.485906,67.059428,203.889000,1.568137,163.216430,1.000000
S4,IWM,2025-08-01,2025-08-29,216.220000,235.170000,206.950784,201.950784,0.933366,5.00,0.0231,-0.2372,-0.1363,381.019479,-197.718283,205.409000,3.201777,38.572784,1.000000
S4,IWM,2025-09-02,2025-09-30,231.990000,241.960000,219.102189,214.102189,0.935462,5.00,0.0216,-0.2185,-0.1411,413.763462,-247.630831,220.390500,5.073097,175.582631,1.000000
S4,IWM,2025-10-01,2025-10-31,240.570000,246.230000,221.680307,216.680307,0.846586,5.00,0.0208,-0.1839,-0.1275,625.714324,-424.937376,228.541500,7.103730,210.226948,1.000000
S4,IWM,2025-11-03,2025-11-28,246.170000,248.750000,228.959392,223.959392,0.734211,5.00,0.0203,-0.1691,-0.1080,530.503002,-168.696429,233.861500,6.039241,371.256573,1.000000
S4,IWM,2025-12-01,2025-12-31,245.570000,246.160000,228.197307,223.197307,0.945946,5.00,0.0204,-0.2047,-0.1447,604.342247,-489.683278,233.291500,6.989369,124.108969,1.000000
S4,IWM,2026-01-02,2026-01-30,247.630000,259.650000,232.885657,227.885657,0.568643,5.00,0.0202,-0.1476,-0.0798,274.567855,-207.725405,235.248500,3.314322,76.292449,1.000000
S4,IWM,2026-02-02,2026-02-27,258.480000,261.410000,244.008535,239.008535,0.779983,5.00,0.0193,-0.1867,-0.1155,420.200045,-54.954030,245.556000,4.981984,374.696016,1.000000
S4,IWM,2026-03-02,2026-03-31,257.810000,248.000000,241.103745,236.103745,0.964223,5.00,0.0194,-0.2107,-0.1488,579.438154,467.999093,244.919500,6.758605,1056.887247,1.000000
S4,IWM,2026-04-01,2026-04-30,249.920000,277.970000,222.477816,217.477816,0.751669,5.00,0.0200,-0.1504,-0.1103,993.317826,-998.129654,237.424000,10.684847,4.638172,1.000000
S4,IWM,2026-05-01,2026-05-29,278.660000,290.430000,260.680300,255.680300,0.682170,5.00,0.0179,-0.1612,-0.1026,429.196927,-360.735829,264.727000,4.974140,77.911098,1.000000
S4,IWM,2026-06-01,2026-06-30,288.370000,300.450000,272.303989,267.303989,0.850682,5.00,0.0173,-0.1972,-0.1323,417.576826,-320.468261,273.951500,5.026450,106.558565,1.000000
S4,IWM,2026-07-01,2026-07-31,299.930000,291.200000,280.229705,275.229705,0.777357,5.00,0.0167,-0.1759,-0.1214,517.670722,-1.723875,284.933500,5.954065,525.396847,1.000000
S4,IWM,2026-08-03,2026-08-31,292.900000,293.930000,273.122573,268.122573,0.637389,5.00,0.0171,-0.1500,-0.0966,456.900857,-353.088920,278.255000,5.206398,113.261937,1.000000
S4,IWM,2026-09-01,2026-09-30,291.980000,277.890000,280.369319,275.369319,0.812462,5.00,0.0171,-0.2095,-0.1240,418.753751,-172.985616,,,,0.000000
```
### SPY-only, longest window -- `out/spy_only.csv` (6 rows)

```
strat,label
S1,+6.86%|-28.15%|0.62|21/32 (66%)|60%|53%
S2,+2.82%|-32.57%|0.35|26/32 (81%)|81%|91%
S3,+10.12%|-23.72%|1.06|26/32 (81%)|76%|70%
S4,-14.46%|-99.44%|-0.34|6/32 (19%)|27%|30%
S5,+5.97%|-23.33%|0.63|22/32 (69%)|66%|66%
S6,+8.91%|-56.47%|0.55|23/32 (72%)|71%|63%
```

---

## Independent re-derivation (`handcheck.py`)

```
==============================================================================
HANDCHECK -- independent re-derivation, no import of study.py
==============================================================================
  read SPY    rows=8485   first=1993-01-29 last=2026-10-14
  read QQQ    rows=6943   first=1999-03-10 last=2026-10-14
  read IWM    rows=6635   first=2000-05-26 last=2026-10-14
  read VIX    rows=9283   first=1990-01-03 last=2026-10-14
  read US03M  rows=18197  first=1954-01-04 last=2026-10-14

  own window: 6436 sessions, 2001-03-13 .. 2026-10-14
  own cash CAGR = 0.017974  (20 of 6436 sessions non-positive)
  own S2 book: CAGR 0.02971104   maxDD -0.26748379   Sharpe 0.40678300

==============================================================================
A. TRADE-LEVEL GAP vs out/s2_structure.csv (S2 rows)
==============================================================================
  study.py S2 trades: 918
  handcheck spread records: 918
  matched on (index, expiry): 918
  S2 short strike K1 (handcheck vs study.py artefact)        gap=4.996e-07      tol=5.1e-04    OK
  S2 long strike K2                                          gap=4.996e-07      tol=5.1e-04    OK
  S2 credit  (handcheck vs study.py, max abs gap)            gap=4.995e-07      tol=5.1e-04    OK
  S2 settlement intrinsic vs the real expiry close           gap=4.996e-07      tol=5.1e-04    OK

==============================================================================
B. HEADLINE GAP vs out/headline.csv (S2)
==============================================================================
  S2 CAGR                                                    gap=0.000e+00      tol=2.0e-06    OK
  S2 maxDD                                                   gap=-3.331e-16     tol=2.0e-06    OK
  S2 Sharpe (raw, daily x sqrt252)                           gap=-5.551e-17     tol=2.0e-06    OK
  S2 fraction of positive complete YEARS                     gap=0.000e+00      tol=1.0e-09    OK
  S2 fraction of positive complete QUARTERS                  gap=0.000e+00      tol=1.0e-09    OK
  S2 fraction of positive complete MONTHS                    gap=0.000e+00      tol=1.0e-09    OK
  own counts: Y 19/24  Q 81/102  M 271/306 ; study: Y 19/24 Q 81/102 M 271/306

==============================================================================
C. CORRELATION GAP vs out/correlation.csv
==============================================================================
  SPY/QQQ yearly corr                                        gap=0.000e+00      tol=5.1e-04    OK
  SPY/QQQ daily corr                                         gap=0.000e+00      tol=5.1e-04    OK
  SPY/IWM yearly corr                                        gap=0.000e+00      tol=5.1e-04    OK
  SPY/IWM daily corr                                         gap=0.000e+00      tol=5.1e-04    OK
  QQQ/IWM yearly corr                                        gap=0.000e+00      tol=5.1e-04    OK
  QQQ/IWM daily corr                                         gap=0.000e+00      tol=5.1e-04    OK

==============================================================================
D. VRP RE-DERIVED FROM THE RAW SPY AND VIX CSVS
==============================================================================
  2008  n=253  mean VRP =   -2.33 vol pts   share VIX>forward RV =  60.1%   mean E_R_fair = +0.0577   total = +14.6R
  2020  n=253  mean VRP =   +2.60 vol pts   share VIX>forward RV =  75.1%   mean E_R_fair = -0.0289   total = -7.3R
  ALL  n=8464 mean VRP =   +3.64 vol pts   share VIX>forward RV =  83.0%   fair-strike E_R = +0.1160
  worst window: 2020-02-20  VIX=15.6  R=-3.07  R_fair=-3.98

  SIBLING STUDY's published finding, for sign/size comparison:
    mean VRP +3.62 vol pts, VIX above forward RV in 82.9% of windows,
    VRP negative in exactly one year (2008, -2.33 vol pts);
    fair-strike E_R = +0.1158R, 2020 the one losing year (-7.3R),
    worst window R = -3.98 starting 2020-02-20.

==============================================================================
E. BY HAND -- one Black-Scholes price, every intermediate shown
==============================================================================
  INPUTS (round numbers, nothing to do with the study's data):
    S = 100.00   K = 95.00   days = 30   T = 0.08219178   r = 0.0400   sigma = 0.2000
    sigma*sqrt(T)            = 0.0573382179
    ln(S/K)                  = 0.0512932944
    (r + sigma^2/2)*T        = 0.0049315068
    d1                       = 0.9805815962
    d2 = d1 - sigma*sqrt(T)  = 0.9232433782
    Phi(-d1)                 = 0.1633995568
    Phi(-d2)                 = 0.1779401939
    e^{-rT}                  = 0.9967177272
    K*e^{-rT}*Phi(-d2)       = 16.8488338359
    S*Phi(-d1)               = 16.3399556785
    PUT = K e^{-rT}N(-d2) - S N(-d1) = 0.5088781574
    put delta = e^{-qT}(N(d1)-1) = -0.1633995568
  This is handcheck.py's own pricer.  It is checked against study.py's
  pricer indirectly, through the whole trade ledger in section A.

==============================================================================
F. BY HAND -- one month's put spread settled against the real path
==============================================================================
  trade: S2 SPY entered 2001-04-02 expiring 2001-04-30
    S at entry (open)          = 116.300000
    short strike K1            = 108.9730
    long  strike K2 = K1 - 5   = 103.9730
    real close on expiry       = 124.9100
    short put intrinsic        = max(0, K1 - S) = 0.000000
    long  put intrinsic        = max(0, K2 - S) = 0.000000
    SPREAD intrinsic           = 0.000000
    credit collected           = 0.606128
    gross per share            = credit - intrinsic = 0.606128
    costs (2 legs x 3.15)      = 6.3000 $/contract
    net P&L per contract       = 0.606128 * 100 - 6.3000 = 54.3128
    study.py pnl_dollars       = 54.312811   gap = -0.000011
  by-hand net P&L per contract                               gap=-1.100e-05     tol=5.1e-04    OK
    R = (width - credit) * 100 = (5.0000 - 0.606128) * 100 = 439.3872
    study.py R_dollars         = 439.387189   gap = 0.000011
  by-hand R unit                                             gap=1.100e-05      tol=5.1e-04    OK

==============================================================================
HANDCHECK PASSED -- every gap above is inside its stated tolerance.
==============================================================================
```
