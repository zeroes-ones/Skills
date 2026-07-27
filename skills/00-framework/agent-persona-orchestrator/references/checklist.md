# Persona Orchestrator — Production Checklist

## Pre-Deployment

- [ ] All persona files validated against Persona Registry Schema
- [ ] Persona `allowed_tools` and `prohibited_tools` reviewed for conflicts
- [ ] `default_skills` for each persona resolve to existing SKILL.md files
- [ ] No circular persona dependencies (personas cannot invoke other personas)
- [ ] Parallel fan-out merge protocol tested with 2+ personas
- [ ] All persona system prompts reviewed for bias and hallucination risk
- [ ] Persona README updated with any new personas

## Deployment

- [ ] Persona files placed in `personas/` directory
- [ ] Agent configuration updated to reference persona layer
- [ ] Hooks configured to inject personas at session start
- [ ] Command wrappers updated with new persona routes

## Post-Deployment

- [ ] Persona invocation smoke test: invoke each persona on a known input
- [ ] Parallel fan-out test: run 2+ personas simultaneously, verify merge correctness
- [ ] Conflict resolution test: feed personas contradictory instructions, verify merge protocol
- [ ] Token budget test: verify persona system prompt fits within agent token limits
- [ ] Team training: document persona usage patterns for developers

## Monitoring

- [ ] Persona invocation metrics dashboard configured
- [ ] Error rate per persona tracked
- [ ] Token usage per persona invocation logged
- [ ] Merge conflict rate tracked for parallel fan-out patterns
