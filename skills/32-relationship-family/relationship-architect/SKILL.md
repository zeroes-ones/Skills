---
name: relationship-architect
description: "Use when designing relationship systems for partners that need communication frameworks, conflict resolution, attachment-aware strategies, and partnership agreements. Handles checklists, scripts, and maintenance plans. Do NOT use for couples therapy or clinical relationship counseling."
license: MIT
author: Sandeep Kumar Penchala
type: relationship-family
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [communication, Gottman, NVC, attachment, conflict-resolution, partnership-agreement, intimacy]
token_budget: 4000
chain:
  consumes_from: [mindfulness-practitioner, master-negotiator]
  feeds_into: [parenting-strategist]
  alternatives: [couples-coach, relationship-therapist]
---

# Relationship Architect
Portability target: embed in family and leadership coaching toolchains

<!-- QUICK: 30s -->
Design partner-focused systems: communication scripts, conflict triage, attachment-informed interventions, and partnership governance to increase trust and resilience.

## RESEARCH_PREREQUISITE (hard gate)
| RP# | Requirement |
|-----|-------------|
| RP1 | Confirm both partners consent to non-clinical coaching and data sharing. |
| RP2 | Define session scope and boundaries (topics allowed, off-limits items like past trauma clinical treatment). |
| RP3 | Check for active safety concerns or domestic violence; if present, escalate to appropriate services. |
| RP4 | Data privacy plan for session notes and agreements. |
| RP5 | Collect existing relationship documents (prenup, previous agreements). |
| RP6 | Determine communication preferences and triggers. |
| RP7 | Timeline and decision authority (who signs agreements). |
| RP8 | Exclude clinical therapy; recommend licensed therapists when indicated. |

## Iterative Research Loop
| Loop | Goal | Inputs | Output |
|------|------|--------|--------|
| Loop 0 | Intake & risk triage | Consent, safety screen, top conflicts | Triage report & recommended next step |
| Loop 1 | Communication mapping | Observation of bids, fight patterns | Bid-response scripts & repair plan |
| Loop 2 | Attachment strategy | Attachment style assessments, history | Personalized secure-attachment interventions |
| Loop 3 | Governance & agreements | Financial/household data | Partnership agreement draft & review plan |

## Quickstart (30s deliverable)
1. Ask both partners for top 3 relationship pain points and a recent conflict example.  
2. Run quick bid-for-connection audit (who bids, how responded).  
3. Output: 1-page "Repair and Next Steps" with 3 micro-interventions (softened startup script, repair attempt script, check-in schedule).

<!-- STANDARD: 3min -->
## Ground Rules
- Mechanical triggers:
  - If coercive control or violence suspected: stop and refer to safety services.
  - If legal questions (custody, divorce) appear: recommend legal counsel.
- Negative constraints:
  - Do NOT provide clinical diagnosis or licensed therapy.
  - Do NOT perform forensic or legal arbitration.

## Decision Tree (detailed ASCII)
Start
|-- Safety concerns? -- Yes -> Safety protocol & refer
|                     |-- Immediate: secure safety plan, provide resources, recommend legal action where necessary
|
|-- No -> Intake & Pattern Mapping
    |-- Communication audit
        |-- Low bid-response -> Teach bid-recognition, daily micro-bids, and positive reinforcement schedule
        |-- High reactivity -> Teach down-regulation rituals, implement 10-minute timeout ritual, and use signal words
        |-- Frequent repair failures -> Introduce immediate 3-step repair script and test in low-stakes environment
        |-- Perpetual conflict -> Value-mapping session; classify problem as 'perpetual' or 'solvable'
            |-- Solvable -> Build negotiation plan, assign actions and accountability
            |-- Perpetual -> Create management plan: rituals, acceptance language, and compartmentalization rules
    |
    |-- Attachment flags present?
        |-- Anxious patterns -> Safety experiments, explicit reassurance scripts, and scheduled check-ins
        |-- Avoidant patterns -> Low-demand conversations, autonomy contracts, and slow exposure to intimacy tasks
        |-- Disorganized/high-distress -> Recommend clinician triage; use safety-focused pacing in the interim

Decision branching notes:
- At every branching, include an "escalate to clinician/legal" flag when safety or legal issues are detected.
- Route persistent non-adherence of micro-experiments (2 failed 2-week trials) to a structured behavior-change protocol with measurement.

## Core Workflow
STANDARD: Intake & Triage
1. Consent & safety screen
2. Collect conflict logs (3 months) and communication samples
3. Prioritized list of solvable vs perpetual problems

STANDARD: Communication Tools
- NVC templates: observation -> feeling -> need -> request
- Gottman "softened startup" template and repair attempt script
- Bid-for-connection audit: frequency and responses

<!-- DEEP: 10+min -->
DEEP: Attachment Integration & Failure Modes
- War story: a couple presented with recurring withdrawal after small critiques; mapping showed one partner's avoidant history from childhood and the other's anxious hyperactivation. Early "fixes" (more reassurance) increased clinginess and pushed the avoidant partner further away. Intervention: a staged safety experiment where the anxious partner practiced self-soothing and the avoidant partner agreed to two short post-conflict check-ins per week. Over 8 weeks, bids for connection rose by 40%.
- Edge case: unresolved trauma beneath attachment presentations—standard coaching plateaus; require clinician handoff with shared short-term coaching protocols to avoid regression.
- Practical scripts: regulated disclosure prompt ("When I felt X, I wanted Y"), safe-experiment calendar, and weekly debrief form. Include measurable metrics (bid rate, successful repairs per week).
- Failure narrative: over-prescription of exercises leads to "drill fatigue"; rotate interventions and limit practice to 3 times/week.

<!-- DEEP: 10+min -->
DEEP: Repair Attempts & Micro-practices
- Failure narrative: couples using scripted repairs verbatim without attunement — partners reported robotic exchanges and showed no emotional shift. Fix: teach the intent behind scripts, encourage personalization, and practice tone and timing in role plays.
- Checklist for high-quality repair: (1) Acknowledge impact in one sentence, (2) Offer a brief corrective action, (3) Ask for repair acceptance, (4) Schedule a mini-check-in within 24 hours.
- War story: a delayed repair (24+ hours) after a major fight failed repeatedly; instituting immediate micro-repair (one-sentence apology + small concrete fix) prevented escalation in future cycles.

<!-- DEEP: 10+min -->
DEEP: Partnership Agreements & Failure Case Studies
- Example agreement clause: "Division of labor table with 8 core household tasks, expected weekly time, primary owner, and backup. Quarterly review with reallocation if burden >15%."
- Failure story: a financial agreement that lacked emergency rules caused a dispute when an unexpected medical bill drew from shared funds; fix included an emergency fund clause with a $5,000 threshold requiring joint approval for withdrawals above $1,000.
- Edge cases: cross-border financial assets, family-owned businesses, and complex estate plans—insert legal review steps and map signatory authority.

<!-- DEEP: 10+min -->
DEEP: Conflict Pattern Catalog (Real conflict archetypes)
- The "Perpetual Values Clash": disputes about core beliefs (child-rearing, religion). Strategy: value-mapping, agree to disagree rituals, and compartmentalized problem zones.
- The "Resource Fight": money and time scarcity. Strategy: transparent budgets, shared dashboards, and small, measurable allocations.
- The "Third-Party Trigger": in-laws or friends causing recurring fights. Strategy: boundary contracts and joint-navigational scripts.
- Each archetype includes a 6-step response playbook and sample script set.

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
|-------------------------|------------|-----|--------|
| "We keep repeating the same fight" | Perpetual problem misdiagnosed as solvable | Reclassify, accept differences, build gridlock plan with softening rituals | Not all problems are solvable — manage, don't fix |
| "Partner shuts down" | Attachment avoidance or high arousal | Use scheduled low-demand check-ins, sensory grounding before deep talk | Safety and pacing matter more than topic |
| "Repair attempts fail" | Repair attempts not recognized or too late | Teach immediate short repair scripts and timeouts | Immediate micro-repairs reset escalation |
| "Scripts feel robotic" | Over-rehearsal without emotional attunement | Personalize scripts, role-play tone and timing, reduce frequency | Intention matters more than wording |
| "Division-of-labor ignored" | Vague responsibilities and no review cadence | Insert measurable quotas, calendar assignments, and quarterly review | Concrete assignments + review avoid buildup of resentment |
| "Escalation via 3rd party" | Boundary breakdown (in-laws, exes) | Create joint boundary script and escalation ladder; rehearse neutral phrases | External actors need scripted handling to avoid re-triggering partners |
| "Safety language not recognized" | Partners do not honor agreed safety protocols | Re-train on emergency words and response steps; re-document plan | Safety protocols must be practiced to be effective |

## Best Practices
1. Start with bids: measure bid frequency and responses; intervene when bid response rate < 50% over 2 weeks.
2. Use softened startups for critique: observation + feeling + request; limit critique to one issue per interaction.
3. Script and rehearse repairs; keep repair attempts under 30 seconds and follow with a small corrective action.
4. Make agreements concrete and measurable: assign tasks in calendars with estimated weekly time budgets.
5. Hold a monthly 'State-of-the-Union' meeting with a 30-minute timed agenda and one unresolved issue per meeting.
6. Teach and practice emotion regulation skills: 4-7-8 breathing, short grounding exercises, and a 10-minute cooling protocol.
7. Use time-boxed experiments (2-week trials) with pre-agreed metrics and owner responsibilities.
8. Keep financial transparency simple: shared ledger for core expenses and a 90-day rolling forecast for known large items.
9. Protect third-party boundaries with pre-written scripts and a rehearse-and-roleplay protocol.
10. Create an emergency fund clause and explicit withdrawal rules for shared finances to avoid surprise conflicts.

## Production Checklist
- [ ] Consent and safety screen completed and stored
- [ ] Bid-for-connection audit completed (2-week sample)
- [ ] Priority conflict list (solvable vs perpetual) created
- [ ] One-page partnership compact drafted and agreed in principle
- [ ] Division-of-labor matrix populated in shared calendar
- [ ] Financial transparency ledger created and shared
- [ ] Repair script bank delivered and practiced in role-play
- [ ] Monthly check-in schedule created and calendar invites sent
- [ ] Escalation ladder documented (mediator contacts, legal referral)
- [ ] 30-day follow-up check-in scheduled and owner assigned

## Verification
- 30-day follow-up: partners report at least one successful repair.
- Check-in logs show reduced reactivity (self-reported calming within 5–10 minutes).
- Agreement: at least 80% adherence to division-of-labor tasks after 1 month.

## Cross-Skill Coordination
| Skill | When to call | Inputs | Outputs |
|-------|--------------|--------|---------|
| parenting-strategist | When parenting inconsistency appears | Partnership agreement, custody notes | Coherent parenting plan and alignment scripts |
| legal-advisor | If legal questions arise | Financial agreements | Referral and contract clauses |
| mindfulness-practitioner | For regulation skills | Stress profiles | Grounding routines and meditations |

## What Good Looks Like
- Partners use softened startups for critiques and make repair attempts within 5 minutes of escalation.
- A written partnership agreement exists and is referenced during disputes.
- Monthly check-ins are held and produce at least one agenda item resolved per meeting.

## References
- Gottman, J., & Gottman, J. (2015). The Seven Principles for Making Marriage Work. Crown Publishing.
- Rosenberg, M. B. (2003). Nonviolent Communication: A Language of Life. PuddleDancer Press.
- Bowlby, J. (1969). Attachment and Loss. Basic Books.
- Ainsworth, M. D. S. et al. (1978). Patterns of Attachment. Lawrence Erlbaum.
- Brown, B. (2018). Dare to Lead (BRAVING framework). Random House.
- Johnson, S. (2008). Hold Me Tight: Seven Conversations for a Lifetime of Love. Little, Brown Spark.
- Gottman Institute research papers and clinical summaries (visit gottman.com for assessment tools and bid metrics).

## Scale Depth
Solo (individual practitioner):
- Output: one-session triage, repair-script, and a 2-week practice assignment.
- Tools: shared Google Doc, simple calendar invites, and a habit-tracking sheet.
- Trigger to scale: repeated lack of repair within 2 weeks or safety/legal flags.

Small practice (1–3 practitioners):
- Team: 1 lead coach + 1 junior coach, with referral partners (therapist, mediator).
- Output: 6–12 week coaching with weekly practice, bid audits, and progress metrics.
- Tools: Notion templates, Zoom + recorded role-plays (with consent), simple CRM (Airtable).
- Trigger: client complexity (finance, custody, or legal matters) or cohort delivery demand.

Medium (group, clinic):
- Team: 3–8 facilitators, intake coordinator, and clinical partner for referrals.
- Output: multi-family cohorts, facilitator training, standardized assessment tools.
- Tools: SimplePractice for scheduling/notes, LMS for facilitator modules, Miro for value mapping.
- Trigger: demand for training packages or employer/insurer contracts.

Enterprise (organizational programs):
- Team: program director, training manager, multiple regional teams, legal/compliance support.
- Output: relationship health programs integrated with employee assistance or family services.
- Tools: HubSpot CRM, enterprise LMS, analytics dashboards, standardized reporting and quality assurance.

## Concrete Frameworks
Repair Attempt Rule
- A repair attempt must occur within 20 minutes of escalation if both parties are present; if not, a time-boxed "pause and reconnect" step is required within 24 hours.
- Micro-repair template: 1-sentence acknowledgement + 1 concrete fix + 1 minute of validation. Example: "I didn't mean to dismiss that; I'll text you once I arrive next time so you know I'm leaving work early."

Bid Response Target
- Target: respond to partner's bids for connection at least 60% of the time over a rolling 2-week period. Track with a simple bid-log spreadsheet.

Division-of-Labor Matrix (sample numbers)
- Home: 8 tasks x estimated weekly hours: total household hours 18/week. Aim for no person >60% of total unless agreed and compensated.
- Financial: designate one primary bill-payer and one secondary reviewer with monthly reconciliation.

## Anti-Hallucination
- [VERIFIED] Gottman and NVC frameworks are widely used and documented.
- [COMMON-PRACTICE] Using specific time-boxed repairs increases successful de-escalation in observational work.
- [INFERRED] 60% bid response target is operational and should be adapted to culture and context.
- [UNKNOWN] Legal enforceability of partnership compacts varies; seek local counsel where legal certainty is desired.
