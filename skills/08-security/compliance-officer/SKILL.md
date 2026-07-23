---
name: compliance-officer
description: >
  Use when preparing for SOC 2, ISO 27001, HIPAA, or PCI-DSS audits, mapping controls
  across frameworks, collecting audit evidence, writing compliance policies, or
  performing vendor risk assessments. Handles framework scoping (SOC 2, ISO 27001,
  HIPAA, PCI-DSS), control mapping, gap analysis, evidence collection, policy
  authoring, and unified control framework design. Do NOT use for GDPR or
  privacy-specific compliance, legal contract review, or regulatory submission
  preparation.
license: MIT
allowed-tools: Read Grep Glob
tags:
- compliance
- soc2
- iso27001
- hipaa
- pci-dss
- audit
- grc
- policy
author: Sandeep Kumar Penchala
type: security
status: stable
version: 1.1.0
updated: 2026-07-23
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
---

# Compliance Officer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Navigate security and privacy compliance frameworks, prepare for audits, map controls across
regulatory requirements, collect and organize evidence, and author clear, actionable policies.
Covers SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, and the unified control framework approach.

## Route the Request

<!-- Machine-executable routing: 8 file_contains/file_exists rows A1-A8 + Intent Route fallback -->

| # | Detect Condition | Route To | Intent Route Fallback |
|---|-----------------|----------|----------------------|
| **A1** | `file_contains("*.md", "SOC.2\|SOC2\|soc2\|soc-2")` or `file_exists("soc2/")` | Core Workflow → Phase 1 (SOC 2 Scoping) | "I detect SOC 2 references — routing to Framework Selection and Scoping for SOC 2." |
| **A2** | `file_contains("*.md", "ISO.27001\|ISO27001\|iso27001\|27001:2022")` or `file_exists("iso27001/")` | Sub-Skills → ISO 27001 Compliance | "I detect ISO 27001 references — routing to ISO 27001 Compliance sub-skill." |
| **A3** | `file_contains("*.md", "GDPR\|data.subject\|DSAR\|DPIA\|right.to.be.forgotten")` or `file_exists("gdpr/")` | Invoke `gdpr-privacy` skill | "I detect GDPR-specific artifacts — this is GDPR work. Routing to gdpr-privacy skill." |
| **A4** | `file_contains("*.md", "HIPAA\|PHI\|ePHI\|BAA\|covered.entity\|HITECH")` or `file_exists("hipaa/")` | Sub-Skills → HIPAA Compliance | "I detect HIPAA/PHI references — routing to HIPAA Compliance sub-skill." |
| **A5** | `file_contains("*.md", "PCI.DSS\|PCI-DSS\|pcidss\|cardholder\|CHD\|SAQ")` or `file_exists("pci-dss/")` | Sub-Skills → PCI-DSS Compliance | "I detect PCI-DSS references — routing to PCI-DSS Compliance sub-skill." |
| **A6** | `file_exists("policies/")` or `file_exists("evidence/")` and `file_contains("*.md", "audit\|control.*framework\|compliance")` | Core Workflow → Phase 2 (Gap Analysis) | "I detect audit evidence and control framework artifacts — routing to Control Mapping and Gap Analysis." |
| **A7** | `file_contains("*.md", "vendor.*assessment\|DPA\|data.processing\|sub.processor\|BAA")` or `file_exists("vendor-assessments/")` | Decision Trees → Vendor Risk Management | "I detect vendor assessment artifacts — routing to Vendor Risk Management decision tree." |
| **A8** | `file_contains("*.md", "penetration.test\|pentest\|security.*audit\|vulnerability.*assessment")` or `file_exists("pentest/")` | Core Workflow → Phase 4 (Evidence Collection) | "I detect pentest/security audit references — routing to Evidence Collection phase." |

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to state an organization is "compliant" without auditor attestation.** Only a certified auditor performing a formal assessment can issue an attestation. | Trigger: output contains "you are compliant" OR "your organization is compliant" OR "you're SOC 2 compliant" OR "you're ISO 27001 certified" | STOP. Respond: "I cannot declare compliance. I can assess controls against known criteria, identify gaps, and recommend remediation — but only a certified auditor performing a formal assessment can issue an attestation. Instead, I can say: 'Your controls appear aligned with [framework section].'" |
| **R2** | **REFUSE to scope a compliance audit without a data flow diagram (DFD).** Every system that processes, stores, or transmits regulated data must be identified before scoping. | Trigger: user asks for audit scope recommendation AND `grep -rn "data.flow\|DFD\|boundary\|system.inventory" --include="*.md" --include="*.drawio"` returns 0 results in the repo | STOP. Respond: "I need a data flow diagram or system inventory first. Without knowing which systems process, store, or transmit regulated data, I cannot define a defensible audit scope. Share your DFD or answer: (1) What systems touch customer data? (2) Where does data enter and leave your environment? (3) What third parties process your data?" |
| **R3** | **REFUSE to recommend controls without verifying the current framework version.** ISO 27001:2022 differs from 2013. SOC 2 criteria are updated by AICPA. PCI-DSS v4.0 has new requirements vs 3.2.1. | Trigger: output references a compliance framework section number without a version check statement | STOP. Insert verification: "Confirm this control reference is current for your target framework version. [Framework] [version] introduced changes. Verify with the authoritative source before proceeding." |
| **R4** | **STOP and require evidence collection mechanism confirmation.** Manual screenshots collected 2 weeks before audit are insufficient. Auditors test the FULL audit period. | Trigger: user describes evidence collection plan AND `grep -rn "automated\|continuous\|Vanta\|Drata\|Secureframe\|evidence.as.code" --include="*.md"` returns 0 results in the repo | STOP. Respond: "Manual evidence collection fails audits. Auditors test the FULL audit period — 2 weeks of screenshots for a 12-month period will be rejected. Before proceeding, confirm: (1) What automated evidence collection tool do you use? (2) What cadence does evidence collection run on? (3) How do you detect evidence gaps?" |
| **R5** | **DETECT and WARN about vendor risk assessments without sub-processor review.** Signing a vendor's DPA without reviewing sub-processor list and cross-border transfer mechanisms is a compliance gap. | Trigger: output mentions vendor/processor approval without `grep -rn "sub.processor\|subprocessor\|SCC\|BCR\|TIA" vendor/` confirmation | WARN: Add comment "⚠️ Verify: (1) Has the vendor's sub-processor list been reviewed? (2) Are SCCs/BCRs in place for non-adequate-jurisdiction sub-processors? (3) Has a Transfer Impact Assessment been completed? Vendor self-declaration of compliance is not a transfer mechanism." |
| **R6** | **DETECT and WARN about policy language that is un-auditable.** Policies using "should" or "aspire to" cannot be tested during an audit. | Trigger: generated policy text contains "should" or "we aspire" or "we aim to" without corresponding "must" + measurement clause | WARN: Replace with auditable language. Every policy statement must be verifiable — "MFA enforced for all human users, verified quarterly via IAM access review." If you can't write the audit test for a policy statement, rewrite it. |
| **R7** | **DETECT and WARN about over-scoping audits to include non-regulated systems.** Every system in scope adds 3-5 controls to test. Over-scoping multiplies time, cost, and complexity. | Trigger: user's scope list includes dev/staging environments, internal wikis, or HR tools not processing regulated data | WARN: Flag "The following systems may not need to be in scope: [list]. Only systems that process, store, or transmit regulated data belong in scope. Each system in scope adds 3-5 controls to test and hours of evidence collection. Confirm with your auditor before finalizing." |

## The Expert's Mindset

Master compliance officers know that compliance is not about checklists — it's about **building evidence of control effectiveness that holds up under regulator scrutiny and, more importantly, actually reduces risk.** The worst compliance program is the one that passes audits while the organization burns.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Checkbox compliance** — confusing framework adherence with actual security | For every control in your framework, ask: "If this control were silently failing, how would we know?" If you can't answer, it's theater. |
| **Framework fetishism** — treating SOC 2 / ISO 27001 as a security program rather than a point-in-time attestation | Compliance is the floor, not the ceiling. Your security program should make auditors nod, not define it. |
| **Evidence theater** — collecting screenshots and policy documents without validating the underlying control | Sample-test controls quarterly: pick 5 evidence items at random and trace them end-to-end. If any fail, the control is not operational. |
| **Audit-as-finish-line** — treating certification as the goal rather than continuous compliance | Between audits is where compliance decays. Automate control monitoring; the audit should be a review of 12 months of evidence, not a fire drill. |

### What Masters Know That Others Don't
- **Which controls auditors actually test deeply vs. skim** — every framework has 5-10 controls that get forensic scrutiny and 50+ that get a nod. Invest your preparation time accordingly.
- **The regulator's unstated concerns** — they care about customer harm, data breaches, and systemic risk. Frame every control in terms of how it prevents these; don't just cite the framework paragraph.
- **That compliance is a product management problem** — you're selling security behavior to engineers, executives, and auditors simultaneously. Each audience needs different evidence, different language, different cadence.

### When to Break Your Own Rules
- **Accept a finding when the remediation creates more risk than the gap.** A "medium" finding on quarterly access reviews that would take 3 sprints to fix might be better accepted with compensating detective controls.
- **Write the exception, don't hide the gap.** Auditors respect documented, risk-accepted exceptions more than undocumented compliance. Transparency builds trust; surprises burn it.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single test/review | Execute defined quality procedures; follow checklists |
| **L2** | Feature quality | Own quality for a feature area; write custom test strategies |
| **L3** | System quality | Design quality strategy for a system; define gates and thresholds; mentor |
| **L4** | Org quality | Define org-wide quality standards; make investment cases for quality tooling |
| **L5** | Industry quality | Create quality methodologies adopted across the industry |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 compliance officer, review..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

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

## What Good Looks Like

> Compliance is a seamless operating rhythm, not a pre-audit fire drill. Every control has automated evidence collection running on a cadence, every policy is versioned and acknowledged, and the unified

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

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

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| A new vendor or SaaS tool is being onboarded without a completed vendor risk assessment | Halt onboarding until the vendor provides a SOC 2 Type II report, ISO 27001 certificate, or completes your security questionnaire. Require a DPA if they process personal data. Unvetted vendors are the #1 source of fourth-party risk. | Vendor risk is your risk. A vendor breach involving your customer data is your breach in the eyes of regulators and customers. |
| A data subject access request (DSAR) arrives with a 30-day GDPR/CCPA response deadline and no process exists to handle it | Start the clock immediately. Identify all systems that store the subject's data, collect and collate the records, redact third-party data, and respond within the deadline. Document every step — regulators will audit the process, not just the outcome. | GDPR Article 15 fines start at €10M or 2% of global turnover. A missed DSAR deadline is the easiest fine for a regulator to issue because the violation is binary: you responded on time or you didn't. |
| The scope of an upcoming SOC 2 audit includes systems that don't process or store customer data | Challenge the scope immediately — over-scoping multiplies audit cost, timeline, and complexity. Define explicit system boundaries with a data flow diagram showing which systems touch regulated data. | Scope creep is the #1 cost driver in compliance audits. Every system in scope adds controls to test, evidence to collect, and auditor hours to bill. |
| A new regulation (e.g., EU AI Act, state privacy law) passes that may apply to the business within 12–18 months | Start a regulatory impact assessment within 30 days. Map the regulation's requirements to your existing control framework. The worst time to discover you need a 12-month implementation program is 6 months before the enforcement date. | Regulatory lead time is your most valuable compliance asset. Starting early means you can phase implementation. Starting late means you're racing a hard deadline with no margin for error. |
| Evidence collection for a continuous monitoring control has been failing silently for >1 week | The control is effectively non-operational for the period the evidence is missing. Fix the collection pipeline immediately and document the gap — auditors will ask about the missing evidence window. A 1-week gap in a 52-week audit period is a finding. | Continuous monitoring means continuous. Every day of missing evidence is a day auditors can claim the control wasn't operating. Document the gap and implement alerting for collection failures. |
| An employee reports that a data processing activity doesn't match what's documented in the Record of Processing Activities (ROPA) | Update the ROPA within 72 hours. GDPR Article 30 requires the ROPA to be accurate and up to date. An inaccurate ROPA is both a standalone violation and evidence that your data governance processes are broken. | The ROPA is the foundation of GDPR compliance. If regulators discover processing activities not documented in your ROPA, they will question what else is missing. |
| A third-party vendor announces a data breach that potentially involves your customer data | Activate your incident response plan: determine what data was exposed, notify your DPO within 24 hours, assess breach notification obligations (GDPR: 72 hours to supervisory authority), and prepare customer notification. Delay turns a vendor breach into your negligence. | The clock starts when you learn of the breach, not when the vendor confirms the details. Regulators expect you to notify within the deadline even if you're still investigating — you can update the notification as more facts become available. |
| A penetration test or security audit finds that documented controls don't match implemented controls | This is a control design failure — your policy says one thing, your infrastructure does another. Remediate the gap and update either the control implementation or the policy. Mismatched documentation is guaranteed to produce audit findings. | Documentation without implementation is compliance theater. Auditors verify that controls exist and operate — if your access review policy says "quarterly" but you only review annually, that's a finding. |

## Deliberate Practice

```mermaid
graph LR
    A[Test/Review] --> B[Find gap] --> C[Study<br/>root cause] --> D[Improve<br/>prevention] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Review your own work from 3 months ago; catalog everything you'd now flag | Monthly |
| **Competent** | Shadow a more senior reviewer; compare their findings to yours; study the delta | Weekly |
| **Expert** | Design a new quality gate; measure false positive/negative rates; tune for 6 months | Quarterly |
| **Master** | Create a training module that teaches others your quality intuition; measure their improvement | Quarterly |

**The One Highest-Leverage Activity:** Keep a "mistakes journal." Every time you miss something, write down: what you missed, why you missed it, and what rule would have caught it.

## Gotchas

- **SOC 2 Type II** covers a period (usually 6-12 months), not a point in time. If you implemented a control on month 5, the auditor only tests months 5-12. Controls added mid-period have partial coverage, which may not satisfy the report's intended use.
- **GDPR "right to erasure"** (Article 17) doesn't mean delete everything. You must erase personal data — but retain transaction records for tax law, fraud logs for security, and backup tapes that can't be surgically deleted. The exception for "legal obligation" must be documented per-request.
- **Audit log immutability**: `chmod -w audit.log` prevents overwriting but not appending. An attacker with write access can APPEND fake log entries that look like normal activity. Immutable storage (S3 Object Lock, WORM drives) prevents both overwrite and append.
- **Data retention policies** that say "delete after 7 years" — if you delete exactly at year 7, data from Jan-Dec is mixed. Records created Dec 31 need to live until Dec 31 + 7 years. Retention must be per-record, not per-calendar-year.
- **"Encryption at rest" means different things** to different auditors. AWS RDS encryption (KMS-managed keys) counts. Application-level encryption (encrypt before writing) counts. But disk-level encryption (EBS volume encryption) doesn't count if the auditor requires separation of duties between data controller and infrastructure provider.

## Verification

- [ ] Control mapping: every compliance requirement (SOC 2, ISO 27001, GDPR) maps to at least one implemented control
- [ ] Evidence collection: for each control, evidence is current (collected within the audit period, not from last year)
- [ ] Policy review: all policies reviewed within last 12 months, version history shows updates
- [ ] Access review: quarterly access review completed — all accounts have documented business justification
- [ ] Vendor risk assessment: all vendors handling sensitive data have current (≤ 12 months) risk assessment
- [ ] Incident response test: tabletop exercise conducted within last 6 months, findings tracked to remediation

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

