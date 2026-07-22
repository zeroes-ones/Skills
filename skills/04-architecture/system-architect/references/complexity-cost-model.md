# System Architect - Complexity Cost Model

How to calculate the real cost of architectural complexity and when it's justified.

---

## The Complexity Cost Formula

```
complexity_cost_per_year = 
    (onboarding_time_days × new_hires_per_year × daily_rate) +
    (bugs_per_month × complexity_factor × avg_fix_hours × hourly_rate) +
    (deploy_freq_per_month × deploy_complexity_hours × hourly_rate) +
    (incident_count × mttr_hours × hourly_rate)
```

### Variable Definitions

| Variable | How to Measure | Example |
|----------|---------------|---------|
| `onboarding_time_days` | Time to first production commit for new hire | Monolith: 5 days, Microservices: 15 days |
| `new_hires_per_year` | Hiring plan | 4 engineers/year |
| `daily_rate` | Fully-loaded daily cost per engineer | $800/day ($200K/year) |
| `bugs_per_month` | Production bugs per month | Monolith: 8, Distributed: 15 |
| `complexity_factor` | How much harder are bugs to fix? | Monolith: 1.0x, Microservices: 2.5x |
| `avg_fix_hours` | Average hours to fix a bug | 2-4 hours |
| `deploy_freq_per_month` | Deployments per month | 20 |
| `deploy_complexity_hours` | Engineer-hours per deployment | Monorepo: 0.5h, Multi-service: 2h |
| `incident_count` | Monthly incidents | 3 |
| `mttr_hours` | Mean time to resolve | Monolith: 1h, Distributed: 3h |
| `hourly_rate` | Engineer hourly rate | $100 |

### Cost Comparison: Monolith vs Microservices

**Scenario: 8-person team, 4 hires/year, 20 deploys/month**

| Cost Component | Modular Monolith | Microservices (8 services) |
|---------------|-----------------|---------------------------|
| Onboarding | 5d × 4 hires × $800 = **$16,000** | 15d × 4 hires × $800 = **$48,000** |
| Bug fixing | 8 bugs × 1.0x × 2h × $100 × 12mo = **$19,200** | 15 bugs × 2.5x × 2h × $100 × 12mo = **$90,000** |
| Deployment overhead | 20 deploys × 0.5h × $100 × 12mo = **$12,000** | 20 × 8 svc × 2h × $100 × 12mo = **$384,000** |
| Incident response | 3 × 1h × $100 × 12mo = **$3,600** | 3 × 3h × $100 × 12mo = **$10,800** |
| **Total/year** | **$50,800** | **$532,800** |

**Annual complexity cost of microservices: ~$482,000 more than modular monolith.**

---

## When Adding a Microservice is Justified

### Cost-Benefit Decision Tree

```
Will this service handle > 1000 req/s independently?
├── NO → Don't extract. It's a library, not a service.
└── YES → Does it need independent scaling?
    ├── NO → Don't extract. Scale everything together.
    └── YES → Does it need a different technology stack?
        ├── NO → Don't extract. Different tech is the only strong justification.
        └── YES → Does it have a different deployment cadence?
            ├── NO → Wait. Extract when deployment is the bottleneck.
            └── YES → EXTRACT. But document the decision as an ADR.
```

### Justification Thresholds

| Condition | Threshold | When Justified |
|-----------|-----------|---------------|
| **Throughput** | >500 QPS independent of other services | Extract when scaling independently saves compute cost |
| **Team ownership** | >2 teams touching the same codebase | Extract to reduce merge conflicts and coordination overhead |
| **Deploy frequency** | Service deploys 3x more often than others | Extract when monolith deploy pipeline is the bottleneck |
| **Failure isolation** | Service failure causes cascading outages | Extract with circuit breaker and fallback |
| **Tech stack** | Requires fundamentally different language/runtime | Extract (only strong reason for greenfield microservice) |

### The "Don't Extract" Checklist
- [ ] Service handles < 100 req/s peak — don't extract
- [ ] Service has 1 consumer — it's a library
- [ ] Same technology stack as monolith — don't extract
- [ ] Same team owns both sides — don't extract
- [ ] No independent scaling need — don't extract
- [ ] Same deploy cadence — don't extract

---

## Monolith Patterns That Scale to 1M+ Users

Before extracting to microservices, exhaust these:

| Pattern | What It Does | Scalability Ceiling |
|---------|-------------|-------------------|
| **Modular Monolith** | Package by feature, strict module boundaries | ~50 engineers, ~100K users |
| **Read Replicas** | Route reads to replica DB; writes to primary | ~100K users for read-heavy apps |
| **Job Queue (async)** | Offload heavy work to background workers (Sidekiq, Celery, Bull) | ~500K users |
| **CDN + Caching** | Cache heavily at edge (CloudFront + Redis) | ~1M users for content-heavy apps |
| **CQRS-lite** | Separate read models from write models, same DB | ~1M users |
| **Sharding (DB)** | Split DB by tenant/region | ~10M users |

**Shopify ran a monolith to 1M+ merchants before extracting services. GitHub ran a monorepo to 30M+ users.**

---

## Architecture Fitness Functions

Automated tests that verify architectural qualities don't degrade:

```python
# Fitness function: No circular dependencies between modules
def test_no_circular_dependencies():
    graph = build_dependency_graph("src/")
    cycles = graph.find_cycles()
    assert len(cycles) == 0, f"Circular dependencies found: {cycles}"

# Fitness function: API response time < 200ms p95
def test_api_latency():
    p95 = load_test(endpoint="/api/orders", duration_seconds=60).p95_latency
    assert p95 < 200, f"P95 latency {p95}ms exceeds 200ms threshold"

# Fitness function: No module exceeds 500 lines (cohesion check)
def test_module_size():
    for module in get_modules("src/"):
        lines = count_lines(module)
        assert lines <= 500, f"{module.name}: {lines} lines > 500"
```

### Fitness Function Categories

| Category | What to Test | Tool |
|----------|-------------|------|
| **Coupling** | No circular deps, allowed dependencies only | `import-linter`, `madge`, `jdepend` |
| **Cohesion** | Module size limits, single responsibility | Custom script |
| **Performance** | Latency budgets, throughput minimums | k6, Locust, JMeter |
| **Security** | No hardcoded secrets, no known vulns | Trivy, Checkov, Semgrep |
| **API compatibility** | No breaking changes to public APIs | OpenAPI diff, GraphQL Inspector |
| **Deployment** | Deploy succeeds, rollback works, smoke tests pass | CI pipeline gates |

---

## When Monolith Wins

### Decision Matrix

| Factor | Monolith Wins When... | Microservices Win When... |
|--------|----------------------|-------------------------|
| **Team Size** | < 20 engineers | > 50 engineers across multiple teams |
| **Scale** | < 100K DAU | > 1M DAU with varied workloads |
| **Complexity** | Simple business domain (< 20 aggregates) | Complex domain with clear bounded contexts |
| **Velocity** | Early stage, pivoting frequently | Mature product, optimizing for throughput |
| **Cost** | Revenue < $10M ARR | Revenue > $50M ARR |
| **Reliability** | 99.9% SLA acceptable | 99.99%+ required |

### The Monolith Bingo Card
You should stay with a monolith if you check 3+ boxes:
- [ ] Team size < 15 engineers
- [ ] Deploy frequency < daily
- [ ] DB CPU < 50% sustained
- [ ] All features share the same technology stack
- [ ] Single bounded context (e.g., "e-commerce platform" not "e-commerce + payments + logistics")
- [ ] < 50K active users
- [ ] Revenue < $20M ARR
