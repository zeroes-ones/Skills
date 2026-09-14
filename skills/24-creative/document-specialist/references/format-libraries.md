# Format Libraries

| Format | Primary library | Use for | Limits |
|---|---|---|---|
| `.docx` | `python-docx` | Create/edit paragraphs, styles, tables, headers | No tracked-change authoring; no field-code evaluation |
| `.docx` (templated) | `docxtpl` | Jinja placeholders over a real template | Inherits python-docx limits; template must be authored in Word |
| `.xlsx` | `openpyxl` | Cells, types, number formats, formulas, charts, named ranges | No recalculation — it writes formulas, does not evaluate them |
| `.xlsx` (data only) | `pandas` | Machine-to-machine dumps | Drops styling, formulas, and formats |
| `.pptx` | `python-pptx` | Slides, layouts, placeholders, notes, images | Cannot render; layout fidelity must be checked in PowerPoint |
| `.pdf` (generate) | `reportlab` | Precise programmatic layout | Verbose; you position everything |
| `.pdf` (generate from HTML) | `weasyprint` | HTML/CSS to PDF, good for reports | CSS subset; check pagination rules |
| `.pdf` (manipulate) | `pypdf` | Merge, split, rotate, watermark, forms, encrypt | Not a renderer; does not reflow |
| Office → PDF | LibreOffice headless | Converting an authored file | Lossy; always inspect |
| Scanned PDF | tesseract / OCRmyPDF | Text from images | Quality depends on DPI and language pack |

## Version caution

All of the above have had breaking releases. Pin the version, and mark any call you have not
verified against the installed version with `# VERIFY:`.

## Selection rule

Use the format's native library for anything a human will open and edit. Reserve `pandas` and
other data-only paths for machine-to-machine interchange.
