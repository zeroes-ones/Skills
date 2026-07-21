# Product Strategy — Orchestra Platform

**Skill:** product-strategist
**Input:** CEO vision, business model, tech strategy

## Product Vision

Orchestra makes platform engineering accessible to every engineering team — not just those who can afford a dedicated platform team. By 2028, 50% of mid-market engineering orgs will use an IDP. Orchestra will power 20% of them.

## 18-Month Roadmap

| Quarter | Theme | Key Deliverables |
|---------|-------|-----------------|
| Q3 2026 | **Core** | Service catalog, 5 software templates, plugin framework, admin dashboard |
| Q4 2026 | **Ecosystem** | Plugin marketplace (10 launch partners), custom template builder, webhook integrations |
| Q1 2027 | **Enterprise** | SSO (Okta, Azure AD), audit logs, RBAC, SOC 2 Type II, usage analytics |
| Q2 2027 | **Intelligence** | AI-powered template recommendations, automated service health scoring, anomaly detection |

## Competitive Analysis

| Competitor | Strengths | Weaknesses | Orchestra Advantage |
|-----------|-----------|------------|-------------------|
| **Backstage** (Spotify) | Open-source, huge community, plugin ecosystem | Self-hosted only, needs 2+ FTE platform team, complex setup | Managed cloud, zero ops, 15-min onboarding |
| **Port** | Great developer portal UX, no-code config | Expensive (starts at $7.5K/month), not open-source, limited templates | Open-core, per-seat pricing, transparent |
| **Cortex** | Service catalog is best-in-class, Scorecards | Focused on catalog only, no templates, enterprise-only pricing | Full platform: catalog + templates + plugins |

## Feature Prioritization (RICE)

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Service catalog (CRUD + search) | 100% | 3 | 90% | 4 weeks | 67.5 |
| Software templates (5 built-in) | 95% | 3 | 85% | 6 weeks | 40.4 |
| Plugin framework | 70% | 2 | 70% | 8 weeks | 12.3 |
| Plugin marketplace | 40% | 2 | 50% | 12 weeks | 3.3 |
| AI recommendations | 60% | 1.5 | 40% | 8 weeks | 4.5 |

**MVP:** Service catalog + templates + plugin framework (RICE > 10).

## Key Assumptions to Validate

1. Mid-market teams will pay $29/dev/month for managed IDP — validate with 20 pricing interviews
2. Plugin ecosystem will create network effects — validate with 5 design partners building plugins
3. Template library is the primary adoption driver — track template usage as north star metric
