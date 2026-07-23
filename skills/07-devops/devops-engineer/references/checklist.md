# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Remote state with encryption at rest + locking (S3+DynamoDB, GCS, Azure Blob) | `grep -rn "backend\s*\"s3\"\|backend\s*\"gcs\"\|backend\s*\"azurerm\"" main.tf \| wc -l` → ≥ 1 AND `grep -rn "encrypt\s*=\s*true\|dynamodb_table" main.tf \| wc -l` → ≥ 1 | Add S3 backend with `encrypt = true` + `dynamodb_table` for locking |
| **[S2]** | State per environment per component (blast radius isolation) | `grep -rn "key\s*=\s*.*env\|workspace_key_prefix" main.tf \| wc -l` → ≥ 1 | Separate state keys: `states/prod/networking/terraform.tfstate` |
| **[S3]** | All modules pinned by immutable git tag or commit SHA | `grep -rn "source\s*=\s*\"git::" main.tf \| grep -c "ref="` → equals total module count | Replace branch refs with `?ref=v1.2.3` or commit SHA |
| **[S4]** | Provider versions pinned (`~>` pessimistic constraint) | `grep -rn "required_providers" main.tf -A 10 \| grep "version" \| grep -c "~>"` → equals provider count | Add `version = "~> 5.0"` to each required_provider |
| **[S5]** | `terraform fmt -check` + `terraform validate` enforced in CI | `grep -rn "terraform fmt\|terraform validate" .github/workflows/ \| wc -l` → ≥ 2 | Add `terraform fmt -check -recursive` and `terraform validate` to CI |
| **[S6]** | Speculative plan posted as PR comment; apply requires human approval | `grep -rn "terraform plan" .github/workflows/ \| wc -l` → ≥ 1 AND `grep -rn "environment.*production" .github/workflows/ \| wc -l` → ≥ 1 | Add plan-to-PR-comment action + production environment protection |
| **[S7]** | Argo CD/Flux deployed and managing all Kubernetes resources | `kubectl get pods -n argocd \| grep argocd \| wc -l` → ≥ 1 OR `kubectl get pods -n flux-system \| wc -l` → ≥ 1 | `helm install argocd argo/argo-cd` |
| **[S8]** | `selfHeal: true` and `prune: true` for production applications | `grep -rn "selfHeal:\s*true" argocd/ \| wc -l` → ≥ 1 AND `grep -rn "prune:\s*true" argocd/ \| wc -l` → ≥ 1 | Set `syncPolicy.automated.selfHeal: true` and `prune: true` |
| **[S9]** | SSO (OIDC) enabled; RBAC configured per team | `grep -rn "oidc\|dex" argocd/ \| wc -l` → ≥ 1 | Configure ArgoCD SSO with OIDC provider |
| **[S10]** | Progressive delivery configured (Argo Rollouts or Flagger) with automated analysis | `kubectl get pods -n argo-rollouts \| wc -l` → ≥ 1 OR `kubectl get pods -n flagger-system \| wc -l` → ≥ 1 | `helm install argo-rollouts argo/argo-rollouts` |
| **[S11]** | No plaintext secrets in Git, `.tfvars`, or Kubernetes manifests | `grep -rnE "(password\|secret\|token\|key)\s*=\s*\"[^\"]{8,}\"" . --include="*.tfvars" --include="*.yaml" \| wc -l` → 0 | Run `trufflehog filesystem .` and rotate any found secrets |
| **[S12]** | External Secrets Operator syncing from cloud secret manager | `kubectl get pods -n external-secrets \| wc -l` → ≥ 1 | `helm install external-secrets external-secrets/external-secrets` |
| **[S13]** | SLOs defined for all critical user journeys with error budgets | `grep -rn "SLO\|error_budget\|sloth\|pyrra" . --include="*.yaml" --include="*.tf" \| wc -l` → ≥ 1 | Generate SLO manifest with `sloth` or `pyrra` |
| **[S14]** | 3-2-1 backup rule applied to all Tier 0-2 data stores | `grep -rn "backup_vault\|backup_plan\|backup_retention" main.tf \| wc -l` → ≥ 1 AND at least 3 copies configured | Add `aws_backup_plan` with cross-region + cross-account copies |
| **[S15]** | DR test conducted within last quarter; postmortem action items tracked | `grep -rn "dr.*test\|game.*day\|failover.*test" .github/workflows/ \| wc -l` → ≥ 1 AND `find . -name "postmortem*" -mtime -90 \| wc -l` → ≥ 1 | Schedule quarterly DR test workflow + postmortem template |
