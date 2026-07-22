# Kubernetes Patterns

> **Author:** Sandeep Kumar Penchala

Production Kubernetes patterns for pod design, deployments, config management, service mesh, autoscaling, namespaces, RBAC, and cost optimization. These patterns extend the docker-kubernetes skill's orchestration and cluster management workflows.

## Pod Design Patterns

### Init Containers

Run setup tasks before the main container starts — database migrations, config downloads, permission fixing.

```yaml
apiVersion: v1
kind: Pod
spec:
  initContainers:
    - name: db-migrate
      image: myapp:migrate
      command: ["./migrate", "up"]
      envFrom:
        - secretRef:
            name: db-credentials
    - name: wait-for-db
      image: busybox
      command: ['sh', '-c', 'until nc -z postgres 5432; do sleep 2; done']
  containers:
    - name: app
      image: myapp:latest
```

### Sidecar Pattern

```yaml
spec:
  containers:
    - name: app
      image: myapp:latest
      volumeMounts:
        - name: logs
          mountPath: /var/log/app
    - name: log-forwarder       # Sidecar — ships logs
      image: fluentd:latest
      volumeMounts:
        - name: logs
          mountPath: /var/log/app
      env:
        - name: FLUENTD_CONF
          value: "fluent.conf"
  volumes:
    - name: logs
      emptyDir: {}
```

### Probes

```yaml
spec:
  containers:
    - name: app
      # Startup probe — gives slow-starting apps time before liveness kicks in
      startupProbe:
        httpGet:
          path: /health
          port: 3000
        failureThreshold: 30    # 30 * periodSeconds = up to 5 minutes to start
        periodSeconds: 10

      # Liveness — restart if app is deadlocked/unresponsive
      livenessProbe:
        httpGet:
          path: /health
          port: 3000
        initialDelaySeconds: 0   # Skip if startupProbe defined
        periodSeconds: 15
        timeoutSeconds: 3

      # Readiness — stop sending traffic if not ready
      readinessProbe:
        httpGet:
          path: /health/ready
          port: 3000
        periodSeconds: 5
```

### Resource Limits

```yaml
resources:
  requests:           # What the scheduler reserves — basis for scheduling
    cpu: "500m"
    memory: "512Mi"
  limits:             # Hard cap — container killed if exceeded (memory)
    cpu: "2000m"
    memory: "1Gi"
# CPU is compressible (throttled), memory is not (OOMKilled)
# Rule of thumb: set requests = expected steady-state; limits = 2-4x requests
```

## Deployment Strategies

### Rolling Update (Default)

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # How many extra pods can be created
      maxUnavailable: 0    # How many pods can be unavailable during update
  template:
    spec:
      containers:
        - name: app
          image: myapp:1.2.0
```

### Blue-Green Deployment

```yaml
# Deploy green (new version) alongside blue (current)
# Service selector decides which receives traffic
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue    # Switch to 'green' to cut over
  ports:
    - port: 80
      targetPort: 3000
```

### Canary Deployment (with Istio)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp
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
          weight: 10          # 10% to canary
```

## Config Management

### ConfigMap vs Secret

| Feature | ConfigMap | Secret |
|---------|-----------|--------|
| Storage | Plain text (etcd) | Base64 encoded (etcd); can be encrypted at rest |
| Size limit | 1 MiB | 1 MiB |
| Use for | App config, feature flags, non-sensitive settings | Passwords, API keys, TLS certs, tokens |
| Immutable | Optional (`immutable: true`) | Optional (`immutable: true`) |

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
immutable: true          # Forces recreate-on-change; better for audits
data:
  username: YWRtaW4=     # echo -n 'admin' | base64
  password: c2VjcmV0
```

### External Secrets Operator

```yaml
# Sync AWS Secrets Manager secret to K8s Secret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: ClusterSecretStore
  target:
    name: db-credentials
  data:
    - secretKey: username
      remoteRef:
        key: prod/database
        property: username
    - secretKey: password
      remoteRef:
        key: prod/database
        property: password
```

## Service Mesh Decision

```
Do you have 10+ services with cross-cutting needs (mTLS, traffic splitting, observability)?
├── NO → Skip service mesh. Use K8s NetworkPolicy + Ingress/Gateway API.
└── YES → Is operational simplicity critical?
    ├── YES → Istio Ambient Mesh (no sidecars needed)
    └── NO → Standard Istio with sidecar injection
```

### Istio VirtualService + DestinationRule

```yaml
# Traffic splitting with retry policy
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
spec:
  hosts:
    - orders
  http:
    - route:
        - destination:
            host: orders
            subset: v2
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 2s
      timeout: 10s
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
spec:
  host: orders
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
    loadBalancer:
      simple: LEAST_REQUEST
```

## Autoscaling

### HPA (Horizontal Pod Autoscaler)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300     # Wait 5min before scaling down
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60               # Max 50% reduction per minute
```

### KEDA (Event-Driven Autoscaling)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-processor
spec:
  scaleTargetRef:
    name: order-processor
  minReplicaCount: 1
  maxReplicaCount: 50
  triggers:
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.eu-west-1.amazonaws.com/123456/orders
        queueLength: "10"             # Scale when 10+ messages queued
        awsRegion: eu-west-1
```

## Namespace Strategy

```
Per-environment:
  ├── prod       ← Strict RBAC; resource quotas; network policies enforced
  ├── staging    ← Mirror prod configs; realistic testing
  └── dev        ← Loose RBAC; developer self-service

Per-team (medium/large orgs):
  ├── team-payments
  ├── team-checkout
  └── team-platform

Best practices:
  - Never mix environments in same namespace
  - Namespace labels: `environment: prod`, `team: platform`, `cost-center: eng-42`
  - ResourceQuota per namespace prevents noisy neighbor
  - NetworkPolicy: deny-all by default; allow specific ingress/egress
```

## RBAC Patterns

```yaml
# Principle of Least Privilege — start with nothing, add what's needed
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
  name: developer
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log", "services", "configmaps"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "update", "patch"]
  # Explicitly DENY secrets, roles, namespaces — not listed = denied
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: dev
  name: developer-binding
subjects:
  - kind: Group
    name: developers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

## Cost Optimization

### Right-Sizing

```bash
# kubectl resource recommendations (VPA-based)
kubectl top pods --containers              # Actual usage
kubectl describe hpa myapp                 # Scaling history

# Check for wasted resources
kubectl get pods -A -o json | jq '[.items[] | {
  name: .metadata.name,
  namespace: .metadata.namespace,
  requests: .spec.containers[].resources.requests,
  limits: .spec.containers[].resources.limits
}]'
```

### Spot Instances

```yaml
# Node affinity for spot instances
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          preference:
            matchExpressions:
              - key: lifecycle
                operator: In
                values: ["spot"]
  tolerations:
    - key: "spot"
      operator: "Equal"
      value: "true"
      effect: "PreferNoSchedule"
```

### Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2     # Or `maxUnavailable: 1`
  selector:
    matchLabels:
      app: myapp
```

### Bin Packing

Schedule pods densely to minimize wasted node capacity. Use tools like Karpenter or Cluster Autoscaler with appropriate instance sizes. Target 70-80% node utilization.

These Kubernetes patterns implement the docker-kubernetes skill's orchestration layer — from pod design through autoscaling to cost optimization — ensuring every workload runs reliably, securely, and efficiently in production.
