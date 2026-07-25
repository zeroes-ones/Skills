## Verification

Run these checks before declaring the conflict resolution complete:

```bash
# 1. Verify no conflict markers remain in any tracked file
grep -r '<<<<<<<' $(git ls-files) && echo "FAIL: Conflict markers still present" || echo "PASS"

# 2. Verify all files are staged
git diff --name-only --diff-filter=U | grep -q . && echo "FAIL: Unstaged conflicted files" || echo "PASS"

# 3. Verify build succeeds
npm run build  # or: make build, cargo build, etc.
# Check exit code: must be 0

# 4. Verify tests pass
npm test  # or: make test, cargo test, etc.
# Check exit code: must be 0

# 5. Verify resolution log exists and covers all hunks
test -f .merge-conflict-resolution-log.md || echo "FAIL: Resolution log missing"

# 6. Semantic conflict check: grep for duplicated function definitions
grep -n 'function\|const.*=.*(' <resolved-file> | sort -t: -k2 | uniq -d -f1 && \
  echo "WARN: Possible duplicate definitions" || echo "PASS"

# 7. Verify no unstaged changes (clean working tree aside from merge state)
git diff --name-only | grep -q . && echo "WARN: Unstaged changes detected" || echo "PASS"
```
