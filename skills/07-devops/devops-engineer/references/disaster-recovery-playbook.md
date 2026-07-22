# Disaster Recovery Playbook — Production Field Manual

## Table of Contents
1. [RPO/RTO Definition Methodology](#rporto-definition-methodology)
2. [Backup Strategy — The 3-2-1 Rule](#backup-strategy--the-3-2-1-rule)
3. [DR Architecture Patterns](#dr-architecture-patterns)
4. [Database DR — Per Engine](#database-dr--per-engine)
5. [Failover Automation](#failover-automation)
6. [DR Testing Cadence & Procedures](#dr-testing-cadence--procedures)
7. [Communication Runbook](#communication-runbook)
8. [Recovery Decision Tree](#recovery-decision-tree)

---

## RPO/RTO Definition Methodology

### Definitions
| Metric | Definition | Question It Answers |
|---|---|---|
| **RPO** (Recovery Point Objective) | Maximum acceptable data loss, measured in time | "How much data can we lose?" |
| **RTO** (Recovery Time Objective) | Maximum acceptable downtime, measured in time | "How long can we be down?" |

### Tiering Framework

| Tier | RPO | RTO | Example Systems | DR Pattern |
|---|---|---|---|---|
| **Tier 0 — Mission Critical** | < 1 min | < 15 min | Payment processing, auth, core API | Multi-region active-active |
| **Tier 1 — Business Critical** | < 15 min | < 1 hour | Customer-facing apps, order mgmt | Pilot light / warm standby |
| **Tier 2 — Important** | < 1 hour | < 4 hours | Internal tools, reporting | Warm standby, cross-region backup |
| **Tier 3 — Non-Critical** | < 24 hours | < 48 hours | Dev/staging, analytics (batch) | Backup & restore |

### RPO/RTO Calculation Method

```
1. Identify critical business functions via BIA (Business Impact Analysis)
2. Quantify revenue loss per hour of downtime per function
3. Map functions to technical systems
4. Rank by combined revenue impact + customer impact
5. Negotiate RPO/RTO with business stakeholders (cost of DR vs cost of downtime)

Revenue at Risk = (Annual Revenue / 8760 hours) × Hours of Downtime × % Revenue Dependent on System
```

**Anti-pattern:** "RPO=0, RTO=0 for everything." This is infinite cost for diminishing returns. Tier your systems.

---

## Backup Strategy — The 3-2-1 Rule

### The Rule
> **3** copies of data, on **2** different media types, with **1** copy off-site.

### Modern Interpretation

| Original | Cloud-Native Equivalent |
|---|---|
| 3 copies | Production + Replica + Backup snapshot |
| 2 media types | Primary (SSD) + Object storage (S3/GCS/Blob) |
| 1 off-site | Cross-region or cross-cloud backup |

### Backup Types by Recovery Speed

| Type | RTO | Cost | Use Case |
|---|---|---|---|
| **Snapshot** (point-in-time) | Seconds to minutes | Low-moderate | Databases, EBS volumes |
| **Continuous backup** (PITR) | Minutes | Moderate | RDS, DynamoDB, Cloud SQL |
| **Replication** (streaming) | Near-zero | High | Multi-region active-passive |
| **Logical dump** (pg_dump, mysqldump) | Hours | Low | Schema versioning, cross-cloud |
| **Object versioning** (S3/GCS) | Seconds | Low (storage) | Data lake, static assets |

### Backup Schedule Template

```yaml
# Per-database backup schedule
postgres-primary:
  snapshot_frequency: 1h
  snapshot_retention: 7d
  pitr_retention: 35d       # Point-in-time recovery
  cross_region_copy: true   # DR region
  logical_dump: 1d          # For cross-cloud portability

redis-cluster:
  snapshot_frequency: 1h
  snapshot_retention: 3d
  cross_region_copy: true

s3-data-lake:
  versioning: true
  cross_region_replication: true
  lifecycle:
    - transition_to_glacier: 90d
    - expire_versions: 365d
```

### Encryption & Access Control for Backups

| Requirement | Implementation |
|---|---|
| Encryption at rest | KMS-managed keys, separate key per backup tier |
| Encryption in transit | TLS 1.2+ for all cross-region replication |
| Access control | Separate IAM role for backup operations; read-only for DR team |
| Immutability | S3 Object Lock / GCS Retention Policy for ransomware protection |
| Audit logging | CloudTrail/Cloud Audit Logs on all backup access |

---

## DR Architecture Patterns

### 1. Active-Active (Multi-Region)

```
                    ┌──────────┐
                    │  Route 53 │  (Latency-based routing)
                    └────┬─────┘
              ┌──────────┴──────────┐
              ▼                     ▼
     ┌────────────────┐    ┌────────────────┐
     │  us-east-1      │    │  eu-west-1      │
     │  ─────────      │    │  ─────────      │
     │  EKS Cluster    │    │  EKS Cluster    │
     │  RDS (writer)   │    │  RDS (reader)   │
     │  ElastiCache    │◄──►│  ElastiCache    │
     │  DynamoDB Global │◄──►│  DynamoDB Global│
     └────────────────┘    └────────────────┘

Recovery: Automatic — DNS fails over healthy region
Cost: 2x+ baseline
RPO: < 1 sec (DynamoDB), < 1 min (RDS cross-region replication)
RTO: < 5 min (DNS propagation)
```

### 2. Pilot Light (Minimal Standby)

```
Production (us-east-1):           DR (eu-west-1):
┌─────────────────────┐           ┌──────────────────────┐
│ Full infrastructure  │           │ Minimal:              │
│ EKS (10 nodes)       │  ──────►  │ EKS (1 node, scaled)  │
│ RDS (db.r5.2xlarge)  │ replicate │ RDS (replica, promote)│
│ ElastiCache (3 nodes)│  data     │ ElastiCache (stopped) │
│ S3 (primary)         │◄────────►│ S3 (replication)      │
└─────────────────────┘           └──────────────────────┘

Recovery: Scale up DR region, promote DB replica, flip DNS
Cost: ~20% of production
RPO: < 1 min (replication lag)
RTO: < 30 min (scale-up + promotion)
```

### 3. Backup & Restore (Cold)

```
Recovery: Deploy infra from IaC, restore backups, configure DNS
Cost: < 5% of production
RPO: Depends on backup frequency (hourly snapshot = up to 1 hour loss)
RTO: 4-24 hours (infra provisioning + data restoration)
```

---

## Database DR — Per Engine

### PostgreSQL / RDS / Cloud SQL

```sql
-- Verify replication lag (must be < RPO threshold)
SELECT
  client_addr,
  state,
  pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS replication_lag_bytes,
  NOW() - pg_last_xact_replay_timestamp() AS replication_lag_time
FROM pg_stat_replication;

-- Alert: replication lag > 60s
```

```bash
# Promote read replica to primary (DR failover)
aws rds promote-read-replica \
  --db-instance-identifier dr-postgres-replica \
  --region eu-west-1

# OR for Cloud SQL
gcloud sql instances promote-replica dr-postgres-replica --project=prod-dr
```

### DynamoDB Global Tables

```yaml
# CloudFormation — multi-region DynamoDB
GlobalTable:
  Type: AWS::DynamoDB::GlobalTable
  Properties:
    TableName: Orders
    AttributeDefinitions:
      - AttributeName: OrderId
        AttributeType: S
    KeySchema:
      - AttributeName: OrderId
        KeyType: HASH
    BillingMode: PAY_PER_REQUEST
    Replicas:
      - Region: us-east-1
      - Region: eu-west-1
    StreamSpecification:
      StreamViewType: NEW_AND_OLD_IMAGES
```

**Recovery:** Fully automatic — writes to one region propagate to all replicas. Conflict resolution: last-writer-wins.

### S3 Cross-Region Replication

```json
{
  "Role": "arn:aws:iam::111111111111:role/s3-crr-role",
  "Rules": [
    {
      "Status": "Enabled",
      "Priority": 1,
      "DeleteMarkerReplication": { "Status": "Enabled" },
      "Filter": { "Prefix": "" },
      "Destination": {
        "Bucket": "arn:aws:s3:::dr-bucket-eu-west-1",
        "EncryptionConfiguration": {
          "ReplicaKmsKeyID": "arn:aws:kms:eu-west-1:111111111111:key/abc-123"
        }
      }
    }
  ]
}
```

### Redis / ElastiCache

```bash
# Create replication group with cluster mode, multi-AZ
aws elasticache create-replication-group \
  --replication-group-id prod-redis \
  --engine redis \
  --cache-node-type cache.r6g.large \
  --num-cache-clusters 3 \
  --multi-az-enabled \
  --automatic-failover-enabled

# DR: restore from snapshot to new cluster in DR region
aws elasticache create-replication-group \
  --replication-group-id dr-redis \
  --snapshot-name prod-redis-daily-snapshot \
  --region eu-west-1
```

---

## Failover Automation

### Declarative DR with Terraform

```hcl
# Variables toggled during DR event
variable "dr_active" {
  type    = bool
  default = false
}

# Primary region resources only when NOT in DR
resource "aws_db_instance" "primary" {
  count = var.dr_active ? 0 : 1

  identifier     = "prod-db"
  instance_class = "db.r6g.xlarge"
  # ...
}

# DR region resources only WHEN in DR
resource "aws_db_instance" "dr_promoted" {
  count = var.dr_active ? 1 : 0

  identifier            = "dr-db-promoted"
  replicate_source_db   = null  # Break replication
  instance_class        = "db.r6g.2xlarge"
  skip_final_snapshot   = false # Safety net
  # ...
}

# Switch DNS
resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.example.com"
  type    = "A"

  alias {
    name                   = var.dr_active ? aws_lb.dr.dns_name : aws_lb.primary.dns_name
    zone_id                = var.dr_active ? aws_lb.dr.zone_id : aws_lb.primary.zone_id
    evaluate_target_health = true
  }
}
```

### Automated Failover Pipeline

```yaml
# GitHub Actions — DR failover workflow
name: DR Failover
on:
  workflow_dispatch:
    inputs:
      target_region:
        description: 'Failover to region'
        required: true
        type: choice
        options: [eu-west-1, us-west-2]

jobs:
  preflight:
    runs-on: ubuntu-latest
    steps:
      - name: Verify replication health
        run: |
          LAG=$(aws rds describe-db-instances --db-instance-identifier dr-replica \
            --region ${{ inputs.target_region }} \
            --query 'DBInstances[0].ReadReplicaDBInstanceIdentifiers' --output text)
          if [ -z "$LAG" ]; then echo "Replica already promoted or missing"; exit 1; fi
      - name: Announce failover start
        run: |
          slack-notify "@channel DR FAILOVER INITIATED to ${{ inputs.target_region }}. ETA: 15 minutes."

  promote_data:
    needs: preflight
    steps:
      - run: aws rds promote-read-replica --db-instance-identifier dr-replica --region ${{ inputs.target_region }}
      - run: aws rds wait db-instance-available --db-instance-identifier dr-replica --region ${{ inputs.target_region }}

  scale_compute:
    needs: preflight
    steps:
      - run: aws eks update-nodegroup-config --cluster-name prod-dr --nodegroup-name workers --scaling-config minSize=10,desiredSize=10,maxSize=30 --region ${{ inputs.target_region }}

  flip_dns:
    needs: [promote_data, scale_compute]
    steps:
      - run: |
          terraform apply -auto-approve -var="dr_active=true" -var="dr_region=${{ inputs.target_region }}"
      - run: slack-notify "DNS cutover complete. Monitoring for 10 minutes."

  validate:
    needs: flip_dns
    steps:
      - run: |
          for i in {1..20}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
            if [ "$STATUS" == "200" ]; then
              slack-notify "DR FAILOVER SUCCESSFUL. API responding 200."
              exit 0
            fi
            sleep 30
          done
          slack-notify "@channel DR FAILOVER VALIDATION FAILED. Manual intervention required."
          exit 1
```

---

## DR Testing Cadence & Procedures

### Testing Schedule

| Test Type | Frequency | Scope | Participants |
|---|---|---|---|
| **Tabletop walkthrough** | Monthly | Key DR scenarios, communication flow | SRE leads, engineering managers |
| **Failover simulation** | Quarterly | Single tier (e.g., promote DB replica) | SRE team |
| **Full DR exercise** | Annually | Complete region failover, all tiers | All engineering |
| **Chaos engineering** | Continuous | Inject faults in production (game days) | SRE + service teams |

### Tabletop Exercise Agenda (60 min)

```
00:00-05:00 — Scenario briefing (e.g., "us-east-1 is unreachable")
05:00-20:00 — Teams triage independently: identify impacted services, assess data loss
20:00-35:00 — War room: collate findings, decide on failover vs wait-and-see
35:00-50:00 — Execute failover (roles switch: SRE runs playbook, observability monitors)
50:00-60:00 — Debrief: what worked? What didn't? Action items captured
```

### Full DR Exercise Success Criteria

- [ ] All Tier 0/1 services operational in DR region within RTO
- [ ] Data consistency verified: record counts match between primary backup and DR
- [ ] Synthetic transactions pass: login, checkout, search, core API calls
- [ ] Monitoring dashboard shows healthy metrics after failover
- [ ] All PagerDuty alerts acknowledged and resolved
- [ ] Communication completed per runbook template
- [ ] Rollback plan validated: fail back to primary region

---

## Communication Runbook

### Declaring a DR Event

```
Subject: INCIDENT: Production Region Failure — DR Failover Initiated

Severity: SEV0
Region Impacted: us-east-1
Time Detected: 2026-07-21T14:32:00Z
Current Status: DR failover to eu-west-1 in progress

What happened: us-east-1 connectivity lost. AWS health dashboard shows EC2/EKS degraded.
Customer impact: All services unavailable in us-east-1. ~15% of users affected (geo-routing).

Actions in progress:
- [x] Incident commander designated: @jane-sre
- [x] DR failover initiated to eu-west-1 (runbook: https://wiki/dr-failover)
- [ ] Promoting DB replicas (ETA: 5 min)
- [ ] Scaling compute in eu-west-1 (ETA: 8 min)
- [ ] DNS cutover (ETA: 10 min)

Next update: 15:00 UTC or on status change
```

### Post-DR Status Updates

```
UPDATE [15:05 UTC]: DB replicas promoted. Compute scaled to 10 nodes. DNS propagating.
UPDATE [15:12 UTC]: DNS propagated. 95% of traffic served from eu-west-1. Monitoring.
UPDATE [15:20 UTC]: All services healthy. SEV0 downgraded to SEV2 — monitoring for 24h.
```

### Postmortem Template

```
## DR Failover Postmortem — [Date]

### Timeline (UTC)
- 14:32 — us-east-1 outage detected (CloudWatch alarm)
- 14:33 — Incident declared; DR runbook opened
- 14:38 — War room established; failover decision made
- 14:45 — DB replica promotion initiated
- 14:50 — Compute scaling triggered
- 15:05 — DNS cutover completed
- 15:12 — 95% traffic migrated
- 15:20 — All clear

### RPO/RTO Compliance
- Target RTO: 15 min | Actual: 33 min | Delta: +18 min
- Target RPO: 1 min | Actual: ~2 min (replication lag spike) | Delta: +1 min

### What Went Well
- Runbook was clear and followed correctly
- Automated failover pipeline worked for DB and compute
- Communication was timely and accurate

### What Went Wrong
- DNS TTL was 300s, causing 5-min propagation delay — reduce to 60s
- Manual step required to update ConfigMap references from us-east-1 to eu-west-1 — automate
- On-call engineer was not trained on DR runbook — schedule cross-training

### Action Items
- [ ] Reduce DNS TTL for api.example.com from 300s to 60s (Owner: @neteng, Due: 2026-07-28)
- [ ] Automate ConfigMap region references via Helm values (Owner: @platform, Due: 2026-08-04)
- [ ] Schedule DR training for all SRE on-call rotations (Owner: @sre-manager, Due: 2026-08-15)
```

---

## Recovery Decision Tree

```
Is the outage a full region failure?
├── NO → Is it a single-AZ failure?
│   ├── YES → Multi-AZ should handle it. Verify failover. If not, escalate to cloud provider.
│   └── NO → Is it a service degradation?
│       ├── YES → Canary / rollback to previous version. Block deploys.
│       └── NO → Investigate specific component (DB, cache, network policy).
│
└── YES → Initiate DR failover:
    1. [ ] Verify it's not a false alarm (check cloud status dashboard)
    2. [ ] Declare SEV0 incident
    3. [ ] Assemble war room — incident commander, SRE lead, service owners
    4. [ ] Check replication lag on all DBs — determine actual RPO at failover time
    5. [ ] Execute runbook per tier:
         - Tier 0: Immediate (route53 flip, DynamoDB Global Tables auto-failover)
         - Tier 1: Promote read replicas, scale compute
         - Tier 2: Restore from latest snapshot, scale from pilot light
         - Tier 3: Deploy from IaC, restore from backup (deferred if Tier 0-1 healthy)
    6. [ ] Validate: health checks + synthetic transactions
    7. [ ] Communicate: status page update, customer notification, executive summary
    8. [ ] Monitor for 24h minimum before declaring resolved
    9. [ ] Schedule postmortem within 48h
```

---

## Production Hardening Checklist

- [ ] RPO/RTO defined and documented per service tier with business sign-off
- [ ] 3-2-1 backup rule applied to all Tier 0-2 data stores
- [ ] Cross-region replication enabled for all databases (RDS, DynamoDB, ElastiCache)
- [ ] S3 cross-region replication + versioning enabled with Object Lock for immutability
- [ ] Backup encryption at rest with KMS; separate key for DR region
- [ ] Automated failover pipeline tested and committed to Git
- [ ] DNS TTL set to ≤ 60s for DR-critical endpoints
- [ ] Infrastructure as Code supports DR region parameterization
- [ ] Tabletop exercises conducted monthly; full DR test annually
- [ ] DR runbook accessible offline (not dependent on primary-region wiki)
- [ ] Communication templates pre-written (SEV0 declaration, status updates, all-clear)
- [ ] On-call rotation includes DR-trained engineers on every shift
- [ ] Synthetic monitoring validates DR region health separately from primary
