# Cloud IAM Architecture — Least Privilege Design Patterns

Reference for designing cloud IAM with least privilege across AWS, Azure, and GCP. Covers role hierarchy, permission boundaries, SCPs, and policy analysis.

---

## AWS IAM Architecture

### Role Hierarchy Design

IAM roles are the **only** secure way to grant permissions to AWS services and federated users. Never create IAM users — use AWS IAM Identity Center (SSO) for human access and IAM roles for service access.

**Role trust policies** define *who* can assume the role:
```json
{
  "Effect": "Allow",
  "Principal": { "AWS": "arn:aws:iam::111122223333:role/CrossAccountRole" },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": { "sts:ExternalId": "random-uuid-per-trusting-account" }
  }
}
```

**Permission boundaries** set a maximum permissions ceiling. Even if the role's identity-based policy grants `s3:*`, the permission boundary can limit it to specific buckets:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::app-bucket-*/*"
}
```

### Service Control Policies (SCPs)

SCPs are applied at the AWS Organization level (OU or account) and function as **guardrails** — they don't grant permissions, they only deny. Key patterns:

1. Deny leaving the organization (`organizations:LeaveOrganization`)
2. Deny disabling CloudTrail or deleting logs (`cloudtrail:StopLogging`, `cloudtrail:DeleteTrail`)
3. Deny creating public S3 ACLs (`s3:PutBucketAcl` with condition)
4. Deny root user usage (`aws:PrincipalArn` condition matches `arn:aws:iam::*:root`)
5. Region restriction (`aws:RequestedRegion` not in allowed list → deny)

### Policy Analysis Tools

- **IAM Access Analyzer**: Identifies resources shared with external entities, generates minimum-privilege policies from CloudTrail activity
- **IAM Policy Simulator**: Test policies against specific actions/resources before deployment
- **Zelkova** (underlying engine): Automated reasoning about policy behavior using SMT solvers
- **AWS Config rules**: `iam-policy-no-statements-with-admin-access`, `iam-user-no-policies-check`

## Azure RBAC + PIM

### Role-Based Access Control

Azure uses **role definitions** (JSON) assigned at management group, subscription, resource group, or resource scope. Built-in roles like `Contributor` are overly permissive — create custom roles:

```json
{
  "Name": "App-Dev-ReadOnly",
  "Actions": ["Microsoft.Compute/virtualMachines/read", "Microsoft.Storage/storageAccounts/read"],
  "NotActions": [],
  "AssignableScopes": ["/subscriptions/{sub-id}"]
}
```

### Privileged Identity Management (PIM)

PIM provides **just-in-time** privileged access:
- Eligible assignments: User is eligible to activate the role
- Time-bound activation: 1-8 hour window, requires MFA + approval
- Audit trail: All activations logged to Azure AD audit logs
- Access reviews: Quarterly review of who holds privileged roles

Preferred over permanent assignments. All Global Administrators should be PIM-eligible, not permanently assigned.

## GCP IAM Conditions

GCP uses **IAM conditions** for attribute-based access control:
```
resource.name.startsWith('projects/-/buckets/prod-')
request.time < timestamp('2026-12-31T00:00:00Z')
```

Key patterns: time-bound access, resource name prefix matching, IP address restrictions, and device policy enforcement (BeyondCorp).

## Least Privilege Implementation Pattern

```
START: Zero permissions (implicit deny)
  ⬇
1. Identify required AWS API calls (CloudTrail analysis, 14-day window)
2. Generate minimum-viable policy (IAM Access Analyzer policy generation)
3. Test in monitor mode (IAM Access Analyzer validates no denied calls)
4. After 14 days of zero denied actions, apply as active policy
5. Archive previous policy version with timestamp
6. Repeat quarterly (right-sizing never ends)
```
