# KYC/AML Program Design

CDD/EDD framework, sanctions screening integration, SAR filing
procedures, PEP detection and monitoring for financial crime compliance.

## Customer Due Diligence (CDD) — Core Program

Minimum required for ALL customers before account activation:

### Identity Verification
- Individual: government-issued photo ID + selfie with liveness detection
- Business: incorporation documents, business license, operating agreement
- Address verification: utility bill, bank statement, or digital verification

### Beneficial Ownership (FinCEN CDD Rule — 25% threshold)
- Any individual owning >=25% of legal entity (ownership prong)
- Any individual with significant control (control prong — CEO, CFO, COO, etc.)
- Collect: name, DOB, address, SSN/TIN (for US), government ID
- Verify: reasonable belief of accuracy (documentation or reliable source)

### Risk Rating (Assign at Onboarding)
| Risk Factor | Low Risk | Medium Risk | High Risk |
|------------|----------|-------------|-----------|
| Geography | FATF compliant, low corruption | Moderate corruption index | High-risk jurisdiction, sanctions risk |
| Business/Profile | Salary employee, long-term resident | Self-employed, freelancer | MSB, crypto, cash-intensive, PEP |
| Product | Basic checking/savings | Credit products, brokerage | Cross-border wires, private banking, correspondent |
| Channel | In-person, branch | Digital with strong IDV | Non-face-to-face with weak IDV |

## Enhanced Due Diligence (EDD) — High-Risk Only

Required for all HIGH-risk customers before and during relationship:

### Source of Wealth (How did they accumulate total wealth?)
- Documentation: tax returns (3 years), audited financials, business sale docs
- Verify consistency: wealth aligns with occupation and age
- Red flags: sudden wealth without explanation, wealth exceeding career earnings

### Source of Funds (Where did THIS specific money come from?)
- Documentation: bank statement showing funds origin, pay stub, sale contract
- For wires: originator bank statement, purpose of transfer
- Red flags: third-party funder, cash deposits without source, crypto conversion

### PEP Screening (Politically Exposed Persons)
- Screen at onboarding: customer + beneficial owners + family members
- Definition: senior official (executive, legislative, judicial, military, SOE)
- Family: spouse, children, parents, siblings
- Close associates: known business partners, beneficial co-owners
- NOT prohibited — EDD required, not denial

### Adverse Media Screening
- Negative news in local language + English
- Categories: financial crime, corruption, sanctions, terrorism, human rights
- Automated + manual review for high-risk matches
- Ongoing monitoring: rescreen on trigger events (negative news alert)

## Sanctions Screening

### Lists to Screen (at minimum)
- OFAC SDN List, FSE List, SSI List (US)
- UN Consolidated Sanctions List
- EU Consolidated Financial Sanctions List
- UK HMT Financial Sanctions List
- Local country sanctions lists

### Screening Schedule
- Onboarding: before account activation
- Transaction: real-time screening of sender and recipient
- Periodic: daily batch rescreen of entire customer base
- Trigger: within 24 hours of sanctions list update

### Match Handling
- Exact match: block transaction, freeze account, file report to OFAC/authority
- Fuzzy match (90%+ confidence): manual review by compliance analyst
- Partial match (<90%): log for audit, no action unless pattern emerges

## Suspicious Activity Reporting (SAR)

### SAR Triggers (File if ANY apply)
- Structuring: transactions just below $10,000 threshold
- Unexplained wealth: deposits inconsistent with profile
- Rapid movement: high-velocity transfers between accounts/countries
- Terrorist financing indicators: specific patterns per FinCEN guidance
- Cyber crime: ransomware payments, business email compromise proceeds
- Elder financial exploitation

### Filing Deadlines (US — FinCEN)
- Discovery: 30 calendar days from identifying suspicious activity
- Extension: additional 30 days (60 total) if suspect not identified
- No SAR decision: 30 days to document why no SAR was filed
- Safe harbor: SAR filing protects from civil liability (31 USC 5318(g)(3))

### SAR Content
- Narrative: who, what, when, where, why, how
- Supporting documentation: transaction records, account statements
- Subject information: full identity, known associates, accounts
- Law enforcement contact: if LEA already involved
