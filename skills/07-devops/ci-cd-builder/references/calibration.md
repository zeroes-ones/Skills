# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You copy-paste workflow YAML from Stack Overflow and tweak it until it turns green — you don't know what `actions/checkout@v4` actually does | Every merge triggers a deterministic, reproducible CI pipeline. You know the difference between `pull_request` and `pull_request_target` and can explain why one is dangerous without looking it up | You've reduced the organization's CI cost per deploy by 60%+ through caching, matrix optimization, and selective test execution — and you have the dashboard to prove it |
| You resolve "build failed" by clicking "Re-run all jobs" — you've never looked at the logs of a failed retry to understand why it failed the first time | You've implemented flaky test quarantining, and your team's flaky test rate dropped below 2%. Failed builds are always real failures | You designed a CI system where the mean time from push to deploy decision is under 4 minutes for a monorepo with 300+ services — only changed services are tested and built |
| You've never audited who has access to repository secrets or what permissions your workflows actually use | Every workflow has a minimal permissions block: `permissions { contents: read }`. You review workflow permissions in every PR like you review code | You've built a supply chain attestation pipeline: every artifact is signed with Sigstore/cosign, has a verifiable SLSA Level 3 provenance, and passes policy checks in an admission controller before deployment |

**The Litmus Test:** Can you receive a PR from an untrusted fork, run its tests safely, and deploy it to production — all automated with SLSA Level 3 provenance — with zero human access to secrets or cloud credentials? Can you prove the artifact running in production is bit-for-bit identical to what was built in CI?
