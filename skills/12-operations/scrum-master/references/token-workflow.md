# Token-Efficient Workflow

```
# Step 1: Sprint health check (query from issue tracker API)
python3 scripts/sprint_health.py --team backend --output json
# Returns: {"sprint":"W15","committed":34,"completed":28,"carryover":6,
#           "velocity_3sprint_avg":31,"cycle_time_p85":4.2,"retro_items_done":2}

# Step 2: Decision tree → action
# carryover > 20% → Overcommitted. Reduce commitment by average carryover.
# cycle_time_p85 > 5 days → Check CFD for bottleneck. Apply WIP limit.
# retro_items_done == 0 → Retros need focus. Pick 1 action. Track.

# Step 3: Generate retrospective data (pull metrics before retro)
python3 scripts/retro_data.py --team backend --sprint 15 --output markdown

# Step 4: Verify improvement
python3 scripts/sprint_health.py --team backend --compare-sprint 14 --output json
# Exit code 0 = metrics improved, 1 = worsened
```

**Principle:** `sprint_health.py` queries Linear/Jira API, returns JSON. Agent reads numbers, not narratives. Retro data auto-generated. Improvement tracked via exit codes.
