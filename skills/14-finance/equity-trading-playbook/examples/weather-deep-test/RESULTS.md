# RESULTS -- weather-deep-test

Every number below is the verbatim stdout of a real run on the real data in
`data/`.  Nothing in this file was typed by hand or carried over from another
study.

Reproduce with:

```
export PYTHONIOENCODING=utf-8
py -3 pull_ohlcv.py --results <tool-results dirs> --out data --pull-date 2026-10-14
py -3 reuse_sibling_data.py --data data --sibling ../frontier-test/data --name SPY
py -3 verify_sources.py
py -3 study.py      > logs/run-output.txt
py -3 handcheck.py  > logs/handcheck-output.txt
py -3 make-results.py
```

Determinism: `study.py` was run twice and the two stdouts are byte-identical
(`diff logs/det-A.txt logs/det-B.txt` is empty), and every one of the artefact
hashes below is stable across runs.

## `out/` artefacts written by this run (sha256 prefix)

```
  book_daily_div_0bps.csv                dd1adaa79e0d6e79
  book_daily_div_20bps.csv               bfa7cc6ad62294e5
  book_daily_div_5bps.csv                db627a0ae2385931
  book_daily_price_0bps.csv              9d6b9df50c41c08b
  book_daily_price_20bps.csv             1ca39b6a4573369e
  book_daily_price_5bps.csv              4890fcfbb57ea98b
  book_monthly_div_0bps.csv              79134ac9afcb1de6
  book_monthly_div_20bps.csv             d1efe433c3c217bc
  book_monthly_div_5bps.csv              00a5ea551e173fb0
  book_monthly_price_0bps.csv            b9dead1b62a21253
  book_monthly_price_20bps.csv           dcbc5950ad211734
  book_monthly_price_5bps.csv            eb1b6c11d6504c0e
  book_weights.csv                       c5babc70dac88189
  cash_daily.csv                         2ab3b3981bd7ea3c
  corr_yearly.csv                        ea07b0d73d822989
  corr_yearly_reduced.csv                8acaffe19a7e3544
  data_inventory.csv                     7f513f8f83923929
  horizon.csv                            14489e1a6eb569c3
  lambda_frontier.csv                    3b1d1181fb7e9dde
  preregistration.txt                    ef8ea98b4a3f4e35
  regime.csv                             fd8142f69a2afa1a
  sleeve_daily_div_0bps.csv              a84903597d0888a6
  sleeve_daily_div_20bps.csv             a07d13996737bac8
  sleeve_daily_div_5bps.csv              63141b7909e74cf4
  sleeve_daily_price_0bps.csv            fc707c22120de9e6
  sleeve_daily_price_20bps.csv           4604823fa26456b1
  sleeve_daily_price_5bps.csv            f615cb4d92f58b84
  sleeve_monthly_div_0bps.csv            2b9c56b42ce457e7
  sleeve_monthly_div_20bps.csv           6be56d49b19cfe68
  sleeve_monthly_div_5bps.csv            3c78ba4e7a324b62
  sleeve_monthly_price_0bps.csv          c03b9136520b6cef
  sleeve_monthly_price_20bps.csv         2ee429715d9a0001
  sleeve_monthly_price_5bps.csv          af7c9390212b4f51
  summary.csv                            8aa10d140db8216c
  vrp_rolls.csv                          69b4c76ce8b9c334
  years.csv                              3a080adbeaa8d28b
```


## PULL -- MCP payload on disk -> data/*.csv

`pull-output.txt` -- sha256 `1f1e663155511f68b857291438003cb6079cc9de430155add05d2154dba46e0f`

```
  SKIP (unmapped symbol 'NASDAQ:AAPL') mcp__tradingview__mcp-tv-get-ohlcv-call_s5dqs68h-800b30dc-c8ce-4955-85c2-9f9302279a60.txt
  SKIP (unmapped symbol 'NASDAQ:MSFT') mcp__tradingview__mcp-tv-get-ohlcv-call_vds5cvxx-22955045-4082-46c5-a37b-6f8e2ef4a72a.txt
  SKIP (unmapped symbol 'NASDAQ:NVDA') mcp__tradingview__mcp-tv-get-ohlcv-call_y773yvib-7b845952-26d1-4b31-9ea2-b50575119a85.txt
  SKIP (unmapped symbol 'NASDAQ:AMZN') mcp__tradingview__mcp-tv-get-ohlcv-call_g0tgtl5r-f2855aaa-6e7e-4851-b675-498ca264b9d3.txt
  SKIP (unmapped symbol 'NASDAQ:GOOGL') mcp__tradingview__mcp-tv-get-ohlcv-call_lm2zfyp1-6381c399-e2be-42a3-9443-39d3dc8b0e49.txt
  SKIP (unmapped symbol 'NASDAQ:META') mcp__tradingview__mcp-tv-get-ohlcv-call_f13v1abp-042e93f7-89f6-44e4-9871-992da77ed352.txt
  SKIP (unmapped symbol 'NASDAQ:TSLA') mcp__tradingview__mcp-tv-get-ohlcv-call_diqfr9p3-ab9255fc-bcc8-4679-a089-a91acce3b965.txt
  SKIP (unmapped symbol 'NASDAQ:AVGO') mcp__tradingview__mcp-tv-get-ohlcv-call_rgu9qqd6-e2a18179-416c-4106-a38e-59d30267d596.txt
  SKIP (unmapped symbol 'NYSE:JPM') mcp__tradingview__mcp-tv-get-ohlcv-call_phzk8mni-06829a3d-c600-4f2c-8e60-9f8afa6ae5ee.txt
  SKIP (unmapped symbol 'NYSE:JNJ') mcp__tradingview__mcp-tv-get-ohlcv-call_trer4eq5-c0726c6e-4bd5-42ea-8ea5-7d32dc650ecc.txt
  SKIP (unmapped symbol 'NYSE:XOM') mcp__tradingview__mcp-tv-get-ohlcv-call_yqn5lq92-a600a3b0-4c94-42da-93c3-8aa97286da33.txt
  SKIP (unmapped symbol 'NYSE:UNH') mcp__tradingview__mcp-tv-get-ohlcv-call_zmh0ic6f-cf1f0b80-9eea-4054-b80c-82768b87bc5f.txt
  SKIP (unmapped symbol 'NYSE:V') mcp__tradingview__mcp-tv-get-ohlcv-call_9ucndcvc-1654f13b-c219-4a81-a10e-e6e91f7f4d62.txt
  SKIP (unmapped symbol 'NASDAQ:WMT') mcp__tradingview__mcp-tv-get-ohlcv-call_pdiqo7pq-a20cfbe8-b856-48f3-8e96-14fa0078bb7e.txt
  SKIP (unmapped symbol 'NASDAQ:AAPL') mcp__tradingview__mcp-tv-get-ohlcv-call_4sgbt6m3-b0edfa1c-cd82-4887-a8c6-1f856d726ccf.txt
  SKIP (unmapped symbol 'NASDAQ:MSFT') mcp__tradingview__mcp-tv-get-ohlcv-call_bqjtldkh-e2d973f0-c933-4a47-a9fe-728469cb682a.txt
  SKIP (unmapped symbol 'NASDAQ:NVDA') mcp__tradingview__mcp-tv-get-ohlcv-call_hylgrf45-da898eb8-499f-498a-b50a-de3bb6a7425e.txt
  SKIP (unmapped symbol 'NASDAQ:AMZN') mcp__tradingview__mcp-tv-get-ohlcv-call_n9cnk5d3-950594fb-4b8e-4357-bedf-e690bbce97e3.txt
  SKIP (unmapped symbol 'NASDAQ:GOOGL') mcp__tradingview__mcp-tv-get-ohlcv-call_uel5ftwh-807634e8-281b-4cc1-a7a2-db23e6fed1e2.txt
  SKIP (unmapped symbol 'NYSE:JPM') mcp__tradingview__mcp-tv-get-ohlcv-call_65er9hb6-cbf47628-0c95-42cc-9cf3-b2945cb2d034.txt
  SKIP (unmapped symbol 'NYSE:JNJ') mcp__tradingview__mcp-tv-get-ohlcv-call_8mhvd7nc-52a62353-2799-492f-80d1-6ba9e2189474.txt
  SKIP (unmapped symbol 'NASDAQ:WMT') mcp__tradingview__mcp-tv-get-ohlcv-call_719ysqgn-a7510ddb-9ab8-42dc-8905-23d1731d25c6.txt
  SKIP (unmapped symbol 'NYSE:XOM') mcp__tradingview__mcp-tv-get-ohlcv-call_dqfl5o3n-930015a2-5b87-4316-bde9-73396582f8cf.txt
  SKIP (unmapped symbol 'NYSE:UNH') mcp__tradingview__mcp-tv-get-ohlcv-call_vaqwhguz-801a2a5a-241c-417a-999c-fbab0b9b95d5.txt
  SKIP (unmapped symbol 'NYSE:V') mcp__tradingview__mcp-tv-get-ohlcv-call_2ve5gy50-f1b24ed2-0eb4-4688-b825-5bae71d775f7.txt
  SKIP (unmapped symbol 'NASDAQ:AVGO') mcp__tradingview__mcp-tv-get-ohlcv-call_th1yn86z-3cb613c8-11d1-411e-aba3-eb5ca0522ff6.txt
  files read (after de-duplication by content): 78

PAYLOADS FOUND
  AMEX:BIL     1 page(s)
  AMEX:DBC     1 page(s)
  AMEX:DIA     1 page(s)
  AMEX:EDV     1 page(s)
  AMEX:EEM     2 page(s)
  AMEX:EFA     1 page(s)
  AMEX:EWJ     1 page(s)
  AMEX:EWZ     1 page(s)
  AMEX:FXI     1 page(s)
  AMEX:GDX     1 page(s)
  AMEX:GLD     2 page(s)
  AMEX:HYG     1 page(s)
  AMEX:ILF     1 page(s)
  AMEX:IWM     2 page(s)
  AMEX:LQD     1 page(s)
  AMEX:MDY     1 page(s)
  AMEX:SLV     1 page(s)
  AMEX:SPY     3 page(s)
  AMEX:TIP     1 page(s)
  AMEX:TLH     1 page(s)
  AMEX:UUP     1 page(s)
  AMEX:VNQ     1 page(s)
  AMEX:XLE     1 page(s)
  AMEX:XLK     1 page(s)
  AMEX:XLP     1 page(s)
  AMEX:XLU     1 page(s)
  AMEX:XLV     1 page(s)
  NASDAQ:EMB   1 page(s)
  NASDAQ:IEF   2 page(s)
  NASDAQ:QQQ   3 page(s)
  NASDAQ:SHY   1 page(s)
  NASDAQ:TLT   2 page(s)
  TVC:DXY      1 page(s)
  TVC:US02Y    1 page(s)
  TVC:US03M    3 page(s)
  TVC:US10Y    1 page(s)
  TVC:US30Y    1 page(s)
  TVC:VIX      4 page(s)

MERGE + WRITE
  BIL    -> BIL_1d.csv     rows=4876   2007-05-30 .. 2026-10-14
  DBC    -> DBC_1d.csv     rows=5206   2006-02-03 .. 2026-10-14
  DIA    -> DIA_1d.csv     rows=7229   1998-01-20 .. 2026-10-14
  EDV    -> EDV_1d.csv     rows=4717   2007-12-13 .. 2026-10-14
  EEM    -> EEM_1d.csv     rows=5915   2003-04-11 .. 2026-10-14
  EFA    -> EFA_1d.csv     rows=6326   2001-08-17 .. 2026-10-14
  EWJ    -> EWJ_1d.csv     rows=7694   1996-03-18 .. 2026-10-14
  EWZ    -> EWZ_1d.csv     rows=6569   2000-07-14 .. 2026-10-14
  FXI    -> FXI_1d.csv     rows=5539   2004-10-08 .. 2026-10-14
  GDX    -> GDX_1d.csv     rows=5132   2006-05-22 .. 2026-10-14
  GLD    -> GLD_1d.csv     rows=5510   2004-11-18 .. 2026-10-14
  HYG    -> HYG_1d.csv     rows=4910   2007-04-11 .. 2026-10-14
  ILF    -> ILF_1d.csv     rows=6243   2001-10-26 .. 2026-10-14
  IWM    -> IWM_1d.csv     rows=6635   2000-05-26 .. 2026-10-14
  LQD    -> LQD_1d.csv     rows=6094   2002-07-26 .. 2026-10-14
  MDY    -> MDY_1d.csv     rows=7908   1995-05-12 .. 2026-10-14
  SLV    -> SLV_1d.csv     rows=5148   2006-04-28 .. 2026-10-14
  SPY    -> SPY_1d.csv     rows=8000   1994-12-30 .. 2026-10-14
  TIP    -> TIP_1d.csv     rows=5750   2003-12-05 .. 2026-10-14
  TLH    -> TLH_1d.csv     rows=4971   2007-01-11 .. 2026-10-14
  UUP    -> UUP_1d.csv     rows=4944   2007-02-20 .. 2026-10-14
  VNQ    -> VNQ_1d.csv     rows=5546   2004-09-29 .. 2026-10-14
  XLE    -> XLE_1d.csv     rows=6995   1998-12-22 .. 2026-10-14
  XLK    -> XLK_1d.csv     rows=6995   1998-12-22 .. 2026-10-14
  XLP    -> XLP_1d.csv     rows=6995   1998-12-22 .. 2026-10-14
  XLU    -> XLU_1d.csv     rows=6995   1998-12-22 .. 2026-10-14
  XLV    -> XLV_1d.csv     rows=6995   1998-12-22 .. 2026-10-14
  EMB    -> EMB_1d.csv     rows=4733   2007-12-19 .. 2026-10-14
  IEF    -> IEF_1d.csv     rows=6094   2002-07-26 .. 2026-10-14
  QQQ    -> QQQ_1d.csv     rows=6943   1999-03-10 .. 2026-10-14
  SHY    -> SHY_1d.csv     rows=6094   2002-07-26 .. 2026-10-14
  TLT    -> TLT_1d.csv     rows=6094   2002-07-26 .. 2026-10-14
  DXY    -> DXY_1d.csv     rows=8000   1995-03-21 .. 2026-10-14
  US02Y  -> US02Y_1d.csv   rows=7342   1994-08-22 .. 2026-10-14
  US03M  -> US03M_1d.csv   rows=18197  1954-01-04 .. 2026-10-14
  US10Y  -> US10Y_1d.csv   rows=7662   1992-07-08 .. 2026-10-14
  US30Y  -> US30Y_1d.csv   rows=7439   1993-06-16 .. 2026-10-14
  VIX    -> VIX_1d.csv     rows=9283   1990-01-03 .. 2026-10-14

REQUESTED BUT NO PAYLOAD ON DISK (failed to resolve, or the response was small enough to stay inline):

DONE: 38 file(s)
```

## REUSE -- extending SPY back to 1993 from the sibling study, with overlap verification

`reuse-output.txt` -- sha256 `62a30122ab583bc2a5e01308092bafa8a64bfc55fc42a0fb7d8b7cdfdd95aa40`

```
VERIFY OVERLAP
  sibling ../frontier-test/data\SPY_1d.csv: 8485 rows, 1993-01-29 .. 2026-10-14
  this study data\SPY_1d.csv: 8000 rows, 1994-12-30 .. 2026-10-14
  overlapping dates: 8000
  identical rows:      7999
  last-bar exceptions: 1
      2026-10-14 volume differs (sibling 55687118 vs this study 55591868) -- the final bar is still forming
  rows only in the sibling file: 485 (1993-01-29 .. 1994-12-29)

WROTE data\SPY_1d.csv  rows=8485  1993-01-29 .. 2026-10-14
```

## SOURCE CROSS-CHECK -- this study's data against the sibling studies' independent pulls

`source-check.txt` -- sha256 `6419a795c2d71fe9c03b954a125e087e4d39f18e62d50464907d95b15c966a35`

```
==============================================================================
SIBLING: frontier-test  (C:\Users\sande\Documents\Projects\Skills\skills\14-finance\equity-trading-playbook\examples\frontier-test\data)
==============================================================================
  SPY    mine=8485  1993-01-29..2026-10-14 | sibling=8485  1993-01-29..2026-10-14 | shared=8485  identical=8484  vol-only-warn=1    OK
  QQQ    mine=6943  1999-03-10..2026-10-14 | sibling=6943  1999-03-10..2026-10-14 | shared=6943  identical=6942  vol-only-warn=1    OK
  IWM    mine=6635  2000-05-26..2026-10-14 | sibling=6635  2000-05-26..2026-10-14 | shared=6635  identical=6635  vol-only-warn=0    OK
  TLT    mine=6094  2002-07-26..2026-10-14 | sibling=6094  2002-07-26..2026-10-14 | shared=6094  identical=6093  vol-only-warn=1    OK
  GLD    mine=5510  2004-11-18..2026-10-14 | sibling=5510  2004-11-18..2026-10-14 | shared=5510  identical=5509  vol-only-warn=1    OK
  EEM    mine=5915  2003-04-11..2026-10-14 | sibling=5915  2003-04-11..2026-10-14 | shared=5915  identical=5914  vol-only-warn=1    OK
  IEF    mine=6094  2002-07-26..2026-10-14 | sibling=6094  2002-07-26..2026-10-14 | shared=6094  identical=6094  vol-only-warn=0    OK
  HYG    mine=4910  2007-04-11..2026-10-14 | sibling=4910  2007-04-11..2026-10-14 | shared=4910  identical=4910  vol-only-warn=0    OK
  DBC    mine=5206  2006-02-03..2026-10-14 | sibling=5206  2006-02-03..2026-10-14 | shared=5206  identical=5206  vol-only-warn=0    OK
  VNQ    mine=5546  2004-09-29..2026-10-14 | sibling=5546  2004-09-29..2026-10-14 | shared=5546  identical=5546  vol-only-warn=0    OK
  EFA    mine=6326  2001-08-17..2026-10-14 | sibling=6326  2001-08-17..2026-10-14 | shared=6326  identical=6326  vol-only-warn=0    OK
  BIL    mine=4876  2007-05-30..2026-10-14 | sibling=4876  2007-05-30..2026-10-14 | shared=4876  identical=4876  vol-only-warn=0    OK
  US03M  mine=18197 1954-01-04..2026-10-14 | sibling=18197 1954-01-04..2026-10-14 | shared=18197 identical=18197 vol-only-warn=0    OK
  VIX    mine=9283  1990-01-03..2026-10-14 | sibling=9283  1990-01-03..2026-10-14 | shared=9283  identical=9283  vol-only-warn=0    OK

==============================================================================
SIBLING: narrow-universe-test  (C:\Users\sande\Documents\Projects\Skills\skills\14-finance\equity-trading-playbook\examples\narrow-universe-test\data)
==============================================================================
  SPY    mine=8485  1993-01-29..2026-10-14 | sibling=8485  1993-01-29..2026-10-14 | shared=8485  identical=8484  vol-only-warn=1    OK
  QQQ    mine=6943  1999-03-10..2026-10-14 | sibling=6943  1999-03-10..2026-10-14 | shared=6943  identical=6942  vol-only-warn=1    OK
  IWM    mine=6635  2000-05-26..2026-10-14 | sibling=6635  2000-05-26..2026-10-14 | shared=6635  identical=6635  vol-only-warn=0    OK
  TLT    mine=6094  2002-07-26..2026-10-14 | sibling=6094  2002-07-26..2026-10-14 | shared=6094  identical=6093  vol-only-warn=1    OK
  GLD    mine=5510  2004-11-18..2026-10-14 | sibling=5510  2004-11-18..2026-10-14 | shared=5510  identical=5509  vol-only-warn=1    OK
  EEM    mine=5915  2003-04-11..2026-10-14 | sibling=5915  2003-04-11..2026-10-14 | shared=5915  identical=5914  vol-only-warn=1    OK
  BIL    mine=4876  2007-05-30..2026-10-14 | sibling=4876  2007-05-30..2026-10-14 | shared=4876  identical=4876  vol-only-warn=0    OK
  US03M  mine=18197 1954-01-04..2026-10-14 | sibling=18197 1954-01-04..2026-10-14 | shared=18197 identical=18197 vol-only-warn=0    OK
  VIX    mine=9283  1990-01-03..2026-10-14 | sibling=9283  1990-01-03..2026-10-14 | shared=9283  identical=9283  vol-only-warn=0    OK

==============================================================================
SIBLING: regime-study  (C:\Users\sande\Documents\Projects\Skills\skills\14-finance\equity-trading-playbook\examples\regime-study\data)
==============================================================================
  SPY    mine=8485  1993-01-29..2026-10-14 | sibling=8485  1993-01-29..2026-10-14 | shared=8485  identical=8485  vol-only-warn=0    OK
  QQQ    mine=6943  1999-03-10..2026-10-14 | sibling=6943  1999-03-10..2026-10-14 | shared=6943  identical=6943  vol-only-warn=0    OK
  TLT    mine=6094  2002-07-26..2026-10-14 | sibling=6094  2002-07-26..2026-10-14 | shared=6094  identical=6094  vol-only-warn=0    OK
  GLD    mine=5510  2004-11-18..2026-10-14 | sibling=5510  2004-11-18..2026-10-14 | shared=5510  identical=5510  vol-only-warn=0    OK

==============================================================================
SIBLING: sweep-test  (C:\Users\sande\Documents\Projects\Skills\skills\14-finance\equity-trading-playbook\examples\sweep-test\data)
==============================================================================
  SPY    mine=8485  1993-01-29..2026-10-14 | sibling=8485  1993-01-29..2026-10-14 | shared=8485  identical=8485  vol-only-warn=0    OK
  QQQ    mine=6943  1999-03-10..2026-10-14 | sibling=6943  1999-03-10..2026-10-14 | shared=6943  identical=6942  vol-only-warn=1    OK
  IWM    mine=6635  2000-05-26..2026-10-14 | sibling=6635  2000-05-26..2026-10-14 | shared=6635  identical=6635  vol-only-warn=0    OK
  TLT    mine=6094  2002-07-26..2026-10-14 | sibling=6094  2002-07-26..2026-10-14 | shared=6094  identical=6094  vol-only-warn=0    OK
  GLD    mine=5510  2004-11-18..2026-10-14 | sibling=5510  2004-11-18..2026-10-14 | shared=5510  identical=5510  vol-only-warn=0    OK
  EEM    mine=5915  2003-04-11..2026-10-14 | sibling=5915  2003-04-11..2026-10-14 | shared=5915  identical=5896  vol-only-warn=19   OK
  IEF    mine=6094  2002-07-26..2026-10-14 | sibling=6094  2002-07-26..2026-10-14 | shared=6094  identical=6094  vol-only-warn=0    OK
  HYG    mine=4910  2007-04-11..2026-10-14 | sibling=4910  2007-04-11..2026-10-14 | shared=4910  identical=4910  vol-only-warn=0    OK
  DBC    mine=5206  2006-02-03..2026-10-14 | sibling=5206  2006-02-03..2026-10-14 | shared=5206  identical=5206  vol-only-warn=0    OK
  VNQ    mine=5546  2004-09-29..2026-10-14 | sibling=5546  2004-09-29..2026-10-14 | shared=5546  identical=5546  vol-only-warn=0    OK
  EFA    mine=6326  2001-08-17..2026-10-14 | sibling=6326  2001-08-17..2026-10-14 | shared=6326  identical=6326  vol-only-warn=0    OK
  VIX    mine=9283  1990-01-03..2026-10-14 | sibling=9283  1990-01-03..2026-10-14 | shared=9283  identical=9283  vol-only-warn=0    OK

==============================================================================
SIBLING: weather-test  (C:\Users\sande\Documents\Projects\Skills\skills\14-finance\equity-trading-playbook\examples\weather-test\data)
==============================================================================
  SPY    mine=8485  1993-01-29..2026-10-14 | sibling=8485  1993-01-29..2026-10-14 | shared=8485  identical=8485  vol-only-warn=0    OK
  TLT    mine=6094  2002-07-26..2026-10-14 | sibling=6094  2002-07-26..2026-10-14 | shared=6094  identical=6094  vol-only-warn=0    OK
  GLD    mine=5510  2004-11-18..2026-10-14 | sibling=5510  2004-11-18..2026-10-14 | shared=5510  identical=5510  vol-only-warn=0    OK
  EEM    mine=5915  2003-04-11..2026-10-14 | sibling=5915  2003-04-11..2026-10-14 | shared=5915  identical=5915  vol-only-warn=0    OK
  VIX    mine=9283  1990-01-03..2026-10-14 | sibling=9283  1990-01-03..2026-10-14 | shared=9283  identical=9283  vol-only-warn=0    OK

==============================================================================
TOTAL: 44 file pairs compared, 311224 shared dates, 311194 identical, 0 price disagreements, 30 volume-only warnings
==============================================================================
```

## STUDY.PY -- the run, verbatim

`run-output.txt` -- sha256 `afacada1736ed0a2eaeb1ecef6075259cf39afa004991124ff2d3e90100dde3d`

```

==============================================================================
WEATHER-DEEP-TEST -- PRE-REGISTRATION (declared before any result)
==============================================================================
  window (primary)   2005-09-30 .. last data date  (0.00 years)
  window (reduced)   1998-12-22 .. last data date
  T  trend           every instrument in the verified universe; long when its own close > its own SMA(200) on the rebalance close, else flat; portfolio = INVERSE-VOLATILITY weights over the instruments that exist at that date, renormalised to 1; rebalanced monthly; flat capital earns the cash rate
     universe        31 instruments: SPY,QQQ,IWM,MDY,DIA,TLT,TLH,EDV,IEF,SHY,TIP,LQD,HYG,EMB,GLD,SLV,GDX,DBC,VNQ,EEM,EFA,EWJ,FXI,ILF,EWZ,UUP,XLE,XLU,XLK,XLP,XLV
     vol window      60 trading days
  C  carry/credit    long HYG and short IEF at inverse-vol weights summing to 1; the short leg's proceeds earn the cash rate; the long leg is credited its estimated dividend and the short leg PAYS the estimated dividend.  Live only when BOTH legs exist; cash before that.
  V  VRP [MODELED]   monthly short 30-DTE put spread on SPY; short strike at |delta| = 0.16 under IV = VIX(t-3); long strike 5% lower; short strike priced at ATM + 1.5 vol pt, long at ATM + 3.0 vol pt; daily Black-Scholes mark, settled at intrinsic vs the real SPY path; return is P&L divided by the spread WIDTH (a conservative margin proxy)
  V  sensitivity     skew steepness re-run at [0.0, 1.5, 3.0] vol points; 1.5 is the BASE case and is the sibling study's break-even
  H  hedge a         equal-risk long GLD/UUP when VIX(close) > SMA(50) of VIX, else flat (cash)
  H  hedge b [MODELED] always-on long 60-DTE 5%-OTM SPY put overlay with a premium budget of 5.0% of sleeve capital PER YEAR, spent at 1/12 a month, rolled monthly
  H  in the book     50% H_a + 50% H_b, fixed
  X  x-sec mom       each month hold the top 5 instruments by trailing 126-day return, equal-weight, rest cash; NO tuning
  B  baseline        100% SPY buy and hold
  BOOK               C 0.15 + CASH 0.10 + H 0.10 + T 0.40 + V 0.10 + X 0.15
  BOOK-NOV           C 0.17 + CASH 0.10 + H 0.11 + T 0.45 + X 0.17
  REDUCED            BOND10M 0.15 + C 0.00 + CASH 0.10 + H 0.10 + T 0.40 + V 0.10 + X 0.15
  REDUCED screen     an EXISTENCE screen only: the trend universe restricted to the instruments with a print on 1998-12-22
  cost levels        round-trip 0.0, 5.0, 20.0 bps; one-way = half of that per unit notional traded
  dividend           constant [ESTIMATED] yields applied per trading day; SPY 1.80%/yr, universe mean 2.38%/yr
  cash               [UPPER BOUND] TVC:US03M 3-month T-bill yield accrued at yield/252 per trading day, no fees, no spread, full quoted yield credited every business day
  success bar        >=90% of years positive AND >=75% of quarters positive AND Sharpe > 0.8 AND CAGR above cash

  The universe is screened on EXISTENCE ONLY (does the source resolve the symbol and does it have history over the window).  No sleeve, weight or rule below was chosen by looking at a result.

==============================================================================
DATA INVENTORY -- what resolved, what did not
==============================================================================
  Master calendar = SPY sessions >= 2005-09-30 : 5292 days, 2005-09-30 .. 2026-10-14  (21.04 years)

  symbol  rows   first       last        no-PRINT on book cal  source symbol
  ------  -----  ----------  ----------  --------------------  -------------
  SPY     8485   1993-01-29  2026-10-14  0.0%                  symbol
  QQQ     6943   1999-03-10  2026-10-14  0.0%                  NASDAQ:QQQ
  IWM     6635   2000-05-26  2026-10-14  0.0%                  AMEX:IWM
  MDY     7908   1995-05-12  2026-10-14  0.0%                  AMEX:MDY
  DIA     7229   1998-01-20  2026-10-14  0.0%                  AMEX:DIA
  TLT     6094   2002-07-26  2026-10-14  0.0%                  NASDAQ:TLT
  TLH     4971   2007-01-11  2026-10-14  0.0%                  AMEX:TLH
  EDV     4717   2007-12-13  2026-10-14  0.4%                  AMEX:EDV
  IEF     6094   2002-07-26  2026-10-14  0.0%                  NASDAQ:IEF
  SHY     6094   2002-07-26  2026-10-14  0.0%                  NASDAQ:SHY
  TIP     5750   2003-12-05  2026-10-14  0.0%                  AMEX:TIP
  LQD     6094   2002-07-26  2026-10-14  0.0%                  AMEX:LQD
  HYG     4910   2007-04-11  2026-10-14  0.0%                  AMEX:HYG
  EMB     4733   2007-12-19  2026-10-14  0.0%                  NASDAQ:EMB
  GLD     5510   2004-11-18  2026-10-14  0.0%                  AMEX:GLD
  SLV     5148   2006-04-28  2026-10-14  0.0%                  AMEX:SLV
  GDX     5132   2006-05-22  2026-10-14  0.0%                  AMEX:GDX
  DBC     5206   2006-02-03  2026-10-14  0.0%                  AMEX:DBC
  VNQ     5546   2004-09-29  2026-10-14  0.0%                  AMEX:VNQ
  EEM     5915   2003-04-11  2026-10-14  0.0%                  AMEX:EEM
  EFA     6326   2001-08-17  2026-10-14  0.0%                  AMEX:EFA
  EWJ     7694   1996-03-18  2026-10-14  0.0%                  AMEX:EWJ
  FXI     5539   2004-10-08  2026-10-14  0.0%                  AMEX:FXI
  ILF     6243   2001-10-26  2026-10-14  0.0%                  AMEX:ILF
  EWZ     6569   2000-07-14  2026-10-14  0.0%                  AMEX:EWZ
  UUP     4944   2007-02-20  2026-10-14  0.0%                  AMEX:UUP
  XLE     6995   1998-12-22  2026-10-14  0.0%                  AMEX:XLE
  XLU     6995   1998-12-22  2026-10-14  0.0%                  AMEX:XLU
  XLK     6995   1998-12-22  2026-10-14  0.0%                  AMEX:XLK
  XLP     6995   1998-12-22  2026-10-14  0.0%                  AMEX:XLP
  XLV     6995   1998-12-22  2026-10-14  0.0%                  AMEX:XLV
  BIL     4876   2007-05-30  2026-10-14  0.0%                  AMEX:BIL
  VIX     9283   1990-01-03  2026-10-14  0.0%                  TVC:VIX
  US03M   18197  1954-01-04  2026-10-14  14.0%                 TVC:US03M
  US02Y   7342   1994-08-22  2026-10-14  16.5%                 TVC:US02Y
  US10Y   7662   1992-07-08  2026-10-14  16.1%                 TVC:US10Y
  US30Y   7439   1993-06-16  2026-10-14  16.6%                 TVC:US30Y
  DXY     8000   1995-03-21  2026-10-14  19.7%                 TVC:DXY

  SYMBOLS THAT FAILED TO RESOLVE (recorded, never substituted):
    AMEX:SHY    -> error: invalid symbol            => resolved instead as NASDAQ:SHY   (same fund, different exchange code)
    AMEX:TLT    -> error: invalid symbol            => resolved instead as NASDAQ:TLT
    AMEX:EMB    -> error: invalid symbol            => resolved instead as NASDAQ:EMB
    AMEX:TLH    -> resolved.  AMEX:SHY/EMB/TLT were retried on NASDAQ and succeeded; the prices are the same fund, but the exchange code differs, so the provenance records which one was actually used.

  Cross-check against the sibling studies' independent pulls on the same date -- run separately by verify_sources.py.

==============================================================================
CASH PROXY -- a yield index, handled explicitly
==============================================================================
  source: TVC:US03M, the 3-month US Treasury bill YIELD in percent per annum
  accrual: r_j = (yield at the close of the PREVIOUS book date / 100) / 252
  n_days               5291
  printed              4550
  carried_forward      741
  carried_pct          14.00%
  longest_gap_days     2
  no_rate_days         1
  rate_min             -0.0406% p.a.
  rate_max             5.5150% p.a.
  rate_mean            1.7634% p.a.
  negative_rate_days   11
  zero_return_days     9

  cash CAGR over the window (upper bound): 1.7750%/yr
  days on which the CASH itself was negative: 11 of 5291 (0.21%)
  BIL price-only cross-check: -0.0045%/yr over 2007-05-30..2026-10-14 -- shown to demonstrate that a T-bill ETF's PRICE is not its return (the yield is distributed away), so BIL cannot be used as the cash series.

  book calendar: 5292 sessions, 2005-09-30 .. 2026-10-14 (21.04 years)
  cash diagnostics on this window:
    n_days               5291
    carried_forward      741
    carried_pct          14.00%
    longest_gap_days     2
    rate_min             -0.0406%
    rate_max             5.5150%
    negative_rate_days   11

==============================================================================
SLEEVE METRICS -- dividend-adjusted and price-only, at 5 bps round-trip
==============================================================================

  --- DIVIDEND-ADJUSTED [ESTIMATED] ---
                CAGR    maxDD    Sharpe  annvol  pos yrs  pos Y    pos Q    pos M    worst yr      worst mo  worst 12m  worst 36m
  ------------  ------  -------  ------  ------  -------  -------  -------  -------  ------------  --------  ---------  ---------
  T             4.39%   -7.31%   0.65    4.0%    18/20    90.00%   72.62%   67.86%   -1.59% 2022   -2.73%    -2.58%     2.31%
  C             1.12%   -22.32%  -0.09   5.7%    13/20    65.00%   76.19%   63.10%   -15.98% 2008  -7.22%    -16.09%    -10.52%
  C_hyg         4.34%   -35.88%  0.29    10.4%   16/20    80.00%   72.62%   68.65%   -18.91% 2008  -11.74%   -29.50%    -22.76%
  V             10.01%  -99.83%  0.74    178.6%  15/20    75.00%   83.33%   90.08%   -99.43% 2008  -93.57%   -99.67%    -99.29%
  H_a           3.83%   -13.58%  0.38    5.7%    17/20    85.00%   67.86%   69.84%   -5.82% 2013   -5.17%    -6.60%     -3.01%
  H_b           -1.30%  -34.16%  -0.76   3.9%    7/20     35.00%   30.95%   28.17%   -4.94% 2013   -1.67%    -5.56%     -14.49%
  H             1.29%   -14.08%  -0.12   3.5%    13/20    65.00%   51.19%   49.60%   -5.36% 2013   -2.99%    -5.71%     -8.62%
  X             11.01%  -29.97%  0.55    19.0%   15/20    75.00%   72.62%   59.52%   -13.75% 2022  -14.69%   -24.03%    -4.75%
  B             11.08%  -55.35%  0.55    19.1%   17/20    85.00%   73.81%   65.48%   -37.15% 2008  -16.38%   -43.75%    -39.15%
  CASH          1.77%   -0.00%   n/a     0.1%    20/20    100.00%  100.00%  100.00%  0.03% 2014    0.00%     0.02%      0.12%
  CASHx(lam=0)  1.77%   -0.00%   n/a     0.1%    20/20    100.00%  100.00%  100.00%  0.03% 2014    0.00%     0.02%      0.12%

  --- PRICE-ONLY (as measured) ---
                CAGR    maxDD    Sharpe  annvol  pos yrs  pos Y    pos Q    pos M    worst yr      worst mo  worst 12m  worst 36m
  ------------  ------  -------  ------  ------  -------  -------  -------  -------  ------------  --------  ---------  ---------
  T             2.88%   -7.44%   0.29    4.0%    17/20    85.00%   67.86%   64.29%   -1.90% 2022   -2.92%    -3.64%     -0.55%
  C             -0.08%  -32.73%  -0.30   5.7%    13/20    65.00%   64.29%   59.52%   -16.71% 2008  -7.14%    -16.71%    -11.59%
  C_hyg         -0.72%  -38.86%  -0.19   10.4%   11/20    55.00%   59.52%   57.14%   -22.99% 2008  -12.20%   -32.72%    -26.29%
  V             10.01%  -99.83%  0.74    178.6%  15/20    75.00%   83.33%   90.08%   -99.43% 2008  -93.57%   -99.67%    -99.29%
  H_a           3.83%   -13.58%  0.38    5.7%    17/20    85.00%   67.86%   69.84%   -5.82% 2013   -5.17%    -6.60%     -3.01%
  H_b           -1.30%  -34.16%  -0.76   3.9%    7/20     35.00%   30.95%   28.17%   -4.94% 2013   -1.67%    -5.56%     -14.49%
  H             1.29%   -14.08%  -0.12   3.5%    13/20    65.00%   51.19%   49.60%   -5.36% 2013   -2.99%    -5.71%     -8.62%
  X             8.80%   -30.70%  0.45    19.0%   15/20    75.00%   65.48%   57.54%   -15.50% 2022  -14.93%   -25.59%    -9.93%
  B             9.10%   -56.47%  0.46    19.1%   15/20    75.00%   72.62%   64.68%   -38.28% 2008  -16.52%   -44.75%    -42.35%
  CASH          1.77%   -0.00%   n/a     0.1%    20/20    100.00%  100.00%  100.00%  0.03% 2014    0.00%     0.02%      0.12%
  CASHx(lam=0)  1.77%   -0.00%   n/a     0.1%    20/20    100.00%  100.00%  100.00%  0.03% 2014    0.00%     0.02%      0.12%

==============================================================================
COST AND DIVIDEND GRID -- CAGR% / Sharpe(excess) per sleeve
==============================================================================
  sleeve  price 0bps      price 5bps      price 20bps     div 0bps        div 5bps        div 20bps
  ------  --------------  --------------  --------------  --------------  --------------  --------------
  T       2.99% / 0.31    2.88% / 0.29    2.56% / 0.21    4.50% / 0.67    4.39% / 0.65    4.06% / 0.57
  C       -0.06% / -0.29  -0.08% / -0.30  -0.15% / -0.31  1.14% / -0.08   1.12% / -0.09   1.05% / -0.10
  C_hyg   -0.71% / -0.19  -0.72% / -0.19  -0.72% / -0.19  4.35% / 0.29    4.34% / 0.29    4.34% / 0.29
  V       10.67% / 0.74   10.01% / 0.74   8.05% / 0.73    10.67% / 0.74   10.01% / 0.74   8.05% / 0.73
  H_a     4.12% / 0.43    3.83% / 0.38    2.94% / 0.23    4.12% / 0.43    3.83% / 0.38    2.94% / 0.23
  H_b     -1.30% / -0.76  -1.30% / -0.76  -1.31% / -0.77  -1.30% / -0.76  -1.30% / -0.76  -1.31% / -0.77
  H       1.44% / -0.08   1.29% / -0.12   0.85% / -0.24   1.44% / -0.08   1.29% / -0.12   0.85% / -0.24
  X       9.01% / 0.46    8.80% / 0.45    8.15% / 0.42    11.23% / 0.56   11.01% / 0.55   10.36% / 0.52
  B       9.11% / 0.46    9.10% / 0.46    9.10% / 0.46    11.08% / 0.55   11.08% / 0.55   11.08% / 0.55
  CASH    1.77% / n/a     1.77% / n/a     1.77% / n/a     1.77% / n/a     1.77% / n/a     1.77% / n/a

  cost drag (CAGR lost from 0 -> 20 bps round trip, dividend-adjusted):
  sleeve  CAGR 0bps  CAGR 5bps  CAGR 20bps  drag@5    drag@20
  ------  ---------  ---------  ----------  --------  --------
  T       4.50%      4.39%      4.06%       0.110 pp  0.439 pp
  C       1.14%      1.12%      1.05%       0.023 pp  0.091 pp
  C_hyg   4.35%      4.34%      4.34%       0.002 pp  0.010 pp
  V       10.67%     10.01%     8.05%       0.661 pp  2.622 pp
  H_a     4.12%      3.83%      2.94%       0.298 pp  1.186 pp
  H_b     -1.30%     -1.30%     -1.31%      0.002 pp  0.010 pp
  H       1.44%      1.29%      0.85%       0.146 pp  0.584 pp
  X       11.23%     11.01%     10.36%      0.219 pp  0.875 pp
  B       11.08%     11.08%     11.08%      0.001 pp  0.005 pp

==============================================================================
THE BOOKS -- fixed pre-registered sleeve weights
==============================================================================
  BOOK      : C 0.15 + CASH 0.10 + H 0.10 + T 0.40 + V 0.10 + X 0.15
  BOOK-NOV  : C 0.17 + CASH 0.10 + H 0.11 + T 0.45 + X 0.17
  BOOK-VT   : the same BOOK weights passed through ONE uniform, declared normalisation -- every sleeve scaled by
              k = min(1, 4% / its own annualised vol), released weight to CASH.  Not searched, not sleeve-specific.

==============================================================================
BOOK METRICS -- every cost level, both dividend treatments
==============================================================================
                          CAGR    maxDD    Sharpe  annvol  pos yrs  pos Y    pos Q    pos M    worst yr      worst mo  worst 12m  worst 36m
  ----------------------  ------  -------  ------  ------  -------  -------  -------  -------  ------------  --------  ---------  ---------
  BOOK div 0bps           8.85%   -28.53%  0.59    12.7%   17/20    85.00%   83.33%   79.37%   -19.55% 2008  -11.25%   -24.85%    -5.04%
  BOOK div 5bps           8.68%   -28.59%  0.58    12.7%   17/20    85.00%   83.33%   79.37%   -19.69% 2008  -11.25%   -24.97%    -5.50%
  BOOK div 20bps          8.16%   -28.77%  0.54    12.7%   17/20    85.00%   83.33%   79.37%   -20.10% 2008  -11.26%   -25.32%    -6.86%
  BOOK price 0bps         7.70%   -28.84%  0.51    12.7%   17/20    85.00%   82.14%   78.97%   -20.26% 2008  -11.33%   -25.47%    -7.98%
  BOOK price 5bps         7.53%   -28.90%  0.50    12.7%   17/20    85.00%   80.95%   78.97%   -20.39% 2008  -11.33%   -25.58%    -8.42%
  BOOK price 20bps        7.02%   -29.08%  0.46    12.7%   17/20    85.00%   79.76%   78.97%   -20.80% 2008  -11.34%   -25.93%    -9.74%
  BOOK-NOV div 0bps       4.63%   -8.03%   0.58    5.0%    15/20    75.00%   77.38%   66.27%   -1.79% 2015   -3.27%    -5.91%     4.09%
  BOOK-NOV div 5bps       4.52%   -8.08%   0.56    5.0%    15/20    75.00%   76.19%   66.27%   -1.90% 2015   -3.28%    -6.00%     3.72%
  BOOK-NOV div 20bps      4.19%   -8.22%   0.50    5.0%    15/20    75.00%   76.19%   65.87%   -2.25% 2015   -3.29%    -6.26%     2.60%
  BOOK-NOV price 0bps     3.38%   -8.60%   0.34    5.0%    15/20    75.00%   72.62%   61.11%   -2.84% 2015   -3.34%    -6.81%     0.20%
  BOOK-NOV price 5bps     3.27%   -8.65%   0.32    5.0%    15/20    75.00%   71.43%   60.32%   -2.95% 2015   -3.34%    -6.90%     -0.16%
  BOOK-NOV price 20bps    2.95%   -8.80%   0.26    5.0%    15/20    75.00%   70.24%   59.92%   -3.29% 2015   -3.36%    -7.16%     -1.23%
  BOOK-VT div 0bps        2.74%   -3.46%   0.54    1.8%    19/20    95.00%   78.57%   71.83%   -0.23% 2015   -0.95%    -1.20%     2.12%
  BOOK-VT div 5bps        2.68%   -3.47%   0.51    1.8%    19/20    95.00%   78.57%   71.43%   -0.29% 2015   -0.95%    -1.25%     1.90%
  BOOK-VT div 20bps       2.50%   -3.49%   0.41    1.8%    19/20    95.00%   78.57%   70.24%   -0.49% 2015   -0.96%    -1.39%     1.21%
  BOOK-VT price 0bps      2.06%   -3.52%   0.16    1.8%    17/20    85.00%   76.19%   67.86%   -0.78% 2015   -1.06%    -1.68%     -0.09%
  BOOK-VT price 5bps      1.99%   -3.53%   0.13    1.8%    17/20    85.00%   76.19%   67.46%   -0.84% 2015   -1.06%    -1.73%     -0.31%
  BOOK-VT price 20bps     1.81%   -3.55%   0.03    1.8%    17/20    85.00%   75.00%   65.48%   -1.03% 2015   -1.07%    -1.88%     -0.98%
  B (SPY buy&hold) div    11.08%  -55.35%  0.55    19.1%   17/20    85.00%   73.81%   65.48%   -37.15% 2008  -16.38%   -43.75%    -39.15%
  B (SPY buy&hold) price  9.10%   -56.47%  0.46    19.1%   15/20    75.00%   72.62%   64.68%   -38.28% 2008  -16.52%   -44.75%    -42.35%
  CASH                    1.77%   -0.00%   n/a     0.1%    20/20    100.00%  100.00%  100.00%  0.03% 2014    0.00%     0.02%      0.12%

  BOOK-VT resolved weights at 5 bps (dividend-adjusted): C=0.1053  CASH=0.3655  H=0.1000  T=0.3954  V=0.0022  X=0.0315
  sleeve vol-scaling k = min(1, 4%/vol):
    T    vol  4.05%  k=0.9886
    X    vol 19.04%  k=0.2101
    C    vol  5.70%  k=0.7021
    V    vol 178.58%  k=0.0224
    H    vol  3.49%  k=1.0000

==============================================================================
POSITIVITY BY HORIZON -- fraction of complete periods with a POSITIVE compounded return
==============================================================================
  series                D                   W                   2W                M                  Q                H                Y
  --------------------  ------------------  ------------------  ----------------  -----------------  ---------------  ---------------  ---------------
  BOOK div 0bps         59.32% (3139/5292)  65.72% (721/1097)   72.50% (398/549)  79.37% (200/252)   83.33% (70/84)   80.49% (33/41)   85.00% (17/20)
  BOOK div 5bps         59.24% (3135/5292)  65.54% (719/1097)   72.31% (397/549)  79.37% (200/252)   83.33% (70/84)   80.49% (33/41)   85.00% (17/20)
  BOOK div 20bps        59.13% (3129/5292)  65.18% (715/1097)   71.40% (392/549)  79.37% (200/252)   83.33% (70/84)   80.49% (33/41)   85.00% (17/20)
  BOOK price 0bps       58.75% (3109/5292)  65.00% (713/1097)   70.31% (386/549)  78.97% (199/252)   82.14% (69/84)   80.49% (33/41)   85.00% (17/20)
  BOOK price 5bps       58.73% (3108/5292)  65.00% (713/1097)   70.13% (385/549)  78.97% (199/252)   80.95% (68/84)   80.49% (33/41)   85.00% (17/20)
  BOOK price 20bps      58.60% (3101/5292)  64.72% (710/1097)   68.85% (378/549)  78.97% (199/252)   79.76% (67/84)   78.05% (32/41)   85.00% (17/20)
  BOOK-NOV div 0bps     55.59% (2942/5292)  57.25% (628/1097)   59.20% (325/549)  66.27% (167/252)   77.38% (65/84)   82.93% (34/41)   75.00% (15/20)
  BOOK-NOV div 5bps     55.50% (2937/5292)  57.06% (626/1097)   58.83% (323/549)  66.27% (167/252)   76.19% (64/84)   80.49% (33/41)   75.00% (15/20)
  BOOK-NOV div 20bps    55.33% (2928/5292)  56.70% (622/1097)   58.29% (320/549)  65.87% (166/252)   76.19% (64/84)   80.49% (33/41)   75.00% (15/20)
  BOOK-NOV price 0bps   54.74% (2897/5292)  55.70% (611/1097)   56.83% (312/549)  61.11% (154/252)   72.62% (61/84)   75.61% (31/41)   75.00% (15/20)
  BOOK-NOV price 5bps   54.65% (2892/5292)  55.15% (605/1097)   56.47% (310/549)  60.32% (152/252)   71.43% (60/84)   75.61% (31/41)   75.00% (15/20)
  BOOK-NOV price 20bps  54.48% (2883/5292)  54.97% (603/1097)   55.92% (307/549)  59.92% (151/252)   70.24% (59/84)   68.29% (28/41)   75.00% (15/20)
  BOOK-VT div 0bps      57.16% (3025/5292)  63.26% (694/1097)   65.94% (362/549)  71.83% (181/252)   78.57% (66/84)   90.24% (37/41)   95.00% (19/20)
  BOOK-VT div 5bps      56.97% (3015/5292)  62.53% (686/1097)   65.94% (362/549)  71.43% (180/252)   78.57% (66/84)   90.24% (37/41)   95.00% (19/20)
  BOOK-VT div 20bps     56.63% (2997/5292)  61.71% (677/1097)   65.03% (357/549)  70.24% (177/252)   78.57% (66/84)   82.93% (34/41)   95.00% (19/20)
  BOOK-VT price 0bps    55.71% (2948/5292)  59.34% (651/1097)   63.39% (348/549)  67.86% (171/252)   76.19% (64/84)   73.17% (30/41)   85.00% (17/20)
  BOOK-VT price 5bps    55.57% (2941/5292)  59.07% (648/1097)   62.84% (345/549)  67.46% (170/252)   76.19% (64/84)   73.17% (30/41)   85.00% (17/20)
  BOOK-VT price 20bps   55.20% (2921/5292)  58.34% (640/1097)   61.75% (339/549)  65.48% (165/252)   75.00% (63/84)   73.17% (30/41)   85.00% (17/20)
  T div 5bps            56.37% (2983/5292)  59.25% (650/1097)   62.84% (345/549)  67.86% (171/252)   72.62% (61/84)   87.80% (36/41)   90.00% (18/20)
  B SPY div 5bps        55.03% (2912/5292)  57.25% (628/1097)   63.02% (346/549)  65.48% (165/252)   73.81% (62/84)   78.05% (32/41)   85.00% (17/20)
  CASH                  99.60% (5271/5292)  99.82% (1095/1097)  99.82% (548/549)  100.00% (252/252)  100.00% (84/84)  100.00% (41/41)  100.00% (20/20)

  A flat period counts as NOT positive (strict reading).  The loose reading (a loss is the only failure) is in the CSVs.

==============================================================================
LAMBDA FRONTIER -- scaling exposure against cash
==============================================================================
  r = lam * book + (1 - lam) * cash.  lam is the fraction of capital at risk.
  book            largest lam with 100% positive YEARS (CAGR there)  100% positive QUARTERS (CAGR)  100% positive MONTHS (CAGR)  lam resolution
  --------------  -------------------------------------------------  -----------------------------  ---------------------------  --------------
  BOOK div        0.063 (2.25%)                                      0.003 (1.80%)                  0.001 (1.78%)                0.0010
  BOOK price      0.060 (2.16%)                                      0.002 (1.79%)                  0.000 (1.77%)                0.0010
  BOOK-NOV div    0.025 (1.85%)                                      0.003 (1.78%)                  0.000 (1.77%)                0.0010
  BOOK-NOV price  0.016 (1.80%)                                      0.002 (1.78%)                  0.000 (1.77%)                0.0010
  BOOK-VT div     0.144 (1.91%)                                      0.012 (1.79%)                  0.002 (1.78%)                0.0010
  BOOK-VT price   0.054 (1.79%)                                      0.009 (1.78%)                  0.001 (1.78%)                0.0010

  frontier in detail (lam, CAGR, posY, posQ, posM):
    lam    CAGR   Sharpe  posY     Y pos  posQ     posM     maxDD
    -----  -----  ------  -------  -----  -------  -------  -------
    0.000  1.77%  14.30   100.00%  20/20  100.00%  100.00%  -0.00%
    0.001  1.78%  14.29   100.00%  20/20  100.00%  100.00%  -0.01%
    0.002  1.79%  14.14   100.00%  20/20  100.00%  99.21%   -0.03%
    0.005  1.81%  13.01   100.00%  20/20  98.81%   97.22%   -0.10%
    0.010  1.85%  10.41   100.00%  20/20  96.43%   95.24%   -0.22%
    0.020  1.92%  6.78    100.00%  20/20  96.43%   93.25%   -0.46%
    0.050  2.15%  3.30    100.00%  20/20  90.48%   89.29%   -1.18%
    0.100  2.52%  1.96    95.00%   19/20  89.29%   87.30%   -2.63%
    0.200  3.25%  1.28    90.00%   18/20  89.29%   84.92%   -5.81%
    0.350  4.33%  0.98    90.00%   18/20  86.90%   83.33%   -10.45%
    0.500  5.38%  0.86    90.00%   18/20  86.90%   82.14%   -14.91%
    0.750  7.07%  0.77    85.00%   17/20  83.33%   80.95%   -21.98%
    1.000  8.68%  0.72    85.00%   17/20  83.33%   79.37%   -28.59%

==============================================================================
REGIME GRID -- trend state x realised-vol tercile, on the MONTHLY book return
==============================================================================
  trend state  : SPY close > SPY SMA(200), read at the PREVIOUS month-end
  vol terciles : trailing 20-day realised SPY vol read at the PREVIOUS month-end

  BOOK -- tercile breakpoints (annualised vol): 0.6591 / 1.0155
    trend  vol   months  mean monthly  frac positive
    -----  ----  ------  ------------  -------------
    UP     LOW   79      0.77%         79.75%
    UP     MID   78      0.86%         83.33%
    UP     HIGH  32      1.42%         84.38%
    DOWN   LOW   0       n/a           n/a
    DOWN   MID   5       0.28%         80.00%
    DOWN   HIGH  48      -0.01%        68.75%
    NEGATIVE CELLS: 1 of 6

  BOOK-NOV -- tercile breakpoints (annualised vol): 0.6591 / 1.0155
    trend  vol   months  mean monthly  frac positive
    -----  ----  ------  ------------  -------------
    UP     LOW   79      0.29%         67.09%
    UP     MID   78      0.41%         65.38%
    UP     HIGH  32      0.83%         71.88%
    DOWN   LOW   0       n/a           n/a
    DOWN   MID   5       0.81%         80.00%
    DOWN   HIGH  48      0.12%         58.33%
    NEGATIVE CELLS: 0 of 6

  BOOK-VT -- tercile breakpoints (annualised vol): 0.6591 / 1.0155
    trend  vol   months  mean monthly  frac positive
    -----  ----  ------  ------------  -------------
    UP     LOW   79      0.22%         74.68%
    UP     MID   78      0.22%         66.67%
    UP     HIGH  32      0.38%         81.25%
    DOWN   LOW   0       n/a           n/a
    DOWN   MID   5       0.21%         80.00%
    DOWN   HIGH  48      0.10%         64.58%
    NEGATIVE CELLS: 0 of 6

  BOOK: 1/6 negative
  BOOK-NOV: 0/6 negative
  BOOK-VT: 0/6 negative

==============================================================================
CORRELATION MATRIX OF YEARLY RETURNS -- the key output
==============================================================================

  years used: 2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025
            T      C      V      H_a    H_b    H      X      B      BOOK   BOOK-NOV  BOOK-VT  CASH
  --------  -----  -----  -----  -----  -----  -----  -----  -----  -----  --------  -------  ----
  T         1.00   0.38   0.43   0.38   -0.27  0.17   0.72   0.47   0.68   0.87      0.87     0.40
  C         0.38   1.00   0.37   0.05   -0.42  -0.16  0.33   0.66   0.63   0.55      0.54     0.34
  V         0.43   0.37   1.00   0.24   -0.67  -0.14  0.39   0.60   0.86   0.44      0.36     0.10
  H_a       0.38   0.05   0.24   1.00   0.24   0.88   0.53   -0.15  0.36   0.54      0.59     0.53
  H_b       -0.27  -0.42  -0.67  0.24   1.00   0.67   -0.23  -0.72  -0.67  -0.24     0.01     0.47
  H         0.17   -0.16  -0.14  0.88   0.67   1.00   0.30   -0.46  -0.05  0.30      0.46     0.63
  X         0.72   0.33   0.39   0.53   -0.23  0.30   1.00   0.39   0.68   0.93      0.66     0.18
  B         0.47   0.66   0.60   -0.15  -0.72  -0.46  0.39   1.00   0.74   0.50      0.38     0.06
  BOOK      0.68   0.63   0.86   0.36   -0.67  -0.05  0.68   0.74   1.00   0.77      0.64     0.22
  BOOK-NOV  0.87   0.55   0.44   0.54   -0.24  0.30   0.93   0.50   0.77   1.00      0.87     0.40
  BOOK-VT   0.87   0.54   0.36   0.59   0.01   0.46   0.66   0.38   0.64   0.87      1.00     0.76
  CASH      0.40   0.34   0.10   0.53   0.47   0.63   0.18   0.06   0.22   0.40      0.76     1.00

  symmetry + unit-diagonal check: PASS (symmetric, diagonal exactly 1.0)

  pairwise correlations with the BOOK, lowest first (the whole point of the exercise):
    H_b       -0.671
    H         -0.048
    CASH      0.225
    H_a       0.357
    C         0.629
    BOOK-VT   0.641
    T         0.681
    X         0.684
    B         0.735
    BOOK-NOV  0.770
    V         0.861

  HOW MANY INDEPENDENT BETS IS THE BOOK ACTUALLY?
  for n sleeves with mean pairwise yearly correlation rho_bar, the effective count is n / (1 + (n-1) * rho_bar)
    the 5 sleeves of BOOK        n=5  mean rho=+0.278  independent bets ~ 2.37
    T and X                      n=2  mean rho=+0.722  independent bets ~ 1.16
    the 5 sleeves plus SPY buy&hold n=6  mean rho=+0.295  independent bets ~ 2.42
    (the predecessor's SPY/QQQ/IWM measurement was 0.875 yearly -> 1.12 bets; a 14-name equity basket gave 2.53)

==============================================================================
DECLARED SENSITIVITIES -- not used anywhere in the books
==============================================================================
  variant   mode   CAGR    maxDD    Sharpe  annvol  pos yrs  pos Y   pos Q   pos M   worst yr      worst mo  worst 12m  worst 36m
  --------  -----  ------  -------  ------  ------  -------  ------  ------  ------  ------------  --------  ---------  ---------
  X         div    11.01%  -29.97%  0.55    19.0%   15/20    75.00%  72.62%  59.52%  -13.75% 2022  -14.69%   -24.03%    -4.75%
  X         price  8.80%   -30.70%  0.45    19.0%   15/20    75.00%  65.48%  57.54%  -15.50% 2022  -14.93%   -25.59%    -9.93%
  X8        div    10.75%  -27.78%  0.61    16.0%   16/20    80.00%  72.62%  61.11%  -10.94% 2022  -9.57%    -24.80%    4.20%
  X8        price  8.57%   -28.70%  0.48    16.0%   15/20    75.00%  71.43%  59.52%  -12.66% 2022  -9.75%    -26.40%    -1.61%
  V_s0      div    -2.54%  -99.89%  0.73    196.9%  15/20    75.00%  82.14%  89.29%  -99.52% 2008  -93.88%   -99.74%    -99.53%
  V_s3      div    15.50%  -99.79%  0.73    163.9%  16/20    80.00%  85.71%  92.06%  -99.42% 2008  -93.64%   -99.65%    -99.18%
  V (base)  div    10.01%  -99.83%  0.74    178.6%  15/20    75.00%  83.33%  90.08%  -99.43% 2008  -93.57%   -99.67%    -99.29%
  C_hyg     div    4.34%   -35.88%  0.29    10.4%   16/20    80.00%  72.62%  68.65%  -18.91% 2008  -11.74%   -29.50%    -22.76%
  C (pair)  div    1.12%   -22.32%  -0.09   5.7%    13/20    65.00%  76.19%  63.10%  -15.98% 2008  -7.22%    -16.09%    -10.52%

  V sleeve internals:
    rolls                          252.0000
    mean_credit_pct_of_width       0.0827
    min_credit_pct_of_width        0.0533
    max_credit_pct_of_width        0.1585
    skew_short_volpts              1.5000
  H_b sleeve internals [MODELED]:
    rolls                          253.0000
    premium_spent_total            0.9237
    premium_spent_per_yr           0.0439
    payoffs_total                  0.3733
    ending_value                   0.7601
  H_a sleeve internals:
    months_long                    109 of 253 months long
  T sleeve internals:
    mean instruments live per rebalance: 18.90
  X sleeve last month's picks: XLK,QQQ,EEM,SPY,EWJ

==============================================================================
REDUCED LONG-WINDOW BOOK -- covering the 2000-2002 dot-com bear
==============================================================================
  window: 1998-12-22 .. 2026-10-14 (27.81 years)
  EXISTENCE screen -- instruments with a print on 1998-12-22 : 9
    SPY,MDY,DIA,EWJ,XLE,XLU,XLK,XLP,XLV
  instruments NOT present at that date (so absent from this book until they list): QQQ,IWM,TLT,TLH,EDV,IEF,SHY,TIP,LQD,HYG,EMB,GLD,SLV,GDX,DBC,VNQ,EEM,EFA,FXI,ILF,EWZ,UUP
  CARRY weight is set to 0.00 in this book because neither HYG nor IEF lists before 2002/2007; that capital earns cash instead.
  BOND10M [MODELED] supplies the duration leg: r = -7.5 * dy10 + y10/252

                          CAGR    maxDD    Sharpe  annvol  pos yrs  pos Y   pos Q   pos M   worst yr      worst mo  worst 12m  worst 36m
  ----------------------  ------  -------  ------  ------  -------  ------  ------  ------  ------------  --------  ---------  ---------
  REDUCED div 0bps        10.52%  -31.31%  0.65    13.6%   22/27    81.48%  82.88%  79.28%  -22.10% 2008  -12.63%   -25.57%    -7.92%
  REDUCED div 5bps        10.37%  -31.43%  0.64    13.6%   22/27    81.48%  82.88%  79.28%  -22.22% 2008  -12.64%   -25.67%    -8.32%
  REDUCED div 20bps       9.92%   -31.79%  0.61    13.6%   22/27    81.48%  82.88%  78.68%  -22.59% 2008  -12.65%   -25.96%    -9.54%
  REDUCED price 0bps      9.56%   -31.69%  0.59    13.6%   22/27    81.48%  82.88%  78.68%  -22.49% 2008  -12.73%   -25.88%    -9.78%
  REDUCED price 5bps      9.42%   -31.82%  0.58    13.6%   22/27    81.48%  82.88%  78.68%  -22.61% 2008  -12.73%   -25.97%    -10.18%
  REDUCED price 20bps     8.97%   -32.18%  0.55    13.6%   22/27    81.48%  82.88%  78.08%  -22.98% 2008  -12.75%   -26.27%    -11.38%
  B (SPY buy&hold) div    8.82%   -55.35%  0.43    19.2%   21/27    77.78%  70.27%  61.86%  -37.15% 2008  -16.38%   -43.75%    -40.54%
  B (SPY buy&hold) price  6.89%   -56.47%  0.34    19.2%   19/27    70.37%  69.37%  61.26%  -38.28% 2008  -16.52%   -44.75%    -43.65%

==============================================================================
REDUCED LONG-WINDOW BOOK -- year by year (dividend-adjusted, 5 bps)
==============================================================================
  year  REDUCED BOOK  T       X        V        H_a     H_b     H       BOND10M  B        CASH
  ----  ------------  ------  -------  -------  ------  ------  ------  -------  -------  -----
  1999  24.63%        23.63%  16.25%   204.52%  4.75%   -0.32%  2.19%   -7.28%   21.27%   4.75%
  2000  14.01%        -3.88%  13.68%   136.32%  5.99%   3.69%   4.86%   16.37%   -9.06%   5.99%
  2001  -2.77%        -4.11%  -9.81%   -40.95%  3.40%   3.80%   3.62%   5.10%    -11.31%  3.40%
  2002  -9.83%        -3.52%  -16.49%  -77.81%  1.62%   1.43%   1.56%   14.86%   -21.40%  1.62%
  2003  27.17%        23.97%  32.75%   191.42%  1.01%   -3.93%  -1.49%  0.12%    28.41%   1.01%
  2004  16.52%        9.34%   15.27%   137.33%  1.38%   -3.55%  -1.11%  4.08%    10.59%   1.38%
  2005  13.91%        4.58%   15.76%   113.91%  8.74%   -1.69%  3.43%   3.41%    4.88%    3.19%
  2006  14.72%        12.27%  13.37%   84.08%   1.00%   0.15%   0.85%   2.25%    15.80%   4.82%
  2007  19.29%        10.72%  11.25%   141.57%  24.63%  0.14%   11.98%  8.34%    5.11%    4.42%
  2008  -22.22%       -6.93%  -30.52%  -99.43%  3.84%   9.14%   6.57%   21.06%   -37.15%  1.38%
  2009  11.09%        16.07%  18.98%   -1.51%   0.18%   -3.33%  -1.57%  -9.81%   25.73%   0.15%
  2010  8.12%         4.14%   10.89%   28.50%   -1.18%  -2.55%  -1.82%  6.27%    14.89%   0.14%
  2011  16.28%        3.45%   4.42%    182.77%  5.69%   -3.07%  1.26%   14.38%   1.61%    0.05%
  2012  13.07%        6.86%   7.53%    120.56%  1.62%   -4.85%  -1.66%  2.91%    15.52%   0.09%
  2013  22.08%        25.86%  26.87%   132.61%  -5.82%  -4.94%  -5.36%  -6.88%   32.04%   0.06%
  2014  16.31%        11.10%  11.84%   118.27%  2.39%   -4.74%  -1.23%  8.80%    13.31%   0.03%
  2015  4.57%         -2.15%  -0.98%   53.97%   2.53%   -1.61%  0.50%   1.16%    0.99%    0.05%
  2016  15.13%        7.74%   12.43%   139.06%  5.76%   -4.12%  0.72%   0.33%    11.63%   0.32%
  2017  17.37%        16.83%  19.37%   96.20%   -0.69%  -3.98%  -2.34%  2.56%    21.54%   0.95%
  2018  -12.75%       -2.80%  -5.86%   -97.02%  0.98%   4.01%   2.54%   0.76%    -4.65%   1.98%
  2019  17.45%        11.50%  26.04%   89.15%   6.25%   -4.29%  0.85%   8.06%    31.12%   2.12%
  2020  8.73%         7.83%   23.83%   -27.54%  3.59%   -0.33%  1.77%   8.59%    18.28%   0.36%
  2021  21.15%        18.08%  21.92%   165.54%  1.38%   -4.83%  -1.77%  -3.12%   29.34%   0.04%
  2022  -4.90%        -6.87%  0.68%    -36.48%  3.73%   1.88%   2.83%   -14.14%  -18.02%  2.07%
  2023  13.85%        3.64%   15.20%   108.54%  8.22%   1.89%   5.02%   3.69%    26.52%   5.30%
  2024  17.51%        13.48%  13.89%   128.76%  3.21%   0.51%   1.87%   -1.33%   25.54%   5.23%
  2025  17.42%        9.62%   11.32%   132.19%  11.86%  -0.01%  5.85%   7.41%    18.45%   4.21%

  dot-com bear years inside this window: 2000, 2001, 2002 (all three are complete years here)
  the reduced book's worst year: -22.22% 2008; losing years: 2001,2002,2008,2018,2022

  correlation matrix of YEARLY returns over the reduced window (27 complete years: 1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025)
           T      X      V      H_a    H_b    H      BOND10M  B      REDUCED  CASH
  -------  -----  -----  -----  -----  -----  -----  -------  -----  -------  -----
  T        1.00   0.79   0.66   -0.16  -0.67  -0.47  -0.45    0.85   0.81     -0.10
  X        0.79   1.00   0.68   -0.05  -0.72  -0.41  -0.42    0.89   0.88     -0.01
  V        0.66   0.68   1.00   0.21   -0.61  -0.15  -0.15    0.63   0.92     0.15
  H_a      -0.16  -0.05  0.21   1.00   0.23   0.87   0.29     -0.14  0.12     0.50
  H_b      -0.67  -0.72  -0.61  0.23   1.00   0.69   0.37     -0.73  -0.73    0.52
  H        -0.47  -0.41  -0.15  0.87   0.69   1.00   0.40     -0.48  -0.28    0.65
  BOND10M  -0.45  -0.42  -0.15  0.29   0.37   0.40   1.00     -0.45  -0.29    0.09
  B        0.85   0.89   0.63   -0.14  -0.73  -0.48  -0.45    1.00   0.83     -0.07
  REDUCED  0.81   0.88   0.92   0.12   -0.73  -0.28  -0.29    0.83   1.00     0.10
  CASH     -0.10  -0.01  0.15   0.50   0.52   0.65   0.09     -0.07  0.10     1.00
  symmetry + unit-diagonal check: PASS
  pairwise correlation with the REDUCED book, lowest first:
    H_b       -0.730
    BOND10M   -0.292
    H         -0.283
    CASH      0.097
    H_a       0.120
    T         0.810
    B         0.833
    X         0.885
    V         0.920

==============================================================================
THE PRE-REGISTERED SUCCESS BAR -- declared before the run, reported honestly
==============================================================================
  bar: >=90% of years positive AND >=75% of quarters positive AND Sharpe > 0.8 AND CAGR above cash

  book                  posY>=90  posQ>=75  S>0.8  CAGR>cash  verdict  posY    posQ    Sharpe  CAGR
  --------------------  --------  --------  -----  ---------  -------  ------  ------  ------  ------
  BOOK div 0bps         n         Y         n      Y          fail     85.00%  83.33%  0.59    8.85%
  BOOK div 5bps         n         Y         n      Y          fail     85.00%  83.33%  0.58    8.68%
  BOOK div 20bps        n         Y         n      Y          fail     85.00%  83.33%  0.54    8.16%
  BOOK price 0bps       n         Y         n      Y          fail     85.00%  82.14%  0.51    7.70%
  BOOK price 5bps       n         Y         n      Y          fail     85.00%  80.95%  0.50    7.53%
  BOOK price 20bps      n         Y         n      Y          fail     85.00%  79.76%  0.46    7.02%
  BOOK-NOV div 0bps     n         Y         n      Y          fail     75.00%  77.38%  0.58    4.63%
  BOOK-NOV div 5bps     n         Y         n      Y          fail     75.00%  76.19%  0.56    4.52%
  BOOK-NOV div 20bps    n         Y         n      Y          fail     75.00%  76.19%  0.50    4.19%
  BOOK-NOV price 0bps   n         n         n      Y          fail     75.00%  72.62%  0.34    3.38%
  BOOK-NOV price 5bps   n         n         n      Y          fail     75.00%  71.43%  0.32    3.27%
  BOOK-NOV price 20bps  n         n         n      Y          fail     75.00%  70.24%  0.26    2.95%
  BOOK-VT div 0bps      Y         Y         n      Y          fail     95.00%  78.57%  0.54    2.74%
  BOOK-VT div 5bps      Y         Y         n      Y          fail     95.00%  78.57%  0.51    2.68%
  BOOK-VT div 20bps     Y         Y         n      Y          fail     95.00%  78.57%  0.41    2.50%
  BOOK-VT price 0bps    n         Y         n      Y          fail     85.00%  76.19%  0.16    2.06%
  BOOK-VT price 5bps    n         Y         n      Y          fail     85.00%  76.19%  0.13    1.99%
  BOOK-VT price 20bps   n         Y         n      Y          fail     85.00%  75.00%  0.03    1.81%
  REDUCED div 0bps      n         Y         n      Y          fail     81.48%  82.88%  0.65    10.52%
  REDUCED div 5bps      n         Y         n      Y          fail     81.48%  82.88%  0.64    10.37%
  REDUCED div 20bps     n         Y         n      Y          fail     81.48%  82.88%  0.61    9.92%
  REDUCED price 0bps    n         Y         n      Y          fail     81.48%  82.88%  0.59    9.56%
  REDUCED price 5bps    n         Y         n      Y          fail     81.48%  82.88%  0.58    9.42%
  REDUCED price 20bps   n         Y         n      Y          fail     81.48%  82.88%  0.55    8.97%

  VERDICT: NOTHING CLEARS THE BAR.  No book, at any cost level, in either dividend treatment, is simultaneously positive in >=90% of years, positive in >=75% of quarters, Sharpe > 0.8 and above cash.
  the closest cell above: BOOK-VT div 0bps

==============================================================================
BEST POINT ACTUALLY ACHIEVED ON THE RETURN-vs-POSITIVITY TRADE-OFF
==============================================================================
  BOOK, dividend-adjusted, 5 bps, lam scan (lam = fraction at risk):
  highest CAGR with 100% of YEARS positive: lam=0.063  CAGR 2.25%

  BEST >=90%-of-years point: lam = 0.553
    CAGR                       5.75%
    max drawdown               -16.45%
    Sharpe (excess of cash)    0.58
    years positive             18/20
    Losing years               -10.47% 2008, -5.44% 2018
    quarters positive          86.90%
    months positive            81.35%
    worst month                -6.20% (2018-10)

  full-scale (lam=1.0) BOOK, dividend-adjusted, 5 bps:
    CAGR 8.68%, maxDD -28.59%, Sharpe 0.58
    vs SPY buy&hold (div): CAGR 11.08%
    Losing years: -19.69% 2008, -11.48% 2018, -2.15% 2022

  wrote 36 CSV/text artefacts to C:\Users\sande\Documents\Projects\Skills\skills\14-finance\equity-trading-playbook\examples\weather-deep-test\out
```

## HANDCHECK.PY -- the independent re-derivation, verbatim

`handcheck-output.txt` -- sha256 `72d6fac89d69e724054e3a7497ff1f50099072d4ecd33bbd726e999a0ce3a32e`

```
==============================================================================
HANDCHECK -- independent re-derivation.  Imports nothing from study.py.
==============================================================================
  book calendar from out/book_daily_div_5bps.csv: 5292 days, 2005-09-30..2026-10-14

[1] SPY buy-and-hold monthly returns from raw closes vs the `B` column
  max |recomputed B - study B| over 252 months               gap = 4.995e-11              worst month 2006-10

[2] BOOK daily series re-simulated from sleeve daily returns and the fixed targets
  fixed targets taken from out/book_weights.csv: C=0.1500, CASH=0.1000, H=0.1000, T=0.4000, V=0.1000, X=0.1500
  max |re-simulated BOOK daily - study BOOK daily|           gap = 8.899e-11              over 5292 days

[3] BOOK monthly returns compounded from the re-simulated daily series
  max |daily-compounded BOOK month - study BOOK month|       gap = 2.232e-10              worst month 2010-06

[4] THE BY-HAND BOOK MONTH: sum_s w_s * r_s(month), fixed weights and sleeve monthly returns ONLY
  month 2013-06 by hand:
      w_C    = 0.1500  x  r = +0.335719%
      w_CASH = 0.1000  x  r = +0.004012%
      w_H    = 0.1000  x  r = -1.341493%
      w_T    = 0.4000  x  r = -0.294799%
      w_V    = 0.1000  x  r = +6.764123%
      w_X    = 0.1500  x  r = -0.385246%
      hand total             = +0.417316%
      study BOOK month       = +0.416960%
      difference             = +0.000356 pp  (intra-month weight drift + the monthly rebalance cost)
  [4a] hand-month vs daily-re-simulated month                gap = 3.558e-06              the drift/cost gap, reported not hidden
  [4b] daily-re-simulated month vs study BOOK month          gap = 3.714e-11

[5] ONE PAIRWISE YEARLY CORRELATION, recomputed by hand from out/years.csv
  corr(T, B) over 20 years: hand vs corr_yearly.csv          gap = 1.928e-10              hand=0.468046 study=0.468046

[6] corr_yearly.csv is symmetric with a diagonal of exactly 1
  max |C[i][j] - C[j][i]|                                    gap = 0.000e+00
  max |C[i][i] - 1|                                          gap = 0.000e+00

[7] CAGR and maximum drawdown recomputed from out/book_daily_div_5bps.csv vs out/summary.csv
  CAGR hand vs summary.csv                                   gap = 9.629e-11              hand=0.086762 study=0.086762
  maxDD hand vs summary.csv                                  gap = 5.310e-11              hand=-0.285909 study=-0.285909

[8] positivity for Y and Q recomputed from the daily series vs out/horizon.csv
  positive-year fraction hand vs horizon.csv                 gap = 0.000e+00              hand=0.850000 study=0.850000 (17/20)
  positive-quarter fraction hand vs horizon.csv              gap = 3.333e-11              hand=0.833333 study=0.833333 (70/84)

[9] THE TREND SLEEVE, month 2013-06, rebuilt from raw prices
  instruments live at 1928: 31 of 31
  hand T month, method B (daily weighted sum, as the study does it) = -0.255035%
  [9b] |hand T month method B - study T month at 0 bps|      gap = 5.214e-11              method B reproduces the engine's own compounding order
  [9c] method A vs method B (the within-month rebalancing effect) gap = 1.891e-04
  long weight this month: 0.1880 ; the rest earns cash (0.004012%)
  hand T month, method A (fixed weights, each instrument compounded then weighted) = -0.273947%
  study T month at 0 bps                          = -0.255035%
  study T month at 5 bps                          = -0.294799%
  => the study's 5 bps rebalance cost for this month is 3.9764 bp
  [9a] |hand T month method A - study T month at 0 bps|      gap = 1.891e-04              method A deliberately does NOT reproduce the engine's daily rebalancing, so a residual here is expected

[10] CASH accrual, month 2013-06, from data/US03M_1d.csv
  [10] |hand cash month - study cash month|                  gap = 5.238e-11              hand=0.00401198%

[11] THE [MODELED] VRP SLEEVE, roll at the start of 2013-06, from VIX and SPY prices
    SPY=163.4450  VIX(t-3)=14.4800  iv=0.1448  r=0.0003  q=0.0180
    K1=156.1027  K2=148.2976  width=7.8051  credit=0.5593  credit/width=7.1655%
    the study's own credit/width for the whole run is in out/summary.csv's [MODELED] V row context; this single-roll value is the check
    expiry 2013-07-01  S_T=161.3600  intrinsic payoff=0.0000
    hand V total-to-expiry P&L = +7.165512% of the posted width
    window 2013-06-03..2013-06-28 (the session before settlement)
    hand mark-to-market over that window = +6.817532% of width
    study, 0 bps   = +6.817532%    study, 5 bps = +6.764123%
    the 0-to-5 bps difference is exactly the roll cost: (5/2)/10000 * turnover 2.0 = 0.050000% per roll
    at 2013-06-28: S=160.4200 T_rem=0.008219 r=0.000560 q=0.0180  put(K1)=0.027161 put(K2)=0.00000017  L=0.027160
    implied study mark at 2013-06-28: L=0.027160   (hand L=0.027160, difference 6.24e-10 in price)
  [11] |hand V mark-to-market - compounded study V, same window| gap = 7.998e-11              hand=0.068175 study=0.068175

==============================================================================
HANDCHECK SUMMARY -- 17 checks
==============================================================================
  gap >= 1e-9 : [4a] hand-month vs daily-re-simulated month                3.557689e-06
  gap >= 1e-9 : [9c] method A vs method B (the within-month rebalancing effect) 1.891182e-04
  gap >= 1e-9 : [9a] |hand T month method A - study T month at 0 bps|      1.891181e-04
  largest gap across every check: 1.891e-04
  checks agreeing to < 1e-12      : 3 of 17

  THE THREE NON-ZERO GAPS, NAMED:
   [4a] 3.6e-06  the by-hand fixed-weight book month vs the
                 engine's monthly return.  The by-hand arithmetic
                 cannot see the intra-month weight drift or the
                 monthly rebalance cost; both are inside the
                 engine's number.  Reported, not hidden.  Check
                 [4b] proves the engine's own book is reproduced
                 exactly (3.7e-11).
   [9a]/[9c] 1.89e-04  fixed weights, each instrument compounded and
                 then weighted, vs the engine's fixed weights with
                 the DAILY weighted sum compounded.  These differ by
                 the within-month rebalancing effect and by nothing
                 else: check [9b] rebuilds the sleeve the engine's
                 way and lands within 5.2e-11, and [9c] is exactly
                 the same number as [9a].
   [11] is now 8.0e-11.  Its earlier 5.3e-04 was ENTIRELY the 5 bps
                 roll cost ((5/2)/10000 x turnover 2.0 = 0.05% a
                 roll), which the check now removes by using the
                 0 bps sleeve series.
```
