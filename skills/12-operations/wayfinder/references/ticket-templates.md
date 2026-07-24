# Ticket Templates

## BLOCKING Ticket Template

```markdown
# [ID]: [Unknown]

## Unknown
We don't know [specific unknown]. This blocks all implementation.

## Classification
- Type: BLOCKING
- Depends on: none

## Method
[How we'll investigate — be specific about tools, data sources, experiments]

## Artifact
- Type: [decision doc | benchmark | prototype | analysis]
- Path: tickets/artifacts/[filename]
- Contains: [description]

## Completion Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Status
- status: pending
- sessions_active: 0
```

## ORDERING Ticket Template

```markdown
# [ID]: [Unknown]

## Unknown
We don't know [specific unknown]. This must be resolved before [dependent ticket IDs].

## Classification
- Type: ORDERING
- Depends on: [ticket IDs]

## Method
[Investigation approach]

## Artifact
- Type: [type]
- Path: tickets/artifacts/[filename]

## Completion Criteria
- [ ] [Criteria]

## Status
- status: pending
- sessions_active: 0
```

## TECHNOLOGY EVALUATION Template

```markdown
# TECH-[ID]: [Technology] Evaluation for [Use Case]

## Unknown
We don't know if [technology] meets our requirements for [use case].

## Evaluation Criteria
| Criterion | Threshold | Weight |
|-----------|-----------|--------|
| Performance | p99 < Xms | High |
| Operational cost | < $X/month | Medium |
| Team familiarity | > 0 team members | Low |

## Method
1. [Benchmark step]
2. [Cost analysis step]
3. [Team survey step]

## Artifact
- Type: Decision document with comparison matrix
- Path: tickets/artifacts/[filename]

## Status
- status: pending
```

## SPIKE/PROTOTYPE Template

```markdown
# SPIKE-[ID]: [Prototype Goal]

## Unknown
We don't know if [approach] can [achieve goal] within [constraints].

## Hypothesis
We believe [approach] will [achieve goal] if [condition].

## Method
Build minimal prototype in `spike/[name]/` — NOT production code.

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## Artifact
- Type: Prototype code + README with findings
- Path: spike/[name]/

## Status
- status: pending
```
