# LogSnap MVP — Backend

## Stack

Go 1.22. Single `main.go` wires up the router, starts the check scheduler, listens on `:8080`. Business logic in `handlers/` package. Compiles to one binary. Deploy: `scp` + `systemctl restart`.

## Routes (7 total)

```
POST   /api/monitors              — Create monitor
GET    /api/monitors              — List monitors (auth'd team)
GET    /api/monitors/:id          — Single monitor + latest check
DELETE /api/monitors/:id          — Delete monitor + cascading checks
GET    /api/monitors/:id/checks   — Paginated check history (24h default)
POST   /api/alerts/rules          — Create/update alert rule per monitor
GET    /status/:team_slug         — Public status page (no auth)
```

No PUT, PATCH, or batch endpoints. CRUD for monitors, one alert rule endpoint, one public status endpoint.

## Database Schema (4 tables)

- **teams**: `id`, `name`, `slug`, `stripe_customer_id`, `stripe_subscription_id`, `is_active`, `created_at`
- **monitors**: `id`, `team_id` (FK), `url`, `check_interval_seconds` (default 60), `is_active`, `created_at`
- **checks**: `id`, `monitor_id` (FK), `status_code`, `response_time_ms`, `region`, `checked_at` — indexed `(monitor_id, checked_at)`
- **alert_rules**: `id`, `monitor_id` (FK, unique), `failure_threshold` (default 2), `notification_email`, `created_at`

No migrations framework. A `schema.sql` applied via Docker entrypoint.

## Check Runner

Goroutine per active monitor, managed by a scheduler watching a `monitorChanges` channel. Each goroutine: HTTP GET with 10s timeout, insert check row, evaluate alert rule. If the last N checks all failed (threshold) and no alert was sent in 5 minutes (dedup window), fire an email. At 100 monitors × 1 check/min = 1.7 checks/sec. A single Go process handles this with ~50MB memory overhead. Not a problem until 10K+ monitors.

## Alert Delivery

Resend free tier: 100 emails/day — plenty for MVP. Plain text template:

```
Subject: ALERT: {name} is DOWN
{name} ({url}) returned HTTP {status_code} at {time}.
{regions_down}/{total_regions} regions confirmed outage.
```

On recovery: "RESOLVED" email with downtime duration. No HTML — plain text gets delivered and read.

## Authentication

Magic link only. `POST /api/auth/login` → email with 15-min signed token → `GET /api/auth/callback?token=` → validates token, creates team if new, sets JWT cookie (24h expiry). No passwords, OAuth, or 2FA. Secure enough, zero friction signup.

## Stripe Integration

Single tier: $9/month, 10 monitors. Stripe Checkout handles payment — I build zero billing UI. Two webhooks: `checkout.session.completed` (activate team), `customer.subscription.deleted` (deactivate). Handler verifies signature, looks up team by `stripe_customer_id`, toggles `is_active`. No proration, no upgrade/downgrade, no invoice hosting.
