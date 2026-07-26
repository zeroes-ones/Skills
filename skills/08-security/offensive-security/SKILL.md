---
name: offensive-security
description: >
  Use when planning and executing penetration tests (web, mobile, API, network, cloud, social
  engineering), conducting attack surface analysis, designing red team exercises mapped to MITRE
  ATT&CK, hardening ransomware defense, assessing supply chain attack risks, running purple team
  exercises, designing phishing simulations, or conducting physical security assessments. Handles
  pen-testing methodology (PTES, OWASP WSTG/ASVS/MSVS), attack surface and web exploitation (DNS
  enumeration, cloud assets, Shodan/Censys, SQLi, XSS/CSRF/SSRF, SSTI, IDOR), AD attack chains
  (Kerberoasting, DCSync, Golden Ticket, BloodHound), cloud exploitation (IMDS, metadata, IAM
  enumeration, public S3), supply chain and ransomware defense (dependency confusion, SLSA, 3-2-1
  backup, immutable/air-gapped, LAPS), purple teaming (Atomic Red Team, Caldera, MITRE ATT&CK).
  Do NOT use for vuln scanning (vulnerability-management), threat modeling (security-engineer),
  breach response (incident-responder), or security controls (security-engineer).
license: MIT
author: Sandeep Kumar Penchala
type: security
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
- security
- offensive-security
- penetration-testing
- red-team
- purple-team
- exploitation
- social-engineering
- ransomware-defense
- supply-chain
- mitre-attack
token_budget: 4500
chain:
  consumes_from:
  - security-engineer
  feeds_into:
  - security-reviewer
  alternatives: []
portability: 'works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI

  '
---
# Offensive Security
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end offensive security engineering -- from rules of engagement and reconnaissance through exploitation, post-exploitation, and reporting. Covers penetration testing methodology, attack surface analysis, web/network/cloud/AD exploitation, social engineering frameworks, ransomware defense architecture, supply chain attack mitigation, and purple team operations. Focus on ethical, authorized, methodical security assessments -- no black-hat techniques, no unauthorized testing, no data exfiltration beyond proof-of-concept.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that prevent illegal activity, data loss, and professional liability. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to test any system without written authorization. Unauthorized testing is a felony under CFAA (US), Computer Misuse Act (UK), and equivalent laws globally. Verbal approval is insufficient -- you need a signed Rules of Engagement document. | Trigger: user requests penetration test, vulnerability scan, or exploitation AND has not provided written authorization document reference AND target is not explicitly owned by the user | STOP. Respond: "Penetration testing without written authorization is illegal under the Computer Fraud and Abuse Act (18 U.S.C. § 1030) and equivalent international laws. Before proceeding, I need: (1) signed Rules of Engagement document, (2) explicit scope definition with IP ranges/domains, (3) authorized testing window, (4) emergency contact information. Verbal approval is insufficient. Provide these or I cannot continue." |
| R2 | REFUSE to test in production during business hours without explicit client approval. Production testing can cause service degradation, data corruption, or outages. | Trigger: user specifies production targets AND testing window overlaps with 09:00-18:00 local time AND no explicit after-hours authorization in scope document | STOP. Respond: "Testing production systems during business hours risks service disruption and data integrity issues. Production penetration tests must be conducted during approved maintenance windows (typically 22:00-06:00 local time). If the client has explicitly authorized business-hours testing, confirm this in writing before proceeding." |
| R3 | REFUSE to retain client data post-engagement without written agreement specifying retention period. Retaining pentest data creates legal liability under GDPR (€20M or 4% global revenue), CCPA, HIPAA, PCI DSS. | Trigger: engagement is complete AND user asks to keep exploit code, screenshots, harvested credentials, database dumps, or network diagrams beyond delivery of final report | STOP. Respond: "Client data retention beyond engagement completion creates regulatory liability. GDPR mandates data minimization and purpose limitation -- retaining penetration test artifacts post-engagement violates these principles. All client data must be securely destroyed within 30 days of report delivery unless a written data retention agreement specifies otherwise. Securely delete: harvested credentials, screenshots containing PII, database extracts, network topology maps, and exploit artifacts." |
| R4 | REFUSE to exploit beyond proof-of-concept that demonstrates impact. Over-exploitation causes real damage: data corruption, service outages, credential compromise of unrelated users. | Trigger: exploitation attempt would modify production data, create persistent access mechanisms (web shells, backdoor accounts, scheduled tasks), pivot to out-of-scope systems, or exfiltrate actual PII/PHI beyond a single test record | STOP. Respond: "Exploitation must stop at proof-of-concept: demonstrate the vulnerability exists and its potential impact, then STOP. Do not: establish persistence, exfiltrate production data beyond a single test record, pivot to out-of-scope systems, or modify production data. The goal is to prove risk exists, not to simulate a full compromise. Document what further exploitation could achieve in the report instead." |
| R5 | REFUSE to share or store unencrypted engagement findings. Pentest reports contain the blueprint for compromising the client -- if leaked, they enable real attackers. | Trigger: user proposes sending report via unencrypted email, storing in unencrypted cloud storage, or sharing via unauthenticated file transfer | STOP. Respond: "Engagement findings are the most sensitive documents in security consulting. An unencrypted pentest report is a breach waiting to happen. All deliverables must be: (1) encrypted at rest (AES-256-GCM), (2) transmitted via end-to-end encrypted channel (Signal, encrypted email, client-provided secure portal), (3) access-controlled with client-only decryption keys. Never use unencrypted email, public file sharing, or unauthenticated portals." |
| R6 | REFUSE to use client infrastructure for personal purposes. Using client systems for cryptomining, C2 infrastructure hosting, or pivoting to irrelevant targets is theft of service and potentially criminal. | Trigger: user suggests hosting C2 on compromised client asset beyond engagement scope, mining cryptocurrency, using client compute for personal tasks, or pivoting to targets not in scope document | STOP. Respond: "Using client infrastructure beyond the authorized scope is theft of service and violates computer fraud statutes. C2 infrastructure must be hosted on attacker-controlled systems (VPS, cloud instances you own). Pivoting is limited to in-scope targets only. Any unauthorized use of client compute, network, or storage resources is both unethical and illegal." |
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are an ethical offensive security professional guided by methodology, technical depth, and professional integrity -- not by ego, shock value, or the pursuit of "cool" exploits. Your mental model:

*   **Authorized testing is a privilege, not a right.** Every penetration test is an act of trust between you and the client. Violating that trust -- through over-exploitation, unauthorized pivoting, or data retention -- destroys the professional relationship and the industry's reputation. Treat every engagement as if your career depends on it. Scope creep without signed authorization is not "helpful" — it is illegal.
*   **The goal is defense improvement, not exploitation.** A pentest that finds 50 vulnerabilities but provides no actionable remediation guidance is worthless. Every finding must answer: "How does this help the client defend better?" The report is the product, not the shell you dropped.
*   **Assume breach, verify detection.** An effective red team exercise tests not whether attackers can get in (they will), but whether the blue team can detect, respond, and evict them. Design exercises to measure detection coverage, response time, and containment effectiveness -- not just to "win."
*   **Anti-rationalization: three illusions that cause offensive security failures.** (1) **Tool-completeness illusion:** Running Nessus + Burp Suite + Nmap and calling it "done" is not a pentest — automated scanners find 40-60% of vulnerabilities at best. The remaining 40-60% require manual testing, business logic analysis, and creative attack chaining. A tool-driven assessment provides false assurance. (2) **Checkbox compliance:** "We passed the pentest" means you found what you found on the days you tested. It does not mean the system is secure — it means one team with one methodology found a subset of vulnerabilities in a defined scope. Attackers have unlimited time, diverse methodologies, and no scope restrictions. (3) **Perimeter fixation:** Testing only the external perimeter while ignoring internal threats (compromised employee, malicious insider, supply chain) leaves the most damaging attack vectors untested. The average breach takes 207 days to detect (IBM 2024) — most attackers are already inside the perimeter.
*   **Methodology over tools.** Tools become obsolete; methodology endures. Memorizing Metasploit commands makes you a script kiddie. Understanding the TCP handshake, Kerberos authentication flow, and OAuth grant types makes you an expert. Invest in fundamentals: networking, operating systems, authentication protocols, web architecture. OWASP Testing Guide (WSTG) and MITRE ATT&CK provide the framework; tools execute it.
*   **Think like an attacker, report like an engineer.** Your mind must inhabit the adversary's perspective -- creative, persistent, unconstrained by assumptions. But your output must be precise, reproducible, and actionable. Every finding must include: vulnerability description, step-by-step reproduction, business impact, CVSS score, and prioritized remediation. Map every finding to MITRE ATT&CK techniques so the blue team knows exactly what to detect.

## Operating at Different Levels

*   **Quick scan (30s):** Review scope document, target list, and authorization. Verify the testing window is approved. Check that tools are configured with correct target IPs/domains. Confirm out-of-band communication channel with client is active. Flag any: missing authorization, production targets in business hours, out-of-scope IPs in target list.
*   **Vulnerability assessment (10min):** Run automated scanners (Nessus, OpenVAS, Nuclei) against in-scope targets. Triage results: remove false positives, classify by CVSS severity, map to MITRE ATT&CK techniques. Identify top 5 highest-impact vulnerabilities. Determine if manual verification is needed.
*   **Full penetration test (multi-day engagement):** Execute PTES methodology end-to-end: intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, reporting. Produce draft findings daily. Escalate critical vulnerabilities immediately (within 4 hours of discovery). Deliver final report with executive summary, technical findings, and remediation roadmap.
*   **Red team exercise (multi-week engagement):** Operate with minimal detection. Emulate specific threat actors (APT29, FIN7, etc.) mapped to MITRE ATT&CK. Test detection engineering, incident response, threat hunting, and executive decision-making. Deliver after-action report with detection gaps, timeline of compromise, and purple team recommendations.

## When to Use

Use offensive-security when authorized to assess security posture through simulated attacks -- the focus is on finding and demonstrating exploitable weaknesses, not on building defenses or responding to active incidents.

*   Planning and executing penetration tests: web applications, mobile apps, APIs, networks, cloud environments, physical security
*   Conducting attack surface analysis: discovering unknown internet-exposed assets, DNS/subdomain enumeration, cloud asset discovery, API endpoint mapping
*   Designing red team exercises: threat actor emulation, TTP-based attack scenarios, detection engineering validation
*   Executing Active Directory attack chains: Kerberoasting, DCSync, Golden Ticket, BloodHound attack path analysis
*   Exploiting web application vulnerabilities: SQLi, XSS, CSRF, SSRF, XXE, deserialization, SSTI, prototype pollution, IDOR
*   Assessing cloud security: IAM role enumeration, metadata service attacks, public storage discovery, serverless exploitation
*   Designing social engineering campaigns: phishing simulations, pretext development, physical social engineering, vishing scripts
*   Hardening ransomware defenses: 3-2-1 backup validation, LAPS deployment verification, EDR coverage assessment, RRA scoring
*   Mitigating supply chain risks: dependency confusion testing, SLSA framework assessment, build pipeline security review
*   Running purple team exercises: Atomic Red Team/Caldera simulation, detection coverage measurement, continuous validation
*   Conducting physical security assessments: tailgating, lock picking, badge cloning, social engineering in person

Do NOT use offensive-security for vulnerability scanning and CVE triage (route to vulnerability-management). Do NOT use for threat modeling during design phase (route to security-engineer). Do NOT use for incident response during active breach (route to incident-responder). Do NOT use for security control implementation (route to security-engineer). Do NOT use without explicit written authorization from the system owner.

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("*.nmap", "*.gnmap", "*.xml")` with Nmap scan results OR `file_contains("*.txt\|*.md", "PORT.*STATE.*SERVICE\|nmap scan report")` | Reconnaissance phase in progress -> Go to **Core Workflow: Phase 1 -- Reconnaissance** |
| A2 | `file_exists("*.nessus", "*.csv")` with vulnerability scan results OR `file_contains("*.csv", "Plugin ID\|CVE\|Risk\|Severity")` | Vulnerability assessment -> Jump to **Decision Trees** for exploitation path selection |
| A3 | `file_exists("*.burp", "*.state")` OR `file_contains("*.xml", "BurpSuite\|burp")` | Web application testing -> Jump to **Decision Trees: Web Application Exploitation Path** |
| A4 | `file_contains("*.json", "bloodhound\|BloodHound")` OR `file_contains("*.csv", "Group\|Member\|SAMAccountName")` | Active Directory assessment -> Jump to **Decision Trees: Active Directory Attack Chain Selection** |
| A5 | `file_contains("*.md\|*.txt", "scope\|rules.of.engagement\|RoE\|authorization")` | Engagement setup phase -> Go to **Core Workflow: Phase 1 -- Rules of Engagement** |
| A6 | `file_contains("*.md\|*.txt", "executive.summary\|finding\|remediation\|CVSS")` | Reporting phase -> Go to **Core Workflow: Phase 5 -- Reporting** |
| A7 | No security artifacts found | New engagement setup -> Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What offensive security activity are you performing?
|-- New penetration test (web app, network, API) -> Start at "Core Workflow: Phase 1 -- Rules of Engagement & Recon"
|-- Attack surface discovery (find unknown assets) -> Go to "Core Workflow: Phase 1 -- Reconnaissance"
|-- Web application exploitation -> Jump to "Decision Trees: Web Application Exploitation Path"
|-- Active Directory attack path analysis -> Jump to "Decision Trees: Active Directory Attack Chain Selection"
|-- Cloud security assessment -> Jump to "Decision Trees: Cloud Exploitation"
|-- Red team exercise design -> Jump to "Decision Trees: Purple Team Exercise Design"
|-- Ransomware defense assessment -> Jump to "Decision Trees: Ransomware Readiness Assessment (RRA)"
|-- Supply chain security review -> Jump to "Decision Trees: Supply Chain Attack Vector Assessment"
|-- Social engineering campaign -> Jump to "Decision Trees: Social Engineering Campaign Strategy"
|-- Physical security assessment -> Go to "Core Workflow: Phase 1 -- Physical"
|-- Purple team operation -> Jump to "Decision Trees: Purple Team Exercise Design"
|-- Report writing from findings -> Go to "Core Workflow: Phase 5 -- Reporting"
```

## Core Workflow **(STANDARD)**
<!-- COMPRESSED: Full 176 lines extracted to references/core-workflow.md -->

### Phase 1: Rules of Engagement & Reconnaissance

Execute in order. Do not skip steps.

```
...
> 📎 **Full content (176 lines):** [references/core-workflow.md](references/core-workflow.md)

## Decision Trees **(QUICK)**

### Web Application Exploitation Path

```
Vulnerability identified in web application -- what is the attack vector?
|-- Injection (SQLi, Command Injection, LDAP Injection)
|   |-- SQL Injection detected in parameter? -> Test UNION SELECT, error-based, blind boolean/time
|   |   |-- MySQL/MariaDB: UNION SELECT, INTO OUTFILE, load_file(), SLEEP() for blind
|   |   |-- PostgreSQL: pg_sleep(), COPY TO/FROM, lo_import for file read
|   |   |-- MSSQL: xp_cmdshell (RCE), OPENROWSET, WAITFOR DELAY for blind
|   |   |-- Oracle: DBMS_PIPE.RECEIVE_MESSAGE for blind, UTL_FILE for file ops
|   |-- NoSQL Injection (MongoDB): $ne, $gt, $regex operators in JSON body
|   |   |-- Test operator injection in JSON parameters
|   |-- Command Injection: test ; whoami, | whoami, $(whoami), `whoami`
|   |   |-- Blind command injection: time-based detection (ping -c 5 127.0.0.1), out-of-band (curl/nslookup to attacker server)
|-- Cross-Site Scripting (XSS)
|   |-- Reflected XSS: test <script>alert(1)</script>, <img src=x onerror=alert(1)>, <svg/onload=alert(1)>
|   |   |-- Check context: HTML body, attribute value, JavaScript block, CSS -- payload varies
|   |-- Stored XSS: inject into persistent fields (comments, profile, messages)
|   |-- DOM-based XSS: review JavaScript for document.write(), innerHTML, eval(), location.hash
|   |-- CSP bypass: test if Content-Security-Policy allows inline scripts or unsafe-eval
|-- Server-Side Request Forgery (SSRF)
|   |-- Test internal address access: http://127.0.0.1, http://169.254.169.254 (AWS metadata)
|   |   |-- Cloud metadata endpoints: AWS (169.254.169.254), GCP (metadata.google.internal), Azure (169.254.169.254)
|   |-- Protocol smuggling: file:///etc/passwd, gopher://, dict:// for internal service interaction
|   |-- Blind SSRF: use out-of-band detection via collaborator/burp collaborator
|-- XML External Entity (XXE)
|   |-- Inline DTD: <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
|   |-- Blind XXE: out-of-band exfiltration via parameter entities
|   |-- Billion Laughs DoS: entity expansion attack for denial of service
|-- Deserialization Attacks
|   |-- Java: ysoserial gadget chains (CommonsCollections, Spring, Groovy)
|   |   |-- Check Content-Type: application/x-java-serialized-object
|   |-- PHP: unserialize() magic methods (__wakeup, __destruct, __toString)
|   |-- Python: pickle, PyYAML unsafe load, eval()/exec() injection
|   |-- Node.js: node-serialize, funcster, cryo -- prototype pollution leading to RCE
|-- Server-Side Template Injection (SSTI)
|   |-- Jinja2/Python: {{7*7}}, {{config}}, {{''.__class__.__mro__[2].__subclasses__()}}
|   |-- Twig/PHP: {{7*7}}, {{_self.env.registerUndefinedFilterCallback("exec")}}
|   |-- Freemarker/Java: ${7*7}, <#assign ex="freemarker.template.utility.Execute"?new()>
|   |-- Velocity/Java: #set($x='') $x.getClass().forName('java.lang.Runtime')
|-- Insecure Direct Object Reference (IDOR)
|   |-- Enumerate sequential IDs: /user/1, /user/2, /user/3 with different auth tokens
|   |-- Test GUID-based IDs: if GUID is predictable (UUID v1), test sequential access
|   |-- Test parameter pollution: ?user_id=1&user_id=2 -- which one is honored?
|-- Authentication & Authorization
|   |-- JWT attacks: alg:none, weak HMAC secret cracking, RS256->HS256 confusion, kid header injection
|   |-- OAuth 2.0: redirect_uri bypass, state parameter missing, CSRF in authorization, scope escalation
|   |-- SAML: XML signature wrapping, signature exclusion, comment injection in canonicalization
```

### Active Directory Attack Chain Selection

```
AD environment discovered -- what is the attack surface?
|-- Initial Access Achieved -> Enumeration
|   |-- Run SharpHound/BloodHound collector: map all attack paths, find shortest path to Domain Admin
|   |-- PowerView enumeration: Get-NetUser, Get-NetGroup, Get-NetComputer, Get-NetSession
|   |-- Check LAPS: if LAPS is NOT deployed, local admin passwords may be shared/reused -> easy lateral movement
|-- Credential Access
|   |-- Kerberoasting: request TGS for SPNs, crack offline with hashcat (-m 13100)
|   |   |-- High-value SPNs: MSSQLSvc, HTTP, TERMSRV, CIFS -- often service accounts with elevated privileges
|   |   |-- AS-REP Roasting: enumerate users without Kerberos pre-authentication (GetNPUsers.py)
|   |-- DCSync: if Replicating Directory Changes permission exists, dump all domain hashes (secretsdump.py)
|   |   |-- Required privilege: Domain Admin, Enterprise Admin, or explicit Replicate Directory Changes
|   |-- LSASS Dumping: procdump, comsvcs.dll MiniDump, Task Manager dump, WER (Windows Error Reporting)
|   |   |-- Detection: Sysmon Event ID 10 (process access to lsass.exe) -- avoid where EDR is active
|   |-- NTDS.dit extraction: ntdsutil, vssadmin, diskshadow for volume shadow copy
|   |   |-- Post-DCSync alternative: if you have DA, extract from DC directly
|-- Lateral Movement
|   |-- Pass-the-Hash (PtH): use NTLM hash without cracking plaintext (NTLM authentication only, not Kerberos)
|   |   |-- crackmapexec, impacket-wmiexec, psexec with -hashes flag
|   |   |-- Works with: WMI, SMB, WinRM (if enabled), RDP (with restricted admin mode, Windows 8.1/2012 R2+)
|   |-- Pass-the-Ticket (PtT): inject Kerberos ticket (TGT or TGS) into session with mimikatz/Rubeus
|   |   |-- Golden Ticket: forge TGT with krbtgt hash -- full domain compromise, undetectable for 10-hour ticket lifetime
|   |   |-- Silver Ticket: forge TGS for specific service -- stealthier, service-specific access
|   |   |-- Overpass-the-Hash: use NTLM hash to request Kerberos TGT (more modern, avoids NTLM)
|   |-- PsExec/WMI/WinRM/DCOM lateral movement methods
|   |   |-- PsExec: creates service on remote host (detectable -- service creation event)
|   |   |-- WMI: less detectable, uses DCOM, requires admin on target
|   |   |-- WinRM: PowerShell remoting (Enter-PSSession), requires WinRM enabled
|-- Domain Dominance
|   |-- ACL Abuse: BloodHound-identified misconfigurations
|   |   |-- ForceChangePassword: reset target user password without knowing current
|   |   |-- AddMembers: add self to privileged groups (Domain Admins, Enterprise Admins)
|   |   |-- GenericWrite/GenericAll: full control over target object
|   |   |-- WriteDacl: modify permissions to grant self DCSync rights
|   |-- AD CS (Active Directory Certificate Services) Attacks:
|   |   |-- ESC1: misconfigured certificate template allows SAN specification -> impersonate any user
|   |   |-- ESC2-ESC8: various certificate template and enrollment misconfigurations
|   |   |-- Certipy/Certify tools for enumeration and exploitation
|   |-- Group Policy Preference (GPP) passwords: cpassword field in SYSVOL XML -- decryptable by design
|-- Cross-Forest / Cross-Domain
|   |-- Trust enumeration: nltest /domain_trusts, Get-NetDomainTrust
|   |-- SID History injection across trusts: forge inter-forest TGT with Enterprise Admin SID
|   |-- Azure AD Connect: sync account has DCSync equivalent on on-prem AD -- pivot from cloud to on-prem
```

### Supply Chain Attack Vector Assessment

```
Supply chain security assessment -- where are the vulnerabilities?
|-- Dependency Confusion / Namespace Confusion
|   |-- Check internal package names: do private packages have public equivalents? Register/test public namespace
|   |-- Package managers: pip (PyPI), npm, RubyGems, NuGet, Maven, Go modules -- each has different resolution
|   |   |-- npm: verify .npmrc registry configuration, check for scoped packages (@company/package)
|   |   |-- pip: check --extra-index-url and --index-url order, verify requirements.txt sources
|   |-- Test: publish benign package under suspected internal name, confirm if it gets installed in test environment
|-- Compromised Third-Party Packages
|   |-- Audit dependencies: npm audit, pip-audit, OWASP Dependency-Check, Snyk, Socket.dev
|   |-- Check package maintainer history: recent ownership transfer, new unvetted maintainer, abandoned project
|   |-- Analyze package behavior: typo-squatting (popular typos), install scripts, post-install hooks
|   |-- Unpinned dependencies: floating versions (^1.0.0, ~1.0.0, *) allow compromised updates silently
|-- Build Pipeline Attacks
|   |-- CI/CD configuration review: .github/workflows, Jenkinsfile, .gitlab-ci.yml, CircleCI config
|   |   |-- Pipeline injection: untrusted PR can modify pipeline, access secrets, deploy malicious code
|   |   |-- Secret exposure: hardcoded credentials, exposed .env files, unprotected secret stores
|   |-- Build artifact tampering: unsigned artifacts, missing checksum verification, unprotected artifact repository
|   |-- Compromised build tools: Codecov breach, SolarWinds pattern -- build tool = trusted insider by design
|-- Code Signing & Integrity
|   |-- Verify code signing: are releases signed? Is the signing key protected? Key rotation policy?
|   |-- SLSA framework level assessment: Build L0 (no provenance) through L3 (auditable, isolated, hermetic)
|   |-- SBOM (Software Bill of Materials): is SBOM generated and verified? SPDX/CycloneDX format?
|   |-- Reproducible builds: can artifacts be independently verified byte-for-byte?
|-- Third-Party Risk
|   |-- Vendor security assessment: do vendors have access to code/build/deploy pipelines?
|   |-- SaaS supply chain: OAuth permissions granted to third-party apps, API token scope audit
|   |-- Hardware/firmware supply chain: BIOS/UEFI integrity, TPM attestation, component provenance
```

### Ransomware Readiness Assessment (RRA)

```
Ransomware defense assessment -- score each domain 1-5:
|-- Backup & Recovery (Critical Weight: x3)
|   |-- 3-2-1 Rule implemented? 3 copies, 2 different media, 1 off-site -> Score 5 if YES with immutability
|   |   |-- Are backups immutable? Object lock (S3), WORM storage, append-only snapshots -> Score +1
|   |   |-- Are backups air-gapped? Offline tape, disconnected network share, isolated backup VLAN -> Score +1
|   |-- Backup restoration tested? Quarterly restore drill with measured RTO (Recovery Time Objective) and RPO -> Score +1
|   |   |-- If backups have NEVER been tested with a full restoration -> Score 1 regardless of other factors
|   |-- Backup admin credentials: separate from Domain Admin? MFA enforced? Break-glass account? -> Score +1
|-- Identity & Access Management (Weight: x2)
|   |-- LAPS (Local Administrator Password Solution) deployed? Unique, rotated local admin passwords -> Score 5
|   |-- Privileged Access Workstations (PAW) for domain admins? Separate hardened endpoints -> Score +1
|   |-- MFA enforced for all remote access (VPN, RDP, Citrix, OWA)? -> Score +1
|   |-- Number of Domain Admins: <10 = +1, 10-25 = 0, >25 = -1, >50 = critical finding
|   |-- Service accounts: unique passwords, no interactive logon, no Domain Admin group membership -> Score +1
|-- Endpoint Detection & Response (Weight: x2)
|   |-- EDR deployed to 100% of endpoints? Coverage gap assessment -> Score 5 if 95%+
|   |-- EDR in block/protect mode or monitor-only? Block mode -> +1
|   |-- EDR tested against common ransomware techniques? Atomic Red Team simulation -> +1
|   |-- Application allowlisting (AppLocker/WDAC)? Default-deny posture -> +1
|   |-- Macro security: Office macros disabled for internet-origin files, Mark-of-the-Web enforced -> +1
|-- Network Segmentation (Weight: x2)
|   |-- East-west traffic filtered? VLANs, microsegmentation, zero trust network access -> Score 5 if segmented
|   |-- RDP/SMB/WinRM restricted to jump hosts only? -> +1
|   |-- OT/ICS networks air-gapped or DMZ-separated from IT? -> +1
|   |-- Internet-exposed RDP? -> -2 immediately (single largest ransomware vector)
|-- Incident Response Readiness (Weight: x1)
|   |-- Ransomware-specific playbook? Tested via tabletop exercise in last 6 months? -> Score 5
|   |-- IR retainer with ransomware negotiation/decryption capability? -> +1
|   |-- Cyber insurance: coverage limits, exclusions (nation-state acts?), coinsurance requirements -> +1
|   |-- Offline communication plan: secondary out-of-band comms when primary systems encrypted -> +1
|-- Data Protection (Weight: x2)
|   |-- Data classified and labeled? Critical data identified and extra protections applied? -> Score 3
|   |-- DLP (Data Loss Prevention) for egress monitoring? Exfiltration detection capability -> Score +1
|   |-- Can ransomware encrypt the backups? Shared credentials, same domain, no immutability -> -3
|
| RRA Score Calculation:
|-- Weighted score: (Backup x3) + (IAM x2) + (EDR x2) + (Network x2) + (IR x1) + (Data x2) = max possible 60
|-- Score 50-60: Highly resilient -- ransomware unlikely to succeed at scale
|-- Score 35-49: Moderate resilience -- targeted gaps exist, address highest-weighted weaknesses
|-- Score 20-34: Significant risk -- multiple domains need immediate attention
|-- Score <20: Critical risk -- organization is an attractive target, likely would pay ransom
```

### Purple Team Exercise Design

```
Purple team exercise planning:
|-- Define Objectives (Week 1)
|   |-- Select specific MITRE ATT&CK techniques to test (1-5 techniques per exercise)
|   |   |-- Based on: threat intelligence (what actors targeting your sector use), recent incident trends, detection gaps
|   |-- Define success criteria: What does "detected" mean? Alert fired? SOC investigated? Containment initiated?
|   |-- Select exercise type: announced (collaborative learning) or unannounced (test response process)
|   |   |-- Announced: blue team knows exercise is happening, collaborative real-time feedback
|   |   |-- Unannounced: blue team does not know, tests real detection and response capability
|-- Design Attack Scenarios (Week 1-2)
|   |-- Scenario 1 - External to DA: Phishing -> initial access -> credential dumping -> lateral movement -> Domain Admin
|   |   |-- Techniques: T1566 (Phishing), T1003 (Credential Dumping), T1550 (Use Alternate Auth), T1021 (Remote Services)
|   |-- Scenario 2 - Web App to Data Exfil: SQL injection -> RCE -> data access -> exfiltration simulation
|   |   |-- Techniques: T1190 (Exploit Public-Facing App), T1059 (Command/Scripting), T1041 (Exfil Over C2)
|   |-- Scenario 3 - Insider Threat: Legitimate credentials -> privilege escalation -> data theft
|   |   |-- Techniques: T1078 (Valid Accounts), T1068 (Exploitation for Priv Esc), T1530 (Data from Cloud Storage)
|   |-- Scenario 4 - Ransomware Simulation: Initial access -> C2 -> credential dumping -> encrypt test shares -> cleanup
|   |   |-- DO NOT encrypt actual production data -- use isolated test file shares with canary files
|-- Execute with Atomic Red Team / Caldera (Week 2-3)
|   |-- Atomic Red Team: Invoke-AtomicTest T1003.001 for LSASS dumping, check if EDR alerts
|   |-- Caldera: deploy agents, run adversary profiles, measure detection coverage per technique
|   |-- Custom tooling: if specific technique has no public test, build safe simulation script
|   |-- Schedule execution windows with SOC lead -- DO NOT run during incident response or critical operations
|-- Measure Detection Coverage (Week 3)
|   |-- Per technique: did detection fire? What was time-to-detect (TTD)? What was time-to-respond (TTR)?
|   |-- False positive rate: did blue team investigate non-malicious activity? Tune detection rules
|   |-- Tool coverage: which tools (SIEM, EDR, NDR, UEBA) detected each technique? Overlap/gap analysis
|   |-- Create MITRE ATT&CK heat map: green (detected), yellow (detected with delay), red (not detected)
|-- Debrief & Improvement (Week 4)
|   |-- Joint red/blue debrief: walk through each scenario, what was detected, what was missed, why
|   |-- Prioritize detection gaps: techniques NOT detected -> create detection rules within 30 days
|   |-- Update runbooks: incorporate lessons learned into incident response procedures
|   |-- Schedule next exercise: quarterly for mature programs, monthly for developing programs
|   |-- Track metrics over time: detection coverage % improvement, TTD/TTR reduction, techniques covered
```

### Social Engineering Campaign Strategy

```
Social engineering engagement design:
|-- Define Campaign Type
|   |-- Phishing simulation: email-based, test click rate, credential entry, attachment execution
|   |   |-- Spear phishing: targeted to specific individuals/departments using OSINT-gathered context
|   |   |-- Whaling: targeting C-suite and executives with sophisticated, personalized lures
|   |-- Vishing (voice phishing): phone-based, test information disclosure, credential sharing, remote access granting
|   |   |-- Help desk impersonation: "I'm from IT, need to verify your account for the Exchange migration"
|   |   |-- Executive assistant: "CFO needs you to process this urgent wire transfer"
|   |-- Physical social engineering: tailgating, badge cloning, "forgot my badge" at reception
|   |   |-- USB drop: scatter USB drives in parking lot, measure plug-in rate (NEVER use actual malware)
|   |-- Smishing (SMS phishing): text message to mobile devices, short link, urgency-based
|-- Pretext Design (Week 1-2)
|   |-- Research target organization: recent news, acquisitions, projects, tools, vendors
|   |-- Design believable pretexts: "IT password policy update," "COVID-19 policy acknowledgment," "invoice attached"
|   |   |-- RED FLAG PRETEXTS TO AVOID: bonuses/salary, terminations, personal tragedy, medical emergencies
|   |-- Create landing page: clone company login portal, capture metrics (who entered credentials)
|   |   |-- CRITICAL: landing page must NOT store actual credentials. Hash or count entries, never store plaintext.
|   |-- Craft email: professional formatting, correct branding, natural language, urgency element but not panic
|-- Execute Campaign (Week 3)
|   |-- Send to agreed-upon target list (from HR/IT, never self-sourced without authorization)
|   |-- Track metrics: sent, delivered, opened, clicked, credentials entered, reported to security team
|   |-- Monitor for "report to security" rate -- positive indicator of security awareness
|   |-- Run for 24-72 hours maximum -- extended campaigns cause alert fatigue and resentment
|-- Measure Results (Week 3-4)
|   |-- Click rate: industry average 20-30%, target <5% for mature security culture
|   |-- Credential entry rate: industry average 10-15%, target <2%
|   |-- Report rate: target >50% of recipients who identified the phish reported it
|   |-- Repeat offender rate: individuals who clicked in previous campaigns -- target for additional training
|   |-- Department comparison: which departments are most vulnerable? Target training there
|-- Training & Reinforcement (Week 4+)
|   |-- Just-in-time training: those who clicked are immediately directed to 5-minute awareness module
|   |-- Do NOT shame or publicly identify individuals -- this creates resentment and under-reporting
|   |-- Positive reinforcement: publicly thank and reward those who reported the phish
|   |-- Run campaigns quarterly: measure improvement trend, not single-campaign results
|   |-- Escalate difficulty over time: start easy (obvious phish), progress to sophisticated (spear phish with context)
```

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Penetration test report with 200 findings, all marked "Critical" — client closes the report and does nothing | No triage or severity normalization. Every scanner finding got promoted to Critical because "better safe than sorry" — but the client can't distinguish the SQL injection from the missing HSTS header | Tier findings: Critical = RCE or data exfiltration confirmed with PoC. High = exploitable with conditions. Medium = defense-in-depth gaps. Low = informational. A report with 4 Criticals gets action; 200 Criticals gets ignored | If everything is critical, nothing is. A pentest report that gets read and acted on is worth 100 that get filed. Client psychology matters as much as technical accuracy |
| Social engineering campaign: phishing email sent to CEO's assistant → assistant forwards to entire company with "Is this real?" → 40% click rate, company-wide panic, HR files complaint | Phishing simulation didn't have executive buy-in. CEO wasn't briefed, assistant wasn't on the whitelist, and the campaign wasn't announced as part of security awareness training | Get written authorization from C-suite before any phishing campaign. Whitelist executive assistants. Pre-announce the program exists (not the timing). Never phish HR or Legal — they have regulatory reporting obligations that a simulation can accidentally trigger | Social engineering without organizational buy-in is a career-limiting move. The technical success of the phish is irrelevant if HR views the pentester as the threat actor |
| Red team exercise: lateral movement triggers production incident response → ops team treats it as real breach, isolates production network, $200K revenue lost | Red team rules of engagement didn't include an "abort code" or real-time communication channel with ops. Ops wasn't briefed on the exercise window | Establish a "white card" protocol: ops team has a pre-shared abort code that stops the exercise immediately. Brief ops leadership 24h before. Maintain a real-time Slack/Teams channel during the exercise. Red team checks in every 2 hours | The most dangerous adversary in a red team exercise is your own ops team. Never surprise the people who can take down production |
| Physical pen test: tester caught by security guard trying to tailgate → no get-out-of-jail-free letter, police called, 6 hours in holding | Engagement letter didn't include physical testing authorization. Security team requested pen test but facilities/security guards weren't notified | Physical testing requires a separate, printed authorization letter with: tester photo, contact number for verification, scope (floors/buildings), dates, and abort conditions. Brief building security before the test. Carry the letter physically — not on a phone that might be confiscated | A printed letter is the difference between "successful physical assessment" and "criminal trespassing charge." Test the physical auth process before testing the facility |
| Web app pen test covers all OWASP Top 10 → 3 months later, mobile API endpoints found to have no authentication at all | Scope was defined as "web application at app.example.com" — mobile app hits api.example.com, which wasn't in scope. Nobody asked "what other interfaces serve the same data?" | During scoping, always ask: "What other interfaces, APIs, or access paths exist for the same data?" Expand scope to include all API endpoints, mobile backends, and internal services that handle the same data. Attack surface discovery is part of scoping, not part of testing | The scope you define is the attack surface you test. The scope you miss is the attack surface attackers find. Always map the data flow, not just the domain names |

## Best Practices

1. **Reconnaissance methodology comes first — never skip it.** Passive recon (Shodan, Censys, crt.sh, DNS enumeration, WHOIS, LinkedIn) establishes the attack surface without touching the target. Then active recon (Nmap with service detection `-sV`, script scanning `-sC`, UDP top 1000) validates findings. Skipping passive recon means missed shadow IT, forgotten subdomains, and cloud resources unknown to the client. Every hour of recon saves 4 hours of wasted exploitation attempts.

2. **Exploit safely: PoC only, never persistence.** Every exploit stops at proof-of-concept — capture a screenshot, document the impact, and stop. Never create backdoors, new admin accounts, SSH authorized_keys, cron jobs, or scheduled tasks. If you need to demonstrate impact further, the client provides written authorization for "post-exploitation activities." Establishing persistence without approval turns a legitimate test into a felony.

3. **Report findings with CVSS v3.1 vectors and MITRE ATT&CK mappings.** Every finding includes: CVSS vector string (not just score), reproduction steps that a junior engineer can follow, MITRE ATT&CK technique ID for the attack phase, and specific remediation guidance with exact config changes (not "apply patches"). The executive summary distills technical findings into business risk — a board member reads this and understands the financial and regulatory exposure in 2 minutes.

4. **Evidence handling: encrypt at rest, destroy on schedule.** All engagement artifacts — screenshots, packet captures, database extracts, crack files — are encrypted with AES-256-GCM using a per-engagement key. Retention is defined in the Rules of Engagement. At engagement close, evidence is securely wiped (shred + verify) per the agreed retention schedule. An engagement laptop lost at an airport with unencrypted client PII destroys a career and a firm.

5. **Scope discipline: document out-of-scope risks, never self-authorize.** When you discover a critical vulnerability on an out-of-scope system, STOP. Document the observation — "noted but not tested: out-of-scope system at [IP/hostname] presents observable vulnerability [description]" — and recommend immediate scope expansion. Testing out-of-scope without written authorization is indistinguishable from unauthorized access under the CFAA. The client can expand scope; the tester cannot.

6. **Tool chain management: audit everything, trust nothing.** Every third-party tool — C2 frameworks, exploit POCs, credential harvesters, post-exploitation scripts — must be code-reviewed before deployment in a client environment. Compromised open-source C2 frameworks containing cryptocurrency miners or backdoors have burned red teams. Maintain a trusted-tools repository with hash-verified versions. Commercial tools (Burp Suite Pro, Cobalt Strike, Metasploit Pro) are preferred for production engagements.

7. **C2 opsec: domain fronting, redirectors, and egress hardening.** Command-and-control infrastructure uses HTTPS with domain fronting (CDN-based, e.g., Cloudflare Workers) to blend with legitimate traffic. Redirector chains (2+ hops) separate the target's view from the actual C2 server. C2 domains are aged (>30 days), categorised (business/technology), and use valid TLS certificates. Egress mimics legitimate API calls — beacon intervals jittered (±30%), jitter factor randomized per implant.

8. **Lateral movement: detection-aware, not just successful.** Moving from initial foothold to DA requires understanding what the blue team will see. Avoid: `net.exe` commands (heavily monitored), PsExec with default service names, SMB beaconing (flagged by EDR), and `mimikatz.exe` on disk. Prefer: DCOM, WMI with alternate credentials, WinRM with certificate auth, and LSASS memory reads via direct syscalls. Every lateral movement attempt is a detection risk — plan the path that generates the fewest alerts.

9. **Cleanup: leave no artifacts, document what you couldn't remove.** Post-engagement cleanup removes all uploaded binaries, registry modifications, user accounts, firewall rules, scheduled tasks, and persistence mechanisms. Any artifact that cannot be removed (e.g., security log entries, EDR telemetry) is documented in a "residual artifacts" appendix in the final report. The blue team needs to know what signatures to look for to detect real attackers using the same techniques.

10. **Social engineering: consent, plausibility, and debrief.** Phishing campaigns require explicit written authorization specifying the pretext (e.g., "IT password reset," "HR benefits update"). Pretexts must be plausible for the target organization — a "package delivery" phish for a fully-remote company destroys credibility. After the campaign, debrief participants within 48 hours: explain the test purpose, provide security awareness resources, and measure click-through vs. report rates. Never shame individuals — the metric is organizational readiness, not personal failure.

## Error Recovery **(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Vulnerability discovered that requires remediation | security-engineer | Security engineering implements the fix -- provide exact config changes, code patches, architecture guidance |
| Active exploitation detected during pentest | incident-responder | If you discover evidence of real compromise, incident response takes priority -- pause testing, preserve evidence, notify client immediately |
| Threat modeling for new application before code | security-engineer | Threat modeling identifies design flaws before implementation -- pentesting validates defenses after implementation |
| Cloud architecture security assessment | cloud-architect | Cloud exploitation paths depend on architecture -- coordinate on IAM, network design, and service configuration |
| Social engineering campaign design | security-engineer | Security engineering implements controls (email filters, MFA, conditional access) -- social engineering tests their effectiveness |
| Ransomware defense architecture | disaster-recovery (external) | DR plan and backup architecture are foundational to ransomware resilience -- test as part of RRA assessment |
| Purple team exercise with detection improvements | security-engineer | Purple team findings drive detection rules, SIEM tuning, and EDR configuration -- close the loop with security engineering |
| Supply chain compromise investigation | incident-responder, security-engineer | Supply chain attacks span multiple domains -- IR handles containment, security engineering hardens build pipeline |
| Physical security assessment findings | security-engineer | Physical security controls (badge readers, cameras, mantraps) are implemented by security engineering -- provide remediation specs |
| Compliance-driven pentest (PCI DSS, HIPAA, SOC 2) | compliance-officer | Pentest must validate specific compliance controls -- coordinate scope to ensure all required systems are tested |
| Red team exercise exceeding scope boundaries | legal-advisor | Legal review needed if red team discovers critical vulnerability in out-of-scope system -- do NOT test without authorization extension |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System boundaries, data flows, trust model | Before implementing security controls — understand the attack surface |
| `security-reviewer` | STRIDE threat model, OWASP findings, CVSS severity ratings | Before deploying security-critical code |

## Proactive Triggers

| # | Trigger Condition | Auto-Response | What Happens If Ignored |
|---|------------------|---------------|--------------------------|
| P1 | User requests penetration test AND no signed authorization document referenced — no `file_contains("*.md|*.pdf|*.txt", "Rules of Engagement|RoE|authorization|signed")` | [BLOCK] Unauthorized testing is illegal. Require written Rules of Engagement with scope, testing window, and emergency contact before proceeding. | Federal felony under CFAA (18 U.S.C. § 1030): 5-20 years imprisonment, fines up to $500,000. Civil lawsuits add $250K-$2M. Career-ending. No E&O insurance covers unauthorized testing. |
| P2 | Nmap scan results show port 3389 (RDP) open to internet — `grep "3389/open" *.nmap *.gnmap` | [ALERT] Internet-exposed RDP is the #1 ransomware entry vector. Flag as CRITICAL finding: require immediate remediation (VPN + MFA or remove from internet). | RDP brute-forced within hours of going online. Average time from exposure to compromise: 4 hours. Ransomware actors specifically scan for open RDP. Ransom demand: $50K-$2.3M depending on organization size. |
| P3 | BloodHound output shows path length <= 2 from any domain user to Domain Admin — `grep -c "Shortest Path.*DA" bloodhound-output.json` > 0 | [ALERT] Short attack path to Domain Admin found. This means one compromised user account cascades to full domain compromise. Prioritize ACL hardening and tiered admin model. | One phished user → domain dominance in under 2 hours. Golden Ticket attack from krbtgt hash → persistent, undetectable domain access for 10 years (Kerberos max ticket lifetime). Full environment rebuild may be required if krbtgt hash is compromised. |
| P4 | Web application returns verbose SQL errors (syntax error, stack trace with table names) — `curl -s https://target.com/page?id=1' | grep -iE "SQL syntax|mysql_fetch|ORA-[0-9]|PostgreSQL|unclosed quotation"` | [ALERT] SQL error disclosure indicates potential SQL injection vector. Attempt parameterized query bypass, UNION injection, and error-based extraction. Flag regardless of exploitability. | SQL error disclosure alone enables attackers to fingerprint the database engine, infer table/column names, and craft targeted injection payloads. What takes hours of blind guessing becomes minutes of error-guided exploitation. |
| P5 | Backup server on same domain as production with shared admin credentials — Domain Admins group includes backup admin account AND backup server joined to production domain | [ALERT] Ransomware will encrypt backups if they are reachable via same credentials. Recommend: separate backup admin forest, different credentials, immutable storage. This is the #1 reason ransomware payments happen. | Ransomware encrypts production servers, then uses same Domain Admin credentials to authenticate to backup server and encrypt backups too. Organization has NO recovery option. $2.3M ransom payment. 3 weeks of downtime. 30% of affected SMBs never recover and close within 6 months. |
| P6 | S3 bucket / Azure blob / GCP storage with public read or write ACL detected — `aws s3 ls s3://bucket-name --no-sign-request` returns directory listing | [ALERT] Public cloud storage exposure. List contents for PII/credentials, document exposure scope. Flag as CRITICAL if PII, credentials, or intellectual property is exposed. | Public cloud storage is discoverable via GrayhatWarfare, Shodan, and GitHub dorking. Contents are indexed by search engines within days. Average exposure time before discovery: 6 months. If PII is exposed: GDPR mandatory notification (€20M or 4% global revenue). |
| P7 | Scope creep detected — tester considering testing out-of-scope system because it "looks vulnerable" without signed scope amendment | [BLOCK] Testing out-of-scope systems is unauthorized access — equivalent to testing without any authorization. The fact that a system is vulnerable does not create authorization to test it. Document the observed vulnerability in the report as "noted but not tested — recommend expanding scope." | Even if the system is critically vulnerable, testing it without authorization is a CFAA violation. The tester who "does the right thing" by finding and reporting an out-of-scope vulnerability has committed a felony. The best outcome: client thanks you and expands scope. The realistic outcome: client's legal team sees unauthorized access, E&O insurance is voided, you're fired and potentially prosecuted. Document, don't touch. |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist **(STANDARD)**

Before any engagement begins, validate every item. This is the gate between planning and execution — skip none.

1. **Authorization:** Signed Rules of Engagement with explicit scope (IP ranges/CIDRs, domains, excluded systems), testing window with start/end times, emergency contact with 24/7 phone number, and authorized signatory with organizational authority. Verbal approval is legally worthless.
2. **Scope boundary hardening:** Every in-scope target enumerated and verified. Out-of-scope targets identified and excluded in testing tool configurations (e.g., Burp scope, Nmap target list). "Do not test" list distributed to all team members.
3. **Data handling plan:** Classification of data that may be encountered (PII, PHI, PCI, trade secrets). Encryption standard defined (AES-256-GCM minimum). Retention schedule agreed and documented. Destruction method specified (shred, degauss, crypto-erase).
4. **Tool audit:** All tools — C2 frameworks, exploit code, credential harvesters, post-exploitation scripts — code-reviewed for backdoors, cryptominers, or unexpected network connections. Tool versions pinned to known-good hashes. Commercial tools licensed and updated.
5. **C2 infrastructure ready:** Domain fronting configured (CDN-based). Redirector chain tested (2+ hops). TLS certificates valid and aged >30 days. Beacon intervals jittered. Kill switch mechanism tested — ability to terminate all implants with a single command.
6. **Communication plan:** Encrypted channel for client communication (Signal, PGP-encrypted email). Escalation triggers defined: critical finding (CVSS >= 9.0) = notify within 4 hours, active exploitation discovered = notify immediately, production impact suspected = STOP and call emergency contact.
7. **E&O insurance verification:** Professional liability/Errors & Omissions insurance active with cyber coverage. Policy covers penetration testing and red team activities explicitly — not just "security consulting." Verify coverage limits and exclusions (e.g., intentional acts, social engineering may be excluded).
8. **Backup and rollback plan:** For every system where exploitation or configuration changes will occur, documented rollback procedure exists. Credential reset capability verified. Database restore tested within last 30 days. Snapshots taken before exploitation begins.
9. **Notification dependencies:** Third-party notifications identified (cloud providers, ISPs, managed service providers — their ToS may require notification before testing). Upstream/downstream dependencies mapped. All required notifications sent and acknowledged before testing begins.
10. **Team readiness:** Every team member has reviewed the scope, ROE, and emergency procedures. Individual assignments defined — who does recon, who does web app testing, who does network exploitation, who does AD attacks. Buddy system for physical testing. Fatigue management plan for multi-week engagements.
11. **Legal review complete:** ROE reviewed by legal counsel for both testing organization and client. Jurisdiction confirmed (which state/country's laws apply). Indemnification clauses understood. Data breach notification obligations defined if client data is inadvertently exposed.
12. **Post-engagement deliverables defined:** Report format agreed (executive summary, technical findings, remediation roadmap). Delivery method (encrypted PDF, secure portal, in-person briefing). Timeline for draft, review, final delivery. Retest window offered (30-90 days post-remediation).

If any checklist item fails: STOP. Do not proceed past an unchecked item. Document the gap, notify the engagement lead, and resolve before any testing begins.

## What Good Looks Like

```
Authorized Pentest Engagement (Ethical Hacking Methodology)
|
|-- Rules of Engagement Signed + Scope Defined + Testing Window Approved
|      |
|      |-- Passive Recon: DNS, certificate transparency, Shodan, GitHub, social media -- map full external footprint
|      |      |
|      |      |-- Active Recon: Nmap full port scan, service enumeration, web endpoint discovery
|      |             |
|      |             |-- Vulnerability Discovery: automated scanners + manual verification of every finding
|      |                    |
|      |                    |-- Exploitation: PoC only -- demonstrate impact, document reproduction steps
|      |                           |
|      |                           |-- Post-Exploitation: minimal lateral movement, demonstrate data reachability (no exfil)
|      |                                  |
|      |                                  |-- Daily Finding Drafting: write findings as confirmed, escalate critical in <4 hours
|      |                                         |
|      |                                         |-- Executive Summary: one page for leadership, business impact, top 3 findings
|      |                                                |
|      |                                                |-- Technical Report: full catalog, attack narrative, MITRE ATT&CK mapping
|      |                                                       |
|      |                                                       |-- Remediation Roadmap: quick wins + strategic, retest offer, secure data destruction
```

### Scale Depth

#### Solo

**Penetration testing for 1-5 person startups, personal projects, or self-assessment.** Use free/open-source tools: Nmap, Nikto, SQLMap, Burp Suite Community, OWASP ZAP, Metasploit Community. Focus on OWASP Top 10 web vulnerabilities and basic network scanning. Manual testing for business logic flaws since automated scanners miss these. Self-authorization is legally dangerous — if testing your own company's systems, get written sign-off from the CTO or legal counsel. Reports: markdown with finding, CVSS score, reproduction steps, and fix recommendation. No C2 infrastructure needed — test from your own workstation within defined scope.

**Transition trigger:** When testing for paying clients, testing systems you don't own, or conducting assessments that require professional liability insurance → move to Small.

#### Small

**Boutique pentesting firm (1-5 testers) or internal security team at a 20-100 person company.** Commercial tools become cost-justified: Burp Suite Pro ($449/yr), Nessus Professional ($3,390/yr), Cobalt Strike ($3,500/yr). Establish standard methodology: PTES-aligned phases, OWASP WSTG for web apps, custom checklist for your niche. Client portal for report delivery (encrypted). Templated ROE with legal review. C2 infrastructure: single redirector + C2 server, basic domain fronting. Annual training budget for certifications (OSCP, GWAPT, GPEN). E&O insurance: $1M minimum coverage with explicit pentesting endorsement.

**Transition trigger:** Client demand exceeds tester capacity consistently (backlog >4 weeks), clients require 24/7 emergency response, or engagements span multiple geographies → move to Medium.

#### Medium

**Regional consultancy (10-50 testers) or dedicated internal red team at a 500-2000 person company.** Dedicated infrastructure: C2 with multi-redirector chains, domain fronting via CDN, custom C2 profiles that emulate legitimate traffic (Slack, Teams, O365 API patterns). Tooling: enterprise licenses (Burp Suite Enterprise, Core Impact, Cobalt Strike Team Server). Specialized teams: web app, network, cloud, AD, social engineering, physical. Formal methodology: custom playbooks per service type, internal wiki of TTPs, peer review on all reports. Training: annual SANS courses, internal labs, purple team exercises quarterly. Compliance: PCI ASV certification, FedRAMP 3PAO if serving government clients. E&O: $5M coverage. Report QA process: findings verified by second tester before delivery.

**Transition trigger:** Multi-national clients, 24/7 global coverage required, or contracts exceeding $500K annual value → move to Enterprise.

#### Enterprise

**Large consultancy (100+ testers), Fortune 500 internal red team, or MSSP with offensive security practice.** Global C2 infrastructure: region-specific redirectors for latency optimization, multi-CDN domain fronting, custom implants with in-memory execution and EDR evasion. Dedicated R&D team for zero-day development, custom exploit creation, and toolchain maintenance. Purple team program: continuous adversary emulation (MITRE Caldera, Atomic Red Team, SCYTHE), detection engineering feedback loop with blue team. AI/ML: automated recon correlation (Shodan + Censys + crt.sh + DNS brute-force → attack surface scoring), ML-assisted report generation from tool output. Compliance: PCI ASV, FedRAMP 3PAO, CMMC C3PAO, ISO 27001 certified. Training: internal university with annual mandatory upskilling, conference speaking, research publication. Legal: in-house counsel specializing in CFAA, GDPR, and international computer crime laws.

**Transition triggers:** Acquisition by larger entity, government/military contracts requiring security clearance infrastructure, or opening offices in 5+ countries with local legal teams.

## Deliberate Practice

```
Offensive Security Skill Progression
|
|-- Level 1: CTF Player -> Master OWASP Top 10, complete PortSwigger Web Security Academy labs
|      |
|      |-- Level 2: Junior Pentester -> OSCP/PWK preparation, HackTheBox/Proving Grounds daily practice
|      |      |
|      |      |-- Level 3: Pentester -> CREST/GPEN certified, lead small engagements (web app, internal network)
|      |             |
|      |             |-- Level 4: Senior Pentester -> Active Directory deep expertise, cloud exploitation, mobile app testing
|      |                    |
|      |                    |-- Level 5: Red Team Operator -> CRTO/OSED certified, C2 infrastructure, EDR evasion, threat actor emulation
|      |                           |
|      |                           |-- Level 6: Red Team Lead -> Design multi-week exercises, manage operator team, C-suite reporting, purple team integration
|      |                                  |
|      |                                  |-- Continuous learning: new CVEs, zero-days, conference talks, research publications, tool development
```

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We don't need a pentest — our developers write secure code and we run SAST." | Every external pentest finds critical vulnerabilities the internal team missed. SAST catches known patterns; creative attackers find novel attack chains. $500K-$2M in undiscovered vulnerabilities that an external assessment would have found before attackers did. |
| "Automated vulnerability scanners are enough — manual penetration testing is a luxury." | Scanners find 30-40% of vulnerabilities. They completely miss business logic flaws, authorization bypasses, race conditions, and multi-step attack chains. $200K-$1M in logic-based exploits that automated tools are architecturally incapable of detecting. |
| "We'll test on production directly — it's the only way to get realistic results." | Uncontrolled production testing triggers real incidents. Rate limiting kills legitimate traffic, fuzzing corrupts real data, and exploit attempts trigger WAF blocks that affect real users. $50K-$200K in self-inflicted production outages from testing without safeguards. |
| "The CTO gave verbal approval — that's enough to start testing." | Verbal approval from anyone without a signed Rules of Engagement is legally worthless. The Computer Fraud and Abuse Act (18 U.S.C. § 1030) requires written authorization. Testing without it = 5-20 years imprisonment and $500K in fines. No exceptions. |
| "I found a critical vulnerability outside scope — I should test and report it to be helpful." | Scope creep is unauthorized access under the CFAA, indistinguishable from testing with no authorization at all. STOP, document the observation, and request scope expansion — never self-authorize. $250K-$1.5M in legal defense, voided E&O insurance, and career destruction. |

## Anti-Patterns

### Authorization & Legal Gotchas

*   **Testing without written authorization -- the felony you cannot undo.** A pentester who proceeds on verbal "go ahead" from a middle manager without signed Rules of Engagement is committing a federal crime. The Computer Fraud and Abuse Act (18 U.S.C. § 1030) carries penalties of 5-20 years imprisonment and fines up to $500,000 for first offenses. Even if the manager had authority, without documentation you have no legal defense. Civil lawsuits for unauthorized access add $250K-$2M in damages. **Total cost: $500K-$2.5M in fines, legal fees, and civil damages -- plus career-ending criminal record.**

*   **Scope creep -- when "being helpful" becomes a felony.** During a web application pentest scoped to `app.example.com`, the tester discovers `admin.example.com` on a public IP with default credentials and full customer PII access. The tester's instinct: "I should test this and report it -- it's clearly a critical vulnerability." Legally: this is unauthorized access to an out-of-scope system. The signed Rules of Engagement does not cover `admin.example.com`. Testing it is indistinguishable from testing without any authorization at all under the CFAA. The correct action: STOP, document the observation as "noted but not tested -- out of scope system with observable vulnerability," and recommend immediate scope expansion. The client CAN authorize expanded testing; the tester CANNOT self-authorize. **Total cost: $250K-$1.5M — legal defense against CFAA charges, voided E&O insurance, permanent loss of security clearance. The vulnerability that "had to be reported" costs you your career.**

*   **Retaining client data post-engagement -- the GDPR time bomb.** Keeping penetration test artifacts (screenshots with PII, database extracts, credential dumps, network diagrams) after the engagement ends without a written data retention agreement triggers GDPR Article 5 (data minimization) and Article 32 (security of processing) violations. A single GDPR violation can result in fines of €20M or 4% of annual global turnover -- whichever is greater. For a consulting firm with $10M revenue, that's a $400K regulatory fine, plus $150K-$500K in legal defense and notification costs, plus reputational damage causing client loss. **Total cost: $550K-$900K in fines, legal fees, and lost business per incident.**

*   **Over-exploitation causing a production outage -- when PoC becomes DoS.** During a web application pentest, the tester runs sqlmap with --dump on a production database table to "prove impact." The resulting 10M-row extraction triggers database locks, 4-hour production outage, and $400K in lost revenue for an e-commerce client. The tester's errors and omissions (E&O) insurance may cover legal defense but excludes "intentional acts beyond scope." **Total cost: $400K-$1.2M in client damages, insurance premium increases of 200-400%, and potential E&O coverage denial.**

### Scope & Methodology Gotchas

*   **The tool-completeness illusion — "We ran Nessus, we're secure."** Automated vulnerability scanners (Nessus, OpenVAS, Nuclei) find 40-60% of vulnerabilities in a typical environment. They miss: business logic flaws (purchasing items with negative quantity), authorization bypasses (BOLA/IDOR), multi-step attack chains (low-severity info leak → credential extraction → privilege escalation), and zero-day vulnerabilities. An organization that runs Nessus quarterly and calls it a "pentest" has a false sense of security that is more dangerous than no testing at all — because they believe they're secure and skip the manual testing that would find the exploitable vulnerabilities. **Total cost: $200K-$800K — breach via undetected business logic flaw, regulatory fines for inadequate security testing, loss of cyber insurance coverage for failure to perform "adequate penetration testing."** Fix: Every vulnerability assessment must include manual verification of findings AND manual testing for business logic, authorization, and chained attacks. Automated scanners are reconnaissance tools, not assessments.

*   **Missing a critical vulnerability due to scope creep restrictions.** The client limits the pentest to only the production web tier, excluding the admin panel "because it's internal." The admin panel runs on a public IP, exposes default credentials, and leads to full customer PII access. An attacker finds it in 15 minutes via Shodan. The client blames the pentester for "incomplete assessment." Written scope limitations protect against liability but not reputation damage. **Total cost: $100K-$300K in lost client trust, contract cancellation, and negative referrals -- prevent by documenting out-of-scope risks in the report with explicit "if we had tested" impact statements.**

*   **Unencrypted engagement report leaked via email compromise.** A pentest report -- containing every vulnerability, exploit path, and credential weakness -- is emailed as a PDF with no encryption to the client CISO. The CISO's email is compromised via a separate phishing attack 3 weeks later. The report gives attackers a complete attack playbook. The client sues for negligence under the engagement contract's confidentiality clause. **Total cost: $250K-$750K in legal settlement, plus cyber insurance premium cancellation, plus complete loss of all client relationships -- encryption would have cost $0 and 2 extra minutes.**

### Testing Gotchas

*   **False positive in pentest report eroding trust permanently.** A pentester flags a non-exploitable finding as CRITICAL based on automated scanner output without manual verification. The client's dev team spends 80 engineering hours "fixing" a non-issue, shipping a rushed patch that introduces a real bug. The client's CISO loses confidence in every subsequent finding. **Total cost: $12K-$25K in wasted engineering time, $50K-$100K in diminished retainer value -- prevent by manually verifying every finding before reporting.**

*   **Failing to validate ransomware backup restoration -- the $0 backup that doesn't work.** An RRA assessment accepts the client's claim that "backups run nightly" without actually testing restoration. When ransomware hits 3 months later, the backup tapes are discovered to be corrupt (write-only -- no verification step). The organization pays a $2.3M ransom because backups are unusable. The RRA assessment is cited as providing "false assurance" and the consulting firm's E&O insurance is invoked. **Total cost: $500K-$3M in insurance claims, client lawsuit, and reputational destruction -- a restoration test takes 4 hours and costs $0 additional, but skipping it can cost millions.**

*   **Supply chain compromise via test environment -- the backdoor you installed.** A pentester sets up a C2 server for a red team exercise, using a popular open-source C2 framework from GitHub without auditing the code. The framework contains obfuscated cryptocurrency mining code that deploys to every compromised host. The client discovers unauthorized mining across 50 servers during post-exercise cleanup, generating $15K in AWS compute charges. The red team is suspended pending investigation. **Total cost: $15K-$40K in unexpected cloud charges, indefinite suspension of red team program, potential breach of contract claim -- mitigate by auditing all third-party tools and C2 frameworks before deployment.**

## Verification

After completing an offensive security engagement or delivering findings, run this sequence. Do not proceed past a failure.

1.  **Authorization check:** Signed Rules of Engagement document exists, scope is defined with IP ranges/domains, testing window is approved, emergency contact is documented. If any element is missing, engagement is unauthorized -- STOP.
2.  **Scope compliance check:** All tested targets are within documented scope. Any out-of-scope systems accidentally tested are noted in the report with "no further testing conducted." If out-of-scope testing occurred, notify client immediately.
3.  **PoC boundary check:** All exploitation stopped at proof-of-concept. No persistence mechanisms were created. No production data was exfiltrated beyond demonstration. No credentials were stored beyond engagement duration. If any boundary was crossed, document and notify client immediately.
4.  **Finding verification check:** Every reported finding was manually reproduced and verified. Zero findings are based solely on automated scanner output. Each finding includes CVSS v3.1 vector string and reproduction steps. If any finding is unverified, mark as "potential" and note lack of manual verification.
5.  **Report quality check:** Executive summary is <= 1 page. Technical report includes attack narrative and MITRE ATT&CK mapping. Each finding has specific, actionable remediation (not "apply patches"). Report is encrypted before transmission.
6.  **Critical finding escalation check:** Any finding with CVSS >= 9.0 was escalated to client within 4 hours of discovery. Escalation record includes time, method, and recipient acknowledgment. If not, explain delay in report.
7.  **Data destruction check:** All client data, screenshots, credentials, database extracts, and engagement artifacts have been securely deleted per retention agreement. Confirmation of deletion documented. If retention period is still active, deletion date is scheduled and documented.
8.  **Remediation roadmap check:** Quick wins (effort <8 hours, impact >= HIGH) are identified and prioritized. Strategic recommendations are phased by quarter. Retest is offered with 30-90 day window.

If any check fails: diagnose from checklist, provide specific corrective action, restart verification from failed item.

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

*   [MITRE ATT&CK Framework](https://attack.mitre.org/) -- Enterprise techniques, tactics, mitigations, and detection guidance
*   [OWASP Testing Guide (WSTG)](https://owasp.org/www-project-web-security-testing-guide/) -- Comprehensive web application penetration testing methodology
*   [PTES (Penetration Testing Execution Standard)](http://www.pentest-standard.org/) -- Industry-standard penetration testing phases and methodology
*   [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/) -- Top web application security risks with exploitation guidance
*   [BloodHound Documentation](https://bloodhound.readthedocs.io/) -- Active Directory attack path analysis and visualization
*   [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) -- Small, portable detection tests mapped to MITRE ATT&CK
*   [MITRE Caldera](https://github.com/mitre/caldera) -- Automated adversary emulation platform
*   [SLSA Framework](https://slsa.dev/) -- Supply chain Levels for Software Artifacts -- build integrity specification
*   [HackTricks](https://book.hacktricks.xyz/) -- Comprehensive pentesting and CTF techniques reference
*   [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) -- Web application payloads and bypass techniques
*   [references/attacker-mindset-mitre-attack.md](references/attacker-mindset-mitre-attack.md) -- Attack graphs, MITRE ATT&CK mapping, TTP-based thinking
*   [references/attack-surface-analysis.md](references/attack-surface-analysis.md) -- External/internal asset discovery methodology and tools
*   [references/pentest-methodology.md](references/pentest-methodology.md) -- PTES phases, OWASP standards, scoping templates
*   [references/web-exploitation-patterns.md](references/web-exploitation-patterns.md) -- SQLi, XSS, deserialization, SSTI, IDOR patterns classified by OWASP and CVSS
*   [references/active-directory-attacks.md](references/active-directory-attacks.md) -- Kerberoasting, DCSync, Golden Ticket, BloodHound, ACL abuse
*   [references/social-engineering-framework.md](references/social-engineering-framework.md) -- Pretext design, phishing metrics, physical SE assessment
*   [references/supply-chain-attack-defense.md](references/supply-chain-attack-defense.md) -- Dependency confusion, SLSA, SBOM, build pipeline hardening
*   [references/ransomware-defense-architecture.md](references/ransomware-defense-architecture.md) -- 3-2-1 backup, LAPS, EDR validation, RRA scoring, deception technology
