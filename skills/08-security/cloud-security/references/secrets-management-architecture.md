# Secrets Management Architecture

Reference for designing secrets management with automatic rotation, dynamic secrets, and JIT credential generation across cloud providers and HashiCorp Vault.

---

## Secret Hierarchy & Classification

```
Level 0 — Root/Master Keys
  ├── AWS KMS CMK / Azure Key Vault HSM / GCP Cloud KMS
  │   └── Encrypts all other secrets (envelope encryption)
  ├── Level 1 — Infrastructure Secrets
  │   ├── Database credentials (rotate every 30 days)
  │   ├── API keys (Stripe, Twilio, SendGrid — rotate every 90 days)
  │   └── TLS certificates (ACM/Key Vault auto-renewal)
  ├── Level 2 — Application Secrets
  │   ├── OAuth client secrets (rotate every 90 days)
  │   └── Encryption keys for application-layer data
  └── Level 3 — Developer Credentials
      ├── AWS SSO / Azure AD PIM temporary credentials (max 8 hours)
      └── CI/CD OIDC tokens (max 1 hour, single-use)
```

## Provider Comparison

| Feature | AWS Secrets Manager | Azure Key Vault | GCP Secret Manager | HashiCorp Vault |
|---------|--------------------|--------------------|--------------------|-----------------|
| Pricing | $0.40/secret/month | $0.03/10K operations | $0.06/secret/month | Free (self-managed infra cost) |
| Auto rotation | Lambda-based | Event Grid + Function | Cloud Scheduler + Function | Built-in database engines |
| HSM backing | KMS (FIPS 140-2 L2) | Premium tier (FIPS 140-2 L3) | Cloud KMS (FIPS 140-2 L2) | HSM backend optional |
| Dynamic secrets | No | No | No | Yes (database, cloud, PKI) |
| Multi-cloud | AWS only | Azure only | GCP only | Yes |
| Versioning | Yes, staged labels | Yes, versions + enabled/disabled | Yes, versions + aliases | Yes, versions |
| Soft delete | 7-30 day recovery window | 7-90 day retention (must enable) | Disable + destroy with delay | Delete + undelete |

## Automatic Rotation Architecture

### Database Credentials (Multi-User Strategy)

A zero-downtime rotation pattern that maintains two valid credentials at all times:

```
Rotation Lambda/Function:
  1. Create new credential (CLONE) — e.g., myapp-user-clone
  2. Wait for credential propagation (5-15 seconds)
  3. Test CLONE credential (connect, run SELECT 1)
  4. If test succeeds: Update secret version to CLONE
  5. Update application connections (secrets manager SDK refreshes)
  6. Delete old credential from database
  7. Rename CLONE to standard name → rotation complete
  8. Next rotation: Repeat with alternating credential names
```

### CI/CD OIDC Federation (No Static Keys)

Eliminate long-lived credentials for CI/CD entirely:

```
GitHub Actions → AWS:
  - Step 1: Configure OIDC provider in AWS IAM (thumbprint: 6938fd4d98bab03faadb97b34396831e3780aea1)
  - Step 2: Create IAM role with trust policy:
      Principal: Federated (arn:aws:iam::ACCOUNT:oidc-provider/token.actions.githubusercontent.com)
      Condition:
        StringEquals: { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" }
        StringLike: { "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:*" }
  - Step 3: configure-aws-credentials action uses the role with no access keys
```

Same pattern applies to GitLab CI (CI_JOB_JWT_V2), CircleCI, and Buildkite.

## Environment Variable Elimination

Never read secrets from `process.env`. Migration path:

| Phase | Approach | Security Level |
|-------|----------|----------------|
| 1 — Current | `const pw = process.env.DB_PASSWORD` | ❌ Insecure — visible to all libraries, child processes, crash dumps |
| 2 — SDK at startup | `const pw = await secretsManager.getSecretValue()` → cache in variable | ✅ Secret fetched at runtime, not in env |
| 3 — CSI Driver (K8s) | CSI Secret Store driver mounts secrets as tmpfs volume | ✅ Secrets never on disk, in-memory only |
| 4 — External Secrets Operator | ESO syncs AWS/GCP/Azure secrets → K8s native secrets (auto-refresh) | ✅ Compatibility with apps that require K8s secrets |

## Just-in-Time Credential Generation

### Developer Access via AWS SSO / Azure AD PIM / GCP Workforce Identity

- **AWS SSO**: Permission sets with session duration 1-12 hours, MFA-enforced
- **Azure PIM**: Eligible (not permanent) role assignments, 1-8 hour activation with MFA + justification
- **GCP Workforce Identity Federation**: SAML/OIDC federated, access tokens max lifetime 12 hours

### Emergency/Break-Glass Access

- Dedicated break-glass IAM role with: MFA required, CloudTrail alarm on all assume events, 1-hour max session
- PagerDuty page to security team whenever break-glass role is assumed
- Mandatory post-incident review within 24 hours
- Quarterly test: Verify break-glass procedure works (dry run — assume role, run `aws sts get-caller-identity`, log event)
