# Token-Efficient Workflow

```
# Step 1: Project health check
python3 scripts/project_health.py --project-id PROJECT --output json
# Returns: {
#   "spi": 0.85, "cpi": 1.05, "critical_path_slippage_days": 4,
#   "risks_high_open": 2, "risks_aging_30d": 1,
#   "blocked_tasks": 3, "stakeholder_nps": 7,
#   "milestones_on_track": 5, "milestones_total": 7
# }

# Step 2: Decision tree
# spi < 0.8 → Schedule compression (fast-tracking or crashing)
# cpi > 1.1 → Under budget (re-allocate or early delivery)
# critical_path_slippage_days > 0 → Focus ONLY on critical path recovery
# risks_high_open > 0 → Top priority: mitigation actions this week
# stakeholder_nps < 6 → Communication plan failing. Fix.
# blocked_tasks > 3 → SWAT unblocking session

# Step 3: Status report — auto-generate from data
python3 scripts/gen_status.py --project-id PROJECT > status_$(date +%Y-%m-%d).md
# 1-page markdown: milestones, top risks, blocked items, decisions needed

# Step 4: Verify RAID freshness
python3 scripts/raid_audit.py --project-id PROJECT --stale-threshold-days 14
# Exit 0 = all items reviewed within 14 days. Exit 1 = stale items found.
```

**Principle:** `project_health.py` reads from the project tracker (Jira/Linear/GitHub issues), computes SPI/CPI, checks milestone dates, and outputs a JSON snapshot. Agent reads 1 JSON file, applies the decision tree, and generates exactly 1 action. No reading task lists into agent context.


<!-- DEEP: 10+min -->
