# Infrastructure as Code (IaC) Security Scanning

Reference for scanning Terraform, CloudFormation, Pulumi, Kubernetes manifests, and other IaC for security misconfigurations before deployment.

---

## Scanning Tools Comparison

| Tool | IaC Support | Policy Count | Custom Policies | Output Formats | Speed |
|------|------------|--------------|-----------------|---------------|-------|
| **tfsec** | Terraform only | 2000+ | Go-based custom checks, YAML config | SARIF, JSON, JUnit, Checkstyle | Very fast (<1s for 50 resources) |
| **checkov** | Terraform, CFN, K8s, Helm, ARM, Bicep, Dockerfile, Serverless, Pulumi | 750+ | Python + YAML custom policies, Graph checks | SARIF, JSON, JUnit, CLI | Fast (1-5s for 50 resources) |
| **terrascan** | Terraform, CFN, K8s, Helm, ARM | 500+ | OPA Rego policies | JSON, YAML, XML, JUnit | Moderate (5-15s) |
| **cfn-nag** | CloudFormation only | 140+ | Ruby-based custom rules | Colored CLI, JSON | Fast |
| **cfn-guard** | CloudFormation only | AWS-provided rules + custom | Guard rules v2 (domain-specific language) | JSON, CLI table | Fast |
| **kube-linter** | Kubernetes YAML | 60+ | YAML config | JSON, SARIF | Fast |
| **Trivy** | Terraform, K8s, Dockerfile, CloudFormation | 500+ | OPA Rego | SARIF, JSON, Table | Moderate |

## Custom Policies vs Built-In Rules

### When Built-In Rules Are Enough

- You follow standard CIS benchmarks and cloud provider security best practices
- Your team uses well-known IaC patterns (standard Terraform modules)
- You need fast deployment with minimal customization overhead

### When You Need Custom Policies

- Organization-specific security requirements (e.g., "Every tag must include `DataClassification: Internal|Confidential|Restricted`")
- Custom compliance requirements not covered by CIS benchmarks
- Internal naming conventions, AMI whitelists, approved instance types
- Cost control guardrails (e.g., "No instance type larger than m5.2xlarge without approval")

## Tool-Specific Configuration

### tfsec Configuration (`.tfsec/config.yml`)

```yaml
severity: HIGH,CRITICAL
minimum_severity: HIGH
exclude:
  - aws-s3-enable-bucket-logging  # Handled by organization-wide logging
  - aws-ec2-require-vpc           # False positive for VPC resources
format: sarif
output: tfsec-results.sarif
```

### checkov Configuration (`.checkov.yml`)

```yaml
branch: main
check:
  - CKV_AWS_*      # All AWS checks
  - CKV_K8S_*      # All Kubernetes checks
  - CKV_GHACTION_* # GitHub Actions checks
skip-check:
  - CKV_AWS_18     # S3 bucket logging (centralized)
  - CKV_AWS_111    # IAM policy wildcard (context-dependent)
soft-fail-on:
  - MEDIUM         # Medium findings don't block merge
hard-fail-on:
  - CRITICAL
  - HIGH
```

### cfn-nag (CloudFormation)

Inline suppression in CloudFormation template:
```yaml
Metadata:
  cfn_nag:
    rules_to_suppress:
      - id: W28
        reason: "Instance in private subnet, no public IP, access via SSM Session Manager"
      - id: F1000
        reason: "IAM role requires these specific permissions per documented architecture"
```

## CI/CD Integration Pattern

### Pre-Commit Hooks (`.pre-commit-config.yaml`)

```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.88.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_tfsec
        args: ['--args=--minimum-severity=HIGH']
  - repo: https://github.com/bridgecrewio/checkov
    rev: 3.2.0
    hooks:
      - id: checkov
        args: ['--soft-fail', '--quiet']
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

### GitHub Actions Pipeline

```yaml
name: IaC Security Scan
on: [pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tfsec
        uses: aquasecurity/tfsec-pr-commenter-action@v1.3.1
        with:
          tfsec_args: --minimum-severity HIGH --format sarif
          github_token: ${{ secrets.GITHUB_TOKEN }}
      - name: Run checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          soft_fail: true
          output_format: sarif
      - name: Upload SARIF results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

### GitLab CI Pipeline

```yaml
iac-scan:
  stage: security
  script:
    - tfsec --format junit --out tfsec-report.xml .
    - checkov -d . --soft-fail -o junitxml --output-file-path checkov-report.xml
  artifacts:
    reports:
      junit:
        - tfsec-report.xml
        - checkov-report.xml
    when: always
```

## Drift Detection

Resources deployed via IaC can drift over time due to emergency console changes, resource modifications, or automatic resource updates. Daily drift detection is essential:

```bash
# AWS: CloudFormation drift detection
aws cloudformation detect-stack-drift --stack-name prod-vpc

# Terraform: Check for drift
terraform plan -detailed-exitcode
# Exit code 0: no changes, 1: error, 2: drift detected

# Azure: Resource Graph query for resources modified outside IaC
az graph query -q "resources | where tags['IaC'] != 'true'"

# GCP: Config Connector sync status
kubectl get resourcechanges --all-namespaces
```

Drift alerts should fire within 1 hour of any change made outside the IaC pipeline, with automatic remediation where safe (re-apply Terraform for known-safe resources like tags and security groups).
