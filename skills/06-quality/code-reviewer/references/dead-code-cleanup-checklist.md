# Code Reviewer - Dead Code & Legacy Cleanup Checklist

Checklist for identifying and removing dead code, legacy artifacts, and unused dependencies during code review. Enforces the Boy Scout Rule: every file touched should be left cleaner than it was found.

---

> **Rule of thumb:** If you touched a file or module, you're responsible for leaving it cleaner than you found it. This checklist helps reviewers enforce that.

---

## 1. Dead Code — Lines That Will Never Execute

- [ ] **Unreachable code** — code after `return`, `throw`, `break`, `continue`, or inside `if (false)` blocks
- [ ] **Functions/methods never called** — grep the codebase; if nothing invokes it, flag it for removal
- [ ] **Classes or modules never instantiated or imported**
- [ ] **Unused variables, constants, or enum members**
- [ ] **Event handlers or callbacks that are registered but never fire**
- [ ] **Empty lifecycle hooks** (e.g., `ngOnInit() {}`, `useEffect(() => {}, [])`) — remove them

---

## 2. Commented-Out Code

- [ ] **Block-commented code** — `/* ... */` wrapping entire functions or logic blocks
- [ ] **Line-commented code** — `// oldThing.doSomething()` left behind "just in case"
- [ ] **Conditional compilation remnants** — `#ifdef OLD_FEATURE` blocks that are never enabled
- [ ] **"Temporarily disabled"** comments with no tracking ticket or stale ticket references

> *If it's in version control history, it doesn't need to be in the file.*

---

## 3. Unused Imports & Dependencies

- [ ] **Unused imports** — `import` statements with no references in the file
- [ ] **Side-effect-only imports** — flag if a module is imported solely for side effects; make it explicit
- [ ] **Unused dependency declarations** — entries in `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, etc. that are no longer imported anywhere
- [ ] **Redundant type/interface imports** — imported but never used as type annotations

---

## 4. Legacy Patterns & Deprecated APIs

- [ ] **Deprecated library calls** — any usage of functions/classes marked `@deprecated` should be replaced
- [ ] **Outdated framework patterns** — e.g., class components where functional components are the standard, old lifecycle methods, legacy Angular forms
- [ ] **Deprecated API versions** — REST endpoints, SDK versions, or protocol versions marked for removal
- [ ] **Polyfills that are no longer necessary** — check if the target browser/engine now supports the feature natively

---

## 5. Duplicate & Near-Duplicate Code

- [ ] **Copy-pasted blocks** — identical logic in two or more places within the changed files
- [ ] **Near-duplicates** — code that differs only by a constant, type, or parameter; extract and parameterize
- [ ] **Reimplemented utilities** — does a shared util, helper, or library function already exist?

---

## 6. Stale Feature Flags & Toggles

- [ ] **Permanently-enabled flags** — if a flag has been `true` in production for >1 release cycle, remove the branching logic
- [ ] **Permanently-disabled flags** — if a feature was killed, remove flag checks and the dead path
- [ ] **Expired experiment flags** — A/B test toggles where the experiment concluded

---

## 7. Stale Comments & Documentation

- [ ] **TODO/FIXME/HACK comments** — is the issue still relevant? If yes, does it have a tracking ticket?
- [ ] **Outdated docstrings** — do function descriptions still match behavior after the refactor?
- [ ] **Misleading comments** — comments that describe behavior that no longer exists
- [ ] **Changelog-in-comments** — version history in file headers; that's what git log is for

---

## 8. Test Artifacts

- [ ] **Skipped tests with no explanation** — `it.skip`, `test.skip`, `xdescribe`, `@pytest.mark.skip`
- [ ] **Commented-out assertions** — `// expect(foo).toBe(bar)` in test files
- [ ] **Test-only code in production files** — `export for testing` patterns, test-specific exports, `window.__DEBUG__`
- [ ] **Dead test fixtures or mocks** — fixtures that are defined but never referenced

---

## 9. Configuration & Build

- [ ] **Unused environment variables** — references to env vars that are never set in any environment
- [ ] **Dead build targets or scripts** — entries in `Makefile`, `package.json#scripts`, `Taskfile` that no one runs
- [ ] **Stale CI steps** — pipeline stages that always pass and do nothing meaningful
- [ ] **Unused config keys** — entries in YAML/JSON/TOML config files with no corresponding code

---

## Review Workflow

| Phase | Action |
|-------|--------|
| **Author (pre-submit)** | Run through this checklist on every file touched. Remove what you find. |
| **Reviewer** | Spot-check 2–3 files. If you find dead code, ask: *"Did you check the rest of the module?"* |
| **Automation** | Add dead-code detection to your linter (e.g., ESLint `no-unused-vars`, `unused-imports`; Ruff `F401`; `ts-prune`; `go vet`; `dead` for Python). Block merge if violations exist. |

---

**The goal is incremental, not perfect.** You don't need to clean the entire codebase in one PR — just the files you're already changing. Over time, this compounds into a healthier codebase.
