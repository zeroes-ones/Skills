# CI/CD Builder - Pipeline Design Patterns

Production-grade pipeline design: stages, caching, matrix builds, deployments, and optimization.

---

## Pipeline Stage Design

Standard pipeline structure: Lint → Test → Build → Deploy

```
[Push/PR] → [Lint] → [Unit Tests] → [Build Artifact] → [Integration Tests] → [Deploy Staging] → [Smoke Tests] → [Deploy Prod]
                  ↘ [Security Scan] ↗                                               ↘ [E2E Tests] ↗
```

### Stage Responsibilities

| Stage | Purpose | Fails Fast | Typical Duration |
|-------|---------|------------|-----------------|
| **Lint** | Style, formatting, static analysis, type checking | Yes | <2 min |
| **Unit Tests** | Isolated logic verification | Yes | <5 min |
| **Security Scan** | SAST, dependency vulns, secret detection | Yes | 2-5 min |
| **Build** | Compile, bundle, containerize | Yes | 3-10 min |
| **Integration Tests** | Service interactions, DB, APIs | No | 5-15 min |
| **Deploy Staging** | Deploy to pre-prod environment | No | 2-5 min |
| **Smoke Tests** | Critical path health checks | No | 2-5 min |
| **E2E Tests** | Full user journey testing | No | 10-30 min |
| **Deploy Prod** | Production rollout with health monitoring | No | 5-15 min |

---

## Caching Strategies

### GitHub Actions

```yaml
# Node.js — npm cache
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

# Python — pip cache
- uses: actions/setup-python@v4
  with:
    python-version: '3.12'
    cache: 'pip'

# Go — module cache
- uses: actions/setup-go@v5
  with:
    go-version: '1.22'
    cache: true  # Auto-detects go.sum

# Docker layer caching
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# Generic path cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/ms-playwright
      node_modules/.cache
    key: ${{ runner.os }}-cache-${{ hashFiles('**/lockfiles') }}
    restore-keys: ${{ runner.os }}-cache-
```

### GitLab CI

```yaml
# npm cache
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/

# Docker layer caching with --cache-from
build:
  before_script:
    - docker pull $CI_REGISTRY_IMAGE:latest || true
  script:
    - docker build --cache-from $CI_REGISTRY_IMAGE:latest -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
```

### Go Module Caching Tips
```yaml
# Best practice: cache both module download dir and build cache
env:
  GOMODCACHE: ${{ github.workspace }}/.gocache/mod
  GOCACHE: ${{ github.workspace }}/.gocache/build
```

---

## Matrix Builds — Multi-Platform Testing

### GitHub Actions Matrix

```yaml
jobs:
  test:
    strategy:
      fail-fast: false  # Don't cancel other jobs if one fails
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [18, 20, 22]
        exclude:
          # Skip Node 18 on Windows
          - os: windows-latest
            node-version: 18
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Platform + Architecture Matrix

```yaml
jobs:
  build:
    strategy:
      matrix:
        platform:
          - linux/amd64
          - linux/arm64
          - linux/arm/v7
    steps:
      - uses: docker/setup-qemu-action@v3
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v5
        with:
          platforms: ${{ matrix.platform }}
```

---

## Deployment Patterns

### Blue-Green Deployment
Two identical environments. Route traffic via load balancer swap.

```yaml
deploy:
  script:
    - deploy_to_green.sh $VERSION
    - smoke_test_green.sh
    - swap_lb_to_green.sh  # Instant rollback: swap back to blue
    - sleep 300            # Keep blue warm for 5 min
    - decomission_blue.sh
```

**Pros:** Zero downtime, instant rollback
**Cons:** Double infrastructure cost during deploy

### Canary Deployment
Gradually shift traffic to new version.

```yaml
canary:
  script:
    - deploy_canary_v2.sh
    - route 5% traffic to v2
    - monitor_errors_v2.sh 5m
    - route 25% traffic to v2
    - monitor_errors_v2.sh 10m
    - route 100% traffic to v2
    - decommission_v1.sh
```

**Pros:** Progressive risk reduction, real-user validation
**Cons:** Complex routing, longer deploy time

### Rolling Deployment
Replace instances one at a time.

```yaml
rolling:
  script:
    - kubectl set image deployment/app app=app:$VERSION
    - kubectl rollout status deployment/app --timeout=5m
    # On failure: kubectl rollout undo deployment/app
```

**Pros:** No extra infra cost, gradual rollout
**Cons:** Mixed versions during deploy, slower rollback

---

## Environment Promotion

```
dev (auto on push) → staging (auto on PR merge) → production (manual approval)
```

```yaml
# GitHub Actions — environment promotion with protection rules
jobs:
  deploy-staging:
    environment: staging
    steps:
      - run: deploy staging

  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://app.example.com
    steps:
      - run: deploy production
```

**Environment Protection Rules (GitHub):**
- Required reviewers (1-6 approvers)
- Wait timer (e.g., 30 minutes before prod deploy)
- Branch restrictions (only from `main`)
- Deployment gates (workflow must pass checks)

---

## Secrets Management in Pipelines

### Principles
1. **Never hardcode secrets** in pipeline files
2. **Use platform secret stores:** GitHub Secrets, GitLab Variables (masked), Vault, AWS Secrets Manager
3. **Least privilege:** Each job gets only secrets it needs
4. **Rotate regularly:** Automate rotation via pipeline or vault

```yaml
# GitHub Actions — referencing secrets
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}  # Masked in logs
  # AVOID: echo $DATABASE_URL — will be masked, but don't risk it

# GitLab CI — masked variables
variables:
  DATABASE_URL: $DATABASE_URL  # Set in Settings → CI/CD → Variables, masked

# Vault integration for dynamic secrets
- name: Get DB credentials from Vault
  run: |
    export VAULT_TOKEN=$(vault write -field=token auth/jwt/login role=ci-role jwt=$CI_JOB_JWT)
    export DB_CREDS=$(vault read -format=json database/creds/readonly)
    echo "DB_USER=$(echo $DB_CREDS | jq -r .data.username)" >> $GITHUB_ENV
```

---

## GitHub Actions vs GitLab CI Comparison

| Feature | GitHub Actions | GitLab CI |
|---------|---------------|-----------|
| **Config file** | `.github/workflows/*.yml` | `.gitlab-ci.yml` |
| **Runners** | GitHub-hosted (Ubuntu, macOS, Windows) + self-hosted | GitLab-hosted (Linux) + self-hosted |
| **Matrix builds** | `strategy.matrix` | `parallel:matrix` |
| **Artifacts** | `upload-artifact` / `download-artifact` | `artifacts:` keyword with expiry |
| **Caching** | `actions/cache@v4` with key + restore-keys | Auto or `cache:` keyword |
| **Environments** | Environment protection rules + approval | `environment:` with approval rules |
| **Reusable workflows** | Yes (`workflow_call`) | Yes (`include`, `extends`, `!reference` tags) |
| **Secrets** | `${{ secrets.NAME }}` | `$VARIABLE_NAME` (masked flag) |
| **Free tier** | 2000 min/month (private), unlimited public | 400 min/month (shared runners) |
| **Marketplace** | Extensive action marketplace | Limited built-in templates |
| **Docker support** | Native (services) + Docker actions | Native + Docker executor |

### Migration Snippets

**GHA → GitLab CI:**
```yaml
# GitHub Actions
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

# GitLab CI equivalent
test:
  image: node:20
  script:
    - npm test
  only:
    - pushes
```

**GitLab CI → GHA:**
```yaml
# GitLab CI
stages:
  - build
  - test

# GitHub Actions
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]
  test:
    needs: build
    runs-on: ubuntu-latest
    steps: [...]
```

---

## Pipeline Optimization

### Parallel Jobs
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [lint]

  unit-tests:
    runs-on: ubuntu-latest
    steps: [unit tests]

  integration-tests:
    needs: [lint, unit-tests]  # Wait for lint + unit, but they run in parallel
    runs-on: ubuntu-latest
    steps: [integration tests]
```

### Conditional Execution
```yaml
# Only run expensive E2E tests if src/ or tests/ changed
- name: Check for relevant changes
  uses: dorny/paths-filter@v3
  id: changes
  with:
    filters: |
      e2e:
        - 'src/**'
        - 'tests/e2e/**'
        - 'package.json'

- name: E2E Tests
  if: steps.changes.outputs.e2e == 'true'
  run: npm run test:e2e
```

### Path Filtering for Monorepos
```yaml
# Only build services that changed
- uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      api:
        - 'services/api/**'
      web:
        - 'services/web/**'
      shared:
        - 'packages/shared/**'

- name: Build API
  if: steps.filter.outputs.api == 'true' || steps.filter.outputs.shared == 'true'
  run: cd services/api && make build
```

### Workflow Optimization Checklist
- [ ] Cancel redundant runs: `concurrency: ci-${{ github.ref }}` — cancel in-progress runs on same branch
- [ ] Use `fail-fast: false` in matrix builds
- [ ] Cache aggressively (npm, pip, Docker layers, Go modules)
- [ ] Profile pipeline: add timing annotations; optimize slowest stage first
- [ ] Skip unnecessary stages (path filtering, conditional execution)
- [ ] Use smaller base images (distroless, alpine, slim)
- [ ] Parallelize independent jobs
- [ ] Set reasonable timeouts: `timeout-minutes: 15`
- [ ] Use `restore-keys` for partial cache hits
- [ ] Pre-warm Docker registries for frequent pull images
