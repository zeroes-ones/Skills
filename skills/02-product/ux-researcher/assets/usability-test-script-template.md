---
author: Sandeep Kumar Penchala
type: asset-template
domain: ux-research
version: "1.0"
last_updated: 2026-07-21
---

# Usability Test Script Template

A moderator's guide for conducting moderated usability testing sessions. Estimated session duration: 45–60 minutes. Adapt sections based on test objectives and session length.

---

## Session Metadata

| Field | Value |
|-------|-------|
| **Study Name** | [Study Title] |
| **Date** | [YYYY-MM-DD] |
| **Participant ID** | [P##] |
| **Session #** | [# of N] |
| **Moderator** | [Name] |
| **Note-taker / Observer** | [Name] |
| **Testing method** | Moderated in-person / Moderated remote / Unmoderated |
| **Platform** | [Prototype URL] / [Staging URL] / [Production URL] |
| **Device/OS/Browser** | [e.g., MacBook Pro / macOS 14 / Chrome 120] |
| **Recording** | [Yes/No — Consent verified?] |

---

## Pre-Session Checklist

- [ ] Recording equipment tested (screen + audio + webcam if applicable)
- [ ] Prototype/staging environment loaded and functional
- [ ] Test accounts created (if needed) — do NOT use real user accounts
- [ ] Task scenarios printed or loaded on moderator's second screen
- [ ] Note-taking template open (split screen with participant's screen)
- [ ] Consent form ready (digital or paper)
- [ ] Incentive/gift card ready for participant
- [ ] Quiet environment — no interruptions expected
- [ ] Back-up plan if prototype crashes (screenshots, paper prototypes, skip tasks)

---

## 1. Introduction (5 minutes)

### Welcome
> "Hi [Participant Name], thank you so much for taking the time to speak with us today. I'm [Name], and this is [Note-taker Name], who will be taking notes during our session."

### Purpose
> "We're working on [product/feature description] and we'd like to get your feedback to help us make it better. I want to emphasize: **we're testing the product, not you.** There are no wrong answers. If something is confusing or difficult, that's valuable information for us — it means we have work to do."

### What to Expect
> "Over the next [45–60] minutes, I'll ask you to complete a few tasks using [the product/prototype]. As you work through each task, I'll ask you to think out loud — just say whatever comes to mind as you look at each screen. What you're noticing, what you're trying to do, what's confusing, what makes sense."

### Think-Aloud Demonstration
> "Let me show you what I mean by thinking out loud. [Demonstrate with a non-product example, e.g., navigating a weather website]. 'Okay, I see the search bar at the top, I'm going to type in 'Chicago.' Now I see the 5-day forecast. Hmm, I'm looking for the hourly breakdown — maybe I need to scroll down...'"

### Ground Rules
> - "Honesty is critical — you won't hurt our feelings. If something is annoying or confusing, please tell us."
> - "I may not answer all your questions directly during the tasks. I want to see how you'd figure things out on your own. I'll circle back at the end."
> - "You can stop at any time for any reason. There's no pressure to finish every task."
> - "Any questions before we begin?"

### Consent & Recording
> "As mentioned in the consent form, I'd like to record this session — your screen and audio. The recording will only be used internally by our team to improve the product. Is that still okay with you?"
- [ ] Participant confirms consent for recording
- [ ] **START RECORDING NOW**

---

## 2. Pre-Test Interview (5–8 minutes)

### Background
> "To start, can you tell me a little about yourself and your role?"

Probes:
- What does a typical day look like for you?
- How long have you been in this role?
- What are your main responsibilities?

### Current Workflow
> "Walk me through how you currently [perform target activity]."

Probes:
- What tools do you use?
- What's the hardest part of that process?
- How often do you do this?
- What happens right before you [perform target activity]? What happens right after?

### Expectations
> "When you hear '[product description or value prop],' what comes to mind? What would you expect a product like this to do?"

### Past Experiences
> "Have you tried any other tools for [target activity]? What worked? What didn't?"

---

## 3. Task Scenarios (25–35 minutes)

### Task Design Principles
- **Realistic**: Tasks should reflect actual user goals, not features
- **Specific**: Provide concrete data/context the participant needs
- **Not leading**: Don't use the product's terminology or describe the UI
- **Independent**: Tasks should be completable in any order (unless testing a sequential flow)

### Task Format
For each task:
1. Read the scenario aloud
2. Hand the participant a printed card with the scenario (or paste into chat for remote)
3. Let them work independently
4. Only intervene if they're completely stuck for 2+ minutes
5. After task completion (or abandonment), ask follow-up questions

---

#### Task 1: [Task Name — ~5 minutes]

**Scenario Card**:
> [Write as a realistic scenario. Example: "Imagine you're planning a team offsite and need to find a venue. You have a budget of $5,000 and 15 attendees. Find and review a venue that fits these requirements."]

**Success Criteria**:
- [ ] [Observable action 1]
- [ ] [Observable action 2]

**Moderator Notes**:
- Watch for: [specific areas of interest]
- Probe on: [specific UI elements or decisions]

**Post-Task Questions**:
> - "On a scale of 1–5, how easy was that task?" (1 = very difficult, 5 = very easy)
> - "What made it [easy/difficult]?"
> - "Was there anything that surprised you?"
> - "Did you notice [specific feature/element]? What did you think it would do?"

---

#### Task 2: [Task Name — ~5 minutes]

**Scenario Card**:
> [Scenario text]

**Success Criteria**:
- [ ] [Observable action 1]
- [ ] [Observable action 2]

**Moderator Notes**:
- Watch for: [specific areas of interest]
- Probe on: [specific UI elements or decisions]

**Post-Task Questions**:
> - "On a scale of 1–5, how easy was that task?"
> - "What would you have done differently if I weren't here?"
> - "Is this how you expected this to work?"

---

#### Task 3: [Task Name — ~5 minutes]

**Scenario Card**:
> [Scenario text]

**Success Criteria**:
- [ ] [Observable action 1]
- [ ] [Observable action 2]

**Post-Task Questions**:
> - "On a scale of 1–5, how easy was that task?"
> - "Did anything feel like it took too many steps?"

---

#### Task 4: [Task Name — ~5 minutes]

**Scenario Card**:
> [Scenario text — can be an error recovery or edge case scenario]

**Success Criteria**:
- [ ] [Observable action 1]

**Post-Task Questions**:
> - "What would you do next if this happened in real life?"

---

#### Task 5: [Task Name — ~5 minutes]

**Scenario Card**:
> [Scenario text]

**Success Criteria**:
- [ ] [Observable action 1]
- [ ] [Observable action 2]

**Post-Task Questions**:
> - "On a scale of 1–5, how easy was that task?"

---

*(Repeat task block for each scenario — target 4–8 tasks per session)*

---

## 4. Think-Aloud Prompts

Use these prompts throughout the session when the participant falls silent or needs encouragement.

### General Prompts
- "What are you looking at right now?"
- "What are you thinking?"
- "What do you expect to happen when you [click/interact with that]?"
- "What would you do next?"
- "Take your time — there's no rush."

### Clarification Prompts
- "Can you tell me more about that?"
- "What does that mean to you?"
- "Why did you decide to [action] instead of [alternative]?"

### Encouragement (avoid judgment words like "good" or "correct")
- "That's helpful feedback."
- "I see what you mean."
- "Keep going."
- "You're doing exactly what we need — just thinking out loud."

### When They're Stuck
- "What would you do if I weren't here?"
- "Is there anything else you might try?"
- "What information would help you decide what to do next?"

### When They Make an Error
- DO NOT correct them.
- DO NOT say "Actually, you should..."
- Instead: "Interesting. Can you tell me what you expected to happen?"
- Only intervene if the participant is completely blocked (2+ minutes of frustration).

---

## 5. Post-Task Overall Ratings (5 minutes)

### Single Ease Question (SEQ)
> "Overall, how difficult or easy was it to complete these tasks?"

| 1 — Very Difficult | 2 | 3 | 4 | 5 | 6 | 7 — Very Easy |
|---|---|---|---|---|---|---|

### Satisfaction
> "If you had to use this product every day for [target activity], how would you feel?"

- [ ] I would hate it
- [ ] I would tolerate it
- [ ] I would be neutral
- [ ] I would like it
- [ ] I would love it

### Expectation
> "How does this compare to what you expected before we started?"

- [ ] Much worse than expected
- [ ] Somewhat worse
- [ ] About what I expected
- [ ] Somewhat better
- [ ] Much better than expected

---

## 6. Post-Test Interview (5–10 minutes)

### Overall Impressions
> "What's the one thing you liked most about what you saw today?"
> "What's the one thing you'd change if you could?"

### Missing Features
> "Was there anything you expected to be able to do that you couldn't?"

### Trust & Credibility
> "How trustworthy did this product feel? What made it feel that way?"

### Comparison
> "How does this compare to [current solution / competitor]?"

### Value Proposition
> "If this product were available today, would you use it? Why or why not?"
> "What would it need to do for you to switch from your current solution?"

### Pricing Intuition
> "If this were a paid product, what do you think a fair price would be?"

### Final Word
> "Is there anything else you want to share that we haven't covered?"

---

## 7. Wrap-Up (2 minutes)

### Debrief
> "Here's what we were testing today: [brief explanation of research goals, if appropriate]. Do you have any questions about the session?"

### Compensation
> "As a thank you for your time, here's [incentive]. We really appreciate your help."

### Future Research
> "Would you be open to participating in future research sessions?"

- [ ] Yes — confirm contact details
- [ ] No

### Close
> "Thank you so much. Your feedback today will directly impact how we build this product. Have a great [morning/afternoon]."

- [ ] **STOP RECORDING**

---

## 8. Post-Session Debrief (for moderator & note-taker — within 30 min)

### Top 3 Positives
1. [Finding]
2. [Finding]
3. [Finding]

### Top 3 Issues (Severity 3+)
1. [Issue — severity — WCAG criterion if applicable]
2. [Issue — severity — WCAG criterion if applicable]
3. [Issue — severity — WCAG criterion if applicable]

### Theme Tags
Tag this session with themes for later affinity mapping:
- [ ] [Theme A]
- [ ] [Theme B]
- [ ] [Theme C]

### Surprises
> What did we learn that we didn't expect?

### Notes for Next Session
> Should we adjust the script? Add/remove tasks? Change probes?

---

## Observation Notes Template (for note-taker)

| Timestamp | Task | Observation | Participant Quote | Severity (1–4) |
|-----------|------|-------------|-------------------|----------------|
| [MM:SS] | [Task #] | [What happened] | "[Verbatim]" | [1–4] |
| | | | | |
| | | | | |

**Severity Scale**:
- **1 — Cosmetic**: Noticeable but doesn't affect task completion
- **2 — Minor**: Causes hesitation or minor inefficiency; task still completable
- **3 — Major**: Causes significant delay or error; task barely completed or requires workaround
- **4 — Catastrophic**: Task cannot be completed; user gives up or requires moderator intervention

---

## Consent Form Template

### Study Title
[Study Title]

### Purpose
We are conducting research to improve [product/feature]. This session will involve you interacting with [a prototype/website/app] while thinking aloud. We'll ask you to complete specific tasks and provide feedback.

### Duration
Approximately [45–60] minutes.

### Recording
With your permission, we will record your screen and audio. The recording will be used internally by our team and will not be shared publicly. You can request that recording stop at any time.

### Voluntary Participation
Your participation is entirely voluntary. You may stop at any time for any reason. You may skip any task or question.

### Confidentiality
Your responses will be kept confidential. Findings will be reported in aggregate or anonymized form. Your name will not be associated with any published results.

### Compensation
You will receive [incentive description] as a thank-you for your participation, regardless of whether you complete all tasks.

### Contact
If you have questions about this study, contact: [Researcher Name] at [email].

### Consent
- [ ] I have read and understood the information above.
- [ ] I consent to participate in this study.
- [ ] I consent to audio and screen recording.
- [ ] I understand I can withdraw at any time.

**Participant Name**: _______________
**Signature**: _______________
**Date**: _______________

**Moderator Name**: _______________
**Signature**: _______________

---

## Remote Session Setup

### Pre-session Email (send 24 hours before)

> **Subject**: Usability Test — [Date & Time] Confirmation
>
> Hi [Name],
>
> Thanks for agreeing to participate in our usability study. Here are the details:
>
> **Date**: [Date]
> **Time**: [Time] [Timezone]
> **Duration**: ~60 minutes
> **Video Call Link**: [Zoom/Google Meet/Teams link]
>
> **What you'll need**:
> - A computer (desktop/laptop preferred)
> - A quiet place where you can talk freely
> - A stable internet connection
> - [Any other requirements: webcam, specific browser, etc.]
>
> During the session, I'll ask you to share your screen while you try out a [product/prototype]. There's nothing to prepare in advance.
>
> If you need to reschedule, please let me know at least 2 hours before the session.
>
> Looking forward to speaking with you!
>
> Best,
> [Name]

### Remote Session Tech Checklist
- [ ] Video call link created and tested
- [ ] Backup link ready (different platform in case primary fails)
- [ ] Participant has tested screen sharing capability (ask at session start)
- [ ] Prototype link ready to paste into chat
- [ ] Recording setup tested (platform-native recording + local backup)
- [ ] Moderation plan: second screen OR tablet for notes (don't type loudly near mic)

---

## References

- _Don't Make Me Think_ by Steve Krug — usability testing methodology
- _Rocket Surgery Made Easy_ by Steve Krug — DIY usability testing guide
- _Handbook of Usability Testing_ (2nd Ed.) by Jeffrey Rubin & Dana Chisnell
- Single Ease Question (SEQ) — Sauro & Dumas, 2009
- Nielsen Norman Group — Usability Testing 101: https://www.nngroup.com/articles/usability-testing-101/
- MeasuringU — SUS and SEQ benchmarks: https://measuringu.com/
