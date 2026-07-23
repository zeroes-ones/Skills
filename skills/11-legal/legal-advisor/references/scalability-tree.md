# Scalability Decision Tree

```
Do you have paying customers?
├── YES → Do you have Terms of Service?
│   ├── NO → Get them TODAY. Use Termly/GetTerms for v1. Lawyer review within 90 days.
│   └── YES → Good. Are they clickwrap (user clicks "I agree")?
│       ├── NO → Implement clickwrap. Browsewrap is unenforceable in most jurisdictions.
│       └── YES → Good.
└── NO → Terms can wait. Focus on building.

Do you collect ANY user data (email, analytics, cookies)?
├── YES → Do you have a Privacy Policy?
│   ├── NO → This is priority #1. Every data privacy law requires one. Iubenda/Termly today.
│   └── YES → Is it accurate? (Check: does it list all 3rd-party tools you use?)
│       ├── NO → Update it. Inaccurate privacy policy is worse than no privacy policy.
│       └── YES → Good.
└── NO → (Unlikely for any software product.) Privacy policy still recommended.

Are you using ANY open-source dependencies? (Answer: yes, you are.)
├── YES → Run `npx license-checker --summary` or `pip-licenses`. Any GPL/AGPL?
│   ├── YES (GPL/AGPL in core) → Urgent: isolate via separate service or replace with MIT/Apache alternative.
│   └── No copyleft → Run FOSSA or similar before fundraising/acquisition. Keep license docs updated.
└── NO → Impossible. Run the scan anyway.

Are you fundraising or being acquired within 12 months?
├── YES → IP audit NOW: trademark filings, open-source license clean, all contractor IP assigned.
└── NO → Maintain good practices. Audit annually.
```


**What good looks like:** All customer-facing legal documents (ToS, Privacy Policy, EULA) published and versioned. Contract template library covers MSA, DPA, and SOW with standard redlines. Clickwrap consent recorded with timestamps. GDPR data map documents every data field and its lawful basis.
