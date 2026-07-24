# Task Decomposition Guide

## When to Decompose
- Task estimated > 100K tokens total (exceeds single context window)
- Clear domain boundaries (different specializations needed)
- Parallelizable sub-tasks (40%+ latency reduction possible)
- Quality requires independent verification

## Decomposition Strategies

### By Domain
"Build a user auth system" →
- Security: OAuth2 flow design → security-reviewer
- Backend: JWT implementation → backend-developer
- Frontend: Login UI → frontend-developer
- Testing: Auth test suite → qa-engineer

### By Layer
"Design system architecture" →
- Data layer → database-designer
- API layer → api-designer
- Compute layer → system-architect
- Infrastructure layer → cloud-architect

### By Risk
"Deploy critical update" →
- Pre-deployment audit → security-reviewer
- Deployment execution → devops-engineer
- Post-deployment validation → qa-engineer

## Anti-Patterns
- **Micro-decomposition:** Split "write a function" → coordination > work
- **Forced parallelism:** Sequential dependencies → pipeline, not fan-out
- **Missing merge strategy:** 3 agents produce 3 outputs → what now?
