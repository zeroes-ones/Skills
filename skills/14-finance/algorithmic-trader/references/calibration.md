# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You backtest a strategy and celebrate a Sharpe of 3.0 without asking "where did the look-ahead bias come from?" | You've run a strategy live for 12+ months and the live Sharpe is within 30% of the backtest Sharpe — and you can explain every source of the gap | You can look at a backtest report for 5 minutes and identify the data leak, survivorship bias, or overfitting pattern before reading the methodology section |
| You size positions as "2% of account" without adjusting for the stock's actual liquidity, spread, or your own market impact | You compute position limits from ADV, spread, and your execution algo's expected fill rate — and you've rejected trades that pass signal quality but fail liquidity checks | You've designed a sizing framework that keeps a $500M book's market impact under 5 bps while trading 200+ names — and the broker's execution consulting desk confirms your numbers |
| You trust the broker API's "order accepted" response without verifying the order reached the exchange | Your system polls for "working" or "live" status with a 5-second timeout and escalates to a human if the order hasn't reached the exchange — and you test this failure path monthly | You've survived a flash crash without a single order stuck in a broker queue because your system detected the gateway throttle, switched to the backup routing path, and executed within 8 seconds |

**The Litmus Test:** Trade your own money — at least $10,000 — on a strategy you designed, for 6 consecutive months, with no manual intervention after the first week. If you can't stomach it, your clients shouldn't either. If you make money, check whether it was luck (run a bootstrap simulation on your trade-level returns). If you can't tell the difference between skill and luck in your own P&L, you're not L3 yet.
