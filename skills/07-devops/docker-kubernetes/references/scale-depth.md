# Scale Depth: Solo → Small → Medium → Enterprise

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
