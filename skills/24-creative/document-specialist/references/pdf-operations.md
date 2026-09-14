# PDF Operations

The PDF is an output format, not an editable document. Know which operation you need before
choosing a tool.

## Operation → tool

| Operation | Approach | Caution |
|---|---|---|
| Generate from code | reportlab (precise) or weasyprint (HTML/CSS) | Pagination rules differ from a word processor |
| Convert an Office file | headless LibreOffice | Lossy — inspect before shipping |
| Merge | pypdf `PdfWriter.append` | Reconcile page counts across all inputs |
| Split | pypdf per-range writer | Confirm no page is dropped in the range math |
| Rotate | pypdf page rotation | Check the reader honours rotation |
| Watermark | pypdf `merge_page` | Verify opacity and that text remains selectable |
| Fill forms | pypdf form fields | Confirm field names — they are not the visible labels |
| Encrypt | pypdf `encrypt` | Record the algorithm; weak RC4 is not acceptable |
| Extract text | pypdf `extract_text` | Scanned pages yield nothing — route to OCR |

## Failure modes of PDF work

- **Uninspected conversion.** Layout, fonts, and table borders drift silently; the defect reaches the customer.
- **Page-count mismatch after merge.** A source silently fails to append and nobody counts.
- **OCR noise shipped as content.** Text extraction returns gibberish and it is treated as real.
- **Form field name guessed from the label.** Filling the wrong field writes data where nobody will look.
- **Encryption algorithm unrecorded.** The file is locked and the method is unknown later.
