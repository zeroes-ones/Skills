# RESULTS — real-quotes-test (verbatim tables from a real run)

Pull date **2026-10-15**.  Run date **2026-10-15**.  Every table below is
copied verbatim from `logs/study-output.txt` / `run-output.txt`, produced
by `py -3 study.py`.  Two consecutive runs are byte-identical (README §7).

Labels: **[MEASURED]** = computed from a real Robinhood option price.
**[MODELED]** = computed from the VIX proxy.

```
REAL-QUOTES-TEST -- measured option prices, measured skew, and what
the old MODELED numbers got wrong.

# PROVENANCE: source=Robinhood MCP get_option_historicals (real option OHLC, regular session)
# PROVENANCE: pull_date=2026-10-15
# PROVENANCE: underlying_close_source=TradingView AMEX:SPY / NASDAQ:QQQ / AMEX:IWM 1D close, carried from the sibling index-options-test pull (2026-10-14), re-verified there
# PROVENANCE: rate_source=TVC:US03M 1D close (per-cent per-annum yield index), carried from the same sibling pull
# PROVENANCE: expiry_rule=Friday weekly closest to 37 DTE
# PROVENANCE: ladder=puts 3%,6%,10%,15%,20% OTM, calls 3%,6%,10% OTM; target strike rounded to the nearest dollar, then substituted to the nearest LISTED strike where the grid lacks it (substituted=yes)
# PROVENANCE: rows=56  unresolved=29
# PROVENANCE: option bars carry NO volume (Robinhood does not publish it); interpolated bars are dropped; bar_date is the last non-interpolated session at or before sample_date

==============================================================================
1. REAL IMPLIED VOL PER CONTRACT  [MEASURED]
==============================================================================
  IV = bisection on Black-Scholes (European, q=0) using the REAL
  underlying close on the sample date, real calendar DTE/365, and the
  3-month bill yield (TVC:US03M) as the risk-free proxy.

  und  date        expiry      dte  type  strike  money    spot    price  IV_real%  delta   VIX_lag  IV_model%
  ---  ----------  ----------  ---  ----  ------  -------  ------  -----  --------  ------  -------  ---------
  IWM  2018-01-02  2018-02-09  38   put   149.00  -0.0318  153.9   1.05   15.02     -0.235  10.47    18.36    
  QQQ  2018-01-02  2018-02-09  38   call  163.00  0.0285   158.49  0.66   10.42     0.220   10.47    19.41    
  QQQ  2018-01-02  2018-02-09  38   put   154.00  -0.0283  158.49  1.30   15.46     -0.264  10.47    19.41    
  SPY  2018-01-02  2018-02-09  38   call  285.00  0.0604   268.77  0.02   7.48      0.009   10.47    10.47    
  SPY  2018-01-02  2018-02-09  38   put   242.50  -0.0977  268.77  0.26   18.68     -0.039  10.47    10.47    
  SPY  2018-01-02  2018-02-09  38   put   261.00  -0.0289  268.77  1.02   11.09     -0.190  10.47    10.47    
  SPY  2020-01-02  2020-02-07  36   call  335.00  0.0312   324.87  0.56   8.26      0.133   13.43    13.43    
  SPY  2020-01-02  2020-02-07  36   call  344.00  0.0589   324.87  0.08   8.88      0.024   13.43    13.43    
  SPY  2020-01-02  2020-02-07  36   put   275.00  -0.1535  324.87  0.16   25.63     -0.017  13.43    13.43    
  SPY  2020-01-02  2020-02-07  36   put   305.00  -0.0612  324.87  0.94   17.10     -0.109  13.43    13.43    
  SPY  2020-01-02  2020-02-07  36   put   315.00  -0.0304  324.87  1.90   14.05     -0.225  13.43    13.43    
  SPY  2020-03-02  2020-04-17  46   call  318.00  0.0288   309.09  5.02   19.25     0.362   27.56    27.56    
  SPY  2020-03-02  2020-04-17  46   call  328.00  0.0612   309.09  1.64   16.61     0.172   27.56    27.56    
  SPY  2020-03-02  2020-03-20  18   call  328.00  0.0612   309.09  0.46   18.58     0.081   27.56    27.56    
  SPY  2020-03-02  2020-04-17  46   call  340.00  0.1000   309.09  0.36   15.79     0.051   27.56    27.56    
  SPY  2020-03-02  2020-04-17  46   put   247.00  -0.2009  309.09  1.62   45.43     -0.069  27.56    27.56    
  SPY  2020-03-02  2020-04-17  46   put   263.00  -0.1491  309.09  2.96   42.12     -0.122  27.56    27.56    
  SPY  2020-03-02  2020-04-17  46   put   278.00  -0.1006  309.09  5.04   38.98     -0.198  27.56    27.56    
  SPY  2020-03-02  2020-03-20  18   put   278.00  -0.1006  309.09  2.78   49.18     -0.151  27.56    27.56    
  SPY  2020-03-02  2020-04-17  46   put   291.00  -0.0585  309.09  7.68   35.89     -0.290  27.56    27.56    
  SPY  2020-03-02  2020-04-17  46   put   300.00  -0.0294  309.09  10.08  33.44     -0.372  27.56    27.56    
  SPY  2020-03-02  2020-03-20  18   put   300.00  -0.0294  309.09  6.93   40.67     -0.351  27.56    27.56    
  SPY  2022-06-01  2022-07-08  37   call  422.00  0.0303   409.59  5.69   20.11     0.338   27.49    27.49    
  SPY  2022-06-01  2022-07-08  37   call  434.00  0.0596   409.59  2.27   18.67     0.177   27.49    27.49    
  SPY  2022-06-01  2022-07-08  37   put   369.00  -0.0991  409.59  2.60   30.28     -0.127  27.49    27.49    
  SPY  2022-06-01  2022-07-08  37   put   385.00  -0.0600  409.59  5.04   28.12     -0.227  27.49    27.49    
  SPY  2022-06-01  2022-07-08  37   put   397.00  -0.0307  409.59  8.00   26.43     -0.335  27.49    27.49    

  contracts with a real bar: 27 of 56 planned
  contracts with a real IV  : 27
  no implied vol (price under the no-arbitrage floor): 0
  no implied vol (above the 500% cap)               : 0

==============================================================================
2. THE MEASURED SKEW  [MEASURED]
==============================================================================
  Fit, per sample date, of IV against d = -ln(K/S) using the PUT
  ladder only (OTM puts).  d increases as the put goes further OTM.
  slope_per_10pct_OTM = coefficient * ln(1/0.90) vol points.

  und  date        n_puts  slope_10%OTM  r2     iv_atm%  put-call%  note        
  ---  ----------  ------  ------------  -----  -------  ---------  ------------
  SPY  2018-01-02  2       10.87         1.000  8.07     3.61                   
  SPY  2020-01-02  3       8.91          0.999  11.58    5.78                   
  SPY  2020-03-02  7       4.87          0.374  36.08    14.19                  
  SPY  2022-06-01  3       5.54          1.000  24.82    6.32                   
  QQQ  2018-01-02  1       n/a           n/a    n/a      n/a        too few puts
  IWM  2018-01-02  1       n/a           n/a    n/a      n/a        too few puts

  AGGREGATE (one observation per underlying-date with >=2 puts):
  stat    slope vol pts per 10% OTM
  ------  -------------------------
  n       4                        
  min     4.87                     
  q25     5.37                     
  median  7.22                     
  q75     9.40                     
  max     10.87                    
  mean    7.55                     

  put-call IV spread (vol points, put minus call, ~3% OTM):
  stat    put-call vol pts
  ------  ----------------
  n       4               
  min     3.61            
  median  6.05            
  max     14.19           
  mean    7.48            

  COMPARISON WITH THE ASSUMED 1.5 VOL POINTS:
    measured slopes above +1.5 vol pts/10% OTM : 4 of 4
    median measured slope                     : 7.22 vol pts
    the sibling study's flip point            : -1.5 vol pts
    NOTE the sign convention differs: the sibling applied a
    haircut of 1.5 vol points to the SOLD leg only, which is a
    LEVEL offset, not a slope.  The comparable measured number is
    the level difference between the ~16-delta put and ATM, see 5.

==============================================================================
3. MODEL ERROR: the old VIX-derived model vs the real prices  [MODELED] vs [MEASURED]
==============================================================================
  model price = Black-Scholes at IV_model = VIX(t-3)/100 * kappa.
  error = model - real.  A positive price error means the OLD study
  was TOO RICH, i.e. it over-credited the option seller.

  und  date        type  strike  money    real$  model$  price_err$  vol_err_pt  pct_err%
  ---  ----------  ----  ------  -------  -----  ------  ----------  ----------  --------
  IWM  2018-01-02  put   149.00  -0.0318  1.05   1.58    +0.53       3.34        50.8    
  QQQ  2018-01-02  call  163.00  0.0285   0.66   2.24    +1.58       9.00        238.7   
  QQQ  2018-01-02  put   154.00  -0.0283  1.30   1.99    +0.69       3.95        52.8    
  SPY  2018-01-02  call  285.00  0.0604   0.02   0.17    +0.15       2.99        772.6   
  SPY  2018-01-02  put   242.50  -0.0977  0.26   0.00    -0.26       -8.21       -99.1   
  SPY  2018-01-02  put   261.00  -0.0289  1.02   0.88    -0.14       -0.62       -14.0   
  SPY  2020-01-02  call  335.00  0.0312   0.56   2.02    +1.46       5.17        259.8   
  SPY  2020-01-02  call  344.00  0.0589   0.08   0.61    +0.53       4.55        668.1   
  SPY  2020-01-02  put   275.00  -0.1535  0.16   0.00    -0.16       -12.20      -99.9   
  SPY  2020-01-02  put   305.00  -0.0612  0.94   0.36    -0.58       -3.67       -61.6   
  SPY  2020-01-02  put   315.00  -0.0304  1.90   1.71    -0.19       -0.62       -9.8    
  SPY  2020-03-02  call  318.00  0.0288   5.02   8.52    +3.50       8.31        69.6    
  SPY  2020-03-02  call  328.00  0.0612   1.64   5.35    +3.71       10.95       226.5   
  SPY  2020-03-02  call  328.00  0.0612   0.46   1.76    +1.30       8.98        281.8   
  SPY  2020-03-02  call  340.00  0.1000   0.36   2.87    +2.51       11.77       698.3   
  SPY  2020-03-02  put   247.00  -0.2009  1.62   0.10    -1.52       -17.87      -94.1   
  SPY  2020-03-02  put   263.00  -0.1491  2.96   0.55    -2.41       -14.56      -81.5   
  SPY  2020-03-02  put   278.00  -0.1006  5.04   1.95    -3.09       -11.42      -61.3   
  SPY  2020-03-02  put   278.00  -0.1006  2.78   0.29    -2.49       -21.62      -89.4   
  SPY  2020-03-02  put   291.00  -0.0585  7.68   4.66    -3.02       -8.33       -39.3   
  SPY  2020-03-02  put   300.00  -0.0294  10.08  7.66    -2.42       -5.88       -24.0   
  SPY  2020-03-02  put   300.00  -0.0294  6.93   3.68    -3.25       -13.11      -46.8   
  SPY  2022-06-01  call  422.00  0.0303   5.69   9.31    +3.62       7.38        63.6    
  SPY  2022-06-01  call  434.00  0.0596   2.27   5.74    +3.47       8.82        152.8   
  SPY  2022-06-01  put   369.00  -0.0991  2.60   1.89    -0.71       -2.79       -27.4   
  SPY  2022-06-01  put   385.00  -0.0600  5.04   4.80    -0.24       -0.63       -4.9    
  SPY  2022-06-01  put   397.00  -0.0307  8.00   8.50    +0.50       1.06        6.3     

  ERROR DISTRIBUTION (n=27 contracts with a real IV):
  stat    price err $  vol-pt err  pct err %
  ------  -----------  ----------  ---------
  min     -3.25        -21.62      -99.9    
  q25     -1.12        -8.27       -54.0    
  median  -0.14        -0.62       -4.9     
  q75     1.38         6.27        189.6    
  max     3.71         11.77       772.6    
  mean    0.11         -1.31       103.3    

  by moneyness band (price error $):
  band   n   median  mean 
  -----  --  ------  -----
  3-6%   19  0.53    0.59 
  6-12%  5   -0.71   -0.81
  >12%   3   -1.52   -1.37

  by tenor bucket (price error $):
  bucket     n   median  mean 
  ---------  --  ------  -----
  10-19 DTE  3   -2.49   -1.48
  30-39 DTE  16  0.33    0.64 
  40-49 DTE  8   -1.97   -0.34

==============================================================================
4. IV TERM STRUCTURE  [MEASURED]
==============================================================================
  One date (SPY 2020-03-02), two expiries, three common strikes.
  type  strike  dte_short  IV_short%  px_short  dte_long  IV_long%  px_long
  ----  ------  ---------  ---------  --------  --------  --------  -------
  put   300     18         40.67      6.93      46        33.44     10.08  
  put   278     18         49.18      2.78      46        38.98     5.04   
  call  328     18         18.58      0.46      46        16.61     1.64   

  Read: the LONGER expiry is richer in absolute price but its IV
  is the comparable number.  Only 3 strikes were measured.

==============================================================================
5. PREMIUM-SELLING RE-RUN WITH THE MEASURED IV  [MEASURED]
==============================================================================
  Sibling programme S2: each month sell a ~30-DTE put spread, short
  leg near 6% OTM (~16 delta), long wing $5 lower, hold to expiry,
  settle against the REAL underlying close.

  Here the SHORT leg is priced at the IV measured on the ladder,
  linearly interpolated in log-moneyness across the measured points;
  the WING at the wing's own moneyness.  No VIX is used anywhere in
  this section -- that is the whole point of the re-run.

  und  entry       K_short  K_wing  IV_short%  IV_wing%  credit$  R      note            
  ---  ----------  -------  ------  ---------  --------  -------  -----  ----------------
  SPY  2018-01-02  253      248     14.30      16.36     14.53    +0.03  S_T=261.50      
  SPY  2020-01-02  305      300     17.10      18.46     27.72    +0.06  S_T=332.20      
  SPY  2020-03-02  291      286     35.89      37.06     114.56   -0.83  S_T=286.64      
  SPY  2022-06-01  385      380     28.12      28.78     92.57    +0.23  S_T=388.67      
  QQQ  2018-01-02  149      144     15.46      15.46     30.05    +0.06  S_T=156.10      
  IWM  2018-01-02  n/a      n/a     n/a        n/a       n/a      n/a    ladder too short

  MEASURED programme over the 5 entries above:
  stat                   value  
  ---------------------  -------
  n entries              5      
  p  (win rate)          0.8000 
  b  (mean win R)        0.0949 
  E  (mean R per entry)  -0.0908
  median R               0.0587 
  min R                  -0.8340
  max R                  0.2272 

  COMPARISON WITH THE SIBLING [MODELED] RESULT:
    sibling, no skew haircut : CAGR +2.97%, 89% of months positive
    sibling, +1.5 vol pts    : CAGR -0.87% (sign FLIPS)
    sibling, +3.0 vol pts    : CAGR -4.03%
    this re-run, measured IV : E_R = -0.0908, sign NEGATIVE
    NOTE: 5 measured entries, not 306 months.  This is a partial
    measured window and is NOT a CAGR.

==============================================================================
6. IS THE SKEW STABLE?  [MEASURED]
==============================================================================
  One row per measured date, ordered in time.  A single assumed
  number is defensible only if these do not move much.

  date        und  slope_10%OTM  put-call%
  ----------  ---  ------------  ---------
  2018-01-02  SPY  10.87         3.61     
  2020-01-02  SPY  8.91          5.78     
  2020-03-02  SPY  4.87          14.19    
  2022-06-01  SPY  5.54          6.32     

  STRESS CHECK: the deepest stress date measured is 2020-03-02
  (COVID).  2008 is NOT reachable -- the Robinhood expired-contract
  catalogue starts at 2017-09-15, so no pre-2017 crisis exists in
  this data.

==============================================================================
END
==============================================================================
```
