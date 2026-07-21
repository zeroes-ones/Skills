# UX Research — Orchestra Platform

**Skill:** ux-researcher
**Date:** Sprint 0 (Discovery)
**Input:** Product strategy, target persona definition

## Research Plan

**Objective:** Understand how platform engineering teams currently manage their service catalog, developer self-service, and infrastructure provisioning.

**Method:** 12 semi-structured interviews (45 min each), contextual inquiry with 3 teams

**Participants:**
- 5 Platform Engineering Leads (50-200 eng orgs)
- 4 Senior Developers who use internal platforms
- 3 VP/Director of Engineering evaluating IDP solutions

## Key Findings

### Pain Points (frequency in 12 interviews)

| Pain Point | Count | Severity |
|-----------|-------|----------|
| "Creating a new service takes 2-5 days of tickets and waiting" | 11/12 | Critical |
| "I don't know who owns which service" | 9/12 | High |
| "Our platform setup took 6+ months and needs 2 FTE to maintain" | 8/12 | High |
| "Developers bypass the platform because it's too slow" | 7/12 | High |
| "Template library is stale — platform team can't keep up" | 6/12 | Medium |

### Journey Map: "Platform Engineer Onboarding a New Service"

```
Current State (45 min - 5 days):
Developer opens Jira ticket → Platform engineer triages (1-4 hrs) →
Creates repo manually → Sets up CI pipeline → Configures monitoring →
Assigns permissions → Developer gets access (2-5 days total)

Pain points at each step:
• Jira ticket: No standard template, missing info, back-and-forth
• Repo creation: Manual, inconsistent naming, wrong defaults
• CI pipeline: Copy-paste from other repos, outdated patterns
• Monitoring: Forgotten 40% of the time, caught in first incident
• Permissions: RBAC errors, over-provisioned access

Desired State (15 min):
Developer opens Orchestra → Selects template → Fills 5 fields →
Submits → 15 minutes later: repo, CI, monitoring, and permissions ready
```

## Design Implications

1. **Speed is the #1 value prop.** Every second of friction in the template wizard costs adoption.
2. **Service ownership must be visible at a glance.** "Who owns X?" is the most-asked question.
3. **Platform teams want curation, not creation.** They want to approve templates and manage plugins — not build scaffolding from scratch.
4. **Shadow IT is real.** If Orchestra isn't faster than the workaround, developers will bypass it.

## What Good Looks Like

Research report with sample size (n=12), methodology (semi-structured interviews + contextual inquiry), and actionable design implications — not just raw findings. Persona details come from research data, not assumptions.
