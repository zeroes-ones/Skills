# Scale Depth: Clinic → Hospital → Health System → ACO

How healthcare security architecture scales from a solo practice to an
Accountable Care Organization managing millions of patient lives.

## Level 1: Solo Practice (1-5 providers, ~2,000 patients)

**Security posture:** Basic HIPAA compliance. Encryption on all endpoints.
Cloud EHR with BAA. No on-premises servers.
**Key concerns:**
- Is the EHR vendor's BAA signed and current?
- Are practice laptops encrypted (BitLocker/FileVault)?
- Is the WiFi network using WPA3 with guest isolation?
- Are patient portal credentials using MFA?
- Is there a documented breach notification contact list?
**Budget:** $500-2,000/year for security tools + EHR BAA-verified vendor.

## Level 2: Small Clinic (5-20 providers, ~10,000 patients)

**Security posture:** Standard HIPAA + basic network segmentation. On-premises
or hybrid infrastructure. Multiple clinical applications integrated.
**Adds over Level 1:**
- VLAN separation: clinical workstations vs. guest WiFi
- Centralized identity (Azure AD/Okta) with SSO to EHR
- PHI-aware DLP on email (block SSN/MRN in outbound)
- Annual security risk assessment (SRA) per HIPAA requirement
- Basic BAA registry (spreadsheet → formal tracker)
**Budget:** $5,000-15,000/year.

## Level 3: Mid-Size Practice (20-100 providers, ~50,000 patients)

**Security posture:** HITRUST CSF basics. Dedicated IT/security staff or MSP.
Multi-site connectivity. In-house or hosted PACS.
**Adds over Level 2:**
- Clinical network micro-segmentation (IoMT VLAN isolation begins)
- SIEM with PHI-aware log monitoring
- FHIR API gateway with OAuth 2.0 + SMART App Launch
- Formal vendor security assessment program
- Breach notification pipeline tested annually
- Medical device inventory with vulnerability scanning
**Budget:** $50,000-150,000/year + 1-2 FTE security staff.

## Level 4: Community Hospital (100-500 beds, ~200,000 patients)

**Security posture:** NIST CSF + HITRUST CSF r2 certified. 24/7 SOC (in-house
or MSSP). Regulatory scrutiny is real — OCR audits, state AG inquiries.
**Adds over Level 3:**
- Full IoMT segmentation: dedicated VLAN per device class, inline IPS
- FDA-aligned medical device cybersecurity program (CBOM, patching, EOL plans)
- De-identification program for research datasets
- 42 CFR Part 2 compliance for substance use disorder records
- Clinical continuity failover — security controls must never block care
- Cyber insurance with ransomware coverage
- Red team exercises annually
**Budget:** $500,000-$2M/year + 3-8 FTE security staff.

## Level 5: Health System (multiple hospitals, 500K-5M patients)

**Security posture:** HITRUST CSF r2 certified, NIST CSF Tier 4 (adaptive).
CISO reports to board. Dedicated healthcare security architecture team.
**Adds over Level 4:**
- Cross-entity PHI flow governance (M&A integration security)
- Multi-tenant BAA registry with sub-processor chain mapping
- HITRUST CSF control automation (evidence collection, continuous monitoring)
- Threat intelligence sharing (H-ISAC membership)
- Clinical engineering + IT security joint governance
- Population health analytics de-identification at scale
**Budget:** $3M-15M/year + 15-50 FTE security staff.

## Level 6: ACO / Health Plan (1M-50M covered lives)

**Security posture:** HITRUST CSF r2 certified with NIST CSF Tier 4. Regulatory
exposure is maximum — OCR, CMS, state AG, FTC, and class-action risk.
**Adds over Level 5:**
- Claims data PHI isolation (separate from clinical PHI)
- Multi-payer PHI segmentation (payer A must not access payer B member data)
- Real-time PHI flow monitoring across partners
- AI/ML model governance for PHI training data
- De-identification at population scale (Expert Determination certification)
- CMS interoperability rule compliance (Patient Access API, Provider Directory API)

## Key Scaling Principles

1. **BAA registry:** Spreadsheet at Level 1 → GRC platform at Level 5.
2. **Network segmentation:** Single VLAN at Level 1 → 10+ micro-segments at Level 5.
3. **Encryption:** Laptop encryption at Level 1 → CMK with HSM at Level 5.
4. **Incident response:** Call tree at Level 1 → 24/7 SOC with IR retainer at Level 5.
5. **De-identification:** Not needed at Level 1 → population-scale at Level 6.
