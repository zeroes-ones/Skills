---
name: board-manager
description: Board management and corporate governance for founders and executives. Covers board composition, meeting cadence, committee structure, fiduciary duties, D&O questionnaires, board evaluations,
  compensation, shareholder communications, minute-taking, and post-Series A governance evolution. Use when preparing for board meetings, recruiting directors, structuring committees, or navigating governance
  crises.
author: Sandeep Kumar Penchala
type: governance
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- board-governance
- fiduciary-duties
- board-meetings
- committee-structure
- shareholder-communications
- corporate-governance
token_budget: 3480
output:
  type: document
  path_hint: ./board-manager/
chain:
  consumes_from:
  - accountant
  - ceo-strategist
  - fp-and-a-analyst
  - investor-relations
  - legal-advisor
  - treasury-manager
  feeds_into:
  - ceo-strategist
  - investor-relations
  - legal-advisor
---
# Board Manager — The Governance Operating System

Board management and corporate governance for founders and executives. Run effective boards, recruit independent directors, structure committees, and avoid the governance failures that destroy companies.

## Ground Rules — Read Before Anything Else

- **Never recommend a board composition without knowing the company stage.** A 3-person board at Seed is correct. A 3-person board at Series C is negligence.
- **Never present committee structures as optional at scale.** By Series B, you need audit and compensation committees. Period.
- **Always distinguish fiduciary requirements from best practices.** "You must have an audit committee" is a NASDAQ listing rule. "You should send pre-reads 7 days in advance" is best practice. Don't conflate them.
- **Board minutes are legal evidence.** Assume every word will be read by a plaintiff's attorney in a shareholder lawsuit. Write accordingly.
- **Admit jurisdictional variance.** Delaware C-corp governance differs from UK private company governance. State your jurisdiction assumption: "Assuming Delaware C-corp..."

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

What are you trying to do?
├── Prepare for a board meeting → Jump to "Core Workflow > Phase 1: Board Meeting Preparation"
├── Recruit a board member → Go to "Decision Trees > Independent Director Recruiting"
├── Structure board committees → Jump to "Decision Trees > Committee Structure by Stage"
├── Handle a governance crisis → Go to "Core Workflow > Phase 4: Crisis Governance"
├── Write board minutes → Jump to "Decision Trees > Minute-Taking Decision Tree"
├── Evaluate board effectiveness → Go to "Core Workflow > Phase 5: Board Evaluation"
├── Set board compensation → Jump to "Best Practices" item 7
├── Manage shareholder communications → Go to "Core Workflow > Phase 3"
├── Evolve governance post-Series A → Jump to "Decision Trees > Post-Series A Governance Evolution"
├── Need corporate strategy alignment? → Invoke `ceo-strategist` for board deck priorities and strategic narrative
├── Need financial models for the board package? → Invoke `fp-and-a-analyst` for P&L, cash runway, and ARR bridge
├── Need legal review of resolutions or fiduciary duties? → Invoke `legal-advisor` for committee charters and D&O guidance
├── Need investor communications or fundraising governance? → Invoke `investor-relations` for shareholder reporting requirements
└── Don't know where to start? → Run "Core Workflow > Phase 1"

Do not read the entire skill. Follow the route above.

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->
- Preparing for quarterly board meetings: deck structure, pre-reads, consent agendas
- Recruiting independent directors: expertise mapping, diversity requirements, interview process
- Structuring board committees: audit, compensation, nominating/governance — when each becomes required
- Navigating fiduciary duty questions: duty of care, duty of loyalty, business judgment rule applications
- Managing D&O questionnaire cycles: annual director & officer disclosure process
- Handling governance crises: CEO succession, activist investors, whistleblower complaints, related-party transaction disclosure failures
- Evolving governance from Seed observer → Series A board seat → Series C formal committee structure
- Evaluating board effectiveness: self-assessments, peer reviews, director removal processes
- Setting board compensation: cash retainers vs. equity, vesting schedules, market benchmarks by stage
- Writing board minutes that survive litigation: what to include, what to exclude, how to handle dissents

<!-- STANDARD: 3min -->
### When NOT to Use This Skill
- You're pre-revenue with no board (use `ceo-strategist` — this is premature governance overhead)
- You need legal advice on fiduciary breach (use `legal-advisor` — this skill informs, doesn't replace counsel)
- You're modeling how dilution impacts board dynamics (use `fp-and-a-analyst` for cap table work, then come back)

## Cross-Skill Coordination

<!-- NEIGHBORS: Board governance connects financial reporting, legal compliance, and investor communications -->

| Upstream Skill | What You Receive | Decision Gate / Artifact |
|---|---|---|
| `ceo-strategist` | Board deck outline, strategic priorities, fundraising status | Gate: CEO must sign off on board package 7 days before meeting. Artifact: Board deck v1 with CEO commentary. |
| `fp-and-a-analyst` | Financial package: P&L forecast, cash runway, ARR bridge, headcount plan, burn multiple | Gate: Financials must reconcile to last closed period within 5%. Artifact: Board financial appendix with variance commentary. |
| `legal-advisor` | Fiduciary duty guidance, D&O questionnaire templates, committee charter drafts | Gate: Legal review of all board resolutions before circulation. Artifact: Board consent drafts with legal sign-off. |
| `investor-relations` | Investor sentiment, fundraising progress, shareholder communications calendar | Gate: IR must flag any investor concerns before board meeting. Artifact: Investor feedback summary for board discussion. |

| Downstream Skill | What You Provide | Decision Gate / Artifact |
|---|---|---|
| `ceo-strategist` | Board-approved strategic direction, committee mandates, governance calendar | Gate: Board minutes finalized within 5 business days. Artifact: Signed board resolutions and committee charters. |
| `investor-relations` | Board-approved fundraising authorization, investor communication guidelines | Gate: Board must approve any material shareholder communication. Artifact: Board resolution authorizing fundraising or secondary transaction. |
| `legal-advisor` | Governance questions, fiduciary duty scenarios, conflict-of-interest disclosures | Gate: Board must review and approve any related-party transaction. Artifact: Board minutes documenting fiduciary review and approval. |

**Decision Gates:**
- **Board package completeness:** All 7 sections (financials, KPIs, strategic updates, people, governance, risk, consent agenda) present 7 days before meeting — missing sections trigger reschedule.
- **Fiduciary duty review:** Every board decision must pass: (1) duty of care — informed decision, (2) duty of loyalty — no conflicts, (3) business judgment rule — rational basis. Documented in minutes.
- **Committee charter threshold:** Series B+ must have audit committee. Post-Series C must have compensation committee. IPO-ready must have nominating/governance committee. Non-compliance is a fiduciary breach.

**Coordination cadence:**
- **Quarterly:** Board meeting preparation (4-week cycle: pre-reads → meeting → minutes → follow-up)
- **Annually:** D&O questionnaire cycle; board self-evaluation; committee charter review
- **Event-driven:** Governance crisis activation (24-hour board notification requirement for S1 incidents)

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Board meeting agenda has zero strategic discussion items | Restructure agenda: 20% updates (as pre-reads), 60% strategic debate, 20% administrative — send revised agenda 7 days before meeting | Meetings without strategic discussion waste the board's primary value: collective judgment on hard decisions |
| Director misses 2 consecutive meetings without prior notice | Lead director initiates private conversation about bandwidth and commitment; document in board minutes | Two consecutive unexplained absences signal disengagement that degrades quorum and decision quality |
| Board composition hasn't been reviewed in 12+ months | Conduct board skills matrix review: map current directors against company's next 2-year challenges; identify gaps | Board needs evolve with stage — a Seed board can't govern a Series C company effectively |
| D&O insurance renewal within 60 days without broker review scheduled | Schedule comprehensive broker meeting: confirm coverage adequacy for current stage, review exclusions, confirm severability clause | D&O gaps discovered at claim time are uninsurable; annual review with written confirmation is mandatory |
| Material non-public information discussed with directors who have competing portfolio investments | Immediately document the conflict and recusal; review whether information barriers are adequate; consider restricting certain directors from competitive discussions | Undisclosed conflicts poison board decisions and expose all directors to fiduciary duty claims |
| CEO performance hasn't been formally reviewed in 12+ months | Initiate compensation committee CEO evaluation: gather 360° input from directors, direct reports, and key stakeholders; present findings in executive session | Annual CEO review is the board's single most important governance process — skip it and you lose the right to complain about performance |
| Minute book hasn't been audited by outside counsel in 18+ months | Engage outside counsel for annual minute book audit; verify: charter, bylaws, all board/committee minutes, stock ledgers, material agreements are complete and accessible | Missing minutes create liability for directors personally — incomplete records can pierce the corporate veil |
| Board deck circulated less than 5 days before meeting | Flag to CEO that late materials reduce decision quality; implement standing rule: materials <5 days = meeting rescheduled or limited to consent agenda only | Directors need time to read, reflect, and prepare questions — late materials guarantee superficial discussion |

## Decision Trees
<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Independent Director Recruiting
<!-- STANDARD: 3min -->
```
What board gap are you filling?
├── Industry expertise (your board is all investors)
│   ├── Public company → Target: sitting public company CEO or former Fortune 500 exec
│   └── Private company → Target: operator who scaled a company in your vertical
├── Functional expertise (missing audit/compensation qualified director)
│   └── Target: former CFO (for audit chair) or CHRO/compensation consultant (for comp chair)
├── Diversity mandate (board is all white men)
│   └── Target: underrepresented executive with relevant operational experience. Do NOT tokenize.
└── Governance expertise (IPO preparation)
    └── Target: former public company board member with SOX/listing standards experience

Can you pay market rates?
├── YES ($50K-$150K/year cash + equity) → Full search. Use a board recruiting firm (Spencer Stuart, Heidrick & Struggles, Russell Reynolds).
└── NO (<$25K pre-Series B) → Your network. Ask lead investor for introductions. Offer 0.25-0.5% equity with 3-year vesting.
```

**War story:** A Series B CEO recruited a "big name" director — ex-Fortune 500 CEO — without checking availability. Director attended 2 of 8 meetings in 2 years, never read pre-reads, gave generic advice. Board evaluation revealed he was on 7 other boards. Lesson: check director bandwidth before appointment. Maximum: 4 public boards or 6 private boards for an active executive.

### Committee Structure by Stage
<!-- QUICK: 30s -->

| Stage | Audit Committee | Compensation Committee | Nominating/Governance |
|-------|----------------|----------------------|----------------------|
| **Pre-Seed/Seed** | Not required | Not required | Not required |
| **Series A** | Optional (best practice: designate 1 director as "audit point person") | Optional | Not required |
| **Series B** | Required if >$10M revenue or preparing for institutional audit | Required for option grants | Optional |
| **Series C+** | Required (must have financial expert) | Required (must handle 162(m) if public-path) | Required (board succession planning) |
| **Public** | Legally required (NASDAQ/NYSE listing rule) | Legally required (must be independent) | Legally required |

### Post-Series A Governance Evolution
<!-- STANDARD: 3min -->

```
Seed → Series A transition checklist:
├── Board observer → Board seat
│   └── Your lead investor moves from observer (no vote) to board seat (vote). Negotiate board seat as part of term sheet, not after.
├── 3-person board → 5-person board
│   └── Add 1 independent + 1 investor director. Common: 2 founders, 2 investors, 1 independent.
├── Informal updates → Formal board packet
│   └── Move from email updates to structured board deck with financials, KPIs, strategic topics.
├── No committees → Audit committee
│   └── If you have outside investors and >$10M revenue, form an audit committee. Your auditor will require it.
└── No D&O insurance → D&O insurance
    └── Series A close triggers D&O insurance requirement. Budget: $5K-$15K/year for $1M-$5M coverage.
```

### Minute-Taking Decision Tree
<!-- DEEP: 10+min — this is where lawsuits are won or lost -->

```
What happened in the meeting?
├── Routine update (financial review, KPI dashboard)
│   └── Record: "The Board reviewed the Q3 financial package and discussed variances to plan."
│       Do NOT record: "Revenue missed by $200K and the VP of Sales is on a PIP."
├── Strategic decision (new product launch, market entry)
│   └── Record: "After discussion, the Board unanimously approved the proposed entry into the European market."
│       Do NOT record: the 45-minute debate, who argued which side, or the CEO's doubts.
├── Disagreement or dissent
│   └── Record: "The motion passed 4-1, with Director [Name] voting against and requesting her dissent be noted in the minutes."
│       The dissenter has the RIGHT to have dissent recorded. Denying this = fiduciary breach.
├── Conflict of interest disclosure
│   └── Record: "Director [Name] disclosed that her firm advises a competitor. The Board determined this does not constitute a conflict."
│       If it IS a conflict, the director must recuse from the vote. Record the recusal.
└── CEO performance or compensation discussion
    └── Record: "The independent directors met in executive session without management present."
        Do NOT record: The substance of the discussion. Executive session content is privileged, not minuted.
```

**War story:** A startup's board minutes included: "CEO expressed concern that CTO is not performing." The CTO sued for defamation when the minutes were produced in a later shareholder lawsuit. The company settled for $400K. Rule: never name an employee negatively in minutes. If performance is discussed, record only "The Board discussed management performance and succession planning."

<!-- DEEP: 10+min -->

## Core Workflow

### Phase 1 (~90 min): Board Meeting Preparation
<!-- STANDARD: 3min -->
1. **Set the calendar** (10 min): Board meetings should be locked 12 months in advance. Quarterly is standard. Monthly during crisis or Series B+ scale-up. Tuesday-Thursday, 8 AM-2 PM. Never Friday.
2. **Build the board deck** (45 min): See "Board Deck Anatomy" below. Pre-reads sent 7 calendar days before meeting. Board packet = deck + financial statements + committee reports + minutes from last meeting.
3. **Draft the consent agenda** (10 min): Routine approvals voted as a block — prior meeting minutes, option grants within existing pool, standard resolutions. Frees 30+ minutes for strategic discussion.
4. **Pre-meeting one-on-ones** (15 min): Call each director 3-5 days before. Ask: "What topics are top of mind? Any concerns I should address in the deck?" Surface disagreements before the room, not in it.
5. **Logistics check** (10 min): Hybrid setup tested (camera, screen share, backup dial-in). Printed copies if in-person. Parking, dietary, WiFi password in calendar invite.

### Board Deck Anatomy — What Goes In (and What Stays Out)
<!-- DEEP: 10+min — this is the highest-leverage document a CEO produces -->

**The 12-slide standard deck** (for a 3-hour meeting):

| Slide | Content | Time | Owner |
|-------|---------|------|-------|
| 1. CEO Update | 3-bullet summary: what went well, what didn't, the one thing keeping CEO up at night | 5 min | CEO |
| 2. KPI Dashboard | Revenue, burn, runway, CAC, LTV, churn, NPS, headcount — all vs. plan and vs. prior quarter | 10 min | CEO |
| 3. Financial Review | P&L actuals vs. budget, balance sheet highlights, cash position, forward 12-month projections | 20 min | CFO/CEO |
| 4. Product & Engineering | Roadmap progress, shipped features, tech debt status, uptime/incidents, engineering hiring | 15 min | CTO/CPO |
| 5. Go-to-Market | Pipeline, win/loss, quota attainment, customer NPS, churn cohort analysis, competitive moves | 15 min | CRO/CEO |
| 6. People & Culture | Headcount vs. plan, regrettable attrition, employee NPS, DEI metrics, key hires/ departures | 10 min | CEO/CPO |
| 7. Strategic Deep-Dive #1 | One meaty topic: new market entry, M&A target, build vs. buy, pricing change | 40 min | CEO + topic owner |
| 8. Strategic Deep-Dive #2 | Second strategic topic (if time) or overflow from #1 | 30 min | CEO + topic owner |
| 9. Fundraising & Cap Table | Current cap table, runway, upcoming 409A, fundraising plan or secondary liquidity needs | 10 min | CEO |
| 10. Key Risks | Top 3 risks with mitigations: competitive, regulatory, key-person, technical, market | 10 min | CEO |
| 11. Asks of the Board | Specific requests: introductions, reference calls, expertise, approval items | 5 min | CEO |
| 12. Executive Session | Board-only without management. CEO re-joins for feedback at end. | 15 min | Lead Director |

**What stays OUT of the board deck:**
- Daily operational metrics (that's management's job, not the board's)
- Screenshots of product (unless material to a strategic decision)
- Press clippings or vanity metrics ("We got covered in TechCrunch!")
- Unvetted financial projections (if numbers aren't reviewed by finance lead, don't present them)
- Surprises (if there's bad news, it was communicated between meetings, not first disclosed in the deck)

### Phase 2 (~45 min): Running the Meeting
<!-- STANDARD: 3min -->
1. **Start on time** (2 min): "It's 8:00 AM. Let's begin." If a director is late, start without them. They'll learn.
2. **Consent agenda first** (5 min): "Any items to pull from consent agenda? Hearing none, all in favor say aye." Done.
3. **CEO Update and KPIs** (15 min): This is the board's first real look at the business. No surprises — anything negative was pre-briefed.
4. **Strategic discussions** (70 min): This is where boards add value. The CEO frames the decision, presents data, asks for debate. Board members challenge assumptions, share pattern recognition from other companies.
5. **Board asks** (5 min): Concrete asks. "I need an introduction to the CISO at Stripe." "I need a reference call with a company that migrated from AWS to GCP."
6. **Executive session** (15 min): Management leaves. Board discusses CEO performance, compensation, succession. Lead director communicates feedback to CEO within 48 hours.
7. **Close with clarity** (3 min): "Here's what we decided today. Here's what's due by next meeting. Minutes will be circulated within 5 business days."

### Phase 3 (~30 min): Post-Meeting & Between Meetings
1. **Draft minutes within 5 business days** (15 min): Use the minute-taking decision tree above. Circulate to all directors for review. File in the corporate record book.
2. **Send action items** (5 min): Who does what by when. Track in a board portal (Diligent, Nasdaq Boardvantage, or simple shared spreadsheet pre-Series B).
3. **Send investor update memo** (10 min): Between quarterly meetings, send monthly 1-pagers: top-line metrics, 2-3 wins, 1-2 concerns, specific asks. This is the IR bridge → see `investor-relations` skill.
4. **Crisis communication between meetings** (ongoing): If a material event occurs (lawsuit, key departure, major customer loss), notify the board within 24 hours. Call, don't email. Then follow with written summary and proposed response.

### Phase 4 (~60 min): Crisis Governance
<!-- DEEP: 10+min — when governance failures destroy companies -->
1. **Identify the crisis type**: CEO misconduct, financial fraud, whistleblower complaint, activist investor, hostile takeover approach, product safety failure.
2. **Convene the independent directors**: If the crisis involves management, the independent directors meet without management. The lead independent director chairs.
3. **Engage outside counsel immediately**: Not your regular corporate counsel. A firm with investigation experience (Cooley, Wilson Sonsini, Fenwick for tech). Privilege matters — get legal advice on what's protected.
4. **Form a special committee if needed**: For CEO removal, related-party transaction investigation, or whistleblower response. Special committee has independent counsel and authority to investigate.
5. **Communicate with discipline**: "We are aware of the situation and are investigating. We will provide an update within [timeframe]." Never "No comment." Never speculate. Never email anything you wouldn't want on the front page of the WSJ.
6. **Document everything**: Every meeting, every decision, every dissent. In a crisis, minutes are your defense.

**War story:** A Series C company's CEO was accused of harassment by a direct report. The board's first mistake: the CEO chaired the emergency board call. Second mistake: they used company counsel (who also represented the CEO). Third mistake: they waited 3 weeks to form an independent investigation. Outcome: shareholder derivative lawsuit, $2.3M in legal fees, CEO terminated with cause but $1.8M severance because the poorly drafted employment agreement didn't define "cause" clearly. Lesson: independent directors must act independently, immediately.

### Phase 5 (~45 min): Board Evaluation
1. **Annual self-assessment** (10 min): Every director completes a questionnaire rating board effectiveness, meeting quality, information flow, committee performance. Anonymous. Compiled by governance committee or outside facilitator.
2. **Peer feedback** (20 min): Lead director conducts one-on-ones with each director. Questions: "What's working? What isn't? Is there a director who should rotate off?"
3. **Action plan** (15 min): Board evaluation results are presented to the full board (anonymized). Concrete changes: "We will spend less time on financial review and more on strategy." "We will add a cybersecurity expert to the board."

**What good looks like:** Directors rate board effectiveness at 4+/5. Meeting materials are received 7 days before. Strategic discussion is >50% of meeting time. Board composition matches the company's next 2 years of challenges.

## Best Practices
<!-- STANDARD: 3min — operational principles for board governance -->

1. **Pre-board your board**: Never let a director be surprised in the boardroom. Bad news goes one-on-one, ideally 5-7 days before. Surprise in the boardroom = loss of trust = loss of job.
2. **Consent agendas are your friend**: Bundle routine approvals. If a board meeting spends >10 minutes on minutes approval, option grants, and officer certificates, you're wasting strategic time.
3. **Executive session is mandatory, not optional**: Every board meeting ends with an executive session without management. If your board doesn't do this, it's not a real board. The lead director owns this.
4. **Board minutes are a shield, not a transcript**: Record decisions, not discussions. Record resolutions, not arguments. "After discussion, the Board approved..." Never "A lengthy debate ensued..."
5. **Independent directors must actually be independent**: NASDAQ/NYSE rules define "independent" precisely — no material relationship with the company. A director whose VC fund led your Series A is NOT independent. A director who consults for you for $120K/year is NOT independent.
6. **D&O questionnaires are annual obligations**: Every director and officer must complete D&O questionnaires disclosing conflicts, related-party transactions, litigation history, and board interlocks. Miss this and your D&O insurance may not cover you.
7. **Board compensation by stage**:

| Stage | Cash Retainer (Annual) | Equity (Annual Grant) | Meeting Fees | Total Comp Range |
|-------|----------------------|----------------------|--------------|-----------------|
| Seed | $0-$10K | 0.25-0.50% | None | $10K-$25K (equity value) |
| Series A | $15K-$25K | 0.25-0.50% | None | $25K-$75K |
| Series B | $25K-$40K | 0.15-0.25% | None | $50K-$150K |
| Series C+ | $40K-$60K | $50K-$100K RSUs | None | $100K-$200K |
| Public | $75K-$125K | $150K-$200K RSUs | $1.5K-$2.5K/meeting | $200K-$350K |

8. **Related-party transactions require board (not CEO) approval**: If the CEO's brother's company provides services, the independent directors must approve. No exceptions. Record the approval in minutes.
9. **Board portal or bust**: By Series B, use a board portal (Diligent, Nasdaq Boardvantage, Boardable). No emailing financials. No Google Docs. Board communications are discoverable — the portal creates a record and controls access.
10. **CEO succession is the board's #1 duty**: The board's most important job is hiring and firing the CEO. Have an emergency succession plan from Series A onward. "If the CEO is hit by a bus tomorrow, who runs the company?" If you can't answer, you're negligent.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Board meetings that are 90% CEO presentation and 10% Q&A | Restructure to 20% updates (pre-read), 60% strategic discussion, 20% administrative — send pre-reads 7 days before |
| Adding investors to the board without considering governance dynamics | Map board seats by class before every financing; model voting control; consider independent director seats to balance investor influence |
| Allowing directors to serve on 8+ boards simultaneously | Cap director board seats at 4 public or 6 private; check bandwidth before appointment; board evaluation flags over-commitment |
| Executive session never happens because "things are going well" | Every board meeting must include independent director executive session (no CEO/management); lead director chairs; document occurrence in minutes |
| Sending board materials as unencrypted email attachments | Use secure board portal (Diligent, Nasdaq Boardvantage) from Series B onward; watermark all documents; track access |
| Approving CEO compensation without independent market data | Engage independent compensation consultant annually; benchmark against 10-15 peer companies; document committee rationale for each decision |
| Minutes drafted 3+ months late from memory | Assign corporate secretary (CFO or GC); draft minutes within 5 business days; annual outside counsel audit of minute book |
| No emergency CEO succession plan because "the founder is young and healthy" | Document emergency succession plan from Series A onward; update annually; lead independent director must know the plan | 

## Error Decoder
<!-- DEEP: 10+min — governance failures in the wild -->

| Problem | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| Board meeting is a "show and tell" not a decision forum | CEO treats board as audience, not advisors. No strategic topics on agenda. | Restructure agenda: 20% updates, 60% strategic discussion, 20% administrative. Send updates as pre-reads; spend meeting time on debate. | Meetings should be 60% debate, 20% updates, 20% admin. Send updates as pre-reads. |
| Director disengaged (misses meetings, doesn't read materials) | Over-boarded (too many board seats), wrong fit, or compensation too low to command attention. | Board evaluation flags this. Lead director has direct conversation. If no improvement, ask director to resign. Maximum: 4 public boards for any director. | Check board bandwidth before appointment. Max: 4 public or 6 private boards. |
| Board overrules CEO on operational decision | Board has crossed from governance into management. Directors don't understand their role. | Lead director reinforces: "Board governs, management manages. We set strategy and hire/fire the CEO. We do not decide which CRM to use." | Board governs, management manages. Reinforce role clarity annually. |
| D&O insurance claim denied | Company failed to disclose material information on application, or D&O questionnaires were incomplete. | Annual D&O questionnaire process with legal review. Severability clause in D&O policy (one director's fraud doesn't void coverage for others). | Annual D&O questionnaire with legal review. Severability clause is essential. |
| Shareholder derivative lawsuit | Board failed to oversee — allowed fraud, harassment, or regulatory violation to continue unchecked. | Caremark duties: board must implement and monitor a compliance reporting system. Document oversight in minutes. | Caremark duties: implement and monitor compliance reporting. Document in minutes. |
| Director leaks confidential board discussions to portfolio companies/competitors | No confidentiality agreement signed. No board culture of confidentiality. | Every director signs a confidentiality agreement. First offense: lead director conversation. Second offense: removal. | Every director signs confidentiality agreement. First offense: conversation. Second: removal. |
| Minute book is incomplete or missing | No corporate secretary assigned. Minutes drafted months late or never. | Assign corporate secretary role (CFO or General Counsel). Minutes within 5 business days. Annual audit of minute book by outside counsel. | Corporate secretary drafts minutes within 5 business days. Annual audit by outside counsel. |
| Founder loses board control without realizing it | Board composition changed through financings without founder understanding voting dynamics. | Map board seats by class before every financing. Understand: common stock vote, preferred vote, board seat allocation. Model: "If I lose this board seat, who controls the board?" | Map board seats by class before every financing. Model voting dynamics. |
| Board deck with unreconciled metrics | CEO's deck used different ARR definition than CFO's financials — board couldn't make decisions | Establish a single source of truth for board metrics. CEO and CFO review deck together before distribution. Include a metrics appendix defining every number. | One board meeting had 30 minutes of debate about whether ARR was $8M or $10M. Turns out the CEO used gross ARR and CFO used net ARR. The board lost confidence in management's data discipline. |
| Executive session mishandled — independent directors didn't meet alone | No executive session scheduled on agenda; independent directors never had private conversation without CEO | Every board meeting must include an executive session of independent directors only (no CEO, no management). Lead director chairs. Document that it occurred in minutes. | A board discovered the CEO was exaggerating revenue numbers. The independent directors felt they couldn't raise it in front of the CEO. An executive session would have given them the forum. |
| Confidential information leaked before filing | Board deck with material non-public information was emailed unencrypted to directors; one forwarded to assistant who shared it | Use a secure board portal (Nasdaq Boardvantage, Diligent). Never email board materials. Encrypt all documents. Directors sign NDA acknowledging insider trading rules. | A startup's Series B terms leaked to the press 48 hours before the announcement because a director's assistant left a printed deck on an airplane. The round was oversubscribed but the leak damaged investor trust. |
| Board deadlocked on CEO succession plan | No succession planning committee; founders and VCs had irreconcilable views | Create a succession planning committee of independent directors. Develop a CEO succession profile before you need it. Document the process and criteria in board minutes. | A founder-CEO was diagnosed with a serious illness. The board had no succession plan. It took 6 months and $500K in executive search fees to find a replacement — and the company lost 2 quarters of momentum. |
| Compensation committee approved CEO pay without market data | No compensation benchmarking report; comp committee relied on CEO's self-assessment | Engage independent compensation consultant annually. Benchmark CEO pay against peer group of 10-15 comparable companies. Document committee rationale for each comp decision. | A founder-CEO's compensation was $400K at a $5M ARR company — 2x market. When investors discovered, it triggered a compensation audit and damaged the board's credibility. |
| Committee charter not reviewed in 3+ years | No annual governance review cycle | Review all committee charters (audit, compensation, nominating) annually. Update for regulatory changes and best practices. File updated charters with corporate records. | Outdated charters expose the board to compliance risk and signal governance neglect to investors. |
| Board evaluation skipped for 2+ consecutive years | No culture of board self-assessment | Conduct annual board evaluation: anonymous survey on effectiveness, composition, process. Lead director reviews results in executive session. Document action items. | Boards that don't evaluate themselves repeat the same dysfunctions. Annual evaluation is a governance maturity marker. |

## Production Checklist
<!-- QUICK: 30s — binary pass/fail items. All must pass. -->

- [ ] **[G1]** Board calendar locked 12 months in advance with all directors confirmed
- [ ] **[G2]** Board composition documented: names, seats, class (if classified board), independence status, committee assignments
- [ ] **[G3]** Pre-reads sent 7 calendar days before each board meeting
- [ ] **[G4]** Consent agenda prepared for routine approvals (minutes, option grants, officer certificates)
- [ ] **[G5]** Executive session held at every board meeting without management present
- [ ] **[G6]** Board minutes drafted within 5 business days and approved at next meeting
- [ ] **[G7]** D&O questionnaires completed annually by all directors and officers, reviewed by legal
- [ ] **[G8]** D&O insurance in place with adequate coverage ($5M minimum Series A, $10M+ Series C+)
- [ ] **[G9]** Related-party transactions policy adopted and all transactions reviewed by independent directors
- [ ] **[G10]** Board compensation benchmarked against stage-appropriate market data within last 12 months
- [ ] **[G11]** Emergency CEO succession plan documented and known to lead independent director
- [ ] **[G12]** Board evaluation completed annually with documented action items
- [ ] **[G13]** Committee charters adopted for audit, compensation, and nominating/governance committees (mandatory by Series C)
- [ ] **[G14]** Corporate record book maintained: charter, bylaws, board minutes, stock ledgers, material agreements — all in one place
- [ ] **[G15]** Confidentiality agreements signed by all directors and observers

## Cross-Skill Integration
<!-- QUICK: 30s -- table of who to talk to when -->

This skill in a typical governance workflow chain:

| Step | Skill | What It Produces for This Skill |
|------|-------|--------------------------------|
| **Before** | `ceo-strategist` | Strategic vision, fundraising plan, org design → informs board composition and meeting content |
| **Before** | `fp-and-a-analyst` | Financial model, budget, cash runway projections, cap table → feeds the board deck financial review |
| **Before** | `legal-advisor` | Term sheet review, charter documents, compliance framework → provides legal underpinning for board actions |
| **This** | `board-manager` | Board meeting cadence, committee structure, fiduciary compliance, governance policies, shareholder communications |
| **After** | `investor-relations` | Consumes board governance framework to manage investor communications, fundraising cadence, and shareholder reporting |
| **After** | `ceo-strategist` | Consumes governance framework for CEO-level decision-making, board relationship management, and strategic planning |

Common chains:
- **Board meeting prep**: `fp-and-a-analyst` → `board-manager` → `investor-relations` — Financial data → board deck → investor update memo
- **Fundraising governance**: `ceo-strategist` → `legal-advisor` → `board-manager` — Raise strategy → term sheet → board seat negotiation and composition
- **Crisis response**: `ceo-strategist` → `board-manager` → `legal-advisor` — Crisis identification → board convening → legal strategy and investigation

```bash
# Example: Produce a board-ready financial package
# 1. Run FP&A model to generate financial statements
# 2. Use board-manager to structure the board deck around those financials
# 3. Feed the deck into investor-relations for monthly update formatting
```

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo
Founder-run board with informal meetings, no outside directors. Focus: legal compliance, basic minutes. Skip: board committees, formal evaluations, D&O insurance (though recommended).

### Small Team
Board with 1-2 outside investors, quarterly meetings, basic governance docs. Focus: strategic guidance, CEO accountability. Coordination: with legal counsel on board resolutions, with founders on pre-read quality.

### Medium Team
Board with independent directors, 2-3 committees (audit, comp, governance), formal evaluation. Focus: independent oversight, committee charters. Coordination: with audit committee chair on financial oversight, with comp committee on executive compensation.

### Enterprise
Fully independent board, all committees active, shareholder engagement, ISS/Glass Lewis engagement. Focus: public company governance, regulatory compliance. Coordination: with IR on shareholder outreach, with legal on SEC filings and proxy statements.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | First outside investor joins board; VC funding round |
| Small → Medium | >$10M revenue; >50 employees; regulatory scrutiny |
| Medium → Enterprise | IPO preparation; listing on public exchange |

## What Good Looks Like

A board meeting where strategic discussion consumes >50% of time. Directors arrive having read the pre-reads — the first question isn't "What's our burn rate?" but "What assumptions did you make in the hiring plan, and what would cause them to break?" Minutes are filed within 5 business days. Every director completed their D&O questionnaire. The board evaluation showed 4.2+/5 effectiveness. The CEO knows exactly which director to call for an intro to a key hire candidate. The lead independent director has the emergency succession plan in their desk drawer — literally and digitally.

## References
<!-- QUICK: 30s — links to deeper reading -->

- `references/committee-charters.md` — Sample charters for audit, compensation, and nominating/governance committees
- `references/do-questionnaire-template.md` — Annual D&O questionnaire template with common disclosure categories
- `references/board-evaluation-template.md` — Board self-assessment and peer evaluation forms
- `references/minutes-template.md` — Board and committee minutes template with do's and don'ts
- `assets/board-deck-template.pptx` — 12-slide board deck template with placeholder slides and speaker notes
- `assets/board-calendar-template.xlsx` — Annual board and committee calendar with meeting dates, deadlines, and deliverables
- `assets/independent-director-interview-guide.md` — Interview questions and evaluation rubric for board candidates
- Related skills: `ceo-strategist`, `investor-relations`, `legal-advisor`, `fp-and-a-analyst`
- Books: Startup Boards (Feld & Ramsinghani), The Board Book (Bowen), Corporate Governance (Larcker & Tayan)
- Governance resources: NASDAQ Listing Rules (5600 series), NYSE Listed Company Manual (Section 303A), Delaware General Corporation Law
