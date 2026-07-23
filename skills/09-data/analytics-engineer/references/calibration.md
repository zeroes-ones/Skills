# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can write SQL and build dbt models but don't know why a query scanning 500M rows at 9 AM every day is a problem for anyone else | You've designed a dbt project from scratch with staging/intermediate/marts layers, full test coverage, and CI that only builds changed models and their downstream dependents | A VP asks "why do Sales and Finance show different revenue numbers?" and you trace the discrepancy through 15 models to the root cause in under 15 minutes |
| You rename a column in a base model without checking downstream dependencies — and discover 40 broken dashboards when Slack blows up at 8:30 AM | You add a column to a staging model and your CI pipeline tells you exactly which 12 downstream models are affected, with impact estimates, before you merge | You can estimate the Snowflake/BigQuery cost of a proposed data model change before it's built, and your estimate is within 20% of actual every time |
| You copy-paste metric definitions between dashboards because "it's the same KPI" and don't realize they've drifted apart over 6 months | You define every metric once in the metric layer, every dashboard references that single definition, and a nightly reconciliation catches discrepancies before anyone sees them | A company adopts your metrics framework and 6 months later, Finance, Sales, and Product all report the exact same Q3 net revenue within the same hour — and an auditor confirms it |

**The Litmus Test:** Take the most complex dashboard your company relies on for weekly decisions. Can you trace every number back to its raw source table, explain every transformation, and prove the number is correct? If you can't do this for your company's top 10 KPIs right now, you're not L3 yet.
