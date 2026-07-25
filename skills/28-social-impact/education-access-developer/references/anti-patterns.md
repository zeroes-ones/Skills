# Anti-Patterns — Education Access Developer

<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Beginning implementation without a validated design or spec | Start with a lightweight design doc, get stakeholder sign-off, then code. Every hour in design saves 10 hours in rework. | Check for SKILL.md without clear decision trees or missing "When to Use" section | Pre-commit: verify-skill.sh blocks commits without completed design sections |
| Hardcoding configuration values (API keys, URLs, feature flags) in source | Use environment variables for config, secrets manager for credentials, feature flags service for toggles. | grep -rn "api_key\\|API_KEY\\|secret\\|password" --include="*.ts" | GitGuardian / detect-secrets in pre-commit hook |
| Skipping error handling for "unlikely" edge cases | Every code path needs error handling. Handle and log explicitly. | grep -rn ".catch\\|try {" --include="*.ts" -A 5 | grep -v "logger.error" | eslint no-empty-function + custom rule requiring logger.error in every catch |
| Building a monolith without a decomposition plan | Start with clear module boundaries even in a monolith. Define API contracts between modules. | Check for src/ directories with no clear module separation | Architecture lint: enforce directory structure with max files per directory |
| Optimizing prematurely before measuring | Profile first. Fix the actual bottleneck. 80% of perf issues come from 20% of code. | PR review: any perf optimization without linked benchmark data gets blocked | Pre-commit: block PRs that mention "optimize" without benchmark data |
| Ignoring accessibility until "later" | Build accessible from day one. WCAG compliance is cheaper to build in than retrofit. | grep -rn "role=\\|aria-" --include="*.tsx" -- count should be >0 for UI | eslint jsx-a11y plugin. Lighthouse CI with accessibility threshold >= 90 |
| Deploying on Friday at 5 PM | Deploy Tuesday-Thursday morning. Have a rollback plan tested and ready. | Check deployment timestamps post Friday 3 PM local | CI/CD policy: block production deploys Friday 3 PM to Monday 9 AM |
