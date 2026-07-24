# Attacker Mindset & MITRE ATT&CK Mapping

## Thinking Like an Adversary

The core distinction between vulnerability scanning and penetration testing is the attacker mindset. A scanner finds CVEs. An attacker chains weaknesses: an information disclosure enables credential harvesting, which enables lateral movement, which exposes a misconfigured service, which yields Domain Admin. This reference covers the mental frameworks, attack graph construction, and MITRE ATT&CK mapping essential for offensive security professionals.

## Attack Graph Construction

An attack graph models the paths from initial access to objective. Unlike a flat vulnerability list, an attack graph shows dependencies: you cannot exploit finding F-012 (internal SSRF) until you achieve finding F-004 (initial foothold on web server). Attack graphs should include:

- **Nodes:** Compromised hosts, credentials, access levels, data stores
- **Edges:** Exploits, credential reuse, trust relationships, network reachability
- **Preconditions:** What must be true for an edge to be traversable (e.g., "attacker has code execution on host A AND host B trusts host A for WinRM")
- **Postconditions:** What becomes true after traversal (e.g., "attacker has SYSTEM on host B")

Tools: BloodHound generates attack graphs automatically from Active Directory data. AttackForge and AttackFlow provide manual attack graph construction for non-AD environments.

## MITRE ATT&CK for Red Teams

MITRE ATT&CK is not just a blue team framework. For red teams, it provides:

- **Tactic categorization:** Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact.
- **Technique selection:** Choose techniques based on the threat actor you are emulating (e.g., APT29 uses T1003.001 LSASS memory dump, T1055 Process Injection, T1071.001 Web Protocols for C2).
- **Defense evasion mapping:** For each technique, MITRE ATT&CK lists known detection methods -- this tells you what to avoid or modify to evade detection.
- **Sub-technique granularity:** T1003.001 (LSASS Memory) vs T1003.002 (Security Account Manager) -- precision matters for detection engineering validation.

## TTP-Based Threat Emulation

Threat actor profiles to emulate by sophistication level:

- **APT29 (Cozy Bear):** Russian SVR. Targets: government, think tanks, healthcare. Techniques: spear phishing, OAuth token theft, Azure AD abuse, custom C2 (WellMess). Disciplined, patient, avoids noisy techniques.
- **FIN7:** Financially motivated. Targets: hospitality, retail, POS systems. Techniques: PowerShell Empire, Cobalt Strike, Carbanak backdoor. Aggressive, uses living-off-the-land, deploys ransomware as secondary payload.
- **Lazarus Group (APT38):** North Korea. Targets: cryptocurrency exchanges, banks, SWIFT. Techniques: destructive wipers, supply chain, macOS malware. High sophistication, willing to cause permanent damage.
- **Ransomware-as-a-Service (RaaS) affiliates:** LockBit, BlackCat/ALPHV, Black Basta. Techniques: initial access brokers (IABs), RDP brute-force, phishing, commodity loaders (QakBot, Emotet), data exfiltration before encryption.

## Kill Chain Analysis

Map each attack phase to ATT&CK: Reconnaissance (T1590-T1598) -> Resource Development (T1583-T1588) -> Initial Access (T1189, T1566, T1190) -> Execution (T1059, T1203, T1204) -> Persistence (T1543, T1547, T1053) -> Privilege Escalation (T1068, T1134, T1548) -> Defense Evasion (T1027, T1055, T1562) -> Credential Access (T1003, T1552, T1558) -> Discovery (T1082, T1083, T1018) -> Lateral Movement (T1021, T1550) -> Collection (T1005, T1114, T1530) -> C2 (T1071, T1090, T1105) -> Exfiltration (T1041, T1048, T1567) -> Impact (T1485, T1486, T1490).
