# Kubernetes & Container Security in Cloud Environments

Reference for securing Kubernetes clusters and container workloads across EKS, AKS, and GKE. Covers Pod Security Standards, NetworkPolicy, admission control, image signing, and runtime protection.

---

## Pod Security Standards (PSS)

Kubernetes 1.25+ includes built-in Pod Security admission controller with three policy levels:

### Privileged (unrestricted — never in production)
- Allows everything: privileged containers, hostNetwork, hostPID, hostPath volumes, all Linux capabilities
- Only for system namespaces (`kube-system`) if absolutely required

### Baseline (minimum security — minimum for all clusters)
- Blocks known privilege escalations:
  - No hostProcess containers
  - No hostNetwork, hostPID, hostIPC
  - No privileged containers
  - No hostPath volumes (or restrict to read-only specific paths)
  - Limited capabilities (drops NET_RAW, ALL)

### Restricted (hardened — production standard)
- Builds on Baseline, adds:
  - `runAsNonRoot: true` (must run as non-root user)
  - `readOnlyRootFilesystem: true`
  - `seccompProfile.type: RuntimeDefault`
  - `allowPrivilegeEscalation: false`
  - Limited capabilities (drops ALL, none added)
  - No ProcMount type

**Enforcement modes:** `enforce` (deny + audit), `audit` (warn only), `warn` (warning to user). Migration: start with `warn`, then `audit`, then `enforce` over 2-4 weeks.

## NetworkPolicy Zero-Trust Design

```
Default profile per namespace:
  1. Deny all ingress (default)
     └── Explicitly allow: ingress from ingress-nginx, monitoring namespace
  2. Deny all egress (default)
     └── Explicitly allow:
         ├── DNS (kube-dns, UDP 53)
         ├── API server (TCP 443, Kubernetes service CIDR)
         ├── Specific databases (e.g., Cloud SQL IP on TCP 5432)
         ├── S3/GCS via VPC endpoints (no egress)
         └── Any other required external services (by CIDR + port)
  3. Cross-namespace traffic: Explicit allow between specific namespaces
```

### NetworkPolicy Example (namespace `app-frontend`)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: app-frontend
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
  ingress: []  # Empty = deny all, explicitly add allows
  egress:
    - to: [{ namespaceSelector: { matchLabels: { name: kube-system } } }]
      ports: [{ protocol: UDP, port: 53 }]  # DNS only
```

## Admission Control

### Kyverno Policy Examples (Recommended over OPA Gatekeeper for K8s-native)

**Block privileged pods:**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
spec:
  validationFailureAction: Enforce
  rules:
    - name: privileged-containers
      match:
        any:
          - resources:
              kinds: [Pod]
      validate:
        message: "Privileged containers are forbidden"
        pattern:
          spec:
            containers:
              - =(securityContext):
                  =(privileged): "false"
```

**Require image signatures (Cosign):**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-image-signature
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-image
      match:
        any:
          - resources:
              kinds: [Pod]
      verifyImages:
        - imageReferences: ["*"]
          attestors:
            - entries:
                - keyless:
                    subject: "*"
                    issuer: "https://token.actions.githubusercontent.com"
                    rekor:
                      url: https://rekor.sigstore.dev
```

**Block `:latest` tag:**
```yaml
validate:
  message: "Using :latest tag is forbidden — use explicit digest or version tag"
  pattern:
    spec:
      containers:
        - image: "!*:latest"
```

## Image Signing with Cosign/Sigstore

### Build-Time Signing (in CI/CD)

```bash
# Keyless signing using OIDC (GitHub Actions identity)
cosign sign \
  --oidc-issuer https://token.actions.githubusercontent.com \
  --identity-token $ACTIONS_ID_TOKEN_REQUEST_TOKEN \
  $REGISTRY/$IMAGE:$TAG

# Attach SBOM
cosign attest --type spdxjson \
  --predicate sbom.spdx.json \
  $REGISTRY/$IMAGE:$TAG
```

### Runtime Verification (via Kyverno)

Kyverno automatically verifies Cosign signatures against Rekor transparency log at admission time. If signature is invalid or missing → pod creation denied.

## etcd Encryption

### EKS
- Enable KMS envelope encryption at cluster creation (cannot be added later)
- KMS key must exist in the same region; key deletion = cluster permanently unrecoverable
- Use `prevent_destroy` lifecycle on the Terraform resource for the KMS key

### AKS
- Enable at cluster creation via `--enable-disk-encryption-set`
- Etcd encryption at rest via Azure Disk Encryption Set (platform-managed or customer-managed keys)

### GKE
- Application-layer secrets encryption enabled by default (GKE 1.18+)
- Use Cloud KMS for customer-managed encryption keys (CMEK)

## Runtime Protection

### Falco (CNCF Graduated)

Syscall-level anomaly detection. Deploy as DaemonSet:

```yaml
# Example Falco rules
- rule: Write below etc
  desc: An attempt to write to /etc
  condition: evt.dir = < and container and (fd.name startswith /etc)
  output: "File below /etc opened for writing (user=%user.name cmdline=%proc.cmdline)"
  priority: WARNING
```

### Tetragon (Cilium/eBPF-based)

Kernel-level enforcement via eBPF. Can enforce policies (not just alert):
- Block specific syscalls
- Enforce file integrity monitoring
- Network observability + enforcement

## Image Scanning Pipeline

```
Build → SBOM (Syft) → Scan (Grype) → Sign (Cosign) → Push → Registry Scan → Admission Verify
  1. syft $IMAGE -o spdx-json > sbom.spdx.json
  2. grype $IMAGE --fail-on critical
  3. cosign sign + cosign attest
  4. docker push $IMAGE
  5. ECR/ACR/GCR enhanced scanning (Inspector, Defender, Container Analysis)
  6. Kyverno verifyImages at admission
```
