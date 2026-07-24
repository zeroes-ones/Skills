# Attack Surface Analysis

## Overview

Attack surface analysis identifies all internet-exposed and internally accessible assets that an adversary could target. The methodology covers external discovery, internal mapping, continuous monitoring, and the tools used at each stage. Unknown or unmanaged assets are the most common root cause of breaches -- if you do not know it exists, you cannot defend it.

## External Attack Surface Discovery

### DNS & Subdomain Enumeration
- **Passive enumeration:** Certificate Transparency logs (crt.sh, CertSpotter), DNS dumpster, VirusTotal subdomains, SecurityTrails, Shodan/DNSDB passive DNS.
- **Active enumeration:** Amass (OWASP tool combining passive and active techniques), Subfinder (fast passive subdomain discovery), puredns (DNS brute-force with resolver rotation), massdns (high-performance DNS resolver for brute-force).
- **Permutation discovery:** Altdns, dnsgen, gotator -- generate likely subdomain permutations (dev-, staging-, test-, admin-, internal-, vpn-, mail-).
- **Zone transfer:** dig AXFR @nameserver domain.com -- rarely succeeds on modern infrastructure but always worth the 5-second check.

### Cloud Asset Discovery
- **AWS:** S3 bucket enumeration (s3-bucket-finder, GrayhatWarfare), CloudFront distributions, RDS snapshots with public access. Check for IAM roles with AssumeRole wildcards.
- **Azure:** Blob storage with public access, Azure App Services exposed, Azure SQL with public endpoint, Key Vault with broad access policies.
- **GCP:** Public Cloud Storage buckets, Cloud Functions with allUsers invoke permissions, BigQuery datasets with public access.
- **Multi-cloud tools:** ScoutSuite, Prowler, Steampipe, cloudsplaining, cloudmapper.

### API Endpoint Mapping
- Swagger/OpenAPI documentation discovery: /swagger.json, /api-docs, /v2/api-docs, /v3/api-docs, /swagger-ui.html.
- GraphQL introspection: query __schema to enumerate all types, queries, mutations, and subscriptions.
- API fuzzing: ffuf, gobuster with API wordlists for endpoint discovery. Test HTTP method overrides (X-HTTP-Method-Override header).

### Search Engine & OSINT Reconnaissance
- **Shodan:** org:"Company Name", ssl:"*.company.com", port:3389, product:"Apache", vuln:CVE-2021-44228. Shodan monitors expose new assets in real-time.
- **Censys:** Similar to Shodan; complementary coverage. Censys indexes SSL certificates differently, may find assets Shodan misses.
- **Google dorking:** site:target.com filetype:pdf, intitle:"index of", inurl:admin, ext:sql intext:password.
- **GitHub dorking:** org:target "password", "api_key", "secret", "BEGIN RSA PRIVATE KEY", filename:.env.

## Internal Attack Surface Mapping

Once inside the network, the attack surface expands to internal services invisible from the internet. Internal mapping is critical because 73% of breaches involve lateral movement after initial compromise.

### Network Service Discovery
- Responder (LLMNR/NBT-NS/mDNS poisoning) -- capture NTLMv2 hashes from broadcast name resolution protocols. Active on most Windows networks by default.
- Nmap internal scans: discover SMB (445), RDP (3389), MSSQL (1433), MySQL (3306), Redis (6379), MongoDB (27017), Elasticsearch (9200).
- SNMP enumeration: default community strings (public/private), SNMPv3 with noAuthNoPriv.
