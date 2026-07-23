# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Discovery & Infrastructure Audit
1. **Inventory & Classification** — Catalog every resource across accounts/projects. Identify snowflake servers, untagged resources, and resources not managed by IaC. Use `aws resourcegroupstaggingapi`, `gcloud asset search-all-resources`, or cloud asset inventory tools.
2. **Architecture Mapping** — Diagram network topology (VPC peering, transit gateway, PrivateLink), data flows, and service dependencies. Document environment topology: dev → staging → UAT → production → DR.
3. **Maturity Assessment** — Evaluate IaC coverage (%), CI/CD adoption, observability posture, incident response process. Score 1-5 on each DORA capability.
4. **Security & Compliance Constraints** — Map regulatory requirements (SOC2, HIPAA, PCI-DSS, GDPR) to infrastructure controls: network segmentation, encryption requirements, data residency, audit logging.

### Phase 2 (~30 min): Infrastructure as Code Design
1. **Tool Selection Matrix**

   | Factor | Terraform | Pulumi | CDK (AWS/Bicep) |
   |---|---|---|---|
   | Ecosystem breadth | ★★★★★ 3,000+ providers | ★★★ Growing, Terraform bridge | ★ AWS/Azure native only |
   | Language flexibility | HCL only | TypeScript, Python, Go, C#, Java | TypeScript, Python, Java, .NET |
   | State management | Self-managed (S3, GCS) or TFC | Pulumi Cloud or self-managed | Cloud-native (CloudFormation) |
   | Testing | Terratest, `terraform test` | Standard test frameworks | CDK assertions, fine-grained |
   | **Best when** | Broad multi-cloud, ops teams | Developer-owned infra, complex logic | Single-cloud, AWS/Azure-native shops |

2. **Repository Structure** — Separate repos per bounded context; never monolithic "infra" repo:
   ```
   infra-networking/     # VPCs, subnets, peering, transit gateway, DNS
   infra-security/       # IAM, KMS, SCPs, security groups, WAF
   infra-compute/        # EKS, ECS, Lambda, ASGs
   infra-data/           # RDS, DynamoDB, ElastiCache, S3 policies
   ```
   Within each repo: `modules/`, `environments/{dev,staging,prod}/`, `global/`

3. **Remote State** — Per-environment, per-component state with locking:
   ```
   s3://org-terraform-state/prod/us-east-1/networking/terraform.tfstate
   s3://org-terraform-state/prod/us-east-1/compute/terraform.tfstate
   ```
   State encryption via KMS; access logged via CloudTrail; alerts on unauthorized reads.

4. **Module Design** — Small, composable, single-purpose. Versioned by git tag (never `main` branch). Every module exports: ARN/ID, endpoint, security group.

5. **Secrets in IaC** — Never in plaintext `.tfvars`. Patterns:
   - `data "aws_secretsmanager_secret_version"` at plan time
   - HashiCorp Vault dynamic database credentials with lease TTL
   - SOPS + age/KMS for encrypted-in-git secrets (decrypted by CI)
   - `sensitive = true` on all secret variables

6. **Policy as Code Pipeline**:
   ```
   pre-commit → terraform fmt -check → terraform validate → checkov/OPA scan → plan → apply
   ```
   High/critical violations block apply. Drift detection: `terraform plan` on cron every 6 hours → alert on non-empty diff.

### Phase 3 (~20 min): GitOps & Deployment Architecture
1. **GitOps Agent Selection** — Argo CD for enterprise (UI, SSO, multi-tenancy, ApplicationSets); Flux for lightweight, OCI-native, Kustomize-first teams.

2. **Application Patterns**:
   - **App of Apps** — Bootstrap Application that discovers child Applications from Git
   - **ApplicationSet** — Template-based multi-cluster/multi-tenant with list, cluster, git, PR generators
   - **PR Generator** — Ephemeral preview environments per pull request, auto-teardown on close

3. **Sync Policy Configuration**:
   ```yaml
   syncPolicy:
     automated:
       prune: true       # Delete resources removed from Git
       selfHeal: true    # Revert manual changes within 5s
     syncWindows:        # Blackout during maintenance
       - schedule: "0 2 * * 1"  # Monday 2 AM
         duration: 2h
         kind: deny
   ```


**What good looks like:** `terraform plan` produces no unexpected changes. CI/CD pipeline deploys to staging in under 10 minutes and production in under 15. Rollback completes in under 5 minutes. All secrets are managed through a vault — zero plaintext credentials in repo.

4. **Deployment Strategy Decision Tree**:
   ```
   Need zero-downtime deploy?
   ├─ Rolling update (Kubernetes default) — Good enough for stateless services
   ├─ Blue-Green — Full duplicate environment, instant rollback, 2x resource cost
   │   └─ Best for: Stateful services, database schema changes, critical releases
   ├─ Canary — Incremental traffic shift with automated analysis
   │   └─ Best for: High-traffic services, risk-averse organizations
   └─ Feature Flags — Decouple deploy from release
       └─ Best for: Continuous delivery, A/B testing, kill switches
   ```

5. **Progressive Delivery with Argo Rollouts**:
   ```yaml
   strategy:
     canary:
       steps:
         - setWeight: 10    # 10% to canary
         - pause: {duration: 5m}
         - analysis:        # Automated metric check
             templates:
               - templateName: error-rate-check
         - setWeight: 50
         - pause: {duration: 10m}
         - setWeight: 100   # Full promotion (or rollback on analysis failure)
   ```

6. **Deployment Gates** — Each environment promotion requires:
   - Smoke tests passing (critical path synthetic transactions)
   - Security scan passing (container CVE threshold, SAST gate)
   - SLO error budget > 50% remaining (automated: block if budget exhausted)
   - Manual approval for production (environment protection rules)

### Phase 4 (~15 min): Secret Management Lifecycle
1. **Hierarchy** — Vault as root of trust → cloud-native secret managers (AWS Secrets Manager, GCP Secret Manager) → Kubernetes Secrets via external-secrets operator or Vault Secrets Operator.

2. **Dynamic Secrets** — No static database credentials. Vault generates ephemeral credentials per application instance with lease TTL:
   ```hcl
   vault write database/roles/app-role \
     db_name=postgres-prod \
     creation_statements="CREATE USER \"{{name}}\" WITH PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
     default_ttl="1h" \
     max_ttl="24h"
   ```

3. **Rotation Automation** — Every secret must have a rotation schedule:
   | Secret Type | Rotation Frequency | Method |
   |---|---|---|
   | Database credentials | 7 days | Vault dynamic secrets or AWS RDS automatic rotation |
   | API keys | 30 days | Vault KV v2 with metadata-driven rotation script |
   | TLS certificates | 90 days | cert-manager with Let's Encrypt; auto-renew at 30-day remaining |
   | Service account keys | 90 days | Automated rotation pipeline; validate new key before revoking old |

4. **Kubernetes Secrets** — Encrypt at rest in etcd (`EncryptionConfiguration`). Never in plaintext manifests. External Secrets Operator syncs from cloud secret managers to Kubernetes Secrets:
   ```yaml
   apiVersion: external-secrets.io/v1beta1
   kind: ExternalSecret
   metadata:
     name: db-credentials
   spec:
     refreshInterval: 1h
     secretStoreRef:
       name: aws-secrets-manager
       kind: ClusterSecretStore
     target:
       name: db-credentials
     data:
       - secretKey: DB_PASSWORD
         remoteRef:
           key: /prod/myapp/db
           property: password
   ```

### Phase 5 (~25 min): Service Mesh Architecture
1. **Istio vs Linkerd Decision**:

   | Factor | Istio | Linkerd |
   |---|---|---|
   | Complexity | High — 10+ CRDs, Envoy sidecar | Low — purpose-built Rust proxy |
   | Features | Traffic splitting, fault injection, rate limiting, authorization (JWT/OAuth), WASM plugins | mTLS, retries, timeouts, circuit breaking, tap |
   | Resource overhead | ~150MB/sidecar | ~30MB/sidecar |
   | Multi-cluster | Native multi-cluster mesh | Multi-cluster via service mirroring |
   | **Best when** | Complex routing, multi-protocol, enterprise governance | Simplicity, low overhead, Kubernetes-only |

2. **mTLS Enforcement**:
   ```yaml
   # Istio PeerAuthentication — strict mTLS mesh-wide
   apiVersion: security.istio.io/v1beta1
   kind: PeerAuthentication
   metadata:
     name: default
     namespace: istio-system
   spec:
     mtls:
       mode: STRICT
   ```

3. **Traffic Splitting for Canary**:
   ```yaml
   apiVersion: networking.istio.io/v1beta1
   kind: VirtualService
   metadata:
     name: myapp
   spec:
     hosts:
       - myapp
     http:
       - route:
           - destination:
               host: myapp-stable
               subset: v1
             weight: 90
           - destination:
               host: myapp-canary
               subset: v2
             weight: 10
   ```

4. **Circuit Breaking** — Prevent cascading failures:
   ```yaml
   apiVersion: networking.istio.io/v1beta1
   kind: DestinationRule
   metadata:
     name: payment-service
   spec:
     host: payment-service
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

5. **Fault Injection** — Chaos testing in production:
   ```yaml
   http:
     - fault:
         delay:
           percentage:
             value: 10
           fixedDelay: 5s
         abort:
           percentage:
             value: 5
           httpStatus: 500
   ```

### Phase 6 (~25 min): Cost Optimization (FinOps)
1. **Tagging Governance** — Every resource tagged with `cost_center`, `environment`, `service`, `managed_by`. Enforced via SCP or OPA policy (block resource creation without tags).

2. **Commitment Discounts**:
   | AWS | GCP | Azure | Coverage Target |
   |---|---|---|---|
   | Reserved Instances (1y/3y) | Committed Use Discounts | Reserved VM Instances | 60-80% of stable baseline |
   | Savings Plans (Compute) | — | Savings Plan for Compute | 60-80% of compute spend |
   | Spot Instances | Preemptible VMs | Spot VMs | 20-40% of stateless workloads |

3. **Idle Resource Detection**:
   ```sql
   -- Cloudability / CloudHealth / custom query: find unattached resources
   SELECT resource_id, resource_type, monthly_cost
   FROM cloud_inventory
   WHERE last_access_time < NOW() - INTERVAL '30 days'
     AND resource_status = 'available'
   ORDER BY monthly_cost DESC;
   ```

4. **Rightsizing Automation** — Weekly analysis: identify over-provisioned instances (CPU < 20%, memory < 30% over 7d) → recommend downgrade. Identify under-provisioned instances → recommend upgrade.

5. **Anomaly Detection** — Monitor daily spend per cost center; alert on +20% deviation from 7-day rolling average.

### Phase 7 (~25 min): Disaster Recovery Implementation
1. **RPO/RTO Definition** — Business Impact Analysis → tiered classification:
   | Tier | RPO | RTO | Pattern | Example |
   |---|---|---|---|---|
   | Tier 0 — Mission Critical | < 1 min | < 15 min | Active-active multi-region | Payment API, Auth |
   | Tier 1 — Business Critical | < 15 min | < 1 hour | Pilot light + read replicas | Customer-facing apps |
   | Tier 2 — Important | < 1 hour | < 4 hours | Backup & restore | Internal tools |
   | Tier 3 — Non-Critical | < 24 hours | < 48 hours | Cold restore | Dev/staging |

2. **3-2-1 Backup Rule** — 3 copies, 2 different media, 1 off-site. Cloud-native: production + replica + cross-region snapshot. Object Lock for ransomware immutability.

3. **Failover Automation** — Terraform parameterized by `dr_active` boolean. Pipeline: verify replication health → promote replicas → scale compute → flip DNS → validate synthetic transactions.

4. **DR Testing Cadence** — Tabletop monthly, component failover quarterly, full regional failover annually. Measure actual RTO/RPO vs targets; every exercise generates postmortem action items.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | cloud-architect | Cloud architecture design and service selection |
| **This** | devops-engineer | Infrastructure as Code, GitOps workflows, deployment automation |
| **After** | ci-cd-builder | Pipeline that deploys the provisioned infrastructure |

Common chains:
- **Chain**: cloud-architect → devops-engineer → ci-cd-builder — Architecture becomes IaC; CI/CD pipeline automates infrastructure deployment
- **Chain**: system-architect → devops-engineer → site-reliability-engineer — System design drives infrastructure provisioning; SRE defines reliability targets for the deployed system
