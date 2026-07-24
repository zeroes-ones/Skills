# SBOM & Supply Chain Security

Software Bill of Materials (SBOM) generation, signing, attestation, and verification for supply chain security.

## What is an SBOM?

A machine-readable inventory of all components in a software artifact. Analogous to a food ingredient list — you cannot assess safety if you do not know what is inside.

## SBOM Formats

- **SPDX (ISO/IEC 5962:2021):** Linux Foundation. Most widely adopted. ISO standard.
- **CycloneDX (OWASP):** OWASP. Lighter weight. Strong security focus.
- **Syft (Anchore):** Generates both formats from container images, filesystems, and codebases.

## Generation Pipeline

1. **Generate:** `syft packages . -o spdx-json > sbom.spdx.json` in CI on every release.
2. **Sign:** `cosign sign-blob --key cosign.key sbom.spdx.json` or keyless signing via OIDC.
3. **Attach:** Attach SBOM to container image: `cosign attach sbom --sbom sbom.spdx.json image:tag`.
4. **Publish:** Store in OCI registry alongside image or in dedicated SBOM repository.

## Verification Pipeline

1. **Verify signature:** `cosign verify-blob --key cosign.pub --signature sbom.spdx.json.sig sbom.spdx.json`.
2. **Policy check:** Parse SBOM. Check each component against:
   - License policy (no blocked licenses).
   - CVE policy (no critical CVEs older than SLA).
   - Maintenance policy (no packages abandoned >12 months).
3. **Block deployment** if policy fails.

## SLSA Framework (Supply-chain Levels for Software Artifacts)

| Level | Requirement | Example |
|-------|-------------|---------|
| L1 | Build provenance documented | GitHub Actions with provenance generation |
| L2 | Hosted build platform + signed provenance | GitHub Actions + SLSA generator workflow |
| L3 | Hardened build platform (isolated, ephemeral) | Custom build service with attestation |
| L4 | Hermetic, reproducible builds + two-person review | Highest assurance. Rare outside critical infra. |

## Dependency Firewall

Block known-bad packages at CI time:
- Known-malicious packages (npm advisory database, Socket.dev).
- Typosquatting detection (package names similar to popular packages).
- Unmaintained packages (>1 year since last commit to main branch).
