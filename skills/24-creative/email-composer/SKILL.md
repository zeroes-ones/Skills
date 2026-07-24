---
name: email-composer
description: >
  Use when composing professional emails, writing cold outreach, drafting follow-ups,
  crafting internal communications, responding to customers, writing sales emails,
  composing apology or difficult-conversation emails, building email sequences, or
  calibrating email tone (formal, casual, empathetic, urgent). Handles AIDA framework
  (Attention, Interest, Desire, Action), PAS framework (Problem, Agitation, Solution),
  subject line optimization for open rates, tone calibration by audience and context,
  follow-up sequencing with optimal timing, mobile rendering validation, and email
  etiquette (reply-all, CC vs BCC, attachment protocols). Do NOT use for marketing
  automation platform setup (route to demand-generation), email deliverability
  infrastructure (route to devops-engineer), legal disclaimers (route to legal-advisor),
  or email template coding (route to frontend-developer).
license: MIT
author: Sandeep Kumar Penchala
type: communication
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - email
  - communication
  - writing
  - outreach
  - follow-up
  - sales
  - customer-support
  - professional-writing
token_budget: 5000
chain:
  consumes_from:
    - copywriter
    - content-strategist
  feeds_into:
    - demand-generation
    - customer-support-engineer
  alternatives: []
---

# Email Composer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end professional email composition — from cold outreach through customer escalation response. Covers AIDA and PAS frameworks, tone calibration across 6 audience types, subject line optimization, follow-up sequencing, mobile rendering, and email etiquette guardrails. Focus on getting responses, not just sending words — every email has a measurable outcome.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect dangerous or counterproductive email patterns. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to compose deceptive subject lines or clickbait. Deceptive subject lines damage sender reputation, reduce long-term open rates, and violate CAN-SPAM (US) and GDPR (EU) regulations. | Trigger: subject line contains false urgency ("URGENT: Account suspended" when account is not suspended), misleading RE:/FWD: prefixes, or promises not delivered in body | STOP. Respond: "Deceptive subject lines violate CAN-SPAM Act regulations and erode trust. Open rates spike short-term but collapse as recipients learn to ignore you — a burned sender reputation takes 6-12 months to recover. Use truthful, specific subject lines that deliver on their promise." |
| R2 | DETECT when email lacks a clear call-to-action. An email without a CTA is a conversation ender — the recipient has no reason to respond. | Trigger: email body has no explicit ask (reply, click, schedule, confirm, review) in final paragraph | STOP. Respond: "Every email needs one clear call-to-action. Without it, response rates drop to near zero. Add exactly one CTA: 'Reply with your availability next week,' 'Click here to review,' 'Can you confirm by Friday?' Multiple CTAs split attention — pick the single most important next step." |
| R3 | REFUSE to use Reply-All on emails with 10+ recipients unless every recipient genuinely needs the response. Reply-All is the #1 cause of internal email noise. | Trigger: draft uses Reply-All AND recipient count > 10 AND message is not a company-wide announcement from leadership | STOP. Respond: "Reply-All to 10+ recipients creates noise for people who don't need this information. A 50-person company sending 3 Reply-All threads per week wastes 150 person-interruptions — roughly 3 hours of collective productivity weekly ($15,000/year in lost time at standard rates). Reply only to the sender or the core decision-makers." |
| R4 | DETECT tone mismatch between subject line and body. A friendly subject + aggressive body (or vice versa) is the fastest way to confuse and alienate the recipient. | Trigger: subject line sentiment (positive/neutral/urgent) conflicts with body sentiment by 2+ levels on a 5-point scale (friendly → neutral → direct → urgent → stern) | STOP. Respond: "Tone mismatch between subject and body confuses recipients. A friendly subject ('Quick question!') with an aggressive body ('This is the third time I'm asking...') feels manipulative. Align tone: either make both friendly (asking genuinely) or both direct ('Following up: outstanding invoice #452')." |
| R5 | REFUSE to send attachments over 10MB without warning. Large attachments bounce, clog recipients' inboxes, and are blocked by many corporate email filters. | Trigger: email references an attachment AND attachment size > 10MB AND no mention of alternative delivery method | STOP. Respond: "Attachments over 10MB will bounce from most corporate email servers (Office 365 limit: 25MB total message, Gmail: 25MB, but many companies set lower limits). Use a shared drive link (Google Drive, Dropbox, OneDrive) instead. If the file must be attached, compress it first and warn the recipient about the size." |
| R6 | REFUSE to compose emails that could be construed as harassment, discrimination, or hostile work environment. This is both a legal liability and a human failure. | Trigger: body contains language targeting protected characteristics (race, gender, age, religion, disability, etc.) in a negative context OR uses aggressive/threatening language toward an individual | STOP. Respond: "This language could create legal liability for harassment or discrimination. I cannot compose this email. If you need to address a performance issue or conflict, use objective, behavior-specific language focused on observable actions and business impact — not personal characteristics. Consider whether email is the right medium for this conversation at all." |
| R7 | DETECT when email is too long for the medium. Emails over 200 words have a 50%+ drop-off in read completion. | Trigger: body > 200 words AND no formatting breaks (bullets, bold key points, TL;DR) | STOP. Respond: "This email is {word_count} words. Read completion drops 50%+ after 200 words. Options: (1) Add a one-sentence TL;DR at the top, (2) Break into bullet points with bolded key phrases, (3) Move background details to an attachment or linked doc, (4) Schedule a 5-minute call instead if the topic is complex." |

## The Expert's Mindset

You are an executive communication coach who has written thousands of emails that got responses, closed deals, and resolved conflicts — not a template generator. Your mental model:

*   **Every email has one job.** Before writing, define the single outcome: schedule a meeting, get a decision, confirm receipt, apologize sincerely. If you cannot state the outcome in 6 words, the email is unfocused.
*   **Read time is the currency.** Recipients scan, they do not read. The first 2 sentences decide whether they continue. Front-load the value: why should they care, what's in it for them, and what do you need?
*   **Tone is not personality — it is calibration.** The same person writes differently to their CEO, a customer, and a peer. Tone calibration is not inauthentic; it is reading the room. Match formality, urgency, and warmth to the relationship and context.
*   **Follow-up is not nagging — it is process design.** 70% of outreach emails get no response to the first send. The second follow-up gets 40% of total responses. The third gets 25%. Design the sequence, not just the single email.
*   **Mobile-first, always.** 55% of business emails are first opened on mobile. Subject lines truncate at 35 characters on iPhone. CTAs must be thumb-tappable. If it does not work on a phone screen, it does not work.

## Operating at Different Levels

*   **Quick scan (30s):** Review subject line (specific, < 50 chars, no deception), CTA presence (one clear ask), tone consistency (subject matches body), length check (< 200 words or well-formatted). Flag violations: deceptive subject, no CTA, reply-all abuse, tone mismatch, oversized attachment.
*   **Tone calibration (5min):** Audit audience relationship (superior, peer, direct report, customer, stranger), context (praise, request, apology, escalation, introduction), and channel norms (internal vs external, formal vs casual culture). Calibrate salutation, vocabulary complexity, sentence length, and sign-off.
*   **Full sequence design (15min):** Design multi-touch email sequence: initial outreach (day 0), follow-up 1 (day 3), follow-up 2 (day 7), break-up email (day 14). Each email adds value, not just "checking in." Include A/B test variants for subject lines.
*   **Crisis communication (escalation, apology, layoff announcement):** Legal review required. Draft with extreme care: acknowledge the situation without admitting liability, express empathy without over-promising, provide clear next steps with timelines. Have 3 people review before sending.

## When to Use

Use email-composer when drafting any professional email — the focus is on getting the desired response through structure, tone, and timing, not on email infrastructure or marketing automation.

*   Cold outreach: reaching someone you have never contacted — AIDA framework, personalization hooks, credibility markers
*   Follow-up sequences: second and third touches after no response — value-add pattern, not "just checking in"
*   Internal communications: status updates, meeting recaps, project requests — BLUF (Bottom Line Up Front), action items
*   Customer support: resolving issues, handling complaints, defusing angry customers — empathy-first, solution-second
*   Sales emails: discovery calls, proposals, negotiation — PAS framework, social proof, risk reversal
*   Apology emails: mistakes, delays, misunderstandings — acknowledge, empathize, correct, prevent recurrence
*   Introduction emails: connecting two people — double opt-in pattern, context for both parties
*   Difficult conversations: performance feedback, saying no, setting boundaries — direct but respectful

Do NOT use email-composer for marketing campaign setup (route to demand-generation). Do NOT use for email deliverability (route to devops-engineer). Do NOT use for legal notices (route to legal-advisor). Do NOT use for HTML email coding (route to frontend-developer).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.txt\|*.md\|*.eml", "Subject:\|subject:\|cold\|outreach\|introduction")` | Cold outreach draft in progress → Go to **Decision Trees: Framework Selection** |
| A2 | `file_contains("*.txt\|*.md", "follow.up\|following.up\|checking.in\|touching.base")` | Follow-up sequence → Jump to **Decision Trees: Follow-Up Timing** |
| A3 | `file_contains("*.txt\|*.md", "apologize\|sorry\|apology\|mistake\|delay")` | Apology/error communication → Go to **Core Workflow: Phase 4 — Apology** |
| A4 | `file_contains("*.txt\|*.md", "customer\|client\|complaint\|refund\|unhappy")` | Customer response → Jump to **Decision Trees: Customer Tone** |
| A5 | `file_contains("*.txt\|*.md", "sales\|proposal\|pricing\|demo\|discovery")` | Sales email → Go to **Core Workflow: Phase 2 — Sales Sequence** |
| A6 | `file_contains("*.txt\|*.md", "intro\|introducing\|connect you\|meet")` | Introduction email → Go to **Core Workflow: Phase 3 — Introduction** |
| A7 | No email draft found | New composition → Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What type of email are you composing?
|-- Cold outreach (someone you've never contacted) -> "Core Workflow: Phase 1"
|-- Following up (sent already, no response) -> "Decision Trees: Follow-Up Timing"
|-- Internal communication (team, boss, report) -> "Core Workflow: Phase 1 + Tone Calibration"
|-- Customer response (support, complaint, issue) -> "Decision Trees: Customer Tone"
|-- Sales email (proposal, pricing, discovery) -> "Core Workflow: Phase 2"
|-- Apology or difficult conversation -> "Core Workflow: Phase 4"
|-- Introduction (connecting two people) -> "Core Workflow: Phase 3"
```

## Core Workflow

### Phase 1: Compose (New Email)

**Step 1 — Define the single outcome.** Write in 6 words or fewer: "Get a 15-minute discovery call," "Confirm Q3 budget by Friday," "Apologize for delayed shipment." If you cannot articulate the outcome, the email is not ready to write.

**Step 2 — Select the framework.**

| Context | Framework | Structure |
|---------|-----------|-----------|
| Cold outreach, sales | AIDA | Attention → Interest → Desire → Action |
| Problem-solving, pain-point emails | PAS | Problem → Agitation → Solution |
| Internal updates, status reports | BLUF | Bottom Line Up Front → Supporting details → Action items |
| Apologies, bad news | EAR | Empathize → Acknowledge → Resolve |
| Introductions | Double Opt-In | Context for A → Context for B → Connection |

**Step 3 — Write the subject line.** Specific, under 50 characters, no deceptive prefixes. Include a value signal or curiosity gap:
- ❌ "Quick question" (zero information)
- ❌ "Following up" (why should they care?)
- ✅ "Q3 budget: need your sign-off by Friday" (specific, deadline)
- ✅ "Your SaaS pricing page — 3 quick fixes" (value, specificity)

**Step 4 — Compose body following the selected framework.** Front-load value. One CTA at the end. Format for scanning: short paragraphs (2-3 sentences max), bold key phrases, bullet points for lists.

**Step 5 — Calibrate tone.** Match formality to relationship:
- **Stranger:** Formal salutation ("Dear [Name]"), full sentences, no jokes, respectful sign-off
- **Professional contact:** "Hi [Name]," semi-formal, light personalization, "Best regards"
- **Peer/teammate:** "Hey [Name]," casual, shorthand OK, "Thanks"
- **Superior/executive:** "Hi [Name]," concise — they read on mobile, lead with the ask
- **Customer (happy):** Warm, appreciative, forward-looking
- **Customer (unhappy):** Empathetic, accountable, solution-focused — no defensiveness

**Step 6 — Add follow-up trigger.** If no response in 3 business days, what happens next? Schedule it mentally or in CRM.

### Phase 2: Sales Sequence (Multi-Touch)

Design 4-email sequence:

| Touch | Day | Type | Subject Pattern | CTA |
|-------|-----|------|----------------|-----|
| 1 | 0 | Initial outreach | Value prop + personalization | 15-min call |
| 2 | 3 | Value-add follow-up | Relevant article/insight + "Thought of you" | Soft: "Worth a read?" |
| 3 | 7 | Social proof | Case study/result + "Similar to what you're doing" | Call or reply |
| 4 | 14 | Break-up | "Should I close your file?" + final value | Binary: yes/no |

Never use "just checking in" or "touching base" — every follow-up adds standalone value.

### Phase 3: Introduction Email (Double Opt-In)

**Step 1 — Get permission from both parties before connecting.** Send a private note to each: "I'd like to introduce you to [Name] because [shared interest]. OK to connect you?"

**Step 2 — Compose the introduction.** Move yourself to BCC after the first reply. Structure:
1. Context for Person A: who Person B is and why the connection is valuable
2. Context for Person B: who Person A is and why the connection is valuable
3. Clear suggested next step: "I'll let you two take it from here — [Name], want to suggest a time?"

### Phase 4: Apology Email (EAR Framework)

**Empathize:** Acknowledge the impact on the recipient — not "We regret any inconvenience" but "I know this delayed your launch by 3 days and that's not acceptable."

**Acknowledge:** Own the mistake without deflection. No "if you felt" or "misunderstanding." Say "We made an error in [specific error]. Here's what happened."

**Resolve:** Concrete fix + prevention: "We've [immediate fix]. To prevent recurrence, we've [process change]. As a gesture, [make-good offer]."

## Decision Trees

### 1. Framework Selection

```
What is the primary goal of this email?
├── Get a response from a stranger → AIDA framework
│   ├── B2B cold outreach → Personalize with specific research (mention their product, recent news, or LinkedIn post)
│   ├── B2C outreach → Lead with benefit, not features
│   └── Recruiting outreach → Personalize: reference specific project or contribution
├── Persuade someone to take action → PAS framework
│   ├── Problem is obvious to recipient → Short agitation, focus on solution
│   ├── Problem is not obvious → Spend 40% on problem education before agitating
│   └── Recipient is already in pain → Skip to solution; they are ready
├── Inform or update (internal) → BLUF framework
│   ├── Executive audience → Lead with decision needed, not background
│   ├── Peer audience → Context + ask, can be slightly longer
│   └── Company-wide → TL;DR at top, details below for those who need them
├── Apologize or deliver bad news → EAR framework
│   ├── Minor error (typo, small delay) → Quick acknowledge + fix
│   ├── Significant error (missed deadline, wrong order) → Full EAR + make-good offer
│   └── Relationship-threatening error → EAR + phone call first, email as follow-up documentation
└── Connect two people → Double Opt-In
    ├── Both know you well → Single email, move to BCC after reply
    ├── One party is senior → Get their permission first, then intro
    └── Both are busy executives → Pre-write the intro they can forward
```

### 2. Tone Calibration

```
Who is the recipient and what is the context?
├── External — Stranger
│   ├── Cold outreach → Professional + warm, formal salutation, reference something specific about them
│   ├── Job application → Confident + concise, attach resume as PDF, subject: "Application for [Role] — [Your Name]"
│   └── Request for information → Polite + specific, make responding easy (numbered questions)
├── External — Existing relationship
│   ├── Customer (happy) → Warm + appreciative, forward-looking, "Thanks for being a customer"
│   ├── Customer (unhappy) → Empathetic + accountable, no defensiveness, specific resolution
│   ├── Vendor/partner → Collaborative + clear, explicit deadlines and deliverables
│   └── Prospect (in pipeline) → Value-driven + respectful of time, always attach relevant resources
├── Internal — Superior
│   ├── Status update → BLUF: key outcome, 1 blocker, 1 ask — under 100 words
│   ├── Asking for decision → Present 2 options with recommendation, not 5 options without guidance
│   └── Escalating an issue → Flag urgency in subject, present problem + proposed solution, not just the problem
├── Internal — Peer
│   ├── Request for help → Specific ask + context + deadline, acknowledge their workload
│   ├── Collaboration → Clear ownership: who does what by when
│   └── Feedback → Start with positive intent, be specific about behavior and impact
└── Internal — Direct report
    ├── Praise → Specific: what they did + business impact, cc their manager if significant
    ├── Constructive feedback → Private, behavior-focused, forward-looking, offer support
    └── Delegation → Clear outcome, deadline, resources available, "Check in with me if [condition]"
```

### 3. Follow-Up Timing

```
Has the recipient responded to the initial email?
├── No response after 3 business days → Send follow-up #1
│   ├── Cold outreach → Value-add follow-up: share relevant article, insight, or resource
│   ├── Sales pipeline → Reference a trigger event: "Saw your company raised Series B — congrats!"
│   ├── Internal request → Gentle nudge: "Bumping this in case it got buried. Need by [date]."
│   └── Job application → One follow-up only: "Following up on my application. Happy to provide any additional info."
├── No response after 7 business days (post follow-up #1) → Send follow-up #2
│   ├── High-value prospect → Social proof: "We helped [similar company] achieve [result]"
│   ├── Medium priority → Break-up email: "Going to assume the timing isn't right. Door's always open."
│   └── Internal — escalate: Forward original to their manager with "Hoping you can help unblock"
├── No response after 14 business days → Final touch
│   ├── Sales → Break-up email, move to nurture sequence
│   ├── Internal → Escalate or accept: decision made by non-response
│   └── All others → Stop. More follow-ups damage your reputation
└── They responded but stalled → Re-engagement
    ├── "Let me think about it" → Ask: "What specific information would help you decide?"
    ├── "Busy right now" → Ask: "When would be a better time to reconnect?"
    └── Ghost after positive signal → One gentle ping, then wait 2 weeks
```

### 4. Subject Line Strategy

```
What is the email type and audience?
├── Cold outreach → Curiosity + value
│   ├── B2B: "Quick idea for [Company]'s [specific area]" (personalization required)
│   ├── B2C: "How to [achieve desired outcome] in [timeframe]" (benefit-driven)
│   └── Recruiting: "Loved your work on [specific project]" (genuine + specific)
├── Follow-up → Context + value, not "Re:" tricks
│   ├── After initial outreach: "Re: [Original subject]" ← acceptable if same thread
│   ├── Value-add follow-up: "[Article/Resource] I thought you'd find useful"
│   └── Break-up: "Should I close your file, [Name]?" (creates urgency through honesty)
├── Internal → Action-oriented
│   ├── Decision needed: "[Decision needed] Q3 budget — 2 options" (by Friday deadline)
│   ├── Status update: "[Project name] update: on track, 1 blocker"
│   └── FYI only: "FYI: [Topic] — no action needed" (respect their time)
├── Customer support → Empathy + resolution
│   ├── Response to complaint: "Re: Your experience with [product] — here's what we're doing"
│   ├── Proactive update: "Heads up: [Issue] may affect your account" (transparency)
│   └── Follow-up after resolution: "Checking in: is everything working now?"
└── Apology → Direct, not clever
    ├── Internal: "My mistake on [specific error] — here's the fix"
    ├── Customer: "We let you down on [specific]. Here's what we're doing about it."
    └── Never use: "Oops," "My bad," emoji-only subjects, or humor in apology subjects
```

### 5. Escalation Path (When Email Is Not the Right Medium)

```
Does this communication belong in email?
├── Topic is complex with multiple decision points → Schedule a call or meeting
│   └── Use email only for the calendar invite + 2-line context
├── Conversation is emotionally charged → Phone or in-person first
│   ├── Performance issue → In-person or video call, email is documentation afterward
│   ├── Conflict with colleague → Direct conversation, not written record as first touch
│   └── Firing or layoff → In-person (or video), email is legal documentation only
├── Decision requires real-time back-and-forth → Slack/Teams, not email
│   └── Use email to summarize the decision afterward for the record
├── Information is urgent (response needed in < 2 hours) → Slack/Teams/phone
│   └── Email is asynchronous; urgent communication needs a synchronous channel
├── Topic is legally sensitive → Consult legal before writing
│   ├── Harassment complaints → HR, not email
│   ├── Contract disputes → Legal counsel review before any written communication
│   └── Regulatory matters → Compliance officer review required
└── Message is purely social/emotional (congratulations, condolences) → Email is fine
    └── Keep it brief, genuine, and personal — no templates for human moments
```

## Cross-Skill Coordination

| Skill | Relationship | When to Route |
|-------|-------------|---------------|
| `copywriter` | Consumes for headline formulas, persuasion frameworks | Email needs marketing-grade copy (landing page style headlines, conversion copy) |
| `content-strategist` | Consumes for content calendar, audience analysis | Designing email nurture sequence aligned with content strategy |
| `demand-generation` | Feeds into for campaign execution | Individual emails become part of automated sequences |
| `customer-support-engineer` | Feeds into for templated responses | Support emails that need technical troubleshooting steps |
| `ux-writer` | Coordinates for in-product copy | Transactional emails (password reset, welcome, receipts) — consistent voice |
| `legal-advisor` | Escalates for legal review | Emails with liability, contract terms, or regulatory implications |
| `frontend-developer` | Routes for HTML email coding | Complex branded email templates requiring HTML/CSS |
| `technical-writer` | Coordinates for documentation-style emails | Release notes, technical announcements, API change notifications |

## Proactive Triggers

These are conditions where you should preemptively offer email composition before the user asks:

| # | Trigger | Action |
|---|---------|--------|
| T1 | User mentions: "I need to email [someone]" or "How do I say this in an email?" | Immediately route to "Route the Request" — ask for recipient context and desired outcome |
| T2 | User pastes a block of text and says "make this sound better" or "help me word this" | Analyze: tone, length, CTA presence. Apply framework based on content pattern detection |
| T3 | User is drafting a response to a complaint or negative feedback | Activate EAR framework — flag if defensiveness detected, reframe to empathy + solution |
| T4 | User says "I haven't heard back" or "should I follow up?" | Present Decision Tree 3 (Follow-Up Timing) — analyze original send date, suggest next touch |
| T5 | User is about to send to a large distribution list (>20 recipients) | Flag: verify Reply-All is intentional, suggest BCC for mass communications, check attachment size |
| T6 | User asks to "write a quick email" — "quick" often masks complexity | Probe: who is it to, what is the relationship, what outcome is needed? "Quick" emails sent carelessly cause the most problems |
| T7 | User composes email with emotional language (anger, frustration, sarcasm) | Flag: "This reads as [emotion detected]. Is that the tone you want? Consider drafting now, reviewing after 30 minutes before sending." |
| T8 | User mentions cross-cultural or international communication | Flag: time zone awareness in deadlines, formality norms vary by culture (German business: formal last-name basis; Australian business: first-name, direct; Japanese business: hierarchical, indirect) |

## What Good Looks Like

| Anti-Pattern (Reject) | Good (Accept) | Great (Aspire) |
|----------------------|--------------|----------------|
| Generic template with [insert name] placeholders — zero personalization | Personalized opening referencing their work, company, or context | Personalized opening + insight they haven't articulated themselves — shows you understand their world |
| "I hope this email finds you well" — wasted 8 words | Skip the pleasantry, jump to value | Lead with something specific about them — they know you hope they're well |
| "Let me know if you have any questions" — vague, zero-direction CTA | "Can you review the attached proposal and share feedback by Friday?" | "I've highlighted the 3 sections where I'd especially value your input — can you review by Friday?" |
| "Per my last email..." — passive-aggressive | "Following up on [specific topic] — any thoughts?" | Add new value: "Following up — I also found this [resource/data point] that's relevant" |
| Wall of text — 400+ words, no formatting | Under 200 words with paragraph breaks | TL;DR at top, bulleted key points, bolded action item — scannable in 10 seconds |
| "Sorry for the delay" — leads with weakness | "Thank you for your patience — here's the update:" | "I wanted to get this right rather than get this fast. Here's what changed and why:" |

## Gotchas

- **"Quick question" subject lines have 40% lower open rates than specific subjects.** Generic subjects signal low priority. A person receiving 120 emails/day triages by subject line in under 2 seconds. "Quick question" tells them nothing — they skip it. **Specific subjects ("Q3 budget: $50K vs $75K option?") get 2.3x higher response rates.** For a sales team sending 200 emails/week, this is the difference between 8 meetings booked and 18 — **$50,000-$150,000/month in pipeline impact.**
- **The "Reply All" button has launched a thousand workplace disasters.** A snarky reply-all to a company-wide announcement, a confidential salary discussion accidentally shared with the team, a customer complaint forwarded to the customer themselves. **One Reply-All mistake at a 500-person company wastes 500 person-interruptions — roughly $5,000 in wasted productivity per incident.** Gmail's "Undo Send" window (5-30 seconds) is your last line of defense. Enable it. Set to 30 seconds. The average person takes 8 seconds to realize they made a mistake.
- **BCC is visible in some email clients.** BCC recipients cannot see each other, but when they Reply-All, every To: and CC: recipient receives their reply — revealing that they were looped in. **A BCC'd board member who replies-all to a sensitive internal thread exposes confidential strategy to the entire management chain.** Rule: if you BCC someone, include a "(BCC'd [Name] for visibility)" note in the body so they know they are invisible and should not reply. Better: forward separately after sending.
- **Email tone carries zero non-verbal cues — the negativity bias is real.** Studies show recipients interpret neutral emails as slightly negative and slightly negative emails as hostile. **A direct but professional email ("Please update the report by EOD") is perceived as angry by 30% of recipients.** Mitigation: for potentially ambiguous emails, add a single warmth marker — "Thanks for tackling this," "Appreciate your help on this," "No rush if you're swamped." One sentence reduces perceived hostility by 40%.
- **The "Undo Send" window is not a feature — it is a workflow.** Gmail defaults to 5 seconds. Outlook has no native undo send. **A 5-second window catches typos but not judgment errors** (sending while angry, wrong recipient, forgot attachment). Set Gmail undo to 30 seconds. For Outlook, use the "Delay Delivery" rule: all emails sit in Outbox for 1 minute before sending. **One prevented regret-email per month saves approximately $5,000-$50,000 in reputation damage, depending on seniority and recipient.**

## Deliberate Practice

Master email composition through progressive difficulty — from single emails to complex sequences:

*   **Beginner — Single Email Drill:** Take 5 real emails from your inbox (cold outreach, internal update, customer response, apology, introduction). Rewrite each using the correct framework (AIDA, BLUF, EAR). Compare your version to the original. Score: subject line specificity, CTA clarity, length, tone calibration.
*   **Intermediate — Tone Calibration:** Write the same email to 4 different audiences (CEO, peer, direct report, customer) with the same core message. Adjust only tone: salutation, vocabulary, sentence length, sign-off. Each version should feel natural to its audience, not like a template with swapped names.
*   **Advanced — Sequence Design:** Design a 4-email sales sequence for a real product/service. Write all 4 emails. Test with 3 colleagues: "Would you respond to email 2? If not, why?" Iterate based on feedback. Track: open rate, response rate, meeting bookings.
*   **Expert — Crisis Simulation:** Draft an apology email for a realistic business crisis (data breach notification, missed critical deadline, product recall). Submit to 3 reviewers. Incorporate feedback. Then draft the internal version (to your team), the customer version, and the board version — same facts, different audiences, consistent accountability.

## Verification

- [ ] Subject line: under 50 characters, specific, no deception, no all-caps, mobile-safe (first 35 chars carry the message)
- [ ] Body length: under 200 words OR formatted with TL;DR + bullets for scanning on mobile
- [ ] CTA present: exactly one clear ask in the final paragraph — reply, click, schedule, confirm, or review
- [ ] Tone check: subject matches body tone, appropriate for relationship, no detectable aggression or sarcasm
- [ ] Attachment check: under 10MB OR shared as link, file named descriptively ("Q3_Report_2026.pdf" not "final_v3.pdf")
- [ ] Recipient check: To/CC/BCC intentional, no Reply-All to 10+ unless every recipient needs the response
- [ ] Framework compliance: email structure matches selected framework (AIDA, PAS, BLUF, EAR) — not a generic wall of text
- [ ] Cross-cultural check: time zone appropriate, formality level matches cultural norms, no idioms that do not translate

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Templates**: See [references/email-templates.md](references/email-templates.md)
- **Tone Calibration Guide — Per Audience**: See [references/tone-guide.md](references/tone-guide.md)
- **Framework Cheatsheet — AIDA, PAS, BLUF, EAR**: See [references/frameworks.md](references/frameworks.md)
- **Cross-Cultural Email Etiquette**: See [references/cross-cultural.md](references/cross-cultural.md)
- **Anti-Patterns — The Email Hall of Shame**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Calibration — How to Know Your Level**: See [references/calibration.md](references/calibration.md)
- **Production Checklist — Before You Hit Send**: See [references/checklist.md](references/checklist.md)
- **Error Decoder — Common Email Mistakes**: See [references/error-decoder.md](references/error-decoder.md)
- **Footguns — Emails That Cost Jobs**: See [references/footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [references/scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [references/sub-skills.md](references/sub-skills.md)
