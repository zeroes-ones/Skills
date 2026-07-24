# Alternative Tools to Git Submodules

## git-subrepo

A Git submodule alternative that stores subrepo data in the parent repo rather than as pointers.

```bash
# Install: brew install git-subrepo (macOS)
git subrepo clone https://github.com/org/lib.git libs/lib
git subrepo pull libs/lib
git subrepo push libs/lib
```

Pros: No detached HEAD, simple workflow, subrepo data travels with parent clone.
Cons: History rewriting on push (similar to subtree), not part of Git core.

## gitslave

Creates a group of related repos that can be operated on simultaneously.

```bash
gitslave add <repo-url>
gits attach <repo-url>
```

Best for: Projects split across multiple repos that are always used together.

## repo (Android Tool)

Google's tool for managing many Git repositories. Used by Android/AOSP.

```bash
repo init -u https://github.com/org/manifest.git
repo sync
```

Best for: Very large polyrepo setups (100+ repos) with a manifest-based approach.

## myrepos (mr)

A tool to manage all your version control repositories.

```bash
mr register  # Add current repo
mr update    # Update all registered repos
```

Best for: Personal workflow across many small repos. Not suitable for team-wide adoption.

## Comparison Matrix

| Tool | Team Scale | Submodule Replacement | CI Complexity |
|------|-----------|----------------------|---------------|
| git-subrepo | 3-20 | Yes | Low |
| gitslave | 5-50 | Partial | Medium |
| repo | 50+ | Yes | High |
| myrepos | 1-10 | No | Low |
