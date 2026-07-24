# PCI DSS v4.0.1 — Data Security Requirements

## Overview
Payment Card Industry Data Security Standard v4.0.1 establishes technical and operational requirements for protecting cardholder data (CHD) and sensitive authentication data (SAD).

## Key Data Requirements

### Requirement 3: Protect Stored Account Data
- PAN must be rendered unreadable (tokenization, truncation, hashing, or encryption)
- Never store SAD (CVV, PIN, full track data) after authorization
- Key management: split knowledge, dual control, least privilege
- Cryptographic key rotation at least annually

### Requirement 4: Protect Data in Transit
- TLS 1.2+ for all CHD transmission over open/public networks
- Certificate validity monitoring
- No deprecated protocols (SSL, early TLS)

### Requirement 7: Restrict Access by Need to Know
- Role-based access control for CHD
- Default-deny, least privilege
- Access review every 6 months

### Requirement 10: Log and Monitor Access
- Audit trails for all CHD access
- Automated monitoring and alerting
- Log retention: 12 months with 3 months online

## References
- PCI SSC: https://www.pcisecuritystandards.org/
- PCI DSS v4.0.1 Summary of Changes
