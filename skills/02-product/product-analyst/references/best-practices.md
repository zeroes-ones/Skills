## Best Practices

1. **Instrument before you ship** — Every feature launch includes tracking spec. Retrofitting instrumentation is 3x the effort and loses historical data.

2. **One metric per experiment** — Primary metric determines ship/kill. Multiple primaries = multiple comparison problem. Use secondary metrics for understanding only.

3. **Cohort by acquisition week, not calendar month** — Week-1 retention for users acquired Jan 1-7 vs Jan 8-14. Calendar months mix users with different product ages.

4. **Always report confidence intervals** — "Lift = 5.2% [95% CI: 2.1% to 8.3%]" is actionable. "Lift = 5.2%" without CI is half the information.

5. **Segment by behavior, not just demographics** — "Users who invite 3+ friends in week 1 retain at 2x" is actionable. "Male users 25-34 retain at 1.1x" rarely is.

6. **Guardrail metrics prevent local optimization** — Optimizing signups at the cost of activation is worse than doing nothing. Always monitor counter-metrics.

7. **Event taxonomy is a contract** — `user_signed_up` must mean the same thing everywhere. Document: event name, properties, when it fires, what it excludes. Taxonomy drift = untrustworthy data.

8. **Time-bound your experiments** — Never run an A/A test to "verify the system." If randomization is broken, fix it. A/A tests waste traffic. Run one at setup, then trust your randomization.

9. **Retention curves need 3+ periods for trends** — One cohort's retention tells you nothing about trajectory. You need at least 3 sequential cohorts to see if retention is improving or degrading.

10. **Dashboards answer questions, not decorate walls** — Every dashboard tile should trace to a decision. "If this number moves, what do we do?" If the answer is "nothing," remove the tile.
