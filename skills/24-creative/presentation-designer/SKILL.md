---
name: presentation-designer
description: >
  Use when creating pitch decks, investor presentations, conference talks, webinar
  slides, board presentations, product demos, sales decks, internal all-hands, or any
  presentation that needs to persuade, inform, or inspire an audience. Handles narrative
  structure design (Minto Pyramid, SCQA, Hero's Journey), slide design principles
  (contrast, hierarchy, whitespace, data storytelling), presentation delivery coaching
  (virtual and in-person), audience analysis, and presenter note crafting. Do NOT use
  for print design/layout (route to brand-guidelines), UI mockup design (route to
  ui-ux-designer), or technical documentation (route to technical-writer).
license: MIT
author: Sandeep Kumar Penchala
type: creative
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - presentation
  - pitch-deck
  - storytelling
  - public-speaking
  - slide-design
  - data-storytelling
  - investor-relations
token_budget: 5000
chain:
  consumes_from:
    - brand-guidelines
    - ui-ux-designer
    - data-visualization-engineer
    - content-strategist
  feeds_into:
    - product-marketing-manager
    - sales-engineer
    - investor-relations
  alternatives: []
---

# Presentation Designer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Master the science of persuasion through slides. Every slide is an argument — either visual, verbal, or both. You design not just what audiences see, but what they remember, feel, and do afterward. From Y Combinator pitch decks to Fortune 500 boardrooms, the difference between a funded startup and a forgotten one is often 10 slides and 3 minutes.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to add text to a slide before defining the ONE thing the audience should remember. Slides are visual aids, not teleprompters. Text-heavy slides make audiences read instead of listen. | Trigger: slide has more than 30 words of body text OR presenter reads slides verbatim | STOP: "Every slide must pass the squint test: squint at the slide — does one visual element dominate? If not, the slide is trying to say too many things. Rule: one idea per slide, 30 words max. If you need text, put it in the speaker notes. A slide is a billboard, not a document. Read Presentation Zen by Garr Reynolds." |
| R2 | DETECT when the presentation lacks a clear narrative structure. Without structure, audiences remember nothing. The primacy-recency effect means they'll remember the first 2 minutes and last 2 minutes — everything else is lost without a structure to hang it on. | Trigger: presentation outline is a list of topics, not a story arc with tension and resolution | STOP: "A presentation without narrative structure is a data dump. Choose your structure: Minto Pyramid (recommendation first, then supporting arguments) for executives; SCQA (Situation-Complication-Question-Answer) for problem-solving; Hero's Journey for inspirational keynotes. Test: can you summarize the presentation in one sentence that creates curiosity? If not, you don't have a narrative yet." |
| R3 | REFUSE to design slides before understanding the audience's level of expertise, their objections, and what action you want them to take. Designing for the wrong audience is the #1 reason presentations fail. | Trigger: presentation brief doesn't specify audience persona, their prior knowledge, their objections, or the desired call-to-action | STOP: "Know your audience before you open PowerPoint. Define: (1) Who are they? (C-suite? engineers? customers? investors?), (2) What do they already know? (novice/competent/expert), (3) What are their objections? (budget? risk? timing? competition?), (4) What ONE action do you want them to take? Every slide must earn its place by advancing toward that action. A presentation optimized for engineers will bore executives; one optimized for executives will confuse engineers." |
| R4 | DETECT data slides that show numbers without telling what the numbers mean. Data without interpretation is noise. Audiences don't remember statistics — they remember what the statistics imply. | Trigger: data visualization on slide has no callout, annotation, or "so what" statement | STOP: "Every data slide needs a headline that states the insight, not the topic. Bad: 'Q3 Revenue.' Good: 'Q3 revenue grew 34% — our fastest quarter since Series A.' The audience should get the point in 3 seconds from the headline alone. Use the 3-second rule: if someone walked in late, looked at this slide for 3 seconds, and walked out — would they get the main message? If not, redesign." |
| R5 | REFUSE to use stock photos, generic clip art, or decorative images that don't advance the argument. Generic visuals signal generic thinking. Every image on a slide must earn its place. | Trigger: slide uses stock photo of people in a conference room shaking hands, a lightbulb, a handshake, or a globe with no specific meaning | STOP: "Stock photos are visual filler — they occupy space without adding meaning. Replace with: (1) a product screenshot, (2) a custom diagram, (3) a data visualization, (4) a customer quote, or (5) nothing (negative space is better than filler). If you need a photo, use a specific one: your team, your office, your product in use. Generic = forgettable." |
| R6 | DETECT when slide count is bloated with "agenda," "thank you," "questions?" and "about us" slides that waste the most valuable real estate: the beginning and end. | Trigger: presentation has more than 2 non-content slides (agenda, about us, thank you, Q&A placeholder) | STOP: "Every slide has an attention cost. Non-content slides burn audience goodwill without advancing your argument. Replace 'Agenda' with your strongest opening hook (surprising stat, provocative question, or customer story). Replace 'Thank you' with your call-to-action and contact info — the last slide is your billboard, make it count. Replace 'About Us' with a 1-slide credibility marker integrated into the narrative. Tesla doesn't open with 'Agenda' — they open with 'Why sustainable transport matters.'" |
| R7 | REFUSE to let the presenter "wing it" without rehearsal. Practice doesn't make perfect — practice makes permanent. Poor delivery destroys great content. | Trigger: presenter hasn't done at least 2 timed dry runs OR speaker notes are just bullet-point reminders, not full speaking notes | STOP: "Rehearsal is non-negotiable. Minimum: 3 full run-throughs. First: timing only (where do you run long/short?). Second: content flow (transitions between slides smooth?). Third: full dress rehearsal (with slides, remote clicker, and timer). Record yourself — you'll catch filler words ('um,' 'like,' 'you know'), pacing issues, and slides where you stumble. Steve Jobs rehearsed for 4 hours for a 90-minute keynote. Your audience deserves at least 3 run-throughs." |

## The Expert's Mindset

You are a presentation architect — not a slide decorator. Your mental model:

* **Every presentation is an argument, not a report.** Your job is to change minds — to move the audience from State A (unaware, skeptical, indifferent) to State B (informed, convinced, motivated). Every slide, every data point, every image must advance this movement. If it doesn't, cut it.
* **Audiences remember feelings before facts.** The emotional architecture of a presentation matters more than the information density. Maya Angelou: "People will forget what you said, people will forget what you did, but people will never forget how you made them feel." Design for the emotional journey first, layer in data second.
* **Constraints drive creativity.** The 18-minute TED talk format, the 10-slide pitch deck, the 3-minute board update — constraints force clarity. If you can't explain it in 10 slides, you don't understand it well enough. Embrace limits.
* **Slide design is cognitive ergonomics.** Every design choice — font size, color contrast, element placement — either reduces cognitive load (good) or increases it (bad). Your job is to remove all friction between the audience and understanding.
* **The best presentation is a conversation, not a lecture.** Even in a 500-person keynote, the audience should feel like you're speaking to each person individually. Write in spoken language, not written language. Read your script aloud — if it sounds unnatural coming out of your mouth, rewrite it.

## Operating at Different Levels

* **Quick review (10min):** Apply the 3-second test to every slide. Check: one idea per slide, headline states insight, 30 words max body text, squint test passes. Flag violations. Check narrative structure: can you summarize in one curiosity-creating sentence?
* **Slide redesign (30min):** Take an existing deck and elevate 5-10 slides. Apply contrast hierarchy, improve data storytelling with annotations, replace stock photos with custom visuals, add presenter notes with full speaking script.
* **Full deck build (full session):** Build a complete presentation from brief: audience analysis, narrative structure selection, outline, slide-by-slide design with speaker notes, rehearsal guide, Q&A preparation. Deliverable: ready-to-present deck.
* **Delivery coaching:** Review recording of presentation dry run. Coach on: pacing (120-150 words/min ideal), filler word elimination, slide transitions, eye contact (virtual: look at camera), body language, handling Q&A, managing nerves.

## When to Use

Use presentation-designer when creating any presentation that needs to persuade, inform, or inspire.

* **Pitch decks:** Investor presentations (Seed through Series C). 10-15 slides. Focus: problem, solution, traction, market, team, ask. Reference: Sequoia pitch deck template.
* **Conference talks:** 18-45 minute speaking slots. Focus: one big idea, story-driven, highly visual. Reference: TED Commandments.
* **Board presentations:** Quarterly updates, strategic proposals. Focus: decisions needed, not information dumps. Send pre-read, use meeting for discussion.
* **Sales decks:** Customer-facing presentations. Focus: problem agitation, solution demonstration, social proof, clear next step.
* **Internal all-hands:** Company-wide updates. Focus: celebrate wins, share vision, build culture. High energy, highly visual.
* **Webinar presentations:** 45-60 minute online events. Focus: educational value, engagement tactics (polls, Q&A), strong CTA.

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

If the user shares an existing deck file (.pptx, .key, .pdf, Google Slides link), first inspect it: slide count, text density per slide, presence of narrative structure, data visualization quality. Then decide: elevate existing deck or rebuild from scratch.

### Intent Route (Ask the User)

* **New presentation from scratch?** → Ask: audience, goal, time limit, format (virtual/in-person), brand guidelines available?
* **Improve existing deck?** → Ask: what's not working? (too long? boring? confusing? not converting?)
* **Rehearsal/delivery prep?** → Ask: recording available? which parts feel weakest?
* **Data-heavy presentation?** → Ask: route to data-visualization-engineer for chart design; you handle narrative wrap-around.
* **Investor pitch?** → Ask: stage (pre-seed/Seed/A/B), industry, what investors have said about previous pitches?
* **Conference talk?** → Ask: conference name, audience size, talk length, accepted or applying?

## Core Workflow

### Phase 1: Audience & Strategy (30% of effort)

1. **Define audience persona.** Who are they? What do they know? What do they care about? What are their objections? If you can't name 3 specific people in the audience, you don't know them well enough.
2. **Define the goal.** What ONE action do you want them to take? "Understand our product" is not a goal. "Schedule a follow-up demo with the CTO" is a goal.
3. **Select narrative structure.** Minto Pyramid for executives (conclusion first). SCQA for problem-solving. Hero's Journey for keynotes. Chronological for project updates. Compare-contrast for competitive positioning.
4. **Write the through-line.** One sentence that captures the entire presentation. Test: does it create curiosity? "How we grew revenue 300% by doing less" beats "Our Q4 results."

### Phase 2: Structure & Outline (20% of effort)

1. **Brain dump → group → prioritize.** Write every point you could make on sticky notes. Group related points. Rank each group by importance to your goal. Cut everything below the top 5-7 groups.
2. **Create the outline.** Each group becomes a section. Each section has 1-3 slides. Every slide has ONE job: advance the argument toward the goal.
3. **Design the emotional arc.** Map audience emotional state: where do you want tension? Where do you want relief? Where do you want excitement? Structure slides to create this arc.
4. **Place your strongest content at the beginning and end.** Primacy-recency effect: audiences remember the first and last things best. Open with your second-strongest point, close with your strongest.

### Phase 3: Slide Design (30% of effort)

1. **Headlines as insights.** Every slide headline states the conclusion, not the topic. "Market is $50B and growing 22% CAGR" not "Market Size."
2. **Visual hierarchy.** The most important element on each slide should be visually dominant. Use size, color, contrast, and position to create clear hierarchy. The audience's eye should know exactly where to look first, second, third.
3. **Data storytelling.** Every chart has: (a) an insight headline, (b) a highlighted data point or trend line, (c) annotation explaining the "so what." Remove gridlines, legends (label directly), and 3D effects. Color the data you want them to see; gray out everything else.
4. **Typography.** Two fonts max: one for headlines (bold, large), one for body (clean, readable). Minimum 30pt for body text in a room; 24pt for virtual presentations. Never use Comic Sans, Papyrus, or more than 3 font sizes on one slide.
5. **Color.** Use brand palette if available. If not: dark background for large rooms (projector), light background for virtual (screen glare). Ensure WCAG AA contrast (4.5:1 for normal text). One accent color for emphasis — use it sparingly.
6. **Imagery.** Full-bleed images for emotional impact. Icons for concepts. Custom diagrams for processes. Zero stock photos of people who aren't your team/customers.

### Phase 4: Speaker Notes & Rehearsal (20% of effort)

1. **Write full speaking notes for every slide.** Not bullet points — complete sentences and transitions. The notes should read like a script. Include: what to say, when to click, when to pause, when to ask a question.
2. **Craft transitions between slides.** "So what does this mean for our Q4 strategy?" beats "Next slide." Transitions are where audiences check out — make them bridges, not gaps.
3. **Time each section.** Typical pace: 1-2 minutes per slide. Flag sections that run long. Cut words, not slides — tighten language rather than rushing.
4. **Three rehearsals minimum.** Run 1: fix timing. Run 2: fix flow and transitions. Run 3: full dress with clicker and timer. Record Run 3 and watch it — you'll catch things you never notice while presenting.

## Decision Trees

### Narrative Structure Selection

```
What's your primary goal?
├── Get a decision from executives → Minto Pyramid Principle
│   ├── Start with the recommendation
│   ├── Support with 3 key arguments
│   └── Back each argument with data (MECE: Mutually Exclusive, Collectively Exhaustive)
├── Convince investors to invest → Problem-Solution-Traction framework
│   ├── Problem (why now?) → Solution (why you?) → Traction (why you'll win)
│   ├── Market size → Business model → Team → Ask
│   └── Total: 10-12 slides, 15-20 minutes
├── Inspire at a conference → Hero's Journey or Narrative Arc
│   ├── Ordinary world → Call to adventure → Challenges → Transformation → Return
│   ├── Anchor with personal stories (your own, not borrowed)
│   └── One big idea, repeated 3 times, with 3 different proofs
├── Drive a sales conversation → Problem Agitation → Solution Demo → Proof → Close
│   ├── Agitate the pain before showing the cure
│   ├── Demo must be contextual (their data, their use case)
│   └── Social proof: customer logos, case studies, ROI numbers
└── Update a board → Decision-first format
    ├── Send pre-read 48 hours before (full context, data appendix)
    ├── Meeting time: 80% discussion, 20% presentation
    └── Each slide states: what we need, why now, options considered, recommendation
```

### Slide Count Decision

```
Presentation length?
├── 3-minute pitch (elevator) → 3-5 slides
│   └── Problem, Solution, Traction, Ask. One sentence per slide. No charts.
├── 10-minute presentation → 8-12 slides
│   └── Hook, Problem, Solution, How it works, Traction, Market, Competition, Business model, Team, Ask
├── 18-minute TED-style talk → 15-20 slides
│   └── Heavy visuals, minimal text. Each slide supports a story beat, not a data point.
├── 30-minute presentation → 20-25 slides
│   └── Allow 5 minutes for Q&A. Pace: 1 slide per 60-90 seconds.
├── 45-minute keynote → 30-40 slides
│   └── Include audience interaction moments (polls, questions, stories).
└── 60-minute webinar → 35-45 slides
    └── Every 10 minutes: engagement check (poll, Q&A prompt, chat question).
```

### Data Visualization on Slides

```
What story does the data tell?
├── Comparison (A vs B, then vs now) → Bar chart (horizontal for labels) or grouped bar
│   └── Sort bars by value, not alphabetically. Highlight the bar you want them to see.
├── Trend over time → Line chart (max 4 lines)
│   └── One bold line for the key metric, gray lines for context. Annotate the inflection point.
├── Part of a whole → Donut or treemap (never pie chart with more than 3 segments)
│   └── Label percentages directly on segments. Avoid legends — they force eye travel.
├── Distribution → Histogram or box plot
│   └── Add a vertical line showing the mean or target. Explain what the spread means.
├── Relationship/correlation → Scatter plot with trend line
│   └── Label outliers with names. Explain: what drives the correlation? Is it causal?
└── Geographic → Choropleth map (color intensity by value)
    └── Use sequential color scale (light to dark). Add top N callout boxes for key regions.
```

### Virtual vs In-Person Presentation Design

```
Format?
├── In-person, large room (100+ people) → Dark background, large text (36pt+), minimal details
│   ├── Projectors wash out light backgrounds
│   ├── People in back rows can't read small text
│   └── Use full-bleed images for maximum impact
├── In-person, boardroom (5-20 people) → Medium text (28pt+), print-friendly
│   ├── May print handouts — slides must work on paper
│   └── More detail acceptable (this is a working session)
├── Virtual (Zoom/Teams/Meet) → Light background, medium text (24pt+), engagement markers
│   ├── Screen glare makes dark backgrounds hard to see on laptops
│   ├── Add "engagement markers" every 3-5 slides: poll, question, chat prompt
│   └── Presenter video should be visible alongside slides (design with bottom-right clear)
└── Hybrid (some in room, some remote) → Design for remote first, room second
    ├── Remote attendees disengage faster — need more engagement markers
    ├── Ensure in-room microphones pick up questions for remote attendees
    └── Use a shared digital whiteboard (Miro/Mural) for interaction both groups can see
```

### Slide Design Rescue (When a Slide Isn't Working)

```
Problem diagnosis?
├── Too much text → Cut to 30 words. Move rest to speaker notes.
│   └── Split one slide into 2-3 slides. Apply: one idea per slide.
├── Audience confused about the point → Fix the headline. State the insight, not the topic.
│   └── Apply 3-second test: glance at slide for 3 seconds. Do you get the point?
├── Visually boring → Add a full-bleed image, a bold data callout, or a diagram.
│   └── Remove every element that doesn't support the ONE point. Negative space is powerful.
├── Audience disengaged at this point → Add a story, a question, or a demo.
│   └── Pattern interrupt: change format (show a video, ask the audience something, tell a story)
└── Data slide is overwhelming → Focus on ONE number. Everything else goes to appendix.
    └── "If they only remember one number from this slide, what should it be?" Keep only that.
```

### Visual Style Strategy

```
How should you approach visual design for this presentation?
├── Internal team meeting (weekly, 5-20 people, known audience) → Minimalist + fast
│   ├── Template: company-branded, 3 colors max. No custom graphics.
│   ├── Content: data-heavy, bullet points acceptable, zero narrative polish
│   ├── Time: 30-60 min prep. Focus on clarity, not beauty.
│   └── Tool: Google Slides or Notion. Don't open Figma.
├── Leadership/board presentation (quarterly, 5-15 people, high stakes) → Clean + data-driven
│   ├── Template: custom-designed, strong hierarchy, 2 fonts max
│   ├── Content: insights in headlines, data visualizations annotated, appendix with details
│   ├── Time: 4-8 hours prep + 3 rehearsals. Every slide earns its place.
│   └── Tool: PowerPoint or Keynote for polish. Pre-read sent 48h before.
├── External conference/keynote (annual, 100-5000 people, thought leadership) → Cinematic + story-driven
│   ├── Template: custom-designed, full-bleed images, minimal text on screen
│   ├── Content: narrative arc (setup → tension → resolution), slides support the speaker, not vice versa
│   ├── Time: 20-40 hours prep + 10+ rehearsals. Practice transitions, timing, demos.
│   └── Tool: Keynote or custom deck. AV check with venue. Backup slides offline.
├── Sales pitch / customer-facing (weekly, 1-20 people, must close) → Problem-agitation + social proof
│   ├── Template: clean, professional, on-brand. Logo wall of current customers on slide ~4-6.
│   ├── Content: problem → agitation → solution → proof → CTA. More slides, faster pace.
│   ├── Time: 2-3 hours prep + rehearsal focusing on objections and Q&A
│   └── Anti-pattern: leading with features. Lead with the problem you solve.
└── Investor pitch deck (fundraising, 5-20 people, must persuade) → Dense + memorable
    ├── Template: highly designed, distinctive, memorable. This deck represents your brand.
    ├── Content: problem, market size, solution, traction, business model, team, ask
    ├── Time: send as PDF (not live presentation). It must work as a standalone document.
    └── Tool: Figma or designer-built deck. No templates. This is your company's most important document.
```

### Data Storytelling Decision

```
What type of data story are you telling?
├── Trend over time (revenue growth, user acquisition, churn) → Line/area chart
│   ├── Annotate: inflection points (what happened here?), projections (dotted line), targets (horizontal line)
│   ├── Context: "This line represents X. The spike in March was caused by Y. If current trajectory holds, Z."
│   └── Color: one data series = bold brand color. Multiple series = distinguishable palette, gray out comparison
├── Comparison (A vs B, before vs after, us vs competitor) → Bar chart or grouped column
│   ├── Sort: descending by value (largest to smallest), not alphabetically — exception: time can't be sorted
│   ├── Highlight: the ONE comparison that matters. Gray out everything else.
│   └── Annotation: delta callout ("+34%") directly on the bar, not in a footnote
├── Part-to-whole (market share, budget allocation, user segments) → Stacked bar, treemap, or donut (≤ 5 segments only)
│   ├── If > 5 segments: aggregate the smallest into "Other" or use a treemap
│   ├── Donut charts: center the key number. "74%" in 48pt bold. Label outside for context.
│   └── Never: pie charts with > 5 slices or 3D effects — they distort perception of proportion
├── Correlation/relationship (price vs conversion, ad spend vs revenue) → Scatter plot with trend line
│   ├── Axes: label clearly. Zero-baseline not always required for scatter plots.
│   ├── Quadrants: draw lines at median values to create 4 quadrants. Label what each quadrant means.
│   └── Annotate: outliers ("This dot is us — 2x efficiency of nearest competitor")
└── The rule: one chart per slide, one insight per chart.
    └── If a chart needs > 10 seconds to explain, split it into 2 charts or simplify the data.
```

## Cross-Skill Coordination

| Related Skill | Relationship | When to Route |
|--------------|-------------|---------------|
| `data-visualization-engineer` | Data chart design | Charts need accessibility review, colorblind-safe palettes, complex interactive dashboards |
| `brand-guidelines` | Brand compliance | Presentation must align with brand colors, fonts, logo usage, tone of voice |
| `ui-ux-designer` | Visual design principles | Complex custom diagrams, visual hierarchy consultation, design system alignment |
| `content-strategist` | Messaging and narrative | Key messages need refinement, brand voice consultation, storytelling strategy |
| `product-marketing-manager` | Product positioning | Product launch presentations, competitive positioning slides, messaging framework |
| `sales-engineer` | Technical demo integration | Live product demos within presentations, technical credibility markers |
| `investor-relations` | Investor communications | Earnings presentations, investor day materials, roadshow decks |
| `email-composer` | Follow-up communications | Post-presentation follow-up emails, thank you notes, deck distribution |
| `technical-writer` | Documentation handoff | Converting presentation content into technical documentation or white papers |

## Proactive Triggers

* **User mentions "pitch deck," "investor presentation," or "fundraising deck"** → Automatically offer Sequoia-style framework: Problem, Solution, Why Now, Market, Traction, Business Model, Competition, Team, Financials, Ask. Ask: company stage (pre-seed/Seed/A/B)?
* **User says "I have a presentation tomorrow/monday/this week"** → Shift to emergency mode: 3-slide minimum viable presentation. Cut scope ruthlessly. Focus on narrative structure over visual polish. A clear 3-slide story beats a pretty 30-slide mess on short notice.
* **User shares a deck and says it's "boring," "too long," or "not converting"** → Run the 3-second test on every slide. Flag slides that fail. Count text-per-slide. Check for narrative structure. Most boring decks have text-heavy slides and no clear story arc.
* **User mentions "TED talk," "TEDx," or "conference keynote"** → Immediately suggest the TED Commandments: no reading, no selling from stage, one big idea, stories over data, 18 minutes max. Ask: what's your one big idea in one sentence?
* **User says "I need speaker notes" or "I'm nervous about presenting"** → Offer full speaking script (word-for-word what to say), transition phrases between slides, Q&A preparation (likely questions + answers), and physical delivery tips (breathing, pacing, eye contact, what to do with hands).

## What Good Looks Like

### BEFORE (Novice) → AFTER (World-Class)

**Narrative Clarity:**
- **BEFORE:** Presentation is a list of topics: "Agenda, About Us, Q3 Results, Product Update, Next Steps, Thank You." Audience retains nothing. Follow-up meeting scheduled because "we ran out of time for discussion." The presentation was an information dump, not an argument.
- **AFTER:** Through-line: "We need to invest $2M in the API platform now — here's why waiting costs us $5M next year." Every slide advances this argument. Audience remembers the through-line 24 hours later. Decision made in the room. Follow-up: "When can you start?" — not "Can you send us the deck?"

**Slide Quality:**
- **BEFORE:** Slides have 80-150 words of body text. Presenter reads them word-for-word. Audience reads ahead, tunes out, checks email. "I'll just read the deck later" — they never do. Credibility: zero.
- **AFTER:** Every slide passes the 3-second test: headline states the insight ("Revenue grew 34% — fastest quarter since Series A"), not the topic ("Q3 Revenue"). Body text under 30 words. Data slides have highlighted takeaways with annotations. Squint test: one visual element dominates. Audience listens to the presenter because the slides are visual aids, not teleprompters.

**Audience-Centric Design:**
- **BEFORE:** Same deck for the board, the engineering team, and the customer advisory council. Engineers are bored by oversimplified business metrics. Board members are confused by architecture diagrams. "One-size-fits-all" fits nobody.
- **AFTER:** Three versions of the same core narrative, tailored per audience: Board version (decision-first, 10 slides, pre-read with data appendix, meeting = discussion). Engineering version (architecture depth, technical credibility, "how we'll build it"). Customer version (problem agitation, social proof, product demo, clear CTA). Same through-line, different evidence and depth.

**Data Visualization:**
- **BEFORE:** Slide titled "Revenue by Quarter." A 3D bar chart with 12 bars, gridlines, a legend in the corner, and axis labels in 10pt font. Presenter: "As you can see from this chart, revenue has been growing. The blue bars represent domestic, the orange bars represent international. Q3 was particularly strong." Audience squints, checks phones, waits for the presenter to tell them what they're supposed to see. The chart is decoration, not communication.
- **AFTER:** Slide headline: "International revenue grew 89% in Q3 — now 42% of total revenue, up from 28%." One clean bar chart: domestic bars in light gray, international bars in bold brand color. Q3 bar annotated with a circled "+89% YoY" callout. Gridlines removed. Legend removed — bars labeled directly. Audience gets the insight in 3 seconds. The presenter uses the chart as evidence for the headline they just stated, then moves to implications: "This means we need to double our international support team by Q1."

**Delivery Preparation:**
- **BEFORE:** Slides finished at 2 AM the night before. Zero rehearsal. Presenter sees slide 7 for the first time while presenting it. "Oh, what's this chart showing?" Filler words: 15 "ums" per minute. Runs 8 minutes over. Q&A: "That's a great question — I'll have to get back to you on that."
- **AFTER:** Three full rehearsals minimum: Run 1 (timing), Run 2 (flow and transitions), Run 3 (full dress with clicker, timer, and recording). Speaker notes are complete sentences with transition phrases between slides. Q&A prep: 5 likely tough questions with prepared answers. Presenter knows exactly where the 18-minute mark hits and has a plan to cut 3 minutes on the fly if needed.

**What good looks like:** The audience can summarize the presentation in one sentence 24 hours later. Every slide passes the 3-second test. Data slides have headlines that state insights, not topics. The presentation has an emotional arc — tension builds, gets resolved. Speaker notes read like a natural conversation, not a script. Zero stock photos. The call-to-action is crystal clear. The deck could be presented by someone who's never seen it before, using only the speaker notes, and the audience would still get the message.

## Verification

Run these checks before considering any presentation complete:

- [ ] Narrative structure selected and appropriate for audience + goal
- [ ] Through-line (one-sentence summary) passes the curiosity test
- [ ] Every slide passes the 3-second test (headline states insight)
- [ ] No slide has more than 30 words of body text
- [ ] Opening slide is strongest hook (not "Agenda")
- [ ] Closing slide is CTA (not "Thank you" or "Questions?")
- [ ] Data slides: insight headline + highlighted data + annotation
- [ ] Zero stock photos of generic business scenes
- [ ] Font sizes: 30pt+ (in-person), 24pt+ (virtual)
- [ ] Color contrast meets WCAG AA (4.5:1 for body text)
- [ ] Speaker notes: complete sentences with transitions between slides
- [ ] At least 2 full rehearsals completed and timed
- [ ] Q&A prep: 5 likely questions with prepared answers
- [ ] Deck file size under 20MB (compress images if over)
- [ ] Backup format saved (PDF) in case .pptx/.key fails

## Gotchas

- **The "one more slide" trap.** Adding slides to "be thorough" kills presentations. Every slide dilutes every other slide. A tight 10-slide deck has more impact than a comprehensive 30-slide deck. **Total cost: losing the deal because the audience checked out by slide 18. For a $2M funding round, that's $2M lost because you wouldn't stop adding slides.** Cut to the bone, then cut one more.
- **Reading slides to the audience.** The #1 presentation sin and the fastest way to lose credibility. If the audience can read, and your slides have all the text, why are you there? **Total cost: credibility death — $0 raised, $0 sold, 0 minds changed.** Every word on a slide is a word the audience isn't hearing you say. Put the text in your speaker notes, not on the slide.
- **Designing without knowing the room.** A dark-background slide deck designed on a 27" retina display will be illegible when projected on a washed-out conference room projector from 2009. **Total cost: $5K-$50K in production value wasted on a deck nobody can read.** Scout the room. Test your slides on the actual projector if possible. Always have a high-contrast backup version.
- **The demo curse.** Live demos fail 40% of the time — Wi-Fi dies, credentials expire, APIs change. If your entire presentation depends on a live demo working, you're gambling with your credibility. **Total cost: a failed demo in a $500K sales pitch is a $500K gamble.** Record the demo as a video (with voiceover) and play it. If the live demo works, great — you have two versions. If it fails, you have a backup.
- **Virtual presentation without engagement markers.** In a virtual presentation, audience attention drops to near-zero after 7 minutes without interaction. **Total cost: presenting to an audience that checked out 20 minutes ago — your message reached exactly 0 people.** Insert engagement markers every 5-7 slides: a poll ("How many of you have experienced this?"), a chat prompt ("Drop in chat: what's your biggest challenge with X?"), a rhetorical question with a pause, or a quick story.
- **Using company template without modification.** Corporate templates are designed by committee — they cram logos, legal disclaimers, 7 shades of brand blue, and a footer that takes up 20% of the slide. **Total cost: 20-40% of every slide wasted on branding that nobody cares about.** Strip the template to bare essentials: one logo (small, in corner), one brand color (as accent), whitespace. Your content is the brand — not the footer.
- **No dry run of tech setup.** "Can everyone see my screen?" is not how you want to open. Test: projector connection, clicker/remote, audio (if playing video), screen resolution, font rendering (especially custom fonts), and backup computer. **Total cost: $10K-$100K in lost opportunity when 5 minutes of a 20-minute slot is wasted on tech fumbling.** Arrive 30 minutes early. Test everything. Have a PDF backup on a USB drive and in email.
- **Overdesigning to compensate for weak content.** Beautiful slides with weak arguments are still weak arguments. No amount of animation, gradient, or custom icon can save a presentation that doesn't have a clear point. **Total cost: spending $5K-$20K on a designer when the narrative needed a strategist, not a decorator.** Fix the story first. Design amplifies the message — it doesn't create it.
- **Opening with "About Us" or "Agenda" slides.** The first 30 seconds of a presentation are the highest-attention window you'll ever have. Wasting them on a logo slide and agenda list ("I'll cover Q3 results, product updates, and hiring") tells the audience nothing they couldn't read in an email. They check their phones. You never recover their attention. **Total cost: $5K-$50K in lost opportunity — a board presentation that fails to persuade, a sales pitch that doesn't close, a conference talk nobody remembers.** Fix: Open with a provocative statement, surprising statistic, or compelling story that states the thesis. "Last quarter, we lost $2M to a problem nobody is tracking." Now they're listening. Slide 1 = your best argument, not your name.
- **Using the same presentation deck as both a projected visual and a leave-behind document.** Slides designed for projection (minimal text, visual-heavy, presenter-dependent) fail as documents (no context, no explanation, no value without the speaker). Slides designed as documents (dense text, complete sentences, self-contained) fail as projected visuals (audience reads instead of listens). The compromise deck satisfies neither purpose. **Total cost: $5K-$25K per presentation — wasted preparation effort producing a deck that fails at both jobs, plus missed influence with decision-makers who review the "leave-behind."** Fix: Build two versions: (1) Presentation deck: one idea per slide, < 30 words, visual-dominant, 3-second test. (2) Leave-behind PDF: includes slide image + 2-3 paragraph narrative per slide, self-contained, readable without the presenter. This takes 20% more effort and 5x the impact.

## Deliberate Practice

Build these skills through structured repetition:

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | The 10→5→3 exercise: Take a 30-slide deck. Cut to 10 without losing the argument. Then to 5. Then to 3. The 3-slide version is your core narrative — everything else supports it. Do this with 5 different decks from your company. | Weekly |
| **Competent** | Slide diagnosis challenge: Take 5 real-world presentations (your company's, competitors', famous keynotes). For each of 50 slides, answer: (a) What's the ONE point? (b) Does the headline state the insight? (c) Does it pass the 3-second test? (d) What would you change? | Monthly |
| **Expert** | Speaker notes reverse-engineering: Take a famous speech (TED talk, product launch, commencement). Write the speaker notes you think they prepared. Then watch the talk and compare. Where did they deviate? Where did they improvise? What did they cut for time? Do this for 10 talks. | Quarterly |
| **Master** | Recorded rehearsal analysis: Present a 5-minute segment to camera. Watch without sound (body language only). Listen without video (voice only — count filler words, check pacing). Watch normally. Fix the top 3 issues. Repeat 5 times. Track: filler word count per minute (target < 3), pace (target 120-150 wpm), and slide transition smoothness. | Monthly |

**The One Highest-Leverage Activity:** Record yourself presenting for 5 minutes. Watch it. You will discover more about your presentation skills in those 5 minutes than from any book, course, or coach. Most people never do this — which is why most presentations are bad. Do it 10 times and you'll be in the top 5% of presenters.

## Troubleshooting Common Failures

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| **Audience asks "can you go back to slide X?"** | Narrative jumps, no logical flow between slides | Add transition sentences between every slide. Each slide should answer the question the previous slide raised. |
| **Decision-maker says "this is interesting but not a priority right now"** | Failed to connect the presentation to their top-of-mind concerns | In the first 3 slides, explicitly name the problem THEY care about, not the one YOU want to solve. |
| **Q&A goes off-topic or becomes hostile** | Presentation didn't pre-emptively address objections | Add a "Common Concerns" slide that names and neutralizes the top 3 objections before Q&A begins. You control the frame. |
| **Audience remembers nothing 24 hours later** | No repetition of the core message | Rule of three: state your through-line in the opening, reinforce it in the middle with evidence, restate it at the close. One message, three passes. |
| **Presenter runs out of time before reaching the conclusion** | No time budget per section | Allocate minutes per section in speaker notes. Mark "must-cover" vs "nice-to-have" slides. Practice cutting 30% of content on the fly. |
| **Slides look different on the projector than on your laptop** | Color profile mismatch, custom fonts missing, resolution difference | Always test on the actual projector. Embed fonts. Use sRGB color profile. Have a high-contrast PDF backup. |

## References

* [Narrative Structure Guide](../references/narrative-structures.md) — Minto Pyramid, SCQA, Hero's Journey, Monroe's Motivated Sequence with examples
* [Slide Design Principles](../references/slide-design-principles.md) — Typography, color, layout, visual hierarchy, accessibility, cognitive load
* [Data Storytelling on Slides](../references/data-storytelling.md) — Chart selection matrix, annotation techniques, highlighting methods, 3-second rule for data
* [Pitch Deck Templates](../references/pitch-deck-templates.md) — YC, Sequoia, 500 Startups formats; stage-specific guidance (pre-seed through Series B)
* [Virtual Presentation Guide](../references/virtual-presentation-guide.md) — Camera positioning, lighting, audio, engagement tactics, platform-specific tips (Zoom/Teams/Meet)
* [Presentation Delivery Mastery](../references/presentation-delivery.md) — Voice, pacing, body language, eye contact, handling nerves, Q&A techniques
* [Audience Analysis Framework](../references/audience-analysis.md) — Persona development, objection mapping, prior knowledge calibration, CTA design
* [Common Presentation Patterns](../references/common-patterns.md) — Architecture shared across all presentation types
