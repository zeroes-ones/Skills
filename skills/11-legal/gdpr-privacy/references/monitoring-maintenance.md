# 12. Monitoring & Maintenance

Compliance is not a one-time project. Build these recurring processes:

### 12.1 Consent Audit

- **Quarterly:** Review a sample (10%) of consent records for completeness (all required fields present, consent valid at time of processing). Verify that consent withdrawal propagates to all downstream systems within 30 days.
- **Annually:** Full audit of consent architecture. Test the consent withdrawal flow end-to-end.
- **Consent refresh cadence:** 13-month maximum. Schedule automated re-consent prompts 30 days before expiration.

### 12.2 Data Retention Schedule Enforcement

- **Automated purging scripts:** Cron/scheduled jobs that query for records past retention period. Must run at least monthly.
- **Deletion logs:** Retain evidence of every deletion run -- what was deleted, when, by which job.
- **Legal hold override:** Mechanism to suspend automated deletion. Each hold must have: case identifier, scope (which records), start date, expiry/review date, legal owner.
- **Quarterly verification:** Spot-check 50-100 records across different data categories to confirm deletion has occurred.

### 12.3 Vendor Compliance

- **Annual review:** For every processor -- reconfirm contract currency, SCC version, sub-processor list, security certification status (SOC 2, ISO 27001), and DPA terms.
- **Sub-processor notifications:** When a processor adds a new sub-processor, assess within 30 days. If you object and the processor cannot accommodate, you may need to terminate.
- **Onboarding checklist:** Before sending data to any new vendor -- DPA executed, SCCs attached (if non-EEA), TIA completed, vendor risk tier assigned, privacy team approval.

### 12.4 Privacy Impact Metrics

Track these KPIs monthly. Review quarterly with DPO and management:

| Metric | Target | Escalation Trigger |
|---|---|---|
| DSAR volume | Track trend | >2x normal monthly volume |
| DSAR response time | <30 days (100%) | Any response approaching day 25 |
| DSAR rejection rate | <15% | >20% in any quarter |
| Consent opt-in rate (marketing) | Track trend | <5% -- your consent UX may be coercive or confusing |
| Breach count (total) | 0 | Any breach triggers review |
| High-risk breaches | 0 | Any high-risk breach triggers full investigation |
| Employee training completion | 100% | <95% within 30 days of assignment |
| Vendor DPA currency | 100% | <100% triggers remediation plan |
| ROPA review currency | <12 months since last review per record | Any record >13 months stale |

---
