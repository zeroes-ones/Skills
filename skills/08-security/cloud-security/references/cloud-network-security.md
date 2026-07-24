# Cloud Network Security Architecture

Reference for hardening cloud network security across AWS (VPC), Azure (VNet), and GCP (VCN). Covers segmentation, security groups, NACLs, private endpoints, WAF, DDoS, and egress filtering.

---

## VPC/VNet/VCN Segmentation Strategy

### Account-Level Isolation

Separate accounts/projects per environment is the strongest isolation primitive in the cloud. Network segmentation within an account is a secondary control — it cannot replace account-level boundaries.

**Recommended structure:**
- **Security/Audit account**: Centralized CloudTrail, GuardDuty, Security Hub, Config aggregator, centralized ingress/egress
- **Shared Services account**: Transit Gateway, Directory Service, CI/CD runners, container registry, secrets manager
- **Production accounts**: One per application tier (web, app, data) or per bounded context
- **Development/Sandbox accounts**: Scoped-down SCPs, spending limits, no production data access

### Subnet Architecture

```
VPC/VNet/VCN: 10.0.0.0/16
├── Public Subnets (10.0.0.0/24, 10.0.1.0/24)    — ALB, NAT Gateway, Bastion only
├── Private App Subnets (10.0.16.0/20, 10.0.32.0/20) — Application instances, no public IPs
├── Private Data Subnets (10.0.64.0/20, 10.0.80.0/20) — RDS, ElastiCache, no internet access
└── Private Endpoint Subnets (10.0.128.0/24) — VPC endpoints for AWS services
```

**Key rules:**
1. Public subnets: Application Load Balancers and NAT Gateways only — never application instances
2. Private subnets: No direct internet access; outbound via NAT Gateway or VPC endpoints
3. Database subnets: No internet access at all (no NAT Gateway route); only VPC endpoint access

## Private Endpoints / PrivateLink

VPC endpoints eliminate the need for internet/NAT Gateway access to AWS services:

| Service | Endpoint Type | Why |
|---------|--------------|-----|
| S3 | Gateway endpoint | Free, route table entry |
| DynamoDB | Gateway endpoint | Free, route table entry |
| KMS | Interface endpoint | $0.01/hr + $0.01/GB |
| SSM / EC2 Messages | Interface endpoint | Required for Session Manager in private subnets |
| ECR (both endpoints) | Interface endpoint | Pull images without NAT Gateway |
| CloudWatch Logs | Interface endpoint | Send logs without NAT Gateway |
| STS | Interface endpoint | Assume role without NAT Gateway |

**Cost comparison:** A NAT Gateway costs $32.85/month + $0.045/GB data processed. For a VPC with 500GB/month of S3 data transfer, VPC endpoints save ~$55/month and eliminate internet-exposed paths.

## Security Groups vs NACLs

| Feature | Security Groups | NACLs |
|---------|----------------|-------|
| Stateful? | Yes (return traffic auto-allowed) | No (must allow both directions) |
| Scope | Per ENI (instance-level) | Per subnet |
| Default | Deny all inbound, allow all outbound | Allow all |
| Rule evaluation | All rules evaluated | First matching rule wins (by number) |
| Use case | Primary access control | Defense-in-depth, broad subnet restrictions |

**Layering strategy:**
- Security groups: Fine-grained, per-workload rules (e.g., "App server SG allows 443 from ALB SG only")
- NACLs: Coarse, subnet-level deny rules (e.g., "Deny all traffic from known-malicious IPs at subnet boundary")

## WAF Architecture

### AWS WAF Deployment Model

Deploy WAF on CloudFront (global) or ALB/API Gateway (regional). Use AWS Managed Rules:
- **Core Rule Set (CRS)**: OWASP Top 10 protection (SQLi, XSS, LFI, RFI)
- **SQL Database**: Additional SQL injection rules for RDS
- **PHP/WordPress**: Application-specific rules
- **IP Reputation**: Block known malicious IPs from AWS threat intelligence
- **Rate-based rules**: 2000 req/5min per IP (adjustable)

### DDoS Mitigation Tiers

| Tier | Service | Cost | Protection |
|------|---------|------|------------|
| Basic | AWS Shield Standard | Free | Automatic L3/L4 protection on all AWS services |
| Advanced | AWS Shield Advanced | $3,000/month (1yr) | L3/L4 + L7, 24/7 DRT access, cost protection for scaling |
| Premium (Azure) | Azure DDoS Protection Standard | $2,944/month | Always-on traffic monitoring, adaptive tuning, DDoS Rapid Response |
| Standard (GCP) | Cloud Armor Standard | Free + $0.75/million requests | L3/L4 protection, WAF rate limiting, Adaptive Protection |

## Egress Filtering

Default deny outbound is critical for data exfiltration prevention:

1. **DNS-layer filtering**: Route 53 Resolver DNS Firewall blocks known malicious domains
2. **Forward proxy**: Squid/Envoy for HTTP/HTTPS with domain allowlisting
3. **AWS Network Firewall** / **Azure Firewall** / **GCP Cloud NGFW**: Stateful L7 inspection
4. **VPC Flow Logs**: Publish to S3 + CloudWatch, analyze with GuardDuty for anomalous traffic
