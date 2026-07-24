# Threat Modeling Methodologies

## STRIDE (Per-Element)

STRIDE is the most widely used threat modeling methodology. It maps threats to system elements in a data flow diagram.

### The Six Threat Categories

| Category | What the Attacker Does | Example |
|----------|----------------------|---------|
| Spoofing | Pretends to be someone/something else | Using stolen JWT to authenticate as another user |
| Tampering | Modifies data or code | Modifying an API request parameter to change the price in a shopping cart |
| Repudiation | Denies performing an action | Deleting an order and claiming "I never did that" because there are no audit logs |
| Information Disclosure | Gains access to data they shouldn't see | IDOR vulnerability allowing access to other users' private data |
| Denial of Service | Prevents legitimate use of the system | Sending 10,000 requests/second to exhaust API rate limits not configured |
| Elevation of Privilege | Gains higher access than authorized | Exploiting a missing authorization check to access admin functions |

### Per-Element Mapping

For each element in the data flow diagram, consider which STRIDE categories apply:

- **External Interactors** (users, external services): Spoofing, Repudiation
- **Processes** (application logic): Tampering, Info Disclosure, DoS, Elevation of Privilege
- **Data Stores** (databases, caches, file systems): Tampering, Info Disclosure, DoS
- **Data Flows** (API calls, message queues, file transfers): Tampering, Info Disclosure, DoS
- **Trust Boundaries** (crossing from untrusted to trusted zone): All six categories are elevated

### Facilitation Guide (60-90 minute session)

Minutes 0-15: Walk the architecture diagram. Identify all elements and trust boundaries.
Minutes 15-60: STRIDE per element. Use the prompt: "Who could [spoof/tamper with] this? What happens if..."
Minutes 60-75: Prioritize. Each threat gets High/Medium/Low based on impact and likelihood.
Minutes 75-90: Assign owners, create tickets, schedule follow-up.

## DREAD (Risk Scoring)

DREAD quantifies risk for threat prioritization. Score each threat 0-10 on each dimension:

- **Damage Potential (0-10):** How bad is it if exploited? 0=trivial, 10=catastrophic (full data breach)
- **Reproducibility (0-10):** How easy to reproduce? 0=theoretical, 10=always works, one-click
- **Exploitability (0-10):** How skilled must the attacker be? 0=NSA-level, 10=script kiddie with a browser
- **Affected Users (0-10):** How many users affected? 0=none, 10=all users
- **Discoverability (0-10):** How easy to discover? 0=requires source code, 10=visible in URL

Average score = (D+R+E+A+D)/5. Fix top quartile first.

## PASTA (7-Stage Process for Attack Simulation and Threat Analysis)

Reserved for critical systems (payments, healthcare, national security). 2-5 day workshop.

1. Define Business Objectives: What are we protecting? Compliance requirements? Business impact of breach?
2. Define Technical Scope: System boundaries, technologies, dependencies, data classification
3. Application Decomposition: Detailed architecture, data flows, trust boundaries, entry/exit points
4. Threat Analysis: Threat intelligence sources applied to this specific system
5. Vulnerability Analysis: Map threats to existing vulnerabilities and weaknesses
6. Attack Modeling: Build attack trees, simulate attack paths, model attacker capabilities
7. Risk and Impact Analysis: Quantify residual risk, recommend controls, build business case

## Attack Trees

Root node = attacker's goal. Children = ways to achieve it. Leaves = specific attack techniques.

AND gates: ALL children must succeed for the parent goal (harder for attacker).
OR gates: ANY child succeeds = parent goal achieved (easier for attacker).

Assign cost/difficulty to each leaf. The cheapest attack path is the most likely threat.
