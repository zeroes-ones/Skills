# Security Engineer - Threat Modeling Guide

STRIDE methodology, DREAD risk rating, attack trees, and trust boundary mapping.

---

## STRIDE Threat Categories

STRIDE maps threats to system elements in a data flow diagram (DFD).

| Element | STRIDE Category | Threat Description |
|---------|----------------|-------------------|
| **Process** | Spoofing | Impersonating a legitimate process or user |
| **Data Flow** | Tampering | Modifying data in transit or at rest |
| **Data Store** | Repudiation | Denying an action was performed (no audit trail) |
| **Process** | Information Disclosure | Leaking sensitive data |
| **Process** | Denial of Service | Exhausting resources to prevent legitimate use |
| **Data Flow** | Elevation of Privilege | Gaining unauthorized access or permissions |

### Spoofing — Can an attacker pretend to be someone/something else?

**Targets:** Authentication processes, API endpoints, inter-service communication

| Threat | Example | Mitigation |
|--------|---------|------------|
| Credential theft | Phished password | MFA, WebAuthn, FIDO2 |
| Token forgery | JWT without signature verification | Always verify signatures; use RS256/ES256 |
| API key theft | Key in client-side code | Server-side proxy; short-lived tokens |
| Service impersonation | Internal service without mTLS | mTLS, SPIFFE/SPIRE |
| Session hijacking | Session cookie stolen over HTTP | Secure; HttpOnly; SameSite=Strict cookies |

**Checklist:**
- [ ] All authentication uses secure protocols (OAuth 2.0 + PKCE, OIDC)
- [ ] Service-to-service auth uses mTLS or signed tokens
- [ ] Session tokens have Secure, HttpOnly, SameSite flags
- [ ] Password reset tokens are single-use with short expiry

### Tampering — Can data be modified without authorization?

**Targets:** Data at rest (DB, file system), data in transit (HTTP, message queues)

| Threat | Example | Mitigation |
|--------|---------|------------|
| Request modification | Changing price in POST body | Server-side validation; signed requests |
| Database tampering | Direct DB access bypassing app | Row-level security; audit triggers |
| Message queue injection | Publishing unauthorized messages | Message signing; schema validation |
| File tampering | Modifying uploaded files | Content hashing; virus scanning |
| Configuration tampering | Changing feature flags | Git-based config; signed deployments |

**Checklist:**
- [ ] TLS 1.3 for all data in transit (internal and external)
- [ ] Database uses encryption at rest (TDE, disk encryption)
- [ ] Integrity checks on all stored data (HMAC, digital signatures)
- [ ] Write operations require authorization checks server-side

### Repudiation — Can actions be denied?

**Targets:** All user and system actions

| Threat | Example | Mitigation |
|--------|---------|------------|
| Action denial | User claims "I didn't make that transfer" | Audit log with user ID, timestamp, IP, action |
| Log deletion | Attacker clearing logs to cover tracks | Append-only logs; remote log shipping |
| Anonymous access | Critical action without attribution | Require authentication for all state changes |
| Order dispute | Customer claims fraudulent order | Digital signatures; confirmation emails |

**Checklist:**
- [ ] All state-changing operations logged with: who, what, when, source IP
- [ ] Logs are append-only and shipped to immutable storage
- [ ] Audit trail includes both success and failure events
- [ ] Log integrity protected (hash chain, WORM storage)

### Information Disclosure — Can sensitive data be exposed?

**Targets:** Data stores, data flows, error messages, logs, caches

| Threat | Example | Mitigation |
|--------|---------|------------|
| Error leakage | Stack trace in API response | Generic error messages in production |
| Log leakage | PII in log entries | Structured logging with PII redaction |
| Cache exposure | Sensitive data in CDN cache | Cache-Control: private; no-store for sensitive |
| Enumeration | "User exists" vs "Invalid password" | Uniform error messages |
| Backup exposure | Unsecured database backups | Encrypted backups; access-controlled storage |
| Side-channel | Timing attack on string comparison | Constant-time comparison |

**Checklist:**
- [ ] Data classified: public, internal, confidential, restricted
- [ ] Encryption at rest for confidential/restricted data
- [ ] TLS for all data in transit
- [ ] Access logging for all sensitive data reads

### Denial of Service — Can the system be overwhelmed?

**Targets:** All system components

| Threat | Example | Mitigation |
|--------|---------|------------|
| Resource exhaustion | CPU-heavy endpoint called repeatedly | Rate limiting; request validation |
| Memory exhaustion | Unbounded file upload | Size limits; streaming processing |
| Connection exhaustion | Slowloris attack | Timeout configuration; connection limits |
| DB exhaustion | Complex query without index | Query timeouts; read replicas |
| Amplification | Small request → large response | Pagination; response size limits |
| Cascading failure | One service down → all services down | Circuit breakers; bulkheads; graceful degradation |

**Checklist:**
- [ ] Rate limiting on all public endpoints
- [ ] Timeouts on all external calls (database, HTTP, gRPC)
- [ ] Circuit breakers for inter-service communication
- [ ] Autoscaling configured with appropriate thresholds

### Elevation of Privilege — Can users gain unauthorized access?

**Targets:** Authorization checks, role assignments, permission systems

| Threat | Example | Mitigation |
|--------|---------|------------|
| Horizontal escalation | User A accessing User B's data (IDOR) | Ownership verification on all queries |
| Vertical escalation | Regular user performing admin action | Role-based access control (RBAC) |
| Privilege creep | Employee retaining access after role change | Access review; time-bound permissions |
| Dependency confusion | Malicious package with internal name | Scoped packages; private registry |
| Injection → RCE | SQL injection leading to code execution | Parameterized queries; input validation |

**Checklist:**
- [ ] Authorization checked on every request (server-side, not client-side)
- [ ] Principle of least privilege applied to all service accounts
- [ ] Regular access reviews (quarterly minimum)
- [ ] All admin actions require re-authentication

---

## Threat Modeling Process

### Step 1: Diagram (Data Flow Diagram)

Draw the system as a DFD with these elements:
- **External entities** (rectangles): Users, third-party services
- **Processes** (circles): Application servers, microservices, functions
- **Data stores** (parallel lines): Databases, caches, object storage
- **Data flows** (arrows): HTTP, gRPC, message queues, file transfers
- **Trust boundaries** (dashed lines): Network segments, auth boundaries, tenant boundaries

### Step 2: Identify Threats

For each element in the DFD, apply STRIDE:
1. Create a table: Element × STRIDE category
2. For each cell, ask: "Is this threat applicable? How could it be exploited?"
3. Document each threat in: `[Element] [Category]: [Description] — [Impact]`

### Step 3: Mitigate

For each identified threat, design controls:
1. **Eliminate:** Can the risk be removed entirely? (e.g., don't store the data)
2. **Mitigate:** Can controls reduce likelihood or impact? (e.g., encryption, rate limiting)
3. **Transfer:** Can risk be transferred? (e.g., insurance, third-party processor)
4. **Accept:** Is residual risk acceptable? (documented sign-off required)

### Step 4: Validate

Verify mitigations:
- [ ] Security review of proposed controls
- [ ] Penetration testing against threat model
- [ ] Automated security tests for each modeled threat
- [ ] Review threat model at each major release

---

## DREAD Risk Rating

Score each threat 1–10 in five categories. Total score determines priority.

| Factor | Question | 1-3 (Low) | 4-6 (Medium) | 7-10 (High) |
|--------|----------|-----------|--------------|-------------|
| **D**amage | How bad would the impact be? | Minor information disclosure | Significant data loss; limited users | Complete system compromise |
| **R**eproducibility | How easy is it to reproduce? | Requires specific timing; very unlikely | Requires some conditions | Always reproducible |
| **E**xploitability | How easy is it to exploit? | Requires deep expertise; custom tools | Requires some skill; known tools | Script-kiddie level; public exploit |
| **A**ffected Users | How many users affected? | Single user; anonymous only | Group of users; authenticated | All users; administrators |
| **D**iscoverability | How easy is it to find? | Requires source code access | Guessable; documented feature | Published CVE; obvious in UI |

**Scoring:**
- **40-50:** Critical (P0 — fix immediately)
- **30-39:** High (P1 — fix this sprint)
- **20-29:** Medium (P2 — next sprint)
- **10-19:** Low (P3 — backlog)
- **0-9:** Informational (P4 — track)

### DREAD Example: SQL Injection in Login

| Factor | Score | Rationale |
|--------|-------|-----------|
| Damage | 10 | Full database access, all user data |
| Reproducibility | 10 | Works every time with crafted input |
| Exploitability | 7 | sqlmap automates; some knowledge needed |
| Affected Users | 10 | All users in database |
| Discoverability | 6 | Fuzzing or code review reveals it |
| **Total** | **43** | **Critical** |

---

## Attack Trees

Attack trees model how an attacker achieves a goal, starting from the root goal and decomposing into sub-goals.

### Structure
```
Goal: [Attack Objective]
├── OR: Method A
│   ├── AND: Sub-step A1
│   └── AND: Sub-step A2
└── OR: Method B
    └── AND: Sub-step B1
```

- **OR nodes:** Any child achieves the parent
- **AND nodes:** All children must succeed for parent

### Example: Steal User Data
```
Goal: Exfiltrate User PII from Database
├── OR: Direct Database Access
│   ├── AND: Discover DB credentials
│   │   ├── OR: Scan public repos for hardcoded creds
│   │   ├── OR: Exploit SSRF to reach metadata service
│   │   └── OR: Social engineer DBA
│   └── AND: Connect to DB from internet
│       └── OR: Exploit security group misconfiguration
├── OR: Application Layer
│   ├── OR: SQL Injection
│   │   ├── AND: Find injectable parameter
│   │   │   ├── OR: Fuzz all input fields
│   │   │   └── OR: Review JavaScript for API endpoints
│   │   └── AND: Bypass WAF
│   │       └── OR: Use encoding techniques
│   └── OR: Broken Access Control
│       ├── AND: Enumerate object IDs
│       └── AND: Access without authorization
└── OR: Insider Threat
    ├── AND: Gain employee credentials
    └── AND: Export data via legitimate channels
```

---

## Kill Chain (Lockheed Martin Cyber Kill Chain)

| Phase | Description | Detection | Mitigation |
|-------|-------------|-----------|------------|
| 1. Reconnaissance | Research target (scanning, OSINT) | Web server logs; netflow | Minimize attack surface |
| 2. Weaponization | Prepare exploit (malware, payload) | N/A (attacker-side) | N/A |
| 3. Delivery | Deliver weapon (phishing, USB, watering hole) | Email filtering; endpoint detection | User training; email security |
| 4. Exploitation | Exploit vulnerability | HIDS; EDR alerts | Patch management; hardening |
| 5. Installation | Install backdoor/persistence | EDR; file integrity monitoring | Least privilege; app allowlisting |
| 6. Command & Control | Establish C2 channel | Network traffic analysis; DNS logs | Egress filtering; proxy |
| 7. Actions on Objectives | Achieve goal (exfiltrate, encrypt, destroy) | DLP; audit logs; SIEM | Data classification; encryption |

---

## Trust Boundary Mapping

Trust boundaries are lines in the DFD where data crosses from one trust level to another.

### Common Trust Boundaries
| Boundary | Lower Trust | Higher Trust | Controls Required |
|----------|------------|-------------|-------------------|
| Internet → DMZ | Public internet | Web servers | WAF, DDoS protection, input validation |
| DMZ → Internal | Web tier | App tier | Internal firewall, mTLS, API gateway |
| App → Database | Application | Data store | Auth, encryption, least privilege DB user |
| User → API | Unauthenticated | Authenticated | Login, MFA, rate limiting |
| Tenant A → Tenant B | Cross-tenant | Cross-tenant | Tenant isolation; row-level security |
| CI/CD → Production | Build pipeline | Production env | Signed artifacts; approval gates |

### Mapping Exercise
For each trust boundary in your DFD:
1. What authentication is required to cross it?
2. What authorization level is granted after crossing?
3. What data transformations occur (validation, sanitization, encryption)?
4. What logging/monitoring exists at the boundary?
5. Can the boundary be bypassed? (direct DB access, internal network pivoting)
