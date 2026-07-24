# Data Classification Schema

## Classification Tiers

| Tier | Label | Description | Examples | Handling Rules |
|------|-------|-------------|----------|---------------|
| **Tier 0** | Public | No harm if disclosed | Press releases, public docs, marketing materials | No restrictions. Can be shared externally. |
| **Tier 1** | Internal | Minor harm if disclosed | Internal wikis, project plans, team org charts | Share within organization only. No external distribution without approval. |
| **Tier 2** | Confidential | Significant harm if disclosed | Source code, financial data, employee records, customer lists | Need-to-know access only. Encrypted at rest and in transit. Access logged. |
| **Tier 3** | Restricted | Severe harm if disclosed | PII, PHI, PCI cardholder data, trade secrets, encryption keys | Strictest controls. Encryption mandatory. Access requires explicit approval. Full audit trail. DLP monitoring active. |

## Classification Process

1. **Discover**: Automated scanning identifies all data stores (structured + unstructured)
2. **Classify**: Apply tier based on data type, regulatory requirements, and business impact
3. **Label**: Apply metadata tags to all data assets at the column/field/object level
4. **Protect**: Enforce handling rules appropriate to classification tier
5. **Monitor**: Continuously scan for misclassified data and policy violations
6. **Review**: Re-classify at least annually or when data sensitivity changes

## Automated Classification Tools

- **AWS Macie**: ML-based PII discovery in S3, automated sensitive data discovery
- **GCP DLP API**: 150+ built-in infoType detectors for PII, PHI, credentials
- **Microsoft Purview**: Sensitivity labels, auto-classification, data catalog integration
- **BigID**: Data intelligence platform for privacy, security, and governance
- **Varonis**: Data security platform with classification, permissions audit, and threat detection

## Classification Metadata Standard

Every classified data asset must include:
- `classification_tier`: Public/Internal/Confidential/Restricted
- `data_owner`: Named individual or team accountable for the data
- `regulatory_tags`: List of applicable regulations (GDPR, HIPAA, PCI DSS, SOX, CCPA)
- `retention_period`: How long data is retained before disposal
- `classification_date`: When classification was assigned
- `review_due_date`: Next mandatory classification review (≤ 12 months from classification_date)
