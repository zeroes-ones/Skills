# Scale Depth

<!-- QUICK: 30s -- find your team size column -->

### Solo
- **What changes**: Single strategy, manual execution via broker UI. Learn market mechanics, prove a thesis. Execute trades manually; no automation; spreadsheet-based tracking.
- **What to skip**: Real-time risk monitoring (end-of-day is fine). Multi-strategy correlation. Automated execution. Colocation or low-latency infrastructure. Regulatory compliance frameworks.
- **Coordination**: Self-contained. Track P&L in a spreadsheet. Review weekly.
- **Cost**: Free — Alpaca paper trading API, Yahoo Finance data, Python.

### Small Team
- **What changes**: Automated trading bot, backtesting framework, paper trading. Build reliable automation, validate strategies. Code executes trades; backtesting catches bad strategies before real money.
- **What to skip**: Multi-strategy portfolio management. Real-time correlation monitoring. Full risk management system. Institutional-grade execution.
- **Coordination**: Weekly strategy review with trader. Backtest results shared before paper trading. Developer handles execution reliability.
- **Cost**: $500-$2K/month (broker API, cloud VM, basic market data).

### Medium Team
- **What changes**: Multi-strategy portfolio, risk management system, real-time monitoring. Diversify alpha, manage drawdowns. Portfolio-level risk controls; strategy correlation monitored; position sizing automated.
- **What to skip**: Market making. Colocation and FPGA execution. SEC/FINRA institutional compliance. Internal quantitative research platform.
- **Coordination**: Daily risk meeting. Bi-weekly strategy review. Integration with execution/OMS. Compliance oversight introduced.
- **Cost**: $5K-$30K/month (risk monitoring platform, multiple data feeds, cloud compute).

### Enterprise
- **What changes**: Market making, institutional execution, regulatory compliance. Scale AUM, minimize market impact. Colocation, smart order routing, SEC/FINRA compliance, institutional counterparties.
- **What's full production**: 24/7 operations team. Dedicated risk management team. Model governance framework. Annual external audits.
- **Coordination**: Daily risk meeting. Weekly strategy performance review. Monthly compliance review. Quarterly model audit.
- **Cost**: $50K-$500K+/month (colocation, data, compute, team, compliance).

### Transition Triggers

| From \u2192 To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo \u2192 Small | Automated strategy profitable for 3+ months, AUM >$100K | Move from manual to automated execution; add basic backtesting; formalize entry/exit rules |
| Small \u2192 Medium | Multi-strategy, AUM >$2M, >10 signals/day | Add portfolio-level risk controls; implement real-time monitoring; hire dedicated operations |
| Medium \u2192 Enterprise | Institutional counterparties, regulatory requirements, AUM >$50M | Colocate; implement smart order routing; build compliance framework; hire risk and compliance team |
