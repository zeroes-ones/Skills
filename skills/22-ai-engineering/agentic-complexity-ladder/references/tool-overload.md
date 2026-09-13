# Tool Overload — when the tool menu is the complexity

> The tool set is part of the action space, and the action space is part of the rung's cost. A
> wider menu is not more capability if the model cannot select from it reliably (R7).

---

## The mechanism

Tool selection is a decision the model makes from the descriptions it is given. Two things degrade
it, and both get worse as the menu widens:

1. **Choice dilution.** Every added tool is another candidate the model must discriminate against.
   Selection accuracy falls as the count rises, even when each tool is individually well described —
   the failure is not that a tool is wrong, it is that the *decision between* tools gets harder.
2. **Near-duplicates.** Two tools with similar names or overlapping descriptions are worse than
   either alone: the model cannot tell which the task wants, so it picks unpredictably and the
   choice stops being a function of the input.

Neither failure is visible in the task's difficulty. A hard task with a coherent 8-tool set can be
handled reliably while an easy task with a 25-tool set and two `search` variants cannot. This is why
tool width must be *measured*, not assumed from the list's length.

## The signals

| Signal | What it means | Fix |
|--------|---------------|-----|
| Wrong tool chosen for a clear input | The menu is wider than selection supports | Narrow to the tools the task actually uses |
| Two tools chosen interchangeably for one class of input | Near-duplicate descriptions | Merge them, or disambiguate the descriptions so the difference is stated |
| Accuracy improves when a tool is removed | The removed tool was a distractor, not a capability | Keep it removed; record why |
| The same agent needs two disjoint tool families | The agent spans two jobs | Split it, or route in front (Rung 3) |
| A tool is present "just in case" | Speculative capability, the same failure as speculative complexity (R1) | Remove until a measured failure justifies it |

## The measurement

Tool-choice accuracy is checkable, so it should be checked rather than argued:

```
1. Build a labelled set: N real inputs, each with the tool a competent operator would choose.
2. Compute selection accuracy at the current tool count.
3. Remove or merge one tool; re-run.
   - Accuracy holds  → the tool was a distractor (or the case set does not cover it)
   - Accuracy falls  → the tool earns its place; restore it
4. Add a tool with a measured need; re-run.
   - Accuracy holds  → the addition was free
   - Accuracy falls  → the addition cost selection accuracy; narrow another tool to pay for it
```

The count is a heuristic, not a law: roughly 15 coherent, well-separated tools is where selection
commonly degrades, but the number that matters is the one measured on your case set. Record it as
`[VERIFIED]` with the case set named, or `[ESTIMATED]` with the assumption written down.

## Where this belongs on the ladder

Tool overload is a **rung cost**, and it is paid by Rung 5 (orchestrator–workers) and by any bounded
agent. It does not justify climbing a rung; it justifies *shaping* the rung you are on:

- **Narrowing** the set is the cheapest fix and needs no new rung.
- **Splitting the agent** so each holds a coherent subset is a new node — a real rung cost, so it
  needs a measured selection failure to justify it (R6).
- **Routing in front** (Rung 3) is the right shape when the input class determines which tool family
  is needed; the router's own accuracy then has to be measured too.

## What this is not

It is not an argument against tools, and not a claim that a specific count is universal. It is the
claim that **the tool set is a measured surface**, in the same way the topology and the state schema
are — and that widening it without measuring selection is the same error as climbing a rung without
measuring the failure it fixes.
