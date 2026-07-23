---
name: compliance-officer
description: SOC2, ISO 27001, GDPR, HIPAA, PCI-DSS compliance frameworks, audit preparation,
  control mapping, evidence collection, and policy writing. Triggered by compliance,
  SOC2, ISO 27001, GDPR, HIPAA, PCI-DSS, audit, GRC, policy, control.
author: Sandeep Kumar Penchala
type: security
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- compliance-officer
token_budget: 2625
chain:
  consumes_from:
  - gdpr-privacy
  - health-regulatory-submission
  - hipaa-technical-implementation
  - incident-responder
  - legal-advisor
  - regulatory-specialist
  - security-engineer
  feeds_into:
  - accountant
  - ai-safety-engineer
  - ai-safety-health-reviewer
  - clinical-informatics-specialist
  - content-policy-manager
  - gdpr-privacy
  - health-regulatory-submission
  - hipaa-technical-implementation
  - hr-manager
  - incident-responder
  - medical-content-reviewer
  - privacy-engineer
  - regulatory-specialist
  - security-engineer
output:
  type: code
  path_hint: ./
------
# Compliance Officer

Navigate security and privacy compliance frameworks, prepare for audits, map controls across
regulatory requirements, collect and organize evidence, and author clear, actionable policies.
Covers SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, and the unified control framework approach.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── SOC 2 certification → Start at "Core Workflow > Phase 1 (Framework Selection and Scoping)"
├── ISO 27001 certification → Go to "Core Workflow > Phase 1" then "Sub-Skills > iso27001-compliance"
├── GDPR compliance → Jump to "Core Workflow > Phase 1" then "Sub-Skills > gdpr-compliance"
├── HIPAA compliance → Go to "Sub-Skills > hipaa-compliance"
├── PCI-DSS compliance → Go to "Sub-Skills > pcidss-compliance"
├── Audit preparation → Jump to "Core Workflow > Phase 1" then "Decision Trees > Audit Readiness Depth"
├── Control mapping → Go to "Core Workflow > Phase 2 (Control Mapping and Gap Analysis)"
├── Evidence collection → Jump to "Core Workflow > Phase 4 (Evidence Collection)"
├── Policy writing → Go to "Core Workflow > Phase 3 (Policy Authoring)"
├── Need security implementation → Invoke `security-engineer` skill instead
├── Need incident response planning → Invoke `incident-responder` skill instead
├── Need legal interpretation → Invoke `legal-advisor` skill instead
├── Need regulatory filing guidance → Invoke `regulatory-specialist` skill instead
└── Don't know where to start? → Start at "Decision Trees > Framework Selection"
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

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
<!-- DEEP: 10+min -->
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

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Control Mapping and Gap Analysis
1. Build a unified control framework: map each regulatory requirement to a single internal control to reduce duplication.
2. Use standard control mappings: Cloud Security Alliance CCM, NIST 800-53, CIS Controls, or UCF Common Controls Hub.
3. Perform a gap analysis: for each required control, assess current state (fully implemented, partially, not implemented).
4. Prioritize gaps by risk: controls that address high-likelihood/high-impact risks get remediation priority.
5. Create a remediation roadmap with owners, deadlines, and success criteria for each gap.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Policy Authoring
1. Establish a policy hierarchy:
   - **Policy**: high-level, principle-based, approved by leadership (e.g., Access Control Policy).
   - **Standard**: specific technical requirements (e.g., password standard: min 16 chars, MFA required).
   - **Procedure**: step-by-step instructions (e.g., employee offboarding checklist).
2. Write policies that are concise, actionable, and auditable. Use clear language: "All production access requires MFA" not "Access should be appropriately secured."
3. Maintain a policy exception process: document, approve, review quarterly, expire after 90 days.
4. Version policies, maintain a review cadence (annual minimum), and require employee acknowledgment.
5. Store policies in a single accessible location with search and linking between related documents.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Evidence Collection
1. Create an evidence matrix mapping each control to the required evidence type and collection frequency.
2. Automate evidence collection where possible: scripts to capture AWS Config rules status, CloudTrail completeness, IAM policy snapshots.
3. For manual evidence: document screenshots with visible timestamps, system identifiers, and clear descriptions.
4. Organize evidence by control ID in a centralized repository (GRC tool, SharePoint, or structured cloud storage).
5. Implement continuous compliance monitoring: drift detection alerts when a previously compliant control falls out of compliance.

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Audit Execution and Ongoing Compliance
1. Hold a kickoff with the auditor: review scope, timeline, evidence delivery method, and communication cadence.
2. Respond to auditor requests within SLA (typically 48 hours); assign a single point of contact to coordinate.
3. For findings: acknowledge, categorize by severity, define a corrective action plan (CAP) with deadlines, and implement.
4. After certification: maintain the compliance posture continuously, not just before audits.
5. Schedule quarterly internal reviews, annual external surveillance audits (ISO), and continuous monitoring.


### Cross-skills Integration
```bash
# Security implementation → Compliance mapping → Legal review → Executive strategy → Regulatory filing
/security-engineer && /compliance-officer && /legal-advisor
/cto-advisor && /compliance-officer && /regulatory-specialist
# Map controls from security implementations. Coordinate with legal for regulatory interpretation and filing.
```

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

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo
Focus: SOC 2 Type I compliance using checklists and shared drive. Tooling: spreadsheets + shared drive. Cost: $0-200/month. Audit prep: DIY with checklist, 1-2 weeks. Policies: 5-10 core policies from templates. Evidence: manual screenshots. Skip: multiple frameworks, automation, enterprise GRC tooling.

### Small Team
Focus: SOC 2 + GDPR compliance with consultant assistance. Tooling: Vanta/Drata for automated monitoring. Cost: $2K-10K/month. Audit prep: consultant-assisted, 4-6 weeks. Policies: 15-25 policies, annual review. Evidence: semi-automated (scripts + docs). Coordination: with engineering on evidence collection automation.

### Medium Team
Focus: 3-4 frameworks (SOC 2, ISO 27001, GDPR, PCI-DSS) with full-time GRC person. Tooling: GRC platform (Vanta + Jira integration). Cost: $10K-50K/month. Audit prep: dedicated GRC person, 8-12 weeks. Policies: 30-50 policies, semi-annual review, exception process. Evidence: automated pipeline (60% auto-collected). Coordination: with legal on policy exceptions, with security on evidence pipeline.

### Enterprise
Focus: Unified Control Framework across 6+ regulations, continuous compliance. Tooling: Enterprise GRC (Archer, ServiceNow) + custom integrations. Cost: $50K-200K+/month. Audit prep: Dedicated GRC team (2+), continuous compliance. Policies: 50+ policies, policy-as-code, automated attestation. Evidence: continuous monitoring with drift detection. Coordination: with audit committee on findings, with legal on regulatory changes, with finance on SOX controls.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | First enterprise customer requires SOC 2 report |
| Small → Medium | First major audit with external auditor; multiple frameworks overlap |
| Medium → Enterprise | IPO prep, FedRAMP, or operating in 5+ regulated jurisdictions |

## What Good Looks Like

> Compliance is a seamless operating rhythm, not a pre-audit fire drill. Every control has automated evidence collection running on a cadence, every policy is versioned and acknowledged, and the unified control framework maps one internal control to five regulatory requirements without duplication. Auditors receive organized evidence packages within hours, not weeks, and the organization passes surveillance audits with zero major findings because compliance is continuously verified, not annually assembled. The GRC program is so well-instrumented that a new framework can be scoped and gap-assessed in under a week.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `legal-advisor` | DPA terms, SCCs for data transfers, breach notification requirements, regulatory filing deadlines | Before interpreting regulatory obligations or drafting compliance policies |
| `security-engineer` | Technical control evidence, vulnerability management metrics, audit preparation support, control implementation status | Before mapping controls to frameworks or preparing audit evidence |
| `regulatory-specialist` | Jurisdiction-specific regulatory requirements, filing procedures, regulator communication protocols | Before scoping frameworks or determining regulatory applicability |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `security-engineer` | Control requirements mapped to technical implementations, compliance evidence expectations, remediation priorities | Security teams build controls without compliance alignment — audit findings inevitable |
| `incident-responder` | Breach classification criteria, regulatory notification clock triggers, evidence preservation requirements | Incident response misses regulatory deadlines — fines and penalties |
| `gdpr-privacy` | Data subject rights requirements, DPIA triggers, cross-border transfer restrictions | GDPR compliance gaps — regulatory exposure |
| `privacy-engineer` | Privacy-by-design requirements, data classification guidance, PII handling policies | Privacy controls not embedded in architecture — retrofitting costs |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Unified control framework**: one control satisfies many requirements; do the work once.
- **Policy as code**: where possible, enforce policies automatically (OPA, AWS SCPs, Azure Policy) rather than relying on manual adherence.
- **Evidence automation**: script evidence collection; manual screenshots don't scale beyond 20 controls.
- **Tone from the top**: executive sponsorship is critical — compliance isn't just a security team responsibility.
- **Vendor risk management**: assess third-party compliance; require SOC 2 reports or ISO certificates from critical vendors.
- **Privacy by design**: bake GDPR/CCPA data subject rights (access, deletion, portability) into system architecture from day one.


<!-- DEEP: 10+min -->
### Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| SOC 2 audit fails -- no evidence for change management control | No automated evidence collection; relies on annual manual screenshots, missing key time periods | Implement continuous evidence automation (Vanta/Drata scripts, evidence-as-code, monthly snapshots stored per control) | Manual evidence collection always misses the gap auditors find -- automate before the audit, not after the finding |
| GDPR fine issued for dark patterns in consent UX | Checkbox pre-ticked, opt-out requires 5 clicks vs 1-click opt-in, no consent audit trail | Deploy proper consent management (granular opt-in, preference center, audit-logged consent events, no pre-ticked checkboxes) | Dark patterns violate GDPR Article 7 (freely given consent) and cost 4% of global revenue -- UX is a compliance surface |
| HIPAA violation -- unsecured PHI found in application logs | Application logging diagnosis codes and patient IDs to plaintext logs with no encryption or access controls | Implement log redaction pipeline (PII detection, log sanitization, encrypted log storage, restricted access) | Logs are a compliance surface, not just a debugging tool -- PHI in logs is a breach, not a bug |
| Penetration test failed -- all critical controls had gaps | Compliance program focused on policy documentation; assumed technical controls were correctly implemented | Run internal pen test before external audit; map security test findings to control framework; remediate gaps before assessment | Documentation without security validation is theater -- auditors and pentesters both check controls independently |
| Scope creep doubled audit cost and timeline | No clear system boundary definition; scoped all SaaS tools and internal tools into initial audit | Define explicit in-scope/out-of-scope systems with boundary diagrams; only include systems that process regulated data | Scope is the #1 cost driver -- over-scoping multiplies time, cost, and complexity without improving compliance posture |
| SOC 2 audit failure from missing evidence collection | Automated evidence collection pipeline wasn't implemented; relied on manual screenshots that auditors rejected as insufficient | Implement continuous evidence collection with automated screenshots and log exports. Use a compliance platform (Vanta/Drata) that maps controls to evidence. Run a mock audit before the real one. | A startup failed SOC 2 Type II because they couldn't prove the control was operating for the full audit period. Their manual screenshots only covered the last 2 weeks. Re-audit cost: $30K + 3 months delay closing enterprise deals. |
| GDPR fine for insufficient consent records | Consent management platform wasn't capturing audit-grade records of user consent | Implement a consent management platform (CMP) that records: who, when, what version of consent was shown, what the user clicked. Keep consent records for the duration of data processing plus 3 years. | A German data protection authority fined a SaaS company 500K EUR because they couldn't prove a user had consented to marketing emails before sending them. The CMP only tracked "accepted/declined" without timestamps or version. |
| HIPAA violation from third-party data sharing without BAA | Engineering team used a subprocessor (analytics tool, cloud provider, AI API) without signing a Business Associate Agreement | Maintain a subprocessor register. Before engaging any third party that touches PHI: sign a BAA, verify their HIPAA compliance, and limit data sharing to minimum necessary. Review quarterly. | A health tech startup used an AI summarization API that analyzed de-identified clinical notes. The API provider didn't have a BAA. HHS fined the startup $150K after an audit discovered the arrangement. |
| Failed penetration test -- critical findings with no remediation plan | Pen test was treated as a checkbox, not a security improvement exercise; findings went unaddressed for months | Run penetration tests annually (bi-annually for critical systems). For each finding: assign owner, set remediation deadline, track to closure. Severity-based SLAs: Critical <7 days, High <30 days, Medium <90 days. | A startup's pen test found 12 critical vulnerabilities. The CEO ignored the report for 6 months. When an enterprise customer's security team asked for the pen test report, they walked from a $500K deal. |
| Ransomware attack encrypted 2 years of financial data | No offline backups; cloud backups were in the same account that got compromised | Implement the 3-2-1 backup rule: 3 copies, 2 different media types, 1 offline/air-gapped. Test restore monthly. Encrypt backups. Use immutable backup storage (WORM). | A company paid $1.2M in Bitcoin to recover from ransomware because their cloud backups were in the same AWS account as production. The attacker deleted the backups before triggering the encryption. Offline backups would have made the ransom unnecessary. |


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
