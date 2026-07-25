## Domain Mapping Table

Map user requests to skill categories and template references:

| User Says | Category | Template Skill to Model From | Key Sections to Adapt |
|-----------|---------|------------------------------|----------------------|
| "I need a skill for Kubernetes" | 07-devops | docker-kubernetes, devops-engineer | Ground rules (pod security, RBAC), decisions (deployment strategy, ingress design), gotchas (misconfigured resource limits, orphaned PVs) |
| "Create a skill for data analytics" | 09-data | data-engineer, analytics-engineer | Decisions (pipeline architecture, batch vs streaming), gotchas (data quality drift, schema evolution), errors (pipeline backpressure failures) |
| "I need a GraphQL API skill" | 05-development | api-designer, backend-developer | Ground rules (N+1 prevention, query depth limiting), decisions (REST vs GraphQL), gotchas (unbounded queries, missing dataloaders) |
| "Skill for incident response" | 08-security | incident-responder, security-engineer | Ground rules (don't destroy evidence, preserve chain of custody), workflow (triage→contain→eradicate→recover), decisions (isolate vs shut down) |
| "Build skill for healthcare compliance" | 11-legal | gdpr-privacy, compliance-officer, hipaa-technical-implementation | Ground rules (HIPAA-specific: BAAs, PHI de-identification, audit controls), gotchas (PHI exposure in logs, unauthorized access), verification (audit trail completeness, access review cadence) |
| "I need a skill for React/Next.js" | 05-development | frontend-developer | Ground rules (SSR security, hydration mismatches), decisions (SSR vs SSG vs ISR), gotchas (bundle size, layout shift from missing Suspense boundaries) |
| "Create skill for AWS architecture" | 07-devops | cloud-architect, finops-engineer | Ground rules (IAM least privilege, public S3 block), decisions (EC2 vs ECS vs Lambda), gotchas (misconfigured security groups, orphaned elastic IPs) |
| "Skill for mobile security testing" | 08-security | security-reviewer, mobile-developer | Ground rules (certificate pinning, jailbreak detection), decisions (static vs dynamic analysis), gotchas (hardcoded API keys in APK, insecure data storage) |
| "I need a skill for CI/CD pipelines" | 07-devops | ci-cd-builder, devops-engineer | Ground rules (secret management in pipelines, artifact integrity), decisions (GitHub Actions vs GitLab CI vs Jenkins), gotchas (pipeline credential leakage, untested deployment scripts) |
| "Create a skill for API security testing" | 08-security | security-reviewer, api-designer | Ground rules (OWASP API Top 10, rate limiting enforcement), decisions (automated scanning vs manual review), gotchas (broken object-level authorization, excessive data exposure) |
| "Skill for FinOps cost optimization" | 07-devops | finops-engineer, cloud-architect | Ground rules (resource tagging mandate, budget alert thresholds), decisions (reserved vs spot vs on-demand), gotchas (orphaned resources, unmonitored data transfer costs) |
| "I need a skill for game development" | 05-development | game-developer, gameplay-programmer | Ground rules (frame budget awareness, asset pipeline), decisions (Unity vs Unreal vs Godot), gotchas (memory fragmentation, shader compilation stutter) |

**Using the mapping table:** Find the closest match to the user's request. The "Template Skill" column tells you which existing 10/10* skills to reference for structure. The "Key Sections to Adapt" column tells you which sections need the most domain-specific customization. Never copy-paste — template FROM, not copy.
