# Fonts and rendering for Hebrew documents

Verified 2026-09-01 on Ubuntu, Typst 0.14.2, WeasyPrint 68.1/69.0, poppler-utils.

## Every failure here is silent

| Tool | What you'd trust | What it actually does |
| --- | --- | --- |
| `typst compile` | exit code | Emits `warning: unknown font family: david libre` and **compiles anyway** with a Latin substitute. Exit 0. PDF produced. |
| `weasyprint` | exit code | Ignores `unicode-bidi: plaintext` with a warning; LTR paragraphs render inside an RTL document. |
| `pdftotext` | extracted text | Logical order with embedding marks. Correct renders look broken; substituted-font renders extract **perfectly**. |
| `fc-match "X"` | returns a font | Returns its best *substitute* when X is absent. Never errors. |

A font-substituted Hebrew PDF extracts all its Hebrew codepoints correctly, so
text-based checking cannot see the fault. Only the embedded font list can:

```bash
pdffonts letter.pdf     # or: scripts/verify_render.py letter.pdf --expect-font DavidLibre
```

## David Libre

Vendored at `assets/fonts/` (SIL OFL 1.1, licence alongside). Not in the Ubuntu
archive under that name — `apt-cache search "david libre"` finds nothing — which
is why it is vendored rather than declared as a system dependency.

Typst reaches it with `--font-path assets/fonts`. **Omitting that flag is the
single most common way to produce a wrong-font letter**, because it does not
fail.

## Font stacks

- **Typst letters** — David Libre. Serif, traditional, correct register for
  official Hebrew correspondence.
- **HTML email** — `Arial, 'Noto Sans Hebrew', sans-serif`. Web-safe first,
  because the recipient's client renders it, not you.
- **Email→PDF (eml_toolkit)** — `IBM Plex Sans Hebrew`, then `DejaVu Sans` for
  Arabic. Missing fonts render as tofu boxes rather than erroring; boxes mean a
  missing font, not a bidi fault.

## Verifying direction

Direction cannot be read back out of a PDF reliably. Render and look:

```bash
pdftoppm -png -r 100 -f 1 -l 1 letter.pdf /tmp/page
```

Check: Hebrew right-aligned, Latin paragraphs left-aligned, `Name <address>`
pairs intact, numbers not reordered.
