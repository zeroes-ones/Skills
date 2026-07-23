# Core Workflow — Full Implementation

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
