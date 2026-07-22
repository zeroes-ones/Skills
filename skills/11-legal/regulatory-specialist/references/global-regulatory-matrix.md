---
name: global-regulatory-matrix
description: Global regulatory landscape matrix: GDPR, CCPA, PIPEDA, LGPD, PDPA, PIPL, plus FinTech and HealthTech regulations.
author: Sandeep Kumar Penchala
---

# Global Regulatory Matrix

Reference map of major data protection and industry-specific regulations across jurisdictions.
Covers scope, key requirements, enforcement, and cross-reference by data type, industry, and geography.

## 1. Data Protection Regulations — Overview

| Regulation | Jurisdiction | Effective | Max Penalty | Territorial Scope |
|------------|-------------|-----------|-------------|-------------------|
| GDPR       | EU / EEA    | May 2018  | €20M or 4% global revenue | Any org processing EU residents' data |
| CCPA/CPRA  | California, USA | Jan 2020 / Jan 2023 | $7,500 per intentional violation | For-profit businesses meeting thresholds |
| PIPEDA     | Canada      | 2001 (amended 2018) | CAD $100K per violation | Commercial activities in Canada |
| LGPD       | Brazil      | Sep 2020  | 2% revenue (max BRL 50M) | Any org processing data in Brazil |
| PDPA       | Singapore   | 2012 (amended 2020) | SGD $1M or 10% turnover | Organizations in Singapore |
| Australian Privacy Act | Australia | 1988 (amended 2023) | AUD $50M or 30% turnover | APP entities, credit reporting |
| PIPL       | China       | Nov 2021  | RMB 50M or 5% revenue | Processing within China + targeting Chinese residents |
| PDPB       | India       | Aug 2023  | INR 250 Cr (~$30M) | Processing within India + offering goods/services to Indians |

## 2. GDPR Deep Dive

### 2.1 Key Principles (Article 5)
- **Lawfulness, fairness, transparency**: must have legal basis; must tell people what you do with their data
- **Purpose limitation**: collect for specified, explicit, legitimate purposes; no incompatible repurposing
- **Data minimization**: adequate, relevant, limited to what is necessary
- **Accuracy**: reasonable steps to keep data accurate and up to date
- **Storage limitation**: keep no longer than necessary for the purpose
- **Integrity and confidentiality**: appropriate security (encryption, pseudonymization)
- **Accountability**: YOU are responsible for demonstrating compliance

### 2.2 Legal Bases for Processing (Article 6)
1. **Consent**: freely given, specific, informed, unambiguous; must be as easy to withdraw as to give
2. **Contractual necessity**: processing necessary to perform a contract with the data subject
3. **Legal obligation**: processing necessary for compliance with law
4. **Vital interests**: protect someone's life
5. **Public interest**: official authority or public interest task
6. **Legitimate interests**: necessary for your or a third party's legitimate interests (requires balancing test)

### 2.3 Data Subject Rights (Articles 12–23)
| Right              | What It Means                                                 | Response Time |
|--------------------|---------------------------------------------------------------|---------------|
| Right to be informed | Privacy notice at collection                                  | At collection |
| Right of access     | Confirm if processing, provide copy of data                   | 1 month        |
| Right to rectification | Correct inaccurate data, complete incomplete data          | 1 month        |
| Right to erasure    | "Right to be forgotten" — delete data under certain conditions | 1 month       |
| Right to restrict   | Limit processing while disputes or verification pending       | 1 month        |
| Data portability    | Receive data in structured, machine-readable format           | 1 month        |
| Right to object     | Object to processing based on legitimate interest or direct marketing | 1 month  |
| Automated decision-making | Right not to be subject to solely automated decisions with legal/significant effects | N/A |

### 2.4 Key Operational Requirements
- **DPO (Data Protection Officer)**: required if public authority, large-scale systematic monitoring, or large-scale sensitive data
- **DPIA (Data Protection Impact Assessment)**: required for high-risk processing (new tech, large-scale, profiling)
- **Data Processing Agreements (DPA)**: required with all processors; must include specific clauses per Article 28
- **Breach notification**: notify supervisory authority within 72 hours; notify data subjects if high risk
- **Cross-border transfers**: adequacy decision, Standard Contractual Clauses (SCCs), Binding Corporate Rules (BCRs), or derogations
- **Records of processing**: maintain ROPA (Record of Processing Activities) documenting all processing

## 3. CCPA / CPRA Deep Dive

### 3.1 Who Must Comply
- Annual gross revenue > $25M, OR
- Buy/sell/sell personal information of 100,000+ consumers/households, OR
- Derive 50%+ of annual revenue from selling personal information
- **CPRA adds**: sharing personal information counts toward thresholds

### 3.2 Consumer Rights
| Right              | CCPA (2020) | CPRA (2023) |
|--------------------|-------------|-------------|
| Right to know      | ✅          | ✅ (expanded) |
| Right to delete    | ✅          | ✅           |
| Right to opt-out   | Sale only   | Sale + sharing + automated decisions |
| Right to correct   | ❌          | ✅ (new)     |
| Right to limit use | ❌          | ✅ (sensitive PI) |
| Data portability   | Limited     | ✅ (expanded) |

### 3.3 Key Differences from GDPR
- **Opt-out, not opt-in**: consumers must be given the right to opt out of sale/sharing; consent not required before collecting (except for minors <16)
- **Do Not Sell/Share link**: must have clear link on homepage: "Do Not Sell or Share My Personal Information"
- **Global Privacy Control (GPC)**: must honor browser-based opt-out signals
- **Private right of action**: only for data breaches (CCPA); CPRA expands slightly
- **Sensitive personal information**: new category under CPRA (SSN, precise geolocation, race, religion, health, biometrics, contents of communications)

## 4. Other Major Regulations

### 4.1 LGPD (Brazil)
- Very similar to GDPR in structure and rights
- 10 legal bases for processing (vs GDPR's 6)
- DPO required for all controllers (broader than GDPR)
- ANPD (Autoridade Nacional de Proteção de Dados) — Brazilian DPA
- Cross-border transfer rules similar to GDPR

### 4.2 PIPL (China)
- **Strictest consent requirements**: separate consent for sensitive data, cross-border transfers, public disclosure, and automated decision-making
- **Data localization**: personal data collected in China must be stored in China for certain volumes/types
- **Security assessment**: government assessment required before cross-border transfer of important data or large volumes of personal data
- **Carve-outs**: "national security" and "public interest" exceptions are broad
- **Enforcement**: aggressive — CAC (Cyberspace Administration of China) has broad powers

### 4.3 India DPDP Act 2023
- Consent-based framework with "deemed consent" for specific legitimate uses
- Data Fiduciaries (controllers) vs Data Principals (individuals)
- Significant Data Fiduciaries have enhanced obligations (impact assessment, DPO, independent auditor)
- Cross-border: government will whitelist countries; data flows to non-whitelisted countries restricted
- Data Protection Board of India for enforcement

## 5. FinTech Regulations

| Regulation        | Scope                             | Key Requirements                                    |
|-------------------|-----------------------------------|-----------------------------------------------------|
| PSD2 (EU) / PSD3  | Payment services in EU            | Strong Customer Authentication (SCA), open banking APIs (PSD2), fraud prevention (PSD3) |
| Open Banking (UK) | UK payment accounts               | CMA9 banks must provide open APIs for AIS (account info) and PIS (payment initiation) |
| SOX (US)          | Public companies                  | Internal controls over financial reporting, CEO/CFO certification, auditor independence |
| PCI DSS v4.0      | Cardholder data globally          | 12 requirements: network security, encryption, access control, monitoring, testing |
| AML/KYC           | Global (varies by country)        | Customer due diligence, suspicious activity reporting, sanctions screening |
| Dodd-Frank (US)   | US financial institutions         | Systemic risk oversight, consumer protection (CFPB), Volcker Rule |
| MiCA (EU)         | Crypto-assets in EU               | Licensing for CASPs, stablecoin reserve requirements, market abuse rules, consumer protection |

### 5.1 PCI DSS v4.0 — 6 Control Objectives

1. **Build and maintain secure network**: firewalls, no vendor defaults
2. **Protect cardholder data**: encrypt at rest (AES-256) and in transit (TLS 1.2+)
3. **Maintain vulnerability management**: anti-malware, secure coding, patch management
4. **Implement strong access control**: need-to-know, unique IDs, physical security
5. **Regularly monitor and test**: access logging, vulnerability scans (quarterly), penetration testing (annual)
6. **Maintain information security policy**: policy documentation, risk assessment (annual)

### 5.2 PSD2 SCA Requirements

**Strong Customer Authentication = 2 of 3:**
- **Knowledge**: something only the user knows (password, PIN)
- **Possession**: something only the user possesses (phone, hardware token)
- **Inherence**: something the user is (fingerprint, face)

**Exemptions to SCA:**
- Low-value transactions (<€30; cumulative up to €100 or 5 consecutive)
- Whitelisted trusted beneficiaries (user-designated)
- Recurring transactions (same payer, payee, amount)
- Corporate payment processes (dedicated protocols)
- Transaction risk analysis (low risk score from PSP)

## 6. HealthTech Regulations

| Regulation  | Jurisdiction | Scope                                       | Key Requirements                               |
|-------------|-------------|---------------------------------------------|------------------------------------------------|
| HIPAA       | US          | Protected Health Information (PHI)          | Privacy Rule, Security Rule, Breach Notification, BAAs |
| HITECH      | US          | Extended HIPAA to business associates       | Mandatory breach notification, enhanced penalties |
| FDA SaMD    | US          | Software as a Medical Device                | Classification (Class I/II/III), 510(k) or PMA, QSR, post-market surveillance |
| EU MDR      | EU          | Medical devices including software          | Classification (I/IIa/IIb/III), CE marking, clinical evaluation, PMS |
| DiGa (Germany) | Germany  | Digital health applications (prescribable apps) | BfArM listing, evidence of positive care effects, data security (BSI TR-03161) |
| DTAC (UK)   | UK          | Digital Technology Assessment Criteria      | NHS standards for digital health tech: clinical safety, data protection, interoperability, usability |

### 6.1 HIPAA Key Requirements
- **Privacy Rule**: limits on use/disclosure of PHI; patient rights (access, amendment, accounting)
- **Security Rule**: administrative, physical, and technical safeguards for ePHI
  - Administrative: risk analysis, workforce training, incident response
  - Physical: facility access, workstation security, device controls
  - Technical: access control, audit controls, integrity, transmission security
- **Breach Notification Rule**: notify affected individuals within 60 days; notify HHS; media notice if >500 individuals
- **Minimum Necessary**: use/disclose only the minimum PHI needed for the purpose
- **Business Associate Agreements (BAA)**: required with all vendors handling PHI

### 6.2 FDA Software as Medical Device (SaMD)

**Classification:**
- **Class I**: low risk (medical device data systems, health information systems) — general controls
- **Class II**: moderate risk (clinical decision support, diagnostic aid) — 510(k) premarket notification
- **Class III**: high risk (life-sustaining, AI diagnostic) — Premarket Approval (PMA)

**Key question:** Is your software a medical device?
- Intended to diagnose, cure, mitigate, treat, or prevent disease?
- Intended to affect the structure or function of the body?
- If yes + not just "general wellness" → regulated as medical device

## 7. Cross-Reference Matrix

### 7.1 By Data Type

| Data Type                  | GDPR      | CCPA/CPRA | HIPAA     | PCI DSS   |
|----------------------------|-----------|-----------|-----------|-----------|
| Names, emails, IPs         | ✅ PII    | ✅ PI     | N/A       | N/A       |
| Health/medical data        | ✅ Special category | ✅ Sensitive PI | ✅ PHI | N/A   |
| Financial/payment data     | ✅ PII    | ✅ PI     | N/A       | ✅ CHD    |
| Biometric data             | ✅ Special category | ✅ Sensitive PI | ✅ PHI (if in medical records) | N/A |
| Precise geolocation        | ✅ PII    | ✅ Sensitive PI | N/A   | N/A       |
| Children's data (<13)      | ✅ Enhanced consent | ✅ Opt-in | N/A    | N/A       |
| Criminal records           | ✅ Special category (with official authority) | N/A | N/A | N/A |
| SSN / government IDs       | ✅ PII    | ✅ Sensitive PI | N/A    | N/A       |
| Race, religion, ethnicity  | ✅ Special category | ✅ Sensitive PI | N/A | N/A       |

### 7.2 By Industry

| Industry        | Primary Regulations                                         | Secondary                          |
|-----------------|-------------------------------------------------------------|------------------------------------|
| SaaS / B2B      | GDPR + CCPA (data privacy), SOC 2 (security)               | ISO 27001, regional privacy laws   |
| FinTech          | PSD2/PSD3 (EU), PCI DSS, SOX, AML/KYC                      | GDPR, CCPA, Open Banking           |
| HealthTech       | HIPAA (US), EU MDR (EU), FDA (US, if device)               | GDPR, HITECH, DiGa (Germany)       |
| E-commerce       | GDPR, CCPA, PCI DSS                                        | Consumer protection laws, PSD2     |
| AdTech / MarTech | GDPR, CCPA, ePrivacy Directive (cookies)                   | DSA (EU), competition law          |
| AI / ML          | GDPR (automated decisions), EU AI Act, NYC Law 144 (HR)    | CCPA/CPRA, FTC guidelines           |
| EdTech           | GDPR, CCPA, COPPA (US, children), FERPA (US, education)    | State student privacy laws          |
| IoT              | GDPR, CCPA, NIST IoT guidelines, EU Cyber Resilience Act  | Product safety regulations          |

### 7.3 By Geography

| Geography     | Data Protection     | Financial         | Healthcare         | Sector-Specific     |
|---------------|---------------------|-------------------|---------------------|----------------------|
| EU            | GDPR, ePrivacy      | PSD2/PSD3, MiCA   | EU MDR, IVDR       | DSA, DMA, EU AI Act |
| US (federal)  | None (sectoral)     | SOX, Dodd-Frank   | HIPAA, HITECH      | COPPA, FCRA          |
| US (California)| CCPA/CPRA           | CalFinLaw         | CMIA               | CPRA regs            |
| Canada        | PIPEDA              | OSFI guidelines   | PHIPA (Ontario)    | CASL (anti-spam)     |
| Brazil        | LGPD                | BACEN regulations | ANVISA regulations | Marco Civil          |
| Singapore     | PDPA                | MAS TRM           | HIMSS guidelines   | Cybersecurity Act    |
| Australia     | Privacy Act 1988    | APRA CPS 234      | My Health Records  | Notifiable Data Breaches |
| China         | PIPL, DSL, CSL      | PBOC regulations  | NHC regulations    | CAC cross-border rules|
| India         | DPDP Act 2023       | RBI guidelines    | NHA guidelines     | IT Act, CERT-In      |
| Japan         | APPI                | FSA regulations   | PMD Act            | My Number Act        |

## 8. Compliance Program Framework

### 8.1 Essential Components
1. **Data mapping / inventory**: what data, where stored, who accesses, why collected, how long kept
2. **Privacy notices**: clear, accessible, compliant with each applicable regulation
3. **Consent management**: mechanism to collect, record, and honor consent preferences
4. **DSAR process**: intake, verification, data collection, response within statutory deadlines
5. **Vendor risk management**: assess all data processors/subprocessors; DPAs in place
6. **Incident response**: breach detection, containment, notification procedures
7. **Training**: role-based, annual, documented
8. **Audit and monitoring**: regular internal audits, compliance monitoring, continuous improvement

### 8.2 Practical Compliance Steps for Startups
1. Start with GDPR — it's the most comprehensive; most other frameworks are subsets
2. Build a data map (spreadsheet is fine for <50 employees)
3. Draft a privacy policy (clear, not copied from another company)
4. Set up cookie consent (if you have EU users, even if you're not in EU)
5. Get DPAs signed with critical vendors (hosting, analytics, CRM, email)
6. Implement DSAR process (at minimum: email address for requests + documented procedure)
7. Conduct annual risk assessment; document it
8. When you hit 50+ employees or $5M revenue → invest in GRC tooling

## References

- GDPR Full Text: https://gdpr-info.eu/
- ICO (UK DPA) Guidance: https://ico.org.uk/
- CCPA/CPRA: https://oag.ca.gov/privacy/ccpa
- PCI DSS v4.0: https://www.pcisecuritystandards.org/
- HIPAA for Developers: https://www.hhs.gov/hipaa/for-professionals/index.html
- EU AI Act: https://artificialintelligenceact.eu/
- OneTrust Compliance Resources: https://www.onetrust.com/resources/
- IAPP (International Association of Privacy Professionals): https://iapp.org/
