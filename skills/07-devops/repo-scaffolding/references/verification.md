## Verification

### Verify Template Quality
```bash
# Check if template repo exists and is marked as template
gh repo view org/template-repo --json isTemplate,name,description
```

```bash
# Scaffold a test repo from template
gh repo create test-scaffold-$(date +%s) --template org/template-repo --private --clone
cd test-scaffold-*
npm install  # or pip install -e . or make setup
npm test     # or pytest or make test
# CI must pass on first push
git add . && git commit -m "init: scaffold from template" && git push
# Check: CI workflow triggered. Check: CI workflow passed.
```

### Verify Template Completeness
```bash
# Required files check
for f in .github/workflows/ci.yml SECURITY.md CODEOWNERS .gitignore LICENSE README.md; do
  [ -f "$f" ] && echo "PASS: $f" || echo "FAIL: $f missing"
done
```

### Verify Downstream Sync
```bash
# For each downstream repo, check drift against template
for repo in $(gh repo list org --json name --jq '.[].name' | grep -v template); do
  echo "=== $repo ==="
  diff <(gh api repos/org/template-repo/contents/.github/workflows/ci.yml --jq '.content' | base64 -d) \
       <(gh api repos/org/$repo/contents/.github/workflows/ci.yml --jq '.content' | base64 -d) \
       && echo "SYNCED" || echo "DRIFT DETECTED"
done
```

### Verify Monorepo Scaffolding
```bash
# Test Nx generator
nx generate @org/generators:library test-lib-$(date +%s) --dry-run
# Test plop.js generator
npx plop package test-pkg-$(date +%s)
```
