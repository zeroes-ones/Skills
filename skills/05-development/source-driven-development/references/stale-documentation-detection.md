# Stale Documentation Detection

## The Problem

Official documentation can lag behind the actual API. This creates a dangerous situation where following "official" docs produces broken code.

## Detection Signals

### Signal 1: Doc "Last Updated" Date
```
If doc page says "Last updated: 2023-06" and latest release is 2024-09 → suspect stale.
Check: Scroll to bottom of page for "last modified" or check git history of docs repo.
```

### Signal 2: Version Mismatch in URL vs. Page Content
```
If URL says /v4/docs/ but code examples use APIs introduced in v5 → overlapping deployment.
Check: Look for a version selector widget. Switch to latest and see if page changes.
```

### Signal 3: Example Code Doesn't Compile
```
Copy the doc's example into a fresh project at the documented version. Run it.
If it fails → docs are stale or wrong.
```

### Signal 4: TypeScript Definitions Disagree with Docs
```bash
# Compare doc signature to actual type definitions
npm ls @types/react --depth=0
# Then check node_modules/@types/react/index.d.ts for the method in question.
# If the type signature differs from docs → trust types (they're generated from source).
```

### Signal 5: GitHub Issues Mentioning Doc Errors
```bash
gh search issues "documentation wrong" --repo owner/repo --label documentation
gh search issues "outdated docs" --repo owner/repo
```

### Signal 6: Release Notes Describe Changes NOT in Docs
```
If v4.3 release notes say "changed parameter order in createUser()" but
docs still show old parameter order → docs weren't updated after release.
```

## Verification Protocol

```
1. Check doc "last updated" → if >3 months since last release, suspect stale
2. Check 2-3 recent GitHub issues with "documentation" label
3. Copy-paste exactly one code example from docs into a test file. Run it.
4. Compare type definitions (if typed language) against doc signatures
5. If any discrepancy → escalate to source code (Level 5)
6. Document the discrepancy: ⚠️ DOC-GAP: {description}. Source at {git tag}. Issue: {link}
```

## When to Trust Despite Signals

- Minor version bumps rarely invalidate docs for stable APIs
- Core/foundational APIs change less frequently than experimental features
- Some projects (e.g., Linux man pages) update docs BEFORE releasing code

## Mechanical Check

```bash
#!/bin/bash
# Compare doc page last-modified header against latest release date
DOC_DATE=$(curl -sI "https://docs.example.com/api/v2/users" | grep -i "last-modified" | cut -d: -f2-)
LATEST_RELEASE=$(curl -sL "https://api.github.com/repos/owner/repo/releases/latest" | jq -r '.published_at')
echo "Doc updated: $DOC_DATE"
echo "Latest release: $LATEST_RELEASE"
# If doc is >90 days older than latest release, flag
```
