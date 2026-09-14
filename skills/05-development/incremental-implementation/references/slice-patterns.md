# Slice Patterns

A thin vertical slice is small, end-to-end, and independently shippable. These are the shapes that
work.

## The walking skeleton

The thinnest path that crosses every layer (UI → service → store) and runs. Not a prototype — every
later slice thickens it. If slice 1 does not cross every layer, the slicing is horizontal.

## Common slice shapes

| Shape | When | Example |
|---|---|---|
| Walking skeleton | Any new capability | Render one hard-coded item end-to-end |
| Read path first | Data features | Display before edit |
| Single record → many | List features | One item, then pagination |
| Happy path → errors | Risky integrations | Success, then timeout handling |
| Behind a flag | Anything user-visible | Ship dark, enable in stages |

## Sizing

A slice is right-sized when it can be implemented, tested, and committed in one sitting, and its
outcome is demonstrable.

## Failure modes of slicing

- **Horizontal slicing.** All models, then all services — nothing is demoable until the end and
  integration risk surfaces last.
- **Slice too large.** "Build the API" is a project, not a slice; it cannot be verified in one sitting.
- **Slice that cannot ship.** A slice depending on an unmerged sibling is not independently shippable.
- **Skeleton skipped.** Going straight to full features defers the integration proof to the end.
