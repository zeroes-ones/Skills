# Project Bootstrap Guide

> **Author:** Sandeep Kumar Penchala  
> **Purpose:** Master navigation map — which skills to invoke at every phase of building a product from scratch

---

## How to Use This Guide

When starting ANY new project, follow this phased approach. Each phase invokes specific skills in sequence. The agent loads only the skills needed for the current phase, saving tokens.

### Choosing Your Starting Tier

Match skills to your project's maturity. Start lean, expand as you grow:

| Tier | Skills | When to Use |
|------|--------|-------------|
| **Solo** (`skills-init --solo`) | 8 essentials | Weekend project, prototype, personal site |
| **Grow** (`skills-init --grow`) | 18 skills | Side project with users, open source, early startup |
| **Full** (`skills-init`) | 101 skills | Team project, funded startup, enterprise |

This bootstrap guide covers the full 101-skill lifecycle. If you started with `--solo`, upgrade to `--grow` around Phase 3 and `--full` around Phase 6. Skills you haven't activated yet won't be loadable by agents.

> **Chain-aware navigation:** Every skill's YAML `chain:` block declares exact upstream/downstream dependencies. Use [`COORDINATION-MATRIX.md`](COORDINATION-MATRIX.md) to find the minimal viable sequence for your phase. The chains are symmetric — if `backend-developer` feeds into `code-reviewer`, then `code-reviewer` consumes from `backend-developer`.

---

## Phase 0: Strategic Foundation (Days 1-5)

**Goal:** Validate the idea before writing a single line of code.

### Step 0.1: Market & Business Validation
```
Invoke: ceo-strategist → business-strategist
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| Is this a business or a feature? | Problem hypothesis template | `ceo-strategist > Vision Crafting` |
| How big is the market? | TAM/SAM/SOM — bottom-up | `business-strategist > Market Sizing` |
| What's the business model? | Business Model Canvas | `business-strategist > Business Model Design` |
| Can we make money? | Unit economics: CAC < LTV/3 | `business-strategist > Unit Economics` |
| Who are competitors? | Porter's Five Forces + Blue Ocean | `ceo-strategist > Competitive Strategy` |

**Outputs:** Business Model Canvas, Market Sizing, Competitive Analysis  
**Gate:** Market > $100M TAM? Unit economics work at scale? → Proceed to 0.2 or kill idea

### Step 0.2: Technical Feasibility
```
Invoke: cto-advisor → system-architect
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| Can we build this? | Build vs Buy analysis | `cto-advisor > Build vs Buy` |
| What's the simplest architecture? | Monolith-first assessment | `system-architect > When Monolith Wins` |
| What stack? | Stack selection by archetype | `TECH-STACK-DECISIONS.md` |
| Team needed? | Roles × timeline | `cto-advisor > Hiring Timeline` |
| Cost to MVP? | Infrastructure + engineer cost | `cto-advisor > TCO Model` |

**Outputs:** Technical feasibility assessment, Stack decision, MVP cost estimate  
**Gate:** MVP buildable in < 4 weeks with 1-3 devs? → Proceed to Phase 1

---

## Phase 1: Product Discovery (Days 5-10)

**Goal:** Define WHAT to build and WHO it's for.

### Step 1.1: User Research
```
Invoke: ux-researcher
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| Who are the users? | Persona creation (data-driven) | `ux-researcher > Persona Creation` |
| What's the core problem? | Generative research | `ux-researcher > Generative Research` |
| What do users do today? | Journey mapping (current state) | `ux-researcher > Journey Mapping` |
| What would success look like? | Jobs-to-be-done framework | `ux-researcher > Persona Creation` |

**Outputs:** 2-3 personas, Current-state journey map, Problem validation evidence

### Step 1.2: Product Definition
```
Invoke: product-manager → idea-to-spec
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| What's the MVP scope? | User story mapping → walking skeleton | `product-manager > User Story Mapping` |
| What's the North Star? | Metric decomposition | `product-manager > Metric Definition` |
| What's NOT in MVP? | Anti-goals documentation | `idea-to-spec > Scoping` |
| How do we prioritize? | RICE/ICE scoring | `product-manager > Prioritization` |

**Outputs:** MVP scope (walking skeleton), North Star metric, Prioritized backlog  
**Gate:** MVP scope < 4 weeks? Clear pass/fail success criteria? → Proceed to Phase 2

### Step 1.3: PRD Creation
```
Invoke: idea-to-spec > Use prd-template.md asset
```

**Outputs:** PRD with: problem statement, user stories, acceptance criteria (Gherkin), success metrics, anti-goals, risks

---

## Phase 2: Design (Days 8-15)

**Goal:** Design the user experience before building.

### Step 2.1: UX Design
```
Invoke: ui-ux-designer
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| What's the information architecture? | Content hierarchy, navigation model | `ui-ux-designer > Interaction Design` |
| What's the design language? | Design tokens, color system, typography | `ui-ux-designer > Design Systems` |
| How does it work on mobile? | Responsive breakpoint strategy | `ui-ux-designer > Responsive Design` |

### Step 2.2: Accessibility Foundation
```
Invoke: accessibility-auditor
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| WCAG target level? | A (minimum), AA (standard), AAA (enhanced) | `accessibility-auditor > WCAG Audit` |
| Semantic structure? | Heading hierarchy, landmarks | `accessibility-auditor > Screen Reader Testing` |
| Color contrast? | All color pairs meet 4.5:1 minimum | `accessibility-auditor > Color Contrast` |

### Step 2.3: Brand Foundation
```
Invoke: brand-guidelines
```

**Outputs:** Brand identity (logo, color, typography), Design system foundation tokens

---

## Phase 3: Architecture (Days 10-15)

**Goal:** Design the technical foundation.

### Step 3.1: System Architecture
```
Invoke: system-architect
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| Architecture style? | Monolith → Modular → Microservices readiness | `system-architect > Architecture Styles` |
| How to communicate architecture? | C4 Model (Context + Container levels) | `system-architect > C4 Modeling` |
| Key decisions to document? | ADR for every significant choice | `system-architect > ADR Writing` |
| Identify the risks? | Risk matrix, failure modes | `system-architect > Resilience Design` |

**Outputs:** C4 Context + Container diagrams, 3-5 ADRs, Risk matrix

### Step 3.2: API Design
```
Invoke: api-designer
```

| API Type Decision | When to Choose |
|------------------|----------------|
| REST | CRUD, resource-oriented, public APIs |
| GraphQL | Flexible clients, mobile, complex nested data |
| gRPC | Internal service-to-service, high performance |
| JSON-RPC | Simple command-style, internal tools |

**Outputs:** OpenAPI 3.1 spec, API versioning strategy, Error handling standard

### Step 3.3: Database Design
```
Invoke: database-designer
```

| Decision Point | Framework | Skill Section |
|---------------|-----------|---------------|
| Database type? | PostgreSQL for 95% of MVPs | `database-designer > Database Selection` |
| Schema design? | Normalize to 3NF, denormalize deliberately | `database-designer > Schema Design` |
| Index strategy? | Index every foreign key + query patterns | `database-designer > Index Strategy` |

**Outputs:** ERD, Migration strategy, Index plan

---

## Phase 4: Development (Days 10-30)

**Goal:** Build the MVP.

### Step 4.1: Backend
```
Invoke: backend-developer
```

| Implementation | Stack Considerations |
|---------------|---------------------|
| API implementation | FastAPI (Python) / Express (Node) / Echo (Go) |
| Auth | JWT access+refresh, OAuth2 if social login |
| Database integration | ORM with migration support |
| Error handling | Circuit breakers, structured error responses |

### Step 4.2: Frontend
```
Invoke: frontend-developer
```
*Or for mobile-first products:* `mobile-developer`

| Implementation | Stack Considerations |
|---------------|---------------------|
| Framework | Next.js (SSR needed) / Vite (SPA) / Astro (content) |
| State management | TanStack Query (server) + Zustand (client) |
| CSS | Tailwind utility-first + design tokens |
| Forms | React Hook Form + Zod validation |

### Step 4.3: Mobile (if applicable)
```
Invoke: mobile-developer
```

| Decision | Framework |
|----------|-----------|
| Cross-platform? | React Native (web team) / Flutter (custom UI) |
| Native? | Swift + Kotlin (GPU, AR, hardware-heavy) |

### Step 4.4: Fullstack Integration
```
Invoke: fullstack-developer
```

**Outputs:** Working MVP, API + Frontend + Database integrated

---

## Phase 5: Quality Assurance (Days 20-35)

**Goal:** Verify the product works, is secure, and performs.

### Step 5.1: Code Review
```
Invoke: code-reviewer
```
Review all code against: security > correctness > performance > maintainability dimensions.

### Step 5.2: Testing
```
Invoke: qa-engineer
```

| Test Type | Tool | When |
|-----------|------|------|
| Unit tests | Jest, pytest, Go testing | Every commit |
| Integration tests | Supertest, pytest | PR checks |
| E2E tests | Playwright, Detox (mobile) | Pre-merge |
| Performance | k6, Lighthouse | Before launch |

### Step 5.3: Security Review
```
Invoke: security-reviewer → security-engineer
```

| Check | Tool | Gate |
|-------|------|------|
| SAST | Semgrep, CodeQL | 0 Critical/High in CI |
| Dependencies | npm audit, pip audit | 0 known Critical vulns |
| Secrets | GitGuardian, truffleHog | 0 detected in codebase |
| Infrastructure | Checkov, tfsec | 0 failed policies |

---

## Phase 6: DevOps & Deployment (Days 25-35)

**Goal:** Deploy, monitor, and operate.

### Step 6.1: CI/CD Pipeline
```
Invoke: ci-cd-builder
```

| Pipeline Stage | What Runs |
|---------------|-----------|
| Build | Compile, type-check, lint |
| Test | Unit → Integration → E2E |
| Security | SAST → Dependency → Secret scan |
| Deploy | Preview (per PR) → Staging → Production |

### Step 6.2: Infrastructure
```
Invoke: devops-engineer → docker-kubernetes → cloud-architect
```

| Scale | Infrastructure Choice |
|-------|----------------------|
| MVP (< 1K users) | Railway / Render / Vercel — single deploy |
| Growth (1K-100K) | ECS / Cloud Run — managed containers |
| Scale (100K+) | EKS / GKE — full K8s |

### Step 6.3: Observability
```
Invoke: observability-engineer
```

- **Logging:** Structured JSON, correlation IDs, PII redacted
- **Metrics:** RED (Rate, Errors, Duration) per service
- **Alerting:** Page on symptoms (p95 > threshold), not causes
- **SLOs:** 99.9% availability, p95 < 500ms

---

## Phase 7: Launch (Days 30-35)

### Step 7.1: Launch Planning
```
Invoke: product-manager > Launch Planning section
```

**Launch Checklist:**
- [ ] Performance tested at 2x expected load
- [ ] Security review passed
- [ ] GDPR/privacy compliance verified (`gdpr-privacy`)
- [ ] Accessibility baseline met (`accessibility-auditor`)
- [ ] Monitoring dashboards ready (`observability-engineer`)
- [ ] Incident response plan ready (`incident-responder`)
- [ ] Rollback plan tested (`ci-cd-builder`)
- [ ] Terms of Service + Privacy Policy published (`legal-advisor`)
- [ ] Customer support ready
- [ ] Analytics tracking verified (`analytics-engineer`)

### Step 7.2: Launch Execution
```
Invoke: ci-cd-builder > Deployment Strategy section
```
- Canary: 5% traffic → monitor 10 min → 25% → 50% → 100%
- Auto-rollback if: error rate > 0.1% OR p95 latency +20%

---

## Phase 8: Growth & Iteration (Ongoing)

### Step 8.1: Post-Launch Analysis
```
Invoke: analytics-engineer → product-manager
```
- Compare actual metrics vs launch success criteria
- Identify top 3 friction points from analytics

### Step 8.2: Growth Engineering
```
Invoke: growth-engineer → seo-specialist
```

| Growth Loop | Skill |
|-------------|-------|
| SEO optimization | `seo-specialist` |
| Content marketing | `content-strategist` |
| A/B testing | `growth-engineer` |
| Viral/referral loops | `growth-engineer > Growth Loops` |

### Step 8.3: Continuous Improvement
```
Monthly cycle: analytics-engineer → product-manager → code-reviewer → qa-engineer
```
- Review metrics → Prioritize improvements → Implement → Verify → Repeat

---

## Phase 9: Scaling (When Needed)

Scale ONLY when metrics demand it, not before:

| Trigger Metric | Action | Skill |
|---------------|--------|-------|
| DB CPU > 70% sustained | Add read replicas | `database-designer` |
| API p95 > 200ms | Profile → Cache → Optimize | `performance-engineer` |
| Deployment risk high | Feature flags, canary deploys | `ci-cd-builder` |
| Team > 15 engineers | Extract bounded context | `system-architect` |
| Users > 100K | Multi-region deployment | `cloud-architect` |
| Security incident | IR process | `incident-responder` |
| Compliance audit | Framework evidence | `compliance-officer` |

---

## Phase 10: Specialized Needs (As Required)

| Need | Skill |
|------|-------|
| Migrating legacy system | `migration-architect` |
| Monorepo setup | `monorepo-manager` |
| Performance degradation | `performance-engineer` |
| Resilience testing | `chaos-engineer` |
| Documentation overhaul | `documentation-engineer` / `technical-writer` |
| Legal/compliance issue | `legal-advisor` / `gdpr-privacy` / `regulatory-specialist` |
| ML/AI feature | `ml-ai-engineer` |
| Enterprise sales prep | `compliance-officer` (SOC 2) + `legal-advisor` (MSA) |

---

## Industry-Specific Variations

### FinTech Startup
Add these phases:
- **Phase 0.3:** Regulatory assessment → `regulatory-specialist` (PCI DSS, SOX, AML/KYC)
- **Phase 3.4:** Security architecture → `security-engineer` (encryption, audit trails)
- **Phase 6.4:** Compliance evidence → `compliance-officer` (PCI DSS SAQ)
- **Phase 7.3:** Regulatory filing → check `industry-compliance-matrix.md`

### HealthTech Startup
Add these phases:
- **Phase 0.3:** HIPAA assessment → `regulatory-specialist` (HIPAA, FDA SaMD)
- **Phase 3.4:** BAA-ready architecture → `security-engineer` (encryption, access controls)
- **Phase 6.4:** HIPAA compliance → `compliance-officer` (technical safeguards)
- **Phase 7.3:** FDA submission prep (if SaMD) → `regulatory-specialist`

### AI/ML Startup
Add these phases:
- **Phase 3.4:** ML architecture → `ml-ai-engineer`
- **Phase 3.5:** Data pipeline → `data-engineer`
- **Phase 5.4:** Model evaluation → `ml-ai-engineer > Model Evaluation`
- **Phase 6.4:** MLOps pipeline → `ml-ai-engineer > MLOps Pipeline`

### Enterprise SaaS
Add these phases:
- **Phase 0.3:** Enterprise readiness → `cto-advisor` (SSO, RBAC, audit logs)
- **Phase 3.4:** Multi-tenancy → `database-designer > Multi-Tenancy`
- **Phase 6.4:** SOC 2 preparation → `compliance-officer > SOC 2 Compliance`

---

## Token-Efficient Workflow

To minimize token consumption when bootstrapping a project:

1. **Load this guide first** — it tells you which skills to invoke at each phase
2. **Invoke skills one at a time** — don't load all SKILL.md files into context
3. **Use decision trees** — each skill has them in SKILL.md, avoid exploration loops
4. **Load references on demand** — only when the specific sub-skill is needed
5. **Run scripts, don't read them** — pass `--help`, pipe output, check exit codes

**Expected token savings:** 40-60% vs loading all skills upfront.

---

*This guide should be the first thing loaded when starting any new project. It maps the entire lifecycle.*
