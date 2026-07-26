# security-compliance

Reference documentation for the automation-engineer skill — SAST (Semgrep, CodeQL, SonarQube), DAST (OWASP ZAP, Burp Suite), SCA (Snyk, Dependabot, OSV-Scanner), container & secret scanning, SBOM generation, image signing, compliance automation (SOC2, HIPAA, GDPR, SLSA), pre-commit hooks, and policy-as-code enforcement.

## SAST: Static Application Security Testing

### Semgrep — custom rules, multi-language, SARIF output

```yaml
# .semgrep.yml — multi-language ruleset
rules:
  - id: no-hardcoded-secrets
    patterns:
      - pattern-either:
          - pattern: $PASSWORD = "..."
          - pattern: $API_KEY = "..."
    message: "Hardcoded secret detected. Use environment variables or a secrets manager."
    languages: [python, javascript, typescript, java, go]
    severity: ERROR

  - id: no-eval
    pattern: eval(...)
    message: "eval() is dangerous. Avoid dynamic code execution."
    languages: [javascript, typescript, python]
    severity: WARNING

  - id: sql-injection-python
    patterns:
      - pattern: cursor.execute("..." % ...)
    message: "SQL injection risk. Use parameterized queries."
    languages: [python]
    severity: ERROR
```

```yaml
# .github/workflows/semgrep.yml
semgrep:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: semgrep/semgrep-action@v1
      id: semgrep
      with:
        config: p/default
        configFile: .semgrep.yml
    - uses: github/codeql-action/upload-sarif@v3
      if: always()
      with:
        sarif_file: semgrep.sarif
```

```bash
# CLI usage
semgrep --config auto .                          # auto-detect languages
semgrep --config .semgrep.yml --sarif -o results.sarif .
semgrep --config "p/owasp-top-ten" .             # OWASP Top 10 rules
semgrep --config "p/r2c-security-audit" .         # comprehensive security audit
```

### CodeQL — GitHub-native, query packs, PR integration

```yaml
# .github/workflows/codeql.yml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'          # weekly Monday scan

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    strategy:
      fail-fast: false
      matrix:
        language: [javascript, python, go]
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-extended,security-and-quality
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
```

```yaml
# Custom query pack config
# .github/codeql/codeql-config.yml
name: "Custom CodeQL Config"
disable-default-queries: false
queries:
  - uses: security-extended
  - uses: security-and-quality
  - uses: ./.github/codeql/custom-queries/
packs:
  - codeql/${{ language }}-queries
paths-ignore:
  - tests/**
  - vendor/**
```

### SonarQube — quality gates, project config

```properties
# sonar-project.properties
sonar.projectKey=myorg:myapp
sonar.projectName=myapp
sonar.sources=src/
sonar.tests=tests/
sonar.language=py
sonar.python.version=3.12
sonar.coverage.exclusions=tests/**,migrations/**
sonar.qualitygate.wait=true             # block pipeline on gate failure
```

```yaml
# CI: SonarQube scan
sonarqube:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0                   # needed for blame data
    - uses: SonarSource/sonarqube-scan-action@v3
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
    - uses: SonarSource/sonarqube-quality-gate-action@v1
      timeout-minutes: 5
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## DAST: Dynamic Application Security Testing

### OWASP ZAP — baseline, full, and API scans

```bash
# Baseline scan (passive only — fast, safe for CI)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://staging.example.com \
  -r zap-baseline-report.html \
  -J zap-baseline-report.json

# Full scan (active attacks — staging only)
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t https://staging.example.com \
  -r zap-full-report.html \
  -I                       # fail on any alerts

# API scan (OpenAPI spec-driven)
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://staging.example.com/api/openapi.json \
  -f openapi \
  -r zap-api-report.html
```

```yaml
# .github/workflows/zap.yml — CI integration
zap-scan:
  runs-on: ubuntu-latest
  environment: staging
  steps:
    - run: |
        docker run --network host -v $(pwd):/zap/wrk \
          owasp/zap2docker-stable zap-baseline.py \
          -t https://staging.example.com \
          -J zap-report.json \
          -I || echo "ZAP found alerts"
    - uses: actions/upload-artifact@v4
      if: always()
      with:
        name: zap-report
        path: zap-report.json
```

### Burp Suite Enterprise

```bash
# Burp Enterprise — scheduled scan via API
curl -X POST https://burp.example.com/graphql/v1 \
  -H "Authorization: $BURP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { start_scan(input: { site_id: \"stg-example\", scan_configuration_id: \"full-audit\" }) { id } }"
  }'

# Poll scan status
curl -s https://burp.example.com/graphql/v1 \
  -H "Authorization: $BURP_API_KEY" \
  -d '{"query": "{ scan(id: \"SCAN_ID\") { status issues { severity count } } }" }'
```

## SCA: Software Composition Analysis

### Snyk — monitor, test, auto-fix, license compliance

```bash
# Test for vulnerabilities (fails on issues above threshold)
snyk test --severity-threshold=high

# Monitor project in Snyk dashboard (always passes CI)
snyk monitor

# Auto-fix PRs
snyk fix

# License compliance
snyk test --json | jq '.licensesPolicy'
```

```yaml
# .github/workflows/snyk.yml
snyk:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: snyk/actions/setup@master
    - name: Snyk Open Source test
      run: snyk test --severity-threshold=high
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
    - name: Snyk Container test
      run: snyk container test ghcr.io/${{ github.repository }}:${{ github.sha }} --severity-threshold=high
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
    - name: Snyk IaC test
      run: snyk iac test --severity-threshold=high
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### Dependabot — auto-PRs, grouped updates

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
      day: monday
    open-pull-requests-limit: 10
    groups:
      dev-deps:
        patterns:
          - "eslint*"
          - "@typescript-eslint/*"
          - "prettier*"
        update-types: [minor, patch]
    labels: [dependencies]
    reviewers: [team-platform]

  - package-ecosystem: docker
    directory: "/"
    schedule:
      interval: weekly

  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly
```

### OWASP Dependency-Check, OSV-Scanner

```bash
# OWASP Dependency-Check
dependency-check --project myapp --scan ./ --format HTML --out ./reports/

# OSV-Scanner (fast, works with lockfiles)
osv-scanner scan -r .                                    # recursive scan
osv-scanner scan --lockfile package-lock.json
osv-scanner scan --format sarif --output osv-results.sarif .
```

```yaml
# CI: OSV-Scanner
- uses: google/osv-scanner-action@v1
  with:
    scan-args: |-
      --format=sarif
      --output=osv-results.sarif
      -r .
- uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: osv-results.sarif
```

## Container scanning

### Trivy — filesystem + image modes, SBOM

```bash
# Filesystem scan (before building image)
trivy fs --severity CRITICAL,HIGH --exit-code 1 ./

# Image scan (after build)
trivy image --severity CRITICAL,HIGH --exit-code 1 myapp:v1.0.0

# Generate SBOM
trivy image --format spdx-json --output sbom.spdx.json myapp:v1.0.0
trivy image --format cyclonedx --output sbom.cdx.json myapp:v1.0.0
```

```yaml
# .github/workflows/trivy.yml
trivy:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: fs
        scanners: vuln,secret,misconfig
        severity: CRITICAL,HIGH
        exit-code: 1
        format: sarif
        output: trivy.sarif
    - uses: github/codeql-action/upload-sarif@v3
      if: always()
      with:
        sarif_file: trivy.sarif
```

### Grype, Docker Scout

```bash
# Grype
grype myapp:v1.0.0 --fail-on critical
grype ./                                          # scan directory (SBOM-based)

# Docker Scout
docker scout quickview myapp:v1.0.0
docker scout cves myapp:v1.0.0 --only-severity critical,high
```

## Secret scanning

### Gitleaks — pre-commit hook + CI

```bash
# Run scan
gitleaks detect --source . --verbose
gitleaks detect --report-format sarif --report-path gitleaks.sarif
```

```toml
# .gitleaks.toml — allow rules
[allowlist]
  description = "global allow list"
  paths = [
    '''go\.sum''',
    '''package-lock\.json''',
    '''\.github/workflows/test\.yml''',
  ]
  regexes = [
    '''EXAMPLE_API_KEY=''',           # test fixtures
  ]

[[rules]]
  id = "generic-api-key"
  [rules.allowlist]
    paths = ['''tests/fixtures/''']
```

```yaml
# .github/workflows/gitleaks.yml
gitleaks:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    - uses: gitleaks/gitleaks-action@v2
```

```bash
# Pre-commit hook with lefthook
# lefthook.yml
pre-commit:
  commands:
    gitleaks:
      run: gitleaks protect --staged --verbose
```

### truffleHog — verify mode, git history scan

```bash
# Scan current state
trufflehog filesystem .

# Scan git history (all branches)
trufflehog git file://. --only-verified

# CI scan — verify secrets are real (API key checks)
trufflehog git file://. --since-commit HEAD~10 --only-verified --json
```

```yaml
# CI: truffleHog
trufflehog:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    - uses: trufflesecurity/trufflehog-action@v3
      with:
        extra_args: --only-verified
```

### detect-secrets — baseline file

```bash
# Create baseline (records known secrets to suppress)
detect-secrets scan > .secrets.baseline

# Audit baseline (review and mark false positives)
detect-secrets audit .secrets.baseline

# CI: scan against baseline, fail on new secrets
detect-secrets scan --baseline .secrets.baseline $(git ls-files)
```

## SBOM generation

### Syft — SPDX + CycloneDX output

```bash
# Generate SBOM from container image
syft myapp:v1.0.0 -o spdx-json > sbom.spdx.json
syft myapp:v1.0.0 -o cyclonedx-json > sbom.cdx.json

# Generate SBOM from filesystem
syft dir:. -o spdx-json > filesystem-sbom.spdx.json
```

### CycloneDX CLI + attach to GitHub Releases

```bash
# Generate from package manifests
cyclonedx-py -r -i requirements.txt -o bom.json
cyclonedx-npm --output bom.json

# Attach SBOM to GitHub Release
gh release upload v1.0.0 sbom.spdx.json sbom.cdx.json
```

```yaml
# CI: Generate + attach SBOM
sbom:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: anchore/sbom-action@v0
      with:
        image: ghcr.io/${{ github.repository }}:${{ github.sha }}
        format: spdx-json
        output-file: sbom.spdx.json
    - uses: anchore/sbom-action@v0
      with:
        image: ghcr.io/${{ github.repository }}:${{ github.sha }}
        format: cyclonedx-json
        output-file: sbom.cdx.json
    - name: Attach SBOMs to release
      if: startsWith(github.ref, 'refs/tags/')
      run: |
        gh release upload ${{ github.ref_name }} sbom.spdx.json sbom.cdx.json
```

## Image signing: Cosign + policy-controller

```bash
# Keyless signing (OIDC)
cosign sign --yes ghcr.io/myorg/myapp:v1.0.0

# Verify keyless
cosign verify ghcr.io/myorg/myapp:v1.0.0 \
  --certificate-identity https://github.com/myorg/myapp/.github/workflows/release.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com

# Sign with key pair
cosign generate-key-pair
cosign sign --key cosign.key ghcr.io/myorg/myapp:v1.0.0
cosign verify --key cosign.pub ghcr.io/myorg/myapp:v1.0.0

# Sign + attest SBOM
cosign attest --key cosign.key --predicate sbom.spdx.json --type spdx ghcr.io/myorg/myapp:v1.0.0
```

```yaml
# K8s: policy-controller — enforce signed images
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: require-github-signed
spec:
  images:
    - glob: "ghcr.io/myorg/**"
  authorities:
    - keyless:
        identities:
          - issuer: https://token.actions.githubusercontent.com
            subjectRegExp: "https://github.com/myorg/.*"
```

## Compliance automation

### SOC2 — automated evidence collection

```yaml
# CI: Evidence collection pipeline
# Collect build logs, test results, deployment records as SOC2 evidence
evidence-collect:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: |
        mkdir -p evidence/$(date +%Y-%m)/soc2/
        # CI/CD pipeline logs as evidence of change management
        curl -s -H "Authorization: Bearer $GH_TOKEN" \
          "${{ github.api_url }}/repos/${{ github.repository }}/actions/runs/${{ github.run_id }}/logs" \
          -o evidence/$(date +%Y-%m)/soc2/pipeline-logs-${{ github.run_id }}.zip
    - name: Capture deployment record
      run: |
        echo "environment: production" >> evidence/$(date +%Y-%m)/soc2/deploy-record.txt
        echo "commit: ${{ github.sha }}" >> evidence/$(date +%Y-%m)/soc2/deploy-record.txt
        echo "timestamp: $(date -Iseconds)" >> evidence/$(date +%Y-%m)/soc2/deploy-record.txt
        echo "approved_by: $(git log -1 --format='%an <%ae>')" >> evidence/$(date +%Y-%m)/soc2/deploy-record.txt
    - uses: actions/upload-artifact@v4
      with:
        name: soc2-evidence
        path: evidence/
```

```yaml
# Access review automation
# Scheduled job: list all IAM users/roles and export for quarterly review
access-review:
  runs-on: ubuntu-latest
  schedule: '0 0 1 */3 *'          # quarterly
  steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789:role/AuditRole
    - run: |
        aws iam list-users --output json > access-review/users.json
        aws iam list-roles --output json > access-review/roles.json
        aws iam get-account-authorization-details --output json > access-review/full-audit.json
    - uses: actions/upload-artifact@v4
      with:
        name: access-review-$(date +%Y-Q%q)
        path: access-review/
```

### HIPAA — BAA verification, encryption checks

```bash
# Verify KMS key rotation for encryption at rest
aws kms get-key-rotation-status --key-id alias/app-encryption-key
aws kms list-keys --query 'Keys[].KeyId' --output text | \
  xargs -I {} aws kms get-key-rotation-status --key-id {} --query 'KeyRotationEnabled'

# Verify TLS enforcement on load balancers
aws elbv2 describe-listeners --load-balancer-arn $ALB_ARN \
  --query 'Listeners[?Protocol!=`HTTPS`].ListenerArn' \
  --output text | grep -q . && echo "FAIL: Non-HTTPS listener found" && exit 1 || echo "OK"
```

```yaml
# CI: HIPAA encryption compliance gate
hipaa-encryption-check:
  runs-on: ubuntu-latest
  steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789:role/ComplianceRole
    - name: Verify encryption at rest
      run: |
        # Check S3 buckets have default encryption
        aws s3api list-buckets --query 'Buckets[].Name' --output text | tr '\t' '\n' | while read bucket; do
          enc=$(aws s3api get-bucket-encryption --bucket "$bucket" 2>/dev/null || echo "NONE")
          [ "$enc" = "NONE" ] && echo "FAIL: $bucket has no encryption" && exit 1
        done
    - name: Verify encryption in transit
      run: |
        # Check RDS instances enforce SSL
        aws rds describe-db-instances --query 'DBInstances[?!contains(DBParameterGroups[].DBParameterGroupName, `ssl`)]' \
          --output text | grep -q . && echo "WARN: Some RDS instances may not enforce SSL"
```

### GDPR — data inventory, DSAR pipeline, retention enforcement

```bash
# Tag-based resource discovery for data inventory
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=data-classification,Values=pii \
  --query 'ResourceTagMappingList[].ResourceARN' --output table

# Automated data retention scan (S3 lifecycle checks)
aws s3api get-bucket-lifecycle-configuration --bucket myapp-data --query 'Rules[].Expiration'
```

```yaml
# CI: DSAR (Data Subject Access Request) pipeline
dsar-pipeline:
  runs-on: ubuntu-latest
  inputs:
    subject-id:
      required: true
  steps:
    - name: Query PII stores
      run: |
        # Query user data across all services
        psql "$DATABASE_URL" -c "SELECT * FROM users WHERE id = '${{ inputs.subject-id }}'" -o dsar/users.json -t -A
        psql "$DATABASE_URL" -c "SELECT * FROM orders WHERE user_id = '${{ inputs.subject-id }}'" -o dsar/orders.json -t -A
    - name: Compile DSAR report
      run: |
        jq -s '{ user: .[0], orders: .[1] }' dsar/users.json dsar/orders.json > dsar/report.json
        # Encrypt report with recipient's public key
        gpg --encrypt --recipient dpo@example.com dsar/report.json
    - name: Upload encrypted report
      uses: actions/upload-artifact@v4
      with:
        name: dsar-${{ inputs.subject-id }}
        path: dsar/report.json.gpg
```

### Audit trails — immutable logs + signed attestations

```hcl
# Terraform: S3 with Object Lock for immutable pipeline logs
resource "aws_s3_bucket" "audit_logs" {
  bucket = "myorg-audit-logs"
}
resource "aws_s3_bucket_object_lock_configuration" "audit_lock" {
  bucket = aws_s3_bucket.audit_logs.id
  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = 2555                # 7 years
    }
  }
}
```

```bash
# Cosign: Sign build provenance attestation (Rekor transparency log)
cosign attest --predicate slsa-provenance.json --type slsaprovenance ghcr.io/myorg/myapp:v1.0.0
cosign verify-attestation --type slsaprovenance ghcr.io/myorg/myapp:v1.0.0
```

### SLSA framework — Level 1-4 build provenance

```yaml
# SLSA Level 3 build provenance via GitHub Actions reusable workflow
# .github/workflows/slsa-build.yml
name: SLSA Build
on:
  push:
    tags: ['v*']
jobs:
  build:
    permissions:
      id-token: write
      contents: read
      actions: read
    uses: slsa-framework/slsa-github-generator/.github/workflows/builder_go_slsa3.yml@v2
    with:
      go-version: "1.22"
```

```json
// SLSA provenance attestation (generated by slsa-github-generator)
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{
    "name": "ghcr.io/myorg/myapp",
    "digest": { "sha256": "abc123..." }
  }],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": {
      "buildType": "https://slsa-framework.github.io/github-actions-buildtypes/workflow/v1",
      "externalParameters": {
        "workflow": { "ref": "refs/tags/v1.0.0", "repository": "https://github.com/myorg/myapp", "path": ".github/workflows/release.yml" }
      }
    },
    "runDetails": {
      "builder": { "id": "https://github.com/slsa-framework/slsa-github-generator/.github/workflows/builder_go_slsa3.yml@v2" },
      "buildMetadata": { "invocationId": "https://github.com/myorg/myapp/actions/runs/123456789/attempts/1" }
    }
  }
}
```

```bash
# Verify SLSA provenance
slsa-verifier verify-image ghcr.io/myorg/myapp:v1.0.0 \
  --source-uri github.com/myorg/myapp \
  --source-tag v1.0.0
```

## Pre-commit hooks

### lefthook

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    eslint:
      glob: "*.{js,ts,tsx}"
      run: npx eslint --fix {staged_files}
    prettier:
      glob: "*.{js,ts,tsx,json,md,yaml}"
      run: npx prettier --write {staged_files}
    gitleaks:
      run: gitleaks protect --staged --verbose
    detect-secrets:
      run: detect-secrets-hook --baseline .secrets.baseline {staged_files}

pre-push:
  commands:
    test:
      run: npm test -- --ci
```

### pre-commit framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/anchore/syft
    rev: v1.8.0
    hooks:
      - id: syft
        args: ['.', '-o', 'cyclonedx-json']
```

### husky (Node.js)

```bash
npx husky-init && npm install
npx husky add .husky/pre-commit "npx lint-staged && gitleaks protect --staged --verbose"
npx husky add .husky/commit-msg "npx commitlint --edit \$1"
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yaml}": ["prettier --write"]
  }
}
```

## Policy-as-code — security enforcement

### Open Policy Agent (OPA) + Rego

```rego
# policy/deny_public_s3.rego
package terraform.analysis

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    resource.change.after.acl == "public-read"
    msg = sprintf("S3 bucket %s has public-read ACL — denied", [resource.address])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group_rule"
    resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
    resource.change.after.from_port <= 22
    resource.change.after.to_port >= 22
    msg = sprintf("SSH open to world on %s — denied", [resource.address])
}
```

```bash
# Evaluate Terraform plan against OPA policy
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan | opa eval --format pretty --data policy/ --input - 'data.terraform.analysis.deny'
```

### Checkov — IaC + K8s policy scanning

```yaml
# .github/workflows/checkov.yml
checkov:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: bridgecrewio/checkov-action@v12
      with:
        directory: .
        framework: terraform,kubernetes,dockerfile,github_actions
        output_format: sarif
        output_file_path: checkov.sarif
        soft_fail: false
```

```bash
# CLI
checkov -d . --framework terraform kubernetes dockerfile
checkov -f deployment.yaml --framework kubernetes
checkov -d deploy/ --skip-check CKV_AWS_20,CKV_AWS_21  # skip specific checks
```

### Kyverno — K8s admission policies

```yaml
# Require resource limits on all pods
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-resources
      match:
        any:
          - resources:
              kinds: [Pod]
      validate:
        message: "CPU and memory limits are required"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-image-tag
      match:
        any:
          - resources:
              kinds: [Pod]
      validate:
        message: "Image tag 'latest' is not allowed"
        pattern:
          spec:
            containers:
              - image: "!*:latest"
```

```yaml
# CI: Kyverno test
kyverno-test:
  runs-on: ubuntu-latest
  steps:
    - run: |
        curl -LO https://github.com/kyverno/kyverno/releases/latest/download/kyverno-cli_linux_x86_64.tar.gz
        tar xf kyverno-cli_linux_x86_64.tar.gz
        ./kyverno apply policies/ --resource deploy/
```

### CI pipeline: unified security gate

```yaml
# .github/workflows/security-gate.yml
name: Security Gate
on:
  pull_request:
  push:
    branches: [main]

jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2

  sast:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        tool: [semgrep, codeql]
    steps:
      - uses: actions/checkout@v4
      - if: matrix.tool == 'semgrep'
        uses: semgrep/semgrep-action@v1
        with: { config: p/default }
      - if: matrix.tool == 'codeql'
        uses: github/codeql-action/init@v3
        with: { languages: python }

  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx snyk test --severity-threshold=high
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  iac-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: bridgecrewio/checkov-action@v12
        with:
          directory: .
          soft_fail: false

  container-scan:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          severity: CRITICAL,HIGH
          exit-code: 1

  sign:
    runs-on: ubuntu-latest
    needs: [sast, sca, iac-scan, container-scan]
    permissions:
      id-token: write
    steps:
      - uses: sigstore/cosign-installer@v3
      - run: cosign sign --yes ghcr.io/${{ github.repository }}:${{ github.sha }}
