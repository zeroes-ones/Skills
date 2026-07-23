# Scalability Decision Tree

```
Are you processing EU personal data with >1K data subjects?
├── YES → GDPR applies. Privacy policy + cookie consent + DSAR process = minimum viable compliance.
│   └── Are you processing special category data (health, biometrics, political, etc.)?
│       ├── YES → DPIA REQUIRED before processing. Must have explicit consent or specific legal basis.
│       └── NO → Lawful basis documentation sufficient.
└── NO → Is your target market going to include EU in 12 months?
    ├── YES → Implement privacy-by-design now. Cheaper than retrofitting.
    └── NO → Basic privacy policy sufficient. Revisit if market expands.

Are you using 10+ third-party tools/SaaS that touch user data?
├── YES → Create vendor assessment process. DPA queue > 20 vendors = automation needed.
└── NO → Manual DPA management fine. Google Sheets tracking is sufficient until >20 vendors.

Are you receiving 5+ DSARs per month?
├── YES → Automate with DSAR portal. Manual handling costs ~2-4 hours/request.
└── NO → Manual email process fine. Template response + identity check.

Do you have a security incident response plan?
├── NO → This is priority #1. GDPR Art. 33 requires 72-hour notification.
│   Without a plan, you can't meet this. Write the plan BEFORE an incident.
└── YES → Test the plan annually with tabletop exercises.

Are you transferring data from EU → non-adequate countries (e.g., US)?
├── YES → SCCs required. Execute and document. Review annually (EDPB guidance evolves).
└── NO → No transfer mechanism needed. Document adequacy decision relied upon.
```


**What good looks like:** Data inventory complete and reviewed within 6 months. Lawful basis documented for every processing activity. Consent records include timestamps, version of consent presented, and audit trail. DPO appointed (if required). Data subject request process tested and documented.
