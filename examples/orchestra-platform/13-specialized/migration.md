# Migration Architecture — Multi-Region Deployment

## Overview

Expand the Orchestra platform from a single region (us-east-1) to dual-region (us-east-1 + eu-west-1) serving European customers with data residency in Germany. The migration uses an expand-contract pattern across 4 phases to ensure zero downtime and a verified rollback path.

## Phase 1: Infrastructure Deployment (Weeks 1–2)

Deploy identical infrastructure to eu-west-1 using Terraform. This includes: VPC (10.1.0.0/16), EKS cluster (v1.30), Aurora PostgreSQL cluster (empty, no data), ElastiCache Redis cluster, S3 bucket (`orchestra-data-eu-west-1`), and CloudFront distribution with an eu-west-1 origin. All IAM roles, security groups, and WAF rules replicated from us-east-1 config. CI/CD pipeline extended to build and push container images to both `us-east-1` and `eu-west-1` ECR registries. Validation: `kubectl` can connect to eu-west-1 EKS, health check endpoint responds 200, database accepts connections.

## Phase 2: Data Replication (Weeks 3–4)

**Aurora Global Database**: Convert us-east-1 Aurora cluster to a Global Database primary. Add eu-west-1 as a secondary region. Replication lag monitored via CloudWatch (`AuroraGlobalDBReplicationLag` metric) — target < 100ms steady state, alert at > 1 second. Initial data sync: 52GB, completed in 47 minutes.

**S3 Cross-Region Replication**: Configure CRR on all application buckets (`orchestra-templates`, `orchestra-plugins`, `orchestra-static-assets`). Enable bi-directional replication with delete marker replication. Existing objects (14,200) replicated via a one-time `aws s3 sync` batch job. New objects replicate within 15 seconds (p99).

Validation: compare row counts between regions (all 7 tables match within 0.001%), spot-check 100 recent records, verify template files are accessible from eu-west-1 S3.

## Phase 3: Dual-Write & Monitoring (Weeks 5–6)

Deploy the application stack to eu-west-1 EKS (same Helm charts, different values for region-specific config). Route53 latency-based routing configured: `api.orchestra.dev` resolves to the nearest region's ALB. Initial configuration: 100% traffic to us-east-1, 0% to eu-west-1 (eu-west-1 serves as a warm standby).

Enable eu-west-1 for internal testing via a feature flag (`multi-region-beta`). QA team performs a 5-day smoke test from a Berlin-based VPN. Monitoring dashboard (Grafana) tracks: cross-region latency (p50, p95, p99), replication lag, error rates per region, and session continuity (users routed to eu-west-1 should see the same data).

## Phase 4: Cutover (Week 7)

Gradual traffic shift using Route53 weighted routing:

- Day 1: 10% EU-based users → eu-west-1 (verified via GeoIP in the BFF)
- Day 3: 50% EU-based users → eu-west-1
- Day 5: 100% EU-based users → eu-west-1, per-region feature flag enabled in production

Cutover checklist (all must be verified before each percentage increase): data consistency (application-level checksum comparison on 1,000 random records), latency (p95 < 200ms for EU→US cross-region API calls, measured from eu-west-1 pods calling us-east-1 services), DR test (simulate us-east-1 failure — eu-west-1 continues serving with read replica promotion in < 5 minutes), and session continuity (same user can authenticate and access data from either region).

## Rollback Plan

If any check fails: disable the EU region via the `multi-region-eu` feature flag (Kubernetes ConfigMap, live-reloaded in < 60 seconds). All traffic automatically routes to us-east-1 via Route53 health checks (ALB in eu-west-1 returns unhealthy when flag is disabled). Data remains in eu-west-1 but is not served — can be re-enabled after fixing the issue without re-replicating. Full decommissioning (if permanently rolling back): delete eu-west-1 Aurora cluster, S3 buckets, and EKS cluster via Terraform destroy.
