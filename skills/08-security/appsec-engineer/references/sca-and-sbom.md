# Software Composition Analysis (SCA) and SBOM

## Dependency Scanning Strategy

### Tiers of Dependency Risk
- Tier 1: Direct dependencies (you chose them). Scan every commit. Any CRITICAL CVE blocks PR.
- Tier 2: Transitive dependencies (pulled in by your dependencies). Scan daily. CRITICAL+KEV blocks release.
- Tier 3: Build tool dependencies (devDependencies, test frameworks). Scan weekly. Alert on CRITICAL only.

### Reachability Analysis

A vulnerable function in a dependency that your code never calls is low risk. Reachability analysis determines if the vulnerable code path is actually exercised.

Static reachability: CodeQL data flow analysis -- does untrusted input reach the vulnerable function?
Runtime reachability (Java/.NET): Aspect-oriented instrumentation -- is the vulnerable method ever called in production?

Decision matrix:
| Reachable? | Internet-facing? | Auth required? | Priority |
|-----------|-----------------|---------------|----------|
| Yes | Yes | No | EMERGENCY (fix now) |
| Yes | Yes | Yes | HIGH (fix in 72h) |
| Yes | No | Yes | MEDIUM (fix in 7d) |
| No | Yes | N/A | MEDIUM (fix in 14d) |
| No | No | N/A | LOW (fix in 30d) |

## SBOM Generation and Verification

### Generation (at build time)
```bash
# Node.js
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Python
pip install cyclonedx-bom && cyclonedx-py --output sbom.json

# Go
go install github.com/CycloneDX/cyclonedx-gomod@latest && cyclonedx-gomod mod -json -output sbom.json
```

### Verification (at deploy time)
1. Compare build-time SBOM against deploy-time SBOM for new or unexpected dependencies
2. Scan SBOM against vulnerability database (Grype, Trivy) for known CVEs
3. Block deployment if new CRITICAL CVE with evidence of active exploitation (CISA KEV)

## SLSA Supply Chain Integrity (Levels 1-3)

| Level | Requirements | Protects Against |
|-------|-------------|-----------------|
| SLSA 1 | Build has provenance (attestation of how it was built) | Basic documentation of build process |
| SLSA 2 | Version control + hosted build service generating provenance | Tampering after build (modifying artifacts) |
| SLSA 3 | Hermetic builds + isolated build environment + signed provenance | Compromised build platform or dependencies |
| SLSA 4 | Two-person review of all changes + reproducible builds | Insider threat, compromised developer accounts |

### Sigstore Integration
- cosign sign: Attach signed attestation to container image or artifact
- cosign verify: Verify provenance attestation before deployment
- Keyless signing: OIDC-based (GitHub Actions -> Fulcio certificate), no long-lived signing keys to manage
