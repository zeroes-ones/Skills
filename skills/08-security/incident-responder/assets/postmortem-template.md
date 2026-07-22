# Postmortem Template

## Incident Summary

| Field | Value |
|-------|-------|
| **Incident ID** | INC-[NNNN] |
| **Date** | [YYYY-MM-DD] |
| **Duration** | [X hours Y minutes] |
| **Severity** | SEV1 / SEV2 / SEV3 |
| **Owner** | [Name] |
| **Status** | Draft / In Review / Complete |

## TL;DR

[2-3 sentences summarizing what happened, impact, and fix.]

---

## Timeline (UTC)

| Time | Event |
|------|-------|
| HH:MM | [What happened — observation, not interpretation] |
| HH:MM | [Alert fired: alert-name] |
| HH:MM | [Engineer paged: name] |
| HH:MM | [Investigation: what was checked] |
| HH:MM | [Mitigation applied: what was done] |
| HH:MM | [Service recovered] |
| HH:MM | [Monitoring confirmed stable] |

---

## Impact

- **User Impact:** [What did users experience? Error rates, latency, data loss?]
- **Revenue Impact:** [$X estimated]
- **Customers Affected:** [X customers / % of traffic]
- **Data Loss:** [Yes/No — describe scope]

---

## Root Cause

[The fundamental reason this happened — not the symptom, the cause.]

**5 Whys Analysis:**
1. Why did the incident occur? → [Answer]
2. Why did [answer 1]? → [Answer]
3. Why did [answer 2]? → [Answer]
4. Why did [answer 3]? → [Answer]
5. Why did [answer 4]? → [Root cause]

---

## Detection

- **How was this detected?** [Alert / User report / Proactive check]
- **Time to Detect:** [X minutes]
- **Could detection have been faster?** [Yes/No — how?]

---

## Resolution

- **Immediate fix:** [What stopped the bleeding?]
- **Permanent fix:** [What prevents recurrence?]
- **Migration/cleanup needed:** [Any data fixes, backfills, communications?]

---

## Action Items

| ID | Action | Owner | Priority | Due | Status |
|----|--------|-------|----------|-----|--------|
| AI-1 | [Preventative action] | [Name] | P0/P1/P2 | [Date] | Open |
| AI-2 | [Detection improvement] | [Name] | P0/P1/P2 | [Date] | Open |
| AI-3 | [Process improvement] | [Name] | P0/P1/P2 | [Date] | Open |

---

## Lessons Learned

### What Went Well
- [Thing that worked well during the incident]

### What Went Poorly
- [Thing that could have been better]

### Where We Got Lucky
- [Near-miss or fortunate coincidence]

---

## Appendix

- [Links to dashboards, logs, relevant PRs, runbooks]
