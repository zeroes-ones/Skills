# Widget Architecture — Composition, Const, Rebuild Scopes, Theming

## Composition Over Inheritance

- Build small focused widgets: `ProductCard`, `PriceTag`, `RatingStars` — not a 300-line `ProductScreen` with everything inline.
- Pass immutable data down via constructors; use providers/blocs only where multiple branches need shared state.
- Extract reusable pieces into the design system (see theming below).

## The Rebuild Model (What Actually Happens)

1. `setState`/provider change marks the widget dirty.
2. Flutter rebuilds that widget and re-runs its `build()`.
3. Children that are **const** or whose constructor args are identical do **not** rebuild (widgets are immutable; identical widget instances short-circuit).

So: **const is the single highest-leverage performance tool in Flutter UI.** A const child never rebuilds.

## Rules

- `const` everywhere possible (constructors, styles, paddings).
- Keep `build()` pure: no IO, no heavy computation, no provider mutation.
- Narrow rebuild scope: watch specific providers, not whole objects.
- `RepaintBoundary` around expensive paints (maps, images, gradients).

## Theming

- `ThemeData` (light/dark) + `ThemeExtension` for brand tokens (colors, spacing, typography).
- Material 3 (`useMaterial3`) with `ColorScheme.fromSeed`; Cupertino widgets for iOS-idiomatic parts where desired.
- Never hardcode colors/spacing in widgets — tokenize in the theme.
- Text: define a type-scale; use `Theme.of(context).textTheme` (or a `ThemeExtension`).

## Accessibility (Semantics)

- Interactive elements get labels (`Semantics(label:)` or tooltips).
- Images that convey meaning get semantic labels; decorative ones are excluded.
- Test with `flutter test` semantics and the Accessibility scanner on device.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Giant build method | Split into small widgets; extract const subtrees |
| No const anywhere | Add const; use `const` constructors and `static const` styles |
| Whole-object provider watch | Watch narrow selectors/providers |
| Hardcoded colors/spacing | Theme tokens |
| Unlabeled interactive icons | Semantics labels |
