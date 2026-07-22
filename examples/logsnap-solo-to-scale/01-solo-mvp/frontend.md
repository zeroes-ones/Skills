# LogSnap MVP — Frontend

## Stack

Next.js 14 (App Router), TypeScript, Tailwind CSS. No component library — Radix and shadcn add 200KB of JS I don't need for six screens. Tailwind utilities give consistency without abstraction overhead.

## Pages (6 routes)

- `/dashboard` — Monitor list with status dots, uptime %, "Add Monitor" button. Home screen.
- `/monitors/new` — URL input, interval dropdown, alert email. Three fields, one button.
- `/monitors/[id]` — 24h uptime sparkline, check history table (paginated, 50 checks), attached alert rule.
- `/alerts` — Alert rules list, one per monitor. Edit inline. No separate edit page.
- `/settings` — Team name (editable), Stripe billing portal link. That's it.
- `/status/[team_slug]` — Public status page. The storefront.

## Data Fetching

Split by audience:

- **Status page** (public, SEO-critical): Server Component with ISR, `revalidate = 60`. Pre-rendered static HTML, regenerated in background. Loads under 200ms. Indexed by Google.

- **Dashboard + admin** (behind auth, real-time): Client Components with SWR, `refreshInterval: 10000`. For 50 monitors, the payload is ~300 bytes of JSON. At 100 concurrent users, that's 30KB/sec — trivial for the single VPS.

- **Monitor detail**: SWR for sparkline + latest check. Check history fetched once on mount with "Load more" pagination. No infinite scroll — simpler and the use case doesn't benefit.

## Real-Time Updates

Polling, not WebSockets. A 10-second interval gives the perception of real-time without connection management, reconnection logic, or persistent server overhead. Too slow? Drop to 5 seconds. Server groaning? Bump to 30. Polling is a knob; WebSockets are a commitment.

## The "Instant Feedback" Loop

Core UX hook: user adds a monitor → row appears with gray "Checking..." badge + pulsing spinner → SWR picks it up next cycle → first check completes (under 60s) → row flips from gray spinner to green dot with "Operational." The user watches their site go from unknown to confirmed-up in under a minute. That moment — typing a URL and watching it turn green — is what gets credit cards pulled out.

## Status Page Component Tree

```
StatusPage (Server Component)
├── TeamName (h1, centered)
├── MonitorList
│   └── MonitorStatusRow
│       ├── MonitorName (left)
│       ├── StatusDot (green | red, right)
│       ├── LastChecked ("Checked 32s ago", muted)
│       └── UptimeBadge (pill, "99.97%")
└── Footer ("Powered by LogSnap" — free marketing)
```

Deliberately sparse. No charts, no incident timelines, no "subscribe" forms. Answers one question — "is the service up?" — and gets out of the way. Complexity is phase 2.
