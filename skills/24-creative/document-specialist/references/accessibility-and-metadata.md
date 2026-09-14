# Accessibility and Metadata

A document that cannot be read by its audience, or that leaks data in its properties, is not
finished.

## Accessibility structure

| Element | Requirement |
|---|---|
| Headings | Real heading levels, not bold text |
| Tables | Header row marked as a header |
| Images | Alt text (or explicitly marked decorative) |
| Reading order | Logical in the object model, not only visually |
| Contrast | Meets the target standard |
| Language | Document language set |

## Metadata hygiene

- **Strip before external send.** Author names, file paths, comments, and tracked changes can leak.
- **Set deliberately:** title, author (if intended), and any classification.
- **Check inherited metadata.** Templated documents inherit the template's properties.

## Failure modes

- **Bold-as-heading.** Screen readers see no structure; a generated table of contents is empty.
- **Leaked tracked changes.** An internal negotiation ships with the contract.
- **Author metadata from the template.** The document claims the wrong origin.
- **Decorative images with no alt marking.** Readers announce noise as content.
- **Language unset.** Pronunciation and hyphenation are wrong for every reader using assistive tech.
