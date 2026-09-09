# Using the Services Stack — Quick Guide

Freelancer/agency view: how to actually *use* the estimation → pricing → SOW → support skills
and the runnable examples, from install to a signed engagement.

Related pages: fit by *type* → `docs/client-request-playbook.md`; fit by *size* →
`docs/service-size-fitting.md`; deep benchmarks → `docs/estimation-research.md`.

---

## 1. Install (once)

```bash
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
cd client-project && skills-init        # --solo (8) | --grow (18) | --full
skills-update                            # later: pull updates
```

The skills are plain `SKILL.md` markdown under `skills/<domain>/<name>/`, so you can also just
clone the repo and let your agent read them (or follow them yourself).

## 2. Four ways to use a skill

| Way | How | When |
|---|---|---|
| **A. Agent auto-routes** | Describe the job; the agent matches your words to the skill's `description` triggers and follows the SKILL.md | daily work |
| **B. Invoke by name** | Claude `/{name}` · Cursor `@skill-{name}` · Copilot `/copilot-skill {name}` · or "Act as `<name>` and…" | you know the skill |
| **C. Read & execute** | Open `SKILL.md`, run its `## Core Workflow` + `## Verification` yourself | no agent, or learning |
| **D. Run as a workflow graph** | `python3 scripts/workflow-runner.py --manifest <example>.yaml --executor <executor>.py` | multi-step delivery with loops and gates |

### 2a. Exact invocation syntax, per tool (after `skills-init` in the project)

| Tool | Invoke by name | Auto-invoke |
|---|---|---|
| Claude Code | `/{skill-name}` e.g. `/software-project-estimator` | describe the job; it routes via descriptions |
| GitHub Copilot CLI | `/copilot-skill {name}` | same |
| Cursor | `@skill-{name}` | same |
| OpenClaw | `/{name}` | same |
| Gemini CLI | paste SKILL.md content or custom injection | same |

Example conversation to invoke a skill explicitly:

```
You: /services-engagement-pricing
     Act as services-engagement-pricing. Solo freelancer, B2B client, effort base 5 weeks
     (range 4–6.5) from software-project-estimator. Build the rate card and give a fixed
     quote with buffer + milestone split.
Agent: reads the skill, runs its Core Workflow, returns rate card + quote + assumptions.
```

Verify it loaded: the agent should follow the skill's sections (decision trees, `Complete
when` outputs, verification table). If it answers from memory instead, invoke by name with
"Read `skills/15-sales/services-engagement-pricing/SKILL.md` first, then…".

## 3. The skills and the prompts that trigger them

| Skill | Ask it (paste after "Act as `<skill>` and…" or route by intent) | Output |
|---|---|---|
| `software-project-estimator` | "Estimate <project>. Give low/base/high effort, size class, contingency, assumptions." | effort range + register |
| `consulting-effort-estimator` | "Estimate this discovery/design/data/fractional engagement in consultant-days." | day range + mix |
| `services-engagement-pricing` | "Price this effort for a B2B client. Build the rate card; fixed or T&M? buffer, milestones." | quote + terms |
| `statement-of-work-authoring` | "Draft the full SOW from this estimate + quote (scope, deliverables+acceptance, milestones, change control, placeholders)." | SOW draft |
| `software-maintenance-support-estimator` | "Estimate annual support for this build. SLA tier? retainer bucket? enhancement lane?" | support price |
| `legal-advisor` | "Review this SOW for risks before I send it." | legal review |

## 4. End-to-end freelancer flow (worked example)

Client: *"build me a booking SaaS MVP, then maintain it."*

1. **Size it** — `docs/service-size-fitting.md` → **M** (4–6 weeks); copy
   `examples/payments-api-ship`; model = fixed + buffer.
2. **Estimate** — `software-project-estimator` → `M · base ~5 wk · range 4–6.5 wk · +25% risk`
   + assumptions register.
3. **Price** — `services-engagement-pricing` (solo, B2B) → rate card (~$140–160/h from your
   costs) → fixed quote base + 20% buffer → milestones 30/30/40.
4. **SOW** — `statement-of-work-authoring` → full draft → `legal-advisor` review → sign.
5. **Deliver** — run the example (see §5), or let your agent execute each node's skill; the
   human release gate is you.
6. **Support terms** — `software-maintenance-support-estimator`: build ≈ $55K → **15–20%/yr ≈
   $8–11K/yr** retainer + enhancement T&M lane → attach as a support annex.

Every client ask maps to the same loop — swap estimators by job type and the example by row:

| Client ask | Estimator | Example to run | Typical gates |
|---|---|---|---|
| new app / feature | software-project-estimator | `payments-api-ship` / `add-feature` | release / acceptance |
| UI change | software-project-estimator (S) | `ui-change` | acceptance |
| API change | software-project-estimator | `api-change` | contract review |
| create DB | software-project-estimator | `db-create` | schema + release |
| migrate DB/system | software-project-estimator (L) | `strangler-migration` | plan + cutover |
| discovery / fractional / non-dev services | consulting-effort-estimator | run directly | deliverable acceptance |
| support / maintenance | software-maintenance-support-estimator | `support-maintain` | month close |
| prod incident | incident workflow | `production-incident` | commander |

## 5. Running an example graph

```bash
# smoke (deterministic stub)
python3 scripts/workflow-runner.py --manifest examples/payments-api-ship/payments-api-ship.yaml

# with the teaching executor (real traces: parallel audits, loop, agent gate, human release)
python3 scripts/workflow-runner.py \
    --manifest examples/payments-api-ship/payments-api-ship.yaml \
    --executor examples/payments-api-ship/executor_demo.py --state /tmp/booking.json
# inspect /tmp/booking.json: nodes, log (done | agent-gate | escalate), handoff, outcome
```

With a real agent executor (`--executor scripts/executors/agent_executor.py` + `AGENT_CMD`),
each node is executed by your agent grounded in that skill — the engine still owns ordering,
budgets, loops, handoffs, and gates.

**Want it auto-generated?** Describe the goal and let
`scripts/goal-to-graph.py` build the whole spec-to-ship graph for you (loop → agent gate →
human release gate): see `examples/goal-to-ship/README.md`.

## 6. If something doesn't fit

- Job too vague to size → run a fixed discovery day-box first, then size.
- No actuals → widen the bands, tag figures `[ESTIMATED]`, calibrate from each skill's
  `examples/backtest/`.
- Mixed-size program → split into size bands and run each band's row (§ `service-size-fitting`).
- Support included → price it while the build is fresh (15–25%/yr + true-up).

## 7. Where everything lives

- Skills: `skills/12-operations/software-project-estimator`, `skills/12-operations/consulting-effort-estimator`,
  `skills/15-sales/services-engagement-pricing`, `skills/11-legal/statement-of-work-authoring`,
  `skills/15-sales/software-maintenance-support-estimator`, `skills/11-legal/legal-advisor`
- Examples + diagrams: `examples/README.md`, `examples/DETAILED-DIAGRAMS.md`
- Onboarding: `examples/payments-api-ship/TUTORIAL.md`

**The honest one-liner:** skills are playbooks, not magic — paste the client ask, name the
skill (or let the agent route), and execute the `SKILL.md`; the money skills convert the work
into estimate → quote → SOW → support terms; the examples show the whole thing as a runnable
graph with your human gates.
