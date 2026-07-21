# Sub-Skill Architecture Map

> **Author:** Sandeep Kumar Penchala  
> **Purpose:** Iterative sub-skill thinking for every domain — industry-specific, phase-specific, role-specific depth

---

## How Sub-Skills Work

Each parent skill identifies sub-skills that an agent can dive into iteratively. This enables:

1. **Progressive depth** — Start with parent skill for overview, then drill into sub-skills for specifics
2. **Token efficiency** — Agent loads only the sub-skill references needed for the current task
3. **Domain completeness** — No gaps — every aspect of a role is covered by a sub-skill

---

## Domain 01: Strategy & Leadership

### CEO Strategist
| Sub-Skill | When to Use | Industry Variations |
|-----------|-------------|---------------------|
| `fundraising-strategy` | Raising any round (pre-seed → Series C+) | SaaS metrics (ARR, NDR) vs marketplace (GMV) vs hardware (margins) |
| `board-management` | Board meetings, governance, investor relations | VC-backed vs bootstrapped vs public company board dynamics |
| `org-design` | Hiring first 10, scaling to 100, 500+ | Remote-first vs hybrid vs in-office org structures |
| `competitive-strategy` | Market entry, pivot, defending against competitors | B2B (enterprise sales cycles) vs B2C (viral growth) strategies |
| `crisis-management` | PR crisis, security breach, down round, co-founder conflict | Industry-specific crisis scenarios and response templates |
| `m-and-a-strategy` | Acquiring or being acquired | Tech M&A vs PE acquisition vs strategic acquisition |
| `vision-to-execution` | Translating 5-year vision to quarterly OKRs | Early-stage (pivots) vs growth-stage (execution) vs mature (innovation) |

### CTO Advisor
| Sub-Skill | When to Use | Tech Variations |
|-----------|-------------|-----------------|
| `build-vs-buy` | Every major technology decision | SaaS tools vs internal tools vs open-source customization |
| `tech-debt-management` | Quarterly technical health assessment | Startup debt vs scale-up modernization vs enterprise legacy |
| `architecture-governance` | RFC process, architecture review board | 5-person team vs 50-person vs 500-person engineering org |
| `hiring-tech-team` | First engineer → VP Engineering → CTO transition | Generalist vs specialist hiring at each stage |
| `tech-due-diligence` | Fundraising, acquisition, enterprise sales | What investors vs acquirers vs enterprise customers evaluate |
| `innovation-management` | R&D allocation, hackathons, 20% time | 0→1 innovation vs incremental improvement vs disruptive bets |
| `vendor-evaluation` | Selecting SaaS, cloud, infrastructure providers | Build vs integrate — total cost of ownership over 3 years |

### Business Strategist
| Sub-Skill | When to Use | Model Variations |
|-----------|-------------|-----------------|
| `business-model-design` | New product, pivot, new market entry | SaaS, marketplace, subscription, transactional, freemium, ad-supported |
| `unit-economics` | Fundraising, pricing, profitability analysis | CAC, LTV, payback period by business model |
| `gtm-strategy` | Launch, expansion, new vertical | PLG vs sales-led vs channel vs community-led |
| `market-sizing` | Fundraising, new market entry | TAM/SAM/SOM methodology, bottom-up vs top-down |
| `pricing-strategy` | Launch, enterprise tier, international | Usage-based, per-seat, hybrid, freemium conversion |
| `partnership-strategy` | Channel sales, integrations, platform plays | Technical vs go-to-market vs strategic partnerships |

---

## Domain 02: Product Management

### Product Manager
| Sub-Skill | When to Use | Context Variations |
|-----------|-------------|---------------------|
| `discovery-methodology` | New feature, new product, pivot | B2B (customer interviews) vs B2C (analytics, A/B tests) |
| `prd-writing` | Any feature spec | Internal tools vs customer-facing vs API products |
| `roadmap-design` | Quarterly planning, board presentation | Startup (now/next/later) vs enterprise (quarters, commitments) |
| `stakeholder-management` | Cross-team initiatives, executive alignment | Engineering vs Design vs Sales vs Execs vs Customers |
| `metric-definition` | North Star, OKRs, feature success metrics | Engagement products vs revenue products vs platform products |
| `user-story-mapping` | New product, major feature, redesign | Greenfield vs legacy migration vs platform modernization |
| `launch-planning` | Any product launch | Dark launch → soft launch → GA → enterprise launch tiers |
| `competitive-analysis` | New market, pricing change, competitive threat | Feature matrix, SWOT, win/loss analysis, battle cards |
| `product-led-growth` | Self-serve conversion, viral loops, activation | PLG + sales hybrid, product qualified accounts |

### UX Researcher
| Sub-Skill | When to Use | Method Variations |
|-----------|-------------|--------------------|
| `generative-research` | Discovery, problem exploration | User interviews, field studies, diary studies |
| `evaluative-research` | Testing designs, validating solutions | Usability testing, A/B testing, heuristic evaluation |
| `persona-creation` | Product strategy, feature prioritization | Data-driven (behavioral) vs assumption-based (when to use each) |
| `journey-mapping` | Onboarding, complex workflows, multi-touchpoint | Current-state vs future-state, service blueprint |
| `survey-design` | Quantitative validation, satisfaction measurement | SUS, NPS, CSAT, custom — when each, proper scales |
| `research-operations` | Scaling research across org | Recruitment, panels, consent, incentives, repository |
| `competitive-benchmarking` | Market positioning, UX quality assessment | Heuristic evaluation vs usability benchmark vs SUS comparison |

### Idea-to-Spec
| Sub-Skill | When to Use | Phase |
|-----------|-------------|-------|
| `problem-validation` | Before building anything | Problem hypothesis → user need evidence → market validation |
| `solution-design` | After problem validation | Ideation → concept testing → prototype → spec |
| `scope-negotiation` | Feature creep, stakeholder demands | MVP slicing, must-have vs nice-to-have, trade-off communication |
| `spec-to-issues` | Handoff to engineering | User story decomposition, acceptance criteria, technical spikes |
| `assumption-testing` | Riskiest assumptions first | Assumption map → experiment design → learn → pivot/persevere |

---

## Domain 03: Design

### UI/UX Designer
| Sub-Skill | When to Use | Platform Variations |
|-----------|-------------|---------------------|
| `design-system` | Building or scaling component library | Web (React/Vue) vs Mobile (iOS/Android) vs Multi-platform |
| `interaction-design` | Complex workflows, novel interactions | Desktop vs Mobile vs Tablet vs Wearable vs TV |
| `visual-design` | Brand expression in product | Consumer (emotional) vs Enterprise (functional) vs Developer tools |
| `responsive-design` | Multi-device, multi-breakpoint | Mobile-first vs desktop-first vs adaptive vs responsive |
| `motion-design` | Micro-interactions, transitions, delight | Subtle (enterprise) vs expressive (consumer brand) |
| `form-design` | Signup, checkout, settings, data entry | Simple (2-3 fields) vs complex (multi-step, conditional logic) |
| `empty-state-design` | First-run, cleared, no results, error | Each state: what to show, what action to prompt |
| `dark-mode-design` | Implementing dark mode | Elevation-based (Material) vs semantic color tokens |

### Accessibility Auditor
| Sub-Skill | When to Use | Standard Variations |
|-----------|-------------|---------------------|
| `wcag-audit` | Compliance verification | WCAG 2.2 A / AA / AAA per component type |
| `screen-reader-testing` | VoiceOver, NVDA, JAWS, TalkBack | Web vs iOS vs Android screen reader differences |
| `keyboard-accessibility` | All interactive components | Desktop web (Tab/Enter/Escape) vs Mobile (switch control) |
| `color-contrast` | Visual design review | WCAG ratios, APCA, dark mode, data visualization |
| `cognitive-accessibility` | Complex workflows, forms | Plain language, consistent patterns, error prevention |
| `accessibility-statement` | GDPR/ADA compliance | Template, conformance claims, contact info |
| `legal-compliance` | ADA Title III, Section 508, EN 301 549 | US vs EU vs Canada (AODA) legal requirements |

### Brand Guidelines
| Sub-Skill | When to Use | Scale |
|-----------|-------------|-------|
| `brand-architecture` | New brand, acquisition, rebrand | Monolithic vs endorsed vs house of brands |
| `visual-identity` | Logo, color, typography | Startup (lean) vs Enterprise (comprehensive) |
| `brand-voice` | Content strategy, marketing | B2B (professional) vs B2C (personality-driven) vs Developer (technical) |
| `brand-application` | Digital, print, merchandise | Each medium has specific requirements |
| `brand-governance` | Multi-team, multi-agency | Approval workflow, asset management, version control |

---

## Domain 04: Architecture

### System Architect
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `architecture-assessment` | New project, acquisition, modernization | Greenfield vs brownfield vs legacy migration |
| `c4-modeling` | Communicating architecture to different audiences | Context (execs) → Container (devs) → Component (team) → Code |
| `adr-writing` | Every significant technical decision | ADR template, storage, linking, superseding |
| `scalability-design` | Growth planning, performance issues | Vertical vs horizontal, caching, sharding, CQRS |
| `resilience-design` | Mission-critical, high-availability | Circuit breakers, bulkheads, retry, graceful degradation |
| `integration-architecture` | Multi-system, multi-vendor | API-led, event-driven, ESB, iPaaS |
| `data-architecture` | Data-heavy, analytics, compliance | Lake, warehouse, lakehouse, mesh, fabric |
| `security-architecture` | Compliance, threat modeling | Zero trust, defense in depth, least privilege |

### API Designer
| Sub-Skill | When to Use | Protocol |
|-----------|-------------|----------|
| `rest-design` | CRUD, resource-oriented APIs | REST maturity levels, HATEOAS practicality |
| `graphql-design` | Flexible clients, mobile, complex data | Schema design, N+1 prevention, security (depth/complexity limits) |
| `grpc-design` | Service-to-service, high-performance | Protobuf, streaming, error handling |
| `api-security` | Auth, rate limiting, threat protection | OAuth2, mTLS, API keys, rate limit algorithms |
| `api-versioning` | Evolution without breaking | URL, header, content negotiation, deprecation |
| `api-documentation` | Developer experience, SDK generation | OpenAPI, AsyncAPI, SDK generation pipeline |
| `api-testing` | Contract testing, integration | Pact, Postman collections, performance testing |

### Database Designer
| Sub-Skill | When to Use | Platform |
|-----------|-------------|----------|
| `schema-design` | New project, new feature | Relational (normalization), document (denormalization), graph |
| `query-optimization` | Slow queries, scaling issues | Index strategy, query plan analysis, materialized views |
| `migration-strategy` | Schema changes, zero-downtime | Expand-contract, online schema change, backfill patterns |
| `multi-tenancy` | SaaS, B2B | Database-per-tenant vs schema-per-tenant vs row-level |
| `backup-recovery` | DR planning, compliance | PITR, WAL archiving, RPO/RTO targets |
| `database-selection` | New project, scaling event | SQL vs NoSQL vs NewSQL vs search vs cache decision matrix |

---

## Domain 05: Development

### Backend Developer
| Sub-Skill | When to Use | Language/Framework |
|-----------|-------------|---------------------|
| `api-implementation` | Building REST/GraphQL/gRPC endpoints | FastAPI, Express, Go-chi, Spring Boot |
| `auth-implementation` | JWT, OAuth2, sessions, API keys | Supabase Auth, Clerk, Auth0, Keycloak, custom |
| `database-integration` | ORM, query optimization, migrations | SQLAlchemy 2.0, Prisma, GORM, jOOQ |
| `caching-strategy` | Performance optimization | Redis patterns, CDN, in-memory |
| `async-processing` | Background jobs, event handling | Celery, BullMQ, Sidekiq, River |
| `error-handling` | Resilience, observability | Circuit breakers, retry, graceful degradation |
| `logging-observability` | Debugging, monitoring | Structured logging, OpenTelemetry, correlation IDs |
| `api-testing` | Unit, integration, contract | pytest, Jest, Go testing, Pact |

### Frontend Developer
| Sub-Skill | When to Use | Framework |
|-----------|-------------|-----------|
| `framework-selection` | New project | Next.js vs Remix vs Vite SPA vs Astro |
| `state-management` | Complex state, multi-component | Context, Zustand, Jotai, TanStack Query, Redux |
| `performance-optimization` | CWV, bundle size, rendering | LCP, INP, CLS — per-metric optimization strategies |
| `accessibility-implementation` | WCAG compliance | Semantic HTML, ARIA, keyboard, focus management |
| `css-architecture` | Design system style implementation | Tailwind, CSS Modules, design tokens |
| `testing-strategy` | Quality gates | Component (RTL), E2E (Playwright), visual regression |
| `bundle-optimization` | Load performance | Dynamic imports, tree shaking, code splitting |
| `ssr-strategy` | SEO, performance | SSR vs SSG vs ISR vs CSR — when each |

### Mobile Developer
| Sub-Skill | When to Use | Platform |
|-----------|-------------|----------|
| `framework-selection` | New mobile project | Native vs React Native vs Flutter vs PWA |
| `ios-hig-compliance` | iOS app design | iOS HIG patterns, Dynamic Type, Safe Area, gestures |
| `material-design` | Android app design | Material 3, dynamic color, adaptive layouts |
| `offline-first` | Connectivity-challenged apps | SQLite/WatermelonDB, sync engine, conflict resolution |
| `mobile-performance` | Jank, startup time, memory | 60fps animations, cold start < 2s, memory profiling |
| `mobile-security` | Secure storage, network, code | Keychain/Keystore, cert pinning, obfuscation, root detection |
| `mobile-testing` | Quality assurance | Unit, widget, integration (Detox/Maestro), E2E |
| `push-notifications` | Engagement, re-engagement | FCM, APNs, notification strategy, deep linking |
| `app-store-optimization` | Discovery, conversion | ASO, screenshots, reviews, keyword optimization |
| `mobile-accessibility` | Inclusivity | VoiceOver, TalkBack, dynamic text, reduced motion |
| `mobile-ci-cd` | Deployment automation | Fastlane, EAS Build, CodePush, TestFlight, Play Console |

### Fullstack Developer
| Sub-Skill | When to Use | Stack |
|-----------|-------------|-------|
| `monorepo-fullstack` | Shared types, unified DX | Turborepo, Nx, shared packages |
| `bff-pattern` | Mobile + Web consuming same data | Backend-for-Frontend implementation |
| `tRPC-end-to-end-types` | TypeScript fullstack | End-to-end type safety from DB to UI |
| `nextjs-fullstack` | Next.js + database | Server Actions, RSC, API routes, middleware |
| `realtime-features` | Chat, collaboration, live updates | WebSocket, SSE, polling strategy comparison |
| `file-upload` | Media, documents, large files | Multipart, presigned URL, tus protocol, chunked |
| `deployment-strategy` | Fullstack deployment | Vercel vs Railway vs Fly.io vs AWS Amplify |

---

## Domain 06: Quality

### QA Engineer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `test-strategy` | New project, new feature area | Risk-based, test pyramid right-sizing, test quadrant |
| `api-testing` | REST/GraphQL/gRPC APIs | Contract (Pact), integration, schema, auth, error scenarios |
| `e2e-testing` | Critical user flows | Playwright patterns, test data, flaky prevention |
| `performance-testing` | Before launch, after changes | k6 scripts, scenarios (ramp, soak, spike, stress) |
| `mobile-testing` | Mobile apps | Device matrix, gestures, network simulation |
| `accessibility-testing` | WCAG compliance | Automated + manual + screen reader testing |
| `security-testing` | OWASP Top 10, SAST | Dependency scanning, secret detection, pen testing |
| `test-automation` | CI integration | Parallelization, flaky quarantine, test impact analysis |

### Code Reviewer
| Sub-Skill | When to Use | Focus |
|-----------|-------------|-------|
| `security-review` | Auth, data handling, input | OWASP Top 10 mapped to code patterns |
| `performance-review` | Hot paths, loops, queries | N+1, unbounded collections, sync I/O |
| `correctness-review` | Complex logic, edge cases | Race conditions, null safety, off-by-one |
| `maintainability-review` | New modules, refactors | Naming, coupling, cohesion, complexity |
| `language-specific-review` | Per-language patterns | Python, TypeScript, Go, Rust, Java |
| `pr-workflow` | Team process | Draft PRs, stacked PRs, size limits, review etiquette |

### Security Reviewer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `threat-modeling-review` | New features, architecture changes | STRIDE per component, attack trees |
| `auth-review` | Authentication, authorization code | JWT, OAuth2, sessions, RBAC, API keys |
| `data-protection-review` | PII, encryption, storage | At rest, in transit, key management, data minimization |
| `injection-review` | User input, queries, commands | SQL, NoSQL, command, LDAP, XPath injection |
| `dependency-review` | Package updates, supply chain | CVSS scoring, reachability, fix strategy |
| `infrastructure-review` | IaC, containers, cloud | Misconfigurations, open ports, public resources |
| `mobile-security-review` | Mobile apps | Secure storage, cert pinning, obfuscation |

---

## Domain 07: DevOps

### DevOps Engineer
| Sub-Skill | When to Use | Platform |
|-----------|-------------|----------|
| `iac-design` | Infrastructure provisioning | Terraform, Pulumi, CDK, Crossplane |
| `gitops-implementation` | K8s deployments | ArgoCD, Flux, sync policies, health checks |
| `secret-management` | Credentials, certificates | Vault, external-secrets, sealed-secrets |
| `disaster-recovery` | BCP, compliance | RPO/RTO design, backup strategy, failover automation |
| `service-mesh` | mTLS, traffic management | Istio, Linkerd, Cilium |
| `progressive-delivery` | Safe deployments | Canary, blue-green, feature flags |

### CI/CD Builder
| Sub-Skill | When to Use | Platform |
|-----------|-------------|----------|
| `pipeline-design` | Pipeline architecture | GitHub Actions, GitLab CI, Jenkins, CircleCI |
| `build-optimization` | Slow builds | Caching, parallelism, incremental builds |
| `deployment-strategy` | Safe releases | Rolling, blue-green, canary, feature-flagged |
| `quality-gates` | Pre-deploy verification | SonarQube, coverage, security, bundle, Lighthouse |
| `environment-management` | Dev/staging/prod | Ephemeral per PR, staging parity, promotion flow |
| `release-management` | Versioning, changelogs | Semantic release, conventional commits, CHANGELOG |

### Observability Engineer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `slo-design` | Service reliability | SLI definition, SLO targets, error budgets, burn rate alerts |
| `dashboard-design` | Monitoring, debugging | USE (infra), RED (services), golden signals |
| `alerting-strategy` | On-call, incident response | Alert philosophy, severity, fatigue prevention |
| `distributed-tracing` | Microservices debugging | OpenTelemetry, span design, sampling |
| `logging-strategy` | Debugging, compliance | Structured logging, PII redaction, retention |
| `metrics-collection` | Performance, capacity | Prometheus, cardinality management, recording rules |

---

## Domain 08: Security

### Security Engineer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `threat-modeling` | Architecture, new features | STRIDE, attack trees, MITRE ATT&CK |
| `sast-implementation` | Code security | Semgrep rules, custom detectors, CI gates |
| `secrets-management` | Credentials | Vault patterns, pre-commit hooks, rotation |
| `auth-security` | Authentication | MFA, password policy, OAuth2 threat mitigation |
| `network-security` | Infrastructure | Zero trust, mTLS, WAF, API gateway |
| `container-security` | Docker/K8s | Image scanning, non-root, read-only, seccomp |
| `dependency-security` | Supply chain | SBOM, vulnerability triage, automated patching |
| `security-champions` | Org security culture | Training, gamification, embedding in teams |

### Compliance Officer
| Sub-Skill | When to Use | Framework |
|-----------|-------------|-----------|
| `soc2-compliance` | Enterprise sales, trust | Type I → Type II roadmap, TSC mapping, evidence collection |
| `iso27001-compliance` | International, enterprise | ISMS, SoA, internal audit, certification audit |
| `pcidss-compliance` | Payment processing | SAQ type selection, ROC, quarterly ASV scans |
| `hipaa-compliance` | Healthcare data | BAA, technical safeguards, breach notification |
| `fedramp-compliance` | US government sales | ATO process, 3PAO assessment, continuous monitoring |
| `gdpr-compliance` | EU data, privacy | DPIA, DPO, DSAR, cross-border transfer, breach notification |
| `evidence-automation` | All frameworks | Automated collection, screen captures, audit trail |

### Incident Responder
| Sub-Skill | When to Use | Phase |
|-----------|-------------|-------|
| `incident-detection` | Monitoring, alerting | Detection rules, SIEM, anomaly detection |
| `incident-triage` | First response | Severity classification, war room activation |
| `containment-strategy` | Active incident | Isolation, access revocation, kill switch activation |
| `forensics` | Investigation | Evidence collection, chain of custody, timeline |
| `rca-methodology` | Post-incident | 5-Whys, Ishikawa, fault tree, contributing factors |
| `postmortem` | After recovery | Blameless, action items, tracking |
| `tabletop-exercises` | Preparedness | Scenario design, facilitation, after-action review |

---

## Domain 09: Data & AI

### Data Engineer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `data-architecture` | Data platform design | Medallion, mesh, lake vs warehouse vs lakehouse |
| `etl-pipeline` | Data ingestion, transformation | Batch, micro-batch, streaming, CDC |
| `schema-design-analytics` | Data modeling | Star, snowflake, data vault, SCD types |
| `data-quality` | Trust, compliance | Great Expectations, WAP, data contracts |
| `pipeline-reliability` | Production pipelines | Idempotency, checkpointing, DLQ, backfill |
| `stream-processing` | Real-time data | Kafka, windowing, watermarking, exactly-once |
| `data-governance` | Catalog, lineage, PII | DataHub, Amundsen, retention, right-to-erasure |

### Analytics Engineer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `dbt-modeling` | Transformation layer | Project structure, layers, incremental, snapshots, tests |
| `metric-definition` | Business metrics | Semantic layer, metric types, time dimensions |
| `bi-architecture` | Reporting, dashboards | Semantic layer vs direct query, caching, RLS |
| `experimentation` | A/B testing | Design, sample size, significance, SRM checks |
| `sql-optimization` | Query performance | CTEs vs subqueries, window functions, materialization |
| `data-visualization` | Dashboards, reports | Chart selection, dashboard design, storytelling |

### ML/AI Engineer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `ml-lifecycle` | End-to-end ML project | Problem framing → data → training → deploy → monitor |
| `model-selection` | Choosing approach | Classical vs deep learning vs foundation models vs heuristics |
| `data-preparation` | Feature engineering | Missing data, encoding, normalization, leakage prevention |
| `training-optimization` | Model training | Hyperparameter tuning, CV, overfitting, regularization |
| `mlops-pipeline` | ML infrastructure | Experiment tracking, registry, feature store, orchestration |
| `model-serving` | Deployment | Batch, real-time, streaming, edge, optimization (quantization) |
| `llm-patterns` | LLM applications | Prompt engineering, RAG, fine-tuning, agents |
| `model-evaluation` | Quality assessment | Classification, regression, ranking, LLM eval metrics |
| `model-monitoring` | Production ML | Data drift, concept drift, performance, fairness |
| `responsible-ai` | Ethics, safety | Bias detection, fairness, explainability, model cards, guardrails |

---

## Domain 10: Growth

### SEO Specialist
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `technical-seo` | Site architecture | Crawl budget, sitemaps, robots.txt, canonical, hreflang |
| `content-seo` | Content strategy | E-E-A-T, topic clusters, semantic search, gap analysis |
| `core-web-vitals-seo` | Performance + ranking | LCP/INP/CLS optimization specific to SEO impact |
| `schema-markup` | Rich results | JSON-LD, Article, Product, FAQ, HowTo, LocalBusiness |
| `international-seo` | Multi-region | hreflang, ccTLD vs subdirectory, localized keywords |
| `javascript-seo` | JS-heavy sites | SSR/SSG for SEO, dynamic rendering, hydration |
| `seo-monitoring` | Ongoing optimization | GSC API, rank tracking, algorithm update response |

### Growth Engineer
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `experimentation-platform` | A/B testing infrastructure | Randomization, SRM, significance, MDE |
| `growth-loops` | Sustainable growth | Viral, content, paid, sales — measurement + optimization |
| `activation-optimization` | User onboarding | AARRR, habit loops, time-to-value |
| `feature-flagging` | Controlled rollouts | LaunchDarkly patterns, gradual rollout, kill switches |
| `analytics-implementation` | Data collection | Event taxonomy, client/server-side, warehouse-native |

---

## Domain 11: Legal & Compliance

*(See industry-compliance-matrix for full industry-to-regulation mapping)*

### Legal Advisor
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `saas-contracts` | Customer agreements | MSA, SLA, DPA, indemnification, liability caps |
| `fundraising-legal` | Fundraising rounds | SAFE, convertible note, Series Seed/A, term sheets |
| `ip-protection` | IP strategy | Patent, trademark, copyright, trade secret |
| `open-source-legal` | OSS usage, contribution | License compatibility, CLA vs DCO, compliance |
| `employment-legal` | Hiring, equity | Contractor vs employee, IP assignment, equity (ISO/NSO) |
| `data-processing-agreements` | GDPR, vendor management | SCCs, DPA, sub-processor management |
| `terms-and-privacy` | Consumer-facing | ToS, privacy policy, cookie policy, AUP |

### GDPR & Privacy
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `data-mapping` | GDPR readiness | Data flow diagrams, asset inventory, RoPA |
| `dsar-implementation` | Data subject rights | Access, erasure, portability — 30-day workflow |
| `dpia-execution` | High-risk processing | When required, methodology, documentation |
| `cookie-compliance` | Web, mobile | Consent management, categorization, audit log |
| `cross-border-transfer` | International data flows | Adequacy, SCCs, BCRs, DPF, Schrems II compliance |
| `breach-notification` | Security incidents | 72-hour DPA notification, data subject communication |
| `privacy-by-design` | Product development | Data minimization, pseudonymization, privacy patterns |

### Regulatory Specialist
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `regulatory-landscape` | New market entry | Research, mapping, gap analysis per industry |
| `compliance-gap-assessment` | Audit preparation | Current state vs regulatory requirements |
| `regulatory-monitoring` | Ongoing compliance | Change tracking across jurisdictions |
| `cross-border-compliance` | Multi-jurisdiction | Managing 5+ regulatory regimes |
| `audit-readiness` | Regulatory audits | Evidence, walkthroughs, remediation |
| `regulatory-risk-calculation` | Risk management | Financial impact quantification |

---

## Domain 12: Operations

### Project Manager, Scrum Master, Technical Writer
*(Each has similar sub-skill depth — see respective SKILL.md files)*

---

## Domain 13: Specialized

### Monorepo Manager, Migration Architect, Performance Engineer, Chaos Engineer, Documentation Engineer
*(Each has deep sub-skill maps — see respective SKILL.md files)*

---

## How to Use Sub-Skills in Practice

1. **Agent loads parent SKILL.md** → Gets overview, workflow, decision trees
2. **Agent identifies specific need** (e.g., "I need to secure this mobile app") → Loads `mobile-security` sub-skill reference
3. **Agent executes** → Follows sub-skill-specific instructions, tools, checklists
4. **Sub-skill references stay in references/** → Not loaded unless needed, saving tokens

---

*This sub-skill map should be referenced from every parent SKILL.md. Each SKILL.md should include a "## Sub-Skills" section linking to relevant sub-skill references.*
