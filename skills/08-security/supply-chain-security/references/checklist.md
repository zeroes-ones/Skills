# Production Checklist

- [ ] All builds produce SLSA Level 2+ provenance attestations
- [ ] SBOM generated for every release artifact (container image, package, binary)
- [ ] VEX document accompanies every SBOM with CVE exploitability assessment
- [ ] All CI/CD pipelines use OIDC federation — zero long-lived credentials
- [ ] Dependency scanning configured to full transitive depth
- [ ] Critical CVE patches merged within 24-hour SLA (CVSS ≥ 9.0)
- [ ] All commits to default branch are signed (GPG/SSH)
- [ ] Package registries scoped to prevent dependency confusion
- [ ] `ignore-scripts=true` in CI `.npmrc` files
- [ ] Build environments are ephemeral and isolated (no shared runners)
- [ ] Artifact signatures verified at every deployment gate
- [ ] Vendor SBOMs collected and independently verified for all critical dependencies
- [ ] Transparency log monitoring enabled for unexpected artifact signatures
- [ ] Supply chain security incidents have documented response playbooks
