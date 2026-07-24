# Security Champions Program

## Program Design

### Champion Selection Criteria
- 1 champion per 10-15 developers (team-level coverage)
- Volunteers only -- assigned champions treat it as a chore
- Respected by peers -- champion recommendations carry weight
- Curious about security -- intrinsic motivation > forced participation
- NOT the team lead -- champion is a peer role, not a management role

### Recruitment Pitch
"Join the security champions program. You'll get: advanced security training (OWASP, threat modeling, secure code review), a $2,000/year conference budget, recognition as a security leader, skills that increase your market value by $30K-50K, and the ability to protect our users from real threats. One day per week dedicated to security activities, in your sprint capacity."

### Training Curriculum (8 weeks, 2 hours/week)

Week 1: OWASP Top 10 Deep Dive -- SQLi, XSS, broken auth, IDOR, SSRF -- with hands-on labs (OWASP Juice Shop)
Week 2: Advanced OWASP -- deserialization, XXE, prototype pollution, race conditions, business logic flaws
Week 3: Threat Modeling Workshop -- STRIDE on the champion's actual team services
Week 4: Secure Code Review -- Review actual PRs alongside a security engineer, learn the reviewer's triangle
Week 5: SAST and SCA Tools -- How to read Semgrep/CodeQL/Snyk output, distinguish true positives from false positives
Week 6: Mobile and API Security -- OWASP Mobile Top 10, API security (OWASP API Top 10), GraphQL security
Week 7: Incident Response Simulation -- Tabletop exercise: a critical vulnerability is exploited in production. What do you do?
Week 8: Certification and Graduation -- Final assessment, certificate of completion, champion badge

### Empowerment Model

Authority:
- Can add "security review required" label on any PR -- blocks merge until resolved
- Can request security engineer review with 4-hour SLA for critical findings
- Security champion review counts as a required reviewer for Tier 2 changes

Time Allocation:
- 20% of engineering time (1 day/week) allocated to security activities
- Time is in sprint capacity -- not "when you have free time"
- Protected from being pulled into feature work during security time

Recognition:
- Quarterly security champion lunch with CISO/VP Engineering
- Annual security offsite (1-2 day workshop, external trainer)
- Conference budget: $2,000/year for security conferences (BSides, OWASP Global AppSec, DEF CON)
- Career growth: security champion title on LinkedIn, internal visibility

## Measuring Impact

### Leading Indicators (monthly)
- Security-related PR comments from champions
- Threat models completed or reviewed
- Vulnerabilities caught in pre-production review
- Security training attendance and completion rates

### Lagging Indicators (quarterly)
- Vulnerabilities found in production: champion teams vs non-champion teams
- Mean time to fix security bugs: champion teams vs non-champion teams
- Security review bypass rate: PRs that should have had review but didn't

### Health Metrics (quarterly)
- Champion retention rate (target: >80% after 1 year)
- Champion satisfaction survey (NPS, open-ended feedback)
- Time to promotion for champions vs non-champions (is the program career-accelerating?)
