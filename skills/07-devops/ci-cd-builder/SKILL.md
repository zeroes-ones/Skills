---
name: ci-cd-builder
description: GitHub Actions, pipeline design patterns, build optimization, artifact management, quality gates, deployment strategies, SLSA supply chain security, DORA metrics, and release management. Triggered
  by CI/CD, pipeline, GitHub Actions, GitLab CI, build, matrix, cache, artifact, deployment gate, SLSA, DORA.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- ci-cd-builder
token_budget: 4000
chain:
  consumes_from:
  - backend-developer
  - devops-engineer
  - monorepo-manager
  - qa-engineer
  - security-engineer
  - translation-manager
  feeds_into:
  - accessibility-testing
  - devops-engineer
  - docker-kubernetes
  - monorepo-manager
  - qa-engineer
  - release-manager
output:
  type: code
  path_hint: ./
---
# CI/CD Pipeline Builder

Design, build, optimize, and secure continuous integration and continuous delivery pipelines. This
skill covers pipeline architecture patterns (fan-in/fan-out, matrix, conditional), GitHub Actions
deep-dive (composite actions, reusable workflows, OIDC, self-hosted runners), build optimization
(caching, incremental builds, artifact management), quality gates (SonarQube, coverage, CVE, budget),
deployment strategies (rolling, blue-green, canary, feature-flagged), SLSA supply chain security,
release management (semantic release, changelog, approval workflows), and DORA metrics tracking.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Create a new CI/CD pipeline from scratch → Jump to "Core Workflow" — Phase 1 (Pipeline Architecture)
├── Optimize slow builds (caching, parallelism, sharding) → Jump to "Core Workflow" — Phase 2 (Build Optimization)
├── Set up deployments (rolling, blue-green, canary) → Jump to "Core Workflow" — Phase 3 (Deployment)
├── Add security scanning (SAST, SCA, secrets) to pipeline → Jump to "Core Workflow" — Phase 4 (Security Gates)
├── Debug a failing pipeline → Go to "Decision Trees" — then "Production Checklist"
├── Need infrastructure provisioning → Invoke `devops-engineer` skill instead
├── Need release management → Invoke `release-manager` skill instead
├── Need container orchestration → Invoke `docker-kubernetes` skill instead
├── Need quality engineering → Invoke `qa-engineer` skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never build without understanding the deployment target.** A pipeline that works for Kubernetes won't work for Lambda. Ask: where does this deploy, how, and what's the rollback strategy?
- **Pipeline failures must have clear error messages.** "Build failed" is not actionable. Every failure must surface: what failed, which step, which file, which line, and what to do about it.
- **Secrets must never be in logs.** Mask all secrets in pipeline output. A leaked API key in a public CI log is a security incident, not a debugging convenience.
- **Cache invalidation must be explicit.** Cache keys must include a content hash or version. A stale cache that passes CI is worse than no cache — it creates false confidence.
- **Always design for pipeline security.** Use OIDC instead of long-lived credentials. Pin action versions by SHA, not tags. Sign artifacts and generate SBOMs.
- **Admit what you don't know.** If you're unfamiliar with a specific CI platform's capabilities or a deployment target's constraints, say so and point to the docs.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Architecting a CI/CD pipeline from scratch for monorepos, microservices, or polyglot codebases
- Migrating pipelines between CI systems: Jenkins → GitHub Actions, CircleCI → GitLab CI
- Optimizing slow builds: dependency caching, parallel job execution, test sharding, incremental builds
- Implementing deployment strategies: rolling, blue-green, canary, feature-flagged rollouts
- Setting up quality gates: SonarQube quality gate, coverage thresholds, CVE severity, bundle size budgets
- Hardening pipeline security: signed commits, SLSA provenance (Level 1-3), SBOM generation
- Building ephemeral per-PR environments with automated provisioning and teardown
- Implementing semantic release with conventional commits enforcement and changelog automation
- Measuring and improving DORA metrics: deployment frequency, lead time, MTTR, change failure rate

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### CI Platform Selection
```
                     ┌──────────────────────────┐
                     │ START: Choose CI platform  │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Code hosted on GitHub AND  │
                    │ team <50 engineers?        │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ GitHub      │   │ Self-hosted or  │
                    │ Actions     │   │ GitLab already? │
                    │ (default)   │   └────┬────────┬───┘
                    └─────────────┘        │ YES    │ NO
                                      ┌────▼────┐ ┌▼──────────┐
                                      │ GitLab  │ │ Jenkins    │
                                      │ CI      │ │ only if     │
                                      │         │ │ migrating   │
                                      └─────────┘ │ legacy      │
                                                  └────────────┘
```
**When to choose GitHub Actions:** Code on GitHub, <50 engineers, <100 concurrent jobs, need OIDC to cloud, DORA-focused. **When to choose GitLab CI:** Self-hosted requirement, GitLab ecosystem, >100 concurrent jobs, need integrated container registry. **When to choose Jenkins:** Legacy migration path only — avoid for greenfield.

### Deployment Strategy Selection
```
                     ┌──────────────────────────┐
                     │ START: Production deploy   │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Zero-downtime required AND │
                    │ >1000 concurrent users?    │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Need gradual │   │ Rolling deploy  │
                    │ traffic shift│   │ (standard)      │
                    │ with metrics?│   └────────────────┘
                    └────┬────────┘
                         │ YES
                    ┌────▼────────┐
                    │ Canary (10%  │
                    │ → 50% → 100%│
                    │ with auto-   │
                    │ rollback on  │
                    │ error spike) │
                    └──────────────┘
```
**When to choose Canary:** >1000 concurrent users, need metrics-based rollback, error budget >0.1%, can afford 10 min observation windows. **When to choose Blue-Green:** Instant rollback needed, DB schema compatible with both versions, can afford 2× infrastructure during deploy. **When to choose Rolling:** Standard case — sequential pod replacement, simplest, works for 90% of services.

### Build Optimization Tactic
```
                     ┌──────────────────────────┐
                     │ START: CI build >10 min    │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Dependencies unchanged     │
                    │ across >80% of commits?    │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Cache deps  │   │ Tests take >60% │
                    │ layer first │   │ of build time?  │
                    │ (50-80%      │   └────┬────────┬──┘
                    │ speedup)     │        │ YES    │ NO
                    └──────────────┘   ┌────▼────┐ ┌▼──────────┐
                                       │ Parallel │ │ Split into │
                                       │ test     │ │ smaller    │
                                       │ sharding │ │ jobs       │
                                       │ (2-4×)   │ │            │
                                       └──────────┘ └────────────┘
```
**When to cache deps:** Dependencies stable, build time >5 min, cache hit rate >80% expected. **When to shard tests:** >200 test cases, tests CPU-bound, CI runner has 4+ cores. **When to split jobs:** Monorepo with independent modules, build >15 min, multiple teams.

### Supply Chain Security Depth
```
                     ┌──────────────────────────┐
                     │ START: Secure the pipeline │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Deploying to production    │
                    │ with paying customers?     │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ SLSA Level 2│   │ SLSA Level 1    │
                    │ + SBOM +    │   │ (provenance     │
                    │ signed      │   │ only)           │
                    │ artifacts   │   └────────────────┘
                    └────┬────────┘
                         │
                    ┌────▼────────┐
                    │ Regulated    │
                    │ industry?    │
                    └────┬────────┘
                    │ YES → SLSA Level 3
                    │ (hermetic builds,
                    │  isolated, policy-
                    │  controlled)
                    └──────────────┘
```
**When to target SLSA L1:** Internal tools, pre-production, non-critical services. **When to target SLSA L2:** All production services — signed provenance + hosted build platform + SBOM generation. **When to target SLSA L3:** Fintech, healthcare, gov — hermetic builds, isolated environments, policy-controlled deployments.

### Release Workflow Design
```
                     ┌──────────────────────────┐
                     │ START: Release strategy    │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Multiple teams deploying    │
                    │ independently to production?│
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Trunk-based │   │ GitFlow with    │
                    │ + feature   │   │ release branches│
                    │ flags       │   │ (simpler for     │
                    │ (DORA elite)│   │ single team)    │
                    └─────────────┘   └────────────────┘
```
**When to choose Trunk-based:** >5 engineers, deploy >daily, DORA elite target, feature flag infrastructure in place. **When to choose GitFlow:** <5 engineers, deploy <weekly, no feature flag system, need explicit release stabilization window.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Pipeline Architecture Design

1. **Standard Pipeline Stages**:
   ```
   Trigger → Lint → Unit Test → Build → Security Scan → Integration Test → Deploy (Dev) → Deploy (Staging) → Deploy (Prod) → Post-Deploy Verify
                └───────────┬───────────┘
                       Quality Gates
   ```


**What good looks like:** Pipeline completes in under 15 minutes for a full build-test-deploy cycle. All stages pass on every PR merge. Failed deploys auto-rollback within 2 minutes. Secrets are injected at runtime — zero plaintext in pipeline config.

2. **Pipeline Topology Decision Tree**:
   ```
   Monorepo?
   ├─ YES → Path-filtered workflows + fan-out per service
   │   └─ pattern: on.push.paths: ['services/auth/**'] triggers only auth pipeline
   ├─ Polyglot?
   │   ├─ YES → Matrix builds across language × version
   │   └─ NO → Single build job, optimized caching
   └─ Multi-cloud deploy?
       └─ Sequential or fan-in: build once → parallel deploy to aws/gcp/azure
   ```

3. **Fan-In/Fan-Out Pattern** (GitHub Actions):
   ```yaml
   # Fan-out: parallel test across platforms
   test:
     strategy:
       matrix:
         os: [ubuntu-latest, windows-latest]
         node: [18, 20, 22]
     runs-on: ${{ matrix.os }}
     steps: [checkout, setup-node, npm test]

   # Fan-in: collect results, gate deploy
   deploy:
     needs: [test, lint, security-scan]
     if: success()
     environment: production
   ```

4. **Conditional Execution** — Don't run expensive steps unnecessarily:
   ```yaml
   - name: Build Docker image
     if: steps.cache-image.outputs.cache-hit != 'true'

   - name: Run integration tests
     if: github.event_name == 'pull_request' && contains(github.event.pull_request.labels.*.name, 'run-integration')

   - name: Deploy to production
     if: github.ref == 'refs/heads/main' && github.event_name == 'push'
   ```

### Phase 2 (~30 min): GitHub Actions Deep-Dive

1. **Composite Actions** — Bundle reusable steps:
   ```yaml
   # .github/actions/setup-node-build/action.yml
   name: Setup Node & Build
   description: Checkout, install Node, restore cache, install deps, build
   inputs:
     node-version:
       required: true
       default: '20'
   runs:
     using: composite
     steps:
       - uses: actions/setup-node@<sha>
         with:
           node-version: ${{ inputs.node-version }}
       - uses: actions/cache@<sha>
         with:
           path: ~/.npm
           key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
       - run: npm ci
         shell: bash
       - run: npm run build
         shell: bash
   ```

2. **Reusable Workflows** — Share entire pipeline patterns:
   ```yaml
   # .github/workflows/_build-and-push.yml
   name: Build & Push
   on:
     workflow_call:
       inputs:
         image-name:
           required: true
           type: string
         dockerfile-path:
           required: true
           type: string
       secrets:
         registry-token:
           required: true
       outputs:
         image-digest:
           value: ${{ jobs.build.outputs.digest }}

   jobs:
     build:
       outputs:
         digest: ${{ steps.build.outputs.digest }}
       steps:
         - uses: docker/build-push-action@<sha>
           id: build
           with:
             push: true
             tags: ${{ inputs.image-name }}:${{ github.sha }}
   ```

3. **OIDC for Cloud Authentication** — No static credentials:
   ```yaml
   jobs:
     deploy:
       runs-on: ubuntu-latest
       permissions:
         id-token: write    # Required for OIDC
         contents: read
       steps:
         - uses: aws-actions/configure-aws-credentials@<sha>
           with:
             role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsDeploy
             role-session-name: deploy-${{ github.run_id }}
             aws-region: us-east-1
   ```
   AWS IAM trust policy:
   ```json
   {
     "Effect": "Allow",
     "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
     "Action": "sts:AssumeRoleWithWebIdentity",
     "Condition": {
       "StringEquals": {
         "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
         "token.actions.githubusercontent.com:sub": "repo:org/repo:environment:production"
       }
     }
   }
   ```

4. **Self-Hosted Runners** — When GitHub-hosted runners aren't enough:
   ```yaml
   # Label-based routing
   runs-on: [self-hosted, linux, x64, gpu]

   # Ephemeral runners via ARC (Actions Runner Controller)
   runs-on: arc-runner-set
   ```
   Considerations: cache warming, security isolation, scaling policies, cost monitoring.

5. **Environment Protection Rules**:
   ```yaml
   deploy-prod:
     environment:
       name: production
       url: https://api.example.com  # Displayed in PR
     # Protection rules (configured in repo Settings → Environments):
     # - Required reviewers: @team-sre, @team-security
     # - Wait timer: 0 min (immediate) or 30 min (cooling period)
     # - Deployment branches: main only
     # - Secrets scoped to this environment
   ```

### Phase 3 (~20 min): Build Optimization

1. **Dependency Caching — Intelligent Keys**:
   ```yaml
   # ✅ Good — cache by lockfile hash
   - uses: actions/cache@<sha>
     with:
       path: |
         ~/.npm
         ~/.cache/pip
         ~/.gradle/caches
       key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt', '**/gradle.lockfile') }}
       restore-keys: |
         ${{ runner.os }}-deps-

   # ❌ Bad — cache by branch name (busts constantly)
   key: ${{ runner.os }}-deps-${{ github.ref }}
   ```

2. **Docker Layer Caching with BuildKit**:
   ```yaml
   - uses: docker/setup-buildx-action@<sha>
   - uses: docker/build-push-action@<sha>
     with:
       context: .
       cache-from: type=gha        # GitHub Actions cache backend
       cache-to: type=gha,mode=max # Export all layers to cache
       build-args: |
         BUILDKIT_INLINE_CACHE=1
   ```

3. **Test Sharding** — Split test suite across parallel jobs:
   ```yaml
   test:
     strategy:
       matrix:
         shard: [1, 2, 3, 4]
     steps:
       - run: npx jest --shard=${{ matrix.shard }}/${{ strategy.job-total }}
       # Or: pytest --splits 4 --group ${{ matrix.shard }}
   ```

4. **Path Filtering** — Skip irrelevant workflows:
   ```yaml
   on:
     pull_request:
       paths-ignore:
         - 'docs/**'
         - '**.md'
         - '.github/**'
   # Or use dorny/paths-filter for complex conditions:
   - uses: dorny/paths-filter@<sha>
     id: changes
     with:
       filters: |
         frontend: ['frontend/**']
         backend: ['backend/**', 'api/**']
   - if: steps.changes.outputs.frontend == 'true'
     run: cd frontend && npm test
   ```

5. **Incremental Builds** — Rebuild only what changed:
   - **Nx/Turborepo** for monorepos: `npx nx affected:build --base=origin/main`
   - **Bazel** remote caching: `bazel build //... --remote_cache=...`
   - **Gradle build cache**: `org.gradle.caching=true`

### Phase 4 (~15 min): Quality Gates

1. **Quality Gate Matrix**:

   | Gate | Tool | Threshold | Stage | Action on Failure |
   |---|---|---|---|---|
   | Linting | ESLint, Ruff, golangci-lint | 0 warnings (treat warnings as errors) | Pre-build | Block merge |
   | Unit test coverage | Jest, pytest-cov, JaCoCo | ≥ 80% line, ≥ 70% branch | Post-build | Warn; block if < 60% |
   | SAST | SonarQube, CodeQL, Semgrep | Quality Gate: no new bugs, vulnerabilities, code smells | Post-build | Block merge |
   | SCA / Dependencies | Dependabot, Snyk, OWASP | 0 critical, < 3 high | Weekly cron + PR | Auto-PR for fixes |
   | Container scan | Trivy, Grype, Snyk | 0 critical, < 5 high | Pre-deploy | Block deploy |
   | Bundle size | bundlesize, Lighthouse | JS < 200KB gzipped, CSS < 50KB | Post-build | Block merge |

2. **SonarQube Quality Gate Integration**:
   ```yaml
   - uses: SonarSource/sonarqube-scan-action@<sha>
     env:
       SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
   - uses: SonarSource/sonarqube-quality-gate-action@<sha>
     timeout-minutes: 5
     env:
       SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
   ```

3. **Lighthouse CI for Frontend Quality**:
   ```yaml
   - uses: treosh/lighthouse-ci-action@<sha>
     with:
       urls: |
         https://staging.example.com
         https://staging.example.com/pricing
       budgetPath: .github/lighthouse/budget.json
       uploadArtifacts: true
   ```

4. **CVE Severity Decision Tree**:
   ```
   Critical CVE with known exploit?
   ├─ YES → Block deploy immediately. Create SEV2 incident.
   ├─ Critical CVE, no known exploit, fix available
   │   └─ Block deploy. Patch within 24h.
   ├─ High CVE
   │   └─ Block deploy if > 5. Auto-create ticket with SLA.
   └─ Medium/Low
       └─ Ticket created. Deploy allowed.
   ```

### Phase 5 (~25 min): Deployment Strategies

1. **Strategy Selection Matrix**:

   | Strategy | Downtime | Rollback Speed | Resource Overhead | Best For |
   |---|---|---|---|---|
   | **Rolling** | None | Slow (wait for new pods) | None (in-place) | Stateless services, Kubernetes |
   | **Blue-Green** | None | Instant (flip LB) | 2× (duplicate env) | Stateful apps, DB migrations |
   | **Canary** | None | Fast (adjust weight) | 1.1-1.3× | High-traffic, risk-averse orgs |
   | **Feature Flagged** | None | Instant (flip flag) | None | CD teams, kill switches |

2. **Kubernetes Rolling Update**:
   ```yaml
   spec:
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxSurge: 25%        # Extra pods during rollout
         maxUnavailable: 25%  # Max pods unavailable
     minReadySeconds: 10      # Wait before marking ready
   ```

3. **Blue-Green via Service Selector Swap**:
   ```yaml
   # Step 1: Deploy "green" with label version: v2
   # Step 2: Smoke test green
   # Step 3: Swap service selector
   apiVersion: v1
   kind: Service
   spec:
     selector:
       app: myapp
       version: v2  # Flipped from v1 → v2
   # Step 4: Keep v1 pods for 24h for fast rollback
   ```

4. **Canary via Istio VirtualService** (see DevOps Engineer skill, Phase 5)

5. **Feature Flag Integration**:
   ```yaml
   - name: Deploy with feature flag OFF
     run: |
       helm upgrade myapp ./chart \
         --set feature.new_checkout.enabled=false
   - name: Enable for 10% of users
     run: |
       flagsmith set-flag new_checkout --environment=production --enabled --percentage=10
   - name: Monitor error rate and latency for 10 min
   - name: Ramp to 100%
     run: |
       flagsmith set-flag new_checkout --environment=production --enabled --percentage=100
   ```

### Phase 6 (~25 min): Pipeline Security

1. **SLSA Levels**:
   | Level | Requirements | Implementation |
   |---|---|---|
   | **Level 1** | Provenance generated, build scripted | GitHub Actions + SLSA generator |
   | **Level 2** | Version control + hosted build service | GitHub Actions on GitHub.com |
   | **Level 3** | Isolated, ephemeral, non-falsifiable | Self-hosted runner isolation + hardened build |

2. **SLSA Provenance Generation**:
   ```yaml
   - uses: slsa-framework/slsa-github-generator/.github/workflows/builder_docker-based.yml@<sha>
     with:
       builder-image: docker.io/library/alpine:latest
   ```

3. **SBOM Generation**:
   ```yaml
   - uses: anchore/sbom-action@<sha>
     with:
       format: spdx-json
       output-file: sbom.spdx.json
   - uses: actions/upload-artifact@<sha>
     with:
       name: sbom
       path: sbom.spdx.json
   ```

4. **Signed Commits Verification**:
   ```yaml
   # Enforce in branch protection: "Require signed commits"
   # Verify in pipeline:
   - name: Verify commit signature
     run: |
       git verify-commit HEAD
       # Or: gh api repos/${{ github.repository }}/commits/${{ github.sha }}/check-runs
   ```

5. **Pipeline Isolation** — Separate build vs deploy permissions:
   ```yaml
   # Build workflow: minimal permissions
   permissions:
     contents: read
     id-token: write  # Only if needed for OIDC

   # Deploy workflow: elevated permissions
   permissions:
     contents: read
     id-token: write
     deployments: write
   ```

### Phase 7 (~25 min): Release Management

1. **Semantic Release Automation**:
   ```yaml
   - uses: cycjimmy/semantic-release-action@<sha>
     with:
       semantic_version: 23
     env:
       GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
   # Requires conventional commits:
   # feat: add feature → minor bump
   # fix: bug fix → patch bump
   # feat!: breaking change OR BREAKING CHANGE: → major bump
   ```

2. **Conventional Commits Enforcement**:
   ```yaml
   - uses: wagoid/commitlint-github-action@<sha>
     with:
       configFile: .commitlintrc.yml
   ```

3. **Changelog Automation**:
   ```yaml
   - uses: release-drafter/release-drafter@<sha>
     with:
       config-name: release-drafter.yml
   ```

4. **Release Approval Workflow**:
   ```yaml
   # Production release requires manual approval
   release-prod:
     needs: [deploy-staging, integration-tests]
     environment: production
     steps:
       - name: Create Release
         run: |
           gh release create v${{ needs.semantic-release.outputs.version }} \
             --title "Release v${{ needs.semantic-release.outputs.version }}" \
             --notes-file CHANGELOG.md
   ```

### Phase 8 (~30 min): Pipeline Monitoring & DORA Metrics

1. **DORA Metrics Dashboard**:

   | Metric | Elite | High | Medium | Low |
   |---|---|---|---|---|
   | Deployment Frequency | On demand (multiple/day) | Once/day - once/week | Once/week - once/month | < Once/month |
   | Lead Time for Changes | < 1 hour | 1 day - 1 week | 1 week - 1 month | > 1 month |
   | MTTR (Mean Time to Restore) | < 1 hour | < 1 day | < 1 week | > 1 week |
   | Change Failure Rate | < 5% | 5-10% | 10-15% | > 15% |

2. **Pipeline Duration Trending**:
   ```yaml
   # Capture pipeline metrics
   - name: Record pipeline duration
     run: |
       DURATION=$(( ${{ job.steps.final-step.outputs.time }} - ${{ github.run_started_at }} ))
       # Send to Datadog/CloudWatch/Prometheus pushgateway
       curl -X POST https://api.datadoghq.com/api/v1/series \
         -H "DD-API-KEY: ${{ secrets.DD_API_KEY }}" \
         -d '{"series":[{"metric":"cicd.pipeline.duration","points":[[$TIMESTAMP,$DURATION]],"tags":["repo:${{ github.repository }}","workflow:${{ github.workflow }}"]}]}'
   ```

3. **Flaky Test Tracking**:
   ```yaml
   # Rerun failed tests once; if they pass on retry, mark as flaky
   - run: npx jest || npx jest --onlyFailures
     continue-on-error: true
   - name: Report flaky tests
     if: steps.retry.outcome == 'success'
     run: |
       # Capture flaky test names, post to flaky test dashboard
       cat junit.xml | grep '<failure' | notify-flaky-tracker
   ```


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | devops-engineer | Infrastructure and deployment target configuration |
| **This** | ci-cd-builder | Automated pipeline with quality gates and deployment strategy |
| **After** | release-manager | Pipeline triggers release with go/no-go gates |

Common chains:
- **Chain**: devops-engineer → ci-cd-builder → release-manager — Infrastructure is provisioned; pipeline builds and tests; release manager coordinates production rollout
- **Chain**: backend-developer → ci-cd-builder → docker-kubernetes — Code is built and tested in CI; container image is built and pushed to registry

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `pipeline-design` | Architecting CI/CD pipelines for GitHub Actions, GitLab CI, Jenkins, or CircleCI |
| `build-optimization` | Speeding up slow builds with caching, parallelism, and incremental compilation |
| `deployment-strategy` | Designing safe release patterns: rolling, blue-green, canary, feature-flagged deploys |
| `quality-gates` | Pre-deploy verification with SonarQube, coverage thresholds, security scans, and Lighthouse |
| `environment-management` | Managing dev/staging/prod with ephemeral per-PR environments and promotion flows |
| `release-management` | Versioning, semantic release, conventional commits, and automated changelog generation |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `backend-developer` | Build commands, test runners, artifact paths, environment variables | Before designing build stages or configuring test integration |
| `devops-engineer` | Terraform modules, infrastructure deployment specs, environment promotion workflows | Before designing deploy stages or environment management |
| `qa-engineer` | Test parallelization strategy, coverage thresholds, quality gate criteria | Before configuring test stages or quality gates |
| `security-engineer` | OIDC setup for cloud auth, secret injection patterns, signed commit verification | Before integrating secrets or cloud authentication into pipelines |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `devops-engineer` | CI/CD pipeline for automated deploy, container registry, environment configs | Infrastructure changes can't ship — velocity zero |
| `release-manager` | Build artifacts, deployment pipeline, quality gate results | Release train stalls — no artifacts to promote |
| `qa-engineer` | Test integration stages, coverage reports, flaky test quarantine | QA can't validate builds — quality gates block everything |
| `docker-kubernetes` | Image build pipeline, registry integration, image signing | Containers can't be built or scanned — deploy blocked |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Pin actions by SHA digest, never by tag** — `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2`. Tags can be force-pushed.
- **Separate build and deploy workflows** — Build (read-only) runs on PR. Deploy (write) runs on merge to main. Different IAM roles, different risk profiles.
- **Artifact promotion: build once, deploy many** — Never rebuild binaries/images between environments. Immutable artifacts with SHA-tagged images.
- **Concurrency groups prevent race conditions** — `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }`. Saves CI minutes and prevents stale deploys.
- **Secrets via environments + OIDC, never hardcoded** — Each environment has its own secrets. CI roles use OIDC with audience + subject restrictions. Rotate any static tokens on schedule.
- **Warm caches on schedule** — `on: schedule: cron: '0 */6 * * *'` runs dependency install to keep cache fresh for PR workflows.
- **Validate locally before pushing** — `act` for GitHub Actions, `gitlab-ci-local` for GitLab CI. Catch syntax errors before CI runtime.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: CI/CD = `git push` to Vercel/Netlify/Railway. No pipeline definition needed. Deploy on push to main. Rollback = `git revert` + push.
- **What to skip**: Custom CI pipeline. Test stages. Build caching. Environment promotion. Secrets management. Preview deployments. Artifact management.
- **Coordination**: You push, platform deploys. Done.

### Small Team (2-10 people, 100-10K users)
- **What changes**: GitHub Actions or GitLab CI. Stages: lint → test → build → deploy. Caching for dependencies. Environment separation (staging + production). Secrets via CI secrets manager. Preview deployments per PR. Notifications on failure.
- **What to skip**: Matrix builds. Blue-green/canary deployments. Progressive delivery. SLSA provenance. SBOM generation. Multi-cloud pipelines.
- **Coordination**: Pipeline changes reviewed in PR. Deploy announcements in Slack. Weekly pipeline health check.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full pipeline: lint → test → build → scan → deploy → verify. Matrix builds for multi-platform. Blue-green or canary deployments. Security scanning (SAST + dependency + container). Path filters in monorepo. Environment promotion (dev → staging → prod). Artifact promotion (build once, deploy many). Concurrency groups.
- **What to skip**: Multi-cloud pipelines. Progressive delivery (canary analysis automated). Full SLSA Level 3. SBOM for every build.
- **Coordination**: Pipeline team or DevOps owner. Bi-weekly pipeline review. Deploy calendar for coordinated releases.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Pipeline platform team. Self-service pipeline templates. Multi-cloud deployment pipelines. Progressive delivery with automated rollback. Full security gates (SAST + DAST + SCA + IAC scan + image scan). SLSA Level 3 provenance. SBOM generation. Compliance gates (SOC 2, PCI DSS). Pipeline metrics (DORA: deployment frequency, lead time, change failure rate, MTTR). Pipeline cost optimization.
- **What's full production**: Internal developer platform. Pipeline catalog. Automated canary analysis. Deployment analytics. Pipeline as product.
- **Coordination**: Pipeline platform team weekly. Monthly pipeline review board. Quarterly DORA metrics review.

### Transition Triggers
- **Solo → Small**: Second developer. Need automated tests before deploy.
- **Small → Medium**: 3+ teams. Deploy coordination overhead. First security incident from deployed code.
- **Medium → Enterprise**: 10+ teams. Compliance requirements. >50 deploys/day.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## What Good Looks Like

> Pipelines run reliably on every commit, complete in under fifteen minutes, and provide clear, actionable feedback. Builds are reproducible and hermetic — the same commit always produces the same artifact. Artifacts are immutable and promoted through environments with zero manual steps. The pipeline enforces quality gates at every stage and blocks deployment on failure. Developers trust the pipeline implicitly: a green build means "ready to ship," and a red build tells them exactly what to fix, where, and why.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
### Pipeline Architecture
- [ ] **[S1]**  Pipeline stages defined: lint → test → build → scan → deploy → verify
- [ ] **[S2]**  Fan-in/fan-out used for parallel execution where beneficial
- [ ] **[S3]**  Path filters skip irrelevant workflows in monorepo
- [ ] **[S4]**  Concurrency groups cancel redundant PR runs

### Security & Secrets
- [ ] **[S5]**  All third-party actions pinned to full-length commit SHA
- [ ] **[S6]**  OIDC federation for cloud authentication — no static credentials
- [ ] **[S7]**  Environment protection rules on production: required reviewers + restricted branches
- [ ] **[S8]**  Secrets scoped per environment; never shared across environments
- [ ] **[S9]**  SLSA provenance generated for all releases (Level 3 target)
- [ ] **[S10]**  SBOM (SPDX/CycloneDX) generated and attached to releases
- [ ] **[S11]**  Signed commits enforced via branch protection rules

### Build Optimization
- [ ] **[S12]**  Dependency caching with lockfile-hash keys; `restore-keys` fallback configured
- [ ] **[S13]**  Docker BuildKit with GitHub Actions cache backend (`type=gha`)
- [ ] **[S14]**  Test sharding for suites > 5 minutes
- [ ] **[S15]**  Self-hosted runners or larger runners for resource-heavy builds
- [ ] **[S16]**  Cache warming scheduled to keep caches fresh

### Quality Gates
- [ ] **[S17]**  SonarQube quality gate: no new bugs/vulnerabilities/smells
- [ ] **[S18]**  Code coverage ≥ 80% (enforced, not advisory)
- [ ] **[S19]**  Container CVE scan: 0 critical, < 5 high (block deploy on critical)
- [ ] **[S20]**  Lighthouse scores/Bundle size budget enforced for frontend

### Deployment
- [ ] **[S21]**  Artifacts built once, promoted across environments (never rebuilt)
- [ ] **[S22]**  Immutable image tags (SHA digest, not `:latest`)
- [ ] **[S23]**  OCI annotations: commit SHA, build timestamp, pipeline URL
- [ ] **[S24]**  Automated rollback tested: health check failure → revert to previous version
- [ ] **[S25]**  Deployment status visible in PR via Checks API

### Release Management
- [ ] **[S26]**  Semantic release configured with conventional commits enforcement
- [ ] **[S27]**  Automated changelog generation from conventional commit messages
- [ ] **[S28]**  Production release requires manual approval in deployment environment
- [ ] **[S29]**  Image retention policy: delete stale feature-branch images after N days

### Monitoring
- [ ] **[S30]**  DORA metrics tracked: deploy frequency, lead time, MTTR, change failure rate
- [ ] **[S31]**  Pipeline duration trending dashboard with alert on degradation
- [ ] **[S32]**  Flaky test detection and reporting (separate flaky from actual failures)
- [ ] **[S33]**  CI minutes/quota monitoring with alert before exhaustion

## References
<!-- QUICK: 30s -- links to deeper reading -->
- GitHub Actions Security Hardening: https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- GitHub Actions Reusable Workflows: https://docs.github.com/en/actions/using-workflows/reusing-workflows
- SLSA Framework: https://slsa.dev/spec/v1.0/levels
- Sigstore Cosign: https://docs.sigstore.dev/cosign/overview/
- Anchore SBOM Action: https://github.com/anchore/sbom-action
- Semantic Release: https://semantic-release.gitbook.io/semantic-release
- DORA Metrics: https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance
- Docker BuildKit Cache: https://docs.docker.com/build/cache/backends/gha/
- Trivy Container Scanning: https://github.com/aquasecurity/trivy
