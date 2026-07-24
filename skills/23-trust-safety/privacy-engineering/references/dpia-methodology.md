# DPIA Methodology

Full Data Protection Impact Assessment template with risk scoring
and mitigation tracking aligned with GDPR Article 35 requirements
and WP29/EDPB guidelines.

## DPIA Trigger Assessment

Checklist to determine if DPIA is legally required:

| Criterion | Threshold | Examples |
|-----------|-----------|----------|
| Systematic profiling | Automated processing with legal/significant effects | Credit scoring, hiring algorithms, insurance underwriting |
| Large-scale special category data | Processing health, biometric, genetic, political, religious, sexual orientation data | Hospital patient records, biometric access systems, political affiliation databases |
| Systematic monitoring of public areas | CCTV at scale, video analytics, automated license plate readers | City-wide surveillance, shopping mall tracking, workplace monitoring |
| New technologies | AI/ML, IoT, facial recognition, blockchain with personal data | Emotion detection in call centers, smart home devices with voice data |
| Vulnerable data subjects | Children, employees, patients, elderly, asylum seekers | Edtech platforms, employee monitoring software, care home systems |
| Large-scale criminal data | Convictions and offenses | Background check services, tenant screening |
| Combined datasets | Linking data from multiple sources beyond expectations | Data broker enrichment, cross-platform tracking, identity graphs |

## DPIA Template Structure

### Section 1: Processing Description
- Controller name and DPO contact
- Purpose of processing (specific, not generic)
- Categories of personal data (with special category flags)
- Categories of data subjects
- Categories of recipients (internal + third parties + countries)
- Data retention periods per category
- Technical and organizational security measures
- Data flows (architecture diagram with all stores)

### Section 2: Necessity & Proportionality Assessment
- Why is this processing necessary to achieve the purpose?
- What less intrusive alternatives were considered and rejected?
- Is the data minimized (least amount needed)?
- Is pseudonymization used where full identification unnecessary?
- How is data accuracy maintained?
- How are data subjects informed of processing?

### Section 3: Risk Identification
For each risk, score Likelihood (1-5) and Impact (1-5):

| Risk ID | Description | Likelihood | Impact | Inherent Risk | Mitigation | Residual Risk |
|---------|-------------|------------|--------|--------------|------------|---------------|
| R-001 | Unauthorized access to health data | 3 | 5 | 15 | Encryption, IAM, audit logging | 6 |
| R-002 | Re-identification of pseudonymized analytics | 4 | 4 | 16 | k-anonymity (k=5), access controls | 8 |

### Section 4: Mitigation Measures
Per risk, document: what, who, by when, verification method

### Section 5: DPO Consultation & Sign-off
- DPO consulted: [Date]
- DPO recommendation: [Proceed / Proceed with conditions / Do not proceed]
- DPO conditions: [List]
- Senior management sign-off: [Name, Title, Date]
- Next review date: [Date, max 3 years from sign-off]

## Prior Consultation Trigger (Article 36)

If residual risk remains HIGH after mitigation AND no measures
available to reduce it: MANDATORY prior consultation with DPA.
Processing must not begin until DPA responds (may take 8 weeks,
extendable to 14). Document the consultation request and response.
