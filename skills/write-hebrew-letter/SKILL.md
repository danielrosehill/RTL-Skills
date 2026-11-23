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

## Legal-style letters (demand letters)

For a letter that may be exhibited later (demand for information or action, sent
registered, "מבלי לפגוע בכל זכות או טענה"), follow
`references/legal-correspondence-hebrew.md`:
- lettered sections, and **numbered paragraphs (סעיפים) running continuously** through the whole letter;
- הח"מ in the third person;
- cite statutes by **סעיף** and regulations by **תקנה**;
- a deadline counted from receipt, and the reservation-of-rights close;
- address to the registered office with the care-of line.

It also covers the Typst traps: restarting enum numbering, reversed ranges, an orphaned signature.

## Identity

`paths.sh stage-typst` brings in `<data dir>/typst/sender.typ` when there is one. If
the staged `sender.typ` still has placeholders, run `setup-rtl` rather than inventing
values. Never commit a filled-in `sender.typ`. If `<data dir>/notes.md` exists, read
it before adapting a template.

## Template vocabulary

The neutral names (`doc-head`, `details`, `subject-line`) are deliberate. Keep them,
and keep the bundled sample a request to a fictional company.

## Two templates

| Template | Use for |
|---|---|
| `letter-he.typ` | A letter to one addressee asking for something (complaint, request, FOI) |
| `statement-he.typ` | A signed personal statement for circulation ("my position as of this date"), addressed לכל מאן דבעי, with an annex in the same PDF |

Options on `formal-doc` and `signature` (all default off, so older letters render unchanged):

- `footer-title: true`: the footer shows the document title instead of phone and email.
- `confidential: s.confidential`: a bold handling line on every page ("פרטי וחסוי – מיועד
  לנמענים בלבד" / "Private and confidential – for the intended recipients only").
- `signature(dated: [...])`: a signed-on date and time under the signature.
- `s.annex` is the word for an annex heading ("נספח" / "Annex"). Put the annex after
  `#pagebreak()` in the same file so "page N of M" counts the whole bundle.

An English edition uses the same files with `lang: "en"`, `is-rtl: false` and
`strings.en`; the page furniture is identical.
