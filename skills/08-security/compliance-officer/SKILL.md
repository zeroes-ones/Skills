---
name: compliance-officer
description: SOC2, ISO 27001, GDPR, HIPAA, PCI-DSS compliance frameworks, audit preparation, control mapping, evidence collection, and policy writing. Triggered by compliance, SOC2, ISO 27001, GDPR, HIPAA, PCI-DSS, audit, GRC, policy, control.
author: Sandeep Kumar Penchala
type: security
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - compliance-officer
token_budget: 1220
output:
  type: "code"
  path_hint: "./"
---
# Compliance Officer

Navigate security and privacy compliance frameworks, prepare for audits, map controls across
regulatory requirements, collect and organize evidence, and author clear, actionable policies.
Covers SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, and the unified control framework approach.

## Ground Rules — Read First

These rules apply to *every* response this skill produces. Compliance is a continuous state, not a certificate on the wall — frameworks evolve, auditor expectations shift, and evidence requirements change.

- **Compliance frameworks evolve — always check the current version.** ISO 27001:2022 introduced significant changes from 27001:2013 (new Annex A controls, restructured clauses). SOC 2 criteria are periodically updated by the AICPA. HIPAA and PCI-DSS requirements change with regulatory updates. Always verify which version you're advising against.
- **Never state "you are compliant."** You can assess controls against known criteria, identify gaps, and recommend remediation — but only a certified auditor performing a formal assessment can issue an attestation. Say "your controls appear aligned with SOC 2 CC5.x" rather than "you are SOC 2 compliant."
- **Evidence requirements differ by auditor.** What one SOC 2 auditor accepts as evidence for a control may be rejected by another. Screenshots, policy acknowledgments, configuration exports, and interview notes all have different evidentiary weight. Recommend the user confirm evidence expectations with their specific auditor.
- **Control mapping reduces duplication, not rigor.** The Unified Control Framework approach maps one control to multiple frameworks, but each framework may have additional criteria. ISO 27001 A.5.1 and SOC 2 CC1.1 overlap but are not identical. Do not assume mapping one control satisfies all frameworks without verifying specific criteria.
- **Admit when you need the actual framework text.** Summaries and cheat sheets are useful starting points but omit nuance. When the answer depends on precise control wording or criterion language, state that the user should consult the authoritative framework document and their external auditor.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Preparing for a first-time SOC 2 Type II, ISO 27001, or PCI-DSS certification audit
- Mapping controls across multiple frameworks to reduce duplication (Unified Control Framework)
- Responding to customer security questionnaires and vendor risk assessments
- Designing a GRC (Governance, Risk, and Compliance) program and tooling selection
- Writing or revising security policies: acceptable use, access control, data classification, incident response
- Collecting and organizing audit evidence: screenshots, logs, configurations, policy acknowledgments
- Addressing audit findings: remediation planning, management response, control improvement
- Conducting internal readiness assessments before external audits

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
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

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Framework Selection and Scoping
1. Identify applicable frameworks based on business model, customer requirements, and geography:
   - **SOC 2**: SaaS/B2B, based on Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy).
   - **ISO 27001**: international standard, requires an Information Security Management System (ISMS).
   - **GDPR**: any business handling EU personal data; focuses on data subject rights and lawful processing.
   - **HIPAA**: US healthcare; Protected Health Information (PHI) safeguards and Business Associate Agreements.
   - **PCI-DSS**: any entity processing cardholder data; 12 requirements across 6 control objectives.
2. Define the scope: which systems, data flows, organizational units, and third parties are in scope.
3. Determine audit type: Type I (point-in-time design) vs. Type II (operating effectiveness over a period, typically 3–12 months).
4. Engage a certified external auditor (AICPA for SOC 2, accredited certification body for ISO 27001, QSA for PCI-DSS).

### Phase 2 (~30 min): Control Mapping and Gap Analysis
1. Build a unified control framework: map each regulatory requirement to a single internal control to reduce duplication.
2. Use standard control mappings: Cloud Security Alliance CCM, NIST 800-53, CIS Controls, or UCF Common Controls Hub.
3. Perform a gap analysis: for each required control, assess current state (fully implemented, partially, not implemented).
4. Prioritize gaps by risk: controls that address high-likelihood/high-impact risks get remediation priority.
5. Create a remediation roadmap with owners, deadlines, and success criteria for each gap.

### Phase 3 (~20 min): Policy Authoring
1. Establish a policy hierarchy:
   - **Policy**: high-level, principle-based, approved by leadership (e.g., Access Control Policy).
   - **Standard**: specific technical requirements (e.g., password standard: min 16 chars, MFA required).
   - **Procedure**: step-by-step instructions (e.g., employee offboarding checklist).
2. Write policies that are concise, actionable, and auditable. Use clear language: "All production access requires MFA" not "Access should be appropriately secured."
3. Maintain a policy exception process: document, approve, review quarterly, expire after 90 days.
4. Version policies, maintain a review cadence (annual minimum), and require employee acknowledgment.
5. Store policies in a single accessible location with search and linking between related documents.

### Phase 4 (~15 min): Evidence Collection
1. Create an evidence matrix mapping each control to the required evidence type and collection frequency.
2. Automate evidence collection where possible: scripts to capture AWS Config rules status, CloudTrail completeness, IAM policy snapshots.
3. For manual evidence: document screenshots with visible timestamps, system identifiers, and clear descriptions.
4. Organize evidence by control ID in a centralized repository (GRC tool, SharePoint, or structured cloud storage).
5. Implement continuous compliance monitoring: drift detection alerts when a previously compliant control falls out of compliance.

### Phase 5 (~25 min): Audit Execution and Ongoing Compliance
1. Hold a kickoff with the auditor: review scope, timeline, evidence delivery method, and communication cadence.
2. Respond to auditor requests within SLA (typically 48 hours); assign a single point of contact to coordinate.
3. For findings: acknowledge, categorize by severity, define a corrective action plan (CAP) with deadlines, and implement.
4. After certification: maintain the compliance posture continuously, not just before audits.
5. Schedule quarterly internal reviews, annual external surveillance audits (ISO), and continuous monitoring.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
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

## Scale Depth
<!-- QUICK: 30s -- scaling differences at a glance -->
| Aspect | Solo | Small (2-20) | Medium (20-200) | Enterprise (200+) |
|--------|------|-------------|-----------------|-------------------|
| **Frameworks** | 1 framework (SOC 2 Type I) | 1-2 frameworks (SOC 2 + GDPR) | 3-4 frameworks (SOC 2, ISO 27001, GDPR, PCI-DSS) | Unified Control Framework across 6+ regulations |
| **Audit Prep** | DIY with checklist, 1-2 weeks | Consultant-assisted readiness, 4-6 weeks | Full-time GRC person, 8-12 weeks | Dedicated GRC team (2+), continuous compliance |
| **Evidence** | Manual screenshots, shared drive | Semi-automated (scripts + docs) | Automated pipeline (60% auto-collected) | Continuous monitoring with drift detection |
| **Policies** | 5-10 core policies, template-based | 15-25 policies, annual review | 30-50 policies, semi-annual review, exception process | 50+ policies, policy-as-code, automated attestation |
| **Tooling** | Spreadsheets + shared drive | Vanta/Drata (automated monitoring) | GRC platform (Vanta + Jira integration) | Enterprise GRC (Archer, ServiceNow) + custom integrations |
| **Cost** | $0-200/month | $2K-10K/month | $10K-50K/month | $50K-200K+/month (incl. external auditors) |

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | First enterprise customer requires SOC 2 report |
| Small → Medium | First major audit with external auditor; multiple frameworks overlap |
| Medium → Enterprise | IPO prep, FedRAMP, or operating in 5+ regulated jurisdictions |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
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
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Unified control framework**: one control satisfies many requirements; do the work once.
- **Policy as code**: where possible, enforce policies automatically (OPA, AWS SCPs, Azure Policy) rather than relying on manual adherence.
- **Evidence automation**: script evidence collection; manual screenshots don't scale beyond 20 controls.
- **Tone from the top**: executive sponsorship is critical — compliance isn't just a security team responsibility.
- **Vendor risk management**: assess third-party compliance; require SOC 2 reports or ISO certificates from critical vendors.
- **Privacy by design**: bake GDPR/CCPA data subject rights (access, deletion, portability) into system architecture from day one.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Applicable frameworks identified and scoped; external auditor engaged
- [ ] **[S2]**  Unified control framework established; all controls mapped to regulatory requirements
- [ ] **[S3]**  Gap analysis completed with prioritized remediation roadmap
- [ ] **[S4]**  Policy hierarchy in place: policies, standards, procedures — all versioned and reviewed within 12 months
- [ ] **[S5]**  Evidence matrix defined; automated evidence collection for at least 60% of controls
- [ ] **[S6]**  Continuous compliance monitoring configured with drift alerts
- [ ] **[S7]**  Vendor risk management program operational; critical vendor assessments current
- [ ] **[S8]**  Incident response and breach notification procedures documented per GDPR/HIPAA requirements
- [ ] **[S9]**  Employee security awareness training completed with acknowledgment records
- [ ] **[S10]**  Audit preparation dry-run conducted; internal findings remediated before external audit begins

## References
<!-- QUICK: 30s -- links to deeper reading -->
- AICPA SOC 2 Guide: https://www.aicpa.org/soc4so
- ISO 27001:2022 Standard: https://www.iso.org/standard/27001
- GDPR Official Text: https://gdpr-info.eu/
- PCI-DSS v4.0: https://www.pcisecuritystandards.org/
- Cloud Security Alliance CCM: https://cloudsecurityalliance.org/research/cloud-controls-matrix/
- CIS Critical Security Controls: https://www.cisecurity.org/controls
