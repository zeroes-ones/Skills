# Compliance Officer - Framework Mapping

Cross-mapping of controls across SOC 2, ISO 27001:2022, GDPR, HIPAA, and PCI DSS v4.0.

---

## Common Control Mapping Table

| Control Domain | SOC 2 CCM | ISO 27001:2022 (Annex A) | GDPR | HIPAA Security Rule | PCI DSS v4.0 |
|---------------|-----------|--------------------------|------|---------------------|-------------|
| **Access Control** | CC6.1, CC6.2, CC6.3 | A.5.15, A.5.16, A.5.18, A.8.2 | Art. 32(1)(b) | §164.312(a)(1), §164.312(d) | Req 7, Req 8, Req 9 |
| **Asset Management** | CC4.1 | A.5.9, A.5.10, A.8.1 | Art. 30 | §164.310(d)(2) | Req 2.4, Req 9 |
| **Audit Logging & Monitoring** | CC7.2, CC7.3, CC7.4 | A.8.15, A.8.16, A.8.17 | Art. 30(1)(g) | §164.312(b) | Req 10 |
| **Business Continuity** | CC7.5 (AICPA: A1.3) | A.5.29, A.5.30, A.8.13 | Art. 32(1)(c) | §164.308(a)(7) | Req 12.10 |
| **Change Management** | CC8.1 | A.8.32, A.8.25 | Art. 25 | §164.308(a)(7)(ii)(A) | Req 6.4, Req 6.5 |
| **Cryptography** | CC6.7 | A.8.24 | Art. 32(1)(a) | §164.312(e)(2)(ii) | Req 3, Req 4 |
| **Data Classification** | CC2.2 | A.5.10, A.5.12, A.5.13 | Art. 5(1)(c), Art. 30 | §164.310(d) | Req 9.6 |
| **Data Retention & Disposal** | CC6.5 | A.8.10, A.8.11, A.8.12 | Art. 5(1)(e), Art. 17 | §164.310(d)(2) | Req 3.1, Req 9.8 |
| **Encryption (Transit)** | CC6.7 | A.8.20, A.8.22, A.8.24 | Art. 32(1)(a) | §164.312(e)(1) | Req 4 |
| **Encryption (At Rest)** | CC6.7 | A.8.24 | Art. 32(1)(a) | §164.312(a)(2)(iv) | Req 3.5 |
| **Identity & Authentication** | CC6.1, CC6.2 | A.5.16, A.5.17, A.8.5 | Art. 32(1)(b) | §164.312(d) | Req 8 |
| **Incident Response** | CC7.3, CC7.4, CC7.5 | A.5.24, A.5.25, A.5.26 | Art. 33, Art. 34 | §164.308(a)(6) | Req 12.10 |
| **Network Security** | CC6.6 | A.8.20, A.8.21, A.8.22 | Art. 32(1)(b) | §164.312(e)(1) | Req 1, Req 2, Req 5, Req 6 |
| **Physical Security** | CC6.4 | A.7.1-A.7.14 | Art. 32(1)(b) | §164.310 | Req 9 |
| **Risk Assessment** | CC3.1, CC3.2, CC3.3 | A.5.1-A.5.8 (Clause 6) | Art. 35 (DPIA) | §164.308(a)(1)(ii)(A) | Req 12.2 |
| **Secure Development** | CC8.1 | A.8.25, A.8.26, A.8.28, A.8.29 | Art. 25 | §164.308(a)(8) | Req 6 |
| **Supplier Management** | CC9.1, CC9.2 | A.5.19, A.5.20, A.5.21, A.5.22 | Art. 28 | §164.308(b)(1) | Req 12.8 |
| **Training & Awareness** | CC1.4 | A.6.3, A.6.8 | Art. 39 | §164.308(a)(5) | Req 12.6 |
| **Vulnerability Management** | CC7.1 | A.8.8 | Art. 32(1)(a) | §164.308(a)(8) | Req 6.3, Req 11 |
| **Configuration Management** | CC8.1 | A.8.9 | Art. 25(2) | §164.312(c) | Req 2 |

---

## SOC 2 — Trust Services Criteria (2017)

SOC 2 reports on five Trust Services Criteria. The most common is **Security** (required in all SOC 2 reports).

### Security (Common Criteria 1.x - 9.x)
| Criteria | Description | Evidence Examples |
|----------|------------|------------------|
| CC1.x | Control Environment | Org chart, code of conduct, board minutes |
| CC2.x | Communication & Information | Security policy docs, incident communication plan |
| CC3.x | Risk Assessment | Risk register, annual risk assessment report |
| CC4.x | Monitoring Activities | Vulnerability scan reports, penetration test results |
| CC5.x | Control Activities (design) | Control matrix mapping risks to controls |
| CC6.x | Logical & Physical Access Controls | Access review logs, SSO configuration, badge logs |
| CC7.x | System Operations | Change management records, incident tickets, backup tests |
| CC8.x | Change Management | SDLC policy, code review evidence, deployment logs |
| CC9.x | Risk Mitigation (vendors) | Vendor risk assessments, SOC reports from subprocessors |

### Additional Criteria (if included in scope)
- **Availability:** A1.1-A1.3 (BCP/DR, capacity management, availability monitoring)
- **Confidentiality:** C1.1-C1.2 (data classification, encryption, disposal)
- **Processing Integrity:** PI1.1-PI1.5 (input validation, processing accuracy, quality assurance)
- **Privacy:** P1.1-P8.1 (notice, consent, data minimization, access, deletion)

---

## ISO 27001:2022 — Key Annex A Controls

ISO 27001:2022 reduced Annex A from 114 controls (2013) to 93 controls across 4 themes.

### Organizational Controls (A.5)
| Control | Title | Key Evidence |
|---------|-------|-------------|
| A.5.1 | Policies for information security | Approved policy documents, version history |
| A.5.2 | Information security roles and responsibilities | RACI matrix, job descriptions |
| A.5.7 | Threat intelligence | Threat intel subscription, threat modeling docs |
| A.5.8 | Information security in project management | Security requirements in project templates |
| A.5.15 | Access control policy | Access control policy, RBAC matrix |
| A.5.24 | Incident management planning | Incident response plan, tabletop exercise results |
| A.5.29 | ICT readiness for business continuity | BCP, DR plan, failover test results |
| A.5.31 | Legal, statutory, regulatory compliance | Compliance register, legal review records |
| A.5.36 | Compliance with security policies and standards | Internal audit reports, findings tracking |

### People Controls (A.6)
| Control | Title | Key Evidence |
|---------|-------|-------------|
| A.6.1 | Screening (background checks) | Screening policy, HR records |
| A.6.3 | Information security awareness and training | Training completion reports, phishing test results |
| A.6.5 | Responsibilities after termination | Offboarding checklist, access revocation records |

### Physical Controls (A.7)
| Control | Title | Key Evidence |
|---------|-------|-------------|
| A.7.2 | Physical entry controls | Badge logs, visitor sign-in, CCTV |
| A.7.7 | Clear desk and clear screen | Clean desk policy, office photos |
| A.7.10 | Storage media disposal | Media destruction certificates, NIST 800-88 compliance |

### Technological Controls (A.8)
| Control | Title | Key Evidence |
|---------|-------|-------------|
| A.8.1 | User endpoint devices | MDM enrollment, device encryption, patch status |
| A.8.2 | Privileged access rights | PAM tool config, privileged access review |
| A.8.7 | Protection against malware | EDR deployment, malware scan reports |
| A.8.8 | Management of technical vulnerabilities | Vulnerability scan schedule, remediation SLAs |
| A.8.15 | Logging | SIEM config, log retention policy |
| A.8.16 | Monitoring activities | SIEM alerts, SOC runbooks |
| A.8.20 | Network security controls | Firewall rules, network segmentation diagram |
| A.8.24 | Use of cryptography | Encryption standards, key management policy |
| A.8.32 | Change management | Change control policy, CAB minutes, deployment logs |

---

## GDPR — Key Articles

| Article | Requirement | Technical Control | Evidence |
|---------|------------|-------------------|----------|
| Art. 5(1)(a) | Lawfulness, fairness, transparency | Privacy notice on signup, consent management | Screen captures, consent logs |
| Art. 5(1)(c) | Data minimization | DB schema showing only required fields collected | Data inventory |
| Art. 5(1)(d) | Accuracy | User self-service data correction; data quality checks | Correction API logs |
| Art. 5(1)(e) | Storage limitation | Automated data retention/deletion jobs | Retention policy, deletion logs |
| Art. 5(1)(f) | Integrity & confidentiality | Encryption at rest, TLS, access control | Encryption config, pentest report |
| Art. 17 | Right to erasure | Account deletion API, hard delete from backups | Deletion workflow screenshots |
| Art. 20 | Data portability | Export API (JSON/CSV), machine-readable format | Export test results |
| Art. 25 | Data protection by design & default | Threat modeling, privacy settings defaulted to restrictive | Design review records |
| Art. 28 | Processor obligations | DPA with all subprocessors, vendor risk assessment | Signed DPAs, vendor list |
| Art. 30 | Records of processing activities | RoPA document, data flow maps | RoPA spreadsheet |
| Art. 32 | Security of processing | All controls in OWASP ASVS Level 1 minimum | Audit results |
| Art. 33 | Breach notification (72 hours) | Incident detection → notification workflow | Incident response plan |
| Art. 35 | Data Protection Impact Assessment | DPIA template completed for high-risk processing | Completed DPIAs |
| Art. 44-49 | International transfers | SCCs, BCRs, adequacy decisions, Transfer Impact Assessment | Signed SCCs, TIA document |

---

## HIPAA Security Rule

### Administrative Safeguards (§164.308)
| Standard | Key Requirement |
|----------|----------------|
| Security Management Process (a)(1) | Risk analysis (required), risk management, sanction policy, information system activity review |
| Assigned Security Responsibility (a)(2) | Designated security official |
| Workforce Security (a)(3) | Authorization/supervision, clearance procedure, termination procedures |
| Information Access Management (a)(4) | Minimum necessary access, role-based access |
| Security Awareness Training (a)(5) | Security reminders, malware protection, log-in monitoring, password management |
| Security Incident Procedures (a)(6) | Response and reporting |
| Contingency Plan (a)(7) | Data backup, disaster recovery, emergency mode operation, testing |
| Evaluation (a)(8) | Periodic technical and non-technical evaluations |

### Physical Safeguards (§164.310)
| Standard | Key Requirement |
|----------|----------------|
| Facility Access Controls (a)(1) | Contingency operations, facility security plan, access control/validation |
| Workstation Use (b) | Proper functions and physical attributes of workstations |
| Workstation Security (c) | Physical safeguards for workstations accessing ePHI |
| Device & Media Controls (d) | Disposal, reuse, accountability, backup |

### Technical Safeguards (§164.312)
| Standard | Key Requirement |
|----------|----------------|
| Access Control (a)(1) | Unique user ID, emergency access, automatic logoff, encryption |
| Audit Controls (b) | Hardware/software/procedural audit mechanisms |
| Integrity (c)(1) | Mechanism to authenticate ePHI |
| Person/Authentication (d) | Identity verification of persons seeking ePHI |
| Transmission Security (e)(1) | Integrity controls and encryption for ePHI in transit |

---

## PCI DSS v4.0 — Requirements Summary

| Requirement | Title | Key Controls |
|------------|-------|-------------|
| Req 1 | Install & maintain network security controls | Firewall configs, network diagrams, change control |
| Req 2 | Apply secure configurations | Hardening standards, no default passwords, only necessary services |
| Req 3 | Protect stored account data | PAN masking, encryption, key management, no sensitive auth data storage |
| Req 4 | Protect cardholder data in transit | TLS 1.2+, strong cryptography, trusted certificates |
| Req 5 | Protect against malware | Anti-malware on all systems, periodic scans, keep current |
| Req 6 | Develop & maintain secure systems | Secure SDLC, code review, vulnerability management, WAF |
| Req 7 | Restrict access by need-to-know | RBAC, least privilege, access denied by default |
| Req 8 | Identify & authenticate access | Unique IDs, MFA for admin/CDE, password policy, lockout |
| Req 9 | Restrict physical access | Physical access controls, visitor logs, media disposal |
| Req 10 | Log & monitor all access | Audit trails, time sync, log protection, daily reviews |
| Req 11 | Test security regularly | Wireless scanning, vulnerability scans, penetration testing, IDS/IPS |
| Req 12 | Maintain security policies | Policy docs, risk assessment, training, incident response, vendor management |

---

## Evidence Collection Template

For each control, collect:

```markdown
## Control: [Name]
- **Framework(s):** SOC 2 CC6.1, ISO A.5.15, PCI Req 7
- **Control Description:** [What the control does]
- **Control Owner:** [Name/Team]
- **Implementation Date:** [Date]
- **Last Reviewed:** [Date]
- **Review Cadence:** [Annual/Quarterly]

### Evidence
1. **Policy Document:** [Link to approved policy]
2. **Configuration Screenshot:** [Link/attachment]
3. **Test Results:** [Audit/sampling results]
4. **Meeting Minutes:** [Approval records]

### Test Procedure
1. [Step-by-step test]
2. [Expected result]
3. [Actual result]

### Gaps & Remediation
- [Gap identified]
- [Remediation plan with target date]
```
