# Cross-Border Data Transfers

SCC module selection, Transfer Impact Assessment methodology,
supplementary measures, and DPF certification requirements
post-Schrems II (CJEU C-311/18, July 2020).

## Valid Transfer Mechanisms (GDPR Chapter V)

### Article 45: Adequacy Decisions
Countries with full adequacy: Andorra, Argentina, Canada (commercial),
Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New
Zealand, Republic of Korea, Switzerland, United Kingdom (post-Brexit),
Uruguay. Partial: US (DPF only for certified companies).

Data flows to adequacy countries = treated as within EEA. No
additional safeguards required beyond standard GDPR compliance.

### Article 46: Appropriate Safeguards (No Adequacy Decision)

**Standard Contractual Clauses (SCCs 2021)**:
- Module 1: Controller to Controller (C2C)
- Module 2: Controller to Processor (C2P) — most common SaaS pattern
- Module 3: Processor to Processor (P2P) — sub-processor chain
- Module 4: Processor to Controller (P2C)
- SCCs cannot be modified except annexes. No redlining allowed.

**Binding Corporate Rules (BCRs)**:
- For intra-group transfers within multinational corporations
- Requires DPA lead authority approval (12-18 month process)
- Must be legally binding, enforceable by data subjects
- Annual compliance audit required

### Article 49: Derogations (Narrow Exceptions)
Explicit consent (informed of risks, no adequate safeguards),
contract necessity, vital interests, public interest, legal claims.
Cannot be used for routine/repetitive transfers.

## Transfer Impact Assessment (TIA) — Six-Step Methodology

Following EDPB Recommendations 01/2020:

### Step 1: Know Your Transfers
Map: what personal data, which categories, to which country, to whom
(controller/processor), for what purpose, under which transfer tool.

### Step 2: Verify the Transfer Tool
Confirm SCCs are signed, BCRs approved, or adequacy decision applies.
Check that the tool covers all parties in the transfer chain.

### Step 3: Assess Third Country Law
Evaluate whether the recipient country's laws on government access
to data (surveillance, national security) undermine the transfer
tool's effectiveness. Key factors from Schrems II:
- Is government access limited to what is necessary and proportionate?
- Do data subjects have effective judicial redress?
- Is there independent oversight of surveillance activities?

### Step 4: Identify Supplementary Measures
If Step 3 identifies gaps, apply measures:
- **Technical**: encryption-at-rest with customer-held keys (CSE),
  pseudonymization with separated key management, split/multi-party
  processing (no single jurisdiction holds complete data)
- **Organizational**: warrant canary, transparency reports,
  commitment to challenge unlawful surveillance requests
- **Contractual**: enhanced SCC provisions where local law permits

### Step 5: Document the TIA
Write TIA report documenting each step, findings, supplementary
measures, and conclusion. This is your evidence of compliance.

### Step 6: Re-assess Periodically
Review TIA when: new surveillance law in recipient country, new
third-party in transfer chain, CJEU/DPA ruling affecting transfer
tools. Minimum: annual review.

## EU-US Data Privacy Framework (DPF)

- Effective July 2023, replacing invalidated Privacy Shield
- US companies must self-certify annually at dataprivacyframework.gov
- Verify certification before transferring data — list is public
- DPF currently under legal challenge (NOYB filed challenge Sept 2023)
- Recommendation: maintain SCC fallback for all DPF transfers
- UK Extension to DPF effective October 2023 (UK-US Data Bridge)
