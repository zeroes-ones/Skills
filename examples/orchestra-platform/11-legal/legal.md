# Legal Setup

## Terms of Service

Terms of Service for the Orchestra SaaS platform, published at `orchestra.dev/terms`. 12 sections covering: (1) Acceptance of Terms, (2) Account Registration and Security, (3) Service Description and Availability (99.5% uptime SLA for enterprise tier), (4) Acceptable Use (prohibited: illegal content, reverse engineering, exceeding rate limits), (5) Intellectual Property (customer retains ownership of their services, templates, and data; Orchestra retains platform IP), (6) Fees and Payment (net-30 invoicing for annual plans, credit card for monthly), (7) Data Handling (see Privacy Policy and DPA), (8) Confidentiality, (9) Limitation of Liability (capped at 12 months of fees paid), (10) Indemnification, (11) Termination (30-day notice, data export available for 30 days post-termination), (12) Governing Law (Delaware, USA). Last updated: July 1, 2026. Version history tracked in Git and displayed on the terms page.

## Privacy Policy

GDPR-compliant Privacy Policy at `orchestra.dev/privacy`. Covers: data controller identity (Orchestra Platform, Inc., Delaware), categories of personal data collected (account info: name, email, organization; usage data: page views, feature interactions; billing data: processed by Stripe, not stored by Orchestra), purposes of processing (service delivery, product improvement, billing, legal compliance), legal bases (contractual necessity for service data, legitimate interest for product analytics, consent for marketing emails), data retention periods, third-party subprocessors (AWS, Auth0, Stripe, Rudderstack, Intercom, PagerDuty — all listed with purpose and location), international transfers (Standard Contractual Clauses for EU-US data transfers), and data subject rights (access, rectification, erasure, portability, objection — contact privacy@orchestra.dev, 30-day response SLA). Cookie consent banner via Cookiebot (IAB TCF 2.2 compliant, opt-in for analytics cookies).

## Data Processing Agreement (DPA)

Standalone DPA available for download at `orchestra.dev/dpa.pdf`. Incorporates the 2021 EU Standard Contractual Clauses (SCCs) for international data transfers. Automatically incorporated by reference into the Terms of Service. Signed copies executed on enterprise plan ($2,500+/mo). Reviewed by external counsel (Wilson Sonsini) — approved for enterprise procurement, including Fortune 500 security reviews.

## Master Services Agreement (MSA)

MSA template for enterprise customers (annual contracts >$50,000). Covers: service levels (99.5% uptime with 5% service credit per 0.1% below SLA), support tiers (Enterprise: 1-hour response, 24/7), security requirements (SOC 2 Type II in progress, expected Q4 2026), business continuity (DR plan summary, RTO < 4 hours, RPO < 15 minutes), and custom terms (IP indemnification, enhanced liability caps). Negotiated with 2 enterprise prospects (Acme Corp, Globex Inc.) — average negotiation cycle: 4 weeks.

## Open-Source License Audit

All third-party dependencies audited via `license-checker` and FOSSA. Dependency count: 847 npm packages, 94 Go modules, 12 Python packages in data pipeline. License breakdown: MIT (72%), Apache 2.0 (18%), BSD (7%), ISC (3%). Zero GPL, LGPL, or AGPL licenses in the core platform. The `orc` CLI is MIT-licensed and will be open-sourced in Q1 2027 (currently in a private repo). FOSSA scan runs in CI on every PR — blocks merge if a copyleft license is introduced.

## Trademark

"Orchestra" trademark application filed with USPTO on June 1, 2026 (Serial No. 98-123,456), Class 42 (Software as a Service for platform engineering and developer operations). Office action received July 12 — requesting clarification on descriptiveness (responding with evidence of acquired distinctiveness from 6 months of market use). Outside counsel: Fenwick & West. Estimated registration: Q1 2027.
