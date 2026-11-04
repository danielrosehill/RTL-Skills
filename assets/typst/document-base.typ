// General right-to-left document: report, memo, brief, guide, one-pager.
// For a formal letter use letter-he.typ instead.
//
// Compile with --font-path pointing at the plugin's assets/fonts. Without it
// Typst warns once, substitutes a font with no Hebrew and still exits 0.
//
// A user's own house style goes in <data dir>/typst/document-base.typ, which
// replaces this file when scripts/paths.sh stage-typst runs.

#let accent-default = rgb("#1f3a5f")
#let muted = rgb("#5a6270")

// Keep a Latin or multi-part run (phone, reference, URL) in one piece.
#let ltr-run(body) = text(dir: ltr, body)

#let rtl-doc(
  title: "",
  subtitle: none,
  author: none,
  date: none,
  lang: "he",
  font: "David Libre",
  accent: accent-default,
  footer-note: none,
  body,
) = {
  set document(title: title, author: if author == none { () } else { author })
  set text(font: font, lang: lang, dir: rtl, size: 12pt, fill: rgb("#1a1a2e"))
  set par(leading: 0.8em, spacing: 1.2em, justify: false)
  set page(
    paper: "a4",
    margin: (x: 2.4cm, top: 2.4cm, bottom: 2.2cm),
    footer: context {
      set text(size: 9pt, fill: muted)
      line(length: 100%, stroke: 0.4pt + muted.lighten(50%))
      v(-0.4em)
      grid(
        columns: (1fr, auto),
        if footer-note != none { footer-note } else { title },
        counter(page).display("1 / 1", both: true),
      )
    },
  )
  show heading: set text(fill: accent, weight: "bold")
  show heading.where(level: 1): set text(size: 16pt)
  show heading.where(level: 2): set text(size: 13.5pt)
  show heading: it => { v(0.7em, weak: true); it; v(0.3em, weak: true) }
  set table(stroke: 0.5pt + muted.lighten(40%), inset: 7pt)
  show table.cell.where(y: 0): set text(weight: "bold", fill: accent)

  block(width: 100%, below: 1.6em, {
    text(size: 23pt, weight: "bold", fill: accent, title)
    if subtitle != none { linebreak(); text(size: 13.5pt, fill: muted, subtitle) }
    let meta = (author, date).filter(x => x != none)
    if meta.len() > 0 {
      v(0.2em)
      text(size: 10.5pt, fill: muted, meta.join(" · "))
    }
    v(0.4em)
    line(length: 100%, stroke: 1.2pt + accent)
  })
  body
}
