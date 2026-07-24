# Healthcare Security Best Practices

Proven patterns for architecting secure healthcare systems.

## 1. Encrypt Everything, Everywhere

ePHI must be encrypted at rest (AES-256, KMS CMK with automatic 90-day key
rotation) and in transit (TLS 1.2+, certificate pinning for internal services).
Database connections use `sslmode=verify-full`. Object storage enforces SSE-KMS
with bucket policies denying unencrypted PUTs. The 2024 HIPAA Security Rule
proposed update makes encryption mandatory — no more "addressable" loophole.

## 2. Segment Clinical Networks Ruthlessly

Minimum five VLANs: IoMT (medical devices, no internet), Biomed (device
management, proxy-only internet), Clinical (workstations, authenticated proxy),
Guest (internet only, no route to clinical), and Corporate (admin/billing).
Default-deny ACLs between all segments. Inline IPS on every inter-VLAN link.

## 3. Maintain a Living BAA Registry

Every vendor that creates, receives, maintains, or transmits PHI must have a
signed, current BAA. Track BAA status, expiration, sub-processor list, and last
audit date in a registry. Quarterly reviews. Conduit exception is narrow — if
the vendor stores PHI for any duration, they need a BAA.

## 4. Design Breach Notification Before You Need It

Pre-built notification pipeline on infrastructure independent from clinical
systems. Contact lists (patients, media, OCR) maintained quarterly. Templates
for 60-day OCR notification, media notification (500+ individuals), and
individual notification. Annual tabletop exercises.

## 5. Classify PHI at Ingestion

Tag every data element at collection: PHI (HIPAA full protections), de-identified
(document method), or non-PHI. Automate classification with data loss prevention
(DLP) rules. PHI data stores get encryption, access logging, and backup encryption
by default.

## 6. Implement SMART on FHIR for API Authorization

All FHIR APIs use SMART App Launch with OAuth 2.0. Resource-level scopes
(e.g., `patient/Observation.rs` not `patient/*`). Psychotherapy notes and
42 CFR Part 2 substance use disorder records require separate, explicit
authorization — never bundle with general PHI access.

## 7. Redact PHI from Logs by Default

Assume all logs leak. Deploy PHI redaction middleware as a gate before any log
shipping. Whitelist audit tables as the only permitted PHI-in-log destination.
Pre-production scan for SSN/MRN/DOB patterns — fail the build if found.

## 8. Patch Medical Devices or Isolate Them

For every network-connected medical device: request CBOM from manufacturer,
assess patch availability, apply patches within FDA-recommended timelines.
Devices on unsupported OS (Windows XP, Windows 7): isolate on dedicated VLAN
with no internet, deploy compensating IPS, create time-bound replacement plan.

## 9. De-identify with Rigor

Use Safe Harbor (18-identifier removal) or Expert Determination (statistical
certification) — nothing else is HIPAA-recognized. Publish the method used.
Execute Data Use Agreements prohibiting re-identification. Audit DICOM headers
and FHIR extensions for hidden identifiers.

## 10. Design for Clinical Continuity

Security controls must not block patient care. Architect fail-open for clinical
safety: if an auth service is down, clinicians must still access records.
Document compensating controls. Patient safety > policy compliance.
