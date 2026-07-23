# Token-Efficient Workflow

```
# Step 1: Quick audit — what legal docs exist and are they current?
python3 scripts/legal_audit.py --site example.com --output json
# Returns: {"tos": {"exists": true, "age_days": 200, "clickwrap": false},
#           "privacy": {"exists": true, "age_days": 400, "score": "outdated"},
#           "open_source": {"gpl_count": 2, "total_deps": 150}}

# Step 2: Decision tree → prioritize by risk
# No ToS on product with users → CRITICAL. Deploy within 48 hours.
# Privacy Policy >365 days → HIGH. Update with current practices.
# GPL/AGPL in codebase → HIGH. Isolate or replace.
# No clickwrap → MEDIUM. Add to signup flow, record consent.

# Step 3: Execute with exit codes
# Check if a site has a privacy policy link in footer
curl -s https://example.com | grep -qi "privacy" && echo "FOUND" || echo "MISSING"

# Run open-source license scan (one command, exit code 1 = GPL found)
npx license-checker --production --summary 2>&1 | \
  python3 -c "import sys; text=sys.stdin.read(); sys.exit(1 if 'GPL' in text or 'AGPL' in text else 0)"

# Step 4: Verify — re-run audit after changes
python3 scripts/legal_audit.py --site example.com --verify --output json
# Exit code 0 = all critical issues resolved
```

**Principle:** `legal_audit.py` outputs structured JSON with issue severity. Agent maps severity → action via decision tree. Never reads legal document text into context (token waste). Exit codes verify fixes.
