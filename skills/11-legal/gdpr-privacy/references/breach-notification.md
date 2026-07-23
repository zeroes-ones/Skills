# 7. Data Breach Notification

### 7.1 The 72-Hour Rule (Art. 33)

**When the clock starts:** Upon becoming *aware* of a personal data breach. Awareness means having a reasonable degree of certainty that a breach has occurred -- not necessarily knowing all details, but enough to conclude that personal data may have been compromised.

**What triggers awareness:**
- An alert from your monitoring system
- A report from a processor
- A third-party notification (security researcher, customer)
- Discovery during internal audit or investigation

**What does NOT start the clock:**
- An unconfirmed rumor
- A vague anomaly that could have non-breach explanations
- A suspicion that requires investigation -- but the investigation must happen *immediately*

**The 72-hour timeline is absolute:** 72 hours from awareness, not 3 business days. If the 72nd hour falls on a weekend or holiday, the deadline does not extend. If you miss the window, you can still notify, but must provide reasons for the delay (Art. 33(1)).

**Internal escalation workflow:**
1. **Detection (0-2 hours):** Anyone who detects a potential breach reports to the incident response team via a dedicated channel (Slack, PagerDuty, email to security@).
2. **Triage (0-4 hours):** Incident response team assesses: is personal data involved? What categories? How many data subjects? What is the nature of the breach (confidentiality, integrity, availability)?
3. **Containment (0-4 hours):** Isolate affected systems, revoke compromised credentials, take affected services offline if necessary, preserve logs and forensic evidence.
4. **Risk assessment (4-24 hours):** Determine the risk to individuals. See risk assessment framework below.
5. **DPA notification (0-72 hours):** If risk exists, notify the supervisory authority.
6. **Data subject notification (without undue delay):** If high risk, notify affected individuals.
7. **Post-incident (<30 days):** Root cause analysis, remediation, update DPIA and security measures, tabletop exercise to test improvements.

### 7.2 Breach Risk Assessment

| Risk Level | Criteria | Action |
|---|---|---|
| **Low** | Encrypted data, no potential for harm, data already publicly available | No notification to DPA or data subjects required. Document in internal breach log. |
| **Medium** | Some potential for inconvenience or limited harm (e.g., exposed email addresses only) | Notify DPA within 72 hours. Data subject notification not required. |
| **High** | Identity theft risk, financial loss, special categories exposed, large data set, data can be linked with other data to cause harm | Notify DPA within 72 hours AND notify data subjects without undue delay. |

**Factors that increase risk:** Special categories of data, financial data, credentials (especially if reused), children's data, data volume, data subjects could be identified from the breach, data can enable identity theft or fraud, data can cause reputational harm, discrimination, or loss of confidentiality.

**Factors that decrease risk:** Strong encryption with intact keys, data that is already public, data that cannot be linked to identifiable individuals.

### 7.3 DPA Notification Content (Art. 33(3))

The notification to the supervisory authority must include:

1. Nature of the breach: categories and approximate number of data subjects, categories and approximate number of records
2. DPO contact details or other contact point
3. Likely consequences of the breach
4. Measures taken or proposed to address the breach, including mitigation of adverse effects

If all information is not available, provide it in phases without undue further delay.

### 7.4 Data Subject Notification Content (Art. 34)

When the breach is likely to result in high risk to rights and freedoms, communicate to data subjects without undue delay. The communication must:

1. Describe the nature of the breach in clear and plain language
2. Provide the DPO contact details or other contact point
3. Describe the likely consequences
4. Describe measures taken or proposed to address the breach
5. Describe steps the data subject can take to protect themselves (change passwords, monitor accounts, contact credit bureaus)

**No notification required if:**
- The data was encrypted with strong encryption (and keys were not compromised)
- The controller has taken subsequent measures ensuring high risk is no longer likely
- Notification would involve disproportionate effort (in which case, use a public communication)

### 7.5 Internal Breach Log

Per Art. 33(5), every breach must be documented regardless of whether notification was made. The log must include:

- Date and time of detection
- Date and time of awareness (when 72-hour clock started)
- Description of the breach (what happened, how, what data, how many subjects)
- Risk assessment outcome (low/medium/high) and justification
- Whether DPA was notified and when
- Whether data subjects were notified and when
- Containment and remediation measures
- Root cause
- Corrective actions to prevent recurrence
- Regulatory reference number (if assigned by DPA)

This log must be available for inspection by the supervisory authority.

### 7.6 Tabletop Exercise Format

Conduct at least annually. Format:

1. **Scenario injection:** Present a realistic breach scenario (e.g., S3 bucket misconfigured exposing 50,000 customer records; phishing attack on HR with employee data exfiltrated; rogue employee downloading customer database)
2. **Timed response:** Participants work through the escalation workflow against the clock. Facilitator tracks times.
3. **Decision points:** Force participants to make decisions: Is this notifiable? Who needs to be involved? What do we tell customers? Do we involve law enforcement?
4. **Hot wash:** Debrief immediately after. What worked? What did not? Where were the delays?
5. **After-action report:** Document findings, assign action items, set deadlines. Feed into updated incident response plan.


---
