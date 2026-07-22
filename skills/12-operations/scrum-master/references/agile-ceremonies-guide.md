# Agile Ceremonies Guide

> **Author:** Sandeep Kumar Penchala

A practical guide to running Scrum ceremonies effectively — not just "going through the motions." Companion to the [Scrum Master SKILL.md](../SKILL.md).

---

## 1. Sprint Planning

### Agenda & Timebox
| Segment | Duration (2-week sprint) | Purpose |
|---|---|---|
| **Set the stage** | 5 min | Review sprint goal from last sprint; check capacity |
| **What:** Product Owner presents priority | 30 min | Top backlog items; answer "what" questions |
| **How:** Team breaks down stories | 90 min | Tasks, estimates, dependencies identified |
| **Commit:** Define sprint goal | 15 min | 1–2 sentence goal; team commits to sprint backlog |
| **Total** | ~2.5 hours | Timebox = 2 hours per week of sprint |

### Inputs
- Prioritized and refined product backlog (DEEP: Detailed, Estimated, Emergent, Prioritized)
- Team capacity (accounting for holidays, PTO, on-call)
- Historical velocity (last 3–5 sprints)
- Definition of Done

### Outputs
- **Sprint goal:** "Enable users to export analytics as PDF reports"
- **Sprint backlog:** Selected PBIs broken into tasks of ≤ 1 day
- **Capacity-committed plan:** Total story points ≤ velocity

### Anti-Patterns
- PO simply reads backlog titles without context
- Team overcommits to please stakeholders
- No sprint goal defined ("just do these tickets")
- Planning runs over timebox regularly

---

## 2. Daily Scrum

### The 15-Minute Standup

```
Timebox: 15 minutes (same time, same place every day)
Format:  Each team member answers:

  1. What did I do yesterday that helped us meet the sprint goal?
  2. What will I do today to help us meet the sprint goal?
  3. Do I see any impediments blocking me or the sprint goal?

NOT: Status report to the Scrum Master
IS:  Developers coordinating their work plan for the next 24 hours
```

### Anti-Patterns
| Anti-Pattern | Why It's Harmful | Fix |
|---|---|---|
| **Status report to SM** | SM becomes bottleneck; devs disengage | Team faces each other; SM stands to the side |
| **Problem solving** | Standup runs 30+ minutes; not everyone needed | "Let's take this offline" — note topic, schedule follow-up |
| **"I'm working on JIRA-1234"** | No context; no one learns anything | Say what you *accomplished*, not what ticket number you touched |
| **Same person speaks for 5 minutes** | Others tune out | SM gently intervenes: "Let's keep updates tight" |
| **People skip standup** | Coordination breaks down | Make standup valuable — if it's not, fix it, don't skip it |

---

## 3. Sprint Review

### Agenda (1 hour per week of sprint)
```
0–5 min:    SM sets context — sprint goal, what was committed
5–40 min:   Team demos working, potentially shippable increment
            — Live demo only (no slides, no mockups)
            — Each story: "Here's what we built, here's how it works"
40–50 min:  Stakeholder Q&A and feedback
50–60 min:  PO reviews backlog changes; discusses what's next
```

### Rules
- **Working software only.** If it's not demoable, it's not done.
- Stakeholders give feedback; PO decides what to do with it.
- No blame, no excuses — this is a celebration of progress.
- Feedback goes into backlog, not directly into next sprint (PO prioritizes).

---

## 4. Sprint Retrospective

### The 5 Phases

| Phase | Duration (90 min total) | Activities |
|---|---|---|
| **1. Set the Stage** | 5–10 min | Check-in question; establish psychological safety; review working agreements |
| **2. Gather Data** | 15–20 min | What happened this sprint? (timeline, metrics, events, emotions) — silent writing first |
| **3. Generate Insights** | 20–25 min | 5 Whys for top issues; group patterns; "What's the one thing we should change?" |
| **4. Decide What to Do** | 15–20 min | Pick 1–3 actionable improvements; SMART format; assign owners |
| **5. Close the Retro** | 5–10 min | Appreciations; retro of the retro (what worked about this session?) |

### Three Retrospective Formats (detailed in [Retrospective Formats](retrospective-formats.md))

---

## 5. Backlog Refinement

### DEEP Principles
- **D**etailed appropriately — top items are ready (2–3 sprints out); bottom items are coarse
- **E**stimated — top items have story points or t-shirt sizes
- **E**mergent — backlog changes as we learn; it's a living artifact
- **P**rioritized — ordered by value; 1 item is #1, not "all P0"

### INVEST Criteria for User Stories
| Letter | Criterion | Question to Ask |
|---|---|---|
| **I** | Independent | Can this story be delivered without another? |
| **N** | Negotiable | Is this a placeholder for conversation, not a spec? |
| **V** | Valuable | Does this deliver value to a user or stakeholder? |
| **E** | Estimable | Can the team roughly size this? |
| **S** | Small | Can this be done within a sprint? (If not, split it) |
| **T** | Testable | How will we know when it's done? |

### Refinement Cadence
- **Mid-sprint:** 1–2 hour session, team + PO
- **Goal:** Top of backlog has 2–3 sprints of ready stories (≅ definition of ready)
- **Definition of Ready:** Story has acceptance criteria, dependencies identified, UI mockups attached (if applicable)

---

## 6. Estimation Techniques

| Technique | Best For | How It Works | Time Per Story |
|---|---|---|---|
| **Story Points** | Established teams | Fibonacci (1, 2, 3, 5, 8, 13, 20); relative sizing | 2–5 min |
| **T-Shirt Sizes** | Early-stage, rough roadmapping | XS, S, M, L, XL; convert to story points later | 1–2 min |
| **Planning Poker** | Teams with anchoring risk | Everyone reveals estimates simultaneously; discuss outliers | 3–5 min |
| **Affinity Estimation** | Large backlogs (20+ items) | Silent grouping by relative size; quick calibration | < 1 min/item |
| **#NoEstimates** | Mature continuous-delivery teams | Split stories to be roughly same size; count throughput | 0 min |

### Story Point Reference Baseline
```
1 pt:  Trivial — fix a typo, change a config value       (~1 hour)
2 pts: Simple — add a small field to a form, minor bug    (~2–4 hours)
3 pts: Average — CRUD endpoint + tests                    (~1 day)
5 pts: Complex — new feature with integration tests        (~2–3 days)
8 pts: Large — new feature spanning multiple layers        (~3–5 days)
13 pts: Too large — must be split before sprint
```

---

## 7. Agile Metrics

| Metric | What It Measures | How to Use | Anti-Pattern |
|---|---|---|---|
| **Velocity** | Story points completed per sprint | Sprint capacity planning | Using as performance metric; comparing teams |
| **Sprint Burndown** | Work remaining vs time | Daily check: are we on track? | Micromanaging from burndown |
| **Cumulative Flow** | WIP across workflow states | Identify bottlenecks (widening bands) | Ignoring CFD; relying only on burndown |
| **Cycle Time** | Time from "in progress" to "done" | Predictability; process improvements | Optimizing for speed over quality |
| **Throughput** | Stories completed per week | Kanban capacity; forecasting | Confusing with velocity |
| **Escaped Defects** | Bugs found in production | Quality trend; test coverage gaps | Blaming individuals |

### Metrics Dashboard (Minimal Viable)
```yaml
sprint_metrics:
  velocity: [23, 21, 19, 25, 22]  # Last 5 sprints
  sprint_goal_met: [true, true, false, true, true]  # 80%
  cycle_time_p85: [3.2, 2.8, 3.5, 2.9, 3.1]  # days
  escaped_defects: [2, 1, 0, 3, 1]  # per sprint
```

---

## 8. Agile Anti-Patterns

| Anti-Pattern | Symptoms | Remedy |
|---|---|---|
| **ScrumBut** | "We do Scrum, but we skip retros… and the PO isn't available… and sprints are 6 weeks." | You're not doing Scrum. Either commit or switch methodology. |
| **Zombie Scrum** | Ceremonies happen, but no inspect-and-adapt. Velocity is flat for months. | Revive retros with real action items. Challenge the status quo. |
| **Water-Scrum-Fall** | "Sprint" is just a 2-week waterfall: design week 1, code week 2 + separate QA sprint. | Cross-functional teams. Build quality in, don't bolt it on. |
| **Feature Factory** | Output measured, not outcomes. "We shipped 47 stories!" — nobody used them. | Tie sprint goals to user outcomes. Measure adoption, not velocity. |
| **Proxy Product Owner** | PO delegates refinement to BA; team never talks to real PO. | PO must be available to team daily. No proxies. |
| **Sprint 0 Ad Infinitum** | "Just one more sprint of setup/architecture, then we'll start." | Start delivering value in sprint 1, even if small. Architecture emerges. |

---

## 9. Scrum Master Stance

```
FACILITATOR ── TEACHER ── COACH ── MENTOR ── IMPEDIMENT REMOVER ── CHANGE AGENT

When to be a Facilitator:   Running ceremonies; ensuring everyone is heard
When to be a Teacher:        Team new to Scrum; explaining the "why"
When to be a Coach:          Team is performing; asking powerful questions
When to be a Mentor:         Sharing experience with specific situations
When to be an Impediment Remover: Organizational blocker beyond team's control
When to be a Change Agent:   Systemic issues across the organization
```

---

*Great Scrum Masters don't just facilitate ceremonies — they build high-performing teams that continuously improve. The ceremonies are the scaffolding, not the building.*
