# Token-Efficient Workflow

```
# Step 1: Quick diagnostic — what's the #1 growth bottleneck?
python3 scripts/growth_diagnostic.py \
  --signups 5000 --activation-rate 0.25 --d7-retention 0.40 --referral-rate 0.05 \
  --output json
# Returns: {"bottleneck":"activation","score":0.25,"benchmark":0.40,"gap_pct":-37.5}

# Step 2: Decision tree → pick the lever
# Bottleneck = activation → onboarding experiment (reduce time-to-aha)
# Bottleneck = retention → re-engagement experiment (email/push cadence)
# Bottleneck = referral → incentive experiment (single-sided vs double-sided reward)
# Bottleneck = acquisition → channel experiment (new paid/organic channel test)

# Step 3: Quick experiment setup — feature flag + analytics event
# Create feature flag (simplest: config key)
echo '{"onboarding_v2": {"enabled": true, "rollout": 0.5}}' > flags/onboarding.json

# Track variant in analytics
# In code: analytics.track('user_signup', {variant: getUserVariant('onboarding_v2')})

# Step 4: Verify after 7-14 days with exit code
python3 scripts/analyze_experiment.py \
  --metric activation_rate --control 0.25 --treatment 0.31 --n 2000 \
  --output json  # Returns: {"significant":true,"lift":0.24,"p_value":0.003}
# Exit code 0 = significant winner, 1 = inconclusive, 2 = significant loser
```

**Principle:** `growth_diagnostic.py` outputs JSON with one bottleneck. Agent follows decision tree to exactly one action. Analysis script outputs exit code for significance. No parsing prose output.
