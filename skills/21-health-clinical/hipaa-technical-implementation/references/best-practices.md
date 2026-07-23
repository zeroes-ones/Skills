# Best Practices

<!-- STANDARD: 3min -->

1. **Audit from day one.** Retrofitting PHI audit trails costs 3x more than building them upfront. Every table with PHI gets an audit shadow table from the first migration.
2. **Encrypt at the application layer for high-sensitivity fields.** Database-level encryption protects against stolen disks, not compromised database credentials. Use Fernet/AES-256-GCM for fields like SSN, diagnosis codes, genetic data.
3. **Minimum necessary is a query-level constraint.** Every API endpoint documents: "Returns: name, email, last_login (minimum for password reset flow)." Not "Returns: user object."
4. **BAA registry is living documentation.** Update it in the same PR that adds a new vendor dependency. Stale BAA registries are worse than none — they create false confidence.
5. **Breach response is rehearsed.** Run a tabletop exercise quarterly. The worst time to discover your notification pipeline is broken is during an actual breach.
6. **Deletion is cascading and verified.** A deletion request must cascade through: primary DB → read replicas → caches → search indexes → backups → logs. Verify with a 30-day follow-up task.
7. **Access logs answer "who saw what when."** Every PHI read is logged with user, timestamp, IP, and purpose. This is required for the HIPAA accounting of disclosures (45 CFR § 164.528).
8. **Never log PHI.** Configure your logger to redact known PHI patterns (emails, SSNs, dates of birth). Use structured logging with PHI-safe fields only.
