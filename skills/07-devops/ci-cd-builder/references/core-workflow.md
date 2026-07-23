# Core Workflow — Full Implementation

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
