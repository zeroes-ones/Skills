# Workflow versus Agent

<!-- DEEP: 5+min -- predictability as the deciding axis, and the bounded-agent form -->

## The deciding axis

Not task difficulty. Not user expectation. **Predictability of the decomposition.**

```text
Can you write the steps down, in order, before seeing the input?
├── Yes → WORKFLOW. The path is code; the model does work inside each step.
└── No  → AGENT, and then only within a bounded action space.
```

A genuinely hard task with a predictable decomposition is a **workflow** — and the workflow is
strictly better, because it is cheaper, faster, debuggable at the step that failed, testable per step,
and safer (the set of actions is known in advance).

**The most common error in agent design is confusing hard with unpredictable.** It produces over-built
systems for difficult-but-structured work, and the resulting cost and debuggability penalty is paid
forever.

## The distinction the literature draws

Worth quoting precisely, because the vocabulary is often used loosely:

> "Workflows are systems where LLMs and tools are orchestrated through predefined code paths.
> Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool
> usage, maintaining control over how they accomplish tasks."
>
> *(Source: Anthropic, "Building Effective Agents".)*

The same source's guidance inverts the usual instinct:

> "add multi-step agentic systems only when simpler solutions fall short"
>
> and, on frameworks: they "can also make it tempting to add complexity when a simpler setup would
> suffice".

So the position this skill takes is not invented: **the simple path is the default, and the burden of
proof is on the complexity.**

## The four questions that settle it

```text
1. Are the steps knowable before seeing the input?
   ├── Yes → workflow. Stop here.
   └── No  → continue

2. Is the variation bounded and enumerable?
   ├── Yes → a workflow WITH ROUTING. Classify, then take a known branch.
   │         This is most "we need an agent" cases: the categories ARE knowable.
   └── No  → continue

3. Is the action space bounded (a known, allow-listed tool set)?
   ├── Yes → a BOUNDED AGENT: agency over WHICH tool, not over WHAT MAY BE DONE.
   └── No  → STOP. Escalate: that is a security decision, not an architecture one.

4. Is the outcome verifiable?
   ├── Yes → the agent can be evaluated; proceed.
   └── No  → an unverifiable agent cannot be trusted or gated.
             Add a verification step, or reconsider the design.
```

**Question 3 is the safety boundary.** Agency over routing inside a fixed tool set is a normal
engineering decision. Agency over what actions the system may take is a security posture, and it
belongs with `appsec-engineer`.

## The bounded-agent form

The safe shape of agency: the model chooses *among* permitted actions, and cannot invent new ones.

```text
Unbounded (refuse):
  "Here is the codebase and a shell. Fix the failing test."
  → the action space is everything the shell can do

Bounded (acceptable):
  "Here are 6 allow-listed tools: read_file, write_file, run_test,
   list_dir, search, request_review. Fix the failing test."
  → autonomy over which tool and in what order; nothing outside the list
```

| Property | Unbounded | Bounded |
|---|---|---|
| Action space | open | allow-listed |
| Auditability | must infer intent | every action is enumerable |
| Failure blast radius | unbounded | bounded by the tool set |
| Reviewability | hard | the tool list is reviewable |
| Security posture | a decision, not a default | an engineering choice |

**The rule:** if you cannot write the complete list of things the agent may do, you have not designed
the system yet.

## What a workflow buys, concretely

| Property | Workflow | Agent |
|---|---|---|
| Cost predictability | known: N steps × per-step cost | variable: depends on the plan |
| Latency | bounded by the step count | unbounded by design |
| Debuggability | which step failed is visible | the plan must be inspected |
| Testability | each step has a contract | the trajectory is the test |
| Failure containment | a step's failure is local | a bad plan fails late and expensively |
| Action safety | the steps ARE the action set | requires an explicit allow-list |
| On-call knowledge | the manifest is the map | the trajectory is the map |

Read the table with the ladder in mind: the workflow column is *not* strictly better — an unpredictable
task genuinely needs agency. The point is that the agency column's risks are real and must be bought
deliberately.

## The hybrid that is usually right

Most real systems are a workflow whose *steps* contain a model, and possibly one step with bounded
agency.

```text
[classify input]        ← model call, structured output
   ↓
[retrieve context]      ← deterministic
   ↓
[generate draft]        ← model call
   ↓
[verify against rules]  ← deterministic check, can fail and loop
   ↓
[agentic repair step]   ← bounded agency, allow-listed tools, only on verification failure
   ↓
[finalise]
```

This shape has the workflow's predictability for the common path and agency only where it is needed —
in the repair loop, behind a verification gate. It is usually the right answer for "the task is mostly
predictable, but the failure handling is not".

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "The agent decides" as a substitute for decomposition | it means nobody wrote the steps down yet |
| Agency over an open action space | a security decision made by accident |
| A workflow where the steps genuinely vary | the deterministic path is wrong for some inputs, and fails opaquely |
| An agent for a task with a fixed sequence | cost, latency and debuggability all worse for no gain |
| Routing when one chain with a conditional would do | N paths to maintain for a distinction that was not real |
| Trusting an unverifiable agent | cannot be gated, so cannot be shipped responsibly |

## Checklist

- [ ] The decomposition's predictability was assessed before choosing the form (R2)
- [ ] A workflow was chosen wherever the steps are knowable in advance
- [ ] Where variation is bounded, routing was considered before agency
- [ ] Agency, where granted, is bounded to an allow-listed tool set (Anti-Hallucination)
- [ ] The complete list of permitted actions can be written down
- [ ] The outcome is verifiable, or a verification step exists
- [ ] The chosen form's cost, latency and debuggability implications are recorded
