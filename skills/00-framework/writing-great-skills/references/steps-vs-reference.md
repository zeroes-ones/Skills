# Steps vs Reference

## The Distinction

**Steps** are ordered actions with completion criteria. The model executes them in sequence.

**Reference** is information the model consults on-demand. The model looks up specific items.

## Steps Characteristics

- Ordered (1, 2, 3...)
- Each step has a completion criterion
- Procedural language: "Do X. Complete when Y."
- Exhaustive for the primary workflow
- Located in: Core Workflow, Decision Trees

## Reference Characteristics

- Unordered (the model looks up what it needs)
- Definitional language: "X is Y. Use when Z."
- Consulted on-demand, not executed in sequence
- Located in: Ground Rules, Gotchas, Verification, Proactive Triggers

## When to Use Each

| Material | Use Steps When... | Use Reference When... |
|----------|------------------|----------------------|
| Primary workflow | The model MUST follow this order | N/A — primary workflow IS steps |
| Rules/constraints | The rule applies at a specific point in the workflow | The rule applies globally, check anytime |
| Definitions | The definition is needed to complete a step | The model may need the definition for multiple steps |
| Examples | The example demonstrates a step | The example illustrates a concept |

## The Sediment Problem

Sediment is reference material that has migrated into steps. It happens when:
- An author adds a definition "just in case" the model needs it during a step
- Over successive edits, the definition grows
- The step now costs 2x tokens because half is sediment

Detection: grep for "is a", "refers to", "means", "defined as" in Core Workflow.

## Completion Criteria

Every step must answer: "How do I know I'm done?"

| Criterion Type | Example |
|----------------|---------|
| Checkmark | `- [ ] File created at path/X` |
| Expected output | `Complete when: curl returns 200` |
| Verification command | `Verify: npm test -- component-name` |
| Terminal condition | `Stop when: all 3 checks pass` |
