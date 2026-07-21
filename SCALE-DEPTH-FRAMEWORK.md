# Scale Depth Framework

Every skill in this library provides depth at 4 scale levels. This framework defines the universal pattern.

## The Four Scales

| Scale | Team | Users | Revenue | Key Constraint |
|-------|------|-------|---------|---------------|
| **Solo** | 1 | 0-100 | $0 | Time & energy — one person does everything |
| **Small** | 2-10 | 100-10K | $0-1M | Coordination overhead begins, shipping speed critical |
| **Medium** | 10-50 | 10K-1M | $1M-20M | Specialization needed, processes form, compliance begins |
| **Enterprise** | 50+ | 1M+ | $20M+ | Governance, compliance, cross-team coordination dominate |

## What Every Skill Must Cover Per Scale

For each scale, answer:

### 1. What Changes?
- Tools, processes, depth of application
- What's overkill at this scale? What's missing?

### 2. What's the Minimum Viable?
- Bare minimum to be effective at this scale
- What can you skip without disaster?

### 3. Coordination Needs
- Who do you coordinate with at this scale?
- What communication cadence?

### 4. Cost Implications
- Tools cost at this scale
- Time investment from the team
- When does tooling pay for itself?

### 5. Transition Triggers
- What signals it's time to move to the next scale?
- What breaks if you stay at current scale too long?

## Anti-Patterns Per Scale

### Solo Anti-Patterns
- Over-engineering: microservices for a solo project
- Premature process: daily standups alone
- Perfectionism: spending weeks on a skill when hours would do

### Small Team Anti-Patterns
- Skipping CI/CD: "we're too small for automation"
- No code review: "we trust each other"
- Manual deploys: "it's just one command"
- No monitoring: "users will tell us"

### Medium Team Anti-Patterns
- Process for process sake: ceremonies without value
- Technology sprawl: every team picks their own stack
- Knowledge silos: only one person knows a system
- No architecture governance: every team invents their own patterns

### Enterprise Anti-Patterns
- Innovation paralysis: process kills experimentation
- Conway's Law ignored: org structure prevents needed architecture
- Technology lock-in: cannot evolve because "compliance said no"
- Overhead exceeding value: more managers than makers

## Token-Efficient Depth Pattern

When an agent invokes a skill, it should:
1. First read the scale-appropriate section (skip the rest)
2. Only go deeper into other scales when triggered
3. Use decision trees to navigate between scales quickly

This conserves tokens: an agent working on a solo project reads ~200 lines instead of all 800+.
