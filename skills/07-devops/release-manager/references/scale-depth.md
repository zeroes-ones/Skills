# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: No formal release process. Merge to main → deploy. Feature flags via env vars. Release notes are git log. Rollback = `git revert` + redeploy.
- **Overkill**: Release trains, go/no-go meetings, release branches, formal versioning, stakeholder briefings, deployment calendars.
- **Coordination**: You decide when to deploy. No coordination needed.
- **Cost**: $0 beyond CI/CD costs.
- **Transition trigger**: First time you break production and can't quickly identify which change caused it. Second person starts deploying.

### Small (2-10 people, 100-10K users)
- **What changes**: Release branches for coordination. Basic go/no-go (tests passing? security scan clean?). Weekly release cadence. Automated release notes (conventional commits + changelog tool). Feature flags for risky changes. Simple versioning (SemVer). Rollback via pipeline.
- **Overkill**: Formal release train with cross-team dependency mapping, stakeholder briefing docs, multi-stage canary with metric verification, release commander role.
- **Coordination**: One person owns the release each week (rotating). Go/no-go checklist in a shared doc. Release notes auto-generated. Brief Slack announcement.
- **Cost**: $0-200/month (changelog tools, feature flag SaaS free tier).
- **Transition trigger**: > 2 teams shipping to same production; merge conflicts during deploy; "who deployed what?" confusion.

### Medium (10-50 people, 10K-1M users)
- **What changes**: Weekly release train with published calendar. Formal go/no-go meeting (30 min, day before). Designated release commander (rotating). Canary deployments with metric verification. Release dashboards. Cross-team dependency tracking. Stakeholder briefing for major releases. Feature flag platform with gradual rollout. Release retrospective every cycle.
- **Overkill**: Full-time release manager, multi-track release trains, deployment window SLAs, formal risk assessment matrix for every release.
- **Coordination**: Release commander coordinates across teams. Go/no-go meeting with QA + engineering leads. Dependency check-in 3 days before freeze. Release retrospective within 1 week.
- **Cost**: ~$20-40K/year (feature flag platform, 10% of senior engineer time for release commander rotation).
- **Transition trigger**: > 5 teams deploying to same production; first customer-reported deployment regression; compliance audit requiring deployment records.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated release management function (1-2 release managers). Multi-track release trains (fast track for hotfixes, standard track for features). Enterprise feature flag platform with kill switches and audit logging. Automated canary analysis with statistical significance testing. Release risk assessment matrix with scoring. Formal stakeholder communication templates. Deployment window SLAs with business units. Release health scorecards. Regulatory compliance evidence collection per release.
- **What's full production**: Release management platform with automated gating. Progressive delivery with automated promotion/rollback. Release predictability metrics (on-time %). Self-service release dashboard for all teams. Compliance artifact auto-generation per release.
- **Coordination**: Release manager runs release planning weekly. Go/no-go with VP-level visibility for major releases. Cross-team dependency sync daily during freeze week. Monthly release program review with CTO.
- **Cost**: $300-600K/year (1-2 release managers + platform). Feature flag enterprise platform $30-80K/year. Release management tooling $10-30K/year.
- **Transition trigger**: > 10 teams deploying to same production, regulatory environment (SOX, FDA), customer contractual release SLAs, > $100M revenue with release-dependent revenue recognition.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ci-cd-builder | Build artifacts and deployment pipeline |
| **This** | release-manager | Release plan, go/no-go decision, deployment coordination |
| **After** | site-reliability-engineer | Production reliability monitoring and incident response |

Common chains:
- **Chain**: ci-cd-builder → release-manager → site-reliability-engineer — Pipeline produces deployable artifacts; release manager orchestrates rollout; SRE monitors production health
- **Chain**: qa-engineer → release-manager → incident-responder — QA reports test results; release manager decides go/no-go; incident responder handles any production issues
