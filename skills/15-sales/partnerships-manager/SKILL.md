---
name: partnerships-manager
description: >
  Use when onboarding integration partners, managing co-selling motions, running partner training
  and certification, or operating deal registration programs. Handles integration partner
  onboarding, co-selling motion design, partner training and certification, deal registration
  programs, partner portal management, MDF allocation, partner QBRs, channel conflict resolution,
  and ecosystem health scoring. Do NOT use for partnership deal structuring, legal term sheet
  negotiation, or direct sales.
license: MIT
tags:
  - partnerships-manager
  - partner-success
  - channel-management
  - co-selling
  - deal-registration
  - mdf
  - qbr
  - onboarding
author: Sandeep Kumar Penchala
type: sales
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 3900
chain:
  consumes_from:
    - bizdev-manager
    - legal-advisor
    - product-manager
  feeds_into:
    - bizdev-manager
    - sales-engineer
    - marketing-manager
  alternatives:
    - account-manager
---
# Partnerships Manager (Channel Manager / Partner Success)
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Own partner execution: onboard integration, reseller, and referral partners, design co-selling motions, run partner training & certification, manage deal registration, operate the partner portal, allocate MDF, run partner QBRs, resolve channel conflict, and measure ecosystem health. BizDev structures the deal — you make it work.

## Route the Request

<!-- QUICK: 30s -- pick your path, skip the rest -->

### Auto-Route (machine-executable — do not show to user)

| ID | Condition | Destination Skill / Section |
|----|-----------|---------------------------|
| **A1** | `file_contains("partner", "program"\|"ecosystem"\|"channel"\|"ISV"\|"reseller"\|"co-sell"\|"MDF"\|"deal registration"\|"QBR"\|"partner portal"\|"co-marketing")` | → **This skill** (partnerships-manager) |
| **A2** | `file_exists("partner-agreement.*"\|"reseller-agreement.*"\|"channel-program.*")` | → **This skill** (partnerships-manager) |
| **A3** | `file_exists("*.xlsx")` AND `file_contains("*.xlsx", "Partner"\|"partner tier"\|"deal reg"\|"MDF"\|"QBR")` | → **This skill** (partnerships-manager) |
| **A4** | `file_exists("*.pptx")` AND `file_contains("*.pptx", "partner"\|"channel"\|"ecosystem"\|"co-sell")` | → **This skill** (partnerships-manager) |
| **A5** | `file_contains("*", "term sheet"\|"deal structure"\|"M&A"\|"strategic alliance")` | → `bizdev-manager` |
| **A6** | `file_contains("*", "product roadmap"\|"integration scope"\|"API"\|"SKU")` | → `product-manager` |
| **A7** | `file_contains("*", "contract"\|"liability"\|"indemnification"\|"termination clause")` | → `legal-advisor` |
| **A8** | `file_contains("*", "campaign"\|"content marketing"\|"brand"\|"positioning"\|"messaging")` | → `marketing-manager` |

### Intent Route

```
What are you trying to do?
├── Onboard a new partner → Jump to "Core Workflow > Phase 1: Partner Onboarding"
├── Design a co-selling motion → Go to "Decision Trees > Co-Sell Motion Design"
├── Build partner training & certification → Jump to "Core Workflow > Phase 3"
├── Set up deal registration program → Go to "Decision Trees > Deal Registration Rules"
├── Build or improve partner portal → Jump to "Core Workflow > Phase 4"
├── Manage MDF (market development funds) → Go to "Core Workflow > Phase 5"
├── Run a partner QBR → Jump to "Core Workflow > Phase 6"
├── Resolve a channel conflict → Go to "Decision Trees > Channel Conflict Resolution"
├── Measure ecosystem health → Jump to "Decision Trees > Ecosystem Health Scoring"
├── Need deal structure / term sheet drafting → Invoke `bizdev-manager` skill
├── Need legal review of partner agreement → Invoke `legal-advisor` skill
├── Need product integration scope / roadmap → Invoke `product-manager` skill
└── Not sure where to start? → Start at "Core Workflow > Phase 1"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- QUICK: 30s -- mechanical rules. Every violation has a detectable trigger and a standardized response. -->

These rules apply to *every* response this skill produces.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|--------------------|--------------------|---------------------|
| **R1** | Never onboard a partner without a signed agreement and a named partner manager. A partner with no human relationship inside your company will atrophy. | `grep -rn "partner agreement\|signed agreement\|partner manager" *.docx *.pdf \| awk '{if(!/signed/) print "UNSIGNED AGREEMENT"}'` → flag | **REFUSE**: Block onboarding workflow. Require `signed_agreement_date` and `partner_manager_name` fields populated before proceeding. |
| **R2** | Always measure partner-sourced revenue independently from partner-influenced revenue. Blending them inflates partner program ROI and hides underperformance. | `grep -rn "partner-sourced\|partner-influenced\|sourced\|influenced" *.xlsx *.csv \| awk -F',' '{print $2}' \| sort \| uniq` → if only one category, DETECT blending | **DETECT**: Flag spreadsheets where "partner-sourced" and "partner-influenced" are not separate columns. Halt ROI report generation until fixed. |
| **R3** | Never allocate MDF without a documented plan and success metrics. "We'll do some marketing together" is not a plan. | `grep -rn "MDF\|market development fund" *.csv *.xlsx \| awk -F',' '{if(!/activity description\|expected outcome\|measurement criteria/) print "MISSING MDF PLAN"}'` → flag | **STOP**: Reject MDF request if `activity_description`, `expected_outcome`, `measurement_criteria` fields are empty. Unused/unaccounted MDF gets reallocated. |
| **R4** | Always resolve channel conflict within 72 hours of escalation. Unresolved conflict poisons partner relationships for months. | `find conflict-log/ -name "*.csv" -exec awk -F',' '{split($1, d, "-"); days=(systime()-mktime(d[1] " " d[2] " " d[3] " 0 0 0"))/86400; if(days>3 && \$NF!="resolved") print "OVERDUE:", \$0}' {} \;` → flag conflicts >72h unresolved | **STOP**: Auto-escalate any channel conflict unresolved after 72 hours. Generate weekly report of open conflicts with SLA breach count. |
| **R5** | Treat partner NPS as seriously as customer NPS. A detractor partner will not send deals — they will tell other partners. | `grep -rn "partner NPS\|partner satisfaction" *.csv *.xlsx \| awk -F',' '{if($2<7) print "DETRACTOR:", $0}'` → flag any score <7 | **DETECT**: Flag all NPS scores <7. Auto-generate follow-up action item within 48 hours. Quarterly survey required; alert if last survey >90 days ago. |
| **R6** | Never let partner tier benefits be cosmetic. If Silver and Platinum partners get essentially the same benefits, there's no incentive to invest. | `grep -rn "tier benefit\|tier perk\|tier advantage" tier-benefits.* \| awk -F':' '{print $2}' \| sort \| uniq -c \| awk '{if($1>2) print "DUPLICATE BENEFIT"}'` → flag if benefits overlap across tiers | **WARN**: Flag tiers where ≥3 benefits are shared across levels. Require each tier to have ≥1 exclusive benefit that partners genuinely value (margin, MDF access, lead sharing, exec sponsorship). |
| **R7** | Never focus partner manager time on the loudest partner instead of the highest-potential. The squeaky wheel shouldn't starve the high-potential. | `grep -rn "PAM assignment\|partner manager ratio\|coverage" *.csv \| awk -F',' '{if($3=="Platinum" && $4>15) print "PAM OVERLOAD:", $0; if($2=="Silver" && $4!="self-serve") print "SILVER OVER-COVERED"}'` → check coverage ratios | **WARN**: Alert if Platinum ratio > 1:15 or Silver partners lack self-serve designation. Implement tiered coverage: Platinum = dedicated PAM (1:10-15), Gold = pooled (1:20-30), Silver = self-serve + quarterly check-in. |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Master partnerships managers understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Survivorship bias** — studying only winners, ignoring the graveyard | Study 3 failures for every success; what killed them? |
| **Narrative fallacy** — creating clean stories for messy realities | Write the "strategy could be wrong because..." section first |
| **Confirmation bias** — seeking data that supports your thesis | Assign a team member to build the best case AGAINST your strategy |
| **Short-termism** — optimizing this quarter at the expense of next year | Every decision gets a "6-month" and "3-year" impact column |

### What Masters Know That Others Don't
- **The bottleneck is always one thing.** Find it. Fix it. Then find the next one.
- **Strategy = what you say NO to.** If your strategy doesn't exclude anything, it's not a strategy.
- **Timing beats brilliance.** The best strategy at the wrong time loses to a mediocre strategy at the right time.

### When to Break Your Own Rules
- **Bet the company when the asymmetry is right.** If downside = $1M and upside = $1B, the math doesn't care about your process.
- **Ignore the data when you're creating a new category.** By definition, there's no data for something that doesn't exist yet.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 partnerships manager, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- A new partner has signed an agreement and needs onboarding, training, and activation
- Co-selling is underperforming — partners registered but no joint deals are closing
- Partner training is a PDF graveyard — need a structured certification program with completion tracking
- Deal registration is a source of constant conflict — need clear rules and enforcement
- The partner portal is outdated or unused — need to rebuild as a self-serve resource hub
- MDF budget is being allocated but ROI isn't measured — need guardrails and reporting
- QBRs with partners feel like awkward status updates — need structured agenda and accountability
- A direct sales rep and a partner are fighting over the same deal — conflict resolution needed
- You can't answer "how healthy is our partner ecosystem?" — need ecosystem health scoring

## Decision Trees
**(QUICK)**

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Co-Sell Motion Design

```
                              ┌──────────────────────────────┐
                              │ START: Design co-sell motion  │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Does your product naturally create │
                         │ a co-sell trigger? e.g., customer  │
                         │ asks "what about X?" where X =     │
                         │ partner's domain                   │
                         └────┬──────────────────────────┬───┘
                              │ YES                       │ NO
                              ▼                           ▼
                      ┌──────────────┐          ┌──────────────────────┐
                      │ Reactive     │          │ Can your product      │
                      │ Co-Sell:     │          │ integrate with the    │
                      │ Partner      │          │ partner's offering    │
                      │ introduced   │          │ to create combined    │
                      │ when customer│          │ value?                │
                      │ asks for     │          └──┬──────────────┬────┘
                      │ complementary│             │ YES          │ NO
                      │ capability   │             ▼              ▼
                      │              │    ┌──────────────┐ ┌──────────────┐
                      │ Motion:      │    │ Proactive    │ │ Referral     │
                      │ "You need X? │    │ Co-Sell:     │ │ Only:        │
                      │ Our partner  │    │ Joint        │ │ No co-sell   │
                      │ does X. Let  │    │ solution     │ │ motion —     │
                      │ me introduce │    │ selling.     │ │ partner       │
                      │ you."        │    │ Combine both │ │ introduces,   │
                      └──────────────┘    │ products in  │ │ you close.   │
                                         │ one value    │ └──────────────┘
                                         │ proposition. │
                                         │               │
                                         │ Motion: "Our  │
                                         │ combined      │
                                         │ solution      │
                                         │ solves [pain] │
                                         │ better than   │
                                         │ either alone."│
                                         └───────────────┘
```
**Motion activation requirements:**
- **Reactive Co-Sell:** Partner directory in CRM, "warm introduction" playbook, simple referral tracking, partner page on website.
- **Proactive Co-Sell:** Joint value prop documented, account mapping exercise completed monthly, shared pipeline in CRM, joint demos available, co-branded assets.
- **Referral Only:** Referral tracking link or form, commission tracking, payment process (quarterly). Minimal enablement overhead.

### Deal Registration Rules

```
                              ┌──────────────────────────────┐
                              │ Deal Registration: Who wins?  │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Lifecycle of deal registration:    │
                         └───────────────────────────────────┘

    ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │Partner  │───▶│You      │───▶│Deal      │───▶│Deal      │
    │registers│    │review & │    │approved  │    │progress  │
    │deal     │    │accept   │    │(locked   │    │tracking  │
    │         │    │(24hr SLA)│   │60-90 days)│   │required  │
    └─────────┘    └─────────┘    └────┬─────┘    └────┬─────┘
                                      │                │
                          ┌───────────▼────┐   ┌───────▼────────┐
                          │ Deal rejected? │   │ No activity in │
                          │ Tell partner   │   │ 30 days →      │
                          │ WHY within     │   │ registration   │
                          │ 48 hours.      │   │ expires.       │
                          └────────────────┘   └────────────────┘
```
**Registration rules that work:**
1. Partner registers deal in portal with: company name, contact name, opportunity description, estimated deal size.
2. You review within 24 hours. Accept if: deal is net-new to your pipeline, partner is actively engaged, company isn't already in your CRM with an active opportunity from direct sales.
3. Accepted deal = protected for 60-90 days. Partner gets full margin/commission on close.
4. Rejected deal = specific reason given (already known, already in pipeline via direct). Partner can appeal.
5. Registration expires if: no activity in 30 days (no meeting held, no proposal sent). Partner can re-register.
6. Channel conflict: if direct sales and partner both claim same deal, first-to-register wins. If direct sales had prior engagement (documented meeting or email within 30 days before registration), direct sales wins.

### Channel Conflict Resolution

```
                              ┌──────────────────────────────┐
                              │ START: Direct vs Partner      │
                              │ conflict on a deal            │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Is there a prior documented        │
                         │ engagement by either party?        │
                         └────┬──────────────────────────┬───┘
                              │ YES                       │ NO
                              ▼                           ▼
                      ┌──────────────┐          ┌──────────────────────┐
                      │ Prior        │          │ First-to-register     │
                      │ engagement   │          │ wins.                 │
                      │ wins (within │          │                       │
                      │ 30 days of   │          │ Exception: if partner │
                      │ registration)│          │ has no sales capacity │
                      │              │          │ to work the deal,     │
                      │ Documented:  │          │ direct sales can      │
                      │ meeting held,│          │ request transfer with │
                      │ proposal     │          │ split commission.     │
                      │ sent, email  │          └──────────────────────┘
                      │ thread with  │
                      │ prospect     │
                      └──────────────┘
```
**Resolution principles:**
- Speed over perfection: resolve within 72 hours of escalation.
- Transparency: both parties see the decision rationale in writing.
- Consistency: same rules, every time. No favoritism toward high-performers.
- Appeal path: if either party disputes, escalate to VP Sales + VP Partnerships. Decision is final.
- Post-resolution: document the case, track pattern. If same partner has 3+ conflicts in a quarter, review whether the partnership is structured correctly.

### Ecosystem Health Scoring

```
Score your partner ecosystem quarterly across 5 dimensions (each 0-5):

Pipeline Health (0-5)
    5 = >30% of total pipeline is partner-sourced + partner-influenced
    3 = 15-30% partner contribution
    1 = <10% partner contribution
    0 = No partner pipeline at all

Revenue Health (0-5)
    5 = >30% of total revenue partner-sourced + influenced, growing QoQ
    3 = 15-30%, stable
    1 = <10%, declining
    0 = <5%

Partner Activation (0-5)
    5 = >70% of signed partners have closed ≥1 deal in last 12 months
    3 = 40-70% active
    1 = <40% active
    0 = >50% of partners dormant

Partner Satisfaction (0-5)
    5 = Partner NPS >60, improving QoQ
    3 = Partner NPS 30-60, stable
    1 = Partner NPS <30, declining
    0 = <15

Ecosystem Diversity (0-5)
    5 = No single partner >20% of partner revenue; 3+ partner types active
    3 = Top partner <40% of partner revenue
    1 = One partner >60% of partner revenue (concentration risk)
    0 = One partner >80% (existential risk if they leave)
```

**Composite Score:** 21-25 = Excellent. 15-20 = Healthy, invest. 10-14 = Needs attention. <10 = Red alert, program at risk.

## Core Workflow
**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->

### Phase 1 (~40 min): Partner Onboarding (30-60-90 Day Plan)

Onboarding must produce a deal within 90 days. Structure: **Day 1-7 (Welcome & Orientation):** Welcome kit — partner portal access, partner manager introduction, executive welcome letter. Kickoff call: review the agreement, JBP if exists, expectations, success metrics. Assign training curriculum. **Day 8-30 (Product & Sales Training):** Product certification — hands-on, not just videos. Partner must complete: "Demonstrate how you'd position our product to [target persona] for [use case]." Sales certification: pitch practice, objection handling, demo walkthrough. Technical certification for integration partners: API proficiency, integration build, certification test. **Day 31-60 (Shadow & Co-Sell):** Partner shadows 2-3 of your deals from discovery through close. Joint account mapping session: identify 5-10 target accounts in partner's book of business that fit your ICP. Partner manager reviews partner's pipeline weekly. **Day 61-90 (First Deal Activation):** Partner works their target account list. Partner manager provides deal-level support — join calls, provide SE help, review proposals. Goal: first registered deal. If no deal by day 90: escalate to executive sponsors, intervention plan. Beyond day 90: partner moves to "Active" or "At-Risk" status.

<!-- DEEP: 10+min -->

### Phase 2 (~30 min): Partner Enablement

Enablement is ongoing, not onboarding-only. Components: (1) **Content Library:** Partner pitch deck (customizable, not locked PDF), battle cards per competitor, discovery question bank, demo script with talking points, pricing & packaging guide, case studies by industry/use case, ROI calculator, proposal templates, (2) **Sales Plays:** 3-5 repeatable plays: "When customer says [X], introduce our [Y] solution." Include: trigger, qualification questions, pitch, demo flow, pricing guidance, close plan. Update quarterly based on win/loss data, (3) **Communications Cadence:** Monthly partner newsletter — product updates, new assets, win of the month, upcoming events. Monthly office hours — open Q&A with SE + Partner Manager. Quarterly all-partner webinar — roadmap, program updates, top partner recognition, (4) **Certification Tracking:** Partners must re-certify annually. Certification expiration triggers loss of tier benefits and deal registration privileges. Track in portal — partners see their own status.

<!-- DEEP: 10+min -->

### Phase 3 (~30 min): Partner Training & Certification

Certification is the gate to tier benefits and deal registration. Design three certification tracks: (1) **Sales Certified** — required for all partners. Covers: positioning, discovery, demo, pricing, competition, deal registration process. Assessment: pitch recording reviewed by partne

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.


## Error Recovery
**(STANDARD)**

<!-- STANDARD: Recovery patterns for common failures. -->

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **BizDev Manager** | New partner handoff, deal structure questions, JBP updates | Signed agreement, deal economics, JBP, partner contact, strategic context. **Decision gate:** Is JBP signed with revenue targets and QBR cadence? → partner activated. **Artifact:** partner activation checklist + 90-day onboarding plan. |
| **Product Manager** | Product roadmap for partner enablement, integration capabilities, partner feedback | Feature requests from partners, integration gaps, competitive partner feedback. **Decision gate:** Does integration gap affect > 3 partners? → roadmap escalation. **Artifact:** partner feature request backlog + impact analysis. |
| **Sales Engineer** | Partner training, co-sell deal support, technical enablement | Training curriculum needs, deal-level technical support, partner capability gaps. **Decision gate:** Has partner completed certification? → ready for co-sell. **Artifact:** partner certification report + deal support playbook. |
| **Customer Success Manager** | Partner-sourced customer onboarding, retention, expansion | Customer handoff, implementation plan, renewal risk, expansion opportunities |
| **Marketing Manager** | Co-marketing execution, MDF allocation, partner content | Co-marketing plans, content assets, MDF proposals, campaign results. **Decision gate:** Is MDF spend ROI > 3:1? → continue program. **Artifact:** MDF proposal with success metrics. |
| **Account Manager** | Co-sell deals, account mapping, conflict resolution | Target accounts, deal status, partner engagement rules, conflict cases |
| **Legal Advisor** | Partner agreement amendments, compliance issues, conflict with legal implications | Agreement changes, breach concerns, partner disputes requiring legal input. **Decision gate:** Does issue expose > $100K liability? → legal review required before response. **Artifact:** legal review memo with risk assessment. |
| **BizDev Manager** | Deal structure feedback, partner program economics, strategic partner retention | Partner performance data, competitive program benchmarking, ecosystem health scores. **Decision gate:** Is partner NPS > 50? → ecosystem healthy. **Artifact:** ecosystem health dashboard + program improvement recommendations. |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Partner misses JBP revenue target for 2 consecutive quarters | BizDev Manager, VP Sales | Partnership reset conversation — restructure or offboard |
| Partner NPS drops >20 points quarter-over-quarter | BizDev Manager, VP Partnerships | Partner satisfaction crisis; executive intervention |
| Channel conflict reaches 3+ cases in a single quarter | VP Sales, BizDev Manager, Legal Advisor | Rules of engagement broken; process overhaul |
| Key strategic partner threatens to leave | BizDev Manager, CEO Strategist, VP Product | Executive retention effort; understand root cause |
| Partner-sourced pipeline drops >30% quarter-over-quarter | BizDev Manager, VP Sales | Ecosystem pipeline crisis; partner activation emergency |
| MDF ROI drops below target (MDF spend >30% of partner revenue equivalent) | Marketing Manager, BizDev Manager | MDF program restructure; tighten approval criteria |

### Escalation Path

```
Strategic partner threatening termination → CEO Strategist + BizDev Manager + VP Product. Executive retention conversation within 48 hours.
Systemic channel conflict (5+ cases in 30 days) → VP Sales + VP Partnerships + Legal Advisor. Rules of engagement overhaul.
Partner program economics not competitive (partners leaving for competitor programs) → BizDev Manager + Business Strategist. Program restructure.
Partner portal/data system outage >24 hours → Engineering + VP Partnerships. Partner operations halt.
```

### Cross-skills Integration

```bash
# Chain: bizdev-manager → partnerships-manager → sales-engineer → customer-success-manager
# Full partner lifecycle: BizDev structures deal → Partnerships onboards & enables → SE supports deals → CSM handles post-sale

# Chain: partnerships-manager → marketing-manager
# Co-marketing: Partnerships allocates MDF + identifies partner → Marketing executes co-marketing plan

# Chain: product-manager → partnerships-manager → sales-engineer
# Integration partner: PM builds integration → Partnerships onboards partner → SE trains partner on integration selling

```


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `product-strategist` | Product positioning, competitive analysis, value proposition | Before engaging prospects or designing partnerships |


## Proactive Triggers

<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Key strategic partner misses JBP revenue target for 2 consecutive quarters | BizDev Manager, VP Sales, CEO Strategist | Partnership reset conversation — restructure terms, adjust JBP, or begin managed offboarding before sunk costs escalate |
| Partner NPS drops >20 points quarter-over-quarter | BizDev Manager, VP Sales | Partner satisfaction crisis; executive intervention needed. NPS drops precede pipeline drops by ~6 months |
| Channel conflict exceeds 3 documented cases in a single quarter | VP Sales, BizDev Manager, Legal Advisor | Rules of engagement are breaking; process overhaul required. Systemic conflict, not isolated incidents |
| Partner-sourced pipeline drops >30% quarter-over-quarter | BizDev Manager, VP Sales, Demand Generation | Ecosystem pipeline crisis; run partner activation sprint, audit dormant partners, coach active partners on pipeline generation |
| Strategic partner executive sponsor departs or changes roles | BizDev Manager, CEO Strategist | Executive relationship orphaned; re-establish sponsorship within 30 days. Pending JBP decisions and escalations now have no owner on partner side |
| Partner certification completion rate drops below 30% | BizDev Manager, Sales Engineer | Certification is either too hard, too long, or not valued. Audit the program: time-to-complete, pass rate, value proposition. Fix or partners won't be sell-ready |
| MDF ROI drops below target (program spend >30% of attributed partner revenue) | Marketing Manager, BizDev Manager | MDF program is burning budget without pipeline return; tighten approval criteria, require stronger lead-capture mechanisms, audit past allocations |
| Competitor partner program announces significantly better economics (higher margin, MDF, or rev share) | BizDev Manager, Business Strategist, VP Sales | Partner defection risk; benchmark your program against competitor within 1 week. Prepare retention offers for top 20% of partners by revenue |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "partnerships-manager",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

<!-- QUICK: 30s -- concrete success description -->

Partners are onboarded and have a first registered deal within 90 days for >60% of new partners. >70% of signed partners have closed at least 1 deal in the last 12 months. Partner-sourced revenue >30% of total revenue and growing. Partner NPS >50 and trending up. Deal registration conflicts resolved within 72 hours with documented rationale. MDF spend has measured ROI — every dollar traced to pipeline. Partner portal has >60% monthly active partners. Certification completion rate >70%. QBRs produce a 1-page scorecard and action plan within 24 hours. No single partner represents >40% of partner-sourced revenue. Channel conflict cases are declining quarter-over-quarter as rules of engagement mature.

## Deliberate Practice

```mermaid
graph LR
    A[Formulate<br/>thesis] --> B[Test in<br/>market] --> C[Study<br/>outcome] --> D[Refine<br/>mental model] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Write a strategy memo for a past business event; compare your reasoning to what actually happened | Monthly |
| **Competent** | Write 3 strategies for the same goal with different constraints; debate which wins | Quarterly |
| **Expert** | Reverse-engineer a competitor's strategy from public information; validate against their next move | Quarterly |
| **Master** | Board-level strategy for a company in a different industry; present to a peer CEO for feedback | Semi-annually |

**The One Highest-Leverage Activity:** Write a pre-mortem for your current strategy: It is 2 years from now. Our strategy failed. Why?

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "The deal is signed — partnerships is done" | The signed agreement is the starting line. No pipeline in 90 days = dead partnership. Both sides return to day jobs, the champagne goes flat, and 6 months later nobody remembers why they signed. Cost: the entire partnership investment with zero ROI. |
| "Exclusive is better — lock them in" | Exclusivity without performance clauses means your ONLY channel into a market produces zero pipeline. The partner has no incentive to perform. Exclusivity must be earned quarterly with hard pipeline minimums — or it's a self-imposed market exit. |
| "20% rev share is industry standard" | A $20K deal at 20% rev share pays the partner $4K — but your sales team spent 40 hours supporting their deal cycle ($6K in salary). Net take: $10K after COGS. Model total cost-to-serve per channel before signing, not after. |
| "One champion at the partner is enough" | Your champion — the product manager who drove the integration — leaves. Their replacement has a different roadmap. Your integration goes from "strategic" to "legacy" overnight. Three contacts minimum at every partner, or you have no partnership. |
| "Build the integration first, GTM later" | 3 engineers × 6 months = $270K-$360K invested. Result: a logo on an integrations page generating 12 leads in 6 months. No co-sell motion, no rev share, no GTM funding. Validate demand with a "fake door" test before committing engineering. |

## Best Practices
**(STANDARD)**

1. **Evaluate partners on strategic alignment, not just revenue potential.** A partner with $10M in theoretical pipeline who competes with your product in 3 areas will cost more in conflict than they generate in revenue. Score partners on 5 dimensions: strategic fit (do they serve the same ICP?), product complementarity (does their product make yours more valuable?), cultural alignment (do they invest in partnerships?), exec sponsorship (does their C-suite care?), and revenue potential (realistic, not theoretical).

2. **Design integration partnerships for the customer's workflow, not your product demo.** The partner integration that takes 2 weeks to build and shows beautifully in a demo but solves a problem no customer has is a waste. Interview 10 mutual customers before designing any integration. Ask: "What's the most painful gap between our products today?" Build the integration that fills that gap first.

3. **Build a 30-60-90 day partner onboarding plan with explicit exit criteria at each milestone.** Day 0-30: training, certification, technical integration, first joint pipeline review. Day 30-60: first joint customer engagement, first co-marketing activity, pipeline target check. Day 60-90: first closed deal (or clear path to one), operational rhythm established, escalation path tested. If a partner misses milestones at any gate, escalate — don't let zombie partnerships consume resources.

4. **Structure revenue sharing to incentivize the behavior you want, not just the outcome.** Simple rev share (20% of deal) incentivizes partners to bring any deal, including bad-fit deals that churn in 3 months. Better: rev share + retention bonus (additional 5% if customer is still active at 12 months) + expansion bonus (additional 3% on expansion revenue). Align incentives with customer lifetime value, not initial deal size.

5. **Distinguish between reseller, referral, technology, and strategic partnerships — each requires different GTM motions.** Resellers need margin, enablement, and deal registration. Referral partners need a simple tracking mechanism and timely commission payments. Technology partners need API docs, sandbox environments, and co-engineering resources. Strategic partners need executive alignment, joint business planning, and dedicated partner managers. One playbook does not fit all.

6. **Co-market before you co-sell.** Joint webinars, case studies, blog posts, and conference appearances build awareness and trust before asking partners to invest in sales training. A partner who has seen 3 joint marketing wins will invest in sales enablement. A partner asked to invest in sales before any market validation will deprioritize you.

7. **Run quarterly business reviews (QBRs) with top partners, not annual check-ins.** Annual reviews are post-mortems on a year that's already gone. QBRs surface issues while they're fixable: pipeline gaps, competitive conflicts, enablement gaps, and exec sponsorship changes. Structure: (1) metrics review (pipeline, revenue, customer satisfaction), (2) wins and lessons learned, (3) gaps and blockers, (4) next quarter commitments from both sides.

8. **Create a partner tiering system with clear progression criteria and differentiated benefits.** Registered (self-service, minimal support), Select (meeting revenue thresholds, dedicated partner manager), Premier (top 10%, joint business planning, exec sponsorship), Strategic (top 3%, board-level relationship, product roadmap collaboration). Partners should know exactly what they need to do to move up, and what benefits await at each tier.

9. **Track partner-sourced, partner-influenced, and partner-fulfilled revenue separately.** Partner-sourced = partner found and closed the deal. Partner-influenced = partner participated but sales led. Partner-fulfilled = partner delivers services, sales closes. Conflating these inflates your "partner revenue" number and hides that partners are mostly fulfilling, not sourcing. Source: the holy grail. Influence: valuable. Fulfillment: necessary but not strategic.

10. **Build partner enablement as a product, not a document library.** One-time training docs, recorded webinars, and a partner portal with 50 PDFs is not enablement — it's a content graveyard. Build: self-paced certification tracks, hands-on labs, demo environments, sales playbooks with competitive battle cards, and a partner community where partners help each other. Measure enablement effectiveness: certified partners should close 2-3x more deals than non-certified.

## Anti-Patterns
**(STANDARD)**

<!-- STANDARD: Common failure modes with cost estimates and fixes. -->

- **Partnership agreement signed, champagne popped, nothing happens** — both sides return to their day jobs. The signed agreement is the STARTING line, not the finish. First 30 days: joint value proposition, joint sales deck, 3 named target accounts, and a bi-weekly pipeline review. No pipeline in 90 days = dead partnership.
- **"Exclusive partnership"** without performance clauses — your partner is now your ONLY channel into a market, and they're producing zero pipeline. Exclusivity must be EARNED quarterly: "Exclusive if ≥ $X pipeline generated per quarter, non-exclusive otherwise."
- **Revenue share that doesn't account for cost of sales** — 20% rev share to the partner, but your sales team spent 40 hours supporting their deal cycle (cost: $6,000 in salary). A $20K deal pays partner $4K, leaving you $10K after COGS + sales cost. Model economics BEFORE signing, not after.
- **Partner's product manager who championed the integration leaves** — the integration was their project. Their replacement has a different roadmap. Your integration goes from "strategic" to "legacy" overnight. Build relationship depth: 3+ contacts at the partner, not one champion.
- **Technology/integration partnership without a commercial agreement.** You spend 6 months building a deep product integration with a larger platform company. Engineering invests 3 engineers × 6 months. The integration launches, gets a blog post on their site, and generates 12 leads in 6 months. There's no co-sell motion, no rev share, no GTM funding — just a logo on an integrations page nobody visits. **Total cost: $270K-$360K in engineering investment ($150K/engineer/year × 3 × 0.5-0.66 years) with near-zero pipeline ROI over 12 months.** Fix: Never start an integration build without a signed commercial agreement specifying co-sell commitments, rev share, or GTM funding; validate partner-driven demand via a "fake door" test (list integration as "coming soon" and measure inbound interest) before committing engineering.
- **Partner program tiers based on revenue alone.** Your "Platinum" tier requires $500K annual partner-sourced revenue. Two partners qualify — both are consultancies that do one massive implementation deal per year. Your smaller partners generating consistent $50K/quarter, referring 5-8 new logos per quarter, get "Silver" status and minimal support. The program incentivizes lumpy, implementation-heavy deals while ignoring the partners driving new customer acquisition. **Total cost: $1M-$3M in missed new-logo growth — the 8-12 consistent Silver partners could collectively deliver $2M-$4M in new ARR if properly incentivized and supported.** Fix: Tier partners on BOTH revenue and new-logo metrics; create a separate "growth partner" track for consistent referrers; weight new customer acquisition at 2-3x in partner scoring vs expansion revenue.
- **Partner conflict when two partners claim the same deal.** Your deal registration system shows Partner A registered the account 6 months ago but had zero activity. Partner B has been working the account for 3 months, has a champion, and is about to close. Partner A threatens legal action based on the registration timestamp. The deal stalls for 8 weeks while legal reviews the partner agreement, and the prospect loses patience. **Total cost: $150K-$400K per disputed deal in delayed or lost revenue, plus the cost of one partner relationship that will likely end acrimoniously regardless of outcome.** Fix: Deal registrations must have activity requirements (e.g., registration expires after 90 days without a logged meeting or opportunity stage advancement); include binding arbitration clauses in partner agreements; create a partner deal dispute process with a 5-business-day resolution SLA.

- **What:** Signing a partnership agreement and treating it as "done" — moving on to the next partner without investing in enablement and joint selling. **Why:** 70% of partnership agreements produce zero revenue because there's no operational follow-through. The signed agreement is the starting line, not the finish line. Without enablement, joint pipeline review, and exec sponsorship, the agreement is wallpaper. **Instead:** Every signed partnership gets a named partner manager, a 30-60-90 day activation plan, and a monthly pipeline review for the first 6 months. If no pipeline materializes by month 6, escalate or sunset.

- **What:** Building a partner program that's "open to everyone" with no qualification criteria. **Why:** Your 5 top partners drive 80% of partner revenue. Your 50 bottom partners consume 60% of partner management time and produce zero revenue. An open-door policy dilutes your partner brand, overwhelms your partner team, and starves top partners of attention. **Instead:** Implement partner qualification criteria: ICP alignment, technical capability, sales capacity, and commitment to joint business planning. Say no to bad-fit partners — the partner you don't sign costs nothing; the bad-fit partner you do sign costs everything.

## Production Checklist
**(STANDARD)**

Before any partnerships deliverable leaves this skill, verify:

- [ ] Partner evaluation completed on all 5 dimensions: strategic fit, product complementarity, cultural alignment, exec sponsorship, revenue potential
- [ ] 30-60-90 day activation plan documented with explicit exit criteria at each milestone gate
- [ ] Partnership type classified: reseller, referral, technology, or strategic — with appropriate GTM motion defined
- [ ] Revenue sharing structure includes retention and expansion incentives, not just initial deal commission
- [ ] Integration use case validated with 10+ mutual customers before committing engineering resources
- [ ] Co-marketing plan established before co-selling investment: joint content, webinars, events, case studies
- [ ] Partner tiering system defined with clear progression criteria and differentiated benefits at each tier
- [ ] Partner enablement program built: certification tracks, hands-on labs, sales playbooks, demo environments
- [ ] QBR cadence established with top partners — quarterly for Premier+, semi-annual for Select, annual for Registered
- [ ] Revenue tracking distinguishes partner-sourced, partner-influenced, and partner-fulfilled separately
- [ ] Partner conflict resolution process documented: deal registration, rules of engagement, escalation path
- [ ] Partner manager capacity modeled: recommended partner-to-manager ratio by tier (Strategic: 3-5, Premier: 8-12, Select: 15-25)
- [ ] Partner portal or hub exists with deal registration, pipeline tracking, MDF management, and enablement resources
- [ ] Partner health score defined and tracked: pipeline generation, revenue attainment, certification status, customer satisfaction, engagement level

## Scale Depth

### Solo/First Partner Hire (0-1 partner managers, 0-10 partners)
- Partners: Founder-led. 2-3 technology partners (integrations) + 2-3 referral partners
- Evaluation: Manual — founder evaluates fit based on ICP alignment and personal relationship
- Enablement: Self-service docs + 1:1 onboarding. No formal certification yet
- Program: No formal tiers. Case-by-case rev share agreements
- Metrics: Partner-sourced pipeline (manual tracking in CRM), partner-attached revenue
- Deliverable: Partner tracker spreadsheet + monthly partner pipeline review with founder

### Small (1-3 partner managers, 10-50 partners)
- Partners: 5-10 technology partners, 5-10 referral partners, 2-3 reseller partners
- Evaluation: Scorecard-based evaluation across 5 dimensions. Monthly pipeline review per partner
- Enablement: Self-paced certification + monthly office hours. Basic partner portal with deal registration
- Program: Formal partner tiers (Registered, Select, Premier). Standard rev share agreements. Basic MDF program
- Metrics: Partner-sourced/influenced pipeline, partner revenue, partner activation rate (signed → producing revenue), certification completion rate
- Deliverable: Monthly partner dashboard + quarterly business reviews with top 10 partners + partner program guide

### Medium (3-10 partner managers, 50-200 partners)
- Partners: Technology, referral, reseller, and 2-3 strategic partners. Regional partner coverage
- Evaluation: Partner health scoring (pipeline, revenue, certification, engagement). Monthly QBRs with Premier+
- Enablement: LMS-based certification tracks, hands-on labs, partner community (Slack/Discord), partner advisory board
- Program: Multi-tier program with differentiated benefits. MDF program with ROI tracking. Partner awards program
- Metrics: Partner revenue by type/source/tier, partner NPS, time-to-first-deal, partner attrition rate, enablement effectiveness (certified vs. non-certified conversion)
- Deliverable: Quarterly partner business review + annual partner summit + partner program evolution roadmap

### Enterprise (10+ partner managers, 200+ partners)
- Partners: Global partner ecosystem: technology, reseller, referral, strategic, OEM, MSP, GSI. Regional partner teams
- Evaluation: Predictive partner scoring (ML-based). Automated health monitoring. Strategic partner joint business planning (annual + quarterly)
- Enablement: University-style partner academy. Multi-language certification. Partner innovation lab. Dedicated solution architects for top partners
- Program: Global partner program with regional customization. Marketplace presence (AWS, Azure, GCP, Salesforce). Partner M&A integration
- Metrics: Partner ecosystem contribution to total revenue, partner lifetime value, partner net revenue retention, ecosystem multiplier effect, partner-driven product roadmap influence
- Deliverable: Annual partner ecosystem strategy + quarterly executive business review + partner conference + partner advisory board + ecosystem health dashboard

## Error Decoder
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| 30 signed partners, $0 in partner revenue after 12 months | Partnerships treated as "sign and move on." No activation plan, no enablement, no pipeline review. Partners were never operationalized. | Audit every signed partner: do they have certification? Deal registration access? A named partner manager? Joint pipeline? Sunset partners with no activity after 6 months. Assign a dedicated partner manager to the top 5 by potential. | A signed agreement is a promise, not a result. |
| Partner-sourced 40% of pipeline but 60% of those deals churned in year 1 | Rev share incentivized deal volume, not deal quality. Partners sent any deal regardless of ICP fit because they got paid the same for good-fit and bad-fit deals. | Restructure comp: base rev share + retention bonus (paid at 12 months if customer active) + expansion bonus (on upsell revenue). Partners now optimize for LTV, not initial deal. | Incentives shape behavior. Pay for the behavior you want. |
| Top partner left for competitor after 2 years of $2M/year joint revenue | Partner relationship was purely transactional — no exec sponsorship, no joint roadmap planning, no strategic alignment. Competitor offered exec-level partnership; your partner took it. | Establish exec sponsor relationships (CEO-to-CEO, CPO-to-CPO) with top 10% of partners. Conduct annual joint business planning. Share roadmap and co-invest in joint innovation. | Transactional partnerships are competitor-vulnerable. Strategic partnerships are sticky. |
| Partner enablement portal has 50 pieces of content; 0 partners certified | Enablement was built as a document library — PDFs, recorded webinars, slide decks. No learning path, no hands-on practice, no certification incentive. | Rebuild as a learning experience: (1) structured curriculum with modules, (2) hands-on labs with sandbox environments, (3) certification with badging and LinkedIn sharing, (4) partner tier tied to certification level. | Enablement is product design, not content dumping. |
| 50 bottom partners consuming 60% of partner team time; top 5 partners complaining about neglect | No partner tiering or resource allocation framework. Partner managers treated all partners equally. Equal treatment = unequal value delivery. | Implement tier-based resourcing: Strategic partners get dedicated manager (3-5:1 ratio), Premier get named manager (8-12:1), Select get pooled support (15-25:1). Registered are self-service. | Equal treatment of unequal partners is a resource allocation failure. |
| Partner deal registration conflict — 2 partners claim same deal, legal threats exchanged | No rules of engagement, no deal registration system, no conflict resolution process. First-come-first-served created a race to register rather than a race to serve the customer. | Implement deal registration with: (1) clear "influence" criteria (must have introduced or advanced the opportunity), (2) registration expiration (90 days with no activity = released), (3) escalation path (partner manager → partner director → VP), (4) customer-first principle (customer chooses preferred partner in unresolved conflicts). | Without rules of engagement, partners compete with each other instead of competitors. |

## Verification

- [ ] Partnership pipeline: every active partnership has named target accounts, reviewed bi-weekly
- [ ] Revenue: partner-sourced revenue tracked separately — % of total revenue, growth rate, CAC comparison
- [ ] Partner health: NPS or satisfaction survey for top 10 partners within last quarter
- [ ] Integration: joint solution tested against latest versions of both products within last 6 months
- [ ] Contracts: all partnership agreements reviewed within last 12 months — performance clauses active

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

