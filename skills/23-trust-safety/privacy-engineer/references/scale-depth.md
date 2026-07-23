# Scale Depth

<!-- DEEP: 10+min -->

<!-- SCALE: How privacy engineering evolves as the organization grows -->

### Solo Developer / Early-Stage Startup (1-5 engineers, < 1,000 users)
- Data inventory: a shared document listing the 2-3 databases and services in use
- BAAs: PDF files in a shared drive, annual review is a calendar reminder
- DSAR: manual — privacy contact email, manual database queries, no SLA tracking
- Consent: a single checkbox at registration, no granular categories, no propagation
- Audit logging: application-level logging to stdout, no tamper-proofing
- Deletion: manual SQL DELETE, no cascade, no backup handling
- Privacy review: "does this feel creepy?" gut check before launch
- De-identification: remove names and emails, call it anonymous
- **Key risk:** Everything is manual. One DSAR can consume a day of engineering time. Privacy posture is entirely dependent on the founding team's good intentions.

### Single Product / Small Team (5-20 engineers, 1,000-100,000 users)
- Data inventory: automated discovery script that scans infrastructure, still manually updated
- BAAs: centralized registry in a project management tool, quarterly review reminders
- DSAR: basic automation — intake form + automated primary database query, manual for other systems
- Consent: granular categories (essential, marketing, research), withdrawal updates primary store
- Audit logging: structured logs to separate storage, but still updatable by admins
- Deletion: scripted cascade across known systems, backup handling via deletion registry
- Privacy review: PIA template completed before launch, reviewed by tech lead (not privacy specialist)
- De-identification: Safe Harbor applied manually to analytics exports
- **Key risk:** Privacy is still a part-time responsibility. The engineer doing privacy is also doing feature work. Incomplete data inventory leads to missed systems in DSAR/deletion.

### Multi-Product Platform (20-100 engineers, 100,000-10M users)
- Dedicated privacy engineer (or small privacy engineering team)
- Data inventory: automated discovery + change detection, data catalog with ownership metadata
- BAAs: automated renewal tracking with 90/60/30-day reminders, risk-tiered sub-processor inventory
- DSAR: fully automated pipeline — intake, identity verification, discovery across all systems, response generation
- Consent: event-driven propagation with reconciliation, 24-hour confirmation window, alerting on failure
- Audit logging: WORM storage, cryptographic chaining, automated integrity verification, separate access control
- Deletion: automated cascade across all registered systems, backup exclusion verified, third-party deletion API integration
- Privacy review: PIA/DPIA integrated into SDLC, privacy gate in CI/CD, dedicated privacy review for high-risk features
- De-identification: automated Safe Harbor + k-anonymity assessment, re-identification risk scoring
- **Key risk:** System complexity outpaces privacy automation. New microservices, data pipelines, and third-party integrations are added faster than the privacy catalog is updated.

### Enterprise with Subsidiaries (100+ engineers, 10M+ users)
- Privacy engineering team with specialists (DSAR, consent, de-identification, privacy infrastructure)
- Data inventory: real-time data flow mapping with automated PHI classification and lineage tracking
- BAAs: automated sub-processor risk scoring, continuous certification monitoring, automated breach notification testing
- DSAR: multi-jurisdiction DSAR handling with jurisdiction-specific response templates and legal review routing
- Consent: global consent management with jurisdiction-specific consent models, cross-border transfer controls
- Audit logging: blockchain-verified audit trails, real-time anomaly detection on access patterns, AI-assisted purpose mismatch detection
- Deletion: zero-touch deletion with automated cascade verification, sub-processor deletion audit, backup purge certification
- Privacy review: privacy engineering embedded in every product team, automated PIA triggers from feature flags, privacy budget enforcement
- De-identification: differential privacy for analytics, synthetic data generation for testing, formal re-identification risk assessment with expert determination
- **Key risk:** Regulatory fragmentation across jurisdictions. Privacy requirements in the EU, US (state-by-state), Brazil, India, and others may conflict. Need jurisdiction-specific privacy policy overlays with conflict resolution mechanisms.
