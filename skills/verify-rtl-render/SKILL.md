---
name: verify-rtl-render
description: Check that an RTL PDF actually rendered correctly — right font embedded, no silent substitution, direction sane — before it is sent to anyone. Use after generating any Hebrew PDF and before any send. Triggers on "check this Hebrew PDF", "did the font work", "is this letter rendered right".
---

# Verify a Hebrew render before it goes out

**Every failure mode in this toolchain is silent.** Run this rather than trusting
that the command succeeded.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/verify_render.py letter.pdf --expect-font DavidLibre
```

Add `--json` for machine-readable output. Exit status is 0 only when no problems
were found.

## What it catches, and why each matters

| Signal that lies | What actually happens |
| --- | --- |
| Typst exit code | Emits `warning: unknown font family` and **compiles anyway**, substituting a Latin serif. Exit 0, PDF produced, Hebrew in the wrong face. |
| WeasyPrint exit code | Ignores `unicode-bidi: plaintext` with a warning; LTR paragraphs render inside an RTL document. |
| `pdftotext` output | Reports **logical** order with embedding marks. A correct RTL render looks broken; a substituted-font render extracts perfectly. |
| `fc-match` | Answers with its best substitute rather than failing when a font is absent. |

A substituted-font PDF still extracts every Hebrew codepoint correctly. Text
extraction cannot detect it. Only the embedded font list can.

## What it cannot check

**Text direction.** There is no reliable way to read paragraph direction back out
of a PDF. The script says so rather than pretending otherwise. Finish the job by
looking:

```bash
pdftoppm -png -r 100 -f 1 -l 1 letter.pdf /tmp/page   # then read /tmp/page-1.png
```

Confirm Hebrew is right-aligned, any Latin paragraph is left-aligned, and
`Name <address>` pairs and numbers are intact. Report what you saw, not that the
command exited cleanly.
