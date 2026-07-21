# Orchestra Platform — GDPR Compliance

**Last reviewed:** 2026-07-21 | **Owner:** Legal & Compliance | **Version:** 2.1

## Data Processing Impact Assessment (DPIA)

Orchestra processes the following categories of personal data:

| Data Category | Retention | Purpose |
|---|---|---|
| Template execution metadata | 90 days | Debugging, usage analytics |
| User accounts (email, name, org) | Until deletion + 30-day grace | Authentication, notifications |
| Billing records | 7 years (legal req.) | Tax and accounting compliance |
| Analytics events (Snowflake) | 25 months active; anonymized at 36 months | Product improvement |

**Note:** Orchestra does not store raw template content, source code, or payment details. Payments are processed entirely through Stripe — Orchestra stores only a customer reference token.

## Consent Management

- **Cookie consent:** CookieYes CMP with opt-in model. Only functional cookies (session, CSRF token) are set before consent.
- **Data processing consent:** Separate, unchecked checkbox at signup — explicitly not bundled with Terms of Service acceptance.
- **Withdrawal:** Users can withdraw consent at any time via Account → Privacy Settings. Withdrawal does not affect lawfulness of prior processing.

## Data Subject Access Requests (DSAR)

1. User submits request to **privacy@orchestra.dev**
2. Identity verified via 2-factor authentication within 48 hours
3. Response provided within 30 calendar days (GDPR Art. 12)
4. Automated data export (JSON format) accessible via admin API endpoint `GET /api/admin/export-data/{user_id}`
5. Deletion cascades to all downstream services and backups within the 30-day grace period

## Cross-Border Data Transfers

- EU customer data stored exclusively in **eu-west-1 (AWS Frankfurt)**
- Standard Contractual Clauses (SCCs) executed for US-based engineering staff who may access EU data for support purposes
- Data Processing Agreement (DPA) available for download at orchestra.dev/legal/dpa

## Cookie Compliance

- **Functional (always on):** Session identifier, CSRF protection token
- **Analytics (opt-in only):** Mixpanel events, Snowflake tracking
- **Marketing (none deployed):** Zero marketing/targeting cookies on the platform

## Compliance Gap — Action Required

> **EU Representative (Art. 27 GDPR):** Orchestra does not have an appointed EU Representative. This is required before onboarding any EU-based customer. **Deadline:** prior to first EU customer contract. Pending legal counsel engagement.

---

*This document is reviewed quarterly. Next review: October 2026.*
