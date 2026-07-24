# PCI DSS 4.0 Implementation

The 12 requirements mapped to implementation with SAQ type selection,
CDE scoping, and the new PCI DSS 4.0 requirements including targeted
risk analysis and customized compensating controls.

## SAQ Type Selection

| SAQ Type | Use Case | Requirements |
|----------|----------|-------------|
| SAQ A | Card-not-present, fully outsourced (iframe/redirect) | 24 |
| SAQ A-EP | Card-not-present, partial outsourced (direct post) | 191 |
| SAQ B | Imprint-only, no electronic storage | 47 |
| SAQ B-IP | Standalone IP-connected terminals, no electronic storage | 116 |
| SAQ C | Payment app connected to internet, no electronic storage | 139 |
| SAQ C-VT | Virtual terminal (web-based), no electronic storage | 82 |
| SAQ D (Merchant) | All other merchants, any CHD storage | 329 |
| SAQ D (SP) | Service providers that store/process/transmit CHD | 343+ |

## CDE Scoping

The CDE includes all system components that store, process, or transmit
cardholder data (CHD) or sensitive authentication data (SAD), plus
connected-to components that can impact CDE security.

```
Scoping methodology:
1. Identify all CHD/SAD flows (data flow diagram)
2. Identify systems that store, process, or transmit CHD/SAD
3. Identify connected-to systems (AD, monitoring, patching, security)
4. Verify segmentation between CDE and non-CDE (penetration test)
5. Document scope in a network diagram with justification
```

## 12 Requirements Summary

### Requirement 1: Network Security Controls
- Firewall configuration at every internet connection and DMZ boundary
- Network diagram documenting all CDE systems and data flows
- Router configuration standards, no default settings
- Review firewall rules every 6 months

### Requirement 2: Secure Configurations
- Configuration standards for all system components (CIS benchmarks)
- No vendor default passwords, SNMP community strings
- Only one primary function per server (no mixed CDE/non-CDE roles)
- Remove unnecessary services, protocols, daemons

### Requirement 3: Protect Stored Account Data
- PAN must be rendered unreadable: tokenization, truncation, hashing, or encryption
- NEVER store SAD post-authorization: full track, CVV/CVC, PIN block
- Key management: separate key-encrypting keys, least access, key rotation
- PAN display: masked to first 6 + last 4 digits

### Requirement 4: Encrypt Transmission
- TLS 1.2+ for all CHD transmission over open/public networks
- No SSL, early TLS (pre-1.1) prohibited
- Strong cryptography: disable weak ciphers, use secure protocol versions
- Certificate validity checked, trusted CAs only

### Requirement 5: Anti-Malware
- Anti-malware on all commonly affected systems
- Phishing protection for personnel
- Anti-malware definitions updated automatically, scans run regularly
- Audit logs from anti-malware solutions per PCI DSS Req 10

### Requirement 6: Secure Systems and Software
- Secure SDLC: security requirements, code review, security testing
- Patch critical/high vulnerabilities within 30 days
- WAF for public-facing web applications
- Change control: documented approval, backout plan, testing

### Requirement 7: Access Control (Need-to-Know)
- Access to CHD restricted by business need-to-know
- RBAC with documented role definitions and access rights
- Default deny-all, explicitly grant per role

### Requirement 8: Identify and Authenticate
- MFA for all CDE access (PCI DSS 4.0: expanded from admin-only)
- Unique user IDs, no shared accounts
- Password policy: 12+ characters, complexity, 90-day rotation
- Lockout after 6 failed attempts in 30 minutes

### Requirement 9: Physical Security
- Physical access controls: badge, video, visitor logs
- Media destruction: shred, incinerate, degauss
- Secure storage of backup media
- POI device inspection for tampering

### Requirement 10: Logging and Monitoring
- Audit trails: individual user access to CHD, actions, timestamps
- Time synchronization: NTP, all critical systems within 1 second
- Log review: daily for security events, automated alerting
- Log retention: 12 months with 3 months immediately available

### Requirement 11: Regular Testing
- ASV vulnerability scans: quarterly, zero >=4.0 CVSS
- Internal vulnerability scans: quarterly, all HIGH/CRITICAL remediated
- Penetration testing: annually, methodology-based (NIST SP 800-115)
- IDS/IPS: monitor traffic at CDE perimeter, alert on suspicious activity
- Change detection (FIM): alert on unauthorized modification of critical files

### Requirement 12: Security Policy
- Information security policy, reviewed annually
- Risk assessment: annually, identify threats and vulnerabilities
- Security awareness training: annually, role-specific
- Incident response plan: tested annually
- Third-party service provider management: due diligence, PCI validation
