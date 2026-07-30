# Portfolio Signal Manager — Error Recovery

## Symptom → Root Cause → Fix

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Conflicting signals from different sources cause inaction | No signal priority framework. Equal weight to contradictory signals. Analysis paralysis. | Signal hierarchy: position sizing overrides > risk limits > entry timing > conviction adjustments. When signals conflict, follow the hierarchy. Log all conflicts for review. | **Conflicting signals without a hierarchy = no signal.** The worst outcome is doing nothing while paying data costs. Define the override chain before conflicts happen. |
| Portfolio concentration creep: 3 positions become 40% of book | Winners grow relative to losers. No rebalancing triggers. Emotional attachment to winners. | Position-size caps enforced at signal generation, not just execution. Rebalance triggers: single position >15% or top 3 >40%. Rebalance monthly or at 5% drift. | **Letting winners run sounds smart until it's not.** Concentration builds slowly and explodes suddenly. Caps prevent the slow drift that becomes catastrophic. |
| Circuit breaker triggers on false positive, missed rally | Circuit breaker too sensitive. Single-day drawdown trigger ignores recovery. No re-entry criteria. | Two-stage circuit: Stage 1 (reduce size 50%) on 5% daily drawdown. Stage 2 (stop trading) on 10% daily drawdown. Auto-resume after 2 consecutive green days with half-size. | **Circuit breakers protect capital but cost opportunity.** Design re-entry criteria as carefully as exit criteria. A breaker without re-entry = portfolio in permanent timeout. |
| Tax-aware management creates tracking error vs. benchmark | Tax-loss harvesting changes sector weights. Wash-sale rules prevent re-entry. STCG vs. LTCG timing mismatch. | Track pre-tax and post-tax performance separately. Tax-alpha = post-tax return - pre-tax return. Accept 1-3% tracking error for 2-5% tax alpha. | **Tax optimization is real alpha, not tracking error.** A 2% annual tax saving compounds to 22% over 10 years. That's bigger than most active manager outperformance. |
| Signal decay: strategy performance degrades over time | Alpha decay as more participants discover the signal. Market structure changes. Regime shift. | Monitor rolling 12-month Sharpe. If Sharpe declines >30% from inception, investigate. Walk-forward test on most recent 2 years. Retire strategies with negative 6-month rolling Sharpe. | **All alpha decays. The question is when.** Monitor for decay continuously. A strategy that worked for 5 years can stop working in 5 months when the market adapts. |

## Provenance
[VERIFIED] Portfolio management failure modes from institutional asset management
[COMPUTED] Concentration and tax cost estimates based on typical portfolio sizes
[AS OF 2026-01]

