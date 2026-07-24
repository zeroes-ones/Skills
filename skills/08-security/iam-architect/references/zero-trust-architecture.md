# Zero Trust Architecture (NIST SP 800-207)

## Core Tenets

1. **Never trust, always verify** -- Every access request is authenticated, authorized, and encrypted, regardless of network location.
2. **Assume breach** -- Operate as if an attacker is already inside the network. Minimize blast radius, segment relentlessly.
3. **Verify explicitly** -- Authenticate and authorize based on all available data points: identity, device health, location, service, data classification, anomalies.

## Zero Trust Maturity Model

| Level | User Auth | Device Trust | Service Auth | Network | Data |
|-------|-----------|-------------|-------------|---------|------|
| 0: Traditional | Password, maybe VPN | None | IP-based allowlists | Flat network | No classification |
| 1: Initial | MFA for admins | MDM enrolled (admins) | API keys (static) | VLAN segmentation | Basic (public/internal/confidential) |
| 2: Advanced | MFA for all, conditional access | Device compliance required | mTLS or SPIFFE | Microsegmentation (default deny) | Data labeling + DLP |
| 3: Optimal | Continuous auth, risk-based step-up | Real-time posture assessment | Short-lived SPIFFE SVIDs | Identity-aware microsegmentation | Automated classification + encryption |

## Microsegmentation Implementation

Policy Structure (OPA/Rego example):
```
package microsegmentation

default allow = false

allow {
    input.source.namespace == "frontend"
    input.destination.namespace == "api"
    input.destination.port == 443
}

allow {
    input.source.namespace == "api"
    input.destination.namespace == "database"
    input.destination.port == 5432
    input.source.service_account == "api-reader"
}
```

## Device Trust Scoring

| Signal | Points | How to Verify |
|--------|--------|---------------|
| Disk encryption (BitLocker/FileVault) | 30 | OS API query |
| OS up-to-date (<=30 days since patch) | 20 | OS version check vs known-good |
| Firewall enabled | 15 | OS API query |
| MDM enrolled and compliant | 20 | MDM attestation |
| No jailbreak/root detected | 10 | Integrity check |
| Screen lock enabled (<=5 min timeout) | 5 | OS policy check |

**Threshold for access: >= 80 points.** Re-evaluate device posture every 15 minutes during active sessions.
