# Assumption Surfacing: Detecting Hidden Premises

## Linguistic Patterns That Signal Assumptions
- Absolute statements without evidence: "The database will handle it," "Users will understand," "The API never fails."
- Future-tense predictions as certainties: "Traffic will grow 10x," "We'll have 3 more engineers by then."
- Comparative claims without benchmarks: "Faster," "Better," "More scalable," "Easier to maintain."
- Universal quantifiers: "Everyone," "Always," "Never," "All users," "No one."

## The "Because Chain" Method
For any statement S, ask "Why?" If the answer is another statement S', ask "Why?" again. Continue until:
- Terminus reached: empirical evidence, physical constraint, regulatory requirement, or explicit axiom.
- Chain loops: "We do X because Y, we do Y because X" → circular reasoning detected.
- Chain breaks: "I don't know why" → assumption surfaced.

## Assumption-to-Branch Conversion
When an assumption is detected:
1. Name it: "ASSUMPTION-[id]: [statement]."
2. Ask: "What would we do differently if this were false?"
3. Add the contingency as a branch in the decision tree.
4. Document the validation plan: how and when will we verify this assumption?
