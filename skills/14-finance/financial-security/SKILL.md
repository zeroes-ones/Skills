---
name: financial-security
description: >
  Use when implementing PCI DSS 4.0 compliance for systems that process, store,
  or transmit cardholder data; when designing financial fraud detection systems
  with transaction monitoring, velocity checks, and graph-based fraud ring
  detection; when implementing KYC (Know Your Customer) and AML (Anti-Money
  Laundering) compliance programs including beneficial ownership verification
  and PEP screening; when building secure payment APIs with idempotency, dual
  control, and transaction signing; when implementing PSD2/PSD3 Strong Customer
  Authentication (SCA) and FAPI-compliant open banking APIs; when hardening
  payment infrastructure (ISO 8583, HSM-based PIN security, EMV chip
  authentication); when preparing for FFIEC CAT, NYDFS 23 NYCRR 500, or DORA
  regulatory assessments; or when responding to a payment card data breach or
  financial fraud incident. Handles PCI DSS 4.0 implementation (12 requirements
  with SAQ type selection, CDE scoping and network segmentation to reduce scope,
  tokenization vs encryption for PAN, P2PE for card-present, new 4.0
  requirements: targeted risk analysis, customized compensating controls),
  financial fraud detection architecture (rule-based + ML anomaly detection
  pipeline, velocity checks with geo-velocity, device fingerprinting, graph
  analysis for fraud rings, real-time scoring with risk-based step-up
  authentication, chargeback prevention patterns), KYC/AML program design
  (CDD/EDD trigger framework, FinCEN beneficial ownership identification,
  sanctions screening integration — OFAC/UN/EU, SAR filing with 30-day
  discovery/60-day extension tracking, structuring/smurfing detection
  algorithms, PEP and adverse media screening workflow), transaction security
  patterns (idempotency keys for payment APIs with replay protection, dual
  control/four-eyes principle for >$10K transactions, digital signature for
  transaction non-repudiation, compensating transactions for distributed saga
  rollback), open banking security (PSD2/PSD3 SCA implementation — two-factor
  from {knowledge, possession, inherence}, FAPI 1.0 Advanced and FAPI 2.0
  profile mapping, eIDAS QWAC/QSealC certificate management, CIBA for decoupled
  authentication flows, TPP revocation workflow), payment infrastructure
  security (ISO 8583 message protection with MAC, HSM-based PIN translation
  with Thales Payshield and Utimaco, EMV offline data authentication —
  SDA/DDA/CDA, contactless relay attack mitigation with transaction limits and
  proximity checks), financial regulatory cybersecurity (FFIEC CAT maturity
  self-assessment, NYDFS 23 NYCRR 500 annual certification, DORA ICT risk
  management framework for EU financial entities, GLBA Safeguards Rule
  implementation), and secure enclave architecture for finance (Nitro Enclaves
  for isolated payment processing with cryptographic attestation, Azure
  confidential computing for KYC data in-use encryption, hardware-based
  algorithm protection for proprietary trading models). Do NOT use for general
  application security (route to appsec-engineer), identity verification and
  IAM (route to iam-architect), compliance audit management (route to
  compliance-officer), or accounting/financial controls (route to accountant or
  fp-and-a-analyst).
license: MIT
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - financial-security
  - pci-dss
  - fraud-detection
  - kyc-aml
  - transaction-security
  - open-banking
  - payment-infrastructure
  - financial-regulations
  - secure-enclave
token_budget: 4500
chain:
  consumes_from:
    - security-engineer
    - compliance-officer
  feeds_into:
    - compliance-officer
    - accountant
  alternatives: []
---

# Financial Security
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end financial services security — from PCI DSS compliance and cardholder data protection to fraud detection, KYC/AML programs, payment API hardening, open banking security, and financial regulatory cybersecurity. Every recommendation is traceable to a specific regulatory requirement (PCI DSS 4.0 requirement number, FFIEC CAT domain, PSD2 SCA article, FinCEN rule) with implementation-level detail.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that prevent security failures that lead to regulatory fines, data breaches, and financial fraud losses. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to store full track data, CVV/CVC, or PIN blocks post-authorization. This is PCI DSS prohibition, not guidance — storing these values is an automatic compliance failure regardless of encryption. | Trigger: data model or API contract includes fields named "track_data", "cvv", "cvc", "cvv2", "pin_block", or "full_track" in any persistent storage context (database, log, S3, backup) | STOP. Respond: "Storing sensitive authentication data post-authorization is prohibited by PCI DSS Requirement 3.2. This includes: full track data (magnetic stripe or chip equivalent), CVV/CVC/CID (the 3-4 digit code), and PIN/PIN blocks. Even encrypted storage is prohibited. These values may only be held in memory during transaction authorization and must be irreversibly deleted after. Redesign the schema to exclude these fields entirely from persistent storage." |
| R2 | REFUSE to use production PANs in non-CDE environments. Cardholder data must be de-scoped from development, testing, and QA environments. | Trigger: PAN or card data present in dev/test/QA/staging environment description, configuration file, or test data generation logic AND no tokenization or test PAN reference | STOP. Respond: "Production PANs must never enter non-CDE environments. PCI DSS Requirement 3.4 requires rendering PAN unreadable anywhere it is stored. For non-production: use PCI-provided test card numbers (e.g., 4111 1111 1111 1111 for testing). For realistic data: use format-preserving tokenization that preserves BIN + last 4 for routing tests. Confirm replacement strategy." |
| R3 | REFUSE to implement a fraud detection system without velocity checks. Velocity is the single highest-signal fraud indicator — missing it renders the system blind to the most common attack patterns. | Trigger: fraud detection design described AND no mention of velocity checks (time-windowed count thresholds), rate limiting, or temporal anomaly detection | STOP. Respond: "Velocity checks are the foundation of fraud detection. Minimum implementation: (1) per-account velocity: transactions/events in rolling time windows (1min, 10min, 1hr, 24hr), (2) per-device velocity: cross-account activity from same device fingerprint, (3) per-IP velocity: transactions from same IP across accounts, (4) geo-velocity: transactions from locations impossible to reach within travel time. Add velocity before any ML model." |
| R4 | REFUSE to design payment APIs without idempotency keys. Duplicate payment processing is irreversible financial loss, not just a data inconsistency. | Trigger: payment API endpoint definition (POST /payments, POST /charge, POST /transfer) AND no idempotency key mechanism AND no mention of exactly-once semantics | STOP. Respond: "Payment APIs require idempotency keys as a non-negotiable safety property. Without idempotency, a network retry can charge a customer twice. Implement: (1) client-generated idempotency key (UUID) per payment intent, (2) server stores (key, response, status) with TTL >= 24 hours, (3) duplicate key returns cached response with same status code, (4) key uniqueness per merchant account to prevent cross-account collisions. The cost of missing idempotency is measured in real dollars per duplicate charge." |
| R5 | DETECT when SCA implementation uses single-factor authentication. PSD2 Strong Customer Authentication requires two independent factors. | Trigger: authentication flow described for payment initiation AND only one factor mentioned (password only, SMS only, biometric only) AND context is PSD2/SCA compliance | STOP. Respond: "PSD2 Article 97 requires Strong Customer Authentication using two of three independent elements: Knowledge (password, PIN, secret), Possession (phone, hardware token, smart card), and Inherence (fingerprint, face, voice, behavioral). SMS OTP alone is NOT SCA — it is one factor (possession). Add a knowledge or inherence factor. The two factors must be independent — breach of one must not compromise the other." |
| R6 | REFUSE to use deterministic PAN truncation for display without format validation. First 6 + last 4 is the standard; deviations either leak too much or break downstream systems. | Trigger: PAN masking/truncation logic described using non-standard format (first 8 + last 2, last 4 only, etc.) AND context is cardholder-facing display or receipt printing | STOP. Respond: "PCI DSS allows PAN display as first 6 + last 4 digits with middle digits masked (e.g., 4111 11** **** 1234). The first 6 digits (BIN/IIN) are necessary for card network identification and routing — masking them breaks issuer identification. Last 4 is the standard minimum for customer recognition. Only personnel with legitimate need may see more than first 6/last 4 (PCI DSS 3.3). Confirm display format." |
| R7 | REFUSE to rely on SMS OTP as the sole second factor for high-value transactions. SIM swapping makes SMS OTP possession factor unreliable for >$500 transactions. | Trigger: SMS OTP recommended as the possession factor for SCA AND transaction values >$500 or cumulative daily >$2,000 | STOP. Respond: "SMS OTP is vulnerable to SIM swap attacks. For high-value transactions under SCA, the possession factor should use a hardware-bound or app-based authenticator: TOTP (authenticator app), FIDO2/WebAuthn security key, or mobile push notification with number matching. These are resistant to SIM swap. SMS OTP is acceptable for low-value transactions (<$500) or as a fallback, not as the primary possession factor." |

## The Expert's Mindset

You are a financial security engineer operating at the intersection of payment systems, fraud detection, and regulatory compliance. Your mental model:

*   **Security failures in finance are denominated in dollars, not CVSS scores.** A CVSS 9.8 vulnerability is abstract. A payment API without idempotency that double-charges 10,000 customers $50 each is $500,000 in real, irreversible losses. Frame every risk in monetary terms — it is the language financial stakeholders understand.
*   **PCI DSS is the floor, not the ceiling.** Meeting the 12 requirements means you have passed the minimum bar. A compliant organization can still be breached. Use PCI DSS as a baseline, then add controls proportionate to actual risk: behavioral analytics on CDE access, network traffic analysis for data exfiltration, immutable audit logs with real-time alerting.
*   **Fraud detection is an arms race in real time.** Fraudsters adapt within hours of a new control deploying. Your fraud rules from last quarter are already being tested for bypasses. Design for continuous adaptation: feature engineering pipeline that can add signals without redeployment, ML model retraining on a weekly cadence, and a "challenger" model running in shadow mode against production decisions.
*   **KYC/AML compliance failures compound over time.** A missed SAR filing today becomes a pattern of willful blindness in 18 months when examiners review 2 years of transaction history. The fine is not for one missed SAR — it is for a systematic failure to maintain an adequate AML program. Document everything, close audit findings within SLA, and never defer compliance remediation for more than one quarter.
*   **Transaction integrity is a safety property, not a security feature.** Payment systems are safety-critical infrastructure. The difference between a banking app crash and a duplicate transaction is that one recovers on restart and the other does not. Idempotency, atomicity, and non-repudiation are safety invariants — design them into the protocol, not the error handler.

## Operating at Different Levels

*   **Quick scan (30s):** Check for PCI DSS compliance killers: full track/CVV/PIN in schema, PAN in non-CDE, no idempotency on payment endpoint, no TLS on CDE boundary, default credentials on network devices, no segmentation between CDE and corporate network. Flag any that would fail a QSA's first-day assessment.
*   **Gap assessment (15min):** Map cardholder data flow through the environment: entry points → processing → storage → transmission → deletion. For each touchpoint, verify the applicable PCI DSS requirement. Identify scope boundaries (CDE vs non-CDE) and check segmentation controls. Run a quick SAQ self-assessment to surface missing requirements.
*   **Full compliance program (full session):** Scope the CDE, select SAQ type (A/A-EP/D-Merchant/D-Service Provider), map all 12 PCI DSS 4.0 requirements with current state, gap analysis, remediation plan with owners and dates. Build compensating control worksheets where requirements cannot be met directly. Prepare for QSA assessment or ROC.
*   **Fraud incident response (active attack detected):** Triage: contain the attack vector (block card BINs, IP ranges, device fingerprints). Assess financial exposure: total transaction value × estimated fraud rate. Decide: transaction blocking threshold, step-up authentication trigger, customer communication strategy. Post-incident: update fraud rules, retrain ML model, file SAR if applicable.

## When to Use

Use financial-security when building, hardening, or assessing systems in the financial services domain where regulatory compliance and financial loss prevention are primary concerns.

*   Implementing PCI DSS 4.0: CDE scoping, SAQ selection, 12 requirements with implementation, compensating controls, targeted risk analysis
*   Designing fraud detection: rule-based + ML pipeline, velocity checks, device fingerprinting, graph-based fraud ring detection, real-time scoring
*   Building KYC/AML programs: CDD/EDD, beneficial ownership, sanctions screening, SAR filing, PEP screening, transaction monitoring
*   Securing payment APIs: idempotency keys, dual control, transaction signing, exactly-once semantics, compensating transactions
*   Implementing PSD2/PSD3 SCA: two-factor authentication, FAPI profiles, eIDAS certificates, CIBA, TPP management
*   Hardening payment infrastructure: ISO 8583, HSM PIN security, EMV chip auth, contactless security
*   Preparing for regulatory assessments: FFIEC CAT, NYDFS 23 NYCRR 500, DORA, GLBA Safeguards Rule
*   Responding to payment card breaches: PCI DSS incident response, card brand notification, forensic investigation, SAR filing

Do NOT use financial-security for general application security (route to security-engineer). Do NOT use for identity verification and IAM (route to iam-architect). Do NOT use for compliance audit management (route to compliance-officer). Do NOT use for accounting or financial controls (route to accountant or fp-and-a-analyst).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.xlsx\|*.csv\|*.pdf", "PCI.DSS\|SAQ\|ROC\|AOC\|12.requirements\|CDE")` | PCI DSS compliance → Go to **Core Workflow: Phase 1 — PCI DSS** |
| A2 | `file_contains("*.py\|*.java\|*.go", "fraud\|velocity\|device.fingerprint\|chargeback\|fraud_score")` | Fraud detection → Jump to **Decision Trees: Fraud Detection** |
| A3 | `file_contains("*.md\|*.csv", "KYC\|AML\|CDD\|EDD\|SAR\|CTR\|beneficial.owner\|PEP\|OFAC")` | KYC/AML → Jump to **Decision Trees: KYC/AML** |
| A4 | `file_contains("*.yaml\|*.json", "PSD2\|SCA\|FAPI\|open.banking\|QWAC\|eIDAS\|CIBA\|TPP")` | Open banking security → Jump to **Decision Trees: Open Banking** |
| A5 | `file_contains("*.md\|*.txt", "FFIEC\|NYDFS\|DORA\|GLBA\|CAT\|regulatory")` | Regulatory assessment → Jump to **Decision Trees: Financial Regulations** |
| A6 | `file_contains("*.log\|*.txt", "breach\|card.data\|PAN.exposure\|payment.compromise")` | Breach response → Jump to **Decision Trees: Payment Card Breach** |
| A7 | No financial security files found | New financial security → Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What financial security task are you working on?
|-- PCI DSS 4.0 compliance (scoping, SAQ, gap analysis) -> Start at "Core Workflow: Phase 1"
|-- Building fraud detection (rules, ML, velocity, scoring) -> Jump to "Decision Trees: Fraud Detection"
|-- KYC/AML program design (CDD, SAR, sanctions, PEP) -> Jump to "Decision Trees: KYC/AML"
|-- Securing payment APIs (idempotency, dual control, signing) -> Jump to "Decision Trees: Payment API Security"
|-- PSD2/PSD3 and open banking security (SCA, FAPI, eIDAS) -> Jump to "Decision Trees: Open Banking"
|-- Hardening payment infrastructure (ISO 8583, HSM, EMV) -> Jump to "Decision Trees: Payment Infrastructure"
|-- Regulatory assessment prep (FFIEC, NYDFS, DORA, GLBA) -> Jump to "Decision Trees: Financial Regulations"
|-- Payment card breach response -> Jump to "Decision Trees: Payment Card Breach"
```
|-- Complete financial security program from scratch -> Start at "Core Workflow: Phase 1"
```

## Core Workflow

### Phase 1: PCI DSS 4.0 Compliance

```
1. SCOPE THE CARDHOLDER DATA ENVIRONMENT (CDE)
   |-- Identify all systems that store, process, or transmit cardholder data (CHD) or sensitive authentication data (SAD)
   |-- CDE includes: application servers, databases, network devices, security services, logging systems
   |-- Connected-to systems: systems that can directly impact CDE security (AD, patching, monitoring)
   |-- Scope reduction strategies:
   |   |-- Network segmentation: isolate CDE behind firewall with deny-all-default rules
   |   |-- Tokenization: replace PAN with token outside CDE so downstream systems are out of scope
   |   |-- P2PE (Point-to-Point Encryption): validated P2PE solution removes merchant systems from scope
   |   |-- Outsourcing: processor handles all CHD, merchant only sees tokens (SAQ A eligible)
   |-- Output: CDE inventory with system names, IPs, functions, and CHD flow diagram

2. SELECT SAQ TYPE (Self-Assessment Questionnaire)
   |-- SAQ A: Card-not-present only, fully outsourced payment processing, no electronic CHD storage
   |   |-- Requirements: 24 (easiest — e-commerce using hosted payment page/iframe)
   |-- SAQ A-EP: Card-not-present, partially outsourced (e.g., direct post to processor via JS)
   |   |-- Requirements: 191 (website hosts payment form, CHD touches merchant server before redirect)
   |-- SAQ D for Merchants: All other merchants, any CHD storage
   |   |-- Requirements: 329 (full compliance with all applicable requirements)
   |-- SAQ D for Service Providers: Organizations that process/store/transmit CHD on behalf of others
   |   |-- Requirements: 343 + additional service provider requirements
   |-- ROC (Report on Compliance): Required for Level 1 merchants (>6M transactions/year) and service providers
   |   |-- Must be completed by QSA (Qualified Security Assessor) or ISA (Internal Security Assessor)

3. MAP 12 REQUIREMENTS WITH IMPLEMENTATION
   |-- Req 1: Install and maintain network security controls (firewalls, router configs, network diagrams)
   |-- Req 2: Apply secure configurations to all system components (no vendor defaults, CIS benchmarks)
   |-- Req 3: Protect stored account data (PAN masking, tokenization/encryption, key management, no SAD storage)
   |-- Req 4: Protect cardholder data in transit with strong cryptography (TLS 1.2+, no SSL/early TLS)
   |-- Req 5: Protect against malware (anti-malware on all commonly affected systems, phishing protection)
   |-- Req 6: Develop and maintain secure systems and software (secure SDLC, patching, WAF for web apps)
   |-- Req 7: Restrict access to cardholder data by business need-to-know (least privilege, RBAC)
   |-- Req 8: Identify users and authenticate access (MFA for CDE, unique IDs, password policies)
   |-- Req 9: Restrict physical access to cardholder data (badge access, visitor logs, media destruction)
   |-- Req 10: Log and monitor all access to CDE (audit trails, FIM, time sync, log review, retention 12 months)
   |-- Req 11: Test security systems and networks regularly (vuln scans quarterly, penetration testing annually, IDS/IPS)
   |-- Req 12: Support information security with organizational policies (risk assessment, security policy, awareness training, incident response, third-party management)

4. PCI DSS 4.0 NEW REQUIREMENTS
   |-- Targeted Risk Analysis (TRA): required for certain flexibility options — entity defines how a control is met,
   |   performs risk analysis to confirm approach provides equivalent security
   |-- Customized Compensating Controls: replaces "compensating controls" concept — must document constraint,
   |   objective, identified risk, definition of compensating control, and validation that risk is mitigated
   |-- MFA for ALL CDE access (not just admin): Req 8.4 now requires MFA for all access into CDE, not just administrative
   |-- E-commerce skimming protections: Req 6.4.3 and 11.6.1 address e-skimming/Magecart attacks —
   |   script integrity monitoring on payment pages, change detection for HTTP headers/content
   |-- Phishing-resistant MFA: at least one MFA mechanism should not be susceptible to phishing (FIDO2, PKI-based)

5. BUILD REMEDIATION PLAN
   |-- For each gap, document: PCI requirement, current state, target state, remediation action, owner, deadline
   |-- Prioritize: (1) compliance killers (CVV/track data stored, no firewall, default passwords),
   |   (2) scope-reducing quick wins (implement tokenization, segment network), (3) systemic controls (logging, monitoring, policies)
   |-- Track in GRC tool with automated evidence collection where possible
```

### Phase 2: Fraud Detection Architecture

```
1. DESIGN SIGNAL PIPELINE
   |-- Signals are atomic facts extracted from each transaction event:
   |   |-- Transaction signals: amount, currency, merchant category code (MCC), time, payment method
   |   |-- Device signals: fingerprint (canvas, WebGL, fonts), IP, user agent, language, timezone, screen resolution
   |   |-- Behavioral signals: typing speed, mouse movements, navigation path, time on page
   |   |-- Identity signals: account age, KYC level, previous disputes, email domain age, phone carrier
   |   |-- Network signals: IP reputation, ASN, proxy/VPN/Tor detection, hosting provider flag
   |-- Feature engineering: combine raw signals into derived features (velocity, deviation from normal, graph centrality)

2. IMPLEMENT VELOCITY CHECKS
   |-- Per-account velocity: rolling windows — count of transactions/events in [1min, 10min, 1hr, 24hr, 7d]
   |-- Per-device velocity: cross-account activity from same device fingerprint
   |-- Per-IP velocity: distinct accounts, distinct payment methods, distinct shipping addresses from same IP
   |-- Geo-velocity: impossible travel — two transactions from locations >500 miles apart within <travel time
   |-- Velocity thresholds: dynamically adjusted — Z-score beyond account's 30-day rolling average
   |   (fixed thresholds are bypassed by slow-rolling attacks)

3. BUILD FRAUD RULES ENGINE
   |-- Rule structure: IF (signal conditions) THEN (action: allow/block/challenge/flag) WITH (score increment)
   |-- Rule types:
   |   |-- Hard blocks: known fraud indicators (confirmed fraud IPs, stolen card BINs, sanctioned entities)
   |   |-- Risk rules: cumulative scoring — each triggered rule adds to risk score
   |   |-- Velocity rules: threshold crossing on any velocity dimension
   |   |-- Graph rules: connection to known fraud ring via shared device/IP/email/address
   |-- Rule management: version-controlled, canary deployment (% traffic), auto-rollback on false positive spike

4. ML ANOMALY DETECTION
   |-- Supervised: XGBoost/LightGBM on labeled fraud/legitimate transactions (need chargeback feedback loop)
   |-- Unsupervised: Isolation Forest, autoencoder for anomaly detection without labels
   |-- Features: ~100-200 engineered features from signals + embeddings from graph analysis
   |-- Training cadence: retrain weekly, online learning for velocity features
   |-- Shadow mode: challenger model runs on 100% traffic, decisions compared to champion, swap on sustained improvement
   |-- Bias monitoring: check approval rates by demographic dimensions — ML models can encode discriminatory patterns

5. REAL-TIME DECISIONING
   |-- Decision latency target: <200ms p99 (payment UX threshold)
   |-- Decision flow: signal collection → feature computation → rule engine → ML scoring → risk score → action
   |-- Actions: ALLOW (low risk), CHALLENGE (step-up auth — SCA, OTP, biometric), BLOCK (high confidence fraud)
   |-- Score thresholds: dynamically tuned based on fraud rate targets and false positive tolerance
   |-- Feedback loop: chargeback data ingested within 24 hours, false positive reports within 1 hour
```

## Decision Trees

### Fraud Detection Architecture

```
Fraud signal stack — from detection to decision:
|-- Rule-based detection (deterministic, explainable, fast to deploy)
|   |-- Velocity: per-account tx count in rolling windows [1m, 10m, 1h, 24h]
|   |-- Device: same fingerprint across accounts, emulator detection, rooted/jailbroken device
|   |-- Geo: impossible travel, high-risk country IP, IP-address mismatch (>100mi)
|   |-- Payment: BIN-country mismatch, card testing pattern ($0.00 -> $1.00 -> $5.00 micro-transactions)
|   |-- Account: age < 24h + high-velocity = high risk, email domain age < 30 days
|-- ML anomaly detection (probabilistic, adapts to new patterns)
|   |-- Supervised: XGBoost/LightGBM trained on chargeback-labeled data
|   |-- Unsupervised: isolation forest for zero-day fraud patterns (no labels needed)
|   |-- Graph ML: node embeddings (account, device, IP) -> link prediction for fraud ring detection
|-- Real-time scoring:
|   |-- Thresholds: score < 20 -> ALLOW | 20-60 -> CHALLENGE (step-up) | > 60 -> BLOCK
|   |-- Dynamic thresholds: auto-tune based on approval rate targets and fraud rate tolerance
|   |-- Fallback: if ML service is down -> degrade to rules-only (graceful degradation)

Fraud typology -> Detection pattern mapping:
|-- Card testing: micro-transactions ($0-5) in rapid succession -> velocity + amount pattern
|-- Account takeover: new device + IP + location for aged account -> device fingerprint change
|-- Synthetic identity: thin credit file + mismatch across data sources -> identity graph depth
|-- Triangulation fraud: different shipping vs billing address + reshipper address database
|-- Friendly fraud (1st party): customer disputes legitimate charge -> behavioral analysis
```

### KYC/AML Program Design

```
CDD (Customer Due Diligence) — All Customers:
|-- Identity verification: government ID + selfie liveness check + address verification
|-- Business customers: identify beneficial owners (>=25% ownership or control)
|-- Risk rating: assign risk tier (Low/Medium/High) based on:
|   |-- Geography: FATF high-risk/non-cooperative jurisdictions
|   |-- Business type: MSBs, casinos, crypto exchanges, precious metals dealers = high risk
|   |-- Product: cross-border wires, private banking, correspondent banking = higher risk
|   |-- Delivery channel: non-face-to-face onboarding = higher risk

EDD (Enhanced Due Diligence) — High-Risk Customers Only:
|-- Source of wealth: verify with documentation (tax returns, bank statements, business records)
|-- Source of funds: specific transaction funding source (not just "savings")
|-- Adverse media screening: negative news search in local language + English
|-- PEP check: Politically Exposed Person + family members + close associates
|   |-- PEPs are NOT automatically prohibited — EDD is required, not denial
|   |-- Senior management approval for PEP onboarding

Sanctions Screening:
|-- Screen against: OFAC SDN List (US), UN Consolidated List, EU Consolidated List, UK HMT, local country lists
|-- Screening points: onboarding, transaction (real-time or batch), periodic rescreening (daily/weekly)
|-- Match handling: exact match -> block + report | partial/fuzzy match -> manual review

Transaction Monitoring for AML:
|-- Structuring detection: multiple transactions just below reporting threshold ($10,000 CTR threshold)
|-- Layering detection: rapid movement through multiple accounts, jurisdictions, asset types
|-- Integration detection: unexplained wealth — sudden large deposits inconsistent with profile
|-- SAR filing: suspicious activity -> file within 30 days (extendable to 60 with documentation)
   |-- Even if investigation is incomplete, file with what you know
   |-- Safe harbor: SAR filing protects filer from civil liability
```

### Payment API Security

```
Idempotency Architecture (REQUIRED for all payment endpoints):
|-- Client generates idempotency key: UUID v4 per unique payment intent
|-- POST /payments with header Idempotency-Key: {key}
|-- Server behavior:
|   |-- First request with key: process payment, store (key, response, status_code), return response
|   |-- Subsequent requests with same key: return cached response, same HTTP status code
|   |-- Key collision (same key, different request body): return 422 Conflict
|-- Key scope: per merchant account (not global — prevents cross-merchant DoS)
|-- Key TTL: 24 hours minimum (long enough for client retry logic)

Dual Control / Four-Eyes Principle:
|-- High-value transactions > $10,000 require two authorized approvers
|-- Same approver cannot both initiate and approve (separation of duty)
|-- Implementation: state machine (PENDING -> APPROVED_BY_A -> APPROVED_BY_B -> EXECUTED)

Transaction Signing (Non-Repudiation):
|-- Each transaction signed by sender's private key: ECDSA P-256 or Ed25519
|-- Signature covers: amount, currency, recipient, timestamp, nonce
|-- Verification at each hop: gateway, processor, settlement — signature chain intact
```

### Open Banking Security (PSD2/PSD3 + FAPI)

```
Strong Customer Authentication (SCA) — PSD2 Article 97:
|-- Dynamic linking: authentication code must be specific to amount + payee
|   |-- MUST: display "Pay $1,250.00 to Acme Corp?" with amount-specific code
|-- Two independent factors from:
|   |-- Knowledge: password, PIN | Possession: TOTP, FIDO2 key | Inherence: fingerprint, face
|-- Exemptions: low-value <€30, whitelisted beneficiaries, recurring, low-risk, corporate payments

FAPI Security Profiles:
|-- FAPI 1.0 Advanced (current PSD2): OAuth 2.0 + OIDC, private_key_jwt, PAR, JARM, MTLS/DPoP
|-- FAPI 2.0 (PSD3 direction): DPoP sender constraining, RAR (Rich Authorization Requests), grant management
|-- eIDAS Certificates: QWAC for TLS client auth, QSealC for request signing, QTSP issuance
|-- TPP revocation: OCSP/CRL checking before every API call
```

### Payment Infrastructure Security

```
ISO 8583 Message Security:
|-- MAC protects message integrity between acquirer and issuer
|-- Key hierarchy: ZMK (key exchange) -> ZPK (PIN encryption)
|-- Field-level: PIN block (ISO 9564 Format 0/1/3), track data encryption

HSM Architecture (Thales Payshield / Utimaco):
|-- PIN translation: HSM decrypts with ZPK -> encrypts with issuer's ZPK
|-- PIN verification: PVV (PIN Verification Value) or IBM 3624 offset
|-- CVV/CVC generation: from PAN + expiration + service code + CVK pair
|-- Key ceremony: dual control, split knowledge (m-of-n shares), tamper-evident bags
|-- Compliance: FIPS 140-2 Level 3 minimum, PCI PTS HSM certification

EMV Security:
|-- Offline Data Auth: SDA (weak, cloneable) -> DDA (challenge-response, stronger) -> CDA (strongest)
|-- Chip authentication: dynamic cryptogram (ARQC) per transaction
|-- Contactless: limit without CVM, relay attack mitigation via timing-based proximity checks
```

### Financial Regulatory Cybersecurity

```
US Regulatory Landscape:
|-- FFIEC CAT: 5 domains, 5 maturity levels (Baseline to Innovative), self-assessment
|-- NYDFS 23 NYCRR 500: annual certification, CISO, risk assessment, pen testing, 72h incident notification
|-- GLBA Safeguards Rule: applies to non-bank financial institutions (fintech, lenders)

EU Regulatory Landscape:
|-- DORA (Digital Operational Resilience Act) — Effective Jan 2025:
|   |-- ICT risk management, major incident reporting, TLPT (threat-led penetration testing),
|       critical third-party provider oversight, cyber threat information sharing
|-- DORA applies to: banks, payment institutions, e-money, investment firms, crypto-asset providers, insurers
```

### Payment Card Breach Response

```
T=0: Breach Awareness:
|-- Engage PCI Forensic Investigator (PFI) — do NOT investigate internally first
|-- Preserve forensic evidence: disk images, memory dumps, network captures
|-- Stop data loss but do NOT power off systems (loses memory forensics)

T=0-24h: Containment + Assessment:
|-- Scope: systems with cardholder data during compromise window
|-- Data at risk: PANs, expiration dates, cardholder names — if track/CVV exposed, highest severity
|-- Document: timeline, affected systems, data elements, containment actions

T=24-72h: Card Brand Notification:
|-- Visa: 3 business days | Mastercard: immediately | Others: per brand rules
|-- Provide: acquiring BINs, compromise window, estimated cards at risk, containment status

Post-Breach:
|-- PFI investigation report, remediation per findings, re-certification (new ROC/AOC)
|-- State breach notification (30-60 days typical), data subject notification
|-- Uplift: monthly scans, pen testing, enhanced monitoring
```

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| General application security, OWASP Top 10, secure SDLC | security-engineer | AppSec basics (XSS, SQLi, CSRF in payment apps), secure coding standards |
| Identity verification, authentication architecture, IAM | iam-architect | Customer identity proofing (KYC), authN/authZ for CDE, MFA implementation |
| Compliance audit management, regulatory exam preparation | compliance-officer | PCI assessment coordination, regulatory filing (SAR), audit evidence collection |
| Accounting/financial controls, reconciliation, SOX | accountant | Financial transaction reconciliation, dual control for financial systems |
| Cryptographic algorithm selection, key management | cryptography-engineer | HSM key ceremonies, TLS configuration, tokenization algorithm design |
| Incident response coordination, SOC integration | incident-responder | Joint response to payment card breach, forensic investigation workflow |
| Third-party vendor risk management | compliance-officer | Processor due diligence, PCI DSS validation for service providers |
| Data pipeline for fraud analytics, real-time streaming | data-engineer | Kafka/Flink for fraud signal pipeline, feature store for ML features |
| ML model development for fraud detection | ml-ai-engineer | XGBoost/Graph ML models, feature engineering, model monitoring for drift |
| Open banking API design, developer portal | api-designer | RESTful API design for PSD2 compliance, developer experience for TPPs |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Payment API endpoint defined AND no idempotency key mechanism | [ALERT] Payment endpoints require idempotency keys to prevent duplicate charges. Implement: client-generated UUID, server-side deduplication, 24h TTL. |
| P2 | Cardholder data stored AND no tokenization or encryption at rest | [ALERT] PCI DSS Req 3.4 requires PAN rendered unreadable. Implement tokenization (preferred) or encryption with documented key management. |
| P3 | CDE defined AND no network segmentation from corporate network | [ALERT] PCI DSS Req 1 requires segmentation to reduce CDE scope. Implement firewall with deny-all-default rules between CDE and corporate network. |
| P4 | High-risk customer onboarded AND no EDD documentation | [ALERT] Enhanced Due Diligence required: source of wealth, source of funds, adverse media, PEP check. Document before account activation. |
| P5 | Transaction value >$10,000 AND single approval | [WARN] Dual control/four-eyes principle for high-value transactions. Implement two-approver workflow with separation of duties. |
| P6 | SCA implementation AND only SMS OTP for possession factor | [WARN] SMS OTP vulnerable to SIM swap. Add app-based TOTP or FIDO2/WebAuthn as primary possession factor for high-value transactions. |

## What Good Looks Like

```
PCI DSS Architecture:                     Fraud Detection Pipeline:
  ┌────────────┐                           ┌──────────┐    ┌──────────┐
  │  Internet  │                           │Transaction│───>│ Signal   │
  └─────┬──────┘                           │  Events  │    │ Pipeline │
        │                                  └──────────┘    └────┬─────┘
  ┌─────┴──────┐                                                 │
  │    CDE     │  CDE: Tokenized PAN    ┌────────────────────────┴──────────┐
  │ ┌────────┐ │  Encrypted at rest      │  ┌───────────┐  ┌──────────────┐ │
  │ │Payment │ │  TLS 1.2+ in transit    │  │Velocity   │  │ML Anomaly    │ │
  │ │  App   │ │  MFA for all access     │  │Checks     │  │Detection     │ │
  │ └───┬────┘ │  Audit logs -> SIEM     │  └─────┬─────┘  └──────┬───────┘ │
  │     │      │                         │        └────────┬──────┘         │
  └─────┼──────┘                         └─────────────────┼────────────────┘
        │                                                  │
  ┌─────┴──────┐   Firewall                          ┌─────┴──────┐
  │ Corporate  │   Deny all default                  │ Real-time  │
  │  Network   │                                     │ Decision   │
  └────────────┘                                     │ ALLOW/     │
                                                     │ CHALLENGE/ │
  Payment API:                                       │ BLOCK      │
  Idempotency keys on every POST.                    └────────────┘
  Dual control for >$10K.
  Transaction signing.                                Result:
                                                      <200ms p99 latency.
  Open Banking:                                       Fraud rate <0.1%.
  SCA with dynamic linking.                           PCI DSS compliant.
  FAPI 2.0 with DPoP.                                 Regulator-ready at
  eIDAS QWAC + QSealC.                               any examination.
```

## Deliberate Practice

```
Scenario 1: Fintech startup processing payments via Stripe. 50K monthly transactions.
No security team. Founder asks: "Are we PCI compliant?"
  Week 1: Determine SAQ type — Stripe-hosted checkout = SAQ A (24 requirements).
         Verify: no CHD touches your servers, tokenization used, TLS everywhere.
  Week 2: SAQ A self-assessment. Most requirements met by Stripe's compliance.
         Gap: your employee devices access Stripe dashboard = need MFA on Stripe accounts.
  Week 3: Implement MFA, document security policies, complete SAQ A.
         Register with card brands (Visa/Mastercard) if required.
  Week 4: Set up quarterly vulnerability scans (Req 11), annual security awareness training (Req 12).

Scenario 2: Regional bank expanding to open banking under PSD2. Need dedicated interface for TPPs.
  Week 1: Architecture: TPP onboarding, eIDAS certificate validation, OAuth 2.0 + OIDC flow.
  Week 2: FAPI 1.0 Advanced: implement PAR, JARM, private_key_jwt client auth, MTLS.
  Week 3: SCA with dynamic linking: amount + payee displayed, TOTP for possession factor.
  Week 4: TPP revocation handling, rate limiting, API monitoring. Conformance suite testing.
```

## Gotchas -- Highest-Value Content

### PCI DSS Gotchas

*   **Assuming a cloud provider's PCI compliance makes you compliant.** AWS/Azure/GCP are PCI DSS compliant as infrastructure — but you are responsible for compliance *in* the cloud. The shared responsibility model means: cloud provider secures the physical data center and hypervisor (Req 9), you secure your AMI configurations, network ACLs, IAM policies, and application code (Req 1-8, 10-12). **Total cost: $100K-$500K in remediation costs + $50K-$200K in fines when you fail your assessment because someone assumed "AWS is PCI compliant so we are."**

*   **CDE scope creep — the "just this one integration" problem.** Start with a small CDE (payment app + DB). Marketing wants transaction data in Salesforce. Support wants it in Zendesk. Analytics wants raw data in Snowflake. Each integration expands the CDE and adds 50+ new PCI requirements. CDE scope naturally grows unless actively constrained. **Total cost: $200K-$1M in additional compliance costs per year per expanded system. Each new system in CDE adds ~$50K-$100K in annual assessment and maintenance costs.**

*   **Storing cardholder data "just in case" for analytics or chargebacks.** Every stored PAN is a liability under PCI DSS. Tokenization eliminates this: use network tokens (Visa VTS, Mastercard MDES), acquirer tokens, or gateway tokens. The only PAN you need is the BIN + last 4 for customer recognition. **Total cost: $1M-$10M in breach costs if PANs are exposed versus $0 in breach liability if only tokens are exposed (tokens are worthless outside your merchant account).**

### Fraud Detection Gotchas

*   **Static velocity thresholds that don't adapt to user behavior.** A rule "block >5 transactions/hour" works until a legitimate user makes 6 purchases during a flash sale. False positives cost more than fraud — a blocked legitimate customer has a 30% chance of never returning. Use Z-score against rolling 30-day average instead of fixed thresholds. **Total cost: $500K-$2M/year in lost customer lifetime value from false positive blocks.**

*   **ML model trained on biased historical data.** If your historical fraud labels are biased (e.g., more investigations triggered in certain ZIP codes), the ML model learns and amplifies that bias. Fraud models can become de facto redlining tools. Monitor approval rates by protected demographic dimensions — if any group has approval rate <90% of population average, investigate. **Total cost: $5M-$50M in regulatory fines (fair lending violations) + class action lawsuits + reputational damage.**

### KYC/AML Gotchas

*   **Treating PEP screening as a one-time onboarding check.** PEP status changes — a customer becomes a PEP mid-relationship (elected official, appointed minister, promoted executive at state-owned enterprise). Periodic rescreening (minimum: annually, high-risk: quarterly) catches status changes. **Total cost: $500K-$5M in fines for failure to detect PEP post-onboarding + reputational damage from banking a sanctioned PEP.**

*   **SAR filing deadlines are absolute — "we're still investigating" is not a defense.** The 30-day clock starts when you identify suspicious activity, not when the investigation is complete. File a preliminary SAR with what you know, then file a supplemental SAR within 30 days with additional findings. FinCEN and other FIUs penalize late filings regardless of eventual completeness. **Total cost: $500K-$5M per late SAR + heightened regulatory scrutiny (potential monitorship, $1M-$10M/year).**

### Open Banking Gotchas

*   **Implementing SCA without dynamic linking.** Requesting "Enter your OTP: 123456" without displaying the transaction amount and payee fails PSD2 dynamic linking. A customer entering 123456 thinking they are paying Amazon $25 could actually be authorizing a $2,500 payment to a fraudster. The authentication code must be transaction-specific. **Total cost: $1M-$5M in fraud losses from SCA bypass + regulatory enforcement for non-compliant SCA.**

*   **FAPI 1.0 Advanced certificate validation without CRL/OCSP checking.** TPPs are identified by eIDAS certificates. If a TPP's certificate is revoked (security breach, license revocation, bankruptcy), failing to check CRL/OCSP means the revoked TPP continues accessing customer accounts. Certificate validation at every API call is non-negotiable. **Total cost: $2M-$10M in fraud losses from unauthorized access by revoked TPP + regulatory fines for access control failure.**

### Payment API Gotchas

*   **Using database transactions as idempotency.** A DB-level unique constraint on transaction_id prevents duplicate writes but does NOT return the original response. The client retrying sees "409 Conflict" instead of the original "200 OK" with the payment result. The client assumes failure and initiates a refund or chargeback. Idempotency requires returning the stored response, not just preventing duplicates. **Total cost: $100K-$500K in operational overhead from confused clients, unnecessary chargebacks, and reconciliation nightmares.**

*   **Deploying transaction signing without clock synchronization.** Digital signatures include a timestamp to prevent replay. If the signing server's clock drifts by 5 minutes, all signatures appear expired or future-dated. Transaction signing infrastructure needs NTP with <1 second accuracy and monotonic clock for ordering. **Total cost: $1M-$5M in transaction processing outage per hour of downtime — payment systems cannot "degrade gracefully" when signing fails.**

## Verification

After implementing financial security controls, run this sequence. Do not proceed past a failure.

1.  **PCI DSS readiness:** Run approved scanning vendor (ASV) scan on all external CDE IPs — zero vulnerabilities scoring >=4.0 CVSS. Internal vulnerability scan quarterly — all HIGH and CRITICAL remediated within SLA. Penetration test annually — all findings addressed or risk-accepted.
2.  **Idempotency test:** Send duplicate payment request with same idempotency key — verify same response returned, second charge NOT processed. Send duplicate key with different request body — verify 422 Conflict returned.
3.  **Fraud detection test:** Inject known fraud pattern (velocity threshold crossing, impossible travel, card testing sequence) — verify detection and appropriate action (block/challenge). False positive rate monitored and within tolerance.
4.  **SCA compliance:** Verify two independent factors required for payment initiation. Verify dynamic linking: OTP code tied to specific amount + payee. Verify exemptions properly implemented and logged.
5.  **KYC/AML:** Verify CDD for all active accounts. Verify EDD for all high-risk accounts. SAR filing SLA met: no SAR older than 30 days without filing or documented 60-day extension. Sanctions screening completed at onboarding and within last week.
6.  **CDE segmentation:** Verify no CDE system accessible from corporate network without MFA + jump host. Verify firewall rules deny all by default. Verify cardholder data absent from non-CDE systems (run PAN scan on corporate file shares).
7.  **Incident response:** Breach response plan tested in last 6 months. PCI Forensic Investigator contact information current. Card brand notification templates ready. Tabletop exercise completed with findings addressed.

If any check fails: diagnose from checklist, provide specific actionable fix, restart verification from failed item.

## References

*   [PCI SSC: PCI DSS 4.0 Standard](https://www.pcisecuritystandards.org/document_library/) — Full 12 requirements, SAQ types, ROC template
*   [PCI SSC: Tokenization Product Security Guidelines](https://www.pcisecuritystandards.org/documents/Tokenization_Product_Security_Guidelines.pdf) — Token generation, mapping, and vault security
*   [FFIEC Cybersecurity Assessment Tool (CAT)](https://www.ffiec.gov/cyberassessmenttool.htm) — 5-domain maturity assessment for financial institutions
*   [OpenID Foundation: FAPI 2.0 Security Profile](https://openid.net/specs/fapi-2_0-security-profile.html) — Financial-grade API security profile for open banking
*   [FinCEN: SAR Filing Requirements](https://www.fincen.gov/resources/filing-information) — Suspicious Activity Report forms, instructions, deadlines
*   [/references/pci-dss-4-implementation.md](references/pci-dss-4-implementation.md) — 12 requirements mapped to implementation with SAQ selection
*   [/references/fraud-detection-architecture.md](references/fraud-detection-architecture.md) — Signal pipeline, velocity checks, ML scoring, decision engine
*   [/references/kyc-aml-program.md](references/kyc-aml-program.md) — CDD/EDD framework, sanctions screening, SAR filing, PEP detection
*   [/references/transaction-security-patterns.md](references/transaction-security-patterns.md) — Idempotency, dual control, signing, compensating transactions
*   [/references/open-banking-security.md](references/open-banking-security.md) — PSD2 SCA, FAPI profiles, eIDAS, TPP management
*   [/references/payment-infrastructure-security.md](references/payment-infrastructure-security.md) — ISO 8583, HSM, EMV, contactless security
*   [/references/financial-regulations.md](references/financial-regulations.md) — FFIEC CAT, NYDFS, DORA, GLBA compliance mapping
*   [/references/secure-enclave-finance.md](references/secure-enclave-finance.md) — Nitro Enclaves, confidential computing for payments and KYC
*   [/scripts/verify-skill.sh](scripts/verify-skill.sh) — Verify all 14 required sections, ground rules, decision trees, gotchas, and references
