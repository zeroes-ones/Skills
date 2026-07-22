# Terraform Patterns — Production Field Manual

## Table of Contents
1. [Module Architecture](#module-architecture)
2. [State Management](#state-management)
3. [Workspace Strategy](#workspace-strategy)
4. [Drift Detection & Remediation](#drift-detection--remediation)
5. [Terraform vs Pulumi Decision Matrix](#terraform-vs-pulumi-decision-matrix)
6. [Plan Review Process](#plan-review-process)
7. [Provider & Version Pinning](#provider--version-pinning)
8. [CI/CD Integration Patterns](#cicd-integration-patterns)

---

## Module Architecture

### Module Taxonomy

```
modules/
├── networking/          # VPC, subnets, peering, transit gateway
│   ├── vpc/
│   ├── subnet/
│   └── peering/
├── compute/             # EC2, ECS, Lambda, K8s node groups
├── data/                # RDS, ElastiCache, DynamoDB, S3
├── security/            # IAM, KMS, Security Groups, WAF
├── observability/       # CloudWatch, Grafana, alerting
└── platform/            # Org-wide: SCPs, Config rules, GuardDuty
```

### Module Versioning — Golden Rule

**Never reference `main` or mutable branches.** Pin modules by git tag or commit SHA:

```hcl
# ❌ ANTI-PATTERN — floating reference, breaks reproducibility
module "vpc" {
  source = "git::https://github.com/org/terraform-modules.git//networking/vpc?ref=main"
}

# ✅ CORRECT — immutable, auditable, deterministic
module "vpc" {
  source = "git::https://github.com/org/terraform-modules.git//networking/vpc?ref=v2.3.1"
}
```

### Module Composition Pattern

Compose small, single-purpose modules; never create monolithic "golden" modules:

```hcl
# ✅ COMPOSITION — each module owns one concern
module "vpc"       { source = "./modules/networking/vpc" }
module "rds"       { source = "./modules/data/rds" }
module "ecs"       { source = "./modules/compute/ecs" }

# ❌ ANTI-PATTERN — "application" module bundles everything
module "myapp" {
  source = "./modules/myapp"  # Creates VPC + RDS + ECS + SG — untestable, uncomposable
}
```

### Input Variable Design

```hcl
# ✅ Descriptive, validated, sensible defaults
variable "instance_type" {
  type        = string
  description = "EC2 instance type for the workload nodes."
  default     = "t3.medium"

  validation {
    condition     = can(regex("^t3\\.|^c5\\.|^m5\\.", var.instance_type))
    error_message = "Instance type must be from t3, c5, or m5 families."
  }
}

# ✅ Object types for complex config — never map(any)
variable "database_config" {
  type = object({
    engine         = string
    version        = string
    instance_class = string
    storage_gb     = number
    multi_az       = bool
  })
  description = "RDS database configuration block."

  validation {
    condition     = var.database_config.storage_gb >= 20
    error_message = "Storage must be at least 20 GB."
  }
}
```

### Output Design — The "Golden Outputs" Pattern

Every module must export:
1. **ARN/ID** for referencing in downstream resources
2. **Endpoint/hostname** for connection strings
3. **Security group ID** for networking rules

```hcl
output "rds_endpoint"        { value = aws_db_instance.main.endpoint }
output "rds_security_group"  { value = aws_security_group.rds.id }
output "rds_arn"             { value = aws_db_instance.main.arn }
```

---

## State Management

### Remote Backend — Mandatory

Local state is for prototypes only. Production requires remote state with locking:

```hcl
# AWS S3 + DynamoDB
terraform {
  backend "s3" {
    bucket         = "org-terraform-state-${var.aws_account_id}"
    key            = "prod/us-east-1/networking/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
    kms_key_id     = "alias/terraform-state"
  }
}

# GCP + GCS
terraform {
  backend "gcs" {
    bucket          = "org-tfstate-${var.project_id}"
    prefix          = "prod/networking"
    encryption_key  = "projects/org-kms/locations/global/keyRings/tfstate/cryptoKeys/tfstate"
  }
}
```

### State File Organization — Per-Environment, Per-Component

```
state/
├── prod/
│   ├── us-east-1/
│   │   ├── networking/terraform.tfstate
│   │   ├── compute/terraform.tfstate
│   │   └── data/terraform.tfstate
│   └── eu-west-1/
├── staging/
│   └── us-east-1/
└── dev/
```

**Why separate state files?** Blast radius reduction — a corrupted state file in `dev/compute` shouldn't block `prod/networking`.

### State Manipulation — Emergency Procedures

```bash
# Remove a resource from state without destroying it (orphaned import)
terraform state rm 'aws_instance.legacy_server'

# Move a resource between state files (refactoring modules)
terraform state mv -state-out=../compute/terraform.tfstate \
  'module.vpc.aws_security_group.app' \
  'module.app.aws_security_group.main'

# Import existing infrastructure
terraform import aws_instance.bastion i-0a1b2c3d4e5f67890
```

### State File Encryption & Access Control

| Requirement | Implementation |
|---|---|
| Encryption at rest | S3 SSE-KMS / GCS CMEK / Azure Storage encryption |
| Encryption in transit | TLS 1.2+ enforced by cloud provider APIs |
| Access audit trail | S3 access logs / Cloud Audit Logs, alert on unauthorized reads |
| Break-glass access | Separate IAM role with `s3:GetObject` on state bucket, short-lived sessions |

---

## Workspace Strategy

### Terraform Cloud/Enterprise Workspaces

```
Organization: acme-corp
├── Workspace: prod-us-east-1-networking     (execution mode: remote)
├── Workspace: prod-us-east-1-compute        (execution mode: remote)
├── Workspace: prod-us-east-1-data           (execution mode: remote)
├── Workspace: staging-us-east-1-networking  (execution mode: remote)
└── Workspace: dev-sandbox                   (execution mode: local)
```

### CLI Workspaces (OSS) — When to Use

CLI workspaces (`terraform workspace`) are per-backend, not per-directory:

```bash
# Create workspace per environment (single backend config)
terraform workspace new prod
terraform workspace new staging
terraform workspace select prod
terraform apply -var-file="prod.tfvars"
```

**Decision: CLI workspaces vs. directory-per-environment**

| Factor | CLI Workspaces | Directory-per-Env |
|---|---|---|
| Code duplication | None | Some (backend config repeated) |
| Blast radius | Higher — single state bucket | Lower — separate state paths |
| CI/CD complexity | Lower — one pipeline | Higher — pipeline per env |
| Terraform Cloud compat | Native | Workspaces map to dirs |
| **Recommendation** | Small teams, <3 envs | Enterprise, strict separation |

### Workspace Variable Sets (TFC/E)

```hcl
# Sensitive — marked as such, never in VCS
variable "db_password" { sensitive = true }

# Environment-specific — set per workspace
variable "instance_count" { default = 2 }  # Override to 5 in prod workspace
```

---

## Drift Detection & Remediation

### Detection Pipeline

```yaml
# GitHub Actions — scheduled drift scan
name: Drift Detection
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  drift-check:
    strategy:
      matrix:
        workspace: [prod-us-east-1-networking, prod-us-east-1-compute]
    steps:
      - uses: actions/checkout@<sha>
      - uses: hashicorp/setup-terraform@<sha>
      - run: terraform init
      - run: terraform plan -detailed-exitcode -out=plan.tfplan
        continue-on-error: true
      - name: Alert on drift
        if: failure()
        run: |
          # Post to Slack/Teams with plan summary
          terraform show -json plan.tfplan | \
            jq '.resource_changes[] | select(.change.actions != ["no-op"])' | \
            slack-notify "Drift detected in ${{ matrix.workspace }}"
```

### Drift Classification

| Category | Example | Response |
|---|---|---|
| **Benign manual fix** | Someone added a tag in console | Update `.tf` to match reality |
| **Security incident** | Security group opened to `0.0.0.0/0` | **Page on-call**, revert immediately, investigate |
| **Capacity adjustment** | Auto-scaling group changed manually | Formalize in IaC or codify the auto-scaling policy |
| **Shadow IT** | Unknown resources in account | Import or destroy; update onboarding docs |

### Automated Remediation (with Guard Rails)

```hcl
# OPA/Checkov policy: must-have tags
# .checkov.yml
soft-fail: false
check:
  - CKV_AWS_23  # Security group description required
  - CKV_AWS_111 # IAM policy attached to groups/roles only
```

---

## Terraform vs Pulumi Decision Matrix

| Dimension | Terraform | Pulumi |
|---|---|---|
| **Language** | HCL (declarative DSL) | TypeScript, Python, Go, C#, Java |
| **State management** | HCL-defined backend | Pulumi Service or self-managed (S3, GCS, Azure) |
| **Abstraction** | Modules + `count`/`for_each` | Real functions, classes, loops, conditionals |
| **Testing** | `terraform test` (basic), Terratest | Standard unit/integration test frameworks |
| **Ecosystem** | 3,000+ providers, massive community | Growing, can use Terraform providers via bridge |
| **Learning curve** | Moderate (HCL) | Low for devs (familiar languages) |
| **Multi-cloud** | Excellent — any provider | Excellent — native SDK integration |
| **Policy as code** | Sentinel, OPA, Checkov | CrossGuard (OPA-based), Pulumi Policy Packs |

### When to Choose Terraform
- Infrastructure team with ops/SRE background
- Mature ecosystem needed (every SaaS has a Terraform provider)
- Org-wide compliance rules already expressed in Sentinel/OPA
- State needs to live in your cloud account, not a SaaS backend

### When to Choose Pulumi
- Developer-owned infrastructure (platform engineering)
- Complex logic: loops with `break`/`continue`, dynamic resource creation based on API calls
- Team already strong in TypeScript/Python/Go
- Need to share code between infra and app (e.g., same types/interfaces)
- Testing infrastructure with standard frameworks (pytest, jest, etc.)

### Hybrid Pattern

```
Terraform: "Platform" layer — VPCs, IAM, org-wide policies, shared services
Pulumi:    "Application" layer — per-service infra defined by dev teams
Bridge:    Pulumi references Terraform outputs via stack references
```

---

## Plan Review Process

### PR Checklist for Terraform Changes

```
## Terraform Plan Review

### Safety
- [ ] No resource replacement (`-/+`) unless intentional (check force recreation)
- [ ] No security group or IAM policy deletions without understanding blast radius
- [ ] No state file path changes

### Cost
- [ ] New resources have cost tags (`cost_center`, `environment`)
- [ ] Instance/storage sizes are right-sized per environment
- [ ] Reserved instance coverage considered for stable workloads

### Operations
- [ ] All new resources tagged with `managed_by = "terraform"`
- [ ] Module version updated if applicable
- [ ] Plan includes `No changes` for resources outside this PR's scope

### Compliance
- [ ] Checkov/OPA scan passes with zero high/critical violations
- [ ] Secrets not hardcoded — use `sensitive = true` variables or Vault data sources
```

### Plan Output Interpretation

```bash
# Plan summary symbols
# +    create
# -    destroy
# -/+  destroy then recreate (REVIEW: data loss risk!)
# ~    update in-place
# <=   read from data source

# Quick safety scan — any -/+ replacements?
terraform plan -out=plan.tfplan 2>&1 | grep -c "\-/+"  # Must be zero without justification
```

### Plan Review Anti-Patterns

1. **Blind `terraform apply -auto-approve` in CI** — always require human review for prod
2. **Reviewing only the plan summary, not each resource change** — "Plan: 3 to add, 1 to change" hides a destroy-recreate of a database
3. **Skipping plan for "trivial" changes** — a one-line IAM change can grant `*:*`
4. **Not diffing the `.tf` changes alongside the plan output** — the plan tells you *what*; the code tells you *why*

---

## Provider & Version Pinning

```hcl
terraform {
  required_version = ">= 1.9.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.70"  # Allows 5.70.x, not 5.71+
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.32"
    }
  }
}

# Provider configuration with explicit region
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      managed_by   = "terraform"
      environment  = var.environment
      repository   = "github.com/org/infra"
    }
  }

  assume_role {
    role_arn     = "arn:aws:iam::${var.aws_account_id}:role/TerraformExecution"
    session_name = "terraform-apply"
  }
}
```

---

## CI/CD Integration Patterns

### Speculative Plan on PR

```yaml
name: Terraform Plan
on: [pull_request]

jobs:
  plan:
    runs-on: ubuntu-latest
    permissions:
      id-token: write    # OIDC
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@<sha>
      - uses: aws-actions/configure-aws-credentials@<sha>
        with:
          role-to-assume: arn:aws:iam::111111111111:role/GitHubActionsTerraform
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@<sha>
      - run: terraform fmt -check -recursive
      - run: terraform init
      - run: terraform validate
      - run: terraform plan -no-color -out=plan.tfplan
      - uses: actions/github-script@<sha>
        with:
          script: |
            // Post plan output as PR comment
            const plan = `### Terraform Plan\n\`\`\`\n${steps.plan.outputs.stdout}\n\`\`\``
            github.rest.issues.createComment({ ... })
```

### Apply on Merge

```yaml
name: Terraform Apply
on:
  push:
    branches: [main]

jobs:
  apply:
    runs-on: ubuntu-latest
    environment: production  # Protection rules enforced
    steps:
      # ... same init as plan job ...
      - run: terraform apply -auto-approve plan.tfplan
      - name: Smoke test
        run: curl -f https://api.example.com/health || terraform destroy -auto-approve  # Immediate rollback
```

### `terragrunt.hcl` for DRY Configurations

```hcl
# terragrunt.hcl (root)
remote_state {
  backend = "s3"
  config = {
    bucket  = "org-terraform-state"
    key     = "${path_relative_to_include()}/terraform.tfstate"
    encrypt = true
  }
}

# prod/us-east-1/networking/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "git::https://github.com/org/modules.git//networking/vpc?ref=v2.3.1"
}

inputs = {
  cidr_block = "10.0.0.0/16"
  az_count   = 3
}
```

---

## Production Hardening Checklist

- [ ] Remote state with encryption at rest + locking (S3+DynamoDB, GCS, Azure Blob)
- [ ] State files organized per-environment, per-component (blast radius isolation)
- [ ] All modules pinned by immutable tag or commit SHA
- [ ] Provider versions pinned with pessimistic constraint (`~>`)
- [ ] `terraform fmt -check` enforced in CI pre-commit
- [ ] `terraform validate` runs on every PR
- [ ] Speculative plan posted as PR comment; apply requires human approval
- [ ] Drift detection runs on schedule with Slack/PagerDuty alerting
- [ ] OPA/Checkov policy scan in CI pipeline; high/critical blocks apply
- [ ] No secrets in `.tf` or `.tfvars` — use Vault data sources or `sensitive = true`
- [ ] IAM roles for Terraform follow least privilege (separate plan vs apply roles)
- [ ] State file access logged; alerts on unauthorized reads
- [ ] Break-glass procedure documented for emergency state manipulation
- [ ] Terraform version pinned; team standardized on a single version
