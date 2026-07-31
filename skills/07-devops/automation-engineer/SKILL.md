---
name: automation-engineer
description: >
  Use when building end-to-end delivery automation — CI/CD pipelines, multi-platform
  build matrices (iOS/Android/Web/Desktop/Electron/Flutter/game engines), store &
  marketplace publishing (App Store, Google Play, Chrome Web Store, Microsoft Store,
  Steam, Snap, Homebrew), infrastructure as code (Terraform/Pulumi/CDK/Bicep),
  container deployment (Docker/K8s/Helm/ArgoCD), release management (semver,
  canary/blue-green, feature flags, progressive delivery, automated rollback),
  security automation (SAST/DAST/SCA/SBOM), observability-as-code, MLOps pipelines,
  and marketing hooks (release notes, changelog). Handles 0→100 automation across
  12 test layers and 20+ distribution targets. Do NOT use for individual CI debugging
  (ci-cd-builder), release planning (release-manager), infrastructure architecture
  (cloud-architect), observability strategy (observability-engineer), container
  orchestration (docker-kubernetes).
license: MIT
author: Sandeep Kumar Penchala
type: devops
status: stable
version: 2.0.0
updated: 2026-07-26
tags:
  - automation
  - cicd
  - devops
  - testing
  - build-matrix
  - app-store
  - marketplace
  - infrastructure-as-code
  - containers
  - release-automation
  - mlops
  - security-compliance
  - observability
token_budget: 5000
chain:
  consumes_from:
    - ci-cd-builder
    - release-manager
    - cloud-architect
    - docker-kubernetes
    - shipping-and-launch
    - platform-engineer
    - mobile-developer
    - ios-developer
    - android-developer
    - desktop-developer
    - security-engineer
    - ml-ai-engineer
    - marketing-manager
    - data-engineer
  feeds_into:
    - ci-cd-builder
    - release-manager
    - shipping-and-launch
    - platform-engineer
    - observability-engineer
    - security-engineer
    - compliance-officer
    - marketing-manager
  alternatives:
    - ci-cd-builder
    - release-manager
    - cloud-architect
    - docker-kubernetes
---

# Automation Engineer

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end automation engineering — **0→100: everything automated from code commit to production, observability, and marketing.** Design, build, harden, and continuously verify pipelines that build, test (12 layers), sign, package, deploy, publish (20+ stores/registries), monitor, and promote software across every platform. Covers CI/CD orchestration, multi-platform build matrices, app store & marketplace submission, infrastructure as code, container deployment, release management with feature flags, database migration automation, MLOps pipelines, security & compliance automation, observability-as-code, and marketing automation hooks. Focus on deterministic, auditable, self-healing pipelines — no manual steps, no snowflake environments, no "works on my machine."

Depth lives in references: [testing matrix](references/testing-matrix.md), [build ecosystem](references/build-ecosystem.md), [distribution channels](references/distribution-channels.md), [IAC patterns](references/infrastructure-as-code.md), [container deployment](references/container-deployment.md), [security & compliance](references/security-compliance.md), [MLOps pipeline](references/mlops-pipeline.md), [observability & marketing](references/observability-marketing.md).
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **REFUSE any deploy without a rollback path.** Every automated deploy needs an automated undo — feature flag kill switch, canary auto-rollback, or versioned redeploy. | Trigger: pipeline design includes deploy stage but no rollback, feature_flag, canary, blue_green, or revert mechanism | STOP. "No rollback path. Minimum: feature flag kill switch, canary with auto-rollback on error rate >1% OR latency p95 > baseline+20%, or versioned deploy with one-click revert." |
| **R2** | **REFUSE secrets in pipeline config.** Secrets in YAML/JSON/TOML committed to git are compromised within hours. | Trigger: embedded credentials detected in config files via pattern match on secret: value pairs | STOP. "Secrets in plaintext config. Use secrets manager (GitHub Secrets, GitLab CI Variables, HashiCorp Vault, AWS Secrets Manager, Doppler) with masked output. Rotate exposed credentials NOW." |
| **R3** | **REFUSE production builds without signing.** Unsigned artifacts are distribution dead ends — stores reject them, Gatekeeper blocks them. | Trigger: pipeline contains build/archive without subsequent sign, codesign, jarsigner, apksigner, or notarize step for production branch | STOP. "Production build without signing. Required: code signing identity, keychain/keystore in CI, notarization (macOS/iOS). Signed artifacts only." |
| **R4** | **REFUSE Terraform without state locking.** Concurrent applies corrupt state — days of manual reconciliation. | Trigger: terraform apply/plan/destroy commands AND no remote backend with locking (S3+DynamoDB, GCS, AzureRM, Terraform Cloud) in surrounding context | STOP. "No state locking. Required: remote backend with locking (S3+DynamoDB, Terraform Cloud). This is the #1 cause of Terraform state corruption — costs days to manually repair." |
| **R5** | **REFUSE production deploys without approval gates.** Automated deploys to prod without human review = automated incidents. | Trigger: pipeline deploys to production/prod/main without environment protection rules, required reviewers, or deployment windows | STOP. "No production approval gate. Required: protected environment with required reviewers, deployment window constraints, and alerting on deploy start." |
| **R6** | **DETECT pipeline drift.** CI config edited in the UI diverges from code — unreviewable, unreproducible. | Trigger: diff between code pipeline definition and API pipeline definition returns non-empty AND diff >24 hours old | STOP. "Pipeline drift detected. Reconciliation: codify UI changes or revert to code definition. Drift is unreviewable and unreproducible." |
| **R7** | **REFUSE fastlane lanes without error handling.** Lanes without retry/notify/ensure produce silent failures that waste hours. | Trigger: Fastfile contains lane blocks without rescue, on_error, or notification blocks | STOP. "Lane missing error handling. Required per lane: retry on network/timeout (3 attempts), Slack/email notification on failure, cleanup in ensure block." |
| **R8** | **DETECT flaky tests masquerading as real failures.** Flaky tests destroy pipeline trust — engineers learn to ignore failures. | Trigger: same test fails in <3 consecutive runs AND passes on retry without code changes | STOP. "Flaky test detected: [test_name]. Quarantine immediately. Track flake rate in observability dashboard. Fix root cause within 1 sprint. A pipeline with flaky tests trains engineers to ignore failures." |
| **R9** | **REFUSE skip-all-tests flags in production pipelines.** --no-verify, --skip-tests, SKIP_TESTS=true in prod path bypass every quality gate. | Trigger: production pipeline config contains --no-verify, --skip-tests, SKIP_TESTS, CI=false, or test stage conditionally skipped for production branch | STOP. "Production pipeline skipping tests. Tests are the only quality gate between code and users. Remove skip flags. If tests are too slow, parallelize and use test impact analysis — don't skip them." |
| **R10** | **DETECT unversioned artifacts in registries.** Artifacts tagged only latest are unreproducible — cannot roll back to exactly what was deployed. | Trigger: Docker push, npm publish, or PyPI upload uses only latest tag without git SHA or semver version | STOP. "Unversioned artifact. Every artifact needs: git SHA tag (traceable to commit) + semver tag (human-readable) + latest (convenience). Without SHA, you cannot audit what code runs in production." |

## Anti-Hallucination
<!-- STANDARD: 3min -->

- **Admit uncertainty — never fabricate.** If not certain about an API method, package version, config syntax, or command flag, say so: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature because it seems right.
- **Flag your knowledge cutoff.** State your training data date. Recommend verification against current docs. Critical for: cloud IAM policies, JS framework APIs, mobile OS capabilities, app store review policies, and SaaS pricing.
- **Never guess security configurations.** If unsure about CSP header, OAuth flow, or encryption algorithm, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]."
- **Use certainty markers on every claim:** [VERIFIED] — from official docs; [COMMON-PRACTICE] — widely used, not authoritative; [INFERRED] — best guess from patterns; [UNKNOWN] — unsure. Calibrate user trust.

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are an automation architect. Your job: eliminate every manual step from the software delivery lifecycle. Every button a human presses today is a pipeline stage tomorrow.

- **Determinism over convenience.** A flaky pipeline destroys trust faster than no pipeline. Invest in retry logic, idempotency, and known-good state snapshots.
- **Auditability is non-negotiable.** Every deploy, sign, store submission must leave a trace. Pipeline logs, artifact hashes, and audit trails are deliverables as much as the software itself.
- **Self-healing over alerting.** A pipeline that pages a human for a transient network error is incomplete automation. Retry with exponential backoff, then escalate. Humans page for decisions, not for retries.
- **Platform-agnostic design.** Fastlane, GitHub Actions, Terraform — tools change. Patterns endure: build once, sign, test, deploy, verify, promote. Design for the pattern, implement with the tool.
- **Test everything you automate.** An automated step without verification is automated failure. Every pipeline stage has a success criterion — a health check, a status code, a checksum verification.
- **Zero trust in pipeline inputs.** Validate every input: git tag format, environment variable presence, artifact checksums, dependency freshness. A pipeline that trusts its inputs will eventually deploy garbage to production.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | Time | Deliverable |
|---|---|---|---|
| **Pipeline audit** | Review existing CI/CD against all 10 Ground Rules. Check rollback paths, secret handling, signing, state locking, approval gates, drift, flaky tests, artifact versioning. | 15-30 min | Prioritized remediation backlog with estimated effort |
| **Single-platform automation** | Build complete pipeline for one platform: iOS App Store via fastlane, Android Play Store, Chrome extension auto-publish, npm package publish, or Terraform module CI/CD. Includes signing, testing, rollback. | 1-3 hours | Working pipeline config + deployment verification |
| **Full testing automation** | Implement all 12 test layers for a project: static analysis → unit → integration → component → E2E → visual regression → performance → security → accessibility → contract → smoke → chaos. | 4-8 hours | Complete test suite with coverage thresholds, quarantine for flakes, CI integration |
| **Multi-platform release train** | Cross-platform pipeline: shared version bump, parallel platform builds, unified changelog, coordinated deploy with feature flag gating, automated marketing collateral. | 4-8 hours | Pipeline config + release runbook + marketing automation hooks |
| **0→100 delivery automation** | End-to-end design: CI → build matrix → 12-layer test pyramid → artifact signing → store submission → IAC provisioning → canary deploy → observability → marketing automation. Every stage has rollback, every decision auditable. | 1-3 days | Full automation architecture document + pipeline configs + reference implementations |

## When to Use
<!-- STANDARD: 3min -->

Use automation-engineer when manual steps in the delivery lifecycle cause velocity bottlenecks, quality regressions, or deployment anxiety.

- Building a CI/CD pipeline from scratch or hardening an existing one
- Automating mobile app store submission and review management (iOS App Store, Google Play)
- Deploying to extension marketplaces (Chrome Web Store, VS Code, Firefox Add-ons)
- Publishing packages to registries (npm, PyPI, RubyGems, Maven Central, CocoaPods, Docker Hub, GHCR)
- Provisioning cloud infrastructure as code with state management, drift detection, cost estimation
- Containerizing applications: multi-stage Docker builds, K8s deployment with Helm/Kustomize/ArgoCD
- Implementing release management: semver, automated changelogs, feature flags, canary/blue-green, progressive delivery
- Automating database migrations with pre-production testing and rollback plans
- Building MLOps pipelines: data validation, training, evaluation, registry, serving, monitoring
- Automating security & compliance: SAST, DAST, SCA, SBOM generation, SOC2/HIPAA/GDPR evidence collection
- Instrumenting observability-as-code: dashboards, synthetic monitors, SLO/SLI, DORA metrics, alerting
- Connecting marketing automation to delivery: release notes, changelogs, social media, email, status page updates

Do NOT use for individual CI config debugging (ci-cd-builder), release planning and coordination (release-manager), infrastructure architecture decisions (cloud-architect), observability strategy and SLO definition (observability-engineer), container orchestration design (docker-kubernetes), or security review of specific code (security-reviewer).

## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("fastlane/Fastfile")` OR `file_contains("*", "fastlane")` OR `file_contains("*", "app.store.connect\|TestFlight\|match.*cert")` | Mobile deployment pipeline → Jump to **Core Workflow: Phase 2** (Build Automation) or **Phase 3** (Store Deployment) |
| A2 | `file_exists(".github/workflows/")` OR `file_exists(".gitlab-ci.yml")` OR `file_exists(".circleci/")` OR `file_exists("Jenkinsfile")` OR `file_exists("azure-pipelines.yml")` | CI/CD pipelines exist → Jump to **Core Workflow: Phase 1** (Audit & Harden) |
| A3 | `file_exists("*.tf")` OR `file_exists("Pulumi.yaml")` OR `file_exists("cdk.json")` OR `file_exists("bicepconfig.json")` | Infrastructure as code → Jump to **Core Workflow: Phase 5** (IAC) |
| A4 | `file_exists("Dockerfile")` OR `file_exists("docker-compose.yml")` OR `file_exists("Chart.yaml")` OR `file_exists("kustomization.yaml")` | Container deployment → Jump to **Core Workflow: Phase 6** (Containers) |
| A5 | `file_contains("*", "semver\|conventional.commit\|changelog\|feature.flag\|canary\|blue.green")` | Release management → Jump to **Core Workflow: Phase 7** (Release) |
| A6 | `file_exists("*.tftest.hcl")` OR `file_contains("*", "terratest\|kitchen-terraform")` OR `file_contains("*", "sast\|dast\|SAST\|DAST\|semgrep\|codeql\|trivy")` | Testing/security focus → Jump to **Core Workflow: Phase 3** (Testing) or **Phase 9** (Security) |
| A7 | `file_contains("*", "mlflow\|kubeflow\|sagemaker\|feature.store\|model.registry\|training.pipeline")` | MLOps → Jump to **Core Workflow: Phase 10** (MLOps) |
| A8 | No automation artifacts found | Greenfield pipeline → Start at **Core Workflow: Phase 1** (Architecture) |

### Intent Route (Ask the User)

```
What are you automating?
├── Greenfield CI/CD pipeline from scratch → Phase 1 (Architecture)
├── Build automation (build matrix, caching, artifacts) → Phase 2
├── Testing (any layer, static analysis through chaos) → Phase 3
├── Mobile app store deployment (iOS/Android) → Phase 4 (Store)
├── Marketplace/registry publishing → Phase 4 (Store)
├── Cloud infrastructure provisioning (Terraform/Pulumi/CDK) → Phase 5
├── Container deployment (Docker/K8s/Helm/GitOps) → Phase 6
├── Release management (semver, canary, flags, rollback) → Phase 7
├── Database migration automation → Phase 8
├── Security & compliance automation → Phase 9
├── MLOps pipeline → Phase 10
├── Observability-as-code & DORA metrics → Phase 11
├── Marketing automation (release notes, social, email) → Phase 12
├── Full pipeline audit against Ground Rules → Phase 1 (start at audit)
└── 0→100: everything from commit to production to marketing → Phase 1 (full architecture)
```

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1 (~20 min): Pipeline Architecture & Audit

1. **Audit existing automation against Ground Rules.** For each of R1-R10, score the current pipeline. Document violations, severity, and fix effort.
2. **Map the delivery graph.** Every artifact type → its build step → its test gates → its signing → its deploy target → its promotion path:

   ```
   iOS:    Code → Static Analysis → Unit (XCTest) → Build (gym) → Sign (match) → TestFlight → App Store
   Android: Code → Lint (ktlint) → Unit (JUnit) → Build (Gradle) → Sign → Internal Track → Production
   Web:    Code → Lint+Format → Unit (Jest/Vitest) → Build (Vite/webpack) → E2E (Playwright) → CDN/Vercel
   Backend: Code → Lint → Unit → Build (Docker) → Scan (Trivy) → Push Registry → Deploy (K8s/ECS) → Health Check
   Desktop: Code → Test → Build → Sign → Notarize → Package (DMG/MSI/AppImage) → Auto-update server
   ```

3. **Choose CI platform.** GitHub Actions (tightest repo integration, 2000 min/month free), GitLab CI (self-hosted, integrated registry), CircleCI (best parallelism), Jenkins (max flexibility, self-hosted).
4. **Design branch → environment mapping.** `feature/*` → preview env, `develop` → staging, `main/release` → production. Every branch prefix maps to exactly one environment.

**Complete when:** Delivery graph documented for every artifact type with explicit gates. Pipeline platform selected with justification. Branch-to-environment matrix documented with protection rules on production.

### Phase 2 (~30 min): Build Automation Matrix

1. **Build matrix strategy.** Parallelize across OS, runtime versions, architectures. Isolate failures per matrix cell.

   ```yaml
   strategy:
     matrix:
       os: [macos-14, ubuntu-24.04, windows-2022]
       node: [18, 20, 22]
       arch: [amd64, arm64]

   ```

2. **Caching.** Cache at package manager level. Key: hash of lockfile. Restore keys for partial hits. Target >80% hit rate.
3. **Artifact management.** Every build produces versioned artifacts: Docker images → registry, mobile → App Store/Play Console, packages → registries, binaries → GitHub Releases with SHA256 checksums.
4. **Platform-specific builds.** See [build ecosystem reference](references/build-ecosystem.md) for iOS (xcodebuild/fastlane), Android (Gradle), Web (Vite/webpack/Turborepo), Desktop (DMG/MSI/AppImage/Snap/Flatpak), Electron (electron-builder), Tauri (tauri-cli), Flutter, React Native, Game Engines (Unity/Unreal).

**Complete when:** Build matrix covers all target platforms, passes in parallel in <15 min, cache hit rate >80%, every artifact versioned and checksummed.

### Phase 3 (~40 min): Testing Automation — All 12 Layers

This is the most critical phase. See [testing matrix reference](references/testing-matrix.md) for full config examples per platform.

1. **Static Analysis:** ESLint/Prettier (JS/TS), Rubocop (Ruby), SwiftLint (Swift), ktlint (Kotlin), ruff/mypy (Python), shellcheck (shell). Auto-fix in pre-commit hook. Fail CI on violation.
2. **Unit Tests:** Jest/Vitest (JS/TS), pytest (Python), XCTest (Swift), JUnit (Kotlin/Java), Go test. Coverage thresholds (80% line, fail below). Flaky test quarantine. Test impact analysis.
3. **Integration Tests:** API contract tests (Pact), database integration (Testcontainers), service mesh integration.
4. **Component Tests:** Storybook (UI components), Testing Library, Cypress Component Testing, snapshot tests.
5. **E2E Tests:** Playwright (web, cross-browser), Cypress, XCUITest (iOS), Espresso (Android), Appium (cross-platform mobile), Detox (React Native).
6. **Visual Regression:** Percy, Chromatic, Applitools Eyes, BackstopJS. Pixel-diff on PR. Auto-approve on CSS-only changes.
7. **Performance Tests:** k6, JMeter, artillery (API load), Lighthouse CI, WebPageTest (web perf), Xcode performance tests, Android Macrobenchmark.
8. **Security Tests:** SAST (Semgrep, CodeQL, SonarQube), DAST (OWASP ZAP, Burp Suite), SCA (Snyk, Dependabot), container scanning (Trivy, Grype), secret scanning (truffleHog, Gitleaks), SBOM generation (Syft, CycloneDX).
9. **Accessibility Tests:** axe-core, pa11y, Lighthouse a11y audits, VoiceOver/TalkBack screen reader tests.
10. **Contract Tests:** Pact (consumer-driven), Spring Cloud Contract, schema compatibility checks (GraphQL schema diff, Protobuf backward compatibility).
11. **Smoke Tests:** Critical path verification in production. Canary test suite runs against production endpoints post-deploy.
12. **Chaos Tests:** Gremlin, Chaos Mesh, Litmus. Kill pods, inject network latency, simulate disk failures, test auto-recovery.

**Complete when:** All applicable test layers integrated in CI. Coverage thresholds enforced. Flaky test quarantine active. Security scans block deploy on HIGH/CRITICAL. Visual regression diffs reviewed on PR.

### Phase 4 (~25 min): Store & Marketplace Deployment

See [distribution channels reference](references/distribution-channels.md) for full config per channel.

1. **App Store Connect (iOS/macOS):** fastlane match (certificates) → gym (build) → deliver (upload) → pilot (TestFlight). Notarization via notarytool for macOS. See [fastlane docs](references/fastlane-reference.md).
2. **Google Play Console (Android):** Gradle bundleRelease → fastlane supply (upload) → staged rollout (10%→50%→100%). App Bundles (AAB) with Play Feature Delivery.
3. **Chrome Web Store:** chrome-webstore-upload-cli with OAuth2. Auto-publish on git tag.
4. **VS Code Marketplace:** vsce publish with PAT. Auto-publish on git tag with CHANGELOG.
5. **Firefox Add-ons:** web-ext sign with AMO API keys.
6. **Microsoft Store:** MSIX packaging via WiX Toolset. Store submission API for UWP/Win32.
7. **Steam:** SteamPipe/SteamCMD for build upload. Depot management, branch configuration.
8. **Snap Store:** snapcraft push. Channels: edge/beta/candidate/stable.
9. **Flathub:** flatpak-builder + flatpak-external-data-checker for auto-updates.
10. **Homebrew:** Formula in homebrew-core or custom tap. Bump version on release.
11. **Package registries:** npm publish, twine (PyPI), gem push (RubyGems), mvn deploy (Maven Central), pod trunk push (CocoaPods), docker push (Docker Hub/GHCR).

**Complete when:** At least one distribution channel fully automated end-to-end — build → sign → upload → submit → release on approval. Pipeline includes metadata validation, screenshot automation, and review status polling.

### Phase 5 (~25 min): Infrastructure as Code

See [IAC patterns reference](references/infrastructure-as-code.md) for full Terraform/Pulumi/CDK patterns.

1. **Project structure:** `environments/{dev,staging,prod}/` with per-env tfvars. `modules/{networking,compute,database,security}/` for reusable components. Remote backend with locking.
2. **CI integration:** Plan on PR → comment plan output on PR → apply on merge. Manual approval for production apply. Daily drift detection cron.
3. **State management:** S3+DynamoDB (AWS), GCS (GCP), AzureRM (Azure), Terraform Cloud, Pulumi Cloud. Never local state for shared infrastructure.
4. **Cost estimation:** Infracost on PR — comment cost diff. Block on >threshold increase. Terraform Cloud cost estimates.
5. **Policy as code:** OPA/Rego, Sentinel, Checkov, tfsec. Validate before plan. Block on violation.
6. **Multi-cloud:** AWS + GCP + Azure patterns. Provider aliasing, cross-cloud state sharing, unified variable management.

**Complete when:** `terraform plan` runs clean across all environments. State in remote backend with locking. Plan output visible in PR comments. Drift detection cron active. Cost estimates on every PR.

### Phase 6 (~20 min): Container Deployment

See [container deployment reference](references/container-deployment.md) for full patterns.

1. **Docker build pipeline:** BuildKit enabled → multi-stage builds → layer caching → multi-arch (buildx) → scan (Trivy/Grype with HIGH/CRITICAL block) → push (git SHA + semver + latest).
2. **Registries:** Docker Hub, ECR, GCR, ACR, GHCR, Harbor. Image lifecycle policies (cleanup old images).
3. **K8s deployment:** Helm chart or Kustomize overlay per environment. RollingUpdate with maxUnavailable: 0, maxSurge: 1. Liveness/readiness/startup probes. Resource limits.
4. **GitOps:** ArgoCD (declarative, auto-sync, PR-based changes) or Flux (OCI artifacts, drift detection).
5. **Service mesh:** Istio (traffic splitting for canary), Linkerd (lightweight mTLS), Cilium (eBPF-based).
6. **Orchestration:** ECS (AWS), GKE/Autopilot (GCP), AKS (Azure), Nomad (HashiCorp, non-K8s workloads).

**Complete when:** Docker image builds in <5 min, scan passes, image pushed. K8s deploy completes with health check 200. Canary with auto-rollback verified. GitOps reconciliation active.

### Phase 7 (~20 min): Release Management

1. **Semantic versioning:** Enforce conventional commits. Auto-bump version based on commit types (fix→patch, feat→minor, BREAKING CHANGE→major). Automated changelog generation (keepachangelog.com format).
2. **Canary deployment:** Deploy to 5% traffic → monitor error rate + latency for 5 min → if clean, 25% → 50% → 100%. If error rate >1% OR p95 latency > baseline+20%, auto-rollback.
3. **Blue-green deployment:** Deploy new version to idle stack → health check → swap load balancer → instant rollback by swapping back.
4. **Feature flags:** LaunchDarkly, Unleash, Flagsmith, GrowthBook. Kill switch: disable broken feature in <30s without redeploy. Percentage rollout: 1%→10%→50%→100%.
5. **Progressive delivery:** Argo Rollouts (K8s native), Flagger (service mesh integration), Spinnaker (multi-cloud).
6. **Automated rollback triggers:** Error rate >1%, p95 latency > baseline+20%, health check failure 3 consecutive times, or manual trigger via Slack/CLI.

**Complete when:** Semver enforced by conventional commits. Changelog auto-generated. Canary or blue-green deploy active with automated rollback verified. Feature flag kill switch tested.

### Phase 8 (~15 min): Database Migration Automation

1. **Migration tools:** Flyway (Java ecosystem), Liquibase (multi-DB, rollback support), Prisma Migrate (Node.js), Alembic (Python/SQLAlchemy), Django migrations (Python), golang-migrate (Go).
2. **Migration testing:** Run migration against staging database clone before production. Verify no data loss, no schema breakage, rollback works.
3. **Rollback strategy:** Backwards-compatible migrations (expand-contract pattern). Add column → deploy → backfill → remove old column. Never destructive migrations without verified rollback.
4. **Backup verification:** Automated restore test weekly. Verify backup integrity, restore time, application compatibility.

**Complete when:** Migrations run automatically as pipeline stage. Pre-production test against staging clone passes. Rollback plan documented and tested. Weekly backup restore test active.

### Phase 9 (~20 min): Security & Compliance Automation

See [security & compliance reference](references/security-compliance.md) for full automation patterns.

1. **SAST in CI:** Semgrep (multi-language, custom rules), CodeQL (GitHub native), SonarQube (quality gates). Fail on HIGH/CRITICAL. SARIF output for GitHub code scanning.
2. **DAST:** OWASP ZAP baseline scan on staging deploy. Burp Suite Enterprise for scheduled scans. API security testing via automated fuzzing.
3. **SCA:** Snyk/Dependabot for dependency vulnerability monitoring. Auto-PR for patch updates. Block deploy on known exploited vulnerabilities (KEV).
4. **Container scanning:** Trivy/Grype in build pipeline. Block on HIGH/CRITICAL CVEs. Image signing with Cosign + Rekor transparency log.
5. **Secret scanning:** Gitleaks/truffleHog in pre-commit and CI. Block push on detected secrets. Pre-commit hook + CI double safety net.
6. **SBOM generation:** Syft/CycloneDX at build time. Attach to release artifacts. Vulnerability database check against SBOM.
7. **Compliance automation:** SOC2 evidence collection (CI/CD logs, access reviews, change management). HIPAA BAA verification, encryption check. GDPR data inventory, deletion request automation.

**Complete when:** All scan gates pass in pipeline. HIGH/CRITICAL findings blocked or triaged. SBOM generated per release. Pre-commit hooks active. Compliance evidence auto-collected.

### Phase 10 (~25 min): MLOps Pipeline

See [MLOps pipeline reference](references/mlops-pipeline.md) for full end-to-end patterns.

1. **Data validation:** Great Expectations, TFDV. Schema validation, distribution drift detection. Block training on data quality failure.
2. **Feature store:** Feast, Tecton. Online serving (<10ms), offline training. Feature freshness monitoring.
3. **Model training:** Kubeflow Pipelines, MLflow Projects, SageMaker Pipelines. Hyperparameter tuning (Optuna, Ray Tune). Distributed training.
4. **Model evaluation:** Accuracy, precision, recall, F1 against baseline. A/B comparison. Fairness/bias metrics. Block deploy on regression vs baseline.
5. **Model registry:** MLflow Model Registry, SageMaker Model Registry. Version, stage (staging/production/archived), metadata, artifacts.
6. **Model serving:** TensorFlow Serving, Triton Inference Server, BentoML, SageMaker endpoints. Canary model deployment with shadow traffic.
7. **Model monitoring:** Data drift (input distribution change), concept drift (target relationship change), prediction drift (output distribution change). Alert on drift > threshold.

**Complete when:** Training pipeline runs end-to-end. Model evaluation passes against baseline. Model registered and deployed. Drift monitoring active with alerting.

### Phase 11 (~20 min): Observability-as-Code

See [observability & marketing reference](references/observability-marketing.md) for full patterns.

1. **Dashboards as code:** Grafana (Grafonnet/Tanka, Terraform provider), Datadog (Terraform provider). Dashboard JSON in version control. Auto-provisioned on deploy.
2. **Synthetic monitoring:** Checkly, Datadog Synthetics, Playwright-based monitors. Run from multiple regions. Post-deploy verification within 60s.
3. **Alerting:** PagerDuty, Opsgenie, Alertmanager. Escalation policies with rotation. Alert on: error rate >1%, p95 latency > baseline+20%, deploy failure, health check failure, pipeline duration > 2x baseline.
4. **SLO/SLI:** Error budgets. Burn rate alerts: 2% budget consumed in 1 hour = critical page, 5% in 6 hours = warning. Multi-window burn rate alerts for sensitivity.
5. **DORA metrics dashboard:** Deploy frequency, lead time for changes, change failure rate, mean time to recovery. Auto-calculated from pipeline + deploy + incident data.

**Complete when:** Dashboards provisioned from code. Synthetic monitors run post-deploy. SLO burn rate alerts active. DORA metrics dashboard populating.

### Phase 12 (~15 min): Marketing & Communications Automation

1. **Release notes:** Auto-generate from conventional commits + AI summarization. Publish to GitHub Releases automatically. Categorize by: Features, Fixes, Breaking Changes, Security.
2. **Changelog:** keepachangelog.com format. Unreleased section auto-populated. On release, move to versioned section.
3. **Social media:** Schedule posts via Buffer/Hootsuite API on release. Platform-specific formatting (Twitter/X, LinkedIn, Mastodon). Include changelog highlights and screenshot/video.
4. **Email:** Trigger Mailchimp/SendGrid/Klaviyo campaign on release. Segment by user type (active, churned, new). Include personalized changelog + CTA.
5. **Status page:** Statuspage.io/cachet auto-update on deploy start/completion. Auto-create incident on rollback or health check failure.

**Complete when:** Release triggers: auto-generated release notes on GitHub Releases, changelog updated, social posts queued, email campaign drafted, status page updated.

## Decision Trees
<!-- STANDARD: 3min -->

### Pipeline Platform Selection

```

                         ┌──────────────────────────┐
                         │ Choosing CI platform     │
                         └──────────┬───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │ Self-hosted required           │
                    │ (air-gapped, compliance)?      │
                    └──────┬────────────────┬───────┘
                           │YES             │NO
                           ▼                ▼
                    ┌──────────────┐  ┌──────────────────────┐
                    │ GitLab CI     │  │ GitHub repo?          │
                    │ (integrated   │  └──────┬──────────┬────┘
                    │ registry,     │         │YES       │NO
                    │ runners)      │         ▼          ▼
                    │ OR Jenkins    │  ┌──────────┐ ┌──────────────┐
                    │ (max flex)    │  │ GitHub    │ │ GitLab CI    │
                    └──────────────┘  │ Actions   │ │ or CircleCI  │
                                     │ (2000min) │ │ (best        │
                                     └──────────┘ │ parallelism) │
                                                  └──────────────┘

```

### Mobile CI Strategy

```

                         ┌──────────────────────────┐
                         │ Building mobile in CI?   │
                         └──────────┬───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │ macOS build required           │
                    │ (iOS/macOS/RN)?                │
                    └──────┬────────────────┬───────┘
                           │YES             │NO
                           ▼                ▼
                    ┌──────────────┐  ┌──────────────────────┐
                    │ GitHub Actions│  │ Android-only?         │
                    │ macOS runner  │  └──────┬──────────┬────┘
                    │ OR self-hosted│         │YES       │NO
                    │ Mac mini fleet│         ▼          ▼
                    │ (Anka/Veertu) │  ┌──────────┐ ┌──────────────┐
                    └──────────────┘  │ Any Linux│ │ Flutter/RN   │
                                     │ runner   │ │ → Linux OK   │
                                     │ (fast)   │ │ for Android  │
                                     └──────────┘ └──────────────┘

```

### Deploy Strategy Selection

```

                         ┌──────────────────────────┐
                         │ Choosing deploy strategy  │
                         └──────────┬───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │ Zero-downtime required?         │
                    └──────┬────────────────┬───────┘
                           │YES             │NO
                           ▼                ▼
                    ┌──────────────┐  ┌──────────────────────┐
                    │ Instant rollback│  │ Rolling deploy OK?    │
                    │ critical?       │  └──────┬──────────┬────┘
                    └──────┬─────────┘         │YES       │NO
                           │YES                ▼          ▼
                           ▼            ┌──────────┐ ┌──────────────┐
                    ┌──────────────┐    │ Canary +  │ │ Basic rolling │
                    │ Blue-Green   │    │ auto-     │ │ update (K8s   │
                    │ (LB swap,    │    │ rollback  │ │ default, ECS) │
                    │ instant)     │    │ (5%→100%) │ └──────────────┘
                    └──────────────┘    └──────────┘

```

Complete when: Deploy strategy selected with rationale. Rollback mechanism documented and tested. Traffic shifting percentages defined with health check criteria.

### Rollback Strategy

```

                         ┌──────────────────────────┐
                         │ Deploy failed — rollback? │
                         └──────────┬───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │ Feature flag kill switch        │
                    │ available?                      │
                    └──────┬────────────────┬───────┘
                           │YES             │NO
                           ▼                ▼
                    ┌──────────────┐  ┌──────────────────────┐
                    │ Toggle flag   │  │ Canary deployment?    │
                    │ off (<30s)    │  └──────┬──────────┬────┘
                    │ BEST OPTION   │         │YES       │NO
                    └──────────────┘         ▼          ▼
                                      ┌──────────┐ ┌──────────────┐
                                      │ Auto-     │ │ Re-deploy     │
                                      │ rollback  │ │ previous      │
                                      │ on error  │ │ version tag   │
                                      │ rate >1%  │ │ (2-5 min)     │
                                      └──────────┘ └──────────────┘

```

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ci-cd-builder` | CI/CD pipeline config, build stages, test integration, artifact storage | Before designing build stages or integrating test runners |
| `release-manager` | Release versioning strategy, changelog format, approval workflow, rollout schedule | Before designing release stages or deployment gates |
| `cloud-architect` | Infrastructure design, Terraform modules, networking topology, IAM roles | Before provisioning infrastructure or configuring cloud auth |
| `docker-kubernetes` | Dockerfile, docker-compose, Helm charts, K8s manifests, container scanning | Before designing container build or deploy stages |
| `mobile-developer` | Build configs, signing certificates, app store API keys, platform requirements | Before automating iOS/Android builds or store submissions |
| `security-engineer` | OIDC setup, secret injection, signed commit verification, SAST/DAST integration | Before integrating secrets management or artifact signing |
| `ml-ai-engineer` | Model training scripts, evaluation metrics, feature definitions, serving requirements | Before building MLOps pipeline stages |
| `marketing-manager` | Release content calendar, social templates, email campaign specs, audience segments | Before adding marketing automation stages |
| `compliance-officer` | SOC2/HIPAA/GDPR control requirements, evidence collection specs, audit schedule | Before designing compliance automation |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `ci-cd-builder` | Automated pipeline with hardened security, drift detection, approval gates | CI/CD remains manual and unreproducible — velocity blocked |
| `release-manager` | Signed artifacts, automated changelogs, deploy pipeline with canary/rollback | No artifacts to promote — release train stalls |
| `shipping-and-launch` | App store submissions, marketplace publishing, notarized binaries | Software cannot reach users — launch blocked |
| `observability-engineer` | Pipeline metrics, deploy frequency, lead time, change failure rate, MTTR | No DORA metrics — cannot measure delivery performance |
| `platform-engineer` | IAC provisioning pipeline, state management, drift detection, cost estimates | Manual infra changes accumulate — drift and incidents grow |
| `security-engineer` | SAST/DAST/SCA results, SBOM, signed attestations, secret scan status | Security posture unknown — vulnerabilities accumulate silently |
| `ml-ai-engineer` | Automated training pipeline, model registry, drift monitoring, A/B canary deploy | Models deployed manually — cannot iterate at ML velocity |
| `marketing-manager` | Release notes, changelog, social media drafts, email campaign triggers | Marketing lags behind releases — users unaware of new features |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Secrets detected in pipeline config (pattern match on credential:value pairs) | [FAIL] Secrets in plaintext. Rotate immediately. Migrate to secrets manager. Block pipeline until resolved. |
| P2 | `terraform plan` returns non-empty diff but no apply in last 7 days | [WARN] Infrastructure drift. Resources out of sync with code. Run plan reconciliation. Investigate manual changes. |
| P3 | Pipeline run duration increased >50% week-over-week | [WARN] Pipeline bloat. Audit stage durations. Check cache hit rates. Optimize slowest stage. Consider parallelization. |
| P4 | Test flake rate exceeds 5% of total test runs in past week | [ALERT] Pipeline trust degrading. Quarantine top-3 flaky tests. Engineers will start ignoring failures within 2 weeks if not fixed. |
| P5 | App Store Connect review rejected 2+ times in 30 days | [ALERT] Rejection pattern. Audit metadata accuracy, screenshot currency, privacy labels. Fix root cause before next submission. |
| P6 | Docker image size increased >30% without intentional dependency addition | [WARN] Image bloat. Run `docker history`. Audit layer sizes. Check for accidental dev dependency inclusion. |
| P7 | No deploy to production in >14 days on active repository | [ALERT] Deployment frequency dropping. Check for: pipeline failures, approval bottlenecks, flaky test accumulation, or fear-based deploy avoidance. |
| P8 | Code signing certificate expiring within 30 days | [ALERT] Certificate expiry imminent. Rotate now. Apple cert renewal takes 24-72 hours. All iOS/macOS builds will fail after expiry. |

## What Good Looks Like
<!-- STANDARD: 3min -->

### Before (Manual Delivery)

```

Developer laptop: ./gradlew assembleRelease
Manual signing: open Keystore Explorer, import cert, sign APK
Manual upload: open Google Play Console, drag APK, write release notes
Manual deploy: SSH into server, docker-compose up -d, hope nothing breaks
Manual promotion: text Slack "new version is live"
Result: 45 minutes per release. Inconsistent. Unauditable. Error-prone.

```

### After (0→100 Automated Pipeline)

```

git push → CI triggers → static analysis → parallel builds (iOS + Android + Web + Desktop)
→ 12-layer tests pass → signed artifacts → store submissions (App Store + Play + Chrome + VS Code)
→ Terraform plan → approval gate → Terraform apply → canary deploy → 5% traffic
→ health checks pass → 25% → 50% → 100% → Slack notification
→ release notes auto-generated → changelog updated → social posts scheduled → email queued
→ status page updated → DORA metrics recalculated → SBOM attached to release
Result: 8-15 minutes from push to production. Every step auditable. Zero manual intervention.

```

## Deliberate Practice
<!-- STANDARD: 3min -->

### Exercise 1: Pipeline Audit (10 min)
Take an existing CI pipeline. Score it against the 10 Ground Rules. For each violation, write a one-sentence fix and estimate implementation time. Deliverable: prioritized remediation backlog in the State Log.

### Exercise 2: Build Matrix Design (15 min)
Design a build matrix for a cross-platform app (iOS, Android, web, desktop). Define: shared build steps, platform-specific signing, artifact naming convention, and failure isolation (one platform failing does not block others). Deliverable: pipeline config in `.github/workflows/` or equivalent.

### Exercise 3: Rollback Drill (15 min)
Take a production deploy pipeline. Add: canary deployment (5% traffic), automated health check (error rate <1%, latency < p95+20%), auto-rollback trigger (3 consecutive failures), and rollback notification. Deliverable: updated pipeline config with rollback stages verified.

### Exercise 4: Full Test Suite Integration (20 min)
For one project, integrate at least 6 of the 12 test layers into CI. Start with: static analysis, unit tests, integration tests, E2E tests, security scanning, and accessibility checks. Configure coverage thresholds, flaky test quarantine, and blocking gates for security findings. Deliverable: CI config with all test stages passing.

### Exercise 5: 0→100 Pipeline Architecture (30 min)
Design a complete 0→100 pipeline for a fictional cross-platform product. Include: build matrix, all applicable test layers, signing, 3+ distribution targets, IAC provisioning, canary deploy, observability, and marketing automation. Every stage has a rollback path. Every artifact is versioned and checksummed. Deliverable: architecture diagram + pipeline config skeleton + rollout plan.

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Code signing certificates expire mid-sprint — iOS/macOS CI pipeline suddenly cannot build. Apple cert renewal takes 24-72 hours. All releases blocked. | $20K-$100K in delayed releases and emergency expedited processing | Set calendar reminders 30 and 14 days before expiry. Use fastlane match with cert repo — rotate before expiry. CI alerts on codesign verification failure. Automate cert expiry monitoring. |
| Terraform state file corrupted by concurrent apply — infrastructure changes blocked 1-3 days while manually repairing state. Manual state surgery is error-prone and risks data loss. | $50K-$200K in blocked deploys and potential data loss | Always remote backend with locking (S3+DynamoDB, Terraform Cloud). Never local apply against shared state. Plan in CI before every apply. Plan output is your audit trail. |
| App Store review rejection on metadata — screenshots do not match current UI, description references removed feature, privacy policy URL broken. Rejection + resubmission: 2-5 days. | $10K-$50K in delayed release and lost App Store feature placement | Automate screenshots with fastlane snapshot + UI testing. Version-control metadata with deliver. Validate metadata in CI: screenshot dimensions, text length limits, URL reachability. |
| Docker image grows 10x over 6 months — developers add layers without cleanup. CI builds take 15+ min. Staging runs out of disk space. | $5K-$20K in wasted CI minutes and infrastructure costs | Multi-stage builds. Separate build deps from runtime. Docker history --no-trunc in CI, alert on layers >100MB. Monthly image optimization sprints. CI disk cleanup automation. |
| Pipeline secret leaked via debug output — developer adds echo $SECRET for debugging, forgets to remove. Secret exposed in public build logs. | $50K-$1M in security incident response, credential rotation, potential breach | Never log environment variables. Use ::add-mask:: (GitHub Actions) or equivalent. Gitleaks/truffleHog in pipeline. Rotate ALL credentials after any suspected exposure. |
| App Store Connect session expires during CI — fastlane fails with auth error. Manual re-auth with app-specific password required. | $2K-$5K per incident in engineer context-switching and delayed release | Use fastlane spaceauth for 30-day session token. Store in CI secrets. Weekly renewal workflow. Monitor auth failures and alert before session expiry. |
| Flaky test not quarantined — engineers learn that re-running the pipeline 3x fixes the problem. They stop investigating failures altogether. A real regression ships because everyone assumes it is a flake. | $50K-$250K in regression incidents caused by ignored pipeline failures | Auto-quarantine flaky tests (fail 2x, pass on retry). Track flake rate per test. Block new flakes from entering main. Fix top-5 flakiest tests each sprint. Pipeline trust is hard to earn back. |
| Database migration runs without pre-prod test — migration locks a table for 45 minutes in production during peak traffic. Customers see errors, data inconsistencies require 6 hours of manual repair. | $100K-$500K in revenue loss, data repair labor, and customer trust damage | Test migration against staging clone before production. Use expand-contract pattern for destructive changes. Set lock timeout. Run migration during maintenance window with verified rollback plan. |

## Best Practices
<!-- STANDARD: 3min -->

1. **Do make every pipeline artifact immutable** — Rebuilding the same git commit on a different day must produce a byte-identical artifact, or the pipeline is non-deterministic. Immutable artifacts eliminate "it worked on my machine" incidents — each costs 2-8 engineer-hours to diagnose and delays releases by hours. Every build must stamp artifacts with git SHA, publish to an immutable registry (no `latest` tags, no tag overwrites), and verify checksums before deployment.
2. **Prefer infrastructure-as-code over click-ops** — Manual infrastructure changes are unreviewable, unreproducible, and unrecoverable during an incident. Every click-ops change that isn't in Terraform/Pulumi/CDK/Bicep will be destroyed on the next `apply`. Running drift detection daily and alerting on any unmanaged resource catches shadow changes before they become production incidents — cost of unmanaged drift: $10K-$100K per incident in debugging and extended outage time.
3. **Always implement automated rollback triggered by error-rate thresholds** — A bad deploy without automated rollback means minutes of manual intervention while errors accumulate. At 1,000 requests/second, a 5-minute manual rollback window = 300,000 failed requests. The rollback must fire on observable signals (error rate >1%, latency P99 >2x baseline, health check failure), not human judgment. Human judgment adds 3-8 minutes of diagnosis delay while customers experience degraded service.
4. **Never store secrets in pipeline configuration files** — YAML, JSON, and environment variables in CI are not secret stores — they appear in logs, build outputs, and audit trails. The Codecov breach (2021) started with a leaked CI credential. Use a secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) with masked logging, short-lived credentials, and rotation policies. One leaked CI credential can cost $50K-$2M in cryptomining, data exfiltration, or compliance fines.
5. **Measure pipeline MTTR (mean time to recovery), not just MTBF** — Pipeline reliability is meaningless if recovery takes hours. Target MTTR <15 minutes for build failures, <30 minutes for deploy rollbacks. Track MTTR per pipeline stage with weekly trend monitoring; any stage with MTTR >1 hour is a deployment bottleneck costing $500-$5K per incident in blocked developer productivity across the team. Alert when MTTR trends upward for 3 consecutive weeks.

## Production Checklist
<!-- STANDARD: 3min -->

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Every pipeline stage has a timeout and retry policy with exponential backoff | Review CI config: no unbounded waits; retries with backoff for all network-dependent steps; dead-letter queue for async failures |
| ☐ | Artifacts are immutable and signed: no `latest` tags, all builds stamped with git SHA, checksums verified before deploy | Verify registry rejects tag overwrites; deployment pulls by SHA256 digest, not mutable tag; artifact signature verified in deploy pipeline |
| ☐ | Secrets zero in pipeline config: all credentials in secrets manager, masked in logs, short-lived where possible | `grep -rE "(password|secret|token|key|credential)" .github/ .gitlab-ci.yml` returns only secret references (${{ secrets.X }}), never literal values |
| ☐ | Automated rollback tested: canary or blue-green with error-rate-based auto-rollback; manual override available as backup | Trigger synthetic errors in canary deployment → verify auto-rollback completes within SLA; rollback time <2 minutes end-to-end |
| ☐ | IaC drift detected and alerted: plan runs daily; any unmanaged resource triggers alert with diff | Scheduled drift detection CI job; alert fires within 5 minutes of drift detection; escalation path documented |
| ☐ | Build matrix covers all target platforms: every OS/arch/platform variant compiles and passes tests in CI | CI matrix shows green across all declared targets; no platform excluded with "test manually" or "not applicable" without justification |
| ☐ | Observability instrumentation present: every deploy emits structured event with version, environment, git SHA, triggering actor, and deploy duration | Check structured logs/event bus for deploy events; all required fields populated; deploy event consumed by monitoring dashboards |
| ☐ | Rollback plan is documented and tested | Rollback runbook exists per service; canary rollback tested in staging within last 30 days; disaster recovery contact list verified current; escalation path tested end-to-end |

## Verification
<!-- STANDARD: 3min -->

1. **[CI step ordering]** — Verify every pipeline's build, test, security-scan, and deploy steps execute in dependency order; no deploy step before tests pass, no scan after deploy
2. **[Rollback path exists]** — Verify every production deploy pipeline has a documented and tested rollback path (feature flag, canary rollback, or versioned redeploy); no irreversibly destructive steps
3. **[State log continuity]** — Verify pipeline architecture decisions are recorded in the State Log with rationale, and no prior decisions are contradicted without documented justification

**Pass criteria:** All checks pass before delivering output.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| fastlane fails: "No code signing identity found" | Certificate expired or not installed on CI machine | Run fastlane match nuke + regenerate. Verify match repo accessible from CI. Check cert expiry with security find-identity. | **Certificates are infrastructure, not configuration.** Treat with same rigor as database credentials — version-controlled, rotated before expiry, monitored. |
| terraform apply hangs indefinitely | State lock held by crashed process. No force-unlock available without admin. | terraform force-unlock LOCK_ID. If fails, manually delete lock from DynamoDB/S3. Run terraform plan to verify state integrity. | **Monitor lock age.** If lock older than pipeline timeout (30 min), auto-alert. Consider auto-force-unlock after human review for stale locks. |
| Docker build fails: "no space left on device" | CI runner disk full from cached Docker layers. 20 builds/day without cleanup = 50GB+/week. | docker system prune -af --filter "until=24h" in CI cleanup. BuildKit with remote cache. Mount >50GB disk for Docker workloads. | **Docker images are the silent disk killer.** Automate cleanup — not optional. Monitor disk usage in CI. |
| App Store submission rejected: "Invalid Binary" | Bitcode or architecture mismatch. Built for simulator, not device. Missing entitlements. | Verify: ONLY_ACTIVE_ARCH=NO, correct ARCHS. Run xcrun altool --validate-app before upload. Check codesign -dvvv. | **Validate before upload, not after rejection.** Apple processing takes 15-30 min before surfacing "Invalid Binary." Pre-validation catches it in 30 seconds. |
| npm publish fails: "cannot publish over existing version" | Version already exists in registry. CI re-run with same version number. | Use semantic-release or standard-version for auto-bump. Never hand-edit version. Pipeline should read version from git tags, not package.json. | **Version collisions are automation failures.** The pipeline owns the version number, not the developer. Semver MUST be automated. |
| K8s deploy succeeds but health check fails after 2 min | Startup probe too short for application boot. Readiness probe fails before app is ready. | Increase initialDelaySeconds. Separate startup probe (longer grace period) from liveness/readiness probes. Set failureThreshold >3. | **Probe configuration is environment-specific.** What passes in staging with minimal data may fail in production with real database connections. Test probes against production-like data volume. |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a decision ledger for automation engineering sessions.

- [ ] Have I read the state log from the previous session?
- [ ] Are pipeline architecture decisions documented (platform choice, environment mapping, deploy strategy)?
- [ ] Do signing/infrastructure decisions align with prior choices?
- [ ] If contradicting a prior decision, have I documented WHY?
- [ ] Are flaky test quarantines, security exceptions, and rollback thresholds recorded?
- [ ] Are DORA metrics baseline and improvement targets tracked session-over-session?

## References
<!-- STANDARD: 3min -->

- [Testing Matrix — all 12 test layers](references/testing-matrix.md)
- [Build Ecosystem — every platform & framework](references/build-ecosystem.md)
- [Distribution Channels — every store, marketplace, registry](references/distribution-channels.md)
- [Infrastructure as Code Patterns](references/infrastructure-as-code.md)
- [Container Deployment Patterns](references/container-deployment.md)
- [Security & Compliance Automation](references/security-compliance.md)
- [MLOps Pipeline](references/mlops-pipeline.md)
- [Observability & Marketing Automation](references/observability-marketing.md)
