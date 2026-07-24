# Financial Regulatory Cybersecurity Framework

FFIEC CAT, NYDFS 23 NYCRR 500, DORA (EU), GLBA Safeguards Rule, and
MAS TRM compliance requirements for financial services cybersecurity.

## FFIEC Cybersecurity Assessment Tool (CAT)

Self-assessment methodology for financial institutions (US). Not a law but
heavily referenced by FDIC/OCC/FRB examiners.

### Maturity Levels
| Level | Name | Characteristics |
|-------|------|----------------|
| 1 | Baseline | Ad hoc, reactive, minimal documentation, no testing |
| 2 | Evolving | Some processes documented, inconsistent execution |
| 3 | Intermediate | Documented, consistently executed, metrics tracked |
| 4 | Advanced | Automated, continuously improved, predictive analytics |
| 5 | Innovative | Cutting-edge, fully integrated, industry-leading |

### Five Domains
1. **Cyber Risk Management & Oversight**: board engagement, risk appetite, policies
2. **Threat Intelligence & Collaboration**: ISAC membership, threat feeds, information sharing
3. **Cybersecurity Controls**: preventive, detective, corrective controls
4. **External Dependency Management**: vendor risk, supply chain, cloud providers
5. **Cyber Incident Management & Resilience**: IR plan, testing, business continuity

## NYDFS 23 NYCRR 500 (New York)

Applies to any financial services company licensed/regulated by NYDFS
(not just NY-based — any company operating in NY).

### Key Requirements

| Section | Requirement | Deadline |
|---------|-------------|----------|
| 500.02 | CISO appointment (qualified individual) | Immediate |
| 500.03 | Cybersecurity policy approved by board/senior officer | Annual |
| 500.04 | CISO annual report to board on program status | Annually by Feb 15 |
| 500.05 | Penetration testing + vulnerability assessment | Annual pen test, twice-yearly vuln |
| 500.06 | Audit trail — detect and respond to cybersecurity events | Continuous |
| 500.07 | Access controls — least privilege, periodic review | Semi-annual review |
| 500.09 | Risk assessment — identify, evaluate, document risks | Annual |
| 500.11 | Third-party service provider security policy | Annual review |
| 500.12 | MFA for any individual accessing internal systems | Rolling deadline |
| 500.14 | Security awareness training (all personnel) | Annual |
| 500.16 | Incident response plan — tested annually | Annual testing |
| 500.17 | Annual certification of compliance to NYDFS superintendent | By April 15 annually |

### Recent Updates (Nov 2023)
- **Class A Companies** (>$20B revenue, >2,000 employees): enhanced requirements
  - Independent audit of cybersecurity program (annual)
  - Centralized vulnerability management
  - Privileged access management (PAM) solution
- All companies: board must have cybersecurity expertise (or advisor)
- CISO must have adequate independence and authority

## DORA (Digital Operational Resilience Act) — EU, effective Jan 2025

Applies to ALL EU financial entities + critical ICT third-party providers.

### Five Pillars
1. **ICT Risk Management**: framework for all ICT risks, governance, policies
2. **ICT Incident Management**: classification, reporting major incidents to regulators (24h initial, 72h detailed, 1 month final)
3. **Digital Operational Resilience Testing**: basic testing annual, TLPT (Threat-Led Penetration Testing) every 3 years for systemic entities
4. **ICT Third-Party Risk**: register of all ICT third-party providers, critical provider oversight framework (EU-level lead overseer), contract termination and exit planning
5. **Information Sharing**: intelligence sharing arrangements, voluntary information exchange

### TLPT (Threat-Led Penetration Testing)
- Must test critical or important functions, production systems
- External testers: independent, certified (TIBER-EU framework)
- Cannot use internal blue/red teams unless independently verified
- Frequency: every 3 years for financial entities identified as systemic

## GLBA Safeguards Rule (US)

Gramm-Leach-Bliley Act — applies to "financial institutions" broadly defined
(includes mortgage brokers, auto dealers, tax preparers, fintech companies).

### Requirements (Updated 2023)
1. Designate qualified individual to coordinate security program
2. Risk assessment: written, criteria for evaluating internal/external risks
3. Access controls: technical + physical controls for customer information
4. Encryption: at rest and in transit for customer information OR equivalent
5. MFA: for any individual accessing customer information systems
6. Secure disposal: customer information no longer needed (2 years post-relationship)
7. Change management: documented, tested before deployment
8. Monitoring and logging: authorized user activity, detect unauthorized access
9. Annual penetration testing + vulnerability assessment (every 6 months)
10. Security awareness training (annual, specialized for security personnel)
11. Incident response plan: written, tested, specific to customer information
12. Service provider oversight: risk assessment, contract requirements, periodic reassessment

### Penalties
- FTC: $50,120 per violation (adjusted for inflation)
- Each day of non-compliance = separate violation
- CFPB: additional penalties for consumer financial protection violations

## MAS TRM (Monetary Authority of Singapore — Technology Risk Management)

### Key Focus Areas
- Technology risk management framework: board-approved, reviewed annually
- IT operations management: capacity, performance, availability monitoring
- Cyber security operations: SOC, incident response within defined SLAs
- Data center resilience: tier requirements, disaster recovery testing
- Access controls: least privilege, privileged access management (PAM)
- Cryptography: key management lifecycle, certificate management, HSMs
- Third-party management: outsourced services, cloud providers
- Online financial services: strong authentication (2FA minimum), transaction signing
