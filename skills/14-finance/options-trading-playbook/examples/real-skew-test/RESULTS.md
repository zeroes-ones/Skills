# RESULTS -- real-skew-test

**Every table below is the VERBATIM stdout of a real run**, pasted by
`make-results.py` from `logs/study-output.txt` and `handcheck-output.txt`.  The
labels are not decoration:

- **`[MEASURED]`** -- derived from a real Robinhood option print.
- **`[MODELED]`** -- derived from the VIX proxy.

Nothing in this file is edited by hand.  Regenerate with:

```bash
py -3 study.py && py -3 handcheck.py && py -3 make-results.py
```

---

## A. The study

```
REAL-SKEW-TEST -- the skew, measured on real SPY option prints, with
its uncertainty, and what it does to the premium-selling edge.

# PROVENANCE: source=Robinhood MCP get_option_historicals (real option OHLC, regular session)
# PROVENANCE: pull_date=2026-10-15
# PROVENANCE: underlying_close_source=TradingView AMEX:SPY 1D close, carried from the sibling index-options-test pull (2026-10-14)
# PROVENANCE: rate_source=TVC:US03M 1D close (per-cent per-annum yield index), carried from the same sibling pull
# PROVENANCE: expiry_rule=Friday weekly closest to 37.5 DTE (centre of the 30-45 band); ONE declared override: SPY 2020-03-02 -> 2020-04-17 (Good Friday closed 2020-04-10)
# PROVENANCE: ladder=puts 3%,6%,10%,15% OTM, calls 3%,6% OTM; target strike rounded to the nearest dollar, then substituted to a neighbouring LISTED strike where the grid lacks it (substituted=yes)
# PROVENANCE: declared=122 resolved=108 returned_bar=82
# PROVENANCE: option bars carry NO volume (Robinhood does not publish it); only NON-interpolated bars are accepted; bar_date is the last non-interpolated session at or before sample_date
# PROVENANCE: filters applied in study.py, not here: price >= $0.10, 150% >= IV >= 2%, bar lag <= 7 days

==============================================================================
0. THE FUNNEL, WITH EVERY EXCLUSION COUNTED
==============================================================================
  declared contracts (panel ladder + parity) : 122
  resolved as an instrument                  : 108
  returned a NON-interpolated bar            : 82
  passed the $0.10 price floor               : 81
  passed the IV band [2%, 150%]           : 81

  EXCLUSIONS BY REASON
  reason                                             n
  -------------------------------------------------  --
  no non-interpolated bar at/before the sample date  40
  print $0.06 below the $0.10 floor                  1

  FLAGS (not exclusions)
  flag           n  meaning
  -------------  -  --------------------------------------------------------------------------------
  flat_bar       6  open==high==low==close: the session's only information is one print
  suspect_range  6  low <= $0.01 while close > $1: a bad tick inside the bar; only the CLOSE is used

  usable date panels: 20 of the 20 drawn

  sample_date  n_puts  n_calls  usable  note
  -----------  ------  -------  ------  ------------------
  2017-10-02   4       1        yes     slope fittable
  2018-04-02   3       2        yes     slope fittable
  2018-10-01   1       2        no      too few put prints
  2019-04-01   3       0        yes     slope fittable
  2019-10-01   4       2        yes     slope fittable
  2020-02-24   3       2        yes     slope fittable
  2020-03-02   4       2        yes     slope fittable
  2020-04-01   1       2        no      too few put prints
  2020-10-01   2       2        yes     slope fittable
  2021-04-01   2       1        yes     slope fittable
  2021-10-01   3       2        yes     slope fittable
  2022-04-01   4       2        yes     slope fittable
  2022-10-03   3       1        yes     slope fittable
  2023-04-03   3       1        yes     slope fittable
  2023-10-02   2       1        yes     slope fittable
  2024-04-01   2       1        yes     slope fittable
  2024-10-01   1       2        no      too few put prints
  2025-04-01   1       2        no      too few put prints
  2025-10-01   1       0        no      too few put prints
  2026-04-01   2       2        yes     slope fittable

  LADDERS WITH >= 2 PUT PRINTS (the skew-slope sample) : 15
  PUT MONOTONICITY: on every ladder, put IV falls with moneyness (no rise above 2.0 vol points between adjacent strikes).
  CALL MONOTONICITY: on every ladder, call IV falls with moneyness.

==============================================================================
1. REAL IMPLIED VOL PER CONTRACT  [MEASURED]
==============================================================================
  IV = bisection on Black-Scholes (European, q=0) using the REAL SPY
  close on the sample date, real calendar DTE/365, and the 3-month
  bill yield (TVC:US03M) at t-3 sessions, the sibling convention.

  --- 2017-10-02  spot 252.32  expiry 2017-11-10 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  260     +3.00%   0.21   6.43%   0.087   2017-10-02  yes   no
  put   215     -15.00%  0.10   23.00%  -0.015  2017-10-02  yes   yes
  put   225     -11.00%  0.18   19.01%  -0.029  2017-10-02  yes   yes
  put   237     -6.00%   0.42   14.03%  -0.079  2017-10-02  yes   no
  put   245     -3.00%   0.89   10.59%  -0.184  2017-10-02  yes   no

  --- 2018-04-02  spot 257.47  expiry 2018-05-11 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  265     +3.00%   3.12   17.62%  0.330   2018-04-02  no    no
  call  273     +6.00%   1.01   16.16%  0.147   2018-04-02  no    no
  put   220     -15.00%  0.65   31.54%  -0.055  2018-04-02  no    yes
  put   242     -6.00%   2.47   24.74%  -0.203  2018-04-02  no    no
  put   250     -3.00%   4.12   22.45%  -0.322  2018-04-02  no    no

  --- 2018-10-01  spot 291.73  expiry 2018-11-09 (39 DTE) ---
  type  strike  money   price  IV      delta   bar_date    flat  subst
  ----  ------  ------  -----  ------  ------  ----------  ----  -----
  call  300     +3.00%  0.70   8.13%   0.171   2018-10-01  no    no
  call  310     +6.00%  0.10   9.37%   0.029   2018-10-01  no    yes
  put   283     -3.00%  1.57   13.09%  -0.216  2018-10-01  no    no

  --- 2019-04-01  spot 285.83  expiry 2019-05-10 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  put   245     -14.00%  0.18   24.07%  -0.021  2019-04-01  no    yes
  put   255     -11.00%  0.33   20.90%  -0.041  2019-04-01  no    yes
  put   277     -3.00%   1.80   14.33%  -0.227  2019-04-01  no    no

  --- 2019-10-01  spot 293.24  expiry 2019-11-08 (38 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  302     +3.00%   1.94   13.08%  0.264   2019-10-01  no    no
  call  311     +6.00%   0.22   10.74%  0.052   2019-10-01  no    no
  put   250     -15.00%  0.36   27.99%  -0.033  2019-10-01  no    yes
  put   265     -10.00%  1.04   24.81%  -0.092  2019-10-01  no    yes
  put   276     -6.00%   2.17   22.28%  -0.183  2019-10-01  no    no
  put   284     -3.00%   3.60   20.20%  -0.290  2019-10-01  no    no

  --- 2020-02-24  spot 322.42  expiry 2020-04-03 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  332     +3.00%   3.16   15.79%  0.306   2020-02-24  no    no
  call  342     +6.00%   0.54   12.77%  0.088   2020-02-24  no    no
  put   290     -10.00%  2.20   30.63%  -0.130  2020-02-24  no    no
  put   303     -6.00%   3.84   27.18%  -0.223  2020-02-24  no    no
  put   313     -3.00%   5.92   24.47%  -0.333  2020-02-24  no    no

  --- 2020-03-02  spot 309.09  expiry 2020-04-17 (46 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  318     +3.00%   5.02   19.25%  0.362   2020-03-02  no    no
  call  328     +6.00%   1.64   16.61%  0.172   2020-03-02  no    no
  put   263     -15.00%  2.96   42.12%  -0.122  2020-03-02  no    no
  put   278     -10.00%  5.04   38.98%  -0.198  2020-03-02  no    no
  put   291     -6.00%   7.68   35.89%  -0.290  2020-03-02  no    no
  put   300     -3.00%   10.08  33.44%  -0.372  2020-03-02  no    no

  --- 2020-04-01  spot 246.15  expiry 2020-05-08 (37 DTE) ---
  type  strike  money   price  IV      delta   bar_date    flat  subst
  ----  ------  ------  -----  ------  ------  ----------  ----  -----
  call  254     +3.00%  11.24  46.76%  0.446   2020-04-01  no    no
  call  261     +6.00%  7.87   43.73%  0.363   2020-04-01  no    no
  put   239     -3.00%  13.88  55.95%  -0.400  2020-04-01  no    no
  put   254     +3.00%  20.09  49.96%  -0.547  2020-04-01  no    no
  put   261     +6.00%  23.72  47.08%  -0.624  2020-04-01  no    no

  --- 2020-10-01  spot 337.04  expiry 2020-11-06 (36 DTE) ---
  type  strike  money   price  IV      delta   bar_date    flat  subst
  ----  ------  ------  -----  ------  ------  ----------  ----  -----
  call  347     +3.00%  6.01   23.85%  0.363   2020-10-01  no    no
  call  357     +6.00%  2.71   21.95%  0.212   2020-10-01  no    no
  put   317     -6.00%  5.24   31.41%  -0.251  2020-10-01  no    no
  put   327     -3.00%  7.70   29.04%  -0.353  2020-10-01  no    no

  --- 2021-04-01  spot 400.61  expiry 2021-05-07 (36 DTE) ---
  type  strike  money   price  IV      delta   bar_date    flat  subst
  ----  ------  ------  -----  ------  ------  ----------  ----  -----
  call  425     +6.00%  0.45   12.38%  0.067   2021-04-01  no    no
  put   377     -6.00%  2.21   20.16%  -0.161  2021-04-01  no    no
  put   389     -3.00%  3.78   16.85%  -0.280  2021-04-01  no    no

  --- 2021-10-01  spot 434.24  expiry 2021-11-05 (35 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  447     +3.00%   2.94   14.13%  0.261   2021-10-01  no    no
  call  460     +6.00%   0.42   11.92%  0.061   2021-10-01  no    no
  put   391     -10.00%  1.94   27.91%  -0.104  2021-10-01  no    no
  put   408     -6.00%   3.71   24.55%  -0.195  2021-10-01  no    no
  put   421     -3.00%   5.95   21.53%  -0.309  2021-10-01  no    no

  --- 2022-04-01  spot 452.92  expiry 2022-05-06 (35 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  467     +3.00%   2.70   13.61%  0.244   2022-04-01  no    no
  call  480     +6.00%   0.52   12.37%  0.069   2022-04-01  no    no
  put   385     -15.00%  0.75   31.11%  -0.041  2022-04-01  no    no
  put   408     -10.00%  1.55   25.95%  -0.089  2022-04-01  no    no
  put   426     -6.00%   3.13   22.45%  -0.178  2022-04-01  no    no
  put   439     -3.00%   5.27   19.82%  -0.292  2022-04-01  no    no

  --- 2022-10-03  spot 366.61  expiry 2022-11-11 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  378     +3.00%   8.02   25.60%  0.389   2022-10-03  no    no
  put   330     -10.00%  3.22   33.55%  -0.148  2022-10-03  no    no
  put   345     -6.00%   5.71   30.95%  -0.246  2022-10-03  no    no
  put   356     -3.00%   8.61   29.22%  -0.347  2022-10-03  no    no

  --- 2023-04-03  spot 410.95  expiry 2023-05-12 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  436     +6.00%   1.16   14.11%  0.126   2023-04-03  no    no
  put   370     -10.00%  1.17   24.32%  -0.077  2023-04-03  no    no
  put   386     -6.00%   2.51   21.58%  -0.159  2023-04-03  no    no
  put   399     -3.00%   4.66   19.31%  -0.280  2023-04-03  no    no

  --- 2023-10-02  spot 427.31  expiry 2023-11-10 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  440     +3.00%   4.04   14.40%  0.318   2023-10-02  no    no
  put   385     -10.00%  0.90   22.64%  -0.064  2023-10-02  no    no
  put   414     -3.00%   3.91   17.99%  -0.252  2023-10-02  no    no

  --- 2024-04-01  spot 522.16  expiry 2024-05-10 (39 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  538     +3.00%   2.80   10.91%  0.255   2024-04-01  no    no
  put   470     -10.00%  0.61   20.10%  -0.043  2024-04-01  no    no
  put   506     -3.00%   2.66   13.79%  -0.199  2024-04-01  no    no

  --- 2024-10-01  spot 568.62  expiry 2024-11-08 (38 DTE) ---
  type  strike  money   price  IV      delta   bar_date    flat  subst
  ----  ------  ------  -----  ------  ------  ----------  ----  -----
  call  586     +3.00%  5.14   14.72%  0.305   2024-10-01  no    no
  call  603     +6.00%  1.12   12.90%  0.101   2024-10-01  no    no
  put   535     -6.00%  4.04   22.65%  -0.175  2024-10-01  no    no

  --- 2025-04-01  spot 560.97  expiry 2025-05-09 (38 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  578     +3.00%   5.98   16.17%  0.322   2025-04-01  no    no
  call  595     +6.00%   1.45   14.01%  0.119   2025-04-01  no    no
  put   505     -10.00%  2.09   26.31%  -0.091  2025-04-01  no    no

  --- 2025-10-01  spot 668.45  expiry 2025-11-07 (37 DTE) ---
  type  strike  money   price  IV      delta   bar_date    flat  subst
  ----  ------  ------  -----  ------  ------  ----------  ----  -----
  put   648     -3.00%  5.19   16.48%  -0.244  2025-10-01  no    no

  --- 2026-04-01  spot 655.24  expiry 2026-05-08 (37 DTE) ---
  type  strike  money    price  IV      delta   bar_date    flat  subst
  ----  ------  -------  -----  ------  ------  ----------  ----  -----
  call  675     +3.00%   7.82   17.65%  0.332   2026-04-01  no    no
  call  695     +6.00%   1.80   14.59%  0.122   2026-04-01  no    no
  put   590     -10.00%  3.40   29.07%  -0.111  2026-04-01  no    no
  put   636     -3.00%   10.13  23.24%  -0.312  2026-04-01  no    no


==============================================================================
2. THE MEASURED SKEW, WITH ITS UNCERTAINTY  [MEASURED]
==============================================================================
  Per date: OLS of IV (vol points) against d = -ln(K/S) over the
  PUT prints only.  d rises as the put goes further OTM.
  slope(vol pts / 10% OTM) = coefficient x ln(1/0.90).

  sample_date  n_puts  slope/10%OTM  IV at d=0  r2     note
  -----------  ------  ------------  ---------  -----  ------------
  2017-10-02   4       10.00         7.95       0.999
  2018-04-02   3       7.50          20.34      1.000
  2018-10-01   1       n/a           n/a        n/a    too few puts
  2019-04-01   3       8.36          11.84      1.000
  2019-10-01   4       6.39          18.46      0.996
  2020-02-24   3       8.48          22.12      1.000
  2020-03-02   4       6.91          31.74      0.995
  2020-04-01   1       n/a           n/a        n/a    too few puts
  2020-10-01   2       8.06          26.72      1.000
  2021-04-01   2       11.12         13.74      1.000
  2021-10-01   3       9.05          18.99      0.997
  2022-04-01   4       9.02          17.14      1.000
  2022-10-03   3       6.02          27.52      1.000
  2023-04-03   3       7.00          17.38      1.000
  2023-10-02   2       6.74          15.97      1.000
  2024-04-01   2       9.01          11.10      1.000
  2024-10-01   1       n/a           n/a        n/a    too few puts
  2025-04-01   1       n/a           n/a        n/a    too few puts
  2025-10-01   1       n/a           n/a        n/a    too few puts
  2026-04-01   2       8.19          20.92      1.000

  AGGREGATE over the 15 fittable ladders:
  stat                        vol pts per 10% OTM
  --------------------------  -------------------
  n                           15
  min                         6.02
  q25                         6.95
  MEDIAN                      8.19
  q75                         9.02
  max                         11.12
  mean                        8.12
  sample sd                   1.40
  standard error of the mean  0.36
  mean 95% CI (bootstrap)     7.45 to 8.83
  median 95% CI (bootstrap)   7.00 to 9.01

  VERDICT ON THE SKEW NUMBER:
    the assumption under test is 1.5 vol points per 10% OTM
    measured median = 8.19  (95% CI 7.00 to 9.01, n=15)
    median / 1.5 = 5.5x
    the LOWER end of the 95% CI is 7.00, still 4.7x the assumed
    1.5 -- so 'the skew is materially bigger than 1.5' survives
    the uncertainty at this n.
    measured slopes above +1.5: 15 of 15

==============================================================================
3. THE PUT-CALL IV SPREAD  [MEASURED]
==============================================================================
  At matched moneyness, IV(put at 3% OTM) - IV(call at 3% OTM),
  each side taken from that side's own fitted line in d.
  This is the LEVEL offset, and it is the comparable number to the
  sibling's 1.5 vol-point haircut on the sold leg.

  sample_date  n_puts  n_calls  IV_put(-3%)  IV_call(+3%)  spread
  -----------  ------  -------  -----------  ------------  --------------------------
  2017-10-02   4       1        10.69        6.43          4.26
  2018-04-02   3       2        22.52        17.54         4.99
  2018-10-01   1       2        13.09        8.22          4.87
  2019-04-01   3       0        n/a          n/a           needs >=1 put and >=1 call
  2019-10-01   4       2        20.20        13.00         7.20
  2020-02-24   3       2        24.54        15.67         8.88
  2020-03-02   4       2        33.48        19.07         14.41
  2020-04-01   1       2        55.95        46.76         9.19
  2020-10-01   2       2        29.05        23.76         5.29
  2021-04-01   2       1        16.96        12.38         4.58
  2021-10-01   3       2        21.53        14.01         7.51
  2022-04-01   4       2        19.82        13.61         6.22
  2022-10-03   3       1        29.28        25.60         3.68
  2023-04-03   3       1        19.37        14.11         5.27
  2023-10-02   2       1        17.99        14.40         3.60
  2024-04-01   2       1        13.79        10.91         2.88
  2024-10-01   1       2        22.65        14.70         7.95
  2025-04-01   1       2        26.31        16.13         10.17
  2025-10-01   1       0        n/a          n/a           needs >=1 put and >=1 call
  2026-04-01   2       2        23.29        17.57         5.72

  AGGREGATE over 18 date panels with both sides measured:
  stat                       vol points
  -------------------------  ------------
  n                          18
  min                        2.88
  q25                        4.65
  MEDIAN                     5.51
  q75                        7.84
  max                        14.41
  mean                       6.48
  sd                         2.86
  median 95% CI (bootstrap)  4.72 to 7.73

  measured put-call spread median 5.51 vs the assumed 1.5 = 3.7x
  minimum observed spread: 2.88 (1.9x the assumption)

==============================================================================
4. IS THE SKEW STABLE?  2017 -> 2026, AND IN STRESS  [MEASURED]
==============================================================================
  era                 n  median slope/10%OTM  slope range   median put-call
  ------------------  -  -------------------  ------------  ---------------
  2017-2019 calm      4  7.93                 6.39 - 10.00  4.93
  COVID Feb-Apr 2020  2  7.69                 6.91 - 8.48   9.19
  late 2020-2021      3  9.05                 8.06 - 11.12  5.29
  2022 drawdown       2  7.52                 6.02 - 9.02   4.95
  2023-2026           4  7.59                 6.74 - 9.01   5.49

  STRESS vs the rest.  STRESS = the declared COVID-window dates
  (2020-02-24, 2020-03-02, 2020-04-01) and the 2022-drawdown dates
  (2022-04-01, 2022-10-03).  One of those five (2020-04-01) has only
  one put print, so it carries a spread but no slope, hence n=4
  slopes against n=5 spreads in the stress row.
  group   n   median slope  median put-call spread
  ------  --  ------------  ----------------------
  stress  4   7.69          8.88
  rest    11  8.19          5.27

  2008 and every pre-2017 crisis are NOT REACHABLE: the expired-
  contract catalogue starts ~2017-09-15, so no pre-2017 skew exists
  in this data and the model is NOT substituted for it.

==============================================================================
5. MODEL ERROR: the old flat-VIX model vs the real prices  [MODELED] vs [MEASURED]
==============================================================================
  model price = Black-Scholes at IV_model = VIX(t-3) (kappa = 1 for
  SPY, the sibling's convention).  error = model - real; POSITIVE
  means the OLD study was TOO RICH, i.e. it over-credited a seller.

  LEVEL CHECK FIRST.  NOTE the sample has NO true at-the-money
  measurement: every put ladder starts at 3% OTM, so d=0 is always
  an extrapolation.  The column below is therefore the MEASURED
  3%-OTM put IV, which by construction sits ABOVE the ATM vol of
  the same surface.  Where it sits BELOW VIX(t-3) anyway, the print
  is stale-low relative to the index.

  sample_date  measured put IV @3%OTM%  VIX(t-3)%  flat VIX minus that
  -----------  -----------------------  ---------  -------------------
  2017-10-02   10.69                    9.87       -0.82
  2018-04-02   22.52                    22.50      -0.02
  2018-10-01   13.09                    12.89      -0.20
  2019-04-01   14.33                    15.15      +0.82
  2019-10-01   20.20                    16.07      -4.13
  2020-02-24   24.54                    14.38      -10.16
  2020-03-02   33.48                    27.56      -5.92
  2020-04-01   55.95                    65.54      +9.59
  2020-10-01   29.05                    26.19      -2.86
  2021-04-01   16.96                    20.74      +3.78
  2021-10-01   21.53                    23.24      +1.71
  2022-04-01   19.82                    18.91      -0.91
  2022-10-03   29.28                    30.19      +0.91
  2023-04-03   19.37                    19.11      -0.26
  2023-10-02   17.99                    18.21      +0.22
  2024-04-01   13.79                    13.23      -0.56
  2024-10-01   22.65                    15.36      -7.29
  2025-04-01   26.31                    18.68      -7.63
  2025-10-01   16.48                    15.29      -1.19
  2026-04-01   23.29                    31.04      +7.75

  ERROR DISTRIBUTION (n=81 contracts):
  stat    price err $  vol-pt err  pct err %
  ------  -----------  ----------  ---------
  min     -3.67        -16.25      -100.0
  q25     -0.76        -5.22       -61.3
  MEDIAN  0.01         0.05        0.3
  q75     1.65         4.67        52.0
  max     10.62        21.81       819.7
  mean    0.69         0.18        40.5

  by moneyness band (price error $):
  band   n   median  mean
  -----  --  ------  -----
  3-6%   62  0.72    1.17
  6-12%  13  -0.88   -0.96
  >12%   6   -0.46   -0.72

  by tenor bucket (price error $):
  bucket     n   median  mean
  ---------  --  ------  -----
  35-39 DTE  75  0.10    0.80
  45-49 DTE  6   -2.42   -0.62

  The old [MODELED] numbers were computed with this same flat-VIX
  assumption, so this distribution IS the error of the prior
  modelled results, at the funnel-adjusted sample size n=81.

==============================================================================
6. PREMIUM-SELLING RE-RUN ON THE MEASURED IV  [MEASURED]
==============================================================================
  Sibling programme S2: sell a ~30-DTE ~16-delta put spread, short
  leg near 6% OTM, long wing $5 lower, hold to expiry, settle at
  intrinsic against the REAL SPY close of the expiry session.

  BOTH legs are priced from the MEASURED put ladder, linearly
  interpolated in d = -ln(K/S) across the date's measured puts and
  clamped outside the measured range.  No VIX appears anywhere here.

  entry       K_short  K_wing  IV_short%  IV_wing%  credit$  R      note
  ----------  -------  ------  ---------  --------  -------  -----  ------------------
  2017-10-02  237      232     14.03      16.07     13.81    +0.03  S_T=258.09
  2018-04-02  242      237     24.74      26.23     66.66    +0.15  S_T=272.85
  2018-10-01  274      269     13.09      13.09     22.22    +0.05  S_T=277.76 CLAMPED
  2019-04-01  269      264     16.66      18.15     29.40    +0.06  S_T=288.10
  2019-10-01  276      271     22.28      23.42     61.80    +0.14  S_T=308.94
  2020-02-24  303      298     27.18      28.49     75.03    -1.00  S_T=248.19
  2020-03-02  291      286     35.89      37.06     114.56   -0.83  S_T=286.64
  2020-04-01  231      226     55.95      55.95     185.68   +0.59  S_T=292.44 CLAMPED
  2020-10-01  317      312     31.41      31.41     128.48   +0.35  S_T=350.16 CLAMPED
  2021-04-01  377      372     20.16      20.16     75.56    +0.18  S_T=422.12 CLAMPED
  2021-10-01  408      403     24.55      25.53     65.56    +0.15  S_T=468.53
  2022-04-01  426      421     22.45      23.41     57.01    -1.00  S_T=411.34
  2022-10-03  345      340     30.95      31.80     98.25    +0.24  S_T=398.51
  2023-04-03  386      381     21.58      22.43     53.79    +0.12  S_T=411.59
  2023-10-02  402      397     19.87      20.67     47.41    +0.10  S_T=440.61
  2024-04-01  491      486     16.37      17.24     24.93    +0.05  S_T=520.84
  2024-10-01  535      530     22.65      22.65     88.11    +0.21  S_T=598.19 CLAMPED
  2025-04-01  527      522     26.31      26.31     105.18   +0.27  S_T=564.34 CLAMPED
  2025-10-01  628      623     16.48      16.48     46.96    +0.10  S_T=670.97 CLAMPED
  2026-04-01  616      611     25.72      26.36     70.14    +0.16  S_T=737.62

  MEASURED re-run over 20 entries (short leg priced at 6% OTM):
  stat                   gross of costs  after LOW costs
  ---------------------  --------------  ---------------
  n entries              20              20
  p  (win rate)          0.8500          0.8500
  b  (mean win R)        0.1745          0.1572
  E  (mean R per entry)  0.0067          -0.0082
  median R               0.1308          0.1149
  min R                  -1.0000         -1.0000
  max R                  0.5907          0.5595
  sd R                   0.4298          0.4229

  COMPARISON
  run                           label       result
  ----------------------------  ----------  ------------------------------------------------
  sibling, no skew haircut      [MODELED]   CAGR +2.97%, 89% of months positive (306 months)
  sibling, +1.5 vol-pt haircut  [MODELED]   CAGR -0.87% (sign flips)
  sibling, +3.0 vol-pt haircut  [MODELED]   CAGR -4.03%
  first pass, measured IV       [MEASURED]  E_R = -0.0908, n=5 entries
  THIS run, measured IV         [MEASURED]  E_R = +0.0067 gross / -0.0082 net, n=20 entries

  The sign of the measured re-run is POSITIVE.
  20 entries, not 306 months: this is a partial measured window
  and is NOT a CAGR.
  bootstrap 95% CI for the mean R: -0.1843 to 0.1706
  The CI CONTAINS ZERO, so at this sample size the measured
  edge is NOT DISTINGUISHABLE FROM ZERO.

  entries where a leg's IV had to be CLAMPED outside the measured
  moneyness range (the ladder does not reach the wing): 7
  entries with only ONE measured put print on the date: 4

==============================================================================
7. SENSITIVITY: how much of the answer is the skew treatment?
==============================================================================
  variant                                                  n   mean R   median R  p       sign
  -------------------------------------------------------  --  -------  --------  ------  --------
  A. measured ladder (both legs) [MEASURED]                20  0.0067   0.1308    0.8500  POSITIVE
  B. sold leg at ZERO vol, wing measured                   20  -0.4045  -0.3310   0.0000  NEGATIVE
  C. both legs at ZERO vol (pure intrinsic spread credit)  20  -0.1436  0.0000    0.0000  NEGATIVE
  D. flat VIX on both legs [MODELED]                       20  0.0129   0.1136    0.8500  POSITIVE
  E. measured, minus 1.5 vol pts on the SOLD leg only      20  -0.0949  0.0139    0.6500  NEGATIVE
  F. measured, minus 3.0 vol pts on the SOLD leg only      20  -0.1704  -0.0709   0.1000  NEGATIVE
  G. sold leg at zero vol, wing at flat VIX [MODELED]      20  -0.3425  -0.2127   0.0000  NEGATIVE
  H. sold leg at flat VIX, wing at zero vol [MODELED]      20  -0.4405  0.2511    0.7500  NEGATIVE

  Read the spread between variant A (both legs from the real
  ladder), D (the sibling's flat-VIX model) and E/F (the haircut
  applied to the sold leg only).  The gap A-vs-D is what the
  measured ladder is worth; the gap A-vs-E/F is the size of the
  error made by pricing only the sold leg off the real skew.

==============================================================================
8. PUT-CALL PARITY AND THE LIVE CROSS-CHECK  [MEASURED]
==============================================================================
  For European options the implied vol of a put and a call at the
  same strike and expiry must be EQUAL.  Two INTRA-MONEY puts
  were resolved by mistake while hunting the calls at the same
  strikes on SPY 2020-04-01, and are used here as a free check.

  strike  put price  put IV  call price  call IV  IV gap (pts)
  ------  ---------  ------  ----------  -------  ------------
  254     20.09      49.96%  11.24       46.76%   +3.20
  261     23.72      47.08%  7.87        43.73%   +3.35

  LIVE CROSS-CHECK -- historical bar close vs the vendor's own
  official settled close for the same session:

  occ                    expiry      strike  type  hist close  official close  verdict  live IV
  ---------------------  ----------  ------  ----  ----------  --------------  -------  -------
  SPY   270115P00750000  2027-01-15  750     put   11.35       11.35           MATCH    16.56%
  SPY   270115P00700000  2027-01-15  700     put   5.34        5.34            MATCH    21.00%
  SPY   270115C00800000  2027-01-15  800     call  13.50       13.50           MATCH    11.99%
  SPY   261218C00760000  2026-12-18  760     call  33.72       33.72           MATCH    14.63%

  All four match the vendor's own settled close EXACTLY, so the
  price series this study analyses is the vendor's own price
  series.  Their live IVs are an independent confirmation of the
  put skew: on the live 2027-01-15 expiry the 750 put prints
  16.56% and the 700 put 21.00%, against the 800 call's 11.99%.

==============================================================================
9. VERDICT
==============================================================================
  1. THE SKEW.  [MEASURED] median 8.19 vol points per 10% OTM over
     15 fittable ladders, 95% bootstrap CI 7.00 to 9.01.
     The assumption under test is 1.5, so the measured skew is
     5.5x the assumption and the CI's lower end is still 4.7x it.
  2. THE PUT-CALL SPREAD.  [MEASURED] median 5.51 vol points
     (n=18, range 2.88 to 14.41).  The sibling's 1.5 vol-point
     haircut is below the MINIMUM observed spread.
  3. THE PREMIUM-SELLING EDGE ON REAL PRICES.  [MEASURED]
       n entries = 20, from 20 of the 20 drawn sample dates
       E_R = +0.0067 GROSS of costs, -0.0082 after LOW costs
       p = 0.8500;  bootstrap 95% CI for the mean R: -0.1843 to 0.1706
       The point estimate is a hair above zero gross and a hair
       BELOW zero after costs, and the 95% CI spans zero.
       READ THIS AS: NOT MEASURABLE AT THIS SAMPLE SIZE.
       What IS established:
       (a) the modelled +2.97% CAGR is NOT reproduced -- the
           best case measured here is +0.7% of max-loss per
           entry gross, and negative after costs;
       (b) the first pass's E_R = -0.0908 does NOT survive the
           larger sample -- it was one COVID loss in five
           entries, not a measured edge;
       (c) the skew treatment alone flips the sign: pricing the
           WING off the real ladder (variant A) versus a flat VIX
           on both legs (variant D) moves the mean R by only
           -0.0063, whereas charging the sold leg a 1.5 vol-point
           haircut (E) moves it to -0.0949 and 3.0 points (F) to
           -0.1704.  A haircut applied only to the sold leg
           OVERSTATES the damage, because the real skew lifts
           the wing too.
  4. NOT MEASURABLE AT ANY SIZE FROM THIS SOURCE:
     - any pre-2017 regime, including 2008 (the expired-contract
       catalogue floor is ~2017-09-15);
     - liquidity, bid/ask or a true MARK (option bars carry no
       volume, bid or ask -- every price here is a last-trade
       print);
     - the skew at the extreme wings, where the prints are
       $0.01-$0.10 and the IV is meaningless.

==============================================================================
END
```

---

## B. The independent hand-check

`handcheck.py` shares no code with `study.py` (a different `erf`, a bracket-expansion bisection, and OLS through the normal equations).  Section D of its output is the gap.

```
HANDCHECK -- independent re-derivation for real-skew-test
erf: Abramowitz & Stegun 7.1.26 (NOT math.erf)
IV : bracket expansion from sigma=0.20, then bisection
OLS: normal equations solved in closed form

==============================================================================
A. IMPLIED VOL FROM REAL PRICES, WITH EVERY INTERMEDIATE SHOWN
==============================================================================

  ---- SPY 2020-03-02  expiry 2020-04-17  PUT strike 300 ----
    bar_date        2020-03-02   (bar lag 0 days)
    real print      $10.08   OHLC 10.08/16.37/8.78/10.08
    spot S          309.09
    strike K        300.00
    days to expiry  46
    T = DTE/365     0.1260273973
    r (US03M, t-3)  1.515000%  on session 2020-02-26
    log(S/K)        +0.0298500220
    sqrt(T)         0.3550033764
    -> sigma        0.334360  (33.44%)
    BS intermediates at that sigma:
      sigma*sqrt(T) 0.1186988665
      d1            +0.3269116937
      d2            +0.2082128272
      N(d1)         0.6281325934
      N(d2)         0.5824685725
      N(-d1)        0.3718674066
      N(-d2)        0.4175314275
      K*exp(-rT)    299.4277519542
      BS price      $10.0800000000  (vs print $10.08)

  ---- SPY 2017-10-02  expiry 2017-11-10  PUT strike 245 ----
    bar_date        2017-10-02   (bar lag 0 days)
    real print      $0.89   OHLC 0.89/0.89/0.89/0.89
    spot S          252.32
    strike K        245.00
    days to expiry  39
    T = DTE/365     0.1068493151
    r (US03M, t-3)  1.057200%  on session 2017-09-27
    log(S/K)        +0.0294399127
    sqrt(T)         0.3268781349
    -> sigma        0.105858  (10.59%)
    BS intermediates at that sigma:
      sigma*sqrt(T) 0.0346027983
      d1            +0.9007421938
      d2            +0.8661393955
      N(d1)         0.8161373245
      N(d2)         0.8067931796
      N(-d1)        0.1838626755
      N(-d2)        0.1932068204
      K*exp(-rT)    244.7234015688
      BS price      $0.8900000000  (vs print $0.89)

  ---- SPY 2018-04-02  expiry 2018-05-11  CALL strike 265 ----
    bar_date        2018-04-02   (bar lag 0 days)
    real print      $3.12   OHLC 3.12/5.25/2.51/3.12
    spot S          257.47
    strike K        265.00
    days to expiry  39
    T = DTE/365     0.1068493151
    r (US03M, t-3)  1.720800%  on session 2018-03-27
    log(S/K)        -0.0288266175
    sqrt(T)         0.3268781349
    -> sigma        0.176176  (17.62%)
    BS intermediates at that sigma:
      sigma*sqrt(T) 0.0575879553
      d1            -0.4398448965
      d2            -0.4974328517
      N(d1)         0.3300247546
      N(d2)         0.3094419219
      N(-d1)        0.6699752454
      N(-d2)        0.6905580781
      K*exp(-rT)    264.5132019673
      BS price      $3.1200000000  (vs print $3.12)

  ---- SPY 2022-10-03  expiry 2022-11-11  PUT strike 330 ----
    bar_date        2022-10-03   (bar lag 0 days)
    real print      $3.22   OHLC 4.15/4.90/2.97/3.22
    spot S          366.61
    strike K        330.00
    days to expiry  39
    T = DTE/365     0.1068493151
    r (US03M, t-3)  3.330001%  on session 2022-09-28
    log(S/K)        +0.1052059583
    sqrt(T)         0.3268781349
    -> sigma        0.335521  (33.55%)
    BS intermediates at that sigma:
      sigma*sqrt(T) 0.1096743922
      d1            +1.0465367106
      d2            +0.9368623184
      N(d1)         0.8523433204
      N(d2)         0.8255853228
      N(-d1)        0.1476566796
      N(-d2)        0.1744146772
      K*exp(-rT)    328.8279189416
      BS price      $3.2200000000  (vs print $3.22)

  ---- SPY 2026-04-01  expiry 2026-05-08  CALL strike 695 ----
    bar_date        2026-04-01   (bar lag 0 days)
    real print      $1.80   OHLC 1.77/1.98/1.63/1.8
    spot S          655.24
    strike K        695.00
    days to expiry  37
    T = DTE/365     0.1013698630
    r (US03M, t-3)  3.691999%  on session 2026-03-26
    log(S/K)        -0.0589102648
    sqrt(T)         0.3183863424
    -> sigma        0.145897  (14.59%)
    BS intermediates at that sigma:
      sigma*sqrt(T) 0.0464517109
      d1            -1.1644094196
      d2            -1.2108611306
      N(d1)         0.1221291255
      N(d2)         0.1129743819
      N(-d1)        0.8778708745
      N(-d2)        0.8870256181
      K*exp(-rT)    692.4037721598
      BS price      $1.8000000000  (vs print $1.80)

==============================================================================
B. ONE LADDER'S SKEW SLOPE, BY HAND  (SPY 2020-03-02, 4 put prints)
==============================================================================

  spot 309.09   T 0.1260273973   r 1.515000%

  strike  price$   d=-ln(K/S)   IV%
  ------  -------  -----------  ------
     263     2.96  +0.16147846   42.1215
     278     5.04  +0.10601138   38.9818
     291     7.68  +0.06030923   35.8863
     300    10.08  +0.02985002   33.4360

  normal equations: n=4  sum(x)=0.35764910  sum(y)=150.4256
                    sum(x^2)=0.04184193  sum(xy)=14.09657278
  slope b         = 65.561119 vol pts per unit of d
  IV at d=0       = 31.7444%
  ln(1/0.90)      = 0.10536052
  slope per 10% OTM = b * ln(1/0.90) = 6.9076 vol points

==============================================================================
C. SETTLE ONE MEASURED SPREAD AGAINST THE REAL PATH
==============================================================================
  SPY 2020-03-02, short the 6%-OTM put, long the wing $5 lower,
  both priced from the MEASURED put ladder by linear interpolation
  in d = -ln(K/S), then settled at intrinsic on the expiry close.

  K_short 291   d 0.06030923   IV 35.8863%
  K_wing  286   d 0.07764069   IV 37.0602%
  BS put 291      $7.680000
  BS put 286      $6.534425
  credit (gross)  $114.5575
  cost (LOW)      $6.3000
  credit (net)    $108.2575
  REAL SPY close on the expiry session 2020-04-17: 286.64
  intrinsic loss  $436.0000
  pnl (gross)     $-321.4425
  max loss        $385.4425  (= width*100 - credit)
  R               -0.833957

==============================================================================
D. GAP AGAINST study.py
==============================================================================
  ladder slope, SPY 2020-03-02
    handcheck.py   6.9076 vol pts per 10% OTM
    study.py       6.9100
    GAP            0.002447 vol pts
  spread settlement, SPY 2020-03-02 short 291 / long 286
    handcheck.py   R = -0.8340
    study.py       R = -0.83
    GAP            0.003957 R  -- study.py's re-run TABLE prints
                   R to 2 decimals, so this gap is rounding,
                   not disagreement: both give -0.833957

  implied vols, section 1 of study.py vs here:
    date        type  strike   study.py IV   handcheck IV   gap
    2017-10-02  put      245    10.5900       10.5858      0.0042
    2018-04-02  call     265    17.6200       17.6176      0.0024
    2020-03-02  put      300    33.4400       33.4360      0.0040
    2022-10-03  put      330    33.5500       33.5521      0.0021
    2026-04-01  call     695    14.5900       14.5897      0.0003

==============================================================================
END
```

---

## C. The call budget

```
section  tool  calls  basis
DISCOVERY  get_option_chains  1  SPY: chain id + upcoming expiries
DISCOVERY  get_option_instruments  1  SPY 2018-02-09 state=expired with NO strike filter -> paged listing of 180 instruments on page 1. Proves the whole strike grid is listable, but at ~75 KB/page it is too large to repeat per date; the study therefore uses the strike filter with retries.
DISCOVERY  get_option_instruments  2  SPY 2018-02-09 strike 242.5 / 261 (known-present flakiness test; both ok on the first attempt here)
RESOLUTION  get_option_instruments  161  sum of the attempts column in instrument-ids.tsv for the 120 declared contracts (20 dates x 6). Includes every exact-strike retry and every declared neighbour probe.
RESOLUTION  get_option_instruments  2  supplementary ITM-put rows for 2020-04-01 (put_254x, put_261x) -- captured in error, kept as a put-call parity check
LIVE CHECK  get_option_instruments  4  2027-01-15 P750, P700, C800; 2026-12-18 C760
BARS  get_option_historicals  29  see logs/bar-log.tsv; 29 batches covering the 20 sample dates, 3 corrected re-pulls, 3 diagnostics, and the live check
LIVE CHECK  get_option_quotes  1  4 live ids: official prior-session close
TOTAL    201

PER-DATE RESOLUTION CALLS (from instrument-ids.tsv attempts column)
sample_date  expiry  contracts  resolution_calls  notes
2017-10-02  2017-11-10  6  16  put_227 needed 8 probes (225 used); put_214 needed 4 (215 used)
2018-04-02  2018-05-11  6  7  put_219 -> 220 on attempt 2
2018-10-01  2018-11-09  6  8  call_309 -> 310 on attempt 3
2019-04-01  2019-05-10  6  10  put_257 -> 255 (3); put_243 -> 245 (3)
2019-10-01  2019-11-08  6  12  put_264 -> 265 (4); put_249 -> 250 (4)
2020-02-24  2020-04-03  6  6  all first attempt
2020-03-02  2020-04-10 -> 2020-04-17  6  12  2020-04-10 is Good Friday (market closed): 6 empty calls, then 6 ok on the substitute expiry
2020-04-01  2020-05-08  6  7  put_209 never resolved (2)
2020-10-01  2020-11-06  6  9  put_286 never resolved (4)
2021-04-01  2021-05-07  6  10  put_361, put_341 never resolved (3 each)
2021-10-01  2021-11-05  6  6  put_369 never resolved (1)
2022-04-01  2022-05-06  6  6  all first attempt
2022-10-03  2022-11-11  6  7  put_312 never resolved (2)
2023-04-03  2023-05-12  6  6  all first attempt
2023-10-02  2023-11-10  6  6  all first attempt
2024-04-01  2024-05-10  6  6  put_444, call_553 never resolved (1 each)
2024-10-01  2024-11-08  6  7  put_512 (2), put_483 (1) never resolved
2025-04-01  2025-05-09  6  6  all first attempt
2025-10-01  2025-11-07  6  8  put_628 (2), put_602 (2), put_568 (1) never resolved
2026-04-01  2026-05-08  6  6  put_557 never resolved (1)
```

---

## D. The declared plan, as emitted before the pull

```
wrote C:\Users\sande\Documents\Projects\Skills\skills\14-finance\options-trading-playbook\examples\real-skew-test\logs\call-plan.tsv (122 contracts to resolve)
  panel ladder : 120 contracts
  panel parity : 2 contracts
  dates: 20
  --- expiry grid (sample_date -> expiry, DTE) ---
  2017-10-02 -> 2017-11-10 (39 DTE)
  2018-04-02 -> 2018-05-11 (39 DTE)
  2018-10-01 -> 2018-11-09 (39 DTE)
  2019-04-01 -> 2019-05-10 (39 DTE)
  2019-10-01 -> 2019-11-08 (38 DTE)
  2020-02-24 -> 2020-04-03 (39 DTE)
  2020-03-02 -> 2020-04-17 (46 DTE)
  2020-04-01 -> 2020-05-08 (37 DTE)
  2020-10-01 -> 2020-11-06 (36 DTE)
  2021-04-01 -> 2021-05-07 (36 DTE)
  2021-10-01 -> 2021-11-05 (35 DTE)
  2022-04-01 -> 2022-05-06 (35 DTE)
  2022-10-03 -> 2022-11-11 (39 DTE)
  2023-04-03 -> 2023-05-12 (39 DTE)
  2023-10-02 -> 2023-11-10 (39 DTE)
  2024-04-01 -> 2024-05-10 (39 DTE)
  2024-10-01 -> 2024-11-08 (38 DTE)
  2025-04-01 -> 2025-05-09 (38 DTE)
  2025-10-01 -> 2025-11-07 (37 DTE)
  2026-04-01 -> 2026-05-08 (37 DTE)
```
