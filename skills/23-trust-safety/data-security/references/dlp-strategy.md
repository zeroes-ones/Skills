# DLP Strategy

## Overview
Data Loss Prevention across email, web, cloud API, and endpoint channels. Progression from detection to blocking with false positive tuning.

## DLP Deployment Phases (Mandatory)
### Phase A: Detection (Days 1-30)
- Deploy policies in detect-only mode
- Log all violations — do NOT block or notify users
- Establish baseline: violations/day, false positive rate per policy

### Phase B: Monitor (Days 31-60)
- Review alerts daily, categorize by severity
- Tune policies: target <5% false positive rate
- Add exceptions for known business workflows

### Phase C: Blocking (Day 61+)
- Enable blocking for high-confidence policies only
- Quarantine with manager notification for medium-confidence
- Log-only for low-confidence and internal-to-internal

## Channel Coverage (Prioritized)
1. **Email DLP:** Highest priority — #1 accidental exfiltration vector
2. **Web DLP:** Browser uploads to personal cloud, pastebin, file sharing
3. **Cloud CASB DLP:** Google Drive, Slack, Jira, Salesforce
4. **Endpoint DLP:** USB, clipboard, print restrictions
5. **Network DLP:** ICAP proxy integration, SMTP MTA

## Policy Design
- Content: regex patterns, data fingerprints, ML classifiers
- Context: source, destination, user role, time of day
- Action: block, quarantine, notify, log-only, auto-encrypt

## False Positive Management
- Never skip directly to blocking — will result in DLP being disabled
- Implement user self-remediation: "Release with justification"
- Weekly false positive review with business stakeholders
