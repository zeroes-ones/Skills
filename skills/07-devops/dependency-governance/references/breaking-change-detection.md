# Breaking Change Detection

Automated detection of breaking changes in shared dependencies before they reach production.

## Detection Methods

### 1. Canary Tests
Run the consumer's test suite against the new dependency version in CI.
- **Setup:** Renovate or Dependabot opens PR -> CI runs full test suite.
- **Detection:** Test failures indicate breaking changes.
- **Limitation:** Only catches changes that tests cover. Missing tests = undetected breakage.

### 2. Compiler/Type Checker
For typed languages, the compiler catches API changes at build time.
- **TypeScript:** `tsc --noEmit` catches removed exports, changed types, renamed methods.
- **Go:** Compiler catches removed functions, changed signatures.
- **Rust:** Compiler catches all API mismatches.
- **Strength:** Near-zero false negatives for statically typed languages.

### 3. API Compatibility Verification
Tools that compare the public API surface between versions.
- **JavaScript:** `npx api-diff-checker` or custom script using TypeScript AST.
- **Python:** `pytest --api-compat` with contract tests.
- **Java:** `japicmp` (Java API Compliance Checker).

### 4. Consumer-Driven Contract Tests
Each consumer defines expected behavior. Provider runs all consumer contracts.
- **Tool:** Pact, Spring Cloud Contract.
- **Benefit:** Provider knows exactly which consumers will break before merging.

## CI Integration

- **Per-PR:** Type check + canary tests on dependency update PRs.
- **Pre-release:** Full API compatibility check + all consumer contracts.
- **Post-release:** Monitor error rates in production for undetected breakage.

## When Breaking Changes Slip Through

1. Identify what broke (error logs, stack traces).
2. Pin the broken version: do not let other repos adopt it.
3. Fix: either add compatibility layer or coordinate migration.
4. Add a test: the specific breakage should have been caught.
