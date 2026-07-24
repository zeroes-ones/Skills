# Scale Depth: Solo → Small → Medium → Enterprise

| Scale | Supply Chain Posture | Tools | Annual Cost |
|---|---|---|---|
| **Solo** | SBOM generation (syft), Dependabot (free), cosign keyless signing (free), gitleaks pre-commit (free) | syft, cosign, gitleaks | $0 |
| **Small (2-10)** | + SLSA Level 2, Renovate with auto-PR, Trivy full-depth scanning, npm provenance | syft, cosign, trivy, renovate | $0-$200/month |
| **Medium (10-50)** | + SLSA Level 3, VEX generation, vendor SBOM collection, admission control (Kyverno/OPA), private package registry | Dependency-Track, Kyverno, sigstore policy-controller | $500-$5K/month |
| **Enterprise (50+)** | + SLSA Level 4 (two-person review + hermetic), continuous vendor monitoring, dedicated supply chain security team, supply chain incident response playbooks | Chainguard Enforce, Anchore Enterprise, dedicated TIP integration | $10K-$100K/month |
