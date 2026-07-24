# Progressive Disclosure Patterns

## Level 1: Always Present (Core Context)
What the agent ALWAYS sees:
- Ground rules (all negative constraints)
- Critical gotchas (top 3 by cost impact)
- Route the Request (for correct skill selection)
- Anti-Rationalization (hard behavioral boundaries)

## Level 2: On-Demand (Domain Triggered)
Loaded when agent encounters relevant domain keyword:
- Full decision trees (specific to task phase)
- Domain-specific gotchas
- Cross-skill coordination details
- Verification checklist (loaded at completion phase)

## Level 3: Referenced (Explicitly Requested)
Available but not auto-loaded:
- Complete reference files
- Example galleries
- Benchmark data
- Historical case studies

## Implementation Pattern
```yaml
progressive_disclosure:
  level_1: [ground_rules, critical_gotchas, route_request, anti_rationalization]
  level_2:
    trigger_keywords: ["architecture", "security", "database", "deploy"]
    load: [decision_trees, domain_gotchas, cross_skill, verification]
  level_3:
    references: true
    load_on_request: true
```
