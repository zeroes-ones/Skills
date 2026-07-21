# Cross-Skill Coordination Matrix

When starting any project, different skills must coordinate. This matrix maps every skill to its dependencies and communication requirements — derived from PROJECT-BOOTSTRAP.md lifecycle phases.

## Coordination by Project Phase

### Phase 1: Ideation & Validation (Week 1-2)
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| CEO Strategist | CTO Advisor, Business Strategist | Fundraising decision, pivot signal |
| Product Strategist | CEO Strategist, UX Researcher | PMF signal, GTM model choice |
| Business Strategist | CEO, Product, Legal Advisor | Market sizing, pricing model |
| UX Researcher | Product Strategist, UI Designer | User interview findings, JTBD |

### Phase 2: Design & Architecture (Week 2-4)
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| System Architect | CTO, Backend Dev, Database Designer | Architecture decision (ADR), scalability model |
| Database Designer | System Architect, Backend Dev, DevOps | Schema change, sharding consideration |
| API Designer | Frontend Dev, Backend Dev, Security | Breaking API change, versioning decision |
| UI/UX Designer | UX Researcher, Frontend Dev, Accessibility | Design system change, component spec |
| Security Reviewer | System Architect, API Designer, All Devs | Threat found, auth architecture change |

### Phase 3: Development (Week 4-12)
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| Frontend Dev | Backend Dev, API Designer, UI Designer | API contract change, component dependency |
| Backend Dev | Frontend Dev, Database Designer, DevOps | Schema migration, API change, performance issue |
| Mobile Dev | API Designer, UI Designer, Backend Dev | Platform-specific limitation, API gap |
| Fullstack Dev | All of above + DevOps | Architecture change, deployment issue |
| Technical Writer | All Devs, Product Manager | API change, feature complete |
| Code Reviewer | All Devs, Security Reviewer | Critical finding, architectural concern |

### Phase 4: Quality & Security (Overlapping with Dev)
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| QA Engineer | All Devs, Product Manager, DevOps | Blocker bug, test environment issue |
| Security Reviewer | All Devs, DevOps, Compliance | Critical vulnerability, compliance gap |
| Performance Engineer | Backend Dev, Frontend Dev, DevOps | Performance regression, bottleneck found |
| Accessibility Auditor | Frontend Dev, UI Designer | WCAG violation, remediation needed |
| Compliance Officer | Security, Legal, DevOps | Audit finding, control gap |

### Phase 5: DevOps & Infrastructure
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| DevOps Engineer | All Devs, Cloud Architect, Security | Pipeline failure, infra change |
| Cloud Architect | DevOps, System Architect, Finance | Cost spike, architecture mismatch |
| CI/CD Builder | All Devs, DevOps, QA | Pipeline redesign, deployment strategy |
| Docker/K8s | DevOps, Cloud Architect, All Devs | Cluster issue, scaling event |
| Observability Engineer | DevOps, All Devs, Incident Responder | Alert fired, SLO breach |
| Incident Responder | DevOps, Security, CEO, Legal | SEV1 incident, data breach |
| Chaos Engineer | DevOps, System Architect, Incident Responder | Experiment found weakness |

### Phase 6: Launch & Growth
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| SEO Specialist | Content Strategist, Frontend Dev, Growth | Traffic drop, algorithm change |
| Content Strategist | SEO, Product, Technical Writer | Content gap, editorial calendar change |
| Growth Engineer | Product, Frontend Dev, Data Engineer | Experiment result, PQL scoring change |
| Data Engineer | Analytics, ML Engineer, Backend Dev | Pipeline failure, schema change |
| Analytics Engineer | Data Engineer, Product, Growth | Metric anomaly, dashboard request |
| ML/AI Engineer | Data Engineer, Backend Dev, Product | Model drift, new model deployment |

### Phase 7: Legal & Compliance (Continuous)
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| Legal Advisor | CEO, Product, All Devs, Operations | Contract change, regulatory update |
| GDPR Privacy | Legal, Security, All Devs, Marketing | Data breach, DPIA trigger, DSAR received |
| Regulatory Specialist | Legal, CEO, Compliance, Product | New regulation, industry standard change |
| Security Engineer | All Devs, DevOps, Compliance | Vulnerability found, threat model change |

### Phase 8: Operations & Scale
| Skill | Must Coordinate With | Communication Trigger |
|-------|---------------------|----------------------|
| Project Manager | Product, All Devs, Design, DevOps, Stakeholders | Sprint at risk, dependency blocker, scope change |
| Scrum Master | Project Manager, All Devs, Product | Retro action incomplete, team velocity change |
| Monorepo Manager | All Devs, DevOps, CI/CD | Build time increase, dependency conflict |
| Migration Architect | System Architect, DevOps, All Devs | Migration milestone, data integrity issue |
| Documentation Engineer | Technical Writer, All Devs, Product | Docs outdated, onboarding friction |

## Escalation Paths

### Technical Escalation
```
Developer → Tech Lead → Engineering Manager → CTO → CEO
Security finding → Security Engineer → CTO → CEO + Legal
Performance issue → Performance Engineer → System Architect → CTO
```

### Product Escalation
```
Feature request → Product Manager → Product Strategist → CEO
Pivot decision → Product Strategist → CEO + Board
Pricing change → Product Strategist + Business Strategist → CEO
```

### Risk Escalation
```
Bug → QA Engineer → Project Manager → Product Manager
SEV incident → Incident Responder → CTO + CEO + Legal
Compliance gap → Compliance Officer → Legal Advisor → CEO
Data breach → GDPR Privacy + Security → Legal → CEO → DPA (72hr)
```

## Token-Efficient Coordination

When an agent invokes a skill, it should:
1. Check the coordination table for that skill
2. If work affects another skill's domain, notify or hand off
3. Use this matrix to decide when cross-skill collaboration is needed — not every task needs coordination

**Anti-pattern:** Coordinating "just in case." Coordinate only when there's a real dependency or shared resource.
