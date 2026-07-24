# PCI DSS 4.0 — Data-Centric Requirements

## Overview
PCI DSS v4.0 focuses on security as a continuous process. Key data protection requirements span multiple domains.

## Requirement 3: Protect Stored Account Data
- **3.2**: Never store SAD after authorization (CVV, PIN, full track)
- **3.3**: Mask PAN when displayed (first 6, last 4 maximum)
- **3.4**: Render PAN unreadable (tokenization, encryption, hashing with salt)
- **3.5**: Protect cryptographic keys (documented key management, split knowledge)
- **3.6**: Key management procedures: generation, distribution, storage, rotation, retirement

## Requirement 4: Encrypt Transmission of Cardholder Data
- **4.1**: Strong cryptography for transmission over open/public networks
- **4.2**: Never send unprotected PAN via end-user messaging (email, SMS, chat)
- **4.3**: TLS 1.2+ minimum, certificates valid and trusted

## Requirement 7: Restrict Access by Need to Know
- **7.1**: Role-based access control for system components and data
- **7.2**: Access control system with default-deny
- **7.3**: Access review at least every 6 months

## Requirement 10: Log and Monitor All Access
- **10.1**: Implement audit trails linking access to individual users
- **10.2**: Automated monitoring with real-time alerting
- **10.6**: Log review: daily for security events, weekly for all other

## References
- PCI DSS v4.0.1: https://www.pcisecuritystandards.org/document_library/
