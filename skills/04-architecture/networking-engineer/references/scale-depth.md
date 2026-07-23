# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: Default VPC or a single custom VPC. 2-3 subnets. Security groups: allow-list for your IP. No NAT gateway (use public subnets with careful security groups). DNS: Route 53 public zone or Cloudflare. CDN: Cloudflare free tier. No service mesh, no Transit Gateway, no VPN, no Direct Connect. Network changes: console or simple Terraform.
- **What's overkill**: Multi-VPC, Transit Gateway, NACLs (security groups are enough), WAF, Direct Connect, service mesh, VPC endpoints, flow logs analysis, network automation beyond basic IaC.
- **Coordination**: You manage the network as part of full-stack responsibility. Document IPs in a README.
- **Cost**: $0-30/mo (Route 53 + data transfer at minimal scale).
- **Transition trigger**: Second environment needed (staging/prod split) OR first compliance requirement (SOC2).

### Small Team (2-10 people, 100-10K users)
- **What changes**: Separate VPCs per environment. Transit Gateway connecting dev/staging/prod (optional — VPC peering may suffice). Public/private subnets. NAT Gateway in each AZ for high availability. Security groups + NACLs. WAF on public endpoints. DNS: split-horizon (public + private zones). CDN: paid tier. VPN for admin access (not Direct Connect yet). Flow logs: enabled, sampled. IaC: all network in Terraform, CI/CD pipeline. Monitoring: basic CloudWatch alarms.
- **What's overkill**: Multi-region, Direct Connect, service mesh, advanced WAF custom rules, dedicated Network account, IPAM, multi-cloud networking, SD-WAN.
- **Coordination**: Network changes reviewed in PR by another engineer. Quarterly network review. On-call rotation for network alerts.
- **Cost**: $100-500/mo (NAT gateways + data transfer + Route 53 + WAF + CDN).
- **Transition trigger**: Multi-region deployment OR hybrid cloud/on-prem connectivity needed OR 10K+ users.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Hub-and-spoke with Transit Gateway. Dedicated Network account (AWS Organizations). Multi-region with inter-region TGW peering. Direct Connect or high-throughput VPN to on-prem. Service mesh (Istio/Linkerd) for east-west traffic with mTLS. WAF with custom rules and rate limiting. Advanced CDN: Origin Shield, Lambda@Edge/CloudFront Functions for header manipulation. DNS: Route 53 Resolver for hybrid DNS. VPC endpoints for all AWS services (reduce NAT gateway costs). Network automation: Terraform modules, CI/CD with plan approval. Flow logs: full resolution, Athena queries. Dedicated network monitoring dashboards.
- **What's overkill**: Multi-cloud SD-WAN, dedicated Network Engineering team, active-active multi-region networking, full Zero Trust architecture (start with service mesh mTLS), network microsegmentation beyond service-level isolation.
- **Coordination**: Monthly network architecture review. Dedicated network engineer (0.5-1 FTE). Network change management process. Bi-weekly security-network sync.
- **Cost**: $2K-10K/mo (NAT gateways + data transfer + Direct Connect + service mesh infra + monitoring).
- **Transition trigger**: Multi-cloud deployment OR 50+ services requiring east-west traffic control OR compliance requires full network segmentation.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Full multi-cloud networking (AWS + Azure + GCP) with SD-WAN or cloud-native interconnects. Dedicated network engineering team (2-5 engineers). Zero Trust Network Access (ZTNA) — no implicit trust, every connection authenticated and authorized. Advanced service mesh: ambient mesh (Istio ambient, Cilium/eBPF) for sidecar-free mTLS. Global load balancing with latency-based routing and geo-steering. IPv6 migration strategy (dual-stack or IPv6-only for new services). Network automation: self-service network provisioning via internal developer platform (IDP). Network cost optimization program: rightsizing, VPC endpoint expansion, inter-AZ traffic analysis. DDoS: Shield Advanced with proactive engagement. WAF: advanced custom rules, bot control, fraud prevention. Network observability: packet capture on demand, VPC Reachability Analyzer, automated compliance audits.
- **What's full production**: Network operations center (NOC). 24/7 network on-call. Network chaos engineering. Automated network compliance enforcement (no manual changes). Multi-region active-active networking with latency SLAs. Network capacity planning with 3-year forecast. M&A network integration playbook.
- **Coordination**: Weekly network operations meeting. Monthly architecture review. Quarterly network strategy with CTO/Cloud Architect. Network change advisory board for high-risk changes.
- **Cost**: $20K-100K+/mo (multi-cloud networking, Direct Connect/ExpressRoute ports, data transfer at scale, network engineering team, tooling).
- **Transition trigger**: Multi-cloud with >$1M/mo cloud spend OR 500K+ users globally OR regulatory requirement for air-gapped or data-residency networking.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | cloud-architect | Region topology, service placement, compliance boundaries |
| **This** | networking-engineer | VPC/subnet design, DNS, load balancers, firewall rules, connectivity topology |
| **After** | devops-engineer | Implements Terraform/CloudFormation from network design, configures CI/CD network access |

Common chains:
- **Cloud landing zone**: cloud-architect → networking-engineer → devops-engineer — Cloud defines regions/accounts, networking designs connectivity, DevOps codifies it
- **Security-first network**: system-architect → networking-engineer → security-engineer — Architecture defines trust boundaries, networking implements segmentation, security audits and hardens
