# Scale Depth: Solo → Small → Medium → Enterprise

<!-- STANDARD: 3min -->

### Solo (1 developer, health app MVP)
**Description:** One developer, one app, cloud-hosted. No dedicated compliance team.
**Approach:** PHI inventory spreadsheet. Audit logging via middleware (not per-endpoint). AWS RDS with encryption enabled (automatic). BAA with AWS only. Deletion: soft-delete in DB only (document limitation). Breach notification: manual process with template.
**Time investment:** ~10 hours for baseline HIPAA technical implementation.

### Small Team (2-10 developers, live product, patients)
**Description:** Growing health app. Real patient data. First compliance audit on horizon.
**Approach:** Full audit table schemas. Application-level encryption for high-sensitivity fields. BAA registry with 5-10 vendors. Cascading deletion with verification. Breach notification pipeline automated. SOC 2 Type II preparation begins.
**Time investment:** ~30 hours initial. ~5 hours/month ongoing.

### Medium Team (10-50 developers, multiple products, HITRUST)
**Description:** Multiple health products. Dedicated security engineer. HITRUST certification target.
**Approach:** KMS with automatic rotation. Per-purpose access control. Audit log aggregation to SIEM. Automated access reviews. Deletion fully automated and verified across all data stores. Breach notification fully rehearsed. HITRUST CSF controls mapped to implementation.
**Time investment:** Dedicated compliance engineering role (0.5 FTE minimum).

### Enterprise (50+ developers, multi-product, multi-regulation)
**Description:** Global health platform. HIPAA + GDPR + state laws. Dedicated compliance team.
**Approach:** Multi-region encryption with customer-managed keys. Real-time PHI flow monitoring. AI-assisted audit log anomaly detection. Zero-trust architecture for PHI access. Fully automated deletion with cryptographic verification. Breach notification with redundant communication channels. Continuous compliance monitoring.
**Time investment:** Dedicated compliance engineering team (2-3 FTE).
