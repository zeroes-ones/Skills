# Engineering Wisdom Framework

> **Author:** Sandeep Kumar Penchala  
> **Purpose:** Universal decision-making principles applied across all skills

---

## Core Principles

### 1. Token Efficiency (Save Agent Context)

Every skill must minimize token consumption:

| Principle | Implementation |
|-----------|---------------|
| **Scripts as black boxes** | Run `python script.py --help`, invoke directly. NEVER read script source into context unless debugging. |
| **References on demand** | Deep knowledge lives in `references/`. Agent loads only the specific guide needed for the current task. |
| **Decision trees first** | Put the decision framework in SKILL.md. Put detailed implementation in references. |
| **Exact commands** | Write copy-paste ready commands, not descriptions of commands. |
| **Fail fast** | Return non-zero exit codes for quality gates. Agent doesn't need to parse output — exit code is enough. |

**Anti-pattern:** A 500-line SKILL.md that the agent reads entirely for every invocation.  
**Pattern:** A 150-line SKILL.md with 5 references (each 200+ lines) loaded only when relevant.

### 2. MVP-First Thinking

Every skill must distinguish between MVP, growth, and scale phases:

| Phase | Team Size | Users | Priority | Architecture |
|-------|-----------|-------|----------|-------------|
| **MVP (0→1)** | 1-3 devs | 0-1K | Speed to validation | Monolith on PaaS (Railway/Render/Vercel) |
| **Growth (1→10)** | 3-15 devs | 1K-100K | Feature velocity | Modular monolith + managed services |
| **Scale (10→N)** | 15+ devs | 100K+ | Reliability, cost | Microservices, multi-region, custom infra |

**MVP Golden Rules:**
1. Ship in 2 weeks, not 2 months. Cut scope ruthlessly.
2. Manual ops are fine. Automate when it becomes painful, not before.
3. One database, one backend, one frontend. Add services only when you have a scaling problem.
4. Use managed everything. Self-host only when managed costs exceed engineer salary.
5. Track 3 metrics: Does it work? Do users come back? Does revenue cover costs?

### 3. Tech Stack Decision Framework

Choose technology based on these dimensions, weighted by phase:

| Factor | MVP Weight | Growth Weight | Scale Weight |
|--------|-----------|---------------|-------------|
| Time to first feature | 40% | 20% | 5% |
| Hiring pool size | 25% | 35% | 30% |
| Ecosystem maturity | 15% | 20% | 25% |
| Performance ceiling | 5% | 15% | 25% |
| Operational cost at scale | 5% | 5% | 10% |
| Long-term maintainability | 10% | 5% | 5% |

**Decision Process:**
1. Start with the stack your team already knows
2. Add new technology only when the existing stack CANNOT solve the problem
3. Every new technology = ongoing cost: learning, maintenance, hiring, integration
4. Monorepo by default. Multi-repo only when you need independent deploy cycles.

### 4. Cost-Effective Deployment Strategy

| Users | Compute | Database | Frontend | Monthly Cost |
|-------|---------|----------|----------|-------------|
| 0-1K | 1 VM / serverless | Managed (RDS/Supabase/PlanetScale) | Vercel/Netlify | $50-200 |
| 1K-10K | 2-3 VMs + CDN | Managed with read replicas | Vercel Pro/CloudFlare | $500-2K |
| 10K-100K | K8s cluster / ECS | Managed HA + caching layer | CDN + edge functions | $2K-10K |
| 100K-1M | Multi-AZ K8s | Sharded DB + Redis cluster | Multi-region CDN | $10K-50K |
| 1M+ | Custom everything | Custom everything | Custom edge | $50K+ |

**Cost optimization checklist:**
1. Reserve instances / committed use for predictable workloads (40-60% savings)
2. Spot/preemptible for batch jobs, CI, dev environments (70-90% savings)
3. Right-size — most workloads use < 30% of allocated resources
4. Delete unused resources automatically (tag everything, audit monthly)
5. CDN-first — serve from edge, reduce origin load
6. Tiered storage — hot (SSD) → warm (HDD) → cold (object storage) → archive (glacier)

### 5. Scalability Without Over-Engineering

**The Scalability Decision Tree:**

```
Do you have a scaling problem RIGHT NOW?
├── YES → Measure the bottleneck → Fix only that → Repeat
└── NO → Don't "prepare for scale." Ship features.

Has your monolith become hard to deploy (merge conflicts, slow CI)?
├── YES → Extract 1 bounded context into a separate service
└── NO → Keep the monolith. It's working.

Is your database CPU consistently > 70%?
├── YES → Add read replicas → If still high, shard by tenant/region
└── NO → Don't shard. Don't add replicas.

Is latency > 200ms p95 for critical paths?
├── YES → Profile → Add caching → Optimize queries → Async what can be async
└── NO → You're fine. Ship features.
```

**When to ADD complexity:**
- Daily active users > 100K → Add caching layer
- DB CPU > 70% sustained → Add read replicas
- CI pipeline > 15 min → Parallelize / split services
- Deployment risk is high → Add feature flags, canary deploys
- Multiple teams stepping on each other → Extract bounded context

**When to REMOVE complexity:**
- Service handles < 100 req/min → Merge back into monolith
- Cache hit rate < 50% → Remove cache (it's just adding latency)
- Feature flag is 6+ months old → Remove the flag, keep the feature
- Microservice has 1 consumer → It's just a library. Make it one.

### 6. Backward Compatibility & Future Growth

**Design for the future, implement for today:**

| Do Today | Defer Until Needed |
|----------|-------------------|
| API versioning strategy (v1 in URL) | Multi-version support |
| Database schema with nullable columns for future fields | Complex migrations for those fields |
| Feature flags for risky changes | Full feature flag platform |
| Structured logging (JSON) | Full observability stack |
| Extract interfaces at module boundaries | Microservices architecture |
| CI that runs tests | Full CI/CD with multi-stage deployment |

**Migration mindset:**
1. Every system you build today will be rewritten within 3-5 years
2. Design for replaceability: clean interfaces, bounded contexts, data portability
3. Avoid vendor lock-in for critical paths: database, auth, deployment
4. Keep data portable: regular exports, documented schemas, no proprietary formats

### 7. Comprehensive Evaluation Checklist

Before any technical decision, evaluate:

```
[ ] Can we do this with our CURRENT stack?
[ ] What's the SIMPLEST thing that could possibly work?
[ ] What happens if this FAILS? (blast radius, recovery time)
[ ] What's the TOTAL cost over 2 years? (not just initial setup)
[ ] Who will MAINTAIN this? (do we have the expertise?)
[ ] What's the MIGRATION path if we need to change later?
[ ] Does this pass LEGAL/COMPLIANCE review? (GDPR, SOC 2, etc.)
[ ] Are we building for 100K users when we have 100?
[ ] Can we MVP this in < 2 weeks?
[ ] What's the ROLLBACK plan?
```

### 8. Token-Efficient Agent Workflow

Every skill should instruct agents to:

```
1. ASSESS: Run diagnostic script → get structured output → decide phase
2. DECIDE: Use decision tree → pick approach → confirm with human if > 1hr impact  
3. EXECUTE: Run tools directly (don't read source) → verify with exit codes
4. VERIFY: Re-run diagnostics → confirm fix → report metrics (before/after)
5. DOCUMENT: Update only what changed → minimal, precise commit
```

**Why this reduces tokens by 40-60%:**
- Scripts output structured data (JSON), not prose to parse
- Exit codes eliminate "is this fixed?" reasoning
- Decision trees eliminate exploration loops
- Verification is automated, not manual review

---

*This framework applies across ALL skills. Every SKILL.md should reference these principles where relevant.*
