# Token-Efficient Workflow

```
# Step 1: Quick audit — which content to refresh first?
# Run a script that queries GA4/GSC API, outputs prioritized list as JSON
python3 scripts/content_audit.py --site example.com --min-age 180 --output json
# Returns: [{"url":"/blog/x","traffic_change":-40,"priority":"high"}, ...]

# Step 2: Decision tree → pick action
# Traffic drop >30% + age >6 months → REFRESH (update data, expand, republish)
# Ranking position 4-15 → QUICK WIN (improve title, meta, internal links)
# Traffic <10 visits/month + age >12 months → DELETE or CONSOLIDATE

# Step 3: Execute the single action. Verify with exit codes.
# Check if a page has proper heading structure
curl -s https://example.com/blog/x | python3 -c "
import sys, re
html = sys.stdin.read()
h1 = len(re.findall(r'<h1[^>]*>', html))
h2 = len(re.findall(r'<h2[^>]*>', html))
print(f'H1:{h1} H2:{h2}')
sys.exit(0 if h1 == 1 else 1)
"

# Step 4: Verify impact — re-run audit after 30 days
python3 scripts/content_audit.py --site example.com --url /blog/x --compare-30d
```

**Principle:** Automated audit scripts output JSON. Agent reads structured data, not prose. Decision tree maps every audit finding to exactly one action. No deliberation loops.
