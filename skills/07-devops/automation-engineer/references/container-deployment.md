# container-deployment

Reference documentation for the automation-engineer skill — Docker multi-stage builds, BuildKit, Compose, registries, image scanning & signing, K8s deployment strategies, Helm, Kustomize, GitOps with ArgoCD & Flux, service mesh (Istio, Linkerd, Cilium), ECS/GKE/AKS/Nomad orchestration, and canary deployment patterns with Argo Rollouts & Flagger.

## Docker: Multi-stage builds

### Build vs runtime stage pattern

```dockerfile
# Dockerfile — Go multi-stage
FROM golang:1.22-alpine AS builder
RUN apk add --no-cache ca-certificates git
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /app ./cmd/server

FROM scratch AS runtime
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app /app
USER 65534:65534
EXPOSE 8080
ENTRYPOINT ["/app"]
```

```dockerfile
# Dockerfile — Node.js multi-stage
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --ignore-scripts

FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --omit=dev

FROM node:20-alpine AS runtime
RUN apk add --no-cache tini
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./
USER node
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/server.js"]
```

### Layer caching strategies

```dockerfile
# Order COPY by change frequency — least-changing first
FROM node:20-alpine
WORKDIR /app

# 1. Dependencies change least often — cache them first
COPY package.json package-lock.json ./
RUN npm ci

# 2. Source changes frequently — copy last
COPY . .

# 3. For monorepos: copy root config + package.json, install, then copy app code
COPY turbo.json tsconfig.base.json ./
COPY apps/api/package.json apps/api/
RUN npm ci -w apps/api
COPY apps/api/ apps/api/
```

## Docker: BuildKit features

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1
# or in /etc/docker/daemon.json: { "features": { "buildkit": true } }
```

### Cache mounts — speed up package installs

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

```dockerfile
# Go module cache
FROM golang:1.22-alpine AS builder
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app ./cmd/server
```

### Secret mounts — avoid leaking credentials in layers

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS build
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

```bash
# Build with secret from file
docker build --secret id=npmrc,src=$HOME/.npmrc -t myapp .
```

### Network isolation during build

```dockerfile
# syntax=docker/dockerfile:1
FROM debian AS build
RUN --network=none apt-get update  # blocks all network — combined with local repos
```

## Docker: buildx for multi-architecture

```bash
# Create a multi-arch builder
docker buildx create --name multiarch --driver docker-container --use
docker buildx inspect --bootstrap

# Build and push for multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag registry.example.com/myapp:v1.0.0 \
  --tag registry.example.com/myapp:latest \
  --push \
  .

# Build and export locally (single platform only)
docker buildx build --platform linux/arm64 --load -t myapp:arm64 .

# CI: GitHub Actions multi-arch build
# .github/workflows/build.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: type=sha,type=ref,event=branch,type=semver,pattern={{version}}
      - uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Docker Compose

### Development vs production configs

```yaml
# docker-compose.yml — base
services:
  app:
    build: .
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_DB: mydb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      retries: 5
volumes:
  pgdata:
```

```yaml
# docker-compose.override.yml — development (auto-merged with base)
services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules  # anonymous volume preserves node_modules
    command: npm run dev
    ports:
      - "3000:3000"
  db:
    ports:
      - "5432:5432"
```

```yaml
# docker-compose.prod.yml — production
services:
  app:
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: "1"
          memory: 512M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
  db:
    restart: always
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

```bash
# Run with override
docker compose up                     # auto-merges docker-compose.yml + override.yml
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Image registries

### Docker Hub — rate limit handling

```bash
# Pull rate limits: 100/6h (anonymous), 200/6h (authenticated free), 5000/day (paid)
# Authenticate to increase limits
docker login -u $DOCKER_USER -p $DOCKER_PASS
```

```yaml
# CI: Mirror pull-through cache to avoid rate limits
# .github/workflows/build.yml
- name: Set up Docker Hub mirror
  run: |
    echo '{ "registry-mirrors": ["https://mirror.gcr.io"] }' | sudo tee /etc/docker/daemon.json
    sudo systemctl restart docker
```

### ECR — lifecycle policies

```json
// ecr-lifecycle-policy.json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep last 30 dev images, expire older",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["dev-"],
        "countType": "imageCountMoreThan",
        "countNumber": 30
      },
      "action": { "type": "expire" }
    },
    {
      "rulePriority": 2,
      "description": "Expire untagged images after 7 days",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 7
      },
      "action": { "type": "expire" }
    }
  ]
}
```

```bash
# ECR login for CI
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
```

### GCR/Artifact Registry, ACR, GHCR, Harbor

```bash
# GCR
gcloud auth configure-docker us-docker.pkg.dev
docker push us-docker.pkg.dev/$PROJECT/repo/image:tag

# ACR
az acr login --name myregistry
docker push myregistry.azurecr.io/image:tag

# GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin
docker push ghcr.io/$OWNER/repo:tag

# Harbor
docker login harbor.example.com -u $HARBOR_USER -p $HARBOR_PASS
```

## Image scanning

### Trivy

```bash
# CLI: scan local image
trivy image --severity CRITICAL,HIGH myapp:v1.0.0

# Filesystem scan (no image needed)
trivy fs --severity CRITICAL,HIGH,MEDIUM ./

# SBOM generation
trivy image --format cyclonedx --output sbom.json myapp:v1.0.0
```

```yaml
# CI: Trivy in GitHub Actions — severity-based blocking
trivy-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: fs
        scanners: vuln,secret,misconfig
        severity: CRITICAL,HIGH
        exit-code: 1           # fail build on CRITICAL or HIGH
        format: sarif
        output: trivy-results.sarif
    - uses: github/codeql-action/upload-sarif@v3
      if: always()
      with:
        sarif_file: trivy-results.sarif
```

### Grype, Docker Scout

```bash
# Grype: scan image and fail on critical
grype myapp:v1.0.0 --fail-on critical

# Docker Scout: quick comparison
docker scout quickview myapp:v1.0.0
docker scout cves myapp:v1.0.0 --only-severity critical,high
docker scout compare myapp:v1.0.0 --to myapp:latest
```

## Image signing: Cosign + Sigstore

### Keyless signing (OIDC — preferred)

```bash
# Sign with OIDC (GitHub Actions workload identity)
cosign sign --yes ghcr.io/myorg/myapp:v1.0.0

# Verify keyless signature
cosign verify ghcr.io/myorg/myapp:v1.0.0 \
  --certificate-identity https://github.com/myorg/myapp/.github/workflows/release.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

### Key-based signing

```bash
# Generate key pair
cosign generate-key-pair

# Sign
cosign sign --key cosign.key ghcr.io/myorg/myapp:v1.0.0

# Verify
cosign verify --key cosign.pub ghcr.io/myorg/myapp:v1.0.0
```

```yaml
# CI: Keyless signing in GitHub Actions
release:
  runs-on: ubuntu-latest
  permissions:
    id-token: write        # needed for OIDC
    packages: write
  steps:
    - uses: actions/checkout@v4
    - uses: sigstore/cosign-installer@v3
    - run: |
        docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
        docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
    - run: cosign sign --yes ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### Verify in K8s admission controller

```yaml
# ClusterImagePolicy — enforce signed images
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: signed-by-github
spec:
  images:
    - glob: "ghcr.io/myorg/**"
  authorities:
    - keyless:
        identities:
          - issuer: https://token.actions.githubusercontent.com
            subject: https://github.com/myorg/*/.github/workflows/*@*
```

## K8s deployment

### kubectl apply (imperative)

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp
kubectl set image deployment/myapp myapp=ghcr.io/myorg/myapp:v1.1.0
kubectl rollout history deployment/myapp
```

### Helm — templates, values per environment, hooks

```yaml
# values/production.yaml
replicaCount: 3
image:
  repository: ghcr.io/myorg/myapp
  tag: "1.0.0"
resources:
  requests: { cpu: 500m, memory: 512Mi }
  limits:   { cpu: 1000m, memory: 1Gi }
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
ingress:
  enabled: true
  hosts: [myapp.example.com]
  tls: [{ secretName: myapp-tls, hosts: [myapp.example.com] }]
```

```yaml
# templates — pre-upgrade hook (database migration)
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ .Release.Name }}-db-migrate"
  annotations:
    "helm.sh/hook": pre-upgrade,pre-install
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["./migrate", "up"]
```

```bash
# Deploy with environment-specific values
helm upgrade --install myapp ./chart \
  -f values/production.yaml \
  --namespace production \
  --set image.tag=v1.1.0 \
  --wait --timeout 5m

# Lint templates, diff before apply
helm lint ./chart
helm template ./chart -f values/production.yaml | kubectl diff -f -
```

### Kustomize — overlays, patches, generators

```
deploy/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── production/
    │   ├── kustomization.yaml
    │   └── replica-patch.yaml
    └── staging/
        └── kustomization.yaml
```

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
configMapGenerator:
  - name: app-config
    files:
      - config.json=configs/default.json
```

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
patches:
  - path: replica-patch.yaml
images:
  - name: myapp
    newTag: "1.0.0"
configMapGenerator:
  - name: app-config
    behavior: merge
    files:
      - config.json=configs/production.json
```

```yaml
# overlays/production/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: myapp
          resources:
            requests: { cpu: "500m", memory: "512Mi" }
            limits:   { cpu: "1", memory: "1Gi" }
```

```bash
kustomize build deploy/overlays/production | kubectl apply -f -
```

## K8s deployment strategies

### RollingUpdate (default)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1     # at most 1 pod down during update
      maxSurge: 1           # at most 1 extra pod during update
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
        - name: myapp
          image: ghcr.io/myorg/myapp:v1.1.0
```

### Recreate

```yaml
spec:
  strategy:
    type: Recreate            # all old pods killed first, then new ones created
```

## K8s probes

```yaml
spec:
  containers:
    - name: myapp
      ports:
        - containerPort: 8080
      startupProbe:           # only runs until first success — gives slow-start apps time
        httpGet:
          path: /healthz
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5
        failureThreshold: 30   # up to 150s for startup (30 x 5s)
      livenessProbe:          # restarts container if probe fails
        httpGet:
          path: /live
          port: 8080
        periodSeconds: 10
        failureThreshold: 3
      readinessProbe:         # removes from service endpoints if probe fails
        httpGet:
          path: /ready
          port: 8080
        periodSeconds: 5
        failureThreshold: 3
```

## GitOps: ArgoCD

### Application CRD + auto-sync

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-production
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/infra.git
    targetRevision: HEAD
    path: deploy/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true           # delete resources no longer in git
      selfHeal: true        # revert manual changes to match git
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
```

### Sync waves and hooks

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"    # lower waves sync first
# Wave 0: CRDs, namespaces
# Wave 1: ConfigMaps, Secrets
# Wave 2: Deployments, StatefulSets
# Wave 3: post-sync hooks
```

```yaml
# PreSync hook — runs before sync wave
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```

### PR-based changes

```yaml
# ApplicationSet for PR environments
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: pr-environments
spec:
  generators:
    - pullRequest:
        github:
          owner: myorg
          repo: myapp
        requeueAfterSeconds: 300
  template:
    metadata:
      name: 'myapp-pr-{{ .number }}'
    spec:
      source:
        repoURL: 'https://github.com/myorg/myapp.git'
        targetRevision: '{{ .head_sha }}'
        path: deploy/base
      destination:
        namespace: 'pr-{{ .number }}'
```

## GitOps: Flux

### OCI artifacts, HelmRelease, drift detection

```yaml
# OCIRepository + HelmRelease
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: myapp
  namespace: production
spec:
  interval: 5m
  url: oci://ghcr.io/myorg/charts/myapp
  ref:
    semver: ">=1.0.0 <2.0.0"
---
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: myapp
  namespace: production
spec:
  interval: 5m
  chartRef:
    kind: OCIRepository
    name: myapp
  values:
    replicaCount: 3
    image:
      repository: ghcr.io/myorg/myapp
      tag: v1.0.0
```

```yaml
# Image automation — auto-update on new image tag
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: myapp
spec:
  image: ghcr.io/myorg/myapp
  interval: 5m
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: myapp
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: ">=1.0.0 <2.0.0"
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageUpdateAutomation
metadata:
  name: myapp
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: flux-system
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: flux@example.com
        name: flux
      messageTemplate: 'chore: update {{ .AutomationObject }} to {{ .Image }}'
    push:
      branch: main
  update:
    path: ./deploy/production
    strategy: Setters
```

## Service mesh

### Istio — VirtualService + DestinationRule (traffic splitting)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp.example.com
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: myapp
            subset: canary
    - route:
        - destination:
            host: myapp
            subset: stable
          weight: 90
        - destination:
            host: myapp
            subset: canary
          weight: 10          # 10% traffic to canary
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
```

### Linkerd — auto-mTLS + tap

```bash
# Install Linkerd
linkerd install | kubectl apply -f -

# Inject into namespace (auto-mTLS without config)
kubectl annotate namespace production linkerd.io/inject=enabled

# Tap live traffic
linkerd tap deploy/myapp -n production
linkerd viz stat deploy -n production
```

### Cilium — eBPF network policy

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: myapp-policy
spec:
  endpointSelector:
    matchLabels:
      app: myapp
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
  egress:
    - toEndpoints:
        - matchLabels:
            app: database
      toPorts:
        - ports:
            - port: "5432"
              protocol: TCP
    - toFQDNs:                         # DNS-based egress
        - matchName: "api.stripe.com"
      toPorts:
        - ports:
            - port: "443"
              protocol: TCP
```

## Orchestration platforms

### ECS — task definition + service auto-scaling + Fargate

```json
// ecs-task-definition.json
{
  "family": "myapp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "myapp",
    "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest",
    "portMappings": [{ "containerPort": 8080 }],
    "secrets": [{
      "name": "DB_PASSWORD",
      "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:db-password"
    }],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/myapp",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
```

```yaml
# CI: Deploy to ECS (GitHub Actions)
- uses: aws-actions/amazon-ecs-deploy-task-definition@v2
  with:
    task-definition: ecs-task-definition.json
    service: myapp-service
    cluster: production
    wait-for-service-stability: true
```

### GKE — Autopilot + Workload Identity

```yaml
# K8s ServiceAccount with GCP Workload Identity
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp
  namespace: production
  annotations:
    iam.gke.io/gcp-service-account: myapp@myproject.iam.gserviceaccount.com
```

```bash
# Bind K8s SA to GCP IAM
gcloud iam service-accounts add-iam-policy-binding myapp@myproject.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:myproject.svc.id.goog[production/myapp]"
```

### AKS — managed + Azure AD

```bash
az aks create --name mycluster --resource-group myrg \
  --enable-managed-identity --network-plugin azure --node-count 3

az aks get-credentials --name mycluster --resource-group myrg
```

### Nomad — multi-cloud, non-K8s orchestration

```hcl
# job.nomad
job "myapp" {
  datacenters = ["dc1"]
  type = "service"
  group "web" {
    count = 3
    network { port "http" { to = 8080 } }
    task "server" {
      driver = "docker"
      config {
        image = "ghcr.io/myorg/myapp:v1.0.0"
        ports = ["http"]
      }
      service {
        name = "myapp"
        port = "http"
        check {
          type = "http"
          path = "/health"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
```

```bash
nomad job run job.nomad
nomad job status myapp
```

## Canary deployment patterns

### Argo Rollouts — AnalysisTemplate + canary steps

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    canary:
      steps:
        - setWeight: 10       # 10% to canary
        - pause: { duration: 5m }
        - analysis:
            templates:
              - templateName: error-rate-check
        - setWeight: 50       # 50% to canary
        - pause: { duration: 10m }
        - analysis:
            templates:
              - templateName: error-rate-check
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate-check
spec:
  metrics:
    - name: error-rate
      interval: 30s
      successCondition: result < 0.01       # less than 1% errors
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            rate(http_requests_total{status=~"5..",app="myapp"}[1m]) /
            rate(http_requests_total{app="myapp"}[1m])
```

### Flagger — service mesh integration + metric analysis

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  service:
    port: 8080
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 1m
    webhooks:
      - name: acceptance-test
        type: pre-rollout
        url: http://flagger-loadtester.production/
        timeout: 5m
        metadata:
          type: bash
          cmd: "curl -s http://myapp-canary.production:8080/health"
```

### Custom canary with weighted K8s services

```yaml
# Two Deployments behind a single Service using Istio
# Or: create two Services with different weights, swap via Flagger/Argo Rollouts
apiVersion: v1
kind: Service
metadata:
  name: myapp-canary
spec:
  selector:
    app: myapp
    track: canary
  ports:
    - port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-stable
spec:
  selector:
    app: myapp
    track: stable
  ports:
    - port: 8080
```

## CI pipeline integration patterns

### Full deployment pipeline (GitHub Actions)

```yaml
name: Build, Scan, Sign, Deploy
on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write
    outputs:
      image: ${{ steps.meta.outputs.tags }}
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: type=sha,type=ref,event=branch,type=semver,pattern={{version}}
      - uses: docker/build-push-action@v6
        id: build
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  scan:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build-and-push.outputs.image }}
          format: sarif
          output: trivy.sarif
          severity: CRITICAL,HIGH
          exit-code: 1

  sign:
    needs: scan
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: sigstore/cosign-installer@v3
      - run: cosign sign --yes ${{ needs.build-and-push.outputs.image }}@${{ needs.build-and-push.outputs.digest }}

  deploy-staging:
    needs: sign
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: azure/setup-kubectl@v4
      - run: |
          kubectl config use-context staging
          kustomize build deploy/overlays/staging | kubectl apply -f -
          kubectl rollout status deployment/myapp -n staging --timeout=5m

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production            # uses protection rules
    steps:
      - uses: azure/setup-kubectl@v4
      - run: |
          kubectl config use-context production
          helm upgrade --install myapp ./chart \
            -f values/production.yaml \
            --namespace production \
            --set image.tag=${{ github.ref_name }} \
            --wait --timeout 10m
