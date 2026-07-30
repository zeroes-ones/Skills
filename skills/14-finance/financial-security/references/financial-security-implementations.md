# Financial Security — Full Implementation Reference

Extracted body sections for progressive disclosure. Loaded on demand.

---

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: PCI DSS Scoping

        ┌── INPUT: Does the system touch cardholder data?
        │
   ┌────┴────────────┐
   │                 │
   ▼                 ▼
In CDE            Outside CDE
   │                 │
   ▼                 ▼
Full PCI DSS       Connected or
assessment        segmentable?
   │            ┌───┴───┐
   ▼            │       │
SAQ D/RoC       ▼       ▼
validate all  Connected  Isolated
12 requirements  │         │
                 ▼         ▼
              In scope   Out of scope
              SAQ D-SP   No assessment
              segment
              with firewall

### Decision Tree 2: Fraud Detection Stack Selection

        ┌── INPUT: What is your fraud detection maturity?
        │
   ┌────┴────────────────────┐
   │                         │
   ▼                         ▼
Launching (no labels)       Scaling (have chargeback data)
   │                         │
   ▼                         ▼
Rule-based detection        ML + Rules hybrid
Velocity, device, geo       XGBoost supervised + rules fallback
   │                         │
   ▼                         ▼
Score < 20 → ALLOW          A/B test ML against
Score 20-60 → CHALLENGE     rules-only baseline
Score > 60 → BLOCK          Deploy winner to production
   │                         │
   ▼                         ▼
Collect labels 6-8 weeks    Add graph ML for fraud rings
before transitioning        when cross-account patterns emerge

### Decision Tree 3: KYC Risk Tier Assignment

        ┌── INPUT: New customer — assess onboarding risk
        │
   ┌────┴────────────┬──────────┬──────────┐
   │                 │          │          │
   ▼                 ▼          ▼          ▼
PEP or              FATF      Sanctions   High-risk
close associate     country   list hit    industry
   │                 │          │          │
   ▼                 ▼          ▼          ▼
EDD required        EDD        BLOCK +    EDD
Verify source       required   file SAR   required
of wealth/funds     Enhanced               │
   │                monitoring             ▼
   ▼                   │              Verify UBOs
Senior mgmt           ▼              (≥25% ownership)
approval for       Periodic          Ongoing review
PEP onboarding     review 6-12mo     every 6-12 months


## Fraud Detection Architecture
<!-- STANDARD: 3min -->

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


## KYC/AML Program Design
<!-- STANDARD: 3min -->

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


## Payment API Security
<!-- STANDARD: 3min -->

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


## Open Banking Security (PSD2/PSD3 + FAPI)
<!-- STANDARD: 3min -->

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


## Payment Infrastructure Security
<!-- STANDARD: 3min -->

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


## Financial Regulatory Cybersecurity
<!-- STANDARD: 3min -->

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


## Payment Card Breach Response
<!-- STANDARD: 3min -->

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


