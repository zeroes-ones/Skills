# Decision Trees for scrum-master

### Scrum vs Kanban vs Scrumban
```
                     ┌──────────────────────────────┐
                     │ START: Which agile framework?  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Work arrives predictably in     │
                    │ batches (features, epics) vs    │
                    │ continuous flow (tickets, bugs)?│
                    └────┬──────────────────────┬───┘
                         │ Batches             │ Continuous
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Team needs     │    │ Need predictable │
                    │ regular        │    │ delivery         │
                    │ ceremony       │    │ cadence (e.g.,   │
                    │ cadence for    │    │ release every    │
                    │ alignment?     │    │ sprint)?         │
                    └──┬────────┬───┘    └──┬──────────┬────┘
                       │YES     │NO        │YES       │NO
                  ┌────▼───┐ ┌─▼──────┐ ┌─▼──────┐ ┌─▼──────────┐
                  │Scrum   │ │Scrumban│ │Scrumban│ │Pure Kanban │
                  │2-week  │ │Sprints │ │Sprints+│ │WIP limits, │
                  │sprints,│ │+ WIP   │ │Kanban  │ │continuous  │
                  │all     │ │limits, │ │metrics │ │flow, CFD   │
                  │ceremonies│ │fewer   │ │        │ │metrics     │
                  └────────┘ │ceremon.│ └────────┘ └────────────┘
                             └────────┘
```
**When to choose Scrum:** Predictable batched work, team needs regular alignment — full ceremonies (sprint planning, daily scrum, review, retro), 2-week cadence, defined sprint goal.
**When to choose Kanban:** Continuous inflow (support tickets, ops), no natural sprint boundary — WIP limits, cycle time, cumulative flow diagram (CFD), no fixed iterations.
**When to choose Scrumban:** Mix of planned features + unplanned work — retain sprint structure with WIP limits, fewer ceremonies, use CFD + burndown metrics.

### Sprint Length Decision
```
                     ┌──────────────────────────────┐
                     │ START: Sprint duration?        │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Requirements change frequently  │
                    │ (stakeholders want flexibility)  │
                    │ AND team is experienced?         │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ 1-week sprint │    │ Team new to      │
                    │ for fast      │    │ Scrum (<6 months)│
                    │ feedback.     │    │ OR work is       │
                    │ Risk: overhead │    │ complex (needs   │
                    │ of ceremonies │    │ spikes + deep    │
                    │ per sprint.   │    │ design)?         │
                    └───────────────┘    └──┬──────────┬────┘
                                           │YES       │NO
                                      ┌────▼────┐ ┌──▼──────────┐
                                      │3-4 week │ │2-week sprint │
                                      │sprint   │ │(default for  │
                                      │for      │ │most teams)   │
                                      │complex  │ │Balance of    │
                                      │work     │ │feedback +    │
                                      └─────────┘ │ceremony cost │
                                                  └──────────────┘
```
**When to choose 1-week:** Experienced team, volatile requirements, fast feedback needed — cost: ceremony overhead ~15% of sprint time.
**When to choose 2-week:** Default for most teams — balances feedback frequency with ceremony overhead (~10%), validates assumptions every 10 business days.
**When to choose 3-4 week:** New Scrum team or inherently complex work (research spikes, deep technical design) — more time to produce meaningful increment, less ceremony overhead.

### Retrospective Health Diagnosis
```
                     ┌──────────────────────────────┐
                     │ START: Retrospectives not      │
                     │ producing value?               │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Same issues surface sprint      │
                    │ after sprint — "Groundhog Day"  │
                    │ retro?                          │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Action items   │    │ Team disengaged  │
                    │ not completed  │    │ (quiet, phones,  │
                    │ or tracked?    │    │ laptops out)?    │
                    └──┬────────┬───┘    └──┬──────────┬────┘
                       │YES     │NO        │YES       │NO
                  ┌────▼───┐ ┌─▼───────┐ ┌─▼──────┐ ┌─▼──────────┐
                  │Implement│ │Issues are│ │Change  │ │Format is   │
                  │action   │ │systemic  │ │format: │ │fine —      │
                  │tracking │ │(outside  │ │silent  │ │investigate │
                  │board    │ │team      │ │writing, │ │why issues  │
                  │with     │ │control): │ │1-on-1  │ │not being   │
                  │owner +  │ │escalate  │ │check-  │ │raised      │
                  │deadline │ │to mgmt   │ │ins,    │ │(psycho-    │
                  └─────────┘ └──────────┘ │start-  │ │logical     │
                                           │stop-cont│ │safety?)    │
                                           │nue     │ └────────────┘
                                           └────────┘
```
**When to implement action tracking:** Same issues recurring — create visible action board with owner + deadline per item, review at start of each retro, escalate if >2 sprints stale.
**When to escalate:** Issues are systemic/organizational — team can't fix alone. Escalate with data (e.g., "3 sprints blocked by procurement SLAs").
**When to change format:** Disengagement — try silent writing, start-stop-continue, 4Ls (liked/learned/lacked/longed), or 1-on-1 check-ins to rebuild psychological safety.

### Impediment Escalation Triage
```
                     ┌──────────────────────────────┐
                     │ START: Team blocked by          │
                     │ impediment?                    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Can the team resolve it         │
                    │ themselves within 24 hours?     │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Team self-    │    │ Impediment is    │
                    │ resolves.     │    │ cross-team       │
                    │ SM monitors   │    │ dependency?      │
                    │ but doesn't    │    └──┬──────────┬────┘
                    │ intervene.    │       │YES       │NO
                    └───────────────┘  ┌────▼────┐ ┌──▼──────────┐
                                       │SM       │ │Organizational│
                                       │facilitates│ │blocker:     │
                                       │cross-team│ │SM escalates │
                                       │resolution│ │to leadership│
                                       │meeting   │ │with business │
                                       └──────────┘ │impact data  │
                                                    └─────────────┘
```
**When team self-resolves:** Impediment within team's span of control — SM observes and coaches but doesn't do it for them. Builds team autonomy.
**When SM facilitates cross-team:** Dependency on another team — SM schedules and facilitates resolution meeting, tracks action items, follows up daily.
**When SM escalates to leadership:** Organizational blocker (procurement, hiring, policy) — SM escalates with quantified business impact data, not just frustration.

### Scaling Framework Selection (LeSS vs SAFe vs Nexus)
```
                     ┌──────────────────────────────┐
                     │ START: Which scaling framework?│
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ 2-8 teams working on same       │
                    │ product, co-located or          │
                    │ timezone-aligned?               │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ LeSS (2-8     │    │ 5+ teams across   │
                    │ teams) or     │    │ multiple products, │
                    │ Nexus (3-9    │    │ need portfolio    │
                    │ teams) —      │    │ management,       │
                    │ lightweight,  │    │ compliance, and   │
                    │ single product│    │ enterprise        │
                    │ backlog       │    │ governance?       │
                    └───────────────┘    └──┬──────────┬────┘
                                           │YES       │NO
                                      ┌────▼────┐ ┌──▼──────────┐
                                      │SAFe     │ │Stay with    │
                                      │Full     │ │coordinated  │
                                      │with ART,│ │Scrum of     │
                                      │PI       │ │Scrums —     │
                                      │Planning,│ │don't        │
                                      │RTE role │ │over-framework│
                                      └─────────┘ └─────────────┘
```
**When to choose LeSS/Nexus:** Single product, 2-9 teams, co-located — LeSS (minimalist), Nexus (Scrum.org). Keep it simple; avoid SAFe overhead for single product.
**When to choose SAFe:** Enterprise with 5+ teams across multiple products/programs, need portfolio management, compliance, executive visibility — ART, PI Planning, RTE role.
**When to choose Scrum of Scrums:** 3-5 teams, no enterprise governance needed — lightweight coordination with ambassador from each team meeting 2-3×/week.
