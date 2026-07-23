# Token-Efficient Workflow

```
# Step 1: Privacy health check
python3 scripts/privacy_check.py --output json
# Returns: {
#   "has_privacy_policy": true, "policy_last_updated": "2024-01-15",
#   "has_cookie_consent": true, "consent_platform": "cookieyes",
#   "has_dpa_with_all_processors": false, "processors_without_dpa": 7,
#   "has_dsar_process": true, "dsar_last_30_days": 2,
#   "has_dpia_for_high_risk": false, "high_risk_activities": 2,
#   "has_ropa": false,
#   "has_data_retention_schedule": true,
#   "has_breach_response_plan": false,
#   "cross_border_transfers_to_non_adequate": true,
#   "sccs_executed": false
# }

# Step 2: Decision tree from JSON
# processors_without_dpa > 0 → Execute DPAs (highest legal risk)
# has_breach_response_plan == false → Write incident response plan
# has_dpia_for_high_risk == false AND high_risk_activities > 0 → Conduct DPIA
# has_ropa == false → Create ROPA (Art. 30 requires it for most businesses)

# Step 3: Quick verification
grep -l "data-protection\|privacy\|gdpr\|CCPA" policies/*.md | wc -l  # Policy coverage count
python3 scripts/check_cookie_banner.py --url https://example.com       # Exit 0 = compliant
python3 scripts/test_dsar_workflow.py                                  # Exit 0 = process works
```

**Principle:** `privacy_check.py` outputs a JSON compliance snapshot. Agent applies decision tree to rank actions by legal risk. No reading privacy policies into agent context (token waste). Cookie banner and DSAR checks use automated scripts returning exit codes.


<!-- DEEP: 10+min -->
