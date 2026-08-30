# Library Freshness Policy — Always Use Updated Libraries

> **Canonical policy.** Every skill that emits library, SDK, or API references MUST follow this policy and use `scripts/lib/library-version-check.sh` to verify freshness before producing output. This is the single source of truth for what "updated" means — do not invent per-skill variants (route, don't duplicate).

## The Rule in One Line

**Before emitting any code that references a library or SDK version, verify against the installed manifest AND check for newer versions; never ship a reference you know is outdated without a documented, time-boxed exception.**

## What "Updated" Means

| Term | Meaning |
|------|---------|
| **Current** | The installed version is the latest stable release (or within the supported window per the provider). |
| **Supported** | The version receives security and bug fixes from the maintainer (check the support policy — e.g., Node LTS, RN release train, Expo SDK window, Flutter stable). |
| **Outdated** | A newer stable release exists that you have no documented reason not to use. |
| **Bleeding edge** | A pre-release / nightly / `latest`-floating version — NOT "updated". Pin stable releases. |

**"Always use updated libraries" does NOT mean "always take the newest."** It means: pin a version, verify it is current or supported, and upgrade deliberately with a plan — never emit stale references by default and never float to `latest` silently.

## The Three-Step Discipline (Pin → Verify → Upgrade)

### 1. Pin
- **Pin every dependency to a concrete version.** Never `latest`, never an unversioned git branch, in production.
- Use the project's native pinning mechanism: `package.json` + lockfile, `pubspec.lock`, Gradle version catalog (`libs.versions.toml`), `Podfile.lock`.
- A lockfile is the contract — commit it, never hand-edit the resolved tree.

### 2. Verify Freshness (mandatory before emitting library references)
Run the shared checker for the project type:

```bash
bash scripts/lib/library-version-check.sh [project-root] --strict
```

| Project type | What the checker runs | Freshness signals |
|--------------|----------------------|-------------------|
| React Native / Expo | `npx expo install --check`, `npm outdated` | SDK alignment, outdated npm deps |
| Flutter | `flutter pub outdated` | Outdated pub deps vs latest |
| Kotlin Multiplatform / Gradle | version catalog review | kotlinx/library version drift (manual verify) |
| Node (generic) | `npm outdated` | Outdated npm deps |

- **`--strict`**: any outdated dependency group is BLOCKING — fix it (or document the exception) before emitting code.
- Without tooling available (e.g., no npm in the environment), the checker warns and you must verify manually against the official release pages and tag the claim `[VERIFIED <date>]`.

### 3. Upgrade Deliberately (not reactively)
- **Upgrade cadence:** check freshness at every material decision point (research loop) and before every release. Batch upgrades; never solo-bump one dependency out of the matrix.
- **Upgrades are migrations, not bumps:** read the release notes/migration guide, check the compatibility matrix (see each skill's `version-matrix.md`), run the test suite, verify the platform-specific seam (e.g., iOS framework export, native modules), and keep a rollback path.
- **Record the decision** in the skill's State Log: what was upgraded, why, what broke, what the rollback is.

## Exceptions (documented, time-boxed)

The only valid reasons to emit an outdated reference:

| Exception | Requirement |
|-----------|-------------|
| **Compatibility pin** | A newer version breaks another pinned dependency or the platform build. Document the conflict. |
| **Stability pin** | A newer major is not yet proven for the app's critical path. Document the review date and the upgrade owner. |
| **Support window** | The provider's supported window still includes the installed version (e.g., still receiving security fixes). |
| **Tooling unavailable** | The checker cannot run; verify manually, tag `[VERIFIED <date>]`, and note the limitation. |

Every exception gets a State Log entry with an expiry/review date. An undocumented outdated reference is a defect.

## How Skills Enforce This

- **Ground rules** reference the checker (e.g., "run the shared library freshness check before emitting library references").
- **Core Workflow Phase 1 (Anchor)** runs the checker alongside the version anchor.
- **Production Checklist / Verification** include a "library currency" gate.
- **References** point to this policy and to `scripts/lib/library-version-check.sh`.

## Related

- `scripts/lib/library-version-check.sh` — the executable checker.
- Each skill's `references/version-matrix.md` — the compatibility contract + upgrade protocol for that stack.
- The RP1 research gate — "verify domain currency" is the research-layer counterpart; this policy is the enforcement-layer counterpart.
