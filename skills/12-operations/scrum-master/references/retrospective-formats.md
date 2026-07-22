# Retrospective Formats

> **Author:** Sandeep Kumar Penchala

Five battle-tested retrospective formats to keep your retros fresh, engaging, and productive. Companion to the [Scrum Master SKILL.md](../SKILL.md) and [Agile Ceremonies Guide](agile-ceremonies-guide.md).

---

## Format 1: Start / Stop / Continue

**Best for:** Teams new to retrospectives; clear, simple, action-oriented.

```
Setup (5 min):
  Whiteboard with 3 columns: START | STOP | CONTINUE

Gather Data (15 min):
  Silent writing (5 min): Each person writes sticky notes
  Group share (10 min): One person reads all their notes; others add

Insights (15 min):
  Cluster similar items; dot vote (3 votes per person)
  Discuss top 2–3 items in each column

Actions (10 min):
  1–2 actions from the top-voted items
```

**Example Output:**
| START | STOP | CONTINUE |
|---|---|---|
| Pair programming on complex stories | Merging PRs without code review | Daily standup at 9:30am |
| Writing ADRs for architecture decisions | Overcommitting in sprint planning | Demo to stakeholders every sprint |

---

## Format 2: 4Ls — Liked / Learned / Lacked / Longed For

**Best for:** Teams that want to balance celebration with improvement; emotionally aware teams.

```
Columns: LIKED | LEARNED | LACKED | LONGED FOR

LIKED: What did you enjoy about this sprint?
LEARNED: What new skill, insight, or fact did you discover?
LACKED: What was missing? (Tools, information, support, clarity)
LONGED FOR: What did you wish for? (Even if unrealistic — "I wish we had a dedicated QA")
```

**Facilitation tip:** Start with Liked and Learned (positive energy first), then move to Lacked and Longed For. This sequence builds psychological safety before diving into criticism.

---

## Format 3: The Sailboat

**Best for:** Creative teams; visual thinkers; when the standard format feels stale.

```
Draw a sailboat with the team:

    ╱▔▔▔▔╲
   ╱      ╲───► WIND (What's pushing us forward?)
  ╱  ⚓    ╲
 ╱  ANCHOR ╲    ANCHOR (What's holding us back?)
╱___________╲
              ROCKS (What risks are ahead?)
              ISLAND (What's our destination / goal?)
```

**Elements:**
- **Wind (pushes us):** CI pipeline speed, design system, team collaboration
- **Anchor (holds us back):** Flaky tests, unclear requirements, context switching
- **Rocks (risks ahead):** Upcoming dependency on another team, tech debt in legacy module
- **Island (destination):** Sprint goal or quarterly objective

---

## Format 4: Mad / Sad / Glad

**Best for:** Teams that need to surface emotions; after particularly stressful sprints.

```
Columns: MAD 😡 | SAD 😢 | GLAD 😊

MAD:  What frustrated or angered you?
SAD:  What disappointed you?
GLAD: What made you happy or proud?
```

**Psychological safety note:** This format surfaces strong emotions. Set ground rules: no personal attacks; use "I" statements; listen without defending. The Scrum Master should model vulnerability first.

**Good ground rule:** "What's said in retro stays in retro." (Exception: agreed action items.)

---

## Format 5: DAKI — Drop / Add / Keep / Improve

**Best for:** Process-heavy teams that need to simplify; teams with technical debt.

```
Columns: DROP | ADD | KEEP | IMPROVE

DROP:   What should we stop doing? (Processes, meetings, tools — not people)
ADD:    What new practice, tool, or ritual should we introduce?
KEEP:   What's working well that we should protect?
IMPROVE: What's valuable but needs tweaking?
```

**Example:**
| DROP | ADD | KEEP | IMPROVE |
|---|---|---|---|
| Friday deploy lockdown | Automated dependency updates | Daily standup | Sprint planning timebox (runs over) |
| Status report emails to manager | Architecture review for all new services | Code review requirement | PR review turnaround (currently 2 days) |

---

## Facilitation Best Practices

### Psychological Safety Prerequisites
- **Prime directive:** "Everyone did the best they could with what they knew at the time."
- Leaders speak last (or not at all in early phases).
- No phones, no laptops (except the facilitator for notes).
- Confidentiality norm: findings are shared, but individual attributions are not.

### Timeboxing
| Phase | 60-min Retro | 90-min Retro |
|---|---|---|
| Set the stage | 5 min | 10 min |
| Gather data | 15 min | 20 min |
| Generate insights | 15 min | 25 min |
| Decide actions | 15 min | 25 min |
| Close | 10 min | 10 min |

### Silent Brainstorming
Always start the "Gather Data" phase with 3–5 minutes of **silent, individual writing** before group discussion. This prevents anchoring on the loudest voice and surfaces diverse perspectives.

### Dot Voting
```
Each person gets 3 votes (dot stickers or markers).
Place dots on the items you believe are most important to address.
Discuss the top 2–3 items (by vote count) as a group.
```

---

## Action Item Tracking

### SMART Actions
```markdown
- [ ] ACTION: Add integration tests for payment flow
  Owner:    @jane
  Deadline: End of next sprint (Mar 15)
  Success:  Payment flow test coverage > 80%

- [ ] ACTION: Create runbook for database failover
  Owner:    @bob
  Deadline: Mar 8
  Success:  Runbook tested in staging; on-call team trained
```

### Review Next Retro
Always start each retrospective by reviewing the previous retro's action items:
- **Completed** → Celebrate ( ✅ )
- **In progress** → Is it still a priority? If not, drop it.
- **Not started** → What blocked it? Do we still need it? Re-assign if needed.
- **Dropped** → Explicitly close; document why.

---

## When to Use Which Format

| Team Situation | Best Format |
|---|---|
| New team, building trust | Start/Stop/Continue |
| After a big launch or milestone | Mad/Sad/Glad |
| Mid-project, steady state | 4Ls |
| Process feels heavy | DAKI |
| Team seems disengaged | The Sailboat |
| After an incident or outage | Mad/Sad/Glad + 5 Whys |

---

*Rotate formats. The same retro every sprint becomes ritual without reflection. Fresh formats keep the team engaged and surface different kinds of insights.*
