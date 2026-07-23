# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can fill out a postmortem template but your corrective actions are always "train the engineer" or "add more monitoring" | You've led 20+ SEV1 incidents as IC, and your postmortems have prevented entire classes of failures — not just the specific bug | Someone on a SEV1 call says "I calmed down when I heard your voice on the bridge" — and your organization's MTTR dropped 60% after you redesigned the incident response program |
| You need your runbook to respond to an incident — if the runbook is wrong or missing, you freeze | You can run an incident without a runbook because you understand the system architecture well enough to triage blind, and you're the one who updates the runbook after | You design the incident response program that scales across 50+ teams, and every team's SEV1 recovery time is under 15 minutes without you on the call |
| You've never run a blameless postmortem where the root cause was a process failure you designed | Your postmortems identify specific controls that would have prevented the incident, and you've personally implemented 10+ such controls that have never been triggered | A regulator reviews your incident response program during an enforcement action and cites it as a mitigating factor because your documentation demonstrated operational maturity beyond compliance requirements |

**The Litmus Test:** You're woken up at 3:00 AM by an alert you've never seen before. The runbook doesn't cover it. The on-call for the affected service isn't answering. Can you assess severity, assemble the right people, establish a comms cadence, and start containment within 10 minutes — without panicking? Masters have done this so many times that the first 10 minutes are muscle memory.
