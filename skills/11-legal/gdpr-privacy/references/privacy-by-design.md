# 10. Privacy by Design

Privacy by design (Art. 25) requires that data protection be integrated into the processing activities and business practices from the design stage through the entire lifecycle. It is not a feature to add later -- it is a design constraint.

### 10.1 Data Minimization in Architecture

- Design schemas so that personal data and non-personal data are stored in separate, access-controlled tables/collections
- At the API layer, implement field-level access control -- never return more fields than the caller needs
- Use GraphQL or sparse field selectors (e.g., `?fields=id,name,email` in REST) to enforce minimization at read time
- Implement purpose-based access tokens: a service calling the user API for authentication receives only auth-relevant fields; a service calling for analytics receives only pseudonymized data
- Audit database schemas quarterly: any field without a documented purpose and legal basis is flagged for deletion

### 10.2 Pseudonymization Techniques

| Technique | What It Does | When to Use | Key Management |
|---|---|---|---|
| **Tokenization** | Replace identifier with a random token, store mapping in a secure vault | When you need to re-identify later (analytics linking, customer support) | Vault must be isolated with strict access control |
| **Hashing (salted)** | One-way transformation with salt -- cannot reverse, but can link records | Analytics, data warehousing -- when re-identification is not needed but consistency is | Salt must be stored separately, rotated periodically |
| **Encryption** | Reversible with key -- protects confidentiality while retaining utility | Data at rest, application-layer protection for sensitive fields | Key must be in a KMS (AWS KMS, HashiCorp Vault), not in the application code |
| **Aggregation** | Replace individual data with statistical summaries | Reporting, dashboards, public datasets | n/a (no key needed) |

**Critical distinction:** Pseudonymized data is still personal data under GDPR because re-identification is possible (you hold the key/mapping). Anonymized data (truly irreversible) is not personal data. Most organizations never achieve true anonymization -- be honest in your assessments.

### 10.3 Privacy Patterns

| Pattern | Description | Use Case |
|---|---|---|
| **k-anonymity** | Ensure each record is indistinguishable from at least k-1 other records in the dataset | Publishing datasets, analytics exports. Typical: k >= 5 for low-risk, k >= 20 for higher-risk. |
| **l-diversity** | Extension of k-anonymity: within each k-anonymous group, at least l distinct values for sensitive attributes | When k-anonymity alone can leak sensitive attribute values (e.g., all k records share same disease). Typical: l >= 2. |
| **Differential privacy** | Add calibrated noise to query results so the presence or absence of any individual record cannot be determined | Public-facing analytics, API responses with aggregate counts. Epsilon (privacy budget) controls the tradeoff. Typical: epsilon 0.1-1.0. |

### 10.4 Privacy-Enhancing Technologies (PETs)

| Technology | What It Does | Maturity | When to Use |
|---|---|---|---|
| **Homomorphic encryption** | Perform computations on encrypted data without decrypting | Emerging (high overhead) | Financial services, healthcare -- when you need to process data without seeing it |
| **Secure multi-party computation (SMPC)** | Multiple parties compute a function over their private inputs without revealing them | Emerging | Cross-organization analytics, fraud detection consortiums |
| **Zero-knowledge proofs (ZKP)** | Prove a statement is true without revealing the underlying data | Maturing | Age verification (prove age > 18 without revealing birthdate), identity verification |
| **Federated learning** | Train ML models across decentralized data without centralizing raw data | Maturing | Mobile keyboard prediction, healthcare model training across hospitals |

**Implementation guidance for PETs:** These are specialist tools. Do not deploy them without expert input. The error mode for a misconfigured PET is that you think data is private but it is not -- far worse than knowing you have a compliance gap.

---
