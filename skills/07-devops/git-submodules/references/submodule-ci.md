# Submodule CI/CD Configuration

## GitHub Actions

```yaml
name: Build and Test
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          token: ${{ secrets.SUBMODULE_PAT }}

      # Cache submodule data for faster subsequent runs
      - uses: actions/cache@v4
        with:
          path: .git/modules
          key: submodules-${{ hashFiles('.gitmodules') }}

      # Submodule health check
      - name: Verify submodule health
        run: |
          git submodule status --recursive
          git submodule foreach 'git fetch origin && echo "Branch: $(git rev-parse --abbrev-ref HEAD)"'
```

## GitLab CI

```yaml
variables:
  GIT_SUBMODULE_STRATEGY: recursive
  GIT_SUBMODULE_DEPTH: 1

build:
  script:
    - git submodule status --recursive
    - make build
```

## Jenkins Pipeline

```groovy
checkout([
    $class: 'GitSCM',
    branches: [[name: 'main']],
    extensions: [[$class: 'SubmoduleOption', recursiveSubmodules: true]],
    userRemoteConfigs: [[url: 'https://github.com/org/repo.git']]
])
```

## Private Submodule Authentication

Use a GitHub Personal Access Token (PAT) or Deploy Key with read access to all submodule repos. Store in CI secrets. Never commit credentials to .gitmodules.
