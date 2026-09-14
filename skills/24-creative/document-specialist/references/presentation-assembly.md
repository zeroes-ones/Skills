# Presentation Assembly

A deck is a layout system with content poured into it, not a canvas of positioned boxes.

## Rules

1. **Use layouts and placeholders.** Content placed in placeholders survives a theme change;
   absolutely positioned text boxes do not.
2. **Never position content by coordinates in a template deck.** Coordinates are a one-off; layouts
   are a system.
3. **Set the theme once.** Fonts and colours belong to the theme, not to individual runs.
4. **Respect the slide master.** If the answer is "override the master", the template is wrong,
   not the content.
5. **Check text fit after assembly.** Overflow is invisible in the object model and obvious on screen.

## Failure modes of deck assembly

- **Absolute positioning.** The deck looks right until a theme change breaks every slide.
- **Per-run styling.** The brand changes and the code must be rewritten instead of the template.
- **No fit check.** Text overflows the placeholder and is discovered during the presentation.
- **Speaker notes lost.** Regenerating the deck silently drops the notes the presenter needs.
- **Alt text omitted.** Images have no description and the deck fails accessibility review.
