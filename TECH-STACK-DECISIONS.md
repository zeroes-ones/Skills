# Technology Stack Decision Framework

> **Author:** Sandeep Kumar Penchala  
> **Purpose:** Make wise, cost-effective tech stack decisions at every stage

---

## Decision Methodology

### Step 1: Constraint Discovery (5 minutes)

Before evaluating any technology, answer:

```
1. Team size now: ___    Team size in 12 months: ___
2. Current budget/month for infra: $___
3. Does this need to scale to > 100K users in 18 months? Y/N
4. Does the team already know a stack that could work? Y/N
5. Are there regulatory constraints? (HIPAA, PCI, FedRAMP, etc.) Y/N
6. What's the expected request volume? ___ req/s peak
7. Is real-time required? (WebSocket, SSE, polling) Y/N
8. Is offline support required? Y/N
```

### Step 2: Eliminate Non-Starters

| Constraint | Eliminates |
|------------|-----------|
| HIPAA compliance | Most startups tools — need BAA-ready providers |
| > 10K req/s from day 1 | Serverless cold starts — need always-warm compute |
| Team of 1-2 | Microservices, Kubernetes — too much ops overhead |
| Offline-first required | Server-rendered frameworks — need local-first architecture |
| < $500/month budget | Managed everything — need to self-host strategically |
| Must ship in 2 weeks | Custom anything — use batteries-included frameworks |

### Step 3: Stack Selection by Archetype

#### Archetype A: SaaS Web App (CRUD-heavy, B2B)

| Layer | MVP (0-1K users) | Growth (1K-100K) | Scale (100K+) |
|-------|------------------|-------------------|---------------|
| Frontend | Next.js / Remix | Same + CDN | Same + edge rendering |
| Backend | Next.js API / FastAPI | Same + worker queue | Dedicated API + BFF |
| Database | Supabase / PlanetScale | RDS + Redis cache | Sharded Postgres + Redis Cluster |
| Auth | NextAuth / Clerk | Same | Custom OIDC provider |
| Deployment | Vercel / Railway | AWS ECS / GCP Cloud Run | Multi-region K8s |
| Monthly Cost | $50-150 | $500-2,000 | $5,000-20,000 |

**When to choose Next.js:** React team, SEO matters, fullstack JS  
**When to choose Remix:** Web standards focus, progressive enhancement important  
**When to choose SPA + API:** Mobile app also needs API, separate frontend/backend teams  

#### Archetype B: API-First (Mobile backend, B2B integrations)

| Layer | MVP | Growth | Scale |
|-------|-----|--------|-------|
| Language | What team knows best | Same + performance profiling | May split by service needs |
| Framework | FastAPI (Python) / Hono (TS) / Echo (Go) | Same + gRPC for internal | Multi-protocol |
| Database | PostgreSQL (managed) | + Redis cache | + Read replicas, maybe sharding |
| API Gateway | Kong / built-in | Apigee / AWS API Gateway | Custom if needed |
| Message Queue | Redis / DB polling | RabbitMQ / SQS | Kafka |
| Monthly Cost | $100-300 | $1,000-5,000 | $10,000-50,000 |

**When Python/FastAPI:** AI/ML integration, data-heavy, rapid prototyping  
**When Go:** High concurrency, low latency requirement, networking  
**When TypeScript/Node:** Fullstack JS team, I/O heavy, real-time (WebSocket)  
**When Rust:** Performance-critical, WASM, systems-level  

#### Archetype C: Mobile App (Consumer-facing)

| Layer | MVP | Growth | Scale |
|-------|-----|--------|-------|
| Framework | React Native / Flutter | Same + native modules | May go full native for perf |
| Backend | BaaS (Firebase/Supabase) | Custom API | Custom everything |
| Real-time | Firebase Realtime DB | WebSocket service | Distributed WebSocket |
| Push | FCM/APNs direct | OneSignal/Firebase | Custom push service |
| Analytics | Firebase Analytics | Mixpanel/Amplitude | Custom + data warehouse |
| Monthly Cost | $25-100 | $500-2,000 | $5,000-25,000 |

**When React Native:** React web team, code sharing with web, rapid iteration  
**When Flutter:** Pixel-perfect custom UI, no web code sharing needed, small team  
**When Native (Swift/Kotlin):** GPU-intensive, AR/VR, heavy hardware integration, platform feel is market differentiator  

#### Archetype D: Data-Heavy (Analytics, ML platform)

| Layer | MVP | Growth | Scale |
|-------|-----|--------|-------|
| Data Warehouse | PostgreSQL | BigQuery / Snowflake | Custom + data mesh |
| ETL | Python scripts + cron | Airflow / Prefect | Dagster + dbt |
| Streaming | N/A | Kafka / Redpanda | Kafka + Flink |
| BI | Metabase (free) | Looker / Lightdash | Custom embedded |
| ML Serving | Flask API | FastAPI + MLflow | K8s + KServe |
| Monthly Cost | $100-500 | $2,000-10,000 | $20,000-100,000+ |

### Step 4: Cost Projection (2-Year TCO)

For each option, calculate:

```
Total Cost = Infra Cost + Engineer Time Cost + Migration Cost + Downtime Risk

Infra Cost = monthly bill × 24
Engineer Time = hours_per_week × hourly_rate × 104 weeks
Migration Cost = (one-time setup + data migration) × engineer hourly rate
Downtime Risk = estimated_hours_downtime × revenue_per_hour
```

**Example: Monolith vs Microservices (Team of 5, 10K users)**

| Factor | Monolith | Microservices |
|--------|----------|---------------|
| Infra (24 months) | $4,800 ($200/mo) | $24,000 ($1,000/mo) |
| Engineer time (ops) | $10,400 (2h/week) | $52,000 (10h/week) |
| Migration cost | $0 | $40,000 (3 months) |
| Downtime risk | $5,000 (rare) | $50,000 (more complex) |
| **Total 2-year** | **$20,200** | **$166,000** |

Decision: Monolith wins by $145,800 at this scale. Revisit at 100K users.

### Step 5: The "Regret Minimization" Check

Before finalizing, ask:

1. "If this stack dies in 2 years, can we migrate?" — Check community size, corporate backing
2. "Can we hire for this stack?" — Check LinkedIn/Indeed for local talent pool
3. "Does this stack have escape hatches?" — Can you eject? Is data portable?
4. "What's the lock-in surface area?" — Auth? Database? Deployment? All three = high risk

---

## Quick Decision Tables

### Database Selection

| Need | MVP Choice | Scale Choice |
|------|-----------|-------------|
| General web app | PostgreSQL | PostgreSQL + read replicas |
| Real-time sync | Supabase (Postgres+realtime) | Custom + CRDT |
| Full-text search | PostgreSQL built-in | Elasticsearch |
| Time-series | PostgreSQL + TimescaleDB | InfluxDB / ClickHouse |
| Graph data | PostgreSQL + CTEs | Neo4j |
| Cache | Redis (managed) | Redis Cluster |
| Queue/Jobs | PostgreSQL SKIP LOCKED | Redis/RabbitMQ/Kafka |
| Analytics | PostgreSQL (small) | BigQuery / ClickHouse |

### Frontend Framework Selection

| Need | MVP Choice | Why |
|------|-----------|-----|
| Marketing site | Astro | Zero JS by default, fastest |
| SaaS dashboard | Next.js | React ecosystem, SSR |
| E-commerce | Next.js / Remix | SEO critical |
| Real-time dashboard | Vite + React | No SSR overhead |
| Documentation site | Docusaurus / Starlight | Built for docs |
| Mobile app (cross-platform) | React Native / Flutter | Depends on team |
| Internal tools | Retool / React Admin | Build in hours, not weeks |

### Deployment Platform Selection

| Users | Best Choice | Monthly Cost | Why |
|-------|------------|-------------|-----|
| 0-1K | Vercel / Railway / Render | $20-50 | Zero DevOps |
| 1K-10K | Railway + RDS / Fly.io | $100-500 | Simple scale |
| 10K-100K | AWS ECS / GCP Cloud Run | $500-3,000 | Managed containers |
| 100K-1M | EKS / GKE (Managed K8s) | $3,000-15,000 | Full control |
| 1M+ | Multi-cloud K8s | $15,000+ | No single cloud risk |

---

*Every technology decision in every skill should reference this framework.*
