---
author: Sandeep Kumar Penchala
type: reference
domain: product-strategy
version: "1.0"
last_updated: 2026-07-21
parent_skill: product-strategist
---

# Product Strategy Frameworks

> **Author:** Sandeep Kumar Penchala

A practical reference of the most impactful product strategy frameworks — how to define, evaluate, and operationalize product direction. Covers North Star metrics, Opportunity Solution Trees, Product Kata, Working Backward, Jobs-to-be-Done, and Blue Ocean Strategy. Use alongside the Product Strategist skill's market analysis and roadmap planning.

---

## 1. North Star Framework

The North Star is a single metric that captures the core value your product delivers. It aligns the entire organization around one measure of success.

### Defining a North Star metric
```
Good North Star = [action] that measures [value] for [user]

Examples:
- Spotify:     "Time spent listening" — value = entertainment consumption
- Airbnb:      "Nights booked" — value = travel fulfilled
- Slack:       "Messages sent" — value = team communication
- Intercom:    "Customer interactions resolved" — value = support delivered
- Duolingo:    "DAUs completing a lesson" — value = learning progress
```

### North Star canvas (copy-paste template)
```
| Component          | Description |
|--------------------|-------------|
| North Star         | [One metric that measures delivered value] |
| Result metric      | [Business outcome (revenue, retention)] |
| Input metric #1    | [Leading indicator 1 — what drives the NS] |
| Input metric #2    | [Leading indicator 2] |
| Input metric #3    | [Leading indicator 3] |
| Metric owner       | [Team/role accountable] |
| Cadence            | [Daily/Weekly/Monthly review] |
```

### Operationalizing
1. Instrument the North Star metric in analytics (Segment/Mixpanel/Amplitude)
2. Create a real-time dashboard visible to the entire company
3. Monthly review: is the North Star moving? Are input metrics predictive?
4. **Counter-metric:** Always track one metric that could be gamed (e.g., if NS is "messages sent," track "daily active users" to ensure engagement isn't hollow)

---

## 2. Opportunity Solution Tree (OST)

OST maps the path from desired outcome → opportunities → solutions → experiments. Created by Teresa Torres for continuous discovery.

```
                            ┌──────────────────┐
                            │  DESIRED OUTCOME  │
                            │  (e.g., "Increase  │
                            │   trial-to-paid   │
                            │   conversion 20%") │
                            └────────┬──────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
    ┌─────────▼────────┐  ┌─────────▼────────┐  ┌─────────▼────────┐
    │   OPPORTUNITY 1   │  │   OPPORTUNITY 2   │  │   OPPORTUNITY 3   │
    │ "Users don't see  │  │ "Onboarding takes │  │ "Pricing page     │
    │  value before     │  │  too many steps"   │  │  creates sticker  │
    │  trial expires"   │  │                    │  │  shock"           │
    └────────┬──────────┘  └────────┬──────────┘  └────────┬──────────┘
             │                      │                      │
    ┌────────▼────────┐    ┌───────▼────────┐    ┌────────▼────────┐
    │  SOLUTIONS       │    │  SOLUTIONS     │    │  SOLUTIONS      │
    │  • Guided setup  │    │  • SSO quick-  │    │  • ROI calc     │
    │  • Sample data   │    │    start       │    │  • Annual plan  │
    │  • Use-case      │    │  • Skip steps  │    │  • Free tier    │
    │    templates     │    │    for role     │    │    limits raise │
    └────────┬────────┘    └───────┬────────┘    └────────┬────────┘
             │                     │                       │
    ┌────────▼────────┐    ┌───────▼────────┐    ┌────────▼────────┐
    │  EXPERIMENTS     │    │  EXPERIMENTS   │    │  EXPERIMENTS    │
    │  A/B test guided │    │  A/B test SSO  │    │  Usability test │
    │  setup vs free-  │    │  button on     │    │  ROI calculator │
    │  form onboarding │    │  first screen   │    │  placement      │
    └─────────────────┘    └───────────────┘    └─────────────────┘
```

### OST rules
1. Start from the outcome — not a solution, not a feature request
2. Opportunities are *customer problems* — framed as "I wish…" or "It's hard to…"
3. Only explore solutions AFTER mapping opportunities
4. Each solution gets at least one experiment before building
5. Revisit the tree monthly; prune branches that don't test well

---

## 3. Product Kata

A scientific method for product development adapted from Toyota Kata. Four steps, repeated continuously.

```
┌──────────────────────────────────────────────────────┐
│                   PRODUCT KATA CYCLE                  │
│                                                      │
│   1. UNDERSTAND    ───►   2. IDEATE                  │
│   Current state,        Brainstorm solutions,        │
│   customer data,         prioritize by impact,        │
│   constraints            form hypotheses              │
│       ▲                                      │        │
│       │                                      ▼        │
│   4. TEST             ◄───   3. PROTOTYPE             │
│   Validate with real       Build smallest             │
│   users, measure,          testable artifact,         │
│   learn, repeat            define success criteria    │
└──────────────────────────────────────────────────────┘
```

### Kata board template (Trello/Jira columns)
```
| Backlog        | Understand      | Ideate        | Prototype     | Test          | Done/Rejected  |
| (unstructured  | (problem        | (solutions    | (build MVP,   | (collect      | (shipped or    |
|  ideas)        |  validated)     |  selected)    |  wireframe,   |  data,        |  killed w/     |
|                |                 |               |  clickable)   |  interview)   |  learnings)    |
```

### Example cycle: "Reduce cart abandonment"
- **Understand:** Analytics show 68% drop-off at shipping page. 5 user interviews reveal: "shipping cost is a surprise."
- **Ideate:** Show estimated shipping earlier (product page), offer free shipping threshold banner
- **Prototype:** Figma mockup of product-page shipping estimate, test with 5 users
- **Test:** 3/5 users noticed the estimate; 2/5 said they'd proceed. Ship A/B test.

---

## 4. Working Backward (Amazon)

Start from the customer and work backward. Write the press release BEFORE writing code.

### The three documents (in order)
1. **Press Release (PR/FAQ):** ~1 page. Announces the product as if it's launching tomorrow. Includes:
   - Headline + subheading (what, who, why)
   - Customer problem paragraph
   - Solution paragraph
   - Customer quote (fictional but realistic)
   - How to get started
2. **FAQ (internal):** External FAQs (customer questions) + Internal FAQs (business/tech questions). 5–10 questions each.
3. **User Manual:** Step-by-step guide for a new user. Forces you to think through the entire experience.

### Press Release template
```markdown
# [Product Name] Launches to [Solve Problem] for [Target Customer]

**Seattle, WA — [Date]** — [Company] today announced [product], a new
[category] that [key benefit in one sentence].

[Paragraph explaining the customer problem with a concrete example
and a relatable quote from a target persona.]

[Paragraph describing how the product solves this problem, including
the 1–2 most compelling features. No feature lists — tell the story.]

["Before [product], we [pain point]. Now, [delight]," said [Name],
[Role] at [Customer Company].]

[Product] is available starting today at [URL]. Plans start at [$X/mo].
```

### When to use
- Major new product or feature launch
- Pivot decisions — write PRs for both paths and compare
- Quarterly roadmap planning — PRs for top 3 bets

---

## 5. Jobs-to-be-Done (JTBD)

Customers "hire" products to make progress in their lives. The job is the unit of analysis — not the customer, not the product.

### Job types
```
| Type         | Definition                          | Example                        |
|--------------|-------------------------------------|---------------------------------|
| Functional   | The practical task                  | "Send money to a friend"       |
| Emotional    | How they want to feel               | "Feel generous and helpful"    |
| Social       | How they want to be perceived       | "Look tech-savvy in my group"  |
```

### JTBD Forces Diagram
```
    PUSH (of current)          PULL (of new solution)
    "Current way is             "New way promises
     frustrating, slow"         instant results"
                    \          /
                     PERSON ──► DECISION
                    /          \
    ANXIETY (of new)           INERTIA (of current)
    "Will it work?             "Switching is a
     Is it worth it?"          hassle, I'm used to this"
```

### JTBD interview questions (10-question guide)
1. "Tell me about the last time you [did the task]. Walk me through it step by step."
2. "What triggered you to look for a solution? What happened right before?"
3. "What alternatives did you consider? Why didn't you choose them?"
4. "What did you try before finding [product]?"
5. "What would you use if [product] didn't exist tomorrow?"
6. "Was there any hesitation before switching? What almost stopped you?"
7. "Who else was involved in the decision? What did they care about?"
8. "What's the biggest frustration with how you did this before?"
9. "What does success look like for this task? How do you know it's done right?"
10. "Has the job changed since you started using [product]? How?"

---

## 6. Strategy Canvas (Blue Ocean)

The eliminate-reduce-raise-create (ERRC) grid identifies uncontested market space.

### ERRC Grid template
```
┌──────────────────────┬──────────────────────┐
│      ELIMINATE        │        RAISE          │
│  Factors the industry │  Factors to raise     │
│  takes for granted    │  well above standard  │
│  that can be removed  │                       │
├──────────────────────┼──────────────────────┤
│       REDUCE          │        CREATE         │
│  Factors to reduce    │  Factors the industry │
│  well below standard  │  has never offered    │
└──────────────────────┴──────────────────────┘
```

### Example: Airbnb (vs. hotels)
- **Eliminate:** Front desk, room service, standardized rooms
- **Reduce:** Price per night, formal check-in process
- **Raise:** Local authenticity, living space size, kitchen access
- **Create:** Host-guest relationship, neighborhood guides, long-term stays

### Strategy canvas construction
1. List 8–12 competitive factors in your industry (x-axis)
2. Score each competitor 1–5 on each factor (y-axis)
3. Plot your current offering as a line
4. Design your target line using ERRC shifts
5. The new line should NOT overlap existing competitors — that's blue ocean

---

See also: Product Strategist skill for market analysis, competitive landscape mapping, and product portfolio strategy.
