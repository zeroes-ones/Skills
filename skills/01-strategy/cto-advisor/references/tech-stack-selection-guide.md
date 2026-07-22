---
author: Sandeep Kumar Penchala
type: reference
domain: technology-strategy
version: "1.0"
last_updated: 2026-07-21
parent_skill: cto-advisor
---

# Technology Stack Selection Guide

> **Author:** Sandeep Kumar Penchala

Systematic framework for selecting languages, frameworks, databases, and infrastructure for new projects. Covers archetype-based recommendations, language trade-offs, database selection, infrastructure scaling, and maturity assessment. Use alongside the CTO Advisor skill's architecture and build-vs-buy frameworks.

---

## 1. Stack Selection by Project Archetype

### SaaS B2B (Web-first, multi-tenant)
```
Frontend:   React (Next.js) or Vue (Nuxt)
Backend:    Python (Django/FastAPI) or TypeScript (NestJS)
Database:   PostgreSQL (primary), Redis (cache/sessions)
Infra:      AWS/GCP, Docker, Kubernetes (at scale)
Auth:       Auth0 / Clerk
Payments:   Stripe
```
**Why:** Python/TS maximizes hiring pool. PostgreSQL handles complex relational data (permissions, billing). Next.js for SSR + SEO on public pages.

### B2C Mobile-First
```
Mobile:     React Native or Flutter (cross-platform), Swift/Kotlin (native)
Backend:    Go or TypeScript (Node.js) — high concurrency
Database:   PostgreSQL + Redis, MongoDB for content-heavy features
Infra:      AWS/GCP, serverless for spikes, CDN for media
Real-time:  WebSocket via Go/Node.js
```
**Why:** Go/Node.js handles high connection counts. Cross-platform saves 40% engineering time. Redis for session and caching under bursty consumer traffic.

### E-Commerce
```
Frontend:   Next.js (headless) or Shopify Hydrogen
Backend:    TypeScript (Node.js) or Python (Django)
Database:   PostgreSQL (orders, inventory), Elasticsearch (search)
Infra:      Vercel/Netlify (frontend), AWS (backend), CDN-heavy
Payments:   Stripe / Adyen
Search:     Algolia or Elasticsearch
```
**Why:** Headless commerce decouples frontend experimentation from backend stability. Elasticsearch handles faceted search. PostgreSQL for ACID on orders and inventory.

### Data-Heavy / Analytics Platform
```
Backend:    Python (data processing) or Go (API layer)
Database:   PostgreSQL (OLTP) + ClickHouse/BigQuery (OLAP)
Pipeline:   Kafka/PubSub → dbt → warehouse → BI tool
Infra:      Kubernetes for services, managed warehouse
ML:         Python (PyTorch, scikit-learn), Jupyter
```
**Why:** Python dominates data/ML ecosystem. ClickHouse for sub-second analytical queries. Kafka for streaming reliability.

### Real-Time / Low-Latency
```
Backend:    Go or Rust (hot path), Python/TS (control plane)
Database:   PostgreSQL, Redis, ScyllaDB/DynamoDB
Messaging:  NATS or Kafka
Infra:      Kubernetes, edge compute (Cloudflare Workers)
```
**Why:** Go/Rust for <10ms p99 latency. NATS for ultra-low-latency messaging. ScyllaDB for write-heavy workloads.

---

## 2. Language & Framework Comparison

| Language | Pros | Cons | Best For |
|----------|------|------|----------|
| **Python** | Largest ML/data ecosystem; fast prototyping; huge hiring pool; Django admin | GIL limits CPU parallelism; dynamic typing at scale; slower runtime | Data/ML, SaaS backends, internal tools, API servers |
| **TypeScript** | Full-stack with one language; huge npm ecosystem; type safety; Next.js/NestJS | Node.js single-threaded; npm supply chain risk; fast-moving ecosystem | Web apps, full-stack SaaS, B2C, real-time |
| **Go** | Excellent concurrency; fast compile; single binary deploy; low memory | Verbose error handling; limited generics (improving); smaller ecosystem | APIs, microservices, CLI tools, networking, infra |
| **Rust** | Memory safety without GC; top performance; excellent tooling (Cargo) | Steep learning curve; slower development speed; smaller hiring pool | Systems programming, WASM, performance-critical paths |
| **Java / Kotlin** | Mature ecosystem (Spring); JVM performance; strong typing; huge talent pool | Verbose; slower startup; memory overhead; less agile iteration | Enterprise, fintech, Android, large-scale backend |

### Framework Quick-Pick

| Task | Python | TypeScript | Go | Java |
|------|--------|------------|----|----- |
| REST API | FastAPI, Django REST | NestJS, Express, Hono | Gin, Chi, Echo | Spring Boot |
| GraphQL | Strawberry, Graphene | Apollo Server, Yoga | gqlgen | DGS (Netflix) |
| Full-stack web | Django | Next.js, Remix | — | — |
| Async tasks | Celery, Dramatiq | BullMQ | Asynq, River | — |
| gRPC | grpcio | @grpc/grpc-js | native | grpc-java |

---

## 3. Database Selection Framework

| Database | Strengths | Weaknesses | When It Wins |
|----------|-----------|------------|--------------|
| **PostgreSQL** | ACID, JSONB, full-text search, extensions, mature | Vertical scaling ceiling; complex HA setup | **Default choice.** 95% of apps. Anything relational + some document needs. |
| **MySQL** | Widely hosted; read replicas; battle-tested | Fewer features than PG; JSON support weaker | Legacy Laravel/WordPress; when cloud provider forces it |
| **MongoDB** | Flexible schema; horizontal scaling; good for rapid iteration | Loses ACID across shards; query language; no joins | Content-heavy apps, catalogs, IoT data, rapid prototyping with unknown schema |
| **DynamoDB** | Infinite scale; predictable latency; fully managed | Rigid access patterns; no ad-hoc queries; expensive at scale without planning | High-scale key-value; serverless apps; known access patterns |
| **Redis** | Sub-ms latency; data structures (streams, sets, sorted sets) | In-memory = expensive for large datasets; persistence is secondary | Caching, rate limiting, queues, real-time leaderboards, session store |
| **Elasticsearch** | Full-text search; aggregations; kibana dashboards | Operational complexity; resource hungry; eventual consistency | Search-heavy apps, log analytics, product catalogs with faceted search |
| **ClickHouse** | Columnar: sub-second on billions of rows; real-time ingest | Not for OLTP; limited updates; operational learning curve | Analytics, event data, time-series, user behavior analysis |

### Selection flowchart
```
Is data relational with complex joins?
├── YES → PostgreSQL
└── NO → Is schema evolving rapidly?
    ├── YES → MongoDB (document model)
    └── NO → Is access pattern purely key-value at massive scale?
        ├── YES → DynamoDB
        └── NO → Is it a cache or ephemeral data?
            ├── YES → Redis
            └── NO → PostgreSQL (seriously, just use PostgreSQL)
```

---

## 4. Infrastructure Choices by Scale

| Stage | Users | Architecture | Cost (est.) | Team needs |
|-------|-------|-------------|-------------|------------|
| **MVP / Pre-seed** | 0–1K | VPS (Hetzner/DigitalOcean) or PaaS (Render/Fly.io/Railway) | $50–500/mo | 1–2 engineers |
| **Seed** | 1K–50K | PaaS + managed DB (RDS, Planetscale) + CDN | $500–5K/mo | 3–8 engineers |
| **Growth / Series A** | 50K–500K | Containers (ECS/Fargate) or Kubernetes (GKE/EKS) + microservices | $5K–50K/mo | 8–25 engineers, dedicated infra person |
| **Scale / Series B** | 500K–10M | Kubernetes (multi-AZ), service mesh, event-driven, multi-region | $50K–200K/mo | 25+ engineers, platform team |
| **Hyper-scale** | 10M+ | Multi-cloud, edge compute, custom hardware | $200K+/mo | Dedicated infra/performance org |

### Infrastructure decision heuristic
```
if team_size < 5 and time_to_market_critical → PaaS (Render, Railway, Fly.io)
if team_size 5–15 and need_control → Containers on managed K8s (GKE, EKS)
if team_size > 15 and compliance_needed → Self-managed or hybrid
if serverless_fit → Lambda/Cloud Functions for event-driven; NOT for latency-sensitive
```

---

## 5. Stack Maturity Assessment

Score each candidate stack 1–5 on these dimensions:

| Dimension | Weight | How to Assess |
|-----------|--------|---------------|
| **Community size** | 25% | GitHub stars, Stack Overflow questions, conference talks, meetup groups |
| **Hiring pool** | 25% | LinkedIn search volume, Hired.com supply, bootcamp output, salary benchmarks |
| **Long-term viability** | 20% | Corporate backing (foundation vs single vendor); release cadence; backward compat |
| **Ecosystem** | 15% | Package count, library quality for your use case, integration maturity |
| **Learning curve** | 10% | Time-to-productivity for new hires; documentation quality; onboarding materials |
| **Performance ceiling** | 5% | Does it scale to your 3-year projected load without rewrite? |

### Stack maturity thresholds
- **Tier 1 (Safe Bet):** Score ≥ 4.0 — e.g., React, PostgreSQL, Python, AWS
- **Tier 2 (Evaluate):** Score 3.0–3.9 — e.g., Svelte, Go, Supabase, Fly.io
- **Tier 3 (Risky):** Score < 3.0 — use only if it provides decisive competitive advantage

### Anti-patterns to avoid
1. **Resume-driven development** — choosing a stack because engineers want to learn it
2. **Over-engineering for scale** — building for 10M users when you have 500
3. **Single-vendor lock-in without escape plan** — always have a migration path documented
4. **Mismatched team skills** — choosing Rust when your team knows Python; factor retraining time into timeline
5. **Ignoring operational maturity** — new database with no hosted offering, no backup tooling, no monitoring

---

See also: CTO Advisor skill for architecture decisions, build-vs-buy analysis, and technical roadmap planning.
