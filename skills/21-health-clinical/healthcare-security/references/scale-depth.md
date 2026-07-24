# Healthcare Security Scale Depth

## Solo Practice (1-10 employees)
- HIPAA Security Risk Assessment (SRA) — annual, documented
- Encrypted email for PHI (Office 365 with BAA or Google Workspace with BAA)
- Disk encryption on all devices (FileVault, BitLocker)
- Password manager + 2FA on all accounts
- Signed BAAs with all vendors (EHR, billing, cloud storage)

## Small Clinic (10-50 employees)
- All Solo items + dedicated HIPAA Security Officer
- Access control: unique user IDs, role-based, audit logs reviewed monthly
- Network segmentation: clinical network separate from guest WiFi
- Breach notification policy + incident response plan
- Annual workforce HIPAA training with documented completion

## Regional Hospital (50-500 employees)
- All Small Clinic items + 24/7 SOC or managed security provider
- SIEM: all PHI access logged, correlated, alerted
- Penetration testing annually + after major changes
- Medical device security: isolated VLAN, inventory with patch status
- Disaster recovery with encrypted backups, tested quarterly
- DLP (Data Loss Prevention) on email and endpoints

## Enterprise Health System (500+ employees)
- All Regional Hospital items + dedicated CISO with healthcare background
- HITRUST CSF certification or equivalent framework
- Red team exercises quarterly
- Zero Trust Architecture for all PHI access
- FHIR API security: automated scope validation, rate limiting, abuse detection
- Bug bounty program with safe harbor for security researchers
- Cross-organization threat intelligence sharing (H-ISAC)
