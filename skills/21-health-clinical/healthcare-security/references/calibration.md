# Calibration — How to Know Your Level

Self-assessment guide to determine your healthcare security maturity and
which level of this skill to invoke.

## Calibration Questions

Answer honestly. Match your current state, not your aspirational state.

### Quick Level (5 min) — You Know Enough to Triage

- [ ] You can identify whether a data element is PHI using the 18-identifier test
- [ ] You know when a cloud service requires a BAA vs. conduit exception
- [ ] You can spot PHI-in-log violations (SSN/MRN/DOB patterns in logs)
- [ ] You understand encryption is required, not optional, for ePHI
- [ ] You can identify flat network topologies as a healthcare security risk

**If most checked → Quick level. Use for triage and specific yes/no questions.**

### Standard Level (30 min) — You Can Assess a System

- [ ] You can perform a PHI data flow mapping for a single application
- [ ] You can verify BAA coverage across a vendor portfolio
- [ ] You can validate encryption posture (at-rest algorithms, in-transit TLS config)
- [ ] You can assess breach notification readiness for a single system
- [ ] You understand HITRUST CSF control domains and can map HIPAA controls
- [ ] You can review FHIR API authorization scopes for minimum necessary compliance
- [ ] You understand clinical network segmentation principles (VLAN isolation)

**If most checked → Standard level. Use for architecture reviews and assessments.**

### Deep Level (2-4 h) — You Can Design an Architecture

- [ ] You can design a complete clinical network segmentation architecture
- [ ] You can build a HITRUST CSF control mapping with evidence collection
- [ ] You can perform an FDA-aligned medical device security risk assessment
- [ ] You can design a breach notification pipeline with regulatory timelines
- [ ] You can architect de-identification strategy (Safe Harbor + Expert Determination)
- [ ] You understand the intersection of HIPAA, 42 CFR Part 2, and state privacy laws
- [ ] You can evaluate telemedicine platforms for HIPAA compliance end-to-end
- [ ] You can design healthcare ransomware response procedures with clinical continuity

**If most checked → Deep level. Use for greenfield architecture and major redesigns.**

## Maturity Indicators by Organization Size

| Organization | Typical Maturity | Common Gaps |
|---|---|---|
| Solo practice | Quick | Encryption, BAA registry, breach notification pipeline |
| Small clinic (5-20 providers) | Quick→Standard | Network segmentation, device inventory, PHI-in-log controls |
| Mid-size practice (20-100 providers) | Standard | HITRUST mapping, vendor due diligence, incident response testing |
| Community hospital | Standard→Deep | IoMT segmentation, FDA device guidance, 42 CFR Part 2 |
| Health system (multiple hospitals) | Deep | Cross-entity PHI flows, ACO data sharing, M&A security integration |
| ACO/Health plan | Deep | Population health PHI, analytics de-identification, multi-tenant BAA registry |

## When to Escalate

If your assessment reveals gaps you cannot close within your level, invoke
the skill at the next level up, or engage a specialist (incident-responder
for active breaches, legal-advisor for OCR investigation response,
compliance-officer for HITRUST certification).
