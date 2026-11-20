---
name: read-israeli-forms
description: Read scanned or photographed Israeli official documents (Tabu land-registry extracts, Form 106 and other Tax Authority forms, Bituach Leumi certificates) into checked structured data, with a Tabu-to-spreadsheet converter. Hosted vision model first, text layer before any OCR, no heavy local OCR. Use on "OCR this Hebrew form", "parse this Nesach Tabu into Excel", "read this scanned Form 106", "extract the data from this Bituach Leumi letter".
---

# Read Israeli forms

Turns an image or PDF of an Israeli government form into fields you can trust: transcribe,
then run deterministic checks on what was read. The reading step is a model's; the checks
are code.

## 1. Text layer first

Most documents gov.il issues are born-digital PDFs (Nesach Tabu, Form 106 from payroll
software, Bituach Leumi certificates from the personal area). Run `pdftotext -layout file.pdf -`.
If real Hebrew comes out, use it and skip OCR: OCR can only lose characters that are already
exact. Some PDFs yield visual (reversed) order; re-order before matching labels. A Nesach is
an original only in digital form, so ask for the PDF rather than re-scanning a printout.

## 2. Image-only pages: use a hosted model, not local OCR

Do not run Tesseract or OpenCV pipelines on a laptop. In order:

1. **Read the page yourself** if you can see images (`pdftoppm -r 200 -png` for PDF pages, one page per image). Fine for a handful of pages.
2. **A hosted vision or document-OCR API** for batches (a vision model through your model gateway, Google Document AI or Cloud Vision with language hint `iw`, Azure Document Intelligence with `he`). Pilot on 2-3 pages and compare against your own reading before a batch. AWS Textract does not support Hebrew.
3. **Tesseract (`heb+eng`, `--oem 1`, `--psm 4` for tables)** only as an offline fallback, one page at a time, never in a loop over hundreds of pages.

Ask the model for the raw text first (keep labels and digits verbatim, mark unreadable
characters `?`, do not guess), then structure it in a second step. Handwriting is unreliable
on every engine: flag handwritten sections for a human.

**Privacy.** These pages carry ID numbers, salaries and benefit data. Before sending pages to
a hosted service: say in one sentence what is going where, confirm the owner allows it, never
send Bituach Leumi medical or maternity letters without explicit consent, mask IDs you do not
need, and delete uploaded copies afterwards. Hosted engines may process outside Israel.

**The result is an unofficial transcription**, not the authority's record. Never present the
CSV as the Nesach itself and give no opinion on what an entry (caution, attachment, order)
means for a transaction.

## 3. Identify the form

Catalogue with identifiers, fields and layout notes: `references/israeli-form-types.md`.
Quick keys: "נסח טאבו" (Tabu), "טופס 106" / "אישור על משכורת וניכוי מס" (Form 106), "אישור ניכוי מס במקור", 806/857 (annual withholding certificate, not capital gains; that is 1399), "טופס 102" (employer report to Bituach Leumi), "המוסד לביטוח לאומי" header (certificates).

## 4. Extract fields

- **Tabu:** gush (גוש), helka (חלקה), tat-helka (mandatory for an apartment; not necessarily the apartment number), owners with share kept verbatim (`125/1000`, `בשלמות`, never a decimal), right type (בעלות, חכירה, חכירה לדורות). A Nesach repeats sections (owners, mortgages, cautions): one row each, not one field per label. Convert a whole extract:

  ```bash
  uv run python ${CLAUDE_PLUGIN_ROOT}/skills/read-israeli-forms/scripts/tabu_to_spreadsheet.py --file nesach.txt --out nesach.csv
  ```

  Stdlib only. UTF-8 with BOM so Excel shows Hebrew. Anything it cannot place goes to `section=unrecognized` and warnings go to stderr (owner shares not summing to the whole, section with no rows, failing ת.ז.). Read the warnings. Section-to-column mapping: `references/nesach-tabu-structure.md`.
- **Form 106:** tax year (שנת מס), withholding file number (מספר תיק ניכויים), employee ID, salary row (field 158/172, the total paid in the year, not "taxable income"), tax withheld (field 042). Amounts print next to the field code and OCR glues them (`04221,340`): split the code off before parsing; a row with an unreadable amount goes to human review, never a guess.

## 5. Validate before you report

- **ת.ז.:** 9 digits (8 if a leading zero was dropped, flag it) and the check digit; `valid_israeli_id()` in `scripts/tabu_to_spreadsheet.py`. A single misread digit usually fails it.
- Dates DD/MM/YYYY and plausible; amounts parse; gush/helka numeric.
- Owner shares sum to the whole.
- Numbers inside Hebrew lines can come back with digit groups shuffled even when every digit was right: re-anchor each number to its field label.
- Missing space between a Hebrew word and a digit (`טופס106`) is common: match labels with whitespace removed, no `\b` between Hebrew and digits.
- When matching labels, strip nikud (`[֑-ׇֽֿׁׂׅׄ]`, which keeps the maqaf) and fold final letters (ך ם ן ף ץ to כ מ נ פ צ) on the matching key only, never the stored value.
- Mixed Hebrew/Arabic forms: say so to the OCR engine, or Arabic gets read as Hebrew or skipped.
- Dot-matrix and old forms read worse than their confidence suggests.
- Report which values you read, which you checked, and which are low-confidence.

## Sources

Adapted from [hebrew-ocr-forms](https://github.com/skills-il/localization/tree/05e4947f777498e993241db5442b2f749c340249/hebrew-ocr-forms) by Skills IL (MIT). Kept: `tabu_to_spreadsheet.py`, the form-type and Nesach references. Dropped: the local Tesseract/OpenCV preprocessing and extraction scripts.
