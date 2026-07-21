# Docker & Kubernetes — Orchestra Platform

**Skill:** docker-kubernetes
**Input:** Service manifests, deployment requirements, architecture decisions

## Docker Strategy

### Multi-Stage Builds (Go Services)

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /service ./cmd/

# Stage 2: Runtime
FROM alpine:3.19
RUN apk add --no-cache ca-certificates tzdata
USER 1000:1000
COPY --from=builder /service /service
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD /service health
ENTRYPOINT ["/service"]
```

**Image sizes:** catalog-service 18MB, template-engine 22MB, plugin-registry 15MB, auth-service 14MB. All under 50MB target.

### Frontend (Next.js)

- Standalone output mode, Node.js 20-alpine base
- Static assets served via CloudFront + S3
- Image: 85MB (with node_modules), 28MB compressed

### Security Rules (Enforced)

- Never run as root — USER 1000 in every Dockerfile
- Never use `latest` tag in deployment manifests
- Resource limits required (no LimitRange dependency)
- Read-only root filesystem where possible
- No secrets in build args (use BuildKit secrets)

## Kubernetes Architecture

### Cluster Topology

- EKS 1.30, 3 AZs, managed node groups
- Dev: 3 × t3.medium (spot), Staging: 3 × t3.large, Prod: 6 × m6i.xlarge (3 AZs × 2 nodes)
- Cluster autoscaler: scale-up at 70% CPU, scale-down after 10 min low utilization
- Pod disruption budgets: catalog 1, template-engine 2, plugin-registry 1, auth-service 1

### Service Deployment (catalog-service example)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: catalog-service
  namespace: orchestra
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    spec:
      serviceAccountName: catalog-service
      containers:
      - name: catalog-service
        image: ghcr.io/orchestra/catalog-service:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests: {cpu: 250m, memory: 256Mi}
          limits: {cpu: 500m, memory: 512Mi}
        livenessProbe: {httpGet: {path: /health}, initialDelaySeconds: 10}
        readinessProbe: {httpGet: {path: /ready}, initialDelaySeconds: 5}
        envFrom:
        - secretRef: {name: catalog-db-credentials}
```

### Istio Service Mesh

- mTLS between all services (STRICT mode in prod)
- Traffic shifting for canary deployments (10% → 50% → 100%)
- Circuit breaking: 5 consecutive 5xx → open circuit for 30s
- Retry policy: 3 retries with 2s timeout for idempotent GET requests

### Helm Charts

- One chart per service, umbrella chart for full platform
- Values files: dev.yaml, staging.yaml, prod.yaml
- Chart versioning: matches app version (v1.0.0)
- All charts in OCI registry (ghcr.io/orchestra/charts/)

## Key Principles

- Resource limits are not optional — every container has requests + limits
- Never use `latest` tag in production manifests — always pinned to SHA or version
- Liveness and readiness probes are different — liveness restarts the pod, readiness controls traffic
- PDBs ensure zero-downtime deployments — minimum 1 replica available during rollouts
