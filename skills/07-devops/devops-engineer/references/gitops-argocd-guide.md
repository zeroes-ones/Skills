# GitOps with Argo CD — Production Field Manual

## Table of Contents
1. [GitOps Principles](#gitops-principles)
2. [Argo CD Architecture](#argo-cd-architecture)
3. [Application Patterns](#application-patterns)
4. [Sync Policies](#sync-policies)
5. [Health Checks](#health-checks)
6. [Progressive Delivery Integration](#progressive-delivery-integration)
7. [Multi-Cluster Management](#multi-cluster-management)
8. [Secrets in GitOps](#secrets-in-gitops)
9. [Disaster Recovery for Argo CD](#disaster-recovery-for-argo-cd)

---

## GitOps Principles

> The single source of truth for desired system state is a Git repository. The system continuously reconciles actual state toward desired state.

| Principle | Enforcement |
|---|---|
| **Declarative** | All config expressed as YAML/JSON manifests in Git |
| **Versioned & Immutable** | Every change is a commit; no `kubectl apply` from laptops |
| **Pulled Automatically** | Agent (Argo CD/Flux) pulls from Git; no CI pushes to cluster |
| **Continuously Reconciled** | Drift detected within 3 minutes (default); auto-corrected or alerted |

### GitOps Decision Tree

```
Need GitOps for Kubernetes?
├── Argo CD
│   ├── Rich UI, multi-tenancy, SSO built-in
│   ├── ApplicationSets for templated multi-cluster
│   └── Best for: enterprise, multi-team, audit requirements
└── Flux CD
    ├── Lightweight, no UI dependency
    ├── Native OCI/Helm support, Kustomize-first
    └── Best for: small teams, GitOps-native toolchain, platform teams
```

---

## Argo CD Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Git Repository                        │
│  apps/                                                    │
│  ├── app-of-apps/                                         │
│  ├── team-a/                                              │
│  └── team-b/                                              │
└──────────────┬───────────────────────────────────────────┘
               │ git pull (every 3min / webhook)
               ▼
┌──────────────────────────────┐
│       Argo CD (Cluster)      │
│  ┌────────────────────────┐  │
│  │   API Server (REST/gRPC)│  │
│  │   Repo Server (Git)    │  │
│  │   Application Controller│  │
│  │   Redis (cache)        │  │
│  └────────────────────────┘  │
└──────────────┬───────────────┘
               │ kubectl apply
               ▼
┌──────────────────────────────┐
│      Target Cluster(s)       │
│  ┌────────────────────────┐  │
│  │  Namespace: team-a      │  │
│  │  Deployments, Services  │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

---

## Application Patterns

### 1. App of Apps — The Bootstrap Pattern

```yaml
# bootstrap/app-of-apps.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-config
    path: apps/
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
---
# apps/team-a-app.yaml — discovered by app-of-apps
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: team-a-services
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/org/team-a-services
    path: overlays/prod
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: team-a
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 2. ApplicationSet — Multi-Cluster / Multi-Tenant

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: team-a-multi-cluster
spec:
  generators:
    - list:
        elements:
          - cluster: prod-us-east-1
            url: https://prod-use1.example.com
          - cluster: prod-eu-west-1
            url: https://prod-euw1.example.com
          - cluster: staging
            url: https://staging.example.com
  template:
    metadata:
      name: 'team-a-{{cluster}}'
    spec:
      source:
        repoURL: https://github.com/org/team-a-services
        path: overlays/{{cluster}}
      destination:
        server: '{{url}}'
        namespace: team-a
      syncPolicy:
        automated:
          prune: true
```

### 3. Pull Request Generator — Ephemeral Environments

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: pr-environments
spec:
  generators:
    - pullRequest:
        github:
          owner: org
          repo: team-a-services
        requeueAfterSeconds: 300
  template:
    metadata:
      name: 'pr-{{branch_slug}}'
    spec:
      source:
        repoURL: https://github.com/org/team-a-services
        targetRevision: '{{head_short_sha}}'
        path: overlays/dev
      destination:
        server: https://kubernetes.default.svc
        namespace: 'pr-{{branch_slug}}'
      syncPolicy:
        automated: {}
```

### 4. Cluster Generator — Auto-Discover Clusters

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production
  template:
    metadata:
      name: 'addons-{{name}}'
    spec:
      source:
        repoURL: https://github.com/org/cluster-addons
        path: addons/
      destination:
        server: '{{server}}'
        namespace: kube-system
```

---

## Sync Policies

### Automated Sync — Auto-Heal vs Auto-Prune

```yaml
syncPolicy:
  automated:
    prune: true       # Delete resources that are no longer in Git
    selfHeal: true    # Revert manual changes within 5 seconds
    allowEmpty: false # Don't sync empty directories (safety)
```

| `prune` | `selfHeal` | Behavior |
|---|---|---|
| `false` | `false` | Manual sync only — operator triggers via UI/CLI |
| `true` | `false` | Auto-sync on git change, but manual drift tolerated |
| `false` | `true` | Auto-heal drift, but orphaned resources persist |
| `true` | `true` | **Full GitOps** — Git is truth, cluster always matches |

### Sync Windows — Maintenance & Blackout Periods

```yaml
syncPolicy:
  syncWindows:
    - kind: deny
      schedule: '0 2 * * 1'      # Every Monday 2 AM
      duration: 2h                # 2-hour maintenance window
      applications:
        - '*-production'
      namespaces:
        - prod-*
    - kind: allow
      schedule: '0 8-17 * * 1-5' # Business hours weekdays
      duration: 9h
```

### Sync Waves & Hooks — Ordering Dependencies

```yaml
# Phase 1: CRDs, Namespaces (wave -1 to 0)
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# Phase 2: ConfigMaps, Secrets (wave 1)
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"
---
# Phase 3: Deployments, StatefulSets (wave 2)
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "2"
---
# Phase 4: Post-sync jobs (wave 5)
metadata:
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
```

---

## Health Checks

### Custom Health Checks

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  source:
    helm:
      values: |
        healthChecks:
          - group: apps
            kind: Deployment
            check: |
              hs = {}
              if obj.status ~= nil then
                if obj.status.readyReplicas ~= nil and obj.status.readyReplicas == obj.spec.replicas then
                  hs.status = "Healthy"
                  hs.message = "All replicas ready"
                else
                  hs.status = "Progressing"
                end
              end
              return hs
```

### Custom Resource Health via Lua

```lua
-- argocd-cm ConfigMap
resource.customizations: |
  cert-manager.io/Certificate:
    health.lua: |
      hs = {}
      if obj.status ~= nil and obj.status.conditions ~= nil then
        for i, condition in ipairs(obj.status.conditions) do
          if condition.type == "Ready" and condition.status == "True" then
            hs.status = "Healthy"
            hs.message = condition.message
            return hs
          end
        end
      end
      hs.status = "Progressing"
      hs.message = "Waiting for certificate"
      return hs
```

### Diff Customization — Ignore Irrelevant Fields

```yaml
# Ignore HPA replicas (controlled by metrics, not Git)
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Prune=false
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas  # HPA-managed
    - group: autoscaling
      kind: HorizontalPodAutoscaler
      jsonPointers:
        - /spec/metrics
```

---

## Progressive Delivery Integration

### Argo Rollouts — Canary Deployment

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
        - setWeight: 20       # Send 20% to canary
        - pause: {duration: 5m}
        - analysis:
            templates:
              - templateName: error-rate-check
        - setWeight: 50
        - pause: {duration: 10m}
        - setWeight: 100      # Full promotion
  template:
    spec:
      containers:
        - name: app
          image: myapp:v1.2.3
---
# AnalysisTemplate — automated canary analysis
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate-check
spec:
  metrics:
    - name: error-rate
      interval: 30s
      successCondition: result[0] <= 0.01
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_errors_total{version="canary"}[2m]))
            /
            sum(rate(http_requests_total{version="canary"}[2m]))
```

### Flagger Integration

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  service:
    port: 80
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
      - name: load-test
        url: http://flagger-loadtester/
        timeout: 5s
        metadata:
          cmd: "hey -z 1m -q 10 http://myapp-canary/"
```

---

## Multi-Cluster Management

### Cluster Registration

```bash
# Add external cluster
argocd cluster add prod-eu-west-1 \
  --name prod-eu-west-1 \
  --label env=production \
  --label region=eu-west-1 \
  --label team=platform

# List managed clusters
argocd cluster list
```

### Declarative Cluster Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: prod-eu-west-1-secret
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
    env: production
    region: eu-west-1
type: Opaque
stringData:
  name: prod-eu-west-1
  server: https://prod-euw1.k8s.example.com
  config: |
    {
      "bearerToken": "<service-account-token>",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64-ca-cert>"
      }
    }
```

---

## Secrets in GitOps

### External Secrets Operator (ESO)

```yaml
# ClusterSecretStore — connects to AWS Secrets Manager
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: eso-sa
            namespace: external-secrets
---
# ExternalSecret — maps to a specific Kubernetes Secret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: team-a
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: db-credentials  # Creates this Kubernetes Secret
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: /prod/team-a/db
        property: password
    - secretKey: DB_USER
      remoteRef:
        key: /prod/team-a/db
        property: username
```

### Sealed Secrets (Alternative)

```bash
# Encrypt a secret (safe to commit to Git)
kubectl create secret generic db-creds \
  --from-literal=password=s3cr3t \
  --dry-run=client -o yaml | \
  kubeseal --controller-name sealed-secrets \
  --controller-namespace kube-system \
  --format yaml > db-creds-sealed.yaml
```

### SOPS + age — Encrypted in Git, Decrypted by Argo CD

```yaml
# .sops.yaml
creation_rules:
  - path_regex: .*.enc.yaml$
    age: age1abc123...
---
# Argo CD Configuration — enable SOPS decryption
# argocd-cm ConfigMap
data:
  application.instanceLabelKey: argocd.argoproj.io/instance
  configManagementPlugins: |
    - name: sops
      generate:
        command: ["sh", "-c"]
        args: ["sops -d $ARGOCD_ENV_SOPS_SOURCE"]
```

---

## Disaster Recovery for Argo CD

### Backup Strategy

```bash
# Back up Argo CD state (argocd namespace)
argocd admin export -n argocd > argocd-backup-$(date +%Y%m%d).yaml

# Include: Applications, AppProjects, Settings (argocd-cm, argocd-secret, argocd-rbac-cm)
```

### Rehydration (Restoring Argo CD)

```bash
# 1. Install Argo CD on new cluster
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Restore configuration
kubectl apply -f argocd-backup-20260101.yaml

# 3. Re-register clusters
argocd cluster add prod-us-east-1
argocd cluster add prod-eu-west-1

# 4. Applications will auto-sync from Git — verify
argocd app list
```

### High Availability Setup

```yaml
# HA manifests — 3 replicas, leader election, Redis HA
# argocd-repo-server: 3 replicas
# argocd-server: 3 replicas
# argocd-application-controller: 1 (leader-elected)
# redis-ha: 3 replicas (sentinel-based failover)
```

---

## Production Hardening Checklist

- [ ] Argo CD accessed via SSO (OIDC/OAuth2), not local admin accounts
- [ ] RBAC configured: project-level access per team, read-only for viewers
- [ ] `default` project restricted — teams use named projects with source/destination allowlists
- [ ] Sync windows defined for production: deny during maintenance, allow during business hours
- [ ] `selfHeal: true` and `prune: true` for all production applications
- [ ] Health checks defined for all custom resources
- [ ] External Secrets Operator (or equivalent) deployed; no plaintext secrets in Git
- [ ] Argo CD Notifications configured for sync failures, health degradations
- [ ] Backup running daily on Argo CD configuration (`argocd admin export`)
- [ ] Webhook configured for instant sync on git push (bypass 3-min polling)
- [ ] Resource limits set on all Argo CD components
- [ ] NetworkPolicy restricting Argo CD → target cluster traffic
- [ ] Audit logging enabled for all `argocd` API calls
- [ ] Disaster recovery playbook tested: restore Argo CD on a fresh cluster within 30 min
