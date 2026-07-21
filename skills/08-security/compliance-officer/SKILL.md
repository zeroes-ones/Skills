---
name: compliance-officer
description: SOC2, ISO 27001, GDPR, HIPAA, PCI-DSS compliance frameworks, audit preparation, control mapping, evidence collection, and policy writing. Triggered by compliance, SOC2, ISO 27001, GDPR, HIPAA, PCI-DSS, audit, GRC, policy, control.
author: Sandeep Kumar Penchala
---

# Compliance Officer

Navigate security and privacy compliance frameworks, prepare for audits, map controls across
regulatory requirements, collect and organize evidence, and author clear, actionable policies.
Covers SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, and the unified control framework approach.

## When to Use

- Preparing for a first-time SOC 2 Type II, ISO 27001, or PCI-DSS certification audit
- Mapping controls across multiple frameworks to reduce duplication (Unified Control Framework)
- Responding to customer security questionnaires and vendor risk assessments
- Designing a GRC (Governance, Risk, and Compliance) program and tooling selection
- Writing or revising security policies: acceptable use, access control, data classification, incident response
- Collecting and organizing audit evidence: screenshots, logs, configurations, policy acknowledgments
- Addressing audit findings: remediation planning, management response, control improvement
- Conducting internal readiness assessments before external audits

## Decision Trees

### Framework Selection

```
Business model and geography?
├── B2B SaaS selling to enterprise (US) → SOC 2 Type II
│     Start with Security criteria. Add Availability/Confidentiality as needed.
├── B2B SaaS selling to EU companies → SOC 2 + GDPR
│     GDPR is mandatory; SOC 2 is commercial expectation.
├── FinTech handling payments → PCI-DSS + SOC 2
│     PCI-DSS is mandatory if you store/process/transmit cardholder data.
├── HealthTech with PHI → HIPAA + HITECH
│     Business Associate Agreement (BAA) required with all vendors.
├── Enterprise selling globally → ISO 27001
│     Internationally recognized. Builds on SOC 2 controls with ISMS governance.
└── Startup, no enterprise deals yet → SOC 2 Type I (point-in-time)
      Quickest path to sellable compliance. Upgrade to Type II within 12 months.
```

### Audit Readiness Depth

```
Time to audit?
├── 12+ months out → Build GRC program. Unified Control Framework. Tool selection. Policy drafting.
├── 6-12 months → Framework mapping. Policy implementation. Evidence collection pipeline.
├── 3-6 months → Internal readiness assessment. Gap remediation. Evidence sprint.
└── < 3 months → Audit prep crunch. Focus on must-pass controls. Get a readiness consultant.
```

## Core Workflow

### Phase 1: Framework Selection and Scoping
1. Identify applicable frameworks based on business model, customer requirements, and geography:
   - **SOC 2**: SaaS/B2B, based on Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy).
   - **ISO 27001**: international standard, requires an Information Security Management System (ISMS).
   - **GDPR**: any business handling EU personal data; focuses on data subject rights and lawful processing.
   - **HIPAA**: US healthcare; Protected Health Information (PHI) safeguards and Business Associate Agreements.
   - **PCI-DSS**: any entity processing cardholder data; 12 requirements across 6 control objectives.
2. Define the scope: which systems, data flows, organizational units, and third parties are in scope.
3. Determine audit type: Type I (point-in-time design) vs. Type II (operating effectiveness over a period, typically 3–12 months).
4. Engage a certified external auditor (AICPA for SOC 2, accredited certification body for ISO 27001, QSA for PCI-DSS).

### Phase 2: Control Mapping and Gap Analysis
1. Build a unified control framework: map each regulatory requirement to a single internal control to reduce duplication.
2. Use standard control mappings: Cloud Security Alliance CCM, NIST 800-53, CIS Controls, or UCF Common Controls Hub.
3. Perform a gap analysis: for each required control, assess current state (fully implemented, partially, not implemented).
4. Prioritize gaps by risk: controls that address high-likelihood/high-impact risks get remediation priority.
5. Create a remediation roadmap with owners, deadlines, and success criteria for each gap.

### Phase 3: Policy Authoring
1. Establish a policy hierarchy:
   - **Policy**: high-level, principle-based, approved by leadership (e.g., Access Control Policy).
   - **Standard**: specific technical requirements (e.g., password standard: min 16 chars, MFA required).
   - **Procedure**: step-by-step instructions (e.g., employee offboarding checklist).
2. Write policies that are concise, actionable, and auditable. Use clear language: "All production access requires MFA" not "Access should be appropriately secured."
3. Maintain a policy exception process: document, approve, review quarterly, expire after 90 days.
4. Version policies, maintain a review cadence (annual minimum), and require employee acknowledgment.
5. Store policies in a single accessible location with search and linking between related documents.

### Phase 4: Evidence Collection
1. Create an evidence matrix mapping each control to the required evidence type and collection frequency.
2. Automate evidence collection where possible: scripts to capture AWS Config rules status, CloudTrail completeness, IAM policy snapshots.
3. For manual evidence: document screenshots with visible timestamps, system identifiers, and clear descriptions.
4. Organize evidence by control ID in a centralized repository (GRC tool, SharePoint, or structured cloud storage).
5. Implement continuous compliance monitoring: drift detection alerts when a previously compliant control falls out of compliance.

### Phase 5: Audit Execution and Ongoing Compliance
1. Hold a kickoff with the auditor: review scope, timeline, evidence delivery method, and communication cadence.
2. Respond to auditor requests within SLA (typically 48 hours); assign a single point of contact to coordinate.
3. For findings: acknowledge, categorize by severity, define a corrective action plan (CAP) with deadlines, and implement.
4. After certification: maintain the compliance posture continuously, not just before audits.
5. Schedule quarterly internal reviews, annual external surveillance audits (ISO), and continuous monitoring.

## Sub-Skills

When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `soc2-compliance` | Preparing for SOC 2 Type I → Type II with TSC mapping, control design, and evidence collection |
| `iso27001-compliance` | Building an ISMS, creating the Statement of Applicability, and navigating certification audit |
| `pcidss-compliance` | Determining SAQ type, completing ROC, and running quarterly ASV scans for payment systems |
| `hipaa-compliance` | Implementing HIPAA technical safeguards, BAA management, and breach notification procedures |
| `fedramp-compliance` | Navigating the ATO process, 3PAO assessment, and continuous monitoring for US government |
| `gdpr-compliance` | Conducting DPIAs, designating a DPO, handling DSARs, and managing cross-border transfers |
| `evidence-automation` | Automating evidence collection, screen captures, and audit trails across all frameworks |

## Cross-Skill Coordination

Compliance officers translate regulatory requirements into actionable controls. They coordinate with security for implementation, engineering for evidence, legal for interpretation, and executives for risk acceptance.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Security Engineer** | Control implementation, technical safeguards | Control requirements mapped to specific technical implementations; evidence of control effectiveness |
| **Security Reviewer** | Pre-audit security assessment, vulnerability management | Findings that map to compliance controls; remediation tracking for audit evidence |
| **DevOps Engineer** | Infrastructure compliance, audit logging | CloudTrail/Audit Log configuration, encryption at rest verification, backup policy enforcement, access review automation |
| **Cloud Architect** | Cloud compliance posture, data residency | Region restrictions, encryption key management, compliance certification scope (SOC 2, ISO 27001, FedRAMP) |
| **Backend Developer** | Data handling, PII processing, DSAR implementation | Data classification guidance, privacy-by-design patterns, data subject access request (DSAR) automation |
| **Legal Advisor** | Regulatory interpretation, contract review | DPA terms, SCCs for data transfers, breach notification requirements, regulatory filing deadlines |
| **CEO/CTO Strategist** | Risk acceptance, compliance investment | Compliance roadmap costs, risk acceptance for non-critical findings, certification timeline commitments |
| **Incident Responder** | Breach notification, forensic evidence | Notification clock (GDPR 72hr, HIPAA 60d), evidence preservation requirements, regulatory reporting triggers |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| New regulation applicable (e.g., EU AI Act, updated PCI DSS) | Legal Advisor, CTO, Affected teams | Gap analysis; implementation roadmap; potential certification timeline impact |
| Control failure during audit | Security Engineer, DevOps, CTO | Immediate remediation; may delay certification |
| Data breach involving PII/PHI | Legal Advisor, Incident Responder, CEO | Regulatory notification clock starts; legal assessment of obligations |
| Vendor security assessment failed (critical vendor) | CTO, Legal, Affected teams | Vendor replacement or risk acceptance; contractual implications |
| Certification expiring within 90 days | Security Engineer, CTO, External auditor | Schedule surveillance/renewal audit; confirm continuous monitoring evidence ready |

### Escalation Path

```
Regulatory inquiry or investigation? → Legal Advisor → CEO
Audit finding threatens certification? → CTO → CEO
Data breach notification required? → Legal Advisor → Incident Responder → Board
Control implementation blocked (technical)? → Security Engineer → CTO Advisor
```

## Best Practices

- **Unified control framework**: one control satisfies many requirements; do the work once.
- **Policy as code**: where possible, enforce policies automatically (OPA, AWS SCPs, Azure Policy) rather than relying on manual adherence.
- **Evidence automation**: script evidence collection; manual screenshots don't scale beyond 20 controls.
- **Tone from the top**: executive sponsorship is critical — compliance isn't just a security team responsibility.
- **Vendor risk management**: assess third-party compliance; require SOC 2 reports or ISO certificates from critical vendors.
- **Privacy by design**: bake GDPR/CCPA data subject rights (access, deletion, portability) into system architecture from day one.

## Production Checklist

- [ ] Applicable frameworks identified and scoped; external auditor engaged
- [ ] Unified control framework established; all controls mapped to regulatory requirements
- [ ] Gap analysis completed with prioritized remediation roadmap
- [ ] Policy hierarchy in place: policies, standards, procedures — all versioned and reviewed within 12 months
- [ ] Evidence matrix defined; automated evidence collection for at least 60% of controls
- [ ] Continuous compliance monitoring configured with drift alerts
- [ ] Vendor risk management program operational; critical vendor assessments current
- [ ] Incident response and breach notification procedures documented per GDPR/HIPAA requirements
- [ ] Employee security awareness training completed with acknowledgment records
- [ ] Audit preparation dry-run conducted; internal findings remediated before external audit begins

## References

- AICPA SOC 2 Guide: https://www.aicpa.org/soc4so
- ISO 27001:2022 Standard: https://www.iso.org/standard/27001
- GDPR Official Text: https://gdpr-info.eu/
- PCI-DSS v4.0: https://www.pcisecuritystandards.org/
- Cloud Security Alliance CCM: https://cloudsecurityalliance.org/research/cloud-controls-matrix/
- CIS Critical Security Controls: https://www.cisecurity.org/controls
