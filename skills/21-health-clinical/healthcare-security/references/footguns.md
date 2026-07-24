# Healthcare Security Footguns

Non-obvious ways to compromise healthcare security — the traps that even
experienced engineers fall into.

## 1. The DICOM Header Trap

**Footgun:** Removing PHI from the DICOM image pixel data but forgetting
DICOM headers. **Why it's dangerous:** DICOM tags contain patient name
(0010,0010), MRN (0010,0020), study date (0008,0020), institution name
(0008,0080), and referring physician (0008,0090). A "de-identified" CT
scan can be fully re-identified from its headers alone. **Mitigation:**
Use DICOM PS 3.15 Annex E de-identification profile. Script all tags —
don't manually review. Verify with `dcmdump` on every exported study.

## 2. The "HIPAA-Compliant" Marketing Claim

**Footgun:** Trusting a vendor's marketing claim of "HIPAA compliant"
without verification. **Why it's dangerous:** "HIPAA compliant" has no
legal definition. Any vendor can claim it. What matters: (1) Will they
sign a BAA? (2) What security controls do they actually implement? (3) Is
their SOC 2 report clean? **Mitigation:** Require BAA execution, SOC 2
Type II review, and independent penetration test results before PHI
processing. Never accept a marketing claim as due diligence.

## 3. The Backup Plaintext Trap

**Footgun:** Encrypting the production database but forgetting that
automated backups are unencrypted. **Why it's dangerous:** Backups are
often stored in object storage, replicated cross-region, and retained for
years. An unencrypted backup defeats production encryption — attackers
target backups specifically because they're easier to exfiltrate.
**Mitigation:** Enable backup encryption at creation time. Verify backup
encryption with a restore test. Audit backup destination bucket policy
for encryption enforcement.

## 4. The Metadata Leak in Free-Text Notes

**Footgun:** Scrubbing structured fields but leaving free-text clinical
notes intact. **Why it's dangerous:** Clinician notes contain patient
names ("Mrs. Smith presents with..."), family member names, employer
names, and specific dates. Free text is the hardest PHI to de-identify.
**Mitigation:** NLP-based PHI detection in free text (AWS Comprehend
Medical, GCP Healthcare NLP). Manual review for high-risk datasets.
Assume free text always contains PHI unless proven otherwise.

## 5. The Sub-processor Chain Blindness

**Footgun:** Signing a BAA with the primary vendor but not auditing their
sub-processors. **Why it's dangerous:** Your vendor's vendor may process
your PHI without any BAA with you. AWS sub-processors, Datadog's
underlying cloud provider, Snowflake's storage layer — each link in the
chain needs coverage. **Mitigation:** Audit sub-processor lists quarterly.
Require BAAs to mandate sub-processor notification and approval rights.
Map the full sub-processor chain for critical PHI workflows.

## 6. The 60-Day Clock on Investigation

**Footgun:** Treating the 60-day breach notification clock as starting
at investigation conclusion. **Why it's dangerous:** The clock starts at
discovery of the impermissible access/use/disclosure — not when you finish
investigating. Spend 45 days investigating and you have 15 days left for
notification to 500+ individuals, media, and OCR simultaneously.
**Mitigation:** Parallelize investigation and notification preparation.
Start drafting notifications on day 1. OCR accepts amended notifications
if scope changes after initial filing.

## 7. The Research Dataset Re-identification

**Footgun:** Publishing a "de-identified" dataset without a Data Use
Agreement (DUA) prohibiting re-identification. **Why it's dangerous:**
Without a DUA, recipients have no contractual restriction on
re-identification attempts. Cross-referencing with voter registration,
property records, or social media can re-identify individuals at scale.
**Mitigation:** Always execute a DUA with re-identification prohibition
and downstream use restrictions. Include audit rights and breach
notification requirements in the DUA.
