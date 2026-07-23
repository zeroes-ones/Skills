---
name: networking-engineer
description: "Cloud networking architecture (VPC/VNet/VCN), subnet/CIDR planning, DNS architecture, CDN strategy, load balancing (L4/L7), network security (security groups/NACLs/WAF/DDoS), hybrid/multi-cloud networking (VPN/Direct Connect/ExpressRoute), BGP routing, service mesh (sidecar/ambient/eBPF), API gateway/ingress, Zero Trust (ZTNA), and network observability. Trigger: networking, VPC, DNS, CDN, load balancer, BGP, network architecture, subnet, firewall, VPN, SDN, network security, network design, peering, transit gateway. Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI."
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - networking-engineer
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
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

Design, deploy, and operate cloud-native and hybrid network architectures. This skill covers the full stack: from IP address planning and subnet design through DNS, load balancing, CDN, firewalls, VPNs, and service mesh. Every design considers cost, latency, security, and operational complexity. The goal is a network that developers never think about because it just works — secure by default, fast everywhere, and cheap at scale.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design a new VPC/subnet topology → Start at "Decision Trees > VPC/Block Design"
├── Configure DNS (public/private zones, split-horizon) → Jump to "Core Workflow > Phase 2 (DNS Architecture)"
├── Set up load balancers (ALB/NLB) with SSL → Go to "Core Workflow > Phase 3 (Load Balancing)"
├── Configure CDN with edge caching → Jump to "Core Workflow > Phase 4 (CDN Strategy)"
├── Design firewall rules and security groups → Go to "Best Practices > Network Security" then "Core Workflow > Phase 5"
├── Set up hybrid cloud connectivity (VPN/Direct Connect) → Jump to "references/hybrid-connectivity-guide.md"
├── Deploy a service mesh (Istio/Linkerd/Cilium) → Go to "references/service-mesh-patterns.md"
├── Design zero-trust architecture → Jump to "references/zero-trust-architecture.md"
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

These rules apply to *every* response this skill produces.

- **Never suggest without understanding existing infrastructure.** Always ask: "What cloud provider? What regions? What's already running?" Do not design in isolation from what exists.
- **Security groups must be least-privilege.** Every rule should specify exact source/destination CIDRs and ports. Never open `0.0.0.0/0` to all ports without explicit justification and a timeline to tighten.
- **Always consider latency implications.** A network design that adds 50ms per request may be architecturally correct but operationally broken. Calculate hop latency for every path. Do not ignore the speed of light.
- **Default-deny, explicitly allow.** Start with all traffic blocked. Open only what's needed. Review rules monthly for unused allowances.
- **Admit what you don't know.** If you haven't seen the existing topology, traffic patterns, or compliance requirements, say so and ask before designing.

## The Expert's Mindset

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

- You are designing a new VPC/VNet with subnets, CIDR ranges, and routing tables from scratch
- You need to connect multiple VPCs across accounts or regions via peering or transit gateway
- You are planning DNS architecture (public/private zones, split-horizon, multi-cloud resolution)
- You need to set up load balancers (ALB/NLB/GLB) with health checks and SSL termination
- You are configuring network security layers — security groups, NACLs, WAF rules, DDoS protection
- You are establishing hybrid connectivity between on-prem data centers and cloud (VPN, Direct Connect, ExpressRoute)
- You need to deploy a service mesh (Istio, Linkerd, Cilium) with mTLS and traffic policies
- You are designing a CDN strategy with edge caching, origin shield, and DDoS mitigation

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
```
VPC/BLOCK DESIGN — How many VPCs and what CIDR ranges?
├── Single region, single environment (dev/prod combined), < 10 services?
│   └── 1 VPC. 10.0.0.0/16. Public subnets for load balancers, private for compute,
│       isolated for databases. Simplicity > multi-VPC complexity.
├── Multi-environment (dev/staging/prod), 10-50 services?
│   └── 1 VPC per environment. Non-overlapping CIDRs (10.0.0.0/16, 10.1.0.0/16, 10.2.0.0/16).
│       VPC peering if services need cross-env communication. Transit Gateway for >3 VPCs.
├── Multi-account (AWS Organizations), 50+ services, compliance isolation needed?
│   └── 1 VPC per account per environment. Centralized egress via Transit Gateway + NAT Gateway
│       in a shared Network account. Centralized ingress via a shared Edge VPC.
│       CIDR planning: allocate a /14 supernet, carve /16 blocks per account.
│       NEVER overlap CIDRs between any VPCs that might ever be peered.
├── Multi-region deployment?
│   └── Same CIDR plan replicated per region (non-overlapping across regions if
│       inter-region peering/VPN is needed). Use a CIDR allocation spreadsheet.
│       Regional Transit Gateways peered inter-region for cross-region routing.
└── Multi-cloud (AWS + Azure + GCP)?
    └── Separate IP plans per cloud. Use a master /12 block, allocate /14 per cloud,
        /16 per region. NEVER let clouds auto-assign CIDRs. Plan every range manually.
        Inter-cloud connectivity: SD-WAN, cloud-native VPN gateways, or Equinix Fabric.

DNS ARCHITECTURE — Public, private, or split-horizon?
├── Single DNS zone, all records public?
│   └── Route 53 / Cloud DNS / Azure DNS public zone. Simple, no split-brain.
│       Only safe if: no internal-only services OR internal services use private IPs
│       that aren't routable from the internet (10.x, 172.16.x, 192.168.x).
├── Separate public and private zones (split-horizon)?
│   └── `example.com` (public) for customer-facing endpoints.
│       `example.internal` (private) or `internal.example.com` for internal services.
│       Private zones resolve to private IPs. Never leak internal hostnames to public DNS.
│       RECOMMENDED for any multi-service deployment.
├── Service discovery via DNS?
│   └── Use private hosted zones + service-specific subdomains:
│       `payment-service.internal.example.com`, `user-service.internal.example.com`.
│       Kubernetes: CoreDNS + ExternalDNS auto-register services. Consul: DNS interface.
│       Cloud Map / Service Directory for cloud-native discovery.
└── Anycast DNS for global latency optimization?
    └── Route 53 (anycast by default), Cloudflare DNS, Google Cloud DNS.
        Resolves to the nearest healthy endpoint. Critical for global products
        with latency SLAs < 100ms. Costs ~$0.50/million queries.

LOAD BALANCING — L4 or L7? Regional or global?
├── Simple HTTP/HTTPS app, single region?
│   └── Application Load Balancer (L7). Path-based routing, host-based routing,
│       SSL termination, WebSocket support. Health checks on `/health` endpoint.
│       Auto-scaling group behind ALB. Done.
├── Non-HTTP traffic (gRPC, TCP, UDP, gaming, IoT)?
│   └── Network Load Balancer (L4). Preserves source IP. Ultra-low latency (<1ms added).
│       Supports static IP. Use for: gRPC streaming, databases, VoIP, game servers.
│       NLB → Target Group → gRPC health checks.
├── Global deployment, users on 3+ continents?
│   └── Global load balancer: AWS Global Accelerator (static anycast IPs, TCP/UDP),
│       Cloudflare Load Balancing (DNS-level, HTTP/S), Google Cloud Load Balancing
│       (global anycast, single anycast IP). Route users to nearest healthy region.
├── Kubernetes ingress?
│   └── Ingress Controller (nginx-ingress, AWS Load Balancer Controller, Traefik).
│       ALB Ingress Controller for AWS/EKS: one ALB per Ingress, path-based routing.
│       Gateway API (successor to Ingress) for complex routing: header-based, weight-based.
└── API gateway needed (auth, rate limiting, request transformation)?
    └── Layer API Gateway in FRONT of the load balancer, not behind it.
        Kong, Apigee, AWS API Gateway, Envoy Gateway. Handles: auth, rate limiting,
        request/response transformation, API versioning, analytics.

NETWORK SECURITY — Defense in depth. Where do we place each layer?
├── DDoS protection?
│   └── Cloud-native: AWS Shield Standard (free, always on) + Shield Advanced ($3K/mo,
│       financial protection against DDoS cost spikes). Cloudflare: DDoS protection
│       included in all plans. ALWAYS enable at least the free tier DDoS protection
│       — an unprotected public endpoint WILL be attacked eventually.
├── Web Application Firewall (WAF)?
│   └── AWS WAF on ALB/CloudFront. OWASP Top 10 rules. Rate-based rules (block IPs
│       exceeding N requests/min). Geo-match (block countries you don't serve).
│       Managed rules (AWS Managed, Cloudflare Managed) > custom rules for starters.
│       Custom rules only when you have specific attack patterns.
├── Network-level filtering?
│   └── Security Groups (stateful, per-instance/ENI): ALLOW rules only. Default deny.
│       NACLs (stateless, per-subnet): ALLOW + DENY rules. Use as defense-in-depth
│       SECOND layer, not primary. Primary filtering = Security Groups.
│       NEVER use NACLs as your only network filter — they're stateless and painful.
└── East-west traffic (service-to-service within the network)?
    └── Zero Trust: no service trusts another by default. Service mesh (Istio/Consul/Linkerd)
        with mTLS. Kubernetes NetworkPolicy (deny-all default, explicit allows).
        Security groups: reference other security groups by ID, not CIDR ranges.
        NEVER open 0.0.0.0/0 between internal services "for convenience."

HYBRID CONNECTIVITY — VPN or Direct Connect?
├── < 100 Mbps sustained, latency-tolerant (50-100ms)?
│   └── Site-to-Site VPN (IPsec). AWS: $0.05/hour per VPN connection + data transfer.
│       Azure: VPN Gateway. GCP: Cloud VPN. Setup: 1-4 hours.
│       Max throughput: ~1.25 Gbps (AWS VPN, depends on instance size).
│       Use for: dev/staging environments, small offices, backup connectivity.
├── > 100 Mbps, latency-sensitive, consistent throughput?
│   └── Direct Connect (AWS) / ExpressRoute (Azure) / Cloud Interconnect (GCP).
│       1 Gbps, 10 Gbps, 100 Gbps ports. Setup: 2-8 weeks (physical cross-connect).
│       Cost: $0.30/hour per 1 Gbps port + data transfer out.
│       Use for: production hybrid workloads, database replication, large data transfer.
├── Multi-cloud or multi-region mesh?
│   └── SD-WAN (Cloudflare Magic WAN, Cisco, VMware) or cloud-native hub-and-spoke
│       (AWS Transit Gateway + VPN/DX to on-prem, peered to other cloud's equivalent).
│       Or Equinix Fabric / Megaport for physical cross-connects between clouds.
└── Remote developer access?
    └── AWS Client VPN (OpenVPN-based, $0.10/hour + $0.05/connection-hour).
        Or Tailscale/ZeroTier (WireGuard-based, simpler, cheaper for <100 users).
        NEVER expose SSH/RDP to 0.0.0.0/0 — always behind VPN or SSM Session Manager.

**What good looks like:** Network topology diagram with VPCs, subnets, route tables, security groups, and load balancers — anyone on-call can find the ingress path from CDN to database in under 2 minutes. Zero-trust segmentation is documented and verified: no service can reach another service without explicit policy. p99 latency between colocated services < 5ms. DNS resolution < 50ms p99 from any region.
## Core Workflow
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
   for 1 year (versioned filenames). Cache API responses selectively (Cache-Control headers).
   Enable Origin Shield (CloudFront) or equivalent to reduce origin load.
   - **Input**: Content types, cacheability analysis, global user distribution.
   - **Output**: CDN distribution deployed. Cache hit rate monitored. Origin load reduced.

### Phase 3 (~20 min): Security Hardening
<!-- DEEP: 10+min -->

1. **Implement security groups and NACLs**: Security groups: least privilege. Allow only required
   ports and sources. Never allow 0.0.0.0/0 on database ports. Reference security group IDs,
   not CIDRs, for inter-service traffic.
   NACLs: stateless defense-in-depth layer. Apply per-subnet. Deny known bad actors,
   allow expected traffic. Use ephemeral port ranges correctly (1024-65535 for return traffic).
   - **Input**: Service communication matrix (who talks to whom, on what port/protocol).
   - **Output**: Security group rules documented. NACL rules applied. Communication matrix verified.

2. **Deploy WAF and DDoS protection**: AWS WAF on ALB/CloudFront. Enable AWS Shield Standard
   (free, automatic). Managed rule groups: AWS Managed Core Rule Set, SQL Injection, XSS,
   IP Reputation. Rate-based rules: block after 2000 requests/5 min per IP (tune per endpoint).
   - **Input**: Public endpoints, expected traffic patterns, threat model.
   - **Output**: WAF web ACL associated. Shield protection active. DDoS dashboard monitored.

3. **Implement network segmentation**: Microsegmentation between services. Kubernetes:
   NetworkPolicy with default-deny + explicit allows. Service mesh: mTLS + authorization
   policies (Istio AuthorizationPolicy). Cloud-native: security group referencing + VPC
   endpoints for AWS services (S3, DynamoDB) instead of internet routing.
   - **Input**: Service dependency graph, compliance boundaries (PCI, HIPAA).
   - **Output**: Segmentation enforced. East-west traffic limited to authorized paths.

### Phase 4 (~15 min): Observability & Operations

1. **Enable network observability**: VPC Flow Logs (to S3/CloudWatch). Publish to CloudWatch
   Logs for real-time analysis, S3 for long-term archive (Athena queryable). DNS query logging
   (Route 53 Resolver Query Logs). Load balancer access logs. CloudFront real-time logs.
   - **Input**: Network components to monitor.
   - **Output**: Flow logs enabled on all VPCs. Dashboards for: top talkers, rejected traffic,
     inter-AZ data transfer, NAT gateway throughput.

2. **Set up network monitoring and alerting**: CloudWatch Alarms on: NAT gateway
   `ErrorPortAllocation` (IP exhaustion), `PacketsDropCount` (blackhole traffic),
   VPC endpoint DNS resolution failures, Transit Gateway attachment status.
   Alert on: VPN tunnel down > 5 min, Direct Connect BGP session down > 1 min,
   load balancer 5xx rate > 1%, CDN cache hit rate drop > 20%.
   - **Input**: Network components to monitor, SLO targets.
   - **Output**: Alerts configured. Runbook documented for each alert.

3. **Network automation (IaC)**: All network resources defined in Terraform / Pulumi / CDK.
   No click-ops. Network changes go through CI/CD: plan → review → apply. Network module
   library: reusable modules for VPC, subnets, Transit Gateway, VPN, load balancers.
   - **Input**: Network design, infrastructure standards.
   - **Output**: IaC repository with network modules. CI pipeline for network changes.

## Cross-Skill Coordination

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

| Trigger | Action | Why |
|---------|--------|-----|
| Deploying a new microservice that needs to communicate with 5+ existing services | Before assigning subnets and security groups, propose a service mesh (Istio/Linkerd/Cilium) evaluation: mTLS for all east-west traffic, sidecar injection for automatic retry/circuit-breaking, and authorization policies per service identity (not IP). Discuss whether the service mesh adds operational complexity worth the security/observability gain | Without a service mesh, every inter-service communication pair needs manually configured security groups, retry logic, and circuit breakers — 5 services = 25 pairs. Adding a 6th creates 11 new pairs. Service mesh centralizes these concerns but requires sidecar resource overhead (50-100MB per pod) and mesh control plane maintenance |
| Configuring a load balancer health check for a backend service | Before setting the health check path, probe the actual application readiness endpoint (`/health/ready`), not just `/health`. Propose distinguishing liveness ("is the process running?") from readiness ("can this instance serve traffic?"). Configure health check interval ≤10s with 2 consecutive failures before marking unhealthy. Discuss graceful shutdown: drain connections before health check fails | A health check on `/health` returns 200 while the DB connection pool is exhausted — the LB routes traffic to a dead instance. Readiness probes that check downstream dependencies prevent this. Without `connection_draining` or `deregistration_delay`, in-flight requests are dropped when an instance is removed |
| Setting up DNS for a multi-region deployment | Before creating records, propose latency-based or geo-steering routing policies. Set TTL to 60s for failover-capable records (not 300s). Configure health checks on each regional endpoint with failure thresholds. Discuss split-horizon DNS for internal service discovery vs public endpoints — internal services should resolve private IPs, not route through public endpoints | DNS is the first link in every request chain. A 300s TTL means 5 minutes of stale routing during a regional failover — users time out while DNS still points to the dead region. Split-horizon prevents internal traffic from egressing through NAT gateways and re-entering, which doubles latency and burns NAT bandwidth |
| Configuring CDN edge caching for an API that serves both authenticated and anonymous users | Before setting `Cache-Control` headers, propose `Vary: Authorization, Accept-Encoding` to prevent authenticated responses leaking to anonymous users. Configure CDN to strip/ignore `Set-Cookie` headers from cached responses. Discuss cache key design: include `Accept` header for content negotiation, exclude tracking params (`utm_*`, `_ga`). Set `stale-while-revalidate` and `stale-if-error` for resilience | CDNs cache by URL by default. If `/api/profile` returns user A's data (with cookie), user B might receive it if the CDN ignores cookies. `Vary: Authorization` tells the CDN to serve different cached responses per auth status. Missing this creates a data leakage vector that's invisible in testing |
| Designing subnet CIDR ranges for a VPC that will grow over 3 years | Before carving subnets, model future growth: count services per tier × environments × AZs. Use a CIDR calculator to allocate `/20` per AZ tier (public, private, isolated) within a `/16` VPC. Never use `/28` subnets (14 usable IPs — ENIs, Lambda, and RDS consume them fast). Document the allocation in a spreadsheet with committed ranges and reserved blocks | A `/28` subnet gives 14 IPs. AWS ALB needs 1 IP per AZ + 1 for scaling, RDS needs 1, Lambda in VPC needs 1 per concurrent execution — a single service can exhaust a /28. Renumbering a live VPC is nearly impossible without a full rebuild. CIDR planning is the one network decision you can't undo |
| Connecting an on-prem data center to a cloud VPC via VPN | Before provisioning, propose redundant tunnels (2 minimum per connection) with BGP dynamic routing. Monitor `TunnelState` AND `TunnelDataIn`/`TunnelDataOut` — tunnels can show "UP" with zero data flow due to Phase 2 parameter mismatch. Set BGP keepalive to 10s with hold time 30s for fast failover. Test failover quarterly | VPN tunnels silently fail. Phase 2 IPsec parameter mismatch shows tunnel "UP" but drops all data — no error log, no alert. Without BGP, failover from a dead tunnel requires manual intervention. The difference between 30s automated failover and 3-hour manual recovery is BGP |
| Designing API gateway → backend routing when the backend fleet auto-scales | Before configuring target groups, propose service discovery integration: register new instances on scale-up, deregister on scale-down with connection draining (30s minimum). Use IP target type (not instance) for direct pod routing. Configure the API gateway retry policy to exclude 5xx from retries on non-idempotent endpoints (`POST /orders`). Discuss sticky sessions only if strictly needed — they break horizontal scaling | Auto-scaling triggers fleet churn: instances come and go in minutes. Without proper deregistration delay, the gateway routes to terminated instances. Without IP target type, traffic double-hops through instance-level load balancing. Retrying a `POST /checkout` that returned 500 can create duplicate charges — the gateway must know which methods are safe to retry |

## Scale Depth
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


## What Good Looks Like

> A packet from a user's device in Tokyo reaches the application server in Frankfurt with under 80ms latency, traversing only the intended paths with no accidental exposure to public subnets. Every subnet is right-sized — no /16s wasting IP space, no /28s causing midnight renumbering emergencies — and CIDR allocations leave room for three years of growth. DNS resolves correctly from inside the VPC, from the office VPN, and from the public internet with consistent, split-horizon-aware answers. Security groups follow strict least-privilege: port 22 is open nowhere, inter-service traffic uses explicit security group references, and no rule contains 0.0.0.0/0 unless it's a public load balancer on 443. DDoS protection absorbs a volumetric attack without a single 5xx reaching users, and the network topology diagram in Lucidchart actually matches what Terraform deployed last Tuesday.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|---|---|---|
| `vpc-design` | Designing a new cloud network or restructuring existing | CIDR planning, subnet architecture, route tables, NAT/IGW/VPC endpoints, multi-VPC peering |
| `dns-architecture` | Setting up public/private/hybrid DNS | Zone management, split-horizon, DNS forwarding, service discovery, DNSSEC, TTL strategy |
| `load-balancing` | Routing traffic to services | ALB vs NLB vs GLB, SSL termination, health checks, stickiness, cross-zone load balancing |
| `cdn-strategy` | Optimizing content delivery globally | Cache behaviors, origin shield, edge functions, cache invalidation, dynamic acceleration |
| `network-security` | Hardening the network perimeter and east-west | Security groups, NACLs, WAF, DDoS, NetworkPolicy, microsegmentation, intrusion detection |
| `hybrid-connectivity` | Connecting cloud to on-prem or multi-cloud | VPN (IPsec/WireGuard), Direct Connect/ExpressRoute, SD-WAN, BGP configuration |
| `service-mesh` | Managing service-to-service communication at scale | Istio/Linkerd/Consul, mTLS, traffic splitting, circuit breaking, observability |
| `network-observability` | Monitoring and troubleshooting the network | VPC Flow Logs, packet capture, route analyzers, latency monitoring, dashboards, alerting |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Never overlap CIDR ranges between any networks that might connect**: This seems obvious but is the #1 cause of multi-VPC/cloud networking pain. Plan all CIDRs in a spreadsheet before creating anything. Overlapping ranges make peering, VPN, and Transit Gateway impossible.
- **Security groups as primary filter, NACLs as defense-in-depth**: Security groups are stateful, easy to reason about, and work per-resource. NACLs are stateless, per-subnet, and easy to misconfigure. Use NACLs as a SECOND layer for broad rules (block entire CIDRs, enforce ephemeral port ranges) — never as your only filter.
- **VPC endpoints for all AWS services**: NAT gateway costs $0.045/hour + $0.045/GB processed. S3 VPC endpoint: free. DynamoDB VPC endpoint: free. Every GB going through VPC endpoints instead of NAT is money saved. Audit quarterly: any AWS service traffic going through NAT should be migrated to VPC endpoints.
- **Use security group referencing, not CIDR ranges, for inter-service traffic**: `sg-abc123` allows `sg-xyz789` on port 8080. This is self-documenting and automatically updates when instances change. If you use CIDRs (`10.0.1.0/24`), you must update them when subnets change — and you WILL forget.
- **Enable flow logs on every VPC from day one**: Flow logs cost ~$0.50/GB ingested (CloudWatch) or ~$0.02/GB (S3). At small scale, this is negligible. When you have a security incident or connectivity issue, you'll wish you had them. They cannot be retroactively enabled.
- **Design for AZ independence**: NAT gateway per AZ (not a single NAT gateway). Load balancer cross-zone enabled. Don't route all traffic through one AZ — an AZ outage will take down everything. Yes, inter-AZ data transfer costs money ($0.01-0.02/GB). It's cheaper than downtime.
- **CDN origin shield saves money and reduces origin load**: CloudFront Origin Shield adds an extra caching layer between edge locations and your origin. One request to origin per cache miss across all edge locations, not one per edge location. Cost: minor. Value: significant at scale.
- **Automate everything — network click-ops cause outages**: A security group rule opened to 0.0.0.0/22 by a tired engineer at 2 AM is a breach waiting to happen. All network changes through Terraform/Pulumi/CDK with plan review. Audit: setup AWS Config / Azure Policy to detect manual changes.
- **Monitor inter-AZ data transfer costs**: Chatty services that talk cross-AZ can generate massive bills. A service making 1000 req/s with 1KB payload cross-AZ costs ~$2,600/month in data transfer ALONE. Use availability-zone-aware service discovery (topology-aware routing in Kubernetes).
- **Plan IPv6 alongside IPv4 — don't treat it as a future project**: IPv4 exhaustion is real. AWS charges $3.65/month per public IPv4 address starting 2024. Dual-stack your VPCs from the start. It adds minimal complexity now and saves a major migration later.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Opening `0.0.0.0/0` on port 22 (SSH) or 3389 (RDP) in security groups | Use SSM Session Manager (AWS) or Bastion with `ssh-over-ssm` — no inbound SSH at all. If SSH is unavoidable, restrict to a specific bastion security group (`sg-bastion`) and rotate IP allow-lists. Port 22 open to the world attracts brute-force attacks within minutes of provisioning |
| Creating a single NAT Gateway in one AZ and routing all private subnets through it | Deploy one NAT Gateway per AZ. Each private subnet routes through the NAT in its own AZ. A single NAT Gateway is an AZ-level single point of failure — when that AZ goes down, all outbound internet from private subnets stops. Cross-AZ NAT routing also doubles inter-AZ data transfer costs |
| Using security group CIDR rules (`10.0.1.0/24`) instead of security group references (`sg-app`) for inter-service traffic | Reference security groups directly: allow `sg-database` from `sg-backend` on port 5432. This is self-documenting, survives instance replacement, and eliminates the risk of stale CIDR rules when subnets are renumbered or services move. If you must use CIDRs, add a comment with the service name |
| Configuring CDN to cache everything with the same TTL regardless of content type | Set differentiated cache policies: static assets (JS/CSS/images) → 1 year with filename hashing; API responses → `Cache-Control: s-maxage=60, stale-while-revalidate=300`; authenticated pages → `Cache-Control: private, no-store`. One-size-fits-all caching serves stale API data and under-caches static assets |
| Running all cross-region traffic without latency budget analysis | Calculate round-trip latency per region pair (e.g., us-east-1 ↔ eu-west-1 = ~80ms). If a request must traverse 3 microservices, each crossing regions, you're at 240ms minimum before processing. Keep synchronous call chains within a region; use async replication for cross-region. Document latency budgets per path |
| Manually editing security group rules in the console during incidents | All security group changes go through IaC (Terraform/Pulumi/CDK) with CI/CD plan review. Console click-ops leave no audit trail, can't be reproduced, and inevitably leave temporary rules permanently open. If an incident requires a manual change, file a ticket to backfill it into IaC within 24 hours |
| Deploying a service mesh without observability and traffic policies configured | Service mesh without mTLS enforcement is just overhead. Configure: (a) mTLS in `STRICT` mode (not permissive), (b) `AuthorizationPolicy` to allow only known service identities, (c) distributed tracing sampling at 10-100%, (d) retry budgets (max 3, exponential backoff + jitter), (e) circuit breaker at 50% error rate. A mesh that only routes is a wasted deployment |
| Not configuring WAF rate limiting on public endpoints until after the first DDoS or scraping attack | Deploy WAF with AWS Managed Rules (Core Rule Set, IP Reputation) and at least a per-IP rate limit (1000 req/5min) on login, checkout, and search endpoints. Scrapers, credential stuffers, and simple DDoS attacks hit every public endpoint. Without WAF, your origin scales to absorb the attack — and your cloud bill scales with it |

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Legitimate API traffic returning connection timeouts from 3rd-party partners | Security group rule was too restrictive — allowed only `10.0.0.0/16` but partner's NAT gateway used `10.2.0.0/16`; traffic was silently dropped | Audit security groups: widen allowed CIDR to include partner ranges. Implement VPC Flow Logs with Athena queries to detect denied traffic patterns. Add monitoring for rejected connection counts | **Security groups need logging and monitoring, not just configuration.** Enable VPC Flow Logs from day one. When partners report connectivity issues, query Flow Logs for `REJECT` records before blaming the partner. Overly restrictive rules that drop legitimate traffic are as bad as overly permissive ones |
| Production DNS stopped resolving for 45 minutes — `dig` returned no answers | A stale NS record pointed to a decommissioned DNS server; TTL was set to 86400s (24 hours) so clients cached the broken NS record | Update NS records to point to current DNS servers. Set TTL to 300s (5 min) during migrations, 86400s only after stability confirmed. Implement DNS monitoring with Route 53 Resolver Query Logs | **Low TTL during migrations saves you.** Set TTL to 300s before infrastructure changes, 86400s only after stability is confirmed. Always have redundant DNS servers. Monitor DNS query failures — if you're not measuring DNS, you're blind to a common failure mode |
| Could not allocate new subnets for a critical service launch | VPC was created with a /16 subnet but only /28 subnets were carved — all 16 subnets were consumed, no IP space left | No fix without renumbering the VPC (impossible at scale). Create a secondary VPC and peer to the existing one. Plan: from day one, allocate a /12 supernet and carve /16 per VPC | **CIDR planning must project 3 years of growth.** A /16 (65,536 IPs) seems like a lot until you account for per-AZ, per-environment, per-service segmentation. Document a CIDR allocation spreadsheet before creating the first VPC. Never use /28 subnets — they run out too fast |
| Site-to-site VPN between AWS and on-prem went down — no traffic passed for 3 hours | Phase 2 IPsec parameters mismatched: on-prem used AES256-SHA1, AWS tunnel expected AES128-SHA256. Tunnel appeared "up" at Phase 1 but dropped all data packets | Reconfigure AWS VPN tunnel to match on-prem phase 2 parameters. Add tunnel monitoring with CloudWatch alarms on `TunnelState`. Implement redundant tunnels (2 tunnels minimum) with BGP for automatic failover | **VPN tunnels can appear "up" but pass zero traffic.** Phase 2 parameter mismatch is silent — no error, no logs. Always configure redundant tunnels with BGP. Monitor tunnel data-in/data-out metrics, not just tunnel state. Test failover quarterly |
| Cross-region data transfer cost was 40% of total cloud bill | Chatty microservices were calling across regions without any data locality awareness — each request crossed a regional boundary | Re-architect: deploy a data-local copy of dependent services in each region. Use region-aware DNS (Route 53 latency-based routing) to keep traffic within region. Add inter-region data transfer cost alerts at $X threshold | **Inter-region networking costs sneak up on you.** Monitor inter-region data transfer from day one. Architect for data locality: services that communicate frequently should be in the same region. Set cost anomaly alerts before the CFO asks why the bill doubled |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Network topology diagram exists and is current — includes all VPCs, subnets, route tables, gateways, and interconnects
- [ ] **[S2]**  CIDR allocation plan documented with no overlaps; sufficient headroom for 3-year growth
- [ ] **[S3]**  Subnets properly tiered: public (IGW), private (NAT), isolated (no internet); one NAT gateway per AZ
- [ ] **[S4]**  Security groups use least-privilege: allow only required ports and sources; no 0.0.0.0/0 on databases
- [ ] **[S5]**  Security group referencing used for inter-service traffic (not CIDR ranges)
- [ ] **[S6]**  NACLs configured as defense-in-depth; ephemeral port ranges correct for return traffic
- [ ] **[S7]**  WAF deployed on all public endpoints with managed rule groups (OWASP Top 10, IP reputation)
- [ ] **[S8]**  DDoS protection enabled (Shield Standard minimum; Shield Advanced for critical workloads)
- [ ] **[S9]**  DNS: split-horizon with public zone (customer-facing) and private zone (internal services)
- [ ] **[S10]**  CDN configured with appropriate cache behaviors, origin shield enabled, access logs to S3
- [ ] **[S11]**  Load balancer health checks passing; access logs enabled; cross-zone load balancing on
- [ ] **[S12]**  VPC Flow Logs enabled on all VPCs; published to S3 + CloudWatch Logs
- [ ] **[S13]**  VPN/Direct Connect redundant (2 tunnels/connections minimum); BGP configured correctly
- [ ] **[S14]**  Service mesh (if applicable): mTLS enforced, authorization policies defined, control plane HA
- [ ] **[S15]**  Network automation: all resources in IaC (Terraform/Pulumi/CDK); changes via CI/CD pipeline
- [ ] **[S16]**  Monitoring: alarms on NAT gateway errors, VPN tunnel status, ALB 5xx rate, CDN cache hit rate
- [ ] **[S17]**  VPC endpoints for S3, DynamoDB, and other frequently accessed AWS services
- [ ] **[S18]**  IPv6 dual-stack (or plan documented); public IPv4 address inventory tracked
- [ ] **[S19]**  Network runbooks documented: common troubleshooting steps, escalation paths, contact info
- [ ] **[S20]**  Network cost review quarterly: data transfer, NAT gateway hours, public IPs, inter-AZ traffic

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/) — Core VPC, Transit Gateway, VPN, Direct Connect
- [AWS Well-Architected Framework — Networking](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/networking.html) — Reliability pillar networking
- [Azure Virtual Network Documentation](https://learn.microsoft.com/en-us/azure/virtual-network/) — VNet, peering, ExpressRoute
- [Google Cloud VPC Documentation](https://cloud.google.com/vpc/docs) — VPC, Shared VPC, Cloud Interconnect
- [Cloudflare Learning Center — CDN](https://www.cloudflare.com/learning/cdn/) — CDN fundamentals
- [Istio Service Mesh Documentation](https://istio.io/latest/docs/) — Service mesh patterns, mTLS, traffic management
- [Cilium / eBPF Networking](https://docs.cilium.io/) — Next-gen networking with eBPF
- [BGP Fundamentals](https://www.amazon.com/BGP-Design-Implementation-Randy-Zhang/dp/1587144442/) — Randy Zhang, Micah Bartell
- [TCP/IP Illustrated, Volume 1](https://www.amazon.com/TCP-Illustrated-Protocols-Addison-Wesley-Professional/dp/0321336313/) — W. Richard Stevens
- [Zero Trust Networks](https://www.oreilly.com/library/view/zero-trust-networks/9781492096592/) — Evan Gilman, Doug Barth
- [IPv6 Address Planning](https://www.oreilly.com/library/view/ipv6-address-planning/9781491908259/) — Tom Coffeen
- [references/cidr-calculator-guide.md](references/cidr-calculator-guide.md) — CIDR math and allocation patterns
- [references/network-cost-model.md](references/network-cost-model.md) — Data transfer cost calculator across cloud providers
