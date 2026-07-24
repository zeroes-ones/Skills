# Healthcare Security Anti-Patterns

Common failure patterns in healthcare security architecture and their
consequences.

## 1. BA-Only Perimeter — "The BAA Is Our Security Program"

**Pattern:** Signing a BAA and assuming the vendor handles all security.
No independent due diligence, no SOC 2 review, no penetration test audit.
**Why it fails:** A BAA is a contract, not a security assessment. BAAs allocate
liability — they don't prevent breaches. Change Healthcare's 2024 breach
involved a vendor with a signed BAA. **Fix:** Independent vendor security
assessment, annual reviews, sub-processor audit rights in the BAA.

## 2. Flat Clinical Network — "We Have a Firewall"

**Pattern:** All clinical devices, workstations, and guest WiFi on one flat
VLAN behind a perimeter firewall. Medical devices on Windows XP share a
broadcast domain with internet-connected endpoints. **Why it fails:** One
compromised clinical workstation gives an attacker lateral movement to every
unpatched medical device. Ransomware propagates across the entire flat network
in minutes. **Fix:** Micro-segmentation: IoMT VLAN, biomed VLAN, clinical VLAN,
guest VLAN — each with explicit deny-by-default ACLs.

## 3. PHI in Logs — "We Need It for Debugging"

**Pattern:** Logging full patient records, MRNs, SSNs, or diagnostic details
to application logs, CloudWatch, Splunk, or ELK without redaction. **Why it
fails:** Logs replicate to observability platforms, SIEMs, and backup tapes —
each copy is a regulated data store requiring encryption, access control,
and retention policy. PHI-in-log incidents trigger mandatory OCR breach
notification if 500+ individuals are affected. **Fix:** Structured logging
with PHI redaction middleware. Whitelist-only audit table for required PHI.

## 4. Encryption as Optional — "It's Addressable"

**Pattern:** Treating encryption as optional or addressable for ePHI under
pre-2024 HIPAA interpretation. Skipping encryption due to cost or performance
concerns. **Why it fails:** The 2024 HIPAA Security Rule proposed update
reclassifies encryption from addressable to required. Unencrypted ePHI is
now a per se violation regardless of compensating controls. **Fix:** Encrypt
all ePHI at rest (KMS CMK with auto-rotation) and in transit (TLS 1.2+).

## 5. De-identification Theater — "We Took Out the Names"

**Pattern:** Removing names and MRNs, calling data "anonymous," and
publishing or sharing without Safe Harbor or Expert Determination
certification. **Why it fails:** ZIP + DOB + gender uniquely identifies 87%
of Americans (Sweeney, 2000). Without Safe Harbor's full 18-identifier removal
or Expert Determination certification, the data remains PHI. **Fix:**
Document which de-identification standard was used. If Safe Harbor, provide
the 18-identifier checklist. If Expert Determination, provide the
statistical certification.

## 6. Telemedicine Without BAA Verification

**Pattern:** Using consumer-grade Zoom, Teams, or Google Meet for telehealth
without verifying healthcare-tier licensing and BAA execution. **Why it
fails:** Consumer versions do not sign BAAs. Recordings stored on consumer
infrastructure are unencrypted PHI. OCR telehealth flexibilities ended
May 11, 2023. **Fix:** Use healthcare-specific tiers (Zoom for Healthcare,
Teams EHR connector). Verify BAA is signed and current. Configure recording
storage in a HIPAA-compliant environment.

## 7. Compliance-as-Ceiling — "We're HIPAA Compliant, We're Done"

**Pattern:** Treating HIPAA compliance as the security program's end state.
No security controls beyond the HIPAA minimum. No HITRUST CSF or NIST CSF
maturity progression. **Why it fails:** HIPAA-compliant organizations are
breached routinely. HIPAA is a regulatory floor, not a security target.
**Fix:** Use HITRUST CSF for progressive maturity. Implement NIST SP 800-53
controls beyond HIPAA's baseline. Annual penetration tests and red team
exercises.
