# Shared Library Publishing & Versioning Strategies

Publishing internal libraries across repos requires disciplined versioning, artifact management, and consumer communication. Here are the battle-tested patterns.

## Publishing Models

### 1. Semver + Internal Registry (Recommended)
```bash
# toolkit/.github/workflows/publish.yml
npm publish --registry https://npm.internal.company.com

# Consumers pin exact versions
# auth/package.json
{ "dependencies": { "@org/toolkit": "3.1.0" } }
```

### 2. Git Submodules / Git References
```bash
# Only for pre-publishing during co-development
git submodule add https://github.com/org/toolkit lib/toolkit
# Consumers reference by commit SHA, not branch
```

### 3. Monorepo Export (Nx/Turborepo)
```bash
# Publish only specific packages from a monorepo
npx nx release publish --projects=@org/toolkit,@org/contracts
```

## Versioning Strategies

### Independent Versioning (Recommended for Polyrepo)
Each repo versions independently. Consumer pins major version, receives minor/patch automatically.
```
contracts v2.3.1 -> consumers pin ^2.0.0
toolkit v3.1.0  -> consumers pin ^3.0.0
```

### Lockstep Versioning
All repos share a version number. Used when repos form a tightly coupled platform.
```
platform-v4.2.0 includes: contracts v4.2.0, toolkit v4.2.0, auth v4.2.0
```
**Risk:** Creates a distributed monolith. Only use when repos cannot evolve independently.

## Release Channels

| Channel | Audience | Stability | Example |
|---------|----------|-----------|---------|
| **latest** | All consumers | Stable, semver releases | `@org/toolkit@3.1.0` |
| **next** | Early adopters | Pre-release, may break | `@org/toolkit@3.2.0-beta.1` |
| **canary** | CI/testing only | Every commit, highly unstable | `@org/toolkit@0.0.0-canary.abc123` |
| **lts** | Risk-averse consumers | Backported fixes only | `@org/toolkit@2.5.1-lts` |

## Consumer Communication

### Automated Dependency Updates
```json
// renovate.json in consumer repos
{
  "packageRules": [{
    "matchPackageNames": ["@org/toolkit"],
    "schedule": ["before 9am on Monday"],
    "automerge": true,
    "automergeType": "pr",
    "matchUpdateTypes": ["patch", "minor"]
  }]
}
```

### Changelog Standards
Every release must include a changelog following Keep a Changelog format:
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be-removed features
- `Removed` for removed features
- `Fixed` for bug fixes
- `Security` for vulnerability fixes

### Breaking Change Banner
Place a prominent warning at the top of any release with breaking changes:
```
⚠️ BREAKING: This release removes the deprecated `User.email` field.
See migration guide: https://docs.internal.company.com/toolkit/migration/v3-to-v4
```
