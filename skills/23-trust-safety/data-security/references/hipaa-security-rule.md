# HIPAA Security Rule — Technical Safeguards for PHI

## Overview
45 CFR Part 160 and Part 164, Subparts A and C establish security standards for protecting electronic Protected Health Information (ePHI).

## Technical Safeguards (45 CFR 164.312)

### Access Control (164.312(a)(1))
- Unique user identification
- Emergency access procedure (break-glass)
- Automatic logoff after inactivity
- Encryption and decryption

### Audit Controls (164.312(b))
- Hardware, software, and procedural mechanisms
- Record and examine ePHI access activity
- Immutable audit logs with tamper detection

### Integrity (164.312(c)(1))
- Protect ePHI from improper alteration or destruction
- Electronic mechanisms to corroborate integrity
- Hash verification, digital signatures

### Person or Entity Authentication (164.312(d))
- Verify identity of users seeking ePHI access
- Multi-factor authentication recommended

### Transmission Security (164.312(e)(1))
- Protect ePHI during electronic transmission
- TLS 1.2+ encryption required
- Implemented whenever deemed appropriate

## Breach Notification
- 60-day notification requirement for breaches affecting 500+ individuals
- HHS Secretary must be notified concurrently

## References
- HIPAA Security Rule: 45 CFR 164.302-318
- HHS OCR: https://www.hhs.gov/hipaa/
