# Active Directory Attack Chains

## Overview

Active Directory remains the most critical attack surface in enterprise environments. A single AD misconfiguration can grant an attacker Domain Admin privileges from a standard user account in under 2 hours. This reference catalogs the attack techniques, tools, detection methods, and defense strategies for AD environments.

## Credential Access Techniques

### Kerberoasting (T1558.003)
Kerberoasting exploits how Kerberos Service Tickets work. Any domain user can request a TGS (Ticket Granting Service) for any service account (identified by SPN -- Service Principal Name). The TGS is encrypted with the service account's NTLM hash, allowing offline password cracking.

- **Tooling:** Impacket-GetUserSPNs, Rubeus kerberoast, PowerView (Invoke-Kerberoast).
- **Cracking:** hashcat -m 13100 (Kerberos 5 TGS-REP etype 23). Hashcat benchmarks: ~1.2M H/s on RTX 4090 for a single hash.
- **High-value targets:** Service accounts with elevated privileges -- MSSQL service accounts are frequently Domain Admins. Exchange service accounts often have WriteDacl on the domain.
- **Detection:** Event ID 4769 with Ticket Encryption Type 0x17 (RC4-HMAC) -- modern environments should use AES (0x12). Unusual volume of 4769 events from a single source.
- **Mitigation:** Group Managed Service Accounts (gMSA) for service accounts with long, complex, automatically rotated passwords. AES-only Kerberos (disable RC4).

### AS-REP Roasting (T1558.004)
Accounts with "Do not require Kerberos preauthentication" enabled (UF_DONT_REQUIRE_PREAUTH) receive an AS-REP that is encrypted with the user's password hash. No domain credentials needed -- any network access allows requesting these tickets.

- **Tooling:** Impacket-GetNPUsers, Rubeus asreproast.
- **Enumeration:** PowerView: Get-DomainUser -PreauthNotRequired; LDAP filter: (userAccountControl:1.2.840.113556.1.4.803:=4194304).
- **Cracking:** hashcat -m 18200 (Kerberos 5 AS-REP etype 23).
- **Prevalence:** Common on service accounts configured before the "preauth required" default changed. Legacy systems, Linux Kerberos clients, and misconfigured accounts are frequent targets.

### DCSync (T1003.006)
DCSync abuses the MS-DRSR (Directory Replication Service Remote) protocol to impersonate a domain controller and request password hashes for any principal. Requires Replicating Directory Changes and Replicating Directory Changes All privileges.

- **Required rights:** Domain Admins, Enterprise Admins, Administrators group, or accounts explicitly delegated these replication rights.
- **Tooling:** Mimikatz lsadump::dcsync, Impacket-secretsdump.
