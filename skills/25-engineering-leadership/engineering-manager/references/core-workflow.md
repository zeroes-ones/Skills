# Core Workflow — Full Implementation

<!-- STANDARD: 3min -->

### Phase 1: 1:1 Cadence — Your Most Important Meeting

1:1s are the foundation of your management practice. Every other responsibility — performance, growth, retention, culture — flows through the 1:1.

**Schedule:** Weekly for direct reports (30 min for junior/mid, 45-60 min for senior/staff who have fewer people touchpoints). Bi-weekly for skip-levels.

**Agenda belongs to the engineer.** Your agenda items come after theirs. A healthy 1:1 is 70% their topics, 30% yours. If you're doing 90% of the talking, the 1:1 is broken.

**Standard opening questions (rotate, don't repeat):**
- "What's top of mind this week?"
- "What's been the hardest part of your work lately?"
- "What's something you're proud of that I might not know about?"
- "Where do you feel stuck?"
- "How's your energy level?"

**Career conversations (every 4-6 weeks):**
Use a growth framework. Map each engineer to: (1) current level and performance, (2) next level and gaps, (3) timeline estimate, (4) specific projects or behaviors that will close the gaps. Reference your company's career ladder — if it doesn't exist, partner with people-ops to build one.

**What to avoid:**
- Don't turn 1:1s into status updates — use standup or async channels for that
- Don't fill silence — pauses produce the most honest answers
- Don't promise confidentiality on things you're obligated to escalate (harassment, safety, legal)

**Follow-up:** Send a brief written summary within 24 hours: key topics discussed, action items, commitments. This creates a searchable record you'll reference in performance reviews.

### Phase 2: Delivery Accountability

Your team ships. You're accountable for what ships, when, and at what quality. You don't write the code, but you create the conditions for reliable delivery.

**Sprint/cycle planning:**
- Attend planning but let the team estimate. Your role: clarify priorities, resolve ambiguity, negotiate scope with product
- When the team commits to 8 story points and product wants 14, you negotiate — start with data (last 3 sprints' velocity), not feelings
- Guard against overcommitment. A consistently overcommitted team burns out; a consistently undercommitted team loses credibility

**Unblocking:**
- The daily question: "What's the single biggest thing slowing the team down right now?"
- Dependencies on other teams? You own the escalation. Don't make your engineers chase down other teams' EMs — you call the other EM directly
- Ambiguous requirements? Schedule the SME meeting yourself and bring the clarity back to the team

**Stakeholder communication:**
- Weekly written status: what shipped, what's at risk, what's next, what help you need. Keep it to one page
- When a date will slip, communicate immediately: "We're tracking to miss the July 15 date. Here's why, here's our new estimate, here's what we're doing differently"
- Build trust by being boringly predictable. Stakeholders relax when they know bad news arrives early and good news is real

**Timeline negotiation:**
- Never negotiate on the spot. "Let me check with the team and get back to you by tomorrow"
- Present options, not ultimatums: "Option A ships faster with reduced scope. Option B takes 2 more weeks but includes everything. Which matters more for this release?"
- The engineering answer is not always "it takes as long as it takes" — understand the business context and make conscious trade-offs

### Phase 3: Performance Management

Performance management is a continuous loop, not an annual event. The annual review should contain zero surprises.

**Continuous feedback:**
- Praise publicly, critique privately. Specific praise ("the way you handled that outage postmortem set a new bar for the team") beats generic praise ("great job")
- Corrective feedback within 24 hours of observation. Use SBI: Situation, Behavior, Impact. "In yesterday's design review (S), you interrupted three people mid-sentence (B), which caused them to stop contributing (I)"
- Keep a running document for each direct report: notable wins, areas for growth, feedback you've given, commitments they've made. This is your single source of truth for reviews

**Review cycles (annual or semi-annual):**
- Self-review → Manager review → Peer feedback → Calibration → Delivery
- Write reviews based on evidence from your running document, not memory
- Calibration: defend your ratings with specific artifacts. "Meets expectations because they shipped 3 features on time and mentored 2 interns" — not "they're a solid engineer"
- After delivery: schedule a 45-minute session, not a 15-minute drive-by. Send the written review 24 hours in advance so they can process before discussing

**Managing underperformers:**
- See "Decision Trees > Performance Issue Handling" for the full path
- Key principle: the underperformer who stays too long is your failure, not theirs. Every month you delay, the rest of the team absorbs the cost
- Partner with HR-manager from the first formal step. Don't go solo on PIPs

**Promotions:**
- Promotions recognize sustained performance at the next level, not one great project
- Build the promotion packet 3-6 months before you plan to submit. Signal gaps early
- A denied promotion with a clear path to next time builds trust. A surprise denial destroys it

### Phase 4: Team Building

**Hiring (partner with recruiting for execution):**
- You own the bar, recruiting owns the pipeline. Write the JD with outcomes, not requirements (see recruiting skill)
- Every interviewer on your panel must be calibrated. Run a norming session quarterly: review the same candidate packet together and align on scoring
- Interview debriefs: read all feedback before the group discussion. Anchor on evidence, not gut feel. "Culture fit" is a dangerous phrase — replace with "demonstrates our values through specific behaviors"
- Closing: the offer letter gets a signature, but *you* get the candidate excited. Paint a vivid picture of their first 6 months. Connect their work to business impact

**Onboarding (first 90 days):**
- Day 1: laptop, access, buddy assignment, team lunch
- Week 1: ship something small to production. A README fix counts. Momentum matters
- Week 2-4: pair with different team members. Build relationships, not just skills
- Day 30: first structured check-in. "What's different from what you expected? What's confusing? What do you need?"
- Day 60: first 360-light. Collect feedback from 3-4 peers. Surface issues before they solidify
- Day 90: formal review. Go/no-go decision. If they're not ramping, escalate immediately

**Team culture and psychological safety:**
- Psychological safety means: team members believe they won't be punished or humiliated for speaking up with ideas, questions, concerns, or mistakes. It's not about being nice — it's about being safe to be honest
- You model it first. Admit your mistakes openly. Ask "what am I missing?" and mean it
- Watch for signs of low safety: people are quiet in meetings but vocal in 1:1s, retrospectives are "everything is fine," mistakes get hidden
- Celebrate learning from failure, not just success. "That outage taught us X — here's how we're hardening the system" should be a valued contribution

**Team charter:**
- Every team should have a written charter: mission, scope, stakeholders, working agreements, definition of done
- Revisit quarterly. Teams evolve, charters should too
- Working agreements: meeting norms, communication channels, code review expectations, on-call responsibilities — written, explicit, agreed

**Retention:**
- Retention is proactive, not reactive. By the time someone has an outside offer, you've already lost (even if they stay)
- Know what motivates each person: title, compensation, autonomy, mastery, purpose, flexibility. Their answer changes over time — ask regularly
- The top reason engineers leave: they stop growing. Growth conversations aren't annual — they're woven into 1:1s
