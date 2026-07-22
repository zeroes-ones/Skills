# Cross-Skill Coordination Matrix

> **Generated from actual YAML `chain:` data across 103 skills, 25 domains.**
> **Last updated:** 2026-07-22

Every skill declares its `consumes_from` (upstream dependencies) and `feeds_into` (downstream consumers).
This matrix organizes skills by project phase to help you navigate the full lifecycle.

## How Chains Work

```yaml
# Example: backend-developer SKILL.md frontmatter
chain:
  consumes_from: [api-designer, database-designer, system-architect]
  feeds_into: [frontend-developer, fullstack-developer, code-reviewer, qa-engineer, devops-engineer]
```

If skill A `feeds_into` skill B, then skill B `consumes_from` skill A. All 1,032 chain edges are symmetric.

## Phase 1: Ideation & Validation

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Business Strategist** | — | `bizdev-manager`, `ceo-strategist`, `marketing-manager`, `product-strategist` | Pivot signal, fundraising decision, market shift |
| **Ceo Strategist** | `accountant`, `bizdev-manager`, `board-manager`, `business-strategist` | `board-manager`, `fp-and-a-analyst`, `hr-manager`, `investor-relations` | Pivot signal, fundraising decision, market shift |
| **Cto Advisor** | `director-engineering`, `engineering-manager`, `security-engineer`, `system-architect` | `ceo-strategist`, `director-engineering`, `system-architect`, `vp-engineering` | Pivot signal, fundraising decision, market shift |
| **Product Strategist** | `business-strategist`, `data-scientist`, `ux-researcher` | `brand-guidelines`, `ceo-strategist`, `fp-and-a-analyst`, `marketing-manager` | Pivot signal, fundraising decision, market shift |
| **Idea To Spec** | `product-manager`, `system-architect`, `ui-ux-designer`, `ux-researcher` | `api-designer`, `backend-developer`, `database-designer`, `frontend-developer` | PRD change, discovery finding, user research insight |
| **Product Manager** | `account-manager`, `ai-safety-engineer`, `ai-safety-health-reviewer`, `analytics-engineer` | `content-strategist`, `customer-success-manager`, `customer-support-engineer`, `director-engineering` | PRD change, discovery finding, user research insight |
| **Ux Researcher** | `product-manager` | `frontend-developer`, `idea-to-spec`, `patient-experience-researcher`, `patient-health-educator` | PRD change, discovery finding, user research insight |

## Phase 2: Design & Architecture

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Ui Ux Designer** | `brand-guidelines`, `product-manager`, `ux-researcher` | `accessibility-auditor`, `frontend-developer`, `idea-to-spec`, `medical-illustrator` | Design system change, WCAG violation, brand decision |
| **Accessibility Auditor** | `accessibility-testing`, `frontend-developer`, `ui-ux-designer` | `accessibility-testing`, `frontend-developer`, `legal-advisor`, `qa-engineer` | Design system change, WCAG violation, brand decision |
| **Brand Guidelines** | `marketing-manager`, `medical-illustrator`, `product-strategist` | `frontend-developer`, `product-marketing-manager`, `ui-ux-designer`, `ux-writer` | Design system change, WCAG violation, brand decision |
| **System Architect** | `cto-advisor`, `product-manager`, `security-engineer`, `staff-engineer` | `algorithmic-trader`, `api-designer`, `backend-developer`, `cloud-architect` | ADR filed, schema migration, API contract change |
| **Api Designer** | `backend-developer`, `database-designer`, `idea-to-spec`, `system-architect` | `backend-developer`, `database-designer`, `documentation-engineer`, `frontend-developer` | ADR filed, schema migration, API contract change |
| **Database Designer** | `api-designer`, `backend-developer`, `idea-to-spec`, `system-architect` | `api-designer`, `backend-developer`, `data-engineer`, `database-reliability-engineer` | ADR filed, schema migration, API contract change |
| **Networking Engineer** | `system-architect`, `cloud-architect`, `security-engineer` | `devops-engineer`, `cloud-architect`, `site-reliability-engineer`, `docker-kubernetes` | ADR filed, schema migration, API contract change |
| **Ux Writer** | `brand-guidelines`, `medical-illustrator`, `patient-health-educator`, `product-manager` | `content-strategist`, `frontend-developer`, `localization-engineer`, `medical-illustrator` | Brand refresh, product launch, content redesign |
| **Product Marketing Manager** | `marketing-manager`, `product-manager`, `brand-guidelines` | `marketing-manager`, `sales-engineer`, `ux-writer` | Brand refresh, product launch, content redesign |

## Phase 3: Development

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Backend Developer** | `algorithmic-trader`, `api-designer`, `code-reviewer`, `database-designer` | `algorithmic-trader`, `api-designer`, `ci-cd-builder`, `clinical-informatics-specialist` | API contract change, breaking change, platform limitation |
| **Frontend Developer** | `accessibility-auditor`, `accessibility-testing`, `algorithmic-trader`, `api-designer` | `accessibility-auditor`, `code-reviewer`, `devrel-advocate`, `fullstack-developer` | API contract change, breaking change, platform limitation |
| **Fullstack Developer** | `backend-developer`, `frontend-developer`, `api-designer`, `database-designer` | `devops-engineer`, `qa-engineer`, `security-reviewer` | API contract change, breaking change, platform limitation |
| **Mobile Developer** | `accessibility-testing`, `api-designer`, `backend-developer`, `localization-engineer` | `localization-engineer`, `qa-engineer`, `security-reviewer`, `translation-manager` | API contract change, breaking change, platform limitation |
| **Localization Engineer** | `frontend-developer`, `mobile-developer`, `translation-manager`, `ux-writer` | `frontend-developer`, `mobile-developer`, `qa-engineer`, `translation-manager` | API contract change, breaking change, platform limitation |
| **Translation Manager** | `localization-engineer`, `frontend-developer`, `mobile-developer` | `localization-engineer`, `qa-engineer`, `ci-cd-builder` | API contract change, breaking change, platform limitation |
| **Technical Writer** | `api-designer`, `backend-developer`, `documentation-engineer`, `product-manager` | `devrel-advocate`, `documentation-engineer`, `ux-writer` | Scope change, sprint at risk, dependency blocker |
| **Documentation Engineer** | `api-designer`, `devrel-advocate`, `hardware-architect`, `technical-writer` | `backend-developer`, `devrel-advocate`, `technical-writer` | Build time increase, migration milestone, performance regression |

## Phase 4: Quality & Security

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Code Reviewer** | `backend-developer`, `frontend-developer`, `qa-engineer`, `security-reviewer` | `backend-developer`, `frontend-developer`, `qa-engineer` | Critical bug, security finding, accessibility regression |
| **Qa Engineer** | `accessibility-auditor`, `accessibility-testing`, `api-designer`, `backend-developer` | `accessibility-testing`, `ci-cd-builder`, `code-reviewer`, `devops-engineer` | Critical bug, security finding, accessibility regression |
| **Security Reviewer** | `backend-developer`, `devops-engineer`, `firmware-developer`, `fullstack-developer` | `backend-developer`, `code-reviewer`, `incident-responder`, `qa-engineer` | Critical bug, security finding, accessibility regression |
| **Accessibility Testing** | `accessibility-auditor`, `qa-engineer`, `ci-cd-builder` | `accessibility-auditor`, `frontend-developer`, `mobile-developer`, `qa-engineer` | Critical bug, security finding, accessibility regression |
| **Security Engineer** | `cloud-architect`, `compliance-officer`, `devops-engineer`, `gdpr-privacy` | `backend-developer`, `ci-cd-builder`, `cloud-architect`, `compliance-officer` | Vulnerability found, compliance gap, SEV incident |
| **Compliance Officer** | `gdpr-privacy`, `incident-responder`, `legal-advisor`, `regulatory-specialist` | `accountant`, `ai-safety-engineer`, `ai-safety-health-reviewer`, `clinical-informatics-specialist` | Vulnerability found, compliance gap, SEV incident |
| **Incident Responder** | `chaos-engineer`, `compliance-officer`, `crisis-response-manager`, `observability-engineer` | `compliance-officer`, `devops-engineer`, `security-engineer` | Vulnerability found, compliance gap, SEV incident |
| **Performance Engineer** | `backend-developer`, `database-designer`, `embedded-engineer`, `observability-engineer` | `backend-developer`, `devops-engineer`, `hardware-architect`, `site-reliability-engineer` | Build time increase, migration milestone, performance regression |
| **Chaos Engineer** | `devops-engineer`, `site-reliability-engineer`, `observability-engineer` | `site-reliability-engineer`, `incident-responder`, `devops-engineer` | Build time increase, migration milestone, performance regression |

## Phase 5: DevOps & Infrastructure

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Devops Engineer** | `backend-developer`, `chaos-engineer`, `ci-cd-builder`, `cloud-architect` | `chaos-engineer`, `ci-cd-builder`, `database-reliability-engineer`, `docker-kubernetes` | Pipeline failure, infra change, SLO breach, cost spike |
| **Ci Cd Builder** | `backend-developer`, `devops-engineer`, `monorepo-manager`, `qa-engineer` | `accessibility-testing`, `devops-engineer`, `docker-kubernetes`, `monorepo-manager` | Pipeline failure, infra change, SLO breach, cost spike |
| **Cloud Architect** | `finops-engineer`, `networking-engineer`, `security-engineer`, `system-architect` | `devops-engineer`, `docker-kubernetes`, `finops-engineer`, `networking-engineer` | Pipeline failure, infra change, SLO breach, cost spike |
| **Docker Kubernetes** | `backend-developer`, `ci-cd-builder`, `cloud-architect`, `devops-engineer` | `devops-engineer`, `observability-engineer`, `platform-engineer`, `site-reliability-engineer` | Pipeline failure, infra change, SLO breach, cost spike |
| **Observability Engineer** | `algorithmic-trader`, `backend-developer`, `devops-engineer`, `docker-kubernetes` | `algorithmic-trader`, `chaos-engineer`, `customer-support-engineer`, `devops-engineer` | Pipeline failure, infra change, SLO breach, cost spike |
| **Platform Engineer** | `cloud-architect`, `devops-engineer`, `docker-kubernetes`, `observability-engineer` | `backend-developer`, `devops-engineer`, `frontend-developer`, `observability-engineer` | Pipeline failure, infra change, SLO breach, cost spike |
| **Site Reliability Engineer** | `chaos-engineer`, `cloud-architect`, `database-reliability-engineer`, `devops-engineer` | `chaos-engineer`, `incident-responder`, `observability-engineer`, `release-manager` | Pipeline failure, infra change, SLO breach, cost spike |
| **Release Manager** | `ci-cd-builder`, `devops-engineer`, `project-manager`, `qa-engineer` | `devops-engineer`, `project-manager`, `site-reliability-engineer` | Pipeline failure, infra change, SLO breach, cost spike |
| **Finops Engineer** | `cloud-architect`, `devops-engineer`, `fp-and-a-analyst` | `cloud-architect`, `vp-engineering`, `fp-and-a-analyst` | Pipeline failure, infra change, SLO breach, cost spike |
| **Migration Architect** | `system-architect`, `database-designer`, `devops-engineer` | `devops-engineer`, `database-reliability-engineer`, `backend-developer` | Build time increase, migration milestone, performance regression |
| **Monorepo Manager** | `devops-engineer`, `ci-cd-builder`, `backend-developer` | `ci-cd-builder`, `backend-developer`, `frontend-developer` | Build time increase, migration milestone, performance regression |

## Phase 6: Data & AI Engineering

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Data Engineer** | `backend-developer`, `clinical-informatics-specialist`, `database-designer`, `database-reliability-engineer` | `analytics-engineer`, `business-intelligence-engineer`, `data-scientist`, `database-reliability-engineer` | Pipeline failure, schema change, model drift, metric anomaly |
| **Analytics Engineer** | `business-intelligence-engineer`, `data-engineer`, `data-scientist` | `business-intelligence-engineer`, `data-scientist`, `demand-generation`, `growth-engineer` | Pipeline failure, schema change, model drift, metric anomaly |
| **Data Scientist** | `analytics-engineer`, `business-intelligence-engineer`, `data-engineer`, `market-data-engineer` | `analytics-engineer`, `business-intelligence-engineer`, `growth-engineer`, `ml-ai-engineer` | Pipeline failure, schema change, model drift, metric anomaly |
| **Ml Ai Engineer** | `data-engineer`, `data-scientist`, `mlops-engineer`, `quantitative-analyst` | `data-scientist`, `llm-engineer`, `mlops-engineer`, `quantitative-analyst` | Pipeline failure, schema change, model drift, metric anomaly |
| **Database Reliability Engineer** | `data-engineer`, `database-designer`, `devops-engineer`, `migration-architect` | `data-engineer`, `devops-engineer`, `market-data-engineer`, `site-reliability-engineer` | Pipeline failure, schema change, model drift, metric anomaly |
| **Llm Engineer** | `ai-safety-engineer`, `backend-developer`, `ml-ai-engineer`, `mlops-engineer` | `ai-safety-engineer`, `ai-safety-health-reviewer`, `frontend-developer`, `mlops-engineer` | Model safety eval, RAG pipeline change, prompt drift |
| **Mlops Engineer** | `ml-ai-engineer`, `devops-engineer`, `data-engineer`, `llm-engineer` | `llm-engineer`, `ai-safety-engineer`, `ml-ai-engineer`, `observability-engineer` | Model safety eval, RAG pipeline change, prompt drift |
| **Ai Safety Engineer** | `ai-safety-health-reviewer`, `mlops-engineer`, `compliance-officer`, `llm-engineer` | `llm-engineer`, `medical-content-reviewer`, `product-manager` | Model safety eval, RAG pipeline change, prompt drift |
| **Ai Safety Health Reviewer** | `clinical-informatics-specialist`, `llm-engineer`, `medical-content-reviewer`, `compliance-officer` | `ai-safety-engineer`, `legal-advisor`, `content-policy-manager`, `product-manager` | Model safety eval, RAG pipeline change, prompt drift |
| **Business Intelligence Engineer** | `data-engineer`, `analytics-engineer`, `data-scientist` | `analytics-engineer`, `data-scientist`, `growth-engineer`, `revops-manager` | Model safety eval, RAG pipeline change, prompt drift |

## Phase 7: Growth, Sales & Marketing

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Seo Specialist** | `content-strategist`, `frontend-developer`, `analytics-engineer` | `content-strategist`, `growth-engineer`, `marketing-manager` | Traffic drop, experiment result, content gap |
| **Content Strategist** | `devrel-advocate`, `product-manager`, `seo-specialist`, `ux-writer` | `devrel-advocate`, `marketing-manager`, `seo-specialist` | Traffic drop, experiment result, content gap |
| **Growth Engineer** | `analytics-engineer`, `business-intelligence-engineer`, `customer-success-manager`, `data-scientist` | `demand-generation`, `marketing-manager`, `product-manager`, `revops-manager` | Traffic drop, experiment result, content gap |
| **Devrel Advocate** | `backend-developer`, `content-strategist`, `documentation-engineer`, `frontend-developer` | `content-strategist`, `documentation-engineer`, `growth-engineer`, `marketing-manager` | Traffic drop, experiment result, content gap |
| **Marketing Manager** | `bizdev-manager`, `business-strategist`, `content-strategist`, `demand-generation` | `bizdev-manager`, `brand-guidelines`, `demand-generation`, `product-marketing-manager` | Pipeline change, GTM launch, partnership opportunity |
| **Demand Generation** | `marketing-manager`, `analytics-engineer`, `growth-engineer` | `sales-engineer`, `marketing-manager`, `revops-manager` | Pipeline change, GTM launch, partnership opportunity |
| **Sales Engineer** | `backend-developer`, `bizdev-manager`, `demand-generation`, `marketing-manager` | `account-manager`, `customer-success-manager`, `product-manager`, `revops-manager` | Pipeline change, GTM launch, partnership opportunity |
| **Revops Manager** | `account-manager`, `analytics-engineer`, `business-intelligence-engineer`, `customer-success-manager` | `fp-and-a-analyst`, `growth-engineer`, `marketing-manager`, `sales-engineer` | Pipeline change, GTM launch, partnership opportunity |
| **Bizdev Manager** | `business-strategist`, `legal-advisor`, `marketing-manager`, `partnerships-manager` | `ceo-strategist`, `marketing-manager`, `partnerships-manager`, `product-manager` | Pipeline change, GTM launch, partnership opportunity |
| **Partnerships Manager** | `bizdev-manager`, `legal-advisor`, `product-manager` | `bizdev-manager`, `sales-engineer`, `marketing-manager` | Pipeline change, GTM launch, partnership opportunity |

## Phase 8: Legal, Compliance & Trust

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Legal Advisor** | `accessibility-auditor`, `ai-safety-health-reviewer`, `board-manager`, `privacy-engineer` | `accountant`, `bizdev-manager`, `board-manager`, `ceo-strategist` | Regulatory update, data breach, audit finding |
| **Gdpr Privacy** | `compliance-officer`, `legal-advisor`, `privacy-engineer` | `compliance-officer`, `privacy-engineer`, `security-engineer` | Regulatory update, data breach, audit finding |
| **Regulatory Specialist** | `compliance-officer`, `legal-advisor` | `ai-safety-health-reviewer`, `clinical-informatics-specialist`, `compliance-officer`, `content-policy-manager` | Regulatory update, data breach, audit finding |
| **Trust Safety Engineer** | `content-policy-manager`, `security-engineer`, `ml-ai-engineer` | `content-policy-manager`, `community-operations-manager`, `crisis-response-manager` | Abuse pattern, content policy violation, privacy incident |
| **Content Policy Manager** | `ai-safety-health-reviewer`, `community-operations-manager`, `compliance-officer`, `crisis-response-manager` | `community-operations-manager`, `crisis-response-manager`, `patient-health-educator`, `trust-safety-engineer` | Abuse pattern, content policy violation, privacy incident |
| **Privacy Engineer** | `gdpr-privacy`, `compliance-officer`, `security-engineer`, `backend-developer` | `security-engineer`, `backend-developer`, `gdpr-privacy`, `legal-advisor` | Abuse pattern, content policy violation, privacy incident |

## Phase 9: People & Operations

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Hr Manager** | `accountant`, `ceo-strategist`, `compliance-officer`, `legal-advisor` | `ceo-strategist`, `director-engineering`, `engineering-manager`, `fp-and-a-analyst` | Hiring need, compensation review, performance issue |
| **People Ops** | `hr-manager`, `recruiting`, `legal-advisor` | `hr-manager`, `recruiting`, `engineering-manager` | Hiring need, compensation review, performance issue |
| **Recruiting** | `director-engineering`, `engineering-manager`, `hr-manager`, `people-ops` | `director-engineering`, `engineering-manager`, `fp-and-a-analyst`, `hr-manager` | Hiring need, compensation review, performance issue |
| **Project Manager** | `engineering-manager`, `product-manager`, `release-manager`, `scrum-master` | `release-manager`, `scrum-master`, `technical-program-manager` | Scope change, sprint at risk, dependency blocker |
| **Scrum Master** | `engineering-manager`, `product-manager`, `project-manager` | `engineering-manager`, `project-manager`, `technical-program-manager` | Scope change, sprint at risk, dependency blocker |
| **Technical Program Manager** | `engineering-manager`, `project-manager`, `scrum-master`, `system-architect` | `director-engineering`, `project-manager`, `vp-engineering` | Scope change, sprint at risk, dependency blocker |
| **Customer Support Engineer** | `backend-developer`, `observability-engineer`, `product-manager` | `product-manager`, `qa-engineer`, `account-manager` | Scope change, sprint at risk, dependency blocker |
| **Customer Success Manager** | `sales-engineer`, `account-manager`, `product-manager` | `account-manager`, `product-manager`, `growth-engineer`, `revops-manager` | Health score change, churn risk, expansion opportunity |
| **Account Manager** | `sales-engineer`, `customer-success-manager`, `customer-support-engineer` | `customer-success-manager`, `revops-manager`, `product-manager` | Health score change, churn risk, expansion opportunity |

## Phase 10: Finance, Governance & Leadership

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Fp And A Analyst** | `accountant`, `business-intelligence-engineer`, `ceo-strategist`, `finops-engineer` | `accountant`, `board-manager`, `ceo-strategist`, `finops-engineer` | Budget variance, cash flow concern, audit finding |
| **Accountant** | `compliance-officer`, `fp-and-a-analyst`, `legal-advisor`, `treasury-manager` | `board-manager`, `ceo-strategist`, `fp-and-a-analyst`, `hr-manager` | Budget variance, cash flow concern, audit finding |
| **Treasury Manager** | `fp-and-a-analyst`, `accountant`, `ceo-strategist`, `legal-advisor` | `accountant`, `fp-and-a-analyst`, `ceo-strategist`, `board-manager` | Budget variance, cash flow concern, audit finding |
| **Algorithmic Trader** | `quantitative-analyst`, `market-data-engineer`, `system-architect`, `backend-developer` | `backend-developer`, `frontend-developer`, `observability-engineer` | Trading signal, market data gap, model validation |
| **Market Data Engineer** | `data-engineer`, `database-reliability-engineer`, `backend-developer` | `algorithmic-trader`, `quantitative-analyst`, `data-scientist` | Trading signal, market data gap, model validation |
| **Quantitative Analyst** | `market-data-engineer`, `data-scientist`, `ml-ai-engineer` | `algorithmic-trader`, `data-scientist`, `ml-ai-engineer` | Trading signal, market data gap, model validation |
| **Board Manager** | `accountant`, `ceo-strategist`, `fp-and-a-analyst`, `investor-relations` | `ceo-strategist`, `investor-relations`, `legal-advisor` | Board meeting prep, cap table change, investor update |
| **Investor Relations** | `accountant`, `board-manager`, `ceo-strategist`, `fp-and-a-analyst` | `board-manager`, `ceo-strategist`, `fp-and-a-analyst`, `treasury-manager` | Board meeting prep, cap table change, investor update |
| **Staff Engineer** | `engineering-manager`, `system-architect`, `backend-developer` | `system-architect`, `backend-developer`, `frontend-developer`, `code-reviewer` | Org change, architecture governance, strategic planning |
| **Engineering Manager** | `director-engineering`, `hr-manager`, `people-ops`, `product-manager` | `backend-developer`, `cto-advisor`, `director-engineering`, `project-manager` | Org change, architecture governance, strategic planning |
| **Director Engineering** | `cto-advisor`, `engineering-manager`, `hr-manager`, `product-manager` | `cto-advisor`, `engineering-manager`, `recruiting`, `vp-engineering` | Org change, architecture governance, strategic planning |
| **Vp Engineering** | `ceo-strategist`, `cto-advisor`, `director-engineering`, `finops-engineer` | `ceo-strategist`, `cto-advisor`, `director-engineering` | Org change, architecture governance, strategic planning |

## Phase 11: Health Clinical, Hardware & Creative

| Skill | Consumes From (Upstream) | Feeds Into (Downstream) | Communication Trigger |
|-------|--------------------------|------------------------|----------------------|
| **Clinical Informatics Specialist** | `backend-developer`, `compliance-officer`, `patient-experience-researcher`, `regulatory-specialist` | `ai-safety-health-reviewer`, `data-engineer`, `medical-content-reviewer`, `patient-experience-researcher` | FHIR spec change, clinical safety finding, AE report |
| **Medical Content Reviewer** | `ai-safety-engineer`, `clinical-informatics-specialist`, `compliance-officer`, `legal-advisor` | `ai-safety-health-reviewer`, `content-policy-manager`, `medical-illustrator`, `patient-health-educator` | FHIR spec change, clinical safety finding, AE report |
| **Patient Health Educator** | `clinical-informatics-specialist`, `content-policy-manager`, `data-scientist`, `medical-content-reviewer` | `community-operations-manager`, `medical-illustrator`, `ux-writer` | FHIR spec change, clinical safety finding, AE report |
| **Patient Experience Researcher** | `ux-researcher`, `community-operations-manager`, `clinical-informatics-specialist` | `product-manager`, `clinical-informatics-specialist`, `patient-health-educator` | FHIR spec change, clinical safety finding, AE report |
| **Community Operations Manager** | `content-policy-manager`, `crisis-response-manager`, `patient-health-educator`, `trust-safety-engineer` | `content-policy-manager`, `crisis-response-manager`, `patient-experience-researcher` | FHIR spec change, clinical safety finding, AE report |
| **Crisis Response Manager** | `community-operations-manager`, `content-policy-manager`, `legal-advisor`, `trust-safety-engineer` | `community-operations-manager`, `content-policy-manager`, `incident-responder` | FHIR spec change, clinical safety finding, AE report |
| **Embedded Engineer** | `backend-developer`, `firmware-developer`, `hardware-architect` | `firmware-developer`, `hardware-architect`, `performance-engineer`, `qa-engineer` | Hardware revision, firmware update, silicon selection |
| **Firmware Developer** | `embedded-engineer`, `hardware-architect`, `security-engineer` | `embedded-engineer`, `hardware-architect`, `qa-engineer`, `security-reviewer` | Hardware revision, firmware update, silicon selection |
| **Hardware Architect** | `system-architect`, `embedded-engineer`, `firmware-developer`, `performance-engineer` | `embedded-engineer`, `firmware-developer`, `documentation-engineer` | Hardware revision, firmware update, silicon selection |
| **Medical Illustrator** | `medical-content-reviewer`, `patient-health-educator`, `ui-ux-designer`, `ux-writer` | `brand-guidelines`, `patient-health-educator`, `ux-writer` | Brand refresh, product launch, content redesign |

## Escalation Paths

### Technical Escalation
```
Developer → Engineering Manager → Director Engineering → VP Engineering → CTO → CEO
Security finding → Security Engineer → CTO → CEO + Legal Advisor
Performance issue → Performance Engineer → System Architect → CTO
AI safety concern → AI Safety Engineer → LLM Engineer → CTO + Legal
Clinical data issue → Clinical Informatics → Medical Content Reviewer → Legal + CEO
```

### Product Escalation
```
Feature request → Product Manager → Product Strategist → CEO
Pivot decision → Product Strategist → CEO + Board Manager
Pricing change → Product Strategist + Business Strategist → CEO
Clinical feature → Clinical Informatics + Medical Content Reviewer → Product Manager
```

### Revenue Escalation
```
Pipeline gap → Sales Engineer → RevOps Manager → Marketing Manager → CEO
Churn signal → Customer Success Manager → Account Manager → Product Manager
Partnership opportunity → Partnerships Manager → BizDev Manager → CEO
```

### Risk Escalation
```
Bug → QA Engineer → Project Manager → Product Manager
SEV incident → Incident Responder → CTO + CEO + Legal Advisor
Compliance gap → Compliance Officer → Legal Advisor → CEO
Data breach → GDPR Privacy + Security Engineer → Legal Advisor → CEO → DPA (72hr)
Medical misinformation → Content Policy Manager → Trust & Safety Engineer → Legal + CEO
```

## Token-Efficient Coordination

When an agent invokes a skill:
1. Read the YAML `chain:` block in the skill's frontmatter for exact upstream/downstream dependencies
2. The `consumes_from` list tells you which skills must complete BEFORE this one
3. The `feeds_into` list tells you which skills need this skill's output NEXT
4. Check the Cross-Skill Coordination section within the SKILL.md for specific decision gates and artifacts
5. Only coordinate when there's a real dependency — chain data defines what those dependencies are

**Anti-pattern:** Invoking every skill in the chain just in case. Use chain data to determine the minimal viable sequence.

## Chain Statistics

- **103 skills** across **25 domains**
- **1032 total chain edges** (516 consumes_from + 516 feeds_into)
- **5.1 avg consumes_from per skill**
- **5.1 avg feeds_into per skill**
- **0 asymmetries** (all `A feeds_into B` ↔ `B consumes_from A` verified)
