# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You `kubectl edit` or click in the AWS console to make changes | All infrastructure changes flow through Git → CI → apply. You haven't touched a cloud console in 6 months | You design the platform other teams use — they don't know what Terraform or Kubernetes are, they just push code and it deploys |
| You run `terraform apply` from your laptop and hope it works | Your CI pipeline runs `terraform plan` on every PR and posts the diff as a comment. Apply requires human approval | You've reduced the mean time from commit to production from 2 hours to 8 minutes, and you can prove it with DORA metrics |
| You discover that a secret is in plaintext by accident — during a code review or security scan | Secrets are managed by Vault/SOPS/External Secrets Operator. A pre-commit hook blocks any commit with an AWS key pattern or `password =` | You've designed a secret rotation system that automatically rotates database credentials every 30 days with zero application downtime |

**The Litmus Test:** Can you recover from a complete region failure — DNS flip, database failover, application redeployment — in under 15 minutes without a runbook? If you need a runbook, your system isn't resilient enough. If the runbook is wrong, you find out during the incident.
