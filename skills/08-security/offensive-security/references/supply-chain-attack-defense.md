# Supply Chain Attack Defense

## Overview

Supply chain attacks compromise an organization through its dependencies, build tools, or third-party services. The 2020 SolarWinds attack demonstrated that a single compromised build pipeline can impact 18,000+ organizations. This reference covers dependency confusion, compromised package detection, SLSA framework implementation, and build pipeline hardening.

## Dependency Confusion Attacks

Dependency confusion (also called namespace confusion) exploits how package managers resolve package names when both private/internal and public registries are configured.

### Attack Mechanism
1. Organization uses private package "company-auth-lib" (published to internal Artifactory/Nexus).
2. Developer configures pip/npm to use both private registry AND public PyPI/npm.
3. Attacker publishes "company-auth-lib" to public PyPI with a higher version number.
4. Package manager resolves to the public (higher version) package instead of the internal one.
5. Malicious package executes via install hooks (setup.py post-install, npm preinstall/postinstall scripts).

### Testing Methodology
- **Discover internal package names:** package.json / requirements.txt files in public repos, CI/CD logs, job postings, developer forum posts, npm/pip internal registry names in error messages.
- **Verify resolution order:** Check .npmrc, .pypirc, pip.conf for registry configuration. pip uses --extra-index-url which prefers higher version regardless of source. npm scoped packages (@company/package) are safer -- they require explicit registry mapping.
- **Safe testing:** Publish a benign package ("company-test-package-{unique-hash}") with no install hooks, just a version file. If it gets installed in a test environment, dependency confusion exists.

### Defenses
- Use scoped packages (@company/package-name in npm) -- scoped packages are tied to specific registries.
- Configure pip with --index-url (exclusive) rather than --extra-index-url (supplemental) for private packages.
- Implement package allowlists in CI/CD: only allow specific packages from specific registries.
- Use dependency proxy/caching (Artifactory remote repositories, Verdaccio) to control upstream sources.

## SLSA Framework (Supply Chain Levels for Software Artifacts)

SLSA v1.0 defines four build integrity levels:
