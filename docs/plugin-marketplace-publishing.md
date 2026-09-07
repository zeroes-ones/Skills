# Plugin & Marketplace Publishing — How to Package, List, and Monetize

How to turn this skills library into **plugins/marketplaces** (Claude Code, skills.sh, and the
wider 2026 agent-store ecosystem) and the realistic revenue model. Companion to
`docs/distribution-best-in-class.md` (registry strategy) and `COMPARISON.md` (measured standing).

> Money numbers below are DIRECTIONAL: platform revenue-share figures conflict across sources
> (Anthropic "zero commission at launch" vs "85/15" vs "terms unpublished"; GPT Store ~$0.03/
> conversation; Windows Agent Store 85% developer share). Median skill earnings are near zero;
> treat every payout figure as an estimate to verify at signing time.

## 1. The two-manifest model (Claude Code marketplaces)

A **marketplace** is a repo with `.claude-plugin/marketplace.json`; each **plugin** inside it has
`.claude-plugin/plugin.json`.

`plugin.json` (minimal):
```json
{
  "name": "workflow-engine",
  "version": "1.0.0",
  "description": "Loops, graphs, and verified handoffs for agentic work",
  "author": { "name": "Sandeep Kumar Penchala" },
  "skills": ["./skills/"]       // component path arrays: commands, skills, agents, hooks, mcpServers
}
```
Required: `name` (kebab-case), `version` (semver), `description`, `author`; optional
`homepage`, `repository`, `license`, `keywords`, `category`, plus component path fields.

`marketplace.json` (catalog):
```json
{
  "name": "zeroes-ones-skills",
  "owner": { "name": "Sandeep Kumar Penchala" },
  "plugins": [
    { "name": "workflow-engine", "source": "github", "repo": "zeroes-ones/Skills", "category": "workflow" },
    { "name": "context-optimizer", "source": "./plugins/context-optimizer", "version": "1.0.0" }
  ]
}
```
- `source`: relative path (Git-based marketplaces), `github`/`repo` (+ optional `ref`/`sha`),
  git URL, or `git-subdir`.
- `strict` (default true): when true, `plugin.json` is the authority; `strict: false` lets the
  marketplace entry carry the whole definition.

**Commands:** `/plugin marketplace add <owner/repo|url|dir>`, `/plugin install name@marketplace`,
`claude plugin validate .` (schema/dup/traversal/component checks), `marketplace update`, `plugin
update`. Private hosting works (git credential helpers); org distribution via Settings → Plugins.

## 2. What WE already satisfy and the concrete gap

- Our skills already follow the open `SKILL.md` standard (frontmatter name/description, optional
  `license`, `version`, `tags`, `references/`, `scripts/`, `examples/`) — same format plugins
  ship.
- We do NOT yet emit `.claude-plugin/plugin.json` per plugin nor a top-level `marketplace.json`,
  so nothing is installable as a Claude plugin today.

**Recommended packaging shape for this repo:**
1. Generate `.claude-plugin/marketplace.json` cataloging a curated **flagship set (~30 plugins)**,
   each `source: "github", repo: "zeroes-ones/Skills"` + `strict: false` with inline component
   paths (`skills: ["./skills/<domain>/<name>/"]`) so no 297 `plugin.json` files are needed for
   the curated list.
2. Add minimal `.claude-plugin/plugin.json` to the flagship dirs later for strict-mode
   consumers (or a generator that emits one per plugin during release).
3. Validate every PR: `claude plugin validate .` locally/CI.
4. Publish a second, **private "pro" marketplace** repo for enterprise/org features (paid tier),
   using git-URL sources.

## 3. skills.sh plugin manifests

Vercel Labs' `skills` CLI also supports plugin-style manifests (advanced:
`plugin-manifests`). Publishing the flat `skills-sh/<name>/SKILL.md` index (see
`distribution-best-in-class.md`) is the prerequisite; a `plugin.json` there adds marketplace
compatibility on top of registry discovery.

## 4. Monetization reality (2026, directional)

| Channel | Terms (verify at signing) | Notes |
|---|---|---|
| Claude marketplace / Skills | 0% launch OR 85/15 developer share (conflicting) | curated partners first; review/safety screening |
| GPT Store | ~$0.03/conversation; ceiling ~$2-5k/mo for viral | median ≈ $0 |
| Windows Agent Store | 85% developer share | early, framework open-sourced |
| OpenClaw/ClawHub, Agensi | ~80-85% dev (Agensi 20% + $0.50) | paid skills $10-200; payments immature |
| Agent-to-agent (OpenStall) | credit-based | emerging |
| **B2B/services (real money)** | $1.5k setup + $300/mo client; $5-20k enterprise GPTs; % of closed deals | where median creators earn |

Reality: **platform payouts are weak and skewed (top 10% ~$500-3k/mo, median < $50/mo)**. The
durable model for this library:

1. **Keep the core MIT and free** (trust + distribution are the moat — matches our philosophy).
2. **Sell the edge**: enterprise/org private marketplace (verified workflow engine, SLI/observability
   suite, priority skills) under a commercial license — the open-core model used by NanoClaw et al.
3. **Sell the outcome, not the skill**: consulting/B2B (setup + maintenance + outcome pricing)
   powered by the skills; freelancing demand for AI agent skills grew ~109% YoY (2026).
4. **Sponsorships/grants**: GitHub Sponsors + foundation-style funding (AICP "freshness gating"
   pattern: keep N-1 free, gate latest behind a sponsorship token if desired — controversial; weigh
   carefully against trust).
5. Pricing sweet spot for any paid skill: $5-15; $30+ needs proprietary methodology + updates.
   Best-selling categories (2026): testing, code review/security, framework codegen, DevOps,
   documentation.

## 5. Concrete next steps for this repo (in order)

1. `scripts/emit-marketplace.py` → generates `.claude-plugin/marketplace.json` + per-flagship
   `plugin.json` (name/version/description/license + skills paths) from existing frontmatter;
   wired into CI validation.
2. Add `claude plugin validate .` (or `npx @anthropic-ai/claude-code`-based check) to the lint
   job when the CLI is available.
3. Publish: push curated marketplace; add `skills.sh` flat index (per distribution doc); add
   marketplace links to README.
4. Monetize edge: private "pro" marketplace repo + B2B offer; keep core MIT; document the offer
   page.

Sources (directional): Claude Code plugin-marketplaces/plugins-reference docs & schema notes;
vercel-labs/skills plugin-manifests; Agent Market Cap creator-economy & distribution reports;
SkillSafe platform comparisons; OpenClaw monetization community reports; VentureBeat (open-core +
managed services); openstall (agent-to-agent). Verify terms at signing.
