# Healthcare Security Anti-Patterns

Reference companion to healthcare-security/SKILL.md. Detailed anti-patterns with real breach examples.

## HIPAA Anti-Patterns
- **Plaintext PHI in logs**: Logging patient names, MRNs, or diagnoses to unprotected log files ($4.8M Anthem settlement)
- **Shared service accounts**: Multiple staff using same EHR credentials — impossible to audit who accessed what
- **Unencrypted backup tapes**: Physical media stolen from vehicles ($2.25M HHS fine for unencrypted drives)
- **Email without TLS**: PHI transmitted over unencrypted SMTP — interceptable in transit

## FHIR Anti-Patterns
- **No scoping on SMART on FHIR tokens**: Access token grants entire patient record instead of specific resources
- **Hardcoded client secrets in mobile apps**: OAuth2 client credentials extractable from APK/IPA binary
- **Missing `aud` claim validation**: Not verifying the token audience is your FHIR server

## Medical Device Anti-Patterns
- **Hardcoded WiFi passwords in infusion pumps** — network pivot point
- **Telnet debug ports left open on production imaging devices**
- **Unvalidated firmware updates via USB** — no cryptographic signature check
