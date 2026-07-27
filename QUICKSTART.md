# Quickstart — 5 Minutes to Your First Skill Chain

> **Goal:** Install the skills library, invoke your first skill, chain two skills together, and see a real output — all in 5 minutes.

---

## Step 1: Install (30 seconds)

```bash
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
```

This clones the library to `~/.zeroes-ones/skills` and creates symlinks for Claude Code, Copilot CLI, Cursor, and OpenClaw.

**Verify:**
```bash
ls ~/.zeroes-ones/skills/skills/  # Should show 00-framework, 01-strategy, ...
```

---

## Step 2: Activate in Your Project (15 seconds)

```bash
cd your-project/
skills-init
```

This creates `.claude/skills`, `.copilot/skills`, etc. as symlinks so your AI agent can discover all 214 skills.

---

## Step 3: Invoke Your First Skill (1 minute)

Open your AI agent (Claude Code, Copilot CLI, Cursor, etc.) and type:

```
/system-architect: I'm building a URL shortener. What architecture should I use?
```

**What to expect:** The agent reads `system-architect/SKILL.md`, follows its decision tree, and produces:
- A recommendation (e.g., "Monolith — you're solo, this is simple")
- Architecture Decision Records (ADRs) for key choices
- A component diagram showing services and data flow
- Trade-offs explained (why NOT microservices right now)

> **Tip:** Every skill has a `<!-- QUICK: 30s -->` marker at the top of each section. Read just those to get the gist in 30 seconds. The `<!-- STANDARD: 3min -->` sections give working knowledge. `<!-- DEEP: 10+min -->` sections cover war stories and edge cases.

---

## Step 4: Chain Two Skills (1 minute)

Skills declare their dependencies in YAML `chain:` blocks. Feed output from one skill into the next:

```
/backend-developer: Use the architecture from system-architect to build the URL shortener API. I need POST /shorten, GET /:slug, and GET /:slug/stats endpoints.
```

The backend-developer skill knows it `consumes_from: [system-architect]` — it expects architecture decisions as input and produces API code as output.

Then feed the API to the reviewer:

```
/code-reviewer: Review the URL shortener API code that backend-developer just produced.
```

**What to expect:** The reviewer catches issues the developer missed — missing input validation, SQL injection risks, missing error handling. All 1,675 chain edges are bidirectionally symmetric (verified programmatically).

---

## Step 5: Scale Up When Ready (30 seconds)

As your project grows, activate more skills:

```bash
skills-init --grow   # 18 skills: add CI/CD, observability, SEO, analytics
skills-init --full   # 214 skills: full enterprise coverage
```

See [`examples/logsnap-solo-to-scale/`](examples/logsnap-solo-to-scale/) for a complete walkthrough of tiered activation — going from solo MVP (8 skills) to $25K MRR (56 skills).

---

## What You Just Learned

| Concept | How It Works |
|---------|-------------|
| **Skill invocation** | `/skill-name: your request` — the agent reads SKILL.md and follows its workflow |
| **Progressive disclosure** | QUICK (30s gist) → STANDARD (3min working knowledge) → DEEP (10+min war stories) |
| **Skill chaining** | Output from skill A feeds into skill B via `chain:` YAML declarations |
| **Tiered activation** | `--solo` (8 skills) → `--grow` (18) → `--full` (214) — activate only what you need |

---

## Next Steps

- **[USAGE-GUIDE.md](USAGE-GUIDE.md)** — Deep dive into skill anatomy, error decoders, decision trees, and advanced patterns
- **[examples/](examples/)** — Real projects built with skills (solo SaaS, team platform, trading system)
- **[PROJECT-BOOTSTRAP.md](PROJECT-BOOTSTRAP.md)** — Phase-by-phase guide: idea → production, all 106 skills mapped
- **[SKILL-QUALITY-STANDARDS.md](SKILL-QUALITY-STANDARDS.md)** — Quality bar and external reviewer scoring rubric
- **[COORDINATION-MATRIX.md](COORDINATION-MATRIX.md)** — Full dependency graph with 1,675 symmetric chain edges

---

*Built by [Zeroes & Ones](https://github.com/zeroes-ones/Skills). 214 skills, 29 domains, 9.9/10 quality.*
