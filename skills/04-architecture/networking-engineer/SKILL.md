---
name: networking-engineer
description: >
  Use when designing cloud network architectures, planning subnet and CIDR layouts,
  architecting DNS and CDN, configuring load balancers, or implementing network
  security controls. Handles VPC/VNet/VCN design, hybrid and multi-cloud networking
  (VPN, Direct Connect, ExpressRoute), BGP routing, service mesh architecture, API
  gateway and ingress design, and Zero Trust network access. Do NOT use for
  on-premises-only networking, physical cabling, or ISP procurement.
license: MIT
tags:
- networking
- vpc
- dns
- load-balancing
- cdn
- firewall
- vpn
- zero-trust
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
    - system-architect
    - cloud-architect
    - security-engineer
  feeds_into:
    - devops-engineer
    - cloud-architect
    - site-reliability-engineer
    - docker-kubernetes
---
# Networking Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

## Core Workflow
<!-- STANDARD: 3min -->

**Phase 1: Discovery & Requirements (15% of effort)**
Inventory the existing topology — map every subnet, ASN, VPC, firewall rule, and peering link. Use `nmap`, `traceroute`, and cloud provider APIs (AWS VPC/Transit Gateway, GCP VPC Network Peering, Azure Virtual Network). Document: CIDR ranges (identify overlaps), connectivity paths (direct peering, VPN, SD-WAN), NAT/bastion topology, DNS resolution paths (split-horizon?), and where TLS terminates. Output: network topology diagram (ASCII or Cloudcraft) + spreadsheet of every subnet with CIDR, route table ID, NACL reference, and connectivity matrix.

**Phase 2: Architecture Design (25% of effort)**
Design the target topology addressing all requirements. Select IP addressing plan (RFC 1918 private — 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 — avoid overlaps across regions/accounts). Design: VPC/VNet network segmentation (public/private/intra tiers), transit routing (Transit Gateway/hub-spoke vs mesh peering), NAT strategy (centralized egress vs per-VPC — cost/capacity trade-off), DNS resolution architecture (Route 53 Resolver/Hybrid DNS/conditional forwarding), and BGP/static routing for hybrid connectivity. Calculate total IP capacity needed per subnet with 2x headroom. Flag: any 0.0.0.0/0 routes wider than necessary.

**Phase 3: Security & Compliance Integration (35% of effort)**
Apply zero-trust networking principles: no implicit trust based on network location. Layer: security groups (stateful, instance-level) + NACLs (stateless, subnet-level) + AWS Network Firewall/Cloud NGFW (stateful, VPC-level) + WAF (L7, edge). Implement: flow logs on every VPC/subnet/ENI (VPC Flow Logs to S3 + Athena for querying), private connectivity (PrivateLink/VPC Endpoints — no traffic traverses public internet), east-west traffic inspection, egress filtering (allow-list outbound destinations), DDoS protection (Shield Advanced for critical workloads). Run `nmap` from inside each subnet to verify actual reachability matches intended reachability.

**Phase 4: Validation & Documentation (25% of effort)**
Run reachability tests: from every tier, verify connectivity to every dependency. Test failure modes: what happens when AZ-a goes down? when Transit Gateway attachments fail? when VPN tunnel drops? Document: runbook for each failure scenario (<2 page turns to execute), network topology diagram updated to as-built, CIDR allocation register with owner/expiry, firewall rule justification spreadsheet (every rule has business justification + ticket reference). Validate: `route` table audit passes (no 0.0.0.0/0 except through approved egress), flow logs show no unexpected traffic, all public-facing endpoints go through WAF/CDN.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "I'll just open 0.0.0.0/0 temporarily for debugging — I'll close it in 5 minutes." | Port 22 open to the world attracts brute-force attacks within 90 seconds. That "temporary" rule is still there 6 months later when auditors find it. Console click-ops leave no audit trail and can't be reproduced via IaC. Cost of a single forgotten 0.0.0.0/0 rule: $50K-$500K in breach scope expansion from unrestricted lateral movement. |
| "VPC Flow Logs are nice-to-have — we'll enable them when we have time." | When partners report connectivity issues, you have zero data to diagnose. You're guessing based on config, not evidence. Every minute of "figuring out how it's connected" during an outage is pure waste. Cost of no flow logs: $50K-$300K per extended outage from undiagnosable network issues. |
| "CIDR-based security group rules are fine — our IPs never change." | Subnets get renumbered. Services migrate. Auto-scaling replaces instances. CIDR rules break silently — traffic drops, nobody knows why, hours of debugging ensue. Security group references survive every topology change. Cost of CIDR rules for inter-service traffic: $15K-$50K in silent breakage incidents per year. |
| "We'll add multi-region failover next quarter — single region is fine for now." | A regional fiber cut or cloud control-plane outage takes down every customer globally for 4-8 hours with no fallback. Mid-market SaaS loses $100K-$500K/hour in revenue during a regional outage. Cost of single-region architecture: $100K-$500K/hour during the inevitable regional outage, plus SLA penalty payouts. |
| "Cloud egress costs? Those line items are negligible." | A data-intensive pipeline moving 50TB/month cross-AZ generates $1,000-$2,000/month in cross-AZ data transfer that nobody budgeted for. Microservices making inter-AZ calls multiply this by service count. Cost of ignoring egress: $5K-$50K/month in unexpected cloud charges — the surprise that turns into a CFO conversation. |

Design, deploy, and operate cloud-native and hybrid network architectures. This skill covers the full stack: from IP address planning and subnet design through DNS, load balancing, CDN, firewalls, VPNs, and service mesh. Every design considers cost, latency, security, and operational complexity. The goal is a network that developers never think about because it just works — secure by default, fast everywhere, and cheap at scale.

## Route the Request
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.tf", "aws_vpc\|google_compute_network\|azurerm_virtual_network")` OR `file_contains("*.yaml", "VPC\|VirtualNetwork\|vpc")` | IaC-defined network topology exists. Jump to **Production Checklist** — audit existing configuration. |
| A2 | `file_contains("*", "DNS\|Route.53\|Cloud.DNS\|zone\|CNAME\|A.record\|NS.record")` AND `file_contains("*", "split.horizon\|private.zone\|public.zone\|resolver")` | DNS architecture concerns. Jump to **Core Workflow** — Phase 2 (DNS Architecture). |
| A3 | `file_contains("*", "load.balancer\|ALB\|NLB\|ELB\|reverse.proxy\|haproxy\|nginx.*upstream")` | Load balancing concerns. Jump to **Core Workflow** — Phase 3 (Load Balancing). |
| A4 | `file_contains("*", "CDN\|CloudFront\|Cloud.CDN\|Fastly\|Akamai\|edge.cache\|cache.policy")` | CDN concerns. Jump to **Core Workflow** — Phase 4 (CDN Strategy). |
| A5 | `file_contains("*", "VPN\|Direct.Connect\|ExpressRoute\|interconnect\|BGP\|IPsec\|tunnel")` | Hybrid/multi-cloud connectivity. Jump to **Decision Trees** — Hybrid Cloud Connectivity. |
| A6 | `file_contains("*", "service.mesh\|Istio\|Linkerd\|Cilium\|Consul.Connect\|sidecar\|mTLS")` | Service mesh concerns. Jump to **Decision Trees** — Service Mesh (Sidecar vs Ambient vs eBPF). |
| A7 | `file_contains("*", "0\.0\.0\.0/0\|security.group.*open\|ingress.*0\.0\.0\.0\|allow.*all\|permissive")` | Potentially insecure network rules. Jump to **Anti-Patterns** — audit security group rules immediately. |
| A8 | `file_contains("*", "zero.trust\|ZTNA\|BeyondCorp\|identity.aware\|mTLS.*everywhere\|SPIFFE")` | Zero-trust architecture. Jump to **Decision Trees** — Zero Trust Network Architecture. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a new VPC/subnet topology → Start at "Decision Trees > VPC/Block Design"
├── Configure DNS (public/private zones, split-horizon) → Jump to "Core Workflow > Phase 2 (DNS Architecture)"
├── Set up load balancers (ALB/NLB) with SSL → Go to "Core Workflow > Phase 3 (Load Balancing)"
├── Configure CDN with edge caching → Jump to "Core Workflow > Phase 4 (CDN Strategy)"
├── Design firewall rules and security groups → Go to "Best Practices > Network Security" then "Core Workflow > Phase 5"
├── Set up hybrid cloud connectivity (VPN/Direct Connect) → Jump to "Decision Trees > Hybrid Cloud Connectivity"
├── Deploy a service mesh (Istio/Linkerd/Cilium) → Go to "Decision Trees > Service Mesh"
├── Design zero-trust architecture → Jump to "Decision Trees > Zero Trust Network Architecture"
├── Need overall system architecture first → Invoke system-architect skill instead
├── Need cloud infrastructure design → Invoke cloud-architect skill instead
├── Need security posture review → Invoke security-engineer skill instead
├── Need DevOps pipeline integration → Invoke devops-engineer skill instead
├── Need container networking and service mesh → Invoke docker-kubernetes skill instead
├── Need site reliability for network → Invoke site-reliability-engineer skill instead
└── Don't know where to start? → Describe your infrastructure and requirements and I'll route you

```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to open `0.0.0.0/0` to any port without explicit justification and a timeline to tighten.** Every `0.0.0.0/0` ingress rule is a bet that no attacker will find that port before you close it. Port 22 (SSH) open to the world attracts brute-force attacks within minutes. Port 3389 (RDP) is a ransomware entry vector. Use SSM Session Manager or a bastion with security group references instead. | Trigger: proposing a security group, firewall rule, or NACL rule with source `0.0.0.0/0` (or `::/0`) for any port other than 80/443 on a public load balancer or CDN | STOP. Require: "Every `0.0.0.0/0` rule must have: (1) explicit justification documented in the rule description, (2) a planned tightening date (within 30 days), (3) alternatives evaluated (security group reference, SSM, VPN). Open `0.0.0.0/0` on SSH/RDP/database ports is a REFUSE — use SSM Session Manager or bastion with `sg-bastion` reference." |
| **R2** | **DETECT and WARN about single-AZ NAT Gateway deployments.** A single NAT Gateway is a single point of failure — when its AZ goes down, all private subnets in all AZs lose outbound internet. It also doubles inter-AZ data transfer costs for private subnets in different AZs. | Trigger: network topology has only 1 NAT Gateway while having subnets in 2+ AZs; or Terraform `aws_nat_gateway` count is 1 with `length(var.availability_zones) > 1` | WARN. Fix: "Deploy one NAT Gateway per AZ. Each private route table routes `0.0.0.0/0` to the NAT Gateway in its own AZ. Cost: $32/mo per NAT GW — cheaper than the cross-AZ data transfer and outage cost from a single NAT GW." |
| **R3** | **REFUSE to use CIDR-based security group rules when security group references are available.** `sg-database` referenced from `sg-backend` is self-documenting, survives instance/IP replacement, and eliminates stale CIDR rules. CIDR rules break silently when subnets are renumbered or services migrate. | Trigger: security group rule uses `cidr_blocks = ["10.0.1.0/24"]` for traffic between services in the same VPC, instead of `source_security_group_id = aws_security_group.backend.id` | STOP. Rewrite: "Use `source_security_group_id = [sg-backend]` instead of CIDR `10.0.1.0/24`. Security group references survive instance replacement, subnet renumbering, and auto-scaling events. CIDR-based rules for inter-service traffic become stale within weeks." |
| **R4** | **REFUSE to design a network without VPC Flow Logs enabled from day one.** Without flow logs, you have zero visibility into dropped traffic, rejected connections, and anomalous traffic patterns. When partners report connectivity issues, you have no data to diagnose — you're guessing based on config, not evidence. | Trigger: network design or Terraform config provisions VPCs/subnets/security groups without `aws_flow_log` or equivalent resource, or Flow Logs are mentioned as "future work" | STOP. Insert: "Add `aws_flow_log` for ALL VPCs: publish to S3 (long-term) + CloudWatch Logs (real-time queries). Enable on VPC creation, not as a post-deployment task. Query example: `SELECT * FROM vpc_flow_logs WHERE action = 'REJECT' AND dstport = 443 LIMIT 100` — this finds the dropped traffic your partner is complaining about." |
| **R5** | **DETECT and WARN about manual security group changes in the console.** Console click-ops leave no audit trail, can't be reproduced via IaC, and inevitably leave temporary rules permanently open. The console should be read-only for network config — all changes through Terraform/Pulumi/CDK with CI/CD plan review. | Trigger: mention of "AWS Console", "click-ops", "manual rule", "temporarily open", or "quick console change" in the context of modifying security groups, NACLs, or WAF rules | WARN. Policy: "All network changes go through IaC (Terraform/Pulumi/CDK) with `terraform plan` review in CI/CD. If a P0 incident requires a console change: document it in the incident channel, file a ticket to backfill into IaC within 24 hours, and add a `terraform import` task. Console changes without IaC backfill = configuration drift = future incident." |
| **R6** | **STOP and WARN about deploying a service mesh without mTLS in STRICT mode and authorization policies.** A service mesh that only routes is overhead with zero security benefit. Without mTLS enforcement, any pod can call any other pod — the mesh is just expensive proxying. | Trigger: deploying, installing, or configuring Istio/Linkerd/Consul Connect with `permissive` mTLS mode, or mesh deployed without `AuthorizationPolicy` resources defined | STOP. Configure: "(1) PeerAuthentication: mTLS STRICT (not permissive), (2) AuthorizationPolicy: ALLOW only from known service accounts, (3) `DENY` all by default, explicitly ALLOW known paths. mTLS in permissive mode is security theater — it encrypts nothing if the other side doesn't require it." |
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

Networking is not about connecting things — it's about **understanding that the network is always the bottleneck until proven otherwise, and designing systems that fail gracefully when that bottleneck manifests**. The best network designs are so boring nobody thinks about them until they're needed.

### Mental Models

| Model | Description |
|---|---|
| **The network is guilty until proven innocent** | When an application is slow, the network is the default suspect. Prove it's not the network before investigating elsewhere. Latency, packet loss, and DNS failures cause more incidents than application bugs. |
| **Every packet tells a story** | Packet-level analysis (tcpdump, Wireshark, flow logs) reveals what actually happened vs. what you think happened. Learn to read packets — they don't lie. |
| **Complexity is the enemy of reliability** | Every additional hop, routing rule, and security policy is a failure mode. The simplest network that meets requirements is the best network. |
| **Default-deny, explicitly allow** | Start with everything blocked. Open only what's needed, to exactly what needs it. Review rules monthly. A rule you haven't reviewed in 6 months is a security gap you've forgotten about. |

### Cognitive Biases in Network Design

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Over-provisioning as security blanket** | Adding more bandwidth, more instances, more complexity instead of diagnosing the actual bottleneck | Find the root cause before scaling. Bandwidth masks problems; it doesn't solve them. |
| **Familiarity bias** | Designing the network you know (e.g., on-prem patterns in cloud) instead of the network that fits | Start from cloud-native primitives. Don't replicate your data center in the cloud. |
| **False sense of security** | "It's in a private subnet behind a security group, so it's safe" — ignoring application-layer attacks | Defense in depth: security groups + NACLs + WAF + application auth. Layers, not silver bullets. |
| **Recency bias in routing** | Over-optimizing for the last failure mode while creating new ones | Design for failure modes you haven't seen yet. Every routing decision should have a "what if this fails?" answer. |

### What Masters Know That Others Don't

- **DNS is always the problem.** When everything looks correct but nothing works, check DNS. Split-horizon, TTL mismatches, cached negative responses, missing PTR records — DNS is the silent killer of network troubleshooting.
- **The best network designs are boring.** If your network topology is exciting, you've over-engineered it. A simple hub-and-spoke with well-defined security groups and transit gateway should feel boring. Boredom = reliability.
- **Latency budgets are design constraints.** A 200ms budget for an API call means: 50ms for TLS handshake, 30ms for load balancer, 50ms for application, 30ms for database, 40ms margin. Design to the budget, not to "as fast as possible."
- **Network observability is underinvested.** Most teams have great application monitoring and poor network visibility. When the app is slow, they can't tell if it's the network because they never instrumented it. VPC flow logs + synthetic probes = non-negotiable.

## Operating at Different Levels
<!-- STANDARD: 3min -->

Network engineering scales from single VPC design to global multi-cloud network architecture.

| Level | Networking Engineer Output Characteristics |
|---|---|
| **L1 — Apprentice** | Configures subnets and security groups from established patterns. Learns CIDR, routing, and DNS fundamentals. |
| **L2 — Practitioner** | Designs VPC/VNet for a service. Configures load balancers, DNS, and network security independently. |
| **L3 — Senior** | Designs multi-region network architecture. Transit gateway, hybrid cloud (VPN/Direct Connect), WAF/DDoS strategy. Trade-off analysis included. |
| **L4 — Staff/Principal** | Sets network architecture standards for the org. Global network topology, multi-cloud networking strategy. "This is our network reference architecture." |
| **L5 — Industry-level** | Creates networking patterns and architectures adopted across the industry. |

**Usage**: Say "as an L3 networking engineer, design the VPC architecture for..." Default: **L3** (multi-region design, independent architectural decisions).

## When to Use
<!-- STANDARD: 3min -->

- You are designing a new VPC/VNet with subnets, CIDR ranges, and routing tables from scratch
- You need to connect multiple VPCs across accounts or regions via peering or transit gateway
- You are planning DNS architecture (public/private zones, split-horizon, multi-cloud resolution)
- You need to set up load balancers (ALB/NLB/GLB) with health checks and SSL termination
- You are configuring network security layers — security groups, NACLs, WAF rules, DDoS protection
- You are establishing hybrid connectivity between on-prem data centers and cloud (VPN, Direct Connect, ExpressRoute)
- You need to deploy a service mesh (Istio, Linkerd, Cilium) with mTLS and traffic policies
- You are designing a CDN strategy with edge caching, origin shield, and DDoS mitigation

## Decision Trees
<!-- STANDARD: 3min -->

**(QUICK)**

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Decision Tree 1: VPC Topology Design

        ┌── INPUT: How many regions, environments, and services?
        │
   ┌────┴──────────────────────────┐
   │                               │
   ▼                               ▼
Single region, < 10 svcs    Multi-region or > 10 services
   │                               │
   ▼                               ▼
Single VPC, public +         ┌────┴────────────┐
private subnets              │                 │
                             ▼                 ▼
                       < 3 accounts,    3+ accounts, shared
                       simple routing   services across teams
                             │                 │
                             ▼                 ▼
                       Multi-VPC peering   Hub-and-spoke with
                       mesh (VPC peering   Transit Gateway +
                       per connection)     centralized egress

### Decision Tree 2: CIDR Allocation Strategy

        ┌── INPUT: Expected scale over 3 years?
        │
   ┌────┴──────────────┐
   │                   │
   ▼                   ▼
< 5 VPCs total     5+ VPCs, multi-region, hybrid cloud
   │                   │
   ▼                   ▼
Use 10.0.0.0/16     ┌── Allocate master supernet (e.g., 10.0.0.0/12)
per VPC, simple     │
allocation          ├── Carve /14 per region
                    ├── Carve /16 per environment per region
                    ├── Carve /18 or /20 per AZ per subnet type
                    └── Reserve 20% for future growth
                             │
                             ▼
                    Must NOT overlap with: on-prem, partner
                    networks, any future cloud connection.
                    Use IPAM for tracking.

### Decision Tree 3: DNS Architecture

        ┌── INPUT: Do you have on-prem or cross-cloud DNS needs?
        │
   ┌────┴──────────────────────┐
   │                           │
   ▼                           ▼
Cloud-only, single        Hybrid (on-prem + cloud)
provider                       │
   │                     ┌─────┴──────┐
   ▼                     │            │
Public hosted zone       ▼            ▼
for customer-facing   Outbound only  Bidirectional
records + private          │            │
hosted zone for            ▼            ▼
internal discovery    Route 53/      Route 53 Resolver
                      Azure DNS      endpoints + forwarding
                      private zone   rules. Conditional
                      - forwarding   forwarding for
                      rule to on-prem on-prem domains.
                                        │
                                        ▼
                                   Private hosted zone
                                   (internal.example.com)
                                   for service discovery.

### Decision Tree 4: Load Balancer Selection

        ┌── INPUT: What protocol and routing needs?
        │
   ┌────┴────────────┐
   │                 │
   ▼                 ▼
HTTP/HTTPS         Non-HTTP (TCP, UDP, TLS)
traffic            or static IP required
   │                 │
   ▼                 ▼
ALB (L7 routing,   NLB (low latency,
SSL termination,   static IP, TLS
host/path routing, passthrough)
WAF integration)        │
   │               ┌────┴──────────┐
   ▼               │               │
Need OIDC/JWT     ▼               ▼
auth at LB?    Need 3rd-party  Need Zonal
   │           virtual appliance? failover?
   ▼               │               │
ALB + Cognito/  GWLB (GENEVE     ALB + cross-zone
Okta/OAuth2     encapsulation,   load balancing
                transparent      enabled
                appliance insert)

**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Network Design & IP Planning
<!-- DEEP: 10+min -->

1. **Define network topology**: Choose single-VPC vs multi-VPC vs hub-and-spoke (Transit Gateway).
   Document in a network topology diagram. Include all: regions, VPCs, subnets, NAT gateways,
   internet gateways, VPC endpoints, Transit Gateways, VPN/Direct Connect connections.
   - **Input**: Application architecture, compliance requirements, expected traffic volume.
   - **Output**: Network topology diagram (draw.io/Lucidchart). CIDR allocation spreadsheet.

2. **Plan CIDR ranges**: Use RFC 1918 private ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).
   Allocate a master supernet (e.g., 10.0.0.0/12). Carve into per-region /14 blocks.
   Carve into per-environment /16 blocks. Carve into per-AZ /18 or /20 blocks for subnets.
   Never use ranges that overlap with on-prem, partner networks, or any cloud you might
   connect to in the future.
   - **Input**: Number of regions, environments, AZs, and expected growth (3-year horizon).
   - **Output**: CIDR allocation plan. IPAM (IP Address Manager) configured if available.

3. **Design subnet architecture**: Per VPC, create subnets in each AZ:
   - **Public subnets**: Route to Internet Gateway. For load balancers, bastions, NAT gateways.
   - **Private subnets**: Route to NAT Gateway for egress. For compute (EC2, ECS, EKS nodes).
   - **Isolated subnets**: No internet route — not even NAT. For databases, caches, secrets stores.
   - **Egress-only subnets**: IPv6-only outbound via Egress-Only Internet Gateway.
   - **Input**: Service placement plan, internet access requirements.
   - **Output**: Subnet map per VPC per AZ. Route tables configured.

Complete when:
- Network topology diagram (draw.io/Lucidchart) with all regions, VPCs, subnets, NAT/Internet gateways, endpoints, and TGW/VPN connections exported
- CIDR allocation spreadsheet with master supernet, per-region, per-environment, and per-AZ blocks documented
- Subnet architecture (public/private/isolated/egress-only) mapped with route tables per VPC per AZ

### Phase 2 (~30 min): DNS & Traffic Management

1. **Design DNS architecture**: Create public hosted zone (`example.com`) for customer-facing records.
   Private hosted zone (`internal.example.com`) for service discovery. Set up DNS forwarding rules
   for hybrid (on-prem ↔ cloud resolution via Route 53 Resolver / Azure DNS Private Resolver).
   - **Input**: Service catalog, public endpoints, internal dependencies.
   - **Output**: DNS zone files. Resolution path documented. TTL strategy defined.

2. **Configure load balancers**: Deploy ALB for HTTP/S (L7 routing, SSL termination).
   NLB for non-HTTP traffic. Configure health checks, target groups, and auto-scaling policies.
   Set up access logs to S3/Blob Storage for troubleshooting.
   - **Input**: Service endpoints, protocol requirements, SSL certificates.
   - **Output**: Load balancers deployed. Health checks passing. Access logs enabled.

3. **Set up CDN and edge caching**: CloudFront (AWS), Cloud CDN (GCP), Azure Front Door.
   Origin: ALB or S3/Blob Storage. Cache behaviors: cache static assets (images, CSS, JS)
   for 1 year (version

Complete when:
- DNS architecture designed: public and private hosted zones, forwarding rules for hybrid resolution, TTL strategy documented
- Load balancers configured: ALB for HTTP/S with SSL termination, NLB for non-HTTP, health checks passing, access logs enabled
- CDN configured with origin, cache behaviors, and edge caching policies for static assets

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Best Practices
<!-- STANDARD: 3min -->

1. **Plan CIDR ranges for 3-year growth.** Allocate contiguous supernets per region (`/12`), carve `/16` per VPC, `/18` or `/20` per AZ tier. Never use `/28` subnets — 14 usable IPs vanish when ALB, RDS, and Lambda ENIs claim addresses. CIDR planning is the one network decision you cannot undo.

2. **Default to internal load balancers.** Consumer on the public internet is the ONLY reason for an internet-facing LB. Every public LB is a potential entry point. For public-facing services, layer: WAF → CDN → LB with security groups scoped to CDN prefix lists — never `0.0.0.0/0`.

3. **Set DNS TTL ≤ 60 seconds for failover-capable records.** A 300s TTL means 5 minutes of stale routing during regional failover. Use latency-based or geo-steering routing policies. Split-horizon DNS for internal service discovery — internal services resolve private IPs.

4. **Use BGP dynamic routing for all hybrid connectivity.** Redundant VPN tunnels (2 minimum) with BGP keepalive 10s, hold time 30s. Static routing fails silently — BGP detects dead tunnels in 30 seconds vs. manual 3-hour recovery during an outage.

5. **Implement micro-segmentation with security groups per workload tier.** Never `0.0.0.0/0` in security group rules except for public-facing CDN/WAF managed prefix lists. Flat networks enable lateral movement — a compromised web server can scan the entire VPC.

6. **Deploy VPC flow logs and DNS query logs before going live.** Network observability cannot be retrofitted during an incident. Flow logs + synthetic probes from multiple regions = non-negotiable. If you can't see the packets, you can't debug the problem.

7. **Co-locate services with heavy communication in the same AZ.** Cross-AZ data transfer at $0.01-0.02/GB accumulates silently. A data pipeline moving 50TB/month cross-AZ costs $1,000-2,000/month that nobody budgeted for. AZ affinity saves 30-50% on inter-service data transfer.

8. **Use VPC endpoints for cloud service access.** S3 and DynamoDB via gateway endpoints (free, no data processing charge). Other services via interface endpoints (~$7/month/AZ plus $0.01/GB). Avoids NAT Gateway data charges entirely for AWS API traffic.

9. **Health-check the readiness endpoint, not the root.** `/health/ready` must verify DB connectivity, cache availability, and downstream dependencies. `/health` returning 200 while the connection pool is exhausted is a false positive that routes traffic to dead instances.

10. **Document network topology as code, not as a diagram.** Diagrams go stale within weeks of creation. Maintain topology in Terraform/CDK with automated diagram generation. Every peering connection, route table entry, security group rule, and TLS termination point must be version-controlled.

## Error Recovery
<!-- STANDARD: 3min -->

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Service topology, communication patterns, latency budgets, capacity projections, security boundaries | Before designing VPC topology or choosing connectivity patterns |
| `cloud-architect` | Cloud service selection, managed service networking limits, multi-cloud strategy, cost optimization targets | Before provisioning cloud networking resources or planning multi-cloud connectivity |
| `security-engineer` | Threat model boundaries, encryption requirements, compliance segmentation (PCI/HIPAA/SOC2), zero-trust policy | Before designing security groups, NACLs, WAF rules, or network segmentation |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `devops-engineer` | VPC/subnet topology, CI runner network access, service-to-service communication paths, Kubernetes node networking | DevOps can't build CI/CD pipelines or provision compute without network pathing |
| `cloud-architect` | Network architecture diagram, inter-region latency matrix, CDN edge strategy, DNS architecture | Cloud architecture decisions made without network feasibility — costly rework |
| `site-reliability-engineer` | Network observability (flow logs, LB access logs), health check endpoints, failover paths, cross-AZ latency baselines | SRE can't define SLOs or design resilience without network topology |
| `docker-kubernetes` | CNI plugin selection, NetworkPolicy design, ingress controller architecture, mTLS mesh configuration | Pod networking and service discovery can't be configured without network substrate |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| VPN tunnel down > 5 minutes | Incident Responder, System Architect | Hybrid connectivity broken; production impact possible |
| DDoS attack detected (Shield Advanced alert) | Security Engineer, Incident Responder | Active attack; mitigation verification, communication |
| NAT gateway IP exhaustion | DevOps Engineer, System Architect | Egress bottleneck; scale NAT or add VPC endpoints |
| Load balancer 5xx rate > 1% | DevOps Engineer, Backend Developer | Service health issue or backend overload |
| CDN cache hit rate drop > 20% | Performance Engineer, Frontend Developer | Origin overload risk; cache behavior regression |
| New VPC peering requested between prod and non-prod | Security Engineer, Compliance Officer | Blast radius increase; must justify and document |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---------|--------|-----|
| Deploying a new microservice that needs to communicate with 5+ existing services | Before assigning subnets and security groups, propose a service mesh (Istio/Linkerd/Cilium) evaluation: mTLS for all east-west traffic, sidecar injection for automatic retry/circuit-breaking, and authorization policies per service identity (not IP). Discuss whether the service mesh adds operational complexity worth the security/observability gain | Without a service mesh, every inter-service communication pair needs manually configured security groups, retry logic, and circuit breakers — 5 services = 25 pairs. Adding a 6th creates 11 new pairs. Service mesh centralizes these concerns but requires sidecar resource overhead (50-100MB per pod) and mesh control plane maintenance |
| Configuring a load balancer health check for a backend service | Before setting the health check path, probe the actual application readiness endpoint (`/health/ready`), not just `/health`. Propose distinguishing liveness ("is the process running?") from readiness ("can this instance serve traffic?"). Configure health check interval ≤10s with 2 consecutive failures before marking unhealthy. Discuss graceful shutdown: drain connections before health check fails | A health check on `/health` returns 200 while the DB connection pool is exhausted — the LB routes traffic to a dead instance. Readiness probes that check downstream dependencies prevent this. Without `connection_draining` or `deregistration_delay`, in-flight requests are dropped when an instance is removed |
| Setting up DNS for a multi-region deployment | Before creating records, propose latency-based or geo-steering routing policies. Set TTL to 60s for failover-capable records (not 300s). Configure health checks on each regional endpoint with failure thresholds. Discuss split-horizon DNS for internal service discovery vs public endpoints — internal services should resolve private IPs, not route through public endpoints | DNS is the first link in every request chain. A 300s TTL means 5 minutes of stale routing during a regional failover — users time out while DNS still points to the dead region. Split-horizon prevents internal traffic from egressing through NAT gateways and re-entering, which doubles latency and burns NAT bandwidth |
| Configuring CDN edge caching for an API that serves both authenticated and anonymous users | Before setting `Cache-Control` headers, propose `Vary: Authorization, Accept-Encoding` to prevent authenticated responses leaking to anonymous users. Configure CDN to strip/ignore `Set-Cookie` headers from cached responses. Discuss cache key design: include `Accept` header for content negotiation, exclude tracking params (`utm_*`, `_ga`). Set `stale-while-revalidate` and `stale-if-error` for resilience | CDNs cache by URL by default. If `/api/profile` returns user A's data (with cookie), user B might receive it if the CDN ignores cookies. `Vary: Authorization` tells the CDN to serve different cached responses per auth status. Missing this creates a data leakage vector that's invisible in testing |
| Designing subnet CIDR ranges for a VPC that will grow over 3 years | Before carving subnets, model future growth: count services per tier × environments × AZs. Use a CIDR calculator to allocate `/20` per AZ tier (public, private, isolated) within a `/16` VPC. Never use `/28` subnets (14 usable IPs — ENIs, Lambda, and RDS consume them fast). Document the allocation in a spreadsheet with committed ranges and reserved blocks | A `/28` subnet gives 14 IPs. AWS ALB needs 1 IP per AZ + 1 for scaling, RDS needs 1, Lambda in VPC needs 1 per concurrent execution — a single service can exhaust a /28. Renumbering a live VPC is nearly impossible without a full rebuild. CIDR planning is the one network decision you can't undo |
| Connecting an on-prem data center to a cloud VPC via VPN | Before provisioning, propose redundant tunnels (2 minimum per connection) with BGP dynamic routing. Monitor `TunnelState` AND `TunnelDataIn`/`TunnelDataOut` — tunnels can show "UP" with zero data flow due to Phase 2 parameter mismatch. Set BGP keepalive to 10s with hold time 30s for fast failover. Test failover quarterly | VPN tunnels silently fail. Phase 2 IPsec parameter mismatch shows tunnel "UP" but drops all data — no error log, no alert. Without BGP, failover from a dead tunnel requires manual intervention. The difference between 30s automated failover and 3-hour manual recovery is BGP |
| Designing API gateway → backend routing when the backend fleet auto-scales | Before configuring target groups, propose service discovery integration: register new instances on scale-up, deregister on scale-down with connection draining (30s minimum). Use IP target type (not instance) for direct pod routing. Configure the API gateway retry policy to exclude 5xx from retries on non-idempotent endpoints (`POST /orders`). Discuss sticky sessions only if strictly needed — they break horizontal scaling | Auto-scaling triggers fleet churn: instances come and go in minutes. Without proper deregistration delay, the gateway routes to terminated instances. Without IP target type, traffic double-hops through instance-level load balancing. Retrying a `POST /checkout` that returned 500 can create duplicate charges — the gateway must know which methods are safe to retry |

## State Log
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

- [ ] **[NE1]** CIDR allocation plan documented: non-overlapping ranges across all VPCs, regions, and on-prem, 3-year growth modeled
- [ ] **[NE2]** Subnet architecture: public/private/isolated tiers per AZ, `/20` or larger per tier, no `/28` subnets
- [ ] **[NE3]** Transit Gateway or hub-and-spoke for ≥4 VPCs, VPC peering only for point-to-point connections <4 VPCs
- [ ] **[NE4]** DNS: split-horizon (public + private zones), TTL ≤ 60s for failover records, health checks on all endpoints
- [ ] **[NE5]** Load balancers: health checks on readiness endpoint, connection draining ≥30s, access logs to S3/Blob Storage
- [ ] **[NE6]** Security groups: least-privilege per workload tier, no `0.0.0.0/0` except CDN/WAF managed prefix lists
- [ ] **[NE7]** VPC flow logs + DNS query logs enabled in all VPCs, shipped to centralized logging
- [ ] **[NE8]** Hybrid connectivity: redundant VPN tunnels (2+), BGP dynamic routing, failover tested quarterly
- [ ] **[NE9]** VPC endpoints for all cloud services (S3/DynamoDB/KMS via gateway; others via interface) — zero NAT Gateway dependency for API calls
- [ ] **[NE10]** CDN: origin shield configured, `Vary: Authorization` header, cache key excludes tracking params, stale-while-revalidate
- [ ] **[NE11]** WAF with managed rule groups + custom rate-limiting rules on all internet-facing endpoints
- [ ] **[NE12]** DDoS protection: Shield Standard (AWS) or equivalent, emergency contact info updated
- [ ] **[NE13]** Network topology documented as code (Terraform/CDK) with automated diagram generation, version-controlled

## What Good Looks Like
<!-- STANDARD: 3min -->

> A packet from a user's device in Tokyo reaches the application server in Frankfurt with under 80ms latency, traversing only the intended paths with no accidental exposure to public subnets.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice
<!-- STANDARD: 3min -->

Network engineering is one of the few domains where a mistake can take down the entire company. Practice must happen in sandboxes, not in production.

```mermaid
graph LR
    A[Design a network topology for a realistic scenario] --> B[Build it in a sandbox]
    B --> C[Break it: simulate failure, misconfiguration, attack]
    C --> D[Fix it, document the lessons, update your patterns]
    D --> A

```

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Build a VPC from scratch: subnets, route tables, NAT gateway, bastion host. Tear it down. Repeat. | Weekly |
| **Competent** | Simulate a network failure scenario in a sandbox — break DNS, cut connectivity between subnets, exhaust IPs | Biweekly |
| **Expert** | Design and test a multi-region failover topology with simulated regional outage | Quarterly |
| **Master** | Publish a reference architecture or postmortem that changes how your org (or industry) thinks about network design | Annually |

**The One Highest-Leverage Activity**: Build a complete VPC from scratch every month. Every time, make it a little better — fewer public IPs, tighter security groups, simpler routing. The repetition builds instincts that documentation can't.

### Decision Tree 4: Choosing Between Transit Gateway and VPC Peering

**Context:** You need to connect multiple VPCs. Should you use VPC peering (point-to-point, free intra-AZ data transfer, simpler) or Transit Gateway (hub-and-spoke, centralized routing, scales better)?

#### Phase 1: Scale & Topology Assessment
- How many VPCs need interconnection?
  - 2-3 VPCs → VPC peering is viable. Each pair needs its own peering connection (N(N-1)/2 connections: 1 for 2 VPCs, 3 for 3 VPCs).
  - 4-10 VPCs → Transit Gateway begins to dominate. 4 VPCs = 6 peering connections to manage vs. 4 TGW attachments.
  - 10+ VPCs → Transit Gateway is the clear choice. Mesh peering at this scale is unmanageable (45 connections for 10 VPCs).
- Are VPCs in different regions?
  - Same region → VPC peering works (no intra-region data transfer charge).
  - Cross-region → Transit Gateway supports inter-region peering. VPC peering also works cross-region but charges inter-AZ data transfer.
- Do you need transitive routing (VPC-A → VPC-B → VPC-C)?
  - Yes → Transit Gateway ONLY. VPC peering is strictly non-transitive. If VPC-A peers with VPC-B and VPC-B peers with VPC-C, A cannot reach C through B.
  - No → Either option works. Peering is simpler if transitivity isn't needed.
  - Need centralized egress (NAT, firewall, inspection) → TGW with a shared services VPC. Route all spoke traffic through centralized inspection before egress.

Complete when:
- VPC count, cross-region requirements, and transitive routing needs assessed and documented
- Scale threshold decision (peering for ≤3 VPCs, TGW for 4+) made with written rationale

#### Phase 2: Cost & Operational Tradeoffs
- **Data transfer volume**: Calculate monthly cross-VPC traffic.
  - Intra-AZ: VPC peering is FREE. TGW charges $0.02/GB processed.
  - Cross-AZ or cross-region: Both charge cross-AZ rates (~$0.01/GB), but TGW adds $0.02/GB processing on top.
  - High intra-AZ traffic (>5 TB/month) → Peering saves significantly. At 10 TB, TGW adds ~$200/month in processing fees.
- **Centralized control requirements**:
  - Need centralized inspection, shared services (firewall/NAT), or network segmentation with separate route domains → TGW with route tables per spoke.
  - Using AWS Network Firewall for east-west inspection → TGW required (firewall attaches to TGW, not peering).
- **Operational complexity**:
  - Small team (<5 engineers) → VPC peering is simpler to debug, fewer moving parts. Each connection is explicit and self-documenting.
  - Larger team with IaC → TGW's centralized management through Terraform/CDK reduces per-VPC configuration overhead.
- **Bandwidth**: VPC peering has no bandwidth limit (limited by instance bandwidth). TGW attachments support 50 Gbps burst each. For >50 Gbps per VPC, use multiple TGW attachments with ECMP.

Complete when:
- Monthly cross-VPC data transfer volume calculated with cost comparison (peering vs TGW)
- Centralized control requirements (inspection, shared services, segmentation) assessed
- Operational complexity evaluation completed factoring team size and IaC maturity

**Decision Matrix:**

| Factor | VPC Peering | Transit Gateway |
|--------|-------------|-----------------|
| VPC count | 2-3 optimal | 4+ optimal |
| Transitive routing | Not supported | Native |
| Intra-AZ data cost | Free | $0.02/GB |
| Centralized inspection | Manual (per VPC) | Native (route tables) |
| Max per-flow bandwidth | Instance-limited | 50 Gbps/attachment |
| Inter-region | Yes | Yes (inter-region peering) |
| Route table management | Per-VPC | Centralized |

**Recommendation:** Start with TGW if you expect to grow past 3 VPCs within 12 months. Migrating from a peering mesh to TGW requires re-architecting IP ranges and route tables — it's far cheaper to start with TGW than to migrate later. Use VPC peering only for point-to-point connections between exactly 2 VPCs that will never need transitive routing or centralized inspection.

### Decision Tree 5: Public vs Private Load Balancer Exposure Decision

**Context:** You're deploying a load balancer. Should it be internet-facing (resolves to public IPs) or internal (only reachable within the VPC/connected networks)?

#### Phase 1: Consumer Identity & Reachability
- Who consumes this service?
  - End users on the public internet → Internet-facing ALB/NLB REQUIRED. No alternative.
  - Partner/customer systems on their own external networks → Internet-facing with security controls (IP allowlisting, mTLS, WAF). Private connectivity (Direct Connect, VPN) is possible but operationally heavy for external partners.
  - Internal microservices within your VPC/network → Internal ALB/NLB. No internet exposure needed.
  - Internal but needs external health checks (e.g., CloudFront origin, global health monitor) → Internal LB + VPC endpoint, or separate health-check-only public endpoint on a dedicated port.
- Is the service part of a customer-facing product?
  - Customer-facing web app, API, or SaaS → Internet-facing behind CDN/WAF.
  - Internal admin dashboard, CI/CD tools, monitoring → Internal LB with VPN/bastion access. NEVER expose admin tools directly to the internet.

Complete when:
- All service consumers identified and classified (public internet, external partners, internal services, admin tools)
- Exposure decision per consumer type documented with rationale (internet-facing vs internal)

#### Phase 2: Security & Compliance Assessment
- Does the service handle regulated data (PCI-DSS, HIPAA, SOC2)?
  - Yes → Strongly prefer internal LB. If internet-facing is unavoidable: add WAF with managed rules, IP reputation filtering, geographic restrictions, bot control, and mandatory TLS 1.2+.
  - No → Internet-facing is acceptable with standard security (security groups, TLS).
- What's the blast radius if this service is compromised?
  - Service has access to databases, secrets, internal APIs → Internal LB. A compromised internet-facing service becomes a pivot point into your VPC.
  - Service is isolated, stateless, with no internal network access → Internet-facing is lower risk (but still apply security groups and WAF).
- Are there compliance mandates for data residency or network segmentation?
  - Yes (data must never traverse public internet) → Internal LB + PrivateLink/VPC endpoints for cross-account/VPC access.
  - No → Internet-facing with TLS is acceptable.

Complete when:
- Regulated data handling requirements (PCI-DSS, HIPAA, SOC2) assessed with security controls documented
- Blast radius analysis completed: what internal resources are reachable if the LB is compromised
- Compliance mandates for data residency and network segmentation verified

#### Phase 3: Architecture Patterns & Exceptions
- **API Gateway pattern**: Use internet-facing API Gateway (AWS API Gateway, Kong, Envoy) as the single public entry point. All backend services use internal LBs behind the gateway. Limits your public surface area to one endpoint.
- **CDN origin pattern**: Deploy internal ALB. Use CloudFront with VPC Origin (or equivalent CDN private origin feature) to keep the ALB private while serving public traffic through the CDN. Avoids exposing the origin to the internet entirely.
- **PrivateLink pattern**: Expose a service to OTHER AWS accounts without internet. Deploy internal NLB + VPC Endpoint Service. Consumers in other accounts create VPC endpoints. Traffic never leaves the AWS backbone.
- **Edge VPC pattern**: Centralize internet-facing LBs in a dedicated edge/ingress VPC. Route to internal LBs in workload VPCs via TGW or PrivateLink. Only the edge VPC has internet gateways — workload VPCs are fully private.

Complete when:
  Complete when: Architecture decision record (ADR) created with context, options, and rationale.
- Architecture pattern (API Gateway, CDN origin, PrivateLink, Edge VPC) selected based on consumer profile
- Pattern decision documented with rationale and rejection of alternatives
- Public surface area minimized to single entry point where possible

**Decision Matrix:**

| Consumer | Recommended Scheme | Fallback |
|----------|-------------------|----------|
| Public internet users | Internet-facing ALB + WAF + CDN | — |
| External partner APIs | Internet-facing NLB + mTLS + IP allowlist | PrivateLink (if partner on AWS) |
| Internal microservices | Internal ALB/NLB | — |
| Cross-account AWS consumers | Internal NLB + PrivateLink | Internet-facing + mTLS |
| Hybrid/on-prem consumers | Internal NLB + VPN/Direct Connect | Internet-facing + WAF + IP allowlist |
| Admin/monitoring tools | Internal ALB + VPN/bastion | NEVER public |

**Recommendation:** Default to internal unless the consumer is definitively on the public internet. Every internet-facing load balancer is a potential entry point. For public-facing services, always layer: WAF, CDN, TLS 1.2+ with strong ciphers, and security group rules scoped to CDN IP ranges or WAF-managed prefix lists — never `0.0.0.0/0` directly.

## Anti-Patterns
<!-- STANDARD: 3min -->

- **Security group rules are stateful** — if you allow outbound on port 443, return traffic is automatically allowed. But Network ACLs are stateless — you must explicitly allow both outbound (ephemeral ports 1024-65535) AND inbound responses.
- **DNS TTL is a maximum, not a guarantee**. Clients and intermediate resolvers may cache beyond TTL. During a DNS cutover, some clients will hit the old IP for up to 48 hours regardless of your 300-second TTL. Always keep old endpoints running for TTL × 2.
- **`0.0.0.0/0` in a security group** means "from anywhere on the internet." But `0.0.0.0/0` in a route table means "the local VPC's internet gateway." Same CIDR, completely different meaning — confusing these two is the #1 cause of accidentally public databases.
- **VPC peering is non-transitive**: A peered with B, B peered with C does NOT mean A can reach C. Every hop needs its own peering connection. This surprises teams migrating from hub-and-spoke network architectures.
- **Load balancer health checks** hitting `/health` on port 80 pass even when the app on port 8080 is down — the health check targets the wrong port. Always verify the health check port matches the actual application port.
- **MTU 1500 with VXLAN/Geneve encapsulation** adds 50 bytes overhead. Packets at exactly 1500 bytes get fragmented or dropped. Set "do not fragment" and reduce MTU to 1450 on overlay networks.
- **CIDR overallocation in cloud VPCs.** Allocating a `/16` (65,536 IPs) per environment when you need 200 IPs wastes address space and exhausts RFC 1918 ranges across dev/staging/prod/mgmt VPCs — when you expand to a new region, you discover overlapping CIDRs that block VPC peering and Transit Gateway connectivity. **Total cost: $15K-$50K/year in IP renumbering projects, downtime during re-addressing, and idle IP addresses billed by cloud providers at ~$0.005/hour per unused Elastic IP.** Use `/22` (1,024 IPs) per VPC with room for 4 `/24` subnets per availability zone, and reserve contiguous supernets for future region expansion.
- **Single region network design with no multi-region failover.** An entire SaaS product runs in `us-east-1` with a single Transit Gateway and one Direct Connect — a regional fiber cut or AWS control-plane outage takes down every customer globally for 4-8 hours with no fallback. **Total cost: $100K-$500K/hour in revenue loss during a regional outage for mid-market SaaS, plus SLA penalty payouts.** Design active-passive multi-region networking with DNS failover and cross-region VPC peering or Transit Gateway inter-region peering, targeting sub-15-minute regional failover.
- **Flat network architecture without segmentation.** All production workloads share a single VPC with no micro-segmentation — when an attacker compromises a public-facing web server, they scan the entire `/16` and pivot to the database tier, the CI/CD runner, and the secrets management instance without any network controls slowing lateral movement. **Total cost: $500K-$2M in breach scope expansion from unrestricted lateral movement — a segmentation architecture typically limits blast radius to a single subnet.** Implement micro-segmentation with security groups per workload tier, Network Policy (Kubernetes) or AWS Firewall, and zero-trust network access between all non-adjacent tiers.
- **Cloud egress cost surprise from cross-AZ or cross-region traffic.** A microservices architecture with NAT gateways in each AZ and inter-service calls across AZ boundaries generates $0.01-$0.02/GB in cross-AZ data transfer — a data-intensive pipeline moving 50TB/month cross-AZ accumulates $1,000-$2,000/month that nobody budgeted for. **Total cost: $5K-$50K/month in unexpected cloud egress charges for data-heavy workloads ($0.05-$0.12/GB internet egress, $0.01-$0.02/GB cross-AZ).** Deploy VPC endpoints (Gateway Endpoints for S3/DynamoDB, Interface Endpoints for other services), co-locate services that communicate heavily in the same AZ, and set billing alerts on data transfer line items before they become CFO conversations.
- **Missing or stale network topology documentation after personnel changes.** The senior network engineer who architected the multi-cloud VPC peering, Transit Gateway, and Direct Connect topology leaves the company — the architecture existed only in their head. Six months later, a routine TLS certificate rotation on an internal-facing Application Load Balancer takes down production for 6 hours because nobody documented which certificates terminate where, which route tables reference which gateways, and which security groups allow health-check traffic between tiers. Network outages caused by missing documentation are the most common avoidable cause of extended MTTR — every minute of downtime from "figuring out how it's connected" is pure waste. **Total cost: $50K-$300K per extended outage from undocumented network topology, plus $10K-$25K in emergency consulting fees to reverse-engineer the architecture.** Maintain a living network diagram (Lucidchart, draw.io, or infrastructure-as-diagram tooling) updated with every infrastructure change, documenting every peering connection, route table entry, security group rule intent, and TLS termination point with expiration dates.

## Gotchas
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Single-region deployment with no multi-region failover | $100K-$500K/hour in revenue loss during a regional outage | Design active-passive multi-region from day 1. Test failover quarterly. Document RTO/RPO targets |
| Flat network with no micro-segmentation — one compromise becomes full network access | $500K-$2M in breach scope expansion from unrestricted lateral movement | Implement least-privilege network segmentation. Use security group references not CIDR ranges. Zero-trust between all non-adjacent tiers |
| Missing network cost monitoring — cross-AZ traffic surprises | $50K-$300K/month in unexpected cross-AZ and egress charges | Set billing alerts on data transfer line items. Co-locate chatty services in same AZ. Use VPC endpoints for S3/DynamoDB |
| CIDR overallocation exhausting RFC 1918 space across environments | $15K-$50K/year in renumbering projects when ranges overlap across VPCs | Plan CIDR allocations with future growth. Use /22 per environment max. Reserve contiguous supernets for region expansion |

## Verification
<!-- STANDARD: 3min -->

- [ ] Run `terraform plan` — no unexpected resource changes, CIDR ranges don't overlap
- [ ] Verify DNS: `dig +short ${service}.internal` resolves to expected private IP
- [ ] Verify firewall: `nc -zv ${host} ${port}` from allowed subnet succeeds; from blocked subnet times out
- [ ] Verify load balancer health checks: `curl ${LB}/health` returns 200 on all backend instances
- [ ] Test failover: stop one backend instance — traffic shifts to remaining instances within health check interval × 3
- [ ] Verify TLS: `openssl s_client -connect ${host}:443` shows valid certificate chain, no expired certs

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| VPC peering works between A↔B and B↔C, but A cannot reach C — production services unreachable after 10 hours | VPC peering is non-transitive. Traffic from A to C goes to B, but B doesn't forward it to C. Engineer assumed peering creates a mesh | Replace VPC peering with Transit Gateway for hub-and-spoke that supports transitive routing. Or create direct A↔C peering connection. Document with network topology diagram | VPC peering is point-to-point, not mesh. Three VPCs need three peering connections. Four VPCs need six. Five VPCs need ten. Past three VPCs, use Transit Gateway. |
| TLS 1.0 disabled — internal service that only supports TLS 1.0 goes dark. No one knew it existed | Security team disabled TLS 1.0 at load balancer level. Legacy internal service running Java 7 never updated. No service inventory, no dependency tracking | Before disabling protocols, grep all service configs and dependency manifests for TLS version requirements. Run service discovery scan: `nmap --script ssl-enum-ciphers` against all internal IPs. Create migration runway for laggard services | Security hardening breaks things when you don't know what depends on what you're hardening. Always scan before you change. A service inventory is network infrastructure. |
| DNS resolution takes 3 seconds in us-east-1 but 5ms in us-west-2 — latency alert fires every morning | Route 53 latency-based routing + misconfigured health checks. East region health check fails intermittently, causing DNS to route to West. Internal apps don't handle cross-region latency | Fix health check thresholds: increase failure threshold to 3 consecutive failures before marking unhealthy. Add inter-region latency budgets in application config. Monitor DNS resolution time from each region | DNS is your first hop. If it adds 3 seconds, nothing else matters. Latency-based routing needs conservative health check thresholds — one failed ping shouldn't reroute half your traffic across the continent. |
| `Destination port unreachable` between two subnets in the same VPC — security group was "correct" | Security group allows traffic from `10.0.1.0/24` but service migrated to `10.0.2.0/24`. SG rules weren't updated. No automation linking service identity to network rules | Use security group references instead of CIDR ranges: allow traffic from `sg-allowlist` not `10.0.1.0/24`. When services move subnets, they keep the same SG ID — rules stay valid. Or use service mesh that abstracts network identity | CIDR-based security group rules are brittle. The IP a service has today is not the IP it'll have after scaling, migrating, or failing over. Reference security groups by ID. |
| Load balancer health checks pass but all requests return 502 — backend is healthy but not serving traffic correctly | ALB targets registered by instance ID, instances pass TCP health check, but application process crashed. Health check verifies port is open, not that application responds with 200 | Use HTTP health checks at `/health` endpoint that validates: database connectivity, cache availability, message queue connection. Set `healthy_threshold` to 2 and `unhealthy_threshold` to 3. Never rely on TCP health checks for application-layer services | TCP health checks prove the port is open. HTTP health checks prove the application works. The gap between them is where 502 errors live. Always health-check the application, not the socket. |
| WAF blocks legitimate traffic with 403 Forbidden — customers can't log in from certain ISPs | AWS WAF rate-based rule triggers on shared IP ranges (mobile carriers, corporate NAT). 500 users behind one IP all throttled as one "client" | Add IP warm-up list for known shared IPs. Use token-based rate limiting (JWT claims) instead of IP-based. Set WAF in COUNT mode for 7 days before switching to BLOCK — review blocked patterns before enforcement | IPs are not users. Rate limiting by IP in the age of CGNAT and corporate VPNs will produce false positives. Token-based limiting or IP reputation overrides are essential. |

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
