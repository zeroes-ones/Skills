# Consequences

- Positive: ACID compliance, JSON support, mature ecosystem, strong community
- Negative: Team needs PG-specific training; migration from MySQL will take 3 sprints
- Risk: PG connection pooling requires PgBouncer for high-concurrency workloads
```

**Architecture Review Board (ARB):**
- Meets bi-weekly, 60 minutes
- Reviews: RFCs that cross team boundaries, new technology adoption requests, architecture departures
- Membership: Principal+ engineers, rotating attendance from each team
- **NOT** an approval bottleneck — decisions default to team autonomy unless cross-cutting

**Decision framework — when to escalate to ARB:**
- Technology choice that multiple teams will depend on
- Data model that crosses bounded contexts
- API contract that external customers will consume
- Deprecation of a widely-used internal service
- Introduction of a new programming language or paradigm

### Phase 4 (~15 min): Technical Due Diligence

**For acquisitions, investments, or major vendor decisions:**

**Code Quality Assessment (1–3 days):**
1. Clone repo; attempt to build and run locally. Time to first successful run = setup quality indicator.
2. Run static analysis: lint, complexity (cyclomatic >10 per function is a smell), test coverage
3. Manual review of 3–5 core modules: architecture coherence, naming consistency, error handling patterns
4. Check for secrets in code, hardcoded credentials, missing .gitignore
5. Dependency health: outdated packages, known CVEs, license compliance

**Architecture Assessment:**
1. Request architecture diagram — if they can't produce one, that's a finding
2. Trace a critical user journey through the system end-to-end
3. Identify single points of failure, scaling bottlenecks, data consistency patterns
4. Evaluate API design: REST/GraphQL consistency, versioning strategy, error handling
5. Assess data model: normalization, indexing, migration management

**Team Capability Assessment:**
| Signal                    | What to Look For                                         |
|---------------------------|----------------------------------------------------------|
| Bus factor                | How many people would need to be hit by a bus to halt dev? Target >3 per critical area |
| Documentation culture     | Do READMEs explain WHY and HOW? Are ADRs present?        |
| Code review practice      | Merge frequency, review depth, comments quality           |
| On-call maturity          | Runbooks, escalation paths, incident postmortems         |
| Deployment frequency      | Multiple per day = elite; weekly = medium; monthly = concern |
| Dependency on individuals | Is the CTO/tech lead the only person who understands X?  |

**Infrastructure Assessment Checklist:**
- [ ] CI/CD pipeline exists and completes in <30 minutes
- [ ] Infrastructure as Code (Terraform, Pulumi, CloudFormation) — not click-ops
- [ ] Secrets management: vault/manager, not in source code or env files
- [ ] Backups automated and tested; recovery time objective documented
- [ ] Monitoring: metrics, logs, alerts — at minimum on critical paths
- [ ] Security: dependency scanning, SAST, penetration testing cadence
- [ ] Scaling: documented auto-scaling policies; load test results from last 6 months

**Red Flags (severity-ordered):**
1. **No automated tests** → everything is legacy the day it's written
2. **Production access via SSH** → no repeatable deployments, no security boundary
3. **"The person who built this left"** → undocumented, unmaintainable systems
4. **Manual deployment process** → inconsistent, slow, error-prone
5. **No monitoring in production** → flying blind; don't know when things break
6. **Single database for everything** → scaling and coupling nightmare
7. **No code reviews** → quality rot, no knowledge sharing

### Phase 5 (~25 min): Innovation Management

**Innovation Time Allocation:**

| Activity                    | % of Engineering Time | Cadence              |
|-----------------------------|-----------------------|----------------------|
| Core product work            | 70%                   | Every sprint         |
| Technical debt + maintenance | 20%                   | Every sprint         |
| Innovation / exploration     | 10%                   | Every sprint or monthly |

**Innovation Funnel:**

```
Ideas (100) → Explore (10) → Experiment (3) → Incubate (1) → Integrate
                                            │
                                            └── Kill decisions at each gate

Gate criteria:
- Explore: aligns with strategic themes? Solves a real user problem?
- Experiment: prototype validated with 5+ users? Technical feasibility confirmed?
- Incubate: metrics show traction? Dedicated team committed?
- Integrate: absorbed by product team; becomes "core product work"
```

**Hackathon ROI:**
- **Structure**: 48 hours, cross-functional teams (eng + design + product), optional attendance
- **Theme**: tie to company strategy or customer pain points (not "build whatever")
- **Judging**: 30% innovation, 30% feasibility, 20% impact, 20% presentation
- **Outcome tracking**: 3-month follow-up: how many projects shipped to production?
- **Target**: >30% of hackathon projects ship within 6 months; <30% = either ideas aren't viable or follow-through is broken
- **Investment**: 2 days/quarter × entire eng team ≈ 2% of engineering time; cheap for the cultural and innovation ROI

### Phase 6 (~25 min): Vendor Evaluation

**RFI/RFP Process:**

```
Phase 0: Internal Alignment (before talking to vendors)
  - Document requirements: must-haves, nice-to-haves, anti-requirements
  - Define budget range internally
  - Identify decision-makers and approval process
  - Create evaluation scorecard with weighted criteria

Phase 1: RFI (Request for Information) — 5–10 vendors
  - Short questionnaire: capabilities, pricing model, SLAs, security certs
  - Eliminate obvious mismatches → narrow to 3–5

Phase 2: RFP (Request for Proposal) — 3–5 vendors
  - Detailed requirements document
  - Scored by evaluation committee against scorecard
  - Narrow to 2–3 finalists

Phase 3: Proof of Concept — 2–3 vendors
  - 2-week time-boxed PoC with real (sanitized) data
  - Test: integration effort, performance, edge cases, support quality
  - Select winner

Phase 4: Negotiation and Contract
  - Pricing: ask for multi-year discount; include termination for convenience
  - SLA: uptime guarantee, support response time, escalation path
  - Security: DPA, SOC 2 report, penetration test results, data residency
  - Exit plan: data export format, transition assistance, notice period
```

**Vendor Evaluation Scorecard:**

| Criterion                  | Weight | Vendor A | Vendor B | Vendor C |
|----------------------------|--------|----------|----------|----------|
| Feature fit (must-haves)   | 25%    | 8/10     | 7/10     | 9/10     |
| Integration effort          | 20%    | 6/10     | 8/10     | 5/10     |
| Total Cost of Ownership    | 20%    | 7/10     | 6/10     | 8/10     |
| Security & compliance       | 15%    | 9/10     | 8/10     | 7/10     |
| Vendor stability/viability  | 10%    | 7/10     | 9/10     | 6/10     |
| Support quality (from PoC)  | 10%    | 8/10     | 7/10     | 8/10     |
| **Weighted Score**          |        | **7.40** | **7.20** | **7.35** |

**Total Cost of Ownership Model (3-year):**

```
                     Year 1      Year 2      Year 3      TOTAL
License/Subscription $120,000    $150,000    $180,000    $450,000
Implementation       $80,000     $0          $0          $80,000
Integration           $40,000     $10,000     $10,000     $60,000
Training              $15,000     $5,000      $5,000      $25,000
Internal FTEs         $150,000    $150,000    $150,000    $450,000
Infrastructure        $20,000     $25,000     $30,000     $75,000
────────────────────────────────────────────────────────────────
TOTAL                $425,000    $340,000    $375,000   $1,140,000
```

**Build equivalent estimate:**
3 engineers × $180K/year × 3 years + cloud costs at $50K/year = $1,770,000
Decision: Buy ($1.14M < $1.77M) — unless this is a competitive differentiator.

**Red flags in vendor evaluation:**
- Won't provide a SOC 2 report or pen-test summary
- Pricing is "contact sales" with no transparency
- Reference customers are all in a different industry/size
- No public status page or incident history
- Product hasn't had a major release in 12+ months
- Key person dependency: "Our CTO will answer that" for every technical question


### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | ceo-strategist | Strategic vision, budget constraints, org design parameters — frames what's technically possible |
| **This** | cto-advisor | Technology strategy, build-vs-buy decisions, architecture governance, eng org design, vendor recommendations |
| **After** | system-architect | Consumes architecture decisions and governance framework to produce detailed system designs |

Common chains:
- **Tech strategy to implementation**: cto-advisor → system-architect → devops-engineer — Build-vs-buy → architecture design → infrastructure provisioning
- **Security hardening**: cto-advisor → security-engineer → devops-engineer — Risk assessment → security architecture → secure deployment
- **Vendor onboarding**: cto-advisor → cloud-architect → devops-engineer — Vendor selection → cloud integration design → deployment automation
- **Org restructure**: ceo-strategist → cto-advisor → system-architect — Org design → engineering team design → squad/tribe mapping
