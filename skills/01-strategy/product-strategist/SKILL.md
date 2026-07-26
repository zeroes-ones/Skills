---
name: product-strategist
description: >
  Use when defining product strategy, validating product-market fit, planning OKRs,
  conducting competitive analysis, modeling product growth, or designing PLG vs SLG
  motions. Handles product discovery, feature prioritization, Jobs-to-be-Done framework,
  pricing strategy, customer journey mapping, North Star metric definition, and product
  roadmapping. Do NOT use for sprint planning, backlog grooming, or day-to-day
  engineering management.
license: MIT
tags:
- product
- strategy
- pmf
- okr
- pricing
- plt
- competitive-analysis
- jtbd
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 2715
chain:
  consumes_from:
  - business-strategist
  - data-scientist
  - ux-researcher
  feeds_into:
  - brand-guidelines
  - ceo-strategist
  - fp-and-a-analyst
  - marketing-manager
  - product-manager
---
# Product Strategist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end product strategy from discovery through growth. Covers product-market fit validation, OKR-driven planning, pricing strategy, competitive positioning, and product-led growth — connecting business outcomes to product execution.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "product.vision\|product.strategy\|North.Star\|strategic.positioning\|competitive.advantage")` AND `file_contains("*", "roadmap\|OKR\|objective\|key.result")` | This is your skill. Jump to **Core Workflow** — Phase 1: Discovery & Validation. |
| A2 | `file_contains("*", "PMF\|product.market.fit\|Sean.Ellis\|retention.cohort\|churn.analysis")` | Jump to **Decision Trees** — Product-Market Fit Assessment. |
| A3 | `file_contains("*", "RICE\|CD3\|prioritization\|feature.priority\|opportunity.scoring\|Kano")` AND `file_contains("*", "roadmap\|backlog\|feature.list")` | Jump to **Core Workflow** — Phase 3: Prioritization. |
| A4 | `file_contains("*", "GTM\|go.to.market\|PLG\|product.led\|sales.led\|channel.strategy")` | Invoke **business-strategist** instead. GTM strategy is business model territory. |
| A5 | `file_contains("*", "persona\|user.research\|journey.map\|usability.test\|user.interview")` | Invoke **ux-researcher** instead. This is user research, not product strategy. |
| A6 | `file_contains("*", "PRD\|product.requirement\|spec\|user.story\|acceptance.criteria")` | Invoke **product-manager** instead. This is feature specification work. |
| A7 | `file_contains("*", "fundraising\|board.deck\|investor.update\|company.vision\|cap.table")` | Invoke **ceo-strategist** instead. This is company-level strategy. |
| A8 | `file_contains("*", "pricing.model\|pricing.strategy\|willingness.to.pay\|Van.Westendorp\|value.based.pricing")` | Jump to **Decision Trees** — Pricing Strategy Matrix. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Validate product-market fit → Jump to "Decision Trees > Product-Market Fit Assessment"
├── Set product vision & strategy → Start at "Core Workflow > Phase 1: Discovery & Validation"
├── Plan a roadmap → Go to "Core Workflow > Phase 2: Strategy & Planning"
├── Prioritize features
│   ├── Using RICE/CD3 → Jump to "Core Workflow > Phase 3: Prioritization"
│   └── Kano or Opportunity Scoring → Go to "Phase 3"
├── Analyze competitors → Jump to "Core Workflow > Phase 1" + "Sub-Skills > competitive-analysis"
├── Set pricing strategy → Jump to "Decision Trees > Pricing Strategy Matrix"
├── Choose GTM model → Jump to "Decision Trees > Go-to-Market Model Selection"
├── Drive growth & retention → Go to "Core Workflow > Phase 4: Growth & Optimization"
├── Scale product operations → Go to "Scale Depth"
├── Need business model or GTM strategy? → `business-strategist`
├── Need user research or persona development? → `ux-researcher`
├── Need feature specs or PRD writing? → `product-manager`
├── Need company vision or board-level decisions? → `ceo-strategist`
└── Don't know where to start? → Run "Core Workflow > Phase 1: Discovery & Validation"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "We talk to users constantly — we know what to prioritize" | What users say they want and what they actually use diverge by 40%+. Your 5 anecdotal conversations are not a prioritization framework. Without systematic user data, you're prioritizing by recency bias — the last person who complained loudest wins. |
| "Let's price at $X/month — it feels competitive" | Pricing-by-feel leaves 20-40% of revenue on the table. Your competitors spent months testing pricing with real customers. You're guessing in 30 seconds and calling it strategy. Willingness-to-pay data costs 2 weeks and pays back for years. |
| "Competitors shipped this feature — we need it too" | Cargo-cult features are the #1 cause of product bloat. 64% of features are rarely or never used (Standish Group). Matching competitors feature-for-feature is not a winning strategy — it's a strategy for being second, with the same overhead and half the differentiation. |
| ""Ship onboarding v2" is a perfectly fine Q3 objective" | That's a task, not an objective. Output-based OKRs measure activity, not impact. When the team ships onboarding v2 and retention doesn't move, you have a "successful" quarter with exactly zero business value. Measure the outcome, not the output. |
| "We'll set the roadmap timeline — engineering will figure out the capacity" | Roadmap dates set without engineering input produce one of two outcomes: missed commitments (credibility damage) or cut corners (quality damage). "Figure it out" is not capacity planning — it's setting your team up for burnout. |

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to prioritize features without user data.** Do not rank features without knowing user impact, adoption signals, or business outcome drivers. Feature prioritization based on intuition produces features nobody uses. | Trigger: response ranks features ("Feature X should be top priority" or provides a numbered priority list) AND `conversation_context` does not contain user demand data (survey results, support ticket volume, churn analysis, usage analytics) | STOP. Respond: "I cannot prioritize features without user data. Provide: (1) user demand signals (survey data, support ticket frequency, feature request volume), (2) business impact estimates (retention lift, revenue potential, activation improvement), (3) effort estimates from engineering. Without these, prioritization is guesswork." |
| **R2** | **REFUSE to set roadmap dates without engineering feasibility input.** Product strategy sets the "what" and "why"; engineering sets the "how long." Committing to dates without engineering validation is setting the team up to fail. | Trigger: response includes a delivery date or timeline ("Q2 delivery", "3-week build", "shipping by [date]") without referencing engineering effort estimates or capacity planning | STOP. Qualify: "Based on product priorities, these are the candidate bets ordered by impact. Validate effort estimates with engineering before committing to dates. Timeline is an engineering output, not a product input." |
| **R3** | **REFUSE to declare a pricing strategy without competitive context and willingness-to-pay data.** Pricing without market context is arbitrary. Freemium, usage-based, and per-seat models have different economics that only make sense in context. | Trigger: response recommends a specific pricing model ("use freemium", "charge $X/month") without referencing competitive landscape pricing data or willingness-to-pay research | STOP. Qualify: "[Pricing model] typically converts at [range]% in [industry/segment]. Before finalizing: (1) benchmark against 3+ direct competitors, (2) test willingness-to-pay with [specific method, e.g., Van Westendorp survey of 20 target customers], (3) model unit economics at each price point." |
| **R4** | **DETECT and WARN when product decisions are justified by "users asked for it" or "competitors have it" without business impact analysis.** User requests are signals, not requirements. Competitor features are validation of a market, not validation for your product. | Trigger: generated content justifies a feature using "users requested", "customers asked for", or "competitors have" without quantifying the expected business impact (retention lift %, revenue increase $, activation improvement) | WARN. Rewrite: "Users have requested [feature] ([N] tickets, [X]% of support volume). If built, it is expected to impact [metric] by [estimate]%. Before committing, validate with a 1-week discovery: survey [N] users in target segment. If < [threshold]% express urgent need, deprioritize." |
| **R5** | **STOP and ASK when critical product context is missing.** Do not assume: user segmentation, current retention rates, activation metrics, revenue per user, or competitive positioning. Product strategy without these is a wish list. | Trigger: generating product strategy recommendations (vision, roadmap, prioritization, pricing) without explicit user segmentation, retention data, or revenue metrics confirmed in the conversation | STOP. Ask: "What are your user segments and their relative revenue contribution? What's your current monthly retention by segment? What's your activation rate (users reaching 'aha moment')? What's your average revenue per user? Without these, strategy recommendations are untethered from business reality." |
| **R6** | **DETECT and WARN about output-based OKRs masquerading as strategy.** "Ship feature X" is a task, not an objective. OKRs measure outcomes — the business results that features are hypothesized to produce. | Trigger: generated OKRs contain "Ship", "Launch", "Build", "Complete", "Deliver", "Release" as the objective verb, rather than "Increase", "Reduce", "Improve", "Achieve" tied to a measurable metric | WARN. Rewrite each output-based OKR: "Instead of 'Ship onboarding v2' → 'Increase week-4 retention from 40% to 55% (hypothesis: improved onboarding reduces early churn).' The feature is the bet; the metric is the outcome. Measure the outcome, not the feature." |
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Product strategy is not about picking the right framework — it's about **seeing what others don't see and having the conviction to act on it before the data is conclusive**. The output is not a strategy document; the output is a company aligned around a shared direction that wins.

### Mental Models

| Model | Description |
|---|---|
| **Strategy = what you don't do** | A strategy that doesn't explicitly say what you're *not* pursuing is not a strategy — it's a wish list. The power is in the trade-offs. |
| **Insight > framework** | Frameworks (SWOT, Porter, BCG) structure thinking but don't produce insight. Great strategy comes from a novel observation about the market that others have missed. |
| **Distribution beats product** | In most markets, the best-distributed product wins, not the best product. Your GTM strategy is at least as important as your product strategy. |
| **Speed of iteration > quality of initial strategy** | No strategy survives contact with customers intact. The best strategists iterate faster, not smarter. |

### Cognitive Biases That Kill Strategies

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Planning fallacy** | Underestimating how long everything takes by 2-3x | Use reference-class forecasting: how long did it take 5 similar companies? |
| **Confirmation bias** | Seeking data that supports your strategy, dismissing contradicting evidence | Appoint a "strategy skeptic" role in every review; their job is to find what's wrong |
| **Anchoring** | First number you see (competitor price, market size estimate) shapes all subsequent thinking | Always generate independent estimates before looking at benchmarks |
| **Survivorship bias** | Studying winners and extracting lessons without examining the graveyard of failures | For every successful strategy you admire, study 2 that failed with similar approaches |
| **Sunk cost fallacy** | Continuing a failing strategy because you've already invested in it | Set kill criteria at strategy launch. If triggered, kill regardless of investment. |

### What Masters Know That Others Don't

- **The best strategy fits on one page.** If you need appendices to explain your strategy, you don't have clarity. Jeff Bezos's 1997 shareholder letter was 2 pages and ran Amazon for decades.
- **Strategy is revealed in resource allocation, not documents.** Show me your budget and headcount allocation — that's your real strategy. Everything else is aspiration.
- **Category creation beats category competition.** The highest-return strategies create new categories where you define the rules (Salesforce: "No software"; Tesla: EVs as desirable, not eco-compromises). But category creation is also the riskiest bet — most new categories fail.
- **Timing is the least discussed, most important variable.** Being right too early is indistinguishable from being wrong. Ask: "Why now? What changed that makes this possible today that wasn't possible 2 years ago?"

### When to Break Your Own Rules

- **Skip competitive analysis when creating a new category.** There are no competitors when you're defining the market. But validate that users have an existing behavior you're replacing — even category creators compete with "the way it's done today."
- **Ignore roadmap discipline during existential pivots.** When the company might die, throw out the roadmap and focus all resources on the one thing that might save it. Survival is the strategy.

## Operating at Different Levels

Product strategy scales from individual product lines to company-defining bets. The scope and time horizon of decisions defines the level.

| Level | Product Strategy Output Characteristics |
|---|---|
| **L1 — Apprentice** | Analyzes a market segment. Contributes to competitive analysis. Learns strategy frameworks. |
| **L2 — Practitioner** | Owns product strategy for a feature area. PMF analysis, pricing recommendations, competitive positioning for a product surface. |
| **L3 — Senior** | Owns product strategy for a full product. Portfolio-level OKRs, build-vs-buy-vs-partner analysis. Strategic rationale for market positioning. |
| **L4 — Director/VP** | Owns strategy for a product line or business unit. Multi-year strategic bets. "These are the three markets we're betting on for the next 3 years." |
| **L5 — CPO/CEO** | Defines the company's product philosophy and strategic decision framework. "This is how we choose which markets to enter and how we win in them." |

**Usage**: Say "as an L3 product strategist, evaluate the PMF for..." Default: **L3** (full-product strategy, independent analysis).

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Validating product-market fit for a new product or feature
- Setting up OKRs cascading from company strategy to team execution
- Pricing strategy: freemium, usage-based, tiered, per-seat, hybrid
- Competitive analysis and market positioning
- Choosing PLG vs SLG go-to-market approach
- Prioritizing features: RICE, Kano, Cost of Delay, Opportunity Scoring
- Customer journey mapping and Jobs-to-be-Done analysis
- North Star metric definition and product metrics framework

## Decision Trees
**(QUICK)**

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Product-Market Fit Assessment

```
Retention: 40%+ "very disappointed" without product? (Sean Ellis test)
├── YES → Organic growth > 50% of signups?
│   ├── YES → Revenue pulling from customers?
│   │   ├── YES → PMF confirmed. Scale.
│   │   └── NO → PMF weak. Pricing/value mismatch.
│   └── NO → Emerging PMF. Double down on delighted segment.
└── NO → No PMF. Interview users. Pivot or iterate.
```

**What good looks like:** Product vision document that the entire leadership team can state in one sentence — no ambiguity, no 5-paragraph preamble. Sean Ellis survey shows >40% 'very disappointed' score with statistical significance. Competitive analysis identifies exactly 3 defensible advantages with evidence. OKRs cascade cleanly from product strategy to quarterly engineering goals with measurable targets.
### Go-to-Market Model Selection

```
Average deal size (ACV)?
├── < $500 → PLG: self-serve, free tier, viral loops
├── $500-$5K → PLG + Sales hybrid: PQL → sales assist
├── $5K-$50K → SLG with product assist: demo-driven
└── > $50K → Enterprise sales: high-touch, MSA, procurement

```

### Pricing Strategy Matrix

| Model | Best For | Conversion | Examples |
|-------|----------|------------|----------|
| Freemium | B2C, PLG tools | 2-5% | Spotify, Notion, Figma |
| Usage-based | API, infra, AI | Variable | AWS, Twilio, OpenAI |
| Per-seat | B2B SaaS, collab | Predictable | Slack, Jira, GitHub |
| Tiered | SMB-Enterprise | Segmented | HubSpot, Intercom |
| Hybrid | Complex products | Maximized | Datadog, Snowflake |

## Core Workflow
**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Discovery & Validation

1. **Problem validation**: Vitamin or painkiller? Talk to 20+ target users.
2. **JTBD**: Functional job + emotional job + social job. "People don't want a drill, they want a hole."
3. **Competitive landscape**: Direct competitors, indirect, substitutes. Win/loss analysis.
4. **Opportunity sizing**: TAM → SAM → SOM. Top-down + bottom-up.
5. **Value proposition**: For [customer] who [problem], [product] is a [category] that [benefit]. Unlike [alternatives], we [differentiator].

Complete when:
- Problem validation summary from 20+ target user interviews documented
- Jobs-to-be-Done canvas with functional, emotional, and social jobs completed
- Competitive landscape map with win/loss analysis and opportunity sizing (TAM/SAM/SOM) saved

### Phase 2 (~30 min): Strategy & Planning

1. **Vision (3-5yr) → Strategy (12-18mo) → Tactics (quarterly)**
2. **OKRs**: Objectives (qualitative, inspiring). KRs (quantitative, outcome-based). NOT output-based.
3. **Roadmap**: Now → Next → Later. Theme-based, tied to objectives.
4. **North Star metric**: Single metric capturing core value. Supporting: AARRR or HEART.

Complete when:
- Vision → Strategy → Tactics hierarchy documented with 12-18 month strategic plan
- OKRs documented: objectives (qualitative, inspiring) with KRs (quantitative, outcome-based)
- Theme-based Now/Next/Later roadmap tied to objectives and North Star metric defined

### Phase 3 (~20 min): Prioritization

1. **RICE**: Reach × Impact × Confidence ÷ Effort
2. **Kano Model**: Basic → Performance → Delighters
3. **Cost of Delay**: CD3 = Cost of Delay ÷ Duration. Highest CD3 first.
4. **Opportunity Scoring**: Importance × (1 − Satisfaction). High importance + low satisfaction = biggest opportunity.

Complete when:
- RICE-scored feature backlog with Reach, Impact, Confidence, and Effort estimates
- Kano model classification (Basic/Performance/Delighters) applied to feature set
- Cost of Delay (CD3) calculated for top initiatives with ranked priority order

### Phase 4 (~15 min): Growth & Optimization

1. **Growth loops**: Identify bottleneck in Acquisition → Activation → Retention → Revenue → Referral. Optimize.
2. **PLG**: Time-to-value < 5 min. PQL scoring for sales handoff.
3. **Pricing optimization**: Value metric research. Willingness-to-pay studies.
4. **Retention**: Cohort analysis. Identify "aha moment". Drive users there faster.

Complete when:
- Growth loop analysis with bottleneck identified across Acquisition → Activation → Retention → Revenue → Referral
- PLG strategy documented: time-to-value target, PQL scoring criteria, and sales handoff triggers
- Retention cohort analysis with "aha moment" identified and optimization plan documented

## Error Recovery
**(STANDARD)**

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
Product strategy sits at the intersection of business, design, engineering, and operations. Know when to coordinate:

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `business-strategist` | TAM/SAM/SOM analysis, GTM strategy, pricing model options, unit economics baseline | During product discovery; before roadmap finalization |
| `ceo-strategist` | Vision, fundraising status, board priorities, strategic direction, resource constraints | Before any major product pivot; quarterly strategic review |
| `ux-researcher` | User personas, journey maps, usability findings, behavioral insights, pain point evidence | During product discovery; before feature prioritization |
| `data-scientist` | Retention cohorts, funnel analytics, A/B test results, user segmentation, LTV projections | During feature prioritization; before pricing strategy decisions |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `ceo-strategist` | Product vision, PMF signal, competitive landscape, roadmap, OKRs, growth model | CEO lacks product context for board meetings and fundraising |
| `product-manager` | Prioritized features with RICE scores, success metrics, user segments, competitive positioning | PM writes PRDs without strategic context — backlog disconnected from business goals |
| `marketing-manager` | ICP definition, positioning framework, competitive differentiation, pricing value metrics | Marketing campaigns target wrong segments with wrong messaging |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Pivot decision | `ceo-strategist`, `cto-advisor`, `product-manager` | Resourcing, timeline, technical replanning |
| PMF signal (positive or negative) | `ceo-strategist`, `board-manager` | Fundraising strategy, burn rate decisions |
| Pricing change | `business-strategist`, `growth-engineer`, `legal-advisor` | Revenue model, experiment design, terms update |
| Major scope change | `product-manager`, `engineering-manager` | Sprint replanning, capacity reallocation |
| Competitive threat | `ceo-strategist`, `business-strategist` | Strategic response, positioning adjustment |
| OKR at risk | `ceo-strategist`, `cto-advisor` | Expectation management, resource reallocation |

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Team says "users are asking for feature X" but nobody has quantified how many users or what job they're trying to accomplish | Intervene: "Feature requests are symptoms, not diagnoses. Run a Jobs-to-be-Done analysis: (1) What job is the user hiring this feature to do? (2) How many users have this job? (3) What do they use today as a workaround? (4) What's the cost of the workaround? If you can't articulate the job, you're building a feature for a vocal minority." | Unvalidated feature requests are the #1 source of feature bloat and wasted engineering capacity. Every feature shipped for a non-existent job consumes maintenance, testing, and cognitive load forever. JTBD separates real demand from loud requests |
| Product roadmap has 20+ items for this quarter but team capacity can only deliver 5 — and the CEO keeps adding more | Flag: "A roadmap without capacity constraints is a wishlist, not a plan. Force-rank: if we can only ship ONE thing this quarter, what creates the most business value? Use RICE scoring (Reach × Impact × Confidence / Effort) with explicit effort estimates from engineering. Any unranked item is a distraction. Present the trade-off: "Adding X means delaying Y by 6 weeks. Which do you choose?"" | Overstuffed roadmaps produce nothing on time. When everything is priority #1, nothing is. The CEO needs to see the trade-off explicitly: adding to the roadmap means removing something of equal size. If they won't choose, default to highest-RICE item and make the rest wait |
| Product discovery consists of "talking to 3 users who are friends of the founders" — no structured research, no segmentation, no competitive analysis | Alert: "Convenience sampling produces false confidence. Run structured discovery: (1) Recruit 15+ users from YOUR target segment (not friends), (2) Observe them using their current solution (not your prototype), (3) Document the moment they "hire" a solution and what triggers the switch. The goal is not to validate your idea — it's to understand their problem deeply enough that the solution becomes obvious" | Friends and early adopters will tell you your product is great because they like you, not because it solves their problem. Structured discovery with strangers reveals the real friction points. Products built on friend-validation fail at scale because real users don't have the same context, patience, or motivation |
| Competitor launched a major new feature — team panics and wants to copy it immediately | Intervene: "Competitive panic is the worst product strategy. Before copying: (1) Is this feature core to THEIR strategy or YOURS? (2) Do YOUR users actually need this? (3) What's the 3-month cost to build vs the opportunity cost of NOT building your roadmap? Run a quick user survey — if <30% of your users care, ignore it. Competitors can validate market demand for you; you don't have to be first to every feature" | Competitive reactivity creates "me-too" products that always lag. The competitor's feature was designed for their user base, their infrastructure, and their business model. Copying without understanding creates a worse version of someone else's strategy. Your roadmap should reflect YOUR users' jobs, not your competitor's |
| Pricing page still has the original 2 tiers from launch (Free/$9.99) after 2 years and 50K users — no enterprise tier, no usage-based option, no annual discount | Flag: "Pricing is product strategy, not a configuration setting. At 50K users, you're leaving 30-50% revenue on the table. Design: (1) 3-tier model with clear value differentiation per tier, (2) Usage-based component for high-volume customers, (3) Annual discount (15-20%) to improve cash flow predictability, (4) Enterprise tier with SSO, SLA, and dedicated support for deals >$10K/year. Test with 10% of new signups first" | Pricing optimization is the highest-ROI product activity. A 10% price increase that loses 2% of customers increases profit by 8%. Products that never revisit pricing leave enormous revenue on the table while competitors capture the high end of the market. Pricing signals value — if you're the cheapest, you're signaling low quality |
| Retention cohort shows 40% of users churn within the first 7 days — team focused on building new features for existing users | Alert: "New user retention is the #1 growth lever. Fix activation before building for retention: (1) Map the time-to-value — what's the minimum steps from signup to "aha moment"? (2) Remove every step between signup and first value, (3) Track activation rate (users who reach aha moment within session 1). A 10% improvement in day-7 retention compounds to 2x more MAU in 12 months. Stop building features until activation rate exceeds 60%" | Acquisition fills a leaky bucket if activation is broken. Every dollar spent on acquisition for a product with 40% week-1 retention is 60% wasted. Fixing activation is the highest-leverage product work — it improves every growth channel simultaneously without spending a dollar on marketing |
| Revenue per customer hasn't grown in 4 quarters but the team attributes it to "market conditions" | Flag: "Revenue stagnation has a root cause. Audit: (1) Is expansion revenue flat because there's nothing to expand to? → add higher-tier features. (2) Is churn offsetting expansion? → fix retention. (3) Are new customers lower-value? → fix ICP targeting. (4) Is pricing below market? → test increases. Market conditions affect everyone equally — if competitors are growing and you're not, it's a product strategy problem, not a market problem" | Blaming market conditions is the product equivalent of "it works on my machine." Revenue stagnation is almost always a product strategy failure: wrong features, wrong pricing, wrong segments, or wrong positioning. The market reveals the truth — listen to it |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

> Your product vision is one sentence every person in the company can repeat from memory — not a paragraph nobody read.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

Product strategy is pattern-matching refined through exposure to diverse business models, markets, and outcomes. The strategist who has studied 100 failures sees patterns the strategist who has only studied successes cannot.

### The Strategy Improvement Loop

```
HYPOTHESIZE → TEST → SYNTHESIZE → (update mental model) → repeat

```

After every strategic decision: write down your explicit prediction. Check it at 3, 6, and 12 months. The gap between prediction and reality is your curriculum.

### Practice Routines by Skill Level

| Level | Practice | Frequency |
|---|---|---|
| **Novice** | Do a competitive analysis of 3 products in your space. For each, identify: what they say they are, what they actually are, and the gap between those two. | Monthly |
| **Competent** | Write a 500-word strategy memo for a product move (launch, pivot, kill). Exchange with a peer for red-teaming. Rewrite based on critiques. | Biweekly |
| **Expert** | Run a Sean Ellis PMF survey with real users. Calculate the "very disappointed" percentage. Benchmark against industry (40%+ is strong). Identify which segment drives the metric. | Quarterly |
| **Master** | Study 1 failed product deeply per quarter: read post-mortems, founder interviews, investor letters. Write what you would have done differently — then write why you might have been wrong about that too. | Quarterly |

### The One Highest-Leverage Activity

**Write your strategy on one page, then delete it and write it again in half the words.** The second version reveals what you actually believe. The first version reveals what you think you should believe. Do this before every strategy presentation.

## When NOT to Product Manage

```
Pre-PMF with < 5 users? → Founder IS the PM. No dedicated PM needed.
Solo developer building for yourself? → Dogfooding IS product management.
< 10 engineers + strong PMF? → Engineer as rotating product owner.
Agency building for clients? → Client = PM. You execute.
```

### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | idea-to-spec | Problem statement, target user personas, initial market opportunity — frames what to discover and validate |
| **This** | product-strategist | Product vision, PMF assessment, OKRs, roadmap, pricing strategy, prioritization framework, growth model |
| **After** | product-manager | Consumes product strategy to write detailed requirements, user stories, and sprint plans |

Common chains:
- **Discovery to delivery**: idea-to-spec → product-strategist → product-manager — Problem validation → product strategy → execution specs
- **Strategic alignment**: ceo-strategist → product-strategist → cto-advisor — Company vision → product direction → technical feasibility
- **User-centered strategy**: ux-researcher → product-strategist → product-manager — User insights → product strategy → feature specs
- **Pricing & GTM**: product-strategist → business-strategist → growth-engineer — Pricing model → GTM strategy → growth experiments

## Best Practices
**(STANDARD)**

1. **Validate product-market fit with the Sean Ellis test, not gut feel.** Ask active users: "How disappointed would you be if this product didn't exist?" Target ≥ 40% answering "very disappointed." Run this survey quarterly, segmenting by cohort. PMF isn't binary — it degrades over time as market expectations rise and competitors improve.

2. **Define your North Star metric as an input metric, not a revenue metric.** Revenue is a lagging indicator of value delivery. Your North Star should measure the core value exchange: daily active users completing the key action (Spotify: time listening; Airbnb: nights booked; Slack: messages sent). When the North Star moves, revenue follows. When revenue moves without the North Star, you're extracting value, not creating it.

3. **Model product-led growth (PLG) and sales-led growth (SLG) as a spectrum, not a binary choice.** Pure PLG works for products with: low ACV (< $10K), short time-to-value (< 15 minutes), viral loops (collaboration invites). Pure SLG works for: high ACV (> $50K), long sales cycles, complex onboarding. Most products need a hybrid: PLG for bottoms-up adoption + SLG for enterprise expansion. Design the handoff deliberately.

4. **Run competitive analysis against future-state competitors, not current-state.** Your competitor's v3 product exists today; their v4 ships in 6 months. Analyze their trajectory (hiring patterns, patent filings, conference talks, engineering blog) to forecast where they'll be when you launch. Time-shifted comparisons systematically understate competitive risk.

5. **Price on value, not cost-plus or competitor-minus.** Use Van Westendorp price sensitivity analysis or conjoint analysis to understand willingness to pay. If your product saves a customer $100K/year, charging $20K/year captures 20% of value delivered — a bargain regardless of what competitors charge. Pricing is the highest-leverage profit lever; a 1% price improvement drives 11% profit improvement (McKinsey).

6. **Use RICE scoring for prioritization but validate Confidence honestly.** RICE = Reach × Impact × Confidence ÷ Effort. The most common failure mode is overstating Confidence (rating everything 80% when actual certainty is 40%). Require evidence for Confidence ratings: A/B test results = 90%+, user interviews = 70%, competitor analysis = 50%, executive intuition = 20%.

7. **Build platforms as point-solution → platform, not platform-first.** The winning sequence: (1) solve one painful problem better than anyone (point solution), (2) accumulate users and data, (3) identify adjacent problems those users have, (4) expand to platform. Starting as a platform without initial applications = chicken-and-egg death. Plan platform expansion seams from day one, but ship point solutions.

8. **Track the "jobs to be done" (JTBD) that cause customers to "hire" your product, not demographics.** Demographics tell you who buys; JTBD tells you why. A 45-year-old VP and a 28-year-old founder may hire the same product for the same job. Interview customers about the moment they realized they needed a solution (the "struggling moment"), not their satisfaction with features.

9. **Run a "kill the product" exercise annually.** Ask: "If we were a startup competing against our own product today, how would we beat it?" This reveals complacency blindspots, feature bloat, and pricing gaps. Most product teams never ask this question because they're optimists by training. Pessimism is a strategic tool.

10. **Define OKRs with outcomes, not outputs.** "Ship onboarding v2" is an output. "Increase week-1 activation rate from 25% to 40%" is an outcome. Output-based OKRs measure activity; outcome-based OKRs measure value. When the team ships v2 and activation doesn't move, an output-based OKR says "success" while an outcome-based OKR says "we learned something — iterate."

## Anti-Patterns
**(STANDARD)**

- **TAM (Total Addressable Market)** top-down calculations: "Global CRM market is $80B, if we capture 1%..." — that 1% number is the most important variable and it's made up. Bottom-up TAM (number of target customers × annual contract value) is slower to calculate but 10x more defensible.
- **Product-market fit surveys** asking "How disappointed would you be if X didn't exist?" — the "40% very disappointed" threshold (Sean Ellis test) only works AFTER the product has active usage. Pre-launch surveys return noise because respondents imagine an idealized product, not yours.
- **Build vs buy vs partner decisions** — "Buy" means "integrate and maintain forever." A $15K/year SaaS tool with 6-week integration and ongoing schema migrations may cost more over 3 years than a $120K internal build. Calculate TCO (total cost of ownership) over 36 months minimum.
- **Competitive analysis** comparing your roadmap v1 against competitor v3 — the competitor will ship v4 by the time you ship v1. Compare against the competitor's likely trajectory, not their current state. Time-shifted comparisons systematically understate competitive risk.
- **Platform vs point solution** decisions require a chicken-and-egg user base. A platform with no initial applications has no users; a point solution with no platform can't expand. The winning sequence is point-solution-first, then platform expansion — but only if you plan the expansion seams from day one.
- **Feature prioritization by "highest-paid person's opinion" (HiPPO).** The CEO wants an AI chatbot because competitors have one. The engineering team drops everything for a 3-month build. Launch day: 2% of users try it, 0.3% use it regularly. Meanwhile, the "boring" CSV export fix that 40% of power users requested sits in the backlog, and churn ticks up among your highest-value cohort. **Total cost: $180K-$250K in engineering time (3 engineers × 3 months) plus $300K-$800K in avoidable churn from neglected power users over 12 months.** Fix: Use a weighted scoring framework (RICE: Reach × Impact × Confidence ÷ Effort) for ALL prioritization decisions; validate demand with a concierge test or fake-door experiment before committing engineering resources.
- **Pricing page that hides all prices behind "Contact Sales."** Enterprise buyers who prefer self-service (now 60%+ of B2B buyers according to Gartner) bounce immediately. Your competitor publishes transparent pricing and captures the evaluation while you're still routing the "Request a Quote" form to the right SDR. **Total cost: $500K-$2M in lost inbound pipeline annually — 15-30% of your addressable self-serve segment never enters the funnel.** Fix: Publish at least a "Starting at" price with a self-service tier or transparent pricing calculator; gate only the enterprise custom pricing; A/B test contact-sales vs transparent pricing on your pricing page.
- **Roadmap driven entirely by customer requests without strategic filtering.** You build every feature the top 5 customers ask for. Two years later, your product is a Frankenstein of custom integrations that only those 5 customers use. New prospects see a cluttered product built for someone else's problems and choose a focused competitor. **Total cost: $1M-$3M in engineering investment in features with zero new-customer acquisition value, plus slowing growth as your product loses competitive differentiation.** Fix: Maintain a "strategic filter" — every feature must map to a company-level strategic goal; track feature adoption by customer segment; sunset features used by < 5% of customers annually; say no with data: "We're prioritizing X because it serves 60% of our ICP."

- **What:** Setting product roadmap by copying the competitor's feature list. **Why:** You're fighting yesterday's battle on their terms. By the time you ship parity, they've moved to v4 — and you've invested $200K-$500K in features your customers never asked for. Feature parity is a strategy for perpetual second place. **Instead:** Identify the job your customers hire your product for that competitors serve poorly. Build depth in that job. Win on differentiation, not imitation.

- **What:** Prioritizing features based on the loudest customer's request without strategic filtering. **Why:** The loudest customer represents exactly one data point with unknown representativeness. Building for them optimizes for retention of one account at the expense of acquisition of dozens. Two years later, your product is a Frankenstein of custom work that only 5 customers use. **Instead:** Use a weighted scoring framework (RICE or CD3). Validate demand with 10+ customers before committing. Every feature must map to a company-level strategic goal.

## Production Checklist
**(STANDARD)**

Before any product strategy deliverable leaves this skill, verify:

- [ ] Product-market fit assessed with Sean Ellis survey (post-launch) or 20+ customer discovery interviews (pre-launch)
- [ ] North Star metric defined as input metric measuring core value exchange, not revenue
- [ ] TAM/SAM/SOM calculated bottom-up with documented assumptions, dated within 90 days
- [ ] Competitive analysis includes competitor trajectory forecasting, not just current-state comparison
- [ ] PLG vs SLG decision documented with product complexity, ACV, time-to-value, and viral coefficient analysis
- [ ] Pricing strategy validated with willingness-to-pay data (Van Westendorp or conjoint), not competitor benchmarking
- [ ] RICE or CD3 prioritization framework applied with documented Confidence evidence for each item
- [ ] Jobs-to-be-done identified for primary customer segment with "struggling moment" interview data
- [ ] Platform expansion seams designed (for point-solution products planning platform moves)
- [ ] OKRs are outcome-based (measure value delivered), not output-based (measure activity completed)
- [ ] "Kill the product" exercise completed within last 12 months with documented competitive vulnerability assessment
- [ ] Customer journey map exists for primary persona covering acquisition, activation, retention, referral, revenue
- [ ] Feature adoption tracked by cohort — features used by < 5% of customers flagged for sunset consideration
- [ ] Product strategy document includes explicit assumptions, risk register, and early warning indicators

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Building features from competitor parity without strategic differentiation | Commoditization — you compete on price alone, margins erode to zero | Every feature must answer: "Why would a customer choose US for this instead of the incumbent?" If the answer is "because we have it too," it's not worth building. Identify your unique advantage and build around it. |
| OKRs that measure output (features shipped) instead of outcomes (behavior changed) | Ship factory — lots of features, zero impact on retention or revenue | Frame every OKR as a customer behavior change: "X% of users now do Y weekly" instead of "Ship Z feature." If you can't describe the behavior change, you haven't defined the outcome. |
| Skipping problem validation and jumping to solution design | Building the wrong thing really well — months wasted on a solution nobody needs | Run at least 10 customer discovery interviews before writing a single requirement. Find the "struggling moment" — the specific situation where customers feel acute pain. If they're not already hacking together a workaround, the problem isn't urgent enough. |
| Pricing based on competitor-minus instead of willingness-to-pay | Leaving 20-40% of potential revenue on the table, or pricing yourself out of the market | Run Van Westendorp or conjoint analysis on your target segment. Your price should reflect YOUR value delivered, not what competitors charge. A competitor's price anchors on THEIR value, not yours. |
| Confusing TAM (total addressable market) with SAM (serviceable available market) in board decks | Overstated market opportunity that erodes investor and board trust | TAM = everyone who could theoretically use your product. SAM = the segment you can actually reach with your current GTM motion. Present SAM as your near-term reality. Break TAM into SAM → SOM (serviceable obtainable market) with documented assumptions at each layer. |

## Verification

- [ ] TAM/SAM/SOM: bottom-up calculation with documented assumptions and source data
- [ ] Competitive landscape: positioning map updated within last 90 days
- [ ] Build vs buy vs partner: TCO calculated over 36 months for each option
- [ ] Product-market fit: Sean Ellis survey conducted (if post-launch) or customer discovery interviews complete (if pre-launch)
- [ ] Strategic assumptions: all assumptions documented, risk-ranked, and validated or invalidated with evidence

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## Scale Depth

### Solo (Founder-PM, pre-PMF, 0-5 customers)
- PMF: Customer discovery interviews (20+), not surveys. Find the "struggling moment"
- North Star: Leading indicator of value (daily active, core action completion) — simple enough to track manually
- Prioritization: Founder judgment + customer urgency. No formal framework needed yet
- Pricing: Cost-based or competitor-anchored — validate willingness to pay before scaling
- OKRs: Not yet — use 3-5 quarterly rocks until you have reliable metrics
- Competitive: Know 3-5 direct competitors. No formal analysis needed
- Deliverable: 1-page lean product strategy canvas

### Small (PM + 5-20 engineers, post-PMF, $1M-$10M ARR)
- PMF: Quarterly Sean Ellis survey, cohort retention analysis, NPS by segment
- North Star: Instrumented metric with dashboard. Weekly review cadence
- Prioritization: RICE or CD3 scoring. Formal backlog with Confidence evidence
- Pricing: Value-based pricing with Van Westendorp analysis. A/B test price points
- OKRs: Company-level outcome-based OKRs (3-5). Quarterly review with grading
- Competitive: Formal competitive analysis updated quarterly with trajectory forecasting
- Deliverable: Product strategy document (5-10 pages) + roadmap (next 4 quarters)

### Medium (PM team + 20-100 engineers, $10M-$50M ARR)
- PMF: Multi-segment PMF analysis. Product-market-expansion-fit for adjacent markets
- North Star: Cascaded — company NSM → product line metrics → feature-level metrics
- Prioritization: Portfolio prioritization — optimize across products, not within one
- Pricing: Multi-tier pricing with expansion revenue path. Price sensitivity by segment
- OKRs: Fully cascaded (company → product → team). Quarterly review with calibration
- Competitive: War-gaming exercises. "Kill the product" workshop annually. Win/loss analysis
- Deliverable: Annual product strategy + quarterly business review + product portfolio roadmap

### Enterprise (CPO + 100+ engineers, $50M+ ARR)
- PMF: Multi-product PMF with cannibalization analysis. Platform PMF for developer ecosystem
- North Star: Multi-metric dashboard with causal model linking input metrics to financial outcomes
- Prioritization: Capital allocation framework across product lines. Investment committee process
- Pricing: Global pricing with regional optimization, bundling strategy, and packaging science
- OKRs: Multi-level cascade with cross-functional alignment. Annual + quarterly + monthly review
- Competitive: Dedicated competitive intelligence function. Scenario planning for market shifts. M&A target identification
- Deliverable: 3-year product strategy + annual operating plan + quarterly board review + analyst briefings

## Error Decoder
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| "Very disappointed" score is 45% but churn is 8%/month | PMF survey run on early adopters (enthusiasts), not mainstream users. Early adopters tolerate rough edges; mainstream users don't. | Segment survey by cohort: signup date, usage frequency, plan tier. PMF must hold across segments, not just in aggregate. Run the survey for each cohort separately. | PMF isn't binary and it isn't uniform — it degrades by segment. |
| RICE-scored backlog has 47 "high priority" items | Confidence scores are inflated — everything rated 80-90% when actual evidence is thin. Reach and Impact are also inflated to justify pet projects. | Require evidence for every Confidence rating: A/B test = 90%, user interviews = 70%, competitor analysis = 50%, executive intuition = 20%. Enforce calibration — if > 30% of items score "high," the scoring system is broken. | RICE without evidence calibration is HiPPO with extra steps. |
| Launched PLG motion; enterprise sales pipeline dropped 60% in 2 quarters | PLG and SLG motions conflicted — self-serve product undercuts enterprise pricing, enterprise sales team demoralized by product-led bypass | Design PLG→SLG handoff: free tier converts to sales-assisted at usage threshold. Enterprise features gated behind sales. Sales comp adjusted to credit product-sourced pipeline. | PLG and SLG need a handshake, not a handoff. |
| Competitor launched feature you "knew about" but didn't expect for 12 months; you're 9 months behind | Competitive analysis compared their current product (v3) against your roadmap, ignoring their trajectory (hiring, patents, conference talks signaled v4 timeline) | Add trajectory analysis to competitive review: track competitor hiring (especially in specific domains), engineering blog posts, open-source contributions, conference talks. Forecast their next 2 releases. | Compete against their next version, not their current one. |
| "Kill the product" exercise reveals you'd beat your own product on 4 of 7 axes | Product has accumulated feature bloat, onboarding friction, and pricing complexity over 3+ years. Incremental improvements haven't addressed structural issues. | Run the exercise seriously — assign one PM to build a competitive startup's product strategy against your own. If the startup wins on onboarding, pricing, or core workflow speed, those become Q1 priorities. | Your product's biggest competitor is the startup you're not building. |
| Top-requested feature shipped after 6 months; 3% adoption at 90 days | Feature prioritized by request volume, not strategic fit. Vocal minority ≠ majority demand. No fake-door test or concierge MVP to validate before building. | Before building, run a fake-door test: add the feature to the UI with a "Coming Soon" notice and track clicks. If < 20% of target users click, don't build it. Interview the 3% who adopted to understand if the problem was the feature or the discovery. | Request volume measures noise, not demand. |

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **MVP vs Growth vs Scale**: See [mvp-growth-scale.md](references/mvp-growth-scale.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

