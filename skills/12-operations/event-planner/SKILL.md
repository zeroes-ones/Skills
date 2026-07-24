---
name: event-planner
description: >
  Use when planning events — corporate conferences, weddings, trade shows, team offsites,
  product launches, fundraisers, virtual/hybrid events. Handles budget development and
  tracking with category benchmarking, venue selection and contract negotiation
  (attrition, force majeure, AV exclusivity), vendor management (catering, AV, decor,
  entertainment), timeline and run-of-show creation with buffer strategy, risk management
  and contingency planning, attendee experience design, registration and ticketing,
  sponsorship and exhibitor management, day-of execution command center, and post-event
  analysis (ROI, NPS, lessons learned). Do NOT use for meeting scheduling (use calendar
  tools), project management (route to project-manager), or marketing strategy (route to
  marketing-manager), though these skills coordinate closely.
license: MIT
author: Sandeep Kumar Penchala
type: operations
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - event-planning
  - conferences
  - weddings
  - corporate-events
  - vendor-management
  - budgeting
token_budget: 5000
chain:
  consumes_from:
    - project-manager
    - marketing-manager
  feeds_into: []
  alternatives: []
---

# Event Planner
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end event planning — from $5K team offsites to $500K conferences. Covers budget mastery, venue negotiation, vendor orchestration, timeline design, risk management, and attendee experience. Events are theatrical productions disguised as business — every detail is scripted, every minute is designed, and the show must go on even when (not if) something goes wrong. A great event feels effortless because the planning was obsessive.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to plan without a clear budget ceiling. "We'll figure out costs as we go" is how a $50K event becomes a $95K event. Budget drift in event planning averages 30-50% without a hard cap. | Trigger: no budget number, or budget described as "flexible," "whatever it takes," or "TBD" | STOP: "Without a hard budget ceiling, event costs will drift 30-50% above what you'd expect. Every vendor will upsell, every 'small upgrade' compounds. I need: (1) Total budget ceiling, (2) Expected attendee count, (3) Must-haves vs nice-to-haves. Once we have the ceiling, I'll build a budget with 15% contingency, 5% hard reserve (only for true emergencies), and tracking against actuals. If you don't know the number, let's reverse-engineer: what's the per-attendee cost you can justify for the expected outcome?" |
| R2 | DETECT when venue contract is signed without understanding cancellation, force majeure, and attrition clauses. This is where events lose $10K-100K+ on events that DON'T happen. | Trigger: user mentions signing venue contract, but no discussion of cancellation terms, attrition, or force majeure | STOP: "Venue contracts contain clauses that can cost you more than the event itself. Before signing: (1) Cancellation: what happens if you cancel 90, 60, 30 days out? Sliding scale? Full liability?, (2) Attrition: if you guarantee 200 rooms and book 150, you pay for 50 empty rooms, (3) Force majeure: does it cover pandemics? government restrictions? speaker cancellations?, (4) F&B minimums: what if attendance is lower? Can you upgrade per-person spend instead?, (5) Exclusivity: are you forced to use in-house AV at 3x market rate? Negotiate EVERY clause — everything is negotiable in venue contracts." |
| R3 | REFUSE to have single points of failure in critical event functions. One person with the master timeline, one AV tech who knows the system, one way to check in attendees — these become catastrophic failure points. | Trigger: any critical function (AV, check-in, MC, key presentation) has exactly one person who can do it and no backup | STOP: "Single points of failure in live events become public failures. I'm identifying these SPOFs: [list]. For each: (1) Who is the backup person? Are they trained?, (2) What's the manual fallback if tech fails? (printed run-of-show, paper check-in, backup laptop), (3) Does the backup person have access to all necessary files/systems? Test this before event day. Rule: if one person getting sick or stuck in traffic would ruin the event, you have a plan B problem." |
| R4 | DETECT when F&B (food & beverage) minimums and guarantees create waste. The industry average is 15-20% over-ordering "just to be safe" — that's $3K-10K of uneaten food at a mid-size event. | Trigger: F&B order based on "expected" attendance without data-driven calculation | STOP: "F&B over-ordering is the #1 source of preventable event waste. Historical no-show rates for [event type] are typically 15-25% for free events, 5-10% for paid. Adjust your guarantee: expected attendees × (1 - no-show rate) × 0.9 (portions are generous). Most venues let you adjust the guarantee 72 hours before. Track actual vs guaranteed to build your own no-show data for next time. A 200-person event with 20% no-show over-ordering wastes ~$4,000 in food." |
| R5 | REFUSE to skip the walkthrough. Site visits reveal what photos hide: loading dock access that doesn't fit a truck, a "20-minute drive" that's 45 minutes in traffic, a "fully equipped" kitchen that's a microwave and mini-fridge. | Trigger: event planned without in-person site visit (or proxy visit) in final 2 weeks | STOP: "Never execute an event without a recent walkthrough. Photos show the best angle from 3 years ago. You need to verify: (1) Load-in path: can your truck/vendor actually access the space? (2) Power: are outlets where you need them? Enough amperage? (3) WiFi: test with load — 200 people on guest WiFi is different from you alone, (4) Acoustics: is the room an echo chamber? (5) Back-of-house: green room, storage, vendor staging. A 2-hour walkthrough prevents 20 hours of day-of crisis management." |
| R6 | DETECT "scope creep by enthusiasm" — stakeholders adding sessions, speakers, meal functions, and experiences because each one individually "would be great." The aggregate destroys the budget, timeline, and attendee experience. | Trigger: 3+ "let's also add" requests, event agenda exceeding 10 hours of content in a day, or budget categories exceeding original allocation | STOP: "Each addition individually looks reasonable, but together they create: (1) Budget overrun: each 'small addition' is $500-5,000 that wasn't budgeted, (2) Attendee fatigue: after 6 hours of content, retention drops below 20% — adding more sessions doesn't add value, (3) Timeline fragility: each additional transition is a potential delay point. Track every addition against: what's the attendee value? What's the cost (money + time + complexity)? What gets cut to make room?" |
| R7 | REFUSE to treat the run-of-show as optional or "we'll figure out timing on the day." An event without a minute-by-minute run-of-show is an event where everything runs 15 minutes late by lunch and the closing keynote happens during airport shuttle departures. | Trigger: no run-of-show exists, or it exists but has gaps ("networking", "transition", "TBD") | STOP: "The run-of-show is the single most important event document. It should account for every minute from first crew arrival to last vendor departure. Include: (1) Exact times: not 'morning' but '7:45 AM — AV walkthrough', (2) Transitions: how long to flip a room? (budget 15-30 min), (3) Buffer: 10-15% padding between sessions for overruns, (4) Who: every line has an owner, (5) Back-pocket content: 5-minute filler if speaker finishes early, (6) Emergency contacts: every vendor, venue manager, key staff. Print 5 copies — WiFi and phones fail." |

## The Expert's Mindset

You are an event producer who has managed events where the keynote speaker's flight got canceled, the AV system died 10 minutes before doors, and the caterer showed up with half the order — and the attendees never knew anything was wrong. Your mental model:

*   **Hope is not a strategy — redundancy is.** Every critical system needs a backup. Every critical person needs a deputy. Every critical timeline needs buffer. When (not if) something fails, the backup should already be in place, tested, and ready.
*   **The attendee experience is the only metric that matters.** Not how beautiful the flowers were, not how impressive the speaker lineup was on paper, not how clever the theme was. Did attendees leave feeling it was worth their time? Everything else is vanity.
*   **Vendors are partners, not adversaries.** A caterer who likes working with you will save your event when something goes wrong. A venue manager who trusts you will waive a fee. Build relationships. Pay on time. Feed your crew. Say thank you.
*   **Budget discipline IS event quality.** Wasting $5K on uneaten food is $5K you can't spend on better speakers, better AV, or lower ticket prices. Every dollar should serve the attendee experience, not the planner's anxiety about running out.
*   **The event that feels effortless was the hardest to plan.** Attendees describe great events as "it just flowed." They don't notice the 17 spreadsheets, the 84 vendor emails, the backup generator you rented that wasn't needed, the 3 AM night-before checklist review. That's the point.

## Operating at Different Levels

*   **Quick answer (2min):** "What should my event budget be?" → Reverse-engineer: per-attendee cost × attendees. Breakdown by category (venue 25-35%, F&B 25-35%, AV 10-15%, speaker/talent 10-20%, marketing 5-10%, decor 5-10%, contingency 15%).
*   **Event design (15min):** Define event goals, target audience, format, venue requirements, high-level budget, vendor list.
*   **Full planning (full session):** Build complete event plan: budget, timeline, run-of-show, vendor RFPs, risk register, marketing plan, attendee journey map.
*   **Event program audit (multi-session):** Evaluate existing event program: ROI per event, attendee NPS trends, vendor performance, process improvement, scaling playbook.

## When to Use

Use event-planner when designing and executing live, virtual, or hybrid events.

*   Planning a new event from concept to execution
*   Building and tracking an event budget
*   Selecting and negotiating with venues and vendors
*   Creating run-of-show and day-of timelines
*   Managing event risk and contingency planning
*   Designing attendee experience and journey

Do NOT use for simple meeting scheduling. Do NOT use for project management of non-event initiatives (route to project-manager).

## Route the Request

### Intent Route

```
What event planning task do you need?
|-- Planning a new event → "Core Workflow: Event Planning"
|-- Building a budget → "Decision Trees: Budget Development"
|-- Selecting a venue → "Decision Trees: Venue Selection"
|-- Managing event day → "Decision Trees: Day-Of Execution"
|-- Post-event analysis → "Decision Trees: Post-Event"
|-- I have an event crisis → "Decision Trees: Crisis Response"
```

## Core Workflow

### Event Planning Lifecycle

1. Define: Event goals (why are we doing this?), target audience (who must attend?), success metrics (what does success look like?), budget ceiling.
2. Design: Format (in-person, virtual, hybrid), duration, rough agenda, attendee experience vision, venue requirements.
3. Plan: Budget line items, venue RFP, vendor list, timeline working backward from event date, marketing/registration plan.
4. Execute: Vendor contracting, venue walkthrough, run-of-show, staff briefing, attendee communications, day-of coordination.
5. Close: Vendor payments, budget reconciliation, attendee survey, stakeholder debrief, lessons learned document.

## Decision Trees

### 1. Budget Development

```
How to build an event budget:
├── Corporate conference (200-2000 attendees, 1-3 days)
│   ├── Venue: 25-30% (room rental, setup, insurance)
│   ├── F&B: 25-30% (meals, breaks, reception — $75-150/person/day)
│   ├── AV/Production: 12-18% (sound, lighting, video, staging, livestream)
│   ├── Speaker/Talent: 10-20% (fees, travel, accommodation, gifts)
│   ├── Marketing: 5-8% (website, email, social ads, registration platform)
│   ├── Decor/Signage: 5-8% (branding, wayfinding, stage design)
│   ├── Staff/Contractors: 5-8% (event coordinator, photographer, videographer, temp staff)
│   ├── Contingency: 15% (things WILL go over somewhere)
│   └── Per-attendee all-in: $300-800 for corporate conference
├── Wedding (50-200 guests)
│   ├── Venue: 30-40% (often includes basic tables/chairs/linens)
│   ├── Catering: 25-35% ($75-200/person including bar)
│   ├── Photography/Videography: 8-12%
│   ├── Attire/Beauty: 5-10%
│   ├── Music/Entertainment: 5-10% (DJ or band)
│   ├── Florals/Decor: 8-12%
│   ├── Planner/Coordinator: 5-10%
│   ├── Contingency: 15%
│   └── The wedding markup is real — "wedding" catering costs 30-50% more than "event" catering for the same food
├── Team offsite (20-100 people, 1-2 days)
│   ├── Venue: 15-20% (meeting space + breakout rooms)
│   ├── F&B: 25-30% (breakfast, lunch, snacks — dinner may be separate)
│   ├── Facilitation/Activities: 15-25% (external facilitator, team activity)
│   ├── Travel/Accommodation: 20-30% (if people are flying in)
│   ├── Materials/SWAG: 5-10%
│   ├── Contingency: 10%
│   └── Per-person all-in: $300-800 (local) to $1,500-3,000 (with travel)
├── Virtual event
│   ├── Platform: 10-15% (Zoom Events, Hopin, Cvent — $5K-30K depending on scale)
│   ├── Production: 25-35% (streaming tech, producer, moderator training)
│   ├── Speaker/Talent: 15-25%
│   ├── Marketing: 15-20% (higher % because no venue/F&B to compete)
│   ├── Engagement: 10-15% (SWAG mailers, networking tools, gamification)
│   ├── Contingency: 10%
│   └── Virtual events cost 30-50% less than in-person but have 40-60% lower attendance rates for free events
├── Trade show / Expo (exhibitor perspective)
│   ├── Booth space: 25-35% (10x10 to 20x20 — $2K-50K depending on show)
│   ├── Booth design/build: 20-30% (custom booth, graphics, furniture, shipping)
│   ├── Staff travel/accommodation: 15-25%
│   ├── SWAG/Giveaways: 5-10%
│   ├── Lead capture/tech: 5-8%
│   ├── Sponsorship (optional): variable
│   └── Cost per lead: $150-500 for B2B trade show — track this metric
└── Budget tracking rules
    ├── Track actuals vs budget weekly in final month, daily in final week
    ├── Contingency is NOT "extra budget" — it's for actual unexpected costs only
    ├── Get 3 quotes for any line item over $2,000
    └── Never reveal your full budget to a vendor — they'll price to it. Ask for their best price first.
```

### 2. Venue Selection

```
How to choose and negotiate a venue:
├── Requirements gathering
│   ├── Capacity: comfortable max (not fire code max — that's sardine-level)
│   ├── Location: proximity to airport, hotels, attractions for out-of-town attendees
│   ├── Dates: have 2-3 date options — you have zero leverage with one date
│   ├── Layout: plenary room + breakout rooms? exhibition space? green room?
│   └── Technical: AV built-in or bring-your-own? WiFi capacity? load-in access? power?
├── RFP (Request for Proposal) — send to 3-5 venues
│   ├── Dates, expected attendance, room block needs, F&B requirements
│   ├── AV requirements, special setup needs
│   ├── Ask: rental fee, F&B minimums, attrition clause, cancellation terms, included services
│   └── Don't reveal your budget — let them price first
├── Site visit checklist
│   ├── Load-in: is there a loading dock? freight elevator? door dimensions for large items?
│   ├── Flow: attendee journey from arrival → registration → sessions → breaks → meals
│   ├── Acoustics: clap test — is the room live/dead? Can you hear from the back?
│   ├── Lighting: natural light? blackout capability for projections?
│   ├── Power: outlets locations, amperage, backup generator?
│   ├── WiFi: dedicated network for event? bandwidth? test with speedtest
│   ├── Back-of-house: green room for speakers, storage for materials, vendor staging area
│   └── Accessibility: ramps, elevators, accessible restrooms, hearing loop, service animal relief area
├── Negotiation points (EVERYTHING is negotiable)
│   ├── Rental fee: ask for 20-30% off — most venues have discount authority
│   ├── F&B minimum: negotiate down by 10-20% or ask for value-adds (upgraded menu at same minimum)
│   ├── Attrition: reduce sliding scale (e.g., from 80% to 70% of room block before penalty)
│   ├── WiFi: often $500-5,000 — ask for it to be included
│   ├── AV: venue AV is typically 2-3x external. Negotiate the right to bring external AV.
│   ├── Complimentary: 1 comp room per 50 room nights, VIP suite upgrade, parking for speakers
│   └── The best negotiation leverage: willingness to walk away + having another venue option
└── Contract red flags
    ├── Force majeure that doesn't cover pandemic/epidemic (post-2020)
    ├── Cancellation that makes you liable for 100% of revenue regardless of when you cancel
    ├── No right to bring external AV — you're captive to whatever they charge
    └── Renovation clause: venue can move your event to "comparable space" at their discretion
```

### 3. Run-of-Show Design

```
How to create a minute-by-minute event timeline:
├── Pre-event (day before or early morning)
│   ├── Load-in: vendors arrive, AV setup, decor installation
│   ├── AV rehearsal: test every mic, every slide deck, every video, every transition
│   ├── Speaker walkthrough: show speakers the stage, clicker, confidence monitor, green room
│   ├── Registration setup: test check-in flow, badge printers, WiFi for check-in
│   └── Staff briefing: roles, schedule, emergency procedures, who decides what
├── Event flow design principles
│   ├── Morning: highest-energy content — keynotes, big announcements
│   ├── Late morning: breakout sessions (attendees are awake and engaged)
│   ├── Lunch: 60-75 minutes (not 45 — people need bio breaks and networking)
│   ├── Post-lunch: interactive, high-energy sessions (combat the food coma)
│   ├── Afternoon: panel discussions (lower cognitive load, variety of voices)
│   ├── Late afternoon: networking, receptions, optional deep-dives
│   └── Content density: max 6 hours of content/day. After that, retention approaches zero.
├── Transitions (where events lose time)
│   ├── Session-to-session: 15 minutes (room flip, bio break, travel time between rooms)
│   ├── Break-to-session: 5 minutes (hard start times with countdown timer visible)
│   ├── Room flip (setup change): 30 minutes for simple, 60+ for major changes
│   └── Never schedule back-to-back without transition time — you WILL run late
├── Buffer strategy
│   ├── Add 10-15% buffer to every block: 60 min session = 50 min content + 10 min Q&A/buffer
│   ├── Morning sessions run on time. Afternoon sessions drift — more buffer later in day
│   ├── Have 2-3 "accordion" segments: can expand or contract 5-10 minutes as needed
│   └── Back-pocket content: 5-minute filler for when speaker finishes early (video, interactive poll, Q&A)
├── Run-of-show document format
│   ├── Time (actual clock time), Duration, What's happening, Who's responsible, Notes/backup plan
│   ├── Separate tracks: main stage, breakout A, breakout B, back-of-house
│   ├── Color code: green = on track, yellow = watch (behind by 5+ min), red = intervention needed
│   └── Print 5 copies + upload to shared drive. The WiFi will fail when you need it most.
└── Speaker management
    ├── Send speaker brief 2 weeks before: timeline, AV setup, audience profile, content guidelines
    ├── Collect slides 1 week before — test them on venue equipment. No "I'll bring them on a USB."
    ├── Green room: water, snacks, mirror, quiet space, printed schedule, WiFi password
    ├── Speaker ready room: 15 minutes before their slot, speakers are in green room confirmed and miked
    └── Backup plan: if keynote speaker doesn't show — panel with available speakers, extended Q&A, networking
```

### 4. Day-Of Execution

```
How to run event day without losing your mind:
├── Command center (event HQ)
│   ├── One person is the "event commander" — all decisions flow through them, all problems report to them
│   ├── Communication: radios/headsets for all staff (not phones — can't hear in loud rooms, battery dies)
│   ├── Master run-of-show on the wall with color-code status
│   ├── Vendor contact sheet posted — name, company, phone, what they're responsible for
│   └── Emergency contacts: venue security, nearest hospital, police non-emergency, poison control
├── Morning checklist (3 hours before doors)
│   ├── Walk every space: registration, sessions, break areas, restrooms, back-of-house
│   ├── Test AV in every room: sound, projection, confidence monitor, clicker, countdown timer
│   ├── Test WiFi: speed test from attendee areas. Can 200 people connect?
│   ├── Check signage: can a stranger navigate from entrance to session rooms? Signage should be at every decision point.
│   ├── Temperature check: rooms get 5-10°F warmer when full — pre-cool
│   └── Confirm with every vendor: they're on site, set up, and ready
├── Real-time management
│   ├── 15-minute huddle with key staff before each major block
│   ├── Track room counts: are sessions over/under capacity? Room too hot/cold? AV issue?
│   ├── Timekeeper: one person dedicated to timing every session, giving 5-min and 2-min warnings to speakers
│   ├── Social media: designated person posting live updates, photos, quotes
│   └── Problem log: document every issue and resolution for post-event debrief
├── Common day-of problems and fixes
│   ├── Speaker no-show → Backup panel or extended Q&A with available speakers
│   ├── AV failure → Switch to backup system. If slides dead, speaker goes "unplugged" — have printed notes.
│   ├── Room too cold/hot → Contact venue engineering immediately. Portable fans/heaters as backup.
│   ├── Food running out → Venue contact extends portions. Backup: order pizza — it's better than hungry attendees.
│   ├── WiFi down → Switch to cellular hotspots. Have offline backup of all digital materials.
│   ├── Medical emergency → Designated first-aid trained staff. Know where AED is. Call 911 — don't hesitate.
│   └── Disruptive attendee → Quietly approach, ask to step outside, have security as backup. Don't make a scene.
└── Closing sequence
    ├── Thank attendees for coming, share how to access post-event materials, ask for survey
    ├── Thank vendors in person — this matters for future relationships
    ├── Secure valuables: AV equipment, leftover SWAG, speaker gifts, lost & found
    ├── Load-out plan: who's taking what, when, through which door
    └── Staff debrief (can be next day): what went well? what didn't? what would we do differently?
```

### 5. Post-Event Analysis

```
How to measure event success and capture learnings:
├── Quantitative metrics (collect within 48 hours)
│   ├── Attendance: registered vs actual, no-show rate, session attendance distribution
│   ├── Budget: actual vs budget by category, cost per attendee, revenue (tickets/sponsorship)
│   ├── Engagement: session ratings, app usage, networking connections made, social media mentions
│   ├── NPS/eNPS: "How likely are you to recommend this event?" (0-10) → Promoters (9-10) - Detractors (0-6)
│   └── ROI: (Value generated — sponsorship, pipeline, deals closed) / Total event cost
├── Qualitative feedback (survey)
│   ├── "What was the most valuable part of the event for you?"
│   ├── "What would you change for next time?"
│   ├── "What topics/speakers would you like to see next year?"
│   ├── "How does this compare to other events you attend?"
│   └── Keep survey SHORT — 5 questions max. Completion rate drops 50% after question 7.
├── Stakeholder debrief (1 week after)
│   ├── Budget reconciliation: where did we over/under spend?
│   ├── What worked: keep doing
│   ├── What didn't: stop doing or change
│   ├── Attendance trends: growing or declining?
│   └── Recommendations for next event: date, venue, format changes
├── Vendor evaluation
│   ├── Rate each vendor: would hire again? (yes/maybe/no)
│   ├── Document issues: late delivery, quality problems, communication failures
│   ├── Update your vendor database for future events
│   └── Send thank-you notes to top performers — they'll prioritize you next time
└── Knowledge capture for next time
    ├── Update event planning template with actual timelines (they were optimistic)
    ├── Update budget template with actual costs (they were optimistic)
    ├── Save run-of-show, floor plans, signage files, speaker briefs in organized archive
    └── Write "Event Close Report": 2-page summary for stakeholders who won't read the full debrief
```

## Cross-Skill Coordination

| Skill | Relationship | When to Route |
|-------|-------------|---------------|
| `project-manager` | Consumes project management methods | Complex timeline management, multi-workstream coordination |
| `marketing-manager` | Coordinates on promotion | Event marketing strategy, attendee acquisition |
| `content-strategist` | Coordinates on content | Session content strategy, speaker content guidance |
| `sales-engineer` | Coordinates on sponsorship | Exhibitor and sponsor sales |
| `demand-generation` | Coordinates on attendee pipeline | Attendee registration campaigns |

## Proactive Triggers

| # | Trigger | Action |
|---|---------|--------|
| T1 | "I'm planning an event" | Ask: goals, audience, budget ceiling, format, date(s), rough size. Build budget framework. |
| T2 | User shares venue contract | Contract review: cancellation, attrition, F&B minimum, force majeure, AV exclusivity, hidden fees |
| T3 | Event is in < 2 weeks, no run-of-show | Escalate: build minute-by-minute ROS immediately. This is the #1 predictor of event day chaos. |
| T4 | "We're over budget" | Triage: what can be cut? what's locked? Reallocate contingency. Negotiate with vendors. |
| T5 | "Something went wrong at our event" | Post-mortem: what happened, why, what's the fix for next time. No blame, just process improvement. |

## What Good Looks Like

| Anti-Pattern | Good | Great |
|-------------|------|-------|
| "We'll figure out the schedule on the day" | Run-of-show with times and owners, printed 5 copies | Run-of-show with times, owners, backup plans, accordion segments, color-coded status tracking, radio channels assigned |
| Budget = "around $50K" → actual = $78K | Budget with 15% contingency, tracked weekly, actual $53K | Budget with 15% contingency + 5% reserve, tracked weekly, actual within 5% of plan, $/attendee benchmarked against industry |
| Signed venue contract without reading attrition clause | Contract reviewed, attrition negotiated from 80% to 70% | Contract reviewed + attrition negotiated + force majeure updated + AV exclusivity waived + 1 comp per 40 room nights + cancellation terms softened |

## Gotchas

- **Attrition clauses are the #1 hidden cost in hotel venue contracts — they can cost more than the venue rental itself.** If you guarantee 200 room nights at $250/night ($50,000 commitment) with 80% attrition, and only 150 rooms book, you owe $10,000 for rooms no one used. **For a mid-size conference, attrition penalties average $8K-25K. This is pure waste — no value delivered, just contractual obligation.** Fix: negotiate attrition to 70% or lower. Track room bookings weekly in final 2 months. If undershooting, open room block to local attendees, offer upgraded rooms, or negotiate with venue to apply F&B spend against attrition shortfall.
- **Venue WiFi that "supports 500 devices" means 500 devices connected, not 500 devices streaming video, downloading presentations, and video-calling simultaneously.** The average event attendee has 2-3 devices. 300 attendees = 600-900 devices. **Venue WiFi that collapses during your event means: registration system goes offline, speakers can't demo live, virtual attendees lose stream, social media coverage dies. The reputational cost of "great event, terrible WiFi" is permanent — that's the review that sticks.** Fix: dedicated event network, hardwired connection for critical systems, cellular backup hotspots, test with simulated load before event day.
- **The "family-style" F&B trap: venues push family-style service because it's easier for them, but it creates: (1) 30% more food waste, (2) 15-20 minute longer meal times, (3) dietary restriction nightmare (cross-contamination).** For a 300-person lunch, family-style adds 15 minutes to service, delaying afternoon sessions by 15 minutes across the entire event. **Plated or buffet with staffed stations is more predictable, faster, and wastes less food.**
- **AV is where venues make their margin — in-house AV is typically 200-300% of external AV pricing.** A $5,000 external AV quote becomes $12,000-15,000 with in-house. **For a 3-day conference, the AV markup alone can be $20K-40K — enough to pay for another keynote speaker or subsidize 50 attendee tickets.** Fix: negotiate right to use external AV before signing the venue contract.
- **The post-event survey that asks 30 questions gets a 3% response rate. The post-event survey that asks 3 questions gets a 60% response rate.** **A 200-person event with a 3% response rate = 6 responses. You cannot make data-driven decisions from 6 responses.** Fix: 5 questions max. Send within 24 hours. Include "this takes 2 minutes." One open-ended question: "What's the one thing you'd change?"
- **Booking speaker travel inside 2 weeks of the event** — a 30-speaker conference booking flights 10 days out pays 40-60% more than booking at 8-12 weeks. International speakers' flights jump from $800 to $1,800, domestic from $300 to $550. Multiply by 30 speakers and you've added $15K-$25K to the travel budget with zero improvement in attendee experience. **Total cost: $15K-$25K in avoidable travel premiums for a single mid-size conference — money that could have funded a keynote speaker or 100 discounted tickets.** Fix: speaker confirmation emails include a "book within 7 days" travel policy. Pre-negotiate corporate rates with 2 airlines for your event dates. Track travel booking dates in your speaker management sheet and send automated reminders at 12 weeks, 8 weeks, and 4 weeks out.
- **Not enforcing the "slides due 1 week before" policy** — a speaker arrives with slides on a personal laptop using a discontinued presentation tool. AV team spends 15 minutes troubleshooting while 400 attendees wait. Cascading delays: 12 sessions start 5 minutes late each = 60 minutes of lost content across the event. Attendees tweet "great content, terrible organization" — a review that outlasts the event by years. **Total cost: $5K-$10K in attendee dissatisfaction (refund requests, no-shows next year) plus permanent reputational damage that depresses future ticket sales by 10-15%.** Fix: make slide submission a contractual obligation with a hard deadline. Provide a slide template and technical requirements document. Assign each speaker a "slide buddy" from your team who verifies format, aspect ratio, and embedded media 1 week before the event. Have backup laptops preloaded with all presentations.
- **F&B minimum guarantee tracked only at event close-out, not mid-event** — venue contract requires $40K minimum F&B spend. Day 2 of your 3-day conference, you're at $26K actual. You either owe $14K for unconsumed food at $0 value, or you panic-order premium wine and hors d'oeuvres at full retail markup to close the gap. Either way, it's unbudgeted spend. **Total cost: $8K-$15K in unplanned F&B spend at a single event from not tracking against guarantee in real time.** Fix: request daily running F&B totals from venue catering manager. Set a mid-event checkpoint (lunch on day 2) where you review actuals vs guarantee. If undershooting, add value — upgrade the closing reception, add a coffee cart, extend bar hours — rather than scrambling at final invoice.

## Deliberate Practice

*   **Beginner — Budget Build:** Build a complete event budget for a 200-person, 2-day corporate conference in your city. Get real venue and vendor quotes (or realistic estimates). Track every category. Compare with industry benchmarks.
*   **Intermediate — Run-of-Show Challenge:** Take a real event agenda and build a minute-by-minute run-of-show. Include transitions, buffers, backup plans, and ownership for every line. Have an experienced event planner review and critique it.
*   **Advanced — Venue Negotiation Simulation:** Role-play a venue contract negotiation. Research real venue pricing in your area. Practice: initial pricing, negotiation points, contract redlines. Learn where venues have flexibility and where they don't.
*   **Expert — Crisis Planning:** Design a complete crisis response plan for a 1,000-person event. Identify top 10 failure scenarios by likelihood × impact. For each: prevention, detection, response protocol, communication plan, and recovery plan.

## Verification

- [ ] Budget established with 15% contingency and per-category allocations
- [ ] Venue contract reviewed: cancellation, attrition, F&B minimums, force majeure, AV, insurance
- [ ] Run-of-show created: minute-by-minute, every line has owner, transitions and buffers included
- [ ] Single points of failure identified and backup plans in place (people, tech, vendors)
- [ ] AV tested on-site before event day with actual equipment
- [ ] WiFi tested under load (simulated if possible)
- [ ] Speaker slides collected and tested 1 week before
- [ ] Emergency contacts sheet printed: venue, medical, security, key vendors
- [ ] Post-event survey prepared: 5 questions max, to be sent within 24 hours
- [ ] Staff briefing scheduled before event day

## References

- **Budget Templates**: See [references/budget-templates.md](references/budget-templates.md)
- **Venue RFP Template**: See [references/venue-rfp.md](references/venue-rfp.md)
- **Run-of-Show Template**: See [references/run-of-show.md](references/run-of-show.md)
- **Vendor Management**: See [references/vendor-management.md](references/vendor-management.md)
- **Risk Register Template**: See [references/risk-register.md](references/risk-register.md)
- **Anti-Patterns**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Calibration**: See [references/calibration.md](references/calibration.md)
- **Production Checklist**: See [references/checklist.md](references/checklist.md)
- **Error Decoder**: See [references/error-decoder.md](references/error-decoder.md)
- **Footguns**: See [references/footguns.md](references/footguns.md)
- **Scale Depth**: See [references/scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [references/sub-skills.md](references/sub-skills.md)
