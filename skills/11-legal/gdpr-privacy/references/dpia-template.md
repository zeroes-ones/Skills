# GDPR Privacy - DPIA Template

Data Protection Impact Assessment template per GDPR Article 35 for high-risk processing activities.

---

## When is a DPIA Required?

A DPIA is mandatory when processing is **likely to result in high risk** to individuals. Triggering criteria (WP29 Guidelines):

- [ ] Systematic and extensive profiling with significant effects
- [ ] Large-scale processing of special categories of data (Art. 9) or criminal data (Art. 10)
- [ ] Systematic monitoring of publicly accessible areas (CCTV, geolocation)
- [ ] Use of new technologies (AI/ML, biometrics, IoT at scale)
- [ ] Processing that prevents data subjects from exercising a right or using a service
- [ ] Combining, comparing, or matching personal data from multiple sources
- [ ] Processing vulnerable persons' data (children, employees, patients)
- [ ] Large-scale processing of sensitive data or data relating to vulnerable persons
- [ ] Automated decision-making with legal or similarly significant effects (Art. 22)

---

## DPIA Document

### Section 1: Processing Overview

| Field | Detail |
|-------|--------|
| **Project Name** | [e.g., Customer Analytics Platform v2] |
| **Department/Team** | [e.g., Data Engineering] |
| **Project Owner** | [Name, Title, Contact] |
| **DPIA Author** | [Name, Title] |
| **Date** | [YYYY-MM-DD] |
| **Version** | [1.0] |

#### 1.1 Processing Description
_Describe the nature, scope, context, and purposes of the processing._

```
[Describe what data is being processed, how, why, and by whom.
Include: data flows, systems involved, third parties, retention periods,
geographic transfers, technology used.]
```

#### 1.2 Purpose of Processing
_What is the objective? What problem does this solve? Why is personal data needed?_

| Purpose | Lawful Basis (Art. 6/9) | Justification |
|---------|------------------------|---------------|
| [e.g., Fraud detection] | Legitimate interest (Art. 6(1)(f)) | [Explain LI balancing test outcome] |
| [e.g., Marketing analytics] | Consent (Art. 6(1)(a)) | [Describe consent mechanism] |

#### 1.3 Data Inventory

| Data Category | Data Subjects | Source | Special Category? | Retention | Location |
|--------------|--------------|--------|-------------------|-----------|----------|
| Email, name, address | Customers | Signup form | No | 7 years after inactivity | AWS eu-west-1 |
| Purchase history | Customers | Order system | No | 3 years | AWS eu-west-1 |
| Behavioral analytics | Website visitors | Analytics SDK | No (aggregated) | 26 months | GCP us-east1 (SCCs) |
| Health data | Claimants | Insurance form | Yes (Art. 9) | 10 years | On-prem EU only |

#### 1.4 Data Flow Diagram
```
[Attach DFD showing: data sources → processing systems → data stores → recipients]
[Mark trust boundaries, encryption points, cross-border transfers]
```

---

### Section 2: Necessity & Proportionality

#### 2.1 Necessity Assessment
| Question | Answer |
|----------|--------|
| Is the processing necessary to achieve the stated purpose? | [Yes/No — Why?] |
| Can the purpose be achieved without personal data? | [Yes/No — Explain alternatives considered] |
| Is the least intrusive method being used? | [Yes/No — Justify approach] |
| Is data minimized to what's strictly necessary? | [Yes/No — List what was excluded] |
| Have privacy-enhancing technologies (PETs) been evaluated? | [Yes/No — Which? e.g., pseudonymization, aggregation, differential privacy] |

#### 2.2 Proportionality Assessment
| Question | Answer |
|----------|--------|
| Does the benefit to the organization outweigh the privacy impact? | [Explain] |
| What would be the impact on data subjects if processing were stopped? | [Explain] |
| Is there a less intrusive alternative that achieves a similar outcome? | [Explain alternatives evaluated] |

---

### Section 3: Risk Assessment

Score each risk: Likelihood (1-5) × Severity (1-5) = Risk Score (1-25)

| Risk ID | Risk Description | Likelihood (1-5) | Severity (1-5) | Score | Inherent Risk |
|---------|-----------------|-------------------|----------------|-------|--------------|
| R1 | Unauthorized access to customer PII via compromised API key | 3 | 4 | 12 | High |
| R2 | Re-identification of anonymized analytics data via linkage attack | 2 | 3 | 6 | Medium |
| R3 | Data breach at third-party analytics processor | 2 | 4 | 8 | Medium |
| R4 | Excessive data collection beyond stated purpose (scope creep) | 3 | 2 | 6 | Medium |
| R5 | Cross-border transfer without adequate safeguards | 1 | 5 | 5 | Medium |

### Likelihood Scale
| Score | Definition |
|-------|-----------|
| 1 | Remote (≤5% chance in 3 years) |
| 2 | Unlikely (5-20%) |
| 3 | Possible (20-50%) |
| 4 | Likely (50-80%) |
| 5 | Almost Certain (>80%) |

### Severity Scale
| Score | Definition | Example Impact |
|-------|-----------|----------------|
| 1 | Minimal | Minor inconvenience, no material harm |
| 2 | Limited | Temporary disruption, minor embarrassment |
| 3 | Significant | Financial loss, distress, reputational damage |
| 4 | Severe | Identity theft, significant financial loss, discrimination |
| 5 | Critical | Physical harm, life-threatening, loss of liberty |

### Risk Matrix
| Likelihood \ Severity | 1-Minimal | 2-Limited | 3-Significant | 4-Severe | 5-Critical |
|----------------------|-----------|-----------|---------------|----------|------------|
| **5 - Almost Certain** | 5-Medium | 10-Medium | 15-High | 20-Critical | 25-Critical |
| **4 - Likely** | 4-Low | 8-Medium | 12-High | 16-High | 20-Critical |
| **3 - Possible** | 3-Low | 6-Medium | 9-Medium | 12-High | 15-High |
| **2 - Unlikely** | 2-Low | 4-Low | 6-Medium | 8-Medium | 10-Medium |
| **1 - Remote** | 1-Low | 2-Low | 3-Low | 4-Low | 5-Medium |

---

### Section 4: Mitigation Measures

| Risk ID | Mitigation | Owner | Deadline | Residual Likelihood | Residual Severity | Residual Score |
|---------|-----------|-------|----------|--------------------|--------------------|----------------|
| R1 | Encrypt all PII at rest (AES-256); enforce MFA on all API access; implement WAF rules | SecEng | 2024-Q2 | 2 | 3 | 6 — Acceptable |
| R2 | Apply k-anonymity (k≥5) and differential privacy (ε≤1); prohibit joins on PII fields | DataEng | 2024-Q1 | 1 | 2 | 2 — Acceptable |
| R3 | Sign SCCs with processor; require SOC 2 Type II report; audit processor security annually | Legal | 2024-Q1 | 2 | 3 | 6 — Acceptable |
| R4 | Implement data catalog with automated classification; quarterly data minimization review | DPO | 2024-Q2 | 2 | 2 | 4 — Acceptable |
| R5 | Execute SCCs; conduct Transfer Impact Assessment; implement supplemental measures (encryption w/ customer-held keys) | Legal | 2024-Q1 | 1 | 4 | 4 — Acceptable |

---

### Section 5: Consultation

| Stakeholder | Role | Consulted? | Date | Feedback Summary |
|------------|------|-----------|------|-----------------|
| Data Protection Officer (DPO) | Independent review | ☐ | | |
| Data Subjects / Representatives | Art. 35(9) where appropriate | ☐ | | |
| Security Team | Technical controls validation | ☐ | | |
| Legal Counsel | Lawfulness assessment | ☐ | | |
| Engineering Lead | Technical feasibility | ☐ | | |
| Processor(s) | DPA obligations | ☐ | | |

---

### Section 6: DPO Recommendation & Sign-Off

#### DPO Recommendation
```
[ ] Proceed — No high residual risks identified; processing is proportionate and necessary
[ ] Proceed with conditions — Specific mitigations must be completed by [date]
[ ] Do not proceed — High residual risks that cannot be adequately mitigated
[ ] Consult supervisory authority — Per Art. 36, prior consultation required
```

#### DPO Comments
```
[Detailed recommendation with justification]
```

#### Signatures

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Project Owner** | | | |
| **DPO** | | | |
| **CISO/Head of Security** | | | |
| **Legal Counsel** | | | |

---

### Section 7: Review & Follow-Up

| Review Trigger | Frequency | Next Review Date |
|---------------|-----------|-----------------|
| Scheduled review | Annual | [Date + 1 year] |
| Significant change in processing | Event-driven | N/A |
| Data breach or near-miss | Event-driven | N/A |
| New technology adoption | Event-driven | N/A |

#### Action Tracking

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [e.g., Deploy encryption at rest for analytics DB] | DevOps | 2024-Q1 | In Progress |
| [e.g., Execute SCCs with analytics processor] | Legal | 2024-Q1 | Pending |
| [e.g., Update privacy notice to reference analytics] | Product | 2024-Q1 | Done |

---

## Examples of High-Risk Processing Activities

### Example 1: AI-Based Candidate Screening
- **Processing:** ML model evaluates job candidates based on CVs, social media, and video interviews
- **High-Risk Factors:** Automated decision-making (Art. 22), profiling, special category data inference, vulnerable subjects (job seekers)
- **Key DPIA Considerations:** Bias testing, human-in-the-loop override, transparency about algorithmic criteria, data sources justified as necessary

### Example 2: Large-Scale Health Data Analytics
- **Processing:** Hospital aggregates patient records for population health analytics shared with researchers
- **High-Risk Factors:** Special category data (Art. 9), large-scale, vulnerable subjects, data sharing with third parties, potential re-identification
- **Key DPIA Considerations:** Patient consent or legal basis for research, de-identification methodology (HIPAA Safe Harbor or Expert Determination), data use agreements, opt-out mechanism

### Example 3: Employee Monitoring Platform
- **Processing:** Software tracks employee activity: keystrokes, screen captures, mouse movement, application usage
- **High-Risk Factors:** Systematic monitoring, vulnerable subjects (employees — power imbalance), invisible processing, potential Art. 22 automated decisions
- **Key DPIA Considerations:** Necessity (can productivity be measured less intrusively?), transparency notice, data minimization (aggregate not individual), works council consultation, GDPR Art. 88 compliance (employment safeguards)

### Example 4: Real-Time Bidding / AdTech
- **Processing:** User browsing behavior shared with hundreds of ad exchanges for real-time ad auctions
- **High-Risk Factors:** Large-scale, invisible processing, profiling, vulnerable subjects, combined data from many sources, special category data inference
- **Key DPIA Considerations:** Valid consent (TCF v2.2), legitimate interest unlikely to pass balancing test, transparency about number of recipients (hundreds), right to object mechanism, data minimization (broadcast vs targeted bid requests)
