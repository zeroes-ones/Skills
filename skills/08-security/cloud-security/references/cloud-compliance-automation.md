# Cloud Compliance Automation

Reference for automating cloud compliance with CIS benchmarks, PCI DSS, HIPAA, SOC 2 control mapping, and compliance-as-code tooling.

---

## CIS Benchmarks Overview

The Center for Internet Security (CIS) publishes cloud-specific benchmarks that are the **de facto** standard for cloud compliance. Most auditors accept CIS benchmark-derived reports.

| Cloud | Benchmark | Controls | Key Tools |
|-------|-----------|----------|-----------|
| AWS | CIS AWS Foundations v2.0.0 | 49 controls (Identity, Logging, Monitoring, Networking) | Prowler, AWS Config conformance packs, ScoutSuite |
| Azure | CIS Azure Foundations v2.0.0 | ~90 controls (IAM, Logging, Networking, Compute, Storage) | Prowler (multi-cloud), Azure Policy initiatives, ScoutSuite |
| GCP | CIS GCP Foundations v2.0.0 | ~90 controls (IAM, Logging, Networking, Compute, Storage, K8s) | Prowler (multi-cloud), GCP Security Command Center, Forseti |
| Kubernetes | CIS K8s Benchmark v1.7.0 | Master node, etcd, worker node, policies | kube-bench, Trivy, checkov |

## Compliance Scanning Tools

### Prowler (AWS + Multi-Cloud)

- **Coverage**: 300+ checks across CIS, PCI DSS, HIPAA, GDPR, SOC 2, ENS, AWS Foundational Technical Review (FTR)
- **Output**: CSV, JSON, HTML, ASFF (Security Hub format)
- **Deployment**: CLI, Lambda scheduled, Docker, GitHub Actions
- **Typical pipeline**: `prowler aws -M csv,json-ocsf,html -o /output` → findings aggregated in Security Hub

### AWS Config Conformance Packs

Pre-built compliance packs deploy AWS Config rules en masse:
```
CIS AWS Foundations Benchmark v2.0.0 — 49 rules
Operational Best Practices for PCI DSS 4.0 — 30+ rules
Operational Best Practices for HIPAA Security — 40+ rules
Operational Best Practices for NIST 800-53 Rev 5 — 150+ rules
```

Deploy via CloudFormation template or AWS Config console.

### Azure Policy Initiatives

Azure Policy maps to compliance frameworks:
- **CIS Microsoft Azure Foundations Benchmark**: Built-in initiative with 90+ policies
- **PCI DSS v4.0**: Built-in initiative with 60+ policies
- **AuditIfNotExists / DeployIfNotExists**: Automatic remediation for non-compliant resources

### GCP Security Command Center

Premium tier includes compliance reports for CIS, PCI DSS, ISO 27001, SOC 1/2/3, NIST 800-53. Custom detectors can be created using Security Health Analytics.

## Compliance-as-Code

### Terraform Sentinel (Terraform Cloud/Enterprise)

Policy-as-code that evaluates `tfplan` before apply:
```sentinel
import "tfplan/v2" as tfplan

s3_buckets_encrypted = rule {
  all tfplan.resource_changes as _, rc {
    rc.type is "aws_s3_bucket" and
    rc.change.after.server_side_encryption_configuration[0].rule[0].apply_server_side_encryption_by_default is not null
  }
}
main = rule { s3_buckets_encrypted }
```

### Open Policy Agent (OPA) with Rego

```rego
package terraform.aws.s3

deny[msg] {
  bucket := input.resource_changes[_]
  bucket.type == "aws_s3_bucket"
  not bucket.change.after.server_side_encryption_configuration
  msg = sprintf("S3 bucket %v must have encryption enabled", [bucket.name])
}
```

### Regula (Fugue)

Pre-built Rego rules evaluating Terraform and CloudFormation against CIS, PCI, NIST, SOC 2. CI/CD integration via `regula run` with SARIF output for GitHub code scanning.

### CloudFormation Guard (cfn-guard)

AWS-native policy validation for CloudFormation:
```
let s3_buckets = Resources.*[ Type == 'AWS::S3::Bucket' ]
rule S3_BUCKET_ENCRYPTION when %s3_buckets !empty {
  %s3_buckets.Properties.BucketEncryption EXISTS
}
```

## Continuous Monitoring Pipeline

```
Scheduled scan (daily 06:00 UTC):
  Prowler/ScoutSuite →
    aggregate findings →
      Security Hub / Log Analytics →
        severity filter →
          CRITICAL: PagerDuty page
          HIGH:    Slack/Teams alert
          MEDIUM:  Weekly email digest
          LOW:     Monthly dashboard report

Real-time monitoring:
  AWS Config / Azure Policy →
    detection (seconds-minutes) →
      remediation (auto or manual) →
        drift detection →
          alert if IaC-captured resource changed manually
```

## Evidence Collection for Audits

For SOC 2 Type II, PCI DSS ROC, and HIPAA attestation:
1. **CloudTrail/Audit Logs**: 7-year retention with legal hold, SHA-256 log file validation enabled
2. **Config timeline**: Configuration Item (CI) history for every resource, exportable to S3
3. **Security Hub findings**: Automated evidence of control effectiveness
4. **Access reviews**: IAM credential reports, PIM audit logs, quarterly access review documentation
5. **Remediation evidence**: Auto-remediated findings with before/after state captured in logs
