# Token-Efficient Workflow

```
# Step 1: Docs health check
python3 scripts/docs_health.py --docs-dir docs --output json
# Returns: {"pages": 85, "broken_links_internal": 3, "broken_links_external": 1,
#           "pages_stale_6mo": 12, "pages_no_owner": 5, "readme_score": 8.5}

# Step 2: Decision tree → single action
# broken_links > 0 → Fix immediately
# pages_stale_6mo > 10% → Batch refresh sprint
# pages_no_owner > 0 → Assign via CODEOWNERS
# readme_score < 7 → Audit README against template

# Step 3: Quick verifications with exit codes
cd docs && npm run build                 # Exit code 0 = builds
lychee --base docs docs/                 # Exit code 0 = no broken links
vale docs/                               # Exit code 0 = no prose issues
npx @redocly/cli lint openapi.yaml       # Exit code 0 = spec valid

# Step 4: Verify improvement
python3 scripts/docs_health.py --docs-dir docs --compare last-week --output json
# Exit code 0 = all metrics improved, 1 = regressed
```

**Principle:** `docs_health.py` scans the docs directory, outputs JSON with metrics. Agent applies decision tree to exactly one action. Build, lint, and link checking all use exit codes. Never reads doc content into agent context (massive token waste).
