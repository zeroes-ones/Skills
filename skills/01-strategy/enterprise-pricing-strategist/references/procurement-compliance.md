# Procurement Compliance Reference

## Security Review Package

### Required Documents

| Document | What It Is | Timeline to Obtain | Cost |
|----------|-----------|-------------------|------|
| **SOC 2 Type II** | Independent audit of security, availability, confidentiality controls | 6-12 months (first), annual renewal | $30K-$100K |
| **Penetration Test Summary** | Third-party security test of your application | 2-4 weeks per test, biannual | $15K-$50K per test |
| **Data Processing Agreement (DPA)** | GDPR-compliant data processing terms with SCCs | 1-2 weeks legal review | Legal fees only |
| **Cyber Liability Insurance** | Coverage for data breaches and security incidents | 2-4 weeks to bind | $5K-$20K/year ($2M-$10M coverage) |

### Recommended Additional Documents

| Document | When Needed | Timeline |
|----------|------------|----------|
| **ISO 27001** | International enterprises, especially EU and APAC | 12-18 months first certification |
| **HIPAA BAA** | Healthcare, health-tech customers | 2-4 weeks to execute |
| **PCI DSS ROC** | Processing payment card data directly | 3-6 months assessment |
| **FedRAMP** | US federal government agencies | 12-24 months, $500K-$2M |
| **GDPR Art 28 DPA** | Any EU customer or EU personal data | 1-2 weeks legal review |

## Vendor Assessment Questionnaires

### Common Assessment Frameworks

| Framework | Full Name | Used By | Length |
|-----------|-----------|---------|--------|
| **VSAQ** | Vendor Security Assessment Questionnaire | Google-originated, widely adopted | 150-300 questions |
| **SIG Lite** | Standardized Information Gathering | Shared Assessments program | 200-400 questions |
| **CAIQ** | Consensus Assessments Initiative Questionnaire | Cloud Security Alliance (CSA) | 300+ questions |
| **HECVAT** | Higher Education Community Vendor Assessment Toolkit | Universities, education sector | 200+ questions |

### Pre-Fill Strategy

Build a master response repository:
1. Answer every VSAQ/SIG/CAIQ question once, thoroughly
2. Store in a knowledge base (Notion, Confluence, dedicated tool like Whistic or SafeBase)
3. For each new customer, pull from master → customize → deliver
4. Update annually or after major infrastructure changes

## DPA Requirements (GDPR)

### Standard Contractual Clauses (SCCs)

Required for data transfers from EU to non-adequate countries. Must include:
- Module 2 (Controller-to-Processor) or Module 3 (Processor-to-Processor)
- Description of processing activities (Annex I)
- Technical and organizational measures (Annex II)
- Sub-processor list (Annex III)
- Transfer impact assessment (TIA) for high-risk transfers

### Key DPA Provisions

| Provision | Standard | Note |
|-----------|----------|------|
| Data processing scope | Limited to providing the contracted service | Never accept "any purpose" |
| Sub-processors | Pre-approved list + notification of changes + right to object | Customer can't unreasonably block |
| Data subject requests | Vendor assists; customer responds | Vendor = processor, customer = controller |
| Breach notification | Within 48-72 hours of discovery | GDPR requires 72hr max |
| Data deletion | 90 days post-termination, certified | Customer can request earlier |
| Audit rights | 1x/year, mutually agreed auditor, customer pays | Unless material non-compliance found |

## Insurance Requirements

### Standard Enterprise Insurance Stack

| Insurance Type | Minimum Coverage | Typical Enterprise Requirement |
|---------------|-----------------|-------------------------------|
| **Cyber Liability** | $2M | $5M-$10M for large enterprises |
| **Technology E&O** | $2M | $5M-$10M (errors & omissions) |
| **General Liability** | $1M per occurrence | $2M aggregate |
| **Workers' Comp** | Statutory limits | Required in US |
| **D&O** | $1M-$5M | Required for board protection |

### Certificate of Insurance (COI)

- Must name customer as "additional insured" on general liability
- Must provide 30-day notice of cancellation
- Must be renewed annually with current certificates

## Supplier Diversity

For enterprises with supplier diversity programs:

| Certification | Issuing Organization | Eligibility |
|--------------|---------------------|-------------|
| **MBE** | NMSDC (National Minority Supplier Development Council) | 51%+ minority-owned |
| **WBE** | WBENC (Women's Business Enterprise National Council) | 51%+ women-owned |
| **VBE** | NaVOBA (National Veteran-Owned Business Association) | 51%+ veteran-owned |
| **LGBTBE** | NGLCC (National LGBT Chamber of Commerce) | 51%+ LGBT-owned |
| **SBE** | SBA (Small Business Administration) | Meets SBA size standards |
| **DOBE** | Disability:IN | 51%+ disability-owned |

> **Note:** Certification takes 2-4 months. Start early if targeting enterprises with diversity spend goals.
