# RESULTS — mean reversion and the volatility premium on real daily prices

Every figure below is sliced out of `run.txt`, the captured stdout of one
`py -3 study.py` run on 2026-10-14 data; `make_results.py` does the slicing, so
the report cannot drift from the run. Nothing here is estimated, and nothing was
re-run until it looked good: the three rule sets and the vol-premium payoff were
fixed in advance, and they are reported as they came out.

- Commands, sources and pull date: `README.md`.
- What the numbers cannot tell you: `FINDINGS.md`.
- Machine-readable tables: `out/*.csv`.

---

## 0. The short version

| question | answer from the data |
|---|---|
| Does mean reversion work on index ETFs? | Partly, and only for one cell. `M1` on SPY
has a real edge (t = 4.79, n = 281) and is the **only 1 of 12 cells** that clears
multiple-comparison correction; the same rule on EEM is indistinguishable from zero
(t = 0.07). It is also the only Sharpe that beats buy-and-hold. |
| Does any rule set win in every regime? | **No.** UP_rising is the only trend state
where all three rules make money pooled; 66 of 155 regime cells have negative
expectancy and DOWN_falling loses for all three. |
| Does any rule set win in every year? | **No.** Every strategy × instrument has
losing years — from 5 of 31 (M1/SPY) up to 14 of 28 (M2/SPY). |
| Does any rule set beat buy-and-hold? | Only M1 on SPY, and only risk-adjusted
(Sharpe 0.71 vs 0.55). On CAGR every rule loses — but they are in the market only
6–25% of sessions, so most of that gap is idle capital, not a missing edge. |
| Is selling premium worth it? | On this proxy, yes on average (mean VRP +3.62 vol
points; VIX above subsequent realised vol in 82.9% of windows) — but it is not free:
the fair-strike series loses in 2020 (−7.3R) and the single worst window is −3.98R. |
| Can parameter fishing create a fake edge? | **Yes.** Tuning M1 on SPY beat the
pre-registered default by +0.213R in-sample and by +0.006R out-of-sample — 3% of the
apparent advantage survived. |

---

## 1. Data

```
====================================================================================================
sym      rows first        last          study window (needs SMA200 + 20d slope)
SPY      8485 1993-01-29   2026-10-14    1993-12-13 -> 2026-10-14  (8265 sessions)
QQQ      6943 1999-03-10   2026-10-14    2000-01-21 -> 2026-10-14  (6723 sessions)
IWM      6635 2000-05-26   2026-10-14    2001-04-11 -> 2026-10-14  (6415 sessions)
EEM      5914 2003-04-14   2026-10-14    2004-02-27 -> 2026-10-14  (5694 sessions)
VIX      9266 1990-01-02   2026-10-14  

R = 2 x ATR(14) read on the signal day. Entry = next open. Long only,
one position at a time. Costs = ZERO. Open-at-end trades excluded from
trade stats. Equity curve risks 1% of equity per trade, marked daily.

====================================================================================================
```

Sources, provenance headers and the pull date are in `README.md` §2 and in the
comment block at the top of each `data/*.csv`.

---

## 2. Headline metrics for the three pre-registered rule sets

Two expectancy columns are shown and the difference matters:

- `E_form` is the pre-registered `p·b − (1−p)`. It measures expectancy **in units of
the average loss**, not in R — the two coincide only when every loss is exactly −1R.
For `M3` losses *are* always exactly −1R, so both columns are identical; for `M1`/`M2`
time-exits produce smaller losses, so `E_form` overstates. The identity is
`E_form = E_R / |avg_loss|`.
- `E_R` is the mean R per trade — the honest per-trade expectancy.

**These figures are gross of costs and assume stops fill exactly at the stop.**
Section 8 sizes both assumptions, and one cell (M1/EEM) turns negative once a
realistic round trip is charged.

```
(Shrp = strategy Sharpe, BHsh = buy-and-hold Sharpe over the same window)
M1   SPY     281    0   0.744   0.68   0.249   0.171   0.595   0.34   0.60      23   4.14    4     48.1   4.79     1.4%    4.9%   0.71   0.55
M2   SPY     110    0   0.591   1.03   0.201   0.186   0.492   0.69   0.98      95   5.26    4     20.4   1.98     0.6%    7.3%   0.32   0.55
M3   SPY      99    0   0.535   1.56   0.371   0.371   0.390   0.87   1.35      53   6.00    5     36.7   2.73     1.1%    6.0%   0.47   0.55
M1   QQQ     226    0   0.664   0.71   0.136   0.091   0.584   0.51   0.64      88   4.97    3     20.5   2.14     0.7%    4.8%   0.38   0.49
M2   QQQ      85    0   0.553   1.06   0.141   0.118   0.485   0.81   0.92     170   5.52    4     10.0   1.18     0.3%    4.3%   0.20   0.49
M3   QQQ     120    0   0.517   1.39   0.234   0.234   0.419   0.94   1.24     112   6.58    4     28.1   2.07     1.0%    6.3%   0.37   0.49
M1   IWM     201    0   0.667   0.70   0.136   0.082   0.587   0.50   0.57      70   4.83    4     16.4   2.04     0.6%    4.3%   0.36   0.40
M2   IWM      78    0   0.603   0.98   0.196   0.162   0.504   0.66   0.88      81   4.72    3     12.7   1.63     0.5%    5.7%   0.30   0.40
M3   IWM     124    0   0.444   1.36   0.048   0.048   0.423   1.25   1.22    2577   8.22    6      5.9   0.44     0.2%    9.0%   0.08   0.40
M1   EEM     158    0   0.633   0.59   0.005   0.003   0.630   0.58   0.60   55876   5.05    4      0.5   0.07     0.0%    5.6%   0.01   0.41
M2   EEM      59    0   0.525   1.09   0.098   0.082   0.479   0.90   0.96     380   5.47    5      4.8   0.66     0.2%    6.0%   0.13   0.41
M3   EEM     127    0   0.394   1.50  -0.016  -0.016   0.400   1.54   1.27   26207   9.68    9     -2.0  -0.14    -0.1%   22.0%  -0.03   0.41
```

```
stra sym   days in mkt     exposure    median risk     risk % of px
M1   SPY          750        8.8%         2.16%      1R = 2.16%
M2   SPY          575        6.8%         2.23%      1R = 2.23%
M3   SPY         1181       13.9%         3.13%      1R = 3.13%
M1   QQQ          655        9.4%         2.81%      1R = 2.81%
M2   QQQ          496        7.1%         3.10%      1R = 3.10%
M3   QQQ         1542       22.2%         3.71%      1R = 3.71%
M1   IWM          592        8.9%         3.09%      1R = 3.09%
M2   IWM          488        7.4%         3.25%      1R = 3.25%
M3   IWM         1502       22.6%         3.65%      1R = 3.65%
M1   EEM          447        7.6%         2.87%      1R = 2.87%
M2   EEM          333        5.6%         3.13%      1R = 3.13%
M3   EEM         1469       24.8%         3.55%      1R = 3.55%

A round-trip cost of c basis points of price costs the trade
c/100/(risk% of price) in R.  With costs set to ZERO in this study, the
per-trade expectancies above are the gross, pre-cost figures.
```

```

stra sym       n open       p      b  E_form     E_R      p*     b*     sd   n_req      L Lobs   totalR      t     CAGR   maxDD   Shrp   BHsh
(Shrp = strategy Sharpe, BHsh = buy-and-hold Sharpe over the same window)
M1   SPY     281    0   0.744   0.68   0.249   0.171   0.595   0.34   0.60      23   4.14    4     48.1   4.79     1.4%    4.9%   0.71   0.55
M2   SPY     110    0   0.591   1.03   0.201   0.186   0.492   0.69   0.98      95   5.26    4     20.4   1.98     0.6%    7.3%   0.32   0.55
M3   SPY      99    0   0.535   1.56   0.371   0.371   0.390   0.87   1.35      53   6.00    5     36.7   2.73     1.1%    6.0%   0.47   0.55
M1   QQQ     226    0   0.664   0.71   0.136   0.091   0.584   0.51   0.64      88   4.97    3     20.5   2.14     0.7%    4.8%   0.38   0.49
M2   QQQ      85    0   0.553   1.06   0.141   0.118   0.485   0.81   0.92     170   5.52    4     10.0   1.18     0.3%    4.3%   0.20   0.49
M3   QQQ     120    0   0.517   1.39   0.234   0.234   0.419   0.94   1.24     112   6.58    4     28.1   2.07     1.0%    6.3%   0.37   0.49
M1   IWM     201    0   0.667   0.70   0.136   0.082   0.587   0.50   0.57      70   4.83    4     16.4   2.04     0.6%    4.3%   0.36   0.40
M2   IWM      78    0   0.603   0.98   0.196   0.162   0.504   0.66   0.88      81   4.72    3     12.7   1.63     0.5%    5.7%   0.30   0.40
M3   IWM     124    0   0.444   1.36   0.048   0.048   0.423   1.25   1.22    2577   8.22    6      5.9   0.44     0.2%    9.0%   0.08   0.40
M1   EEM     158    0   0.633   0.59   0.005   0.003   0.630   0.58   0.60   55876   5.05    4      0.5   0.07     0.0%    5.6%   0.01   0.41
M2   EEM      59    0   0.525   1.09   0.098   0.082   0.479   0.90   0.96     380   5.47    5      4.8   0.66     0.2%    6.0%   0.13   0.41
M3   EEM     127    0   0.394   1.50  -0.016  -0.016   0.400   1.54   1.27   26207   9.68    9     -2.0  -0.14    -0.1%   22.0%  -0.03   0.41

exposure and the risk unit - both matter for reading the CAGR comparison
stra sym   days in mkt     exposure    median risk     risk % of px
M1   SPY          750        8.8%         2.16%      1R = 2.16%
M2   SPY          575        6.8%         2.23%      1R = 2.23%
M3   SPY         1181       13.9%         3.13%      1R = 3.13%
M1   QQQ          655        9.4%         2.81%      1R = 2.81%
M2   QQQ          496        7.1%         3.10%      1R = 3.10%
M3   QQQ         1542       22.2%         3.71%      1R = 3.71%
M1   IWM          592        8.9%         3.09%      1R = 3.09%
M2   IWM          488        7.4%         3.25%      1R = 3.25%
M3   IWM         1502       22.6%         3.65%      1R = 3.65%
M1   EEM          447        7.6%         2.87%      1R = 2.87%
M2   EEM          333        5.6%         3.13%      1R = 3.13%
M3   EEM         1469       24.8%         3.55%      1R = 3.55%

A round-trip cost of c basis points of price costs the trade
c/100/(risk% of price) in R.  With costs set to ZERO in this study, the
per-trade expectancies above are the gross, pre-cost figures.

buy and hold over the same window, for reference (not traded by the rules):
  SPY  price-only CAGR    8.9%  total-return CAGR   10.8%  max DD   56.5%  (dividend drag   2.0%)
  QQQ  price-only CAGR   10.1%  total-return CAGR   10.8%  max DD   83.0%  (dividend drag   0.7%)
  IWM  price-only CAGR    7.0%  total-return CAGR    8.4%  max DD   59.5%  (dividend drag   1.4%)
  EEM  price-only CAGR    7.7%  total-return CAGR    9.8%  max DD   67.2%  (dividend drag   2.1%)

====================================================================================================
```

**Reading it.** `M1` on SPY is the one clearly positive result: n = 281, p = 0.744,
E_R = +0.171R, total +48.1R, t = 4.79, against an `n_req` of only 23. Across the other
instruments the per-trade edge shrinks toward noise: M1/EEM has E_R = +0.003R with
`n_req` = 55,876. `M3` on EEM has a **negative** expectancy (E_R = −0.016R, t = −0.14)
and the worst drawdown in the table (22.0%). The sample-size column does its job:
every result with a large `n_req` relative to `n` also has a small |t|.

**The exposure column is essential to reading the CAGR column.** M1 on SPY is in the
market only **8.8%** of sessions and M3 tops out at 24.8%. The strategies make
0.0–1.4% CAGR because the capital sits idle most of the time, not because the edge is
absent — so the 7.0–10.8% buy-and-hold CAGR is not a like-for-like comparison. The
Sharpe column is the fair one, and on Sharpe only M1/SPY (0.71 vs 0.55) wins.

**The risk unit matters for costs.** 1R is 2.16% of price for M1/SPY. A round-trip
cost of c basis points of price costs the trade `c/100 ÷ 2.16` in R, so 5 bps ≈ 0.023R
and 10 bps ≈ 0.046R — against a gross edge of +0.171R that is 14% and 27% of it. Costs
are set to ZERO in this study (see `FINDINGS.md` §3.1), so every expectancy here is a
pre-cost figure.

---

## 3. Per-year results, with the losses kept in

Total R by entry year, with trade count and win rate. `-` means no signal that year.
**Read the minus signs — they are the point.**

```
====================================================================================================
total R by entry year, with n and win rate.  '-' = no trades that year.

M1
  year                SPY               QQQ               IWM               EEM
  1993     +0.8R n2 p1.00                 -                 -                 -
  1994     +1.3R n5 p0.80                 -                 -                 -
  1995     +2.6R n6 p0.83                 -                 -                 -
  1996    -3.2R n12 p0.50                 -                 -                 -
  1997    +5.4R n15 p0.87                 -                 -                 -
  1998     +3.0R n9 p0.89                 -                 -                 -
  1999    +2.5R n14 p0.79                 -                 -                 -
  2000     +1.6R n8 p0.62    -1.0R n7 p0.57                 -                 -
  2001                  -                 -    +0.6R n2 p1.00                 -
  2002                  -                 -    +1.2R n5 p0.80                 -
  2003     +1.7R n6 p0.83    +2.5R n9 p1.00    +3.0R n9 p0.89                 -
  2004    +2.1R n10 p0.90    +1.9R n9 p0.67    +1.3R n9 p0.67    -0.1R n8 p0.50
  2005    +0.7R n12 p0.75   -0.1R n14 p0.64   -1.1R n13 p0.62    -3.2R n9 p0.44
  2006     +2.2R n9 p0.67    +0.9R n8 p0.62   +1.1R n11 p0.73    -0.1R n9 p0.67
  2007    +1.1R n10 p0.80    +0.7R n9 p0.67    -0.3R n9 p0.56   +0.2R n12 p0.75
  2008                  -    -0.6R n2 p0.50    +0.2R n1 p1.00    +1.1R n3 p0.67
  2009     +1.8R n5 p0.80    +2.0R n8 p0.75    +1.7R n8 p0.75    -1.4R n4 p0.25
  2010     -1.0R n7 p0.57    -0.1R n8 p0.62    -0.3R n6 p0.50   -0.6R n12 p0.75
  2011     +0.3R n7 p0.71    -0.7R n9 p0.67    +1.4R n9 p0.67    +4.2R n9 p0.67
  2012    +3.5R n14 p0.64   +2.1R n13 p0.54   +0.0R n12 p0.58    +0.6R n5 p0.80
  2013     +2.1R n6 p0.83    +3.0R n8 p0.88    +2.0R n8 p0.75    -0.6R n6 p0.67
  2014    +2.0R n12 p0.75   +0.3R n11 p0.55    -0.9R n9 p0.56    +1.7R n6 p0.83
  2015    +0.7R n12 p0.67   +2.6R n15 p0.73    +0.5R n8 p0.75    -2.0R n2 p0.00
  2016     +1.8R n7 p0.57    -1.7R n7 p0.43    +1.0R n6 p0.83    +0.9R n7 p0.86
  2017     +3.9R n9 p1.00   +3.6R n11 p0.82   +1.5R n11 p0.73   +1.9R n11 p0.73
  2018    -2.2R n11 p0.55    -0.8R n8 p0.38    -2.2R n8 p0.38    -0.9R n4 p0.50
  2019     +1.4R n8 p0.62    -1.7R n9 p0.56    -0.2R n2 p0.50    +0.6R n7 p0.71
  2020     -0.0R n8 p0.75    +0.9R n7 p0.57    -0.9R n7 p0.57    -2.1R n4 p0.00
  2021    +4.8R n11 p0.82   +2.3R n11 p0.73   -0.1R n11 p0.45    +2.2R n8 p0.75
  2022     -0.8R n2 p0.50    -0.8R n2 p0.50                 -                 -
  2023    +0.3R n10 p0.50    +1.4R n9 p0.56    +0.4R n6 p0.67    -0.9R n6 p0.67
  2024    +4.0R n13 p0.92   +3.2R n12 p0.83   +1.9R n11 p0.64   -2.0R n12 p0.50
  2025     +1.7R n8 p0.88   +1.3R n11 p0.82    +2.3R n8 p0.88    +0.4R n7 p0.57
  2026    +1.9R n13 p0.77    -0.7R n9 p0.56   +2.4R n12 p0.75    +0.7R n7 p0.71

M2
  year                SPY               QQQ               IWM               EEM
  1994     -1.0R n1 p0.00                 -                 -                 -
  1996     +4.0R n8 p0.75                 -                 -                 -
  1997     +2.9R n4 p0.75                 -                 -                 -
  1998     +2.9R n5 p0.80                 -                 -                 -
  1999     -0.6R n2 p0.50                 -                 -                 -
  2000     -0.9R n3 p0.33    -1.0R n1 p0.00                 -                 -
  2001                  -                 -    +0.6R n1 p1.00                 -
  2002                  -                 -    +0.1R n3 p0.33                 -
  2003     +1.6R n2 p1.00    +2.2R n3 p1.00    +1.8R n2 p1.00                 -
  2004     -2.1R n3 p0.00    -0.2R n2 p0.50    +0.3R n2 p0.50    -0.1R n4 p0.50
  2005     -0.2R n5 p0.40    +0.7R n5 p0.40    -2.2R n4 p0.25    +0.1R n4 p0.50
  2006     +0.6R n3 p0.67    +0.4R n3 p0.67    -1.0R n1 p0.00    -0.9R n3 p0.33
  2007     +2.1R n6 p0.67    +0.9R n4 p0.50    -1.4R n3 p0.33    +0.8R n5 p0.40
  2009                  -    +1.7R n2 p1.00    +1.7R n2 p1.00    +2.4R n2 p1.00
  2010     -3.0R n3 p0.00    -3.0R n3 p0.00    +0.5R n3 p0.67    -3.0R n3 p0.00
  2011     -1.2R n3 p0.33    +0.5R n4 p0.50    +0.1R n4 p0.50    -1.1R n2 p0.00
  2012     -2.6R n4 p0.25    -1.4R n4 p0.25    +0.0R n4 p0.50    +0.8R n1 p1.00
  2013     +3.2R n5 p0.80    +3.9R n5 p1.00    +3.7R n5 p1.00    +0.3R n3 p0.67
  2014     -0.2R n7 p0.43    +1.8R n8 p0.62    -1.1R n3 p0.33    -2.0R n2 p0.00
  2015     +2.9R n3 p1.00    +1.7R n4 p0.75    +1.2R n4 p0.50    -1.0R n1 p0.00
  2016     +3.8R n3 p1.00    +1.9R n3 p0.67    +0.3R n4 p0.50    +2.8R n3 p1.00
  2017     +4.1R n6 p1.00    +1.4R n2 p1.00    +2.0R n7 p0.71    +3.3R n4 p1.00
  2018     -1.8R n4 p0.25    -1.7R n4 p0.25    +1.1R n5 p0.60    -1.5R n3 p0.33
  2019     -1.4R n4 p0.25    +1.3R n3 p0.67    -1.0R n1 p0.00    -2.6R n3 p0.00
  2020     +0.4R n2 p0.50    -0.9R n3 p0.33    +2.3R n5 p0.80    +0.1R n2 p0.50
  2021     +2.2R n6 p0.67    +1.9R n8 p0.62    +2.8R n5 p0.80    +1.0R n4 p0.50
  2022     -1.0R n1 p0.00    -1.0R n1 p0.00                 -                 -
  2023     -0.1R n2 p0.50    +0.1R n3 p0.33    -1.0R n1 p0.00                 -
  2024     +3.4R n5 p0.80    -0.8R n3 p0.33    +0.7R n4 p0.75    +2.3R n3 p0.67
  2025     -0.8R n4 p0.50    -0.2R n2 p0.50    +1.3R n1 p1.00    +0.9R n4 p0.75
  2026     +3.2R n6 p0.83    -0.3R n5 p0.60    -0.2R n4 p0.50    +2.2R n3 p1.00

M3
  year                SPY               QQQ               IWM               EEM
  1994     +2.8R n4 p0.75                 -                 -                 -
  1996     +0.3R n2 p0.50                 -                 -                 -
  1997     +2.9R n6 p0.50                 -                 -                 -
  1998     -4.0R n4 p0.00                 -                 -                 -
  1999     +2.8R n6 p0.67                 -                 -                 -
  2000     +4.6R n8 p0.62   -3.3R n13 p0.38                 -                 -
  2001                  -                 -    -3.0R n3 p0.00                 -
  2002                  -                 -    -5.3R n8 p0.12                 -
  2003                  -    +6.2R n5 p1.00    +3.3R n2 p1.00                 -
  2004     +2.5R n2 p1.00    -0.5R n5 p0.40    +1.4R n6 p0.50    +3.3R n7 p0.57
  2005     -1.0R n1 p0.00    +1.3R n4 p0.50    +2.6R n6 p0.67    +3.7R n7 p0.57
  2006     -1.0R n1 p0.00    -0.3R n4 p0.50    -1.8R n6 p0.33    -0.5R n8 p0.38
  2007     +2.3R n5 p0.60    +1.4R n5 p0.60    +0.2R n4 p0.50   -0.2R n11 p0.36
  2008                  -    -2.2R n4 p0.25    -2.0R n2 p0.00    -4.3R n6 p0.17
  2009     +2.5R n2 p1.00    +2.8R n2 p1.00    +2.7R n4 p0.75    +3.4R n4 p0.75
  2010     +0.2R n6 p0.50    +1.9R n5 p0.60    -1.4R n6 p0.33    -2.8R n9 p0.33
  2011     +1.4R n6 p0.50    +4.1R n6 p0.67    -2.4R n7 p0.29    -0.0R n5 p0.40
  2012     +1.0R n4 p0.50    -2.4R n7 p0.29    +2.3R n5 p0.60    -1.4R n6 p0.33
  2013     +2.0R n1 p1.00    +2.2R n1 p1.00    +1.5R n1 p1.00    -5.0R n5 p0.00
  2014     +3.3R n3 p0.67    +5.5R n5 p0.80    +0.0R n5 p0.40    -3.0R n5 p0.20
  2015     -0.8R n3 p0.33    +0.1R n2 p0.50    +1.1R n4 p0.50    -4.0R n4 p0.00
  2016     +1.2R n2 p0.50    +1.4R n4 p0.50    +2.4R n3 p0.67    +2.3R n6 p0.50
  2017                  -    +1.5R n1 p1.00    +1.4R n1 p1.00    +1.5R n1 p1.00
  2018     -0.2R n8 p0.38    -0.5R n6 p0.33    +0.4R n5 p0.40    -3.0R n3 p0.00
  2019     +2.6R n2 p1.00    +1.8R n3 p0.67    +2.1R n4 p0.75    +1.1R n3 p0.67
  2020     +0.7R n7 p0.43    -1.9R n9 p0.33    +1.9R n9 p0.44    -1.8R n7 p0.29
  2021     +1.5R n1 p1.00    +3.7R n6 p0.67   +3.0R n10 p0.60    +0.9R n6 p0.50
  2022     -1.4R n3 p0.33    -3.0R n3 p0.00                 -                 -
  2023     +1.8R n4 p0.50    +3.4R n4 p0.75    -5.5R n7 p0.14    -0.3R n6 p0.33
  2024     +5.0R n2 p1.00    +3.3R n5 p0.60    +4.9R n6 p0.67    +1.8R n6 p0.50
  2025     +2.6R n4 p0.50    +1.7R n5 p0.60    -0.9R n5 p0.40    +3.8R n5 p0.60
  2026     +1.1R n2 p0.50    +0.1R n6 p0.33    -3.0R n5 p0.20    +2.6R n7 p0.57

====================================================================================================
```

### 3b. The losing-year ledger

The direct answer to "is any rule set profitable in every year":

```
====================================================================================================
stra sym    years  losing     worst year (total R)    worst R
M1   SPY       31       5            1996 (-3.17R)      -3.17
M1   QQQ       25      10            2019 (-1.73R)      -1.73
M1   IWM       25       8            2018 (-2.16R)      -2.16
M1   EEM       22      11            2005 (-3.16R)      -3.16
M2   SPY       28      14            2010 (-3.00R)      -3.00
M2   QQQ       24      10            2010 (-3.00R)      -3.00
M2   IWM       24       7            2005 (-2.15R)      -2.15
M2   EEM       20       8            2010 (-3.00R)      -3.00
M3   SPY       27       6            1998 (-4.00R)      -4.00
M3   QQQ       25       8            2000 (-3.35R)      -3.35
M3   IWM       25       9            2023 (-5.46R)      -5.46
M3   EEM       22      12            2013 (-5.00R)      -5.00

====================================================================================================
```

**No strategy × instrument combination is green every year.** The best record is
M1 on SPY (5 losing years in 31); the worst are M2 on SPY (14 of 28) and M1 on EEM
(11 of 22). The worst single year in the study is **M3 on IWM in 2023 at −5.46R**,
then M3 on EEM in 2013 at −5.00R and M3 on SPY in 1998 at −4.00R.

---

## 4. Regime grid

Each day is classified two ways:

- **Trend state** — `close` vs `SMA(200)`, crossed with the 20-day sign of
`SMA(200)`: `UP_rising`, `UP_falling`, `DOWN_rising`, `DOWN_falling`.

- **Realised-vol tercile** — trailing 20-day realised vol, cut per instrument into
`LOW` / `MID` / `HIGH`.

A trade is assigned the regime of its **entry** day. The full per-instrument grid is
also in `out/regime_grid.csv` (155 cells).

### 4a. The full grid (strategy × instrument × trend × vol tercile)

```
====================================================================================================
Trend state from close vs SMA(200) and the 20-day sign of SMA(200).
Vol tercile from trailing 20-day realised vol, cut per instrument.
Trades are assigned the regime of their ENTRY day.

SPY  (vol tercile cuts: LOW<= 10.7 < MID <= 16.7 < HIGH, annualised %)
  strategy         regime    n       p       b        E   total_R
  M1               UP_rising|LOW  105   0.752    0.84    0.388    +23.47
  M1               UP_rising|MID  116   0.724    0.57    0.138    +12.44
  M1               UP_rising|HIGH   49   0.837    0.73    0.444    +14.81
  M1               UP_falling|LOW    1   0.000    0.00   -1.000     -0.31
  M1               UP_falling|MID    2   0.500    2.88    0.939     +0.50
  M1               UP_falling|HIGH    1   0.000    0.00   -1.000     -0.56
  M1               DOWN_rising|LOW    2   0.500    0.03   -0.484     -0.97
  M1               DOWN_rising|MID    2   0.500    0.11   -0.446     -0.89
  M1               DOWN_rising|HIGH    2   0.500    0.31   -0.345     -0.69
  M2               UP_rising|LOW   32   0.688    1.07    0.421    +10.82
  M2               UP_rising|MID   54   0.574    1.00    0.146     +7.48
  M2               UP_rising|HIGH   16   0.688    1.10    0.444     +7.11
  M2               DOWN_rising|LOW    1   0.000    0.00   -1.000     -1.00
  M2               DOWN_rising|MID    4   0.250    1.88   -0.280     -0.98
  M2               DOWN_rising|HIGH    3   0.000    0.00   -1.000     -3.00
  M3               UP_rising|MID   24   0.458    1.64    0.208     +5.00
  M3               UP_rising|HIGH   31   0.645    1.64    0.705    +21.86
  M3               UP_falling|MID    1   0.000    0.00   -1.000     -1.00
  M3               UP_falling|HIGH    1   1.000     inf      inf     +0.83
  M3               DOWN_rising|MID   10   0.400    1.15   -0.138     -1.38
  M3               DOWN_rising|HIGH   25   0.520    1.48    0.292     +7.30
  M3               DOWN_falling|MID    3   1.000     inf      inf     +5.15
  M3               DOWN_falling|HIGH    4   0.250    1.98   -0.254     -1.02

QQQ  (vol tercile cuts: LOW<= 14.8 < MID <= 23.4 < HIGH, annualised %)
  strategy         regime    n       p       b        E   total_R
  M1               UP_rising|LOW   97   0.732    0.79    0.308    +18.58
  M1               UP_rising|MID   86   0.628    0.66    0.043     +2.60
  M1               UP_rising|HIGH   22   0.682    0.56    0.063     +0.97
  M1               UP_falling|LOW    3   0.333    0.40   -0.533     -1.47
  M1               UP_falling|MID    5   0.800    1.37    0.897     +1.41
  M1               UP_falling|HIGH    3   0.667    5.17    3.112     +0.77
  M1               DOWN_rising|LOW    1   0.000    0.00   -1.000     -0.61
  M1               DOWN_rising|MID    5   0.400    0.83   -0.267     -1.33
  M1               DOWN_rising|HIGH    3   0.000    0.00   -1.000     -1.48
  M2               UP_rising|LOW   27   0.704    1.18    0.535    +11.08
  M2               UP_rising|MID   41   0.488    1.08    0.012     +0.41
  M2               UP_rising|HIGH   12   0.500    0.97   -0.014     -0.16
  M2               UP_falling|MID    1   1.000     inf      inf     +0.66
  M2               DOWN_rising|MID    3   0.000    0.00   -1.000     -3.00
  M2               DOWN_falling|LOW    1   1.000     inf      inf     +0.99
  M3               UP_rising|LOW    4   0.250    1.61   -0.346     -1.39
  M3               UP_rising|MID   47   0.532    1.47    0.316    +14.84
  M3               UP_rising|HIGH   27   0.519    1.34    0.212     +5.74
  M3               UP_falling|LOW    1   1.000     inf      inf     +1.92
  M3               UP_falling|MID    3   1.000     inf      inf     +3.63
  M3               UP_falling|HIGH    1   1.000     inf      inf     +1.33
  M3               DOWN_rising|LOW    1   0.000    0.00   -1.000     -1.00
  M3               DOWN_rising|MID   12   0.333    2.06    0.021     +0.26
  M3               DOWN_rising|HIGH   16   0.375    1.26   -0.153     -2.45
  M3               DOWN_falling|LOW    1   1.000     inf      inf     +1.06
  M3               DOWN_falling|MID    2   1.000     inf      inf     +1.95
  M3               DOWN_falling|HIGH    3   1.000     inf      inf     +2.55

IWM  (vol tercile cuts: LOW<= 16.1 < MID <= 22.1 < HIGH, annualised %)
  strategy         regime    n       p       b        E   total_R
  M1               UP_rising|LOW   84   0.655    0.63    0.065     +3.58
  M1               UP_rising|MID   68   0.676    0.98    0.337    +11.11
  M1               UP_rising|HIGH   23   0.609    0.76    0.070     +0.90
  M1               UP_falling|LOW    6   0.667    0.32   -0.121     -0.73
  M1               UP_falling|MID    7   0.857    0.22    0.049     +0.34
  M1               UP_falling|HIGH    6   0.667    1.45    0.636     +0.91
  M1               DOWN_rising|LOW    1   1.000     inf      inf     +0.26
  M1               DOWN_rising|MID    3   0.667    0.52    0.012     +0.03
  M1               DOWN_rising|HIGH    2   0.500    0.42   -0.292     -0.58
  M1               DOWN_falling|MID    1   1.000     inf      inf     +0.60
  M2               UP_rising|LOW   29   0.621    0.89    0.173     +4.34
  M2               UP_rising|MID   26   0.538    1.05    0.101     +2.30
  M2               UP_rising|HIGH   11   0.727    1.40    0.748     +4.74
  M2               UP_falling|LOW    2   0.500    0.61   -0.195     -0.39
  M2               UP_falling|MID    3   1.000     inf      inf     +2.01
  M2               UP_falling|HIGH    2   1.000     inf      inf     +1.56
  M2               DOWN_rising|LOW    2   0.000    0.00   -1.000     -1.39
  M2               DOWN_falling|MID    2   0.000    0.00   -1.000     -1.58
  M2               DOWN_falling|HIGH    1   1.000     inf      inf     +1.08
  M3               UP_rising|LOW   16   0.438    1.29    0.003     +0.05
  M3               UP_rising|MID   34   0.412    1.50    0.029     +1.00
  M3               UP_rising|HIGH   20   0.650    1.32    0.507    +10.14
  M3               UP_falling|MID    4   0.250    1.38   -0.406     -1.62
  M3               UP_falling|HIGH    4   0.750    1.52    0.894     +3.57
  M3               DOWN_rising|LOW    4   0.250    1.46   -0.386     -1.54
  M3               DOWN_rising|MID   13   0.462    1.40    0.110     +1.43
  M3               DOWN_rising|HIGH   16   0.375    1.12   -0.206     -3.30
  M3               DOWN_falling|LOW    1   0.000    0.00   -1.000     -1.00
  M3               DOWN_falling|MID    6   0.333    0.93   -0.358     -2.15
  M3               DOWN_falling|HIGH    6   0.333    1.68   -0.106     -0.64

EEM  (vol tercile cuts: LOW<= 16.4 < MID <= 22.1 < HIGH, annualised %)
  strategy         regime    n       p       b        E   total_R
  M1               UP_rising|LOW   56   0.589    0.74    0.023     +0.75
  M1               UP_rising|MID   43   0.651    0.60    0.040     +1.14
  M1               UP_rising|HIGH   38   0.711    0.44    0.022     +0.65
  M1               UP_falling|LOW    5   0.600    0.24   -0.257     -1.28
  M1               UP_falling|MID    5   0.800    0.38    0.102     +0.51
  M1               UP_falling|HIGH    3   0.333    1.12   -0.292     -0.27
  M1               DOWN_rising|MID    1   1.000     inf      inf     +0.24
  M1               DOWN_rising|HIGH    3   0.333    0.85   -0.382     -0.68
  M1               DOWN_falling|LOW    1   0.000    0.00   -1.000     -1.00
  M1               DOWN_falling|MID    1   1.000     inf      inf     +0.33
  M2               UP_rising|LOW   18   0.611    0.92    0.176     +2.92
  M2               UP_rising|MID   15   0.400    1.26   -0.096     -1.06
  M2               UP_rising|HIGH   18   0.444    1.12   -0.056     -0.87
  M2               UP_falling|MID    1   1.000     inf      inf     +0.76
  M2               UP_falling|HIGH    1   1.000     inf      inf     +0.99
  M2               DOWN_rising|MID    1   1.000     inf      inf     +0.07
  M2               DOWN_rising|HIGH    2   1.000     inf      inf     +2.04
  M2               DOWN_falling|LOW    1   0.000    0.00   -1.000     -1.00
  M2               DOWN_falling|MID    1   0.000    0.00   -1.000     -0.59
  M3               UP_rising|LOW   10   0.300    2.04   -0.087     -0.87
  M3               UP_rising|MID   24   0.458    1.84    0.302     +7.25
  M3               UP_rising|HIGH   39   0.410    1.37   -0.026     -1.03
  M3               UP_falling|LOW    1   0.000    0.00   -1.000     -1.00
  M3               UP_falling|MID    1   0.000    0.00   -1.000     -1.00
  M3               UP_falling|HIGH    2   0.500    1.09    0.047     +0.09
  M3               DOWN_rising|LOW    6   0.333    1.31   -0.229     -1.37
  M3               DOWN_rising|MID    7   0.714    1.91    1.076     +7.53
  M3               DOWN_rising|HIGH   16   0.438    1.11   -0.078     -1.24
  M3               DOWN_falling|LOW    6   0.000    0.00   -1.000     -6.00
  M3               DOWN_falling|MID   10   0.400    1.08   -0.169     -1.69
  M3               DOWN_falling|HIGH    5   0.200    1.35   -0.529     -2.65
```

### 4b. Pooled across all four instruments

```
Totals pool by summing R and n across instruments (valid); E_R = total_R/n.
stra trend state           n        p        E_R   total_R
M1   UP_rising           787    0.695      0.116    +91.00
M1   UP_falling           47    0.638     -0.004     -0.19
M1   DOWN_rising          25    0.440     -0.269     -6.71
M1   DOWN_falling          3    0.667     -0.023     -0.07
M2   UP_rising           299    0.582      0.164    +49.11
M2   UP_falling           10    0.900      0.559     +5.59
M2   DOWN_rising          16    0.250     -0.454     -7.26
M2   DOWN_falling          6    0.333     -0.183     -1.10
M3   UP_rising           276    0.489      0.227    +62.58
M3   UP_falling           19    0.579      0.355     +6.75
M3   DOWN_rising         126    0.429      0.034     +4.23
M3   DOWN_falling         47    0.404     -0.094     -4.42

stra vol tercile           n        p        E_R   total_R
M1   LOW                 363    0.686      0.112    +40.54
M1   MID                 347    0.680      0.084    +29.16
M1   HIGH                156    0.692      0.101    +15.79
M2   LOW                 114    0.640      0.245    +27.93
M2   MID                 152    0.513      0.043     +6.49
M2   HIGH                 66    0.591      0.204    +13.49
M3   LOW                  51    0.314     -0.219    -11.15
M3   MID                 201    0.473      0.195    +39.19
M3   HIGH                218    0.500      0.187    +40.74
```

### 4c. The losing cells, listed

```
  M1  SPY  UP_falling     vol LOW   n=1    E=-1.000 totalR=-0.31
  M1  SPY  UP_falling     vol HIGH  n=1    E=-1.000 totalR=-0.56
  M1  SPY  DOWN_rising    vol LOW   n=2    E=-0.484 totalR=-0.97
  M1  SPY  DOWN_rising    vol MID   n=2    E=-0.446 totalR=-0.89
  M1  SPY  DOWN_rising    vol HIGH  n=2    E=-0.345 totalR=-0.69
  M1  SPY  UP_falling     vol ALL   n=4    E=-0.249 totalR=-0.38
  M1  SPY  DOWN_rising    vol ALL   n=6    E=-0.425 totalR=-2.55
  M2  SPY  DOWN_rising    vol LOW   n=1    E=-1.000 totalR=-1.00
  M2  SPY  DOWN_rising    vol MID   n=4    E=-0.280 totalR=-0.98
  M2  SPY  DOWN_rising    vol HIGH  n=3    E=-1.000 totalR=-3.00
  M2  SPY  DOWN_rising    vol ALL   n=8    E=-0.658 totalR=-4.98
  M3  SPY  UP_falling     vol MID   n=1    E=-1.000 totalR=-1.00
  M3  SPY  DOWN_rising    vol MID   n=10   E=-0.138 totalR=-1.38
  M3  SPY  DOWN_falling   vol HIGH  n=4    E=-0.254 totalR=-1.02
  M3  SPY  UP_falling     vol ALL   n=2    E=-0.085 totalR=-0.17
  M1  QQQ  UP_falling     vol LOW   n=3    E=-0.533 totalR=-1.47
  M1  QQQ  DOWN_rising    vol LOW   n=1    E=-1.000 totalR=-0.61
  M1  QQQ  DOWN_rising    vol MID   n=5    E=-0.267 totalR=-1.33
  M1  QQQ  DOWN_rising    vol HIGH  n=3    E=-1.000 totalR=-1.48
  M1  QQQ  DOWN_rising    vol ALL   n=9    E=-0.523 totalR=-3.42
  M2  QQQ  UP_rising      vol HIGH  n=12   E=-0.014 totalR=-0.16
  M2  QQQ  DOWN_rising    vol MID   n=3    E=-1.000 totalR=-3.00
  M2  QQQ  DOWN_rising    vol ALL   n=3    E=-1.000 totalR=-3.00
  M3  QQQ  UP_rising      vol LOW   n=4    E=-0.346 totalR=-1.39
  M3  QQQ  DOWN_rising    vol LOW   n=1    E=-1.000 totalR=-1.00
  M3  QQQ  DOWN_rising    vol HIGH  n=16   E=-0.153 totalR=-2.45
  M3  QQQ  DOWN_rising    vol ALL   n=29   E=-0.110 totalR=-3.19
  M1  IWM  UP_falling     vol LOW   n=6    E=-0.121 totalR=-0.73
  M1  IWM  DOWN_rising    vol HIGH  n=2    E=-0.292 totalR=-0.58
  M1  IWM  DOWN_rising    vol ALL   n=6    E=-0.049 totalR=-0.29
  M2  IWM  UP_falling     vol LOW   n=2    E=-0.195 totalR=-0.39
  M2  IWM  DOWN_rising    vol LOW   n=2    E=-1.000 totalR=-1.39
  M2  IWM  DOWN_falling   vol MID   n=2    E=-1.000 totalR=-1.58
  M2  IWM  DOWN_rising    vol ALL   n=2    E=-1.000 totalR=-1.39
  M2  IWM  DOWN_falling   vol ALL   n=3    E=-0.211 totalR=-0.50
  M3  IWM  UP_falling     vol MID   n=4    E=-0.406 totalR=-1.62
  M3  IWM  DOWN_rising    vol LOW   n=4    E=-0.386 totalR=-1.54
  M3  IWM  DOWN_rising    vol HIGH  n=16   E=-0.206 totalR=-3.30
  M3  IWM  DOWN_falling   vol LOW   n=1    E=-1.000 totalR=-1.00
  M3  IWM  DOWN_falling   vol MID   n=6    E=-0.358 totalR=-2.15
  M3  IWM  DOWN_falling   vol HIGH  n=6    E=-0.106 totalR=-0.64
  M3  IWM  DOWN_rising    vol ALL   n=33   E=-0.103 totalR=-3.41
  M3  IWM  DOWN_falling   vol ALL   n=13   E=-0.291 totalR=-3.78
  M1  EEM  UP_falling     vol LOW   n=5    E=-0.257 totalR=-1.28
  M1  EEM  UP_falling     vol HIGH  n=3    E=-0.292 totalR=-0.27
  M1  EEM  DOWN_rising    vol HIGH  n=3    E=-0.382 totalR=-0.68
  M1  EEM  DOWN_falling   vol LOW   n=1    E=-1.000 totalR=-1.00
  M1  EEM  UP_falling     vol ALL   n=13   E=-0.111 totalR=-1.04
  M1  EEM  DOWN_rising    vol ALL   n=4    E=-0.188 totalR=-0.45
  M1  EEM  DOWN_falling   vol ALL   n=2    E=-0.333 totalR=-0.67
  M2  EEM  UP_rising      vol MID   n=15   E=-0.096 totalR=-1.06
  M2  EEM  UP_rising      vol HIGH  n=18   E=-0.056 totalR=-0.87
  M2  EEM  DOWN_falling   vol LOW   n=1    E=-1.000 totalR=-1.00
  M2  EEM  DOWN_falling   vol MID   n=1    E=-1.000 totalR=-0.59
  M2  EEM  DOWN_falling   vol ALL   n=2    E=-1.000 totalR=-1.59
  M3  EEM  UP_rising      vol LOW   n=10   E=-0.087 totalR=-0.87
  M3  EEM  UP_rising      vol HIGH  n=39   E=-0.026 totalR=-1.03
  M3  EEM  UP_falling     vol LOW   n=1    E=-1.000 totalR=-1.00
  M3  EEM  UP_falling     vol MID   n=1    E=-1.000 totalR=-1.00
  M3  EEM  DOWN_rising    vol LOW   n=6    E=-0.229 totalR=-1.37
  M3  EEM  DOWN_rising    vol HIGH  n=16   E=-0.078 totalR=-1.24
  M3  EEM  DOWN_falling   vol LOW   n=6    E=-1.000 totalR=-6.00
  M3  EEM  DOWN_falling   vol MID   n=10   E=-0.169 totalR=-1.69
  M3  EEM  DOWN_falling   vol HIGH  n=5    E=-0.529 totalR=-2.65
  M3  EEM  UP_falling     vol ALL   n=4    E=-0.477 totalR=-1.91
  M3  EEM  DOWN_falling   vol ALL   n=21   E=-0.492 totalR=-10.34

Total negative cells: 66

====================================================================================================
```

**What the regime data says.**

- `UP_rising` — price above a rising 200-day average — is the only trend state where
all three rules make money (+91.0R, +49.1R, +62.6R pooled). Essentially all the profit
in this study is here.
- `DOWN_falling` loses for all three rules (−0.1R, −1.1R, −4.4R pooled).
- `DOWN_rising` (price below a rising average — a bounce inside a downtrend) is the
worst trap for the two reversion rules: M1 −6.7R and M2 −7.3R pooled, with M2 winning
only 25% of them.
- By vol tercile all three rules are positive except **M3 in LOW vol** (−11.2R pooled,
p = 0.314, n = 51): dip-buying a quiet market gives back more than it takes.
- **66 of 155** strategy × instrument × trend × vol cells have negative expectancy.

---

## 5. The volatility-premium proxy

**This is a proxy, not an option P&L.** VIX is a 30-day constant-maturity implied-vol
index on the S&P 500; it is not the implied vol of any particular instrument, and a
21-day realised move is not the P&L of a short option position. Full statement of
limits in `FINDINGS.md` §2.

```
====================================================================================================
PROXY, not an option P&L.  VIX is a 30-day constant-maturity implied-vol
index on the S&P 500: it is not the IV of any traded instrument, and a
realised move is not the P&L of a short option position.  Collect
VIX/sqrt(252)*sqrt(21) in vol points at entry, pay the realised ABSOLUTE
move over the next 21 sessions.  R = payoff / (2 * collected), so a move
beyond 3x the implied move loses more than 1R.  Overlapping windows (every
session) give each year enough samples; the every-21st-session subset is
reported separately for independence.

as specified : n=8464 p=0.8332 b=1.458 E_formula=+1.0477 E_R=+0.1934R p*=0.4069 b*=0.2002 totalR=+1637.2
               E_formula is inflated: it counts expectancy in units of the
               average loss (here 0.185R), and this payoff has a fat left
               tail, so the honest per-trade figure is E_R = +0.1934R
fair strike  : n=8464 p=0.7092 b=1.119 E_R=+0.1158R totalR=+979.9   <- the same series with the sqrt(2/pi) artifact removed
               (collecting the 1-sigma move and paying the realised ABSOLUTE
               move guarantees a positive mean on its own, because the mean
               absolute value of a normal is sqrt(2/pi) = 0.798, not 1.)
mean VRP (VIX minus forward 21-day realised vol) = +3.62 vol points
share of windows with VIX above subsequent realised vol = 82.9%
worst single trade: R=-3.07 on 2020-02-20 (VIX 15.6, implied move 4.49%, realised abs move 32.10%)
best  single trade: R=+0.50 on 1993-04-07 (VIX 13.6, realised abs move 0.00%)

====================================================================================================
```

**The structural artifact, stated plainly.** As pre-registered, the trade collects
the 1-sigma move and pays the realised absolute move. That is biased positive on its
own, because the mean absolute value of a standard normal is √(2/π) ≈ 0.798, not 1 —
so the payoff carries a built-in positive drift that has nothing to do with option
selling. Hence E_R = +0.1934R and **zero losing years**. The `fair strike` line in the
block above removes the artifact by collecting the fair straddle value (0.798 ×
implied); that is the version to trust.

### 5a. Per calendar year

```
====================================================================================================
year       n       p       b    E_form      E_R       p*   total_R   mean_VRP    worst_R
1993     234   0.974   12.91    12.552    0.316    0.072     +73.8      +3.87      -0.06
1994     252   0.893    2.90     2.485    0.230    0.256     +57.9      +3.48      -0.35
1995     252   0.698    2.67     1.563    0.141    0.272     +35.6      +3.57      -0.28
1996     254   0.768    1.56     0.966    0.166    0.391     +42.1      +3.75      -0.73
1997     253   0.802    1.36     0.896    0.168    0.423     +42.4      +2.74      -0.77
1998     252   0.774    2.03     1.345    0.166    0.330     +41.8      +5.14      -0.56
1999     252   0.901    2.14     1.831    0.244    0.318     +61.4      +5.71      -0.31
2000     252   0.841    1.90     1.443    0.221    0.344     +55.8      +0.32      -0.55
2001     248   0.734    1.26     0.658    0.155    0.443     +38.5      +5.28      -0.95
2002     252   0.730    1.45     0.789    0.150    0.408     +37.9      +1.91      -0.74
2003     252   0.845    3.08     2.451    0.225    0.245     +56.7      +6.70      -0.33
2004     252   0.913    2.04     1.774    0.237    0.329     +59.8      +4.34      -0.37
2005     252   0.861    3.00     2.442    0.220    0.250     +55.5      +2.62      -0.27
2006     251   0.916    2.57     2.275    0.245    0.280     +61.6      +3.26      -0.30
2007     251   0.757    1.79     1.114    0.163    0.358     +40.9      +1.91      -0.51
2008     253   0.798    0.71     0.362    0.147    0.586     +37.2      -2.33      -1.59
2009     252   0.877    1.62     1.299    0.220    0.381     +55.4      +7.84      -0.38
2010     252   0.845    1.55     1.158    0.174    0.392     +43.8      +6.17      -0.71
2011     252   0.893    0.66     0.479    0.196    0.604     +49.4      +3.33      -1.29
2012     250   0.904    2.71     2.353    0.222    0.270     +55.5      +5.16      -0.39
2013     252   0.857    2.45     1.957    0.192    0.290     +48.3      +3.38      -0.35
2014     252   0.841    2.29     1.765    0.224    0.304     +56.4      +3.20      -0.49
2015     252   0.810    1.36     0.907    0.218    0.424     +54.9      +1.69      -0.68
2016     252   0.933    4.36     3.997    0.251    0.187     +63.1      +4.44      -0.16
2017     251   0.817    1.42     0.974    0.175    0.414     +43.9      +4.36      -0.73
2018     251   0.801    0.99     0.592    0.159    0.503     +39.9      +0.56      -0.82
2019     252   0.802    2.45     1.765    0.151    0.290     +38.0      +4.20      -0.27
2020     253   0.834    0.32     0.097    0.078    0.760     +19.7      +2.60      -3.07
2021     252   0.905    2.44     2.111    0.259    0.291     +65.4      +6.81      -0.44
2022     251   0.725    1.33     0.691    0.124    0.429     +31.2      +1.68      -0.56
2023     250   0.772    1.76     1.128    0.157    0.363     +39.2      +4.27      -0.39
2024     252   0.810    1.87     1.322    0.166    0.349     +41.9      +3.19      -0.43
2025     250   0.868    1.36     1.052    0.199    0.423     +49.8      +3.22      -0.46
2026     176   0.841    2.15     1.645    0.240    0.318     +42.2      +5.45      -0.29

losing years: 0 of 34  (none)
worst year: 2020 at +19.7R (253 windows)

====================================================================================================
```

### 5b. Per regime

```
====================================================================================================
vol tercile cuts on SPY: LOW<= 10.7 < MID <= 16.7 < HIGH
trend            vol          n       p       b    E_form      E_R   total_R   mean_VRP
UP_rising        LOW       2500   0.846    1.86     1.423    0.206    +515.5      +2.66
UP_rising        MID       2252   0.849    1.14     0.818    0.192    +431.9      +3.84
UP_rising        HIGH      1087   0.845    1.72     1.293    0.202    +219.8      +5.15
UP_falling       LOW        100   0.910    3.08     2.714    0.256     +25.6      +4.41
UP_falling       MID        105   0.914    2.27     1.991    0.227     +23.8      +4.28
UP_falling       HIGH       130   0.846    1.78     1.350    0.157     +20.4      +6.14
DOWN_rising      LOW         53   0.887    4.82     4.163    0.189     +10.0      +2.37
DOWN_rising      MID        183   0.727    1.79     1.030    0.167     +30.6      +5.26
DOWN_rising      HIGH       333   0.781    1.63     1.051    0.186     +61.9      +3.14
DOWN_falling     LOW         18   0.611    1.44     0.492    0.047      +0.8      +3.39
DOWN_falling     MID        213   0.695    0.91     0.328    0.090     +19.3      +2.36
DOWN_falling     HIGH      1271   0.784    1.32     0.819    0.163    +207.3      +3.57

non-overlapping subset (every 21st session): n=404 p=0.8540 b=1.568 E=+1.1934R totalR=+79.4

====================================================================================================
```

### 5c. The fair-strike variant — the honest both-sides answer

```
====================================================================================================
Collect the expected absolute move (0.798 x implied) instead of the
1-sigma move.  Now the payoff is unbiased and the only edge left is
whether VIX really exceeded the vol that followed.
year       n       p       b       E_R   total_R   mean_VRP    worst_R
1993     234   0.919    3.24     0.269     +62.9      +3.87      -0.20
1994     252   0.750    1.90     0.161     +40.7      +3.48      -0.56
1995     252   0.544    1.35     0.051     +12.7      +3.57      -0.48
1996     254   0.626    1.15     0.081     +20.6      +3.75      -1.04
1997     253   0.640    1.15     0.084     +21.1      +2.74      -1.09
1998     252   0.615    1.32     0.081     +20.5      +5.14      -0.83
1999     252   0.821    1.36     0.179     +45.1      +5.71      -0.52
2000     252   0.754    1.22     0.151     +38.0      +0.32      -0.81
2001     248   0.629    0.92     0.068     +16.8      +5.28      -1.32
2002     252   0.651    0.86     0.062     +15.6      +1.91      -1.05
2003     252   0.734    1.61     0.155     +39.1      +6.70      -0.54
2004     252   0.794    1.62     0.171     +43.0      +4.34      -0.59
2005     252   0.722    1.77     0.149     +37.6      +2.62      -0.47
2006     251   0.793    1.82     0.181     +45.4      +3.26      -0.50
2007     251   0.649    1.06     0.078     +19.5      +1.91      -0.77
2008     253   0.715    0.57     0.058     +14.6      -2.33      -2.12
2009     252   0.774    1.23     0.149     +37.6      +7.84      -0.61
2010     252   0.679    1.22     0.091     +23.0      +6.17      -1.01
2011     252   0.734    0.92     0.119     +30.0      +3.33      -1.74
2012     250   0.776    1.74     0.152     +37.9      +5.16      -0.61
2013     252   0.690    1.57     0.114     +28.6      +3.38      -0.57
2014     252   0.742    1.38     0.154     +38.7      +3.20      -0.74
2015     252   0.770    0.82     0.147     +36.9      +1.69      -0.98
2016     252   0.817    2.26     0.187     +47.2      +4.44      -0.33
2017     251   0.725    0.88     0.093     +23.2      +4.36      -1.04
2018     251   0.673    0.84     0.073     +18.2      +0.56      -1.15
2019     252   0.587    1.44     0.062     +15.7      +4.20      -0.47
2020     253   0.719    0.33    -0.029      -7.3      +2.60      -3.98
2021     252   0.806    1.70     0.199     +50.0      +6.81      -0.68
2022     251   0.578    0.93     0.029      +7.4      +1.68      -0.83
2023     250   0.608    1.23     0.070     +17.5      +4.27      -0.61
2024     252   0.639    1.28     0.082     +20.6      +3.19      -0.67
2025     250   0.700    1.36     0.123     +30.8      +3.22      -0.71
2026     176   0.773    1.24     0.174     +30.6      +5.45      -0.49

FAIR-STRIKE losing years: 1 of 34  (2020)
FAIR-STRIKE worst year: 2020 at -7.3R
FAIR-STRIKE worst single trade: R=-3.98 on 2020-02-20 (VIX 15.6, implied expected abs move 3.58%, realised 32.10%)

This is the honest answer to "is selling premium worth it?": on average
the premium is real, but it is not free - the loss years and the single
worst window above are the price of it.

====================================================================================================
```

**Answering the question with data.**

- The variance risk premium is real on average: mean VRP is **+3.62 vol points** and
VIX exceeded the vol that followed in **82.9%** of 21-day windows.
- It is negative in exactly **one** calendar year, **2008 (−2.33 vol points)** — the
year the premium was most expensive to be short. The fair-strike series still scrapes
+14.6R in 2008, because the *ratio* of realised to implied, not the difference, sets
the payoff; the year that actually breaks is **2020**.
- **Worst single trade:** the window entered **2020-02-20** — VIX 15.6, implied 21-day
move 4.49% (fair strike 3.58%), realised **32.10%**. That is R = **−3.98** on a stake
whose maximum gain is +0.5R: one window gave back roughly eight typical wins.
- **Worst year:** 2020, the only losing year for the fair-strike series, at **−7.3R**.
- So: selling premium earns in most years and is destroyed by the onset of a crisis —
exactly the shape practitioners warn about, and the shape this proxy can show even
though it cannot price a real option book.
- Robustness: the every-21st-session (non-overlapping) subset agrees — n = 404,
p = 0.854, E_form = +1.193, total +79.4R — so the result is not an artefact of
overlapping windows.

---

## 6. Task 5 — does parameter fishing manufacture an edge?

Two grids were searched on the M1 rule family (RSI threshold × holding period), with
the first 70% of sessions in-sample and the last 30% held out. The held-out data was
touched **once**, on the in-sample winner.

```
====================================================================================================
Pre-registered M1 is RSI(2)<10 with a 5-day cap.  Here we deliberately
search instead.  First 70% of sessions = in-sample, last 30% = held out.
The in-sample winner is then evaluated once on the held-out data.

GRID-A GRID - SPY: 30 combinations, in-sample 1993-01-29 -> 2016-08-29, held-out 2016-08-29 -> 2026-10-14
RSI<   hold    n_is     p_is     b_is      E_is   totR_is | n_oos    p_oos    b_oos     E_oos
5      2         85    0.647     1.28     0.473      14.1 |    53    0.642     0.97     0.263
5      3         83    0.651     1.20     0.430      15.6 |    49    0.673     0.74     0.170
5      5         82    0.707     1.09     0.480      19.8 |    49    0.755     0.62     0.225
5      8         81    0.728     0.97     0.436      19.5 |    49    0.755     0.63     0.231
5      10        81    0.728     0.97     0.436      19.5 |    49    0.755     0.63     0.231
10     2        199    0.603     0.95     0.174      14.3 |   104    0.587     0.86     0.089
10     3        188    0.654     0.89     0.238      22.8 |   100    0.700     0.79     0.250
10     5        184    0.739     0.71     0.267      31.8 |    97    0.753     0.62     0.219
10     8        182    0.747     0.67     0.248      30.7 |    97    0.753     0.63     0.228
10     10       182    0.747     0.67     0.248      30.7 |    97    0.753     0.63     0.228
15     2        308    0.581     0.88     0.091      12.3 |   152    0.592     0.91     0.130
15     3        289    0.640     0.85     0.187      27.8 |   147    0.707     0.87     0.320
15     5        276    0.717     0.65     0.184      33.9 |   140    0.757     0.64     0.241
15     8        274    0.737     0.61     0.185      35.6 |   139    0.763     0.65     0.256
15     10       274    0.737     0.61     0.185      35.6 |   139    0.763     0.65     0.256
20     2        400    0.585     0.87     0.093      16.7 |   183    0.574     0.87     0.076
20     3        361    0.615     0.78     0.095      18.6 |   170    0.671     0.74     0.166
20     5        344    0.683     0.61     0.100      24.1 |   159    0.736     0.58     0.162
20     8        343    0.703     0.59     0.116      28.3 |   159    0.748     0.57     0.175
20     10       343    0.703     0.59     0.116      28.3 |   159    0.748     0.57     0.175
25     2        481    0.586     0.85     0.087      18.5 |   231    0.589     0.82     0.070
25     3        433    0.624     0.74     0.082      19.9 |   210    0.686     0.63     0.121
25     5        407    0.683     0.61     0.099      27.4 |   199    0.724     0.59     0.147
25     8        404    0.693     0.59     0.105      29.5 |   198    0.742     0.54     0.146
25     10       404    0.693     0.60     0.106      29.6 |   198    0.742     0.54     0.146
30     2        557    0.576     0.81     0.043      10.8 |   277    0.606     0.78     0.077
30     3        501    0.625     0.66     0.036      10.5 |   250    0.676     0.65     0.113
30     5        469    0.665     0.57     0.045      14.2 |   234    0.726     0.59     0.156
30     8        466    0.680     0.55     0.057      18.5 |   233    0.738     0.55     0.146
30     10       466    0.680     0.56     0.058      18.6 |   233    0.738     0.56     0.151

  in-sample E distribution over 30 tried: best +0.480 | median +0.116 | worst +0.036
  in-sample positive-E combinations: 30 of 30 (100%)
  Bonferroni bar for m=30 at alpha=0.05: per-test alpha=0.001667, critical |t| = 3.144
  combinations clearing the bar in-sample: 9 of 30
  of those, still positive out-of-sample: 9 of 9

  --- the winner, in-sample vs held out ---
  best in-sample: RSI<5 hold=5 | IS  n=82 p=0.707 b=1.09 E=+0.480 totalR=+19.8
  same rule held out:                    | OOS n=49 p=0.755 b=0.62 E=+0.225 totalR=+9.6
  expectancy change IS -> OOS: -0.255R (-53% of the in-sample value)
  VERDICT: the edge SURVIVES the holdout

  --- tuned winner vs the PRE-REGISTERED default (RSI<10 hold=5) ---
  in-sample, the search beat the default by +0.213R per trade
  out-of-sample, the same search beat the default by +0.006R per trade
  the tuned advantage retained: 3% of what it looked like in-sample
  IS  default E=+0.267  winner E=+0.480
  OOS default E=+0.219  winner E=+0.225

GRID-B GRID - QQQ: 56 combinations, in-sample 1999-03-10 -> 2018-07-02, held-out 2018-07-02 -> 2026-10-14
RSI<   hold    n_is     p_is     b_is      E_is   totR_is | n_oos    p_oos    b_oos     E_oos
5      2         82    0.573     1.22     0.270       8.1 |    38    0.526     1.25     0.184
5      3         79    0.646     0.82     0.173       7.7 |    37    0.568     1.09     0.187
5      4         77    0.649     0.78     0.157       7.4 |    37    0.703     0.86     0.306
5      5         77    0.662     0.76     0.165       7.9 |    37    0.730     0.84     0.340
5      8         76    0.671     0.77     0.188       8.7 |    37    0.730     0.88     0.371
5      10        76    0.671     0.77     0.187       8.8 |    37    0.730     0.88     0.371
5      15        76    0.671     0.77     0.187       8.8 |    37    0.730     0.88     0.371
10     2        167    0.527     1.09     0.102       6.5 |    79    0.570     0.78     0.012
10     3        158    0.614     0.94     0.193      15.1 |    74    0.581     0.85     0.073
10     4        154    0.662     0.73     0.148      14.4 |    74    0.622     0.73     0.076
10     5        152    0.664     0.71     0.135      13.8 |    74    0.662     0.72     0.136
10     8        151    0.695     0.65     0.149      15.9 |    74    0.662     0.74     0.152
10     10       151    0.695     0.65     0.149      16.1 |    74    0.662     0.74     0.152
10     15       151    0.695     0.65     0.149      16.1 |    74    0.662     0.74     0.152
15     2        241    0.523     1.08     0.086       8.4 |   123    0.545     0.91     0.040
15     3        224    0.607     0.90     0.156      18.2 |   115    0.643     0.96     0.261
15     4        214    0.645     0.77     0.143      18.7 |   110    0.682     0.79     0.217
15     5        209    0.651     0.73     0.126      17.3 |   108    0.704     0.72     0.209
15     8        208    0.668     0.71     0.146      20.0 |   107    0.710     0.75     0.242
15     10       208    0.668     0.71     0.146      20.1 |   107    0.710     0.75     0.242
15     15       208    0.668     0.71     0.146      20.1 |   107    0.710     0.75     0.242
20     2        314    0.541     0.98     0.071       9.4 |   169    0.568     0.84     0.043
20     3        285    0.600     0.86     0.114      17.2 |   156    0.647     0.79     0.162
20     4        269    0.632     0.75     0.107      17.5 |   148    0.709     0.65     0.170
20     5        263    0.646     0.71     0.103      17.4 |   146    0.719     0.63     0.174
20     8        262    0.660     0.71     0.129      21.5 |   143    0.727     0.64     0.196
20     10       262    0.660     0.71     0.131      21.9 |   143    0.727     0.64     0.196
20     15       262    0.660     0.71     0.131      21.9 |   143    0.727     0.64     0.196
25     2        387    0.574     0.96     0.122      18.9 |   192    0.573     0.81     0.036
25     3        342    0.594     0.82     0.078      13.8 |   174    0.649     0.74     0.130
25     4        324    0.651     0.68     0.095      18.9 |   164    0.695     0.62     0.127
25     5        319    0.668     0.64     0.098      20.3 |   162    0.704     0.61     0.135
25     8        315    0.676     0.64     0.111      22.8 |   159    0.711     0.62     0.153
25     10       315    0.676     0.65     0.113      23.1 |   159    0.711     0.62     0.153
25     15       315    0.676     0.65     0.113      23.1 |   159    0.711     0.62     0.153
30     2        448    0.565     0.91     0.076      13.8 |   223    0.601     0.83     0.097
30     3        402    0.600     0.76     0.056      11.7 |   204    0.672     0.73     0.163
30     4        379    0.639     0.65     0.054      12.7 |   194    0.701     0.61     0.131
30     5        373    0.657     0.61     0.059      14.3 |   192    0.714     0.60     0.140
30     8        368    0.666     0.61     0.072      17.4 |   189    0.720     0.61     0.155
30     10       368    0.666     0.61     0.074      17.8 |   189    0.720     0.61     0.158
30     15       368    0.666     0.61     0.074      17.8 |   189    0.720     0.61     0.158
35     2        495    0.554     0.86     0.028       5.8 |   251    0.614     0.70     0.045
35     3        448    0.592     0.75     0.038       8.7 |   224    0.656     0.65     0.082
35     4        422    0.630     0.67     0.052      12.9 |   214    0.692     0.56     0.081
35     5        414    0.647     0.62     0.051      13.2 |   211    0.716     0.53     0.095
35     8        408    0.657     0.62     0.065      16.6 |   208    0.721     0.54     0.107
35     10       408    0.657     0.62     0.066      17.0 |   208    0.721     0.54     0.109
35     15       408    0.657     0.62     0.066      17.0 |   208    0.721     0.54     0.109
40     2        545    0.569     0.82     0.034       7.7 |   279    0.620     0.69     0.049
40     3        493    0.615     0.72     0.056      14.2 |   252    0.659     0.66     0.093
40     4        461    0.644     0.65     0.062      16.8 |   241    0.693     0.58     0.094
40     5        452    0.666     0.59     0.060      17.2 |   238    0.710     0.55     0.104
40     8        445    0.672     0.59     0.069      19.5 |   234    0.718     0.55     0.116
40     10       445    0.672     0.59     0.070      19.8 |   234    0.718     0.56     0.118
40     15       445    0.672     0.59     0.070      19.8 |   234    0.718     0.56     0.118

  in-sample E distribution over 56 tried: best +0.270 | median +0.107 | worst +0.028
  in-sample positive-E combinations: 56 of 56 (100%)
  Bonferroni bar for m=56 at alpha=0.05: per-test alpha=0.000893, critical |t| = 3.322
  combinations clearing the bar in-sample: 0 of 56
  of those, still positive out-of-sample: 0 of 0

  --- the winner, in-sample vs held out ---
  best in-sample: RSI<5 hold=2 | IS  n=82 p=0.573 b=1.22 E=+0.270 totalR=+8.1
  same rule held out:                    | OOS n=38 p=0.526 b=1.25 E=+0.184 totalR=+3.1
  expectancy change IS -> OOS: -0.086R (-32% of the in-sample value)
  VERDICT: the edge SURVIVES the holdout

  --- tuned winner vs the PRE-REGISTERED default (RSI<10 hold=5) ---
  in-sample, the search beat the default by +0.135R per trade
  out-of-sample, the same search beat the default by +0.048R per trade
  the tuned advantage retained: 36% of what it looked like in-sample
  IS  default E=+0.135  winner E=+0.270
  OOS default E=+0.136  winner E=+0.184

====================================================================================================
```

### 6b. The conclusion, stated plainly

```
====================================================================================================
Grid A searched 30 M1 variants on SPY; grid B searched 56 on QQQ.
Grid A best in-sample: RSI<5 hold=5 at E=+0.480R
  held out, the same combination scores E=+0.225R
Grid B best in-sample: RSI<5 hold=2 at E=+0.270R
  held out, the same combination scores E=+0.184R
Bonferroni grid A: m=30 -> |t|>3.144; 9 cleared, 9 of those held up
Bonferroni grid B: m=56 -> |t|>3.322; 0 cleared, 0 of those held up

Iterating until a backtest turns green produces a number fitted to that
sample.  The out-of-sample gap above is the evidence, and the in-sample
distribution shows the best of many tries is expected to look good by luck.

====================================================================================================
7. HOW MANY OF THE PRE-REGISTERED CELLS SURVIVE MULTIPLE COMPARISONS?
====================================================================================================
The study tested 12 pre-registered cells (3 rule sets x 4 instruments).
Bonferroni bar at alpha=0.05 for m=12: per-test alpha=0.004167, |t| > 2.865
stra sym         t      n       E_R   verdict
M1   SPY      4.79    281     0.171    CLEARS
M3   SPY      2.73     99     0.371     fails
M1   QQQ      2.14    226     0.091     fails
M3   QQQ      2.07    120     0.234     fails
M1   IWM      2.04    201     0.082     fails
M2   SPY      1.98    110     0.186     fails
M2   IWM      1.63     78     0.162     fails
M2   QQQ      1.18     85     0.118     fails
M2   EEM      0.66     59     0.082     fails
M3   IWM      0.44    124     0.048     fails
M3   EEM     -0.14    127    -0.016     fails
M1   EEM      0.07    158     0.003     fails

1 of 12 cells clear the bar after correcting for the search.
M1/SPY

====================================================================================================
7b. ROBUSTNESS OF THE SURVIVING EDGE
====================================================================================================

M1 on SPY: 281 closed trades, E_R=+0.1711, t=4.79
  calendar years with trades: 31 | positive: 26 (84%) | negative: 5
  first half   n=123 p=0.772 E_R=+0.1926 t=+3.70 totalR=+23.7
  second half  n=158 p=0.722 E_R=+0.1543 t=+3.14 totalR=+24.4
  by decade:
    1990s  n= 63 E_R=+0.1983 totalR=+12.5
    2000s  n= 60 E_R=+0.1867 totalR=+11.2
    2010s  n= 93 E_R=+0.1357 totalR=+12.6
    2020s  n= 65 E_R=+0.1810 totalR=+11.8
  A fished parameter would not survive all four decades; this does or does
  not - read the numbers above rather than the claim.

====================================================================================================
8. EXIT MIX AND COST SENSITIVITY - sizing the zero-cost assumption
====================================================================================================
Every expectancy in this study is GROSS: no commission, no slippage, no
borrow.  These two tables let a reader size that omission instead of just
noting it.

8a. How each trade ended
stra sym        n       stop     target   time/eod
M1   SPY      281   42 (15%)  228 (81%)    11 (4%)
M1   QQQ      226   42 (19%)  169 (75%)    15 (7%)
M1   IWM      201   29 (14%)  154 (77%)    18 (9%)
M1   EEM      158   33 (21%)  115 (73%)    10 (6%)
M2   SPY      110   39 (35%)   61 (55%)    10 (9%)
M2   QQQ       85   29 (34%)   44 (52%)   12 (14%)
M2   IWM       78   22 (28%)   42 (54%)   14 (18%)
M2   EEM       59   20 (34%)   26 (44%)   13 (22%)
M3   SPY       99   46 (46%)   53 (54%)     0 (0%)
M3   QQQ      120   58 (48%)   62 (52%)     0 (0%)
M3   IWM      124   69 (56%)   55 (44%)     0 (0%)
M3   EEM      127   77 (61%)   50 (39%)     0 (0%)

8b. Cost sensitivity: a round trip of c basis points of price costs
    c/100 / (1R as a percent of price) in R, because 1R is 2 x ATR(14).
stra sym      1R %px  gross E_R    b/e bps     cost@1bp     cost@5bp
M1   SPY       2.16%      0.171         36.9      0.0046R      0.0232R
M1   QQQ       2.81%      0.091         25.4      0.0036R      0.0178R
M1   IWM       3.09%      0.082         25.2      0.0032R      0.0162R
M1   EEM       2.87%      0.003          1.0      0.0035R      0.0174R
M2   SPY       2.23%      0.186         41.5      0.0045R      0.0224R
M2   QQQ       3.10%      0.118         36.4      0.0032R      0.0161R
M2   IWM       3.25%      0.162         52.8      0.0031R      0.0154R
M2   EEM       3.13%      0.082         25.6      0.0032R      0.0160R
M3   SPY       3.13%      0.371        116.0      0.0032R      0.0160R
M3   QQQ       3.71%      0.234         86.9      0.0027R      0.0135R
M3   IWM       3.65%      0.048         17.5      0.0027R      0.0137R
M3   EEM       3.55%     -0.016          n/a      0.0028R      0.0141R

'b/e bps' is the round-trip cost at which that cell's gross edge is
exactly consumed.  A cell whose b/e is below the instrument's real spread
has no net edge at all.
```

### The table that matters most — tuned winner vs the pre-registered default

The pre-registered M1 is RSI(2) < 10 with a 5-day cap, and it sits inside both grids,
so the comparison is like-for-like on the same split:

| | SPY (grid A, 30 combos) | QQQ (grid B, 56 combos) |
|---|---|---|
| in-sample gain of the fished winner over the default | **+0.213R** | **+0.135R** |
| out-of-sample gain of the same winner over the same default | **+0.006R** | **+0.048R** |
| tuned advantage retained | **3%** | **36%** |
| default in-sample E | +0.267 | +0.135 |
| winner in-sample E | +0.480 | +0.270 |
| default held-out E | +0.219 | +0.136 |
| winner held-out E | +0.225 | +0.184 |

This is the cleanest evidence in the study. On SPY the search appeared to improve the
rule by +0.213R per trade; out-of-sample the improvement was +0.006R, and the winner's
held-out expectancy (+0.225R) was indistinguishable from the un-tuned default's
(+0.219R). **The apparent gain was selection, not signal.**

Two supporting facts:

- **100% of combinations looked profitable in-sample** (30 of 30, and 56 of 56). When
every point in the grid is green the grid has stopped discriminating — the search is
finding the family's modest real edge, not a better parameter.
- **The Bonferroni bar does its job.** For grid A (m = 30) the bar is |t| > 3.144 and
9 combinations cleared it; for grid B (m = 56) the bar is |t| > 3.322 and **none**
cleared. The wider search on the second instrument found nothing that survives
multiple-testing correction.

**Conclusion.** Iterating until the backtest turns green produces a number fitted to
that sample. Here the fitted number halved out-of-sample and the fitted *advantage*
over the honest default almost entirely disappeared (3% retained on SPY). The
out-of-sample gap is the evidence, and the in-sample distribution — best +0.480,
median +0.116, worst +0.036 — shows the best of many tries is expected to look good by
luck alone.

---

## 7. How many of the pre-registered cells survive multiple comparisons?

The main study is not immune to the problem Task 5 demonstrates: 3 rule sets × 4
instruments is 12 tests, so one of them looking good is partly luck. Correcting for
that search matters.

```
====================================================================================================
The study tested 12 pre-registered cells (3 rule sets x 4 instruments).
Bonferroni bar at alpha=0.05 for m=12: per-test alpha=0.004167, |t| > 2.865
stra sym         t      n       E_R   verdict
M1   SPY      4.79    281     0.171    CLEARS
M3   SPY      2.73     99     0.371     fails
M1   QQQ      2.14    226     0.091     fails
M3   QQQ      2.07    120     0.234     fails
M1   IWM      2.04    201     0.082     fails
M2   SPY      1.98    110     0.186     fails
M2   IWM      1.63     78     0.162     fails
M2   QQQ      1.18     85     0.118     fails
M2   EEM      0.66     59     0.082     fails
M3   IWM      0.44    124     0.048     fails
M3   EEM     -0.14    127    -0.016     fails
M1   EEM      0.07    158     0.003     fails

1 of 12 cells clear the bar after correcting for the search.
M1/SPY

====================================================================================================
```

**Only 1 of the 12 cells clears the bar** (|t| > 2.865 for m = 12): M1 on SPY, at
t = 4.79 against the next best at t = 2.73. Everything else — including M3 on SPY,
whose per-trade expectancy of +0.371R is the *largest* in the table — is
indistinguishable from noise once the search is accounted for. A big expectancy with
a wide spread and a small sample is not a finding; that is exactly what the `sd` and
`n_req` columns are for.

### 7b. Is the one survivor a real edge or a lucky cell?

```
====================================================================================================

M1 on SPY: 281 closed trades, E_R=+0.1711, t=4.79
  calendar years with trades: 31 | positive: 26 (84%) | negative: 5
  first half   n=123 p=0.772 E_R=+0.1926 t=+3.70 totalR=+23.7
  second half  n=158 p=0.722 E_R=+0.1543 t=+3.14 totalR=+24.4
  by decade:
    1990s  n= 63 E_R=+0.1983 totalR=+12.5
    2000s  n= 60 E_R=+0.1867 totalR=+11.2
    2010s  n= 93 E_R=+0.1357 totalR=+12.6
    2020s  n= 65 E_R=+0.1810 totalR=+11.8
  A fished parameter would not survive all four decades; this does or does
  not - read the numbers above rather than the claim.

====================================================================================================
8. EXIT MIX AND COST SENSITIVITY - sizing the zero-cost assumption
====================================================================================================
Every expectancy in this study is GROSS: no commission, no slippage, no
borrow.  These two tables let a reader size that omission instead of just
noting it.

8a. How each trade ended
stra sym        n       stop     target   time/eod
M1   SPY      281   42 (15%)  228 (81%)    11 (4%)
M1   QQQ      226   42 (19%)  169 (75%)    15 (7%)
M1   IWM      201   29 (14%)  154 (77%)    18 (9%)
M1   EEM      158   33 (21%)  115 (73%)    10 (6%)
M2   SPY      110   39 (35%)   61 (55%)    10 (9%)
M2   QQQ       85   29 (34%)   44 (52%)   12 (14%)
M2   IWM       78   22 (28%)   42 (54%)   14 (18%)
M2   EEM       59   20 (34%)   26 (44%)   13 (22%)
M3   SPY       99   46 (46%)   53 (54%)     0 (0%)
M3   QQQ      120   58 (48%)   62 (52%)     0 (0%)
M3   IWM      124   69 (56%)   55 (44%)     0 (0%)
M3   EEM      127   77 (61%)   50 (39%)     0 (0%)

8b. Cost sensitivity: a round trip of c basis points of price costs
    c/100 / (1R as a percent of price) in R, because 1R is 2 x ATR(14).
stra sym      1R %px  gross E_R    b/e bps     cost@1bp     cost@5bp
M1   SPY       2.16%      0.171         36.9      0.0046R      0.0232R
M1   QQQ       2.81%      0.091         25.4      0.0036R      0.0178R
M1   IWM       3.09%      0.082         25.2      0.0032R      0.0162R
M1   EEM       2.87%      0.003          1.0      0.0035R      0.0174R
M2   SPY       2.23%      0.186         41.5      0.0045R      0.0224R
M2   QQQ       3.10%      0.118         36.4      0.0032R      0.0161R
M2   IWM       3.25%      0.162         52.8      0.0031R      0.0154R
M2   EEM       3.13%      0.082         25.6      0.0032R      0.0160R
M3   SPY       3.13%      0.371        116.0      0.0032R      0.0160R
M3   QQQ       3.71%      0.234         86.9      0.0027R      0.0135R
M3   IWM       3.65%      0.048         17.5      0.0027R      0.0137R
M3   EEM       3.55%     -0.016          n/a      0.0028R      0.0141R

'b/e bps' is the round-trip cost at which that cell's gross edge is
exactly consumed.  A cell whose b/e is below the instrument's real spread
has no net edge at all.
```

**This is what separates M1/SPY from the fished parameters in §6.** It is positive in
**26 of 31 years (84%)**, holds in both halves of the sample (+0.193R then +0.154R),
and holds in **all four decades** (+0.198, +0.187, +0.136, +0.181). A parameter
chosen by search does not behave like that, as §6 shows directly: the tuned winner's
advantage over the default went from +0.213R in-sample to +0.006R held out.

---

## 8. Sizing the two assumptions that flatter these numbers

Two conventions do most of the work in making the results above look as good as
they do — **costs set to zero** and **stops filled exactly at the stop**. Both are
measurable from the data, so neither has to be left as a footnote.

```
====================================================================================================
Every expectancy in this study is GROSS: no commission, no slippage, no
borrow.  These two tables let a reader size that omission instead of just
noting it.

8a. How each trade ended
stra sym        n       stop     target   time/eod
M1   SPY      281   42 (15%)  228 (81%)    11 (4%)
M1   QQQ      226   42 (19%)  169 (75%)    15 (7%)
M1   IWM      201   29 (14%)  154 (77%)    18 (9%)
M1   EEM      158   33 (21%)  115 (73%)    10 (6%)
M2   SPY      110   39 (35%)   61 (55%)    10 (9%)
M2   QQQ       85   29 (34%)   44 (52%)   12 (14%)
M2   IWM       78   22 (28%)   42 (54%)   14 (18%)
M2   EEM       59   20 (34%)   26 (44%)   13 (22%)
M3   SPY       99   46 (46%)   53 (54%)     0 (0%)
M3   QQQ      120   58 (48%)   62 (52%)     0 (0%)
M3   IWM      124   69 (56%)   55 (44%)     0 (0%)
M3   EEM      127   77 (61%)   50 (39%)     0 (0%)

8b. Cost sensitivity: a round trip of c basis points of price costs
    c/100 / (1R as a percent of price) in R, because 1R is 2 x ATR(14).
stra sym      1R %px  gross E_R    b/e bps     cost@1bp     cost@5bp
M1   SPY       2.16%      0.171         36.9      0.0046R      0.0232R
M1   QQQ       2.81%      0.091         25.4      0.0036R      0.0178R
M1   IWM       3.09%      0.082         25.2      0.0032R      0.0162R
M1   EEM       2.87%      0.003          1.0      0.0035R      0.0174R
M2   SPY       2.23%      0.186         41.5      0.0045R      0.0224R
M2   QQQ       3.10%      0.118         36.4      0.0032R      0.0161R
M2   IWM       3.25%      0.162         52.8      0.0031R      0.0154R
M2   EEM       3.13%      0.082         25.6      0.0032R      0.0160R
M3   SPY       3.13%      0.371        116.0      0.0032R      0.0160R
M3   QQQ       3.71%      0.234         86.9      0.0027R      0.0135R
M3   IWM       3.65%      0.048         17.5      0.0027R      0.0137R
M3   EEM       3.55%     -0.016          n/a      0.0028R      0.0141R

'b/e bps' is the round-trip cost at which that cell's gross edge is
exactly consumed.  A cell whose b/e is below the instrument's real spread
has no net edge at all.
```

**Exit mix.** M1 usually leaves on its signal (73–81% of exits are targets) so only
14–21% of its trades touch the stop. M3 is the opposite: **46–61% of its exits are
stops**, all booked at exactly −1.000R, which is why M3 carries the widest spread of
outcomes (`sd` = 1.22–1.35 against M1's 0.57–0.64) and is the most exposed to any gap
through a stop.

**Costs.** `b/e bps` is the round-trip cost that exactly consumes each cell's gross
edge. The spread across cells is enormous:

- **M3/SPY, 116.0 bps** — the widest margin in the table, and the largest per-trade
edge (+0.371R), though it is also the cell that *fails* the multiple-comparison bar.
- **M1/SPY, 36.9 bps** — comfortable against a realistic ~1 bp round trip in SPY.
- **M1/IWM, 25.2 bps** and **M3/IWM, 17.5 bps** — survivable but not comfortable on an
instrument whose round trip is not free.
- **M1/EEM, 1.0 bps** — the edge is consumed by a round trip below the spread on the
instrument. **This cell is not positive after any realistic cost**, despite showing a
positive gross expectancy in §2.

That last line is the practical content of this section: the zero-cost convention is
not a rounding error for the thin cells, it is the difference between a positive and a
negative result.

---

## 9. The all-weather verdict

**Is any single rule set profitable in every regime and every year? No.** The data is
unambiguous:

- **Every year:** each of the 12 strategy × instrument pairs has losing years, from
5 of 31 (M1/SPY) to 14 of 28 (M2/SPY). Ten of the twelve lose in a third or more of
their years.
- **Every regime:** 66 of the 155 strategy × instrument × trend × vol cells have
negative expectancy, and `DOWN_falling` loses for all three rules pooled.
- **Every timeframe tested:** per-trade expectancy is positive on SPY and QQQ for all
three rules, near zero on IWM, and negative for M3 on EEM. Same code, same rules,
different instrument — different answer.
- **Nothing beat buy-and-hold on returns.** The rules make 0.0–1.4% CAGR against
7.0–10.8% for holding the ETF. They risk 1% of equity per trade and sit in cash most
of the time, so this is not like-for-like — but only M1 on SPY (Sharpe 0.71 vs 0.55)
beat buy-and-hold even after that adjustment; every other cell lost on Sharpe too.
- **One positive cell does not survive costs.** §2 shows all twelve cells with a
positive gross expectancy except M3/EEM. §8 shows that M1/EEM's +0.003R edge is
consumed by a **1.0 bps** round trip, which is inside the spread on the instrument.
So the honest count of cells with a *net* edge is not eleven of twelve — M1/EEM
belongs with M3/EEM on the negative side.

**What does hold up.** M1 on SPY is a genuine, statistically comfortable effect:
n = 281, p = 0.744, E_R = +0.171R, t = 4.79, well past n_req = 23, and it repeats in
the pooled `UP_rising` regime at +91.0R. M2 and M3 are weaker (t = 1.98 and 2.73 on
SPY, 1.18 and 2.07 on QQQ) and M3's apparent strength carries the highest variance in
the study. The volatility premium is real on average, concentrated in calm and
grinding-up markets, and punctured by crisis onsets with a fat left tail.

**The one-line honest summary:** mean reversion in an uptrend is the only thing here
with a defensible edge, that edge is worth about +0.17R per trade before costs — costs
were set to zero in this study, so the real figure is lower — and the most reliable way
to manufacture a fake edge is to keep searching until the backtest agrees with you.

---

## 10. Reproduce

```bash
cd skills/14-finance/options-trading-playbook/examples/regime-study
export PYTHONIOENCODING=utf-8
py -3 pull_data.py          # data/*.csv with provenance headers
py -3 verify_sources.py     # exit 0 = primary series certified by TradingView
py -3 study.py > run.txt    # the study
py -3 make_results.py       # slice run.txt into this file
py -3 verify_metrics.py     # exit 0 = longhand hand-check agrees on 13 quantities
```
