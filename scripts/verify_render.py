#!/usr/bin/env python3
"""Verify a Hebrew PDF actually rendered the way it was meant to.

Exists because every failure mode in this toolchain is silent:

- Typst emits ``warning: unknown font family: david libre`` and **compiles
  anyway**, substituting a Latin serif. Exit code 0, PDF produced, wrong font.
- WeasyPrint ignores ``unicode-bidi: plaintext`` with a warning and renders
  left-to-right paragraphs in an otherwise RTL document.
- ``pdftotext`` reports logical order with embedding marks, so a *correct* RTL
  render looks broken under it and a wrong one can look fine.

So none of exit status, stderr, or text extraction is a trustworthy signal.
This checks the artefact: which fonts are embedded, and whether the Hebrew
codepoints are covered by a font that actually has Hebrew.

Usage:
    verify_render.py letter.pdf [--expect-font DavidLibre] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata

HEBREW = re.compile(r"[֐-׿יִ-ﭏ]")

# Fonts that cover Latin but NOT Hebrew. Seeing one of these in a document that
# contains Hebrew is the signature of a silent substitution.
LATIN_ONLY_HINTS = (
    "libertinus", "libertine", "computermodern", "cmr", "latinmodern",
    "timesnewroman", "georgia", "garamond", "baskerville", "nimbusroman",
)


def _need(tool: str):
    if not shutil.which(tool):
        sys.exit(f"required tool not found: {tool} (install poppler-utils)")


def embedded_fonts(pdf: str) -> list[dict]:
    _need("pdffonts")
    out = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines()[2:]:
        parts = line.split()
        if len(parts) < 5:
            continue
        name = parts[0]
        # pdffonts prefixes subset fonts with a 6-letter tag and a '+'.
        if "+" in name:
            name = name.split("+", 1)[1]
        rows.append({"name": name, "embedded": "yes" in parts[-4:-1]})
    return rows


def pdf_text(pdf: str) -> str:
    _need("pdftotext")
    return subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout


def check(pdf: str, expect_font: str | None = None) -> dict:
    fonts = embedded_fonts(pdf)
    text = pdf_text(pdf)
    heb_chars = HEBREW.findall(text)
    names = [f["name"] for f in fonts]
    lower = " ".join(names).lower()

    problems, notes = [], []

    if not fonts:
        problems.append("no embedded fonts — the PDF may be image-only or empty")

    if heb_chars:
        latin_only = [h for h in LATIN_ONLY_HINTS if h in lower]
        has_hebrew_capable = any(
            k in lower for k in ("david", "hebrew", "noto", "dejavu", "frank", "rubik",
                                 "assistant", "heebo", "alef", "opensans", "arial", "liberation")
        )
        if latin_only and not has_hebrew_capable:
            problems.append(
                f"document contains Hebrew but the only embedded fonts look "
                f"Latin-only ({', '.join(names)}). This is the signature of a "
                f"silent Typst font substitution — check --font-path."
            )
        elif latin_only:
            notes.append(
                f"a Latin-only face is embedded alongside a Hebrew-capable one "
                f"({', '.join(names)}); confirm the Hebrew is not set in it"
            )
    else:
        notes.append("no Hebrew codepoints found in the extracted text")

    if expect_font:
        want = expect_font.replace(" ", "").lower()
        if want not in lower.replace(" ", ""):
            problems.append(
                f"expected font {expect_font!r} is not embedded; found: "
                f"{', '.join(names) or '(none)'}"
            )

    unembedded = [f["name"] for f in fonts if not f["embedded"]]
    if unembedded:
        problems.append(f"fonts not embedded, will not travel: {', '.join(unembedded)}")

    # Directional marks in extracted text mean bidi ran; their absence in a
    # Hebrew document is not proof of anything, so this is a note, not a check.
    if heb_chars and any(ord(c) in (0x202B, 0x202A, 0x2068) for c in text):
        notes.append("directional embedding marks present in extracted text — "
                     "normal, and NOT evidence of a broken render")

    return {
        "pdf": pdf,
        "fonts": fonts,
        "hebrew_chars": len(heb_chars),
        "problems": problems,
        "notes": notes,
        "verdict": "check the rendered image" if not problems else "problems found",
        "ok": not problems,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--expect-font", help="fail unless this font is embedded, e.g. DavidLibre")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    r = check(a.pdf, a.expect_font)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print(f"fonts: {', '.join(f['name'] for f in r['fonts']) or '(none)'}")
        print(f"hebrew codepoints: {r['hebrew_chars']}")
        for p in r["problems"]:
            print(f"  PROBLEM: {p}")
        for n in r["notes"]:
            print(f"  note:    {n}")
        if r["ok"]:
            print("\nNo automated problems found. This does not mean the render is "
                  "correct —\ntext direction cannot be verified from extracted text. "
                  "Render a page to PNG\nand look at it:\n"
                  f"  pdftoppm -png -r 100 -f 1 -l 1 {a.pdf} /tmp/page")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
