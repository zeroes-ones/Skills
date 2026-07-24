# Sub-Skills — Healthcare Security Dependency Map

The healthcare security skill integrates with 20+ other skills across the
framework. This map shows what you need before, during, and after a healthcare
security engagement.

## Direct Dependencies (Consumes From)

| Skill | What Healthcare Security Needs from It |
|---|---|
| **security-engineer** | General security architecture patterns, threat modeling (STRIDE), encryption design |
| **hipaa-technical-implementation** | HIPAA Security Rule control details, addressable-vs-required guidance, implementation specs |
| **compliance-officer** | Regulatory interpretation, audit readiness, OCR investigation response |
| **cloud-architect** | Cloud service selection, shared responsibility model, multi-region PHI architecture |
| **networking-engineer** | VLAN design, NAC deployment, east-west traffic filtering, IPS placement |
| **system-architect** | System design, C4 modeling, ADR documentation, scalability patterns for PHI workloads |
| **database-designer** | Schema design for PHI, column-level encryption, audit table design, backup encryption |
| **api-designer** | FHIR API design, OAuth 2.0 + SMART scopes, rate limiting, gateway security |
| **legal-advisor** | BAA contract review, breach notification legal requirements, state law preemption analysis |
| **regulatory-specialist** | FDA device regulations, CMS interoperability rule, state health data privacy laws |

## Downstream Consumers (Feeds Into)

| Skill | What Healthcare Security Provides to It |
|---|---|
| **incident-responder** | Breach notification pipeline design, PHI scope assessment, clinical continuity procedures |
| **cloud-security-architect** | Healthcare-specific cloud controls, BAA integration with cloud services |
| **database-reliability-engineer** | PHI encryption at rest requirements, audit logging specifications, backup encryption |
| **security-engineer** | Healthcare-specific threat models, IoMT attack surface analysis, clinical network patterns |
| **compliance-officer** | HITRUST CSF control evidence, audit trail completeness, security program maturity metrics |
| **devops-engineer** | CI/CD pipeline PHI scanning, infrastructure-as-code encryption enforcement, container security for PHI |
| **networking-engineer** | Clinical VLAN requirements, IoMT isolation rules, medical device traffic patterns |
| **backend-developer** | PHI redaction middleware specs, structured logging requirements, FHIR authorization patterns |
| **platform-engineer** | Golden path templates for HIPAA-compliant services, pre-approved PHI infrastructure patterns |
| **security-reviewer** | Healthcare-specific review criteria, PHI-in-code scanning rules, BAA verification checks |
| **cto-advisor** | Healthcare security strategy, build-vs-buy for clinical systems, security budget benchmarks |

## Compatible (Side-by-Side)

| Skill | Integration Point |
|---|---|
| **gdpr-privacy** | Cross-jurisdictional PHI handling: HIPAA + GDPR for EU patient data |
| **privacy-engineer** | De-identification design, privacy-by-design for health data, consent management |
| **site-reliability-engineer** | Clinical system SLOs, downtime procedures, disaster recovery for PHI systems |
| **finops-engineer** | Healthcare security cost optimization, encryption cost modeling, BAA-required service pricing |
| **migration-architect** | PHI-safe cloud migrations, legacy EHR lift-and-shift security, data center exit compliance |

## Typical Engagement Sequence

```
1. regulatory-specialist → Confirm applicable regulations (HIPAA, state laws, FDA)
2. legal-advisor → Review BAA templates and breach notification obligations
3. system-architect → Model the target system (C4 context + container diagrams)
4. healthcare-security → Design security architecture (this skill)
5. cloud-architect → Select cloud services with BAA support
6. networking-engineer → Design clinical network segmentation
7. api-designer → Design FHIR API with SMART authorization
8. database-designer → Design encrypted PHI storage schemas
9. security-engineer → Review and harden all components
10. compliance-officer → Map controls to HITRUST CSF, prepare audit evidence
11. incident-responder → Validate breach notification pipeline
```

## Skill Interaction Rules

- **Never override security-engineer on general hardening decisions.** Healthcare
  security adds healthcare-specific constraints on top of general security.
- **Always consult compliance-officer before claiming HIPAA compliance.**
  Compliance is a legal determination, not a technical one.
- **Engage legal-advisor for any breach notification decision.** The 60-day
  clock and notification thresholds have legal consequences.
- **Fed into incident-responder at first sign of compromise.** Do not attempt
  to contain a breach within the healthcare security skill alone.
