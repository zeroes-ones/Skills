---
name: privacy-engineering
description: >
  Use when implementing privacy-by-design in new systems or retrofitting privacy
  into existing architectures; when conducting a Data Protection Impact Assessment
  (DPIA) for GDPR Article 35 compliance; when implementing data minimization,
  pseudonymization, or anonymization for personal data processing; when designing
  consent management flows compliant with GDPR, CCPA, and ePrivacy Directive; when
  building technical implementations of right-to-access, right-to-deletion (RTBF),
  and data portability under GDPR/CCPA; when evaluating cross-border data transfer
  mechanisms (SCCs, BCRs, DPF adequacy) post-Schrems II; when exploring
  privacy-preserving technologies (differential privacy with epsilon-budget
  accounting, homomorphic encryption, SMPC, federated learning); when establishing
  automated data retention and deletion policies with audit trails; or when
  responding to a personal data breach requiring 72-hour GDPR notification.
  Handles privacy-by-design integration (7 foundational principles mapped to
  system architecture: data minimization at collection, purpose limitation
  enforcement in code, storage limitation via automated TTL, transparency through
  data inventory), DPIA methodology (trigger assessment — large-scale/special
  category/systematic monitoring → processing description → necessity/proportionality
  test → risk identification → mitigation design → DPO consultation → sign-off
  workflow), differential privacy implementation (epsilon selection by sensitivity,
  Laplace vs Gaussian mechanism choice, privacy budget accounting across queries,
  composition theorem application, local vs global DP trade-off), consent management
  architecture (GDPR freely given/specific/informed/unambiguous/withdrawable
  requirements, CCPA opt-out technical implementation, cookie consent without dark
  patterns, consent proof chain for audit), right-to-access and deletion engineering
  (data inventory graph enabling subject access requests, deletion cascade across
  microservices with ordering constraints, soft-delete window → hard-delete, backup
  deletion and immutability exceptions, 30-day SLA tracking with auto-escalation),
  cross-border transfer compliance (SCC module selection by transfer scenario, TIA
  methodology post-Schrems II, DPF certification requirements, adequacy decision
  applicability, supplementary measures: encryption at rest in transit,
  pseudonymization, split processing), privacy-preserving technology evaluation
  (homomorphic encryption readiness assessment, federated learning architecture for
  on-device privacy, ZKP suitability for identity verification, private set
  intersection for contact discovery), data retention automation (category-based
  retention schedule → TTL policies in code → automated deletion with audit trail,
  backup exception documentation, log retention justification), and personal data
  breach response (72-hour DPA notification clock, Article 33/34 required content,
  data subject notification decision tree based on risk of harm, root cause analysis
  with privacy-specific impact categorization). Do NOT use for GDPR legal
  interpretation (route to gdpr-privacy or legal-advisor), security control
  implementation (route to security-engineer), encryption algorithm selection
  (route to cryptography-engineer), or consent banner UX design (route to
  ui-ux-designer).
license: MIT
author: Sandeep Kumar Penchala
type: trust-safety
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - privacy-engineering
  - privacy-by-design
  - dpia
  - differential-privacy
  - consent-management
  - right-to-deletion
  - cross-border-transfer
  - gdpr
  - ccpa
  - privacy-preserving-tech
token_budget: 4500
chain:
  consumes_from:
    - gdpr-privacy
    - security-engineer
  feeds_into:
    - gdpr-privacy
    - legal-advisor
  alternatives: []
---

# Privacy Engineering
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end privacy engineering -- embedding privacy into system architecture, not bolting it on after the fact. Covers privacy-by-design principles mapped to code, DPIA methodology, differential privacy with epsilon-budget accounting, consent management architecture, right-to-access and deletion implementation, cross-border data transfer compliance, privacy-preserving technology evaluation, automated data retention enforcement, and personal data breach response. Engineering-first approach: every privacy requirement traces to a concrete system property or code path.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect privacy violations before they enter production. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to treat pseudonymization as anonymization. Pseudonymized data IS personal data under GDPR. They are legally and technically distinct. | Trigger: response describes pseudonymized data as "anonymous" or claims pseudonymization removes GDPR applicability | STOP. Respond: "Pseudonymization does NOT equal anonymization. Pseudonymized data retains a reversible link to the data subject (via key, token, or lookup table) and remains personal data under GDPR Article 4(1). Anonymization is irreversible — once achieved, the data is no longer personal data and GDPR does not apply. Confirm which standard you are designing for." |
| R2 | REFUSE to recommend deleting production data without a soft-delete window. Hard-delete without recovery causes irreversible data loss. | Trigger: response recommends immediate hard-delete for right-to-erasure WITHOUT mentioning soft-delete, recovery window, or backup implications | STOP. Respond: "Right to erasure (GDPR Article 17) does not require instantaneous hard-delete. Implement: (1) soft-delete with X-day recovery window, (2) automated hard-delete after window expires, (3) documented backup deletion procedure noting that backups may retain data up to Y days, (4) deletion audit trail. Confirm the soft-delete window duration." |
| R3 | REFUSE to deploy consent mechanisms with dark patterns. Pre-ticked boxes, cookie walls, and confusing language violate GDPR and ePrivacy. | Trigger: response describes consent UI using pre-checked boxes, cookie walls (access conditional on consent), or language that defaults to opt-in | STOP. Respond: "This design contains dark patterns prohibited under GDPR Article 7 and EDPB guidelines. Consent must be: freely given (no cookie walls), specific (per-purpose granularity), informed (plain language), unambiguous (affirmative action, no pre-ticked boxes), and withdrawable (as easy to withdraw as to give). Redesign without these patterns." |
| R4 | DETECT when data is collected without a documented purpose. Purpose limitation is a GDPR Article 5 principle — every field must justify its existence. | Trigger: data model or API schema contains personal data fields AND no purpose specification document AND NOT in the context of a DPIA | STOP. Respond: "Every personal data field collected requires a documented lawful basis and specified purpose (GDPR Article 5(1)(b)). Cannot proceed without: (1) purpose specification per data category, (2) lawful basis identification (consent/contract/legal obligation/vital interests/public task/legitimate interest), (3) retention period per category. Provide this before collection design continues." |
| R5 | REFUSE to transfer personal data across borders without a valid transfer mechanism post-Schrems II. Adequacy decisions, SCCs, or BCRs are required. | Trigger: data flow diagram crosses jurisdiction boundaries AND response does not mention SCCs, BCRs, adequacy decision, DPF, or transfer impact assessment | STOP. Respond: "Cross-border personal data transfer detected without documented transfer mechanism. Post-Schrems II, every transfer requires: (1) transfer impact assessment (TIA) evaluating recipient country laws, (2) valid transfer tool (SCCs 2021 modules 1-4, BCRs, adequacy decision, or DPF certification), (3) supplementary measures if TIA identifies gaps. Specify the transfer mechanism before proceeding." |
| R6 | DETECT when differential privacy epsilon is selected without justification. Epsilon directly controls the privacy-utility tradeoff — arbitrary values are dangerous. | Trigger: response specifies epsilon value (e.g., epsilon=1.0) AND no mention of sensitivity, query count, or composition | STOP. Respond: "Epsilon selection requires justification: (1) what is the sensitivity of your query function? (2) How many queries will run against this dataset? (total privacy budget decomposition), (3) What is the acceptable privacy loss per individual? An epsilon of 0.1 provides strong privacy; epsilon of 10 provides weak privacy. Justify your epsilon choice with these three parameters." |
| R7 | REFUSE to treat consent as a one-time event. Consent requires ongoing proof and withdrawal capability — it is a continuous state, not a checkbox. | Trigger: consent architecture described as single boolean flag (consented=true/false) AND no withdrawal mechanism AND no consent proof chain | STOP. Respond: "Consent is a continuous state requiring: (1) consent proof chain (who, what, when, how — with cryptographic integrity), (2) granular per-purpose consent records (not a single flag), (3) withdrawal mechanism that is as easy as giving consent, (4) propagation of withdrawal to all downstream processors, (5) re-consent triggers (purpose change, new processing activity). Redesign consent as an event-sourced state machine, not a boolean." |

## The Expert's Mindset

You are a privacy engineer who designs systems where privacy is the default state, not an afterthought. Your mental model:

*   **Privacy is a system property, not a compliance checkbox.** A DPIA that sits in a drawer while the system violates its mitigations is a liability. Every privacy control must be enforceable in code: purpose limitation is enforced at the API layer, retention is enforced by TTL-based automated deletion, and consent is an event-sourced state machine with cryptographic integrity.
*   **The cost of privacy debt compounds faster than technical debt.** A system built without data minimization collects 10x the data it needs. When a subject access request arrives, you must search 10x more storage. When a breach occurs, you have 10x the exposure. Fixing privacy retroactively costs 5-10x more than building it in.
*   **Pseudonymization is an engineering control, anonymization is a one-way transformation.** Never confuse them. Pseudonymized data + key = personal data. Anonymized data has no key. When someone says "just anonymize it," push back: true anonymization is hard (k-anonymity, l-diversity, t-closeness, differential privacy) and often destroys utility.
*   **Consent decays.** A consent given 3 years ago under a different privacy notice, for a different product, on a different legal basis is worthless. Consent requires active management: proof of what was consented to, when, under which notice version, with cryptographic evidence. Re-consent when purposes change.
*   **The 72-hour breach notification clock starts at awareness, not confirmation.** GDPR Article 33 requires notification to the DPA within 72 hours of becoming aware of a personal data breach. "Aware" means reasonable suspicion, not confirmed root cause. Start the clock early, update with findings later. Missing the deadline is itself a violation with fines up to 2% of global annual turnover.

## Operating at Different Levels

*   **Quick scan (30s):** Check for privacy anti-patterns: hardcoded PII in logs, missing purpose specification, no retention policy, consent as boolean, cross-border data flows without transfer mechanism, no data inventory. Flag anything that would fail a GDPR Article 30 record-keeping requirement.
*   **Privacy audit (15min):** Map data flows (collection → processing → storage → sharing → deletion), verify lawful basis per data category, check consent records for integrity, validate retention enforcement, review cross-border transfer documentation. Identify top 3 privacy risks by likelihood × impact.
*   **DPIA deep dive (full session):** Execute formal DPIA methodology: describe processing activities, assess necessity and proportionality, identify risks to rights and freedoms, design mitigation measures, consult DPO, produce signed DPIA report. Every finding maps to a system change.
*   **Breach response mode (72-hour clock running):** Contain the breach, assess scope (data categories × subjects affected), determine notification obligation (risk of harm to data subjects?), prepare Article 33 DPA notification, prepare Article 34 data subject notification if required, document everything for the Article 33(5) breach register.

## When to Use

Use privacy-engineering when building systems that process personal data and privacy must be embedded in architecture, not documented after the fact.

*   Implementing privacy-by-design: mapping Cavoukian's 7 principles to concrete system properties (data minimization at collection, purpose limitation in API authorization, storage limitation with TTL)
*   Conducting a DPIA: GDPR Article 35 trigger assessment, processing description, necessity/proportionality test, risk identification, mitigation design, DPO sign-off
*   Implementing differential privacy: epsilon selection by query sensitivity, Laplace vs Gaussian mechanism, privacy budget accounting, composition theorems
*   Designing consent management: event-sourced consent with proof chain, per-purpose granularity, withdrawal propagation, CCPA opt-out architecture
*   Building right-to-access and deletion: data inventory graph for subject access requests, deletion cascade across microservices, 30-day SLA tracking
*   Evaluating cross-border transfers: SCC module selection, transfer impact assessment, supplementary measures, DPF certification requirements
*   Exploring privacy-preserving tech: homomorphic encryption readiness, federated learning architecture, ZKP for identity, private set intersection
*   Automating data retention: category-based retention schedules, TTL policy enforcement, automated deletion with audit trail
*   Responding to personal data breaches: 72-hour DPA notification, Article 33/34 requirements, data subject risk-of-harm decision tree

Do NOT use privacy-engineering for GDPR legal interpretation (route to gdpr-privacy or legal-advisor). Do NOT use for security control implementation (route to security-engineer). Do NOT use for encryption algorithm selection (route to cryptography-engineer). Do NOT use for consent banner UX design (route to ui-ux-designer).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.md\|*.docx", "DPIA\|data.protection.impact\|Article.35\|processing.activity")` | DPIA in progress → Go to **Core Workflow: Phase 1 — DPIA** |
| A2 | `file_contains("*.yaml\|*.json", "consent\|purpose\|lawful.basis\|cookie")` | Consent management → Jump to **Decision Trees: Consent Architecture** |
| A3 | `file_contains("*.csv\|*.json", "data.category\|retention\|deletion\|data.inventory")` | Data inventory or retention → Go to **Core Workflow: Phase 2 — Data Inventory & Retention** |
| A4 | `file_contains("*.md\|*.txt", "SCC\|BCR\|transfer.impact\|Schrems\|cross.border\|DPF")` | Cross-border transfer → Jump to **Decision Trees: Cross-Border Transfer** |
| A5 | `file_contains("*.py\|*.sql\|*.java", "epsilon\|differential.privacy\|laplace\|gaussian\|privacy.budget")` | Differential privacy implementation → Jump to **Decision Trees: Differential Privacy** |
| A6 | `file_contains("*.md\|*.txt", "breach\|72.hour\|Article.33\|Article.34\|notification")` | Breach response → Jump to **Decision Trees: Breach Response** |
| A7 | No privacy files found | New privacy engineering → Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What privacy engineering task are you working on?
|-- Conducting a DPIA (GDPR Article 35) -> Start at "Core Workflow: Phase 1"
|-- Building a data inventory and retention policy -> Go to "Core Workflow: Phase 2"
|-- Designing consent management architecture -> Jump to "Decision Trees: Consent Architecture"
|-- Implementing right-to-access and deletion (RTBF) -> Jump to "Decision Trees: Right to Access & Deletion"
|-- Evaluating cross-border data transfers -> Jump to "Decision Trees: Cross-Border Transfer"
|-- Implementing differential privacy -> Jump to "Decision Trees: Differential Privacy"
|-- Responding to a personal data breach -> Jump to "Decision Trees: Breach Response"
|-- Evaluating privacy-preserving technologies -> Jump to "Decision Trees: Privacy-Preserving Tech"
|-- Embedding privacy-by-design from scratch -> Start at "Core Workflow: Phase 1"
```

## Core Workflow

### Phase 1: Data Protection Impact Assessment (DPIA)

Execute in order. Do not skip steps.

```
1. DETERMINE IF DPIA IS REQUIRED (Article 35 Trigger Assessment)
   |-- DPIA is legally required when processing is likely to result in HIGH RISK to individuals:
   |   |-- Systematic and extensive profiling with legal/significant effects
   |   |-- Large-scale processing of special category data (health, biometric, political, religious)
   |   |-- Systematic monitoring of publicly accessible areas (CCTV at scale)
   |   |-- Processing of data relating to criminal convictions and offenses
   |   |-- Use of new technologies (AI/ML, IoT, facial recognition) at scale
   |   |-- Combining datasets from multiple sources beyond reasonable expectations
   |   |-- Processing vulnerable person data (children, employees, patients)
   |-- If none of these triggers apply → document why DPIA is not required, proceed without DPIA
   |-- If any trigger applies → DPIA is mandatory, proceed to step 2

2. DESCRIBE THE PROCESSING (Systematic Description)
   |-- Nature: what data, how collected, how stored, how processed, who accesses
   |-- Scope: volume of data subjects, duration, frequency, geographical extent
   |-- Context: relationship between controller and data subjects, control level, prior expectations
   |-- Purposes: specific, explicit, legitimate purposes for each processing operation
   |-- Technical overview: architecture diagram, data flow, integrations, third parties
   |-- Data lifecycle: collection → processing → storage → sharing → archiving → deletion

3. ASSESS NECESSITY AND PROPORTIONALITY
   |-- Necessity: Is this processing the least intrusive way to achieve the purpose?
   |   |-- Can the purpose be achieved without personal data? (aggregated data, synthetic data)
   |   |-- Can the purpose be achieved with less data? (data minimization review)
   |   |-- Can the purpose be achieved with pseudonymized data instead of identified data?
   |-- Proportionality: Do the benefits justify the privacy intrusion?
   |   |-- List benefits to data subject, controller, and society
   |   |-- Compare intrusion level to benefit magnitude
   |   |-- Document why less intrusive alternatives were rejected
   |-- Lawful basis: Identify specific GDPR Article 6(1) basis for each purpose
   |   |-- Consent, contract, legal obligation, vital interests, public task, legitimate interest
   |   |-- For special category data: Article 9(2) exemption must apply

4. IDENTIFY RISKS TO RIGHTS AND FREEDOMS
   |-- Risk sources: internal threats (employees, contractors), external threats (hackers, third parties)
   |-- Risk categories per data subject:
   |   |-- Physical harm (stalking, doxxing, violence)
   |   |-- Financial harm (identity theft, fraud, discrimination in lending)
   |   |-- Reputational harm (social scoring, public exposure of private facts)
   |   |-- Psychological harm (distress from surveillance, loss of autonomy)
   |   |-- Discrimination (employment, housing, insurance decisions)
   |-- Rate each risk: Likelihood (1-5) × Impact (1-5) = Risk Score (1-25)
   |-- Residual risk = inherent risk - control effectiveness

5. DESIGN MITIGATION MEASURES
   |-- For each risk with residual score > 6, design specific mitigation:
   |   |-- Organizational: policies, training, access controls, NDAs, audits
   |   |-- Technical: encryption, pseudonymization, access logging, data masking, DP
   |   |-- Contractual: data processing agreements (DPAs), SCCs, processor obligations
   |-- Recalculate residual risk after mitigation
   |-- If residual risk remains HIGH after mitigation → MANDATORY prior consultation with DPA (Article 36)
   |-- Document each mitigation: what, who implements, by when, how verified

6. CONSULT AND SIGN OFF
   |-- DPO review: Data Protection Officer must be consulted (Article 35(2))
   |-- Stakeholder input: seek views of data subjects or their representatives where appropriate
   |-- Controller sign-off: senior management approval with accountability
   |-- Publish summary: (optional but recommended) transparency builds trust
   |-- Review trigger: DPIA is a living document — review when processing changes significantly or every 3 years
```

### Phase 2: Data Inventory & Retention Automation

```
1. BUILD DATA INVENTORY (GDPR Article 30 — Records of Processing)
   |-- For each data category, document:
   |   |-- Category name (e.g., "customer email", "health metrics", "location history")
   |   |-- Data subjects: customers, employees, visitors, patients, children
   |   |-- Personal data fields: exact schema, not "contact info" but "name, email, phone, address"
   |   |-- Source: collected directly, third-party, inferred/derived, public records
   |   |-- Lawful basis: consent/contract/legal obligation/legitimate interest — per category
   |   |-- Purpose: specific purpose linked to each category (not "business operations")
   |   |-- Retention period: X days/months/years with justification
   |   |-- Storage locations: database tables, S3 buckets, logs, backups, analytics warehouse
   |   |-- Recipients: internal teams, third-party processors, sub-processors, affiliates
   |   |-- Cross-border: countries where data is stored/processed, transfer mechanism
   |-- Output: data inventory as a graph (nodes = data stores, edges = data flows)

2. DEFINE RETENTION SCHEDULES
   |-- Per data category, determine retention period:
   |   |-- Legal requirement: tax records (7 years), employment records (varying by jurisdiction)
   |   |-- Contractual: active account + X years after closure
   |   |-- Business need: analytics data (aggregate after X days, delete raw after Y days)
   |   |-- Consent duration: delete when consent expires or is withdrawn
   |-- Document retention justification for each category
   |-- Flag categories with conflicting retention requirements for legal review

3. IMPLEMENT AUTOMATED DELETION
   |-- TTL-based deletion:
   |   |-- Add `retention_until` or `expires_at` column to every table with personal data
   |   |-- Cron job: DELETE/UPDATE WHERE expires_at < NOW() — runs daily
   |   |-- Partition by retention date for efficient bulk deletion
   |-- Event-based deletion:
   |   |-- Account deletion triggers cascade: user → orders → analytics events → logs
   |   |-- Consent withdrawal triggers deletion of data held under that consent
   |-- Soft-delete pattern:
   |   |-- Stage 1: soft-delete (is_deleted=true, deleted_at=NOW()) — recoverable for 30 days
   |   |-- Stage 2: hard-delete after recovery window — irreversible
   |   |-- Stage 3: backup deletion — documented exception: backups retain up to 90 days
   |-- Audit trail: log every deletion with timestamp, data category, deletion reason, operator/automated

4. HANDLE DELETION EXCEPTIONS
   |-- Backups: document maximum backup retention (e.g., 90 days rolling)
   |-- Logs: justify log retention beyond data retention (security, debugging — must be documented)
   |-- Legal holds: implement litigation hold override preventing deletion
   |-- Archival: if archiving for research/statistics, ensure anonymization or pseudonymization with separated keys
```

## Decision Trees

### Consent Architecture

```
What type of consent are you implementing?
|-- GDPR-standard consent (freely given, specific, informed, unambiguous, withdrawable)
|   |-- Data model: event-sourced consent ledger, not a boolean column
|   |   |-- Each row: {subject_id, purpose_id, consent_version, notice_version, timestamp, proof_hash}
|   |   |-- Proof hash = SHA-256(subject_id + purpose_id + notice_text + timestamp + nonce)
|   |-- Purposes: granular per-purpose consent (marketing != analytics != personalization != sharing)
|   |   |-- No bundling: cannot make service conditional on consent to unrelated purposes
|   |-- Withdrawal: DELETE or mark-withdrawn consent row, propagate to all processors
|   |   |-- Withdrawal must be as easy as giving consent (same interface, same clicks)
|   |   |-- Withdrawal propagation SLA: processors notified within 24 hours
|   |-- Re-consent triggers: new processing purpose, new data recipient, new technology, merger/acquisition
|   |-- Cookie consent (ePrivacy Directive + GDPR):
|   |   |-- Strictly necessary cookies: no consent required (session, CSRF, load balancing)
|   |   |-- All others: prior consent before setting cookie (no pre-ticked, no cookie walls)
|   |   |-- Consent proof: store consent receipt with timestamp for regulatory audit
|-- CCPA opt-out (right to opt out of sale/sharing)
|   |-- "Do Not Sell or Share My Personal Information" link on homepage
|   |-- Global Privacy Control (GPC) signal: honor browser-based opt-out preference
|   |-- Opt-out persistence: respect opt-out for at least 12 months before re-requesting
|   |-- No dark patterns: opt-out cannot require more steps than opt-in
|-- Children's data (COPPA, GDPR Article 8, UK Age Appropriate Design Code)
|   |-- Age verification: gate collection behind age check (not self-declared, use estimation)
|   |-- Under 13 (COPPA): verifiable parental consent required
|   |-- Under 16 (GDPR default, member states may lower to 13): parental consent required
|   |-- Design: highest privacy settings by default, no nudge toward lowering privacy, no profiling
```

### Right to Access & Deletion (RTBF)

```
Subject Access Request (SAR) — GDPR Article 15 / CCPA Right to Know:
|-- Receipt: acknowledge within 24 hours, verify identity before releasing data
|   |-- Identity verification: proportional to data sensitivity (email verification vs government ID)
|   |-- Do NOT collect more data to verify identity than you would normally have
|-- Data collection: query data inventory graph for all data stores containing subject_id
|   |-- Automated: data inventory graph with subject_id index across all stores
|   |-- Scope: user profile, orders, support tickets, analytics events, logs, third-party shares
|   |-- Format: structured, machine-readable (JSON/CSV), portable (Article 20 right to data portability)
|-- Response: within 30 calendar days (extendable to 60 for complex requests — must notify within 30)

Right to Erasure (RTBF) — GDPR Article 17 / CCPA Right to Delete:
|-- Deletion cascade design:
|   |-- Step 1: Identify all data stores containing subject_id
|   |-- Step 2: Order deletion by dependency graph (child records before parent records)
|   |-- Step 3: Soft-delete (is_deleted=true, deleted_at=NOW()) in each store
|   |-- Step 4: Queue hard-delete job with delay (30-day recovery window)
|   |-- Step 5: Notify all downstream processors of deletion (contractual obligation in DPA)
|   |-- Step 6: Log deletion in immutable audit trail
|-- SLA tracking: 30-day timer starts at request receipt, auto-escalate at day 25 if not completed
```

### Cross-Border Transfer

```
Transfer type determination:
|-- EU/EEA -> Adequacy country: data flows freely as if within EEA
|-- EU/EEA -> US (under DPF): verify certification at dataprivacyframework.gov, have SCC fallback
|-- EU/EEA -> All other countries: Requires Article 46 transfer tool
|   |-- Option A: Standard Contractual Clauses (SCCs 2021)
|   |   |-- Module 1: Controller->Controller | Module 2: Controller->Processor
|   |   |-- Module 3: Processor->Processor | Module 4: Processor->Controller
|   |-- Option B: Binding Corporate Rules (BCRs) for intra-group transfers
|   |-- Option C: Approved certification mechanisms, codes of conduct

Transfer Impact Assessment (TIA) — Post-Schrems II:
|-- Step 1: Map the transfer (data, recipient, purpose, country)
|-- Step 2: Assess recipient country surveillance laws (government access, judicial redress)
|-- Step 3: Evaluate if SCCs/BCRs effective given local laws
|-- Step 4: Apply supplementary measures if gaps found
|   |-- Technical: encryption-at-rest with customer-held keys, pseudonymization, split processing
|   |-- Organizational: warrant canary, transparency report
|   |-- If gaps cannot be closed -> transfer cannot proceed
```

### Differential Privacy

```
Epsilon Selection Framework:
|-- Query sensitivity: max change in output from one individual
|   |-- Count queries: sensitivity = 1 | Sum queries: max individual contribution
|-- Epsilon budget:
|   |-- e=0.01: Extremely strong privacy (Census Bureau) | e=0.1: Strong (Apple emoji suggestions)
|   |-- e=1.0: Moderate (typical research) | e=5.0: Weak (aggregate dashboards) | e=10+: Very weak
|-- Mechanism: Laplace (L1 sensitivity, count/sum) | Gaussian (L2, complex composition)
|-- Local vs Global DP: Global = trusted curator, more utility | Local = per-user noise, stronger privacy
```

### Breach Response

```
Personal Data Breach — 72-Hour Clock Running:
|-- T=0: Breach awareness (reasonable suspicion = clock starts)
|-- T=0-12h: Containment + scope assessment (data categories, subjects, root cause type)
|-- T=12-36h: Risk assessment — likelihood x severity of harm to data subjects
|   |-- High risk -> mandatory DPA notification (Art 33) + data subject notification (Art 34)
|   |-- Low risk -> DPA notification only (Art 33)
|-- T=36-60h: Prepare DPA notification (nature, categories, approx subjects, consequences, measures)
|-- T=60-72h: Submit DPA notification; prepare plain-language data subject communication if required
|-- Post-72h: Document in breach register (Art 33(5)), root cause analysis, remediation plan
```

### Privacy-Preserving Technology Evaluation

```
Use case -> Technology mapping:
|-- Aggregate analytics on sensitive data:
|   |-- Differential privacy (first choice) -> Homomorphic encryption (if computation on encrypted data)
|   |-- SMPC (if multi-party computation without sharing inputs)
|-- Identity verification without exposing identity:
|   |-- Zero-Knowledge Proofs: prove attribute (age > 18) without revealing value
|   |-- Private Set Intersection: find common elements across datasets privately
|-- ML on user data without centralization:
|   |-- Federated learning: train on-device, share gradients (add DP noise to gradients)
|   |-- On-device processing: all data stays local, only insights/triggers sent to server
|-- FHE readiness: compute on data you cannot see? Small computation -> PHE/SHE. Complex -> FHE too slow for prod.
```

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| GDPR legal interpretation, data subject complaints, DPA investigation | gdpr-privacy, legal-advisor | Legal advice on GDPR applicability, DPA response strategy, fine negotiation |
| Security control implementation for personal data protection | security-engineer | Encryption at rest/transit, access controls, IAM, network segmentation, vulnerability management |
| Encryption algorithm selection (which cipher, key management strategy) | cryptography-engineer | AES-256 vs ChaCha20, key rotation, HSM integration, TLS configuration |
| Consent banner UI/UX design, cookie preference center, privacy dashboard | ui-ux-designer | User experience, accessibility, dark pattern avoidance, mobile responsiveness |
| IAM integration for privacy controls — who can access PII, access reviews | iam-architect | Role-based access to personal data, attribute-based access for data minimization |
| Data pipeline architecture — where personal data flows, ETL with privacy controls | data-engineer | Data lineage tracking, PII detection in data pipelines, automated data classification |
| Third-party vendor risk assessment — processor due diligence | compliance-officer | Vendor DPAs, SOC 2 reports, ISO 27001 certification review, sub-processor mapping |
| Incident response coordination — security breach may also be privacy breach | incident-responder | Joint incident response, forensic investigation coordination, parallel notification streams |
| AI/ML models trained on personal data — fairness, bias, privacy | ml-ai-engineer | Federated learning architecture, DP-SGD for training, model inversion attack mitigation |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Personal data fields in API responses AND no purpose specification document | [ALERT] Every personal data field requires documented purpose and lawful basis per GDPR Article 5(1)(b). Build purpose specification before collection begins. |
| P2 | Cross-border data flow in architecture diagram AND no SCC/BCR/DPF reference | [ALERT] Personal data crossing jurisdictional boundaries requires a valid transfer mechanism post-Schrems II. Document SCC module, adequacy decision, or DPF certification. |
| P3 | Consent model uses boolean field (consented=true/false) instead of event-sourced ledger | [WARN] Boolean consent cannot prove what was consented to, when, under which notice. Replace with event-sourced consent model: {subject_id, purpose_id, version, timestamp, proof_hash}. |
| P4 | Retention policy missing AND personal data stored beyond 24 months | [ALERT] Undefined retention violates GDPR Article 5(1)(e) storage limitation principle. Define retention period per data category with documented justification. |
| P5 | Production access logs show PII in plaintext (emails, names, SSNs in log messages) | [ALERT] PII in logs violates data minimization and creates unnecessary breach exposure. Implement log scrubbing: hash/mask PII before logging. |
| P6 | Third-party data sharing AND no Data Processing Agreement (DPA) on file | [ALERT] GDPR Article 28 requires a DPA with every processor. Without a DPA, the data sharing is unlawful. Request DPA or suspend sharing. |

## What Good Looks Like

```
Architecture:                                      Privacy Controls Mapped:
  ┌──────────┐  ┌──────────┐  ┌──────────┐         Consent: Event-sourced ledger
  │ Collection│─>│Processing│─>│ Storage  │         with cryptographic proof chain
  │ Layer    │  │ Layer    │  │ Layer    │         and per-purpose granularity.
  └──────────┘  └──────────┘  └──────────┘
      │             │              │               Retention: TTL column on every
      │   Privacy   │   Privacy    │               table. Cron deletes expired rows.
      ▼   Gate ▼    ▼   Gate ▼    ▼               Soft-delete -> 30d -> hard-delete.
  ┌──────────────────────────────────┐
  │     Data Inventory Graph         │              DPIA: Living document. Updated
  │  (nodes = stores, edges = flows) │              per major release. Risk scores
  └──────────────────────────────────┘              with named mitigations + owners.
      │
      ▼                                            SAR: Automated. Data inventory
  ┌──────────┐  ┌──────────┐  ┌──────────┐         graph powers subject access.
  │ Retention│  │ Consent  │  │ Breach   │         <5 days is target SLA.
  │ Engine   │  │ Engine   │  │ Response │
  └──────────┘  └──────────┘  └──────────┘         Breach: 72h clock documented.
                                                   Playbook tested quarterly.
  Result: Privacy is enforceable in code. Every
  requirement traces to a system property. Audit
  ready at any moment. Zero dark patterns.
```

## Deliberate Practice

```
Scenario 1: Healthcare startup collects patient vitals via wearable + stores in AWS US-East-1.
EU patients included. No DPIA done. Consent is a checkbox on signup.
You inherit this system.
  Week 1: DPIA trigger assessment -> Article 35 applies (health data, systematic monitoring).
        Build data inventory. Find 17 data stores with PII, no retention policy.
  Week 2: Consent redesign: event-sourced ledger, per-purpose (treatment vs research vs marketing).
        Cross-border: EU-US transfer needs SCC Module 2 + TIA + supplementary measures.
  Week 3: Retention: add expires_at columns, cron jobs, 30d soft-delete window.
        SAR automation: build subject_id index across all stores.
  Week 4: Breach playbook: define roles, notification templates, test with tabletop exercise.
        DPA prior consultation (Article 36) if residual risk remains high.

Scenario 2: E-commerce platform wants "anonymized" analytics shared with advertisers.
Current approach: hash(email) and call it anonymized. You must correct this.
  Day 1: Explain hash(email) IS pseudonymization, not anonymization. Reversible via rainbow table.
  Day 2: Propose differential privacy: count queries with epsilon=1.0, Laplace mechanism.
        Privacy budget: 10 queries/day, total epsilon budget = 10.0/month.
  Day 3: Alternative: k-anonymity with k>=5 on demographic attributes, plus l-diversity on sensitive.
  Day 4: Implement: replace raw data export with DP query interface. Advertisers query aggregates only.
```

## Gotchas -- Highest-Value Content

### DPIA Gotchas

*   **Treating the DPIA as a one-time document.** A DPIA written for system v1.0 is useless for v3.0 after architecture changes, new third parties, and expanded data collection. Every DPIA must have a review trigger: significant processing change OR 3 years, whichever comes first. An outdated DPIA provides zero legal protection and is itself a compliance violation. **Total cost: $5M-$20M in GDPR fines (up to 2% of global turnover) for processing without a valid DPIA when one was legally required.**

*   **Skipping prior consultation when residual risk remains high.** Article 36 requires mandatory consultation with the DPA when the DPIA indicates high residual risk that the controller cannot mitigate. Proceeding without consultation is a separate violation from the underlying risk. The DPA can impose a temporary or permanent processing ban. **Total cost: $2M-$10M in fines + potential processing ban costing $500K-$5M/month in lost revenue.**

*   **Not consulting the DPO.** GDPR Article 35(2) mandates DPO consultation during the DPIA process. A DPIA signed off without DPO input is procedurally invalid. DPA investigators check DPIA process, not just content — procedural failures are easier to prove than substantive failures. **Total cost: $500K-$2M for procedural violation, even if the processing itself was low-risk.**

### Consent Gotchas

*   **Bundling consent so service is conditional on accepting unrelated purposes.** "Accept all or you cannot use the app" is illegal under GDPR. Consent must be granular per purpose. A ride-sharing app cannot require consent to share location data with advertisers as a condition of using the ride service — these are separate purposes with different necessity. **Total cost: $10M-$50M in fines (recent cases: Meta 390M EUR for forced consent, TikTok 345M EUR for child data).**

*   **Storing consent as a boolean with no proof of what was consented to.** A DB column `consented=true` is unprovable to a regulator. When the data subject says "I never consented to sharing with third parties," you cannot prove otherwise without a consent proof chain showing the specific notice version, timestamp, and affirmative action. **Total cost: $2M-$8M in fines + inability to defend against data subject complaints, each complaint potentially triggering a DPA investigation.**

### Deletion Gotchas

*   **Forgetting that backups are personal data too.** You delete the production row on day 30. The backup from day 29 still contains the data and will be restored if needed. GDPR right to erasure extends to backups. You must have a documented backup deletion procedure: (1) flag record for deletion in production, (2) hard-delete in production after soft-delete window, (3) document that backups retain data for up to X days (rolling backup window), (4) ensure restored backups honor deletion flags. **Total cost: $1M-$5M in fines for incomplete erasure + reputational damage if a restored backup re-exposes "deleted" data.**

*   **Cascade failures in microservice deletions.** User deletion triggers 15 downstream services. Service #7 times out. Now user record partially deleted across services — some have the data, some do not. GDPR erasure requires complete deletion. Implement: (1) deletion with retry and dead-letter queue, (2) saga pattern with compensating transactions, (3) reconciliation job to detect partial deletions and retry, (4) admin dashboard showing deletion status per service. **Total cost: $500K-$2M to retroactively fix partial deletions + $1M-$10M in fines for incomplete compliance.**

### Cross-Border Transfer Gotchas

*   **Assuming SCCs are sufficient without a TIA.** Post-Schrems II, SCCs alone are not sufficient. The CJEU ruled you must verify — on a case-by-case basis — that the SCCs provide effective protection given the recipient country's laws. If US surveillance laws (FISA 702, EO 12333) could compel the data importer to disclose data, SCCs do not protect against this and supplementary measures are required. **Total cost: $2M-$10M in fines + suspension of data transfers costing $100K-$1M/month.**

*   **Forgetting that EU representatives need a transfer mechanism too.** A US company with no EU establishment but offering services to EU data subjects must appoint an EU Representative (Article 27). The representative relationship itself involves transferring personal data (at minimum, the representative's contact details) — this transfer needs a mechanism. **Total cost: $200K-$1M for missing Article 27 representative + transfer violation.**

### Breach Response Gotchas

*   **Waiting for "confirmed" root cause before starting the 72-hour clock.** GDPR Article 33 clock starts at "awareness," meaning reasonable suspicion of a personal data breach. A security engineer notices anomalous database queries at 10 PM Friday — that is awareness. Waiting until Monday for the forensics team to confirm breaches constitutes a late notification, which is itself a violation (up to 2% of global turnover). **Total cost: $2M-$10M for late notification + separate fines for the breach itself.**

*   **Notifying data subjects with vague, unhelpful information.** "Your data may have been involved in a security incident. We take your privacy seriously." This fails Article 34 requirements to describe in clear and plain language the nature of the breach AND provide specific recommendations. Regulators increasingly penalize vague breach notices. **Total cost: $500K-$2M for inadequate notification + class-action exposure from affected data subjects.**

## Verification

After implementing privacy controls, run this sequence. Do not proceed past a failure.

1.  **Lawful basis check:** Every personal data category has documented lawful basis (GDPR Article 6) and specified purpose. Verify by auditing data model against purpose specification document. No orphan data fields.
2.  **DPIA completeness:** If DPIA is required, verify it contains all 6 elements: processing description, necessity/proportionality assessment, risk identification, mitigation measures, DPO consultation, sign-off. DPIA dated within last 3 years or after last major system change.
3.  **Consent audit:** Consent records are event-sourced with proof hash. Each purpose has separate consent. Withdrawal mechanism exists and propagates to processors within 24h SLA.
4.  **Retention enforcement:** Every table with personal data has `expires_at` or equivalent TTL. Automated deletion job runs daily. Deletion audit trail exists. Backup retention policy is documented.
5.  **Cross-border audit:** Every cross-border data flow has documented transfer mechanism (SCC module, adequacy decision, BCR, or DPF). TIA completed within last 12 months. Supplementary measures documented where TIA identified gaps.
6.  **SAR readiness:** Data inventory graph covers all data stores. Subject access can be completed within 30 days. Test with a dummy subject access request — time from request to delivery.
7.  **Breach playbook:** Documented breach response procedure with roles, notification templates, 72-hour clock process, Article 33/34 content requirements. Tested in tabletop exercise within last 6 months.

If any check fails: diagnose from checklist, provide specific actionable fix, restart verification from failed item.

## References

*   [ICO: Guide to Data Protection Impact Assessments](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments/) — UK ICO DPIA guidance with examples and templates
*   [EDPB Guidelines 4/2019 on Data Protection by Design and by Default](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42019-article-25-data-protection-design-and_en) — Article 25 PbD obligations
*   [European Commission: Standard Contractual Clauses](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) — SCCs 2021 modules and implementation guidance
*   [NIST Privacy Framework](https://www.nist.gov/privacy-framework) — Enterprise privacy risk management aligned with NIST CSF
*   [Differential Privacy by Cynthia Dwork and Aaron Roth](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) — Foundational text on DP algorithms and composition
*   [/references/privacy-by-design-principles.md](references/privacy-by-design-principles.md) — Cavoukian's 7 principles mapped to system architecture
*   [/references/dpia-methodology.md](references/dpia-methodology.md) — Full DPIA template with risk scoring and mitigation tracking
*   [/references/differential-privacy.md](references/differential-privacy.md) — Epsilon selection, Laplace/Gaussian mechanisms, budget accounting
*   [/references/consent-management.md](references/consent-management.md) — Event-sourced consent architecture with proof chain implementation
*   [/references/right-to-access-deletion.md](references/right-to-access-deletion.md) — SAR and RTBF implementation patterns, deletion cascade
*   [/references/cross-border-transfers.md](references/cross-border-transfers.md) — SCC module selection, TIA methodology, supplementary measures
*   [/references/privacy-preserving-tech.md](references/privacy-preserving-tech.md) — HE, SMPC, ZKP, FL decision framework and readiness assessment
*   [/references/data-retention-automation.md](references/data-retention-automation.md) — TTL-based deletion, retention schedule templates, audit trail
*   [/scripts/verify-skill.sh](scripts/verify-skill.sh) — Verify all 14 required sections, ground rules, decision trees, gotchas, and references
