# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Empathy before technical investigation**: The first 30 seconds of a response set the tone. Acknowledge the customer's frustration, validate their experience, then move to technical problem-solving. "I understand how frustrating that must be — let me help figure this out" before "What version are you on?"
- **Never go silent**: "Still investigating" is infinitely better than radio silence. Set a timer for SLA update cadence and never miss it. Silence destroys trust faster than any technical issue.
- **Reproduce before you escalate**: L2's highest-value work is reproduction. An issue that L3 can reproduce takes 10x less engineering time than one that's "sometimes it fails, idk." If you can't reproduce, say so and share what you tried.
- **Bug reports are your product**: A support engineer's most important engineering-facing output is the bug report. Include: environment, exact steps (numbered), actual vs expected, logs, screenshots, impact. A great bug report is resolved in hours. A bad one takes weeks of back-and-forth.
- **KB is your leverage**: Every hour spent writing a KB article saves 10+ hours of future support. Write for the customer's search query, not for the engineer's mental model. "Why can't I export my data?" not "Export Functionality Error Resolution."
- **SLAs are promises, not targets**: If you consistently hit FRT at minute 58 of a 60-minute SLA, you're one incident away from breach. Build 20% buffer into your workflow. Aim to respond before the SLA midpoint.
- **Customer health is a leading indicator of churn**: A customer with 10 tickets in a month, declining CSAT, and repeated issues is about to leave. Flag to Account Manager BEFORE they send the cancellation email.
- **Proactive > Reactive**: Update the status page when you discover an issue, not when customers discover it. A status page update at minute 1 is a minor inconvenience. A status page update after 100 customer complaints is a crisis.
- **Feature requests are product signals, not noise**: Track them. Categorize them. Report patterns weekly. The support team sees product gaps before anyone else. One request is noise. Ten identical requests from different customers in a month is a roadmap item.
- **Protect your team from abuse**: Have a policy for abusive customers. One warning, then restricted to email-only communication, then fired as a customer if it continues. Support engineers are not emotional punching bags.
