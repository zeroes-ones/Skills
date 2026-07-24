# Best Practices

- **SLSA by default**: every new repository should start at SLSA Level 2 (signed provenance, hermetic builds) and target Level 3 within 6 months.
- **SBOM as build artifact**: generate SBOMs automatically in CI; never generate them manually or post-hoc.
- **VEX before deployment**: every CVE in your SBOM must have a VEX status (Not Affected / Affected / Under Investigation) before the artifact reaches production.
- **OIDC everywhere**: every CI/CD pipeline authenticates via workload identity federation; no static credentials in any pipeline configuration.
- **Registry scoping**: configure package managers to prefer your private registry, with explicit scoping rules that prevent public registry fallback.
- **Signed commits mandatory**: enable branch protection requiring signed commits; reject unsigned pushes automatically.
- **Dependency freshness scoring**: track and alert on dependencies that haven't been updated in >12 months or whose upstream maintainer activity has dropped below threshold.
