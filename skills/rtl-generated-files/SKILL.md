---
name: rtl-generated-files
description: Produce files with Hebrew or other right-to-left content that open correctly — Word (.docx), PDF, Excel (.xlsx), CSV, charts and images made with code. Covers the RTL switches in each format and the silent failures (reversed Hebrew in charts and PDFs, mojibake CSVs in Excel, substituted fonts). Use whenever you generate a document, spreadsheet, chart or image containing Hebrew with code or a file tool.
---

# RTL in generated files

Apply the rules in the rtl-basics skill. This skill covers files you produce with
code (for example Python in a sandbox). The library details below were checked on
2026-10-16 (openpyxl, python-docx, python-bidi); the rest is established practice
and is marked where unverified.

## The two silent failures

1. **Reversed Hebrew.** Drawing libraries that do not run the Unicode bidi
   algorithm place Hebrew characters left to right, so `שלום` comes out as `םולש`.
   This affects matplotlib and most image libraries, and the low-level PDF
   libraries such as reportlab and fpdf.
2. **Font substitution.** If the font lacks Hebrew, you get boxes, or a fallback
   font, with no error. Text extraction from the PDF still reads perfectly, so
   extracting text cannot catch it. Check the embedded fonts (`pdffonts file.pdf`)
   or render the page to an image and look at it.

## Word (.docx)

- Each RTL paragraph needs `<w:bidi/>` in its paragraph properties, and each RTL
  run needs `<w:rtl/>` in its run properties. Right alignment alone is not RTL.
- python-docx has no direct property for this. Add the elements yourself, as
  below. This produces `<w:pPr><w:bidi/></w:pPr>` and `<w:rPr><w:rtl/></w:rPr>`
  (verified):

  ```python
  from docx.oxml import OxmlElement
  p = doc.add_paragraph(); run = p.add_run("שלום עולם")
  p._p.get_or_add_pPr().insert(0, OxmlElement("w:bidi"))
  run._r.get_or_add_rPr().append(OxmlElement("w:rtl"))
  ```
  Insert `w:bidi` before any alignment (`w:jc`) element: Word expects a fixed
  element order in paragraph properties.
- Font: set a Hebrew-capable font on the runs, including the complex-script font
  slot (`w:rFonts w:cs="Arial"`). Word uses the `cs` font for Hebrew.

## PDF

- **Best route where a shell is available:** the `write-rtl-document` skill (Typst).
- **Otherwise:** write HTML with `dir="rtl"` on every block and convert
  it with a renderer that handles bidi text (a browser engine, or WeasyPrint). Or,
  where you have it, use Typst or LaTeX (XeLaTeX with polyglossia/bidi).
- With reportlab or fpdf, reorder each line yourself before drawing
  (`from bidi.algorithm import get_display`; `get_display("שלום 123")` returns the
  visual order, verified) and register a TTF font that contains Hebrew. Wrap the
  lines yourself too, and call `get_display` per line *after* wrapping, never on a
  whole paragraph before it.
- Verify: `pdffonts` shows the expected font embedded, and a rendered page image
  shows right-aligned text with the full stops on the left.

## Excel (.xlsx)

- RTL sheet: `ws.sheet_view.rightToLeft = True` (openpyxl, verified).
- Hebrew cells: `Alignment(horizontal="right", readingOrder=2)`, where 2 means
  right-to-left (openpyxl, verified).
- Store phone numbers and ID numbers as text so leading zeros survive.

## CSV

Write CSV as **UTF-8 with a BOM** (`encoding="utf-8-sig"` in Python). Without the
BOM, Excel on Windows opens Hebrew CSV as garbled characters. A CSV has no
direction; whoever opens it decides.

## Charts and images (matplotlib, PIL)

- Pass every Hebrew string (titles, axis labels, tick labels, legend entries,
  annotations) through `get_display` from python-bidi before drawing it.
- Use a font that has Hebrew. DejaVu Sans, usually present, does. Check that the
  font you set actually exists: matplotlib only warns about a missing font and
  carries on.
- Look at the image before handing it over. A reversed label is obvious to a
  Hebrew reader and invisible to a check that only reads the file.

## Markdown and plain text files

Markdown has no direction. A .md file renders according to the viewer: GitHub and
most editors guess per paragraph. If direction matters, make it HTML (`<div
dir="rtl">` blocks are allowed in most Markdown renderers) or a .docx instead.

## Arabic, Farsi and Urdu

Everything above applies, plus letter shaping: Arabic-script letters change form
by position. Bidi reordering alone is not enough for reportlab, fpdf or
matplotlib. Reshape first (`arabic-reshaper`), then call `get_display`. Hebrew
needs no shaping.
