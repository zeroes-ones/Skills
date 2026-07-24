# License Compliance Automation

Automated detection and enforcement of license policies across the full dependency tree.

## License Risk Classification

### Green (Auto-Approved)
MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unlicense, CC0-1.0, Python-2.0, PostgreSQL.

### Yellow (Review Required)
MPL-2.0, LGPL-2.1, LGPL-3.0, EPL-2.0, CDDL-1.0, CPL-1.0, Artistic-2.0.

### Red (Legal Approval Required)
GPL-2.0, GPL-3.0, AGPL-3.0, EUPL-1.2, SSPL-1.0, BSL-1.1.

### Blocked
No license, WTFPL, Beerware, Commons Clause, custom/proprietary without approval.

## CI Enforcement

1. **Pre-commit/CI hook:** Scan `package.json` changes for new dependencies.
2. **License check:** `license-checker --production --json` or equivalent.
3. **Policy check:** Compare each license against the classification matrix.
4. **Action:**
   - Green -> pass.
   - Yellow -> warn, require documented review.
   - Red -> block merge. Require legal approval.
   - Blocked -> block merge. No exceptions without legal + engineering leadership.

## Copyleft Nuances

- **GPL linking:** Static linking likely contaminates proprietary code. Dynamic linking is jurisdiction-dependent.
- **AGPL network use:** Triggered by SaaS/network use. Stricter than GPL for web services.
- **LGPL:** Lesser GPL. Dynamic linking generally safe for proprietary code.
- **MPL-2.0:** File-level copyleft. Only modified MPL files must be shared.

## Tools

- **license-checker (JS):** CLI. Direct + transitive. JSON output.
- **FOSSA:** Commercial. Deep dependency analysis. Policy enforcement.
- **Snyk License Compliance:** Commercial. Integrated with vulnerability scanning.
- **ORT (OSS Review Toolkit):** Open source. Comprehensive license + vulnerability analysis.
- **GitHub Dependency Review:** Built-in. Surface-level but free.

## Exceptions Process

1. Engineer requests exception with justification.
2. Legal reviews and approves (or denies) with documented rationale.
3. Exception added to allow-list with expiration date.
4. Monthly review: still needed? Can we replace the dependency?
