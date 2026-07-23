# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | All images pinned by SHA256 digest, not mutable tags | `grep -rn "image:.*:latest\b\|image:.*:v[0-9]" k8s/ --include="*.yaml" \| wc -l` → 0 | Replace tags with `@sha256:...` digests |
| **[S2]** | Multi-stage builds produce minimal images; no build tools in final layer | `grep -rn "FROM.*as\|FROM.*AS" Dockerfile \| wc -l` → ≥ 2 | Convert single-stage Dockerfile to multi-stage |
| **[S3]** | Non-root user configured in every container; `allowPrivilegeEscalation: false` | `grep -rn "USER" Dockerfile \| wc -l` → ≥ 1 AND `grep -rn "allowPrivilegeEscalation:\s*false" k8s/ \| wc -l` → ≥ 1 | Add `USER 1000:1000` + `allowPrivilegeEscalation: false` |
| **[S4]** | Resource requests and limits set for every container in every namespace | `kubectl get pods -A -o json \| jq '[.items[].spec.containers[] | select(.resources.requests == null or .resources.limits == null)] | length'` → 0 | Add `resources.requests` and `resources.limits` via VPA recommender |
| **[S5]** | Liveness and readiness probes configured with appropriate initial delays | `kubectl get deployments -A -o json \| jq '[.items[] | select(.spec.template.spec.containers[].livenessProbe == null or .spec.template.spec.containers[].readinessProbe == null)] | length'` → 0 | Add `/healthz` liveness and `/ready` readiness probes |
| **[S6]** | PodDisruptionBudget defined for all deployments with replicas > 1 | `kubectl get pdb -A \| wc -l` → ≥ number of deployments with replicas > 1 | Add PDB: `minAvailable: 1` or `maxUnavailable: 25%` |
| **[S7]** | NetworkPolicy denies all by default; explicit allow rules for required flows | `kubectl get networkpolicies -A \| wc -l` → ≥ 1 per namespace | Add deny-all NetworkPolicy + explicit allow rules per service |
| **[S8]** | PodSecurityStandard enforced at `restricted` level cluster-wide | `kubectl get pods -A -o json \| jq '[.items[].spec.containers[] | select(.securityContext.allowPrivilegeEscalation != false)] | length'` → 0 | Apply `PodSecurity` admission label: `pod-security.kubernetes.io/enforce: restricted` |
| **[S9]** | Image vulnerability scanning in CI pipeline; HIGH/CRITICAL CVEs block deployment | `grep -rn "trivy\|snyk\|grype" .github/workflows/ \| wc -l` → ≥ 1 | Add `aquasecurity/trivy-action` with `--severity HIGH,CRITICAL` |
| **[S10]** | Helm charts versioned, linted, and tested before release | `grep -rn "helm lint\|helm unittest\|helm test" .github/workflows/ \| wc -l` → ≥ 2 | Add `helm lint` + `helm unittest` to CI pipeline |
| **[S11]** | cert-manager and external-dns configured for automated TLS and DNS | `kubectl get pods -n cert-manager \| wc -l` → ≥ 1 AND `kubectl get pods -n external-dns \| wc -l` → ≥ 1 | `helm install cert-manager jetstack/cert-manager` + `helm install external-dns` |
