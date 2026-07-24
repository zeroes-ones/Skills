# Split-Filter Extraction: Monorepo to Polyrepo

## Prerequisites

```bash
pip install git-filter-repo
```

git-filter-repo is the officially recommended replacement for git filter-branch. It is faster, safer, and produces cleaner history.

## Extraction Procedure

```bash
# 1. Clone a fresh copy (never filter in-place)
git clone https://github.com/org/monorepo.git extraction-workspace
cd extraction-workspace

# 2. Filter to keep only the target subdirectory
git filter-repo --subdirectory-filter path/to/extracted-lib --force

# Now the repo root contains what was in path/to/extracted-lib
# All history for files outside that path is removed

# 3. Verify
git log --oneline --all | head -20
ls -la  # Should show lib files, not path/to/extracted-lib/lib/...

# 4. Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Push to new remote
git remote add origin https://github.com/org/extracted-lib.git
git push -u origin --all
git push -u origin --tags
```

## Post-Extraction in the Monorepo

Option A: Replace with submodule pointing to new repo
Option B: Replace with subtree (git subtree add)
Option C: Remove entirely if the lib is now independently maintained

## Common Pitfalls

- Filtering in-place destroys the original repo — always clone first
- Tags that span extracted and non-extracted files are preserved but may reference removed files
- Large repos may take hours to filter; test on a shallow clone first
