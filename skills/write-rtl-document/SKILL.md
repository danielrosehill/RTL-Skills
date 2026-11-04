---
name: write-rtl-document
description: Generate a Hebrew or other RTL PDF with Typst, such as a report, memo, brief, guide or one-pager. Use for "make a PDF in Hebrew", "מסמך בעברית".
---

# Write an RTL document with Typst

For a formal letter use `write-hebrew-letter`. This is for everything else. Read
`rtl-basics` for the number and date rules.

## Build

```bash
W=<working-dir>
${CLAUDE_PLUGIN_ROOT}/scripts/paths.sh stage-typst "$W"
cd "$W"
# copy document-he.typ to <name>.typ and replace the content
typst compile --root . --font-path ${CLAUDE_PLUGIN_ROOT}/assets/fonts <name>.typ <name>.pdf
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/verify_render.py <name>.pdf --expect-font DavidLibre
pdftoppm -png -r 80 -f 1 -l 1 <name>.pdf /tmp/page   # then look at it
```

`--font-path` is not optional. Without it Typst warns, substitutes a font with no
Hebrew and exits 0. A passing `verify_render.py` still doesn't prove direction, so
always look at the page. See `verify-rtl-render`.

## Writing the content

- `rtl-doc.with(...)` takes `title`, `subtitle`, `author`, `date`, `lang`, `font`,
  `accent` and `footer-note`.
- Wrap Latin and multi-part runs (phone numbers, references, versions) in
  `#ltr-run[...]`.
- Tables mirror by themselves: the first column sits on the right. Write columns in
  reading order.
- Put an RLM (U+200F) before a number that opens a cell or line with a currency,
  such as `‏1,250 ₪`.

## Other scripts

David Libre covers Hebrew and Latin only. For Arabic, Farsi or Urdu, set `lang` and
`font` to a face with that coverage, add its folder to `--font-path`, and pass that
font to `--expect-font`. Note that `verify_render.py` counts Hebrew codepoints only,
so for these scripts check `pdffonts` and the page image yourself.

## House styles

A user style goes in `<data dir>/typst/document-base.typ` and replaces the built-in
when staged. It must keep the `rtl-doc` and `ltr-run` names. See
`references/user-data.md`.
