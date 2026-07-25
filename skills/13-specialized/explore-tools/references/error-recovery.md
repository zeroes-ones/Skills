## Error Recovery

<!-- Explicit recovery procedures for when tool discovery goes wrong -->

### E1: npm install fails with native module errors
**Symptom:** `node-gyp rebuild` errors, missing Python/make/gcc, `nan` deprecation warnings
**Diagnosis:** The package wraps a C/C++ library that requires native compilation. Your Node.js version, OS, or build toolchain doesn't match.
**Recovery steps:**
1. Check Node.js version compatibility: `nvm ls && node -v`. The package may require Node 18 but you're on Node 22 (or vice versa). Switch versions: `nvm use 18`.
2. Install build tools: macOS: `xcode-select --install`; Ubuntu: `sudo apt install build-essential python3`; Windows: `npm install --global windows-build-tools`
3. Try the prebuilt binary first: many native packages ship prebuilt binaries for common platforms. Check if the error is from a fallback compilation.
4. Docker-based approach: run inside a container with matching build environment: `docker run -it -v $(pwd):/app node:18-alpine sh`
5. WASM alternative: search for `[package-name]-wasm` or `[package-name]-pure-js` — many native packages now ship WASM fallbacks (e.g., `argon2-browser` vs `argon2`)
6. If all fails: find a pure-JavaScript alternative. Native modules add deployment complexity and platform fragility. Prefer JS/WASM implementations.

### E2: Tool doesn't support your platform
**Symptom:** Package is Linux-only (uses `epoll`, `io_uring`, `libsystemd`), macOS-only (uses CoreFoundation, Metal), or Windows-only (uses Win32 API)
**Diagnosis:** The tool depends on platform-specific APIs. Check the package.json `os` field, README platform support section, or CI build matrix.
**Recovery steps:**
1. Check GitHub issues for "[platform] support" — there may be a branch or community fork
2. Search for platform patches: `gh search issues --repo owner/repo "macos" OR "windows" OR "arm64" label:enhancement`
3. Containerization: if Linux-only, run on macOS/Windows via Docker: `docker run -v $(pwd):/app -it alpine`
4. Evaluate WASM/JS alternatives: cross-platform by design, no native dependencies
5. If a critical dependency is platform-locked and no alternatives exist, reconsider the dependency. Platform lock-in is a form of vendor lock-in that limits deployment options and team flexibility.

### E3: Cost estimate was wrong by 10x
**Symptom:** The tool was supposed to cost $50/month but the first bill is $530. Unexpected charges for data transfer, API calls, storage, or "active users" counted differently than expected.
**Diagnosis:** Pricing models are complex and intentionally confusing. "Free tier" definitions vary: requests vs. compute time vs. data transfer vs. active users vs. stored items.
**Recovery steps:**
1. Verify actual usage in billing dashboard: which line items are driving the cost?
2. Check for unexpected API calls (data transfer = largest hidden cost in serverless)
3. Check for polling/retry loops that inflate usage (10x expected API calls)
4. Contact vendor for credit: most will refund unexpected first-month charges as goodwill
5. Implement usage monitoring: set billing alerts at $5, $25, $100, $500. Add usage dashboards.
6. Implement usage limits in code: `maxRequestsPerDay`, `maxStoragePerUser`, circuit breakers
7. If cost is structural (not a bug), switch to a cheaper alternative or negotiate enterprise pricing

### E4: Recommended tool has a CVE disclosed after adoption
**Symptom:** `npm audit` or Dependabot flags a HIGH/CRITICAL CVE in a tool you adopted based on a previous recommendation.
**Diagnosis:** New CVEs are discovered constantly. A clean security record at adoption time doesn't guarantee future safety. Check if the CVE affects YOUR usage pattern — many CVEs are in code paths you don't use.
**Recovery steps:**
1. Assess severity: read the CVE details. Is it remotely exploitable? Does it require user interaction? What's the attack vector?
2. Check if your usage is affected: are you using the vulnerable function/code path? Many CVEs are in edge-case features.
3. Update to patched version: `npm update [package]` or `npm install [package]@latest`
4. If no patch exists: (a) implement a workaround (input validation, WAF rule, disabled feature), (b) use `npm overrides` or `resolutions` to force a patched transitive dependency, (c) fork and patch the vulnerable code
5. If the vulnerability is unfixable and critical to your usage: switch tools. Document the CVE-triggered migration as a case study for future evaluations.
6. Update your tool evaluation criteria: add "CVE response time" to the Adoption Risk Assessment. Prefer tools with <7 day CVE resolution.

### E5: Tool is deprecated after adoption
**Symptom:** The maintainer archives the repo, adds a deprecation notice, or stops publishing updates. Your project now depends on dead code.
**Diagnosis:** Check: (a) is the tool truly dead (archived repo + deprecation notice) or just slow? (b) Is there a community fork continuing development? (c) Is there a recommended migration path from the maintainer?
**Recovery steps:**
1. Check for community forks: `gh api search/repositories?q=[package-name]+fork:true` sorted by stars
2. Check the deprecation notice for a recommended successor — many maintainers recommend specific alternatives
3. Assess migration cost vs. maintenance cost. Quick heuristic:
   - <100 lines of integration code → migrate within 2 weeks
   - 100-1000 lines → migrate within 1-2 months, budget 20-40 engineering hours
   - >1000 lines or core architectural component → plan migration in stages over 3-6 months
4. Do NOT stay on a deprecated tool long-term. Every week you delay, the cost increases: (a) security vulnerabilities accumulate, (b) dependency conflicts multiply, (c) team knowledge of the migration context fades, (d) new hires must learn a dead tool.
5. Post-mortem: what signals did you miss? (declining commit frequency, maintainer burnout tweets, issue backlogs growing). Add these to your Adoption Risk Assessment checklist.

### E6: Recommended tool doesn't integrate with your existing stack
**Symptom:** Tool works in isolation but doesn't play well with your framework (Next.js App Router, FastAPI middleware, Go's context propagation). Integration requires hundreds of lines of adapter code.
**Diagnosis:** Some tools are designed for specific ecosystems. A state management library might work with React but not Next.js SSR. A logging library might work with Express but not Fastify.
**Recovery steps:**
1. Search GitHub issues for "[tool] [framework] integration" or "[tool] [framework] not working"
2. Check if there's a framework-specific wrapper or plugin: `[tool]-[framework]` or `[framework]-[tool]`
3. Build a minimal integration test BEFORE committing: a single-file proof-of-concept that exercises the tool in your framework context
4. If integration is fragile and no wrapper exists: switch to a framework-native alternative. A tool that doesn't integrate with your framework costs 2-5x in adapter code and debugging time.

### E7: The candidate tool list is empty or all candidates are bad
**Symptom:** After searching registries, GitHub, and community sources, you found 0-2 candidates and they all score poorly on the evaluation matrix.
**Diagnosis:** You may be: (a) in a truly novel domain with no existing tools, (b) searching with too-narrow constraints, (c) using the wrong keywords or ecosystem, or (d) the problem doesn't require a dedicated tool.
**Recovery steps:**
1. Broaden the search: search adjacent ecosystems (npm for a Python problem? Rust crate callable from Python via PyO3?)
2. Relax constraints: is the "must-have" feature really must-have? Can you compose 2 simpler tools to achieve the result?
3. Consider building: if the problem is genuinely novel or simple enough, a custom solution may be appropriate. But document WHY no existing tool works — revisit in 6 months as the ecosystem may have caught up.
4. Re-examine the problem: maybe the problem itself is the wrong framing. Are you trying to solve the right problem with the wrong tool category?
