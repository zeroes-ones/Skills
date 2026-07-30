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

