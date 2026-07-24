# Smart Contract Audit Report Template

## Executive Summary
- **Protocol**: [Name + Version]
- **Audit Type**: Full (manual + automated + formal) / Light (static only)
- **Timeline**: [Start] — [End] ([N] person-days)
- **Findings**: Critical [N], High [N], Medium [N], Low [N], Info [N]
- **Overall Assessment**: [Pass / Pass with Remediation / Fail]

## Severity Classification
| Severity | Definition | Example |
|----------|-----------|---------|
| Critical | Direct loss of funds, no preconditions | Reentrancy draining all TVL |
| High | Loss possible with common preconditions | Oracle manipulation, access control bypass |
| Medium | Loss possible with unlikely preconditions | Edge case rounding to 0 |
| Low | No direct loss, best practice violation | Missing events, unused imports |
| Info | Informational, no risk | Gas optimization suggestions |

## Finding Format
### [S-#] [Title] — [Severity]
**Location**: `contracts/X.sol:L100-L120`
**Description**: [What the vulnerability is]
**Impact**: [Concrete scenario with dollar estimate]
**Proof of Concept**:
```solidity
function test_exploit() public {
    // Working exploit demonstrating the vulnerability
}
```
**Recommendation**: [Specific fix with code]
**Status**: [Open / Acknowledged / Fixed in commit <hash>]

## Automated Analysis Results
| Tool | Version | Findings | False Positives |
|------|---------|----------|-----------------|
| Slither | X.Y.Z | N | N |
| Echidna | X.Y.Z | N properties | — |
| Manticore | X.Y.Z | N paths | N |
| Certora | X.Y.Z | N rules | N |

## Deployment Verification
- [ ] Deployed bytecode matches audited source at commit `<hash>`
- [ ] Constructor arguments verified on Etherscan
- [ ] Proxy admin set to expected address
- [ ] Initial parameters match spec
