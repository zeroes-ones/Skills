# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You think FinOps means "look at the AWS bill once a month and tell engineers to delete unused EBS volumes" | You've implemented automated tagging enforcement, a cost anomaly detection system that catches spikes within 24 hours, and a showback/chargeback dashboard that every team lead reviews weekly | You've negotiated a 3-year Enterprise Discount Program with AWS that reduced the organization's blended rate by 37%, and you can prove it with a before/after analysis that the CFO presented to the board |
| You discover cloud waste by accident — a developer asks "why is this EC2 instance still running?" 8 months after the project ended | Every resource has an owner tag, every non-production resource auto-shuts-down outside business hours, and your stale resource report runs weekly with < 5 orphaned resources | You've built a unit economics model that calculates cloud cost per customer, per API call, and per feature — and product managers use it to prioritize features based on margin, not just revenue |
| You bought Reserved Instances for "everything that runs 24/7" and discovered 40% were the wrong instance family, region, or platform 6 months later | Savings Plan coverage is at 92%+ for compute, RI coverage is at 85%+ for RDS/ElastiCache, and your commitment portfolio is rebalanced quarterly based on the last 90 days of usage | You've reduced cost per transaction by 58% year-over-year while traffic doubled — the unit economics improved because you negotiated better rates, optimized architectures, and eliminated the bottom 20% of underutilized resources |

**The Litmus Test:** Can you look at a $500,000 monthly AWS bill with 40 linked accounts, identify the top 3 cost drivers in under 10 minutes, and propose changes that will reduce next month's bill by at least $75,000 — without degrading performance or availability — and actually deliver those savings?
