# Verification Recipes

Reopen-and-assert is the only proof a document is correct. These are the shapes to reach for.

## docx

```python
from docx import Document
d = Document("out.docx")
paras = [p.text for p in d.paragraphs]
assert "Expected Heading" in paras, "heading missing"
assert len(d.tables) == EXPECTED_TABLES, f"tables: {len(d.tables)}"
```

## xlsx

```python
from openpyxl import load_workbook
wb = load_workbook("out.xlsx")
ws = wb["Sheet1"]
assert ws.max_row == EXPECTED_ROWS, f"rows: {ws.max_row} (expected {EXPECTED_ROWS})"
# types matter: a date must not be a string
val = ws["B2"].value
assert not isinstance(val, str), "date written as string"
```

## pptx

```python
from pptx import Presentation
p = Presentation("out.pptx")
assert len(p.slides) == EXPECTED_SLIDES, f"slides: {len(p.slides)}"
texts = " ".join(sh.text_frame.text for s in p.slides for sh in s.shapes if sh.has_text_frame)
assert "Expected Title" in texts
```

## pdf

```python
from pypdf import PdfReader
r = PdfReader("out.pdf")
assert len(r.pages) == EXPECTED_PAGES, f"pages: {len(r.pages)}"
text = "".join(pg.extract_text() for pg in r.pages)
assert "Expected Phrase" in text, "text not extractable — is it a scan?"
```

## Count reconciliation

For any transform, assert both sides:

```python
assert out_rows == src_rows, f"silent truncation: {src_rows} -> {out_rows}"
```

## Atomic write

```python
import os, tempfile
tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
build(tmp)
verify(tmp)          # reopen and assert BEFORE moving into place
os.replace(tmp, "final.docx")
```
