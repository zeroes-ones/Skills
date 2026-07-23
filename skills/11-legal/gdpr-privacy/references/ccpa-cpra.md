# 11. CCPA/CPRA Comparison

The California Consumer Privacy Act (CCPA, as amended by the California Privacy Rights Act -- CPRA) is the closest US equivalent to GDPR. Understanding the differences is essential for any organization processing both EU and California resident data.

### 11.1 Applicability Thresholds

An organization must comply with CCPA/CPRA if it does business in California AND meets any ONE of:
- Annual gross revenue exceeds $25 million (globally)
- Buys, sells, or shares personal information of 100,000 or more consumers or households
- Derives 50% or more of annual revenue from selling or sharing consumers' personal information

**Comparison:** GDPR applies to any organization that processes personal data of individuals in the EEA, regardless of revenue or scale (subject to the household exemption for purely personal activities).

### 11.2 Consumer Rights Under CCPA/CPRA

| Right | Description | GDPR Equivalent |
|---|---|---|
| **Right to Know** | Request disclosure of categories and specific pieces of personal information collected, sources, purposes, and third parties shared with | Right of Access (Art. 15) |
| **Right to Delete** | Request deletion of personal information, subject to exceptions | Right to Erasure (Art. 17) |
| **Right to Correct** | Request correction of inaccurate personal information (added by CPRA) | Right to Rectification (Art. 16) |
| **Right to Opt-Out of Sale/Sharing** | Direct businesses to stop selling or sharing personal information for cross-context behavioral advertising | Right to Object (Art. 21) -- but CCPA is opt-OUT, GDPR is opt-IN for some processing |
| **Right to Limit Use of Sensitive PI** | Limit use of sensitive personal information to what is necessary to perform the service (added by CPRA) | Special categories under Art. 9 with explicit consent |
| **Right to Non-Discrimination** | Businesses cannot discriminate against consumers who exercise CCPA rights | No explicit equivalent, but fairness principle (Art. 5(1)(a)) covers this |

### 11.3 Key Differences from GDPR

| Dimension | GDPR | CCPA/CPRA |
|---|---|---|
| **Default consent model** | Opt-in for most processing (consent as legal basis) | Opt-out for sale/sharing (business can process until consumer opts out) |
| **Personal information definition** | Any information relating to an identified or identifiable natural person | Broader: includes household data, inferences drawn from personal information |
| **Sensitive data** | Special categories of personal data (Art. 9) with heightened protections | Sensitive personal information subcategory (SSN, precise geolocation, race, religion, health, biometrics, etc.) with right to limit use |
| **Enforcement** | Supervisory authorities, administrative fines up to 4% global annual turnover or EUR20M | California AG and California Privacy Protection Agency (CPPA); administrative fines; private right of action ONLY for data breaches (not for other violations) |
| **DPO requirement** | Required in specific circumstances | No DPO requirement, but businesses must provide methods for submitting requests |
| **DPIA requirement** | Required for high-risk processing (Art. 35) | Cybersecurity audit and risk assessment required for processing presenting significant risk (CPRA) |
| **Data retention** | Storage limitation principle (Art. 5(1)(e)) | No explicit storage limitation, but must inform consumers of retention period at collection |
| **Cross-border transfers** | Extensive restrictions with adequacy decisions, SCCs, etc. | No cross-border transfer restrictions (US federal system) |

### 11.4 Operational Impact

For organizations subject to both:
- **Do not build parallel systems.** A single DSAR engine that handles both GDPR and CCPA request types, with jurisdiction logic to apply the correct rules (timeline, verification standard, data scope).
- **Unify consent management.** Your CMP should handle GDPR (opt-in, granular) and CCPA (opt-out link, GPC signal) with jurisdiction detection.
- **Privacy notices can be unified** but must clearly differentiate rights available to different jurisdictions.
- **Data mapping is the common foundation** -- both regimes require you to know what data you have and where it lives.

---
