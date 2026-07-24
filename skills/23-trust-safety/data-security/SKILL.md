---
name: data-security-engineer
description: >
  Use when designing data classification schemas, implementing data loss prevention (DLP),
  configuring encryption at rest/transit/use, building data masking and tokenization pipelines,
  securing databases and data warehouses, planning data retention and disposal, conducting
  sensitive data discovery, handling cross-border data transfers (Schrems II, EU-US DPF),
  or implementing data access auditing. Handles data protection engineering (classification,
  encryption, masking, DLP), cryptographic controls for data (KMS hierarchy, envelope encryption,
  TLS 1.3), data lifecycle management (retention, disposal, crypto-shredding), database hardening
  (TDE, column-level encryption, RLS, audit logging), PCI DSS 4.0 data requirements (tokenization,
  CDE scoping, never store CVV), HIPAA PHI protection (encryption, access controls, BAA requirements),
  GDPR data minimization and storage limitation, and CCPA data rights implementation. Do NOT use for
  network security (use security-engineer), application security (use security-reviewer), identity
  and access management (use security-engineer), cloud infrastructure security (use cloud-architect),
  compliance program design (use compliance-officer), or privacy program management (use privacy-engineer).
author: Sandeep Kumar Penchala
license: MIT
compatible_with:
  - security-engineer
  - compliance-officer
  - privacy-engineer
  - cloud-architect
  - backend-developer
  - devops-engineer
  - fullstack-developer
  - qa-engineer
  - incident-responder
  - database-designer
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - WebFetch
  - Task
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: security
status: stable
version: 1.0.0
updated: 2025-12-02
tags:
  - security
  - data-security
  - dlp
  - encryption
  - masking
  - tokenization
  - data-classification
  - database-hardening
  - pci-dss
  - hipaa
  - gdpr
  - sensitive-data
  - audit
token_budget: 3200
chain:
  consumes_from:
    - security-engineer
    - compliance-officer
    - cloud-architect
    - database-designer
    - backend-developer
  feeds_into:
    - security-engineer
    - compliance-officer
    - backend-developer
    - devops-engineer
    - cloud-architect
    - database-designer
    - incident-responder
---

# Data Security Engineer — Portability Target

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design, implement, and validate data protection controls across structured and unstructured data stores.
This skill covers data classification, DLP architecture, encryption strategy, data masking and tokenization,
database hardening, cross-border data transfer compliance, and sensitive data discovery.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|----------------|---------|
| "We don't have sensitive data worth protecting." | Every organization has PII, financial data, or business-critical IP. 83% of organizations have experienced multiple breaches. Assume you are a target — the question is when, not if. |
| "The cloud provider encrypts everything by default." | Provider-managed encryption protects against physical theft only. It does not protect against insider threats, compromised credentials, or multi-tenant isolation failures. Customer-managed keys (CMK) are required for CONFIDENTIAL+ data. |
| "We'll classify data later — let's ship first." | Data that accumulates unlabeled for years costs 10x more to classify retroactively. Without classification during a breach, you must assume ALL data is exposed, ballooning notification costs to $500K–$4M. Classify at creation time. |
| "Our DLP is in monitor-only mode for now." | DLP in eternal monitor-only mode is security theater. Every exfiltration is recorded but none are stopped. If monitor-only exceeds 30 days, executive sign-off is required. Deploy in phases: 14 days baseline, then enable blocking at <10% FPR. |
| "Encryption will kill our database performance." | AES-NI makes AES-256-GCM overhead <3% on modern hardware. Encrypt first, benchmark second. The performance cost of a data breach ($4.45M average) vastly exceeds any encryption overhead. |

## Ground Rules — Read Before Anything Else

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|--------------------|--------------------|
| **R1** | **REFUSE to bypass data classification for performance.** Every data field must be classified before protection controls are applied. | Trigger: grep for data export patterns with no corresponding classification metadata file | REFUSE. Respond: "Data classification must precede protection. Before I design controls, I need: (1) What data types exist? (2) Where does each type live? (3) What is the sensitivity tier for each? Run Phase 1: Data Discovery & Classification first." |
| **R2** | **DETECT — All data protection MUST start with data discovery and classification.** You cannot protect what you do not know exists. Shadow data is the #1 source of preventable breaches. | Trigger: request asks for encryption or DLP implementation but no data inventory exists | WARN: "Data discovery has not been performed. Run an automated scan for sensitive data across all data stores first. Estimated uncovered data stores: 30-40%." |
| **R3** | **STOP — Never implement encryption without key management.** Encryption with co-located keys is cryptographic theater. KMS MUST be configured first. | Trigger: encryption code detected but no KMS infrastructure found | STOP. Respond: "Encryption code detected without KMS infrastructure. Implement envelope encryption (DEK → KEK → Master Key → HSM) before encrypting any data." |
| **R4** | **REFUSE — Production data MUST NOT be used in non-production environments.** Production PII/PHI/PCI in dev/test/staging constitutes an unauthorized disclosure. | Trigger: production data detected in non-production context | REFUSE. Respond: "Production data detected in non-production context. This violates GDPR, HIPAA, and PCI DSS. Implement static data masking pipeline first." |
| **R5** | **DETECT — Cross-border data transfers MUST have documented legal basis.** Post-Schrems II, transferring EU personal data without SCCs + TIA is unlawful. | Trigger: EU data flowing to non-EU infrastructure without legal documentation | WARN: "Cross-border data transfer detected without documented legal mechanism. Under GDPR Chapter V, transfers require adequacy decision, SCCs + TIA, or BCRs." |
| **R6** | **STOP — Never disable audit logging for sensitive data access.** Without audit trails, a data breach is undetectable and uncontainable. | Trigger: audit logging disabled on sensitive databases | STOP. Respond: "Audit logging is disabled. Enable pgaudit/MySQL audit/SQL Server Audit for all sensitive data access. Forward to SIEM with real-time alerting." |
| **R7** | **REFUSE — Data minimization is NOT optional.** Collecting data "just in case" violates GDPR Art. 5(1)(c), increases breach impact, and multiplies DSAR costs. | Trigger: wide-open schema designs for user/profile tables without minimization documentation | REFUSE. Respond: "Schema design lacks data minimization. GDPR requires personal data to be adequate, relevant, and limited. Remove unnecessary fields before protecting them." |

## The Expert's Mindset

Data security is not a feature to bolt on after the breach. It is an architectural property, like structural integrity in a building.

| Cognitive Bias | How It Manifests | Antidote |
|---|---|---|
| **Optimism bias** — "Our data isn't that sensitive" | Teams classify everything as INTERNAL to avoid overhead | Assume every data store will be breached. Classify based on worst-case exposure impact. |
| **Availability heuristic** — "We've never had a data breach" | Past safety confused with future safety | The question is not whether a breach will occur, but when. 83% of organizations have multiple breaches. |
| **Tooling illusion** — "We use cloud, so our data is secure" | Cloud defaults mistaken for comprehensive protection | Provider-managed encryption protects against physical theft only. CMK needed for Confidential+ data. |
| **Friction aversion** — "Encryption will slow queries too much" | Teams avoid encryption without measuring overhead | AES-NI makes AES-256-GCM overhead <3%. Encrypt first, benchmark second. |
| **Classification procrastination** — "We'll classify later" | Data accumulates unlabeled for years | Classify at creation time. 5 minutes now vs. 5 months of remediation later. |

**Every data field is a liability until proven otherwise.** The default stance: this field contains sensitive data.

**The adversary only needs one unprotected data store.** Defense-in-depth: classification, access control, encryption, DLP, audit logging, alerting. Each layer must fail independently.

**Compliance ≠ security.** PCI DSS means you passed an audit. Build to the threat model, not the checklist.

## Operating at Different Levels

| Level | Name | Time Budget | Scope | Output |
|---|---|---|---|---|
| **L1** | Quick Review | 5-15 min | Single table, single concern | Specific recommendation (e.g., "This column needs AES-256-GCM with KMS-managed key") |
| **L2** | Standard Audit | 30-90 min | Database or service, data flow audit | Audit report with classification gaps, encryption gaps, DLP coverage gaps |
| **L3** | Deep Assessment | 2-6 hours | Full data estate | Comprehensive data protection strategy with all artifacts |
| **L4** | Incident Response | Until resolved | Breach containment, forensics, notification | Incident timeline, exposed data inventory, root cause analysis |

## When to Use

| Trigger | Action | Cross-Skill |
|---|---|---|
| New database schema with PII fields | Classify each field, apply column-level encryption, add audit logging | database-designer, security-engineer |
| DLP rule design for data exfiltration prevention | Design rules at network, endpoint, email, cloud layers | security-engineer, devops-engineer |
| Encryption key management architecture design | Design KMS hierarchy (DEK, KEK, Master Key, HSM) | cloud-architect, devops-engineer |
| Data masking pipeline for non-production | Design static/dynamic masking, tokenization, synthetic data | database-designer, qa-engineer |
| Database hardening | Apply CIS benchmarks, disable dangerous functions | database-designer, security-engineer |
| PCI DSS 4.0 data requirements | Tokenize PAN, scope CDE, implement key management | compliance-officer, security-engineer |
| HIPAA PHI protection design | Encrypt ePHI, implement access controls, ensure BAA coverage | compliance-officer, security-engineer |
| Cross-border data transfer compliance | Conduct TIA, implement SCCs, apply supplementary measures | privacy-engineer, compliance-officer |
| Data retention and disposal policy design | Define retention schedules, implement TTL deletion | compliance-officer, database-designer |
| Sensitive data discovery | Run automated scanners, build data catalog | cloud-architect, security-engineer |
| Encryption at rest implementation | AES-256-GCM envelope encryption, integrate with KMS | cloud-architect, backend-developer |
| Audit trail design for sensitive data access | Design audit log schema, forward to SIEM | security-engineer, devops-engineer |
| Data anonymization for analytics | k-anonymity, differential privacy with epsilon budget | privacy-engineer, data-scientist |
| Data warehouse/lake security | RBAC, column-level security, audit logging | cloud-architect, data-engineer |
| Tokenization of sensitive fields | Design token vault, format-preserving tokenization | backend-developer, database-designer |
| Data disposal and crypto-shredding | NIST 800-88 purge/clear/destroy | cloud-architect, devops-engineer |
| Third-party data access security review | Review vendor data handling, verify DPA coverage | compliance-officer, privacy-engineer |
| Secrets management for database credentials | Vault/KMS/Secrets Manager, rotate credentials | devops-engineer, security-engineer |

## Route the Request

| # | Detect Condition | Route To | Intent Route Fallback |
|---|-----------------|----------|----------------------|
| **A1** | file_contains("*.sql", "CREATE TABLE.*password|CREATE TABLE.*ssn|CREATE TABLE.*credit") or file_contains("*.tf", "aws_db_instance|google_sql_database|azurerm_mssql") | Core Workflow → Phase 1 (Data Discovery & Classification) | "I detect sensitive data schemas or database infrastructure — routing to Data Discovery & Classification phase." |
| **A2** | file_contains("*.py|*.js|*.go", "AES|encrypt|decrypt|crypto|cipher") and not file_exists("kms-policy/|key-policy/") | Core Workflow → Phase 2 (Protection Design — Encryption Strategy) | "I detect encryption code without KMS policy — routing to Protection Design phase for key management architecture." |
| **A3** | file_contains("*.tf", "aws_kms|google_kms|azurerm_key_vault") or file_contains("docker-compose.yml", "vault") | Core Workflow → Phase 2 (Protection Design — Key Management) | "I detect KMS/Vault infrastructure — routing to Key Management architecture." |
| **A4** | file_contains("*.py|*.sql", "SELECT *|COPY.*TO|pg_dump|mysqldump") and file_contains("*.tf", "s3_bucket|google_storage|azurerm_storage") | Decision Trees → DLP Architecture | "I detect data export patterns + cloud storage — routing to DLP Architecture decision tree." |
| **A5** | file_contains("*.md|*.txt", "GDPR|Schrems.II|cross.border|data.transfer|SCC|DPF") | Decision Trees → Cross-Border Data Transfer | "I detect cross-border transfer references — routing to Cross-Border Data Transfer decision tree." |
| **A6** | file_contains("*.md|*.txt", "PCI|PCI.DSS|cardholder|PAN|CHD") or file_contains("*.py", "credit_card|card_number|luhn") | Decision Trees → Data Classification (PCI branch) | "I detect PCI DSS/cardholder data references — routing to PCI data classification and protection." |
| **A7** | file_contains("*.md|*.txt", "HIPAA|PHI|ePHI|BAA|covered.entity") | Decision Trees → Data Classification (PHI branch) | "I detect HIPAA/PHI references — routing to healthcare data classification and protection." |
| **A8** | file_contains("*.sql", "DROP|DELETE|TRUNCATE") and file_contains("*.md", "retention|disposal|purge") | Decision Trees → Data Retention & Disposal | "I detect data deletion + retention references — routing to Data Retention & Disposal decision tree." |

### Intent Route (Ask the User)

```
What are you trying to do?
├── CLASSIFY data across your data estate → Jump to Decision Trees → Data Classification
├── PREVENT data loss with DLP → Go to Decision Trees → DLP Architecture
├── ENCRYPT data at rest, in transit, or in use → Go to Decision Trees → Encryption Strategy
├── MASK or TOKENIZE sensitive data for non-production → Go to Decision Trees → Data Classification
├── SECURE a database or data warehouse → Jump to Core Workflow → Phase 3
├── HANDLE cross-border data transfer compliance → Go to Decision Trees → Cross-Border Data Transfer
├── DESIGN data retention and disposal policies → Go to Decision Trees → Data Retention & Disposal
├── DISCOVER sensitive data across the organization → Jump to Core Workflow → Phase 1
├── IMPLEMENT PCI DSS data requirements → Go to Decision Trees → Data Classification
└── RESPOND to a data breach involving exposed sensitive data → Invoke incident-responder skill first
```

## Core Workflow

Execute these phases in order. Each phase gates the next.

**Phase 1: Data Discovery & Classification (~30 min)**
1. Run automated sensitive data discovery across all data stores
2. Scan schemas for PII patterns, credential leaks
3. Build classification taxonomy: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
4. Assign classification labels to every data store and sensitive column
5. Identify data owners and map data flows
6. **Output:** Data classification matrix, data flow diagram, shadow data report

**Phase 2: Protection Design (~60 min)**
1. Select encryption approach per threat model: at rest (AES-256-GCM), in transit (TLS 1.3), in use (app-level)
2. Design DLP rules based on classification tiers
3. Define masking/tokenization strategy for non-production
4. Design key management hierarchy and rotation schedule
5. **Output:** Protection architecture document, DLP rule set, KMS configuration

**Phase 3: Implementation & Hardening (~90 min)**
1. Apply database hardening per CIS Benchmarks
2. Configure DLP policies at each layer
3. Implement column-level encryption for PII/PHI/PCI fields
4. Set up audit logging with structured format
5. Configure SIEM forwarding with real-time alerting
6. **Output:** Hardened configurations, deployed DLP policies, audit log pipeline

**Phase 4: Validation & Testing (~45 min)**
1. Test DLP rules with sample sensitive data
2. Verify encryption at storage layer
3. Validate data masking in non-production
4. Penetration test data access controls
5. Verify audit logs appear in SIEM
6. **Output:** Test results report, gap analysis, remediation tickets

**Phase 5: Monitoring & Response (~30 min)**
1. Configure DLP alerts with severity tiers
2. Set up audit log aggregation
3. Define data breach response playbook
4. Schedule recurring data discovery scans
5. Configure automated compliance reporting
6. **Output:** Alert configurations, incident response runbook, scan schedule

## Decision Trees

### Data Classification Decision

```
Sensitive data field detected
│
├─ Contains payment card data? (PAN, track data, CVV, PIN)
│  ├─ YES → Apply PCI DSS 4.0 controls
│  │        ├─ Tokenize PAN immediately (vault or format-preserving)
│  │        ├─ NEVER store CVV post-authorization (Req 3.2)
│  │        ├─ Encrypt stored PAN with AES-256-GCM + KMS-managed DEK
│  │        ├─ Scope entire environment into CDE
│  │        └─ Quarterly ASV scans, annual pentest (Req 11.4)
│  └─ NO → Continue
│
├─ Contains protected health information? (18 HIPAA identifiers + health data)
│  ├─ YES → Apply HIPAA Security Rule
│  │        ├─ Encrypt ePHI at rest (AES-256) and in transit (TLS 1.3)
│  │        ├─ Unique user IDs + emergency access procedure + auto logoff
│  │        ├─ Audit controls on all ePHI access (read + write)
│  │        ├─ Transmission security (addressable but de facto required)
│  │        └─ Ensure BAA coverage from all vendors touching ePHI
│  └─ NO → Continue
│
├─ Contains PII subject to GDPR?
│  ├─ YES → Apply GDPR data protection
│  │        ├─ Data minimization: collect only what is necessary (Art. 5(1)(c))
│  │        ├─ Storage limitation: define and enforce retention period
│  │        ├─ Encryption + pseudonymization as technical measures (Art. 32)
│  │        ├─ DSAR pipeline: 30-day SLA, machine-readable export, cascade deletion
│  │        └─ Data transfer: SCCs + TIA for any non-adequate country
│  └─ NO → Continue
│
├─ Contains internal business data (financials, trade secrets, source code)?
│  ├─ YES → CONFIDENTIAL tier
│  │        ├─ Encryption at rest: mandatory (AES-256-GCM)
│  │        ├─ Encryption in transit: mandatory (TLS 1.2+)
│  │        ├─ Access: RBAC with least privilege, quarterly access review
│  │        └─ Audit: log all writes and admin reads
│  └─ NO → INTERNAL or PUBLIC tier
│           ├─ INTERNAL: authenticated access, encryption recommended
│           └─ PUBLIC: open access, no encryption required
```

### Encryption Strategy Decision

```
Data protection requirement
│
├─ Full database encryption needed?
│  └─ YES → Transparent Data Encryption (TDE)
│           ├─ PostgreSQL: pg_tde extension or filesystem-level (LUKS/dm-crypt)
│           ├─ MySQL: InnoDB tablespace encryption with keyring plugin
│           ├─ SQL Server: TDE with Azure Key Vault / EKM provider
│           ├─ Oracle: TDE with external HSM (SafeNet/Thales)
│           └─ Key: single DEK per database, rotated annually
│
├─ Specific columns (PII/PHI/PCI) need encryption?
│  └─ YES → Column-Level Encryption
│           ├─ Deterministic: AES-256-SIV for equality lookups (email, SSN)
│           ├─ Randomized: AES-256-GCM + random IV for storage-only (no lookup needed)
│           └─ Always Encrypted: client-side encryption, DB never sees plaintext
│
├─ Payment card data in scope (PCI DSS)?
│  └─ YES → Tokenization (NOT encryption for PCI compliance preference)
│           ├─ Vault-based: store token in CDE, map to PAN in isolated vault
│           ├─ Vaultless: format-preserving encryption (FF1 mode) with KMS
│           └─ Principle: the CDE should never hold both token AND decryption key
│
├─ Search/analytics needed on encrypted data?
│  └─ YES → Application-Level Encryption with Blind Indexing
│           ├─ Exact match: HMAC(sensitive_field) as searchable index
│           ├─ Range queries: order-revealing encryption (HIGH RISK — escrow to DBA approval)
│           └─ Computation: homomorphic encryption (performance cost: 1,000x-1,000,000x)
│
└─ Key Management Hierarchy
   ├─ Root KMS: AWS KMS / GCP Cloud KMS / Azure Key Vault / HashiCorp Vault (HSM-backed)
   ├─ Master Key (KEK): generated by KMS, encrypts DEKs, rotated annually
   ├─ Data Encryption Key (DEK): per-database or per-table, rotated quarterly
   └─ Audit: log every key access, enforce separation of duties
```

### DLP Architecture Decision

```
DLP deployment strategy selection
│
├─ Need to block data exfiltration in real time?
│  └─ YES → Network DLP (inline/proxy mode)
│           ├─ Deploy at: CASB, SWG, email gateway, API gateway
│           ├─ Inspects: HTTP body, file uploads, email attachments, API responses
│           ├─ Blocks on: SSN pattern + proximity keywords ("payroll", "employee")
│           ├─ Limitation: TLS inspection requires MITM (legal review + perf impact)
│           └─ Tooling: Microsoft Purview, Netskope, Zscaler, Forcepoint
│
├─ Need to prevent data from leaving endpoints?
│  └─ YES → Endpoint DLP
│           ├─ Monitors: local drives, USB, clipboard, print, screenshot, browser upload
│           ├─ Blocks: copy to USB, upload to personal cloud, print with sensitive content
│           ├─ Discovers: shadow data (prod snapshots, unencrypted PII on laptop)
│           └─ Tooling: Microsoft Purview Endpoint DLP, Digital Guardian, Trellix
│
├─ Need to discover exposed data in cloud storage?
│  └─ YES → Cloud DLP (API-based discovery)
│           ├─ AWS: Macie (S3 scanning + ML classification)
│           ├─ GCP: Cloud DLP API (inspection jobs + risk analysis + de-identification)
│           ├─ Azure: Purview Information Protection (sensitivity labels + auto-labeling)
│           └─ Limitation: API rate limits. 100TB+ scans = days. Plan accordingly.
│
├─ Need to monitor/audit database queries?
│  └─ YES → Database Activity Monitoring (DAM)
│           ├─ Detects: mass SELECT on PII tables, unauthorized DDL, SQL injection in logs
│           ├─ Alerts on: `SELECT * FROM users` by service account, `DROP TABLE patients`
│           └─ Tooling: Imperva SecureSphere, IBM Guardium, AWS RDS Enhanced Monitoring
│
└─ Integration: All DLP layers → SIEM (Splunk/Elastic/Sumo Logic)
   └─ Correlation rule: Endpoint DLP alert + Network DLP alert within 5 min → INCIDENT
```

### Data Masking & Tokenization Decision

```
Data protection for non-production / analytics
│
├─ Need to use production-like data in non-production environments?
│  └─ YES → Static Data Masking
│           ├─ Irreversible masking (SHA-256 + salt) for fields that must not be reversible
│           ├─ Format-preserving masking for fields with format constraints (email, phone)
│           ├─ Substitution: replace with realistic fake data from lookup tables
│           ├─ Shuffling: permute column values within a table (preserves distribution)
│           └─ Tooling: Delphix, IBM Optim, Informatica Persistent Data Masking
│
├─ Need to retain referential integrity while masking?
│  └─ YES → Consistent Masking
│           ├─ Same input value → same masked value across all tables/databases
│           ├─ Use HMAC(key, original_value) truncated to format constraints
│           └─ Key stored in KMS, separate from masking pipeline
│
├─ Need to query production data without exposing raw values?
│  └─ YES → Dynamic Data Masking
│           ├─ SQL Server: Dynamic Data Masking (built-in, 4 mask types: default, email, random, custom)
│           ├─ PostgreSQL: pg_ddm extension or RLS + views
│           ├─ Application-level: intercept result set at ORM/API layer
│           └─ Limitation: masking at DB layer can be bypassed by users with elevated privileges
│
├─ Need to permanently de-identify PII for analytics?
│  └─ YES → Tokenization
│           ├─ Vault-based: generate random token → store token-PAN mapping in isolated vault
│           ├─ Vaultless (FF1): format-preserving encryption with KMS, reversible with key
│           ├─ Token attributes: single-use vs multi-use, scoped to data domain
│           └─ Audit: every token generation and detokenization logged
│
└─ Need aggregate analytics without individual-level data?
   └─ YES → Differential Privacy
            ├─ Epsilon budget: start with ε=1.0, tune based on utility requirements
            ├─ Mechanisms: Laplace for count queries, Gaussian for numeric aggregates
            ├─ Limitations: repeated queries erode privacy budget, small cell counts need suppression
            └─ Tooling: Google DP library, OpenDP, Tumult Analytics
```

### Cross-Border Data Transfer Decision

```
Data transfer to non-adequate country detected
│
├─ Is the destination country covered by an adequacy decision?
│  ├─ YES (EU: Andorra, Argentina, Canada, Japan, South Korea, Switzerland, UK, etc.)
│  │  └─ Transfer permitted; document adequacy decision + data categories
│  └─ NO → Continue
│
├─ Are Standard Contractual Clauses (SCCs) in place?
│  ├─ YES → Conduct Transfer Impact Assessment (TIA)
│  │        ├─ Step 1: Map data flows — what data, where from, where to, who accesses
│  │        ├─ Step 2: Assess destination country laws — can government access data?
│  │        ├─ Step 3: Identify supplementary measures — E2EE, pseudonymization, tokenization
│  │        ├─ Step 4: Document TIA → legal review sign-off → DPO approval
│  │        └─ Step 5: If TIA fails → STOP TRANSFER; explore alternatives (on-prem, EU-only)
│  └─ NO → STOP
│           └─ Implement SCCs before any transfer. No exceptions for EU personal data.
│
├─ Supplementary measures applied?
│  ├─ Technical: End-to-end encryption (data inaccessible to provider), BYOK/HYOK
│  ├─ Organizational: Zero-access architecture, DPA with provider, annual audit rights
│  └─ Contractual: SCCs + supplementary clauses, data processing agreement (DPA)
│
└─ Special categories of data? (health, biometrics, criminal, political, genetic)
   └─ YES → Enhanced TIA required + explicit consent or substantial public interest basis
```

### Data Retention & Disposal Decision

```
Data retention decision
│
├─ Is this data subject to a legal/regulatory retention requirement?
│  ├─ YES → Define minimum retention
│  │        ├─ Financial records: 7 years (SEC 17a-4, IRS, SOX)
│  │        ├─ Healthcare: varies by state (HIPAA: 6 years from creation or last effective date)
│  │        ├─ Employment records: 3-7 years (by jurisdiction)
│  │        ├─ Tax records: 7 years (IRS)
│  │        └─ Telecom metadata: 1-2 years (by jurisdiction, e.g., EU Data Retention Directive)
│  └─ NO → Apply data minimization → retain only as long as needed for business purpose
│
├─ Is this data subject to a litigation hold?
│  ├─ YES → FREEZE DELETION
│  │        ├─ Flag in database: `legal_hold = true`
│  │        ├─ TTL deletion job MUST check this flag BEFORE every delete
│  │        ├─ Automate: if legal_hold column changes, notify legal team
│  │        └─ Quarterly reconciliation: compare legal hold spreadsheet to database flags
│  └─ NO → Continue to disposal
│
├─ Is this a DSAR deletion request?
│  ├─ YES → Apply cascade deletion
│  │        ├─ Primary database → Replicas → Backups → Logs → CDN caches → Analytics
│  │        ├─ Verify: query every system that ingested this user's data
│  │        └─ SLA: GDPR 30 days, CCPA 45 days, LGPD 15 days
│  └─ NO → Apply standard retention TTL
│
└─ Disposal method selection
   ├─ Cloud: crypto-shredding (delete DEK → data irrecoverable) preferred over physical destruction
   ├─ Database: DELETE with verified vacuum/reclaim
   ├─ Backups: expire from retention policy naturally (do NOT manually delete from backup chain)
   └─ Physical media: NIST 800-88 Clear (logical overwrite), Purge (degauss/block erase), Destroy (shred)
```

### Database Hardening Checklist

```
Database hardening per CIS Benchmarks
│
├─ Authentication & Authorization
│  ├─ Disable default accounts (postgres, sa, root, sys, system)
│  ├─ Enforce strong password policy (12+ chars, complexity, rotation)
│  ├─ Implement role-based access control (RBAC) — no direct user-table grants
│  └─ Application service accounts: minimum required permissions, no DDL rights
│
├─ Network Security
│  ├─ Bind to localhost or private subnet only — no public database endpoints
│  ├─ Enforce TLS 1.2+ for all client connections
│  ├─ Firewall: restrict to application servers' IP ranges only
│  └─ Disable unused network protocols (IPv6 if not needed, NetBIOS, named pipes)
│
├─ Encryption
│  ├─ Enable Transparent Data Encryption (TDE) for data at rest
│  ├─ Configure column-level encryption for PII/PHI/PCI fields
│  ├─ Encrypt backups — backup without encryption violates PCI DSS 4.0 Req 3
│  └─ Rotate database encryption keys annually minimum
│
├─ Auditing & Logging
│  ├─ Enable audit logging for all DDL, privileged operations, and sensitive data access
│  ├─ Forward logs to SIEM with 1-minute granularity
│  ├─ Protect audit logs from tampering (immutable storage, append-only)
│  └─ Alert on: failed logins > 5/min, privilege escalation, mass data exports
│
├─ Dangerous Feature Hardening
│  ├─ Disable: `COPY TO` (PostgreSQL), `LOAD DATA INFILE` (MySQL), `xp_cmdshell` (SQL Server)
│  ├─ Restrict: dynamic SQL execution, file system access, network access from database
│  ├─ Remove: default stored procedures, sample schemas, test databases
│  └─ Sandbox: PL/SQL execution to prevent OS command injection
│
└─ Backup & Recovery
   ├─ Encrypt all backups: AES-256-GCM with KMS-managed keys
   ├─ Test restoration quarterly — untested backups are theoretical
   └─ Offsite backup with geo-redundancy: minimum 2 regions
```

## Cross-Skill Coordination

| Partner Skill | When to Invoke | Handoff Artifact |
|---|---|---|
| **security-engineer** | Identity-based access, network segmentation, WAF rules | Data classification matrix, DLP rule set |
| **compliance-officer** | Audit preparation, regulatory gap analysis, policy documentation | Control implementation evidence, audit trails |
| **cloud-architect** | KMS design, S3 bucket policies, cross-region replication | Encryption architecture, key hierarchy |
| **database-designer** | Schema design with encryption-awareness, TDE configuration | Classification tags per column, masking requirements |
| **backend-developer** | Application-level encryption, log scrubbing, DSAR pipeline | Encryption API spec, masking library config |
| **devops-engineer** | CI/CD integration of DLP scanning, secret rotation, vault integration | DLP scan config, KMS IAM policies |
| **privacy-engineer** | DPIA, privacy-by-design review, DSAR workflow design | Data flows, classification tiers, retention schedules |
| **incident-responder** | Data breach containment, forensic analysis, breach notification | Exposed data inventory, access audit logs |
| **qa-engineer** | Data masking verification, DLP rule testing, DSAR pipeline testing | Test data masking config, DLP test cases |
| **data-engineer** | Data pipeline security, analytics data masking | Classification tags, masking rules |

## Proactive Triggers

| # | Trigger | Action | Why It Matters | If Ignored |
|---|---------|--------|----------------|------------|
| **P1** | New database or S3 bucket created via Terraform/Pulumi/CloudFormation | Auto-classify data stores based on naming convention and tags; flag any PUBLIC ACL | 58% of cloud data breaches originate from misconfigured storage — catch at provisioning, not during audit | Storage provisioned with default (often permissive) policies; sensitive data exposed for months before discovery |
| **P2** | `CREATE TABLE` with columns named `password`, `ssn`, `credit_card`, `token`, `secret` | Apply column-level encryption + audit logging as part of migration; refuse to deploy without KMS configuration | Plaintext secrets in databases = instant P1 incident. Attackers search for these columns first | Breach within hours of exposure; credential stuffing attacks; regulatory fines for inadequate safeguards |
| **P3** | Production database copied to non-production environment | Automatically apply static data masking to PII/PHI/PCI fields; enforce via CI/CD gate | Production data in dev = unauthorized disclosure under GDPR/HIPAA/PCI. Every developer laptop is a breach risk | Mandatory breach notification when dev laptop is stolen; PCI DSS non-compliance; developer access audit failure |
| **P4** | GDPR/CCPA DSAR received | Trigger automated data discovery → assemble all user data from all systems → export or delete per request → verify cascade completion | Manual DSAR handling does not scale beyond ~50/month. Missed 30-day GDPR SLA = supervisory authority complaint | Fine of up to 4% global annual revenue (GDPR) or statutory damages (CCPA) + supervisory enforcement |
| **P5** | KMS key > 365 days since last rotation | Trigger automated rotation; re-encrypt all data encrypted with old key; log rotation to compliance evidence folder | Unrotated encryption keys are a single point of failure. NIST SP 800-57 recommends annual rotation | Extended key exposure window; compliance audit finding (SOC 2 CC6.1, PCI DSS 3.6.4); increased forensic cost |
| **P6** | DLP alert: PII detected in outbound email attachment | Auto-block send; notify sender with secure file sharing alternative; log incident for security review | 64% of data breaches involve email exfiltration. Blocking a single email prevents a reportable breach | Mandatory breach notification; forensics cost ($50K-$500K); reputation damage; possible regulatory fine |
| **P7** | Schema change adds new PII column without encryption | Auto-flag in CI/CD; block PR until column-level encryption is configured | PII added in plaintext = data classification failure. Once data is written, remediation requires backfill | Plaintext PII accumulates; detection requires full column scan; GDPR non-compliance |
| **P8** | Data retention period exceeded on production table | Auto-trigger TTL deletion; check legal hold flag first; log deletion to compliance evidence | Data kept beyond retention increases e-discovery scope, breach impact, and storage costs | 10TB of obsolete data = $500K+ in unnecessary e-discovery costs; expanded breach notification scope |
| **P9** | Third-party vendor gains data access without DPA/BAA | Flag in procurement workflow; block data access until DPA/BAA is signed and archived | GDPR Art. 28 requires DPA for every processor. HIPAA requires BAA for every business associate | Regulatory fine (GDPR: 4% revenue; HIPAA: $50K-$1.5M per violation); unauthorized data processing |
| **P10** | Audit log gap detected (no logging on sensitive table for > 24h) | Auto-enable audit logging; alert security team; flag as compliance incident | Audit gap means any data exfiltration during the gap is undetectable and uncontainable | Undetected data breach during gap; cannot determine scope of exposure; regulatory finding of inadequate monitoring |

## What Good Looks Like

| Element | Excellent | Mediocre | Unacceptable |
|---|---|---|---|
| Data classification | Every data store and sensitive column classified with PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED tags; classification validated by data owner + legal; classification metadata queryable via API | Half the data stores classified; classification based on table name, not column contents; no data owner assigned | No classification at all; team cannot answer "where does our PII live?"; "we'll classify later" |
| Encryption coverage | All RESTRICTED data: AES-256-GCM at column level with KMS-managed DEKs; CONFIDENTIAL: TDE + TLS 1.3; KMS keys rotate annually; key access fully audited | TDE on database but no column-level encryption; PII in plaintext within encrypted database; KMS keys not rotated | No encryption at rest; plaintext PII/PCI/PHI; "the cloud provider encrypts by default" as sole control |
| DLP posture | Blocking mode with <5% FPR at all four layers (network, endpoint, cloud, database); monthly tuning based on alert analysis; DR tested semi-annually | Monitor-only mode with thousands of uninvestigated alerts; no blocking rules because "too many false positives" | No DLP deployed; "we trust our employees"; no capability to detect or block data exfiltration |
| Retention compliance | TTL indexes on every data collection; automated deletion with legal hold override; DSAR pipeline completes within 48 hours; monthly reconciliation report | TTL defined but not enforced; manual deletion quarterly; DSAR handled ad-hoc by legal with engineering fire drills | No retention policy; data accumulates indefinitely; no DSAR pipeline; "GDPR won't apply to us" |
| Audit readiness | Real-time audit logs → SIEM → dashboards; monthly automated audit report; evidence folder organized by control; pentest findings tracked to closure | Audit logs exist but not aggregated; evidence scattered across email/Jira/wiki; pentest findings unresolved from last year | No audit logging; no evidence of security controls; cannot demonstrate compliance to auditor or regulator |

## Deliberate Practice

| # | Exercise | Focus Area | Duration | Difficulty |
|---|---|---|---|---|
| 1 | **Shadow Data Hunt**: Run a sensitive data scanner (AWS Macie, GCP DLP, or grep-based) on all your cloud storage. Find 3 data stores you did not know contained PII. Classify and protect them. | Sensitive data discovery, shadow data | 60 min | Intermediate |
| 2 | **DLP Rule Crafting**: Write 5 DLP rules for your organization's most sensitive data type (e.g., PAN, SSN, PHI). Test with both positive (should trigger) and negative (should not trigger) samples. Tune to <5% FPR. | DLP rules, false positive reduction | 45 min | Advanced |
| 3 | **Key Rotation Drill**: Rotate a production KMS key. Verify all data encrypted with the old key is re-encrypted. Verify no application errors during rotation. Measure downtime (target: zero). | KMS key rotation, zero-downtime operations | 30 min | Intermediate |
| 4 | **DSAR Deletion Test**: Submit a test DSAR for a synthetic user. Time the full cascade: discovery → assembly → export → deletion → verification across all systems (DB, cache, CDN, analytics). | DSAR pipeline, cascade verification | 60 min | Advanced |
| 5 | **Breach Tabletop**: Simulate an S3 bucket with PII becoming public. Walk through: detection (how fast?), containment (who does what?), forensics (what was exposed?), notification (legal requirements). | Incident response, breach notification | 90 min | Advanced |
| 6 | **Classification Deep Dive**: Pick your largest database. Classify every column. Identify columns classified as INTERNAL that contain RESTRICTED data (re-identification risk). Fix the classification. | Data classification, re-identification risk | 45 min | Intermediate |
| 7 | **Cross-Border TIA**: Pick one cross-border data flow (e.g., EU → US analytics). Conduct a full Transfer Impact Assessment: map flows, assess destination laws, identify supplementary measures, document findings. | Cross-border compliance, TIA methodology | 60 min | Expert |

## Gotchas

### Data Classification Gotchas

**Classifying data after the breach costs 10x more than classifying before.** Without pre-breach classification labels, you cannot determine what was exposed — forcing the worst-case assumption that all data is sensitive. Notification costs balloon because you must notify for all possible data types, forensic investigation takes weeks instead of hours, and regulators penalize the uncertainty as negligence. **Total cost: $500K–$4M in notification, forensics, and regulatory penalties.** Fix: Classify data at creation time with automated tagging (Macie, Purview, Cloud DLP). Implement CI gates: schema changes without classification labels fail the build.

**Missing data retention policy turns every byte of stored data into discoverable evidence in litigation.** Data kept beyond its defined retention period is still discoverable in e-discovery. Every terabyte of unnecessary data increases legal review costs, extends discovery timelines, and exposes the organization to additional liability from old communications and documents. **Total cost: $500K–$5M+ in e-discovery costs, adverse inferences from old data, and extended litigation exposure.** Fix: Implement automated data lifecycle management with hard deletes at retention expiration. Per-data-classification retention schedules. Crypto-shredding for Confidential+ data.

**Encrypting everything without classification wastes resources and creates operational friction.** Encrypting PUBLIC data (marketing assets, public docs) consumes KMS API calls at scale, adds latency to every read, and complicates backup/restore. Meanwhile, RESTRICTED data might be under-protected because everything is treated equally. Classification tells you where to spend your encryption budget. **Total cost: $50K–$500K in unnecessary KMS costs, query latency impact, and operational complexity over 3 years.** Fix: Classify first, then encrypt based on tier: PUBLIC (no encryption), INTERNAL (TLS + provider-managed keys), CONFIDENTIAL (AES-256-GCM + CMK), RESTRICTED (AES-256-GCM + CMK + application-level encryption + audit).

### Encryption Gotchas

**Hardcoded encryption keys invalidate all compliance certifications retroactively.** If encryption keys are found in source code, config files, or environment variables during an audit, auditors will deem all data "encrypted" with those keys as unprotected. This triggers mandatory customer notification, re-encryption of all historical data, and potential fines for each compliance framework claimed (PCI DSS, HIPAA, GDPR, SOC 2). The re-encryption alone on a 50TB production database can take weeks of downtime. **Total cost: $250K–$2M in audit penalties, re-encryption costs, and customer notification.** Fix: Use KMS with automatic rotation (90-day maximum). Store keys only in HSM-backed KMS. Scan CI/CD pipelines for hardcoded key patterns.

**Unrotated encryption keys turn a 30-day exposure into a permanent, catastrophic breach.** If encryption keys are not rotated and an attacker gains access to a historical backup containing old keys, all data ever encrypted with those keys is compromised — potentially years of historical data. Key rotation limits the blast radius: if keys rotate every 90 days, a key compromise only exposes data encrypted in that 90-day window. **Total cost: $1M–$10M+ for mass data exposure spanning years of records, multi-jurisdiction notification, and class-action litigation.** Fix: Implement automatic key rotation every 90 days in KMS. Use key versioning to track which data was encrypted with which key version. Destroy old key versions when all associated data exceeds retention period.

### DLP Gotchas

**DLP deployed in eternal monitor-only mode is security theater.** Organizations deploy DLP, get flooded with alerts, and switch to monitor-only mode "temporarily" to tune rules. Months later, DLP records every exfiltration without stopping any. The annual DLP license cost ($100K–$500K for enterprise) is wasted while data exfiltration continues. **Total cost: $300K–$2M in wasted DLP licensing, undetected exfiltration, and eventual breach notification.** Fix: Deploy DLP in phased approach: 14 days monitor-only to baseline, enable blocking for external when FPR under 10%, enable internal blocking for RESTRICTED data, tune to under 5% FPR. Never exceed 30 days in monitor-only without executive sign-off.

**Cross-border data transfer without adequate safeguards triggers GDPR fines up to 4% of global annual turnover.** Under Schrems II (CJEU C-311/18), transferring EU personal data to the US without SCCs + Transfer Impact Assessment + supplementary technical measures can result in orders to suspend transfers plus fines. The Irish DPC fined Meta €1.2 billion in 2023 for unlawful EU-US data transfers. Even at smaller scale, a transfer suspension order halts operations. **Total cost: €20M–€1.2B+ in GDPR fines plus business disruption.** Fix: Implement SCCs (2021 version) for all EU data transfers. Conduct and document Transfer Impact Assessment. Apply supplementary technical measures: CMK encryption, pseudonymization, split processing. Review annually.

### Database Hardening Gotchas

**Production data in non-production environments triggers mandatory breach notification.** Under GDPR Art. 33-34, HIPAA Breach Notification Rule, and PCI DSS Requirement 3, using real PII/PHI/PCI in dev/test/staging/sandbox environments constitutes an unauthorized disclosure. This is not a best practice violation — it is a regulatory breach requiring notification to regulators (within 72 hours for GDPR) and affected individuals. **Total cost: $100K–$1.5M in notification costs, regulatory fines, and remediation.** Fix: Implement static data masking as a prerequisite for non-production data refreshes. Use synthetic data generation for scale testing.

**Database public endpoints are the #1 cloud data breach vector.** A database exposed to the internet with default credentials is discoverable within hours by automated scanners. Once discovered, the time to full compromise averages 72 hours. 58% of cloud data breaches originate from misconfigured storage. **Total cost: $1M–$10M+ for a database breach involving PII or PHI, including notification, forensic investigation, regulatory fines, and class-action litigation.** Fix: Bind databases to private subnets only. Use VPC/service endpoints for cloud database services. Never assign public IP addresses to database instances.

### Data Masking Gotchas

**Format-preserving masking that preserves uniqueness can be reverse-engineered.** If masking uses a deterministic algorithm (e.g., HMAC truncated to format), an attacker with access to both masked and unmasked datasets can build a mapping table to reverse the mask. This is particularly dangerous when masked data is shared with third-party analytics providers. **Total cost: $100K–$1M in unauthorized PII exposure via masked data re-identification.** Fix: For high-sensitivity fields, use randomized masking or tokenization with a central vault. For deterministic masking, use a per-field HMAC key stored in KMS with strict access controls.

**Dynamic data masking can be bypassed by privileged users.** Most database-native dynamic masking solutions (SQL Server DDM, PostgreSQL RLS) can be bypassed by users with elevated privileges (db_owner, superuser). The application layer may show masked data, but a DBA connecting directly with full privileges sees plaintext. **Total cost: $200K–$1M in insider threat data exposure when a DBA with plaintext access exfiltrates data thought to be universally masked.** Fix: Defense-in-depth — apply masking at multiple layers (database + application + API gateway). Use column-level encryption with application-layer decryption so even DBAs cannot access plaintext.

## Verification

| # | Verification Step | Expected Result |
|---|-------------------|-----------------|
| 1 | Run data discovery scan across all data stores | All sensitive data fields identified and classified |
| 2 | Verify encryption at rest on all database connections | TLS 1.3 active on all database connections |
| 3 | Check column-level encryption on PII columns | Encryption key ID returned for all PII columns |
| 4 | Test DLP blocking rule with sample credit card number | Request blocked with DLP violation (HTTP 403), alert generated |
| 5 | Verify key rotation status for data encryption keys | Key rotation enabled, last rotation within 90 days |
| 6 | Check audit logging for PII table accesses | All PII table accesses logged with user identity and timestamp |
| 7 | Validate non-prod data masking on staging database | All sensitive values match mask pattern, no real data found |
| 8 | Test database hardening on public role | PUBLIC role has no access to dangerous functions |
| 9 | Verify retention policy enforcement on deleted records | Zero records beyond retention period remain in database |
| 10 | Check cross-border transfer documentation | SCC executed for each cross-border transfer, TIA signed within 12 months |
| 11 | Test backup encryption by restoring without KMS key | Restoration fails, backup requires KMS key |
| 12 | Verify access control for read-only users | Read-only role has no access to PII-containing tables |

## References

### Industry Standards & Frameworks
- [PCI DSS v4.0.1](references/pci-dss-v4.md) — Payment Card Industry Data Security Standard, Requirements 3, 4, 7, 10
- [NIST SP 800-88](references/nist-sp-800-88.md) — Guidelines for Media Sanitization
- [NIST SP 800-57](references/nist-sp-800-57.md) — Recommendation for Key Management
- [NIST SP 800-122](references/nist-sp-800-122.md) — Guide to Protecting the Confidentiality of PII
- [CIS Benchmarks](references/cis-benchmarks.md) — Database hardening benchmarks (PostgreSQL, MySQL, SQL Server, Oracle)
- [ISO 27001/27002](references/iso-27001-27002.md) — Information Security Management Controls (A.10 Cryptography, A.12 Operations Security)

### Regulations
- [GDPR Articles 5, 25, 32, 44-49](references/gdpr-data-protection.md) — Data protection by design, security of processing, cross-border transfers
- [HIPAA Security Rule](references/hipaa-security-rule.md) — 45 CFR 164.312 Technical Safeguards for PHI
- [CCPA/CPRA](references/ccpa-cpra.md) — California data minimization and security requirements
- [Schrems II Ruling](references/schrems-ii.md) — CJEU C-311/18, EU-US data transfer requirements
- [EU-US Data Privacy Framework](references/eu-us-dpf.md) — Adequacy decision for certified US organizations
- [PCI DSS 4.0 Requirements](references/pci-dss-requirements.md) — Requirements 3 (stored data), 4 (transit encryption), 7 (access control), 10 (logging)

### Technical References
- [OWASP Top 10 A02:2021](references/owasp-crypto-failures.md) — Cryptographic Failures
- [OWASP Top 10 A04:2021](references/owasp-insecure-design.md) — Insecure Design
- [AWS KMS Cryptographic Details](references/aws-kms-crypto.md) — Envelope encryption, key hierarchy, automatic rotation
- [Azure Key Vault](references/azure-key-vault.md) — Secrets, keys, and certificate management
- [GCP Cloud KMS](references/gcp-cloud-kms.md) — Symmetric and asymmetric encryption at scale
- [HashiCorp Vault](references/hashicorp-vault.md) — Multi-cloud secrets management and encryption as a service

### Data Security Tools
- [AWS Macie](references/aws-macie.md) — Managed sensitive data discovery and classification
- [Google Cloud DLP](references/gcp-dlp.md) — Sensitive data inspection, classification, de-identification
- [Azure Purview](references/azure-purview.md) — Unified data governance and classification
- [Varonis](references/varonis.md) — Data security platform for classification and threat detection
- [Imperva](references/imperva.md) — Database activity monitoring and protection
- [IBM Guardium](references/ibm-guardium.md) — Database activity monitoring and vulnerability assessment
