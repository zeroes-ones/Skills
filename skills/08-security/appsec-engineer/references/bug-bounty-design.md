# Bug Bounty Program Design

## Program Architecture

### Vulnerability Disclosure Program (VDP)
- Purpose: Provide a clear path for researchers to report vulnerabilities without fear of legal action
- Budget: $0 (no bounties, swag optional -- t-shirts, stickers, hall of fame)
- Volume: 1-10 reports/month (low)
- Setup: security.txt at standard path, VDP policy page, security@ email alias
- Safe harbor: "Researchers acting in good faith will not face legal action. We will respond within 5 business days and resolve validated reports within 90 days."
- Disclosure timeline: Researcher may disclose publicly 90 days after report if unresolved

### Private Bug Bounty (Invite-Only)
- Purpose: Pay for valid vulnerabilities while controlling researcher volume
- Budget: $5K-$25K/month
- Volume: 20-80 reports/month (medium)
- Setup: HackerOne or Bugcrowd private program, 10-50 invited researchers
- Recruitment: Invite top submitters from VDP, top-ranked researchers on platform, researchers with relevant expertise

### Public Bug Bounty
- Purpose: Maximum vulnerability discovery, crowd-sourced security testing at scale
- Budget: $25K-$250K+/month
- Volume: 100-500 reports/month (high)
- Setup: Dedicated triage team (1-2 people minimum), published bounty table, clear scope
- Prerequisites: VDP for 6 months, private bounty for 6 months, mature triage process

## Bounty Table Design

### CVSS-Based Rewards
| CVSS Range | Severity | Example Vulnerabilities | Reward Range |
|-----------|----------|------------------------|--------------|
| 9.0-10.0 | Critical | RCE, auth bypass for all users, SQLi exposing all data | $2,500-$15,000 |
| 7.0-8.9 | High | Stored XSS on authenticated page, IDOR on PII, SSRF to internal services | $1,000-$5,000 |
| 4.0-6.9 | Medium | Reflected XSS, CSRF on sensitive actions, info disclosure (non-regulated) | $250-$1,000 |
| 0.1-3.9 | Low | Missing security headers without exploit path, clickjacking without sensitive action | $50-$250 |
| N/A | Informational | Best practice suggestions, unclear documentation | Swag or Hall of Fame |

### Bonus Multipliers
- +50%: Exceptional report quality (clear repro steps, impact analysis, suggested fix, video PoC)
- +25%: Critical vulnerability in a recently launched feature (<30 days old)
- +100%: Vulnerability with a working proof-of-concept exploit (not just theoretical)

## Triage Workflow

### States
New -> Triaging -> Needs More Info -> Accepted -> Fix In Progress -> Resolved -> Bounty Awarded

### SLAs
- First response: <24 hours (acknowledge receipt, initial triage assessment)
- Triage complete: <72 hours (accepted/duplicate/needs more info/out of scope)
- Fix deployed: Based on severity SLA (24h critical, 72h high, 7d medium, 30d low)
- Bounty awarded: <1 week after fix verified

### Duplicate Handling
- Link to original report
- Thank researcher, acknowledge duplicate
- Consider small bonus ($50-$100) for high-quality duplicate reports
- Track duplicate rate -- if a bug class is frequently duplicated, it's under-tested

## Scope Definition
- In-scope: *.example.com, *.api.example.com, mobile apps (iOS/Android), specific IP ranges
- Out-of-scope: *.blog.example.com (static site), third-party services, social engineering, physical security, DoS/DDoS
- Excluded vulnerability classes: Missing security headers without demonstrated impact, clickjacking on static pages, SSL/TLS configuration issues already documented, self-XSS
