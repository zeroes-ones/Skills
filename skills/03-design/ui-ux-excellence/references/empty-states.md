# Empty States

<!-- STANDARD: 3min -- first-run, no-results, no-permission and error-adjacent empties -->

## The empty state is the first impression

The first-run experience of almost every product is an empty state. Users meet the surface before
it has any content, so the empty state *is* the onboarding — whether or not it was designed as
one. This is why R2 treats it as a gate rather than a nicety, and why "No data" is the most
expensive string in a product.

## The four kinds of empty

They look similar and must behave differently. Conflating them is the core empty-state defect.

| Kind | Situation | The user needs to know | Primary action |
|---|---|---|---|
| **First-run** | Nothing exists yet, by definition | What this surface is for | Create the first thing |
| **No results** | A query/filter returned nothing | What was searched and why it failed | Clear or broaden the search |
| **Nothing yet** | The feature is real but unused | That it is not broken, and how to start | Enable or set up the feature |
| **Cleared / completed** | There is deliberately nothing to do | That this is success | Celebrate, then offer the next thing |

The critical distinction is first-run vs. no-results: "No projects" and "No projects match
'quarterly'" are different messages with different remedies.

## The anatomy of a good empty state

```text
┌──────────────────────────────────┐
│   [ illustration of the thing ]  │  ← optional; shows what it will look like
│                                  │
│   No projects yet                │  ← the concrete noun the product uses
│   Projects hold your team's work.│  ← one line: what this surface is FOR
│                                  │
│   [ Create your first project ]  │  ← exactly one primary action
│   or import from a template      │  ← subordinate secondary path, if useful
└──────────────────────────────────┘
```

| Element | Required? | Notes |
|---|---|---|
| Concrete noun | Yes | Not "items", not "data" — the word the product's own UI uses |
| One line of purpose | Yes | What the surface is for, in the user's terms |
| One primary action | Yes | The single most likely next step |
| Illustration | Optional | Only if it communicates; decorative art wastes the space |
| Secondary path | Optional | Subordinate visually; a genuine alternative, not a competing primary |
| Sample/demo content | Sometimes | Useful when the surface is hard to imagine populated |

## Variant copy that works

| Kind | Headline | Body | Action |
|---|---|---|---|
| First-run (list) | "No projects yet" | "Projects hold your team's work." | "Create your first project" |
| First-run (search surface) | "Search your workspace" | "Find any document, or start something new." | "Search" |
| No results | "No results for 'quarterly report'" | "Try a shorter phrase, or clear the filters." | "Clear filters" |
| Nothing yet (feature) | "Notifications are off" | "Turn them on to hear about changes." | "Turn on notifications" |
| Permission | "You don't have access" | "Ask [owner] for access to this project." | "Request access" |
| Completed | "You're all caught up" | "Nothing needs your attention right now." | — |
| Filtered-to-empty | "No tasks match these filters" | "3 filters are applied." | "Clear filters" |

Note that each row names the *specific* condition. "No data" would serve all seven and help in
none.

## Rules

1. **Never present a normal condition as an error.** An empty list is not a failure. Error styling
   on a normal state teaches the user that the product is broken.
2. **Always offer a way out.** An empty state with no action is a dead end; the user is stuck and
   knows it.
3. **Echo the input for no-results states.** The user must see what produced the empty set.
4. **Distinguish filters from absence.** If filters are the cause, say how many are applied.
5. **Do not apologise.** "Sorry, nothing here!" adds nothing and implies fault.
6. **Keep the layout stable.** The empty state should occupy the space the content would, so
   nothing jumps when content arrives.
7. **Make it reachable deliberately.** Verify the empty state by using the product as a new user —
   it is invisible to anyone with data.

## Empty vs. zero vs. loading

A frequent confusion with real consequences:

| The user sees | It should mean | The defect |
|---|---|---|
| Empty state | The data loaded; there is legitimately none | — |
| Skeleton | Data is arriving | Skeleton shown when data is empty and final |
| Spinner | Work is happening | Spinner as the permanent state of an empty surface |
| Blank | Nothing — which is never correct | Blank stands in for all three |

The rule: **a blank region must never be reachable.** It is always one of loading, empty, error or
partial, and each has a designed state (Decision Tree 2).

## Empty states in tables and dense surfaces

| Situation | Treatment |
|---|---|
| Table with no rows | A single spanning row with the empty message and the action |
| Table with filters applied | The no-results variant, with the filter count and a clear action |
| Chart with no data | An empty axis frame with the message — not an absent chart |
| Dashboard with no widgets configured | An add-widget affordance, not an empty grid |
| Search with no query yet | Guidance and recent items — this is a first-run state |

## Testing the empty states

```text
1. New account, first visit          → is there a first-run state, and does it teach?
2. Search for a nonsense string      → is there a no-results state that echoes the query?
3. Apply filters that match nothing  → is the filter state distinguishable from absence?
4. Visit a feature you never enabled → is the "nothing yet" state honest about why?
5. Complete all work                 → is the completed state positive rather than blank?
6. Remove access as another user     → is the permission state a permission state?
7. Inspect every list and table      → is any region ever blank?
```

Seven steps. Each one is a state most products have never rendered on purpose.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "No data" | Names nothing; teaches nothing; helps nobody |
| Empty state with no action | A dead end with a friendly face |
| Error styling on a normal empty | Teaches the user the product is broken |
| Illustration with no message | Pretty and uninformative |
| No way to distinguish filtered from empty | The user cannot tell whether to clear filters |
| Apologetic copy | Implies fault and adds no information |
| Empty state that changes the layout | Content arrival causes a jump |
| Never testing as a new user | The state ships unrendered and broken |
