# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Tagging strategy documented with mandatory tags (`Environment`, `Service`, `Team`, `CostCenter`, `Owner`) | `grep -rn "tags\s*=" main.tf \| wc -l` → ≥ 1 AND `grep -rnE "(Team\|Environment\|CostCenter\|Service)" main.tf \| wc -l` → ≥ 3 | Add mandatory tag block to all resource modules |
| **[S2]** | Tag enforcement in place via SCP, Azure Policy, or Org Policy; > 95% resource tag compliance | `aws resourcegroupstaggingapi get-resources --tags-per-page 100 \| jq '.ResourceTagMappingList \| length'` → equals total resources | Apply SCP denying resource creation without required tags |
| **[S3]** | Budget alerts configured per team/environment at 50%, 80%, 100%, 120% thresholds | `grep -rn "budgets_budget\|budget_alert" main.tf \| wc -l` → ≥ 1 | Add `aws_budgets_budget` with 4 threshold alerts |
| **[S4]** | Cost anomaly detection enabled and alerting to team communication channels | `grep -rn "anomaly_monitor\|anomaly_subscription" main.tf \| wc -l` → ≥ 1 | Add `aws_ce_anomaly_monitor` + `aws_ce_anomaly_subscription` |
| **[S5]** | Cost dashboards available to all engineering teams (self-service, updated daily) | `grep -rn "grafana\|cost.*dashboard\|infracost\|vantage" . --include="*.md" \| wc -l` → ≥ 1 | Deploy Infracost dashboard or CloudHealth/Vantage |
| **[S6]** | RI/SP coverage at 60-80% for steady-state compute; review coverage monthly | `aws ce get-reservation-coverage --time-period \| jq '.Total.CoverageHours.CoverageHoursPercentage'` → between 60-80 | Purchase Savings Plans for gap to reach 60-80% coverage |
| **[S7]** | Right-sizing review completed within last 90 days; recommendations implemented | `find . -name "right-sizing*" -mtime -90 \| wc -l` → ≥ 1 | Run AWS Compute Optimizer + generate right-sizing report quarterly |
| **[S8]** | Spot instances adopted for > 40% non-production and > 20% production stateless workloads | `grep -rn "spot\|spot_instance\|spot_fleet" main.tf \| wc -l` → ≥ 1 | Add Spot instance pools for stateless workloads |
| **[S9]** | S3/Azure Blob/GCS lifecycle policies applied to all buckets | `aws s3api get-bucket-lifecycle-configuration --bucket <name>` → non-empty for all buckets | Add lifecycle policy: transition to IA after 30d, expire after 90d |
| **[S10]** | Data transfer optimization: VPC endpoints for S3/DynamoDB, CDN for egress-heavy endpoints | `grep -rn "vpc_endpoint\|cloudfront\|cdn" main.tf \| wc -l` → ≥ 1 | Add S3/DynamoDB VPC endpoints + CloudFront distribution |
| **[S11]** | Kubernetes cost allocation implemented (kubecost or equivalent) | `kubectl get pods -n kubecost \| wc -l` → ≥ 1 | `helm install kubecost kubecost/cost-analyzer` |
| **[S12]** | Idle resource cleanup automated: non-production shutdown nights/weekends | `grep -rn "schedule\|cron" --include="*.tf" AND grep -rn "stop\|terminate\|shutdown"` → related to instance scheduling | Add Instance Scheduler: stop dev/staging instances 8pm-7am + weekends |
| **[S13]** | Monthly FinOps review established with action items and ownership | `find . -name "finops*review*" -mtime -30 \| wc -l` → ≥ 1 | Schedule recurring calendar + FinOps review template |
| **[S14]** | Unit economics dashboard for at least top-3 products/customer segments | `grep -rn "unit.economics\|cost.per.customer\|cost.per.request" . --include="*.md" \| wc -l` → ≥ 1 | Build unit economics dashboard linking cost to business metrics |
| **[S15]** | Carbon footprint baseline measured; reduction targets set | `grep -rn "carbon\|sustainability\|emissions" . --include="*.md" \| wc -l` → ≥ 1 | Enable AWS Customer Carbon Footprint Tool + set 12-month reduction target |
