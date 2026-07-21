---
name: docker-kubernetes
description: Dockerfile optimization, docker-compose, Kubernetes manifests, Helm charts, service mesh, pod security, and ingress design. Triggered by docker, kubernetes, k8s, helm, container, service mesh, ingress, pod, deployment.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - docker-kubernetes
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Docker & Kubernetes Engineer

Design, build, and operate containerized workloads on Kubernetes. Covers production-grade Dockerfiles,
multi-service development with compose, Kubernetes resource manifests, Helm chart authoring,
service mesh integration, security hardening, and traffic management.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Writing or optimizing Dockerfiles for production with multi-stage builds and non-root users
- Composing local development environments with docker-compose for multi-service apps
- Authoring Kubernetes manifests: Deployments, StatefulSets, Services, Ingresses, ConfigMaps, Secrets
- Building and publishing Helm charts for internal or community use
- Configuring service mesh (Istio, Linkerd, Cilium) for mTLS, traffic splitting, and observability
- Hardening pod security: securityContext, PodSecurityStandards, network policies, RBAC
- Designing ingress architectures with cert-manager, external-dns, and multiple ingress controllers

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Docker Compose vs Kubernetes
```
                     ┌──────────────────────────┐
                     │ START: Container           │
                     │ orchestration choice       │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ >5 services OR need         │
                    │ auto-scaling/self-healing?  │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Team >5 AND │   │ docker-compose  │
                    │ budget >$1K │   │ on single VM    │
                    │ /month?     │   │ ($40-200/mo,    │
                    └────┬────────┘   │ <1K DAU)        │
                         │ YES    NO  └────────────────┘
                    ┌────▼────┐ ┌▼───────────┐
                    │ K8s     │ │ ECS Fargate │
                    │ (EKS/   │ │ or Cloud Run│
                    │ GKE/AKS)│ │ (middle      │
                    │         │ │ ground)      │
                    └─────────┘ └─────────────┘
```
**When to choose docker-compose:** <5 services, <5 engineers, <1K DAU, budget <$500/month, no auto-scaling needed. **When to choose ECS/Cloud Run:** 2-20 services, no K8s expertise, managed containers, $200-500/month. **When to choose K8s:** >5 services, >5 engineers, auto-scaling/self-healing required, budget >$1K/month, GitOps desired.

### Managed K8s vs Self-Managed
```
                     ┌──────────────────────────┐
                     │ START: K8s deployment      │
                     │ model                     │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Team has dedicated 2+       │
                    │ K8s experts AND >50 nodes?  │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Self-managed│   │ EKS/GKE/AKS     │
                    │ (Kops/      │   │ (managed control │
                    │ Kubespray)  │   │ plane, $73/mo    │
                    │ — 20-40     │   │ control plane)   │
                    │ hrs/week ops│   │ — 2-8 hrs/week   │
                    └─────────────┘   └────────────────┘
```
**When to choose Managed (EKS/GKE/AKS):** <50 nodes, <2 dedicated K8s experts, want control plane managed, budget for $73-150/month per cluster. **When to choose Self-Managed:** >50 nodes, in-house K8s expertise (2+ FTEs), cost savings on control plane justify 20-40 hrs/week ops overhead.

### Ingress Controller Selection
```
                     ┌──────────────────────────┐
                     │ START: Ingress controller  │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Need advanced rate limiting │
                    │ WAF, or Lua scripting?      │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ NGINX       │   │ K8s-native     │
                    │ Ingress     │   │ features enough │
                    │ Controller  │   │ → AWS LB        │
                    │ (most       │   │ Controller or   │
                    │  flexible)  │   │ GCE Ingress     │
                    └─────────────┘   └────────────────┘
```
**When to choose NGINX Ingress:** Cross-cloud, need custom Lua/OpenResty, advanced rate limiting, canary by header, >10 routing rules. **When to choose Cloud-Native LB:** Single cloud, simple host/path routing, want cloud WAF integration (AWS WAF), managed TLS termination.

### Service Mesh Decision
```
                     ┌──────────────────────────┐
                     │ START: Service mesh        │
                     │ evaluation                │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Compliance requires mTLS    │
                    │ AND >10 services?           │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Istio /     │   │ No service mesh │
                    │ Linkerd /   │   │ — sidecar-free  │
                    │ Cilium      │   │ K8s networking  │
                    │ (adds 0.5-  │   │ + NetworkPolicy │
                    │  2ms latency│   │ is sufficient   │
                    │  per hop)   │   └────────────────┘
                    └─────────────┘
```
**When to deploy Service Mesh:** mTLS required, >10 services, need traffic splitting (canary), need L7 observability per service, team can absorb 0.5-2ms added latency. **When to skip:** <10 services, no mTLS requirement, NetworkPolicy sufficient, latency budget <5ms — mesh adds unnecessary complexity.

### Container Image Security Posture
```
                     ┌──────────────────────────┐
                     │ START: Image security      │
                     │ hardening                 │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Production deployment with  │
                    │ PII or regulated data?      │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Distroless  │   │ Alpine/slim     │
                    │ base + non- │   │ base + non-root │
                    │ root + read-│   │ user (standard) │
                    │ only rootfs │   └────────────────┘
                    │ + image     │
                    │ signing     │
                    │ (Cosign)    │
                    └─────────────┘
```
**When to use Distroless+Signing:** PII/PCI/HIPAA workloads, production, CVE surface must be minimized, SLSA L2+ required. **When Alpine/Slim is enough:** Internal tools, no regulated data, simpler Dockerfile maintenance, acceptable CVE risk profile.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Docker Image Engineering
1. Start from minimal base images: `distroless`, `alpine`, or `scratch` for Go/Rust binaries; `slim` variants for interpreted languages.
2. Use multi-stage builds: compile/build in a full SDK image, copy only the runtime artifact to the final image.
3. Order layers by change frequency: install OS packages first, then dependencies (locked), then application code.
4. Run as non-root: `USER 1000:1000`; set `WORKDIR`; never expose privileged ports (<1024) in the container.
5. Use `.dockerignore` to exclude `.git`, `node_modules`, build artifacts, and secrets.
6. Pin base images by digest: `FROM node:20-alpine@sha256:abc...` — not by tag.
7. Add HEALTHCHECK instructions for container orchestrators to detect hung processes.
8. Leverage BuildKit features: `--mount=type=cache` for package manager caches, `--mount=type=secret` for credentials during build.

### Phase 2 (~30 min): Kubernetes Manifests
1. Use Deployments for stateless workloads, StatefulSets for databases/queues with persistent identity, DaemonSets for node-level agents.
2. Define resource requests and limits for every container; use Vertical Pod Autoscaler for right-sizing.
3. Configure liveness probes (restart hung containers) and readiness probes (stop routing to unready pods).
4. Use PodDisruptionBudgets to ensure minimum availability during voluntary disruptions.
5. Externalize configuration: ConfigMaps for non-sensitive data, Secrets (with encryption at rest) for credentials; mount as files or env vars.
6. Implement affinity/anti-affinity rules for high availability: spread pods across nodes and availability zones.
7. Set PodSecurityStandard to `restricted` by default; relax only with explicit exceptions and justifications.
8. Apply NetworkPolicy to deny all traffic by default; explicitly allow only required ingress/egress flows.

### Phase 3 (~20 min): Helm Charts
1. Structure charts with `templates/`, `values.yaml`, `Chart.yaml`, and optional `values-{env}.yaml` environment overrides.
2. Use `helm create` as a starting point; remove unused boilerplate to keep charts minimal.
3. Parameterize everything environment-specific: replica counts, resource sizes, ingress hosts, image tags.
4. Use named templates (`_helpers.tpl`) for repeated labels, selectors, and naming conventions.
5. Version charts semantically; publish to OCI-compliant registries (`helm push` to ECR/ACR/GAR).
6. Test charts with `helm lint`, `helm template --debug`, and `helm unittest` plugin.
7. Sign charts with `helm package --sign` using GPG or Cosign keys.

### Phase 4 (~15 min): Service Mesh and Traffic Management
1. Deploy a service mesh (Istio/Ambient, Linkerd, Cilium) when you need mTLS, traffic splitting, or fine-grained observability.
2. Enforce strict mTLS mesh-wide; use permissive mode during migration, then lock down.
3. Configure traffic splitting for canary deployments: 90% → stable, 10% → canary; shift progressively based on metrics.
4. Use request timeouts, circuit breakers, and retries at the sidecar level to implement resilience patterns.
5. Ingress: use cert-manager with Let's Encrypt for automatic TLS; external-dns for automatic Route53/Cloud DNS record creation.


### Cross-skills Integration
The preceding skill in the chain documents output format requirements. The following skill in the chain expects that format. Run them sequentially:
```bash
#[previous-skill] && #[this-skill] && #[next-skill]
```
Document the output contract explicitly so consuming skills know what to expect.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `dockerfile-optimization` | Writing production Dockerfiles with multi-stage builds, minimal base images, and layer caching |
| `docker-compose` | Orchestrating multi-service local development environments with networking and volumes |
| `kubernetes-manifests` | Authoring Deployments, StatefulSets, Services, Ingresses, ConfigMaps, and Secrets |
| `helm-charts` | Building, versioning, and publishing Helm charts with templating and environment overrides |
| `pod-security` | Hardening containers with securityContext, PodSecurityStandards, NetworkPolicies, and RBAC |
| `service-mesh-integration` | Deploying Istio, Linkerd, or Cilium for mTLS, traffic splitting, and observability |
| `ingress-traffic-management` | Configuring cert-manager, external-dns, multiple ingress controllers, and load balancing |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Docker/Kubernetes specialists build the container platform that every service runs on. They coordinate with developers for application packaging, DevOps for cluster operations, security for pod hardening, and observability for runtime visibility.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | Dockerfile creation, resource requirements | Multi-stage build patterns, base image selection, resource requests/limits guidance, health check design |
| **Frontend Developer** | Static asset serving, SSR containerization | Nginx config for SPA routing, SSR Node.js container sizing, CDN integration |
| **DevOps Engineer** | Cluster provisioning, Helm deployments | Cluster API access, Helm repository management, GitOps integration (ArgoCD/Flux) |
| **Security Engineer** | Pod security, network policies, image scanning | PodSecurityStandards enforcement, NetworkPolicy design, image CVE triage, non-root user requirements |
| **Cloud Architect** | Node groups, cluster networking, service mesh | Instance type selection, VPC CNI configuration, service mesh (Istio/Linkerd) architecture, cluster autoscaling |
| **Observability Engineer** | Container metrics, log collection | Prometheus pod monitors, Fluentd/Fluent Bit config, OpenTelemetry sidecar injection, Grafana dashboards |
| **CI/CD Builder** | Image build pipeline, registry integration | Kaniko/Buildah in CI, image signing (Cosign), registry cleanup policies, tag immutability |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Base image CVE discovered (Critical/High) | Security Engineer, All service owners | Rebuild all affected images; coordinate deployment |
| Cluster upgrade planned (Kubernetes version bump) | DevOps, All service owners | API deprecation check; schedule maintenance window; verify compatibility |
| Node pool scaling event or capacity issue | Cloud Architect, DevOps | May need instance type changes or cluster autoscaler tuning |
| Service mesh misconfiguration (mTLS broken, routing error) | DevOps, Affected service teams | Debug traffic flow; potential partial outage |
| Ingress certificate expiring within 7 days | DevOps, Service owners | Renew certificate; verify cert-manager automation working |

### Escalation Path

```
Cluster-wide outage? → Cloud Architect → DevOps Engineer → Incident Responder
Security policy violation (privileged pod)? → Security Engineer → Compliance Officer
Image registry unavailable? → Cloud Architect → DevOps Engineer
Persistent node failures? → Cloud Architect (cloud provider escalation)
```


**What good looks like:** Docker image builds in under 5 minutes and is under 200MB. Kubernetes manifests pass `kubeval` validation. Pod startup time < 10 seconds. Liveness and readiness probes configured on every deployment. Resource requests and limits set on every container.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **One process per container**: use sidecar containers for log shippers, proxies, or metrics exporters.
- **Images are immutable**: tag with git SHA, never use `:latest` in production manifests.
- **Secrets at rest**: enable encryption at rest in etcd; use External Secrets Operator or Sealed Secrets for git-safe storage.
- **Resource limits are mandatory**: without limits, a memory leak in one pod can OOM the entire node.
- **Use `kubectl diff` before applying**: preview changes and catch unintended mutations.
- **Scan images**: integrate Trivy, Grype, or Snyk into CI; block deployment on HIGH/CRITICAL CVEs.

## When Kubernetes is Overkill

```
Team < 5 engineers? → Overkill. Use docker-compose or managed PaaS.
< 5 services? → Overkill. docker-compose + a small VM.
< 100 req/s total? → Overkill. A single VM handles this easily.
Monthly infra budget < $500? → Overkill. K8s control plane alone costs $73/month (EKS).
No multi-service orchestration needed? → Overkill. docker-compose is enough.

Check 2+ boxes? DON'T use Kubernetes. Use one of:
- docker-compose (single VM, 0-5 services, < $100/month)
- ECS Fargate (managed containers, no K8s ops)
- Cloud Run (serverless containers, zero ops)
- Railway/Render/Fly.io (PaaS, heroku-like, < 5 services)
```

## docker-compose for MVP

```yaml
# Production-ready MVP stack: docker-compose on single $40/month VM
version: '3.8'
services:
  app:
    build: .
    ports: ['3000:3000']
    depends_on: [db, redis]
    restart: unless-stopped
  db:
    image: postgres:16-alpine
    volumes: [pgdata:/var/lib/postgresql/data]
    restart: unless-stopped
  redis:
    image: redis:7-alpine
    restart: unless-stopped
volumes:
  pgdata:
```
**Ceiling:** 1K-10K DAU, 50-200 req/s. Migrate to managed DB (RDS) first, then to K8s when you need auto-scaling.

## Managed K8s vs Self-Managed: Cost Comparison

| Approach | Monthly Cost (3 nodes) | Ops Overhead | Best For |
|----------|----------------------|--------------|----------|
| **docker-compose on VM** | $40-200/month | 1-2 hrs/week | MVP, < 5 services, < 1K DAU |
| **ECS Fargate** | $200-500/month | 30 min/week | < 20 services, no K8s expertise |
| **EKS (managed K8s)** | $600-1.5K/month | 4-8 hrs/week | 5-50 services, team > 5 |
| **GKE (managed K8s)** | $500-1.2K/month | 2-4 hrs/week | Autopilot mode: pay per pod |
| **Self-managed K8s** | $300-800/month (nodes only) | 20-40 hrs/week (dedicated person) | 50+ nodes, team > 20 with K8s expertise |
| **K3s/MicroK8s (edge)** | $100-300/month | 4-8 hrs/week | Edge/IoT, < 10 nodes |

**K8s hidden costs:** Control plane management, etcd backups, cert rotation, CNI troubleshooting, RBAC, network policies, pod security policies, Helm chart maintenance, ingress controller, cert-manager, external-dns, monitoring stack (Prometheus + Grafana). Budget 20-40 hrs/week for self-managed.

### K8s Readiness Checklist
Don't adopt K8s until you can answer YES to:
- [ ] Team > 5 engineers comfortable with containers
- [ ] > 5 services deployed independently
- [ ] Need auto-scaling beyond what vertical scaling provides
- [ ] Need self-healing (restart failed containers automatically)
- [ ] Need declarative configuration (GitOps with Argo CD/Flux)
- [ ] Willing to invest 20+ hrs/week in K8s operations (or pay for managed)
- [ ] Monthly infra budget > $1,000

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Docker = `docker-compose up` on a single VM. One Dockerfile (multi-stage). No orchestration. No registry (build on deploy target). Restart policy: `unless-stopped`. Volumes for persistence.
- **What to skip**: Kubernetes. Docker Swarm. Container registry. Image scanning. Resource limits. Network policies. Helm charts. GitOps.
- **Coordination**: You write the Dockerfile + compose file. Done.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Docker Compose for dev/staging. Container registry (Docker Hub, ECR, GHCR). CI builds and pushes images. Multi-stage builds optimized. Non-root users. Health checks. docker-compose for production on 1-2 VMs, or ECS Fargate. Image scanning in CI.
- **What to skip**: Kubernetes. Service mesh. GitOps. Pod disruption budgets. Network policies beyond basic.
- **Coordination**: Dockerfiles reviewed in PR. Image tags follow semver. CI manages build + push.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Kubernetes (EKS/GKE/AKS, managed). Helm charts for deployments. GitOps (Argo CD). Resource requests + limits. Liveness/readiness probes. PodDisruptionBudget. NetworkPolicy (deny all, allow explicit). cert-manager + external-dns. Container scanning in CI (block CRITICAL/HIGH). Multi-environment K8s clusters.
- **What to skip**: Self-managed Kubernetes. Service mesh (Istio/Linkerd) — unless mTLS required. Multi-cluster. Custom operators.
- **Coordination**: K8s platform owner (1-2 people). Weekly K8s review. Helm chart PR review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-cluster Kubernetes. Service mesh (Istio/Linkerd). Platform team managing K8s. Custom operators. PodSecurityPolicy/PSS enforced. OPA/Gatekeeper for policy. K8s autoscaling (HPA + cluster autoscaler). Secrets management (External Secrets Operator + Vault). Chaos engineering. Multi-region clusters. K8s cost monitoring (Kubecost).
- **What's full production**: K8s platform as a product. Self-service namespaces. Policy as code. Automated cluster lifecycle. K8s upgrade automation.
- **Coordination**: K8s platform team weekly. Cluster upgrade planning monthly. Security policy review quarterly. Capacity planning quarterly.

### Transition Triggers
- **Solo → Small**: Second developer. Need consistent environments across dev/prod.
- **Small → Medium**: 5+ services. Need auto-scaling. Need self-healing. docker-compose can't keep up.
- **Medium → Enterprise**: 10+ clusters or multi-region. 50+ services. Dedicated platform team justified.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  All images pinned by SHA256 digest, not mutable tags
- [ ] **[S2]**  Multi-stage builds produce minimal images; no build tools in the final layer
- [ ] **[S3]**  Non-root user configured in every container; `allowPrivilegeEscalation: false`
- [ ] **[S4]**  Resource requests and limits set for every container in every namespace
- [ ] **[S5]**  Liveness and readiness probes configured with appropriate initial delays
- [ ] **[S6]**  PodDisruptionBudget defined for all deployments with replicas > 1
- [ ] **[S7]**  NetworkPolicy denies all by default; explicit allow rules for required flows
- [ ] **[S8]**  PodSecurityStandard enforced at `restricted` level cluster-wide
- [ ] **[S9]**  Image vulnerability scanning in CI pipeline; HIGH/CRITICAL CVEs block deployment
- [ ] **[S10]**  Helm charts versioned, linted, and tested before release
- [ ] **[S11]**  cert-manager and external-dns configured for automated TLS and DNS

## References
<!-- QUICK: 30s -- links to deeper reading -->
- Dockerfile Best Practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- Kubernetes Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- Helm Best Practices: https://helm.sh/docs/chart_best_practices/
- Istio Traffic Management: https://istio.io/latest/docs/concepts/traffic-management/
- Trivy Vulnerability Scanner: https://github.com/aquasecurity/trivy
