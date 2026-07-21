# LogSnap MVP — Architecture Decisions

## ADR 1: Monolith (Go)

I'm one person. Microservices add deployment complexity, network latency, and a distributed debugging nightmare with zero benefit at this scale. One Go binary, one `systemd` service, one log file to grep at 3am. Code is organized into packages (`handlers/`, `checks/`, `alerts/`, `billing/`) — clean enough to extract later, not so abstract I'm building infrastructure for scale I don't have.

## ADR 2: PostgreSQL (Single Instance)

Monitoring data is relational: checks belong to monitors, monitors belong to teams, alert rules reference monitors. I need joins and foreign keys. SQLite for local dev (`go run .` against a file, zero setup), Postgres in prod via Docker Compose. No read replicas — a single instance handles thousands of reads per second, and the check runner writes at ~1.7 writes/second at 100 monitors.

## ADR 3: Cron-Based Checks (Go Goroutines)

No Kafka. No RabbitMQ. No Redis queues. At 100 monitors × 1 check/min, that's 144K checks/day — 1.7 checks/second. A goroutine per active monitor with a `time.Ticker` handles this trivially. A scheduler goroutine watches a channel, spawning or canceling check goroutines as monitors are added or removed. Zero infrastructure dependencies. Won't bottleneck until north of 10,000 monitors — I'll revisit then.

## ADR 4: Next.js for Frontend (SSR for Status Pages)

Status pages are the differentiator. They must be public, fast, SEO-friendly, and available even if the API is degraded. Next.js ISR gives me this: pre-rendered at build time, revalidated every 60 seconds, served as static HTML. Dashboard pages behind auth are client-side — nobody SEO-optimizes their monitor list. One framework, both use cases.

## ADR 5: Single VPS ($20/mo Hetzner or DigitalOcean)

Docker Compose: Go binary + Postgres + optional Redis. Caddy for auto-SSL (zero config). Daily `pg_dump` to S3 via cron. If the server dies, I'm down for an hour while I restore — acceptable for an MVP at $9/month. High availability is phase 2.

## What I'm Deliberately NOT Building

- **Public API**: No customer has asked. When they do, I'll design against real use cases.
- **Webhooks**: Email alerts cover the MVP. Slack/Discord is phase 2.
- **Multi-region checks**: One region catches 80% of outages. Add regions when a customer reports a false positive.
- **Full auth**: Magic link via email. No passwords, no OAuth, no 2FA. Simple and secure enough.
