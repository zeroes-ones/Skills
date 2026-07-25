## Cost Optimization Matrix

<!-- SIGNATURE FEATURE: Cost ladders for common tool categories -->

For ANY tool category, provide a cost ladder from $0 to enterprise. Below are reference ladders for the most commonly evaluated categories.

### 1. Authentication & Identity

| Tier | Solution | Cost/Month | When to Use |
|------|----------|-----------|-------------|
| $0 | NextAuth.js / Auth.js + GitHub OAuth | $0 (self-host) | MVP, side projects, <1K users |
| $0 | Lucia Auth (OSS, framework-agnostic) | $0 (self-host) | When you want database-owner auth with no vendor lock-in |
| $0-25 | Clerk (free up to 10K MAU) | $0-25 | Growing startups, React/Next.js apps, social login needed |
| $0-25 | Supabase Auth (free up to 50K MAU) | $0-25 | When already using Supabase for database/storage |
| $25-100 | Auth0 (B2C Essentials, 1K-10K MAU) | $25-100 | SMB, B2B SaaS, need SAML/OIDC enterprise connections |
| $100-500 | WorkOS (AuthKit) | $100-500 | B2B SaaS needing enterprise SSO, SCIM, directory sync |
| $500+ | Okta / Azure AD B2C / Ping Identity | $500-5,000+ | Enterprise, SOC2/HIPAA/FedRAMP, >50K employees |

### 2. Hosting & Deployment

| Tier | Solution | Cost/Month | When to Use |
|------|----------|-----------|-------------|
| $0 | Vercel (Hobby), Netlify (Starter), Cloudflare Pages | $0 | Static sites, JAMstack, personal projects |
| $0-20 | Vercel (Pro), Railway (Hobby), Fly.io (free allowance) | $0-20 | Small SaaS, side projects with backend, <100K requests |
| $20-100 | Railway (Pro), Render, Fly.io (scale-up) | $20-100 | Growing SaaS, 100K-1M requests/month, need databases |
| $100-500 | AWS ECS + RDS (small), GCP Cloud Run, DigitalOcean App Platform | $100-500 | Production SaaS, 1M-10M requests/month, multi-region |
| $500-2K | AWS EKS/GCP GKE (managed K8s), multi-AZ RDS, CloudFront | $500-2,000 | Scale-up phase, >10M requests, need auto-scaling + multi-region |
| $2K+ | Enterprise AWS/GCP/Azure with reserved instances, private link, dedicated support | $2,000-20,000+ | Enterprise, compliance, dedicated infrastructure, SLA-backed |

### 3. Databases

| Tier | Solution | Cost/Month | When to Use |
|------|----------|-----------|-------------|
| $0 | SQLite (Turso free), Supabase (free tier), Neon (free tier) | $0 | Prototypes, small projects, <500MB data, <100 concurrent users |
| $0-25 | Supabase (Pro $25), PlanetScale (Scaler $29), Turso (Scaler $9) | $0-29 | Startups, 1-10GB data, need backups + branching + pooled connections |
| $25-100 | Railway PostgreSQL, Render PostgreSQL, AWS RDS (t3.small) | $25-100 | Production, 10-100GB, need managed backups + monitoring + multi-AZ |
| $100-500 | AWS RDS (multi-AZ, Provisioned IOPS), GCP Cloud SQL (HA) | $100-500 | Scale-up, 100GB-1TB, need read replicas + point-in-time recovery |
| $500+ | AWS Aurora, CockroachDB Cloud, PlanetScale Enterprise | $500-3,000+ | Global scale, >1TB, multi-region, auto-sharding, enterprise SLA |

### 4. Monitoring & Observability

| Tier | Solution | Cost/Month | When to Use |
|------|----------|-----------|-------------|
| $0 | Grafana + Prometheus + Loki (self-hosted), Sentry (free tier) | $0 (self-host) | Small projects, can manage own infra, <1M metrics series |
| $0-30 | Grafana Cloud (free 10K series), SigNoz (OSS self-host), Better Stack (free) | $0-30 | Startups, need managed metrics + logs, <50M events |
| $30-150 | Datadog (Infrastructure $15/host), New Relic (Standard), Grafana Cloud Pro | $30-150 | Growing SaaS, 10-100 hosts, need APM + distributed tracing + dashboards |
| $150-500 | Datadog (APM $40/host + logs), Honeycomb (Pro $150/seat) | $150-500 | Scale-up, >100 hosts, need high-cardinality analytics + SLO tracking |
| $500+ | Datadog Enterprise, Splunk, New Relic Enterprise | $500-10,000+ | Enterprise, compliance retention, dedicated support, SSO, audit logging |

### 5. Email Delivery

| Tier | Solution | Cost/Month | When to Use |
|------|----------|-----------|-------------|
| $0 | Resend (100 emails/day), SendGrid (100 emails/day free), Mailgun (flex free) | $0 | MVPs, low-volume transactional, password resets only |
| $0-35 | Resend (50K emails $20), Postmark (10K emails $15), SES ($0.10/1K emails) | $0-35 | Startups, transactional + marketing, <100K emails/month |
| $35-100 | Postmark (50K emails $55), SendGrid (50K emails $35), Mailgun Foundation $35 | $35-100 | Growing SaaS, need dedicated IP + suppression management + analytics |
| $100-500 | Postmark (300K emails), SendGrid Pro, Mailgun Scale | $100-500 | Scale-up, >500K emails/month, need sub-accounts + team management |
| $500+ | Postmark Enterprise, SendGrid Enterprise, dedicated sending infrastructure | $500-5,000+ | Enterprise, >5M emails/month, dedicated IP pools, deliverability consulting |

### 6. Payment Processing

| Tier | Solution | Cost/Month | When to Use |
|------|----------|-----------|-------------|
| $0 | Stripe (2.9% + 30¢/transaction), LemonSqueezy (5% + 50¢) | $0/mo + per-transaction | All stages — pay-as-you-go, no monthly fee |
| $0-50 | Paddle ($0 monthly, 5% + 50¢), Gumroad (10% flat) | $0-50 effective | Need merchant-of-record (handles global tax/VAT), digital products |
| $50-200 | Stripe + Stripe Billing, Chargebee (Starter $0 then scales), Recurly (Core $199) | $50-200 | SaaS with subscription management, dunning, invoicing, revenue recognition |
| $200-1K | Chargebee (Performance $599), Recurly (Elite), Stripe Enterprise | $200-1,000 | Scale-up, complex subscription logic, multi-currency, advanced analytics |
| $1K+ | Adyen, Braintree Enterprise, custom merchant accounts | $1,000-10,000+ | Enterprise, >$10M annual volume, need interchange+ pricing, multi-country acquiring |

### Cost Optimization Principles:
- **Start at $0 for every category.** Even if you have budget, evaluate the free tier first. You can always upgrade. Upgrading is easy; downgrading is painful.
- **The jump from $0 to $25 is the most important.** This is where you go from "works for demos" to "works for production." Know exactly what that $25 buys.
- **Self-hosting saves subscription fees but costs engineering time.** At $150/hr fully loaded engineering cost, 10 hours/month of maintenance = $1,500/month. Is the SaaS tool cheaper?
- **Enterprise pricing is negotiable.** Never pay list price for enterprise tiers. Expect 20-40% discount with annual commitment and 40-60% with multi-year.
- **Bundle where it makes sense.** Supabase = database + auth + storage + realtime. Vercel = hosting + analytics + edge functions. Bundles reduce integration cost and vendor count.
