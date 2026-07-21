# LogSnap MVP — Product Spec

## Problem

Indie hackers are stuck. Free monitoring (UptimeRobot, cron jobs hitting `/health`) works fine internally, but the moment you share a status page with paying customers, it looks amateur. Nobody trusts a SaaS whose status page is a Notion embed. Meanwhile, "real" tools cost real money: Better Uptime at $24/month, Statuspage at $99/month. When your MRR is $400, tripling your tooling cost for a prettier status page feels irresponsible. Result: indie hackers either skip status pages entirely (bad look) or waste hours duct-taping free tools together.

## Solution

LogSnap: dead-simple uptime monitoring with a beautiful public status page, $9/month. Paste a URL, pick an alert email, and within 60 seconds you've got a professional status page in your footer. No YAML, no webhooks, no configuration files. Just a URL and an email.

## Core Features (MVP)

- Add a URL, set check interval (default 60s), done.
- 60-second checks from 3 geographic regions. One region down = degraded. Two down = alert.
- Email alert via Resend within 30 seconds of confirmed failure.
- Public status page: team name, monitor list with green/red dots, last checked time, 90-day uptime %. SSR + ISR — fast, SEO-friendly, available even if the dashboard is down.
- Stripe checkout: single plan, $9/month, 10 monitors. No free trial. Cancel anytime.

## Explicitly Out of Scope

Team accounts, SSO, SMS/call alerts, public API, custom domains, Slack/Discord integrations, incident templates, white-label, logo upload, multi-user, audit logs.

## Success Metric

**1 paying customer in 30 days.** Product Hunt launch on day 28. If nobody pays, the product doesn't exist.

## Target User

Indie hacker with a SaaS that has 50–500 paying customers. Makes enough to care about perception, not enough to justify Atlassian pricing. Has been burned by a customer emailing "hey, your site is down."

## Competitor Comparison

| Tool | Price | Status Page | Verdict |
|------|-------|-------------|---------|
| Better Uptime | $24/mo | Yes, overkill | Too expensive for side projects |
| UptimeRobot | Free | Ugly, no branding | Free costs you credibility |
| Statuspage | $99/mo | Enterprise | Too much complexity |
| **LogSnap** | **$9/mo** | **Yes, beautiful** | **The gap** |
