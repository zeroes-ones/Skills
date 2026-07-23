# 4. Data Subject Rights (DSAR)

GDPR provides 8 data subject rights. Implementing these at scale requires a centralized DSAR engine -- a request management system that orchestrates identity verification, data collection across all data stores, response assembly, and fulfillment tracking.

For a comprehensive DSAR implementation guide including technical architecture, deletion cascades, portability formats, exemption handling, and quarterly testing protocols, see `references/dsar-implementation-guide.md`.

### 4.1 The 8 Rights at a Glance

| Right | Art. | Summary |
|---|---|---|
| **Access** | 15 | Data subject can obtain confirmation of whether their data is processed, a copy of the data, and metadata (purposes, categories, recipients, retention, rights). |
| **Rectification** | 16 | Correct inaccurate data; complete incomplete data. |
| **Erasure (Right to be Forgotten)** | 17 | Delete data where: no longer necessary, consent withdrawn, objection upheld, unlawful processing, legal obligation. Subject to exemptions (freedom of expression, legal obligation, public health, archiving, legal claims). |
| **Restriction** | 18 | Limit processing while accuracy is contested, processing is unlawful, data is needed for legal claims, or objection is pending. |
| **Portability** | 20 | Receive data in structured, commonly used, machine-readable format (JSON, CSV, XML). Only applies to data provided by the data subject, processed by automated means, based on consent or contract. |
| **Objection** | 21 | Object to processing based on legitimate interest or public task. Absolute right to object to direct marketing. |
| **Automated decision-making** | 22 | Right not to be subject to decisions based solely on automated processing that produce legal or similarly significant effects. Exceptions: contract necessity, authorized by law, explicit consent. |
| **Notification obligation** | 19 | Controllers must communicate rectification, erasure, or restriction to each recipient unless impossible or disproportionate. |

### 4.2 30-Day Response Timeline

- **Clock starts:** Upon receipt of the request. Receipt means the request has been received by the designated DSAR channel and contains sufficient information to identify the data subject and the right being exercised.
- **Standard deadline:** 30 calendar days (not business days).
- **Extensions:** Up to an additional 60 days (total 90) for complex or numerous requests. Must inform the data subject within the first 30 days of the extension and the reasons.
- **ID verification tolling:** The clock pauses while you await identity verification. Start the clock only after identity is confirmed.
- **CCPA comparison:** CCPA allows 45 days (extendable to 90 with notice).

### 4.3 Identity Verification

Use a tiered approach based on the sensitivity of data requested:

| Tier | Risk Level | Methods | When to Use |
|---|---|---|---|
| **Basic** | Low | Email confirmation, logged-in session | Access request for non-sensitive data by authenticated user |
| **Medium** | Moderate | Government ID + selfie match, knowledge-based authentication | Account data including contact details, purchase history |
| **High** | High | Notarized document, in-person verification, multi-factor | Special category data, financial data, deletion requests |

**Critical principle:** Do not request more personal data for verification than necessary. If the data subject is already authenticated in your system, do not demand a passport scan for a simple access request.

### 4.4 Exemptions and Limitations

**Manifestly unfounded (Art. 12(5)):**
- The request is vexatious, harassing, or made in bad faith
- Examples: repetitive requests with no interval for data refresh, requests made to disrupt operations
- Response: refuse or charge a reasonable fee. Must demonstrate why it is manifestly unfounded.

**Excessive (Art. 12(5)):**
- The request overlaps with a recent previous request
- Response: charge a reasonable fee or refuse. The bar is higher than manifestly unfounded -- repetition alone may not qualify if sufficient time has passed.

**Adversely affecting others' rights (Art. 15(4)):**
- Access response cannot include personal data of third parties unless they consent or it is unreasonable to withhold
- Must redact third-party data or split files with joint data subjects

**Other exemptions:** Legal professional privilege, management forecasting, negotiation data, regulatory references, journalistic/academic/artistic purposes (Member State derogations).

### 4.5 Technical Architecture

A centralized DSAR engine should follow this architecture:

1. **Intake Layer:** Web form, email parser, API endpoint. Validates request completeness, creates case in tracking system.
2. **ID Verification Service:** Integrates with auth system, optionally with third-party IDV provider. Returns verified identity token.
3. **Data Store Connectors:** A plugin system -- one connector per data store (PostgreSQL, MongoDB, S3, Salesforce, Zendesk, Stripe, analytics warehouse). Each connector implements: `search(subject_id)`, `retrieve(record_ids)`, `delete(record_ids)`, `export(record_ids, format)`.
4. **Response Assembly Engine:** Aggregates results from all connectors, deduplicates, organizes by category, applies redactions, generates the response package.
5. **Deletion Orchestrator:** Coordinates cascading deletion across all stores. Tracks confirmation from each processor. Implements legal hold checks.
6. **Tracking Dashboard:** See the DSAR implementation guide for dashboard design.


---
