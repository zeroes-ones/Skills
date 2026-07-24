# CI/CD Template Sharing

> Sharing CI configurations across repos with reusable workflows, orbs, and templates.

## GitHub Reusable Workflows

```yaml
# org/shared-workflows/.github/workflows/ci-base.yml
name: CI Base
on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm run lint
```

## GitLab CI Templates

```yaml
# Consuming repo
include:
  - project: 'org/ci-templates'
    ref: 'v2.0.0'
    file: '/templates/ci-base.yml'
```

## CircleCI Orbs

```yaml
# .circleci/config.yml
version: 2.1
orbs:
  ci-orb: org/ci-orb@1.0.0
workflows:
  build:
    jobs:
      - ci-orb/lint
      - ci-orb/test
      - ci-orb/build
```

## Versioning Strategy

* **Major (X.0.0):** Breaking changes to the interface
* **Minor (X.Y.0):** New features, backward compatible
* **Patch (X.Y.Z):** Bug fixes, no interface change

**Deprecation policy:** Support each major version for 6 months after successor release. Announce deprecation 3 months before end-of-life.
