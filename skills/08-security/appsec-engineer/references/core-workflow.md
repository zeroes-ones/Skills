## Core Workflow

### Phase 1: SSDLC Foundation

Execute in order. Do not skip steps.

```
1. ASSESS CURRENT MATURITY
   |-- Map existing security activities: design review? code review? SAST? DAST? pen test? bug bounty?
   |-- Identify gaps using OWASP SAMM or BSIMM as reference model
   |-- Interview: developers (what slows them down?), security team (what keeps them up?), leadership (risk appetite)
   |-- Artifact audit: look at 10 recent PRs — any security review? Last 3 incidents — root cause in design, code, or deps?
   |-- Output: maturity scorecard with gap analysis

2. DEFINE SECURITY GATES (minimum viable SSDLC)
   |-- GATE 1 — Design: Threat model required for features touching auth, payments, PII, or admin functions
   |   |-- Output: threat model document + security requirements checklist + architecture risk accepted by security lead
   |-- GATE 2 — Development: Pre-commit hooks (secrets, lint-security), IDE plugins (Semgrep, Snyk)
   |   |-- Output: zero secrets committed, security lints addressed or suppressed with justification
   |-- GATE 3 — Pull Request: SAST (net-new HIGH/CRITICAL findings = block), SCA (CRITICAL CVEs with KEV = block)
   |   |-- Output: automated scan results in PR, required reviewer for auth/crypto/input validation changes
   |-- GATE 4 — Staging: DAST scan (OWASP ZAP baseline), dependency audit (npm audit / pip audit / go vulncheck)
   |   |-- Output: DAST report with zero HIGH/CRITICAL findings, dependency scan clean
   |-- GATE 5 — Pre-Release: Security review for changes touching auth/crypto/sessions/API keys
   |   |-- Output: security sign-off, pen test if major release

3. TOOLCHAIN ARCHITECTURE
   |-- Secret detection: pre-commit (detect-secrets, git-secrets) + CI (truffleHog, gitleaks) + GitHub push protection
   |-- SAST: Semgrep (fast, community rules, custom rules) OR CodeQL (deep analysis, variant analysis) OR both
   |   |-- PR scan: Semgrep (must finish <5 min). Scheduled deep scan: CodeQL (nightly).
   |-- SCA: Snyk, Dependabot, or OWASP Dependency-Check — must include reachability analysis
   |-- DAST: OWASP ZAP (baseline on staging), Burp Suite Enterprise (scheduled), Nuclei (known CVE scanning)
   |-- Container: Trivy, Grype, or Snyk Container — scan images in CI before push to registry
   |-- IaC: Checkov, tfsec, or KICS — scan Terraform/CloudFormation/Pulumi for misconfigurations

4. METRICS AND REPORTING
   |-- Lead time for security fixes: time from vulnerability discovery to production fix (target: 24h critical, 7d high, 30d medium)
   |-- Mean time to detect (MTTD): time from vulnerability introduction to detection (target: <1 hour via CI scanning)
   |-- Security debt: count of open vulnerabilities by severity, tracked sprint-over-sprint (target: flat or declining)
   |-- Developer friction: survey developers quarterly — "Security tools slow me down" (target: <20% agree)
   |-- Auto-remediation rate: % of vulnerabilities fixed within SLA (target: >90%)
```

### Phase 2: Threat Modeling Integration

```
1. SELECT METHODOLOGY PER CONTEXT
   |-- STRIDE (per-element): Best for new features and services — systematic, comprehensive, developer-friendly
   |   |-- Elements: Data Flows, Data Stores, Processes, External Interactors, Trust Boundaries
   |   |-- Per-element: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
   |   |-- Output: threat list with severity, mitigation, and ticket links
   |-- DREAD (risk scoring): Best for prioritizing existing threat backlog
   |   |-- Damage potential, Reproducibility, Exploitability, Affected users, Discoverability
   |   |-- Score 0-10 per dimension, average = risk score. Sort descending, fix top quartile first.
   |-- PASTA (attack simulation): Best for high-risk systems (payments, healthcare, critical infra)
   |   |-- 7-stage process from business objectives through attack modeling to residual risk analysis
   |   |-- Heavyweight: 2-5 day workshop per system. Reserved for top 5% most critical systems.
   |-- Attack Trees: Best for complex systems with multiple attack paths
   |   |-- Root = attacker goal, children = ways to achieve goal, leaves = specific attacks
   |   |-- AND/OR gates: OR = any child achieves goal, AND = ALL children required

2. FACILITATE THREAT MODELING SESSION (STRIDE, 60-90 minutes)
   |-- Pre-work (participants): system architecture diagram, data flow diagram, API spec
   |-- Session (security engineer + 2-3 senior developers + product owner):
   |   |-- 0-15 min: Walk through architecture — what are we building? data flows? trust boundaries?
   |   |-- 15-60 min: STRIDE per element. Facilitator: "Who could spoof this? What if data is tampered? Can actions be repudiated?"
   |   |-- 60-90 min: Prioritize threats (High/Medium/Low), assign mitigation owner, create tickets
   |-- Post-session: Document threats in standard template, file tickets, schedule follow-up (2 weeks)

3. THREAT MODEL AS CODE
   |-- Store threat models in the repo: threat-model.md or threat-model.yaml next to the code
   |-- Template: Threat ID, STRIDE category, Description, Affected Component, Severity, Mitigation, Ticket, Status
   |-- Version: threat models evolve with the code — update on major architecture changes
   |-- Review: threat model review at architecture change and quarterly for active systems
```

### Phase 3: Security Tooling Pipeline

```
1. PRE-COMMIT (developer machine, 0-second latency goal)
   |-- detect-secrets: block secrets (API keys, tokens, credentials) before commit
   |-- Semgrep local: run subset of rules (<30 seconds) — SQL injection, XSS, hardcoded secrets
   |-- Dependency check: npm audit / pip audit on dependency changes only (<10 seconds)

2. PULL REQUEST (CI, must complete <5 minutes)
   |-- SAST (Semgrep diff scan): scan changed lines only, block on HIGH/CRITICAL findings
   |   |-- Baseline existing findings: suppress pre-existing issues, flag only net-new
   |   |-- Ruleset: start with p/default, add p/owasp-top-ten, p/jwt, p/secrets
   |-- SCA (Snyk/Dependabot): new dependency additions only
   |   |-- Block on: CRITICAL CVEs with KEV, known-malware packages
   |   |-- Warn on: CRITICAL CVEs without KEV, HIGH CVEs
   |-- Secret scanning (truffleHog): full history scan on PR, block on any finding
   |-- IaC scanning (Checkov): block on HIGH/CRITICAL misconfigurations

3. MAIN BRANCH / NIGHTLY (CI, no time constraint)
   |-- SAST (CodeQL deep analysis): full codebase, variant analysis across data flows
   |-- SCA (full audit): all dependencies, reachability analysis, license compliance
   |-- Container scanning (Trivy): all images, OS packages + application dependencies
   |-- DAST (ZAP baseline): staging environment, authenticated scan, active scan on high-risk endpoints

4. FALSE POSITIVE TRIAGE WORKFLOW
   |-- Triage rotation: 1 security engineer per week, 25% time allocation
   |-- Triage SLA: new findings triaged within 1 business day
   |-- Actions: Accept (create ticket), False Positive (suppress with justification), Defer (accept risk with owner + expiry)
   |-- Weekly dashboard: FP rate per rule — disable rules >70% FP, tune rules 40-70% FP
   |-- Monthly retro: top 5 noisiest rules, action plan to reduce noise
```

### Phase 4: Secure Code Review

```
1. PRIORITIZE WHAT TO REVIEW (cannot review everything)
   |-- Tier 1 (review every change): Authentication, authorization/access control, session management, cryptography, API key handling, token generation/validation, password reset flows, payment processing
   |-- Tier 2 (review high-risk changes): Input validation for user-facing endpoints, file upload/download, data export, admin functions, OAuth integration, webhook handlers
   |-- Tier 3 (spot-check): Database queries, logging, configuration changes, dependency updates

2. THE SECURITY REVIEWER'S TRIANGLE (apply to every review)
   |-- AUTHENTICATION: How is the user/service identified?
   |   |-- Check: JWT validation (alg allowlist? expiry check? signature verification?), session cookie attributes (HttpOnly? Secure? SameSite?), MFA enforcement for privileged actions, password policy (argon2id? minimum length 8+?), account lockout after N failed attempts
   |-- AUTHORIZATION: Does this user have permission for this specific operation on this specific resource?
   |   |-- Check: Is there an authorization check on EVERY endpoint? (Insecure Direct Object Reference: can user X access user Y's data by changing an ID?) Is there a privilege escalation path? (can editor become admin by changing a role parameter?) Are permissions checked server-side? (client-side checks are bypassable)
   |-- INPUT VALIDATION: Is every external input validated, sanitized, and safely processed?
   |   |-- Check: SQL queries parameterized? (never string concatenation) HTML output encoded? (context-aware: HTML, JS, CSS, URL) File uploads: type validated server-side? size limited? stored outside web root? Commands: shell = False, args as list? XML: external entity processing disabled? Deserialization: from untrusted source? (if yes, RED FLAG)
   |-- CRYPTO CORRECTNESS (sub-check of all three):
   |   |-- Check: Using standard libraries (libsodium, Tink, Web Crypto)? (NEVER custom crypto) Algorithm choices: AES-256-GCM (not ECB/CBC), RSA 2048+ or ECDSA P-256, SHA-256+ (not MD5/SHA-1), bcrypt/argon2 for passwords? Randomness: secrets.token_urlsafe() or crypto.randomBytes() (not Math.random() or rand())?

3. REVIEW CHECKLIST BY LANGUAGE (common anti-patterns)
   |-- Python: eval()/exec() with user input, pickle deserialization, yaml.load() (use yaml.safe_load()), os.system() with user input, SQL string formatting, DEBUG=True in production
   |-- JavaScript/TypeScript: eval()/Function() with user input, dangerouslySetInnerHTML (React), innerHTML with user data, JSON.parse() on untrusted input without try/catch, noSQL injection (MongoDB $where, $regex), JWT with jsonwebtoken without algorithm option
   |-- Java: Runtime.exec() with user input, ObjectInputStream deserialization, XML parsing without disabling external entities, PreparedStatement not used, String comparison for secrets (use MessageDigest.isEqual), Log4j in classpath (if version <2.17)
   |-- Go: template.HTML() with user data (no auto-escaping), os/exec with user input not sanitized, crypto/md5 or crypto/sha1 for security, math/rand for tokens (use crypto/rand), database/sql with fmt.Sprintf for queries
```

### Phase 5: Zero-Day Response (Dependency Vulnerability)

```
IMMEDIATE (first 4 hours):
1. TRIAGE
   |-- Identify the vulnerability: CVE ID, affected package, fixed version
   |-- Determine exploitability in OUR stack:
   |   |-- Is the vulnerable package in our dependency tree? (dependency:tree / pipdeptree / go mod graph)
   |   |-- Is the vulnerable FUNCTION actually called in our code paths? (reachability analysis)
   |   |-- Is it internet-facing or internal-only?
   |   |-- Does it require authentication to exploit?
   |   |-- Is it actively exploited in the wild? (CISA KEV, threat intel feeds)
   |   |-- Is a public PoC available? (GitHub, Exploit-DB, Twitter/X security researchers)
   |-- Priority matrix: KEV + internet-facing + no auth = EMERGENCY (fix now, deploy immediately)
   |-- Priority matrix: KEV + internal + auth required = HIGH (fix in 24 hours)
   |-- Priority matrix: Non-KEV + not reachable + internal = MEDIUM (fix in next sprint)

2. REMEDIATE OR MITIGATE
   |-- Option A (best): Update to fixed version immediately
   |-- Option B (if no fix available): Apply vendor workaround, WAF rule, or disable vulnerable feature
   |-- Option C (temporary): Add compensating control — restrict network access, require additional auth, increase logging
   |-- Test: run full test suite, security regression tests against the affected component

3. COMMUNICATE
   |-- Internal: Post in security Slack channel within 1 hour of confirmation
   |-- Template: CVE-YYYY-NNNNN, Package X version Y, Exploitable? Yes/No/Investigating, Fix ETA, Who is handling
   |-- External (if applicable): Follow vulnerability disclosure policy — notify affected customers within 24 hours of confirmed exploitation

POST-INCIDENT (within 1 week):
4. ROOT CAUSE ANALYSIS
   |-- Why was vulnerable version in use? (pinned? transitive? missed by scanning?)
   |-- Why wasn't it detected sooner? (scan frequency? reachability analysis not configured?)
   |-- How can we detect this class of vulnerability faster? (improve CVE feed integration, add detection rules)

5. PREVENT RECURRENCE
   |-- Automate: dependabot/snyk auto-PRs for patch-level updates enabled with auto-merge for passing CI
   |-- Reachability: integrate runtime reachability analysis (contrast, aspect-oriented) for Java/.NET
   |-- Scanning cadence: increase SCA scan frequency to every commit (not just daily) for critical dependencies
