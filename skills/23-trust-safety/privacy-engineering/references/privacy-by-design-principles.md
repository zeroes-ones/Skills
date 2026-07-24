# Privacy-by-Design Principles

Cavoukian's 7 foundational principles mapped to system architecture
and enforceable code properties. Privacy must be embedded into design,
not bolted on after the fact — this is the engineering translation.

## Principle 1: Proactive not Reactive — Preventative not Remedial

Anticipate privacy-invasive events before they happen. In code: threat
modeling includes privacy harms (not just security), privacy review is
a gate in the SDLC before any code reaches production.

## Principle 2: Privacy as the Default Setting

No action required by the individual to protect their privacy — it is
built into the system by default. In code: all personal data fields
require explicit opt-in consent at collection. Default retention is
minimum necessary. Default sharing is "none" until purpose specified.

## Principle 3: Privacy Embedded into Design

Privacy is an essential component of the core functionality, not an
add-on. In code: data minimization is enforced at the API layer
(reject requests with unnecessary PII fields). Retention is enforced
by TTL policies in the database schema, not by manual cleanup scripts.

## Principle 4: Full Functionality — Positive-Sum, not Zero-Sum

Privacy and functionality are not tradeoffs — design achieves both.
In code: differential privacy provides analytics utility without
exposing individual records. Federated learning trains models without
centralizing raw data. Privacy-preserving technologies enable
functionality that would otherwise be impossible under regulation.

## Principle 5: End-to-End Security — Lifecycle Protection

Strong security from collection to deletion. In code: encryption at
rest and in transit is table stakes. Access controls are enforced
per data category, not per table. Deletion is automated, verified,
and auditable — not a manual ticket in a backlog that never gets done.

## Principle 6: Visibility and Transparency

Data subjects know what is collected, why, and by whom. In code:
privacy notice version is stored with consent records. Data inventory
is queryable programmatically, not a static spreadsheet. SAR responses
are automated, complete, and delivered within SLA.

## Principle 7: Respect for User Privacy

Keep it user-centric — data subjects own their data, you are the
custodian. In code: consent withdrawal triggers automated deletion
cascade. Data portability exports are machine-readable JSON. No dark
patterns in privacy UI — privacy options are as prominent as any other
setting, not buried in "Advanced Settings > Privacy > Sub-menu #4."

## Architecture Mapping

| Principle | System Property | Enforcement Mechanism |
|-----------|----------------|----------------------|
| Proactive | Privacy gate in CI/CD | Pre-merge privacy review checklist |
| Default | Opt-in data collection | API requires explicit purpose + consent |
| Embedded | TTL-based retention | Database schema enforces `expires_at` |
| Full Functionality | Differential privacy | DP query layer on analytics pipeline |
| End-to-End Security | Encryption + access control | IAM policies per data category |
| Visibility | Programmatic data inventory | Graph database of all PII stores |
| Respect | Deletion cascade + portability | Event-sourced consent + automated SAR |
