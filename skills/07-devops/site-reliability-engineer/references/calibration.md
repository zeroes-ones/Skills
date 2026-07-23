# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You think SRE means "ops team with a cooler name." You page the on-call engineer for every alert, including "disk usage at 71%" | Every service has defined SLOs with error budgets. Alerts fire on burn rate, not threshold breaches. The on-call rotation has a < 10% burnout rate | You've designed an error budget policy that is enforced programmatically: when the budget burns > 50%, deploys are automatically frozen until root cause is fixed, and the VP of Engineering supports this without exception |
| You manually run `top`, `df -h`, and `netstat` on production servers to "check health" — you call this "monitoring" | Toil is tracked as a metric. The team's toil percentage dropped from 60% to under 25% in 6 months because you automated the top 5 toil sources. Every PR reduces toil or adds reliability — never the reverse | You've led the SRE transformation of an organization from "no SRE" to "every team has embedded SRE practices": SLOs, error budgets, blameless postmortems, and gamedays are standard operating procedure across 200+ engineers |
| Your postmortems end with "human error" as the root cause. You've never heard of "blameless culture" | Every significant incident has a blameless postmortem published within 72 hours. Action items are tracked to completion in the team's backlog. The same class of incident never happens twice | You've reduced the organization's change failure rate from 30% to under 3% in 18 months, and the MTTR dropped from 4 hours to 12 minutes — you can prove both with 18 months of DORA metrics tracked in a public dashboard |

**The Litmus Test:** Can you calculate your team's error budget burn rate, toil percentage, and change failure rate — right now, without looking anything up — and cite the exact number of incidents that consumed the most error budget in the last 30 days?
