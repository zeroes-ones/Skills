# Footguns

- **`npm publish` without `--provenance`** ships packages with no supply chain attestation. GitHub's npm provenance is free and adds 2 seconds to publish — but you must explicitly opt in.
- **`.docker/config.json` with stored credentials** survives in CI cache between runs. A compromised dependency with a postinstall script can read and exfiltrate registry credentials.
- **`pip install -r requirements.txt` without `--require-hashes`** accepts any package with the right name and version — including a dependency confusion attack with the same version number.
- **Renovate's `:automergeMinor` preset** auto-merges minor version bumps — but semver minor can introduce new dependencies, breaking changes, and supply chain risks.
- **`cosign sign` with `--key` flag using a CI secret** signs with the same key for every build. Key compromise means all historical signatures are untrustworthy. Use keyless signing (`cosign sign` without `--key`) for per-build ephemeral keys.
- **`docker save image | docker load`** strips signatures and attestations. Container images transferred via `docker save` lose all Sigstore signatures — verify after loading, not before saving.
