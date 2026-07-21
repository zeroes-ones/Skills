# PRD (Product Requirements Document) Template

## Executive Summary
**Product/Feature:** [Name]  
**Status:** Draft | In Review | Approved | In Development  
**Author:** [Name]  
**Date:** [YYYY-MM-DD]  
**Version:** [X.Y]

### Problem Statement
[1-2 sentences: What problem are we solving? For whom?]

### Solution Overview
[1-2 sentences: How does this solve the problem?]

### Success Metrics
- [Metric 1 — e.g., 30% reduction in onboarding time]
- [Metric 2 — e.g., $X monthly revenue impact]
- [Metric 3 — e.g., NPS increase from X to Y]

---

## 1. User Stories

### Epic 1: [Epic Name]
- As a [persona], I want to [action] so that [outcome].
- As a [persona], I want to [action] so that [outcome].

### Epic 2: [Epic Name]
...

---

## 2. User Flows

### Primary Flow: [Flow Name]
```
Entry Point
  │
  ├─ Decision point? ──Yes──→ Path A
  │
  └─ No → Path B
      │
      ▼
  Result
```

### Edge Cases
- [What happens when the user has no data?]
- [What happens with network failure?]
- [What happens at scale? (1000s of items)]
- [What about accessibility? (screen reader, keyboard)]

---

## 3. Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-01 | [Description] | P0/P1/P2 | Proposed |
| FR-02 | [Description] | P0/P1/P2 | Proposed |

**Priority definitions:**
- **P0**: Must have — cannot launch without
- **P1**: Should have — painful to launch without
- **P2**: Nice to have — can add post-launch

---

## 4. Non-Functional Requirements

### Performance
- Page load: < [X]ms (p95)
- API response: < [X]ms (p95)
- Concurrent users: [X]

### Security
- Authentication method: [JWT/OAuth/SAML]
- Authorization model: [RBAC/ABAC]
- Data classification: [Public/Internal/Confidential/Restricted]

### Availability
- Uptime target: [99.X%]
- RTO (Recovery Time Objective): [X hours]
- RPO (Recovery Point Objective): [X hours]

### Compliance
- [ ] GDPR compliant
- [ ] SOC 2 controls applicable
- [ ] PCI scope: in/out

---

## 5. Technical Design (Brief)

### Components Affected
- [Backend service, API endpoint, database table, UI component]

### Data Model Changes
```
[Brief description of new/modified entities]
```

### Integration Points
- [External services, APIs, third-party dependencies]

---

## 6. Success Metrics & Analytics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| [Metric] | [Current value] | [Target value] | [How measured] |

### Events to Track
- `event_name` — when user does [X], log [properties]

---

## 7. Timeline & Dependencies

| Phase | Deliverable | Owner | Due |
|-------|-------------|-------|-----|
| Design | Figma mockups | [Name] | [Date] |
| Backend | API endpoint | [Name] | [Date] |
| Frontend | UI implementation | [Name] | [Date] |
| QA | Test plan execution | [Name] | [Date] |

### Dependencies
- [Dependency 1 — must be completed before X]
- [Dependency 2 — blocks Y until resolved]

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Mitigation strategy] |

---

## 9. Open Questions

- [ ] [Question that needs resolution before development]
- [ ] [Question that can be resolved during development]

---

## 10. Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| Product Manager | | | |
| Engineering Lead | | | |
| Design Lead | | | |
| Security Review | | | |
