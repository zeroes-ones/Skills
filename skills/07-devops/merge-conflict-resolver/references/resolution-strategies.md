# Resolution Strategies

Deep dive into each resolution strategy with examples, risk profiles, and when each is most appropriate.

## accept-ours
Keep our branch's version, discard theirs. Use when THEIRS is a refactor our feature already accounts for, or THEIRS changes were superseded. Risk: MEDIUM — verify no lost functionality.

## accept-theirs
Keep their branch's version, discard ours. Use when OURS is redundant (merged into THEIRS refactor) or THEIRS fixes a bug our feature depends on. Risk: MEDIUM — verify our feature intent preserved.

## manual-merge
Interleave both sides' changes into a single correct version. Use when both sides add independent value. Risk: HIGH — requires deep understanding of both intents and careful semantic validation.

## extract-to-shared
Create a new shared abstraction that both sides consume. Use when both sides introduce the same concept with incompatible implementations. Risk: HIGHEST — structural change affecting both branches.

## Default Strategy
When uncertainty exists, always default to manual-merge. Never default to accept-ours or accept-theirs without explicit justification.
