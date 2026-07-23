# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Pin actions by SHA digest, never by tag** — `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2`. Tags can be force-pushed.
- **Separate build and deploy workflows** — Build (read-only) runs on PR. Deploy (write) runs on merge to main. Different IAM roles, different risk profiles.
- **Artifact promotion: build once, deploy many** — Never rebuild binaries/images between environments. Immutable artifacts with SHA-tagged images.
- **Concurrency groups prevent race conditions** — `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }`. Saves CI minutes and prevents stale deploys.
- **Secrets via environments + OIDC, never hardcoded** — Each environment has its own secrets. CI roles use OIDC with audience + subject restrictions. Rotate any static tokens on schedule.
- **Warm caches on schedule** — `on: schedule: cron: '0 */6 * * *'` runs dependency install to keep cache fresh for PR workflows.
- **Validate locally before pushing** — `act` for GitHub Actions, `gitlab-ci-local` for GitLab CI. Catch syntax errors before CI runtime.
