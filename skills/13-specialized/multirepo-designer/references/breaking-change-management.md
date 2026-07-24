# Breaking Change Management Across Repositories

Breaking changes in a multirepo ecosystem are high-stakes: one repo's change can break N downstream consumers silently. A disciplined process is non-negotiable.

## The Breaking Change Lifecycle

### Phase 1: Deprecation (Release N)
- Add `@deprecated` annotation with a migration hint
- Emit a warning at runtime (not error) for deprecated usage
- Update changelog with `DEPRECATED:` prefix
- Example commit message: `deprecate: User.email -> User.emailAddress (removal in v4.0)`

### Phase 2: Grace Period (Release N+1 to N+K)
- Keep deprecated code functional for K releases (typically 2-3 minor versions)
- Monitor adoption: track how many consumers have migrated
- Send automated PRs to downstream repos (e.g., RenovateBot + codemod)
- Publish migration guide in contracts/ or toolkit/ docs

### Phase 3: Removal (Release N+K+1)
- Remove deprecated code in a MAJOR version bump (semver)
- Block release if any known consumer hasn't migrated (CI gate)
- Post-removal: run integration tests across all downstream repos before merge

## Detection Tooling

```yaml
# In contracts repo CI: detect breaking changes automatically
breaking-change-detection:
  steps:
    - uses: bufbuild/buf-breaking-action@v1  # Protobuf
    - uses: openapi-diff-action@v2            # REST APIs
    - run: npx @org/schema-diff                # Internal schemas
```

## Communication Channels

| Change Severity | Notification | Lead Time | Approval Required |
|----------------|-------------|-----------|-------------------|
| **PATCH** (non-breaking) | Changelog | None | None |
| **MINOR** (additive) | Changelog + Slack | 1 week | None |
| **MAJOR** (breaking) | Changelog + Slack + Email + Automated PRs | 4+ weeks | Architecture Review Board |
| **SECURITY** | Private channel first, then coordinated disclosure | As needed | Security team + ARB |

## Emergency Breaking Changes

When a security vulnerability forces an immediate breaking change:
1. Create a private fork
2. Test against all known consumer contracts
3. Ship with a migration script in the release
4. Open automated PRs to all downstream repos simultaneously
5. Post-mortem within 48 hours: why wasn't this caught earlier?

## Anti-Pattern: "YOLO Major"

Never ship breaking changes without deprecation. Even "nobody uses this" is wrong — you don't know who uses it until they break. Always deprecate first, even if it feels unnecessary. The cost of a deprecation cycle is ~10x cheaper than a production incident.
