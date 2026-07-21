---
name: finops-engineer
description: FinOps, cloud cost optimization, AWS billing, Azure cost management, GCP billing, cloud economics, cost governance, resource optimization, waste reduction, reserved instances, savings plans, unit economics. Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - finops-engineer
token_budget: 2314
output:
  type: "code"
  path_hint: "./"
---
# FinOps Engineer / Cloud Cost Optimization

Drive cloud financial accountability through the FinOps lifecycle: Inform (visibility, allocation),
Optimize (right-sizing, commitment discounts, waste elimination), and Operate (governance, unit
economics, continuous improvement). Covers multi-cloud cost management, tagging strategy,
Reserved Instances/Savings Plans, Kubernetes cost optimization, spot instance strategy, storage
tiering, data transfer optimization, anomaly detection, and carbon-aware cost reduction.

## When to Use

- Your monthly cloud bill (AWS/Azure/GCP) has spiked and you need to identify the root cause
- You need to implement a tagging strategy to allocate cloud costs to teams, projects, and environments
- You are evaluating Reserved Instances vs. Savings Plans vs. on-demand to reduce compute spend
- You need to right-size underutilized resources — instances with <10% CPU or idle load balancers
- You are setting up cost anomaly detection and budget alerts to catch spending surprises early
- You need to optimize Kubernetes cluster costs through node autoscaling, bin packing, and spot instances
- You are building unit economics dashboards to tie cloud spend to business metrics (cost per customer, per API call)
- You need to reduce data transfer costs between regions, availability zones, or out to the public internet

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. Reserved Instance vs. Savings Plan vs. On-Demand
```
What's the workload profile?
├─ Steady-state, predictable (24/7 production, no seasonal spikes)?
│   └─ All Upfront Reserved Instance (3-year): max discount (up to 72% off on-demand)
│       └─ Rule: commit only when workload has been stable for > 90 days
├─ Steady-state but may change instance family over time?
│   └─ Compute Savings Plan (1-year or 3-year): 66% off, flexible across families/regions
│       └─ Rule: best default choice — balances discount with flexibility
├─ Variable but has a minimum baseline (e.g., 40% of peak at all times)?
│   └─ Savings Plan for baseline (40-60%) + On-Demand/Spot for variable
│       └─ Rule: RI/SP coverage target = 60-80% of compute spend; not 100%
├─ Stateless, fault-tolerant, batch, or CI/CD workloads?
│   └─ Spot instances (up to 90% off): with fallback to on-demand
│       └─ Rule: MUST have graceful interruption handling; Spot cannot be > 70% of a critical service
├─ Short-lived, unpredictable (hackathon, POC, burst)?
│   └─ On-Demand: no commitment penalty
└─ WARNING: Buying RIs/SPs for workloads < 6 months old = overcommitment risk
```

### 2. Right-Sizing Decision
```
Resource utilization analysis:
├─ CPU < 10% avg over 30 days?
│   ├─ AND Memory < 20% → DOWNGRADE 2 sizes (or consolidate workloads)
│   ├─ AND Memory 20-50% → DOWNGRADE 1 size
│   └─ AND Memory > 50% → Memory-bound; CPU is irrelevant → consider memory-optimized instance
├─ CPU 10-40% AND Memory 10-40%?
│   └─ Adequate: no change unless cost-per-transaction exceeds target
├─ CPU 40-70%?
│   └─ Optimal range: no action unless bursting patterns suggest auto-scaling would save more
├─ CPU > 70% sustained?
│   └─ UPGRADE or enable auto-scaling
│       └─ Rule: if utilization is > 70% for > 4 hours/day, you need more capacity
├─ Storage attached (EBS, managed disk, persistent disk)?
│   └─ Check provisioned IOPS vs consumed: paying for unused IOPS → switch to GP3/auto-tier
└─ Implementation: change instance type in IaC, deploy during maintenance window, verify performance
```

### 3. Storage Tier Optimization
```
Object storage lifecycle decision:
├─ Accessed hourly?
│   └─ Hot tier (S3 Standard, GCS Standard, Azure Hot): $0.021-0.023/GB
├─ Accessed weekly/monthly?
│   └─ Infrequent access (S3 Standard-IA, GCS Nearline): $0.0125/GB + retrieval fee
│       └─ Rule: minimum 30-day storage; retrieval cost must be < savings from storage
├─ Accessed quarterly/annually (backups, logs, compliance)?
│   └─ Cold tier (S3 Glacier Instant Retrieval, GCS Coldline, Azure Cool): $0.004-0.005/GB
│       └─ Rule: retrieval time < 5 minutes; cost is 75% cheaper than Standard
├─ Accessed rarely (< 1x/year, regulatory archive)?
│   └─ Deep archive (S3 Glacier Deep Archive, Azure Archive): $0.00099-0.002/GB
│       └─ Rule: retrieval time 12-48 hours; minimum 180-day storage
├─ Can we just delete it?
│   └─ YES → Set lifecycle policy: delete after X days
│       └─ Savings: 100% — always the best optimization
└─ Implementation: S3 lifecycle policies, GCS object lifecycle management, Azure Blob lifecycle
```

### 4. Data Transfer Cost Optimization
```
Service-to-service communication:
├─ Same availability zone?
│   └─ Free within AZ (AWS/GCP/Azure)
│       └─ Optimization: use AZ-aware service discovery; avoid cross-AZ load balancing for chatty services
├─ Cross-AZ within same region?
│   └─ $0.01/GB each direction (AWS/Azure), $0.01/GB (GCP)
│       └─ Optimization: consolidate services that talk frequently into same AZ when possible
├─ Cross-region?
│   └─ $0.02/GB (inter-region) — MOST EXPENSIVE PER GB
│       └─ Optimization: replicate data once, serve locally; use CloudFront/CDN to cache at edge
├─ Internet egress?
│   └─ $0.05-0.12/GB after free tier (AWS), $0.087-0.12/GB (Azure), $0.12/GB (GCP)
│       └─ Optimization: CDN (reduces origin egress), PrivateLink/Private Service Connect (keeps traffic on backbone)
├─ NAT Gateway?
│   └─ $0.045/GB + $0.045/hour per AZ
│       └─ Optimization: VPC endpoints for S3/DynamoDB (free, no NAT); consolidate to 1 NAT in hub VPC
└─ WARNING: Cross-region data transfer is the #1 hidden cost in multi-region architectures
```

### 5. Kubernetes Cost Optimization
```
Cluster cost attack surface:
├─ Node right-sizing?
│   ├─ Average node utilization < 40%? → Use smaller nodes or enable cluster autoscaler
│   │   └─ Rule: target 60-80% allocatable capacity utilization
│   └─ Too many node pools? → Consolidate; each pool adds management overhead
├─ Pod resource requests vs usage gap?
│   └─ requests > 2x actual usage? → Reduce requests (frees up bin-packing capacity)
│       └─ Tool: kubecost, Goldilocks, VPA recommender mode
├─ Idle workloads?
│   └─ Namespaces with 0 pods running? → Clean up; idle namespaces waste cluster overhead
│   └─ CronJobs running too frequently? → Reduce frequency or batch
├─ Spot nodes?
│   └─ 60-80% of worker nodes SHOULD be spot for stateless workloads
│       └─ Rule: production stateless services (web, API) on spot with PodDisruptionBudget; stateful on on-demand
├─ Over-provisioned cluster?
│   └─ Cluster autoscaler not scaling down? → Check PDBs preventing eviction; tune scale-down thresholds
└─ Implementation: kubecost for visibility → right-size requests → spot adoption → autoscaler tuning

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Inform — Visibility and Allocation
1. **Implement comprehensive tagging strategy**: mandatory tags (`Environment`, `Service`, `Team`, `CostCenter`, `Owner`) enforced via SCP/Azure Policy/Org Policy.
   - Output: Tagging policy document with enforcement mechanism; > 95% resource tag compliance within 60 days.
2. **Enable cost allocation**: map untagged costs to teams using proportional allocation rules.
   - Input: Resource inventory with tags, total cloud bill at account/project level.
   - Output: Cost-per-team, cost-per-service, cost-per-environment dashboards.
3. **Configure cost dashboards**: AWS Cost Explorer, Azure Cost Management, GCP Billing reports — shared with all engineering teams.
   - Output: Self-service dashboard with weekly cost trend, top-10 spenders, and budget vs. actual.
4. **Set budgets and alerts**: budgets per team/environment with alerts at 50%, 80%, 100%, 120%.
   - Output: Budget alerting pipeline; alerts routed to team channels (Slack, email, PagerDuty).
5. **Enable anomaly detection**: AWS Cost Anomaly Detection, Azure Anomaly Alerts, GCP Billing anomaly detection.
   - Output: Anomaly alerting with < 24-hour detection; > 90% of anomalies investigated within 48 hours.

### Phase 2 (~30 min): Optimize — Cost Reduction
1. **Right-size underutilized resources**: run Compute Optimizer / Recommender across all compute; implement changes.
   - Input: 30-day utilization data from cloud provider.
   - Output: Right-sizing recommendations list with estimated savings; implementation plan.
2. **Purchase commitment discounts**: RIs, Savings Plans, CUDs for baseline workloads (see Decision Tree #1).
   - Input: Steady-state workload inventory with historical utilization, growth forecast.
   - Output: Commitment purchase plan with ROI analysis (< 12-month payback); implemented purchases.
3. **Implement spot instance strategy**: identify stateless/fault-tolerant workloads; migrate to spot with fallback.
   - Input: Workload classification (stateless vs stateful, critical vs batch).
   - Output: Spot adoption plan; > 40% of non-production compute on spot; > 20% of production.
4. **Optimize storage tiers**: implement lifecycle policies (see Decision Tree #3).
   - Input: Storage inventory with access patterns (S3 Inventory, Azure Blob Inventory).
   - Output: Lifecycle policy configuration; estimated savings from tier transitions and deletions.
5. **Reduce data transfer costs**: optimize cross-AZ, cross-region, and egress traffic (see Decision Tree #4).
   - Input: VPC Flow Logs, data transfer billing reports.
   - Output: Data transfer optimization plan; CDN/PrivateLink/VPC endpoint implementation.
6. **Optimize Kubernetes costs**: right-size nodes, pods, and adopt spot (see Decision Tree #5).
   - Input: kubecost or equivalent cost allocation data.
   - Output: K8s optimization backlog ranked by savings; implemented changes.

### Phase 3 (~20 min): Operate — Governance and Continuous Improvement
1. **Establish cost governance**: define approval workflow for resources above cost threshold; auto-approve below.
   - Output: Cost governance policy; automated guardrails for high-cost resource provisioning.
2. **Define unit economics**: cost per customer, cost per transaction, cost per API call — tie cloud cost to business value.
   - Output: Unit cost dashboard; trends tracked monthly; anomalies trigger investigation.
3. **Run monthly FinOps review**: review spend vs. budget, optimization opportunities, commitment coverage gaps.
   - Attendees: FinOps lead, engineering leads, finance, CTO (quarterly).
   - Output: FinOps review report with action items and owner assignments.
4. **Automate waste elimination**: schedule idle resource shutdown (non-production nights/weekends); auto-delete unattached resources.
   - Output: Waste elimination automation with weekly savings report; < 5% idle resource waste.
5. **Manage cloud provider relationships**: negotiate EDP/private pricing, track credit consumption, renew commitments.
   - Output: Provider relationship dashboard; quarterly business review with providers.

### Phase 4 (~15 min): Carbon-Aware Optimization (GreenOps)
1. **Measure carbon footprint**: cloud provider carbon dashboards (AWS Customer Carbon Footprint Tool, Azure Emissions Impact, GCP Carbon Footprint).
   - Output: Carbon baseline; monthly carbon report alongside cost report.
2. **Shift workloads to low-carbon regions**: prioritize regions with low carbon intensity for new and relocatable workloads.
   - Output: Carbon-aware region selection policy; migration plan for eligible workloads.
3. **Optimize for carbon**: schedule batch workloads during low-carbon-intensity hours; right-size reduces carbon proportionally.
   - Output: Carbon optimization playbook integrated into standard FinOps practices.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
| Coordinate With | When | What to Share/Ask |
|---|---|---|
| **Cloud Architect** | Architecture decisions impacting cost, multi-cloud strategy, landing zone design | Cost implications of architecture choices, tagging requirements, commitment discount strategy |
| **DevOps Engineer** | Infrastructure provisioning, autoscaling configuration, resource lifecycle automation | Right-sizing recommendations, idle resource identification, cost guardrail implementation |
| **SRE** | Error budget integration, reliability vs. cost trade-offs, spot instance reliability | Spot adoption risk assessment, over-provisioning for reliability vs. cost efficiency balance |
| **Platform Engineer** | Golden path cost defaults, self-service cost visibility, tagging enforcement in templates | Cost-optimized defaults in templates, cost dashboard integration in portal, budget enforcement |
| **Backend/Frontend Developers** | Application-level cost optimization, caching strategies, data transfer patterns | Code-level cost drivers (N+1 queries, oversized payloads), cost awareness training |
| **Data Engineer** | Data storage optimization, pipeline cost management, query optimization | Storage tiering recommendations, data retention policies, costly query patterns |
| **Kubernetes Specialist** | Cluster cost optimization, node right-sizing, spot adoption, bin packing | K8s cost allocation, resource request optimization, autoscaler configuration |
| **Engineering Manager** | Team budget accountability, cost awareness culture, optimization prioritization | Team-level cost reports, optimization opportunity backlog, cost KPIs |
| **Finance/Business** | Budget planning, commitment purchases, cloud provider negotiations | Cost forecasts, commitment purchase ROI, provider discount programs, unit economics |
| **Security Engineer** | Security tooling costs, compliance-related infrastructure, logging costs | Security service cost optimization (GuardDuty, WAF, log storage tiering) |

### Escalation Path
```
Cost anomaly > 50% of monthly forecast? → FinOps Lead → Engineering Manager → CTO
Commitment purchase > $50K/year? → FinOps Lead → Finance → CTO
Cost optimization blocked by team resistance? → Engineering Manager → CTO
Budget overrun > 20% for 2 consecutive months? → FinOps Lead → Finance → CTO
Cloud provider negotiation needed? → FinOps Lead → Finance → CTO (exec sponsor)
```

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: No FinOps practice. Check cloud bill monthly. Set billing alerts for $X/month threshold. Use free tier aggressively. No tagging, no RIs, no optimization beyond "did my bill spike?"
- **Overkill**: Tagging strategy, RIs/Savings Plans, cost allocation to teams, unit economics, FinOps lifecycle, carbon tracking, budget governance.
- **Coordination**: You pay the bill. No coordination needed.
- **Cost**: $0 beyond cloud services. Focus on staying in free tier.
- **Transition trigger**: Monthly bill exceeds $500 consistently; first surprise bill > 2x expected.

### Small (2-10 people, 100-10K users)
- **What changes**: Basic tagging (`Environment`, `Service`). Budget alerts at 80% and 100%. Monthly bill review. RI/SP for steady production (1-year, no upfront). Delete unattached EBS/disks monthly. S3 lifecycle policies for logs (30-day → IA, 90-day → delete). No spot instances yet.
- **Overkill**: Unit economics, formal FinOps governance, anomaly detection automation, carbon footprint tracking, Kubernetes cost optimization (unless running K8s at scale), provider negotiation.
- **Coordination**: One person reviews bill monthly. Shared dashboard visible to team. Cost discussed in monthly engineering sync (5 min).
- **Cost**: $0-200/month (cloud cost tools free tier). 30 min/month bill review time.
- **Transition trigger**: Monthly bill > $2K; > 50 resources running; first RI/SP purchase opportunity > $5K/year.

### Medium (10-50 people, 10K-1M users)
- **What changes**: Dedicated FinOps function (part-time, 20-50% of one engineer). Full tagging strategy with SCP enforcement. Budgets per team with alerts. RI/SP coverage 60-80% of compute. Spot for non-production (40%+). Right-sizing program (quarterly reviews). S3 lifecycle policies across all buckets. Anomaly detection enabled. Cost dashboards per team. Kubernetes cost allocation via kubecost. Monthly FinOps review.
- **Overkill**: Dedicated FinOps team, unit economics (unless SaaS with per-customer cost sensitivity), carbon tracking, provider EDP negotiation, formal chargeback.
- **Coordination**: Monthly FinOps review with engineering leads. Cost dashboards self-service for teams. Quarterly optimization sprint. Budget overruns escalate to engineering manager.
- **Cost**: $30-70K/year (part-time FinOps engineer). kubecost or equivalent $2-5K/year. Commitment management overhead ~5 hours/month.
- **Transition trigger**: Monthly bill > $20K; > 5 teams with independent cloud usage; first compliance audit requiring cost allocation evidence.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated FinOps team (1-3 people). FinOps lifecycle fully implemented. Multi-cloud cost management platform (CloudHealth, Cloudability, Vantage). Unit economics per product/customer. Chargeback or showback with detailed allocation. Formal cost governance with approval workflows. EDP/private pricing negotiation. Carbon-aware optimization. Automated waste elimination (nightly non-prod shutdown). Continuous right-sizing automation. Cost optimization integrated into CI/CD (cost estimate on PR). FinOps certified practitioners.
- **What's full production**: Real-time cost anomaly detection with automated response. Cost-per-feature measurement. Cloud provider business reviews quarterly. FinOps council with cross-functional membership. Published cost optimization scorecards. Carbon reduction targets integrated with cost optimization.
- **Coordination**: Weekly FinOps team sync. Monthly FinOps council (FinOps, finance, engineering leads, CTO). Quarterly business review with cloud providers. Budget governance integrated with procurement.
- **Cost**: $400K-1.2M/year (1-3 FinOps engineers + tools). Multi-cloud cost platform $30-100K/year. Expected savings 20-40% of cloud spend (ROI positive at > $1M/year cloud spend).
- **Transition trigger**: Monthly bill > $100K; multi-cloud environment; > 100 engineers; public company financial controls; customer-facing SaaS with per-tenant cost sensitivity.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|---|---|---|
| `tagging-strategy` | Designing and enforcing a cost allocation tagging taxonomy | Tag taxonomy design, enforcement mechanisms (SCP, Policy), tag propagation, compliance tracking |
| `commitment-discount-management` | Purchasing and managing RIs, Savings Plans, CUDs across clouds | RI/SP strategy, purchase timing, exchange/modification, coverage tracking, ROI analysis |
| `right-sizing-automation` | Systematically reducing over-provisioned resources | Utilization analysis, recommendation engines, implementation workflows, performance validation |
| `spot-instance-strategy` | Adopting spot/preemptible instances for fault-tolerant workloads | Workload assessment, fallback patterns, interruption handling, spot diversification |
| `storage-lifecycle-optimization` | Implementing tiering and deletion policies for object and block storage | Access pattern analysis, lifecycle policy design, retrieval cost modeling, compliance retention |
| `kubernetes-cost-optimization` | Optimizing Kubernetes clusters for cost efficiency | Node right-sizing, pod resource tuning, spot adoption, bin packing, idle workload cleanup |
| `data-transfer-optimization` | Reducing cross-AZ, cross-region, and internet egress costs | Traffic analysis, CDN integration, PrivateLink/VPC endpoint, AZ-aware architecture |
| `unit-economics` | Tying cloud cost to business value (cost per customer, per transaction) | Metric definition, data pipeline, dashboard design, anomaly detection, pricing model feedback |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Tag or die**: untagged resources are invisible costs. Enforce tags via policy; auto-shutdown resources that remain untagged after 24 hours. > 95% compliance is non-negotiable.
- **RI/SP coverage targets 60-80%, not 100%**: 100% coverage means you're committed for every workload — no flexibility. Keep 20-40% on-demand for variable workloads and new services.
- **Right-size before you commit**: never buy a 3-year RI for an instance that's 80% idle. Right-size first, then commit to the optimized size.
- **Spot is free money (with engineering investment)**: spot instances save 60-90% but require interruption handling. Invest in spot-compatible architecture once; save forever.
- **Storage has infinite gravity**: data grows, access patterns decay, but storage costs compound. Lifecycle policies are the highest-ROI, lowest-effort optimization.
- **Data transfer costs hide in plain sight**: cross-AZ traffic is hard to see but easy to accumulate. Use AZ-aware service discovery and VPC endpoints to keep traffic local.
- **Cost is a feature**: every PR that adds a resource should estimate its monthly cost. CI/CD integration (Infracost, Terraform cost estimation) makes cost visible at design time.
- **Showback before chargeback**: start by showing teams their costs without charging them. Build cost awareness before adding financial accountability. Chargeback too early breeds resentment.
- **FinOps is cultural, not a tool**: tools provide visibility; the culture of cost awareness drives savings. Engineers who see their costs optimize them; engineers who don't, don't.
- **GreenOps is the next frontier**: carbon-aware scheduling and region selection often align with cost optimization (low-carbon regions tend to be cheaper). Track carbon alongside cost.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Tagging strategy documented with mandatory tags (`Environment`, `Service`, `Team`, `CostCenter`, `Owner`)
- [ ] **[S2]**  Tag enforcement in place via SCP, Azure Policy, or Org Policy; > 95% resource tag compliance
- [ ] **[S3]**  Budget alerts configured per team/environment at 50%, 80%, 100%, 120% thresholds
- [ ] **[S4]**  Cost anomaly detection enabled and alerting to team communication channels
- [ ] **[S5]**  Cost dashboards available to all engineering teams (self-service, updated daily)
- [ ] **[S6]**  RI/SP coverage at 60-80% for steady-state compute; review coverage monthly
- [ ] **[S7]**  Right-sizing review completed within last 90 days; recommendations implemented
- [ ] **[S8]**  Spot instances adopted for > 40% non-production and > 20% production stateless workloads
- [ ] **[S9]**  S3/Azure Blob/GCS lifecycle policies applied to all buckets; deletion policies for logs/temp data
- [ ] **[S10]**  Data transfer optimization: VPC endpoints for S3/DynamoDB, CDN for egress-heavy endpoints
- [ ] **[S11]**  Kubernetes cost allocation implemented (kubecost or equivalent); resource requests right-sized
- [ ] **[S12]**  Idle resource cleanup automated: non-production shutdown nights/weekends; unattached resources deleted
- [ ] **[S13]**  Monthly FinOps review established with action items and ownership
- [ ] **[S14]**  Unit economics dashboard for at least top-3 products/customer segments
- [ ] **[S15]**  Carbon footprint baseline measured; reduction targets set

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [FinOps Foundation](https://www.finops.org/) — FinOps Framework, lifecycle, maturity model, certification
- [Well-Architected Cost Optimization Pillar (AWS)](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/) — AWS cost optimization best practices
- [Google Cloud FinOps](https://cloud.google.com/finops/) — GCP cost optimization guides and best practices
- [Microsoft Azure Well-Architected — Cost Optimization](https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/) — Azure cost optimization framework
- [kubecost](https://www.kubecost.com/) — Kubernetes cost monitoring and optimization
- [Infracost](https://www.infracost.io/) — Infrastructure cost estimates in CI/CD
- [Vantage](https://www.vantage.sh/) — Multi-cloud cost management platform
- [Cloud Carbon Footprint](https://www.cloudcarbonfootprint.org/) — Open-source carbon measurement for cloud
- Internal: [../../domain/references/finops-playbook.md](../../domain/references/) — Detailed cost optimization playbooks per cloud provider
