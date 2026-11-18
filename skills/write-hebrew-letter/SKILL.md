---
name: write-hebrew-letter
description: Typeset a formal letter in Hebrew to PDF — RTL, David Libre, dual Hebrew/Gregorian dating, addressee and subject blocks. For complaints to a company or authority, קבילות, freedom-of-information requests, and any letter that needs to look official. Triggers on "write a formal Hebrew letter", "מכתב רשמי", "draft a complaint in Hebrew", "Hebrew letter PDF".
---

# Typeset a formal Hebrew letter

Sources are vendored at `${CLAUDE_PLUGIN_ROOT}/assets/typst/`, fonts at
`${CLAUDE_PLUGIN_ROOT}/assets/fonts/`.

## Build

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/paths.sh stage-typst <working-dir>
cd <working-dir>
# edit letter-he.typ: addressee, subject line, body, sign-off
typst compile --root . --font-path ${CLAUDE_PLUGIN_ROOT}/assets/fonts letter-he.typ letter.pdf
```

`--font-path` is **not optional**. Without it Typst warns once, substitutes a
Latin serif that has no Hebrew coverage, and compiles successfully. See
`references/fonts-and-rendering.md`.

### Handwritten signature (optional)

If the profile in `<data dir>/config.json` has `handwritten_signature`, copy the image for
the letter's language (`he`, or `he_full` for the full name) into the working directory
as `signature.png` and add `--input sig=signature.png` to the compile. The template puts
it above the signed name. Don't copy the image into a public repo, and don't commit the
built PDF if it carries an ID number.

Then always:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/verify_render.py letter.pdf --expect-font DavidLibre
```

## Register

Formality follows the **recipient, not the language**. Vendor and personal mail
is plain; banks, insurers, regulators, municipalities and government offices get
`לכבוד` in the addressee block, `בכבוד רב` in the sign-off, and any filing or
reference identifiers repeated in the sign-off. Details and stock phrasing in
`references/register-hebrew-letters.md`.

## Identity

`paths.sh stage-typst` brings in `<data dir>/typst/sender.typ` when there is one. If
the staged `sender.typ` still has placeholders, run `setup-rtl` rather than inventing
values. Never commit a filled-in `sender.typ`. If `<data dir>/notes.md` exists, read
it before adapting a template.

## Template vocabulary

The neutral names (`doc-head`, `details`, `subject-line`) are deliberate. Keep them,
and keep the bundled sample a request to a fictional company.
