# OWASP Top 10 — A04:2021 Insecure Design

## Overview
Insecure Design focuses on risks related to design and architectural flaws — not implementation bugs. Calls for secure-by-design patterns.

## Design Flaws in Data Security
1. **Missing data classification**: No tiering model, everything treated the same
2. **No threat modeling**: Data flows not analyzed for exposure risks
3. **Security bolted on**: Encryption added after deployment without key management
4. **No data minimization**: Collecting everything, retaining forever
5. **Shared secrets**: Same credentials for multiple environments
6. **No audit logging**: Can't detect or investigate data access
7. **Missing DLP**: No controls for data exfiltration at any layer

## Secure-by-Design Principles
- **Zero trust for data**: Assume breach, verify every access
- **Data minimization by default**: Only collect what's operationally needed
- **Privacy by design**: Embed protection from architecture stage
- **Defense in depth**: Multiple independent data protection layers
- **Fail closed**: If protection mechanism fails, deny access
- **Least privilege**: Access granted per data classification tier

## Prevention
- Threat model data flows before coding
- Security user stories in backlog (refer to ASVS)
- Reference architecture with documented data protection patterns
- CI/CD gates for data protection requirements

## References
- OWASP A04:2021: https://owasp.org/Top10/A04_2021-Insecure_Design/
