## Core Workflow

### Phase 1: Submodule Health Audit

Execute in order. Do not skip steps.

```
1. INVENTORY ALL SUBMODULES
   |-- List all submodules: git submodule status --recursive
   |-- For each submodule, record: path, pinned commit SHA, configured branch, remote URL
   |-- Count: total submodules (warn if >20)
   |-- Check for stale entries: submodules in .gitmodules whose paths do not exist

2. DETACHED HEAD CHECK
   |-- For each submodule: cd <path> && git status | head -1
   |-- If "HEAD detached at": submodule is NOT tracking a branch
   |-- Fix: git config -f ../.gitmodules submodule.<path>.branch main
   |-- Then: git submodule update --remote -- <path>

3. REACHABILITY CHECK
   |-- For each submodule, verify the pinned SHA exists in the remote:
   |   |-- cd <path> && git fetch origin
   |   |-- git cat-file -t <pinned-sha>
   |   |-- If fails: pinned commit has been force-pushed away or repo deleted
   |-- Document all unreachable SHAs — these are ticking time bombs

4. DIVERGENCE CHECK
   |-- Compare pinned SHA with remote branch tip:
   |   |-- cd <path> && git rev-list --count HEAD..origin/main
   |-- If >50 commits behind: submodule is significantly stale
   |-- Assess: is this intentional (known-good version) or neglect?
   |-- Flag: security-sensitive deps (auth libs, crypto) more than 30 days behind

5. CI VERIFICATION
   |-- Check CI config for submodule checkout:
   |   |-- GitHub Actions: actions/checkout@v4 with: submodules: recursive
   |   |-- GitLab CI: GIT_SUBMODULE_STRATEGY: recursive
   |   |-- Jenkins: git clone --recurse-submodules
   |-- Verify: do all CI jobs that touch code have submodule checkout?
  Complete when: all submodules are inventoried with pinned SHA and remote URL, detached HEADs are resolved with branch tracking, all pinned SHAs are reachable on their remotes, and divergence gaps are documented with intentionality.
```

### Phase 2: Split-Filter Extraction (Monorepo to Polyrepo)

```
1. PREPARE THE EXTRACTION
   |-- Identify the subdirectory to extract: path/to/lib
   |-- Verify the subdirectory has meaningful independent history
   |-- Install git-filter-repo: pip install git-filter-repo
   |-- Clone a fresh copy (never filter in-place): git clone <monorepo> extraction-workdir

2. FILTER THE HISTORY
   |-- Extract only the subdirectory, preserving its internal structure:
   |   |-- cd extraction-workdir
   |   |-- git filter-repo --subdirectory-filter path/to/lib --force
   |-- Verify: git log --oneline | head -20 (should show only commits touching path/to/lib)
   |-- Verify: file structure at root is the lib contents, not path/to/lib/lib/...
   |-- Clean: git reflog expire --expire=now --all && git gc --prune=now --aggressive

3. PUSH TO NEW REPO
   |-- Create empty remote repo (GitHub/GitLab/etc.)
   |-- git remote add origin <new-repo-url>
   |-- git push -u origin --all
   |-- git push -u origin --tags
   |-- Verify: git log in new repo shows correct history, git blame works on key files

4. UPDATE ORIGINAL MONOREPO
   |-- Option A: Replace extracted code with submodule pointer
   |   |-- rm -rf path/to/lib
   |   |-- git submodule add <new-repo-url> path/to/lib
   |-- Option B: Replace with subtree
   |   |-- git subtree add --prefix=path/to/lib <new-repo-url> main --squash
   |-- Option C: Archive (if lib is fully independent, no ongoing changes needed)
  Complete when: git-filter-repo extracts the subdirectory with clean history, new repo has correct history with git blame working on key files, and original monorepo is updated with submodule/subtree pointer.
```

### Phase 3: Subtree Workflow

```
1. ADDING A SUBTREE (one-time)
   |-- git subtree add --prefix=path/to/dep <remote-url> <branch> --squash
   |-- --squash: condenses entire remote history into one merge commit
   |-- Without --squash: full history imported (use for ongoing bidirectional sharing)

2. PULLING UPDATES (one-way sync)
   |-- git subtree pull --prefix=path/to/dep <remote-url> <branch> --squash
   |-- Resolve merge conflicts if local changes to subtree files exist
   |-- After pull: subtree files are updated in working tree, commit the merge

3. PUSHING CHANGES BACK (bidirectional)
   |-- Make changes in path/to/dep within the parent repo
   |-- Commit those changes
   |-- git subtree push --prefix=path/to/dep <remote-url> <branch>
   |-- WARNING: This rewrites history. Subsequent pulls will conflict.
   |-- Best practice: push immediately after making changes, minimize divergence

4. SPLITTING A SUBTREE (extract to standalone)
   |-- git subtree split --prefix=path/to/dep -b split-branch
   |-- This creates a new branch with only the subtree's history
   |-- Push split-branch to new remote: git push <new-remote> split-branch:main
  Complete when: subtree add/pull/push commands are documented for the team, bidirectional sync workflow is tested end-to-end, and subtree split produces a clean standalone branch.
```

### Phase 4: CI Integration

```
1. GITHUB ACTIONS SUBMODULE SETUP
   |-- Checkout with submodules:
   |   |-- uses: actions/checkout@v4
   |   |   with:
   |   |     submodules: recursive
   |   |     token: ${{ secrets.SUBMODULE_PAT }}  # for private submodules
   |-- Caching submodules:
   |   |-- uses: actions/cache@v4
   |   |   with:
   |   |     path: .git/modules
   |   |     key: submodules-${{ hashFiles('.gitmodules') }}
   |-- Submodule health check job:
   |   |-- git submodule status --recursive
   |   |-- git submodule foreach 'git fetch origin && git status'
   |   |-- Fail CI if any submodule is on detached HEAD (unless intentional)

2. GITLAB CI SUBMODULE SETUP
   |-- variables:
   |     GIT_SUBMODULE_STRATEGY: recursive
   |     GIT_SUBMODULE_DEPTH: 1  # shallow clone submodules for speed
   |-- For private submodules: configure deploy keys or CI job tokens

3. COMMON CI FAILURES AND FIXES
   |-- "fatal: could not read Username": private submodule without auth -> configure PAT/deploy key
   |-- "fatal: reference is not a tree": pinned commit force-pushed -> update submodule pointer
   |-- "error: Server does not allow request for unadvertised object": shallow clone -> set GIT_SUBMODULE_DEPTH: 0
  Complete when: CI config is verified for all CI providers in use, submodule checkout works with private repos via PAT/deploy keys, and health check job runs in CI passing or flagging detached HEADs.
```
