# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Multi-account/multi-project isolation with separate production and non-production environments | `grep -rn "provider.*aws" main.tf \| wc -l` → ≥ 2 (separate accounts) OR `grep -rn "project_id\|subscription_id" main.tf \| sort -u \| wc -l` → ≥ 2 | Create separate provider aliases per environment |
| **[S2]** | Networking: non-overlapping CIDRs, private subnets for workloads, NAT Gateway for egress, VPC Flow Logs | `grep -rnE "cidr_block.*10\.\|cidr.*172\.\|cidr.*192\." main.tf \| wc -l` → ≥ 1 AND `grep -rn "vpc_flow_log\|flow_log" main.tf \| wc -l` → ≥ 1 | Generate VPC module with private subnets + flow logs |
| **[S3]** | IAM: SSO configured, no long-lived access keys, break-glass roles, permission boundaries | `grep -rn "aws_iam_access_key\|access_key" main.tf \| wc -l` → 0 AND `grep -rn "permissions_boundary" main.tf \| wc -l` → ≥ 1 | Replace access keys with OIDC roles; add permission boundaries |
| **[S4]** | Encryption: data at rest with CMK, TLS 1.2+ in transit, S3 bucket policies block public access | `grep -rn "kms_key_id\|kms_key_arn" main.tf \| wc -l` → ≥ 1 AND `grep -rn "block_public_\|restrict_public" main.tf \| wc -l` → ≥ 1 | Add `aws_s3_bucket_public_access_block` + CMK to all data stores |
| **[S5]** | Logging: CloudTrail/Audit Logs enabled org-wide, centralized to security account | `grep -rn "cloudtrail\|aws_cloudtrail\|audit_log" main.tf \| wc -l` → ≥ 1 | Add `aws_cloudtrail` with org-wide + log validation |
| **[S6]** | Backups: automated backups for all data stores, cross-region replication, restore tested quarterly | `grep -rn "backup_retention_period\|backup_window\|backup_vault" main.tf \| wc -l` → ≥ 1 AND `grep -rn "cross_region_replication\|replica\|replication" main.tf \| wc -l` → ≥ 1 | Add `aws_backup_plan` + cross-region replica for critical data stores |
| **[S7]** | Cost: budgets set with alerts, tagging strategy enforced, RI/SP coverage for baseline workloads | `grep -rn "budgets_budget\|budget_alert" main.tf \| wc -l` → ≥ 1 AND `grep -rn "tags\s*=" main.tf \| wc -l` → ≥ 1 | Add `aws_budgets_budget` with 50/80/100% alerts + mandatory tag policy |
| **[S8]** | DR: RPO/RTO defined, failover runbook documented and tested, multi-region for tier-1 services | `grep -rn "rpo\|rto\|recovery_time\|recovery_point" . --include="*.md" \| wc -l` → ≥ 2 AND `grep -rn "dr.*test\|failover.*test" .github/workflows/ \| wc -l` → ≥ 1 | Create DR runbook template + scheduled DR test workflow |
| **[S9]** | Well-Architected Framework review completed within the last 6 months | `find . -name "wafr*" -mtime -180 \| wc -l` → ≥ 1 | Run WAFR tool: `aws wellarchitected list-lenses` |
| **[S10]** | Incident response plan covers cloud-specific scenarios and tested annually | `grep -rn "incident.*response\|ir.*plan" . --include="*.md" \| wc -l` → ≥ 1 | Generate IR plan template + schedule annual game day |
