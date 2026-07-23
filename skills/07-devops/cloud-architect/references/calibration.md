# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You design architecture by opening the AWS console and clicking "Launch Wizard" — you don't know what a CIDR block is or why subnets matter | You've designed a multi-account landing zone with AWS Organizations, centralized logging, and network hub-and-spoke. You can draw the entire architecture from memory in 20 minutes | You've led a cloud migration of 200+ services across 3 providers with zero customer-impacting outages — and the migration was completed under budget because you modeled costs at the SKU level before moving a single workload |
| You hear "well-architected" and think it means "it works and has an auto-scaling group" | You've run the AWS Well-Architected Tool against production workloads in the last 6 months, have a prioritized remediation backlog, and can name all 6 pillars without Googling | You've designed a multi-cloud architecture where a single-region provider failure triggers automatic failover to a different cloud provider in under 5 minutes — and you've proven it works in an unannounced gameday |
| Your disaster recovery plan is "we have multi-AZ" — you've never tested failover, and you don't know the difference between RPO and RTO for your tier-1 services | All tier-1 services have documented RPO ≤ 5 minutes and RTO ≤ 15 minutes. You've executed unannounced DR tests quarterly for 2 years and the team recovers within the window every time | You've reduced the organization's cloud spend by 40% year-over-year while simultaneously improving availability from 99.9% to 99.99% — the CFO and CTO both cite your work in board decks |

**The Litmus Test:** Can you receive a merger-acquired company's AWS organization on Friday at 4:00 PM and have their production workloads running in your landing zone — with networking, IAM, logging, and security controls fully integrated — by Monday 9:00 AM, without breaking either company's existing production traffic?
