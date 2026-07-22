---
author: Sandeep Kumar Penchala
type: reference
domain: network-architecture
version: "1.0"
last_updated: 2026-07-21
parent_skill: networking-engineer
---

# Network Topology Patterns

> **Author:** Sandeep Kumar Penchala

A reference of battle-tested network topology patterns for cloud-native and hybrid infrastructure. Covers VPC/hub-spoke design, service mesh architectures, CDN topology, DNS design, load balancing strategies, zero trust networking, and multi-region connectivity. Use alongside the Networking Engineer skill's architecture design and troubleshooting workflows.

---

## 1. VPC / Hub-Spoke Topology

### Architecture description

```
                    ┌──────────────────────────┐
                    │      TRANSIT GATEWAY      │
                    │         (Hub VPC)          │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │  Shared Services    │  │
                    │  │  • NAT GW           │  │
                    │  │  • VPN/Direct Connect│  │
                    │  │  • Firewall/IDS     │  │
                    │  │  • Monitoring       │  │
                    │  └─────────────────────┘  │
                    └──┬───────┬───────┬────────┘
                       │       │       │
              ┌────────▼┐ ┌────▼──┐ ┌──▼────────┐
              │ SPOKE A │ │SPOKE B│ │ SPOKE C   │
              │ (Prod)  │ │(Stag) │ │ (Dev)     │
              │         │ │       │ │           │
              │ 10.1.0  │ │10.2.0 │ │ 10.3.0    │
              │ /16     │ │/16    │ │ /16       │
              └─────────┘ └───────┘ └───────────┘
```

### Routing configuration (AWS Transit Gateway example)

```hcl
# Terraform: Hub-spoke with Transit Gateway
resource "aws_ec2_transit_gateway" "main" {
  description                     = "Main hub TGW"
  amazon_side_asn                = 64512
  default_route_table_association = "disable"
  default_route_table_propagation = "disable"
  auto_accept_shared_attachments  = "enable"
}

# Hub VPC attachment
resource "aws_ec2_transit_gateway_vpc_attachment" "hub" {
  subnet_ids         = aws_subnet.hub_tgw[*].id
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = aws_vpc.hub.id

  transit_gateway_default_route_table_association = false
  transit_gateway_default_route_table_propagation = false
}

# Route: spoke → 0.0.0.0/0 → TGW → hub → NAT GW → internet
resource "aws_ec2_transit_gateway_route" "spoke_to_internet" {
  destination_cidr_block         = "0.0.0.0/0"
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.hub.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.spoke.id
}

# Route: hub → spoke CIDRs → TGW → spoke (for return traffic)
resource "aws_ec2_transit_gateway_route" "hub_to_spoke" {
  for_each = toset(["10.1.0.0/16", "10.2.0.0/16", "10.3.0.0/16"])
  destination_cidr_block         = each.value
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.hub.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.hub.id
}
```

### When to use hub-spoke
```
✅ Multi-account AWS organizations (> 3 accounts)
✅ Centralized egress (all traffic exits through hub)
✅ Shared services: monitoring, logging, CI/CD runners
✅ Consistent security posture (inspect all cross-VPC traffic)

❌ Single VPC application (overkill)
❌ High-throughput cross-spoke traffic (TGW adds latency + cost)
❌ When spokes need direct peering for latency-sensitive workloads
```

### VPC CIDR planning
```
| Environment | CIDR        | IPs available | Purpose          |
|-------------|-------------|---------------|------------------|
| Hub         | 10.0.0.0/16 | 65,536        | Shared services  |
| Prod        | 10.1.0.0/16 | 65,536        | Production       |
| Staging     | 10.2.0.0/16 | 65,536        | Pre-production   |
| Dev         | 10.3.0.0/16 | 65,536        | Development      |
| Sandbox     | 10.4.0.0/16 | 65,536        | Experiments      |
| DMZ         | 172.16.0.0/16| 65,536       | Public-facing    |

Rule: Never overlap CIDRs — reserve /16s even if not fully used.
```

---

## 2. Service Mesh Patterns

### Sidecar vs Ambient

```
SIDECAR (Istio/Linkerd classic):
┌──────────────┐
│   Service A  │
│  ┌────────┐  │
│  │ Envoy  │──┼─────── mTLS ────────┐
│  │ proxy  │  │                     │
│  └────────┘  │              ┌──────▼───────┐
└──────────────┘              │  Service B   │
                              │ ┌────────┐   │
                              │ │ Envoy  │   │
                              │ │ proxy  │   │
                              │ └────────┘   │
                              └──────────────┘
Each pod has an injected sidecar container.
Proxy handles all ingress/egress.

AMBIENT (Istio ambient mesh):
┌──────────────┐     ┌──────────────┐
│   Service A  │     │   Service B  │
│   (no proxy) │     │   (no proxy) │
└──────┬───────┘     └──────┬───────┘
       │                    │
       ▼                    ▼
┌──────────────────────────────────────┐
│       Node-level ztunnel             │  ← Per-node, not per-pod
│       (L4: mTLS, authN, authZ)      │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│       Waypoint proxy (L7)            │  ← Per-identity, optional
│       (traffic splitting, retries)   │
└──────────────────────────────────────┘

Trade-offs:
| Aspect          | Sidecar                      | Ambient                       |
|-----------------|------------------------------|-------------------------------|
| Resource cost   | Per-pod overhead (~50MB+)   | Shared per-node (cheaper)    |
| Latency         | +1–2ms per hop              | +0.5–1ms (L4 only)          |
| L7 features     | Full (retries, splitting)   | Waypoint proxy required       |
| Upgrade         | Restart every pod            | Transparent node-level        |
| Maturity        | Battle-tested (2017+)        | Newer (2023+)                 |
```

### Key service mesh features
```yaml
# Istio VirtualService — Traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-rollout
spec:
  hosts:
    - reviews
  http:
    - match:
        - headers:
            end-user:
              exact: beta-tester
      route:
        - destination:
            host: reviews
            subset: v2        # Beta testers → v2
          weight: 100
    - route:
        - destination:
            host: reviews
            subset: v1         # Everyone else → v1
          weight: 90
        - destination:
            host: reviews
            subset: v2         # 10% canary
          weight: 10
---
# DestinationRule — Circuit breaking
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews-cb
spec:
  host: reviews
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50
```

---

## 3. CDN Architecture

### Origin shield topology
```
CLIENTS GLOBALLY
    │     │     │
    ▼     ▼     ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Edge POP    │  │  Edge POP    │  │  Edge POP    │
│  (Frankfurt) │  │  (Singapore) │  │  (Virginia)   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │ Cache miss       │ Cache miss       │ Cache miss
       ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────┐
│                 ORIGIN SHIELD                         │
│              (Single mid-tier cache)                   │
│         All edge misses coalesce here                  │
└──────────────────────────┬───────────────────────────┘
                           │ Only true miss
                           ▼
                    ┌──────────────┐
                    │   ORIGIN     │
                    │  (Your app)  │
                    └──────────────┘
```

### Cache hierarchy and invalidation strategies
```
TTL STRATEGY BY CONTENT TYPE:
| Content           | TTL       | Invalidation              |
|-------------------|-----------|---------------------------|
| Static assets     | 1 year    | Cache-busting (hash in URL)|
| HTML pages        | 5–15 min  | Purge on deploy           |
| API responses     | Varies    | Surrogate keys / tags     |
| User-specific     | 0 (bypass)| Not cached                |
| Config/feature flag| 30–60s  | Purge by tag              |

SURROGATE KEY PATTERN (Fastly / Cloudflare):
Response header: Surrogate-Key: product-42 category-shoes
Purge request:    PURGE / with Surrogate-Key: product-42
                  → Invalidates ALL cached responses for product 42
                  across all edge POPs in < 150ms
```

### CDN security headers
```nginx
# CDN edge configuration
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
add_header X-Content-Type-Options "nosniff";
add_header X-Frame-Options "DENY";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.example.com; img-src * data:;";
```

---

## 4. DNS Design

### Split-horizon DNS
```
                    ┌─────────────────────┐
                    │   DNS RESOLVER      │
                    │                     │
                    │ Internal clients:   │
                    │  db.internal →      │
                    │  10.1.2.3            │
                    │                     │
                    │ External clients:   │
                    │  db.example.com →   │
                    │  203.0.113.5         │
                    └─────────────────────┘
```

### Geo-routing with latency-based routing (Route 53)
```
ALIAS RECORDS:
api.example.com → latency-based routing
  ├── us-east-1  → api-us.example.com (latency: 20ms for East Coast)
  ├── eu-west-1  → api-eu.example.com (latency: 30ms for Europe)
  └── ap-southeast-1 → api-ap.example.com (latency: 40ms for Asia)

FAILOVER RECORDS:
app.example.com → primary: us-east-1 (health check: /health, 30s interval)
                  secondary: us-west-2 (activated on 3 consecutive failures)
```

### TTL strategy
```
| Record type       | TTL      | Rationale                                     |
|-------------------|----------|-----------------------------------------------|
| A/AAAA (static)   | 86400    | Stable IP — cache aggressively                 |
| A (dynamic/ELB)   | 60–300   | IP can change; balance freshness vs load       |
| CNAME (CDN)       | 300      | Allows CDN origin changes within 5 min         |
| MX                | 86400    | Mail server IPs rarely change                  |
| TXT (SPF/DKIM)    | 86400    | Rarely changes                                 |
| TXT (verification)| 3600     | Temporary — reduce after verified              |
| NS                | 172800   | Delegation records — cache aggressively        |
| SOA               | 900–3600 | Zone refresh timing                            |

ANTI-PATTERN: Setting all records to TTL=300 because "what if we need to change?"
→ Increases DNS latency and cost; set appropriate TTLs.
```

### DNSSEC chain
```
Root (.) ──DS──► .com ──DS──► example.com ──DS──► sub.example.com
   │                │               │                    │
   KSK/ZSK         KSK/ZSK        KSK/ZSK             KSK/ZSK
   signs            signs           signs               signs

Key roles:
  KSK (Key Signing Key):   Signs the DNSKEY record set. Rotate annually.
  ZSK (Zone Signing Key):  Signs individual records. Rotate monthly.
  DS (Delegation Signer):  Hash of KSK stored in parent zone. Establishes chain of trust.
```

---

## 5. Load Balancing Patterns

### L4 vs L7 load balancing

```
| Aspect            | L4 (TCP/UDP)             | L7 (HTTP/HTTPS)              |
|-------------------|--------------------------|------------------------------|
| OSI layer         | Transport (4)            | Application (7)              |
| Routing decision  | IP + port                | URL path, headers, cookies   |
| TLS termination   | Pass-through or at LB    | At LB (most common)          |
| Sticky sessions   | Source IP hash           | Cookie-based                 |
| Use cases         | Databases, game servers  | Web apps, APIs, microservices|
| Latency           | Very low (< 1ms)         | Low (1–5ms)                  |
| Examples          | HAProxy (L4 mode), NLB   | NGINX, Envoy, ALB, Traefik   |
```

### Load balancing algorithms

| Algorithm | How it works | Best for |
|-----------|-------------|----------|
| **Round-robin** | Distribute sequentially: A→B→C→A… | Homogeneous backends; stateless services |
| **Least connections** | Send to backend with fewest active connections | Variable request duration; WebSocket |
| **IP hash** | Hash client IP → consistent backend | Sticky sessions without cookies |
| **Weighted** | Distribute proportionally by weight | Heterogeneous backends (bigger = more traffic) |
| **Least response time** | Send to fastest-responding backend | Latency-sensitive; backends at different distances |

### Health check design
```
Active health checks:
  GET /health → 200 OK  → Healthy
  Any 5xx or timeout   → Unhealthy (retry 3 times before marking down)

Passive health checks (outlier detection):
  If backend returns 5xx > 5 times in 30s window → temporarily eject for 60s

Health check endpoint requirements:
  - Lightweight (< 10ms, no DB query)
  - Checks actual dependencies (not just "server is up")
  - Returns JSON: {"status":"ok","version":"2.1.0","dependencies":{"db":"ok","cache":"ok"}}
```

---

## 6. Zero Trust Networking

### BeyondCorp principles
```
1. ACCESS TIED TO IDENTITY, NOT NETWORK LOCATION
   - Being on the office network grants zero additional privileges
   - Every access decision based on: user identity + device trust + context

2. ACCESS POLICIES ARE DYNAMIC
   - Device posture (OS patch level, disk encryption, approved device)
   - User role + group membership (from IdP)
   - Context: time of day, geo-location, session risk score

3. ALL TRAFFIC IS ENCRYPTED & AUTHENTICATED
   - mTLS between all services — no "trusted internal network"
   - Every service-to-service call requires authentication
```

### Identity-aware proxy architecture
```
User ──► Identity-Aware Proxy (IAP) ──► Application
              │
              ▼
         ┌─────────┐
         │  IdP    │  (Okta, Azure AD, Google Identity)
         │  OIDC   │
         └─────────┘
              │
              ▼
         ┌─────────┐
         │  Policy │  "Allow: eng-team + corp-device + MFA + US-only"
         │  Engine │  "Deny:  personal-device OR no-MFA"
         └────┬────┘
              │
    ┌─────────▼─────────┐
    │ Device Trust Store │  OS version, disk encryption, firewall status
    └───────────────────┘

Tools: Google IAP, Cloudflare Access, Pomerium, Ory Oathkeeper
```

### Microsegmentation
```
Traditional:
┌──────────────────────────────┐
│       PRODUCTION VPC         │
│                              │
│  ┌─────┐  ┌─────┐  ┌─────┐  │  ← All services can reach each other
│  │ App │  │ DB  │  │Cache│  │     within the VPC
│  └─────┘  └─────┘  └─────┘  │
└──────────────────────────────┘

Microsegmented:
┌──────────────────────────────┐
│       PRODUCTION VPC         │
│                              │
│  ┌─────┐     ┌─────┐        │
│  │ App │────▶│ DB  │        │  ← Only App → DB (port 5432)
│  └──┬──┘     └─────┘        │
│     │                        │
│     ▼       ┌─────┐         │
│  ┌─────┐    │Cache│         │  ← Only App → Cache (port 6379)
│  │ App │───▶│     │         │     DB ↛ Cache, App1 ↛ App2
│  └─────┘    └─────┘         │
└──────────────────────────────┘

Implementation: Security groups per service, Kubernetes NetworkPolicies, service mesh authZ
```

### NetworkPolicy example (Kubernetes)
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-access
spec:
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-server     # Only API server pods can reach DB
      ports:
        - protocol: TCP
          port: 5432
    # No other ingress — even in same namespace
```

---

## 7. Multi-Region Networking

### Transit gateway + Global Accelerator
```
┌────────────────────────────┐     ┌────────────────────────────┐
│     REGION: us-east-1      │     │     REGION: eu-west-1       │
│                            │     │                            │
│  ┌─────────┐ ┌─────────┐  │     │  ┌─────────┐ ┌─────────┐   │
│  │  VPC A  │ │  VPC B  │  │     │  │  VPC C  │ │  VPC D  │   │
│  └────┬────┘ └────┬────┘  │     │  └────┬────┘ └────┬────┘   │
│       └──────┬────┘        │     │       └──────┬────┘        │
│              │              │     │              │             │
│       ┌──────▼──────┐      │     │       ┌──────▼──────┐      │
│       │  TGW us-east│◄─────┼─────┼──────►│  TGW eu-west│      │
│       └─────────────┘      │     │       └─────────────┘      │
└────────────────────────────┘     └────────────────────────────┘
              │                                   │
              └──────────────┬────────────────────┘
                             │
                  ┌──────────▼──────────┐
                  │  Global Accelerator  │   ← Anycast IP: 13.248.x.x
                  │  (2 static anycast)  │      Routes to nearest healthy region
                  └─────────────────────┘
                             │
                     ┌───────▼───────┐
                     │   END USERS   │
                     └───────────────┘
```

### Multi-region routing strategies
```
| Strategy            | How it works                         | Use case            |
|---------------------|--------------------------------------|---------------------|
| Latency-based       | Route to lowest-latency region       | Global user base, active-active |
| Geo-proximity       | Route by user location (GDPR)        | Data residency requirements |
| Weighted            | Split traffic % across regions       | Canary region rollout, blue-green |
| Failover            | Active-Passive: primary → secondary  | DR, RPO/RTO requirements |
```

### Multi-region data considerations
```
SYNCHRONOUS REPLICATION:
  - Zero data loss (RPO=0)
  - Max distance ~500km (latency ceiling: ~5ms round-trip)
  - Each write waits for replica ACK → higher write latency
  - Example: PostgreSQL synchronous_commit = 'remote_write'

ASYNCHRONOUS REPLICATION:
  - Sub-second lag typical (< 1s)
  - Minimal write latency impact
  - Potential data loss on failover (RPO = replication lag)
  - Example: PostgreSQL streaming replication, DynamoDB Global Tables

EVENTUAL CONSISTENCY (Active-Active):
  - Conflict resolution required (LWW, CRDTs, custom merge)
  - DynamoDB Global Tables: last-writer-wins
  - CockroachDB: serializable across regions (but high latency)
```

---

See also: Networking Engineer skill for network design, troubleshooting, and performance optimization.
