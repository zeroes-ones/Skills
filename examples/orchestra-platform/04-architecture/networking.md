# Network Architecture

## VPC Design

CIDR block: `10.0.0.0/16` spanning 3 Availability Zones (us-east-1a, us-east-1b, us-east-1c). Each AZ contains one public subnet (for load balancers and NAT gateways) and one private subnet (for all application workloads). Subnet allocation: public subnets `/20`, private subnets `/19` to accommodate EKS node scaling.

## Subnet Topology

**Public Subnets** (10.0.0.0/20, 10.0.16.0/20, 10.0.32.0/20): Host the Application Load Balancer (ALB) and NAT Gateways. The ALB terminates TLS (ACM certificate, TLS 1.3 minimum) and routes to EKS ingress controllers in private subnets. NAT Gateways (one per AZ) provide outbound internet access for private resources (container image pulls, API calls to external services).

**Private Subnets** (10.0.64.0/19, 10.0.96.0/19, 10.0.128.0/19): Host EKS node groups (managed, t3.large minimum), RDS Aurora PostgreSQL clusters, and ElastiCache Redis clusters. No direct inbound internet access. Inter-service communication flows through Kubernetes network policies and Istio service mesh.

## DNS and CDN

Route53 hosts the `orchestra.dev` zone with latency-based routing between regions. CloudFront distribution serves static assets from S3 (`assets.orchestra.dev`) with a 1-year cache policy for versioned assets (`/static/v1.2.3/*`) and 5-minute cache for `index.html`. Origin shield enabled in us-east-1 to reduce S3 request load.

## WAF Configuration

AWS WAF WebACL associated with both the ALB and CloudFront distribution. Rule groups: AWS Managed Rules — Core Rule Set (SQL injection, XSS, path traversal), rate-based rule (1,000 requests per 5-minute window per IP, with a lower 200/min threshold on the `/api/auth/login` endpoint), IP reputation list blocking known malicious IPs, and geo-match blocking traffic from sanctioned countries.

## Zero-Trust Network

mTLS enforced between all services via Istio service mesh in STRICT mode. Certificates issued by cert-manager with a Let's Encrypt ClusterIssuer for internet-facing endpoints and a self-signed CA for internal service-to-service communication. No security group rules allow `0.0.0.0/0` ingress to application ports — all traffic flows through the ALB (public) or Istio ingress gateway (internal). Kubernetes NetworkPolicies enforce deny-by-default within the cluster, with explicit allow rules per service pairing. SSH access to nodes is replaced by AWS Systems Manager Session Manager (no open port 22).
