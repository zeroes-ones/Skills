# Regulatory Assessment

## Current Scope — No Regulated Industries

As of July 2026, Orchestra's product scope and customer base do not involve regulated data categories that would trigger HIPAA, PCI-DSS, or FDA requirements. Orchestra processes standard business data (service configurations, template definitions, user activity logs) and does not store, process, or transmit protected health information (PHI), payment card data (cardholder data environment is fully outsourced to Stripe), or medical device data. No regulatory filings or certifications are required before launch.

## Preparedness Frameworks

Despite no current regulatory obligations, Orchestra maintains preparedness frameworks to avoid blocking future enterprise deals in regulated industries:

### HIPAA Readiness

A HIPAA compliance checklist is maintained in the internal compliance repo (`compliance/hipaa-checklist.md`). Key readiness items: Business Associate Agreement (BAA) template drafted by Wilson Sonsini and ready for execution (estimated 2-week turnaround per customer), all data stores support encryption at rest (Aurora: AWS KMS, S3: SSE-KMS) and encryption in transit (TLS 1.3), audit logging infrastructure exists (CloudTrail for AWS API calls, application-level audit logs stored in a dedicated `audit_logs` table), and access controls are granular (RBAC down to the service level). Gap analysis completed with a healthcare compliance consultant (Clearwater) — 14 items flagged, all categorized as "implementable within 4 weeks of BAA signing". No PHI will be accepted until the BAA is executed and the compliance checklist is fully resolved.

### PCI-DSS Scope Assessment

All payment processing uses Stripe Elements (hosted iframe) and Stripe Checkout (hosted page). Orchestra never touches raw card data — the PCI-DSS scope is limited to SAQ A (simplest self-assessment questionnaire, 22 requirements). If billing moves from Stripe-hosted to a custom checkout experience (planned evaluation Q2 2027), the scope would expand to SAQ A-EP or a full Report on Compliance (ROC). A PCI scope assessment document (`compliance/pci-scope.md`) maps data flows and identifies the 7 systems that would move into scope with a custom checkout.

### FDA / SaMD Classification

Not applicable — Orchestra is not a medical device, does not perform clinical decision support, and does not interface with medical devices. Confirmed via analysis of FDA's 21 CFR Part 820 and the IMDRF SaMD classification framework. If a healthcare customer requests a validated (GxP) deployment, the DevOps pipeline would need Computer System Validation (CSV) — a separate assessment document covers GxP readiness but no action is required currently.

## Regulatory Monitoring

A quarterly regulatory review is on the compliance team's calendar. Triggers for reassessment: (1) a new customer in a regulated industry, (2) a new feature involving PHI or payment data, (3) a material change in applicable regulations. Next review: October 1, 2026. The compliance team is a single person (Head of Legal + external counsel as needed) — not a dedicated compliance department.
