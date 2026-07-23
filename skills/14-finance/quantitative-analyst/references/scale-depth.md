# Scale Depth

<!-- QUICK: 30s — find your team size column -->

### Solo (1 person, personal account)
- **What changes**: You are the quant, the data engineer, and the trader. Use free options data (Yahoo Finance delayed quotes, Polygon.io free tier). Focus on UOA on 5-10 mid-cap names you know well. Rules-based signals only (no ML). Manual entry from signals — no automated execution. Excel + Python scripts. Greeks from free calculators (no real-time surface).
- **What to skip**: Real-time scanning (end-of-day is fine). Multi-leg detection (manual spotting). Full IV surface construction. Automated execution. ML-based classification. Institutional-grade data feeds.
- **Coordination**: Self-contained. Track signals in a spreadsheet. Review weekly.
- **Cost**: Free — Yahoo Finance, Python (scipy, numpy, pandas), Polygon.io free tier (5 API calls/min).

### Small Team (2-10 people, small fund/prop trading)
- **What changes**: Real-time options data feed (OPRA via broker API or paid provider like ORATS, CBOE DataShop). Automated UOA scanner running intraday. Greeks computed in real-time (Black-Scholes inversion on every tick). Rules-based signals with basic backtesting. Signal delivery via Slack/email to trader. IV surface built daily. Multi-leg detection via time-clustering. Sector ETF context from free market data APIs.
- **What to skip**: ML-based signal classification. Real-time IV surface (daily rebuild is fine). Full portfolio Greeks integration. Automated execution (manual review still). Tick-level data storage. Custom pricing models beyond Black-Scholes.
- **Coordination**: Morning signal review. Weekly backtest review with trader feedback loop. Coordinate with data provider for feed reliability.
- **Cost**: $500-$3,000/month (OPRA data feed, small cloud VM for scanner, basic market data APIs).

### Medium Team (10-50 people, mid-size fund)
- **What changes**: Full institutional data feed (Bloomberg/Reuters/OPRA direct). Real-time UOA scanner with tick-level processing. ML-based signal classification alongside rules-based (ensemble approach). Real-time IV surface with arbitrage-free interpolation (SVI/SSVI parameterization). Automated execution of STRONG BUY signals (human override for BUY/WEAK). Portfolio-level Greeks and risk. Historical tick database for backtesting. Automated multi-leg detection with strategy recognition.
- **What to skip**: Custom exchange connectivity (use broker API). Full HFT infrastructure (not needed for mid-frequency options flow). Market making models. Exotic options pricing (focus on vanilla US equity options).
- **Coordination**: Daily signal review meeting. Bi-weekly model performance review with data scientist. Integration with execution/OMS. Compliance review of signal methodology.
- **Cost**: $10K-$50K/month (Bloomberg terminal, OPRA direct feed, cloud compute for scanning + ML, execution platform).

### Enterprise (50+ people, large fund/bank trading desk)
- **What changes**: Colocated OPRA feed processing. FPGA-accelerated UOA detection (microsecond latency). Deep learning signal classification with attention mechanisms on order flow. Real-time, arbitrage-free IV surface across all strikes/expiries. Full integration with OMS/EMS for automated execution with smart order routing. Real-time portfolio Greeks with scenario analysis (SPX -5%, VIX +10, etc.). Tick data warehouse with petabyte scale. Quantitative research platform for signal alpha research. Counterparty flow analysis. Multi-asset options (equity, index, ETF, futures options).
- **What's full production**: 24/7 operations team. Model risk management framework. Regulatory capital calculations integrated with options positions. Cross-asset risk management. Dedicated quant research team. Annual model audits.
- **Coordination**: Daily risk meeting. Weekly quant research review. Monthly model governance committee. Quarterly regulatory review.
- **Cost**: $200K-$1M+/month (colocation, data, compute, team, compliance, execution).

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | >$50K AUM or 10+ signals/week requiring real-time response | Add real-time data feed; automate UOA scanner; start Greeks computation |
| Small → Medium | 50+ signals/day, AUM >$5M, need automated execution | Add ML classification; build real-time IV surface; integrate with OMS |
| Medium → Enterprise | Multi-asset options, regulatory requirements, >$100M AUM | Colocate; add FPGA/DL pipeline; build quant research platform; hire risk team |
