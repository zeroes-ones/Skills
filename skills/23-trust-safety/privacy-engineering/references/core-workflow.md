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
