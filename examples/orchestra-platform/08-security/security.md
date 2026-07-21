# Security Engineering

## Penetration Test Results

**Engagement**: July 5–9, 2026, by Cobalt.io (3 testers, 40 hours)  
**Scope**: orchestra.dev web application, API, and mobile app  
**Findings**: 2 Medium severity, 0 High, 0 Critical

**MED-001 — Rate Limiting Bypass on Login API**: The `/api/auth/login` endpoint enforced rate limiting by source IP, but did not account for the `X-Forwarded-For` header being spoofed. An attacker could cycle through IPs in the header to bypass the 5-attempt-per-minute limit. **Fix**: Rate limiting moved to the ALB level using AWS WAF token-based rate limiting with a client-signed challenge, independent of IP headers. Deployed July 10. Verified by retest July 12.

**MED-002 — Insecure Direct Object Reference on Template API**: The endpoint `GET /api/templates/:id/executions` returned execution history without verifying that the requesting user had access to the template's organization. A user from org-A could enumerate execution IDs of org-B's templates. **Fix**: Added an organization-scoped authorization middleware using the session's `org_id` claim. Middleware applies to 14 affected endpoints across templates and plugins. Deployed July 11. Verified by retest July 12.

## IAM Hardening

All Kubernetes workloads use IAM Roles for Service Accounts (IRSA) — no long-lived AWS credentials in the cluster. Policies follow least-privilege: each service account has exactly the permissions needed (e.g., `template-executor` can only `s3:GetObject` on `arn:aws:s3:::orchestra-templates-prod/*` and `sqs:SendMessage` on its dedicated queue). Zero IAM policies contain `"Resource": "*"` in production. IAM Access Analyzer runs daily and has flagged 0 findings for 42 consecutive days.

## WAF Rules in Production

| Rule | Source | Action |
|------|--------|--------|
| Rate limit — global | Custom | Block after 1,000 req/5min per IP |
| Rate limit — login | Custom | Block after 20 req/5min per token |
| SQL injection | AWS Managed — SQL Database | Block |
| XSS | AWS Managed — Cross Site Scripting | Block |
| CSRF origin check | Custom (checks Origin/Referer headers) | Block mismatches |
| IP reputation | AWS Managed — IP Reputation List | Block known bad actors |
| Geo-block | Custom | Block North Korea, Iran, Syria, Cuba |

## Secrets Management

All secrets (API keys, DB passwords, signing keys) stored in HashiCorp Vault with a 90-day automatic rotation policy. Kubernetes workloads consume secrets via the Vault Sidecar Injector — secrets are mounted as temporary files, never in environment variables. Database credentials rotate via Vault's PostgreSQL secret engine with a 7-day TTL and automatic renewal. Rotation failures trigger a PagerDuty P2 alert.

## Dependency Scanning

CI pipeline runs `osv-scanner` (open-source vulnerabilities) and `trivy` (container image scanning) on every PR. Blocking policy: no CRITICAL or HIGH vulnerabilities in dependencies. Dependabot configured for automatic minor/patch updates on npm and Go modules (auto-merge if CI passes). Current dependency status: 0 known vulnerabilities across 847 npm packages and 94 Go modules.
