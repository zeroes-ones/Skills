# Token-Efficient Workflow

```
# Step 1: Generate comp band
python3 scripts/build_comp_band.py --level L5 --geo "SF Bay Area" --stage "Series B" \\
  --percentile 65 --output json
# Returns: {"level":"L5","base":{"min":185000,"mid":215000,"max":258000},...}

# Step 2: Onboarding checklist for new hire start date
python3 scripts/onboarding_checklist.py --employee-id 42 --start-date 2026-08-01 \\
  --hris rippling --output markdown
# Returns: 0-30-60-90 day task list with owners

# Step 3: Performance calibration distribution check
python3 scripts/calibration_audit.py --cycle 2026H1 --department engineering --output json
# Returns: {"ratings_distribution":{...},"skew_detected":true,"affected_managers":["alice","bob"]}

# Step 4: Retention risk scan
python3 scripts/retention_risk.py --high-performers-only --output json
# Returns: [{"employee":"jane","risk_score":78,"reasons":["18mo_since_promo","bottom_quartile_comp"]},...]
```
