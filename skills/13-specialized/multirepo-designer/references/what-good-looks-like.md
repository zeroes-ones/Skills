# What Good Looks Like: Multirepo Architecture

A well-designed multirepo ecosystem balances autonomy with coherence. Below is the BEFORE/AFTER quality standard for multirepo design.

## BEFORE (Anti-Pattern)

```
org/
├── user-service/          # Java 8, no README
├── auth-service/          # Java 11, different build tool
├── payment-service/       # Go (why?), no CODEOWNERS
├── shared-models/         # Duplicated across 3 repos
├── common-utils/          # 47 dependencies, v0.0.1-alpha
└── legacy-migration-repo/ # 200k LOC, no owner, no CI
```

**Symptoms:**
- Every repo uses a different language version, linter config, and CI pipeline
- Shared code is copy-pasted; breaking changes cascade without warning
- No one knows who owns `legacy-migration-repo`
- Onboarding takes 6+ weeks just to understand repo boundaries

## AFTER (Quality Standard)

```
org/
├── platform-api/          # API gateway + versioning, owned by Platform
├── auth/                  # OAuth2/OIDC, owned by Identity
├── billing/               # Payments + invoicing, owned by Commerce
├── contracts/             # Protobuf/OpenAPI specs, shared across repos
├── toolkit/               # Shared CLI, CI templates, lint configs
└── sdk-generator/         # Client SDKs from contracts
```

**Characteristics:**
- Each repo has a single clear owner team, documented in CODEOWNERS
- Contracts repo publishes versioned API specs consumed by all dependents
- Toolkit repo provides `@org/eslint-config`, shared CI workflows, and boilerplate
- Breaking changes are announced via changelog + migration guide before release
- CI/CD is consistent across repos via shared GitHub Actions from toolkit
- Onboarding: clone toolkit, read contracts, and you're productive in 1 day
