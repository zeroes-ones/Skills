# Scale Depth: From 2 Repos to 200+

Scaling a multirepo ecosystem through organizational growth stages requires different strategies at each level. Here's the roadmap from startup to enterprise.

## Stage 1: Solo/Small (2-5 repos, 1-3 teams)

**Pattern:**
```
backend/     # Monolith API
frontend/    # SPA
contracts/   # Shared types (optional)
```

**Key Practices:**
- Simple CI: one workflow per repo, no orchestration needed
- Direct Git dependencies (`"@org/shared": "file:../shared"`)
- Manual coordination: Slack or hallway conversations suffice
- No formal breaking change process — just talk to the other team

**When to move on:** You need a third team and contracts start breaking silently.

## Stage 2: Medium (5-20 repos, 4-10 teams)

**Pattern:**
```
contracts/       # Published OpenAPI/Protobuf specs
toolkit/         # Shared CI, linting, auth middleware
auth/            # Identity service
billing/         # Payments service
gateway/         # API gateway
user-service/    # User profiles
notification/    # Email/push/SMS
web/             # Frontend SPA
admin/           # Admin dashboard
mobile/          # React Native app
```

**Key Practices:**
- Shared CI templates in toolkit repo
- Semver versioning for internal packages
- Automated dependency updates (Renovate)
- Breaking change deprecation cycle (1 minor version grace period)
- CODEOWNERS on every repo
- Weekly "repo health" standup: which repos are drifting?

**When to move on:** 10+ teams, cross-repo coordination becomes the bottleneck.

## Stage 3: Large (20-100 repos, 10-50 teams)

**Pattern:**
```
platform/
├── contracts/           # All API specs
├── toolkit/             # Shared tooling
├── service-catalog/     # Backstage/Port entries
└── sdk-generator/       # Client SDKs from contracts

domains/
├── identity/            # auth/, user-service/, permissions/
├── commerce/            # billing/, payments/, invoicing/
├── content/             # cms/, search/, recommendations/
└── analytics/           # events/, reporting/, data-warehouse/

infrastructure/
├── terraform-modules/
├── kubernetes-charts/
└── ci-templates/
```

**Key Practices:**
- Platform team dedicated to cross-cutting concerns
- InnerSource model: domain teams contribute to platform repos
- Architecture Review Board for breaking changes
- Automated CDC (Consumer-Driven Contract) testing
- Monorepo builds for tightly coupled domains; polyrepo for loosely coupled
- Quarterly calibration: are repo boundaries correct?

**When to move on:** 50+ teams, you need federated governance.

## Stage 4: Enterprise (100-500+ repos, 50-200+ teams)

**Pattern:**
```
Federated platform with multiple platform teams:
- DevEx team (tooling, CI, local dev)
- API platform team (contracts, gateway, SDKs)
- Infrastructure platform (TF modules, K8s, observability)
- Security platform (auth, secrets, compliance)
- Data platform (events, warehouse, ML infra)

Domain teams own their repos; platform teams own shared infrastructure.
```

**Key Practices:**
- Multiple platform teams, each with clear scope
- Federated CODEOWNERS with escalation paths
- Automated repo lifecycle management (incubating → active → deprecated → archived)
- Centralized service catalog (Backstage)
- SLO-based cross-repo monitoring
- Annual architecture review for repo topology

## The Key Insight

The number of repos doesn't matter as much as **how well team boundaries align with repo boundaries**. Conway's Law is inescapable: your repo structure will mirror your communication structure. Design both together.
