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
