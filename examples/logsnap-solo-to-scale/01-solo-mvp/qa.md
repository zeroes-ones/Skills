# LogSnap MVP — QA

## Test Strategy

Manual only. No CI suite, no Playwright, no Selenium. Shipping to maybe 50 people from a Product Hunt launch — ROI on automated tests at this stage is negative. Structured 18-case manual session two hours before launch. All pass? Ship. Any fail? Fix and re-test.

## Test Cases

### Happy Path (6)

1. **Add monitor**: Valid URL, 60s interval. Appears with "Checking..." then turns green within 60s.
2. **Check runs**: Verify record inserted with `status_code: 200`, response time, region.
3. **Status page**: `/status/{team_slug}` — all monitors display with green dots and uptime %.
4. **Alert fires**: Stop test endpoint. Alert email delivered within 120s (two cycles × 3 regions).
5. **Alert resolves**: Restart endpoint. "RESOLVED" email arrives within 120s with downtime duration.
6. **Stripe checkout**: `checkout.session.completed` webhook → team `is_active` flips to `true`.

### Edge Cases (6)

7. **URL redirect (301/302)**: Follows redirect, records final status code. Green if 2xx.
8. **URL returning 500**: Records `status_code: 500`. Red dot. Alert fires after threshold.
9. **URL times out**: HTTP client timeout at 10s. Check records as failure, not "no data."
10. **Very long URL (2048+ chars)**: Validation rejects with friendly error. DB column is `VARCHAR(2048)`.
11. **IDN domain**: `münchen.de` → punycode → checked → displayed as original Unicode.
12. **Concurrent checks**: 50 monitors added simultaneously. No goroutine leaks, no data races.

### Error Cases (6)

13. **Invalid URL**: `not-a-url` → "Please enter a valid URL starting with http:// or https://".
14. **Duplicate monitor**: Same URL twice → "This URL is already being monitored."
15. **Deleted monitor**: Navigate to `/monitors/deleted-id` → 404 page, not blank screen or panic.
16. **Expired token**: Wait 16 min (15-min expiry), use magic link → "Link expired. Request a new one."
17. **Bad Stripe webhook**: Invalid signature → 400 logged, no activation. Stripe retries.
18. **DB connection lost**: Postgres restarts mid-check. Runner logs error, retries next tick.

## Bugs Found and Fixed

**Bug 1 — Silent timeout**: HTTP client timeout was 30s but check interval was 60s. Timeouts logged as "no response." **Fix**: Timeout to 55s (just under interval), log as "degraded" with reason.

**Bug 2 — Empty check panic**: Status page called `checks[0].status_code` on empty array → server panic. **Fix**: Guard with `len(checks) == 0`, render "Waiting for first check…"

**Bug 3 — Alert flap spam**: Monitor flapping (down-up-down) sent three separate alert emails. **Fix**: Require 3 consecutive UP checks before a DOWN triggers new alert. Prevents email storms.

## Performance Baseline

- Dashboard: under 500ms with 50 monitors (cold client-side render).
- Status page (ISR, cached): under 200ms.
- Check runner: 100 monitors at 1.7 checks/sec, CPU at 2–3% on a single core.
- Postgres: ~100 inserts/sec at 6,000 checks/min. Any Postgres instance handles this.

## Ship Criteria

Manual test session, 2 hours before Product Hunt launch. All 18 cases pass. Any failure → fix → re-run full suite. No partial passes. Ship it.
