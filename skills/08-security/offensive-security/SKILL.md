---
name: offensive-security
description: >
  Use when planning and executing penetration tests (web, mobile, API, network,
  cloud, social engineering); when conducting attack surface analysis to identify
  unknown or unmanaged internet-exposed assets; when designing and executing red
  team exercises mapped to MITRE ATT&CK techniques; when hardening defenses against
  ransomware attacks with backup strategy and lateral movement detection; when
  assessing and mitigating supply chain attack risks (dependency confusion,
  compromised packages, build pipeline security); when running purple team exercises
  to measure and improve detection engineering coverage; when designing security
  awareness training and phishing simulation programs; or when conducting physical
  security assessments. Handles penetration testing methodology (PTES phases, OWASP
  WSTG/ASVS/MSVS, exploitation and post-exploitation technique classification by
  impact), attack surface discovery (external: DNS/subdomain enumeration, cloud asset
  discovery, API endpoint mapping, Shodan/Censys reconnaissance; internal: microservice
  topology, database accessibility, message queue exposure), web application
  exploitation patterns (SQLi variants, XSS/CSRF/SSRF/XXE, deserialization in
  Java/PHP/Python, SSTI, prototype pollution in Node.js, IDOR detection methodology),
  Active Directory attack chains (Kerberoasting, AS-REP roasting, DCSync, Golden
  Ticket, Pass-the-Hash/Ticket, BloodHound for attack path visualization), cloud
  exploitation (IMDSv1/v2, metadata service endpoints, IAM role enumeration, public
  S3/blob/bucket discovery), social engineering framework (pretext design, phishing
  campaign metrics, physical social engineering assessment, awareness training
  effectiveness measurement), supply chain attack defense (dependency confusion
  detection, SLSA framework implementation, package signing, artifact provenance
  verification), ransomware defense architecture (3-2-1 backup with immutable/air-gapped
  tiers, LAPS rollout, EDR deployment validation, RRA scoring methodology, lateral
  movement detection via deception technology), and purple teaming operations
  (continuous security validation with Atomic Red Team/Caldera, detection coverage by
  MITRE ATT&CK technique, automated attack simulation pipelines). Do NOT use for
  vulnerability scanning and CVE triage (route to vulnerability-management), threat
  modeling during design phase (route to security-engineer), incident response during
  active breach (route to incident-responder), or security control implementation
  (route to security-engineer).
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
  consumes_from: []
  feeds_into: []
  alternatives: []
portability: >
  works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
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

## Core Workflow

### Phase 1: Rules of Engagement & Reconnaissance

Execute in order. Do not skip steps.

```
1. VALIDATE AUTHORIZATION
   |-- Confirm signed Rules of Engagement document exists
   |-- Verify scope: IP ranges, domains, excluded systems, testing window
   |-- Confirm emergency contact and escalation procedure
   |-- Verify testing window: dates, times, prohibited hours
   |-- Document out-of-scope systems explicitly (do not test even if discovered)
   |-- CRITICAL: If any element is missing, STOP. Do not proceed.

2. EXTERNAL RECONNAISSANCE (Passive)
   |-- DNS enumeration: Amass, Subfinder, dnsrecon, crt.sh certificate transparency
   |   |-- Subdomain discovery via brute-force, certificate logs, search engines
   |   |-- Zone transfer attempt (AXFR) -- rarely succeeds but quick to check
   |-- WHOIS/RDAP lookup: registrant, nameservers, domain age, email addresses
   |   |-- Historical WHOIS via WhoisXML, DomainTools
   |-- Search engine reconnaissance: Google dorking (site:, inurl:, filetype:, intitle:)
   |   |-- Shodan/Censys: exposed services, banners, SSL certificates, IoT devices
   |   |-- GitHub dorking: API keys, credentials, configuration files, internal URLs
   |-- Cloud asset discovery: AWS/Azure/GCP public buckets, cloudfront, blob storage
   |   |-- GrayhatWarfare, Bucket Finder tools for public S3/blob enumeration
   |-- Social media & employee profiling: LinkedIn (job titles, tech stack clues), Twitter, GitHub
   |   |-- Harvest email format from public sources (first.last@company.com patterns)
   |-- Technology stack fingerprinting: Wappalyzer, BuiltWith, WhatWeb, retire.js
   |   |-- Identify: web server, framework, CDN, JavaScript libraries, CMS versions

3. EXTERNAL RECONNAISSANCE (Active)
   |-- Port scanning: Nmap TCP SYN scan (-sS), service version detection (-sV), OS detection (-O)
   |   |-- Full port scan (-p-) for TCP top 1000 AND UDP top 100 -- missed ports = missed vulnerabilities
   |   |-- NSE scripts: default (-sC), vulnerability scan (--script vuln), specific service scripts
   |-- Web endpoint discovery: directory brute-force (gobuster, ffuf, dirsearch, feroxbuster)
   |   |-- API endpoint discovery: Swagger/OpenAPI docs, GraphQL introspection, REST API fuzzing
   |   |-- Virtual host discovery: Host header fuzzing for hidden vhosts
   |-- SSL/TLS analysis: testssl.sh, sslscan -- check for weak ciphers, POODLE, Heartbleed, BEAST
   |   |-- Certificate chain validation and expiration

4. INTERNAL RECONNAISSANCE (Post-Compromise or Internal Test)
   |-- Network mapping: ARP scanning, ping sweeps, NetBIOS/LLMNR enumeration
   |-- Service discovery: SMB shares, LDAP, MSSQL, RDP, SSH, VNC, printers, IoT
   |-- Active Directory enumeration (if Windows environment):
   |   |-- BloodHound/SharpHound: map AD trust relationships, attack paths, ACL abuse paths
   |   |-- PowerView: user/group/computer enumeration, session enumeration, GPO mapping
   |   |-- LDAP queries: user descriptions, service principal names (SPNs), admin group membership
   |-- Microservice topology: container discovery (Docker socket, Kubernetes API), message queues
   |-- Database discovery: open MongoDB/Redis/Elasticsearch/PostgreSQL/MySQL with default credentials
   |-- Internal documentation: SharePoint, Confluence, wiki for credentials and network diagrams
```

### Phase 2: Vulnerability Discovery

```
1. AUTOMATED SCANNING
   |-- Network vulnerability scanners: Nessus, OpenVAS, Nexpose against all in-scope IPs
   |   |-- Authenticated scans (where credentials available) -- yield 40-60% more findings
   |-- Web application scanners: Burp Suite Pro, OWASP ZAP, Nikto, Nuclei with custom templates
   |   |-- Authenticated crawling: spider with session tokens to discover hidden endpoints
   |-- Container/cloud scanning: Trivy, ScoutSuite, Prowler, cloudsplaining for IAM analysis
   |-- Code analysis: Semgrep, CodeQL, SonarQube for SAST (if source code access granted)

2. MANUAL VERIFICATION
   |-- Triage all automated findings: remove false positives, classify severity (CVSS v3.1)
   |   |-- CRITICAL (CVSS 9.0-10.0): Remote code execution, authentication bypass exposing PII
   |   |-- HIGH (7.0-8.9): SQL injection, SSRF to internal services, privilege escalation
   |   |-- MEDIUM (4.0-6.9): Stored XSS, directory listing, missing security headers
   |   |-- LOW (0.1-3.9): Information disclosure, verbose error messages, clickjacking
   |-- Verify each finding: reproduce the vulnerability manually with step-by-step documentation
   |   |-- Screenshot every step with timestamps and tool output
   |   |-- Document exact request/response pairs, payloads, and environmental conditions

3. ATTACK PATH ANALYSIS
   |-- Chain vulnerabilities: a low-severity information leak may enable a critical exploit
   |   |-- Example: version disclosure -> CVE lookup -> known exploit -> RCE chain
   |-- Map findings to MITRE ATT&CK techniques for red team integration
   |-- Prioritize by business impact, not just CVSS: PII exposure > internal RCE > XSS
```

### Phase 3: Exploitation

```
1. EXPLOIT SELECTION & PREPARATION
   |-- Search for known exploits: ExploitDB, Metasploit, GitHub PoCs, Packet Storm
   |   |-- Verify exploit code before running: read the source, understand what it does
   |   |-- Test in isolated lab environment first if exploit is novel or destructive
   |-- Custom exploit development: only if no public exploit exists and vulnerability is critical
   |   |-- Buffer overflows, format strings, heap exploitation require deep C/assembly knowledge
   |-- Payload generation: msfvenom, custom shellcode, living-off-the-land binaries (LOLBins)
   |   |-- Prefer LOLBins over custom payloads: certutil, bitsadmin, powershell, wmic, mshta

2. EXPLOITATION EXECUTION (Proof-of-Concept Only)
   |-- Execute exploit with minimum necessary impact:
   |   |-- Web: read /etc/passwd or a test file -- NOT full database dump
   |   |-- Network: establish reverse shell, capture proof screenshot, then exit
   |   |-- Cloud: read metadata service, list IAM permissions -- NOT deploy resources
   |-- DOCUMENT EVERY STEP: timestamp, command, output, screenshot
   |-- If exploit fails: investigate, adjust, retry -- but NEVER brute-force authentication
   |-- CRITICAL CHECKPOINT: Have you exceeded proof-of-concept? If yes, STOP immediately.

3. POST-EXPLOITATION (Minimal, Documented)
   |-- Demonstrate impact: if RCE achieved, show what data/access is reachable
   |-- Privilege escalation: local enumeration (sudo -l, SUID, capabilities, unquoted service paths)
   |   |-- Windows: PowerUp, SharpUp, Seatbelt, WinPEAS for privilege escalation vectors
   |   |-- Linux: LinPEAS, pspy, GTFOBins, SUID/GUID binary exploitation
   |-- Credential harvesting (minimum necessary): demonstrate access to credential store
   |   |-- NEVER dump entire NTDS.dit without explicit authorization
   |-- Persistence: document where persistence COULD be established -- DO NOT create actual persistence
   |   |-- Example: "Scheduled task could be created for persistence" -- do not create the task
```

### Phase 4: Post-Exploitation & Lateral Movement

```
1. SITUATIONAL AWARENESS
   |-- Network reconnaissance from compromised host: ARP table, routing table, DNS cache
   |-- Identify domain controller, file servers, database servers, jump hosts
   |-- Map trust relationships: domain trusts, forest trusts, Azure AD Connect
   |-- Identify high-value targets: PII stores, financial systems, source code repositories, PKI

2. LATERAL MOVEMENT (Proof-of-Concept Only)
   |-- Windows: Pass-the-Hash, Pass-the-Ticket, WMI, PsExec, WinRM, RDP, DCOM
   |   |-- Demonstrate can move to ONE additional host to prove lateral movement possible
   |   |-- DO NOT pivot beyond what is needed to demonstrate risk
   |-- Linux: SSH key reuse, SSH agent forwarding hijack, NFS share access, .bash_history mining
   |-- Cloud: IAM role chaining, cross-account access via trust relationships, metadata service pivot
   |-- Container escape: access host from container via mounted Docker socket, /proc, capabilities

3. DATA ACCESS DEMONSTRATION (Read-Only, Minimal)
   |-- Identify and access ONE test/sample record to demonstrate data reachability
   |-- NEVER exfiltrate production data, PII, PHI, or PCI data beyond a single demonstration record
   |-- Screenshot access path and data visibility -- do not download or transfer data off-network
   |-- If data exfiltration is in scope, use synthetic test data and document the exfiltration path
```

### Phase 5: Reporting & Remediation

```
1. DRAFT FINDINGS (Daily During Engagement)
   |-- Write each finding as it is confirmed -- do not wait until the end
   |-- Each finding template:
   |   |-- Title: Descriptive, unique identifier (e.g., F-001: SQLi in /api/users endpoint)
   |   |-- Severity: CVSS v3.1 vector string and score
   |   |-- Description: What the vulnerability is, in plain English
   |   |-- Reproduction Steps: Exact commands, requests, payloads to reproduce
   |   |-- Impact: Business risk if exploited -- data loss, financial, reputational, compliance
   |   |-- Remediation: Specific, actionable fix -- code snippet, config change, architecture recommendation
   |   |-- References: CWE, OWASP, vendor advisory links
   |-- Escalate CRITICAL (CVSS >= 9.0) within 4 hours of discovery via phone + encrypted email

2. EXECUTIVE SUMMARY
   |-- One page maximum, written for non-technical leadership (CEO, CISO, Board)
   |-- Overall risk rating: Critical/High/Medium/Low based on worst-case scenario
   |-- Top 3 findings with business impact in dollar terms or compliance consequences
   |-- Positive findings: what the organization did well, defense mechanisms that worked
   |-- Remediation roadmap: phased approach with quick wins (week 1-2) and strategic (quarterly)

3. TECHNICAL REPORT
   |-- Full findings catalog sorted by severity (Critical -> Low)
   |-- Attack narrative: chronological walkthrough of the engagement from recon to exploitation
   |-- MITRE ATT&CK mapping: which techniques were successfully executed
   |-- Defense observations: what detection mechanisms fired, what was missed
   |-- Appendices: full tool output, scan results, raw evidence, scope document

4. REMEDIATION SUPPORT
   |-- Remediation matrix: effort vs impact for each finding
   |   |-- Quick wins: low effort (hours), high impact, fix immediately
   |   |-- Strategic: high effort (weeks), high impact, plan for next quarter
   |   |-- Accept risk: high effort, low impact, document risk acceptance
   |-- Offer retest: verify fixes after remediation window (typically 30-90 days)
   |-- Knowledge transfer: walkthrough with security/dev teams on exploitation techniques used
   |-- Secure destruction: delete all client data, findings drafts, credentials, screenshots per retention agreement
```

## Decision Trees

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

## Gotchas -- Highest-Value Content

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
