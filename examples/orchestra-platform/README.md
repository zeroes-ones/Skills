# Orchestra Platform — A 56-Skill End-to-End Example

Building a developer platform SaaS from zero to production, exercising every skill in the library in a realistic sequence. This isn't a tutorial — it's a field manual showing how skills chain together, what each produces, and how handoffs work.

## The Scenario

**Orchestra** is an internal developer platform (IDP) SaaS. Think Backstage-as-a-service: service catalog, software templates, developer self-service, and plugin marketplace. Target: mid-market engineering teams (50-200 engineers) that want platform benefits without the platform team overhead.

## Skill Chain Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: FOUNDATION                          │
│  ceo-strategist ──► business-strategist ──► cto-advisor             │
│       │                    │                      │                 │
│       ▼                    ▼                      ▼                 │
│  product-strategist ◄── idea-to-spec ◄── project-manager            │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 2: DESIGN & ARCHITECTURE                  │
│  ux-researcher ──► ui-ux-designer ──► brand-guidelines              │
│       │                  │                    │                     │
│       ▼                  ▼                    ▼                     │
│  accessibility-auditor ◄── system-architect                         │
│       │                         │                                   │
│       ▼                         ▼                                   │
│  api-designer ◄── database-designer ──► networking-engineer         │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 3: BUILD & VERIFY                         │
│  backend-developer ──► frontend-developer ◄── mobile-developer      │
│       │                      │                    │                 │
│       ▼                      ▼                    ▼                 │
│  fullstack-developer ──► localization-engineer                      │
│       │                                                             │
│       ▼                                                             │
│  code-reviewer ──► qa-engineer ──► security-reviewer ◄── scrum-master│
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 4: INFRASTRUCTURE                         │
│  cloud-architect ──► devops-engineer ──► docker-kubernetes          │
│       │                    │                    │                   │
│       ▼                    ▼                    ▼                   │
│  ci-cd-builder ──► platform-engineer ──► finops-engineer            │
│       │                    │                                         │
│       ▼                    ▼                                         │
│  observability-engineer ──► site-reliability-engineer               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 5: SECURE & COMPLY                        │
│  security-engineer ──► compliance-officer                           │
│       │                      │                                      │
│       ▼                      ▼                                      │
│  incident-responder ◄── gdpr-privacy ──► legal-advisor             │
│                             │                    │                  │
│                             ▼                    ▼                  │
│                       regulatory-specialist                          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 6: DATA & INTELLIGENCE                    │
│  database-reliability-engineer ──► data-engineer                    │
│       │                                │                            │
│       ▼                                ▼                            │
│  analytics-engineer ──► data-scientist ──► ml-ai-engineer           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 7: LAUNCH & GROW                          │
│  release-manager ──► customer-support-engineer                      │
│       │                     │                                       │
│       ▼                     ▼                                       │
│  content-strategist ──► devrel-advocate ──► growth-engineer         │
│       │                     │                    │                  │
│       ▼                     ▼                    ▼                  │
│  seo-specialist ◄─── technical-writer ◄── documentation-engineer   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 8: SCALE & EVOLVE                         │
│  technical-program-manager ──► migration-architect                   │
│       │                              │                              │
│       ▼                              ▼                              │
│  monorepo-manager ──► performance-engineer ──► chaos-engineer       │
└─────────────────────────────────────────────────────────────────────┘
```

## Phase-by-Phase Walkthrough

### Phase 1: Foundation (4 skills, 1 week)

**Skill chain:** `ceo-strategist → business-strategist → cto-advisor → product-strategist`

| Skill | Input | Output |
|-------|-------|--------|
| **ceo-strategist** | "Should we build an IDP SaaS?" | Vision doc, competitive landscape, fundraising strategy, org design for seed stage. See [01-strategy/ceo-vision.md](01-strategy/ceo-vision.md) |
| **business-strategist** | Vision doc from CEO | Business model canvas (B2B SaaS, per-seat + platform fee), TAM/SAM/SOM, unit economics (LTV:CAC 4:1 target), pricing tiers. See [01-strategy/business-model.md](01-strategy/business-model.md) |
| **cto-advisor** | Business model + vision | Build vs buy analysis (build core, buy auth/payments), technology strategy, engineering org design (6 engineers, 2 squads), vendor evaluation. See [01-strategy/tech-strategy.md](01-strategy/tech-strategy.md) |
| **product-strategist** | Tech strategy + business model | Product vision, 18-month roadmap, competitive analysis (Backstage, Port, Cortex), feature prioritization (RICE framework). See [01-strategy/product-strategy.md](01-strategy/product-strategy.md) |

**Key decision from this phase:** Build the service catalog and software templates first (highest RICE score). Plugin marketplace in v2. Skip self-hosted — go cloud-first.

### Phase 2: Design & Architecture (8 skills, 2 weeks)

**Skill chain:** `ux-researcher → ui-ux-designer → brand-guidelines → accessibility-auditor → system-architect → api-designer → database-designer → networking-engineer`

| Skill | Input | Output |
|-------|-------|--------|
| **ux-researcher** | Product strategy, target persona (platform team lead) | User research plan, 12 interview summaries, journey map: "Platform engineer onboarding a new service." See [02-product/ux-research.md](02-product/ux-research.md) |
| **ui-ux-designer** | Journey maps, brand strategy | Wireframes (service catalog, template wizard, plugin config), design system tokens, Figma prototype. See [03-design/ui-ux.md](03-design/ui-ux.md) |
| **brand-guidelines** | Product name, target audience | Brand architecture (Orchestra parent + plugin sub-brands), color palette (#1A1A2E primary, WCAG AA verified), typography (Inter + JetBrains Mono), iconography system. See [03-design/brand.md](03-design/brand.md) |
| **accessibility-auditor** | UI designs, component library | WCAG 2.2 AA audit: 94% pass rate, 12 findings (4 focus management, 3 color contrast, 2 ARIA labels, 3 keyboard nav). See [03-design/accessibility.md](03-design/accessibility.md) |
| **system-architect** | Product spec, NFRs (99.9% uptime, p95 < 200ms, 10k concurrent) | C4 diagrams (context, container, component), ADRs (microservices over monolith, PostgreSQL primary DB, Redis for caching, RabbitMQ for async), tech stack decision matrix. See [04-architecture/system-arch.md](04-architecture/system-arch.md) |
| **api-designer** | System architecture, domain model | OpenAPI 3.1 spec: Catalog API, Templates API, Plugins API, Auth API. REST + GraphQL hybrid. Pagination, filtering, versioning strategy. See [04-architecture/api-design.md](04-architecture/api-design.md) |
| **database-designer** | Domain model, access patterns (read-heavy catalog, write-light config) | Schema design (7 tables in services domain, 5 in templates), indexing strategy, migration plan, data retention policy. See [04-architecture/database-design.md](04-architecture/database-design.md) |
| **networking-engineer** | Architecture, deployment model (AWS) | VPC design (public/private subnets, NAT gateway), DNS (orchestra.dev), CDN (CloudFront), WAF rules, zero-trust service mesh. See [04-architecture/networking.md](04-architecture/networking.md) |

**Key output:** Architecture Decision Records (ADRs) for all major decisions. API spec that frontend and backend teams develop against in parallel.

### Phase 3: Build & Verify (7 skills, 6 weeks)

**Skill chain:** `backend-developer → frontend-developer → fullstack-developer → mobile-developer → localization-engineer → code-reviewer → qa-engineer → security-reviewer`

| Skill | Input | Output |
|-------|-------|--------|
| **backend-developer** | API spec, database schema | Go services: catalog-service, template-engine, plugin-registry, auth-service. gRPC for internal, REST for external. JWT auth, rate limiting, circuit breakers. See [05-development/backend.md](05-development/backend.md) |
| **frontend-developer** | API spec, Figma designs, brand guidelines | React + TypeScript SPA: service catalog with search/filter, template wizard (5-step form), plugin config dashboard, admin panel. State management with Zustand, React Query for API. See [05-development/frontend.md](05-development/frontend.md) |
| **fullstack-developer** | Backend + frontend integration points | BFF layer (Next.js API routes), SSR for catalog pages, real-time WebSocket for template execution status, end-to-end type safety with tRPC types shared between frontend/backend. See [05-development/fullstack.md](05-development/fullstack.md) |
| **mobile-developer** | API spec, design system | React Native companion app: service health dashboard, on-call alert management, template execution monitoring. Not full platform — read-only operational view. See [05-development/mobile.md](05-development/mobile.md) |
| **localization-engineer** | All UI strings, date/number formats | i18n setup (react-i18next), English + German launch locales, RTL-ready layout, pseudolocalization testing complete, translation pipeline (Lokalise integration). See [05-development/localization.md](05-development/localization.md) |
| **code-reviewer** | All PRs from sprints 1-6 | 47 PRs reviewed: 3 architecture concerns, 12 performance findings, 8 security issues, 41 style nits (auto-fixed). Zero blockers at merge. See [06-quality/code-review.md](06-quality/code-review.md) |
| **qa-engineer** | Feature specs, deployed staging | Test strategy (test pyramid: 60% unit, 30% integration, 10% E2E), 247 automated tests, 12 manual test cases, performance baseline (p95 < 180ms), load test (1k concurrent users). See [06-quality/qa.md](06-quality/qa.md) |
| **security-reviewer** | Codebase, API surface, infrastructure config | STRIDE threat model (7 threats, 2 high), OWASP Top 10 audit (0 critical, 2 medium), dependency scan (3 CVEs, all patched), API security review (JWT rotation, CORS policy, rate limiting verified). See [06-quality/security-review.md](06-quality/security-review.md) |

**Sprint cadence:** 2-week sprints, scrum-master facilitating throughout. 3 sprints to MVP.

### Phase 4: Infrastructure (7 skills, 3 weeks)

**Skill chain:** `cloud-architect → devops-engineer → docker-kubernetes → ci-cd-builder → platform-engineer → finops-engineer → observability-engineer → site-reliability-engineer`

| Skill | Input | Output |
|-------|-------|--------|
| **cloud-architect** | System architecture, NFRs | AWS landing zone (3 accounts: dev, staging, prod), EKS cluster design (3 AZs, spot instances for dev), RDS Aurora PostgreSQL, ElastiCache Redis, S3 for artifacts. See [07-devops/cloud-arch.md](07-devops/cloud-arch.md) |
| **devops-engineer** | Cloud architecture | Terraform modules (networking, compute, data, monitoring), GitOps with ArgoCD, secrets with AWS Secrets Manager + Vault, Atlantis for Terraform automation. See [07-devops/devops.md](07-devops/devops.md) |
| **docker-kubernetes** | Service manifests, deployment requirements | Multi-stage Dockerfiles (prod images < 200MB), Kubernetes manifests (Deployment, Service, Ingress, HPA, PDB), Helm charts per service, Istio service mesh. See [07-devops/docker-k8s.md](07-devops/docker-k8s.md) |
| **ci-cd-builder** | Repo structure, deployment targets | GitHub Actions: lint → test → build → scan → deploy-staging → integration-test → deploy-prod. Matrix builds, artifact caching, SLSA Level 3 provenance, DORA metrics dashboard. See [07-devops/ci-cd.md](07-devops/ci-cd.md) |
| **platform-engineer** | Developer workflows, toolchain | Backstage developer portal (customized), golden path templates (new service in 15 min), self-service infrastructure (Terraform modules behind Backstage scaffolder), developer CLI (orc CLI). See [07-devops/platform.md](07-devops/platform.md) |
| **finops-engineer** | Cloud architecture, usage estimates | Cost model ($12.5k/month at 100 customers, $45k/month at 1000), reserved instance strategy (1-year commit saves 30%), waste reduction (5 unattached EBS volumes, 12 unused elastic IPs), unit economics ($125/customer/month infra cost). See [07-devops/finops.md](07-devops/finops.md) |
| **observability-engineer** | Service architecture, SLO targets | Prometheus + Grafana (RED dashboards per service), Loki for logs, Tempo for traces, OpenTelemetry instrumentation, 12 SLOs defined (99.9% API uptime, p95 latency < 200ms), alert routing to PagerDuty. See [07-devops/observability.md](07-devops/observability.md) |
| **site-reliability-engineer** | SLO definitions, incident history | Error budget policy (0.1% monthly, freeze deployments at 50% burned), toil reduction (automated 4 manual processes, saved 8 hrs/week), on-call rotation (follow-the-sun, 3 engineers), capacity planning (6-month forecast). See [07-devops/sre.md](07-devops/sre.md) |

**Key output:** Platform deploys in < 15 minutes. Rollback in < 5 minutes. All secrets in Vault, zero in code or env vars.

### Phase 5: Secure & Comply (5 skills, 2 weeks)

**Skill chain:** `security-engineer → compliance-officer → incident-responder ← gdpr-privacy ← legal-advisor ← regulatory-specialist`

| Skill | Input | Output |
|-------|-------|--------|
| **security-engineer** | Architecture, codebase, cloud config | Penetration test (2 medium findings — rate limiting bypass, IDOR on template API), IAM hardening (least-privilege policies, role-per-service), secrets rotation policy, WAF rules (OWASP Top 10 coverage). See [08-security/security.md](08-security/security.md) |
| **compliance-officer** | Security posture, data flows | SOC 2 Type I readiness assessment (8 controls need work, 24 passing), ISO 27001 control mapping, evidence collection framework, policy templates (InfoSec, Access Control, Change Management). See [08-security/compliance.md](08-security/compliance.md) |
| **gdpr-privacy** | Data flows, user data inventory | DPIA for template execution data, consent management (cookie consent + data processing opt-in), DSAR process (30-day SLA), data retention policy (90 days execution logs, 7 years billing), cookie compliance. See [11-legal/gdpr.md](11-legal/gdpr.md) |
| **legal-advisor** | Business model, data processing, IP | Terms of Service (SaaS), Privacy Policy, DPA (GDPR-compliant), MSA template, open-source license audit (MIT, Apache 2.0 — all compatible), trademark filing for "Orchestra." See [11-legal/legal.md](11-legal/legal.md) |
| **regulatory-specialist** | Product features, data handling | Not applicable for current scope (no healthcare/financial data). Prepared framework for future: HIPAA readiness checklist if healthcare customers onboard, PCI-DSS scope assessment for billing. See [11-legal/regulatory.md](11-legal/regulatory.md) |
| **incident-responder** | SRE runbooks, security findings | Incident response plan (severity levels, escalation path, communication templates), 2 tabletop exercises (data breach scenario, API outage scenario), postmortem template, on-call runbook. See [08-security/incident-response.md](08-security/incident-response.md) |

**Key output:** SOC 2 Type I ready. GDPR compliance verified. Incident response tested with 2 tabletop exercises.

### Phase 6: Data & Intelligence (5 skills, 2 weeks)

**Skill chain:** `database-reliability-engineer → data-engineer → analytics-engineer → data-scientist → ml-ai-engineer`

| Skill | Input | Output |
|-------|-------|--------|
| **database-reliability-engineer** | Database design, usage patterns | HA setup (RDS Multi-AZ, 15-min RPO, 5-min RTO), read replicas (2 for analytics), connection pooling (PgBouncer, 200 connections), backup strategy (daily snapshots + WAL archiving), zero-downtime migration plan. See [09-data/database-reliability.md](09-data/database-reliability.md) |
| **data-engineer** | Database schemas, analytics requirements | ETL pipeline (Airbyte → dbt → Snowflake), medallion architecture (bronze: raw events, silver: cleaned models, gold: business metrics), event tracking (Rudderstack), data quality checks (Great Expectations). See [09-data/data-engineering.md](09-data/data-engineering.md) |
| **analytics-engineer** | dbt models, business questions | 18 dbt models (6 staging, 8 intermediate, 4 marts), metric layer (activation rate, WAU/MAU, template execution success rate, time-to-value), Metabase dashboards for product + exec + engineering. See [09-data/analytics.md](09-data/analytics.md) |
| **data-scientist** | Cleaned data, product questions | A/B test framework (template completion rate: 68% control vs 74% variant, p=0.03, n=1,200), churn prediction model (features: login frequency, template usage, support tickets — AUC 0.82), time-to-value analysis (median 3.2 days to first service creation). See [09-data/data-science.md](09-data/data-science.md) |
| **ml-ai-engineer** | Use cases, data availability | AI-powered template recommendations (collaborative filtering, deployed as FastAPI microservice), LLM-based service description generator (fine-tuned Llama 3, internal API), model monitoring (drift detection on recommendation accuracy). See [09-data/ml-ai.md](09-data/ml-ai.md) |

**Key output:** Product analytics live. Template completion rate improved 6% via A/B test. AI recommendations driving 22% of template selections.

### Phase 7: Launch & Grow (7 skills, ongoing)

**Skill chain:** `release-manager → customer-support-engineer → content-strategist → devrel-advocate → growth-engineer → seo-specialist ← technical-writer ← documentation-engineer`

| Skill | Input | Output |
|-------|-------|--------|
| **release-manager** | All QA sign-offs, staging validation | v1.0 release train: feature freeze → staging deploy → smoke tests → go/no-go (GO) → production deploy → monitoring watch (48 hrs, no incidents). Canary: 10% → 50% → 100% over 6 hours. Feature flags: plugin marketplace behind flag. See [07-devops/release.md](07-devops/release.md) |
| **customer-support-engineer** | Product, runbooks, escalation paths | Support workflow (Intercom → Linear → PagerDuty escalation), knowledge base (42 articles at launch), SLA tiers (Enterprise: 1hr response, Pro: 4hr, Starter: 24hr), feedback loop to product (tagged issues → roadmap). See [12-operations/support.md](12-operations/support.md) |
| **content-strategist** | Product, target persona, brand | Content plan: technical blog (2x/week), changelog, case studies, comparison pages (Orchestra vs Backstage, vs Port), content calendar (Q3 2026), topic clusters (IDP, platform engineering, developer experience). See [10-growth/content.md](10-growth/content.md) |
| **devrel-advocate** | Product, content plan, developer personas | DevRel strategy: 3 conference talks (KubeCon, PlatformCon, DevOpsDays), sample code repos (5 examples), workshop ("Build your IDP in 2 hours"), community Discord (500 members in 3 months), developer newsletter (bi-weekly). See [10-growth/devrel.md](10-growth/devrel.md) |
| **growth-engineer** | Product analytics, user journey | A/B test (homepage: 12% conversion lift), onboarding optimization (time-to-value from 3.2 days to 1.8 days), referral program ("Refer a team, get 1 month free"), activation metric (first template execution = activated). See [10-growth/growth.md](10-growth/growth.md) |
| **technical-writer** | API specs, architecture docs, runbooks | API documentation (OpenAPI → Redoc, with examples), architecture docs (ADRs published), onboarding guide (5-step quickstart), changelog (keepachangelog.com format), runbook templates. See [12-operations/technical-writing.md](12-operations/technical-writing.md) |
| **documentation-engineer** | Docs content, information architecture | Docs site (Docusaurus, docs.orchestra.dev), docs-as-code pipeline (Markdown → GitHub → CI build → deploy), versioned docs (v1.0, v1.1), broken link checker (CI gate), search (Algolia). See [13-specialized/docs-engineering.md](13-specialized/docs-engineering.md) |
| **seo-specialist** | Content strategy, docs structure | Technical SEO audit (Core Web Vitals: 92 mobile, 98 desktop), schema markup (TechArticle, SoftwareApplication), keyword strategy ("internal developer platform," "Backstage alternative," "platform engineering tool"), hreflang tags for German locale. See [10-growth/seo.md](10-growth/seo.md) |

**Launch metrics (90 days):** 120 customers, 85% activation rate, 4.2% weekly churn, NPS 42, 3,200 unique docs visitors/month.

### Phase 8: Scale & Evolve (5 skills, ongoing)

**Skill chain:** `technical-program-manager → migration-architect → monorepo-manager → performance-engineer → chaos-engineer`

| Skill | Input | Output |
|-------|-------|--------|
| **technical-program-manager** | Roadmap, team velocity, customer feedback | Q4 program plan (3 initiatives: plugin SDK, enterprise SSO, multi-region), dependency map across 3 squads, risk register (7 risks, 2 with mitigation plans), exec dashboard (OKR tracking, burndown, blocker list). See [12-operations/tpm.md](12-operations/tpm.md) |
| **migration-architect** | Multi-region requirement, existing architecture | Multi-region migration plan (expand-contract pattern: deploy to eu-west-1, replicate data, switch DNS), rollback strategy (per-region feature flag), dual-write phase (2 weeks), verified cutover checklist. See [13-specialized/migration.md](13-specialized/migration.md) |
| **monorepo-manager** | Current polyrepo (7 repos), growing complexity | Turborepo migration plan (7 repos → 1 monorepo), dependency graph, build caching (remote: 73% hit rate), affected-based CI (only build/test changed packages), migration timeline (4 weeks, incremental). See [13-specialized/monorepo.md](13-specialized/monorepo.md) |
| **performance-engineer** | Production metrics, user complaints (template execution slow) | Flame graphs (CPU: template parsing 38% of time), load testing (k6: 500 RPS sustained, p95 degraded to 450ms at 800 RPS), bundle analysis (catalog page: 420KB → 180KB, code splitting), DB query optimization (3 slow queries, indexes reduced from 2.1s to 45ms). See [13-specialized/performance.md](13-specialized/performance.md) |
| **chaos-engineer** | Production architecture, SLOs | Chaos experiment catalog (5 experiments: pod kill, AZ failure, Redis primary failover, DB replica failure, network latency injection), GameDay Q4 2026 (2 findings: circuit breaker missing on plugin registry, Redis reconnection timeout too short), resilience score: 82% → 94%. See [13-specialized/chaos.md](13-specialized/chaos.md) |

**Scale metrics (6 months):** 500 customers, 99.95% uptime, p95 < 180ms, multi-region (us-east-1, eu-west-1), SOC 2 Type II in progress.

## How to Read This Example

1. **Follow the chain:** Each phase shows which skills to invoke in which order. Start at Phase 1, work forward.
2. **Read the handoffs:** The "Input" column shows what the upstream skill produced. The "Output" column shows what this skill creates for downstream.
3. **Drill into artifacts:** Each skill has a detailed artifact file in its phase folder showing actual output.
4. **Adapt for your project:** Not every project needs all 56 skills. Use the Route the Request section in each skill's SKILL.md to determine which path is relevant.

## Key Patterns Demonstrated

- **Route the Request:** Before reading any skill, the decision tree routes you to the right section. You don't read whole skills — you read what's relevant.
- **Ground Rules:** Each skill's anti-hallucination rules catch bad output before it reaches you. For example, the financial modeler never invents market sizing numbers without citing sources.
- **Cross-skills Integration:** Every skill knows its predecessors and successors. No skill works in isolation.
- **What Good Looks Like:** Each artifact has a concrete quality bar. You know when you're done.
- **Error Decoder:** When things go wrong, the error decoder tells you why and how to fix it — before you waste hours debugging.

## Running This Example Yourself

```bash
# Bootstrap a new project using the full skill chain
cd your-project
/path/to/skills/scripts/init-project.sh --full --name orchestra-platform

# Or start with just the strategy phase
/path/to/skills/scripts/init-project.sh --solo --name my-saas-idea
```

Then invoke skills in order using your agent. Reference each skill's Route the Request section to jump to the right part.

---

*This example uses all 56 skills from the [zeroes-ones/Skills](https://github.com/zeroes-ones/Skills) library. Each phase folder contains actual artifacts — specifications, diagrams, code samples, and decisions — generated by the corresponding skill.*
