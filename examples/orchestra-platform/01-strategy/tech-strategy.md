# Orchestra Platform — Technology Strategy

## Technology Strategy

Orchestra follows a **cloud-native, API-first, open-core** model. The open-source Backstage project serves as the foundation, extended with proprietary managed services for multi-tenancy, billing, and operational tooling. Every capability is exposed via well-versioned APIs so that customers can integrate Orchestra into their existing workflows — Terraform providers, CI/CD webhooks, and a public GraphQL API are first-class concerns, not afterthoughts.

## Build vs. Buy Decisions

| Capability | Decision | Rationale |
|-----------|----------|-----------|
| Service Catalog | **Build** | Core differentiator; must own the data model and query performance |
| Template Engine | **Build** | Scaffolder is the heart of the product; custom execution sandbox required |
| Plugin Framework | **Build** | Network-effects moat; SDK design is our competitive advantage |
| Authentication | **Buy (Auth0)** | Undifferentiated heavy lifting; SOC 2 compliance out of the box |
| Billing & Subscription | **Buy (Stripe)** | Mature API, usage-based billing, invoicing, and tax handling built in |
| Customer Support | **Buy (Intercom)** | In-app messaging, knowledge base, and ticket routing |

## Engineering Organization Design

At seed stage (6 engineers), we organize into two squads:

- **Platform Squad (4 engineers):** Owns the service catalog, software templates, and the core orchestration layer. They ship the MVP experience that turns Backstage into a turnkey product.
- **Ecosystem Squad (2 engineers):** Owns the plugin SDK, plugin registry, and developer documentation. They ensure third-party developers can build and publish plugins from day one.

At Series A (15 engineers), we add a third squad for **Enterprise & Security** (SSO, audit logs, compliance) and grow each existing squad. Every squad has a tech lead reporting to the CTO; product managers are embedded at squad level.

## Vendor Evaluation Matrix

| Criteria | AWS | GCP | Azure | Winner |
|----------|-----|-----|-------|--------|
| Kubernetes maturity | EKS (best-in-class) | GKE (strong) | AKS (improving) | **AWS** |
| Managed PostgreSQL | RDS Aurora (proven) | Cloud SQL (solid) | Azure DB (solid) | **AWS** |
| KMS for SOC 2 | AWS KMS (FIPS 140-2) | Cloud KMS | Azure Key Vault | **AWS** |
| Startup credits | $100K / 2 years | $100K / 2 years | $150K / 2 years | **AWS** |

**Decision: AWS.** EKS maturity and RDS Aurora performance were the deciding factors. Azure's larger credits were attractive but operational familiarity and hiring market for AWS engineers tipped the scales.

## Key Risks

1. **Plugin SDK adoption is make-or-break.** If third-party developers don't build plugins, our marketplace network effects never materialize. Mitigation: fund 5 reference plugins ourselves and offer 90% revenue share to early partners.

2. **Dependency on Auth0 availability.** An Auth0 outage is an Orchestra outage. Mitigation: Cache validated tokens locally; maintain a migration path to a self-hosted alternative (e.g., Keycloak) if needed.

3. **Multi-tenant isolation complexity.** A noisy neighbor in a shared cluster could degrade performance for all customers. Mitigation: Namespace-level isolation in Year 1, dedicated clusters for Enterprise tier, and aggressive resource quotas enforced via OPA/Gatekeeper.
