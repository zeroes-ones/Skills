# Shared Code Strategies Across Repos

Decision framework for how to share code when repositories are independent. Not all sharing requires a package — sometimes copy-paste is the right answer.

## Strategy 1: Internal Package Registry

Publish shared code as versioned packages to an internal registry (npm, PyPI, Maven, Cargo).

- **When:** 3+ consumer teams, code changes weekly or more, need semantic versioning
- **Setup:** GitHub Packages, Artifactory, Nexus, or cloud-native (AWS CodeArtifact)
- **Versioning:** Strict SemVer. Automated changelog from conventional commits.
- **CI integration:** Publish on merge to main. Downstream auto-PR via Renovate on new version.

## Strategy 2: Git Submodules

Embed another repo at a specific commit within your repo.

- **When:** Code MUST be identical across repos (legal text, compliance configs), changes extremely rare
- **Pros:** Exact version pinning. No registry infrastructure needed.
- **Cons:** Detached HEAD states, recursive clone required, merge conflicts on submodule pointers

## Strategy 3: Vendoring (Copy with Attribution)

Copy the source code into your repo with a clear source-of-truth annotation.

- **When:** 1-2 consumers, changes rare (<quarterly), extracting a package is over-engineering
- **Rule:** Annotate each file with source repo, commit SHA, and copy date
- **Limit:** Maximum 3 copies across the org. At 4+, extract to an internal package.
- **Verification:** Annual grep to find diverged copies. Update or consolidate.

## Strategy 4: Published Config Packages

Share tooling configuration (ESLint, Prettier, TypeScript) as a versioned package.

- **When:** Multiple repos use the same tooling with the same rules
- **Example:** `@company/eslint-config` v9.0.0 for ESLint 9
- **Versioning:** Track the tool version (config v9.x for ESLint 9, config v10.x for ESLint 10)

## When NOT to Share

- **"Future-proofing" a library with one consumer.** Wait until 3+ consumers exist.
- **Sharing 20 lines of code.** The package overhead exceeds the duplication cost.
